#
#
#

from gi.repository import Gtk
import ui
from logitech.devices.constants import (STATUS, PROPS)


def create(window, menu_actions=None):
	icon = Gtk.StatusIcon()
	icon.set_title(window.get_title())
	icon.set_name(window.get_title())
	icon.set_from_icon_name(ui.appicon(0))

	icon.connect('activate', window.toggle_visible)

	menu = Gtk.Menu()
	for action in menu_actions or ():
		if action:
			menu.append(action.create_menu_item())

	menu.append(ui.action.quit.create_menu_item())
	menu.show_all()

	icon.connect('popup_menu',
					lambda icon, button, time, menu:
						menu.popup(None, None, icon.position_menu, icon, button, time),
					menu)

	return icon


def update(icon, receiver):
	icon.set_from_icon_name(ui.appicon(receiver.status))

	# device_with_battery = None

	if receiver.devices:
		lines = []
		if receiver.status < STATUS.CONNECTED:
			lines += (receiver.status_text, '')

		devlist = list(receiver.devices.values())
		devlist.sort(lambda x, y: x.number < y.number)
		for dev in devlist:
			name = '<b>' + dev.name + '</b>'
			if dev.status < STATUS.CONNECTED:
				lines.append(name + ' (' + dev.status_text + ')')
			else:
				lines.append(name)
				if dev.status > STATUS.CONNECTED:
					lines.append('    ' + dev.status_text)
			lines.append('')

			# if device_with_battery is None and PROPS.BATTERY_LEVEL in dev.props:
			# 	device_with_battery = dev

		text = '\n'.join(lines).rstrip('\n')
		icon.set_tooltip_markup(ui.NAME + ':\n' + text)
	else:
		icon.set_tooltip_text(ui.NAME + ': ' + receiver.status_text)
