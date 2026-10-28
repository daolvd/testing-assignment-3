#!/usr/bin/env bash
# ==============================================================================
# AUTOMATED ENVIRONMENT SETUP SCRIPT (FOR MACOS / LINUX / GIT BASH)
# Automatically: creates .venv, installs requirements.txt, creates .env, and registers a test account.
# ==============================================================================
set -e

cd "$(dirname "$0")"

# Console color formatting
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}======================================================================${NC}"
echo -e "${BLUE}    STARTING TEST ENVIRONMENT SETUP                                    ${NC}"
echo -e "${BLUE}======================================================================${NC}"

# 1. Check Python
if command -v python3 &>/dev/null; then
    PY_CMD="python3"
elif command -v python &>/dev/null; then
    PY_CMD="python"
elif command -v py &>/dev/null; then
    PY_CMD="py -3"
else
    echo -e "${RED}[ERROR] Python was not found! Please install Python 3.11+.${NC}"
    exit 1
fi

# 2. Create the .venv virtual environment
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}[1/4] Creating the .venv virtual environment...${NC}"
    $PY_CMD -m venv .venv
else
    echo -e "${GREEN}[OK] The .venv virtual environment already exists.${NC}"
fi

# Activate the virtual environment
if [ -f ".venv/bin/activate" ]; then
    source ".venv/bin/activate"
elif [ -f ".venv/Scripts/activate" ]; then
    source ".venv/Scripts/activate"
else
    echo -e "${RED}[ERROR] The activate file was not found in .venv!${NC}"
    exit 1
fi

# 3. Install dependencies
echo -e "${YELLOW}[2/4] Checking and installing dependencies from requirements.txt...${NC}"
python -m pip install --upgrade pip >/dev/null 2>&1 || true
python -m pip install -r requirements.txt

# 4. Create the .env configuration file
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}[3/4] Creating .env from .env.example...${NC}"
    cp .env.example .env
else
    echo -e "${GREEN}[OK] The .env file already exists.${NC}"
fi

# 5. Automatically register a test account if one does not exist
EMAIL_VAL=$(grep -E "^TEST_EMAIL=" .env 2>/dev/null | cut -d '=' -f2- | tr -d '[:space:]' || true)
PWD_VAL=$(grep -E "^TEST_PASSWORD=" .env 2>/dev/null | cut -d '=' -f2- | tr -d '[:space:]' || true)

if [ -z "$EMAIL_VAL" ] || [ -z "$PWD_VAL" ]; then
    echo -e "${YELLOW}[4/4] Automatically registering a new test account and saving it to .env...${NC}"
    python -m scripts.register_account --save-env || {
        echo -e "${RED}[WARNING] Could not create the account automatically (please check your internet connection).${NC}"
    }
else
    echo -e "${GREEN}[OK] A test account already exists: ${EMAIL_VAL}${NC}"
fi

echo ""
echo -e "${GREEN}======================================================================${NC}"
echo -e "${GREEN} [SUCCESS] Setup completed successfully!                              ${NC}"
echo -e "${GREEN} Run ./run.sh to start testing.                                       ${NC}"
echo -e "${GREEN}======================================================================${NC}"
