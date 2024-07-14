import sys, traceback, warnings
from config import *
from utils import *
from functions import *
from updater import *


with warnings.catch_warnings():
    # IGNORE WARNINGS
    warnings.simplefilter("ignore")


    # Update checking
    if (get_actual_version_link() != None):
        print(replace_all(LOCALIZATION_DATA['INFO_MSG_UPDATE'], { '{version}': ''.join({list(get_actual_version_link().keys())[0]}) }))


    # APP MAIN CODE
    try:
        if (len(sys.argv) > 1):
            arguments = sys.argv[1::]
            function_argument = arguments[0]
            match function_argument:
                case "append" | "add":
                    if (is_admin()):
                        if (len(arguments) >= 3):
                            source = arguments[1]
                            targets = arguments[2::]
                            try:
                                credentials = arguments[arguments.index('--cred')+1]
                            except Exception:
                                credentials = None
                            try:
                                if (credentials != None):
                                    hosts = arguments[arguments.index('--host')+1:arguments.index('--cred'):]
                                    targets = arguments[2:arguments.index('--host'):]
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


                case "config" | "creds":
                    pass


                case "inventory" | "inv":
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
                                credentials = arguments[arguments.index('--cred')+1]
                            except Exception:
                                credentials = None
                            try:
                                if (credentials != None):
                                    hosts = arguments[arguments.index('--host')+1:arguments.index('--cred'):]
                                    targets = arguments[2:arguments.index('--host'):]
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
                                credentials = arguments[arguments.index('--cred')+1]
                            except Exception:
                                credentials = None
                            try:
                                if (credentials != None):
                                    hosts = arguments[arguments.index('--host')+1:arguments.index('--cred'):]
                                    targets = arguments[2:arguments.index('--host'):]
                                else:
                                    hosts = ["localhost"]
                            except Exception:
                                hosts = ["localhost"]
                            question_answer = input(replace_all(LOCALIZATION_DATA['QST_MSG_REMOVE'], 
                                                { "{source}": source, "{targets}": ' '.join(targets), "{hosts}": ' '.join(hosts) }))
                            if (question_answer.lower() == 'y'):
                                print(replace_all(LOCALIZATION_DATA['INFO_MSG_REMOVE'], 
                                                { "{source}": source, "{targets}": ' '.join(targets), "{hosts}": ' '.join(hosts) }))
                                remove_hosts(source, targets, hosts, credentials)
                                print(INFO_MSG_DONE)
                            else:
                                pass
                        else:
                            print(f"{LOCALIZATION_DATA['ERROR_MSG_PARAM']}{HELP_MSG_REMOVE}")
                    else:
                        input(f"{LOCALIZATION_DATA['ERROR_MSG_ADMIN']}")


                case "print" | "show" | "-p":
                    try:
                        credentials = arguments[arguments.index('--cred')+1]
                    except Exception:
                        credentials = None
                    try:
                        if (credentials != None):
                            hosts = arguments[arguments.index('--host')+1:arguments.index('--cred'):]
                            targets = arguments[2:arguments.index('--host'):]
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
                    print(f"{replace_all(LOCALIZATION_DATA['INFO_MSG_VERSION'], { '{version}': VERSION, '{state}': STATE, '{os_type}': OS_TYPE, '{hosts}': HOSTS, '{locales}': ', '.join(LOCALE_AVAILABLE), '{locale_name}': CURRENT_LOCALE, '{author}': LOCALE_AUTHOR } )}")
                
                
                case "--update":
                    if (get_actual_version_link() != None):
                        download_update()
                    else:
                        print(LOCALIZATION_DATA['INFO_MSG_UPTODATE'])


                case _:
                    print(replace_all(LOCALIZATION_DATA['ERROR_MSG_ARG'], 
                                         { "{function_argument}": function_argument }),HELP_MSG)
        else:
            print(HELP_MSG)

    
    except Exception:
        traceback.print_exc()
