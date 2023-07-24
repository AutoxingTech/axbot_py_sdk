from enum import Enum
from typing import List

from axbotpy.common.conversion import DictConvertMixin


class DeviceField(DictConvertMixin):
    def __init__(self, d: dict) -> None:
        self.model: str
        self.sn: str
        self.name: str

        super().__init__(d)


class RobotField(DictConvertMixin):
    def __init__(self, d: dict) -> None:
        self.footprint: List[List[float]]
        self.inscribed_radius: float
        self.height: float
        self.thickness: float
        self.width: float

        super().__init__(d)


class CapsField(DictConvertMixin):
    def __init__(self, d: dict) -> None:
        self.supportsImuRecalibrateService = False  # supports /services/imu/recalibrate
        self.supportsShutdownService = False  # supports /services/baseboard/shutdown
        self.supportsRestartService = False  # supports /services/restart_service
        self.supportsResetOccupancyGridService = False  # supports /services/occupancy_grid_server/reset
        self.supportsImuRecalibrationFeedback = False  # supports /imu_state WebSocket topic
        self.supportsSetControlModeService = False  # supports /services/wheel_control/set_control_mode
        self.supportsSetEmergencyStopService = False  # supports /services/wheel_control/set_emergency_stop
        self.supportsWheelStateTopic = False  # supports /wheel_state WebSocket topic
        self.supportsWsV2 = False  # supports ws://HOST/ws/v2/topics
        self.supportsRgbCamera = False  # supports RGB related topics
        self.combineImuBiasAndPoseCalibration = False
        super().__init__(d)


class DeviceInfo:
    def __init__(self, msg: any) -> None:
        self.axbot_version = msg["axbot_version"]
        self.device = DeviceField(msg["device"])
        self.robot = RobotField(msg["robot"])
        self.caps = CapsField(msg["caps"])
