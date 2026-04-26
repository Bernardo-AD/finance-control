import sys
from src.menu import run
from src.gui import run_gui

if __name__ == "__main__":
    if "--terminal" in sys.argv:
        run()
    else:
        run_gui()