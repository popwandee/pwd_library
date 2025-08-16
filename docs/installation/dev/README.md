# Development Machine Installation Guide

**Version:** 1.0.0  
**Last Updated:** 2024-08-16  
**Author:** Edge AI Team  
**Category:** Installation - Development  
**Status:** Active

## Overview

คู่มือการติดตั้งสำหรับเครื่องพัฒนา (Development Machine) ที่ใช้สำหรับพัฒนาและทดสอบระบบ Edge AI

## 📋 Prerequisites

### Hardware Requirements
- **OS:** Windows 10/11, macOS, หรือ Linux
- **RAM:** 8GB+ (16GB recommended)
- **Storage:** 50GB+ free space
- **CPU:** 4+ cores (8+ cores recommended)
- **Network:** Stable internet connection

### Software Requirements
- **Python 3.10+**
- **Git**
- **IDE:** VS Code, PyCharm, หรือ Cursor
- **Docker** (optional)
- **Postman** หรือ **curl** สำหรับ API testing

## 🚀 Installation Steps

### Step 1: Install Python

#### Windows
```bash
# Download Python from python.org
# หรือใช้ winget
winget install Python.Python.3.10

# หรือใช้ Chocolatey
choco install python

# Verify installation
python --version
pip --version
```

#### macOS
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.10

# Verify installation
python3 --version
pip3 --version
```

#### Linux (Ubuntu/Debian)
```bash
# Update system
sudo apt update

# Install Python
sudo apt install python3 python3-pip python3-venv

# Verify installation
python3 --version
pip3 --version
```

### Step 2: Install Git

#### Windows
```bash
# Download from git-scm.com
# หรือใช้ winget
winget install Git.Git

# หรือใช้ Chocolatey
choco install git
```

#### macOS
```bash
# Install with Homebrew
brew install git

# หรือใช้ Xcode Command Line Tools
xcode-select --install
```

#### Linux
```bash
# Ubuntu/Debian
sudo apt install git

# CentOS/RHEL
sudo yum install git
```

### Step 3: Install IDE

#### VS Code (Recommended)
```bash
# Windows
winget install Microsoft.VisualStudioCode

# macOS
brew install --cask visual-studio-code

# Linux
sudo snap install code --classic
```

#### PyCharm
```bash
# Download from jetbrains.com
# หรือใช้ package manager
```

#### Cursor
```bash
# Download from cursor.sh
# หรือใช้ package manager
```

### Step 4: Install Development Tools

#### Windows
```bash
# Install Chocolatey (if not installed)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install tools
choco install postman
choco install docker-desktop
choco install nodejs
```

#### macOS
```bash
# Install tools with Homebrew
brew install --cask postman
brew install --cask docker
brew install node

# Install additional tools
brew install jq
brew install httpie
```

#### Linux
```bash
# Install tools
sudo apt install curl wget jq httpie

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### Step 5: Setup Development Environment

```bash
# Clone repository
git clone <your-repository-url>
cd <your-project-directory>

# Create virtual environment
python3 -m venv venv_dev

# Activate virtual environment
# Windows
venv_dev\Scripts\activate

# macOS/Linux
source venv_dev/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Step 6: Install Tailscale

#### Windows
```bash
# Download from tailscale.com
# หรือใช้ winget
winget install Tailscale.Tailscale
```

#### macOS
```bash
# Install with Homebrew
brew install tailscale
```

#### Linux
```bash
# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh
```

## ⚙️ Configuration

### IDE Configuration

#### VS Code Configuration
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./venv_dev/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": [
        "tests"
    ],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/venv_dev": true
    }
}
```

#### PyCharm Configuration
1. **Project Interpreter:** เลือก `venv_dev/bin/python`
2. **Code Style:** ใช้ Black formatter
3. **Linting:** เปิดใช้งาน Pylint
4. **Testing:** ตั้งค่า pytest

### Environment Configuration

สร้างไฟล์ `.env` ในโฟลเดอร์หลัก:

```bash
# Development Configuration
FLASK_ENV=development
FLASK_APP=app.wsgi:app
PYTHONPATH=/path/to/your/project

# Database Configuration (for local testing)
DATABASE_URL=sqlite:///dev.db
# หรือใช้ PostgreSQL local
# DATABASE_URL=postgresql://user:password@localhost:5432/dev_db

# Network Configuration
HTTP_PORT=5000
WEBSOCKET_PORT=8765
DEBUG=True

# Logging Configuration
LOG_LEVEL=DEBUG
LOG_FILE=logs/dev_app.log

# Testing Configuration
TEST_DATABASE_URL=sqlite:///test.db
TESTING=True

# Edge Device Configuration (for testing)
EDGE_HOST=aicamera1
SERVER_HOST=lprserver
```

### Git Configuration

```bash
# Configure Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Setup SSH key (if not already done)
ssh-keygen -t ed25519 -C "your.email@example.com"

# Add SSH key to GitHub/GitLab
cat ~/.ssh/id_ed25519.pub
# Copy and paste to your Git provider

# Test SSH connection
ssh -T git@github.com
```

## 🔧 Verification

### Step 1: Verify Installation

```bash
# Check Python
python --version
pip list

# Check Git
git --version

# Check IDE
code --version  # VS Code
# หรือตรวจสอบ PyCharm/Cursor

# Check Tailscale
tailscale status
```

### Step 2: Test Development Environment

```bash
# Activate virtual environment
source venv_dev/bin/activate  # macOS/Linux
# หรือ venv_dev\Scripts\activate  # Windows

# Test Python packages
python -c "import flask, sqlalchemy, pytest; print('All packages installed')"

# Test Git
git status
```

### Step 3: Test Communication

```bash
# Test connection to Edge device
ping aicamera1

# Test connection to Server
ping lprserver

# Test SSH access
ssh camuser@aicamera1
ssh ubuntu@lprserver
```

### Step 4: Test Development Tools

```bash
# Test Postman
# เปิด Postman และทดสอบ API endpoints

# Test Docker (if installed)
docker --version
docker run hello-world

# Test Node.js
node --version
npm --version
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Python Installation Issues
```bash
# Windows: Check PATH
echo $env:PATH

# macOS: Check Python installation
which python3
python3 --version

# Linux: Check Python installation
which python3
python3 --version
```

#### 2. Virtual Environment Issues
```bash
# Create new virtual environment
python3 -m venv venv_dev_new

# Activate virtual environment
source venv_dev_new/bin/activate  # macOS/Linux
# หรือ venv_dev_new\Scripts\activate  # Windows

# Install packages
pip install -r requirements.txt
```

#### 3. Git Issues
```bash
# Check Git configuration
git config --list

# Reset Git configuration
git config --global --unset user.name
git config --global --unset user.email

# Reconfigure Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

#### 4. IDE Issues
```bash
# VS Code: Reset settings
# ลบ .vscode folder และสร้างใหม่

# PyCharm: Reset project
# File -> Invalidate Caches and Restart
```

### Diagnostic Commands

```bash
# System information
uname -a  # Linux/macOS
systeminfo  # Windows

# Python information
python --version
pip list

# Git information
git --version
git config --list

# Network information
ping google.com
nslookup aicamera1
```

## 📊 Development Workflow

### Code Development

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes
# ... edit code ...

# Test changes
pytest tests/

# Format code
black .
isort .

# Commit changes
git add .
git commit -m "Add new feature"

# Push changes
git push origin feature/new-feature
```

### Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api.py

# Run with coverage
pytest --cov=app tests/

# Run integration tests
pytest tests/integration/
```

### Debugging

```bash
# Run with debug mode
FLASK_ENV=development FLASK_DEBUG=1 python app.py

# Use debugger
import pdb; pdb.set_trace()

# Use logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔒 Security Configuration

### SSH Key Management

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Add to SSH agent
ssh-add ~/.ssh/id_ed25519

# Copy public key
cat ~/.ssh/id_ed25519.pub
```

### Git Security

```bash
# Use SSH instead of HTTPS
git remote set-url origin git@github.com:username/repository.git

# Enable GPG signing (optional)
gpg --full-generate-key
git config --global user.signingkey YOUR_GPG_KEY_ID
git config --global commit.gpgsign true
```

### Environment Security

```bash
# Never commit sensitive data
echo ".env" >> .gitignore
echo "*.key" >> .gitignore
echo "*.pem" >> .gitignore

# Use environment variables
export SECRET_KEY="your-secret-key"
export DATABASE_PASSWORD="your-database-password"
```

## 📚 References

### Official Documentation
- [Python Documentation](https://docs.python.org/)
- [Git Documentation](https://git-scm.com/doc)
- [VS Code Documentation](https://code.visualstudio.com/docs)
- [PyCharm Documentation](https://www.jetbrains.com/pycharm/documentation/)

### Development Tools
- [Postman Documentation](https://learning.postman.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Node.js Documentation](https://nodejs.org/docs/)

### Best Practices
- [Python Style Guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
- [Git Best Practices](https://git-scm.com/book/en/v2)
- [VS Code Best Practices](https://code.visualstudio.com/docs/getstarted/tips-and-tricks)

---

**Note:** เอกสารนี้เป็นคู่มือการติดตั้งสำหรับเครื่องพัฒนา
