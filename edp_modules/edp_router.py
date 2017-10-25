
from support.logging import log
from edp_modules.edp_system import EdpSystem


class Route:
    def __init__(self):
        self.node_list = []
        self.length = 0


    def pretty_string(self):
        out = ''
        i = 1
        for node in self.node_list:
            out = out + '{0:3d}:  {1}\n'.format(i, node.system.name)
            i = i+1
        out = out + '{:-^30}\n'.format('')
        out = out + 'Total distance: {0:.2f} Ly'.format(self.length)
        return out


    def pretty_print(self):
        i = 1
        print('{:=^30}'.format(''))
        print(self.pretty_string())
        print('{:=^30}'.format(''))


    def add_node_at_end(self, node):
        if node is None:
            return
        if len(self.node_list) > 0:
            self.length = self.length + self.node_list[len(self.node_list) - 1].distance_to[node.system.name]
        self.node_list.append(node)


    def add_node_at_start(self, node):
        if node is None:
            return
        if len(self.node_list) > 0:
            self.length = self.length + self.node_list[0].distance_to[node.system.name]
        self.node_list.insert(0, node)


    def copy(self):
        new_route = Route()
        new_route.length = self.length
        new_route.node_list = self.node_list.copy()
        return new_route


class RouteNode:
    def __init__(self, system):
        self.system = system
        self.distance_to = {}


def _compute_distance_table(route_node_set):
    target_node_set = route_node_set.copy()
    for ref_key in route_node_set:
        ref_node = route_node_set[ref_key]
        del target_node_set[ref_node.system.name]
        for target_key in target_node_set:
            target_node = target_node_set[target_key]
            distance = ref_node.system.distanceTo(target_node.system)
            ref_node.distance_to[target_node.system.name] = distance
            target_node.distance_to[ref_node.system.name] = distance


def _create_route_node_set(system_list):
    route_node_set = {}
    for s in system_list:
        route_node_set[s.name] = RouteNode(s)

    _compute_distance_table(route_node_set)
    return route_node_set


def _extract_from_node_set(system_key, route_node_set):
    if system_key not in route_node_set:
        return None
    system = route_node_set[system_key]
    del route_node_set[system_key]
    return system


def _select_shortest_route(route_a, route_b):
    if route_a is None:
        return route_b
    if route_b is None:
        return route_a

    if (route_a.length < route_b.length):
        return route_a

    return route_b


def _create_route_recursive(route_node_set, reference_route, current_route, start_node, end_node):
    route = None

    if reference_route is not None:
        if current_route.length > reference_route.length:
            return reference_route
        route = reference_route.copy()

    if len(route_node_set) == 0:
        current_route.add_node_at_start(start_node)
        current_route.add_node_at_end(end_node)
        return _select_shortest_route(route, current_route)
    
    for k in route_node_set:
        iteration_route = current_route.copy()
        remaining_node_set = route_node_set.copy()
        current_node = _extract_from_node_set(k, remaining_node_set)
        iteration_route.add_node_at_end(current_node)
        
        route = _create_route_recursive(remaining_node_set, route, iteration_route, start_node, end_node)

    return route


def _create_route(route_node_set, start_system_name = None, end_system_name = None):
    start_node = None
    end_node = None

    if start_system_name is not None:
        start_node = _extract_from_node_set(start_system_name, route_node_set)
    if end_system_name is not None:
        end_node = _extract_from_node_set(end_system_name, route_node_set)
    if start_system_name == end_system_name:
        end_node = start_node

    shortest_route = _create_route_recursive(route_node_set, None, Route(), start_node, end_node)

    return shortest_route


def create_route(system_list, start_system_name = None, end_system_name = None):
    route_node_set = _create_route_node_set(system_list)
    return _create_route(route_node_set, start_system_name, end_system_name)


## TESTS ##

_test_system_descriptor_1 = { 'name': 'system name 1', 'x': 3.5, 'y': 2, 'z': -5.5 }
_test_system_descriptor_2 = { 'name': 'system name 2', 'x': 30.5, 'y': 91, 'z': -0.5222 }
_test_system_descriptor_3 = { 'name': 'system name 3', 'x': 7.0, 'y': -12.2, 'z': -15.5 }
_test_system_descriptor_4 = { 'name': 'system name 4', 'x': 20, 'y': 70, 'z': 2.543 }

def _create_test_system_list():
    test_system_list = []
    test_system_list.append(EdpSystem(_test_system_descriptor_1))
    test_system_list.append(EdpSystem(_test_system_descriptor_2))
    test_system_list.append(EdpSystem(_test_system_descriptor_3))
    test_system_list.append(EdpSystem(_test_system_descriptor_4))
    return test_system_list


def _should_create_a_route_node_set():
    sl = _create_test_system_list()

    rn = _create_route_node_set(sl)
    
    assert len(rn) == 4
    assert rn[sl[0].name].system.name == sl[0].name
    assert rn[sl[1].name].system.name == sl[1].name
    assert rn[sl[2].name].system.name == sl[2].name
    assert rn[sl[3].name].system.name == sl[3].name
    assert len(rn[sl[0].name].distance_to) == len(rn) - 1
    assert len(rn[sl[1].name].distance_to) == len(rn) - 1
    assert len(rn[sl[2].name].distance_to) == len(rn) - 1
    assert len(rn[sl[3].name].distance_to) == len(rn) - 1


def _should_find_the_shortest_route_with_no_start_and_no_end():
    sl = _create_test_system_list()

    route = create_route(sl)

    assert len(route.node_list) == 4
    assert route.length < 111.85 and route.length > 111.80


def _should_find_the_shortest_route_with_a_start_system():
    sl = _create_test_system_list()
    
    start_system_name = sl[2].name
    route = create_route(sl, start_system_name)
    
    assert len(route.node_list) == 4
    assert route.node_list[0].system.name == start_system_name
    assert route.length < 111.85 and route.length > 111.80

    start_system_name = sl[0].name
    route = create_route(sl, start_system_name)
    
    assert len(route.node_list) == 4
    assert route.node_list[0].system.name == start_system_name
    assert route.length < 126.56 and route.length > 126.54


def _should_find_the_shortest_route_with_a_end_system():
    sl = _create_test_system_list()
    
    end_system_name = sl[1].name
    route = create_route(sl, None, end_system_name)
    
    assert len(route.node_list) == 4
    assert route.node_list[3].system.name == end_system_name
    assert route.length < 111.85 and route.length > 111.80
    
    end_system_name = sl[3].name
    route = create_route(sl, None, end_system_name)
    
    assert len(route.node_list) == 4
    assert route.node_list[3].system.name == end_system_name
    assert route.length < 134.54 and route.length > 134.52


def _should_find_the_shortest_route_with_start_and_end_system():
    sl = _create_test_system_list()
    
    start_system_name = sl[2].name
    end_system_name = sl[1].name
    route = create_route(sl, start_system_name, end_system_name)
    
    assert len(route.node_list) == 4
    assert route.node_list[0].system.name == start_system_name
    assert route.node_list[3].system.name == end_system_name
    assert route.length < 111.85 and route.length > 111.80
    
    start_system_name = sl[3].name
    end_system_name = sl[0].name
    route = create_route(sl, start_system_name, end_system_name)
    
    assert len(route.node_list) == 4
    assert route.node_list[0].system.name == start_system_name
    assert route.node_list[3].system.name == end_system_name
    assert route.length < 148.30 and route.length > 148.28


def tests():
    _should_create_a_route_node_set()
    _should_find_the_shortest_route_with_no_start_and_no_end()
    _should_find_the_shortest_route_with_a_start_system()
    _should_find_the_shortest_route_with_a_end_system()
    _should_find_the_shortest_route_with_start_and_end_system()
    log('edp_router: OK')
