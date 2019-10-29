#SET UP ENVIRONMENT

## install virtual display xvfb
$> sudo apt-get install xvfb xserver-xephyr

## install PyVirtualDisplay which is python wrapper for xvfb
$> sudo pip install pyvirtualdisplay

## install selenium python driver
$> sudo pip install selenium

## selenium server
$> curl -O http://selenium.googlecode.com/files/selenium-server-standalone-3.13.0.jar

## selenium chrome driver
$> curl -O http://chromedriver.googlecode.com/files/chromedriver_linux32_21.0.1180.4.zip
$> unzip chromedriver_linux32_21.0.1180.4.zip

### or 
$> sudo apt install google-chrome-stable

## install chrome on debia
$> sudo apt-get install chromium-browser chromium-browser-l10n

#RUN

##Star selenium server -> default server run on port 4444
$> java -jar /home/<user_name>/selenium-server-standalone-2.24.1.jar 2>&1 > /dev/null &

## (Option) check selenium server is running:
$> netstat -l | grep 4444 

## Run script for scraping
$> python3 ggplay_scrape.py

