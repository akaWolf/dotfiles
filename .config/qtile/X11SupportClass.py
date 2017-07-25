# -*- coding: utf-8 -*-

from ctypes import *

#typedef struct _XkbStateRec {
#	unsigned char	group;
#	unsigned char   locked_group;
#	unsigned short	base_group;
#	unsigned short	latched_group;
#	unsigned char	mods;
#	unsigned char	base_mods;
#	unsigned char	latched_mods;
#	unsigned char	locked_mods;
#	unsigned char	compat_state;
#	unsigned char	grab_mods;
#	unsigned char	compat_grab_mods;
#	unsigned char	lookup_mods;
#	unsigned char	compat_lookup_mods;
#	unsigned short	ptr_buttons;
#} XkbStateRec,*XkbStatePtr;

class XkbStateRec(Structure):
	_fields_ = [('group', c_ubyte),
		('locked_group', c_ubyte),
		('base_group', c_ushort),
		('latched_group', c_ushort),
		('mods', c_ubyte),
		('base_mods', c_ubyte),
		('latched_mods', c_ubyte),
		('locked_mods', c_ubyte),
		('compat_state', c_ubyte),
		('grab_mods', c_ubyte),
		('compat_grab_mods', c_ubyte),
		('lookup_mods', c_ubyte),
		('compat_lookup_mods', c_ubyte),
		('ptr_buttons', c_ushort),
	]

#typedef struct _XkbRF_VarDefs {
#	char *			model;
#	char *			layout;
#	char *			variant;
#	char *			options;
#	unsigned short		sz_extra;
#	unsigned short		num_extra;
#	char *			extra_names;
#	char **			extra_values;
#} XkbRF_VarDefsRec,*XkbRF_VarDefsPtr;

class XkbRF_VarDefsRec(Structure):
	_fields_ = [('model', c_char_p),
		('layout', c_char_p),
		('variant', c_char_p),
		('options', c_char_p),
		('sz_extra', c_ushort),
		('num_extra', c_ushort),
		('extra_names', c_char_p),
		('extra_values', POINTER(c_char_p)),
	]

class X11SupportClass:
	def __init__(self):
		self.X11 = cdll.LoadLibrary('libX11.so')
		self.display = self.X11.XOpenDisplay(None)
		self.xkbfile = cdll.LoadLibrary('libxkbfile.so')
		self.state = XkbStateRec()
		self.vdr = XkbRF_VarDefsRec()

	def GetGroup(self):
		self.X11.XkbGetState(self.display, c_uint(0x0100), byref(self.state))
		return self.state.group

	def SetGroup(self, group):
		self.X11.XkbLockGroup(self.display, c_uint(0x0100), c_uint(group))
		self.X11.XFlush(self.display)

	def GetLayouts(self):
		tmp = pointer(c_char())
		self.xkbfile.XkbRF_GetNamesProp(self.display, byref(tmp), byref(self.vdr))
		return self.vdr.layout.decode('ASCII').split(',')
