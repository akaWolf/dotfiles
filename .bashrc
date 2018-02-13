#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

# set prompt settings
#PS1='[\u@\h \W]\$ '
#export PS1="\${debian_chroot:+(\$debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ "
export GITAWAREPROMPT=~/.bash/git-aware-prompt
. "${GITAWAREPROMPT}/main.sh"
export PS1="\${debian_chroot:+(\$debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\] \[$txtcyn\]\$git_branch\[$txtred\]\$git_dirty\[$txtrst\]\$ "

# set command-not-found handler
. /usr/share/doc/pkgfile/command-not-found.bash

# load usefull aliases
test -s ~/.bash_aliases && . ~/.bash_aliases || true

# add ~/bin to PATH
test -d ~/bin && PATH=~/bin:$PATH

# set editor
export EDITOR=qtcreator-client

# hist settings
export HISTCONTROL=ignoreboth	# ignorespace + ignoredups
export HISTSIZE=1000000			# big big history
export HISTFILESIZE=$HISTSIZE
#export HISTTIMEFORMAT="%h %d %H:%M:%S> "
shopt -s histappend				# append to history, don't overwrite it

# Set GPG TTY
export GPG_TTY=$(tty)

# Refresh gpg-agent tty in case user switches into an X session
gpg-connect-agent updatestartuptty /bye >/dev/null

# nnn: edit all files in EDITOR
export NNN_USE_EDITOR=1
