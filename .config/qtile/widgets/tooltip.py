"""TooltipMixin ported from qtile-extras (BSD-3 licensed).

Adjusted vs. upstream: Popup is created with a size estimated up-front from
text length × font size (instead of created huge then shrunk), because in the
qtile Wayland backend the post-creation resize leaves the cairo surface
oversized and only a tiny corner of the drawn text ends up visible.
"""

from libqtile.log_utils import logger
from libqtile.popup import Popup


class TooltipMixin:
	defaults = [
		("tooltip_delay", 1, "Time in seconds before tooltip displayed"),
		("tooltip_background", "#000000", "Background colour for tooltip"),
		("tooltip_color", "#ffffff", "Font colour for tooltip"),
		("tooltip_font", "sans", "Font for tooltip"),
		("tooltip_fontsize", 12, "Font size for tooltip"),
		("tooltip_padding", 4, "int for all sides or [vertical, horizontal]"),
	]

	def __init__(self, **kwargs):
		self._tooltip = None
		self._tooltip_timer = None
		self.tooltip_text = ""
		self.mouse_enter = self._start_tooltip
		self.mouse_leave = self._stop_tooltip
		self._tooltip_padding = None

	def _show_tooltip(self, x, y):
		if self._tooltip_padding is None:
			if isinstance(self.tooltip_padding, int):
				self._tooltip_padding = [self.tooltip_padding] * 2
			elif (
				isinstance(self.tooltip_padding, list)
				and len(self.tooltip_padding) == 2
				and all(isinstance(m, int) for m in self.tooltip_padding)
			):
				self._tooltip_padding = self.tooltip_padding
			else:
				logger.warning("Invalid tooltip padding. Defaulting to [4, 4]")
				self._tooltip_padding = [4, 4]

		fs = self.tooltip_fontsize
		text = self.tooltip_text
		lines = text.splitlines() or [""]
		est_w = max(1, int(max(len(line) for line in lines) * fs * 0.6))
		est_h = max(1, int(fs * 1.4 * len(lines)))
		width = est_w + 2 * self._tooltip_padding[1]
		height = est_h + 2 * self._tooltip_padding[0]

		self._tooltip = Popup(
			self.qtile,
			font=self.tooltip_font,
			fontsize=self.tooltip_fontsize,
			foreground=self.tooltip_color,
			background=self.tooltip_background,
			vertical_padding=self._tooltip_padding[0],
			horizontal_padding=self._tooltip_padding[1],
			wrap=False,
			width=width,
			height=height,
		)
		self._tooltip.layout.text = self.tooltip_text

		screen = self.bar.screen
		if screen.top == self.bar:
			x = min(self.offsetx, self.bar.width - width)
			y = self.bar.height
		elif screen.bottom == self.bar:
			x = min(self.offsetx, self.bar.width - width)
			y = screen.height - self.bar.height - height
		elif screen.left == self.bar:
			x = self.bar.width
			y = min(self.offsety + self.bar.window.y, screen.height - height)
		else:
			x = screen.width - self.bar.width - width
			y = min(self.offsety + self.bar.window.y, screen.height - height)
		x += screen.x
		y += screen.y

		self._tooltip.x = x
		self._tooltip.y = y
		self._tooltip.place()
		self._tooltip.draw_text()
		self._tooltip.unhide()
		self._tooltip.draw()

	def _start_tooltip(self, x, y):
		if not self.configured or not self.tooltip_text:
			return
		if not self._tooltip_timer and not self._tooltip:
			self._tooltip_timer = self.timeout_add(
				self.tooltip_delay, self._show_tooltip, (x, y)
			)

	def _stop_tooltip(self, x, y):
		if self._tooltip_timer and not self._tooltip:
			self._tooltip_timer.cancel()
			self._tooltip_timer = None
			return
		if self._tooltip is not None:
			self._tooltip.hide()
			self._tooltip.kill()
			self._tooltip = None
		self._tooltip_timer = None
