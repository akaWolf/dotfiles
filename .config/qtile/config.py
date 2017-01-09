from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

from KeyboardLayoutCustom import KeyboardLayoutCustom

mod = "mod4"

keys = [
	# Switch between windows in current stack pane
	Key(
		[mod], "k",
		lazy.layout.down()
	),
	Key(
		[mod], "j",
		lazy.layout.up()
	),

	# Move windows up or down in current stack
	Key(
		[mod, "control"], "k",
		lazy.layout.shuffle_down()
	),
	Key(
		[mod, "control"], "j",
		lazy.layout.shuffle_up()
	),

	# Switch window focus to other pane(s) of stack
	Key(
		[mod], "space",
		lazy.layout.next()
	),

	# Swap panes of split stack
	Key(
		[mod, "shift"], "space",
		lazy.layout.rotate()
	),

	# Toggle between split and unsplit sides of stack.
	# Split = all windows displayed
	# Unsplit = 1 window displayed, like Max layout, but still with
	# multiple stack panes
	Key(
		[mod, "shift"], "Return",
		lazy.layout.toggle_split()
	),

	# Toggle between different layouts as defined below
	Key([mod], "Tab", lazy.next_layout()),

	# Close current window
	Key([mod], "w", lazy.window.kill()),

	# Restart qtile
	Key([mod, "control"], "r", lazy.restart()),

	# Close qtile
	Key([mod, "control"], "q", lazy.shutdown()),

	# Run command
	Key([mod], "r", lazy.spawncmd(prompt = '$')),

	# PrintScreen
	Key([], "Print", lazy.spawn("spectacle")),

	# Start VT
	Key([mod], "Return", lazy.spawn("konsole")),

	# Lock screen
	Key([mod], "l", lazy.spawn("i3lock -c000000")),
]

groups = [Group(i) for i in "asdfgzxcvb"]

for i in groups:
	# mod + letter of group = switch to group
	keys.append(
		Key([mod], i.name, lazy.group[i.name].toscreen())
	)

	# mod + shift + letter of group = move focused window to group
	keys.append(
		Key([mod, "shift"], i.name, lazy.window.togroup(i.name))
	)

layouts = [
	layout.Max(),
	layout.Stack(num_stacks = 2)
]

widget_defaults = dict(
	font = "ttf-droid",
	fontsize = 16,
	foreground = "26292B",
	background = "FFFFFF",
	padding = 3
)

screens = [
	Screen(
		bottom = bar.Bar(
			[
				widget.GroupBox(active = "26292B", inactive = "606060", urgent_text = "FF0000"),
				widget.Prompt(),
				widget.Sep(foreground = "606060"),
				#widget.WindowName(),
				widget.TaskList(border = "606060", borderwidth = 1),
				widget.Notify(),
				widget.Systray(),
				widget.Sep(foreground = "606060"),
				KeyboardLayoutCustom(update_interval = 0.1),
				#widget.KeyboardLayout(configured_keyboards = ["us intl", "ru"], update_interval = 0.1),
				widget.Sep(foreground = "606060"),
				widget.CurrentLayout(),
				#widget.Sep(foreground = "606060"),
				#widget.Volume(),
				widget.Sep(foreground = "606060"),
				widget.Clock(format = '%Y-%m-%d %a %H:%M:%S'),
			],
			30,
		),
	),
]

# Drag floating layouts.
mouse = [
	Drag([mod], "Button1", lazy.window.set_position_floating(),
		start = lazy.window.get_position()),
	Drag([mod], "Button3", lazy.window.set_size_floating(),
		start = lazy.window.get_size()),
	Click([mod], "Button2", lazy.window.disable_floating())
]

@hook.subscribe.client_new
def dialogs(window):
	if (window.window.get_wm_type() == 'dialog'
		or window.window.get_wm_transient_for()):
		window.floating = True

@hook.subscribe.startup
def runner():
	#return
	import subprocess
	import os
	import glob
	# startup-script is simple a list of programs to run
	#subprocess.Popen('startup-script')
	# just a list of needed programs spawn
	#subprocess.Popen(['kmix'])
	#subprocess.Popen(['skype'])
	#subprocess.Popen(['qtox'])
	#subprocess.Popen(['pidgin'])
	#subprocess.Popen(['goldendict'])
	#subprocess.Popen(['thunderbird'])
	#subprocess.Popen(['amarok'])
	#subprocess.Popen(['python3', '1900_port.py'], cwd='/home/akawolf')

	#progs = ['kmix', 'skype', 'qtox', 'pidgin', 'goldendict', 'thunderbird', 'amarok', 'konsole']
	#progs = ['kmix', 'skype', 'qtox', 'pidgin', 'goldendict', 'thunderbird', 'deadbeef', 'konsole', 'telegram-desktop']
	#progs = ['kmix', 'skype', 'qtox', 'pidgin', 'goldendict', 'thunderbird', 'amarok', 'konsole']
	home = os.path.expanduser('~')
	prog_files = glob.glob(home + '/.config/autostart/*.desktop')
	progs = []

	for prog in prog_files:
		try:
			executable = ''
			with open(prog, 'r') as prog_f:
				for line in prog_f:
					if line.startswith('Exec='):
						executable = line[5:].strip()
						break
			if executable != '':
				progs.append(executable)
		except:
			print('can\'t open ' + prog)

	for prog in progs:
		try:
			print('starting ' + prog.split(' ').__str__())
			subprocess.Popen(prog.split(' '))
		except:
			print('error: can\'t start ' + prog)
	# terminal programs behave weird with regards to window titles
	# we open them separately and in a defined order so that the
	# client_new hook has time to group them by the window title
	# as the window title for them is the same when they open
	#subprocess.Popen(['urxvt', '-e', 'ncmpcpp-opener'])
	#subprocess.Popen(['urxvt', '-e', 'weechat-curses'])

	# set background
	try:
		os.system("feh --bg-scale ~/theme_ntp_background.png")
	except:
		print('can\'t start feh')
	# set cursor
	try:
		os.system("xsetroot -cursor_name left_ptr")
	except:
		print('can\'t start xsetroot')
	# set layouts
	try:
		os.system("setxkbmap -model pc104 -layout us,ru -variant intl-unicode, -option '' -option grp:caps_toggle -option terminate:ctrl_alt_bksp")
	except:
		print('can\'t start setxkbmap')

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating()
auto_fullscreen = True
