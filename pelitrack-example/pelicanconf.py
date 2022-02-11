AUTHOR = 'Flugschwein'
SITENAME = 'Pelitrack Sample Project'
SITEURL = ""

PATH = 'content'

TIMEZONE = 'Europe/Vienna'


DEFAULT_LANG = 'de'

THEME = 'theme/notmyidea-gps'

STATIC_PATHS = []

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'https://getpelican.com/'),
         ('Python.org', 'https://www.python.org/'),
         ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
         ('Check out Pelitrack', 'https://github.com/pelican-plugins/pelitrack'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

PELITRACK_MINIFY_GPX = True
