"""Monkey-patch qtile-wayland to dispatch pointer enter/leave to bar widgets.

Core qtile's Wayland backend wires cursor motion only to per-window focus and
button-drag motion; bar widgets never receive mouse_enter / mouse_leave, so
hover-driven UI (TooltipMixin and the like) doesn't fire. This patch wraps
Core.handle_cursor_motion to also locate the widget under the cursor and
dispatch enter/leave when it changes. No-op on the X11 backend.
"""

from libqtile import hook, qtile
from libqtile.log_utils import logger


def _bar_rect(bar):
	scr = bar.screen
	if bar is scr.top:
		return scr.x, scr.y, scr.width, bar.size
	if bar is scr.bottom:
		return scr.x, scr.y + scr.height - bar.size, scr.width, bar.size
	if bar is scr.left:
		return scr.x, scr.y, bar.size, scr.height
	if bar is scr.right:
		return scr.x + scr.width - bar.size, scr.y, bar.size, scr.height
	return None


def _bar_at(qtile_obj, gx, gy):
	for screen in qtile_obj.screens:
		for bar in (screen.top, screen.bottom, screen.left, screen.right):
			if bar is None:
				continue
			rect = _bar_rect(bar)
			if rect is None:
				continue
			bx, by, bw, bh = rect
			if bx <= gx < bx + bw and by <= gy < by + bh:
				return bar, gx - bx, gy - by
	return None, 0, 0


def install():
	if qtile is None or qtile.core.name != "wayland":
		return
	core = qtile.core
	cls = type(core)
	# Bind to the unwrapped class methods so re-installs don't nest.
	orig_motion = lambda: cls.handle_cursor_motion(core)

	state = {"widget": None}

	def patched_motion():
		orig_motion()
		try:
			gx = int(core.qw_cursor.cursor.x)
			gy = int(core.qw_cursor.cursor.y)
			bar, lx, ly = _bar_at(qtile, gx, gy)
			cur = bar.get_widget_in_position(lx, ly) if bar else None
			if cur is not state["widget"]:
				prev = state["widget"]
				if prev is not None:
					try:
						prev.mouse_leave(0, 0)
					except Exception:
						logger.exception("widget.mouse_leave failed")
				if cur is not None:
					try:
						cur.mouse_enter(lx - cur.offsetx, ly - cur.offsety)
					except Exception:
						logger.exception("widget.mouse_enter failed")
				state["widget"] = cur
		except Exception:
			logger.exception("hover patch failed")

	core.handle_cursor_motion = patched_motion


@hook.subscribe.startup_complete
def _on_startup_complete():
	install()


# Also install at module load (handles `qtile cmd-obj reload_config` paths
# where startup_complete doesn't fire).
install()
