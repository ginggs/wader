# -*- coding: utf-8 -*-
# Copyright (C) 2011-2012  Vodafone España, S.A.
# Author:  Andrew Bird
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from wader.common.consts import WADER_CONNTYPE_USB
from core.hardware.zte import (ZTEWCDMADevicePlugin,
                                       ZTEWCDMACustomizer,
                                       ZTEWrapper)


class ZTEMF180Wrapper(ZTEWrapper):

    def send_ussd(self, ussd):
        """Sends the ussd command ``ussd``"""
        # XXX: assumes it's the same as 637U
        # MF180 wants request in ascii chars even though current
        # set might be ucs2
        return super(ZTEMF180Wrapper, self).send_ussd(ussd, force_ascii=True)


class ZTEMF180Customizer(ZTEWCDMACustomizer):
    wrapper_klass = ZTEMF180Wrapper


class ZTEMF180(ZTEWCDMADevicePlugin):
    """:class:`~core.plugin.DevicePlugin` for ZTE's MF180"""
    name = "ZTE MF180"
    version = "0.1"
    author = u"Andrew Bird"
    custom = ZTEMF180Customizer()

    __remote_name__ = "MF180"

    __properties__ = {
        'ID_VENDOR_ID': [0x19d2],
        'ID_MODEL_ID': [0x2003],
    }

    conntype = WADER_CONNTYPE_USB

zte_mf180 = ZTEMF180()
