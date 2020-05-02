#  *** Vishnu Chakra SCHEDULER *** | v1.0 Developed By Jay Akbari
# DYNAMIC 24x7 PERIODIC MULTI SCHEDULER WITH ALARM
# ======================================================================================================================
# Suggestions & More on GITHUB/developerjay-jokerfriend
# ======================================================================================================================
# FEATURES
# Schedules 3 kind of activity reminders from user :-
#                1. Drink Water Reminder (to drink how much ML of water to meet 3.5L of water requirement.)
#                2. Eye Care Reminder (to wash eyes after certain minutes everyday)
#                3. Physical Activity Reminder ( to perform physical activity after certain minutes everyday.)
# ======================================================================================================================
# * USER ANALYTICS *
# Creates respective reminder Logs to view the reminder activity performance for the user.
# (VIEW LOG FILES OF YOUR REMINDERS IN "VISHNU CHAKRA SCHEDULER" FOLDER LOCATED WHERE YOU HAVE PERFORMED INSTALLATION.)
# ======================================================================================================================
# * DYNAMIC *
#   - USER can schedule time for which reminder will work in a day and how often reminders will repeat itself.
#   - USER can choose which reminders to activate
#   - Can activate one or more reminders simultaneously.
#   - User can use their own mp3 file audio to set their own kind of alarm for all reminders.
# =======================================================================================================================
# * PERIODIC *
#   - Once scheduled, it works 24x7 daily during the schedule time set by the user.
#   - reminders repeat themselves  after certain interval of minutes set by user.
# ========================================================================================================================
# * ALARM *
#   - Uses Pygame module to play alarm music in background via mp3 file when reminders occur.
#   - Replace .mp3 files with the same names in "VISHNU CHAKRA SCHEDULER" folder where you have performed installation.
# ========================================================================================================================

import time
import pygame

# flag to activate reminders
# 1.WATER = b for blue
# 2.EYE = r for red
# 3.PHYSICAL ACTIVITY = g for green
flag="none"

# Program Start Stop Times
start_time = 0 # 9AM = 09:00 == 900 , 12AM = 00:00 = 0 (remove any leading 0's)
end_time = 2359 # 23:59

# Activity Interval Period
water_period = 0 # minutes
pa_period = 0  # minutes
eye_period = 0  # minutes

# Initialization Of Schedule
WaterHit = 9999
EyeHit = 9999
PaHit = 9999

# music files:
water_file = 'water.mp3' # for water drinking
eye_file = 'eye.mp3' # for eye exercise
pa_file = 'physical_activity.mp3' # for physical activity

# Water Capacity
capacity=3500 # unit= ml


def NextHit(current_time, interval):
    # Returns updated hit time after addition of int(interval) and int(current time)

    hours = RenderHours(current_time)
    minutes = RenderMinutes((current_time))
    total_mins = minutes + interval

    # Hours >= 24 and minutes >= 60 OVERFLOW. MINUTES CAN INCREASE HOURS BUT not VICE VERSA
    if total_mins >= 60: # Mins Overflow So, Hours May/May Not overflow
        hours = hours + (total_mins // 60)
        if hours >= 24:
            hours = 0 + (hours % 24) # Hours Overflow
        total_mins = 0 + (total_mins % 60)
    return Adjust(hours, total_mins)


def Adjust(h,m): # intakes integer values
    if h==0:
        return m
    else:
        adjust= str(h)+str(Formate(m))
        return int(adjust)

def RenderMinutes(n):
    l = list(str(n))
    if len(str(n)) == 3:  # 900=9:00
        return int(l[1]+l[2])
    elif len(str(n)) == 4:
        return int(l[2]+l[3])
    else:  # len(str(n))==1 |  0=00:00 | len(str(start))==2 | 12:05 AM = 00:05 = 005 =5 | 12:50 = 0050 =50
        return n



def RenderHours(n):
    #Returns Hours from start_time and end_time variables or any other integer time
    l = list(str(n))
    if len(str(n))==3: #900=9:00
        return int(l[0])
    elif len(str(n))==4: #1245=12:45
        return int(l[0]+l[1])
    else: # len(str(n))==1 |  0=00:00 | len(str(start))==2 | 12:05 AM = 00:05 = 005 =5 | 12:50 = 0050 =50
        return 0

def MinsCount(start,end):
    num2=RenderHours(end)
    num1=RenderHours(start)
    if (num2-num1) != 0:
        if (num2 > num1):
            return (num2-num1)*60
        else: #(num1 > num 2)
            return (num1 - num2)*60
    else:
        return RenderMinutes(end)-RenderMinutes(start)



def Get_Date():
    # Fetch and return timestamp
    import datetime
    return datetime.datetime.now()

def Play(file):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)


def Formate(n):
    # To convert single digit numeral to double digit numeral. Eg 2 to 02.
    if (n in [0,1,2,3,4,5,6,7,8,9]):
          return "0"+ str(n)
    else: return n

def FetchTime():
    # for 12:00 AM only minutes are returned. eg.5 mins ,50 mins, etc
    # for any other time hours<>minutes are returned such that minutes are always 2 decimal places from LSB.
    # eg. 01:05 = 105. (where 1 is hour and 05 is minutes.) (remove front zeroes!)
    temp=time.localtime(time.time())
    return Adjust(temp.tm_hour, temp.tm_min)

def Start():
    global start_time, end_time
    return (FetchTime() == start_time)

def WaterDrinking():
    global WaterHit, water_file, water_period, capacity, start_time, end_time
    Play(water_file)
    capacity_drank_str = str((capacity // MinsCount(start_time, end_time)) * water_period)
    while (True):
        try:
            print(f"\nPLEASE DRINK {capacity_drank_str} ML OF WATER NOW IN ORDER TO DRINK TOTAL {capacity} ML OF WATER BETWEEN TIMINGS {NormalTime(start_time)} and {NormalTime(end_time)} !")
            if (int(input("Press 1 if Drank: ")) == 1):
                pygame.mixer.music.stop()
                string_water = str(Get_Date()) + "  Water Drank = " + capacity_drank_str + " ml\n"
                f = open("Water_Log.txt", "a")
                f.write(string_water)
                f.close()
                WaterHit = NextHit(FetchTime(), water_period)
                break
            else:
                print("\nPLEASE ENTER CORRECT INPUT.\n\n")
        except Exception as e:
            print(f"\nERROR: PLEASE ENTER CORRECT INPUT.\n\n")
    # < WHILE BREAK AREA >

def EyeEx():
    global EyeHit, eye_file, eye_period, start_time, end_time
    Play(eye_file)
    while (True):
        try:
            print(f"\nPlease Take Care Of Your EYES !")
            if (int(input("Press 1 if DONE: ")) == 1):
                pygame.mixer.music.stop()
                string_eyes = str(Get_Date()) + "  Took Care of My Eyes.\n"
                f = open("Eyes_Log.txt", "a")
                f.write(string_eyes)
                f.close()
                EyeHit = NextHit(FetchTime(), eye_period)
                break
            else:
                print("\nPLEASE ENTER CORRECT INPUT.\n\n")
        except Exception as e:
            print(f"\nERROR: PLEASE ENTER CORRECT INPUT.\n\n")
    # < WHILE BREAK AREA >


def PaActivity():
    global PaHit, pa_file, pa_period, start_time, end_time
    Play(pa_file)
    while (True):
        try:
            print(f"\nPlease Perform Some PHYSICAL ACTIVITY !")
            if (int(input("Press 1 if DONE: ")) == 1):
                pygame.mixer.music.stop()
                string_pa = str(Get_Date()) + "  Performed Some Physical Activity.\n"
                f = open("PhysicalActivity_Log.txt", "a")
                f.write(string_pa)
                f.close()
                PaHit = NextHit(FetchTime(), pa_period)
                break
            else:
                print("\nPLEASE ENTER CORRECT INPUT.\n\n")
        except Exception as e:
            print(f"\nERROR: PLEASE ENTER CORRECT INPUT.\n\n")
    # < WHILE BREAK AREA >


def Schedule():
    global  WaterHit, EyeHit, PaHit, start_time, end_time, water_period, eye_period, pa_period,flag
    if (Start()):
        print("\nVishnu Chakra SCHEDULER IS RUNNING...")
        if flag in ["b","br","bg","brg"]:
            WaterHit = NextHit(FetchTime(), water_period)
        if flag in ["r","br","rg","brg"]:
            EyeHit = NextHit(FetchTime(), eye_period)
        if flag in ["g","bg","rg","brg"]:
            PaHit = NextHit(FetchTime(), pa_period)

        while (FetchTime() != end_time):

            # CONCURRENCY of SCHEDULE in EXECUTION =( 1 or more activities in schedule being executed.)
            # SYNCHRONIZATION = (Syncs execution of activites when multiple activities collide to execute at a same time.)
            if WaterHit == FetchTime() and EyeHit == FetchTime() and PaHit == FetchTime():
                WaterDrinking()
                EyeEx()
                PaActivity()

            elif WaterHit == FetchTime() and EyeHit == FetchTime():
                WaterDrinking()
                EyeEx()
            elif WaterHit == FetchTime() and PaHit == FetchTime():
                WaterDrinking()
                PaActivity()
            elif PaHit == FetchTime() and EyeHit == FetchTime():
                PaActivity()
                EyeEx()
            # Water Drinking
            elif WaterHit == FetchTime():
                WaterDrinking()
                # Eye Activity
            elif EyeHit == FetchTime():
                EyeEx()
           # Physical Activity
            elif PaHit == FetchTime():
                PaActivity()
            else: pass
        print(f"\n\nVishnu Chakra SCHEDULER PAUSED AT TIME = {NormalTime(end_time)}\n"
              f"Vishnu Chakra SCHEDULER WILL RESUME AT TIME = {NormalTime(start_time)}\n"
              f"(SCHEDULER  will start only from {NormalTime(start_time)} till {NormalTime(end_time)} timings.)\n")
    else:
        print(f"\n\n# Vishnu Chakra SCHEDULER  will automatically start reminding from {NormalTime(start_time)} till {NormalTime(end_time)} timings.\n")

def RunForever(): # MASTER-PIECE
    # KEEP RUNNING PROGRAM FOR THE SCHEDULED ENVIRONMENT forever 24x7 EVERYDAY
    while(True):
        Schedule()
        while(not(Start())): continue


def ActivateActivity():
    global PaHit,WaterHit,EyeHit,flag
    print("\n\n====================== *** Welcome to Vishnu Chakra *** =========================\n"
          "================ DYNAMIC 24x7 PERIODIC MULTI SCHEDULER WITH ALARM ===============\n"
          "============================= Developed By Jay Akbari ===========================\n"
          "****** Suggestions & More on GITHUB = https://github.com/developerjay-jokerfriend\n\n")
    print("ACTIVATE REMINDERS\n"
          "Enter 1  --->  WATER DRINKING REMINDER\n"
          "Enter 2  --->  EYE CARE REMINDER\n"
          "Enter 3  --->  PHYSICAL ACTIVITY REMINDER\n"
          "(You can enter combinations of 1, 2 and 3 to activate multiple reminders.)\n"
          "(Eg. Enter '23' for activating option 2 and 3 both.)\n"
          )
    while (True):
        choice_activity = input("Enter: ")
        try:
            choice_activity = int(choice_activity)
            if choice_activity == 1:
                WaterHit = 0
                flag = "b"
                break
            elif choice_activity == 12 or choice_activity == 21:
                WaterHit = 0
                EyeHit = 0
                flag = "br"
                break
            elif choice_activity == 13 or choice_activity == 31:
                WaterHit = 0
                PaHit = 0
                flag = "bg"
                break
            elif choice_activity == 2:
                EyeHit = 0
                flag = "r"
                break
            elif choice_activity == 23 or choice_activity == 32:
                EyeHit = 0
                PaHit = 0
                flag = "rg"
                break
            elif choice_activity == 3:
                PaHit = 0
                flag = "g"
                break
            elif choice_activity in [123, 132, 213, 231, 312, 321]:
                WaterHit = 0
                EyeHit = 0
                PaHit = 0
                flag = "brg"
                break
            else:
                print("\nInvalid Input! Enter Again.")

        except Exception as e:
            print(f"\nERROR: Invalid Input! Enter Again.")


def SetRepeatMinutes():
    global flag, water_period, eye_period, pa_period
    while(True):
        try:
            print("\n\n\n# REPEAT REMINDER AFTER HOW MANY MINUTES ?")
            if flag == "b":
                m=input("--> MINUTES FOR WATER DRINKING REMINDER = ")
                water_period=int(m)
                break
            elif flag == "br":
                m=input("--> MINUTES FOR WATER DRINKING REMINDER = ")
                n = input("--> MINUTES FOR EYE CARE REMINDER = ")
                water_period = int(m)
                eye_period = int(n)
                break
            elif flag == "bg":
                m = input("--> MINUTES FOR WATER DRINKING REMINDER = ")
                n = input("--> MINUTES FOR PHYSICAL ACTIVITY REMINDER = ")
                water_period = int(m)
                pa_period=int(n)
                break
            elif flag == "rg":
                m = input("--> MINUTES FOR EYE CARE REMINDER = ")
                n = input("--> MINUTES FOR PHYSICAL ACTIVITY REMINDER = ")
                eye_period = int(m)
                pa_period = int(n)
                break
            elif flag == "brg":
                l = input("--> MINUTES FOR WATER DRINKING REMINDER = ")
                m = input("--> MINUTES FOR EYE CARE REMINDER = ")
                n = input("--> MINUTES FOR PHYSICAL ACTIVITY REMINDER = ")
                water_period = int(l)
                eye_period = int(m)
                pa_period = int(n)
                break
            elif flag == "r":
                m = input("--> MINUTES FOR EYE CARE REMINDER = ")
                eye_period = int(m)
                break
            elif flag == "g":
                m=input("--> MINUTES FOR PHYSICAL ACTIVITY REMINDER = ")
                pa_period=int(m)
                break
            else: print("\nInvalid Input. Please enter minutes in integers only!\n")
        except Exception as e:
            print(f"\nERROR: Invalid Input. Please enter minutes in integers only!\n")
def ValidateTimeFormate(time):
    l=list(time)
    if (" " in l): return False # Filter Spaces
    if not ((len(time)==5) and (l[2]==":")): return False
    try:
        if not((int(l[0]+l[1]) in range(24)) and (int(l[3]+l[4]) in range(60))):return False
    except:return False
    return True

def SetSchedule():
    global start_time, end_time
    print("\n\n\n# SCHEDULE TIME FOR REMINDERS TO WORK DAILY:")
    while(True):
        s_time=input("Enter Schedule Start Time in HH:MM - 24 hrs format\n"
                "(Example: Enter '13:30' to start schedule at 1.30 PM)"
                "\n\n--> Enter Schedule START Time (HH:MM): ")
        if ValidateTimeFormate(s_time):  break
        print("\n\n\nERROR: INVALID INPUT !!! \n")
    while(True):
        e_time=input("--> Enter Schedule END Time (HH:MM): ")
        if ValidateTimeFormate(e_time): break
        print("\n\n\nERROR: INVALID INPUT !!!\n Enter Schedule END Time in HH:MM - 24 hrs format\n"
              "(Example: Enter '13:30' to start schedule at 1.30 PM)\n")
    s_time=list(s_time)
    e_time=list(e_time)
    start_time = Adjust(int(s_time[0]+ s_time[1]), int(s_time[3]+ s_time[4]))
    end_time = Adjust(int(e_time[0]+ e_time[1]), int(e_time[3]+ e_time[4]))
    if end_time == start_time:
        print("\n\n\nERROR: Schedule START time CANNOT BE EQUAL to schedule END time!\nPlease Enter Again.")
        SetSchedule()



def NormalTime(t): #intakes integer XXXX My Special Format of Time, eg. start_time value.
    l=list(str(t))
    if len(str(t)) == 1:
        return ("00:0"+l[0])
    elif len(str(t)) == 2:
        return ("00:"+l[0]+l[1])
    elif len(str(t)) == 3:
        return ("0"+l[0]+ ":" +l[1]+l[2])
    else: #len(str(t)) == 4:
        return (l[0]+l[1]+ ":" +l[2]+l[3])


#--------------------------- PROGRAM START -------------------------

ActivateActivity() #1
SetRepeatMinutes() #2
SetSchedule() #3
RunForever() #4



