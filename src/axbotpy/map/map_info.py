from datetime import datetime


class MapInfo:
    def __init__(self, obj: dict = None) -> None:
        self.id: int
        self.uid: str
        self.map_name: str
        self.map_version: int
        self.overlays_version: int
        self.grid_origin_x: float
        self.grid_origin_y: float
        self.grid_resolution: float
        self.create_time: datetime
        self.last_modified_time = datetime

        if obj != None:
            self.id = obj["id"]
            self.uid = obj["uid"]
            self.map_name = obj["map_name"]
            self.map_version = obj["map_version"]
            self.overlays_version = obj["overlays_version"]
            self.grid_origin_x = obj["grid_origin_x"]
            self.grid_origin_y = obj["grid_origin_y"]
            self.grid_resolution = obj["grid_resolution"]
            self.create_time = datetime.fromtimestamp(obj["create_time"])
            self.last_modified_time = datetime.fromtimestamp(obj["last_modified_time"])
