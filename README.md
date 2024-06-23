# hostscli

CLI which helps manage hosts file in terminal app


## Supported systems

- Windows
- MacOS
- Linux


## hostscli commands

### Add

```bash
hostscli add [SOURCE] [TARGETS...]
```

### Edit

```bash
hostscli edit from [SOURCE] [TARGETS...] to [SOURCE] [TARGETS]
```

### Remove

```bash
hostscli rm [SOURCE] [TARGETS...]
```

### Print

```bash
hostscli print
```

## Remote features

In 02.2306.2024 Test Build added features for remote hosts administration

### Add

```bash
hostscli add [SOURCE] [TARGETS...] [[args]]
```

Usage:

```bash
hostscli add 127.0.0.1 example.com --host 192.168.1.20 192.168.1.21 192.168.1.22 --cred login:password
```

### Edit

```bash
hostscli edit from [SOURCE] [TARGETS...] to [SOURCE] [TARGETS] [[args]]
```

Usage:

```bash
hostscli edit from 127.0.0.1 example.com to 127.0.0.1 somesite.com --host 192.168.1.20 192.168.1.21 192.168.1.22 --cred login:password
```

### Remove

```bash
hostscli rm [SOURCE] [TARGETS...] [[args]]
```

Usage:

```bash
hostscli rm 127.0.0.1 somesite.com --host 192.168.1.20 192.168.1.21 192.168.1.22 --cred login:password
```

### Print

```bash
hostscli print
```

Usage:

```bash
hostscli print --host 192.168.1.20 192.168.1.21 192.168.1.22 --cred login:password
```

## Build hostscli from source

### For Unix

```bash
pip install pyinstaller
git clone https://github.com/YeezyWhy/hostscli.git /tmp/hostscli
cd /tmp/hostscli
pip install -r requirements.txt
sh ./build.sh
```

### For Windows (using PowerShell)

```bash
pip install pyinstaller
git clone https://github.com/YeezyWhy/hostscli.git %TEMP%/hostscli
cd %TEMP%
pip install -r requirements.txt
./build.ps1
```


## TODO List

- [x] Basic functions like: add, edit, remove
- [x] Windows, MacOS support
- [ ] Remote hosts administation (in progress)
