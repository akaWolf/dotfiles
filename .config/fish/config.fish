# load usefull aliases
test -s ~/.fish_aliases && source ~/.fish_aliases || true

# add ~/bin to PATH
test -d ~/bin && set PATH ~/bin $PATH

# set editor
set -xg EDITOR qtcreator-client

# Set GPG TTY
set -xg GPG_TTY $tty

# Refresh gpg-agent tty in case user switches into an X session
gpg-connect-agent updatestartuptty /bye > /dev/null

# nnn: edit all files in EDITOR
set -xg NNN_USE_EDITOR 1
