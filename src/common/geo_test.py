import math

import pytest

from .geo import Pose2, Pose3, Quaternion, Vector2, Vector3, get_turn_angle, polygon_inside, wrap_two_pi


def test_vector2():
    assert Vector2(3, 2) == Vector2(3, 2)
    assert Vector2(3, 2) != Vector2(3, 1)
    assert Vector2(3, 2) != None
    assert None != Vector2(3, 2)

    assert Vector2(1, 2) + Vector2(1, 1) == Vector2(2, 3)
    assert Vector2(3, 2) - Vector2(1, 1) == Vector2(2, 1)
    assert str(Vector2(1, 2)) == "Vector2(1, 2)"
    assert Vector2(1, 2) * 2 == Vector2(2, 4)
    assert 2 * Vector2(1, 2) == Vector2(2, 4)
    assert Vector2(2, 4) / 2 == Vector2(1, 2)


def test_vector3():
    assert Vector3(3, 2, 1) == Vector3(3, 2, 1)
    assert Vector3(3, 2, 1) != Vector3(0, 2, 1)
    assert Vector3(3, 2, 1) != Vector3(3, 0, 1)
    assert Vector3(3, 2, 1) != Vector3(3, 2, 0)
    assert Vector3(3, 2, 1) != None
    assert None != Vector3(3, 2, 0)

    assert Vector3(1, 2, 3) + Vector3(1, 1, 1) == Vector3(2, 3, 4)
    assert Vector3(3, 2, 1) - Vector3(1, 1, 1) == Vector3(2, 1, 0)
    assert str(Vector3(1, 2, 3)) == "Vector3(1, 2, 3)"
    assert Vector3(1, 2, 3) * 2 == Vector3(2, 4, 6)
    assert 2 * Vector3(1, 2, 3) == Vector3(2, 4, 6)
    assert Vector3(2, 4, 6) / 2 == Vector3(1, 2, 3)


def test_pose():
    assert Pose2(Vector2(1, 2), 3) == Pose2(Vector2(1, 2), 3)
    assert Pose2(Vector2(1, 2), 3) != Pose2(Vector2(0, 2), 3)
    assert Pose2(Vector2(1, 2), 3) != Pose2(Vector2(1, 0), 3)
    assert Pose2(Vector2(1, 2), 3) != Pose2(Vector2(1, 0), 0)
    assert Pose2(Vector2(1, 2), 3) != None
    assert None != Pose2(Vector2(1, 2), 3)

    pose = Pose2(Vector2(1, 2), 3)
    assert pose.pos.x == 1
    assert pose.pos.y == 2
    assert pose.ori == 3


def test_quaternion():
    assert Quaternion.from_xyzw(1, 2, 3, 4) == Quaternion.from_xyzw(1, 2, 3, 4)
    assert Quaternion.from_xyzw(1, 2, 3, 4) != Quaternion.from_xyzw(0, 2, 3, 4)
    assert Quaternion.from_xyzw(1, 2, 3, 4) != Quaternion.from_xyzw(1, 0, 3, 4)
    assert Quaternion.from_xyzw(1, 2, 3, 4) != Quaternion.from_xyzw(1, 2, 0, 4)
    assert Quaternion.from_xyzw(1, 2, 3, 4) != Quaternion.from_xyzw(1, 2, 3, 0)
    assert Quaternion.from_xyzw(1, 2, 3, 4) != None
    assert None != Quaternion.from_xyzw(1, 2, 3, 4)

    q = Quaternion.from_xyzw(0, 0, 0.7072, 0.7072)
    rpy = q.to_rpy()
    assert rpy.roll == 0
    assert rpy.pitch == 0
    assert rpy.yaw == pytest.approx(1.5710599372799763, 0.001)

    assert Quaternion.from_rpy(0.1, 0.2, 0.3).yaw == pytest.approx(0.3, 0.00001)

    q = Quaternion.from_rpy(rpy)
    assert q.x == pytest.approx(0, 0.001)
    assert q.y == pytest.approx(0, 0.001)
    assert q.z == pytest.approx(0.7072, 0.001)
    assert q.w == pytest.approx(0.7072, 0.001)

    assert Quaternion.identity() == Quaternion(0, 0, 0, 1)
    assert Quaternion(0, 0, 0, 1).inverse() == Quaternion(0, 0, 0, -1)

    q = Quaternion.from_rpy(1, 0, 0)
    angles = q.to_rpy()
    assert angles.roll == pytest.approx(1, 0.01)
    assert angles.pitch == pytest.approx(0, 0.01)
    assert angles.yaw == pytest.approx(0, 0.01)

    q = Quaternion.from_rpy(0, 1, 0)
    angles = q.to_rpy()
    assert angles.roll == pytest.approx(0, 0.01)
    assert angles.pitch == pytest.approx(1, 0.01)
    assert angles.yaw == pytest.approx(0, 0.01)

    q = Quaternion.from_rpy(0, 0, 1)
    angles = q.to_rpy()
    assert angles.roll == pytest.approx(0, 0.01)
    assert angles.pitch == pytest.approx(0, 0.01)
    assert angles.yaw == pytest.approx(1, 0.01)

    q = Quaternion.from_rpy(1, 1.2, 1.3)
    angles = q.to_rpy()
    assert angles.roll == pytest.approx(1, 0.01)
    assert angles.pitch == pytest.approx(1.2, 0.01)
    assert angles.yaw == pytest.approx(1.3, 0.01)

    q = Quaternion.from_rpy(0, 0, math.pi / 2)
    r = q.transform_vector(Vector3(10, 0, 0))
    assert r.x == pytest.approx(0, 0.0001)
    assert r.y == pytest.approx(10, 0.0001)
    assert r.z == pytest.approx(0, 0.0001)


def test_quaternion_multiply():
    q1 = Quaternion.from_rpy(1, 0, 0)
    q2 = Quaternion.from_rpy(0, 1.2, 0)
    q3 = Quaternion.from_rpy(0, 0, 1.3)

    combined = q3 * q2 * q1

    angles = combined.to_rpy()
    assert angles.roll == pytest.approx(1, 0.01)
    assert angles.pitch == pytest.approx(1.2, 0.01)
    assert angles.yaw == pytest.approx(1.3, 0.01)


def test_quaternion_2():
    q = Quaternion.from_rpy(1, 0, 0)
    rpy = q.to_rpy()
    assert rpy.roll == pytest.approx(1, 0.01)
    assert rpy.pitch == pytest.approx(0, 0.01)
    assert rpy.yaw == pytest.approx(0, 0.01)

    q = Quaternion.from_rpy(0, 1, 0)
    rpy = q.to_rpy()
    assert rpy.roll == pytest.approx(0, 0.01)
    assert rpy.pitch == pytest.approx(1, 0.01)
    assert rpy.yaw == pytest.approx(0, 0.01)

    q = Quaternion.from_rpy(0, 0, 1)
    rpy = q.to_rpy()
    assert rpy.roll == pytest.approx(0, 0.01)
    assert rpy.pitch == pytest.approx(0, 0.01)
    assert rpy.yaw == pytest.approx(1, 0.01)


def test_pose2():
    pose = Pose2()
    assert pose.pos == Vector2(0, 0)
    assert pose.ori == 0

    pose.pos.x = 1
    pose = Pose2()
    assert pose.pos == Vector2(0, 0)

    assert str(Pose2(Vector2(1, 2), 3)) == "Pose2(x = 1, y = 2, ori = 3)"

    # equals
    assert Pose2(Vector2(1, 2), 0.3) == Pose2(Vector2(1, 2), 0.3)
    assert pose != Pose2(Vector2(2, 2), 0.3)

    # inverse
    pose = Pose2(Vector2(1, 2), 0.3)
    pose = pose.inverse()
    assert pose.pos == Vector3(-1, -2)
    assert pose.ori == -0.3


def test_pose3():
    pose = Pose3()
    assert pose.pos == Vector3(0, 0, 0)
    assert pose.ori == Quaternion.identity()

    pose.pos.x = 1
    pose = Pose3()
    assert pose.pos == Vector3(0, 0, 0)

    # equals
    assert Pose3(Vector3(1, 2, 3), Quaternion.from_rpy(0.1, 0.2, 0.3)) == Pose3(
        Vector3(1, 2, 3), Quaternion.from_rpy(0.1, 0.2, 0.3)
    )
    assert pose != Pose3(Vector3(2, 2, 3), Quaternion.from_rpy(0.1, 0.2, 0.3))

    # convert with pose2
    pose = Pose3(Vector3(1, 2, 3), Quaternion.from_rpy(0.1, 0.2, 0.3))
    pose2 = pose.to_pose2()
    assert pose2.pos == Vector2(1, 2)
    assert pose2.ori == pytest.approx(0.3, 0.0001)
    pose = Pose3.from_pose2(pose2)
    assert pose.pos == Vector3(1, 2, 0)
    assert pose.ori.to_rpy().roll == 0
    assert pose.ori.to_rpy().pitch == 0
    assert pose.ori.to_rpy().yaw == pytest.approx(0.3, 0.0001)

    # inverse
    ori = Quaternion.from_rpy(0.1, 0.2, 0.3)
    pose = Pose3(Vector3(1, 2, 3), ori)
    pose = pose.inverse()
    assert pose.pos == Vector3(-1, -2, -3)
    assert pose.ori == ori.inverse()


def test_pose3_multiple_vector3():
    pose = Pose3(Vector3(1, 2, 3), Quaternion.from_rpy(0, math.pi / 2, 0))
    v = pose * Vector3(1, 0, 0)
    assert v.x == pytest.approx(1, 0.0001)
    assert v.y == pytest.approx(2, 0.0001)
    assert v.z == pytest.approx(2, 0.0001)


def test_pose2_concatenate():
    pose = Pose2(Vector2(0, 1), math.pi / 4)
    pose2 = Pose2(Vector2(math.sqrt(2) / 2, math.sqrt(2) / 2), math.pi / 4)

    assert pose2.pos.length == pytest.approx(1, 0.0001)

    final_pose = pose2 * pose

    assert final_pose.ori == pytest.approx(math.pi / 2, 0.0001)

    assert final_pose.pos.x == pytest.approx(0, 0.0001)
    assert final_pose.pos.y == pytest.approx(1.414, 0.001)

    # inverse sequence
    final_pose = pose * pose2

    assert final_pose.ori == pytest.approx(math.pi / 2, 0.0001)

    assert final_pose.pos.x == pytest.approx(0, 0.0001)
    assert final_pose.pos.y == pytest.approx(2, 0.001)

    # another
    final_pose = pose * pose2.inverse()

    assert final_pose.ori == pytest.approx(0, 0.0001)

    assert final_pose.pos.x == pytest.approx(0, 0.0001)
    assert final_pose.pos.y == pytest.approx(0, 0.001)


def test_pose3_concatenate():
    pose = Pose3(Vector3(0, 1, 0), Quaternion.from_rpy(0, 0, math.pi / 4))
    pose2 = Pose3(Vector3(math.sqrt(2) / 2, math.sqrt(2) / 2, 0), Quaternion.from_rpy(0, 0, math.pi / 4))

    assert pose2.pos.length == pytest.approx(1, 0.0001)

    final_pose = pose2 * pose

    assert final_pose.ori.yaw == pytest.approx(math.pi / 2, 0.0001)

    assert final_pose.pos.x == pytest.approx(0, 0.0001)
    assert final_pose.pos.y == pytest.approx(1.414, 0.001)

    # inverse sequence
    final_pose = pose * pose2

    assert final_pose.ori.yaw == pytest.approx(math.pi / 2, 0.0001)

    assert final_pose.pos.x == pytest.approx(0, 0.0001)
    assert final_pose.pos.y == pytest.approx(2, 0.001)

    # another
    final_pose = pose * pose2.inverse()

    assert final_pose.ori.yaw == pytest.approx(0, 0.0001)

    assert final_pose.pos.x == pytest.approx(0, 0.0001)
    assert final_pose.pos.y == pytest.approx(0, 0.001)


def test_polygon_inside():
    poly = [[0, 0], [1, 0], [0, 1]]

    assert polygon_inside(poly, 0.1, 0.1) == True
    assert polygon_inside(poly, 0, 0) == False
    assert polygon_inside(poly, 1, 0) == False
    assert polygon_inside(poly, 0.999, 0.001) == True
    assert polygon_inside(poly, 0.999, 0.111) == False
    assert polygon_inside(poly, 0.5, 0.50001) == False
    assert polygon_inside(poly, 0.5, 0.45999) == True

    poly = []
    assert polygon_inside(poly, 0, 0) == False

    poly = [[0, 0]]
    assert polygon_inside(poly, 0, 0) == False

    poly = [[0, 0], [1, 0]]
    assert polygon_inside(poly, 0, 0) == False


def test_wrap_two_pi():
    assert wrap_two_pi(math.pi) == -math.pi
    assert wrap_two_pi(-math.pi) == -math.pi
    assert wrap_two_pi(math.pi * 3.5) == -math.pi / 2


def test_get_turn_angle():
    assert get_turn_angle(0, math.pi) == -math.pi
    assert get_turn_angle(0, -math.pi) == -math.pi
    assert get_turn_angle(0, math.pi / 2) == math.pi / 2
    assert get_turn_angle(math.pi / 2, 0) == -math.pi / 2

    turn = get_turn_angle(-3.121977923887787, 3.128226898163481)
    assert turn == pytest.approx(-0.033, 0.01)
