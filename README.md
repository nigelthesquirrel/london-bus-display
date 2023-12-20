
![image](https://github.com/nigelthesquirrel/london-bus-display/assets/65233876/f4a0e7e1-e65c-44e3-9c35-0148c4109ceb)
![image](https://github.com/nigelthesquirrel/london-bus-display/assets/65233876/87c92b91-0f73-47ab-bff4-cc1c69a4b218)


# london-bus-display
Some simple Python code to display a realistic looking bus countdown display sourcing real data from TFL(Transport for London) on a raspberry pi (will work on any Python supported OS with tkinter)
I have an old PiTop CEED that I am going to run it on

So in the morning my Son can flick it on, catch his bus 
Was planning to autoshut down after say 20 minutes but doing a linux shutdown command does not kill the PiTop ceed monitor
He may just need to switch it off on his way out!

You can specify the stop, font family and size in the config file
I used the font LED Counter 8 Font File from here https://www.1001fonts.com/led-counter-7-font.html
You will need to download and install the font on your Operating System (This is very easy in Windows)

For details of the api I use for this see: https://content.tfl.gov.uk/tfl-live-bus-river-bus-arrivals-api-documentation.pdf

To workout your stopId you can use this call:
https://countdown.api.tfl.gov.uk/interfaces/ura/instant_V1?ReturnList=LineName,DestinationName,EstimatedTime,StopPointName,StopId,Towards&StopId=BP2236

Then remove the last parameter i.e.
https://countdown.api.tfl.gov.uk/interfaces/ura/instant_V1?ReturnList=LineName,DestinationName,EstimatedTime,StopPointName,StopId,Towards

You can then search in your browser using ctrl+f
One of my local stops in "Church Road" obviously there are lots of those across London
Also you need the stop that is going the right direction as often they have the same name!
Knowing the buses and where they are going in the above call helps with that!

I'd also recommend cross-referencing the times displayed with the (free) official TFL app (or other similar apps)  as a check!

Note that there are other APIs available to help you figure out your local bus stop in a more elegant way!

Couple of other niceities - 
* If you can't work out how to shut the full screen Window try alt+f4 - seems to work on PiTop OS and Windows
* To get thtis to autostart on the PI had to create a dir ~/.config/autostart then add a file BusTimes.desktop
  [Desktop Entry]
  Name=But Times
  Type=Application
  Comment=Countdown Bus Times
  Exec=/home/pi/london-bus-display/run.sh
* In the run.sh I am using unclutter to hide the mouse pointer - I'll let you google how to install it for the pi

When/If I get a chance I may rewrite this so the display can just be a web-page so you could full-screen a browser anywhere to use
Maybe able to do this in just a single html/javascript file (which could either be hosted or opened locally)
