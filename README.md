# gpx2kml
gpx2kml is a library for combining [gpx](https://en.wikipedia.org/wiki/GPS_Exchange_Format) files exported from [Runkeeper](https://runkeeper.com/cms/) to [kml](https://developers.google.com/kml/documentation/kml_tut) files. Below is a screenshot of the generated kml file in Google Earth.
![A demo screenshot from Google Earth](/demo/google%20earth%20demo.png)

## Introduction
Runkeeper is one of many mobile apps that can track exercises. Usually they provide UI for displaying individual activity (like biking, running, etc.) with route map and statistics, and the functionality to bulk export archive files. 

gpx2kml can combine all the gpx files exported from Runkeeper into a single kml file so that it can be displayed in the Google Earth. The motivation is mainly to prepare data for my [bike journey webpage](https://bike-journey.netlify.app/).

## User scenario 
I use Runkeeper to track my biking and walking activities. Tracking is a long term activity, so file generation and archive is an incremental process. 

I export the gpx files once per month, and generate kml files from the gpx files with the format YYYY-MM.kml. After that, all the kml files are combined into a single kml file, usually named after the city or the event related with those activities.

## Install and use
Run the interactive command and choose tasks from a terminal menu.

Without uv:
```commandline
pip install gpx2kml
gpx2kml
```

With uv (no global installation required):
```commandline
uvx gpx2kml
```

1. Accumulate a few activities using Runkeeper.
2. [Export the acitives](https://support.runkeeper.com/hc/en-us/articles/201109886-How-to-Export-Your-Runkeeper-Data) from the Runkeeper web UI and download the file. The demo folder provides a sample zip file.
3. Open a terminal, and change the working directory to the one that contains the zip file.
4. Select menu option 1 to archive GPX files from a Runkeeper export zip. This creates an *archive* folder.
5. Select menu option 2 to generate monthly KML files. This creates a *kml* folder with YYYY-MM.kml files.
6. Move the kml files into kml/XXX, then select menu option 3 and input XXX to combine them into XXX.kml.

 Other than running the commands in the terminal, there is a demo.py that demonstrates how to call the methods in a python file. 