from libqtile.widget import base
from libqtile.command.base import expose_command


class KeyboardGroup(base.InLoopPollText):
	"""Widget for displaying the current XKB keyboard group on Wayland.
	Updated from a monkey-patched handle_keyboard_key that detects
	ISO_Next_Group without creating a key binding (to avoid key repeat)."""

	defaults = [
		("update_interval", 0.5, "Update time in seconds."),
		("configured_keyboards", ["us", "ru"], "Layout names to display"),
	]

	def __init__(self, **config):
		base.InLoopPollText.__init__(self, **config)
		self.add_defaults(KeyboardGroup.defaults)
		self._current_index = 0

	@expose_command()
	def next_keyboard(self):
		self._current_index = (self._current_index + 1) % len(self.configured_keyboards)
		self.tick()

	def poll(self):
		return self.configured_keyboards[self._current_index].upper()
