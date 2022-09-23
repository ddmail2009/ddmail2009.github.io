<h1 align='center'>Bashrc</h1>

My Curated list of useful tmux config which makes life easier.
Run install.py to replace your existing .tmux.conf with the updated config.

## Understanding of tmux config term/syntax

###### Session/Window/Pane

![session, window, pane explaination](https://arcolinux.com/wp-content/uploads/2020/02/tmux-server.png)
- Session
  - A tmux session is a terminal multiplexer which survive the connection even though the connection to the workstation may lost. When tmux is started, it creates a new session with a single window.
- Window
  - tmux displays one window on screen at a time. A single session can have multiple windows. 
- Pane
  - tmux window can be split by panes either vertically or horizontally. Each pane partition the window into seperate terminals.

###### Common tmux actions
Inside a tmux session, user may interact with tmux start with hitting `<Ctrl+b>`(Control+B) by default. This may often specific as `C-b` in man page or simply `Prefix`.
```sh
# Create window
C-b + c  
# Rename current window
C-b + ,  
# Close current window
C-b + &  
# Navigate to previous window
C-b + p  
# Navigate to next window
C-b + n  
# Bring up the last selected window
C-b + l  
# Go to a window with a match of a text string
C-b + f  
# Switch/select window by number
C-b + 0 … 9  
```


###### Launch tmux
```sh
# Start a new tmux session
tmux

# Start a named session
tmux new -s ${NAME}

# Show current existing sessions
tmux ls

# Attach to an existing tmux session
tmux --attach

# Attach to an existing tmux session by name
tmux --attach-session -t 0

```

## Default .tmux.conf
```sh
# Start the windows and panes index from 1, not 0
set -g base-index 1
set -g pane-base-index 1

# Show two line version of status bar
set -g status 2

# Automatically set window title
set-window-option -g automatic-rename on
set-option -g set-titles on

# Set scrollback buffer to 10000
set -g history-limit 10000
```


#### TEMP
```sh
# 0 is too far from ` ;)
set -g base-index 1

# Automatically set window title
set-window-option -g automatic-rename on
set-option -g set-titles on

set -g default-terminal screen-256color
set -g status-keys vi
# Set Scroll history
set -g history-limit 30000

# Make mouse useful in copy mode
setw -g mode-keys vi
# Allow mouse interation
set -g mouse on

setw -g monitor-activity on

bind-key v split-window -h
bind-key s split-window -v

# Use Alt-arrow keys without prefix key to switch panes
bind -n C-Left select-pane -L
bind -n C-Right select-pane -R
bind -n C-Up select-pane -U
bind -n C-Down select-pane -D

# Shift arrow to switch windows or move pane to/from window
bind -n S-Left  previous-window
bind -n S-Right next-window
bind -n S-Down command-prompt -p "join pane from:" "join-pane -s '%%'"
bind -n S-Up command-prompt -p "send pane to:" "join-pane -t '%%'"

# Move x clipboard from/to tmux paste buffer
bind C-p run "tmux set-buffer \"$(xclip -o)\"; tmux paste-buffer"
bind C-y run "tmux show-buffer | xclip -i"

# No delay for escape key press
set -sg escape-time 0

# Reload tmux config
bind r source-file ~/.tmux.conf

# THEME
set -g status-bg black
set -g status-fg yellow
set -g status-interval 60
set -g status-left-length 30
set -g status-left '#[fg=green](#S) #(whoami) '
set -g status-right "#[fg=colour088]#I:#W #[fg=colour232]#h #[fg=colour255]%r"
set -g window-status-format `#[fg=yellow,bg=default]#I:#W`
set -g window-status-current-format `#[fg=black,bg=yellow]#I:#W`
set-window-option -g monitor-activity off
set-window-option -g monitor-silence 0

# renumber window after window closed.
set -g renumber-windows on

# List of plugins
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'ChanderG/tmux-notify'


# Initialize TMUX plugin manager (keep this line at the very bottom of tmux.conf)
run '~/.tmux/plugins/tpm/tpm'
```

