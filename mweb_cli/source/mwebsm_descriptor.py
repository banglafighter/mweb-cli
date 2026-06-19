from dataclasses import dataclass
from mw_common import SDLize


class MWebSMConst:
    ACTIVE = "active"
    INACTIVE = "inactive"


@dataclass(kw_only=True)
class GitRepository(SDLize):
    url: str
    dir: str = None
    branch: str = None
    script: list[str] = None


@dataclass(kw_only=True)
class SourceDirectory(SDLize):
    name: str
    script: list[str] = None


@dataclass(kw_only=True)
class Module(SDLize):
    status: str = MWebSMConst.ACTIVE
    script: list[str] = None
    sourceDir: list[SourceDirectory]


@dataclass(kw_only=True)
class Clone(SDLize):
    branch: str = None
    status: str = MWebSMConst.ACTIVE
    script: list[str] = None
    repo: list[GitRepository]


@dataclass(kw_only=True)
class Dependency(SDLize):
    name: str
    dir: str
    status: str = MWebSMConst.ACTIVE
    module: Module = None
    clone: Clone = None


@dataclass(kw_only=True)
class MwebSmDescriptor(SDLize):
    name: str
    startScript: list[str] = None
    endScript: list[str] = None
    dependencies: list[Dependency] = None
