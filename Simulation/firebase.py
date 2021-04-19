#!/usr/bin/env python

import os
import sys
import optparse
import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyDYQXZjbRQ9wLOaqXH-MMgef4mnATIsS_8",
    "authDomain": "parking-sumo.firebaseapp.com",
    "databaseURL": "https://parking-sumo-default-rtdb.firebaseio.com/",
    "projectId": "parking-sumo",
    "storageBucket": "parking-sumo.appspot.com",
    "messagingSenderId": "1013612292554",
    "appId": "1:1013612292554:web:795bfcf04a9744b4828733",
    "measurementId": "G-XFP4JR8QTY"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()

db.child("bookingstatus").set("true")

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # Checks for the binary in environ vars
import traci


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                          default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options


# contains TraCI control loop
def run():
    step = 0

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        step = step + 1
    print(step)
    traci.close()
    sys.stdout.flush()

    # main entry point


if __name__ == "__main__":
    options = get_options()

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "parking.sumocfg",
                 "--tripinfo-output", "tripinfo.xml"])
    run()
