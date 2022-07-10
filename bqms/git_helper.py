from collections import namedtuple
from enum import Enum, auto
import os
import subprocess


class WorkingDirStatus(Enum):
    CLEAN = auto()
    UNSTAGED_CHANGES = auto()
    FILES_STAGED = auto()
    UNTRACKED_FILES = auto()
    NOT_CLEAN = auto()


class GitHelper:
    def __init__(self) -> None:
        pass

    def git_init(self, dir_path: str) -> bool:
        result = False

        git_command_list = ["git", "init"]
        git_result = self._run_git_command(dir_path, git_command_list)
        # TODO: check output, handle errors, get actual result from git_result
        result = True and bool(git_result)

        return result

    def git_add(self, dir_path: str, filename: str) -> bool:
        result = False

        git_command_list = ["git", "add", filename]
        git_result = self._run_git_command(dir_path, git_command_list)
        # TODO: check output, handle errors, get actual result from git_result
        result = True and bool(git_result)

        return result

    def git_commit(self, dir_path: str, commit_message: str) -> bool:
        result = False

        git_command_list = ["git", "commit", "-m", commit_message]
        git_result = self._run_git_command(dir_path, git_command_list)
        # TODO: check output, handle errors, get actual result from git_result
        result = True and bool(git_result)

        return result

    def git_create_branch(self, dir_path: str, branch_name: str) -> bool:
        result = False

        git_command_list = ["git", "checkout", "-b", branch_name]
        git_result = self._run_git_command(dir_path, git_command_list)
        # TODO: check output, handle errors, get actual result from git_result
        result = True and bool(git_result)

        return result

    def git_check_out_existing_branch(self, dir_path: str, branch_name: str) -> bool:
        result = False

        git_command_list = ["git", "checkout", branch_name]
        git_result = self._run_git_command(dir_path, git_command_list)
        # TODO: check output, handle errors, get actual result from git_result
        result = True and bool(git_result)

        return result

    def get_working_dir_status(self, dir_path: str) -> WorkingDirStatus:
        git_status = self._git_status(dir_path)

        # TODO: handle nonzero exit codes
        no_commits_yet = git_status.stdout.find(b"No commits yet") != -1
        untracked_files = git_status.stdout.find(b"Untracked files:") != -1
        staged_files = git_status.stdout.find(b"Changes to be committed:") != -1
        nothing_to_commit = (
            (git_status.stdout.find(b"nothing to commit") != -1)
            or (git_status.stdout.find(b"nothing added to commit") != -1)
            or (git_status.stdout.find(b"no changes added to commit") != -1)
        )
        changes_not_staged_for_commit = (
            git_status.stdout.find(b"Changes not staged for commit:") != -1
        )

        GitStatusFlags = namedtuple(
            "GitStatusFlags",
            "no_commits_yet untracked_files staged_files nothing_to_commit changes_not_staged_for_commit",  # noqa: E501
        )

        git_status_flags = GitStatusFlags(
            no_commits_yet,
            untracked_files,
            staged_files,
            nothing_to_commit,
            changes_not_staged_for_commit,
        )

        match git_status_flags:
            case GitStatusFlags(
                no_commits_yet=True,
                untracked_files=False,
                staged_files=False,
                nothing_to_commit=True,
                changes_not_staged_for_commit=False,
            ):
                return WorkingDirStatus.CLEAN
            case GitStatusFlags(
                no_commits_yet=True,
                untracked_files=True,
                staged_files=False,
                nothing_to_commit=True,
                changes_not_staged_for_commit=False,
            ):
                return WorkingDirStatus.UNTRACKED_FILES
            case GitStatusFlags(
                no_commits_yet=True,
                untracked_files=False,
                staged_files=True,
                nothing_to_commit=False,
                changes_not_staged_for_commit=False,
            ):
                return WorkingDirStatus.FILES_STAGED
            case GitStatusFlags(
                no_commits_yet=False,
                untracked_files=False,
                staged_files=False,
                nothing_to_commit=True,
                changes_not_staged_for_commit=False,
            ):
                return WorkingDirStatus.CLEAN
            case GitStatusFlags(
                no_commits_yet=False,
                untracked_files=False,
                staged_files=False,
                nothing_to_commit=True,
                changes_not_staged_for_commit=True,
            ):
                return WorkingDirStatus.UNSTAGED_CHANGES
            case GitStatusFlags(
                no_commits_yet=False,
                untracked_files=False,
                staged_files=True,
                nothing_to_commit=False,
                changes_not_staged_for_commit=False,
            ):
                return WorkingDirStatus.FILES_STAGED
            case _:
                raise Exception("Invalid working dir state encountered.")

    def _git_status(self, dir_path: str) -> subprocess.CompletedProcess:
        git_command_list = ["git", "status"]
        git_result = self._run_git_command(dir_path, git_command_list)
        return git_result

    def _run_git_command(
        self, dir_path: str, command_list: list[str]
    ) -> subprocess.CompletedProcess:
        original_working_dir = os.getcwd()

        try:
            os.chdir(dir_path)
            git_result = subprocess.run(command_list, capture_output=True)

        finally:
            os.chdir(original_working_dir)

        return git_result
