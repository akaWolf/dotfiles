# -*- coding: utf-8 -*-

from cffi import FFI
ffi = FFI()

ffi.cdef('''typedef struct _XkbStateRec {
	unsigned char	group;
	unsigned char   locked_group;
	unsigned short	base_group;
	unsigned short	latched_group;
	unsigned char	mods;
	unsigned char	base_mods;
	unsigned char	latched_mods;
	unsigned char	locked_mods;
	unsigned char	compat_state;
	unsigned char	grab_mods;
	unsigned char	compat_grab_mods;
	unsigned char	lookup_mods;
	unsigned char	compat_lookup_mods;
	unsigned short	ptr_buttons;
} XkbStateRec,*XkbStatePtr;''')

ffi.cdef('void *XOpenDisplay(char *display_name);')
ffi.cdef('int XkbGetState (void *display, unsigned int device_spec, XkbStatePtr state_return);')
ffi.cdef('bool XkbLockGroup (void *display, unsigned int device_spec, unsigned int group);')
ffi.cdef('int XFlush(void *display);')

ffi.cdef('''typedef struct _XkbRF_VarDefs {
	char *			model;
	char *			layout;
	char *			variant;
	char *			options;
	unsigned short		sz_extra;
	unsigned short		num_extra;
	char *			extra_names;
	char **			extra_values;
} XkbRF_VarDefsRec,*XkbRF_VarDefsPtr;''')

ffi.cdef('bool XkbRF_GetNamesProp(void * dpy, char ** rules_file_rtrn, XkbRF_VarDefsPtr var_defs_rtrn);')

class X11SupportClass:
	def __init__(self):
		#libX11
		self.X11 = ffi.dlopen('libX11.so')
		self.display = self.X11.XOpenDisplay(ffi.NULL)
		self.state = ffi.new('XkbStateRec[1]')
		#libxkbfile
		self.xkbfile = ffi.dlopen('libxkbfile.so')
		self.vdr = ffi.new('XkbRF_VarDefsRec[1]')

	def GetGroup(self):
		self.X11.XkbGetState(self.display, 0x0100, self.state)
		return self.state[0].group

	def SetGroup(self, group):
		self.X11.XkbLockGroup(self.display, 0x0100, group)
		self.X11.XFlush(self.display)

	def GetLayouts(self):
		tmp = ffi.new('char **')
		self.xkbfile.XkbRF_GetNamesProp(self.display, tmp, self.vdr)
		return ffi.string(self.vdr[0].layout).decode('ASCII').split(',')
