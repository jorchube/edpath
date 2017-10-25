#!/usr/bin/env python3

from tkinter import *
import tkinter.messagebox as messagebox

from support.logging import log
import edp_modules.edp_controller as edp_controller

root = Tk(className="EDPath")

systemList = StringVar()
startSystem = StringVar()
endSystem = StringVar()
startSystemCheckState = IntVar()
endSystemCheckState = IntVar()


def _check_arguments():
    system_names_list = []
    start_system = None
    end_system = None
    
    if startSystemCheckState.get() is 1:
        start_system = startSystem.get().upper().strip()
    if endSystemCheckState.get() is 1:
        end_system = endSystem.get().upper().strip()

    system_names_list_tmp = systemList.get().split(",")
    for system_name in system_names_list_tmp:
        system_names_list.append(system_name.strip().upper())

    log("system list: {0}".format(system_names_list))
    log("start: {0}".format(start_system))
    log("end: {0}".format(end_system))

    return (system_names_list, start_system, end_system)


def calculateRouteButtonPressed():
    system_names_list, start_system_name, end_system_name = _check_arguments()
    route = edp_controller.compute_route(system_names_list, start_system_name, end_system_name)
    messagebox.showinfo("Computed Route", route.pretty_string())


startSystemCheck = Checkbutton(root, text="Start System", variable=startSystemCheckState, onvalue=1, offvalue=0)
startSystemCheck.pack()

startSystemTextEntry = Entry(root, textvariable=startSystem)
startSystemTextEntry.pack()

endSystemCheck = Checkbutton(root, text="End System", variable=endSystemCheckState, onvalue=1, offvalue=0)
endSystemCheck.pack()

endSystemTextEntry = Entry(root, textvariable=endSystem)
endSystemTextEntry.pack()

systemListLabel = Label(root, text="System List:")
systemListLabel.pack()

systemListTextEntry = Entry(root, textvariable=systemList, width=100)
systemListTextEntry.pack()

calculateRouteButton = Button(None, text="Calculate Route", command=calculateRouteButtonPressed)
calculateRouteButton.pack()

root.mainloop()
