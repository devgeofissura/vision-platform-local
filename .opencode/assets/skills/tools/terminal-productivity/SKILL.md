---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: terminal-productivity
description: Terminal and CLI productivity with tmux, fzf, shell aliases, and history
category: tools
version: 0.1.0
author: devtiagoabreu
tags: [terminal, cli, tmux, fzf, shell, zsh, bash, aliases]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A POSIX shell (bash or zsh) with a modern terminal emulator
  - Homebrew, apt, or dnf for installing CLI tools
  - tmux, fzf, and ripgrep installed (see usage)
provides:
  - Tmux session and pane management workflow
  - Fuzzy finding for files, history, and processes with fzf
  - A starter library of safe, high-value shell aliases
  - Configuration snippets for bash and zsh
---

# Terminal Productivity

## Overview

This skill is a practical guide to getting more done in the terminal by
combining tmux, fzf, and shell aliases into a fast, low-friction workflow. It
covers persistent sessions with tmux, fuzzy file/history navigation with fzf,
and the aliases that turn frequent long commands into two keystrokes. The goal
is to keep your hands on the keyboard and your context intact across tasks and
restarts. Everything here is configurable and applies to both bash and zsh.

## Prerequisites

- bash or zsh as your interactive shell
- `tmux`, `fzf`, `rg` (ripgrep), and `bat` installed
- A terminal emulator with truecolor support (iTerm2, kitty, GNOME Terminal,
  Windows Terminal, or similar)

## Usage Instructions

### Step 1: Install the Toolchain

```bash
# Debian/Ubuntu
sudo apt install tmux fzf ripgrep bat

# macOS
brew install tmux fzf ripgrep bat
```

Enable fzf's shell integration:

```bash
# bash
echo 'eval "$(fzf --bash)"' >> ~/.bashrc

# zsh
echo 'source <(fzf --zsh)' >> ~/.zshrc
```

### Step 2: Manage tmux Sessions

Keep long-running work alive across disconnects:

```bash
tmux new -s dev                      # create session
tmux ls                              # list sessions
tmux attach -t dev                   # reattach later
tmux detach                          # Ctrl-b d
tmux kill-session -t dev             # destroy
```

Split a window into panes with `Ctrl-b %` (vertical) and `Ctrl-b "` (horizontal).

### Step 3: Navigate Files with fzf

Replace repetitive `cd` and `find` with fuzzy search:

```bash
# Fuzzy search file paths (uses ripgrep's ignore rules)
alias f="fzf --preview 'bat --color=always --line-range=:80 {}'"
f                                   # pick a file, then run editor

# Open the picked file in your editor
alias fo='vim "$(fzf --preview "bat --color=always {}")"'
```

Use `Ctrl-r` to fuzzy-search shell history and `Ctrl-t` to insert a file path
into the current command.

### Step 4: Fuzzy Search History and Processes

Search command history and kill processes interactively:

```bash
# Ctrl-r is built in after fzf init; kill a process by fuzzy pick
alias killp='kill "$(ps aux | fzf --height 20% | awk "{print \$2}")"'

# Jump to a directory anywhere below the current tree
alias d='cd "$(find . -type d | fzf)"'
```

### Step 5: Add High-Value Aliases

Adopt a safe starter set:

```bash
# -- navigation -----------------------------------------------------------
alias ..='cd ..'
alias ...='cd ../..'
alias home='cd ~'
alias ls='ls --color=auto'          # or eza/lsd if installed
alias ll='ls -lah'

# -- git ------------------------------------------------------------------
alias gs='git status'
alias ga='git add -p'
alias gc='git commit -m'
alias gl='git log --oneline --graph --decorate -20'
alias gd='git diff'
alias gco='git checkout'
alias gb='git branch'

# -- general --------------------------------------------------------------
alias c='clear'
alias h='history | tail -50'
alias cat='bat'                     # syntax-highlighted pager
alias rg='rg --smart-case'
```

### Step 6: Persist Your Config

Make everything survive new shells and machines:

```bash
# ~/.tmux.conf
set -g base-index 1
set -g mouse on
bind r source-file ~/.tmux.conf

# git-track your dotfiles
mkdir -p ~/dotfiles && cp ~/.bashrc ~/.zshrc ~/.tmux.conf ~/dotfiles/
git -C ~/dotfiles init
```

## Examples

### Example 1: Session + Split Workflow

```bash
tmux new -s api-work
# Ctrl-b c            -> new window: run the API server
# Ctrl-b %            -> split: edit config
# Ctrl-b d            -> detach (server keeps running)
tmux attach -t api-work   # come back hours later
```

### Example 2: Fuzzy File Search Pipeline

```bash
# Find a test by name and jump to its first line
rg -l "describe\('checkout" tests | fzf --preview 'bat --color=always {}'
# -> prints the chosen path; pipe into vim
```

## References

- [tmux Manual](https://man.openbsd.org/tmux)
- [fzf README](https://github.com/junegunn/fzf)
- [Oh My Zsh](https://ohmyz.sh/)
- [ripgrep README](https://github.com/BurntSushi/ripgrep)
- [bat README](https://github.com/sharkdp/bat)
- [tz: tmux cheat sheet](https://tmuxcheatsheet.com/)

## Notes

- Rebind tmux prefix (`Ctrl-b`) to `Ctrl-a` if you came from GNU screen.
- fzf respects `.gitignore` when using `rg` as its file source.
- Prefer `eza`/`lsd` for colorized listings with icons.
- Keep aliases in a separate `~/.aliases` file sourced by both shells.
- Add aliases only after you type the long form three times.
- Version your dotfiles so setup on a new machine takes minutes.
