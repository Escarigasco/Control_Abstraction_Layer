import syslab
import syslab.core.datatypes.CompositeMeasurement as CM
import syslab.core.datatypes.HeatCirculationPumpMode as PM
import time
import sys

_BUILDING_NAME = "716-h1"
_MULTIPLIER = 1000000
_TURN_ME_ON = 1.0
_TURN_ME_OFF = 0.0
_CONSTANT_CURVE = 0
_VALVES = 'Valves_active'
_VALVES_TO_SHUT = 'Valves_to_shut'
_PUMP = "Pump"
_SOURCE = 1
_VALIDITY = 1
_ZERO = 0


valves = ["Bay_3H-Busbar_1F", "Bay_3H-Busbar_2F", "Bay_3H-Busbar_B", "Bay_3L-Busbar_1R", "Bay_3L-Busbar_2R", "Bay_3L-Busbar_B",
          "Bay_4L-Busbar_2R", "Bay_4L-Busbar_1R", "Bay_4H-Busbar_B", "Bay_4H-Busbar_2F", "Bay_4H-Busbar_1F", "Bay_4L-Busbar_B",
          "Bay_5L-Busbar_1R", "Bay_5L-Busbar_2R", "Bay_5H-Busbar_B", "Bay_5H-Busbar_1F", "Bay_5H-Busbar_2F", "Bay_5L-Busbar_B",
          "Bay_6L-Busbar_1R", "Bay_6L-Busbar_2R", "Bay_6H-Busbar_B", "Bay_6H-Busbar_1F", "Bay_6H-Busbar_2F", "Bay_6L-Busbar_B",
          "Bay_7H-Busbar_1F", "Bay_7H-Busbar_2F", "Bay_7L-Busbar_1R", "Bay_7L-Busbar_2R",
          "Bay_8H-Busbar_1F", "Bay_8H-Busbar_2F", "Bay_8L-Busbar_1R", "Bay_8L-Busbar_2R"]
pumps = ["Pump_Bay3", "Pump_Bay4", "Pump_Bay5", "Pump_Bay6", "Pump_Bay7", "Pump_Bay8"]

interface = syslab.HeatSwitchBoard(_BUILDING_NAME)
CompositMess_Shut = CM(_TURN_ME_OFF, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
mode = PM(_CONSTANT_CURVE, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
for pump in pumps:
    interface.stopPump(pump)
    interface.setPumpControlMode(pump, mode)
    time.sleep(0.2)
for valve in valves:
    print("setpoint at 0 for valve", valve)
    interface.setValvePosition(valve, CompositMess_Shut)
    time.sleep(0.2)
