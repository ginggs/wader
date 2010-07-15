# -*- coding: utf-8 -*-
# Copyright (C) 2006-2010  Vodafone España, S.A.
# Copyright (C) 2008-2009  Warp Networks, S.L.
# Author:  Pablo Martí
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

from wader.common import consts
from wader.common.hardware.base import build_band_dict
from wader.common.hardware.huawei import (HuaweiWCDMADevicePlugin,
                                          HuaweiWCDMACustomizer,
                                          HuaweiSIMClass,
                                          HUAWEI_BAND_DICT)


class HuaweiE220Customizer(HuaweiWCDMACustomizer):
    """
    :class:`~wader.common.hardware.huawei.HuaweiWCDMACustomizer` for the E220
    """

    # GSM/GPRS/EDGE 900/1800 MHz
    # HSDPA/UMTS 2100 MHz
    band_dict = build_band_dict(
                  HUAWEI_BAND_DICT,
                  [consts.MM_NETWORK_BAND_ANY,

                   consts.MM_NETWORK_BAND_EGSM,#  900
                   consts.MM_NETWORK_BAND_DCS, # 1800

                   consts.MM_NETWORK_BAND_U2100])


class HuaweiE220SIMClass(HuaweiSIMClass):
    """Huawei E220 SIM Class"""

    def __init__(self, sconn):
        super(HuaweiE220SIMClass, self).__init__(sconn)

    def initialize(self, set_encoding=False):
        d = super(HuaweiE220SIMClass, self).initialize(set_encoding)

        def init_cb(size):
            self.sconn.get_smsc()
            # before switching to UCS2, we need to get once the SMSC number
            # otherwise as soon as we send a SMS, the device would reset
            # as if it had been unplugged and replugged to the system

            def process_charset(charset):
                """
                Do not set charset to UCS2 if is not necessary, returns size
                """
                if charset == "UCS2":
                    return size
                else:
                    d3 = self.sconn.set_charset("UCS2")
                    d3.addCallback(lambda ignored: size)
                    return d3

            d2 = self.sconn.get_charset()
            d2.addCallback(process_charset)
            return d2

        d.addCallback(init_cb)
        return d


class HuaweiE220(HuaweiWCDMADevicePlugin):
    """:class:`~wader.common.plugin.DevicePlugin` for Huawei's E220"""
    name = "Huawei E220"
    version = "0.1"
    author = u"Pablo Martí"
    custom = HuaweiE220Customizer()
    sim_klass = HuaweiE220SIMClass

    __remote_name__ = "E220"

    __properties__ = {
        'ID_VENDOR_ID': [0x12d1],
        'ID_MODEL_ID': [0x1003, 0x1004],
    }
