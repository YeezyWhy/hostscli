import os, sys, ctypes


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def is_admin() -> bool:
    """Checks user for administrator privilages"""
    try:
        return os.getuid() == 0 | 501
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0


def replace_all(string, dict) -> str:
    """Replace all substrings represented in "dict" variable in string represented in "string" variable
    Usage: replace_all("Some text [string1] here, but i [string2]", { "[string1]": "was", "[string2]": "replaced it" }) -> Some text was here, but i replaced it"""
    for i, j in dict.items():
        string = string.replace(i, j)
    return string