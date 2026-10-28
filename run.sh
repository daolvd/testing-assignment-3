#!/usr/bin/env bash
# ==============================================================================
# RUN ALL TESTS SCRIPT (FOR MACOS / LINUX / GIT BASH)
# Automatically completes setup on the first run, then executes the Behave tests.
# No additional configuration is required.
# ==============================================================================
set -e

cd "$(dirname "$0")"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# If setup has not been completed, automatically run setup.sh
NEEDS_SETUP=0
if [ ! -d ".venv" ] || [ ! -f ".env" ]; then
    NEEDS_SETUP=1
fi

if [ "$NEEDS_SETUP" -eq 1 ]; then
    echo -e "${YELLOW}[INFO] First run detected. Automatically completing the full setup...${NC}"
    chmod +x ./setup.sh 2>/dev/null || true
    ./setup.sh
fi

# Activate the virtual environment (.venv)
if [ -f ".venv/bin/activate" ]; then
    source ".venv/bin/activate"
elif [ -f ".venv/Scripts/activate" ]; then
    source ".venv/Scripts/activate"
else
    echo -e "${YELLOW}[INFO] The environment is not ready. Running setup again...${NC}"
    chmod +x ./setup.sh 2>/dev/null || true
    ./setup.sh
    [ -f ".venv/bin/activate" ] && source ".venv/bin/activate" || source ".venv/Scripts/activate"
fi

# Ensure all dependencies are installed
if ! python -c "import behave, selenium, dotenv" &>/dev/null; then
    echo -e "${YELLOW}[INFO] Dependencies are missing. Updating through setup...${NC}"
    chmod +x ./setup.sh 2>/dev/null || true
    ./setup.sh
fi

# Ensure a test account exists in .env
EMAIL_VAL=$(grep -E "^TEST_EMAIL=" .env 2>/dev/null | cut -d '=' -f2- | tr -d '[:space:]' || true)
PWD_VAL=$(grep -E "^TEST_PASSWORD=" .env 2>/dev/null | cut -d '=' -f2- | tr -d '[:space:]' || true)
if [ -z "$EMAIL_VAL" ] || [ -z "$PWD_VAL" ]; then
    echo -e "${YELLOW}[INFO] No test account found. Creating one automatically...${NC}"
    python -m scripts.register_account --save-env
fi

# Run Behave tests
echo -e "${BLUE}======================================================================${NC}"
echo -e "${BLUE}    STARTING BEHAVE TESTS...                                           ${NC}"
echo -e "${BLUE}======================================================================${NC}"

python -m behave "$@"

EXIT_CODE=$?
echo ""
echo -e "${GREEN}======================================================================${NC}"
echo -e "${GREEN} [COMPLETE] Evidence and screenshots are saved at:                    ${NC}"
echo -e "${GREEN} reports/screenshots/                                                 ${NC}"
echo -e "${GREEN}======================================================================${NC}"

exit $EXIT_CODE
