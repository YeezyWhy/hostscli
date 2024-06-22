# hostscli

CLI which helps manage hosts file in terminal app


## Supported systems

- Windows
- MacOS


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

```bash
  pip install pyinstaller
  sudo ln -s ~/.local/bin/pyinstaller /usr/local/sbin/pyinstaller
  git clone https://github.com/YeezyWhy/hostscli.git /tmp/hostscli
  cd /tmp/hostscli
  sh ./build.sh
```


## TODO List

- [x] Basic functions like: add, edit, remove
- [x] Windows, MacOS support
- [ ] Linux support
- [ ] Remote hosts administation (in progress)
