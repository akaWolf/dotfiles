import subprocess
from libqtile import widget
from .tooltip import TooltipMixin

ICON = ""
DND_ICON = ""


class SwayncIcon(widget.GenPollText, TooltipMixin):
	def __init__(self, **kwargs):
		widget.GenPollText.__init__(self, func=self._poll, **kwargs)
		TooltipMixin.__init__(self)
		self.add_defaults(TooltipMixin.defaults)
		self._dnd = False
		self.mouse_callbacks.setdefault("Button3", self.toggle_dnd)

	def finalize(self):
		# Иначе popup переживает reload_config, если tooltip виден в этот момент
		self._stop_tooltip(0, 0)
		super().finalize()

	def toggle_dnd(self):
		subprocess.Popen(["swaync-client", "-d", "-sw"])
		self._dnd = not self._dnd
		self.draw()

	def _poll(self):
		try:
			n = subprocess.check_output(
				["swaync-client", "-c"], text=True, timeout=2
			).strip() or "0"
		except Exception:
			n = "0"
		try:
			dnd = subprocess.check_output(
				["swaync-client", "-D"], text=True, timeout=2
			).strip() == "true"
		except Exception:
			dnd = False
		self._dnd = dnd
		self.tooltip_text = ("DND. " if dnd else "") + f"Уведомлений: {n}"
		color = "#606060" if n == "0" else "#0D47A1"
		return f'<span rise="1500" foreground="{color}">{ICON}</span>'

	def draw(self):
		if not self.can_draw():
			return
		self.drawer.clear(self.background or self.bar.background)
		self.drawer.ctx.save()
		x = self.padding if self.length_type != 1 else 0  # bar.STATIC == 1
		y = (self.bar.size - self.layout.height) / 2 + 1
		self.layout.draw(x, y)
		if self._dnd:
			ctx = self.drawer.ctx
			ctx.set_source_rgb(1.0, 0.0, 0.0)
			ctx.set_line_width(3)
			ctx.set_line_cap(1)  # cairo.LINE_CAP_ROUND
			ctx.move_to(0, y + self.layout.height)
			ctx.line_to(self.width, y)
			ctx.stroke()
		self.drawer.ctx.restore()
		self.draw_at_default_position()
