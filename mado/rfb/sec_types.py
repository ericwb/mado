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

    # RSA-AES
    RSA_AES = 5

    # RSA-AES Unencrypted
    RSA_AES_UNENCRYPT = 6

    # RSA-AES Two-step
    RSA_AES_TWO_STEP = 13

    # Tight
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

    # Diffie-Hellman Authentication
    DIFFIE_HELLMAN_AUTH = 30

    # RealVNC = 128 to 255
