"""
Copyright (c) 2021-, Haibin Wen, sunnypilot, and a number of other contributors.

This file is part of sunnypilot and is licensed under the MIT License.
See the LICENSE.md file in the root directory for more details.
"""
from cereal import car

AudibleAlert = car.CarControl.HUDControl.AudibleAlert

ALERTS_ALWAYS_PLAY = {
  AudibleAlert.warningSoft,
  AudibleAlert.warningImmediate,
  AudibleAlert.promptDistracted,
  AudibleAlert.promptRepeat,
}

class QuietMode:
  def should_play_sound(self, current_alert: int) -> bool:
    """
    Check if a sound should be played based on the Quiet Mode setting
    and the current alert.
    """
    return current_alert in ALERTS_ALWAYS_PLAY
