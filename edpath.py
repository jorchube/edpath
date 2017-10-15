#!/usr/bin/env python3

import argparse
from support.logging import log

import edp_modules.edp_db as edp_db
import edp_modules.edp_system as edp_system
import edp_modules.edp_router as edp_router


def _run_tests():
    edp_db.tests()
    edp_system.tests()
    edp_router.tests()


def _check_arguments(args):
    start_system = None
    end_system = None

    if args.tests:
        _run_tests()
        exit(0)

    if args.refresh:
        edp_db.retrieve_database()
        log('Latest systems database has been downloaded')

    if args.list is None:
        log('list argument ([-l] or [--list]) is required')
        exit(0)

    if args.start is not None:
        start_system = " ".join(args.start).upper().strip()

    if args.end is not None:
        end_system = " ".join(args.end).upper().strip()

    system_names_list = []
    system_names_list_tmp = " ".join(args.list).split(",")
    for system_name in system_names_list_tmp:
        system_names_list.append(system_name.strip().upper())

    return (system_names_list, start_system, end_system)


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


def _compute_route(system_names_list, start_name, end_name):
    system_list = _create_system_list(system_names_list, start_name, end_name)
    return edp_router.create_route(system_list, start_name, end_name)



parser = argparse.ArgumentParser()
required = parser.add_argument_group("required arguments")
required.add_argument("-l", "--list", nargs = "*", help = "List of systems to compute the route")
parser.add_argument("-s", "--start", nargs = "*", help = "Starting system for the route")
parser.add_argument("-e", "--end", nargs = "*", help = "Ending system for the route")
parser.add_argument("--refresh", action = "store_true", help = "Downloads the latest version of the systems database before proceeding")
parser.add_argument("--tests", action = "store_true", help = "Run self tests")
args = parser.parse_args()

system_names_list, start_system_name, end_system_name = _check_arguments(args)
route = _compute_route(system_names_list, start_system_name, end_system_name)

route.pretty_print()



