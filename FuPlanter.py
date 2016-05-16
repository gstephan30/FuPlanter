#setup general libaries
from datetime import datetime
from apscheduler.scheduler import Scheduler
import time
import datetime
import sys
import os
import subprocess
 
now =datetime.datetime.now()
 
#twitter setup
import tweepy
consumer_key="LONGKEY"
consumer_secret="LONGSECTRET"
access_token="INCREDIBLE_LONG_TOKEN"
access_token_secret="INCREDIBLE_LONG_SECRET"
#"logs in" to twitter,
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#Flickr Setup
import flickrapi
api_key = 'LONGKEY'
api_secret = 'SMALLERSECRET'
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')
(token, frob) = flickr.get_token_part_one(perms='write')
if not token: raw_input("Press ENTER after you authorized this program")
flickr.get_token_part_two((token, frob))
 
#the adc's SPI setup
import spidev
spi = spidev.SpiDev()
spi.open(0, 0)
 
#mysql wirting setup
import MySQLdb
con = MySQLdb.connect('localhost','root','fuplanter','fuplanter');
cursor = con.cursor()
 
#adds mysql table
global table_number
table_number = 0
 
#Variable Setup
ontime = 60

#adc reading
def readadc(adcnum): 
# read SPI data from MCP3008 chip
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    adcout = ((r[1] & 3) << 8) + r[2]
    return adcout
       
def hourlyUpdate():
    print "-----start reading-----\n"
     
    time.sleep(1)
     
    sampleTime = time.ctime()

    mst1 = 1024-readadc(0)
    mst2 = 1024-readadc(3)
    mst3 = 1024-readadc(4)
    mst4 = 1024-readadc(5)
    
    mst = str(format(float(100-(float((mst1)/1)/1024)*100),'.2f'))
    
    millivolts = (readadc(2)*(3300.0/1024.0))
    temp_c = (((millivolts - 100.0)/10)-40.0)
 
    tmp1 = str(format(((temp_c * 9.0 / 5.0) + 32),'.2f')) #converts to fahrenheit
 
    tmp2 = str(format(((temp_c * 1.0) + 0.0),'.2f')) #defines celcius
    
    ldr1 = str(format(((100-(float(readadc(1))/1024)*100)),'.2f')) #LDR data into a percentage
   
    print 'Capturing Data \n'
     
    #debug msg
    print sampleTime,"|","MST1:",mst1,"MST2:",mst2,"MST3:",mst3,"MST4:",mst4,"LDR1:",ldr1,"TMP2:",tmp2 #prints the debug 
     
    global table_number
    print 'Adding Data To MySQL-Table: ' + str(table_number)
 
    #adds data to mysql table
    global table_number
    cursor.execute('INSERT INTO fuplanter_table_'+ table_code +'(Time,mst1_V,mst2_V,mst3_V,mst4_V,ldr1_V,tmp2_C) VALUES(%s,%s,%s,%s,%s,%s,%s)',(sampleTime,mst1,mst2,mst3,mst4,ldr1,tmp2))
    con.commit() 
    print 'Data Captured, reset sensor \n'
     
    #picture of garden bed
    print 'Capturing Picture'
    picture_dir = '/home/pi/fuplanter/temp/pictures/'
    grab_cam = subprocess.Popen("sudo fswebcam -r 1280x960 -d /dev/video0 -q /home/pi/fuplanter/temp/pictures/%m-%d-%y-%H%M.jpg", shell=True) #replace as necessary
    grab_cam.wait()
    print 'Capture Successfull: ' + picture_dir + str(time.strftime('%m-%d-%y_%H-%M-%S')) + '.jpg'
     
    time.sleep(10)
     
    #renders image of graph
    print "Graph Render Start"
    global table_code
    os.system('php /var/www/fuplanter/renderScript.php ' + table_code ) #renders the .png file
    print "Graph Render Complete \n"
     
    #tweets the images and data
    send = 'Hlgt: ' + ldr1 + '% / ' + 'Temp: ' + tmp2 + ' Grad C' + ' / durchschn. Bodenf.: ' + mst + ' %' #builds the text of the tweet
    print "Tweeting Data:" , send  #for debug purposes
    api.update_status(send) #tweets the tweet
          
    print "\n-----finished-----"
     
def upload():
    
    time.sleep(.1)
    
    #finds the newest image in the directory
    print '\nUploading Picture To Flickr'
    picture_dir = '/home/pi/fuplanter/temp/pictures/'
    picture_allfiles = sorted(os.listdir(picture_dir), key=lambda p: os.path.getctime(os.path.join(picture_dir, p)))
    picture_newest = picture_dir+picture_allfiles[-1]
    print 'File for upload: ' + picture_newest #prints location and file to console
     
    #uploads the picture of the plants to flickr
    picture_title = 'Picture @ ' + str(sampleTime)
    picture_response = flickr.upload(filename=picture_newest, title=picture_title, format='etree') #uploads the file to flickr
    picture_photoID = picture_response.find('photoid').text #gets the id of the photo for constructing a url
    print 'Picture Upload Successful, Photo ID: ' + picture_photoID + '\n' #more debug info
    
    time.sleep(10)
    
    #finds the newest image in the directory
    print 'Uploading Graph To Flickr'
    graph_dir = '/home/pi/fuplanter/temp/graphs/'
    graph_allfiles = sorted(os.listdir(graph_dir), key=lambda p: os.path.getctime(os.path.join(graph_dir, p)))
    graph_newest = graph_dir+graph_allfiles[-1]
    print 'File for upload: ' + graph_newest #prints location and file to console
     
    graph_title = 'Graph @ ' + str(sampleTime)
    graph_response = flickr.upload(filename=graph_newest, title=graph_title, format='etree') #uploads the file to flickr
    graph_photoID = graph_response.find('photoid').text #gets the id of the photo for constructing a url
    print 'Graph Upload Successful, Photo ID: ' + graph_photoID + '\n' #more debug info
    
    time.sleep(10)
    
    #tweets the images and data
    send = ' Bild: ' + 'https://www.flickr.com/photos/125695156@N08/' + str(picture_photoID) + ' Graph: ' + 'https://www.flickr.com/photos/125695156@N08/'+ str(graph_photoID) #builds the text of the tweet
    print "Tweeting Pictures:" , send  #for debug purposes
    api.update_status(send) #tweets the tweet
        
def table_update():
     
    global table_number
    table_number = table_number + 1
     
    global table_code
    table_code = str(time.strftime('%m_%d_%y_%H_%M_%S')) + '__' + str(table_number)
    print 'Creating Table: ' + table_code
    cursor.execute('USE fuplanter')
    cursor.execute('CREATE TABLE fuplanter_table_'+ table_code +'(Sample_Number INT NOT NULL AUTO_INCREMENT PRIMARY KEY, Time VARCHAR(100), mst1_V VARCHAR(100), mst2_V VARCHAR(100), mst3_V VARCHAR(100), mst4_V VARCHAR(100), ldr1_V VARCHAR(100), tmp2_C VARCHAR(100) );')
    con.commit()

#deleting old pictures
def clear_pictures():
    
    path = r"/home/pi/fuplanter/temp/pictures/"
    now = time.time()
    for f in os.listdir(path):
        f = os.path.join(path, f)
        if os.stat(os.path.join(path,f)).st_mtime < now - 60:
            if os.path.isfile(f):
                os.remove(f)
                
#deleting old graphs
def clear_graphs():
    
    path = r"/home/pi/fuplanter/temp/graphs/"
    now = time.time()
    for f in os.listdir(path):
        f = os.path.join(path, f)
        if os.stat(os.path.join(path,f)).st_mtime < now - 60:
            if os.path.isfile(f):
                os.remove(f)                
                
clear_graphs()
clear_pictures()   
upload()
table_update()
hourlyUpdate()
     
#setting up scheduled events
scheduler = Scheduler(standalone=True)

scheduler.add_interval_job(clear_graphs, minutes=16)
scheduler.add_interval_job(clear_pictures, minutes=16)
scheduler.add_interval_job(upload, minutes=2)
scheduler.add_interval_job(hourlyUpdate, minutes=0.5)
scheduler.add_interval_job(table_update, minutes=15)
 
scheduler.start() #runs the program indefianately once every hour
