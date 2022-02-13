"""Add GPS Tracks to your pelican articles."""
import itertools
import json
import logging
import os
import pathlib
import shutil
import subprocess
import tempfile
from urllib.parse import urljoin

from pelican import Pelican, signals
from pelican.contents import Article
from pelican.generators import ArticlesGenerator
from pelican.settings import DEFAULT_CONFIG

logger = logging.getLogger(__name__)

try:
    import xmlformatter

    xmlformatter_available = True
except ImportError:
    xmlformatter_available = False
    logger.debug("xmlformatter isn't installed.")
processed_tracks = []


def initialized(pelican: Pelican):
    """Initialize the default settings."""
    DEFAULT_CONFIG.setdefault("PELITRACK_GPX_OUTPUT_PATH", "tracks")
    DEFAULT_CONFIG.setdefault("PELITRACK_PROVIDER", ["OpenStreetMap.Mapnik"])
    DEFAULT_CONFIG.setdefault("PELITRACK_HEIGHT", "480px")
    DEFAULT_CONFIG.setdefault("PELITRACK_WIDTH", "100%")
    DEFAULT_CONFIG.setdefault("PELITRACK_GPSBABEL_PATH", shutil.which("gpsbabel"))
    DEFAULT_CONFIG.setdefault(
        "PELITRACK_GPSBABEL_FILTERS", {"simplify": "error=0.001k"}
    )
    DEFAULT_CONFIG.setdefault("PELITRACK_USE_GPSBABEL", True)
    DEFAULT_CONFIG.setdefault("PELITRACK_GPX_OPTIONS", "{async: true}")
    DEFAULT_CONFIG.setdefault(
        "PELITRACK_SCRIPT_LOCATIONS",
        {
            "leaflet.js": "theme",
            "leaflet.css": "theme",
            "gpx.min.js": "theme",
            "leaflet-providers.js": "theme",
        },
    )
    DEFAULT_CONFIG.setdefault("PELITRACK_GPX_ICON_DIR", "./leaflet-gpx")
    DEFAULT_CONFIG.setdefault(
        "PELITRACK_GPX_ICON_FILENAMES",
        [
            "pin-icon-start.png",
            "pin-icon-end.png",
            "pin-icon-wpt.png",
            "pin-shadow.png",
        ],
    )
    DEFAULT_CONFIG.setdefault("PELITRACK_MINIFY_GPX", False)
    DEFAULT_CONFIG.setdefault("PELITRACK_GPX_MINIFIER", "minify")
    DEFAULT_CONFIG.setdefault("PELITRACK_MINIFY_PATH", shutil.which("minify"))

    if pelican:
        pelican.settings.setdefault("PELITRACK_GPX_OUTPUT_PATH", "tracks")
        pelican.settings.setdefault("PELITRACK_PROVIDER", ["OpenStreetMap.Mapnik"])
        pelican.settings.setdefault("PELITRACK_HEIGHT", "480px")
        pelican.settings.setdefault("PELITRACK_WIDTH", "100%")
        pelican.settings.setdefault("PELITRACK_GPSBABEL_PATH", shutil.which("gpsbabel"))
        pelican.settings.setdefault(
            "PELITRACK_GPSBABEL_FILTERS", {"simplify": "error=0.001k"}
        )
        pelican.settings.setdefault("PELITRACK_USE_GPSBABEL", True)
        pelican.settings.setdefault("PELITRACK_GPX_OPTIONS", "{async: true}")
        pelican.settings.setdefault(
            "PELITRACK_SCRIPT_LOCATIONS",
            {
                "leaflet.js": "theme",
                "leaflet.css": "theme",
                "gpx.min.js": "theme",
                "leaflet-providers.js": "theme",
            },
        ),
        pelican.settings.setdefault("PELITRACK_GPX_ICON_DIR", "./leaflet-gpx")
        pelican.settings.setdefault(
            "PELITRACK_GPX_ICON_FILENAMES",
            [
                "pin-icon-start.png",
                "pin-icon-end.png",
                "pin-icon-wpt.png",
                "pin-shadow.png",
            ],
        )
        pelican.settings.setdefault("PELITRACK_MINIFY_GPX", False)
        pelican.settings.setdefault("PELITRACK_GPX_MINIFIER", "minify")
        pelican.settings.setdefault("PELITRACK_MINIFY_PATH", shutil.which("minify"))
    global pelican_settings
    pelican_settings = pelican.settings
    global pelican_output_path
    pelican_output_path = pelican.output_path

    replace_online_scripts()
    if isinstance(pelican_settings["PELITRACK_PROVIDER"], str):
        pelican_settings["PELITRACK_PROVIDER"] = [
            pelican_settings["PELITRACK_PROVIDER"]
        ]


def copy_pin_icons(article_generator, writer):
    """Copy icon files needed for leaflet-gpx to root of the website."""
    for filename in pelican_settings["PELITRACK_GPX_ICON_FILENAMES"]:
        file = pathlib.Path(pelican_settings["PELITRACK_GPX_ICON_DIR"], filename)
        shutil.copyfile(file, pathlib.Path(pelican_output_path, filename))


def replace_online_scripts():
    """
    Replace "online" in the script locations config with the corresponding URLs.

    Returns
    -------
    None.

    """
    online_script_locations = {
        "leaflet.js": "https://unpkg.com/leaflet@1.7.1/dist/leaflet.js",
        "leaflet.css": "https://unpkg.com/leaflet@1.7.1/dist/leaflet.css",
        "gpx.min.js": "https://cdnjs.cloudflare.com/ajax/"
        "libs/leaflet-gpx/1.7.0/gpx.min.js",
        "leaflet-providers.js": "http://leaflet-extras.github.io/"
        "leaflet-providers/leaflet-providers.js",
    }

    theme_script_locations = {
        "leaflet.js": "js/leaflet.js",
        "leaflet.css": "css/leaflet.css",
        "gpx.min.js": "js/gpx.min.js",
        "leaflet-providers.js": "js/leaflet-providers.js",
    }

    pelican_settings["PELITRACK_SCRIPT_LOCATIONS"] = (
        DEFAULT_CONFIG["PELITRACK_SCRIPT_LOCATIONS"]
        | pelican_settings["PELITRACK_SCRIPT_LOCATIONS"]
    )

    for key, value in pelican_settings["PELITRACK_SCRIPT_LOCATIONS"].items():
        if value == "online":
            if key == "leaflet-providers.js":
                logging.warning(
                    "Please host leaflet-providers.js yourself."
                    " That isn't the intended way to use it"
                )
            pelican_settings["PELITRACK_SCRIPT_LOCATIONS"][
                key
            ] = online_script_locations[key]
        elif value == "theme":
            pelican_settings["PELITRACK_SCRIPT_LOCATIONS"][key] = pathlib.Path(
                pelican_settings["THEME_STATIC_DIR"], theme_script_locations[key]
            )

        path = pelican_settings["PELITRACK_SCRIPT_LOCATIONS"][key]
        if not isinstance(path, pathlib.Path):
            path = pathlib.Path(path)
        if not pelican_settings["RELATIVE_URLS"]:
            if not path.is_absolute():
                pelican_settings["PELITRACK_SCRIPT_LOCATIONS"][key] = urljoin(
                    pelican_settings["SITEURL"], path.as_posix()
                )
        else:
            pelican_settings["PELITRACK_SCRIPT_LOCATIONS"][key] = path.as_posix()
    logger.debug("Script locations: %s", pelican_settings["PELITRACK_SCRIPT_LOCATIONS"])


def parse_individual_settings(track):
    """Parse additional settings for a given track.

    Parameters
    ----------
    track : list
        The list of arguments given for the track metadata tag.

    Returns
    -------
    settings : dict
        Settings considering the specified settings but falling back on the defaults.

    """
    default_settings = {
        "gpx_output_path": pelican_settings["PELITRACK_GPX_OUTPUT_PATH"],
        "height": pelican_settings["PELITRACK_HEIGHT"],
        "width": pelican_settings["PELITRACK_WIDTH"],
        "provider": pelican_settings["PELITRACK_PROVIDER"],
        "use_gpsbabel": pelican_settings["PELITRACK_USE_GPSBABEL"],
        "gpsbabel_filters": pelican_settings["PELITRACK_GPSBABEL_FILTERS"],
        "gpx_options": pelican_settings["PELITRACK_GPX_OPTIONS"],
    }

    if len(track) > 2:
        logger.debug("Found additional arguments for gps track.")
        updates = []
        for arg in track[2:]:
            arg, val = arg.split("=>")
            if arg == "provider":
                if val.startswith("+"):
                    val = [*pelican_settings["PELITRACK_PROVIDER"], *val.split("+")[1:]]
                else:
                    val = val.split("+")
            updates.append((arg, val))
        settings = default_settings | dict(updates)
        if isinstance(settings["gpsbabel_filters"], str):
            settings["gpsbabel_filters"] = json.loads(settings["gpsbabel_filters"])
        logger.debug("Modified pelitrack settings: %s", settings)
    else:
        settings = default_settings
    return settings


def process_track(article: Article):
    """
    Process track if present in an article.

    This function will process the track metadata tag and set a few variables,
    which can then be used by jinja2 for creating the leaflet. It will also
    convert, modify and copy the GPS tracks specified in the tag.

    Parameters
    ----------
    article : Article
        The article object to process.

    Returns
    -------
    None.

    """
    if "track" not in article.metadata:
        return
    track = article.metadata.get("track").split(";")
    os.makedirs(
        pathlib.Path(
            pelican_output_path, pelican_settings["PELITRACK_GPX_OUTPUT_PATH"]
        ),
        exist_ok=True,
    )

    settings = parse_individual_settings(track)

    location = pathlib.Path(settings["gpx_output_path"], f"{article.slug}.gpx")

    if not settings["use_gpsbabel"]:
        shutil.copyfile(
            track[0],
            pathlib.Path(pelican_output_path, location),
        )
    else:
        if len(track) <= 1:
            logger.warning("No filetype found for %s in %s", track[0], article.slug)
            article.track = None
            return
        command = [
            pelican_settings["PELITRACK_GPSBABEL_PATH"],
            "-i",
            track[1],
            "-f",
            track[0],
        ]
        for gps_filter, options in settings["gpsbabel_filters"].items():
            command.append("-x")
            fil = ",".join([gps_filter] + [options])
            command.append(fil)
        command += ["-o", "gpx", "-F", pathlib.Path(pelican_output_path, location)]

        logger.debug("Running GPSBabel with command: %s", command)
        comm_exit = subprocess.run(command)

        if comm_exit.returncode != 0:
            logger.warning("GPSBabel execution did not succeed.")
            logger.debug("GPSBabel error code: %s", comm_exit)
    processed_tracks.append(location)

    if not pelican_settings["RELATIVE_URLS"]:
        location = urljoin(pelican_settings["SITEURL"], location.as_posix())
    else:
        location = location.as_posix()
    article.track_location = location
    article.track_settings = settings


def handle_articles_generator(gen: ArticlesGenerator):
    """Handle the ArticlesGenerator from the signal to process the articles."""
    for article in itertools.chain(gen.articles, gen.drafts, gen.translations):
        process_track(article)


def minify_gpx(pelican: Pelican):
    """Minify all generated gpx files.

    Parameters
    ----------
    pelican : Pelican
        Pelican instance given by the signal.

    Returns
    -------
    None.

    """
    if not pelican_settings["PELITRACK_MINIFY_GPX"]:
        return
    minify_functions = {
        "xmlformatter": minify_with_xmlformatter,
        "minify": minify_with_minify,
    }

    if (
        pelican_settings["PELITRACK_GPX_MINIFIER"] == "xmlformatter"
        and not xmlformatter_available
    ):
        logging.warning(
            "Can not use xmlformatter for minifying gpx files."
            " Please check your installation and configuration."
        )
    elif pelican_settings["PELITRACK_GPX_MINIFIER"] not in minify_functions:
        logging.warning(
            "GPX minifier %s is not known. Make sure to check your spelling.",
            pelican_settings["PELITRACK_GPX_MINIFIER"],
        )
    else:
        for location in processed_tracks:
            location = pathlib.Path(pelican_output_path, location)
            minify_functions[pelican_settings["PELITRACK_GPX_MINIFIER"]](location)


def minify_with_xmlformatter(filepath: str):
    """Minify gpx file with xmlformatter.

    Replaces the provided gpx file with a minified version of itself.
    The module used for minifying in this function is very slow.


    Parameters
    ----------
    filepath : str
        Path to the gpx file that should be minified.

    Returns
    -------
    None.

    """
    formatter = xmlformatter.Formatter(compress=True)
    formatted_bytes = formatter.format_file(filepath)
    with open(filepath, "wb") as file:
        file.write(formatted_bytes)


def minify_with_minify(filepath: str):
    """Minify gpx file with minify.

    Replaces the provided gpx file with a minified version of itself.
    This function uses "minify" for minifying. Much faster than xmlformatter.


    Parameters
    ----------
    filepath : str
        Path to the gpx file that should be minified.

    Returns
    -------
    None.

    """
    minify = pelican_settings["PELITRACK_MINIFY_PATH"]
    tmp_file = pathlib.Path(tempfile.gettempdir(), "tmp.gpx")
    command = [minify, filepath, "--type", "xml", "-o", tmp_file]
    logging.debug("Executing minify with args %s.", command)
    process = subprocess.run(command)
    if process.returncode != 0:
        logging.error("minify execution failed. %s was left untouched.", filepath)
        return
    shutil.move(tmp_file, filepath)


def register():
    """Connect the relevant functions to the respective functions."""
    signals.initialized.connect(initialized)
    signals.article_writer_finalized.connect(copy_pin_icons)
    signals.article_generator_finalized.connect(handle_articles_generator)
    signals.finalized.connect(minify_gpx)
