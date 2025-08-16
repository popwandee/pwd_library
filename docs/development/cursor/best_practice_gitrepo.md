# Git Repository Best Practices

**แนวปฏิบัติที่ดีสำหรับการจัดการ Git Repository และ Workflow**

## 🗂️ **Repository Structure**

### **1. Multi-Repository Setup**

```
iot-projects/
├── aicamera.git/              # Edge Device Repository
│   ├── .git/
│   ├── src/
│   ├── config/
│   ├── tests/
│   ├── scripts/
│   ├── docs/
│   ├── requirements.txt
│   ├── .cursorrules
│   ├── .gitignore
│   ├── README.md
│   └── Dockerfile
│
├── lprserver_v3.git/          # Server Repository
│   ├── .git/
│   ├── app/
│   ├── migrations/
│   ├── tests/
│   ├── docker/
│   ├── scripts/
│   ├── docs/
│   ├── requirements.txt
│   ├── .cursorrules
│   ├── .gitignore
│   ├── README.md
│   └── docker-compose.yml
│
└── shared-tools/              # Shared Development Tools
    ├── templates/
    ├── scripts/
    ├── docs/
    └── config/
```

### **2. Git Configuration**

**Global Git Configuration:**
```bash
# Set up global Git configuration
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global core.editor "code --wait"
git config --global init.defaultBranch main

# Enable Git LFS for large files
git config --global lfs.https://github.com/username/repo.git/info/lfs.locksverify false

# Set up credential helper
git config --global credential.helper store
```

**Repository-Specific Configuration:**
```bash
# For aicamera.git
cd aicamera.git
git config user.name "AI Camera Developer"
git config user.email "aicamera@example.com"

# For lprserver_v3.git
cd lprserver_v3.git
git config user.name "LPR Server Developer"
git config user.email "lprserver@example.com"
```

## 🔄 **Git Workflow**

### **1. Branch Strategy**

```
main (production)
├── develop (integration)
│   ├── feature/edge-camera-integration
│   ├── feature/server-api-enhancement
│   └── hotfix/urgent-fix
└── release/v1.2.0
```

**Branch Naming Convention:**
```bash
# Feature branches
feature/edge-camera-integration
feature/server-api-enhancement
feature/mqtt-communication

# Bug fix branches
bugfix/memory-leak-fix
bugfix/connection-timeout

# Hotfix branches
hotfix/security-patch
hotfix/critical-bug

# Release branches
release/v1.2.0
release/v1.3.0
```

### **2. Commit Message Standards**

**Conventional Commits Format:**
```bash
# Format: <type>[optional scope]: <description>

# Examples:
feat(edge): add DHT22 sensor support
fix(server): resolve database connection timeout
docs(api): update API documentation
test(edge): add sensor integration tests
refactor(server): improve error handling
style(edge): format code with black
perf(server): optimize database queries
chore(deps): update dependencies
```

**Commit Message Template:**
```bash
# .gitmessage template
# Save as ~/.gitmessage
# git config --global commit.template ~/.gitmessage

# <type>[optional scope]: <description>
#
# [optional body]
#
# [optional footer(s)]
#
# Types:
#   feat: A new feature
#   fix: A bug fix
#   docs: Documentation only changes
#   style: Changes that do not affect the meaning of the code
#   refactor: A code change that neither fixes a bug nor adds a feature
#   perf: A code change that improves performance
#   test: Adding missing tests or correcting existing tests
#   chore: Changes to the build process or auxiliary tools
```

### **3. Development Workflow**

**Feature Development:**
```bash
# 1. Create feature branch
git checkout develop
git pull origin develop
git checkout -b feature/new-feature

# 2. Make changes and commit
git add .
git commit -m "feat: add new feature"

# 3. Push and create pull request
git push origin feature/new-feature

# 4. Merge via pull request
# (Create PR on GitHub/GitLab)
```

**Release Process:**
```bash
# 1. Create release branch
git checkout develop
git checkout -b release/v1.2.0

# 2. Update version numbers
# Update version in setup.py, __init__.py, etc.

# 3. Commit version bump
git add .
git commit -m "chore: bump version to 1.2.0"

# 4. Merge to main
git checkout main
git merge release/v1.2.0

# 5. Tag release
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin v1.2.0

# 6. Merge back to develop
git checkout develop
git merge release/v1.2.0
git push origin develop

# 7. Delete release branch
git branch -d release/v1.2.0
git push origin --delete release/v1.2.0
```

## 📋 **Git Hooks**

### **1. Pre-commit Hooks**

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running pre-commit checks..."

# Run linting
echo "Running flake8..."
flake8 src/ tests/
if [ $? -ne 0 ]; then
    echo "Flake8 found issues. Please fix them before committing."
    exit 1
fi

# Run tests
echo "Running tests..."
python -m pytest tests/ -v
if [ $? -ne 0 ]; then
    echo "Tests failed. Please fix them before committing."
    exit 1
fi

# Check for large files
echo "Checking for large files..."
find . -type f -size +10M | grep -v ".git" | grep -v "venv"
if [ $? -eq 0 ]; then
    echo "Large files found. Consider using Git LFS."
    exit 1
fi

echo "Pre-commit checks passed!"
```

### **2. Pre-push Hooks**

```bash
#!/bin/bash
# .git/hooks/pre-push

echo "Running pre-push checks..."

# Run full test suite
echo "Running full test suite..."
python -m pytest tests/ --cov=src --cov-report=html
if [ $? -ne 0 ]; then
    echo "Tests failed. Please fix them before pushing."
    exit 1
fi

# Check security vulnerabilities
echo "Checking for security vulnerabilities..."
safety check
if [ $? -ne 0 ]; then
    echo "Security vulnerabilities found. Please update dependencies."
    exit 1
fi

echo "Pre-push checks passed!"
```

## 🔧 **Repository Management**

### **1. .gitignore Configuration**

**Python .gitignore:**
```gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
logs/
*.log
config/local.yaml
secrets/
certs/
```

**Edge Device Specific:**
```gitignore
# Hardware specific
*.img
*.iso
backup/
snapshots/

# Sensor data
data/raw/
data/processed/
*.csv
*.json

# Model files
models/*.pkl
models/*.h5
models/*.onnx
```

**Server Specific:**
```gitignore
# Database
*.db
*.sqlite
*.sqlite3

# Docker
.dockerignore
docker-compose.override.yml

# Nginx
nginx/logs/
nginx/ssl/

# Application logs
app/logs/
*.log
```

### **2. Git LFS Configuration**

**.gitattributes:**
```gitattributes
# Large files
*.pkl filter=lfs diff=lfs merge=lfs -text
*.h5 filter=lfs diff=lfs merge=lfs -text
*.onnx filter=lfs diff=lfs merge=lfs -text
*.model filter=lfs diff=lfs merge=lfs -text

# Images
*.jpg filter=lfs diff=lfs merge=lfs -text
*.jpeg filter=lfs diff=lfs merge=lfs -text
*.png filter=lfs diff=lfs merge=lfs -text
*.gif filter=lfs diff=lfs merge=lfs -text
*.bmp filter=lfs diff=lfs merge=lfs -text
*.tiff filter=lfs diff=lfs merge=lfs -text

# Videos
*.mp4 filter=lfs diff=lfs merge=lfs -text
*.avi filter=lfs diff=lfs merge=lfs -text
*.mov filter=lfs diff=lfs merge=lfs -text
*.mkv filter=lfs diff=lfs merge=lfs -text

# Archives
*.zip filter=lfs diff=lfs merge=lfs -text
*.tar.gz filter=lfs diff=lfs merge=lfs -text
*.rar filter=lfs diff=lfs merge=lfs -text

# Documents
*.pdf filter=lfs diff=lfs merge=lfs -text
*.doc filter=lfs diff=lfs merge=lfs -text
*.docx filter=lfs diff=lfs merge=lfs -text
```

## 🔄 **Multi-Repository Synchronization**

### **1. Sync Script**

```bash
#!/bin/bash
# scripts/sync-repos.sh

echo "Synchronizing repositories..."

# Configuration
AICAMERA_REPO="/path/to/aicamera.git"
LPRSERVER_REPO="/path/to/lprserver_v3.git"
SHARED_TOOLS="/path/to/shared-tools"

# Function to sync repository
sync_repo() {
    local repo_path=$1
    local repo_name=$2
    
    echo "Syncing $repo_name..."
    cd "$repo_path"
    
    # Fetch latest changes
    git fetch origin
    
    # Check if there are local changes
    if [ -n "$(git status --porcelain)" ]; then
        echo "Warning: $repo_name has uncommitted changes"
        git status --short
    fi
    
    # Pull latest changes
    git pull origin main
    
    echo "$repo_name synced successfully"
}

# Sync each repository
sync_repo "$AICAMERA_REPO" "AI Camera"
sync_repo "$LPRSERVER_REPO" "LPR Server"

# Sync shared tools
echo "Syncing shared tools..."
rsync -av --exclude='.git' "$SHARED_TOOLS/templates/" "$AICAMERA_REPO/templates/"
rsync -av --exclude='.git' "$SHARED_TOOLS/templates/" "$LPRSERVER_REPO/templates/"

echo "All repositories synchronized!"
```

### **2. Deployment Script**

```bash
#!/bin/bash
# scripts/deploy.sh

echo "Deploying to devices..."

# Configuration
EDGE_DEVICE="pi@192.168.1.200"
SERVER_DEVICE="ubuntu@192.168.1.100"
AICAMERA_REPO="/path/to/aicamera.git"
LPRSERVER_REPO="/path/to/lprserver_v3.git"

# Deploy to edge device
deploy_edge() {
    echo "Deploying to edge device..."
    
    # Sync code
    rsync -avz --exclude='.git' --exclude='venv' --exclude='__pycache__' \
        "$AICAMERA_REPO/" "$EDGE_DEVICE:/home/pi/aicamera/"
    
    # Execute deployment commands
    ssh "$EDGE_DEVICE" << 'EOF'
        cd /home/pi/aicamera
        source venv/bin/activate
        pip install -r requirements.txt
        sudo systemctl restart aicamera
        echo "Edge device deployment complete"
EOF
}

# Deploy to server
deploy_server() {
    echo "Deploying to server..."
    
    # Sync code
    rsync -avz --exclude='.git' --exclude='venv' --exclude='__pycache__' \
        "$LPRSERVER_REPO/" "$SERVER_DEVICE:/home/ubuntu/lprserver_v3/"
    
    # Execute deployment commands
    ssh "$SERVER_DEVICE" << 'EOF'
        cd /home/ubuntu/lprserver_v3
        docker-compose down
        docker-compose build
        docker-compose up -d
        echo "Server deployment complete"
EOF
}

# Main deployment
case "$1" in
    "edge")
        deploy_edge
        ;;
    "server")
        deploy_server
        ;;
    "all")
        deploy_edge
        deploy_server
        ;;
    *)
        echo "Usage: $0 {edge|server|all}"
        exit 1
        ;;
esac

echo "Deployment completed!"
```

## 📊 **Repository Analytics**

### **1. Git Statistics**

```bash
#!/bin/bash
# scripts/git-stats.sh

echo "Git Repository Statistics"
echo "========================"

# Get repository size
echo "Repository Size:"
du -sh .git/

# Get commit statistics
echo -e "\nCommit Statistics:"
git log --oneline | wc -l | xargs echo "Total commits:"

# Get file statistics
echo -e "\nFile Statistics:"
find . -type f -name "*.py" | wc -l | xargs echo "Python files:"
find . -type f -name "*.md" | wc -l | xargs echo "Markdown files:"
find . -type f -name "*.yaml" -o -name "*.yml" | wc -l | xargs echo "YAML files:"

# Get contributor statistics
echo -e "\nContributor Statistics:"
git shortlog -sn

# Get recent activity
echo -e "\nRecent Activity (last 7 days):"
git log --since="1 week ago" --oneline

# Get branch information
echo -e "\nBranch Information:"
git branch -r
```

### **2. Code Quality Metrics**

```python
# scripts/code_metrics.py
import os
import subprocess
from pathlib import Path
from typing import Dict, Any

def get_code_metrics(repo_path: str) -> Dict[str, Any]:
    """Get code quality metrics for repository"""
    
    metrics = {
        "lines_of_code": 0,
        "python_files": 0,
        "test_coverage": 0,
        "complexity": 0
    }
    
    # Count lines of code
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = len(f.readlines())
                    metrics["lines_of_code"] += lines
                    metrics["python_files"] += 1
    
    # Get test coverage
    try:
        result = subprocess.run(
            ["python", "-m", "pytest", "--cov=src", "--cov-report=term-missing"],
            capture_output=True,
            text=True,
            cwd=repo_path
        )
        
        # Parse coverage output
        for line in result.stdout.split('\n'):
            if 'TOTAL' in line:
                coverage = line.split()[-1].replace('%', '')
                metrics["test_coverage"] = float(coverage)
                break
                
    except Exception as e:
        print(f"Error getting test coverage: {e}")
    
    return metrics

if __name__ == "__main__":
    repos = ["aicamera.git", "lprserver_v3.git"]
    
    for repo in repos:
        print(f"\nMetrics for {repo}:")
        metrics = get_code_metrics(repo)
        
        for key, value in metrics.items():
            print(f"  {key}: {value}")
```

## 🔒 **Security Best Practices**

### **1. Repository Security**

```bash
# Check for sensitive data in repository
git log --all --full-history -- "*.key" "*.pem" "*.crt" "*.p12"
git log --all --full-history -- "password" "secret" "token"

# Remove sensitive data from history
git filter-branch --force --index-filter \
    'git rm --cached --ignore-unmatch config/secrets.yaml' \
    --prune-empty --tag-name-filter cat -- --all

# Force push to remove from remote
git push origin --force --all
```

### **2. Access Control**

```bash
# Set up SSH keys for secure access
ssh-keygen -t ed25519 -C "your.email@example.com"

# Add to SSH agent
ssh-add ~/.ssh/id_ed25519

# Copy public key to devices
ssh-copy-id pi@192.168.1.200
ssh-copy-id ubuntu@192.168.1.100
```

---

**Last Updated**: December 2024  
**Version**: 2.0.0
