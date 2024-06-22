# hostscli

CLI which helps manage hosts file in terminal app


## Supported systems

- Windows
- MacOS
- Linux


## hostscli commands

Add data to hosts file

```bash
hostscli add [SOURCE] [TARGETS...]
```

Edit data in hosts file

```bash
hostscli edit from [SOURCE] [TARGETS...] to [SOURCE] [TARGETS]
```

Remove data from hosts file

```bash
hostscli rm [SOURCE] [TARGETS...]
```

Print hostscli data

```bash
hostscli print
```

## Build hostscli from source

### For Unix

```bash
pip install pyinstaller
git clone https://github.com/YeezyWhy/hostscli.git /tmp/hostscli
cd /tmp/hostscli
sh ./build.sh
```

### For Windows (using PowerShell)

```bash
pip install pyinstaller
git clone https://github.com/YeezyWhy/hostscli.git %TEMP%/hostscli
cd %TEMP%
./build.ps1
```


## TODO List

- [x] Basic functions like: add, edit, remove
- [x] Windows, MacOS support
- [ ] Remote hosts administation (in progress)
