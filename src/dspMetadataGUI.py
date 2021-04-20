"""
Runner module for the DSP metadata application.

Execute this as a script, or call `main()`  to run the application.
"""

from gui import mainWindow


def main():
    """
    Runs the DSP metadata application.
    
    Calls `mainWindow.run()`
    """
    mainWindow.run()


if __name__ == "__main__":
    main()
