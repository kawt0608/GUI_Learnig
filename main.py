# main.py
import sys
from PySide6.QtWidgets import QApplication
from stopwatch import Stopwatch

def main():
    app = QApplication(sys.argv)
    stopwatch = Stopwatch()
    stopwatch.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
