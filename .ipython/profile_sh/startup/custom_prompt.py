#!/usr/bin/env python
# -*- coding: utf-8 -*-

from IPython.terminal.prompts import Prompts, Token

class TerminalInteractiveShellCustomPrompt(Prompts):
	def in_prompt_tokens(self, cli=None):
		import getpass
		#import pwd
		import os
		user = getpass.getuser()
		#user = pwd.getpwuid(os.getuid()).pw_name
		homedir = os.path.expanduser('~')
		pwd = os.getcwd()
		pwd = pwd.replace(homedir, '~', 1)
		symb = '#' if os.getuid() == 0 else '$'
		#prompt = [(Token, pwd),(Token.Prompt, ' {} '.format(symb))]
		prompt = [ (Token.PromptNum, '{}:{}{} '.format(user, pwd, symb)) ]
		return prompt

	def continuation_prompt_tokens(self, cli=None, width=None):
		if width is None:
			width = self._width()
		return [ (Token.PromptNum, (' ' * (width - 5)) + '...: ') ]

	def rewrite_prompt_tokens(self):
		width = self._width()
		return [ (Token.PromptNum, ('-' * (width - 2)) + '> ') ]

	def out_prompt_tokens(self):
		return []

ip = get_ipython()
ip.prompts = TerminalInteractiveShellCustomPrompt(ip)
