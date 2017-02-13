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

BOB = Struct(
    'sunsensor' / BitsInteger(10)[3],
    'paneltemp' / BitsInteger(10)[4],
    '3v3voltage' / BitsInteger(10),
    '3v3current' / BitsInteger(10),
    '5voltage' / BitsInteger(10),
)

RF = Struct(
    'rxdoppler' / Octet,
    'rxrssi' / Octet,
    'temp' / Octet,
    'rxcurrent' / Octet,
    'tx3v3current' / Octet,
    'tx5vcurrent' / Octet,
    )

PA = Struct(
    'revpwr' / Octet,
    'fwdpwr' / Octet,
    'boardtemp' / Octet,
    'boardcurr' / Octet,
    )

Ants = Struct(
    'temp' / Octet[2],
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

WholeOrbitFC1 = BitStruct(
    'tempthermistor' / BitsInteger(12)[4],
    'solarpaneltemp' / BitsInteger(10)[4],
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
