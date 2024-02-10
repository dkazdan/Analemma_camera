"""
Raspberry Pi analemma picture-taking.
***CHANGE ECLIPSE DAY TO 2024 4 8 BEFORE DEPLOYING CAMERA BOX***
Started 20 January 2024
v. 2 29 Jan
DK

Mostly started from
https://www.tomshardware.com/how-to/use-picamera2-take-photos-with-raspberry-pi

Takes exposures daily around clock time of 8 April 2024 eclipse.
Timings are hard-coded by location. Consider finding library to do this automatically.
On eclipse day, takes photos from first contact, to second contact (totality),
moves away sun shade with servo motor,
takes photos from second contact through maximum eclipse to third contact,
Replaces sun shade,
Continues photos to fourth contact.

TODO:
Complete photo timing sequence for eclipse day.
Write photo timing sequences for non-eclipse days.
Write file transfer to Dropbox
Write directory space-clearing

"""

from picamera2 import Picamera2, Preview
from os import system
from time import sleep
from datetime import date, datetime, time, timedelta
import schedule

# eclipse yr/mo/day/hr/min/sec
# from https://www.timeanddate.com/eclipse/in/@41.49402,-81.57778?iso=20240408
eclipse_begins =datetime(2024,4,8,17,59,31) # first contact
totality_begins=datetime(2024,4,8,19,13,56) # second contact
totality_max   =datetime(2024,4,8,19,15,49) # maximum eclipse
totality_ends  =datetime(2024,4,8,19,17,42) # third contact
eclipse_ends   =datetime(2024,4,8,20,29, 8) # fourth contact
eclipse_date=eclipse_begins.date()
print('eclipse date: ', eclipse_date)
"""
TEST DATE: DELETE THIS FOR ACTUAL ANALEMMA RUN
"""
eclipse_date=date(2024,2,10) # DELETE THIS LINE
temp_storage_dir='/home/DK/Pictures/analemma_to_be_uploaded/'

picam2 = Picamera2()
# print(sensor_modes) # gives list of all the camera arguments
# sensor_modes = picam2.sensor_modes
# set resolution. I think this is highest:
full_res=picam2.sensor_resolution

# create configuration object

#camera_config=picam2.create_still_configuration(main={"size": (1920,1080)}, lores={"size": (640,480)}, display="lores")
camera_config=picam2.create_still_configuration(main={"size": (4608, 2592)}, lores={"size": (640,480)}, display="lores")
picam2.configure(camera_config)
#problem here: Can't close preview window, capture_file will hang
#picam2.start_preview(Preview.QTGL)
picam2.start()
# get a sample picture
# cannot use raw?
now = datetime.now()
iso_date = now.isoformat('T', 'seconds')
picam2.capture_file('/home/DK/Pictures/analemma_to_be_uploaded/analemma_'+ iso_date +'.png')

def move_servo(angle=0):
    print('rotating servo to ', angle)
    
def save_to_dropbox():
    print('Saving files to dropbox')
    
def open_directory_space():
    print('Opening directory space')

def take_photos(n=4, interval=15):	# interval in seconds
    now = datetime.now()
    for i in range(0,n):
        # Get current ISO 8601 datetime in string format
        iso_date = now.isoformat('T', 'seconds')
        print('ISO DateTime:', iso_date)

        picam2.capture_file(temp_storage_dir+'analemma_'+ iso_date +'.png')
        print('taking picture ', i)
        next= now + timedelta(seconds=interval)
        print(now, next)
        while (next > now): # wait for given time interval
            now=datetime.now()
        now=next
        
def today_is_eclipse_day():
    if (date.today() == eclipse_date):
        return True
    else:
        return False
    
def take_analemma_photos():
    if today_is_eclipse_day():
        print('starting eclipse photos')
        timedif=totality_begins-eclipse_begins
        tenth_timedif=timedif/10
        # start exposures at FIRST CONTACT. Second contact in next exposure set
        take_photos(n=10, interval=tenth_timedif.total_seconds())# start at first contact. Second contact in next set
        # OPEN SHUTTER for corona exposures
        move_servo(180)
        # take TOTALITY pictures
        print('take totality pictures')
        timedif=totality_ends-totality_begins
        tenth_timedif=timedif/10
        take_photos(n=10, interval=tenth_timedif.total_seconds())# start at second contact. Third contact in next set
        # CLOSE SHUTTER
        move_servo(0)
        # take pictures THIRD to FOURTH CONTACT
        print('take pictures to fourth contact')
        timedif=eclipse_ends-totality_ends
        tenth_timedif=timedif/10
        take_photos(n=10, interval=tenth_timedif.total_seconds())# start at third contact. Fourth contact ends the sequence
    else: # skip ahead to regular analemma times
        print('No eclipse today: wait for second contact time')
        while (datetime.now().time() < totality_begins.time()):  # idle until eclipse time
            sleep(1)	# keeps microprocessor cooler than using pass here.
        timedif=totality_ends-totality_begins # same times as eclipse totality
        tenth_timedif=timedif/10
        print('starting regular daily analemma photos')
        # 11 photos over 10 intervals
        take_photos(n=11, interval=tenth_timedif.total_seconds())# start at second contact. Third contact in next set

def hms_str(dt): # create string for schedule from datetime objecti 
    hms_string= str(dt.hour)+':'\
               +str(dt.minute)+':'\
               +str(dt.second)
    return hms_string
    
# set up the analemma schedule
eclipse_begins_str=hms_str(eclipse_begins)
schedule.every().day.at(eclipse_begins_str).do(take_analemma_photos)

while True:
    schedule.run_pending()
    sleep(1)  # keeps microprocessor cooler

print('\ndone')