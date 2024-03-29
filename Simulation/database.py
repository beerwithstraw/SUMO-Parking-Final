#!/usr/bin/env python

import os
import random
import sys
import optparse
from multiprocessing import Process

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


def username1():
    # Car number and car status
    car_number = db.child("Users").child("username1").child("carnumber").get().val()
    car_status = db.child("Users").child("username1").child("carstatus").get().val()
    parkinglot = db.child("Users").child("username1").child("parkinglot").get().val()
    if car_number == 'ABC123' and car_status != 'idle':
        traci.simulationStep()

        # User presses button -- state changes from IDLE => BOOKED
        if db.child("Users").child("username1").child("carstatus").get().val() == 'booked':
            traci.simulationStep()

            parkinglot = db.child("Users").child("username1").child("parkinglot").get().val()

            if db.child("Users").child("username1").child("parkinglot").get().val() == 0:
                parkinglot = random.randint(1, 5)
                db.child("Users").child("username1").child("parkinglot").set(parkinglot)
                print("Newly Assigned parking Lot:", parkinglot)
            else:
                print("Assigned Parking Lot:", parkinglot)

            # Assigning parking route according to the allotted Parking Lot
            if parkinglot == 1:
                traci.vehicle.add(car_number, 'route_R1', typeID="reroutingType")  # Adding vehicle to simulation
                traci.vehicle.setRouteID(car_number,
                                         'route_R1')  # Setting route depending on the parking lot assigned
                print(traci.vehicle.getRouteID(car_number))

                traci.vehicle.setParkingAreaStop(car_number, 1,
                                                 10)  # Setting a parking area STOP at the parking lot

            elif parkinglot == 2:
                traci.vehicle.add(car_number, 'route_R2', typeID="reroutingType")
                traci.vehicle.setRouteID(car_number, 'route_R2')
                print(traci.vehicle.getRouteID(car_number))

                traci.vehicle.setParkingAreaStop(car_number, 2, 10)

            elif parkinglot == 3:
                traci.vehicle.add(car_number, 'route_R3', typeID="reroutingType")
                traci.vehicle.setRouteID(car_number, 'route_R3')
                print(traci.vehicle.getRouteID(car_number))

                traci.vehicle.setParkingAreaStop(car_number, 3, 10)

            elif parkinglot == 4:
                traci.vehicle.add(car_number, 'route_R4', typeID="reroutingType")
                traci.vehicle.setRouteID(car_number, 'route_R4')
                print(traci.vehicle.getRouteID(car_number))

                traci.vehicle.setParkingAreaStop(car_number, 4, 10)

            elif parkinglot == 5:
                traci.vehicle.add(car_number, 'route_R5', typeID="reroutingType")
                traci.vehicle.setRouteID(car_number, 'route_R5')
                print(traci.vehicle.getRouteID(car_number))

                traci.vehicle.setParkingAreaStop(car_number, 5, 10)

            db.child("Users").child("username1").child("carstatus").set("to_parking")

        # Parking lot assigned -- Car approaching to Parking Lot
        if db.child("Users").child("username1").child("carstatus").get().val() == 'to_parking':
            traci.simulationStep()
            # When car is parked -- Status update to PARKED
            if traci.vehicle.isStoppedParking(car_number):
                traci.simulationStep()
                db.child("Users").child("username1").child("carstatus").set("parked")

        # Endless parking loop -- Unless specified otherwise by USER
        if db.child("Users").child("username1").child("carstatus").get().val() == 'parked':
            traci.simulationStep()
            traci.vehicle.setParkingAreaStop(car_number, parkinglot, 5)

        # USER wants to exit parking
        if db.child("Users").child("username1").child("carstatus").get().val() == 'exiting':
            traci.simulationStep()
            traci.vehicle.setParkingAreaStop(car_number, parkinglot, 1)
            print('EXITING PARKING')

            db.child("Users").child("username1").child("carstatus").set("to_exit")

        if db.child("Users").child("username1").child("carstatus").get().val() == 'to_exit':
            traci.simulationStep()
            lane = traci.vehicle.getLaneID(car_number)

            if lane == '0b_0':
                db.child("Users").child("username1").child("carstatus").set("exited")

        if db.child("Users").child("username1").child("carstatus").get().val() == "exited":
            traci.simulationStep()
            print("Successfully exited. See you next time!")
            db.child("Users").child("username1").child("carstatus").set("idle")
            db.child("Users").child("username1").child("parkinglot").set(0)


def pulkit():
    # Car number and car status
    car_number = db.child("Users").child("Pulkit").child("carnumber").get().val()
    car_status = db.child("Users").child("Pulkit").child("carstatus").get().val()
    parkinglot = db.child("Users").child("Pulkit").child("carstatus").get().val()

    if car_number == 'AAA123' and car_status != 'idle':
        traci.simulationStep()

        # User presses button -- state changes from IDLE => BOOKED
        if db.child("Users").child("Pulkit").child("carstatus").get().val() == 'booked':
            traci.simulationStep()

            parkinglot = db.child("Users").child("Pulkit").child("parkinglot").get().val()

            if db.child("Users").child("Pulkit").child("parkinglot").get().val() == 0:
                # parkinglot = random.randint(1, 5)
                parkinglot = 5
                db.child("Users").child("Pulkit").child("parkinglot").set(parkinglot)
                print("Newly Assigned parking Lot:", parkinglot)
            else:
                print("Assigned Parking Lot:", parkinglot)

            # Assigning parking route according to the allotted Parking Lot
            if parkinglot == 1:
                traci.vehicle.add(car_number, 'route_R1', typeID="reroutingType")  # Adding vehicle to simulation
                traci.vehicle.setRouteID(car_number,
                                         'route_R1')  # Setting route depending on the parking lot assigned
                print(traci.vehicle.getRouteID(car_number))

                traci.vehicle.setParkingAreaStop(car_number, 1,
                                                 10)  # Setting a parking area STOP at the parking lot

            elif parkinglot == 2:
                traci.vehicle.add(car_number, 'route_R2', typeID="reroutingType")
                traci.vehicle.setRouteID(car_number, 'route_R2')
                print(traci.vehicle.getRouteID(car_number))

                traci.vehicle.setParkingAreaStop(car_number, 2, 10)

            elif parkinglot == 3:
                traci.vehicle.add(car_number, 'route_R3', typeID="reroutingType")
                traci.vehicle.setRouteID(car_number, 'route_R3')
                print(traci.vehicle.getRouteID(car_number))

                traci.vehicle.setParkingAreaStop(car_number, 3, 10)

            elif parkinglot == 4:
                traci.vehicle.add(car_number, 'route_R4', typeID="reroutingType")
                traci.vehicle.setRouteID(car_number, 'route_R4')
                print(traci.vehicle.getRouteID(car_number))

                traci.vehicle.setParkingAreaStop(car_number, 4, 10)

            elif parkinglot == 5:
                traci.vehicle.add(car_number, 'route_R5', typeID="reroutingType")
                traci.vehicle.setRouteID(car_number, 'route_R5')
                print(traci.vehicle.getRouteID(car_number))

                traci.vehicle.setParkingAreaStop(car_number, 5, 10)

            db.child("Users").child("Pulkit").child("carstatus").set("to_parking")

        # Parking lot assigned -- Car approaching to Parking Lot
        if db.child("Users").child("Pulkit").child("carstatus").get().val() == 'to_parking':
            traci.simulationStep()
            # When car is parked -- Status update to PARKED
            if traci.vehicle.isStoppedParking(car_number):
                traci.simulationStep()
                db.child("Users").child("Pulkit").child("carstatus").set("parked")

        # Endless parking loop -- Unless specified otherwise by USER
        if db.child("Users").child("Pulkit").child("carstatus").get().val() == 'parked':
            traci.simulationStep()
            parkinglot = db.child("Users").child("Pulkit").child("parkinglot").get().val()
            traci.vehicle.setParkingAreaStop(car_number, parkinglot, 5)

        # USER wants to exit parking
        if db.child("Users").child("Pulkit").child("carstatus").get().val() == 'exiting':
            traci.simulationStep()
            parkinglot = db.child("Users").child("Pulkit").child("parkinglot").get().val()
            traci.vehicle.setParkingAreaStop(car_number, parkinglot, 1)
            print('EXITING PARKING')

            db.child("Users").child("Pulkit").child("carstatus").set("to_exit")

        if db.child("Users").child("Pulkit").child("carstatus").get().val() == 'to_exit':
            traci.simulationStep()
            lane = traci.vehicle.getLaneID(car_number)

            if lane == '0b_0':
                db.child("Users").child("Pulkit").child("carstatus").set("exited")

        if db.child("Users").child("Pulkit").child("carstatus").get().val() == "exited":
            traci.simulationStep()
            print("Successfully exited. See you next time!")
            db.child("Users").child("Pulkit").child("carstatus").set("idle")
            db.child("Users").child("Pulkit").child("parkinglot").set(0)


def vinny():
    # Car number and car status
    car_number = db.child("Users").child("Vinny").child("carnumber").get().val()
    car_status = db.child("Users").child("Vinny").child("carstatus").get().val()
    parkinglot = db.child("Users").child("Vinny").child("parkinglot").get().val()

    if car_number == 'BBB123' and car_status != 'idle':
        traci.simulationStep()

        # User presses button -- state changes from IDLE => BOOKED
        if db.child("Users").child("Vinny").child("carstatus").get().val() == 'booked':
            traci.simulationStep()
            parkinglot = db.child("Users").child("Vinny").child("parkinglot").get().val()

            if db.child("Users").child("Vinny").child("parkinglot").get().val() == 0:
                # parkinglot = random.randint(1, 5)
                parkinglot = 4

                db.child("Users").child("Vinny").child("parkinglot").set(parkinglot)
                print("Newly Assigned parking Lot:", parkinglot)
            else:
                print("Assigned Parking Lot:", parkinglot)

            # Assigning parking route according to the allotted Parking Lot
            if parkinglot == 1:
                traci.vehicle.add(car_number, 'route_R1', typeID="reroutingType")  # Adding vehicle to simulation
                traci.vehicle.setRouteID(car_number,
                                         'route_R1')  # Setting route depending on the parking lot assigned
                print(traci.vehicle.getRouteID(car_number))

                traci.vehicle.setParkingAreaStop(car_number, 1,
                                                 10)  # Setting a parking area STOP at the parking lot

            elif parkinglot == 2:
                traci.vehicle.add(car_number, 'route_R2', typeID="reroutingType")
                traci.vehicle.setRouteID(car_number, 'route_R2')
                print(traci.vehicle.getRouteID(car_number))

                traci.vehicle.setParkingAreaStop(car_number, 2, 10)

            elif parkinglot == 3:
                traci.vehicle.add(car_number, 'route_R3', typeID="reroutingType")
                traci.vehicle.setRouteID(car_number, 'route_R3')
                print(traci.vehicle.getRouteID(car_number))

                traci.vehicle.setParkingAreaStop(car_number, 3, 10)

            elif parkinglot == 4:
                traci.vehicle.add(car_number, 'route_R4', typeID="reroutingType")
                traci.vehicle.setRouteID(car_number, 'route_R4')
                print(traci.vehicle.getRouteID(car_number))

                traci.vehicle.setParkingAreaStop(car_number, 4, 10)

            elif parkinglot == 5:
                traci.vehicle.add(car_number, 'route_R5', typeID="reroutingType")
                traci.vehicle.setRouteID(car_number, 'route_R5')
                print(traci.vehicle.getRouteID(car_number))

                traci.vehicle.setParkingAreaStop(car_number, 5, 10)

            db.child("Users").child("Vinny").child("carstatus").set("to_parking")

        # Parking lot assigned -- Car approaching to Parking Lot
        if db.child("Users").child("Vinny").child("carstatus").get().val() == 'to_parking':
            traci.simulationStep()
            # When car is parked -- Status update to PARKED
            if traci.vehicle.isStoppedParking(car_number):
                traci.simulationStep()
                db.child("Users").child("Vinny").child("carstatus").set("parked")

        # Endless parking loop -- Unless specified otherwise by USER
        if db.child("Users").child("Vinny").child("carstatus").get().val() == 'parked':
            traci.simulationStep()
            # parkinglot = db.child("Users").child("Vinny").child("parkinglot").get().val()
            traci.vehicle.setParkingAreaStop(car_number, parkinglot, 5)

        # USER wants to exit parking
        if db.child("Users").child("Vinny").child("carstatus").get().val() == 'exiting':
            traci.simulationStep()
            traci.vehicle.setParkingAreaStop(car_number, parkinglot, 1)
            print('EXITING PARKING')

            db.child("Users").child("Vinny").child("carstatus").set("to_exit")

        if db.child("Users").child("Vinny").child("carstatus").get().val() == 'to_exit':
            traci.simulationStep()
            lane = traci.vehicle.getLaneID(car_number)

            if lane == '0b_0':
                db.child("Users").child("Vinny").child("carstatus").set("exited")

        if db.child("Users").child("Vinny").child("carstatus").get().val() == "exited":
            traci.simulationStep()
            print("Successfully exited. See you next time!")
            db.child("Users").child("Vinny").child("carstatus").set("idle")
            db.child("Users").child("Vinny").child("parkinglot").set(0)


# def janedoe():
#     # Car number and car status
#     car_number = db.child("Users").child("Jane Doe").child("carnumber").get().val()
#     car_status = db.child("Users").child("Jane Doe").child("carstatus").get().val()
#     parkinglot = db.child("Users").child("Jane Doe").child("parkinglot").get().val()
#
#     if car_number == 'DEF123' and car_status != 'idle':
#         traci.simulationStep()
#
#         # User presses button -- state changes from IDLE => BOOKED
#         if db.child("Users").child("Jane Doe").child("carstatus").get().val() == 'booked':
#             traci.simulationStep()
#
#             parkinglot = db.child("Users").child("Jane Doe").child("parkinglot").get().val()
#
#             if db.child("Users").child("Jane Doe").child("parkinglot").get().val() == 0:
#                 parkinglot = random.randint(1, 5)
#                 db.child("Users").child("Jane Doe").child("parkinglot").set(parkinglot)
#                 print("Newly Assigned parking Lot:", parkinglot)
#             else:
#                 print("Assigned Parking Lot:", parkinglot)
#
#             # Assigning parking route according to the allotted Parking Lot
#             if parkinglot == 1:
#                 traci.vehicle.add(car_number, 'route_R1', typeID="reroutingType")  # Adding vehicle to simulation
#                 traci.vehicle.setRouteID(car_number,
#                                          'route_R1')  # Setting route depending on the parking lot assigned
#                 print(traci.vehicle.getRouteID(car_number))
#
#                 traci.vehicle.setParkingAreaStop(car_number, 1,
#                                                  10)  # Setting a parking area STOP at the parking lot
#
#             elif parkinglot == 2:
#                 traci.vehicle.add(car_number, 'route_R2', typeID="reroutingType")
#                 traci.vehicle.setRouteID(car_number, 'route_R2')
#                 print(traci.vehicle.getRouteID(car_number))
#
#                 traci.vehicle.setParkingAreaStop(car_number, 2, 10)
#
#             elif parkinglot == 3:
#                 traci.vehicle.add(car_number, 'route_R3', typeID="reroutingType")
#                 traci.vehicle.setRouteID(car_number, 'route_R3')
#                 print(traci.vehicle.getRouteID(car_number))
#
#                 traci.vehicle.setParkingAreaStop(car_number, 3, 10)
#
#             elif parkinglot == 4:
#                 traci.vehicle.add(car_number, 'route_R4', typeID="reroutingType")
#                 traci.vehicle.setRouteID(car_number, 'route_R4')
#                 print(traci.vehicle.getRouteID(car_number))
#
#                 traci.vehicle.setParkingAreaStop(car_number, 4, 10)
#
#             elif parkinglot == 5:
#                 traci.vehicle.add(car_number, 'route_R5', typeID="reroutingType")
#                 traci.vehicle.setRouteID(car_number, 'route_R5')
#                 print(traci.vehicle.getRouteID(car_number))
#
#                 traci.vehicle.setParkingAreaStop(car_number, 5, 10)
#
#             db.child("Users").child("Jane Doe").child("carstatus").set("to_parking")
#
#         # Parking lot assigned -- Car approaching to Parking Lot
#         if db.child("Users").child("Jane Doe").child("carstatus").get().val() == 'to_parking':
#             traci.simulationStep()
#             # When car is parked -- Status update to PARKED
#             if traci.vehicle.isStoppedParking(car_number):
#                 traci.simulationStep()
#                 db.child("Users").child("Jane Doe").child("carstatus").set("parked")
#
#         # Endless parking loop -- Unless specified otherwise by USER
#         if db.child("Users").child("Jane Doe").child("carstatus").get().val() == 'parked':
#             traci.simulationStep()
#             traci.vehicle.setParkingAreaStop(car_number, parkinglot, 5)
#
#         # USER wants to exit parking
#         if db.child("Users").child("Jane Doe").child("carstatus").get().val() == 'exiting':
#             traci.simulationStep()
#             traci.vehicle.setParkingAreaStop(car_number, parkinglot, 1)
#             print('EXITING PARKING')
#
#             db.child("Users").child("Jane Doe").child("carstatus").set("to_exit")
#
#         if db.child("Users").child("Jane Doe").child("carstatus").get().val() == 'to_exit':
#             traci.simulationStep()
#             lane = traci.vehicle.getLaneID(car_number)
#
#             if lane == '0b_0':
#                 db.child("Users").child("Jane Doe").child("carstatus").set("exited")
#
#         if db.child("Users").child("Jane Doe").child("carstatus").get().val() == "exited":
#             traci.simulationStep()
#             print("Successfully exited. See you next time!")
#             db.child("Users").child("Jane Doe").child("carstatus").set("idle")
#             db.child("Users").child("Jane Doe").child("parkinglot").set(0)


def johndoe():
    # Car number and car status
    car_number = db.child("Users").child("John Doe").child("carnumber").get().val()
    car_status = db.child("Users").child("John Doe").child("carstatus").get().val()
    parkinglot = db.child("Users").child("John Doe").child("parkinglot").get().val()

    if car_number == 'GHI123' and car_status != 'idle':
        traci.simulationStep()

        # User presses button -- state changes from IDLE => BOOKED
        if db.child("Users").child("John Doe").child("carstatus").get().val() == 'booked':
            traci.simulationStep()

            parkinglot = db.child("Users").child("John Doe").child("parkinglot").get().val()

            if db.child("Users").child("John Doe").child("parkinglot").get().val() == 0:
                parkinglot = random.randint(1, 5)
                db.child("Users").child("John Doe").child("parkinglot").set(parkinglot)
                print("Newly Assigned parking Lot:", parkinglot)
            else:
                print("Assigned Parking Lot:", parkinglot)

            # Assigning parking route according to the allotted Parking Lot
            if parkinglot == 1:
                # Adding vehicle to simulation
                traci.vehicle.add(car_number, 'route_R1', typeID="reroutingType")
                # Setting route depending on the parking lot assigned
                traci.vehicle.setRouteID(car_number, 'route_R1')
                print(traci.vehicle.getRouteID(car_number))
                # Setting a parking area STOP at the parking lot
                traci.vehicle.setParkingAreaStop(car_number, 1, 10)

            elif parkinglot == 2:
                traci.vehicle.add(car_number, 'route_R2', typeID="reroutingType")
                traci.vehicle.setRouteID(car_number, 'route_R2')
                print(traci.vehicle.getRouteID(car_number))
                traci.vehicle.setParkingAreaStop(car_number, 2, 10)

            elif parkinglot == 3:
                traci.vehicle.add(car_number, 'route_R3', typeID="reroutingType")
                traci.vehicle.setRouteID(car_number, 'route_R3')
                print(traci.vehicle.getRouteID(car_number))

                traci.vehicle.setParkingAreaStop(car_number, 3, 10)

            elif parkinglot == 4:
                traci.vehicle.add(car_number, 'route_R4', typeID="reroutingType")
                traci.vehicle.setRouteID(car_number, 'route_R4')
                print(traci.vehicle.getRouteID(car_number))

                traci.vehicle.setParkingAreaStop(car_number, 4, 10)

            elif parkinglot == 5:
                traci.vehicle.add(car_number, 'route_R5', typeID="reroutingType")
                traci.vehicle.setRouteID(car_number, 'route_R5')
                print(traci.vehicle.getRouteID(car_number))

                traci.vehicle.setParkingAreaStop(car_number, 5, 10)

            db.child("Users").child("John Doe").child("carstatus").set("to_parking")

        # Parking lot assigned -- Car approaching to Parking Lot
        if db.child("Users").child("John Doe").child("carstatus").get().val() == 'to_parking':
            traci.simulationStep()
            # When car is parked -- Status update to PARKED
            if traci.vehicle.isStoppedParking(car_number):
                traci.simulationStep()
                db.child("Users").child("John Doe").child("carstatus").set("parked")

        # Endless parking loop -- Unless specified otherwise by USER
        if db.child("Users").child("John Doe").child("carstatus").get().val() == 'parked':
            traci.simulationStep()
            traci.vehicle.setParkingAreaStop(car_number, parkinglot, 5)

        # USER wants to exit parking
        if db.child("Users").child("John Doe").child("carstatus").get().val() == 'exiting':
            traci.simulationStep()
            traci.vehicle.setParkingAreaStop(car_number, parkinglot, 1)
            print('EXITING PARKING')

            db.child("Users").child("John Doe").child("carstatus").set("to_exit")

        if db.child("Users").child("John Doe").child("carstatus").get().val() == 'to_exit':
            traci.simulationStep()
            lane = traci.vehicle.getLaneID(car_number)

            if lane == '0b_0':
                db.child("Users").child("John Doe").child("carstatus").set("exited")

        if db.child("Users").child("John Doe").child("carstatus").get().val() == "exited":
            traci.simulationStep()
            print("Successfully exited. See you next time!")
            db.child("Users").child("John Doe").child("carstatus").set("idle")
            db.child("Users").child("John Doe").child("parkinglot").set(0)


def stefan():
    # Car number and car status
    car_number = db.child("Users").child("Stefan").child("carnumber").get().val()
    car_status = db.child("Users").child("Stefan").child("carstatus").get().val()
    parkinglot = db.child("Users").child("Stefan").child("parkinglot").get().val()

    if car_number == 'CCC123' and car_status != 'idle':
        traci.simulationStep()

        # User presses button -- state changes from IDLE => BOOKED
        if db.child("Users").child("Stefan").child("carstatus").get().val() == 'booked':
            traci.simulationStep()

            parkinglot = db.child("Users").child("Stefan").child("parkinglot").get().val()

            if db.child("Users").child("Stefan").child("parkinglot").get().val() == 0:
                # parkinglot = random.randint(1, 5)
                parkinglot = 1
                db.child("Users").child("Stefan").child("parkinglot").set(parkinglot)
                print("Newly Assigned parking Lot:", parkinglot)
            else:
                print("Assigned Parking Lot:", parkinglot)

            # Assigning parking route according to the allotted Parking Lot
            if parkinglot == 1:
                # Adding vehicle to simulation
                traci.vehicle.add(car_number, 'route_R1', typeID="reroutingType")
                # Setting route depending on the parking lot assigned
                traci.vehicle.setRouteID(car_number, 'route_R1')
                print(traci.vehicle.getRouteID(car_number))
                # Setting a parking area STOP at the parking lot
                traci.vehicle.setParkingAreaStop(car_number, 1, 10)

            elif parkinglot == 2:
                traci.vehicle.add(car_number, 'route_R2', typeID="reroutingType")
                traci.vehicle.setRouteID(car_number, 'route_R2')
                print(traci.vehicle.getRouteID(car_number))
                traci.vehicle.setParkingAreaStop(car_number, 2, 10)

            elif parkinglot == 3:
                traci.vehicle.add(car_number, 'route_R3', typeID="reroutingType")
                traci.vehicle.setRouteID(car_number, 'route_R3')
                print(traci.vehicle.getRouteID(car_number))

                traci.vehicle.setParkingAreaStop(car_number, 3, 10)

            elif parkinglot == 4:
                traci.vehicle.add(car_number, 'route_R4', typeID="reroutingType")
                traci.vehicle.setRouteID(car_number, 'route_R4')
                print(traci.vehicle.getRouteID(car_number))

                traci.vehicle.setParkingAreaStop(car_number, 4, 10)

            elif parkinglot == 5:
                traci.vehicle.add(car_number, 'route_R5', typeID="reroutingType")
                traci.vehicle.setRouteID(car_number, 'route_R5')
                print(traci.vehicle.getRouteID(car_number))

                traci.vehicle.setParkingAreaStop(car_number, 5, 10)

            db.child("Users").child("Stefan").child("carstatus").set("to_parking")

        # Parking lot assigned -- Car approaching to Parking Lot
        if db.child("Users").child("Stefan").child("carstatus").get().val() == 'to_parking':
            traci.simulationStep()
            # When car is parked -- Status update to PARKED
            if traci.vehicle.isStoppedParking(car_number):
                traci.simulationStep()
                db.child("Users").child("Stefan").child("carstatus").set("parked")

        # Endless parking loop -- Unless specified otherwise by USER
        if db.child("Users").child("Stefan").child("carstatus").get().val() == 'parked':
            traci.simulationStep()
            traci.vehicle.setParkingAreaStop(car_number, parkinglot, 5)

        # USER wants to exit parking
        if db.child("Users").child("Stefan").child("carstatus").get().val() == 'exiting':
            traci.simulationStep()
            traci.vehicle.setParkingAreaStop(car_number, parkinglot, 1)
            print('EXITING PARKING')

            db.child("Users").child("Stefan").child("carstatus").set("to_exit")

        if db.child("Users").child("Stefan").child("carstatus").get().val() == 'to_exit':
            traci.simulationStep()
            lane = traci.vehicle.getLaneID(car_number)

            if lane == '0b_0':
                db.child("Users").child("Stefan").child("carstatus").set("exited")

        if db.child("Users").child("Stefan").child("carstatus").get().val() == "exited":
            traci.simulationStep()
            print("Successfully exited. See you next time!")
            db.child("Users").child("Stefan").child("carstatus").set("idle")
            db.child("Users").child("Stefan").child("parkinglot").set(0)


# contains TraCI control loop
def run():
    parking = db.child("admin").child("parking").get().val()

    # Entry and Exit Parking Routes -- adding to the system
    traci.route.add('route_R1', ["0a", "1a", "4", "0b"])
    traci.route.add('route_R2', ["0a", "1a", "1b", "0b"])
    traci.route.add('route_R3', ["0a", "1a", "2a", "3a", "3b", "2b", "4", "5", "6", "7", "8", "0b"])
    traci.route.add('route_R4', ["0a", "1a", "2a", "3a", "3b", "2b", "4", "5", "6", "7", "8", "0b"])
    traci.route.add('route_R5', ["0a", "1a", "4", "5", "6", "7", "8", "0b"])

    # Not necessary loop -- increases complexity
    while parking == 'open':
        traci.simulationStep()

        Process(target=username1()).start()
        Process(target=pulkit()).start()
        Process(target=vinny()).start()
        # Process(target=janedoe()).start()
        Process(target=johndoe()).start()
        Process(target=stefan()).start()

        # Step system to implement slot based parking assistance system
        parking = db.child("admin").child("parking").get().val()
    traci.close()
    sys.stdout.flush()


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
#    list = []
#
# def user():
#    if traci.simulationStep() % 5 == 0:
#        if db.child("Users").child(user).child("carstatus").get().val() == 'booked':
#            # Code for booked here
#
#    # Rest of the conditions for "carstatus"
#
#    if traci.simulationStep() % 5 == 0:
#        if db.child("Users").child(user).child("carstatus").get().val() == 'to_exit':
#            # Code for exiting car
#
#    # Remaining code
#
# def simulation():
#    parking = db.child("admin").child("parking").get().val()
#    while parking == 'open':
#        traci.simulationStep()
#
#        for Users in list:
#                Process(target=user).start()
#
#        parking = db.child("admin").child("parking").get().val()
#
#    traci.close()
#    sys.stdout.flush()
