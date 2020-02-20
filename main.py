# Tutorial Room program - See which tutorial room is available for use
# DEPENDENCIES:
# Modules: 
# Spider.py - mine module, schedule data
# Process.py - process data, stores data in csv
# Viewer.py - a simple command line info output (AIM)
# User.py - a GUI for user navigation (Done Last)

# Functionalities:
# 1) See when tutorial room X is available
# 2) See which class is in tutorial room X now, and at a certain time
# 3) Which tutorial room is best for doing work in an N hour period

import pickle
import Spider
import Process

#INITIALISATION
DAYS = {0: "SUN", 1:"MON", 2:"TUE", 3:"WED", 4:"THU", 5:"FRI", 6:"SAT"}

#IF DATA DOES NOT EXIST, RUN THESE TO GET DATA
# Spider.storeData()
# Process.buildSchedule()


timetable = pickle.load(open("timetable", "rb"))

# Functionality 1
def availTime(timetable, room):
    classes = timetable[room]

    for i in range(7):
        current = 0  #tracking time
        print("For ", DAYS[i], ":")
        if(len(classes[i]) == 0):
            print("Whole Day")
        else:
            print(current, " - ", classes[i][0][0])
            current = classes[i][0][1]
            for j in range(1, len(classes[i])):
                if(current != classes[i][j][0]):
                    print(current, " - ", classes[i][j][0])
                
                current = classes[i][j][1] #set time to end of class then loop again to see if it coincides with next class

            print(current, " - 2359")
        print("-----------------")

# Functionality 2
def checkClass(timetable, room, day, time):
    classes = timetable[room]
    room_schedule = classes[day]

    for i in range(len(room_schedule)):
        if(room_schedule[i][0] > time):
            print("There is no lesson")
            return
        elif(room_schedule[i][0] <= time and time < room_schedule[i][1]):
            print("There is lesson: ", room_schedule[i][2], " ", room_schedule[i][3])
            return


#Functionality 3 to be implemented