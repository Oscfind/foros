# Virtual environment
py -3.11 -m venv .venv
'.\.venv\Scripts\Activate.ps1'
## 'Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser'

# Install dependencies
pip install --upgrade pip
pip install --requirement requirements.txt --requirement requirements-dev.txt

# Uninstall packages that aren't in requirements.txt
pip uninstall $(pip freeze) -y

# List outdated packages
pip list --outdated

# Git (local repository)
git config user.name "..."
git config user.email "..."

# Delete DevContainer Docker volumes
rm -r .devcontainer/.docker-volumes