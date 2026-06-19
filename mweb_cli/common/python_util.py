import sys
from pathlib import Path
from mw_file_content import FileUtil
from .mweb_cli_const import MWebCLIConst


class PythonUtil:

    @classmethod
    def py_executable(cls):
        return sys.executable

    @classmethod
    def get_venv_python(cls, project_root: str):
        base = Path(project_root) / MWebCLIConst.VENV_DIR_NAME
        if sys.platform == "win32":
            return FileUtil.join_path(base, "Scripts", "python.exe")
        return FileUtil.join_path(base, "bin", "python")
