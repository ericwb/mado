# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later

class AuthException(Exception):
    """
    Exception raised when authentication has failed.
    """
    def __init__(self, secresult, reason):
        self.secresult = secresult
        self.reason = reason
