
from support.logging import log

import edp_modules.edp_db as edp_db
import edp_modules.edp_system as edp_system
import edp_modules.edp_router as edp_router



def run_tests():
    edp_db.tests()
    edp_system.tests()
    edp_router.tests()


def compute_route(system_names_list, start_name, end_name):
    system_list = _create_system_list(system_names_list, start_name, end_name)
    return edp_router.create_route(system_list, start_name, end_name)


def _complete_system_names_list(systems_list, start, end):
    if start is not None and start not in systems_list:
        systems_list.append(start)
    if end is not None and end not in systems_list:
        systems_list.append(end)


def _warn_for_unresolved_names(system_list, system_names_list):
    resolved_names = []
    
    for s in system_list:
        resolved_names.append(s.name)
    
    for n in system_names_list:
        if n not in resolved_names:
            log('Warning: Unable to resolve system {0}. Skipping it.'.format(n))


def _create_system_list(system_names_list, start_system_name, end_system_name):
    cache = edp_db.load_data()
    system_list = []
    _complete_system_names_list(system_names_list, start_system_name, end_system_name)
    
    for system_descriptor in cache:
        if system_descriptor['name'].upper() in system_names_list:
            system = edp_system.EdpSystem(system_descriptor)
            system_list.append(system)
        if len(system_list) == len(system_names_list):
            break

    _warn_for_unresolved_names(system_list, system_names_list)

    return system_list



