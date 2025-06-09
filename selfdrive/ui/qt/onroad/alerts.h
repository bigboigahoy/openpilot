#pragma once

#include <QWidget>

#include "selfdrive/ui/ui.h"

class OnroadAlerts : public QWidget {
  Q_OBJECT

public:
  OnroadAlerts(QWidget *parent = 0) : QWidget(parent) {}
  void updateState(const UIState &s, const FrogPilotUIState &fs);
  void clear();

  // FrogPilot variables
  int alertHeight;

protected:
  struct Alert {
    QString text1;
    QString text2;
    QString type;
    cereal::ControlsState::AlertSize size;
    cereal::ControlsState::AlertStatus status;

    bool equal(const Alert &other) const {
      return text1 == other.text1 && text2 == other.text2 && type == other.type;
    }
  };

  const QMap<cereal::ControlsState::AlertStatus, QColor> alert_colors = {
    {cereal::ControlsState::AlertStatus::NORMAL, QColor(0x18, 0x18, 0x25, 0xf1)},
    {cereal::ControlsState::AlertStatus::USER_PROMPT, QColor(0xfA, 0xb3, 0x87, 0xf1)},
    {cereal::ControlsState::AlertStatus::CRITICAL, QColor(0xf3, 0x8b, 0xa8, 0xf1)},

    // FrogPilot alert colors
    {cereal::ControlsState::AlertStatus::FROGPILOT, QColor(0xa6, 0xe3, 0xa1, 0xf1)},
  };

  void paintEvent(QPaintEvent*) override;
  OnroadAlerts::Alert getAlert(const SubMaster &sm, uint64_t started_frame, bool random_events);

  QColor bg;
  Alert alert = {};
};
