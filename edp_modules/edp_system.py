
import math
from support.logging import log



def _distance_between_two_points_3d(x0, y0, z0, x1, y1, z1):
    x_component = math.pow((x1 - x0), 2)
    y_component = math.pow((y1 - y0), 2)
    z_component = math.pow((z1 - z0), 2)
    return math.sqrt(x_component + y_component + z_component)


class EdpSystem:
    def __init__(self, descriptor):
        self.name = descriptor['name'].upper()
        self.x = descriptor['x']
        self.y = descriptor['y']
        self.z = descriptor['z']


    def distanceTo(self, target):
        return _distance_between_two_points_3d(self.x, self.y, self.z, target.x, target.y, target.z)



## TESTS ##

_test_descriptors = [{ 'name': '1 G. Caeli', 'x': 80.90625, 'y': -83.53125, 'z': -30.8125 },
                     { 'name': '1 Geminorum', 'x': 19.78125, 'y': 3.5625, 'z': -153.8125 }]

def _should_create_a_system_object_from_a_dict():
    s = EdpSystem(_test_descriptors[1])
    assert s.name == _test_descriptors[1]['name'].upper()
    assert s.x == _test_descriptors[1]['x']
    assert s.y == _test_descriptors[1]['y']
    assert s.z == _test_descriptors[1]['z']


def _should_compute_distance_to_another_system():
    ref = EdpSystem(_test_descriptors[0])
    tgt = EdpSystem(_test_descriptors[1])

    distance = ref.distanceTo(tgt)
    assert distance < 162.64 and distance > 162.63


def tests():
    _should_create_a_system_object_from_a_dict()
    _should_compute_distance_to_another_system()
    log('edp_system: OK')
