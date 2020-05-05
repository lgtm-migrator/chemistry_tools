#!/usr/bin/env python3
#
#  notify.py
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

import os
import subprocess
import time


class Notify:
	def __init__(self, msg=lambda t: "Job finished in %.1f seconds" % t):
		self.msg = msg
		self.t0 = time.time()
	
	def __enter__(self):
		pass
	
	def notify(self, title, message):
		if os.environ.get('DISPLAY', ''):
			subprocess.call(['notify-send', title, message])
		else:
			print(title)
			print(message)
	
	def __exit__(self, exc_t, exc_v, tb):
		if exc_t is None:
			title = "Success"
		else:
			title = "Failure"
		self.notify(title, self.msg(time.time() - self.t0))

