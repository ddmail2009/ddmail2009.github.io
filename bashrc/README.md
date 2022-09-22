<h1 align='center'>Bashrc</h1>

My Curated list of useful command for bashrc snippets that will make your work easier.
Run install.py to replace your existing bashrc and bash_aliases with the updated config.

##### Inspiration

This collection is insipred by [awesome-barshrc](https://github.com/aashutoshrathi/awesome-bashrc) and [The Ultimate Bad Ass .bashrc File](https://gist.github.com/zachbrowne/8bc414c9f30192067831fafebd14255c)

## Contents

- [Contents](#contents)
    - [Default Bashrc](#default-bashrc)
    - [Colors Definition](#colors-definition)
    - [C/C++ & Make Compile And Run](#cpp-make-compile-and-run)
    - [Git Related Commands](#git-related-commands)
    - [Useful bash alias & function](#useful-bash-alias--function)

## Default Bashrc
##### Settings and exports
```sh
# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# Source global definitions
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi

# Alias/Function definitions.
if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# Device specific configs.
if [ -f ~/.bash_config ]; then
    . ~/.bash_config
fi

# enable programmable completion features.
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi

# check the window size after each command and, if necessary, update the values of LINES and COLUMNS.
shopt -s checkwinsize

# let pattern "**" used in a pathname expansion context will match all files and zero or more directories and subdirectories.
shopt -s globstar

# Set Default permission mask
umask 022

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# colored GCC warnings and errors
export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'

# Set the default editor
export EDITOR=vim
export VISUAL=vim

# Color for manpage in less makes manpages easier to read
export LESS_TERMCAP_mb=$'\E[01;31m'        # Begin blinking
export LESS_TERMCAP_md=$'\E[01;38;5;74m'   # Begin Bold
export LESS_TERMCAP_me=$'\E[0m'            # End mode
export LESS_TERMCAP_se=$'\E[0m'            # end standout-mode
export LESS_TERMCAP_so=$'\E[01;44;33m'     # begin stadout-mode - info box
export LESS_TERMCAP_us=$'\E[04;38;5;146m'  # begin underline
export LESS_TERMCAP_ue=$'\E[0m'            # end underline
```

##### Bash Prompt
```sh
function __setprompt {
    local LAST_COMMAND=$?
    local COLOR_PROMPT=yes

    # set a fancy prompt (non-color, unless we know we "want" color)
    case "$TERM" in
        xterm-color|*-256color) COLOR_PROMPT=yes;;
    esac
    if [ -x /usr/bin/tput ] && tput setaf 1 >& /dev/null; then
        COLOR_PROMPT=yes
    else
        COLOR_PROMPT=
    fi

    if [ "${COLOR_PROMPT}" != yes ]; then 
        PS1="${debian_chroot:+($debian_chroot)}\u@\h:\w\$ "
    else
        PS1=""
        if [[ ${LAST_COMMAND} != 0 ]]; then
            PS1="${Color_BBlack}(${Color_BRed}ERROR)-(${Color_Red}Exit Code ${Color_BRed}${LAST_COMMAND}${Color_BBlack})-(${Color_Red}"
            if [[ $LAST_COMMAND == 1 ]]; then
                PS1+="General error"
            elif [ $LAST_COMMAND == 2 ]; then
                PS1+="Missing keyword, command, or permission problem"
            elif [ $LAST_COMMAND == 126 ]; then
                PS1+="Permission problem or command is not an executable"
            elif [ $LAST_COMMAND == 127 ]; then
                PS1+="Command not found"
            elif [ $LAST_COMMAND == 128 ]; then
                PS1+="Invalid argument to exit"
            elif [ $LAST_COMMAND == 129 ]; then
                PS1+="Fatal error signal 1"
            elif [ $LAST_COMMAND == 130 ]; then
                PS1+="Script terminated by Control-C"
            elif [ $LAST_COMMAND == 131 ]; then
                PS1+="Fatal error signal 3"
            elif [ $LAST_COMMAND == 132 ]; then
                PS1+="Fatal error signal 4"
            elif [ $LAST_COMMAND == 133 ]; then
                PS1+="Fatal error signal 5"
            elif [ $LAST_COMMAND == 134 ]; then
                PS1+="Fatal error signal 6"
            elif [ $LAST_COMMAND == 135 ]; then
                PS1+="Fatal error signal 7"
            elif [ $LAST_COMMAND == 136 ]; then
                PS1+="Fatal error signal 8"
            elif [ $LAST_COMMAND == 137 ]; then
                PS1+="Fatal error signal 9"
            elif [ $LAST_COMMAND -gt 255 ]; then
                PS1+="Exit status out of range"
            else
                PS1+="Unknown error code"
            fi
            PS1+="${Color_BBlack})${Color_Off}\n"
        fi
        
        # Username and Host
        PS1+="${Color_BBlue}\u@\h: "
        
        # Current Directory
        PS1+="${Color_BGreen}\$PWD${Color_Off}"

        # Date & Time
        # PS1+="${Color_BBlack}${Color_BCyan}$(date +%a) $(date +%b-'%-d')" # Date
        # PS1+=" $(date +'%-I':%M:%S%P)${Color_BBlack}" # Time

        # Git branch
        local gitPS1=$(__git_ps1)
        if [[ ! -z ${gitPS1} ]]; then
            local gitColor=${Color_Cyan}
            if ! git diff --no-ext-diff --cached --quiet; then
                # have staged file
                gitColor=${Color_BCyan}
            fi
            if ! git diff --no-ext-diff --quiet; then
                # Have unstaged file
                gitColor=${Color_BRed}
            fi
            PS1+="${gitColor}${gitPS1}${Color_BBlack}"
        fi


        PS1+="\n"

        if [[ $EUID -ne 0 ]]; then
            PS1+="${Color_Yellow}\$${Color_Off} " # Normal user
        else
            PS1+="${Color_Red}\$${Color_Off} " # Root user
        fi
    fi
}
export PROMPT_COMMAND='__setprompt'

# If set, show unstaged (*) and staged (+) next to the branch name.
export GIT_PS1_SHOWDIRTYSTATE=1

# If set, show stashed ($) next to the branch name.
export GIT_PS1_SHOWSTASHSTATE=1

# Show upstream name and versions ahead/behind upstream.
export GIT_PS1_SHOWUPSTREAM="verbose name"
```

##### Bash history
```sh
# Don't put duplicate lines in the history
export HISTCONTROL=erasedups:ignoredups

# append to the history file, don't overwrite it so if you start a new terminal, you have old session history
shopt -s histappend

# Allow ctrl-S for history navigation (with ctrl-R)
stty -ixon

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=10000
```

##### Bash auto completion
```sh
# Ignore case on auto-completion
bind "set completion-ignore-case on"

# Show auto-completion list automatically, without double tab
bind "set show-all-if-ambiguous On"
```

## Colors Definition
```sh
# Reset
export Color_Off="\[\033[0m\]"

# Regular Colors
export Color_Black="\[\033[0;30m\]"
export Color_Red="\[\033[0;31m\]"
export Color_Green="\[\033[0;32m\]"
export Color_Yellow="\[\033[0;33m\]"
export Color_Blue="\[\033[0;34m\]"
export Color_Purple="\[\033[0;35m\]"
export Color_Cyan="\[\033[0;36m\]"
export Color_White="\[\033[0;37m\]"

# Bold
export Color_BBlack="\[\033[1;30m\]"
export Color_BRed="\[\033[1;31m\]"
export Color_BGreen="\[\033[1;32m\]"
export Color_BYellow="\[\033[1;33m\]"
export Color_BBlue="\[\033[1;34m\]"
export Color_BPurple="\[\033[1;35m\]"
export Color_BCyan="\[\033[1;36m\]"
export Color_BWhite="\[\033[1;37m\]"

# Underline
export Color_UBlack="\[\033[4;30m\]"
export Color_URed="\[\033[4;31m\]"
export Color_UGreen="\[\033[4;32m\]"
export Color_UYellow="\[\033[4;33m\]"
export Color_UBlue="\[\033[4;34m\]"
export Color_UPurple="\[\033[4;35m\]"
export Color_UCyan="\[\033[4;36m\]"
export Color_UWhite="\[\033[4;37m\]"

# Background
export Color_On_Black="\[\033[40m\]"
export Color_On_Red="\[\033[41m\]"
export Color_On_Green="\[\033[42m\]"
export Color_On_Yellow="\[\033[43m\]"
export Color_On_Blue="\[\033[44m\]"
export Color_On_Purple="\[\033[45m\]"
export Color_On_Cyan="\[\033[46m\]"
export Color_On_White="\[\033[47m\]"

# High Intensty
export Color_IBlack="\[\033[0;90m\]"
export Color_IRed="\[\033[0;91m\]"
export Color_IGreen="\[\033[0;92m\]"
export Color_IYellow="\[\033[0;93m\]"
export Color_IBlue="\[\033[0;94m\]"
export Color_IPurple="\[\033[0;95m\]"
export Color_ICyan="\[\033[0;96m\]"
export Color_IWhite="\[\033[0;97m\]"

# Bold High Intensty
export Color_BIBlack="\[\033[1;90m\]"
export Color_BIRed="\[\033[1;91m\]"
export Color_BIGreen="\[\033[1;92m\]"
export Color_BIYellow="\[\033[1;93m\]"
export Color_BIBlue="\[\033[1;94m\]"
export Color_BIPurple="\[\033[1;95m\]"
export Color_BICyan="\[\033[1;96m\]"
export Color_BIWhite="\[\033[1;97m\]"

# High Intensty backgrounds
export Color_On_IBlack="\[\033[0;100m\]"
export Color_On_IRed="\[\033[0;101m\]"
export Color_On_IGreen="\[\033[0;102m\]"
export Color_On_IYellow="\[\033[0;103m\]"
export Color_On_IBlue="\[\033[0;104m\]"
export Color_On_IPurple="\[\033[10;95m\]"
export Color_On_ICyan="\[\033[0;106m\]"
export Color_On_IWhite="\[\033[0;107m\]"
```

## CPP Make Compile And Run
```sh

# Compile single file and run
function cpp-run {
    # cpp-run file-name
    echo "Compiling ${file}"
    g++ -o $(basename $file) ${file}
    ./$(basename $file)
}

# make and then make run
function make-run {
    # make-run
    make
    make run
}
```

## Git Related Commands
##### Rebase all branch and drop
```sh
function skip-branch-name {
    echo "master|main"
}

function rebase-and-drop {
    for branch in $(git for-each-ref --format='%(refname:short)' refs/heads/); do 
        git checkout ${branch}
        git rebase || echo "Failed to rebase branch ${branch}"; git rebase --abort
    done
    git checkout main
    git branch --merged | egrep -v "(^\*|skip-branch-name)" | xargs git branch -d
}

alias git-pretty-print='git log --online --pretty --graph'
```

## Useful bash alias & function
##### Alias
```sh

# Those Environmental Variable controls `ls` colors
export CLICOLOR=1
export LSCOLORS=ExFxCxDxBxegedabagacad

# General command
alias ls='ls --color=always'
alias l='ls -CF'
alias la='ls -AlhF'
alias ll='ls -alhFt'
alias df='df -h'
alias vi='vim'

# Add an "alert" alias for long running commands.  Use like so:
# sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# Make mkdir creates parent by default
alias mkdir='mkdir -p'

# Make ps prettier and shows process hierarchy tree
alias ps='ps auxf'

# Make less escape ASI 'color' escape sequences
alias less='less -R'

# make cd resolve symbolic link
alias cd='cd -P'

# cd into the old directory
alias bd='cd "$OLDPWD"'

# Search for text in all files in the current folder
alias ftext="grep -iIHrn --color=always"
```

##### Functions
```sh
# Extracts any archive(s) (if unp isn't installed)
function extract {
    for archive in $*; do
        if [ -f $archive ] ; then
            case $archive in
                *.tar.bz2)   tar xvjf $archive    ;;
                *.tar.gz)    tar xvzf $archive    ;;
                *.bz2)       bunzip2 $archive     ;;
                *.rar)       rar x $archive       ;;
                *.gz)        gunzip $archive      ;;
                *.tar)       tar xvf $archive     ;;
                *.tbz2)      tar xvjf $archive    ;;
                *.tgz)       tar xvzf $archive    ;;
                *.zip)       unzip $archive       ;;
                *.Z)         uncompress $archive  ;;
                *.7z)        7z x $archive        ;;
                *)           echo "don't know how to extract '$archive'..." ;;
            esac
        else
            echo "'$archive' is not a valid file!"
        fi
    done
}

# Goes up a specified number of directories  (i.e. up 4)
function up {
    local d=""
    limit=$1
    for ((i=1 ; i <= limit ; i++))
        do
            d=$d/..
        done
    d=$(echo $d | sed 's/^\///')
    if [ -z "$d" ]; then
        d=..
    fi
    cd $d
}
```
