# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
from enum import Enum


class SecResult(Enum):
    OK = 0
    FAILED = 1
    FAILED_TOO_MANY_ATTEMPTS = 2
