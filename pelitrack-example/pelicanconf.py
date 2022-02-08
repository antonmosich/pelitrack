AUTHOR = "Flugschwein"
SITENAME = "Pelitrack Sample Project"
SITEURL = ""

PATH = "content"

TIMEZONE = "Europe/Vienna"


DEFAULT_LANG = "de"

THEME = "theme/notmyidea-gps"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Pelican", "https://getpelican.com/"),
    ("Python.org", "https://www.python.org/"),
    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
    ("You can modify those links in your config file", "#"),
)

# Social widget
SOCIAL = (
    ("You can add links in your config file", "#"),
    ("Another social link", "#"),
)

DEFAULT_PAGINATION = False

PELITRACK_GPSBABEL_FILTERS = {
    "simplify": "error=0.01k",
    "nuketypes": "waypoints",
}

PELITRACK_GPX_OPTIONS = """{async: true,
						 marker_options: {
										  startIconUrl:  'theme/images/icons/pin-icon-start.png',
										  endIconUrl: 'theme/images/icons/pin-icon-end.png',
										  shadowUrl: 'theme/images/icons/pin-shadow.png'}}"""
# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
