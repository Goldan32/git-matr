#!/usr/bin/env python3

import subprocess
import os
import argparse
from typing import List, Callable

def main():
    ls = []
    find_configs(ls, os.getcwd())
    ls.sort(key=lambda c: c.count('/'), reverse=True)
    args = parse_args()
    e = GitExecutor(ls)
    e.run(args)


def find_configs(configs: List, cwd: str):
    with os.scandir(cwd) as entries:
        for entry in entries:
            if entry.is_dir():
                find_configs(configs, f"{cwd}/{entry.name}")
            elif entry.name == ".gitmatr":
                configs.append(cwd)

def parse_args():
    parser = argparse.ArgumentParser(
        description="A simple git-like CLI with commit and push commands."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    commit_parser = subparsers.add_parser("commit", help='git add . && git commit -m for all repos')
    commit_parser.add_argument("-m", "--message", dest="message", required=True, help="Commit message")

    _ = subparsers.add_parser("push", help="Update remote refs along with associated objects")

    checkout_parser = subparsers.add_parser("checkout", help='git checkout')
    checkout_parser.add_argument("branch", help="Branch to checkout")

    _ = subparsers.add_parser("status", help='git status')

    _ = subparsers.add_parser("amend", help='git add . && git commit --amend --no-edit')

    pull_parser = subparsers.add_parser("pull", help='git pull')
    pull_parser.add_argument("-f", "--force", dest="force", action="store_true", help="git reset --hard origin/$(git bs)")

    return parser.parse_args()

class GitExecutor:
    def __init__(self, configs: List):
        self.configs = configs

    def _exec(self,
              params: List[List[str]], 
              pre: Callable[[dict], None] = lambda x: None,
              post: Callable[[dict], None] = lambda x: None,
        ):
        cb_args = {
            "dir": "",
        }
        commands = []
        for p in params:
            cmd = ["git"]
            cmd.extend(p)
            commands.append(cmd)
        for dir in self.configs:
            cb_args["dir"] = dir
            pre(cb_args)
            for c in commands:
                subprocess.run(c, cwd=dir)
            post(cb_args)

    def run(self, args):
        match args.command:
            case "commit":
                self.add_and_commit(args.message)
            case "push":
                self.push()
            case "checkout":
                self.checkout(args.branch)
            case "status":
                self.status()
            case "amend":
                self.amend()
            case "pull":
                self.pull(args.force)

    def add_and_commit(self, message):
        self._exec([["add", "."], ["commit", "-m", f"{message}"]])

    def push(self):
        self._exec([["push"]])

    def checkout(self, branch):
        self._exec([["checkout", f"{branch}"]])

    def status(self):
        def pre(x):
            print(f"{x["dir"]}:")
        def post(x):
            print("")
        self._exec([["status", "--short", "--branch"]], pre=pre, post=post)

    def amend(self):
        self._exec([["add", "."], ["commit", "--amend", "--no-edit"]])

    def pull(self, force):
        if force:
            self._exec([["reset", "--hard", "@{u}"]])
        else:
            self._exec([["pull"]])

if __name__ == "__main__":
    main()
