from .map_info import MapInfo


def test_map_info():
    m = MapInfo(
        {
            "id": 1,
            "map_name": "5层地图",
            "uid": "620620f9c0fd0ecb0f66d981",
            "map_version": 9,
            "create_time": 1644568815,
            "last_modified_time": 1647333821,
            "grid_origin_x": -53.1968,
            "grid_origin_y": -25.0135,
            "grid_resolution": 0.05,
            "overlays_version": 14,
            "overlays": '{"type": "FeatureCollection", "features": [{"id": ...',
            "thumbnail_url": "http://localhost:8000/maps/1/thumbnail",
            "image_url": "http://localhost:8000/maps/1.png",
            "pbstream_url": "http://localhost:8000/maps/1.pbstream",
        }
    )

    assert m.id == 1
    assert m.map_name == "5层地图"
    assert m.uid == "620620f9c0fd0ecb0f66d981"
    assert m.map_version == 9
    assert m.create_time.timestamp() == 1644568815
    assert m.last_modified_time.timestamp() == 1647333821
    assert m.grid_origin_x == -53.1968
    assert m.grid_origin_y == -25.0135
    assert m.grid_resolution == 0.05
    assert m.overlays_version == 14
