import os, json, platform, socket, sys, locale, warnings
from utils import *


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    CULTURE = locale.getdefaultlocale()[0]
    HOSTSCLI_BIN = None
    HOSTSCLI_PATH = None
    if getattr(sys, 'frozen', False):
        HOSTSCLI_PATH = os.path.dirname(os.path.abspath(sys.executable))
    elif __file__:
        HOSTSCLI_PATH = os.path.dirname(os.path.abspath(__file__))
    LOCAL_IP = socket.gethostbyname(socket.gethostname())
    LOCALE_PATH = resource_path("locales")
    BIN_PATH = resource_path("bin")
    WIN_BIN_PATH = f"{BIN_PATH}/hostscli.exe"
    MACOS_BIN_PATH = f"{BIN_PATH}/hostscli_macos"
    LINUX_BIN_PATH = f"{BIN_PATH}/hostscli_linux"
    LOCALE_AVAILABLE = [json.load(open(f"{LOCALE_PATH}/{file}", encoding="utf-8"))['name'] for file in os.listdir(LOCALE_PATH) if os.path.splitext(file)[1] == ".json"]
    LOCALE_AVAILABLE.sort()
    if (os.path.exists(f"{LOCALE_PATH}/{CULTURE}.json")):
        LOCALE_DATA = json.load(open(f"{LOCALE_PATH}/{CULTURE}.json", encoding="utf-8"))
    else:
        LOCALE_DATA = json.load(open(f"{LOCALE_PATH}/en_US.json", encoding="utf-8"))
    LOCALIZATION_DATA = LOCALE_DATA['localization_data']
    OS_TYPE = platform.system()
    CURRENT_LOCALE = LOCALE_DATA['name']
    LOCALE_AUTHOR = LOCALE_DATA['author']
    VERSION = "02.0607.2024"
    STATE = "Test"


    match OS_TYPE:
            
        case "Windows":
            # CONFIG_LOCATION = f"C:\\ProgramData\\hostscli\\hostscli.yaml"
            HOSTS = f"{os.environ['SystemRoot']}\\system32\\drivers\\etc\\hosts"
            
        case "Darwin" | "Linux":
            # CONFIG_LOCATION = "/etc/hostscli/hostscli.yaml"
            HOSTS = "/etc/hosts"


    # STATIC USAGE MESSAGES
    HELP_MSG = LOCALIZATION_DATA['HELP_MSG']
    HELP_MSG_ADD = LOCALIZATION_DATA['HELP_MSG_ADD']
    # HELP_MSG_CONFIG = LOCALIZATION_DATA['HELP_MSG_CONFIG']
    HELP_MSG_EDIT = LOCALIZATION_DATA['HELP_MSG_EDIT']
    HELP_MSG_REMOVE = LOCALIZATION_DATA['HELP_MSG_REMOVE']


    # STATIC INFO MESSAGES
    INFO_MSG_DONE = LOCALIZATION_DATA['INFO_MSG_DONE']