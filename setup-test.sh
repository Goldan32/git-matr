#!/usr/bin/env bash
set -euxo pipefail

PROOT="$(realpath $(dirname ${BASH_SOURCE[0]}))"
TEST_DIR="$PROOT/test"
CWD="$(pwd)"

# Cleanup first
rm -rf "$TEST_DIR"

# Recreate
mkdir -p "$TEST_DIR/a/b/c"

cd "$TEST_DIR/a/b/c"
echo "Start of C" > c.txt
echo '#.gitkeep' > .gitmatr
git init && git branch -m master && git add . && git commit -m "Init C"

cd "$TEST_DIR/a/b"
echo "Start of B" > b.txt
echo '#.gitkeep' > .gitmatr
git init && git branch -m master
git submodule add ./c
git add . && git commit -m "Init B"

cd "$TEST_DIR/a"
echo "Start of A" > a.txt
echo '#.gitkeep' > .gitmatr
git init && git branch -m master
git submodule add ./b
git add . && git commit -m "Init A"

cd "$CWD"
