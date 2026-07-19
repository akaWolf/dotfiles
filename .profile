# if running bash
if [ -n "$BASH_VERSION" ]; then
  # include .bashrc if it exists
  if [ -f "$HOME/.bashrc" ]; then
    . "$HOME/.bashrc"
  fi
fi
#export GDK_SCALE=2
#export QT_SCALE_FACTOR=2
#export QT_FONT_DPI=170
#export MOZ_ENABLE_WAYLAND=1
#export XDG_CURRENT_DESKTOP=KDE
export XDG_CURRENT_DESKTOP=X-Generic
