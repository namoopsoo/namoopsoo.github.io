---
title: "Chrome Fuzzy Find"
# slug: "2026-06-07--chrome-fuzzy-find"
date: 2026-06-07T15:58:16-04:00
# draft: true

# optional thumbnail
#images:
#  - "THUMBNAIL_PLACEHOLDER"
#cover:
#  image: "THUMBNAIL_PLACEHOLDER"
---


Since I have been using fuzzy find `fzf`<sup>[1](#references)</sup> lately,  switching to fzf for reverse shell search<sup>[2](#references)</sup>, I was wondering hey can I use this for switching to a chrome tab?

With a super quick trial and error session with ChatGPT, I have an Applescript answer to this question, below. 

So this works really well for me so far. Will try it out a bit more before adding it to my `~/.bash_profile`. But pretty game changing for now.

```sh
chrome-tabs-fzf() {
  local choice win tab

  choice="$(
    osascript <<'APPLESCRIPT' | fzf
tell application "Google Chrome"
  set output to ""
  repeat with w from 1 to count of windows
    repeat with t from 1 to count of tabs of window w
      set tabTitle to title of tab t of window w
      set tabURL to URL of tab t of window w
      set output to output & w & ":" & t & " | " & tabTitle & " | " & tabURL & linefeed
    end repeat
  end repeat
  return output
end tell
APPLESCRIPT
  )"

  [ -z "$choice" ] && return

  win="${choice%%:*}"
  rest="${choice#*:}"
  tab="${rest%% | *}"

  osascript <<APPLESCRIPT
tell application "Google Chrome"
  activate
  set index of window $win to 1
  set active tab index of window 1 to $tab
end tell
APPLESCRIPT
}
```

## Also extensions exist
Apparently extensions exist for chrome, called raycast an alfred, though I kind of just didn't want to add extra third party extensions to chrome, in favor of just something simpler and terminal based.

# References
1. https://github.com/junegunn/fzf.vim
2. https://michal.piekarczyk.xyz/note/2026-06-06--install-atuin/
3. https://www.raycast.com/Codely/google-chrome
