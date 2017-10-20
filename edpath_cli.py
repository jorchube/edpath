#!/usr/bin/env python3

import argparse

from support.logging import log
import edp_modules.edp_controller as edp_controller

def _check_arguments(args):
    start_system = None
    end_system = None

    if args.tests:
        edp_controller.run_tests()
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




parser = argparse.ArgumentParser()
required = parser.add_argument_group("required arguments")
required.add_argument("-l", "--list", nargs = "*", help = "List of systems to compute the route (colon separated)")
parser.add_argument("-s", "--start", nargs = "*", help = "Starting system for the route")
parser.add_argument("-e", "--end", nargs = "*", help = "Ending system for the route")
parser.add_argument("--refresh", action = "store_true", help = "Downloads the latest version of the systems database before proceeding")
parser.add_argument("--tests", action = "store_true", help = "Run self tests")
args = parser.parse_args()

system_names_list, start_system_name, end_system_name = _check_arguments(args)
route = edp_controller.compute_route(system_names_list, start_system_name, end_system_name)

route.pretty_print()



