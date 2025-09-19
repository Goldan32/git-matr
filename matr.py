#!/usr/bin/env python3

import subprocess
import os
import argparse
from sys import argv
from typing import List

def main():
    ls = []
    find_configs(ls, os.getcwd())
    ls.sort(key=lambda c: c.count('/'), reverse=True)

def find_configs(configs: List, cwd: str):
    with os.scandir(cwd) as entries:
        for entry in entries:
            if entry.is_dir():
                find_configs(configs, f"{cwd}/{entry.name}")
            elif entry.name == ".gitmatr":
                configs.append(cwd)

def parse_args():
    def parse_args():
        parser = argparse.ArgumentParser(
            description="A simple git-like CLI with commit and push commands."
        )

        subparsers = parser.add_subparsers(dest="command", required=True)

        commit_parser = subparsers.add_parser("commit", help="Record changes to the repository")
        commit_parser.add_argument("-m", "--message", required=True, help="Commit message")

        push_parser = subparsers.add_parser("push", help="Update remote refs along with associated objects")

        return parser.parse_args()

class GitExecutor:
    def __init__(self, configs: List):
        self.configs = configs

    @staticmethod
    def _exec(args: List, dir: str):
        cmd = ["git"]
        cmd.extend(args)
        subprocess.run(cmd, cwd=dir)


if __name__ == "__main__":
    main()
