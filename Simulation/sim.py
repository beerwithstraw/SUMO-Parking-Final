#!/usr/bin/env python

import os
import random
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
    parking = 'open'
    step = 0

    next_count = 1
    prev_count = 0

    # Entry Routes
    traci.route.add('route_E1a', ["0a", "1a"])
    traci.route.add('route_E1b', ["0a", "1a", "1b"])
    traci.route.add('route_E3a', ["0a", "3a"])
    traci.route.add('route_E3b', ["0a", "3b"])
    traci.route.add('route_E5', ["0a", "5"])

    # Exit Routes
    traci.route.add('route_L1a', ["1a", "8"])
    traci.route.add('route_L1b', ["1b", "0b"])
    traci.route.add('route_L3a', ["3a", "8"])
    traci.route.add('route_L3b', ["3b", "8"])
    traci.route.add('route_L5', ["5", "8"])

    if db.child("bookingstatus").get().val() == "true":
        value = db.child("bookingstatus").set("false")
        print(value)

    if db.child("bookingstatus").get().val() == "false":
        parkingslot = random.randint(1, 2)
        print(parkingslot)

        if parkingslot == 1:
            print(parkingslot)
            traci.vehicle.add('carX', 'route_E1a', typeID="reroutingType")
            db.child("bookingstatus").set("parked")
            print(traci.vehicle.getRouteID('carX'))
            print('***************')

        elif parkingslot == 2:
            print(parkingslot)
            traci.vehicle.add('carX', 'route_E1b', typeID="reroutingType")
            db.child("bookingstatus").set("parked")
            print(traci.vehicle.getRouteID('carX'))
            print('***************')

        elif parkingslot == 3:
            traci.vehicle.add('carX', 'route_E3a', typeID="reroutingType")
            db.child("bookingstatus").set("parked")
            print(traci.vehicle.getRouteID('carX'))
            print('***************')

        elif parkingslot == 4:
            traci.vehicle.add('carX', 'route_E3b', typeID="reroutingType")
            db.child("bookingstatus").set("parked")
            print(traci.vehicle.getRouteID('carX'))
            print('***************')

        elif parkingslot == 5:
            traci.vehicle.add('carX', 'route_E5', typeID="reroutingType")
            db.child("bookingstatus").set("parked")
            print(traci.vehicle.getRouteID('carX'))
            print('***************')

        else:
            print('6')

    if db.child("bookingstatus").get().val() == "parked":
        if parkingslot == 1:
            print(parkingslot)
            # if db.child("bookingstatus").get().val() != "exiting":
            traci.vehicle.setParkingAreaStop('carX', '1', duration=100)
            # traci.vehicle.setRouteID('carX', 'route_L1a')
            traci.vehicle.setRoute('carX', ['1b', '0b'])

                # traci.vehicle.setParkingAreaStop('carX', '1', duration=5)
                # traci.vehicle.setRouteID('carX', 'route_L1a')

        elif parkingslot == 2:
            print(parkingslot)
            # if db.child("bookingstatus").get().val() != "exiting":
            traci.vehicle.setParkingAreaStop('carX', '2', duration=100)
            # traci.vehicle.setRouteID('carX', 'route_L1b')
            traci.vehicle.setRoute('carX', ['1b', '0b'])


                # traci.vehicle.setParkingAreaStop('carX', '2', duration=5)
                # traci.vehicle.setRouteID('carX', 'route_L1b')

        elif parkingslot == 3:
            print(parkingslot)
            traci.vehicle.setParkingAreaStop('carX', '4')

        elif parkingslot == 4:
            print(parkingslot)
            traci.vehicle.setParkingAreaStop('carX', '3')

        elif parkingslot == 5:
            print(parkingslot)
            traci.vehicle.setParkingAreaStop('carX', '5')

        else:
            print('yoo')
    else:
        pass

    if db.child("bookingstatus").get().val() == "exiting":
        if parkingslot == 1:
            # traci.vehicle.setParkingAreaStop('carX', '1', duration=0)
            traci.vehicle.setRouteID('carX', 'route_L1a')

        elif parkingslot == 2:
            # traci.vehicle.setParkingAreaStop('carX', '2', duration=0)
            traci.vehicle.setRouteID('carX', 'route_L1b')
        else:
            print('No vehicle here')

    else:
        print('no')

        # if (step <= 200):
        #     x, y = traci.vehicle.getPosition('car1')
        #     lon, lat = traci.simulation.convertGeo(x, y)
        #     print(lon, lat)
        #     # x2, y2 = traci.simulation.convertGeo(lon, lat, fromGeo=True)
        #     # print(x2, y2)
        #
        # if (step == 200):
        #     print('***************')
        #     print(traci.vehicle.getAccel("car1"))
        #     print(traci.vehicle.getRouteID('car1'))
        #     print(traci.vehicle.getLanePosition('car1'))
        #     print(traci.vehicle.getRoute('carX'))
        #     print(traci.vehicle.getRouteIndex('car1'))
        #
        #
        #
        # if (step == 220):
        #     traci.vehicle.remove('car1')

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        step = step + 1

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
