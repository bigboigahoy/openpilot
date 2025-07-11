#!/usr/bin/env python3
from cereal import car, custom
from openpilot.common.conversions import Conversions as CV
from openpilot.selfdrive.car.mazda.values import CAR, LKAS_LIMITS, MazdaFlags, GEN1
from openpilot.selfdrive.car import create_button_events, get_safety_config
from openpilot.selfdrive.car.interfaces import CarInterfaceBase
from panda import Panda
from openpilot.common.params import Params
from selfdrive.car.isotp_parallel_query import IsoTpParallelQuery
from openpilot.common.swaglog import cloudlog
from panda.python.uds import CONTROL_TYPE, MESSAGE_TYPE

ButtonType = car.CarState.ButtonEvent.Type
FrogPilotButtonType = custom.FrogPilotCarState.ButtonEvent.Type
EventName = car.CarEvent.EventName

class CarInterface(CarInterfaceBase):

  @staticmethod
  def _get_params(ret, candidate, fingerprint, car_fw, experimental_long, docs, frogpilot_toggles):
    ret.carName = "mazda"
    ret.safetyConfigs = [get_safety_config(car.CarParams.SafetyModel.mazda)]
    ret.radarUnavailable = True

    ret.steerActuatorDelay = 0.1
    ret.steerLimitTimer = 0.8

    ret.openpilotLongitudinalControl = True
    if candidate in GEN1:
      # ret.safetyConfigs[0].safetyParam |= Panda.FLAG_MAZDA_GEN1
      ret.experimentalLongitudinalAvailable = True
      ret.radarUnavailable = False
      ret.startingState = True
      ret.longitudinalTuning.kpBP = [0., 5., 30.]
      ret.longitudinalTuning.kpV = [1.3, 1.0, 0.7]
      ret.longitudinalTuning.kiBP = [0., 5., 20., 30.]
      ret.longitudinalTuning.kiV = [0.36, 0.23, 0.17, 0.1]
      # ret.safetyConfigs[0].safetyParam |= Panda.FLAG_MAZDA_RADAR_INTERCEPTOR



    CarInterfaceBase.configure_torque_tune(candidate, ret.lateralTuning)

    if candidate not in (CAR.MAZDA_CX5_2022, ):
      ret.minSteerSpeed = LKAS_LIMITS.DISABLE_SPEED * CV.KPH_TO_MS

    ret.centerToFront = ret.wheelbase * 0.41

    ret.enableBsm = True

    return ret

  # returns a car.CarState
  def _update(self, c, frogpilot_toggles):
    ret, fp_ret = self.CS.update(self.cp, self.cp_cam, frogpilot_toggles)

     # TODO: add button types for inc and dec
    ret.buttonEvents = [
      *create_button_events(self.CS.distance_button, self.CS.prev_distance_button, {1: ButtonType.gapAdjustCruise}),
      *create_button_events(self.CS.lkas_enabled, self.CS.lkas_previously_enabled, {1: FrogPilotButtonType.lkas}),
    ]

    # events
    events = self.create_common_events(ret)

    if self.CS.lkas_disabled:
      events.add(EventName.lkasDisabled)
    elif self.CS.low_speed_alert:
      events.add(EventName.belowSteerSpeed)

    ret.events = events.to_msg()

    return ret, fp_ret


  @staticmethod
  def init(CP, logcan, sendcan):
    if CP.openpilotLongitudinalControl:
      # Disable radar
      bus = 0
      addr = 0x764

      EXT_DIAG_REQUEST = b'\x10\x02'
      EXT_DIAG_RESPONSE = b'\x50\02'
      query = IsoTpParallelQuery(sendcan, logcan, bus, [addr], [EXT_DIAG_REQUEST], [EXT_DIAG_RESPONSE], debug=False)
      resp = query.get_data(2)

      if not len(resp):
        cloudlog.warning("failed to enter diagnostic session...")
        return

      sub_function = CONTROL_TYPE.DISABLE_RX_DISABLE_TX
      communication_type = MESSAGE_TYPE.NORMAL
      COMM_CONT_REQUEST = b'\x28' + int.to_bytes(sub_function, 1, byteorder="big") + int.to_bytes(communication_type, 1, byteorder="big")
      COM_CONT_RESPONSE = b' '
      query = IsoTpParallelQuery(sendcan, logcan, bus, [addr], [COMM_CONT_REQUEST], [COM_CONT_RESPONSE], debug=False)
      resp = query.get_data(2)

      if not len(resp):
        cloudlog.warning("failed to disable ecu...")
        return