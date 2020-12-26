# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
from enum import Enum


class SecTypes(Enum):
    # Invalid type
    INVALID = 0

    # No security type
    NONE = 1

    # VNC Authentication
    VNC_AUTH = 2

    # Tight Security Type
    TIGHT = 16

    # VeNCrypt
    VENCRYPT = 19
