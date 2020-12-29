# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
from enum import Enum


class EncodingTypes(Enum):
   RAW = 0
   COPY_RECT = 1
   RRE = 2
   CORRE = 4
   HEXTILE = 5
   ZLIB = 6
   ZLIBHEX = 8
   TRLE = 15
   ZRLE = 16
   # RealVNC = 1024 to 1099
   CURSOR = -239
   DESKTOP_SIZE = -223
