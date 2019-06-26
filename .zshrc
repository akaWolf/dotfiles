# zsh settings

# load common settings
source "$HOME/.shrc"

# history settings
export HISTSIZE=100000
export HISTFILESIZE=100000

setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_SPACE
setopt APPEND_HISTORY
setopt HIST_VERIFY
unsetopt SHARE_HISTORY

# set ZLE mode
bindkey -e

# enable completion
autoload -Uz compinit
compinit

# add custom path to autoloading functions
fpath=( "$HOME/.zfunctions" $fpath )

# prompt configuration
autoload -U promptinit; promptinit
prompt pure

# dirstack config
DIRSTACKFILE="$HOME/.cache/zsh/dirs"
if [[ -f $DIRSTACKFILE ]] && [[ $#dirstack -eq 0 ]]; then
  dirstack=( ${(f)"$(< $DIRSTACKFILE)"} )
  [[ -d $dirstack[1] ]] && cd $dirstack[1]
fi
chpwd() {
  print -l $PWD ${(u)dirstack} >$DIRSTACKFILE
}

DIRSTACKSIZE=20

setopt AUTO_PUSHD PUSHD_SILENT PUSHD_TO_HOME

## Remove duplicate entries
setopt PUSHD_IGNORE_DUPS

## This reverts the +/- operators.
setopt PUSHD_MINUS

# auto completion rehash on changes
zstyle ':completion:*' rehash true

# auto resize at app exit
ttyctl -f

# syntax highlight
source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
