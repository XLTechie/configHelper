# -*- coding: utf-8 -*-
# configHelper.py
# Config Helper version 0.1
# Part of the NVDA screen reader (https://nvaccess.org)
# A helper module for NVDA add-ons

#    Copyright (C) 2019-2020 Luke Davis <newanswertech@gmail.com>
#
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by    the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import config
from config import ConfigObj
import re

# Used to write a dictionary of configuration values into the existing NVDA configuration dictionary
# It accepts a multi-dimensional dictionary, and overwrites existing values on conflict.
def mergeWithConfig(newValues):
	"""Merges the passed in (multi-dimensional) dictionary of NVDA configuration values into the existing NVDA config.
	Wraps dictMerge()"""
	dictMerge(config.conf, newValues)

# Merges dict b into dict a, overwriting duplicate values. Properly handles multiple dimensions.
# Only tested with strings as the final right leaf for each entry.
def dictMerge(a, b, path=None):
	"""Merges (multi-dimensional) dict b, into (multi-dimensional) dict a. Modifies a in-place and also returns it."""
	if path is None: path = []
	for key in b:
		if key in a:
			if isinstance(a[key], dict) and isinstance(b[key], dict):
				dictMerge(a[key], b[key], path + [str(key)])
			elif a[key] == b[key]:
				pass # same leaf value
			else:
				raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
		else:
			a[key] = b[key]
	return a

class Spec:
	"""
	Provides methods for reading the configspec in convenient ways.
	Uses regular expressions to do its processing.
	Caches searches and retrievals. In theory this will speed execution, but maybe pointless because of infrequency of use.
	In other words: if you retrieve the min of a value, it caches the min, max, default, etc.
	Tries to be intelligent about values, so you don't have to specify full paths.
	"""

	__init__(self, *args, **kwargs):
		self.cache = {} # Initialize the cache
		
	def min(self, requestedVal):
		return self._getFromCache(requestedVal, 'min')

	def max(self, requestedVal):
		return self._getFromCache(requestedVal, 'max')

	def default(self, requestedVal):
		return self._getFromCache(requestedVal, 'default')

	def type(self, requestedVal):
		return self._getFromCache(requestedVal, 'type')

	def _getFromCache(self, requestedVal, requestedAttr):
		"""Searches the cache for the requested value. If it's not found, caches it. If it is found, returns the requested attribute."""
		if not self._isCached(requestedVal): # If value hasn't been cached yet
			self._cache(requestedVal) # Cache it. Raises valueAmbiguousError or valueNotFoundError
		# If we got here: cache attempt was successful, or value was already cached
		return getattr(self.cache[requestedVal], requestedAttr)

	def _cache(self, requestedVal):
		"""Reads an NVDA configuration spec value, parses it into attributes, and caches it for later use."""



	def _isCached(self, requestedVal):
