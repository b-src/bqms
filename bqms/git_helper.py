import os
import subprocess


class GitHelper:
    def __init__(self) -> None:
        pass

    # TODO: turn working dir management into a decorator or something, will probably need that for all of these functions
    def git_init(self, dir_path: str) -> bool:
        original_working_dir = os.getcwd()
        result = False

        try:
            os.chdir(dir_path)
            git_result = subprocess.run(["git", "init"], capture_output=True)
            # TODO: check output, handle errors, get actual result from git_result
            result = True

        finally:
            os.chdir(original_working_dir)

        return result
