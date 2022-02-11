Title: Samplepost with KML track
Date: 2022-02-09 20:00
Track: content/tracks/sample_kml.kml;kml;gpsbabel_filters=>{"simplify": "error=0.01k", "nuketypes": "waypoints"};provider=>OpenTopoMap

This post contains a KML file, which was converted by GPSBabel in order to be displayed by leaflet-gpx successfully.
You can modify how GPSBabel converts and modifies you files by setting the `PELITRACK_GPSBABEL_FILTERS` in you `pelicanconf.py`.
When GPSBabel converts a KML file (at least one downloaded from Garmin Connect), it interprets each single point in the track as a waypoint. To circumvent the 
track vanishing behind waypoint icons, just add `"nuketypes": "waypoints"` to your GPSBabel filter configuration.
