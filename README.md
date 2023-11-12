# gpx2kml
gpx2kml is a library for combining [gpx](https://en.wikipedia.org/wiki/GPS_Exchange_Format) files exported from [Runkeeper](https://runkeeper.com/cms/) to [kml](https://developers.google.com/kml/documentation/kml_tut) files. Below is a screenshot of the generated kml file in Google Earth.
![A demo screenshot from Google Earth](/demo/google%20earth%20demo.png)

## Introduction
Runkeeper is one of many mobile apps that can track exercises. Usually they provide UI for displaying individual activity (like biking, running, etc.) with route map and statistics, and the functionality to bulk export archive files. 

gpx2kml can combine all the gpx files exported from Runkeeper into a single kml file so that it can be displayed in the Google Earth. The motivation is mainly to prepare data for my [bike journey webpage](https://bike-journey.netlify.app/).

## User scenario 
I use Runkeeper to track my biking and walking activities. Tracking is a long term activity, so file generation and archive is an incremental process. 

I export the gpx files once per month, and generate kml files from the gpx files with the format YYYY-MM.kml. After that, all the kml files are combined into a single kml file, usually named after the city or the event related with those activities.

## Installation
```commandline
pip install gpx2kml
```

## How to use it
1. Accumulate a few activities using Runkeeper.
2. [Export the acitives](https://support.runkeeper.com/hc/en-us/articles/201109886-How-to-Export-Your-Runkeeper-Data) from the Runkeeper web UI and download the file. The demo folder provides a sample zip file.
3. Open a terminal, and change the working directory to the one that contains the zip file.
4. Run `gpx-archive` in the terminal. This will create an *archive* folder under the working directory, with all the gpx files inside.
```commandline
gpx-archive
```
5. Run `kml-gen` in the terminal. This will create a *kml* folder under the working directory, with the generated kml files organized by month.
```commandline
kml-gen
```
6. Run `kml-combine XXX` in the terminal. This will create a `XXX.kml`` file that includes all the kml files in the kml folder.
```commandline
kml-combine XXX
```

 Other than running the commands in the terminal, there is a demo.py that demonstrates how to call the methods in a python file. 