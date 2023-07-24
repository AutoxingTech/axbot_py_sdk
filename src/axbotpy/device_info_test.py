from .device_info import DeviceInfo


def test_device_info():
    msg = {
        "rosversion": "1.15.11",
        "rosdistro": "noetic",
        "axbot_version": "1.9.x",
        "device": {"model": "hygeia", "sn": "71822043000350z", "name": "71822043000350z"},
        "baseboard": {"firmware_version": "22a32218"},
        "wheel_control": {"firmware_version": "amps_20211103"},
        "bottom_sensor_pack": {"firmware_version": "1.1.1"},
        "depth_camera": {"firmware_version": "[/dev/camera:1.2.5-s2-ax-D1]"},
        "robot": {
            "footprint": [],
            "inscribed_radius": 0.248,
            "height": 1.2,
            "thickness": 0.546,
            "wheel_distance": 0.36,
            "width": 0.496,
            "charge_contact_position": "back",
        },
        "caps": {
            "supportsImuRecalibrateService": True,
            "supportsShutdownService": True,
            "supportsRestartService": True,
            "supportsResetOccupancyGridService": True,
            "supportsImuRecalibrationFeedback": True,
            "supportsSetControlModeService": True,
            "supportsSetEmergencyStopService": True,
            "supportsWheelStateTopic": True,
            "supportsWsV2": True,
            "supportsRgbCamera": True,
            "combineImuBiasAndPoseCalibration": True,
        },
    }
    info = DeviceInfo(msg)

    assert info.device.sn == "71822043000350z"
    assert info.caps.supportsImuRecalibrationFeedback
