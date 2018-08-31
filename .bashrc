# bash settings

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

# load common settings
source "$HOME/.shrc"

# set prompt settings
#PS1='[\u@\h \W]\$ '
#export PS1="\${debian_chroot:+(\$debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ "
export GITAWAREPROMPT=~/.bash/git-aware-prompt
. "${GITAWAREPROMPT}/main.sh"
export PS1="\${debian_chroot:+(\$debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\] \[$txtcyn\]\$git_branch\[$txtred\]\$git_dirty\[$txtrst\]\$ "

# hist settings
export HISTCONTROL=ignoreboth	# ignorespace + ignoredups
export HISTSIZE=1000000			# big big history
export HISTFILESIZE=$HISTSIZE
#export HISTTIMEFORMAT="%h %d %H:%M:%S> "
shopt -s histappend				# append to history, don't overwrite it
