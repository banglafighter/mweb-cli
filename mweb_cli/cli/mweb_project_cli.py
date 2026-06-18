from mw_common import MWebCLIGroup, Console

project_cli = MWebCLIGroup(name="project", help_text="MWeb Project Management CLI")


@project_cli.command(name="setup",help="Setup MWeb Project")
def setup():
    Console.log("Setup")