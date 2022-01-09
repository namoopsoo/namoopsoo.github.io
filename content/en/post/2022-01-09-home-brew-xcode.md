---
title: Xcode Command Line Tools on HomeBrew
date: 2022-01-09
---

Wow, I am setting up on a fresh laptop today and I just ran the typical homebrew https://brew.sh setup and when I saw this, my eyes got slightly watery.

```
==> This script will install:
/usr/local/bin/brew
...
...
==> The Xcode Command Line Tools will be installed.

Press RETURN to continue or any other key to abort:
...
==> Searching online for the Command Line Tools
==> /usr/bin/sudo /usr/bin/touch /tmp/.com.apple.dt.CommandLineTools.installondemand.in-progress
==> Installing Command Line Tools for Xcode-13.2
==> /usr/bin/sudo /usr/sbin/softwareupdate -i Command\ Line\ Tools\ for\ Xcode-13.2
Software Update Tool

Finding available software

Downloading Command Line Tools for Xcode
Downloaded Command Line Tools for Xcode
Installing Command Line Tools for Xcode
Done with Command Line Tools for Xcode
Done.
...
==> /usr/bin/sudo /bin/rm -f /tmp/.com.apple.dt.CommandLineTools.installondemand.in-progress
==> /usr/bin/sudo /usr/bin/xcode-select --switch /Library/Developer/CommandLineTools
==> Downloading and installing Homebrew...
...
```

etc.

