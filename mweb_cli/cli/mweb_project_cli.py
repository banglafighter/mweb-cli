from mw_common import MWebCLIGroup, Console
from ..source.mweb_source_manager import SourceManager

project_cli = MWebCLIGroup(name="project", help_text="MWeb Project Management CLI")


@project_cli.command(name="install",help="Install MWeb Project")
@project_cli.option("--environment", "-e", help="Enter project environment name", default=None, show_default=True, type=str)
def install(environment: str | None = None) -> None:
    Console.log(f"Install {environment}")
    try:
        SourceManager().install_or_update(environment=environment)
    except Exception as e:
        Console.error(e)