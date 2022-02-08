import itertools
import logging
import os
import shutil

from pelican import Pelican, signals
from pelican.contents import Article
from pelican.generators import ArticlesGenerator
from pelican.settings import DEFAULT_CONFIG

logger = logging.getLogger(__name__)


def initialized(pelican: Pelican):
    """Initialize the default settings"""
    DEFAULT_CONFIG.setdefault("PELITRACK_GPX_OUTPUT_PATH", "tracks")
    DEFAULT_CONFIG.setdefault("PELITRACK_PROVIDER", "OpenStreetMap.Mapnik")
    DEFAULT_CONFIG.setdefault("PELITRACK_HEIGHT", "480px")
    DEFAULT_CONFIG.setdefault("PELITRACK_WIDTH", "100%")
    DEFAULT_CONFIG.setdefault("PELITRACK_GPSBABEL_PATH", shutil.which("gpsbabel"))
    DEFAULT_CONFIG.setdefault(
        "PELITRACK_GPSBABEL_FILTERS", {"simplify": "error=0.001k"}
    )
    DEFAULT_CONFIG.setdefault("PELITRACK_USE_GPSBABEL", True)
    DEFAULT_CONFIG.setdefault("PELITRACK_GPX_OPTIONS", "{async: true}")

    if pelican:
        pelican.settings.setdefault("PELITRACK_GPX_OUTPUT_PATH", "tracks")
        pelican.settings.setdefault("PELITRACK_PROVIDER", "OpenStreetMap.Mapnik")
        pelican.settings.setdefault("PELITRACK_HEIGHT", "480px")
        pelican.settings.setdefault("PELITRACK_WIDTH", "100%")
        pelican.settings.setdefault("PELITRACK_GPSBABEL_PATH", shutil.which("gpsbabel"))
        pelican.settings.setdefault(
            "PELITRACK_GPSBABEL_FILTERS", {"simplify": "error=0.001k"}
        )
        pelican.settings.setdefault("PELITRACK_USE_GPSBABEL", True)
        pelican.settings.setdefault("PELITRACK_GPX_OPTIONS", "{async: true}")

    global pelican_settings
    pelican_settings = pelican.settings
    global pelican_output_path
    pelican_output_path = pelican.output_path


def process_track(article: Article):
    if "track" not in article.metadata:
        return
    track = article.metadata.get("track").split(",")

    os.makedirs(
        os.path.join(
            pelican_output_path, pelican_settings["PELITRACK_GPX_OUTPUT_PATH"]
        ),
        exist_ok=True,
    )

    location = os.path.join(
        pelican_settings["PELITRACK_GPX_OUTPUT_PATH"], f"{article.slug}.gpx"
    )

    if not pelican_settings["PELITRACK_USE_GPSBABEL"]:
        shutil.copyfile(
            track[0],
            os.path.join(pelican_output_path, location),
        )
    else:
        assert len(track) > 1, f"No filetype found for {track[0]} in {article.slug}"
        command = [
            pelican_settings["PELITRACK_GPSBABEL_PATH"],
            "-i",
            track[1],
            "-f",
            track[0],
        ]
        for gps_filter, options in pelican_settings[
            "PELITRACK_GPSBABEL_FILTERS"
        ].items():
            command.append("-x")
            fil = ",".join([gps_filter] + [options])
            command.append(fil)

        command += ["-o gpx", "-F", os.path.join(pelican_output_path, location)]
        command = " ".join(command)

        logger.debug(f"Running GPSBabel with command: {command}")

        comm_exit = os.system(command)
        if comm_exit != 0:
            logger.warning("GPSBabel execution did not succeed")

    if not pelican_settings["RELATIVE_URLS"]:
        location = pelican_settings["SITEURL"] + location

    article.track_location = location


def handle_articles_generator(gen: ArticlesGenerator):
    for article in itertools.chain(gen.articles, gen.drafts, gen.translations):
        process_track(article)


def register():
    signals.initialized.connect(initialized)
    signals.article_generator_finalized.connect(handle_articles_generator)
