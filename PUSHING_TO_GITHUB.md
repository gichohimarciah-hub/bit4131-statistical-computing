# Updating the GitHub repository

The first version is on GitHub. After making changes in this local project folder, add and commit them, then push:

```powershell
$repo = "C:\Users\hp\Documents\Codex\2026-11-27\i-x20\outputs\bit4131-statistical-computing"
git -c "safe.directory=$repo" -C $repo add .
git -c "safe.directory=$repo" -C $repo commit -m "Update project"
git -c "safe.directory=$repo" -C $repo push
```

The `safe.directory` setting is applied only to those commands because the project folder was created by a different Windows account. Do not add a password or personal access token to any project file.
