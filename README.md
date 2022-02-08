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

Contributing
------------

Contributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].

To start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.

[existing issues]: https://github.com/pelican-plugins/pelitrack/issues
[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html

License
-------

This project is licensed under the AGPL-3.0 license.
