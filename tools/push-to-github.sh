#!/usr/bin/env bash
# Commit this site and push it to a GitHub repo in the gravy-robot organization.
# Run from the site root:  bash tools/push-to-github.sh [repo-name] [--public]
# Defaults: repo "tcc-pilot-showcase", private. Requires git and the GitHub CLI (gh), signed in.
set -euo pipefail

ORG="gravy-robot"
REPO="${1:-tcc-pilot-showcase}"
VISIBILITY="--private"
[[ "${2:-}" == "--public" ]] && VISIBILITY="--public"

command -v git >/dev/null || { echo "git is not installed."; exit 1; }
command -v gh  >/dev/null || { echo "GitHub CLI (gh) is not installed: https://cli.github.com"; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "Run 'gh auth login' first."; exit 1; }

# Keep local clutter and the bundled kit zip out of the repo.
if [[ ! -f .gitignore ]]; then
  cat > .gitignore <<'IGNORE'
.DS_Store
*.zip
__pycache__/
.claude/
IGNORE
fi

if [[ ! -d .git ]]; then
  git init -b main
fi

git add -A
if git diff --cached --quiet; then
  echo "Nothing new to commit."
else
  git commit -m "Content Example prototypes: Stage, Canvas and requirements-only models"
fi

if git remote get-url origin >/dev/null 2>&1; then
  git push -u origin main
else
  echo "Creating ${ORG}/${REPO} (${VISIBILITY#--})..."
  gh repo create "${ORG}/${REPO}" ${VISIBILITY} --source . --remote origin --push \
    --description "TCC curated content pilot: hub, research maps, audit and Content Example prototypes"
fi

echo "Done: https://github.com/${ORG}/${REPO}"
