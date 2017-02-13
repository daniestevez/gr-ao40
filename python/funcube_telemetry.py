#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# gr-ao40 GNU Radio OOT module for AO-40 FEC
# 
# Copyright 2017 Daniel Estevez <daniel@destevez.net>
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from construct import *

SatID = Enum(BitsInteger(2),\
                  FC1EM = 0,\
                  FC2 = 1,\
                  FC1FM = 2,\
                  extended = 3)

FrameType = Enum(BitsInteger(6),\
    WO1 = 0,\
    WO2 = 1,\
    WO3 = 2,\
    WO4 = 3,\
    WO5 = 4,\
    WO6 = 5,\
    WO7 = 6,\
    WO8 = 7,\
    WO9 = 8,\
    WO10 = 9,\
    WO11 = 10,\
    WO12 = 11,\
    HR1 = 12,\
    FM1 = 13,\
    FM2 = 14,\
    FM3 = 15,\
    HR2 = 16,\
    FM4 = 17,\
    FM5 = 18,\
    FM6 = 19,\
    HR3 = 20,\
    FM7 = 21,\
    FM8 = 22,\
    FM9 = 23)

class FrameTypeAdapter(Adapter):
    def _encode(self, obj, context):
        return obj.value
    def _decode(self, obj, context):
        return FrameType(obj)

FrameTypeField = FrameTypeAdapter(BitsInteger(6))

Header = BitStruct(
    'satid' / SatID,
    'frametype' / FrameType,
    )

EPSFC1 = Struct(
    'photovoltage' / BitsInteger(16)[3],
    'photocurrent' / BitsInteger(16),
    'batteryvoltage' / BitsInteger(16),
    'systemcurrent' / BitsInteger(16),
    'rebootcount' / BitsInteger(16),
    'softwareerrors' / BitsInteger(16),
    'boostconvertertemp' / Octet[3],
    'batterytemp' / Octet,
    'latchupcount5v' / Octet,
    'latchupcount3v3' / Octet,
    'resetcause' / Octet,
    'MPPTmode' / Octet,
    )

class TempXpAdapter(Adapter):
    def _encode(self, obj, context):
        return int((obj-158.239)/-0.2073)
    def _decode(self, obj, context):
        return -0.2073*obj + 158.239
TempXp = TempXpAdapter(BitsInteger(10))
class TempXmAdapter(Adapter):
    def _encode(self, obj, context):
        return int((obj-159.227)/-0.2083)
    def _decode(self, obj, context):
        return -0.2083*obj + 159.227
TempXm = TempXmAdapter(BitsInteger(10))
class TempYpAdapter(Adapter):
    def _encode(self, obj, context):
        return int((obj-158.656)/-0.2076)
    def _decode(self, obj, context):
        return -0.2076*obj + 158.656
TempYp = TempYpAdapter(BitsInteger(10))
class TempYmAdapter(Adapter):
    def _encode(self, obj, context):
        return int((obj-159.045)/-0.2087)
    def _decode(self, obj, context):
        return -0.2087*obj + 159.045
TempYm = TempYmAdapter(BitsInteger(10))

class V3v3Adapter(Adapter):
    def _encode(self, obj, context):
        return int(obj/4.0)
    def _decode(self, obj, context):
        return 4*obj
V3v3 = V3v3Adapter(BitsInteger(10))

class V5vAdapter(Adapter):
    def _encode(self, obj, context):
        return int(obj/6.0)
    def _decode(self, obj, context):
        return 6*obj
V5v = V5vAdapter(BitsInteger(10))

BOB = Struct(
    'sunsensor' / BitsInteger(10)[3],
    'paneltempX+' / TempXp,
    'paneltempX-' / TempXm,
    'paneltempY+' / TempYp,
    'paneltempY-' / TempYm,
    '3v3voltage' / V3v3,
    '3v3current' / BitsInteger(10),
    '5voltage' / V5v,
)

class RFTempAdapter(Adapter):
    def _encode(self, obj, context):
        return int((obj-193.672)/-0.857)
    def _decode(self, obj, context):
        return -0.857*obj + 193.672
RFTemp = RFTempAdapter(Octet)

class RXCurrAdapter(Adapter):
    def _encode(self, obj, context):
        return int(obj/0.636)
    def _decode(self, obj, context):
        return 0.636*obj
RXCurr = RXCurrAdapter(Octet)

class TXCurrAdapter(Adapter):
    def _encode(self, obj, context):
        return int(obj/1.272)
    def _decode(self, obj, context):
        return 1.272*obj
TXCurr = TXCurrAdapter(Octet)

RF = Struct(
    'rxdoppler' / Octet,
    'rxrssi' / Octet,
    'temp' / RFTemp,
    'rxcurrent' / RXCurr,
    'tx3v3current' / RXCurr,
    'tx5vcurrent' / TXCurr,
    )

class PwrAdapter(Adapter):
    def _encode(self, obj, context):
        return int((obj/5e-3)**(1.0/2.0629))
    def _decode(self, obj, context):
        return 5e-3*obj**2.0629
Pwr = PwrAdapter(Octet)

class PACurrAdapter(Adapter):
    def _encode(self, obj, context):
        return int((obj-2.5435)/0.5496)
    def _decode(self, obj, context):
        return 0.5496*obj + 2.5435
PACurr = PACurrAdapter(Octet)

PA = Struct(
    'revpwr' / Pwr,
    'fwdpwr' / Pwr,
    'boardtemp' / Octet, # TODO use lookup table
    'boardcurr' / PACurr,
    )

Ants = Struct(
    'temp' / Octet[2], # TODO use ISIS manual
    'deployment' / Flag[4],
    )

SWFC1 = Struct(
    'seqnumber' / BitsInteger(24),
    'dtmfcmdcount' / BitsInteger(6),
    'dtmflastcmd' / BitsInteger(5),
    'dtmfcmdsuccess' / Flag,
    'datavalid' / Flag[7],
    'eclipse' / Flag,
    'safemode' / Flag,
    'hwabf' / Flag,
    'swabf' / Flag,
    'deploymentwait' / Flag,
    )

RealTimeFC1 = BitStruct(
    'eps' / EPSFC1,
    'bob' / BOB,
    'rf' / RF,
    'pa' / PA,
    'ants' / Ants,
    'sw' / SWFC1,
    )

HighResolution = BitStruct(
    'sunsensor' / BitsInteger(10)[5],
    'photocurrent' / BitsInteger(15),
    'batteryvoltage' / BitsInteger(15),
    )

HRPayload = HighResolution[20]

class TempBlackChassisAdapter(Adapter):
    def _encode(self, obj, context):
        return int((obj-75.244)/-0.024)
    def _decode(self, obj, context):
        return -0.024*obj + 75.244
TempBlackChassis = TempBlackChassisAdapter(BitsInteger(12))
class TempSilverChassisAdapter(Adapter):
    def _encode(self, obj, context):
        return int((obj-74.750)/-0.024)
    def _decode(self, obj, context):
        return -0.024*obj + 74.750
TempSilverChassis = TempSilverChassisAdapter(BitsInteger(12))
class TempBlackPanelAdapter(Adapter):
    def _encode(self, obj, context):
        return int((obj-75.039)/-0.024)
    def _decode(self, obj, context):
        return -0.024*obj + 75.039
TempBlackPanel = TempBlackPanelAdapter(BitsInteger(12))
class TempSilverPanelAdapter(Adapter):
    def _encode(self, obj, context):
        return int((obj-75.987)/-0.024)
    def _decode(self, obj, context):
        return -0.024*obj + 75.987
TempSilverPanel = TempSilverPanelAdapter(BitsInteger(12))

WholeOrbitFC1 = BitStruct(
    'tempblackchassis' / TempBlackChassis,
    'tempsilverchassis' / TempSilverChassis,
    'tempblackpanel' / TempBlackPanel,
    'tempsilverpanel' / TempSilverPanel,
    'paneltempX+' / TempXp,
    'paneltempX-' / TempXm,
    'paneltempY+' / TempYp,
    'paneltempY-' / TempYm,
    'photovoltage' / BitsInteger(16)[3],
    'photocurrent' / BitsInteger(16),
    'batteryvoltage' / BitsInteger(16),
    'systemcurrent' / BitsInteger(16),
)

Callsign = String(8)

FC2BatteryCommon = Struct(
    'current' / Octet,
    'voltage' / Octet,
    )

FC2Battery = Struct(
    'direction' / Flag,
    Embedded(FC2BatteryCommon),
    'temp' / Octet,
    )

EPSFC2 = Struct(
    'sunlight' / Flag,
    'solarcurrent' / BitsInteger(10)[12],
    'solartemp' / Octet,
    'batteries' / FC2Battery[3],
    'batteryheater' / Flag,
    )

SWFC2 = Struct(
    'seqnumber' / BitsInteger(24),
    'dtmfcmdcount' / BitsInteger(6),
    'dtmflastcmd' / BitsInteger(5),
    'dtmfcmdsuccess' / Flag,
    )

RealTimeFC2 = BitStruct(
    'eps' / EPSFC2,
    'antstimeout' / Octet,
    'antsstatus' / BitsInteger(12),
    'antstemp' / Octet,
    'rf' / RF,
    'pa' / PA,
    'amacmode' / BitsInteger(3),
    'magnetometer' / BitsInteger(12)[3],
    'funtrxenable' / Flag,
    'funtrxsampleenable' / Flag,
    'modemanagermode' / BitsInteger(3),
    'modemanagercommsnominal' / Flag,
    'modemanagercommsstate' / BitsInteger(2),
    'tmtcmanageridleenable' / Flag,
    'tmtceventforwarding' / Flag,
    'tcbufferreceiveenable' / BitsInteger(3),
    'tcbuffersendenable' / BitsInteger(3),
    'obcsoftresetcount' / Octet,
    'epshardresetcount' / Octet,
    Padding(20),
    'sw' / SWFC2,
    )

FC2Battery0 = Struct(
    Embedded(FC2BatteryCommon),
    'temp' / Octet,
    )

FC2Battery2 = Struct(
    'direction' / Flag,
    Embedded(FC2BatteryCommon),
    )

WholeOrbitFC2 = BitStruct(
    'tempthermistor' / BitsInteger(12)[4],
    'solartemps' / BitsInteger(8)[5],
    'battery0' / FC2Battery0,
    'battery1' / FC2Battery,
    'battery2' / FC2Battery2,
    Padding(6),
    )

Frame = Struct(
    Embedded(Header),
    'realtime' / Switch(lambda c: c.satid, {
        'FC1EM' : RealTimeFC1,
        'FC1FM' : RealTimeFC1,
        'FC2' : RealTimeFC2,
        'extended' : Bytes(55),
        }),
    'payload' / Switch(lambda c: c.frametype[:2], {
        'WO' : Bytes(200),
        'HR' : HRPayload,
        'FM' : String(200),
        }),
    )

def WholeOrbit(satid):
    if satid == 'FC1EM' or satid == 'FC1FM':
        return WholeOrbitFC1
    if satid == 'FC2':
        return WholeOrbitFC2
    return Bytes(23)

FitterMessage = String(200)

def beacon_parse(data):
    return Frame.parse(data)
