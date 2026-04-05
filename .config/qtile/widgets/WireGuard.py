import os
import subprocess
from libqtile import widget
from libqtile.popup import Popup

from widgets.wg_interface import is_active, get_statistics
from widgets.wg_config import wg_config
from widgets.utils import humanize_size


class WireGuard(widget.Image):
    """WireGuard VPN status widget for Qtile.

    Shows VPN status with icons:
    - Left click: toggle VPN connection
    - Mouse hover: show statistics popup
    """

    defaults = [
        ("update_interval", 1, "Update interval in seconds."),
        (
            "icon_active",
            "~/.config/qtile/widgets/icons/wireguard_active.svg",
            "Icon for active state.",
        ),
        (
            "icon_inactive",
            "~/.config/qtile/widgets/icons/wireguard_inactive.svg",
            "Icon for inactive state.",
        ),
        ("margin_y", 7, "Vertical margin to reduce icon size."),
        ("margin_x", 5, "Horizontal margin."),
        ("popup_background", "#000000", "Popup background color."),
        ("popup_foreground", "#ffffff", "Popup text color."),
        ("popup_font", "sans", "Popup font family."),
        ("popup_fontsize", 20, "Popup font size."),
    ]

    def __init__(self, **config):
        # Expand icon paths before initialization
        icon_inactive = os.path.expanduser(
            config.get("icon_inactive", self.defaults[2][1])
        )
        icon_active = os.path.expanduser(
            config.get("icon_active", self.defaults[1][1])
        )

        # Initialize base class
        widget.Image.__init__(self, filename=icon_inactive, **config)
        self.add_defaults(WireGuard.defaults)

        # Store icon paths
        self.icon_active = icon_active
        self.icon_inactive = icon_inactive

        # State tracking
        self.is_vpn_active = None
        self.stats_text = ""
        self.popup = None
        self.popup_timer = None

        # Mouse callbacks
        self.mouse_callbacks = {
            "Button1": self.toggle_vpn,
        }

    def _configure(self, qtile, bar):
        """Configure widget when added to bar."""
        widget.Image._configure(self, qtile, bar)
        self.timeout_add(0.1, self.update_status)

    def mouse_enter(self, x, y):
        """Show popup on mouse enter with 2 second delay."""
        # Cancel any existing timer
        if self.popup_timer:
            self.popup_timer.cancel()
        # Schedule popup to show after 2 seconds
        self.popup_timer = self.timeout_add(2, self.show_stats)

    def mouse_leave(self, x, y):
        """Hide popup on mouse leave."""
        # Cancel pending popup
        if self.popup_timer:
            self.popup_timer.cancel()
            self.popup_timer = None
        # Hide if showing
        self.hide_popup()

    def update_status(self):
        """Update widget icon and stats."""
        # Check VPN status
        active = is_active()

        # Update icon if status changed
        if active != self.is_vpn_active:
            self.is_vpn_active = active
            self.filename = self.icon_active if active else self.icon_inactive

            # Force image reload
            self.img = None
            self._update_image()
            if self.bar:
                self.bar.draw()

        # Update stats text
        if active:
            try:
                rx_bytes, tx_bytes = get_statistics()
                self.stats_text = f"<b>rx:</b> {humanize_size(rx_bytes)}\n<b>tx:</b> {humanize_size(tx_bytes)}"
            except Exception:
                self.stats_text = "<b>stats unavailable</b>"
        else:
            self.stats_text = "<b>disconnected</b>"

        # Schedule next update
        self.timeout_add(self.update_interval, self.update_status)

    def show_stats(self):
        """Show stats popup."""
        # Already showing
        if self.popup:
            return

        try:
            # Create temporary popup to measure text size
            # (Popup doesn't support auto-sizing, so we need to measure first)
            temp_popup = Popup(
                self.qtile,
                x=0,
                y=0,
                width=800,
                height=200,
                background=self.popup_background,
                foreground=self.popup_foreground,
                font=self.popup_font,
                fontsize=self.popup_fontsize,
            )
            temp_popup.layout.text = self.stats_text
            text_width, text_height = temp_popup.layout.layout.get_pixel_size()
            temp_popup.kill()

            # Add padding
            padding = 15
            popup_width = text_width + padding * 2
            popup_height = text_height + padding * 2

            # Calculate position: above widget, centered horizontally
            widget_x = self.bar.x + self.offsetx
            widget_y = self.bar.y
            widget_width = self.length

            # Center popup horizontally relative to widget
            popup_x = widget_x + (widget_width - popup_width) // 2
            # Place popup above the bar with small gap
            popup_y = widget_y - popup_height - 5

            # Create popup at calculated position
            self.popup = Popup(
                self.qtile,
                x=popup_x,
                y=popup_y,
                width=popup_width,
                height=popup_height,
                background=self.popup_background,
                foreground=self.popup_foreground,
                font=self.popup_font,
                fontsize=self.popup_fontsize,
            )

            # Set text in layout
            self.popup.layout.text = self.stats_text

            self.popup.clear()
            self.popup.draw_text(x=padding, y=padding)
            self.popup.place()
            self.popup.unhide()
        except Exception:
            pass

    def hide_popup(self):
        """Hide stats popup."""
        if self.popup:
            self.popup.hide()
            self.popup = None

    def toggle_vpn(self):
        """Toggle VPN connection on left click."""
        current_status = is_active()
        cmd = wg_config.down_cmd if current_status else wg_config.up_cmd

        try:
            subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            # Force update after a short delay
            self.timeout_add(1, self.update_status)
        except Exception:
            pass
