pelitrack: A Plugin for Pelican
====================================================

[![Build Status](https://img.shields.io/github/workflow/status/pelican-plugins/pelitrack/build)](https://github.com/pelican-plugins/pelitrack/actions)
[![PyPI Version](https://img.shields.io/pypi/v/pelican-pelitrack)](https://pypi.org/project/pelican-pelitrack/)
![License](https://img.shields.io/pypi/l/pelican-pelitrack?color=blue)

Include GPS Tracks in your blog posts with this plugin

Installation
------------

This plugin can be installed via:

    python -m pip install pelican-pelitrack

Usage
-----

This pelican plugin is used for adding GPS Tracks to you articles. For displaying the map with the GPS Track,
it uses the popular [leaflet][] library as well as the [leaflet-gpx][] plugin and the [leaflet-providers][] project. For converting other GPS formats to the `gpx` standard, [GPSBabel][]
is used. The usage of GPSBabel is optional, if you only want to use `gpx` files. If you intend to use GPSBabel, make sure that it's either in your PATH, or specify its location in your config file, by
setting `PELITRACK_GPSBABEL_PATH`.

[leaflet-gpx]: https://github.com/mpetazzoni/leaflet-gpx
[leaflet]: https://leafletjs.com/
[leaflet-providers]: https://github.com/leaflet-extras/leaflet-providers
[GPSBabel]: https://www.gpsbabel.org/index.html

### Setup
You'll need to setup several things, in order to be able to use pelitrack. First, you will need to setup the javascript libraries. The prefered way of doing so is by moving the relevant `.js` and `.css`
files into you theme folder. You will need to download leaflet, leaflet-gpx and leaflet-providers and set them up in your theme such that the structure then looks like the following:
```theme/
├─ static/
│  ├─ js/
│  │  ├─ gpx.min.js
│  │  ├─ leaflet.js
│  │  ├─ leaflet-providers.js
│  ├─ css/
│  │  ├─ leaflet.css
│  │  ├─ images/
│  │  │  ├─ layers.png
│  │  │  ├─ layers-2x.png
│  │  │  ├─ marker-icon.png
│  │  │  ├─ marker-shadow.png
│  │  │  ├─ marker-icon-2x.png
│  ├─ images/
│  │  ├─ icons/
│  │  │  ├─ pin-icon-end.png
│  │  │  ├─ pin-icon-start.png
│  │  │  ├─ pin-icon-wpt.png
│  │  │  ├─ pin-shadow.png```
You will probably want to move the `track.html` from `pelitrack-example/theme/templates/track.html` to your own theme. Then you can modify your theme with an `{% include track.html %}` wherever
you want to include the associated track. In those pages, you need to include the `leaflet.css` in the head as well.

It also is possible to source the needed files from the web without hosting them yourself. Then you'll need to make modifications to the `track.html` in order to link to the correct sources.

Then you will need to set up GPSBabel. Just download it from the website, and install it. If it is not on your PATH, you will need to set `PELITRACK_GPSBABEL_PATH` in your config file to the corresponding
location. Otherwise pelitrack will find GPSBabel itself.

### Usage
To use pelitrack after it's been setup, just include the track tag in your posts metadata. It should look like the following:
```:track: path/to/your/trackfile.gpx,fileformat```
The path to the trackfile should be either absolute, or relative to the folder you execute pelican in. The fileformat needs to be one of the formats [GPSBabel supports][] with the corresponding code.
(e.g. `gpx` for .gpx files `kml` for .kml files, `garmin_fit` for .fit files)
Pelitrack will then convert the file to gpx and apply the configured filters (by default it will simplify your track while keeping the error from the simplification <10m).

[GPSBabel supports]: https://www.gpsbabel.org/htmldoc-1.8.0/The_Formats.html

#### Without GPSBabel
If you don't want to use GPSBabel just set `PELITRACK_USE_GPSBABEL` to `False` in your config. Pelitrack only supports `gpx` files that way, and isn't able to modify or simplify them.
Usage remains the same, but you don't have to set the fileformat in order to use it.


Contributing
------------

Contributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].

To start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.

[existing issues]: https://github.com/pelican-plugins/pelitrack/issues
[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html

License
-------

This project is licensed under the AGPL-3.0 license.
