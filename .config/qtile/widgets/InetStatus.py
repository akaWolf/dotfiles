# ~/.config/qtile/widgets/InetStatus.py
"""Виджет статуса интернета: есть ли IPv4/IPv6-связность.

Отображение:
- «4»  — есть только IPv4
- «6»  — есть и IPv4, и IPv6
- «6!» — есть только IPv6 (v4 отвалился)
- 󰖪    — интернета нет вообще

Проверка двухступенчатая:
1. Наличие маршрута для family — UDP-connect(): только route lookup в ядре,
   мгновенно и без трафика. Отсекает ожидание таймаута, когда v6 вообще нет.
2. Реальная связность — TCP-подключение к публичным anycast-серверам
   с таймаутом, асинхронно (бар не блокируется). Трафик — один SYN-handshake
   на проверку.

Клик по виджету — внеплановая проверка. При наведении — tooltip с деталями.
"""

import asyncio
import socket

from libqtile.log_utils import logger
from libqtile.widget import base

from .tooltip import TooltipMixin


class InetStatus(base.BackgroundPoll, TooltipMixin):
	defaults = [
		("update_interval", 30, "Интервал проверки, сек."),
		("probe_timeout", 2, "Таймаут одной TCP-пробы, сек."),
		("hosts_v4", [("1.1.1.1", 443), ("8.8.8.8", 443)], "Хосты проб IPv4: (host, port), пробуются по очереди."),
		("hosts_v6", [("2606:4700:4700::1111", 443), ("2001:4860:4860::8888", 443)], "Хосты проб IPv6."),
		("text_both", "6", "Текст: есть и v4, и v6."),
		("text_v4_only", "4", "Текст: только v4."),
		("text_v6_only", "6!", "Текст: только v6."),
		("text_none", "󰖪", "Текст: инета нет."),
		("color_both", None, "Цвет при v4+v6 (None — обычный цвет виджета)."),
		("color_v4_only", None, "Цвет при только v4."),
		("color_v6_only", "#FFB300", "Цвет при только v6."),
		("color_none", "#E53935", "Цвет значка «инета нет»."),
	]

	def __init__(self, **config):
		base.BackgroundPoll.__init__(self, "…", **config)
		TooltipMixin.__init__(self)
		self.add_defaults(InetStatus.defaults)
		self.add_defaults(TooltipMixin.defaults)
		self.tooltip_text = "Ещё не проверялось"
		self.add_callbacks({"Button1": self.force_update})

	def finalize(self):
		# Иначе popup переживает reload_config, если tooltip виден в этот момент
		self._stop_tooltip(0, 0)
		super().finalize()

	@staticmethod
	def _has_route(family, probe_host):
		"""Есть ли вообще маршрут до probe_host (без отправки пакетов)."""
		try:
			with socket.socket(family, socket.SOCK_DGRAM) as s:
				s.connect(probe_host)
			return True
		except OSError:
			return False

	async def _probe_tcp(self, family, host, port):
		try:
			_, writer = await asyncio.wait_for(
				asyncio.open_connection(host=host, port=port, family=family),
				self.probe_timeout,
			)
		except (OSError, asyncio.TimeoutError):
			return False
		writer.close()
		try:
			await writer.wait_closed()
		except OSError:
			pass
		return True

	async def _check_family(self, family, hosts):
		"""Возвращает (связность есть, деталь для tooltip)."""
		if not self._has_route(family, hosts[0]):
			return False, "нет маршрута"
		for host, port in hosts:
			if await self._probe_tcp(family, host, port):
				return True, f"ok ({host})"
		return False, "маршрут есть, пробы не прошли"

	async def apoll(self):
		try:
			(v4, d4), (v6, d6) = await asyncio.gather(
				self._check_family(socket.AF_INET, self.hosts_v4),
				self._check_family(socket.AF_INET6, self.hosts_v6),
			)
		except Exception:
			logger.exception("InetStatus: ошибка проверки связности")
			return "?"
		self.tooltip_text = f"IPv4: {d4}\nIPv6: {d6}"
		return self._render(v4, v6)

	def _render(self, v4, v6):
		if v4 and v6:
			text, color = self.text_both, self.color_both
		elif v4:
			text, color = self.text_v4_only, self.color_v4_only
		elif v6:
			text, color = self.text_v6_only, self.color_v6_only
		else:
			text, color = self.text_none, self.color_none
		if color and self.markup:
			return f'<span foreground="{color}">{text}</span>'
		return text
