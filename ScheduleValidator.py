'''
This is the main file for ScheduleValidator. This is a recruitment task
@Tomasz Radwan
'''

import datetime
import json
import sys



#----DEFINITIONS-----


# Opening and Reading a json file
def get_schedule_data(filename: str) -> dict:
    """
    Tries to open a json file, checking if it exists and contains correct data
    """
    try:
        with open(filename) as json_file:
            schedule_data = json.load(json_file)
    except FileNotFoundError as error :
        print(error)
        sys.exit()
    except json.decoder.JSONDecodeError :
        print('There is an incorrect value in json file, aborting... ')
        sys.exit()
    else:
        # Returns python dict  
        return schedule_data    


# Task 1
def hours_per_month_threshold(schedule_data: dict) -> bool:
    """
    Monthly hours threshold validator
    returns False if there is too many hours per workday, 
    returns True otherwise
    """

    workday_count = 0
    hour_count = 0
    
    # Counts workdays in set month. 
    # --WARNING-- In this case, as month has not been specified in the task,
    # I have chosen January. Futhermore, from point 3 of the task, 
    # it seems that in this theoretical company, workdays are MON - SAT

    for i in range(len(schedule_data)):
        d=datetime.datetime(2022,1,i+1)
        if d.weekday()<6 :
            workday_count += 1
  
    hour_count = sum(schedule_data.values())
    hours_per_workday = hour_count / workday_count
    if hours_per_workday > 8:
        print('There is too many hours per workday') 
        return False
    else:
        print(f'Monthly hours per Workday value is correct: {hours_per_workday}')
        return True


# Task 2
def is_work_scheduled_for_sunday(schedule_data: dict) -> bool:
    """
    Checks if work is scheduled on Sunday, 
    returns True if there is work scheduled on sunday
    returns False otherwise
    """
    is_work = False
    for i in range(len(schedule_data)):
        d = datetime.datetime(2022,1,i+1)

        if d.weekday() == 6 and (schedule_data.get(str(i+1))>0): 
            print('Warning: there is work scheduled on a Sunday: %s' % d.strftime('%x'))
            is_work= True

    return is_work


# Task 3
def get_overtime_count(schedule_data: dict) -> int:
    """
    Overtime hours counter.
    returns count of overtime hours
    """
    overtime_hours = 0
    for i in range(len(schedule_data)):
        d = datetime.datetime(2022,1,i+1)

        # Checks if [i] day is a Sunday
        if d.weekday() == 6 :
            overtime_hours = overtime_hours + (schedule_data.get(str(i+1)))

        # Checks if [i] day has more then 8 hours of work within in
        elif (schedule_data.get(str(i+1))) > 8:
            overtime_hours = overtime_hours + (schedule_data.get(str(i+1))-8)

    print('There is %s hours of overtime scheduled' % round(overtime_hours,2))
    return round(overtime_hours,2)


# Task 4
# ---WARNING---: Neither task or data file does specify working hours
# As there is only workhours COUNT in the file (as requested in the task)
# I am assuming that every workday starts at 8:00 am

def breakCheck(schedule_data: dict) -> bool:
    """
    11 hours break check - Validates mandatory 11 hours break
    returns True if there are 11 hours breaks between every day of work
    returns False otherwise
    """
    starting_hour = 8
    break_check = True
    for i in range(len(schedule_data)-1):
        # Sets current and next workday, with starting hour - 8.00 am
        d=datetime.datetime(2022,1,i+1,starting_hour)
        f=datetime.datetime(2022,1,i+2,starting_hour)

        # Calculates work end hour
        end_work_time = (d+datetime.timedelta(hours=(schedule_data.get(str(i+1)))))

        # Checks hour delta between end of a workday and start of the next one 
        if (f-end_work_time) < datetime.timedelta(hours=11):
            print('On %s break between end of this workday and start of the next one is only: %s' %(d.strftime('%x'),f-end_work_time))
            break_check = False
            
    return break_check
        
#------Main program Logic----------


def main():
    # Opening a Schedule
    current_schedule = get_schedule_data('Styczen2022.json')
    separator = '-' * 30
    # Checking threshold of hours per workdays
    if hours_per_month_threshold(current_schedule) == True:
        print(f'{separator}+Validation 1 - Passed {separator}')
    else:
        print(f'{separator}+Validation 1 - Failed {separator}')

        
    # Checking if there is work scheduled for Sunday
    if is_work_scheduled_for_sunday(current_schedule) == True:
        print(f'{separator}+Validation 2 - Failed {separator}')
    else:
        print(f'{separator}+Validation 2 - Passed {separator}')


    # Counting overtime hours
    get_overtime_count(current_schedule)
    print(f'{separator}+Validation 3 - Passed {separator}')

    # Checking 11hour breaks
    if breakCheck(current_schedule) == True:
        print('11 Hours breaks are kept through the month')
        print(f'{separator}+Validation 4 - Passed {separator}')
    else:
        print(f'{separator}+Validation 4 - Failed {separator}')
    
if __name__ == '__main__':
    main()
    sys.exit()
