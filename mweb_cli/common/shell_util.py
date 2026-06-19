import os
import subprocess
import sys
from .mweb_cli_const import MWebCLIConst
from mw_file_content import FileUtil


class ShellUtil:

    @classmethod
    def run(cls, command, home: str, env=None):
        response = subprocess.run(command, shell=True, cwd=home, env=env)
        return response

    @classmethod
    def get_venv_activation_command(cls, project_root: str):
        bin_directory = "bin"
        command_prefix = "source "
        if sys.platform == "win32":
            bin_directory = "Scripts"
            command_prefix = ""

        activation_path = FileUtil.join_path(MWebCLIConst.VENV_DIR_NAME, bin_directory, "activate")
        if project_root:
            activation_path = FileUtil.join_path(project_root, activation_path)

        return f"{command_prefix}{activation_path}"

    @classmethod
    def run_in_venv(cls, command, project_root: str, command_root: str, env: dict | None = None):
        activation_command = cls.get_venv_activation_command(project_root)
        env = {**os.environ, **(env or {})}
        full_command = f"{activation_command} && {command}"
        return cls.run(command=full_command, home=command_root, env=env)
