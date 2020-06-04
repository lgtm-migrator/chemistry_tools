#!/usr/bin/env python3
#
#  rate_limiter.py
"""
Rate limiters for making calls to external APIs in a polite manner
"""
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
import datetime
import pathlib
import time
import zlib

# 3rd party
import appdirs  # type: ignore
import requests
from cachecontrol import CacheControl, CacheControlAdapter  # type: ignore
from cachecontrol.caches.file_cache import FileCache  # type: ignore
from cachecontrol.heuristics import ExpiresAfter  # type: ignore

__all__ = [
		"rate_limit",
		"RateLimitAdapter",
		"cache_dir",
		"cached_requests",
		"clear_cache",
		]


def rate_limit(func):
	"""
	Decorator to force a function to run no less than 0.2 seconds
	after it last ran (i.e. max 5 calls per second). Used for rate limiting.
	"""

	min_time = 0.2

	def rate_limit_wrapper(*args, **kwargs):
		now = datetime.datetime.now()

		time_since_last_run = (now - rate_limit_wrapper.last_run_time).total_seconds()
		print(f"Last ran {time_since_last_run} seconds ago")

		if time_since_last_run < min_time:
			wait_time = min_time - time_since_last_run
			print(f"Waiting {wait_time} seconds")
			time.sleep(wait_time)

		rate_limit_wrapper.last_run_time = now
		res = func(*args, **kwargs)
		return res

	rate_limit_wrapper.last_run_time = datetime.datetime.fromtimestamp(0)

	return rate_limit_wrapper


class RateLimitAdapter(CacheControlAdapter):

	def send(self, request, cacheable_methods=None, **kwargs):
		"""
		Send a request. Use the request information to see if it
		exists in the cache and cache the response if we need to and can.
		"""

		cacheable = cacheable_methods or self.cacheable_methods
		if request.method in cacheable:
			try:
				cached_response = self.controller.cached_request(request)
			except zlib.error:
				cached_response = None
			if cached_response:
				return self.build_response(request, cached_response, from_cache=True)

			# check for etags and add headers if appropriate
			request.headers.update(self.controller.conditional_headers(request))

		resp = self.rate_limited_send(request, **kwargs)

		return resp

	@rate_limit
	def rate_limited_send(self, *args, **kwargs):
		return super(CacheControlAdapter, self).send(*args, **kwargs)


cache_dir = pathlib.Path(appdirs.user_cache_dir("chemistry_tools"))
if not cache_dir.exists():
	cache_dir.mkdir(parents=True, exist_ok=True)

session = requests.session()

cache_adapter = CacheControlAdapter(heuristic=ExpiresAfter(days=28))
cached_requests = CacheControl(requests.Session(), cache=FileCache(cache_dir))


def clear_cache() -> None:
	import shutil
	shutil.rmtree(cache_dir)


# import codetiming

#
# class ForceMinTime:
# 	"""
# 	Decorator to force a function to take an amount of time to run.
# 	Used for rate limiting to external APIs.
#
# 	:param min_time: The minimum run time in seconds
# 	:type min_time: float
# 	"""
#
# 	def __init__(self, min_time: float):
# 		"""
# 		If there are decorator arguments, the function
# 		to be decorated is not passed to the constructor!
# 		"""
#
# 		self.min_time = min_time
#
# 	def __call__(self, func):
# 		"""
# 		If there are decorator arguments, __call__() is only called
# 		once, as part of the decoration process! You can only give
# 		it a single argument, which is the function object.
# 		"""
#
# 		def wrapper(*args, **kwargs):
# 			with codetiming.Timer(logger=None) as t:
# 				r = func(*args, **kwargs)
#
# 			sleep_time = self.min_time - t.last
# 			print(t.last)
#
# 			if sleep_time > 0:
# 				time.sleep(sleep_time)
#
# 			return r
#
# 		return wrapper
