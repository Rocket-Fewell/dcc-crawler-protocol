#!/bin/sh
# Install the tracked pre-commit hook into this clone's .git/hooks (hooks are not part of a clone).
set -e
ROOT="$(git rev-parse --show-toplevel)"
cp "$ROOT/tools/hooks/pre-commit" "$ROOT/.git/hooks/pre-commit"
chmod +x "$ROOT/.git/hooks/pre-commit" "$ROOT/tools/check_repo_safe.py"
echo "pre-commit hook installed"
