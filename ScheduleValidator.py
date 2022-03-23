'''
This is the main file for ScheduleValidator. This is a recruitment task
@Tomasz Radwan

'''

import json
import datetime
import sys



#----DEFINITIONS-----


#Opening and Reading a json file
def openSchedule(FileName):
    '''
    Tries to open a json file, checking if it exists and contains correct data
    '''
    try:
        with open(FileName) as jsonFile:
            scheData=json.load(jsonFile)
    except FileNotFoundError as err :
        print(err)
        sys.exit()
    except json.decoder.JSONDecodeError :
        print('There is an incorrect value in json file, aborting... ')
        sys.exit()

    #returns python dict
    return scheData


# Task 1
def hoursPerMonthTrh(scheData):
    '''
    Monthly hours threshold validator, pass dictionary as an argument,
    returns False if there is too many hours per workday (incorrect), 
    returns True if Monthly Hours per workday do not execeed the limit (correct)    
    '''

    workDayCount = 0
    hCount = 0
    
    # Counts workdays in set month. 
    # --WARNING-- In this case, as month has not been specified in the task,
    # I have chosen January. Futhermore, from point 3 of the task, 
    # it seems that in this theoretical company, workdays are MON - SAT

    for i in range(len(scheData)):
        d=datetime.datetime(2022,1,i+1)
        if d.weekday()<6 :
            workDayCount += 1
  
  
    for i in range(len(scheData)):
        #Counts monthly hours from dict taken from json file
        hCount = hCount + scheData.get(str(i+1))
    
    if hCount/ workDayCount > 8:
        print('There is too many hours per workday') 
        return False
    else :
        print('Monthly hours per Workday value is correct: %s per workday' % (hCount/ workDayCount))
        return True


# Task 2
def sunWork(scheData):
    '''
    Checks if work is scheduled on Sunday, pass dictionary as an argument 
    returns True if there is work scheduled on sunday
    returns False if there is no work scheduled on sunday
    '''
    isWork = False
    for i in range(len(scheData)):
        d = datetime.datetime(2022,1,i+1)

        if d.weekday() == 6 and (scheData.get(str(i+1))>0): 
            print('Warning: there is work scheduled on a Sunday: %s' % d.strftime('%x'))
            isWork= True

    return isWork


# Task 3
def overtimeCount(scheData):
    '''
    Overtime hours counter. Pass dictionary as an argument,
    returns count of overtime hours
    '''
    overH = 0
    for i in range(len(scheData)):
        d = datetime.datetime(2022,1,i+1)

        # Checks if [i] day is a Sunday
        if d.weekday() == 6 :
            overH = overH + (scheData.get(str(i+1)))

        # Checks if [i] day has more then 8 hours of work within in
        elif (scheData.get(str(i+1))) > 8:
            overH = overH + (scheData.get(str(i+1))-8)

    print('There is %s hours of overtime scheduled' % round(overH,2))
    return round(overH,2)


# Task 4
# ---WARNING---: Neither task or data file does specify working hours
# As there is only workhours COUNT in the file (as requested in the task)
# I am assuming that every workday starts at 8:00 am

def breakCheck(scheData):
    '''
    11 hours break check - Validates mandatory 11 hours break
    Pass dictionary as an argument
    returns True if there are 11 hours breaks between every day of work
    returns False if there is at lest one break missing
    '''
    startingHour = 8
    brkCheck = True
    for i in range(len(scheData)-1):
        #Sets current and next workday, with starting hour - 8.00 am
        d=datetime.datetime(2022,1,i+1,startingHour)
        f=datetime.datetime(2022,1,i+2,startingHour)

        #Calculates work end hour
        endWorkTime = (d+datetime.timedelta(hours=(scheData.get(str(i+1)))))

        #Checks hour delta between end of a workday and start of the next one 
        if (f-endWorkTime) < datetime.timedelta(hours=11):
            print('On %s break between end of this workday and start of the next one is only: %s' %(d.strftime('%x'),f-endWorkTime))
            brkCheck = False
            
    return brkCheck
        
#------Main program Logic----------


def main():
    #Opening a Schedule
    currentSchedule = openSchedule ('Styczen2022.json')

    #Checking threshold of hours per workdays
    if hoursPerMonthTrh(currentSchedule) == True:
        print('-'*30+'Validation 1 - Passed '+'-'*30)
    else:
        print('-'*30+'Validation 1 - Failed '+'-'*30)

        
    #Checking if there is work scheduled for Sunday
    if sunWork(currentSchedule) == True:
        print('-'*30+'Validation 2 - Failed '+'-'*30)
    else:
        print('-'*30+'Validation 2 - Passed '+'-'*30)


    #Counting overtime hours
    overtimeCount(currentSchedule)
    print('-'*30+'Validation 3 - Passed '+'-'*30)

    #Checking 11hour breaks
    if breakCheck(currentSchedule) == True:
        print('11 Hours breaks are kept through the month')
        print('-'*30+'Validation 4 - Passed '+'-'*30)
    else:
        print('-'*30+'Validation 4 - Failed '+'-'*30)
    
if __name__ == '__main__':
    main()
    sys.exit()
