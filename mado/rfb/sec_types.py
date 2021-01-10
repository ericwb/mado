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

    # Ultra
    ULTRA = 17

    # TLS
    TLS = 18

    # VeNCrypt
    VENCRYPT = 19

    # GTK-VNC SASL
    GTK_VNC_SASL = 20

    # MD5 hash authentication
    MD5_HASH_AUTH = 21

    # Colin Dean xvp
    COLIN_DEAN_XVP = 22

    # RealVNC = 128 to 255
