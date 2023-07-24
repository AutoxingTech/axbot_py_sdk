from .actions import AlongGivenRouteMoveAction, MoveAction


def test_make_request_data():
    action1 = MoveAction(target=[1, 2])
    action2 = AlongGivenRouteMoveAction(coordinates=[[2, 3], [3, 4]])
    data = action2.make_request_data(action1)
    assert data["route_coordinates"] == "1,2,2,3,3,4"
