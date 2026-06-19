from git import Repo, GitCommandError
from mw_common import MwException, Console
from mw_file_content import FileUtil


class GitUtil:

    @classmethod
    def get_repo_name(cls, url: str, default=None):
        if not url:
            return default

        url = url.rstrip("/")
        if url.endswith(".git"):
            url = url[:-4]

        last_slash = max(url.rfind("/"), url.rfind(":"))

        if last_slash == -1 or last_slash == len(url) - 1:
            raise MwException(f"Invalid repository URL: {url}")

        return url[last_slash + 1:]

    @classmethod
    def clone_or_pull_repo(cls, repo_url: str, clone_repo_path: str, branch: str):
        try:
            repo_name = cls.get_repo_name(url=repo_url)
            if not repo_name:
                raise MwException("Invalid repo")

            if not FileUtil.is_exist(clone_repo_path):
                Console.success(f"Cloning project: {repo_name}, Branch: {branch}")
                Repo.clone_from(repo_url, branch=branch, to_path=clone_repo_path)
            else:
                Console.success(f"{repo_name} taking pull...")
                repo = Repo(clone_repo_path)
                origin = repo.remotes.origin

                origin.fetch()
                local_branch = repo.active_branch.name

                Console.info(f"Local branch: {local_branch}, Target branch: {branch}")

                if local_branch != branch:
                    if branch in repo.heads:
                        repo.git.checkout(branch)
                    else:
                        repo.git.checkout("-b", branch, f"origin/{branch}")

                origin.pull(branch)

        except GitCommandError as ex:
            Console.error(f"Git command failed: {ex}")

        except Exception as ex:
            Console.error(f"Unexpected error: {ex}")
