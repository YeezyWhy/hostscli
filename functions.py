import warnings, paramiko, traceback
from utils import *
from config import *


with warnings.catch_warnings():
    warnings.simplefilter("ignore")


    # REMOTE
    def execute_command_on_remote_host(host, credentials, command, sudo = False) -> str:
        """Executes command on remote host via ssh"""
        try:
            username = credentials.split(':')[0]
            password = credentials.split(':')[1]
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=host, username=username, password=password, timeout=10)
            stdin, stdout, stderr = client.exec_command(command=command)
            if (sudo == True):
                stdin.write(password + "\n")
                stdin.flush()
            stdoutput = [line for line in stdout]
            stderroutput = [line for line in stderr]
            if not stdout.channel.recv_exit_status():
                client.close()
                return '\n'.join(stdoutput).strip()
            else:
                client.close()
                raise Exception('\n'.join(stderroutput).strip())
        except:
            return f"{replace_all(LOCALIZATION_DATA['ERROR_MSG_SSH'], { '{host}': host })}"


    def add_hostscli_to_remote_host(host, credentials, remote_system_type) -> None:
        """Copying hostscli bin file to target host"""
        try:
            username = credentials.split(':')[0]
            password = credentials.split(':')[1]
            port = 22
            transport = paramiko.Transport((host, port))
            transport.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            match remote_system_type:
                case "Windows":
                    SSH_LOCALPATH = WIN_BIN_PATH
                    SSH_REMOTEPATH = "C:\\Windows\\Temp\\hostscli.exe"
                case "Darwin":
                    SSH_LOCALPATH = MACOS_BIN_PATH
                    SSH_REMOTEPATH = "/tmp/hostscli"
                case "Linux":
                    SSH_LOCALPATH = LINUX_BIN_PATH
                    SSH_REMOTEPATH = "/tmp/hostscli"
            sftp.put(SSH_LOCALPATH, SSH_REMOTEPATH)
            sftp.close()
            transport.close()
            if (remote_system_type in ["Linux", "Darwin"]):
                execute_command_on_remote_host(host, credentials, f"chmod +x {SSH_REMOTEPATH}", False)
        except Exception:
            traceback.print_exc()


    def get_remote_system_type(host, credentials):
        """Gets remote system type (Linux, Darwin, Windows)"""
        return execute_command_on_remote_host(host, credentials, "uname")


    # LOCAL
    def append_hosts(source, targets, hosts: list[str], credentials: str) -> None:
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
                    print(execute_command_on_remote_host(f"C:\\Windows\\Temp\\hostscli.exe add {source} {' '.join(targets)}"))
                elif (remote_system_type in ["Linux", "Darwin"]):
                    print(execute_command_on_remote_host(host, credentials, f"sudo /tmp/hostscli add {source} {' '.join(targets)}", True))


    def import_hosts(file: str, hosts: list[str], credentials: str) -> None:
        imported_content = None
        with open(file, 'r') as imported_file:
            imported_content = imported_file.read()
            imported_file.close()
        for host in hosts:
            if (host in ['localhost', '127.0.0.1', LOCAL_IP]):
                with open(HOSTS, 'a') as hosts_file:
                    hosts_file.write(imported_content)
                    hosts_file.close()
            else:
                remote_system_type = get_remote_system_type(host, credentials)
                print(replace_all(LOCALIZATION_DATA["INFO_MSG_SFTP_COPY"], { "{host}": host }))
                add_hostscli_to_remote_host(host, credentials, remote_system_type)
                print(INFO_MSG_DONE)
                if (remote_system_type == "Windows"):
                    for line in imported_content.split('\n'):
                        print(execute_command_on_remote_host(f"C:\\Windows\\Temp\\hostscli.exe add {line}"))
                elif (remote_system_type in ["Linux", "Darwin"]):
                    for line in imported_content.split('\n'):
                        print(execute_command_on_remote_host(host, credentials, f"sudo /tmp/hostscli add {line}", True))


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
            else:
                remote_system_type = get_remote_system_type(host, credentials)
                print(replace_all(LOCALIZATION_DATA["INFO_MSG_SFTP_COPY"], { "{host}": host }))
                add_hostscli_to_remote_host(host, credentials, remote_system_type)
                print(INFO_MSG_DONE)
                if (remote_system_type == "Windows"):
                    print(execute_command_on_remote_host(f"C:\\Windows\\Temp\\hostscli.exe edit from {source1} {' '.join(targets1)} to {source2} {' '.join(targets2)}"))
                elif (remote_system_type in ["Linux", "Darwin"]):
                    print(execute_command_on_remote_host(host, credentials, f"sudo /tmp/hostscli edit from {source1} {' '.join(targets1)} to {source2} {' '.join(targets2)}", True))


    def print_hosts(hosts, credentials) -> None:
        """Prints hosts data"""
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
                    print(execute_command_on_remote_host(host, credentials, "C:\\Windows\\Temp\\hostscli.exe print"))
                elif (remote_system_type in ["Linux", "Darwin"]):
                    print(f"{host} hosts:\n")
                    print(execute_command_on_remote_host(host, credentials, f"/tmp/hostscli print"))


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
            else:
                remote_system_type = get_remote_system_type(host, credentials)
                print(replace_all(LOCALIZATION_DATA["INFO_MSG_SFTP_COPY"], { "{host}": host }))
                add_hostscli_to_remote_host(host, credentials, remote_system_type)
                print(INFO_MSG_DONE)
                if (remote_system_type == "Windows"):
                    print(execute_command_on_remote_host(host, credentials, f""))
                elif (remote_system_type in ["Linux", "Darwin"]):
                    print(execute_command_on_remote_host(host, credentials, f"sudo /tmp/hostscli rm {source} {' '.join(targets)}", True))