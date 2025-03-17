#!/bin/bash
set -e

GITHUB_TOKEN=$(cat D:\\Workspace\\python-snippets-1\\git\\github_token)

# Check if we're inside a Git repository
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "This script must be run inside a Git repository."
  exit 1
fi

# Ensure the GITHUB_TOKEN is set.
if [ -z "$GITHUB_TOKEN" ]; then
  echo "Error: GITHUB_TOKEN environment variable is not set."
  exit 1
fi

# Configurable variables
OWNER="chandramgc"                         # Your GitHub username or organization
# List of repositories to process (modify as needed)
REPOS=(
  "food-saver"
)
BASE_BRANCH="feature-dev-devlopment-enviroment-dev"                       # Branch from which to create the new branch (target for the PR)
MERGE_BRANCH="feature-dev-devlopment-enviroment"                         # Branch to merge into the new branch

# Use current date/time for unique branch naming.
DATE=$(date +%Y%m%d%H%M%S)

# Loop through each repository in the list.
for REPO in "${REPOS[@]}"; do
  echo "=============================="
  echo "Processing repository: $REPO"
  
  REPO_URL="https://github.com/${OWNER}/${REPO}.git"

  # Clone the repository if it doesn't exist locally.
  if [ ! -d "${REPO}" ]; then
    echo "Cloning repository from ${REPO_URL}..."
    git clone "${REPO_URL}"
  fi

  # Change directory into the repository.
  cd "${REPO}" || { echo "Failed to enter directory ${REPO}"; exit 1; }

  # Fetch latest remote updates for all branches.
  echo "Fetching latest changes..."
  git fetch origin

  # Ensure the BASE_BRANCH is up-to-date.
  echo "Checking out ${BASE_BRANCH} branch..."
  git checkout ${BASE_BRANCH} || { echo "Failed to checkout ${BASE_BRANCH} in $REPO"; exit 1; }
  git pull origin ${BASE_BRANCH}

  # Create a new branch from BASE_BRANCH.
  # Append repository name to ensure branch name uniqueness across repos.
  NEW_BRANCH="${REPO}-update-${DATE}"
  echo "Creating new branch '${NEW_BRANCH}' from '${BASE_BRANCH}'..."
  git checkout -b ${NEW_BRANCH}

  # Merge MERGE_BRANCH into the new branch.
  echo "Merging '${MERGE_BRANCH}' into '${NEW_BRANCH}'..."
  if ! git merge origin/${MERGE_BRANCH} --no-edit; then
    echo "Merge conflicts detected in $REPO. Please resolve them manually."
    cd ..
    continue
  fi

  # Push the new branch to remote.
  echo "Pushing new branch '${NEW_BRANCH}' to remote..."
  git push origin ${NEW_BRANCH}

  # Create a Pull Request (PR) via GitHub API.
  echo "Creating pull request from '${NEW_BRANCH}' to '${BASE_BRANCH}'..."
  PR_TITLE="Merge ${MERGE_BRANCH} into ${BASE_BRANCH}"
  PR_BODY="Automated PR: Merging changes from ${MERGE_BRANCH} into ${BASE_BRANCH} via branch ${NEW_BRANCH}."
  PR_ENDPOINT="https://api.github.com/repos/${OWNER}/${REPO}/pulls"

  echo "------------------------------"

  RESPONSE=$(curl -s -X POST \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github+json" \
    -d "{\"title\": \"${PR_TITLE}\", \"body\": \"${PR_BODY}\", \"head\": \"${NEW_BRANCH}\", \"base\": \"${BASE_BRANCH}\"}" \
    "$PR_ENDPOINT")
  
  # Check if the response contains an "errors" field.
  if echo "$RESPONSE" | grep -q '"errors":'; then
    echo "Error creating PR for $REPO:"
    # If jq is available, format the errors nicely.
    if command -v jq >/dev/null; then
      echo "$RESPONSE" | jq '{errors: [.errors[] | {message: .message}]}'
    else
      # Fallback: use grep/awk to extract error messages.
      echo "$RESPONSE" | grep -o '"message": "[^"]*"' | awk 'NR>1'
    fi
  else    
    echo "Pull Request created for $REPO:"
    echo "$RESPONSE" | grep -o -m1 '"html_url": "[^"]*"'
  fi
  echo "------------------------------"

  # Return to the parent directory for the next repository.
  cd ..
done

echo "=============================="
echo "Processing complete."
