import os, sys, traceback, ctypes, locale, json, warnings, platform, socket
import paramiko


with warnings.catch_warnings():
    # IGNORE WARNINGS
    warnings.simplefilter("ignore")
    

    # RESOURCE PATH FUNCTION
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    

    # CONFIG
    CULTURE = locale.getdefaultlocale()[0]
    HOSTSCLI_BIN = None
    HOSTSCLI_PATH = None
    if getattr(sys, 'frozen', False):
        HOSTSCLI_BIN = os.path.basename(sys.executable)
        HOSTSCLI_PATH = os.path.dirname(os.path.abspath(sys.executable))
    elif __file__:
        HOSTSCLI_BIN = os.path.basename(__file__)
        HOSTSCLI_PATH = os.path.dirname(os.path.abspath(__file__))
    LOCAL_IP = socket.gethostbyname(socket.gethostname())
    LOCALE_PATH = f"{HOSTSCLI_PATH}/locales"
    LOCALE_AVAILABLE = [json.load(open(f"{LOCALE_PATH}/{file}", encoding="utf-8"))['name'] for file in os.listdir(LOCALE_PATH) if os.path.splitext(file)[1] == ".json"]
    LOCALE_DATA = json.load(open(f"{LOCALE_PATH}/{CULTURE}.json", encoding="utf-8"))
    LOCALIZATION_DATA = LOCALE_DATA['localization_data']
    OS_TYPE = platform.system()
    VERSION = "01.1206.2024 Test Build"
    SSH_CONFIG = ""


    # HOSTSCLI SETTINGS BY SYSTEM
    match OS_TYPE:
        case "Windows":
            # CONFIG_LOCATION = f"C:\\ProgramData\\hostscli\\hostscli.yaml"
            HOSTS = f"{os.environ['SystemRoot']}\\system32\\drivers\\etc\\hosts"
        case "Darwin":
            # CONFIG_LOCATION = "/etc/hostscli/hostscli.yaml"
            HOSTS = "/etc/hosts"
        case "Linux":
            # CONFIG_LOCATION = "/etc/hostscli/hostscli.yaml"
            HOSTS = "/private/etc/hosts"
    

    # STATIC USAGE MESSAGES
    HELP_MSG = LOCALIZATION_DATA['HELP_MSG']
    HELP_MSG_ADD = LOCALIZATION_DATA['HELP_MSG_ADD']
    HELP_MSG_CONFIG = LOCALIZATION_DATA['HELP_MSG_CONFIG']
    HELP_MSG_EDIT = LOCALIZATION_DATA['HELP_MSG_EDIT']
    HELP_MSG_REMOVE = LOCALIZATION_DATA['HELP_MSG_REMOVE']


    # STATIC INFO MESSAGES
    INFO_MSG_DONE = LOCALIZATION_DATA['INFO_MSG_DONE']


    # FUNCTIONS
    

    # REMOTE
    def execute_command_on_remote_host(host, credentials, command, sudo = False) -> str:
        try:
            username = credentials.split(':')[0]
            password = credentials.split(':')[1]
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=host, username=username, password=password)
            channel = client.get_transport().open_session()
            channel.get_pty()
            channel.exec_command(command)
            if (sudo == True):
                channel.send(password+'\n')
            remote_system_type = channel.recv(1024)
            channel.close()
            client.close()
            return str(remote_system_type.decode()).strip()
        except:
            return f"{replace_all(LOCALIZATION_DATA['ERROR_MSG_SSH'], { "{host}": host })}"


    def add_hostscli_to_remote_host(host, credentials, remote_system_type) -> None:
        try:
            username = credentials.split(':')[0]
            password = credentials.split(':')[1]
            port = 22
            transport = paramiko.Transport((host, port))
            transport.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            match remote_system_type:
                case "Windows":
                    SSH_LOCALPATH = f"{HOSTSCLI_PATH}\\hostscli.exe"
                    SSH_REMOTEPATH = "C:\\Windows\\Temp\\hostscli.exe"
                case "Darwin" | "Linux":
                    SSH_LOCALPATH = f"{HOSTSCLI_PATH}/hostscli"
                    SSH_REMOTEPATH = "/tmp/hostscli"
            locale_files = [file for file in os.listdir(LOCALE_PATH) if os.path.splitext(file)[1] == ".json"]
            execute_command_on_remote_host(host, credentials, "cd /tmp/ && mkdir locales")
            for file in locale_files:
                sftp.put(f"{LOCALE_PATH}/{file}", f"/tmp/locales/{file}")
            sftp.put(SSH_LOCALPATH, SSH_REMOTEPATH)
            sftp.close()
            transport.close()
            execute_command_on_remote_host(host, credentials, f"chmod +x {SSH_REMOTEPATH}", False)
        except Exception:
            traceback.print_exc()


    def get_remote_system_type(host, credentials):
        return execute_command_on_remote_host(host, credentials, "uname")


    def is_admin() -> bool:
        """ Checks user for administrator privilages """
        try:
            return os.getuid() == 0
        except AttributeError:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0


    def replace_all(string, dict) -> str:
        """Replace all substrings represented in "dict" variable in string represented in "string" variable
        Usage: replace_all("Some text [string1] here, but i [string2]", { "[string1]": "was", "[string2]": "replaced it" }) -> Some text was here, but i replaced it"""
        for i, j in dict.items():
            string = string.replace(i, j)
        return string


    # LOCAL
    def append_hosts(source, targets, hosts, credentials) -> None:
        """Appends new string in the end of the hosts file"""
        for host in hosts:
            if (host in ['localhost', '127.0.0.1', LOCAL_IP]):
                with open(HOSTS, 'a') as hosts_file:
                    targets = ' '.join(targets)
                    content = f"{source} {targets}"
                    hosts_file.write(content)
                    hosts_file.close()
            else:
                remote_system_type = get_remote_system_type(host, credentials)
                print(replace_all(LOCALIZATION_DATA["INFO_MSG_SFTP_COPY"], { "{host}": host }))
                add_hostscli_to_remote_host(host, credentials, remote_system_type)
                print(INFO_MSG_DONE)
                if (remote_system_type == "Windows"):
                    print(f"{host} hosts:\n")
                    print(execute_command_on_remote_host())
                elif (remote_system_type in ["Linux", "Darwin"]):
                    print(f"{host} hosts:\n")
                    print(execute_command_on_remote_host(host, credentials, f"cd /tmp && ./hostscli add {source} {' '.join(targets)}"))


    def edit_hosts(source1, targets1, source2, targets2, hosts, credentials) -> None:
        """Edits string in hosts file"""
        for host in hosts:
            if (host in ['localhost', '127.0.0.1', LOCAL_IP]):
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


    def print_hosts(hosts, credentials) -> None:
        for host in hosts:
            if (host in ['localhost', '127.0.0.1', LOCAL_IP]):
                with open(HOSTS, 'r') as f:
                    print(f"{host} hosts:\n")
                    print(f.read())
            else:
                remote_system_type = get_remote_system_type(host, credentials)
                print(replace_all(LOCALIZATION_DATA["INFO_MSG_SFTP_COPY"], { "{host}": host }))
                add_hostscli_to_remote_host(host, credentials, remote_system_type)
                print(INFO_MSG_DONE)
                if (remote_system_type == "Windows"):
                    print(f"{host} hosts:\n")
                    print(execute_command_on_remote_host())
                elif (remote_system_type in ["Linux", "Darwin"]):
                    print(f"{host} hosts:\n")
                    print(execute_command_on_remote_host(host, credentials, f"cd /tmp && ./hostscli print"))


    def remove_hosts(source, targets, hosts, credentials) -> None:
        """Removes string from hosts file"""
        for host in hosts:
            if (host in ['localhost', '127.0.0.1', LOCAL_IP]):
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


    # APP MAIN CODE
    try:
        if (len(sys.argv) > 1):
            arguments = sys.argv[1::]
            arguments = [s.lower() for s in arguments]
            function_argument = arguments[0]
            match function_argument:
                case "append" | "add":
                    if (is_admin()):
                        if (len(arguments) >= 3):
                            source = arguments[1]
                            targets = arguments[2::]
                            try:
                                credentials = arguments[arguments.index('cred')+1]
                            except Exception:
                                credentials = None
                            try:
                                if (credentials != None):
                                    hosts = arguments[arguments.index('host')+1:arguments.index('cred'):]
                                else:
                                    hosts = ["localhost"]
                            except Exception:
                                hosts = ["localhost"]
                            print(replace_all(LOCALIZATION_DATA['INFO_MSG_ADD'], 
                                            { "{source}": source, "{targets}": ' '.join(targets), "{hosts}": ' '.join(hosts) }))
                            append_hosts(source, targets, hosts, credentials)
                            print(INFO_MSG_DONE)
                        else:
                            print(f"{LOCALIZATION_DATA['ERROR_MSG_PARAM']}{HELP_MSG_ADD}")
                    else:
                        input(f"{LOCALIZATION_DATA['ERROR_MSG_ADMIN']}")


                case "config" | "creds" | "-conf":
                    pass


                case "edit":
                    if (is_admin()):
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
                            try:
                                credentials = arguments[arguments.index('cred')+1]
                            except Exception:
                                credentials = None
                            try:
                                if (credentials != None):
                                    hosts = arguments[arguments.index('host')+1:arguments.index('cred'):]
                                else:
                                    hosts = ["localhost"]
                            except Exception:
                                hosts = ["localhost"]
                            print(replace_all(LOCALIZATION_DATA['INFO_MSG_EDIT'], 
                                            { "{source1}": source1, "{source2}": source2, "{targets1}": ' '.join(targets1), "{targets2}": ' '.join(targets2), "{hosts}": ' '.join(hosts) }))
                            edit_hosts(source1, targets1, source2, targets2, hosts, credentials)
                            print(INFO_MSG_DONE)
                        else:
                            print(f"{LOCALIZATION_DATA['ERROR_MSG_PARAM']}{HELP_MSG_EDIT}")
                    else:
                        input(f"{LOCALIZATION_DATA['ERROR_MSG_ADMIN']}")


                case "remove" | "delete" | "del" | "rm":
                    if (is_admin()):
                        if (len(arguments) >= 3):
                            source = arguments[1]
                            targets = arguments[2::]
                            try:
                                credentials = arguments[arguments.index('cred')+1]
                            except Exception:
                                credentials = None
                            try:
                                if (credentials != None):
                                    hosts = arguments[arguments.index('host')+1:arguments.index('cred'):]
                                else:
                                    hosts = ["localhost"]
                            except Exception:
                                hosts = ["localhost"]
                            print(replace_all(LOCALIZATION_DATA['INFO_MSG_REMOVE'], 
                                            { "{source}": source, "{targets}": ' '.join(targets), "{hosts}": ' '.join(hosts) }))
                            remove_hosts(source, targets, hosts, credentials)
                            print(INFO_MSG_DONE)
                        else:
                            print(f"{LOCALIZATION_DATA['ERROR_MSG_PARAM']}{HELP_MSG_REMOVE}")
                    else:
                        input(f"{LOCALIZATION_DATA['ERROR_MSG_ADMIN']}")


                case "print" | "show" | "-p":
                    try:
                        credentials = arguments[arguments.index('cred')+1]
                    except Exception:
                        credentials = None
                    try:
                        if (credentials != None):
                            hosts = arguments[arguments.index('host')+1:arguments.index('cred'):]
                        else:
                            hosts = ["localhost"]
                    except Exception:
                        hosts = ["localhost"]
                    print_hosts(hosts, credentials)


                case "--help" | "-h":
                    if (len(arguments) == 2):
                        match arguments[1]:
                            case "append" | "add" | "-a":
                                print(HELP_MSG_ADD)
                            case "config" | "creds" | "-conf":
                                pass
                                # print(HELP_MSG_CONFIG)
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
        else:
            print(HELP_MSG)

    
    except Exception:
        traceback.print_exc()