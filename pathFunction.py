import os

def resource_path(relative_path):
    """
    function from:
    http://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile?lq=1
    User: max
    """
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
