from common.git_util import GitUtil
from mw_common import MwException, Console
from mw_file_content.file_content.mwfc_data_file_util import DataFileUtil
from .mwebsm_descriptor import MwebSmDescriptor, MWebSMConst, Module, Clone
from ..common.python_util import PythonUtil
from ..common.mweb_cli_const import MWebCLIConst
from ..common.shell_util import ShellUtil
from mw_file_content import FileUtil


class SourceManager:

    @classmethod
    def get_project_root(cls, directory: str | None = None) -> str:
        project_root = FileUtil.get_current_path()
        if directory:
            project_root = FileUtil.join_path(project_root, directory)
        return project_root

    @classmethod
    def create_virtual_env(cls, project_root: str):
        if not FileUtil.is_exist(FileUtil.join_path(project_root, MWebCLIConst.VENV_DIR_NAME)):
            ShellUtil.run(f"{PythonUtil.py_executable()} -m venv {MWebCLIConst.VENV_DIR_NAME}", home=project_root)

    @classmethod
    def get_descriptor_file_name(cls, environment: str | None = None):
        name = "mweb-sm"
        if environment:
            name = f"{name}-{environment}"
        return f"{name}.yml"

    def get_descriptor(self, project_root: str, environment: str | None = None) -> MwebSmDescriptor | None:
        descriptor_file_name = self.get_descriptor_file_name(environment)
        file_path = FileUtil.join_path(project_root, descriptor_file_name)
        if not FileUtil.is_exist(file_path):
            raise MwException(f"Descriptor file {descriptor_file_name} does not exist")
        descriptor_dict = DataFileUtil.read_yaml(file_path=file_path, exception_message="Unable to read descriptor file")
        if not descriptor_dict:
            raise MwException("Descriptor is empty")
        return MwebSmDescriptor.load_dict(descriptor_dict)

    @classmethod
    def install_setuptools(cls, project_root: str):
        command = f"python -m pip install setuptools"
        ShellUtil.run_in_venv(command=command, project_root=project_root, command_root=project_root)

    @classmethod
    def run_script(cls, scripts: list[str] | None, project_root: str, command_root: str, script_name: str | None = None):
        if not scripts:
            return

        if script_name:
            Console.info(script_name, system_log=True)

        for script in scripts:
            ShellUtil.run_in_venv(command=script, project_root=project_root, command_root=command_root)

    @classmethod
    def process_module(cls, project_root: str, dependency_dir: str, module: Module):
        if not module or (module.status and module.status != MWebSMConst.ACTIVE):
            return

        Console.yellow(f"Processing Module", system_log=True)
        for source_dir in module.sourceDir:
            command_root = FileUtil.join_path(project_root, dependency_dir, source_dir.name)
            scripts = module.script
            if source_dir.script:
                scripts = source_dir.script

            if not scripts:
                continue

            cls.run_script(
                script_name=f"Running script for {source_dir.name}",
                scripts=scripts,
                project_root=project_root,
                command_root=command_root
            )

    @classmethod
    def process_clone(cls, project_root: str, dependency_dir: str, clone: Clone):
        if not clone or (clone.status and clone.status != MWebSMConst.ACTIVE):
            return

        Console.yellow(f"Processing Clone", system_log=True)
        for repo in clone.repo:
            if not repo.url:
                continue

            dir_name = repo.dir
            if not dir_name:
                dir_name = GitUtil.get_repo_name(url=repo.url)

            branch = clone.branch
            if repo.branch:
                branch = repo.branch

            script = clone.script
            if repo.script:
                script = repo.script

            clone_path = FileUtil.join_path(project_root, dependency_dir)
            FileUtil.create_directories(path=clone_path)
            clone_repo_path = FileUtil.join_path(clone_path, dir_name)

            Console.info(f"Cloning Project : {repo.url}", system_log=True)
            Console.cyan(f"Cloning at : {clone_repo_path}", enable_staring=True, system_log=True)
            GitUtil.clone_or_pull_repo(repo_url=repo.url, branch=branch, clone_repo_path=clone_repo_path)

            if not FileUtil.is_exist(clone_repo_path) or not script:
                continue

            cls.run_script(
                script_name=f"Running script for {dir_name}",
                scripts=script,
                project_root=project_root,
                command_root=clone_repo_path
            )


    def install_or_update(self, environment: str | None = None, directory: str | None = None) -> None:
        project_root = self.get_project_root(directory=directory)
        self.create_virtual_env(project_root=project_root)
        self.install_setuptools(project_root=project_root)

        descriptor : MwebSmDescriptor | None = self.get_descriptor(project_root=project_root, environment=environment)
        if not descriptor:
            raise MwException(f"Descriptor is empty")

        Console.yellow(f"Project name : {descriptor.name}", system_log=True)
        self.run_script(
            script_name="Running start scripts",
            scripts=descriptor.startScript,
            command_root=project_root,
            project_root=project_root
        )

        if descriptor.dependencies:
            for dependency in descriptor.dependencies:
                if dependency.status and dependency.status != MWebSMConst.ACTIVE:
                    continue
                Console.yellow(f"Processing Dependency : {dependency.name}", system_log=True)

                if dependency.module:
                    self.process_module(project_root=project_root, dependency_dir=dependency.dir, module=dependency.module)

                if dependency.clone:
                    self.process_clone(project_root=project_root, dependency_dir=dependency.dir, clone=dependency.clone)


        self.run_script(
            script_name="Running end scripts",
            scripts=descriptor.endScript,
            command_root=project_root,
            project_root=project_root
        )