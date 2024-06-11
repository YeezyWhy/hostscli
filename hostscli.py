import os, sys, traceback, ctypes, locale, json, warnings, platform

with warnings.catch_warnings():
    # IGNORE WARNINGS
    warnings.simplefilter("ignore")
    

    # RESOURCE PATH FUNCTION
    def resource_path(relative_path: str):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    

    # CONFIG
    VERSION = "01.1006.2024"
    CULTURE = locale.getdefaultlocale()[0]
    LOCALE_PATH = resource_path("locales")
    LOCALE_AVAILABLE = [json.load(open(f"{LOCALE_PATH}/{file}", encoding="utf-8"))['name'] for file in os.listdir(LOCALE_PATH) if os.path.splitext(file)[1] == ".json"]
    LOCALE_DATA = json.load(open(f"{LOCALE_PATH}/{CULTURE}.json", encoding="utf-8"))
    LOCALIZATION_DATA = LOCALE_DATA['localization_data']
    OS_TYPE = platform.system()


    # HOSTS BY SYSTEM
    match OS_TYPE:
        case "Windows":
            HOSTS = f"{os.environ['SystemRoot']}\\system32\\drivers\\etc\\hosts"
        case "Darwin":
            HOSTS = "/etc/hosts"
        case "Linux":
            HOSTS = "/private/etc/hosts"
    

    # STATIC USAGE MESSAGES
    HELP_MSG = LOCALIZATION_DATA['HELP_MSG']
    HELP_MSG_ADD = LOCALIZATION_DATA['HELP_MSG_ADD']
    HELP_MSG_EDIT = LOCALIZATION_DATA['HELP_MSG_EDIT']
    HELP_MSG_REMOVE = LOCALIZATION_DATA['HELP_MSG_REMOVE']

    # STATIC INFO MESSAGES
    INFO_MSG_DONE = LOCALIZATION_DATA['INFO_MSG_DONE']

    # FUNCTIONS
    def append_hosts(source: str, targets: list[str]) -> None:
        """Appends new string in the end of the hosts file"""
        with open(HOSTS, 'a') as hosts_file:
            targets = ' '.join(targets)
            content = f"{source} {targets}"
            hosts_file.write(content)
            hosts_file.close()


    def edit_hosts(source1: str, targets1: list[str], source2: str, targets2: list[str]) -> None:
        """Edits string in hosts file"""
        content = None
        with open(HOSTS, 'r') as hosts_file:
            targets1 = ' '.join(targets1)
            targets2 = ' '.join(targets2)
            old = f"{source1} {targets1}"
            new = f"{source2} {targets2}"
            content = hosts_file.read()
            content = content.replace(old, new)
            hosts_file.close()
        with open(HOSTS, 'w') as hosts_file:
            hosts_file.write(content)
            hosts_file.close()


    def remove_hosts(source: str, targets: list[str]) -> None:
        """Removes string from hosts file"""
        content = None
        with open(HOSTS, 'r') as hosts_file:
            targets = ' '.join(targets)
            old = f"{source} {targets}"
            new = ""
            content = hosts_file.read()
            content = content.replace(old, new)
            hosts_file.close()
        with open(HOSTS, 'w') as hosts_file:
            hosts_file.write(content)
            hosts_file.close()


    def is_admin() -> bool:
        """ Checks user for administrator privilages """
        try:
            return os.getuid() == 0
        except AttributeError:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0


    def replace_all(string: str, dict) -> str:
        """Replace all substrings represented in "dict" variable in string represented in "string" variable
        Usage: replace_all("Some text [string1] here, but i [string2]", { "[string1]": "was", "[string2]": "replaced it" }) -> Some text was here, but i replaced it"""
        for i, j in dict.items():
            string = string.replace(i, j)
        return string


    # APP MAIN CODE
    try:
        if (len(sys.argv) > 1 and is_admin()):
            arguments = sys.argv[1::]
            arguments = [s.lower() for s in arguments]
            function_argument = arguments[0]
            match function_argument:
                case "append" | "add":
                    if (len(arguments) >= 3):
                        source = arguments[1]
                        targets = arguments[2::]
                        print(replace_all(LOCALIZATION_DATA['INFO_MSG_ADD'], 
                                          { "{source}": source, "{targets}": ' '.join(targets) }))
                        append_hosts(source, targets)
                        print(INFO_MSG_DONE)
                    else:
                        print(f"{LOCALIZATION_DATA['ERROR_MSG_PARAM']}{HELP_MSG_ADD}")
                case "edit":
                    if (len(arguments) >= 3):
                        if ("from" in arguments):
                            from_index = arguments.index("from")
                        if ("to" in arguments):
                            to_index = arguments.index("to")
                        source1 = arguments[from_index+1]
                        source1_index = arguments.index(source1)
                        source2 = arguments[to_index+1]
                        source2_index = arguments.index(source2, to_index)
                        targets1 = arguments[source1_index+1:to_index]
                        targets2 = arguments[source2_index+1::]
                        print(replace_all(LOCALIZATION_DATA['INFO_MSG_EDIT'], 
                                          { "{source1}": source1, "{source2}": source2, "{targets1}": ' '.join(targets1), "{targets2}": ' '.join(targets2) }))
                        edit_hosts(source1, targets1, source2, targets2)
                        print(INFO_MSG_DONE)
                    else:
                        print(f"{LOCALIZATION_DATA['ERROR_MSG_PARAM']}{HELP_MSG_EDIT}")
                case "remove" | "delete" | "del" | "rm":
                    if (len(arguments) >= 3):
                        source = arguments[1]
                        targets = arguments[2::]
                        print(replace_all(LOCALIZATION_DATA['INFO_MSG_REMOVE'], 
                                          { "{source}": source, "{targets}": ' '.join(targets) }))
                        remove_hosts(source, targets)
                        print(INFO_MSG_DONE)
                    else:
                        print(f"{LOCALIZATION_DATA['ERROR_MSG_PARAM']}{HELP_MSG_REMOVE}")
                case "print" | "show" | "-p":
                    with open(HOSTS, 'r') as f:
                        print(f.read())
                case "--help" | "-h":
                    if (len(arguments) == 2):
                        match arguments[1]:
                            case "append" | "add" | "-a":
                                print(HELP_MSG_ADD)
                            case "edit" | "-e":
                                print(HELP_MSG_EDIT)
                            case "remove" | "delete" | "del" | "rm":
                                print(HELP_MSG_REMOVE)
                            case _:
                                print(replace_all(LOCALIZATION_DATA['ERROR_MSG_HELP'], 
                                                  { "{action_argument}": arguments[1] }))
                    else:
                        print(HELP_MSG)
                case "--version" | "-v":
                    print(f"hostscli version {VERSION}\nOS: {OS_TYPE}\nhosts location: {HOSTS}\navailable locales: {', '.join(LOCALE_AVAILABLE)}")
                case _:
                    print(replace_all(LOCALIZATION_DATA['ERROR_MSG_ARG'], 
                                         { "{function_argument}": function_argument }),HELP_MSG)
        elif (is_admin() == False):
            
            input(f"{LOCALIZATION_DATA['ERROR_MSG_ADMIN']}")
        else:
            print(HELP_MSG)

    except Exception as ex:
        traceback.print_exc()