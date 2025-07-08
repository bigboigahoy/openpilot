using Cxx = import "./include/c++.capnp";
$Cxx.namespace("cereal");

using Car = import "car.capnp";

@0xb526ba661d550a59;

# custom.capnp: a home for empty structs reserved for custom forks
# These structs are guaranteed to remain reserved and empty in mainline
# cereal, so use these if you want custom events in your fork.

# you can rename the struct, but don't change the identifier
enum LongitudinalPersonalityCopy {
  aggressive @0;
  standard @1;
  relaxed @2;
}

struct FrogPilotCarControl {
  hudControl @0 :HUDControl;

  struct HUDControl {
    audibleAlert @0: AudibleAlert;

    enum AudibleAlert {
      none @0;

      engage @1;
      disengage @2;
      refuse @3;

      warningSoft @4;
      warningImmediate @5;

      prompt @6;
      promptRepeat @7;
      promptDistracted @8;

      # FrogPilot sounds
      angry @9;
      continued @10;
      dejaVu @11;
      doc @12;
      fart @13;
      firefox @14;
      goat @15;
      hal9000 @16;
      mail @17;
      nessie @18;
      noice @19;
      startup @20;
      thisIsFine @21;
      uwu @22;
    }
  }
}

struct FrogPilotCarEvent @0x81c2f05a394cf4af {
  name @0 :EventName;

  enable @1 :Bool;
  noEntry @2 :Bool;
  warning @3 :Bool;
  userDisable @4 :Bool;
  softDisable @5 :Bool;
  immediateDisable @6 :Bool;
  preEnable @7 :Bool;
  permanent @8 :Bool;
  overrideLateral @10 :Bool;
  overrideLongitudinal @9 :Bool;

  enum EventName @0xaedffd8f31e7b55d {
    canError @0;
    steerUnavailable @1;
    wrongGear @4;
    doorOpen @5;
    seatbeltNotLatched @6;
    espDisabled @7;
    wrongCarMode @8;
    steerTempUnavailable @9;
    reverseGear @10;
    buttonCancel @11;
    buttonEnable @12;
    pedalPressed @13;  # exits active state
    preEnableStandstill @73;  # added during pre-enable state with brake
    gasPressedOverride @108;  # added when user is pressing gas with no disengage on gas
    steerOverride @114;
    cruiseDisabled @14;
    speedTooLow @17;
    outOfSpace @18;
    overheat @19;
    calibrationIncomplete @20;
    calibrationInvalid @21;
    calibrationRecalibrating @117;
    controlsMismatch @22;
    pcmEnable @23;
    pcmDisable @24;
    radarFault @26;
    brakeHold @28;
    parkBrake @29;
    manualRestart @30;
    lowSpeedLockout @31;
    joystickDebug @34;
    steerTempUnavailableSilent @35;
    resumeRequired @36;
    preDriverDistracted @37;
    promptDriverDistracted @38;
    driverDistracted @39;
    preDriverUnresponsive @43;
    promptDriverUnresponsive @44;
    driverUnresponsive @45;
    belowSteerSpeed @46;
    lowBattery @48;
    accFaulted @51;
    sensorDataInvalid @52;
    commIssue @53;
    commIssueAvgFreq @109;
    tooDistracted @54;
    posenetInvalid @55;
    soundsUnavailable @56;
    preLaneChangeLeft @57;
    preLaneChangeRight @58;
    laneChange @59;
    lowMemory @63;
    stockAeb @64;
    ldw @65;
    carUnrecognized @66;
    invalidLkasSetting @69;
    speedTooHigh @70;
    laneChangeBlocked @71;
    relayMalfunction @72;
    stockFcw @74;
    startup @75;
    startupNoCar @76;
    startupNoControl @77;
    startupNoSecOcKey @121;
    startupMaster @78;
    startupNoFw @104;
    fcw @79;
    steerSaturated @80;
    belowEngageSpeed @84;
    noGps @85;
    wrongCruiseMode @87;
    modeldLagging @89;
    deviceFalling @90;
    fanMalfunction @91;
    cameraMalfunction @92;
    cameraFrameRate @110;
    processNotRunning @95;
    dashcamMode @96;
    controlsInitializing @98;
    usbError @99;
    roadCameraError @100;
    driverCameraError @101;
    wideRoadCameraError @102;
    highCpuUsage @105;
    cruiseMismatch @106;
    lkasDisabled @107;
    canBusMissing @111;
    controlsdLagging @112;
    resumeBlocked @113;
    steerTimeLimit @115;
    vehicleSensorsInvalid @116;
    locationdTemporaryError @103;
    locationdPermanentError @118;
    paramsdTemporaryError @50;
    paramsdPermanentError @119;
    actuatorsApiUnavailable @120;

    # FrogPilot Events
    accel30 @122;
    accel35 @123;
    accel40 @124;
    blockUser @125;
    customStartupAlert @126;
    dejaVuCurve @127;
    firefoxSteerSaturated @128;
    forcingStop @129;
    goatSteerSaturated @130;
    greenLight @131;
    hal9000 @132;
    holidayActive @133;
    laneChangeBlockedLoud @134;
    leadDeparting @135;
    noLaneAvailable @136;
    openpilotCrashed @137;
    openpilotCrashedRandomEvent @138;
    pedalInterceptorNoBrake @139;
    speedLimitChanged @140;
    thisIsFineSteerSaturated @141;
    toBeContinued @142;
    torqueNNLoad @143;
    trafficModeActive @144;
    trafficModeInactive @145;
    turningLeft @146;
    turningRight @147;
    vCruise69 @148;
    yourFrogTriedToKillMe @149;
    youveGotMail @150;

    radarCanErrorDEPRECATED @15;
    communityFeatureDisallowedDEPRECATED @62;
    radarCommIssueDEPRECATED @67;
    driverMonitorLowAccDEPRECATED @68;
    gasUnavailableDEPRECATED @3;
    dataNeededDEPRECATED @16;
    modelCommIssueDEPRECATED @27;
    ipasOverrideDEPRECATED @33;
    geofenceDEPRECATED @40;
    driverMonitorOnDEPRECATED @41;
    driverMonitorOffDEPRECATED @42;
    calibrationProgressDEPRECATED @47;
    invalidGiraffeHondaDEPRECATED @49;
    invalidGiraffeToyotaDEPRECATED @60;
    internetConnectivityNeededDEPRECATED @61;
    whitePandaUnsupportedDEPRECATED @81;
    commIssueWarningDEPRECATED @83;
    focusRecoverActiveDEPRECATED @86;
    neosUpdateRequiredDEPRECATED @88;
    modelLagWarningDEPRECATED @93;
    startupOneplusDEPRECATED @82;
    startupFuzzyFingerprintDEPRECATED @97;
    noTargetDEPRECATED @25;
    brakeUnavailableDEPRECATED @2;
    plannerErrorDEPRECATED @32;
    gpsMalfunctionDEPRECATED @94;
  }
}

struct FrogPilotCarParams @0xf35cc4560bbf6ec2 {
  fpFlags @0 :UInt32;
  isHDA2 @1 :Bool;
  openpilotLongitudinalControlDisabled @2 :Bool;
}

struct FrogPilotCarState @0xda96579883444c35 {
  struct ButtonEvent {
    enum Type {
      lkas @0;
    }
  }

  accelPressed @0 :Bool;
  alwaysOnLateralAllowed @1 :Bool;
  alwaysOnLateralEnabled @2 :Bool;
  brakeLights @3 :Bool;
  dashboardSpeedLimit @4 :Float32;
  decelPressed @5 :Bool;
  distancePressed @6 :Bool;
  distanceLongPressed @7 :Bool;
  distanceVeryLongPressed @8 :Bool;
  ecoGear @9 :Bool;
  forceCoast @10 :Bool;
  pauseLateral @11 :Bool;
  pauseLongitudinal @12 :Bool;
  sportGear @13 :Bool;
  trafficModeEnabled @14 :Bool;
}

struct FrogPilotControlsState @0x80ae746ee2596b11 {
  startMonoTime @48 :UInt64;
  longitudinalPlanMonoTime @28 :UInt64;
  lateralPlanMonoTime @50 :UInt64;

  state @31 :OpenpilotState;
  enabled @19 :Bool;
  active @36 :Bool;

  experimentalMode @64 :Bool;
  personality @66 :LongitudinalPersonalityCopy;

  longControlState @30 :Car.CarControl.Actuators.LongControlState;
  vPid @2 :Float32;
  vTargetLead @3 :Float32;
  vCruise @22 :Float32;  # actual set speed
  vCruiseCluster @63 :Float32;  # set speed to display in the UI
  upAccelCmd @4 :Float32;
  uiAccelCmd @5 :Float32;
  ufAccelCmd @33 :Float32;
  aTarget @35 :Float32;
  curvature @37 :Float32;  # path curvature from vehicle model
  desiredCurvature @61 :Float32;  # lag adjusted curvatures used by lateral controllers
  forceDecel @51 :Bool;

  # UI alerts
  alertText1 @24 :Text;
  alertText2 @25 :Text;
  alertStatus @38 :AlertStatus;
  alertSize @39 :AlertSize;
  alertBlinkingRate @42 :Float32;
  alertType @44 :Text;
  alertSound @56 :Car.CarControl.HUDControl.AudibleAlert;
  engageable @41 :Bool;  # can OP be engaged?

  cumLagMs @15 :Float32;

  lateralControlState :union {
    indiState @52 :LateralINDIState;
    pidState @53 :LateralPIDState;
    angleState @58 :LateralAngleState;
    debugState @59 :LateralDebugState;
    torqueState @60 :LateralTorqueState;

    curvatureStateDEPRECATED @65 :LateralCurvatureState;
    lqrStateDEPRECATED @55 :LateralLQRState;
  }

  enum OpenpilotState @0xbd443b539493bc68 {
    disabled @0;
    preEnabled @1;
    enabled @2;
    softDisabling @3;
    overriding @4;  # superset of overriding with steering or accelerator
  }

  enum AlertStatus {
    normal @0;       # low priority alert for user's convenience
    userPrompt @1;   # mid priority alert that might require user intervention
    critical @2;     # high priority alert that needs immediate user intervention
    frogpilot @3;    # FrogPilot startup alert
  }

  enum AlertSize {
    none @0;    # don't display the alert
    small @1;   # small box
    mid @2;     # mid screen
    full @3;    # full screen
  }

  struct LateralINDIState {
    active @0 :Bool;
    steeringAngleDeg @1 :Float32;
    steeringRateDeg @2 :Float32;
    steeringAccelDeg @3 :Float32;
    rateSetPoint @4 :Float32;
    accelSetPoint @5 :Float32;
    accelError @6 :Float32;
    delayedOutput @7 :Float32;
    delta @8 :Float32;
    output @9 :Float32;
    saturated @10 :Bool;
    steeringAngleDesiredDeg @11 :Float32;
    steeringRateDesiredDeg @12 :Float32;
  }

  struct LateralPIDState {
    active @0 :Bool;
    steeringAngleDeg @1 :Float32;
    steeringRateDeg @2 :Float32;
    angleError @3 :Float32;
    p @4 :Float32;
    i @5 :Float32;
    f @6 :Float32;
    output @7 :Float32;
    saturated @8 :Bool;
    steeringAngleDesiredDeg @9 :Float32;
   }

  struct LateralTorqueState {
    active @0 :Bool;
    error @1 :Float32;
    errorRate @8 :Float32;
    p @2 :Float32;
    i @3 :Float32;
    d @4 :Float32;
    f @5 :Float32;
    output @6 :Float32;
    saturated @7 :Bool;
    actualLateralAccel @9 :Float32;
    desiredLateralAccel @10 :Float32;
    nnLog @11 :List(Float32);
   }

  struct LateralLQRState {
    active @0 :Bool;
    steeringAngleDeg @1 :Float32;
    i @2 :Float32;
    output @3 :Float32;
    lqrOutput @4 :Float32;
    saturated @5 :Bool;
    steeringAngleDesiredDeg @6 :Float32;
  }

  struct LateralAngleState {
    active @0 :Bool;
    steeringAngleDeg @1 :Float32;
    output @2 :Float32;
    saturated @3 :Bool;
    steeringAngleDesiredDeg @4 :Float32;
  }

  struct LateralCurvatureState {
    active @0 :Bool;
    actualCurvature @1 :Float32;
    desiredCurvature @2 :Float32;
    error @3 :Float32;
    p @4 :Float32;
    i @5 :Float32;
    f @6 :Float32;
    output @7 :Float32;
    saturated @8 :Bool;
  }

  struct LateralDebugState {
    active @0 :Bool;
    steeringAngleDeg @1 :Float32;
    output @2 :Float32;
    saturated @3 :Bool;
  }

  # deprecated
  vEgoDEPRECATED @0 :Float32;
  vEgoRawDEPRECATED @32 :Float32;
  aEgoDEPRECATED @1 :Float32;
  canMonoTimeDEPRECATED @16 :UInt64;
  radarStateMonoTimeDEPRECATED @17 :UInt64;
  mdMonoTimeDEPRECATED @18 :UInt64;
  yActualDEPRECATED @6 :Float32;
  yDesDEPRECATED @7 :Float32;
  upSteerDEPRECATED @8 :Float32;
  uiSteerDEPRECATED @9 :Float32;
  ufSteerDEPRECATED @34 :Float32;
  aTargetMinDEPRECATED @10 :Float32;
  aTargetMaxDEPRECATED @11 :Float32;
  rearViewCamDEPRECATED @23 :Bool;
  driverMonitoringOnDEPRECATED @43 :Bool;
  hudLeadDEPRECATED @14 :Int32;
  alertSoundDEPRECATED @45 :Text;
  angleModelBiasDEPRECATED @27 :Float32;
  gpsPlannerActiveDEPRECATED @40 :Bool;
  decelForTurnDEPRECATED @47 :Bool;
  decelForModelDEPRECATED @54 :Bool;
  awarenessStatusDEPRECATED @26 :Float32;
  angleSteersDEPRECATED @13 :Float32;
  vCurvatureDEPRECATED @46 :Float32;
  mapValidDEPRECATED @49 :Bool;
  jerkFactorDEPRECATED @12 :Float32;
  steerOverrideDEPRECATED @20 :Bool;
  steeringAngleDesiredDegDEPRECATED @29 :Float32;
  canMonoTimesDEPRECATED @21 :List(UInt64);
  desiredCurvatureRateDEPRECATED @62 :Float32;
  canErrorCounterDEPRECATED @57 :UInt32;
}

struct FrogPilotDeviceState @0xa5cd762cd951a455 {
  freeSpace @0 :Int16;
  usedSpace @1 :Int16;
}

struct FrogPilotModelDataV2 @0xf98d843bfd7004a3 {
  turnDirection @0 :TurnDirection;

  enum TurnDirection {
    none @0;
    turnLeft @1;
    turnRight @2;
  }
}

struct FrogPilotNavigation @0xf416ec09499d9d19 {
  approachingIntersection @0 :Bool;
  approachingTurn @1 :Bool;
  navigationSpeedLimit @2 :Float32;
}

struct FrogPilotPlan @0xa1680744031fdb2d {
  accelerationJerk @0 :Float32;
  accelerationJerkStock @1 :Float32;
  cscControllingSpeed @2 :Bool;
  cscSpeed @3 :Float32;
  cscTraining @4 :Bool;
  dangerJerk @5 :Float32;
  desiredFollowDistance @6 :Int64;
  experimentalMode @7 :Bool;
  forcingStop @8 :Bool;
  forcingStopLength @9 :Float32;
  frogpilotEvents @10 :List(FrogPilotCarEvent);
  lateralCheck @11 :Bool;
  laneWidthLeft @12 :Float32;
  laneWidthRight @13 :Float32;
  maxAcceleration @14 :Float32;
  minAcceleration @15 :Float32;
  redLight @16 :Bool;
  roadCurvature @17 :Float32;
  slcMapSpeedLimit @18 :Float32;
  slcMapboxSpeedLimit @19 :Float32;
  slcNextSpeedLimit @20 :Float32;
  slcOverriddenSpeed @21 :Float32;
  slcSpeedLimit @22 :Float32;
  slcSpeedLimitOffset @23 :Float32;
  slcSpeedLimitSource @24 :Text;
  speedJerk @25 :Float32;
  speedJerkStock @26 :Float32;
  speedLimitChanged @27 :Bool;
  tFollow @28 :Float32;
  themeUpdated @29 :Bool;
  togglesUpdated @30 :Bool;
  trackingLead @31 :Bool;
  unconfirmedSlcSpeedLimit @32 :Float32;
  vCruise @33 :Float32;
}

struct FrogPilotRadarState @0xcb9fd56c7057593a {
  leadOne @0 :LeadData;
  leadLeft @1 :LeadData;
  leadRight @2 :LeadData;

  struct LeadData {
    dRel @0 :Float32;
    yRel @1 :Float32;
    vRel @2 :Float32;
    aRel @3 :Float32;
    vLead @4 :Float32;
    dPath @6 :Float32;
    vLat @7 :Float32;
    vLeadK @8 :Float32;
    aLeadK @9 :Float32;
    fcw @10 :Bool;
    status @11 :Bool;
    aLeadTau @12 :Float32;
    modelProb @13 :Float32;
    radar @14 :Bool;
    radarTrackId @15 :Int32 = -1;

    aLeadDEPRECATED @5 :Float32;
  }
}
