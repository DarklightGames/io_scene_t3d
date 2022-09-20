from typing import List, Tuple, Optional


class Polygon:
    def __init__(self,
                 flags: int,
                 link: Optional[int],
                 origin: Tuple[float, float, float],
                 normal: Tuple[float, float, float],
                 texture_u: Tuple[float, float, float],
                 texture_v: Tuple[float, float, float],
                 pan: Tuple[float, float],
                 vertices: List[Tuple[float, float, float]]):
        self.flags = flags
        self.link = link
        self.origin = origin
        self.normal = normal
        self.texture_u = texture_u
        self.texture_v = texture_v
        self.pan = pan
        self.vertices = vertices


class Brush:
    def __init__(self, name: str):
        self.name: str = name
        self.polygons: List[Polygon] = []


class Actor:
    def __init__(self, name: str):
        self.name = name
        self.brush: Optional[Brush] = None


class Map:
    def __init__(self):
        self.actors: List[Actor] = []


classes = tuple()
