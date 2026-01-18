#!/bin/bash
# End-to-end test script for G13 Linux daemon + Web GUI
#
# Usage:
#   ./scripts/e2e_test.sh          # Normal mode (needs sudo)
#   ./scripts/e2e_test.sh --no-gui # Don't open browser
#   ./scripts/e2e_test.sh --mock   # Mock mode (no hardware needed)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$PROJECT_DIR/.venv"
PORT=8765
HOST="127.0.0.1"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse arguments
OPEN_GUI=true
MOCK_MODE=false
for arg in "$@"; do
    case $arg in
        --no-gui)
            OPEN_GUI=false
            ;;
        --mock)
            MOCK_MODE=true
            ;;
    esac
done

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         G13 Linux - End-to-End Test                        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check virtual environment
if [[ ! -d "$VENV_DIR" ]]; then
    echo -e "${RED}Error: Virtual environment not found at $VENV_DIR${NC}"
    echo "Run: python3 -m venv .venv && pip install -e ."
    exit 1
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# Check if web GUI is built
if [[ ! -f "$PROJECT_DIR/gui-web/dist/index.html" ]]; then
    echo -e "${YELLOW}Warning: Web GUI not built${NC}"
    echo "Building web GUI..."
    cd "$PROJECT_DIR/gui-web"
    if command -v npm &> /dev/null; then
        npm run build
    else
        echo -e "${RED}Error: npm not found. Install Node.js or build manually.${NC}"
        exit 1
    fi
    cd "$PROJECT_DIR"
fi

echo -e "${GREEN}✓ Web GUI built${NC}"

# Check for G13 device (unless mock mode)
if [[ "$MOCK_MODE" == "false" ]]; then
    echo ""
    echo -e "${BLUE}Checking for G13 device...${NC}"

    if lsusb | grep -q "046d:c21c"; then
        echo -e "${GREEN}✓ G13 device found${NC}"
    else
        echo -e "${YELLOW}⚠ G13 device not detected${NC}"
        echo "  - Make sure the G13 is connected via USB"
        echo "  - Try: lsusb | grep -i logitech"
        echo ""
        read -p "Continue anyway? [y/N] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi

    # Check if we need sudo
    if [[ $EUID -ne 0 ]]; then
        echo ""
        echo -e "${YELLOW}Note: USB access typically requires root privileges${NC}"
        echo "The daemon will be started with sudo..."
        SUDO_CMD="sudo"
    else
        SUDO_CMD=""
    fi
else
    echo -e "${YELLOW}Running in mock mode (no hardware)${NC}"
    SUDO_CMD=""
fi

# Print test instructions
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}                    Test Instructions                        ${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Once the daemon starts:"
echo ""
echo "  1. Open browser to: ${GREEN}http://$HOST:$PORT${NC}"
echo ""
echo "  2. Test these features:"
echo "     ${YELLOW}Buttons${NC}    - Press G1-G22, M1-M3, watch GUI highlights"
echo "     ${YELLOW}Joystick${NC}   - Move thumbstick, verify position in GUI"
echo "     ${YELLOW}Profiles${NC}   - Load/switch profiles from GUI"
echo "     ${YELLOW}Backlight${NC}  - Change LED color from GUI"
echo "     ${YELLOW}Macros${NC}     - List and trigger macros"
echo "     ${YELLOW}LCD Menu${NC}   - Press thumbstick on device"
echo ""
echo "  3. Check WebSocket events in browser DevTools:"
echo "     - Open DevTools (F12) → Network → WS"
echo "     - Watch for button_pressed, joystick events"
echo ""
echo "  4. Press Ctrl+C to stop the daemon"
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""

# Open browser (in background)
if [[ "$OPEN_GUI" == "true" ]]; then
    (
        sleep 2  # Wait for server to start
        URL="http://$HOST:$PORT"

        # Try different browser openers
        if command -v xdg-open &> /dev/null; then
            xdg-open "$URL" 2>/dev/null &
        elif command -v open &> /dev/null; then
            open "$URL" &
        elif command -v firefox &> /dev/null; then
            firefox "$URL" &
        elif command -v chromium-browser &> /dev/null; then
            chromium-browser "$URL" &
        else
            echo -e "${YELLOW}Could not open browser. Please navigate to: $URL${NC}"
        fi
    ) &
fi

# Start the daemon
echo -e "${GREEN}Starting G13 daemon...${NC}"
echo ""

if [[ "$MOCK_MODE" == "true" ]]; then
    # Run a quick API test instead of full daemon
    echo "Running API tests in mock mode..."
    python3 -c "
import asyncio
import aiohttp
from pathlib import Path
from g13_linux.server import G13Server
from g13_linux.gui.models.event_decoder import EventDecoder
from g13_linux.gui.models.macro_manager import MacroManager
from g13_linux.gui.models.profile_manager import ProfileManager

class MockDaemon:
    def __init__(self):
        self._device = True
        self._led_controller = None
        self._event_decoder = EventDecoder()
        self._last_joystick = (128, 128)
        self._enable_server = True
        self._server = None
        self._server_loop = None
        self.profile_manager = ProfileManager()
        self.macro_manager = MacroManager()

async def run_mock_server():
    daemon = MockDaemon()
    static_dir = Path('$PROJECT_DIR/gui-web/dist')
    server = G13Server(daemon, '$HOST', $PORT, static_dir=static_dir)
    daemon._server = server

    await server.start()
    daemon._server_loop = asyncio.get_event_loop()

    print('Mock server running at http://$HOST:$PORT')
    print('Press Ctrl+C to stop')

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        await server.stop()

asyncio.run(run_mock_server())
"
else
    # Run actual daemon
    cd "$PROJECT_DIR"
    $SUDO_CMD "$VENV_DIR/bin/python" -m g13_linux.cli run --server-host "$HOST" --server-port "$PORT"
fi

echo ""
echo -e "${GREEN}Test complete.${NC}"
