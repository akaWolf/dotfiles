# load usefull aliases
test -s ~/.fish_aliases && source ~/.fish_aliases || true

# add ~/bin to PATH
test -d ~/bin && set PATH ~/bin $PATH

# set editor
set -xg EDITOR emacs-client

# set pager
set -xg PAGER most

# set GPG TTY
set -xg GPG_TTY $tty

# refresh gpg-agent tty in case user switches into an X session
gpg-connect-agent updatestartuptty /bye > /dev/null

# nnn: edit all files in EDITOR
set -xg NNN_USE_EDITOR 1

# emacs-specific
if [ -n "$INSIDE_EMACS" ]
  # dir tracking
  # see https://emacs.stackexchange.com/a/31446
  function prompt_AnSiT -e fish_prompt
    printf "\eAnSiTc %s\n" "$PWD"
  end
  # set title to nothing to prevent sending OSC escape sequences
  # see https://github.com/fish-shell/fish-shell/issues/107
  function fish_title
    true
  end
  # usefull for TRAMP, disabled for local machine
  # see https://github.com/emacs-mirror/emacs/blob/220f16cab6c40a1b0df1a5d2101c6602abbc6aae/lisp/term.el#L241
  #printf "\eAnSiTu %s\n" "$USER"
  #printf '\033AnSiTh %s\n' "$HOSTNAME"
end