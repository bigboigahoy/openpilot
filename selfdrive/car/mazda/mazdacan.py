from openpilot.selfdrive.car.mazda.values import Buttons, MazdaFlags, GEN1


def create_steering_control(packer, CP, frame, apply_steer, lkas):

  tmp = apply_steer + 2048

  lo = tmp & 0xFF
  hi = tmp >> 8

  # copy values from camera
  b1 = int(lkas["BIT_1"])
  er1 = int(lkas["ERR_BIT_1"])
  lnv = 0
  ldw = 0
  er2 = int(lkas["ERR_BIT_2"])

  # Some older models do have these, newer models don't.
  # Either way, they all work just fine if set to zero.
  steering_angle = 0
  b2 = 0

  tmp = steering_angle + 2048
  ahi = tmp >> 10
  amd = (tmp & 0x3FF) >> 2
  amd = (amd >> 4) | (( amd & 0xF) << 4)
  alo = (tmp & 0x3) << 2

  ctr = frame % 16
  # bytes:     [    1  ] [ 2 ] [             3               ]  [           4         ]
  csum = 249 - ctr - hi - lo - (lnv << 3) - er1 - (ldw << 7) - ( er2 << 4) - (b1 << 5)

  # bytes      [ 5 ] [ 6 ] [    7   ]
  csum = csum - ahi - amd - alo - b2

  if ahi == 1:
    csum = csum + 15

  if csum < 0:
    if csum < -256:
      csum = csum + 512
    else:
      csum = csum + 256

  csum = csum % 256

  values = {}
  if CP.flags & MazdaFlags.GEN1:
    values = {
      "LKAS_REQUEST": apply_steer,
      "CTR": ctr,
      "ERR_BIT_1": er1,
      "LINE_NOT_VISIBLE" : lnv,
      "LDW": ldw,
      "BIT_1": b1,
      "ERR_BIT_2": er2,
      "STEERING_ANGLE": steering_angle,
      "ANGLE_ENABLED": b2,
      "CHKSUM": csum
    }

  return packer.make_can_msg("CAM_LKAS", 0, values)


def create_alert_command(packer, cam_msg: dict, ldw: bool, steer_required: bool):
  values = {s: cam_msg[s] for s in [
    "LINE_VISIBLE",
    "LINE_NOT_VISIBLE",
    "LANE_LINES",
    "BIT1",
    "BIT2",
    "BIT3",
    "NO_ERR_BIT",
    "S1",
    "S1_HBEAM",
  ]}
  values.update({
    # TODO: what's the difference between all these? do we need to send all?
    "HANDS_WARN_3_BITS": 0b111 if steer_required else 0,
    "HANDS_ON_STEER_WARN": steer_required,
    "HANDS_ON_STEER_WARN_2": steer_required,
    "LINE_VISIBLE":       1,
    "LINE_NOT_VISIBLE":   0,
    "LANE_LINES":         2,
    "BIT1":               1,

    # TODO: right lane works, left doesn't
    # TODO: need to do something about L/R
    "LDW_WARN_LL": 0,
    "LDW_WARN_RL": 0,
  })
  return packer.make_can_msg("CAM_LANEINFO", 0, values)


def create_button_cmd(packer, CP, counter, button):

  can = int(button == Buttons.CANCEL)
  res = int(button == Buttons.RESUME)

  if CP.flags & MazdaFlags.GEN1:
    values = {
      "CAN_OFF": can,
      "CAN_OFF_INV": (can + 1) % 2,

      "SET_P": 0,
      "SET_P_INV": 1,

      "RES": res,
      "RES_INV": (res + 1) % 2,

      "SET_M": 0,
      "SET_M_INV": 1,

      "DISTANCE_LESS": 0,
      "DISTANCE_LESS_INV": 1,

      "DISTANCE_MORE": 0,
      "DISTANCE_MORE_INV": 1,

      "MODE_X": 0,
      "MODE_X_INV": 1,

      "MODE_Y": 0,
      "MODE_Y_INV": 1,

      "BIT1": 1,
      "BIT2": 1,
      "BIT3": 1,
      "CTR": (counter + 1) % 16,
    }

    return packer.make_can_msg("CRZ_BTNS", 0, values)


def create_radar_command(packer, car_fingerprint, frame, CC, CS, hold):
  #accel = 0
  ret = []
  # crz_ctrl = CS.crz_cntr
  # crz_info = CS.crz_info
  # crz_ctrl = dict()
  # crz_info = dict()
  active = int(CC.longActive)

  if True: # this is set true in longcontrol.py
    accel = CC.actuators.accel * 1150
    accel = accel if accel < 1000 else 1000
  # else:
    # accel = int(crz_info["ACCEL_CMD"])

  # # TODO: LIKELY NOT ENOUGH MESSAGES FOR CRZ_INFO AND CRZ_CTRL
  # crz_info["ACC_ACTIVE"] = active
  # crz_info["ACC_SET_ALLOWED"] = int(bool(int(CS.cp.vl["GEAR"]["GEAR"]) & 4)) # we can set ACC_SET_ALLOWED bit when in drive. Allows crz to be set from 1kmh.
  # crz_info["CRZ_ENDED"] = 0 # this should keep acc on down to 5km/h on my 2018 M3
  # crz_info["ACCEL_CMD"] = accel
  # crz_info["STATIC_1"] = 0x7FF
  # crz_info["STATIC_2"] = 0
  # crz_info["STOPPING_MAYBE"] = hold
  # crz_info["STOPPING_MAYBE2"] = hold
  # crz_info["CTR1"] = frame % 6

  # crz_ctrl["CRZ_ACTIVE"] = active
  # crz_ctrl["ACC_ACTIVE_2"] = active
  # crz_ctrl["NEW_SIGNAL_2"] = 0
  # crz_ctrl["DISABLE_TIMER_1"] = 0
  # crz_ctrl["DISABLE_TIMER_2"] = 0
  # crz_ctrl["NEW_SIGNAL_7"] = 0
  # crz_ctrl["NEW_SIGNAL_1"] = 0
  # crz_ctrl["RADAR_HAS_LEAD"] = 0

  if car_fingerprint in GEN1:
    values_21B = {
        "ERROR_STATUS"      : 1,
        "ACC_ACTIVE"        : int(CC.longActive),
        "ACC_SET_ALLOWED"   : int(bool(int(CS.cp.vl["GEAR"]["GEAR"]) & 4)), # we can set ACC_SET_ALLOWED bit when in drive. Allows crz to be set from 1kmh.
        "CRZ_ENDED"         : 0, # this should keep acc on down to 5km/h on my 2018 M3
        "ACCEL_CMD"         : accel,
        "STATIC_1"          : 0x7FF,
        "STATIC_2"          : 0,
        "NEW_SIGNAL_7"      : 0,
        "CTR1"              : frame % 6
        "STOPPING_MAYBE"    : hold
        "STOPPING_MAYBE2"   : hold
    }

    values_21C = {

        "LANE_LINE_VISIBLE"           : 1,
        "NEW_SIGNAL_2"                : 0,
        "CRZ_ACTIVE"                  : int(CC.longActive),
        "ERROR_STATUS"                : 0,
        "LANE_LINE_TYPE"              : 2,
        "WARN_FLASH_IND"              : 0,
        "WARN_HUD_COLOR"              : 0,
        "STATUS"                      : 0,
        "WARN_DRSS_DISTANCE"          : 3,
        "WARN_DISTANCE_SW_STATUS"     : 0,
        "WARN_POPUP_DISPLAY_REQUEST"  : 0,
        "ACC_HAS_LEAD"                : 0,
        "DRSS_DISTANCE"               : 1,
        "WARN_PCS_FAILED"             : 0,
        "WARN_ACC_DEACTIVATED"        : 0,
        "WARN_ACC_FAILED"             : 0,
        "WARN_FSC_STATUS"             : 0,
        "a_3"                         : 0,
        "WARN_DRSS_FAILED"            : 0,
        "BRAKE_WARN"                  : 0,
        "CRZ_ACTIVE_2"                : int(CC.longActive),
        "WARN_RADAR_BLOCKED"          : 0,
        "NEW_SIGNAL_1"                : 0,
    }


  ret.append(packer.make_can_msg("CRZ_INFO", 0, values_21B))
  ret.append(packer.make_can_msg("CRZ_CTRL", 0, values_21C))

  return ret