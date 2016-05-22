# FuPlanter
FuPlanter - Garden Monitor - Weather, Ground Moisture, Plant Growth

Please read [a link](https://github.com/gstephan30/FuPlanter/Project_Overview.pdf) Project_Overview.pdf for more details.

Twitter Overview: https://twitter.com/FuPlanter<br />
Photo upload: https://www.flickr.com/photos/125695156@N08/<br />
Weather Station Data: https://www.wunderground.com/personal-weather-station/dashboard?ID=ITHURING3<br />

Picture of the Prototype: https://goo.gl/photos/ya9PyC1QEwmJoXnf7<br />

Setting up the Raspberry Pi for remote control and needed libaries:<br />
<code>sudo apt-get install update</code><br />
<code>sudo apt-get install upgrade</code><br />
<code>sudo apt-get install gnome-schedule</code><br />
<code>sudo apt-get install tightvncserver</code><br />
<code>sudo apt-get install python-imaging python-imaging-tk python-pip python-dev git</code><br />
<code>sudo pip install spidev</code><br />
<code>sudo pip install wiringpi</code><br />
<code>sudo apt-get install apache2</code><br />
<code>sudo apt-get install mysql-server</code><br />
<code>sudo apt-get install php5</code><br />
<code>sudo apt-get install php5-mysql</code><br />
<code>sudo pip install tweepy</code><br />
<code>pip install apscheduler==2.1.2</code><br />
<code>easy_install flickrapi</code><br />

Setting up the Sensors:<br />
<code>sudo nano /etc/modprobe.d/raspi-blacklist.conf</code><br />
Comment out the spi-bcm2708 line:<br />
<code>#blacklist spi-bcm2708</code><br />

Then run this to make it more permanent.<br />
<code>sudo modprobe spi-bcm2708</code><br />

Command for Input promt to get VNC connection<br />
<code>vncserver :1</code><br />


