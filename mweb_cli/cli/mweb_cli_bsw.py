from mw_common import MWebCLIGroup, Console
from .mweb_project_cli import project_cli

Console.blue("----------------------------------------------", bold=True)
Console.green("      MWeb Command Line Interface (CLI)      ", bold=True)
Console.blue("----------------------------------------------", bold=True)


mweb_cli = MWebCLIGroup()
mweb_cli.add_command(project_cli)

def bsw():
    mweb_cli()


