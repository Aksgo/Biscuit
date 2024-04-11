from __future__ import annotations

import os
import re
import typing
from tkinter import messagebox

from ..floating.palette.actionset import ActionSet

git_available = True
try:
    import git

    from .repo import GitRepo
except ImportError:
    messagebox.showerror("Git not found", "Git is not installed on your PC. Install and add Git to the PATH to use Biscuit")
    git_available = False


if typing.TYPE_CHECKING:
    from biscuit import App

URL = re.compile(r'^(?:http)s?://')

class Git(git.Git):
    def __init__(self, master: App, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.base = master
        self.repo = None
        self.branches =  {}

        self.actionset = ActionSet(
            "Manage git branches", "branch:",
            self.branches,
            pinned=[["Create new branch: {}", lambda branch=None: self.repo.create_branch(branch)]],
        )
    
    def late_setup(self) -> None:
        self.base.palette.register_actionset(lambda: self.actionset)

    def check_git(self) -> None:
        if not (git_available and self.base.active_directory):
            self.base.git_found = False
            return

        try:
            self.repo = GitRepo(self, self.base.active_directory)
            self.base.git_found = True
            self.update_repo_info()
        except git.exc.InvalidGitRepositoryError:
            self.base.git_found = False

    def update_repo_info(self) -> None:
        self.branches = {}

        for branch in self.repo.branches:
            latest_commit = next(self.repo.iter_commits(branch))            
            self.branches[branch] = latest_commit.committed_datetime
        self.branches = sorted(self.branches.items(), key=lambda x: x[1], reverse=True)

        # TODO: make use of the commit_time in palette items
        self.actionset.update([(str(branch), lambda e=None, b=branch: self.repo.switch_to_branch(b)) for branch, commit_time in self.branches])

    def get_version(self) -> str:
        if not git_available:
            return

        return self.version()

    @property
    def active_branch(self) -> str:
        if not git_available:
            return 

        return self.repo.active_branch

    def checkout(self, branch: str) -> None:
        self.repo.index.checkout(branch)

    def clone(self, url: str, dir: str) -> str:    
        if not URL.match(url):
            # assumes github as repo host
            url = f'http://github.com/{url}'

        if name := self.repo_name(url):
            dir = os.path.join(dir, name)
            GitRepo.clone_from(url, dir)
            return dir

        raise Exception(f'The url `{url}` does not point to a git repo')

    def repo_name(self, url: str) -> None:
        match = re.search(r'/([^/]+?)(\.git)?$', url)
        if match:
            return match.group(1)
