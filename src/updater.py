import requests, wget
from config import *


def get_actual_version_link() -> dict | None:
    """Checks for update and return dict object {"version": "download_link"}"""
    response = requests.get("https://api.github.com/repos/yeezywhy/hostscli/releases/latest").json()
    assets = response['assets']
    version_on_git = int(''.join(str(response['tag_name']).split('.')))
    current_version = int(''.join(VERSION.split('.')))
    update_data = None
    if (current_version < version_on_git):
        for asset in assets:
            match OS_TYPE:
                case "Windows":
                    if (asset['name'] == "hostscli_Windows.exe"):
                        update_data = {response['tag_name']: asset['browser_download_url']}
                        return update_data
                
                case "Linux":
                    if (asset['name'] == "hostscli_Linux"):
                        update_data = {response['tag_name']: asset['browser_download_url']}
                        return update_data
                
                case "Darwin":
                    if (asset['name'] == "hostscli_MacOS"):
                        update_data = {response['tag_name']: asset['browser_download_url']}
                        return update_data


"""Downloads update from download_link"""
def download_update() -> None:
    match OS_TYPE:
        case "Windows":
            output_name = "hostscli.exe"

        case "Darwin" | "Linux":
            output_name = "hostscli"

    wget.download(list(get_actual_version_link().values())[0], f"{HOSTSCLI_PATH}/{output_name}")


try:
    if (len(sys.argv) > 1):
        arguments = sys.argv[1::]
        function_argument = arguments[0]
        match function_argument:
            case "--update":
                if (get_actual_version_link() != None):
                    download_update()
except:
    pass