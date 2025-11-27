# Scrapers from the `scrapers` directory that will be run.
#
# For example the idnes scraper will cause a lot of duplicated real estates to
# show up because many of them are listed on sreality as well; that's why it's
# not included here.
enabled_scrapers = ["bezrealitky", "idnes", "sreality"]

# Geographical regions where we're looking for real estates.
#
# This will use the first result returned by the site-specific API. For example,
# if one of these regions is nonsensical (say, "aosidghaohgfda"), it will use
# the first result returned by the API, if any is returned at all.
regions = ["okres Brno-město", "okres Brno-venkov", "dsafojojo"]

# Dispositions of the estates we want to scrape, in the format "N+1" and "N+kk"
dispositions = ["1+1", "2+kk", "2+1", "3+kk"]

# Only real estates matching the following filters will be scraped and retained.
# The "listing" here is the `ListingRoot` class in `classes.py`.
# The variables are described there as well; read the file for more info.
filters = [
    lambda listing: listing.area > 70,
    lambda listing: listing.price < 18000,
]

# The browser in which.
browser = "firefox"
