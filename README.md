
![image](https://github.com/nigelthesquirrel/london-bus-display/assets/65233876/f4a0e7e1-e65c-44e3-9c35-0148c4109ceb)


# london-bus-display
Some simple Python code to display a realistic looking bus countdown display on a raspberry pi (will work on any Python supported OS with tkinter)
I have an old PiTop that I am going to run it on
Plan is to install a quick booting OS and run straight into fulls screen mode in the init
Will then shut down the PI after 20 minutes
So in the morning my Son can flick it on, catch his bus and then it will auto-shutdown after he has gone

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
