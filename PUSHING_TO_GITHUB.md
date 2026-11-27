# Pushing the project to GitHub

The local folder is prepared as a Git repository. No GitHub repository is currently connected to this task, so there is no remote to push to yet. Create an empty repository on GitHub (do not initialize it with a README, license, or .gitignore), then from this folder run:

```sh
git remote add origin https://github.com/OWNER/REPOSITORY.git
git add .
git commit -m "Add BIT 4131 statistical computing project"
git branch -M main
git push -u origin main
```

Replace `OWNER/REPOSITORY` with the real account and repository. GitHub CLI users may instead authenticate with `gh auth login` and push using their configured credential helper. Never put a password or personal access token in the repository or command history. Once pushed, add the repository URL to `PRESENTATION_OUTLINE.md` and share it during the presentation as requested in the brief.
