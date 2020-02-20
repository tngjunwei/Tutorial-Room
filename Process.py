import pickle

def getDay(day_str):
    if day_str == 'MON':
        return 1
    elif day_str == 'TUE':
        return 2
    elif day_str == 'WED':
        return 3
    elif day_str == 'THU':
        return 4
    elif day_str == 'FRI':
        return 5
    elif day_str == 'SAT':
        return 6
    elif day_str == 'SUN':
        return 0

def getTime(time_str):
    time_str = time_str.strip()
    if time_str == "":
        return "None", "None"
    token = time_str.split("-")
    return int(token[0]), int(token[1])

def getModules(data):
    code =  data.keys() # list of tuples of module info (x, name, AU, remark)
    modules = {} # stores module info as id key
    lookuptable = {} # allows conversion of module code to id

    counter = 0 # associate each module x with an ID
    
    for x in code:
        c = x[0] #module code
        name = x[1] #module name

        #process module remarks
        remark = x[3]
        if name[-1] == '#':
            remark += ";Course is available as General Education Prescribed Elective"
            name = name.rstrip('#')
        
        if name[-1] == '^':
            remark += ";Self - Paced Course"
            name = name.rstrip('^')

        if name[-1] == '*':
            remark += ";Course is available as Unrestricted Elective"
            name = name.rstrip('*')

        au = x[2].strip(" ") #module credits
        modules[counter] = (c, name, au, remark) #id -> module info
        lookuptable[c] = counter #module code -> id
        counter += 1

    # stores processed info in local data
    pickle.dump(modules, open("module", "wb")) 
    pickle.dump(lookuptable, open("lookup", "wb"))

def getClasses(data, lookup):
    location = {}
    progress = 0

    for module, classes in data.items():

        #progress tracker
        if(progress % 10 == 0):
            print(progress, " out of ", len(data.items()))
        progress += 1

        #iterate through the list of classes for a particular module
        for i in range(len(classes)):
            room = classes[i][5] #str
            
            if(room.strip() == ""):
                continue #skip modules with no classes

            day = getDay(classes[i][3]) #int
            start, end = getTime(classes[i][4]) #int
            index = classes[i][0] #str
            type_of_class = classes[i][1] #str
            group = classes[i][2] #str
            remark = classes[i][6] #str
            id_num = lookup[module[0]]

            #stores/updates the classes held in a particular room
            if room in location:
                location[room].update({ (day, start, end): (id_num, type_of_class, index, group, remark) })
            else:
                location[room] = { (day, start, end): (id_num, type_of_class, index, group, remark) }

    pickle.dump(location, open("classes", "wb")) #stores data locally

def getLocation(data):
    lookup_location = {}
    location = {}
    all_rooms = list(data.keys())
    all_rooms.sort()

    for i in range(len(all_rooms)):
        lookup_location[i] = all_rooms[i]
        location[all_rooms[i]] = i
    
    pickle.dump(location, open("location", "wb"))
    pickle.dump(lookup_location, open("lookuploc", "wb"))

def getModuleCode(modules, id):
    return modules[id][0]

data = pickle.load(open("data","rb"))
modules = pickle.load(open("module","rb")) #id -> module info (c, name, au, remark)
lookup = pickle.load(open("lookup","rb")) #mod code -> id
classes = pickle.load(open("classes", "rb")) #all class info at each location
location = pickle.load(open("location", "rb")) #all locations -> id
lookuploc = pickle.load(open("lookuploc", "rb")) #id -> all locations

def buildSchedule():
    
    data = pickle.load(open("data","rb"))
    getModules(data)
    modules = pickle.load(open("module","rb")) #id -> module info (c, name, au, remark)
    lookup = pickle.load(open("lookup","rb")) #mod code -> id
    getClasses(data, lookup)
    classes = pickle.load(open("classes", "rb")) #all class info at each location
    
    timetable = {}
    for key, all_classes in classes.items():
        timetable[key] = [[None], [None], [None], [None], [None], [None], [None]] #empty array for each day
        print(timetable[key])

        for datetime, lecture in all_classes.items():
            day = datetime[0]
            start = datetime[1]
            end = datetime[2]

            module_code = getModuleCode(modules, lecture[0])
            type_of_class = lecture[1]
            index = lecture[2]

            x = (start, end, module_code, type_of_class, index)
            timetable[key][day].append(x)
        
        for i in range(7):
            timetable[key][i].pop(0)
            timetable[key][i].sort()

    pickle.dump(timetable, open("timetable", "wb"))
