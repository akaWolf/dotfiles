#!/bin/sh

# Файл, который мы будем "сорсить"
WAYLAND_ENV_FILE="$HOME/.wprofile"

# Загружаем переменные, если файл существует
if [ -f "$WAYLAND_ENV_FILE" ]; then
  . "$WAYLAND_ENV_FILE"
fi

# Запускаем qtile в режиме Wayland
# Убедитесь, что у вас установлен qtile-extras для этой команды
exec qtile start -b wayland
