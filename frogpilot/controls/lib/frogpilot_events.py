#!/usr/bin/env python3
import bisect
import random

from types import SimpleNamespace

import cereal.messaging as messaging

from cereal import log, car, custom
from openpilot.common.conversions import Conversions as CV
from openpilot.common.params import Params
from openpilot.common.realtime import DT_CTRL, DT_MDL
from openpilot.selfdrive.controls.lib.desire_helper import TurnDirection
from openpilot.selfdrive.controls.lib.events import ET, Alert, AlertCallbackType, AlertSize, AlertStatus, AudibleAlert, EventName, Events, Priority, StartupAlert, VisualAlert

from openpilot.frogpilot.assets.theme_manager import update_wheel_image
from openpilot.frogpilot.common.frogpilot_variables import CRUISING_SPEED, NON_DRIVING_GEARS, params, params_memory

FrogPilotAlertStatus = custom.FrogPilotControlsState.AlertStatus
FrogPilotAudibleAlert = custom.FrogPilotCarControl.HUDControl.AudibleAlert
FrogPilotEventName = custom.FrogPilotCarEvent.EventName

EVENT_NAME = {v: k for k, v in FrogPilotEventName.schema.enumerants.items()}

RANDOM_EVENTS_CHANCE = 0.01 * DT_MDL

class Events:
  def __init__(self):
    self.events: list[int] = []
    self.static_events: list[int] = []
    self.event_counters = dict.fromkeys(FROGPILOT_EVENTS.keys(), 0)

  @property
  def names(self) -> list[int]:
    return self.events

  def __len__(self) -> int:
    return len(self.events)

  def add(self, event_name: int, static: bool=False) -> None:
    if static:
      bisect.insort(self.static_events, event_name)
    bisect.insort(self.events, event_name)

  def clear(self) -> None:
    self.event_counters = {k: (v + 1 if k in self.events else 0) for k, v in self.event_counters.items()}
    self.events = self.static_events.copy()

  def contains(self, event_type: str) -> bool:
    return any(event_type in FROGPILOT_EVENTS.get(e, {}) for e in self.events)

  def create_alerts(self, event_types: list[str], callback_args=None):
    if callback_args is None:
      callback_args = []

    ret = []
    for e in self.events:
      types = FROGPILOT_EVENTS[e].keys()
      for et in event_types:
        if et in types:
          alert = FROGPILOT_EVENTS[e][et]
          if not isinstance(alert, Alert):
            alert = alert(*callback_args)

          if DT_CTRL * (self.event_counters[e] + 1) >= alert.creation_delay:
            alert.alert_type = f"{EVENT_NAME[e]}/{et}"
            alert.event_type = et
            ret.append(alert)
    return ret

  def add_from_msg(self, events):
    for e in events:
      bisect.insort(self.events, e.name.raw)

  def to_msg(self):
    ret = []
    for event_name in self.events:
      event = custom.FrogPilotCarEvent.new_message()
      event.name = event_name
      for event_type in FROGPILOT_EVENTS.get(event_name, {}):
        setattr(event, event_type, True)
      ret.append(event)
    return ret

def custom_startup_alert(CP: car.CarParams, CS: car.CarState, sm: messaging.SubMaster, metric: bool, soft_disable_time: int, frogpilot_toggles: SimpleNamespace) -> Alert:
  return StartupAlert(frogpilot_toggles.startup_alert_top, frogpilot_toggles.startup_alert_bottom, alert_status=FrogPilotAlertStatus.frogpilot)

def forcing_stop_alert(CP: car.CarParams, CS: car.CarState, sm: messaging.SubMaster, metric: bool, soft_disable_time: int, frogpilot_toggles: SimpleNamespace) -> Alert:
  model_length = sm["frogpilotPlan"].forcingStopLength
  model_length_msg = f"{model_length:.1f} meters" if metric else f"{model_length * CV.METER_TO_FOOT:.1f} feet"

  return Alert(
    f"Forcing the car to stop in {model_length_msg}",
    "Press the gas pedal or 'Resume' button to override",
    FrogPilotAlertStatus.frogpilot, AlertSize.mid,
    Priority.MID, VisualAlert.none, AudibleAlert.prompt, 1.)

def holiday_alert(CP: car.CarParams, CS: car.CarState, sm: messaging.SubMaster, metric: bool, soft_disable_time: int, frogpilot_toggles: SimpleNamespace) -> Alert:
  holiday_messages = {
    "new_years": "Happy New Year! 🎉",
    "valentines": "Happy Valentine's Day! ❤️",
    "st_patricks": "Happy St. Patrick's Day! 🍀",
    "world_frog_day": "Happy World Frog Day! 🐸",
    "april_fools": "Happy April Fool's Day! 🤡",
    "easter_week": "Happy Easter! 🐰",
    "may_the_fourth": "May the 4th be with you! 🚀",
    "cinco_de_mayo": "¡Feliz Cinco de Mayo! 🌮",
    "stitch_day": "Happy Stitch Day! 💙",
    "fourth_of_july": "Happy Fourth of July! 🎆",
    "halloween_week": "Happy Halloween! 🎃",
    "thanksgiving_week": "Happy Thanksgiving! 🦃",
    "christmas_week": "Merry Christmas! 🎄",
  }

  return Alert(
    holiday_messages.get(frogpilot_toggles.current_holiday_theme),
    "",
    AlertStatus.normal, AlertSize.small,
    Priority.LOWEST, VisualAlert.none, FrogPilotAudibleAlert.startup, 5.)

def no_lane_available_alert(CP: car.CarParams, CS: car.CarState, sm: messaging.SubMaster, metric: bool, soft_disable_time: int, frogpilot_toggles: SimpleNamespace) -> Alert:
  lane_width = sm["frogpilotPlan"].laneWidthLeft if CS.leftBlinker else sm["frogpilotPlan"].laneWidthRight
  lane_width_msg = f"{lane_width:.1f} meters" if metric else f"{lane_width * CV.METER_TO_FOOT:.1f} feet"

  return Alert(
    "No lane available",
    f"Detected lane width is only {lane_width_msg}",
    AlertStatus.normal, AlertSize.mid,
    Priority.LOWEST, VisualAlert.none, AudibleAlert.none, .2)

def torque_nn_load_alert(CP: car.CarParams, CS: car.CarState, sm: messaging.SubMaster, metric: bool, soft_disable_time: int, frogpilot_toggles: SimpleNamespace) -> Alert:
  model_name = params.get("NNFFModelName", encoding="utf-8")
  if model_name is None:
    return Alert(
      "NNFF Torque Controller not available",
      "Donate logs to Twilsonco to get your car supported!",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.prompt, 10.0)
  else:
    return Alert(
      "NNFF Torque Controller loaded",
      model_name,
      FrogPilotAlertStatus.frogpilot, AlertSize.mid,
      Priority.LOW, VisualAlert.none, AudibleAlert.engage, 5.0)

FROGPILOT_EVENTS: dict[int, dict[str, Alert | AlertCallbackType]] = {
  FrogPilotEventName.blockUser: {
    ET.PERMANENT: Alert(
      "Don't use the 'Development' branch!",
      "Forcing you into 'Dashcam Mode' for your safety",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.HIGHEST, VisualAlert.none, AudibleAlert.none, 1.),
  },

  FrogPilotEventName.customStartupAlert: {
    ET.PERMANENT: custom_startup_alert,
  },

  FrogPilotEventName.forcingStop: {
    ET.WARNING: forcing_stop_alert,
  },

  FrogPilotEventName.goatSteerSaturated: {
    ET.WARNING: Alert(
      "JESUS TAKE THE WHEEL!!",
      "Turn Exceeds Steering Limit",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.LOW, VisualAlert.steerRequired, FrogPilotAudibleAlert.goat, 2.),
  },

  FrogPilotEventName.greenLight: {
    ET.PERMANENT: Alert(
      "Light turned green",
      "",
      FrogPilotAlertStatus.frogpilot, AlertSize.small,
      Priority.MID, VisualAlert.none, AudibleAlert.prompt, 3.),
  },

  FrogPilotEventName.holidayActive: {
    ET.PERMANENT: holiday_alert,
  },

  FrogPilotEventName.laneChangeBlockedLoud: {
    ET.WARNING: Alert(
      "Car Detected in Blindspot",
      "",
      AlertStatus.userPrompt, AlertSize.small,
      Priority.LOW, VisualAlert.none, AudibleAlert.warningSoft, .1),
  },

  FrogPilotEventName.leadDeparting: {
    ET.PERMANENT: Alert(
      "Lead departed",
      "",
      FrogPilotAlertStatus.frogpilot, AlertSize.small,
      Priority.MID, VisualAlert.none, AudibleAlert.prompt, 3.),
  },

  FrogPilotEventName.noLaneAvailable: {
    ET.WARNING: no_lane_available_alert,
  },

  FrogPilotEventName.openpilotCrashed: {
    ET.IMMEDIATE_DISABLE: Alert(
      "openpilot crashed",
      "Please post the 'Error Log' in the FrogPilot Discord!",
      AlertStatus.normal, AlertSize.mid,
      Priority.HIGHEST, VisualAlert.none, AudibleAlert.prompt, .1),

    ET.NO_ENTRY: Alert(
      "openpilot crashed",
      "Please post the 'Error Log' in the FrogPilot Discord!",
      AlertStatus.normal, AlertSize.mid,
      Priority.HIGHEST, VisualAlert.none, AudibleAlert.prompt, .1),
  },

  FrogPilotEventName.pedalInterceptorNoBrake: {
    ET.WARNING: Alert(
      "Braking Unavailable",
      "Shift to L",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.HIGH, VisualAlert.wrongGear, AudibleAlert.promptRepeat, 4.),
  },

  FrogPilotEventName.speedLimitChanged: {
    ET.PERMANENT: Alert(
      "Speed limit changed",
      "",
      FrogPilotAlertStatus.frogpilot, AlertSize.small,
      Priority.LOW, VisualAlert.none, AudibleAlert.prompt, 3.),
  },

  FrogPilotEventName.thisIsFineSteerSaturated: {
    ET.WARNING: Alert(
      "This is fine ☕",
      "Turn Exceeds Steering Limit",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.LOW, VisualAlert.steerRequired, FrogPilotAudibleAlert.thisIsFine, 2.),
  },

  FrogPilotEventName.torqueNNLoad: {
    ET.PERMANENT: torque_nn_load_alert,
  },

  FrogPilotEventName.trafficModeActive: {
    ET.WARNING: Alert(
      "Traffic Mode enabled",
      "",
      FrogPilotAlertStatus.frogpilot, AlertSize.small,
      Priority.LOW, VisualAlert.none, AudibleAlert.prompt, 3.),
  },

  FrogPilotEventName.trafficModeInactive: {
    ET.WARNING: Alert(
      "Traffic Mode Disabled",
      "",
      FrogPilotAlertStatus.frogpilot, AlertSize.small,
      Priority.LOW, VisualAlert.none, AudibleAlert.prompt, 3.),
  },

  FrogPilotEventName.turningLeft: {
    ET.WARNING: Alert(
      "Turning left",
      "",
      AlertStatus.normal, AlertSize.small,
      Priority.LOWEST, VisualAlert.none, AudibleAlert.none, .1, alert_rate=0.75),
  },

  FrogPilotEventName.turningRight: {
    ET.WARNING: Alert(
      "Turning right",
      "",
      AlertStatus.normal, AlertSize.small,
      Priority.LOWEST, VisualAlert.none, AudibleAlert.none, .1, alert_rate=0.75),
  },

  # Random Events
  FrogPilotEventName.accel30: {
    ET.WARNING: Alert(
      "UwU u went a bit fast there!",
      "(⁄ ⁄•⁄ω⁄•⁄ ⁄)",
      FrogPilotAlertStatus.frogpilot, AlertSize.mid,
      Priority.LOW, VisualAlert.none, FrogPilotAudibleAlert.uwu, 4.),
  },

  FrogPilotEventName.accel35: {
    ET.WARNING: Alert(
      "I ain't giving you no tree-fiddy",
      "You damn Loch Ness Monsta!",
      FrogPilotAlertStatus.frogpilot, AlertSize.mid,
      Priority.LOW, VisualAlert.none, FrogPilotAudibleAlert.nessie, 4.),
  },

  FrogPilotEventName.accel40: {
    ET.WARNING: Alert(
      "Great Scott!",
      "🚗💨",
      FrogPilotAlertStatus.frogpilot, AlertSize.mid,
      Priority.LOW, VisualAlert.none, FrogPilotAudibleAlert.doc, 4.),
  },

  FrogPilotEventName.dejaVuCurve: {
    ET.WARNING: Alert(
      "♬♪ Deja vu! ᕕ(⌐■_■)ᕗ ♪♬",
      "🏎️",
      FrogPilotAlertStatus.frogpilot, AlertSize.mid,
      Priority.LOW, VisualAlert.none, FrogPilotAudibleAlert.dejaVu, 4.),
  },

  FrogPilotEventName.firefoxSteerSaturated: {
    ET.WARNING: Alert(
      "IE Has Stopped Responding...",
      "Turn Exceeds Steering Limit",
      AlertStatus.userPrompt, AlertSize.mid,
      Priority.LOW, VisualAlert.steerRequired, FrogPilotAudibleAlert.firefox, 4.),
  },

  FrogPilotEventName.hal9000: {
    ET.WARNING: Alert(
      "I'm sorry Dave",
      "I'm afraid I can't do that...",
      AlertStatus.normal, AlertSize.mid,
      Priority.HIGH, VisualAlert.none, FrogPilotAudibleAlert.hal9000, 4.),
  },

  FrogPilotEventName.openpilotCrashedRandomEvent: {
    ET.IMMEDIATE_DISABLE: Alert(
      "openpilot crashed 💩",
      "Please post the 'Error Log' in the FrogPilot Discord!",
      AlertStatus.normal, AlertSize.mid,
      Priority.HIGHEST, VisualAlert.none, FrogPilotAudibleAlert.fart, 10.),

    ET.NO_ENTRY: Alert(
      "openpilot crashed 💩",
      "Please post the 'Error Log' in the FrogPilot Discord!",
      AlertStatus.normal, AlertSize.mid,
      Priority.HIGHEST, VisualAlert.none, FrogPilotAudibleAlert.fart, 10.),
  },

  FrogPilotEventName.toBeContinued: {
    ET.PERMANENT: Alert(
      "To be continued...",
      "⬅️",
      FrogPilotAlertStatus.frogpilot, AlertSize.mid,
      Priority.MID, VisualAlert.none, FrogPilotAudibleAlert.continued, 7.),
  },

  FrogPilotEventName.vCruise69: {
    ET.WARNING: Alert(
      "Lol 69",
      "",
      FrogPilotAlertStatus.frogpilot, AlertSize.small,
      Priority.LOW, VisualAlert.none, FrogPilotAudibleAlert.noice, 2.),
  },

  FrogPilotEventName.yourFrogTriedToKillMe: {
    ET.PERMANENT: Alert(
      "Your Frog tried to kill me...",
      "👺",
      FrogPilotAlertStatus.frogpilot, AlertSize.mid,
      Priority.MID, VisualAlert.none, FrogPilotAudibleAlert.angry, 5.),
  },

  FrogPilotEventName.youveGotMail: {
    ET.WARNING: Alert(
      "You've got mail! 📧",
      "",
      FrogPilotAlertStatus.frogpilot, AlertSize.small,
      Priority.LOW, VisualAlert.none, FrogPilotAudibleAlert.mail, 3.),
  },
}

class FrogPilotEvents:
  def __init__(self, FrogPilotPlanner):
    self.frogpilot_planner = FrogPilotPlanner

    self.events = Events()

    self.accel30_played = False
    self.accel35_played = False
    self.accel40_played = False
    self.always_on_lateral_enabled_previously = False
    self.dejaVuCurve_played = False
    self.fcw_played = False
    self.firefoxSteerSaturated_played = False
    self.goatSteerSaturated_played = False
    self.hal9000_played = False
    self.holidayActive_played = False
    self.previous_traffic_mode = False
    self.random_event_playing = False
    self.startup_seen = False
    self.stopped_for_light = False
    self.thisIsFineSteerSaturated_played = False
    self.toBeContinued_played = False
    self.torqueNNLoad_played = False
    self.vCruise69_played = False
    self.yourFrogTriedToKillMe_played = False
    self.youveGotMail_played = False

    self.max_acceleration = 0
    self.random_event_timer = 0
    self.tracking_lead_distance = 0

  def update(self, v_cruise, sm, frogpilot_toggles):
    current_event_names = [event.name.raw for event in sm["onroadEvents"]] + [event.name.raw for event in sm["frogpilotOnroadEvents"]]

    self.events.clear()

    if self.random_event_playing:
      self.random_event_timer += DT_MDL

      if self.random_event_timer >= 5:
        update_wheel_image(frogpilot_toggles.wheel_image, frogpilot_toggles.current_holiday_theme, False)

        params_memory.put_bool("UpdateWheelImage", True)

        self.random_event_playing = False

        self.random_event_timer = 0

    if self.frogpilot_planner.frogpilot_vcruise.forcing_stop:
      self.events.add(FrogPilotEventName.forcingStop)

    if not self.frogpilot_planner.tracking_lead and sm["carState"].standstill and sm["carState"].gearShifter not in NON_DRIVING_GEARS and frogpilot_toggles.green_light_alert:
      if not self.frogpilot_planner.model_stopped and self.stopped_for_light:
        self.events.add(FrogPilotEventName.greenLight)

      self.stopped_for_light = self.frogpilot_planner.cem.stop_light_detected
    else:
      self.stopped_for_light = False

    if not self.holidayActive_played and self.startup_seen and sm["controlsState"].alertText1 == "" and frogpilot_toggles.current_holiday_theme != "stock" and len(self.events) == 0:
      self.events.add(FrogPilotEventName.holidayActive)

      self.holidayActive_played = True

    if self.frogpilot_planner.tracking_lead and sm["carState"].standstill and sm["carState"].gearShifter not in NON_DRIVING_GEARS and frogpilot_toggles.lead_departing_alert:
      if self.tracking_lead_distance == 0:
        self.tracking_lead_distance = self.frogpilot_planner.lead_one.dRel

      lead_departing = self.frogpilot_planner.lead_one.dRel - self.tracking_lead_distance > 1
      lead_departing &= self.frogpilot_planner.lead_one.vLead > 1

      if lead_departing:
        self.events.add(FrogPilotEventName.leadDeparting)
    else:
      self.tracking_lead_distance = 0

    if not self.torqueNNLoad_played and self.startup_seen and sm["controlsState"].alertText1 == "" and len(self.events) == 0 and params.get("NNFFModelName", encoding="utf-8") is not None and frogpilot_toggles.nnff:
      self.events.add(FrogPilotEventName.torqueNNLoad)

      self.torqueNNLoad_played = True

    if not self.random_event_playing and frogpilot_toggles.random_events:
      acceleration = sm["carState"].aEgo

      if not sm["carState"].gasPressed:
        self.max_acceleration = max(acceleration, self.max_acceleration)
      else:
        self.max_acceleration = 0

      if not self.accel30_played and 3.5 > self.max_acceleration >= 3.0 and acceleration < 1.5:
        self.events.add(FrogPilotEventName.accel30)

        update_wheel_image("weeb_wheel")

        params_memory.put_bool("UpdateWheelImage", True)

        self.accel30_played = True
        self.random_event_playing = True

        self.max_acceleration = 0

      elif not self.accel35_played and 4.0 > self.max_acceleration >= 3.5 and acceleration < 1.5:
        self.events.add(FrogPilotEventName.accel35)

        update_wheel_image("tree_fiddy")

        params_memory.put_bool("UpdateWheelImage", True)

        self.accel35_played = True
        self.random_event_playing = True

        self.max_acceleration = 0

      elif not self.accel40_played and self.max_acceleration >= 4.0 and acceleration < 1.5:
        self.events.add(FrogPilotEventName.accel40)

        update_wheel_image("great_scott")

        params_memory.put_bool("UpdateWheelImage", True)

        self.accel40_played = True
        self.random_event_playing = True

        self.max_acceleration = 0

      if not self.dejaVuCurve_played and sm["carState"].vEgo > CRUISING_SPEED * 2 and self.frogpilot_planner.road_curvature_detected:
        if sm["carState"].vEgo > (1 / abs(self.frogpilot_planner.road_curvature))**0.75 * 2 > CRUISING_SPEED * 2 and abs(sm["carState"].steeringAngleDeg) > 30:
          self.events.add(FrogPilotEventName.dejaVuCurve)

          self.dejaVuCurve_played = True
          self.random_event_playing = True

      if not self.hal9000_played and sm["controlsState"].alertType == ET.NO_ENTRY:
        self.events.add(FrogPilotEventName.hal9000)

        self.hal9000_played = True
        self.random_event_playing = True

      if EventName.steerSaturated in current_event_names or FrogPilotEventName.goatSteerSaturated in current_event_names:
        event_choices = []
        if not self.firefoxSteerSaturated_played:
          event_choices.append("firefoxSteerSaturated")
        if not self.goatSteerSaturated_played:
          event_choices.append("goatSteerSaturated")
        if not self.thisIsFineSteerSaturated_played:
          event_choices.append("thisIsFineSteerSaturated")

        if event_choices and random.random() < RANDOM_EVENTS_CHANCE:
          event_choice = random.choice(event_choices)

          if event_choice == "firefoxSteerSaturated":
            self.events.add(FrogPilotEventName.firefoxSteerSaturated)

            update_wheel_image("firefox")

            params_memory.put_bool("UpdateWheelImage", True)

            self.firefoxSteerSaturated_played = True

          elif event_choice == "goatSteerSaturated":
            self.events.add(FrogPilotEventName.goatSteerSaturated)

            update_wheel_image("goat")

            params_memory.put_bool("UpdateWheelImage", True)

            self.goatSteerSaturated_played = True

          elif event_choice == "thisIsFineSteerSaturated":
            self.events.add(FrogPilotEventName.thisIsFineSteerSaturated)

            update_wheel_image("this_is_fine")

            params_memory.put_bool("UpdateWheelImage", True)

            self.thisIsFineSteerSaturated_played = True

          self.random_event_playing = True

      if not self.vCruise69_played and 70 > max(sm["controlsState"].vCruise, sm["controlsState"].vCruiseCluster) * (1 if frogpilot_toggles.is_metric else CV.KPH_TO_MPH) >= 69:
        self.events.add(FrogPilotEventName.vCruise69)

        self.vCruise69_played = True
        self.random_event_playing = True

      if EventName.fcw in current_event_names or EventName.stockAeb in current_event_names:
        event_choices = []
        if not self.toBeContinued_played:
          event_choices.append("toBeContinued")
        if not self.yourFrogTriedToKillMe_played:
          event_choices.append("yourFrogTriedToKillMe")

        event_choice = random.choice(event_choices)
        if event_choice == "toBeContinued":
          self.events.add(FrogPilotEventName.toBeContinued)

          self.toBeContinued_played = True

        elif event_choice == "yourFrogTriedToKillMe":
          self.events.add(FrogPilotEventName.yourFrogTriedToKillMe)

          self.yourFrogTriedToKillMe_played = True

        self.random_event_playing = True

      if not self.youveGotMail_played and sm["frogpilotCarState"].alwaysOnLateralEnabled and not self.always_on_lateral_enabled_previously:
        if random.random() < RANDOM_EVENTS_CHANCE:
          self.events.add(FrogPilotEventName.youveGotMail)

          self.youveGotMail_played = True
          self.random_event_playing = True

      self.always_on_lateral_enabled_previously = sm["frogpilotCarState"].alwaysOnLateralEnabled

    if frogpilot_toggles.speed_limit_changed_alert and self.frogpilot_planner.frogpilot_vcruise.slc.speed_limit_changed_timer == DT_MDL:
      self.events.add(FrogPilotEventName.speedLimitChanged)

    self.startup_seen |= sm["controlsState"].alertText1 == frogpilot_toggles.startup_alert_top and sm["controlsState"].alertText2 == frogpilot_toggles.startup_alert_bottom

    if sm["frogpilotCarState"].trafficModeEnabled != self.previous_traffic_mode:
      if self.previous_traffic_mode:
        self.events.add(FrogPilotEventName.trafficModeInactive)
      else:
        self.events.add(FrogPilotEventName.trafficModeActive)
      self.previous_traffic_mode = sm["frogpilotCarState"].trafficModeEnabled

    if sm["frogpilotModelV2"].turnDirection == TurnDirection.turnLeft:
      self.events.add(FrogPilotEventName.turningLeft)
    elif sm["frogpilotModelV2"].turnDirection == TurnDirection.turnRight:
      self.events.add(FrogPilotEventName.turningRight)
