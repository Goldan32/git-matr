#!/usr/bin/env python3

import subprocess
import os
import argparse
from typing import List

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

    return parser.parse_args()

class GitExecutor:
    def __init__(self, configs: List):
        self.configs = configs

    def _exec(self, params: List[List[str]]):
        commands = []
        for p in params:
            cmd = ["git"]
            cmd.extend(p)
            commands.append(cmd)
        for dir in self.configs:
            for c in commands:
                subprocess.run(c, cwd=dir)

    def run(self, args):
        match args.command:
            case "commit":
                self.add_and_commit(args.message)
            case "push":
                self.push()

    def add_and_commit(self, message):
        self._exec([["add", "."], ["commit", "-m", f"{message}"]])

    def push(self):
        self._exec([["push"]])


if __name__ == "__main__":
    main()
