import requests
import os
import csv
from bs4 import BeautifulSoup
import pickle

url = 'https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1' # Retrieve page for each code
url_menu = 'https://wish.wis.ntu.edu.sg/webexe/owa/aus_schedule.main' # Retrieve code for each year

formdata = {
'acadsem':'2019;2',
'r_course_yr': '',  #blank, to be filled from url_menu
'r_subj_code': 'Enter+Keywords+or+Course+Code',
'r_search_type': 'F',
'boption': 'CLoad',
'staff_access': 'False' }

#get code, name, AU, remark (first tr -> td)
def getCourseDetail(table):
    tr = table.find_all('tr')

    #Code, name, AU
    brief_details = tr[0].find_all('td')
    code = brief_details[0].get_text()
    name = brief_details[1].get_text()
    credit = brief_details[2].get_text()

    tr.pop(0) # Remove course details, to start looping from 0
    req = []

    if(len(tr) == 0): # No requisite
        return (code, name, credit, "")
    else:
        for i in range(len(tr)):
            x = tr[i].find_all('td')
            if(x[0].get_text() == "Remark:"):
                req.append("Remark:" + x[1].get_text())
            else:
                req.append(x[1].get_text())
    
    toRet = req[0]
    for i in range(1, len(req)):
        toRet = toRet + " " + req[i] #concatenate the multiple lines of prerequisite
    
    return (code, name, credit, toRet)

#index, type, group, day, time, venue, remark (every tr) in a tuple for each course
def getCourseSchedule(table):
    toRet = []
    x = table.find_all('tr')
    index = ''
    for i in range(1, len(x)):
        y = x[i].find_all('td')
        if(index == ''): # get index of class from first row of table
            index = y[0].get_text()
        elif(y[0].get_text() != ''): # if encounters a new index, update index
            index = y[0].get_text()

        type_of_class = y[1].get_text()
        group = y[2].get_text()
        day = y[3].get_text()
        time = y[4].get_text()
        venue = y[5].get_text()
        remark = y[6].get_text()

        toRet.append((index, type_of_class, group, day, time , venue, remark))

    return toRet # contains a tuple of all class schedule details for the module

# Get all the module code to be used for GetDetail()
def getCourse():
    arr = []
    response = requests.get(url_menu)
    soup = BeautifulSoup(response.text, 'html.parser')
    course_option = soup.find(attrs={"name" : "r_course_yr"}) # finds the selection menu containing the module code
    course_yr = course_option.find_all('option') # gets the HTML containing each module code
    for i in range(len(course_yr)):
        x = course_yr[i].get('value')
        if(x != ''):
            arr.append(x)

    return arr

# returns a list of dictionary of (code, name, AU, remark): [(index, type, group, day, time, venue, remark)]
def getDetail(course):
    dictionary = {}
    formdata['r_course_yr'] = course
    response = requests.post(url, data=formdata)
    soup = BeautifulSoup(response.text, 'html.parser')
    x = soup.find_all("table") # the schedule for each course -> many tables of different modules

    for i in range(0,len(x),2):
        detail = getCourseDetail(x[i])
        schedule = getCourseSchedule(x[i+1])
        dictionary[detail] = schedule

    return dictionary  # contains the entire course schedule data extracted

def storeData():
    data = {}
    arr = getCourse()
    for i in range(len(arr)):

        #progress tracker
        if(i % 10 == 0):
            print(i, " out of ", len(arr))

        x = getDetail(arr[i]) # dictionary of modules in the course

        for mod, sch in x.items():
            if mod in data: #if module already in data, update
                data[mod] += sch
            else:   #if module not in data, add it
                data[mod] = sch

    with open('data', 'wb') as file:
        pickle.dump(data, file) #stores data locally to prevent subsequent downloading


storeData()