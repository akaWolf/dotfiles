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

	# Move current window to the next stack
	Key(
		[mod, "shift"], "h",
		lazy.layout.client_to_next()
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

	# Add/Delete stack
	Key([mod], "t", lazy.layout.add()),
	Key([mod], "y", lazy.layout.delete()),

	# Close current window
	Key([mod], "w", lazy.window.kill()),

	# Restart qtile
	Key([mod, "control"], "r", lazy.restart()),

	# Close qtile
	Key([mod, "control"], "q", lazy.shutdown()),

	# Run command
	#Key([mod], "r", lazy.spawncmd(prompt = '$')),
	Key([mod], "r", lazy.spawn("dmenu_run -l 10 -fn '-16' -nf '#26292B' -nb '#FFFFFF' -sb '#606060' -sf '#FFFFFF'")),

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

dgroups_key_binder = None
dgroups_app_rules = []

layouts = [
	layout.Max(),
	layout.Stack(num_stacks = 2)
]

widget_defaults = dict(
	font = "ttf-droid",
	fontsize = 20,
	foreground = "26292B",
	background = "FFFFFF",
	padding = 3
)

screens = [
	Screen(
		bottom = bar.Bar(
			[
				widget.GroupBox(active = "26292B", inactive = "606060", urgent_text = "FF0000"),
				widget.Sep(foreground = "606060"),
				widget.Prompt(),
				#widget.WindowName(),
				widget.TaskList(border = "606060", borderwidth = 1),
				widget.Notify(),
				widget.Systray(),
				widget.Battery(battery_name = "BAT0", charge_char = "↑", discharge_char = "↓", energy_full_file = "energy_full", energy_now_file = "energy_now", error_message = "NB", power_now_file = "power_now", status_file = "status", update_delay = 5, format = "{char} {percent:2.0%}"),
				widget.Sep(foreground = "606060"),
				KeyboardLayoutCustom(update_interval = 0.1),
				#widget.KeyboardLayout(configured_keyboards = ["us intl", "ru"], update_interval = 0.1),
				widget.Sep(foreground = "606060"),
				widget.CurrentLayout(),
				#widget.Sep(foreground = "606060"),
				#widget.Volume(),
				widget.Sep(foreground = "606060"),
				widget.Clock(format = '%Y-%m-%d %a %H.%M.%S'),
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

# Controls whether or not focus follows the mouse around as it moves across windows in a layout.
follow_mouse_focus = False
# When clicked, should the window be brought to the front or not. (This sets the X Stack Mode to Above.)
bring_front_click = False
# If true, the cursor follows the focus as directed by the keyboard, warping to the center of the focused window.
cursor_warp = False

@hook.subscribe.client_new
def dialogs(window):
	if (window.window.get_wm_type() == "dialog"
		or window.window.get_wm_transient_for()):
		window.floating = True

@hook.subscribe.startup
def runner():
	startup()
	pass

# Set default rules which defines floating windows
#floating_layout = layout.Floating(float_rules=[{'wmclass': x} for x in ('file_progress', "notification", "toolbar", "splash", "dialog")])
# If a window requests to be fullscreen, it is automatically fullscreened. Set this to false if you only want windows to be fullscreen if you ask them to be.
auto_fullscreen = True

def startup():
	import os
	import glob
	home = os.path.expanduser("~")
	prog_files = glob.glob(home + "/.config/autostart/*.desktop")
	progs = []

	for prog in prog_files:
		try:
			executable = ""
			with open(prog, 'r') as prog_f:
				for line in prog_f:
					if line.startswith('Exec='):
						executable = line[5:].strip()
						break
			if executable != '':
				progs.append(executable)
		except:
			print("qtile: can't open " + prog)

	for prog in progs:
		runInBackground(prog)

	runInBackground("feh --bg-scale " + home + "/theme_ntp_background.png", "set background")

	runInBackground("xsetroot -cursor_name left_ptr", "set cursor")

	runInBackground("setxkbmap -model pc104 -layout us,ru -variant intl-unicode, -option '' -option grp:caps_toggle -option terminate:ctrl_alt_bksp", "set layouts")

	runInBackground("/usr/lib/polkit-kde-authentication-agent-1", "authentication agent polkit-kde-agent")

	runInBackground("udiskie --smart-tray --use-udisks2", "udisks2 automounter (mount helper)")

def runInBackground(prog, descr = None):
	import subprocess

	try:
		progspl = prog.split(" ")
		progname = progspl[0]
	except:
		print("qtile: error: can't parse " + prog)

	print("qtile: starting " + prog)

	#killProcWithDelay(progname)
	if isProcRunning(progname):
		print("qtile: already started " + prog)
		return

	try:
		if descr != None:
			print("\t" + descr)
		subprocess.Popen(progspl)
	except:
		print("qtile: error: can't start " + progname)

import psutil
def isProcRunning(processName):
	flag = False
	for pid in psutil.pids():
		try:
			proc = psutil.Process(pid)
		except:
			continue
		if proc.name() == processName:
			flag = True
			break
	return flag

import subprocess
import os
import signal
import sys
import time
def killProcWithDelay(processName):
	MAXDELAY = 3 # in seconds
	proc = subprocess.Popen(["pgrep", processName], stdout = subprocess.PIPE)
	for pid in proc.stdout:
		# TODO: SIGKILL or SIGABORT after unsuccessfull SIGTERM
		os.kill(int(pid), signal.SIGTERM)
		timetosleep = 0.1
		while timetosleep <= MAXDELAY:
			time.sleep(timetosleep)
			# Check if the process that we killed is alive.
			try:
				os.kill(int(pid), 0)
			except OSError as ex:
				break
			timetosleep *= 2
		if timetosleep > MAXDELAY:
			print("qtile: wasn't able to kill the process " + processName)
			break
		else:
			print("qtile: successfully killed " + processName)
