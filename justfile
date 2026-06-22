#!/usr/bin/env -S just --justfile
# ^ A shebang isn't required, but allows a justfile to be executed
#   like a script, with `./justfile test`, for example.

install: && prepare
  uv sync

prepare: clean
  rm -f CONSIDERATIONS.md # Agentic section
  uv run python ./scripts/generate-schemas.py

clean:
  rm -rf output

generate:
  mkdir -p output
  uv run python ./scripts/join-properties.py
  rendercv render output/rendercv.yaml

watch:
  watchexec -W rendercv -e yaml -- just generate

pre-commit: clean generate
  uv run python ./scripts/pre-commit.py

git-add branch_name: pre-commit
  git checkout -B {{branch_name}}
  git add --force output
  git add rendercv
