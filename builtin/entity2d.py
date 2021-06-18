from renderers.renderer import Renderable, BaseRenderer


class Entity2d:
    position: (float, float)
    orientation: float

    def __init__(self, x: float, y: float, orientation: float = 0.0):
        self.position = (x, y)
        self.orientation = orientation

    def move(self, dx: float, dy: float):
        self.position = (self.position[0] + dx, self.position[1] + dy)

    def rotate(self, angle: float):
        self.orientation += angle
        if self.orientation > 360.0:
            self.orientation -= 360.0


class GridEntity2d:
    position: (int, int)

    def __init__(self, x: int, y: int):
        self.position = (x, y)

    def move(self, dx, dy):
        self.position = (self.position[0] + dx, self.position[1] + dy)


class CircleEntity(Entity2d, Renderable):

    r: float

    def __init__(self, x: float, y: float, r: float, orientation: float = 0.0, renderer: BaseRenderer = None):
        Entity2d.__init__(self, x, y, orientation)
        Renderable.__init__(self, renderer)
        self.r = r

    def change_radius(self, r: float):
        self.r = r

    def check_collision(self, entity: Entity2d):
        collision = False
        if entity is CircleEntity:
            collision = (self.position[0] - entity.position[0]) ** 2 + \
                        (self.position[1] - entity.position[1]) ** 2 < (self.r + entity.r) ** 2

        return collision

    def render(self):
        self.renderer.render(self)

    def __str__(self):
        return "Circle entity (x, y) = " + self.x.__str__() + ", " + self.y.__str__() + ") r = " + \
               self.r.__str__()
