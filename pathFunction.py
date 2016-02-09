import os

def resource_path(relative_path, meipass):
    """
    function from:
    http://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile?lq=1
    User: max
    """
    """ Get absolute path to resource, works for dev and for PyInstaller """
    return relative_path
    #if meipass is "":
    #    base_path = os.path.abspath(".")
    #else:
    #    base_path = meipass
    #return os.path.join(base_path, relative_path)
