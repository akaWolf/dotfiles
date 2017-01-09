#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libqtile.widget import base
from X11SupportClass import X11SupportClass

class KeyboardLayoutCustom(base.InLoopPollText):
	"""Widget for changing (not yet) and displaying the current keyboard layout"""

	orientations = base.ORIENTATION_HORIZONTAL
	defaults = [
		("update_interval", 0.5, "Update time in seconds."),
	]

	def __init__(self, **config):
		base.InLoopPollText.__init__(self, **config)
		self.add_defaults(KeyboardLayoutCustom.defaults)
		self.X11 = X11SupportClass()

	def poll(self):
		return self.configured_keyboards[self.keyboard].upper()

	@property
	def configured_keyboards(self):
		"""Return the currently used keyboard layouts as a list of string"""
		return self.X11.GetLayouts()

	@property
	def keyboard(self):
		"""Return the currently used keyboard layout as a number"""
		return self.X11.GetGroup()

	@keyboard.setter
	def keyboard(self, keyboard):
		self.X11.SetGroup(keyboard)
