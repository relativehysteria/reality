from typing import Optional, List, Tuple
from sys import stderr

# Dispositions are in the form of 1+kk, 1+1, 2+kk, 2+2 etc.
class DispositionsRoot:
    def __init__(self, disp_list=[]):
        self.inner = set()

        for disp in disp_list:
            self.add(disp)

    def __iter__(self):
        return iter(self.inner)

    def disp_is_valid(self, disp: str) -> bool:
        if self.verify_disp_str(disp):
            return True

        module = f"{self.__module__}".replace("scrapers.", "")
        print(f'{module}: Disposition "{disp}" is invalid. Ignoring it!',
              file=stderr)
        return False


    def add(self, disp: str):
        if self.disp_is_valid(disp):
            self.inner.add(self.disp_str_to_api(disp))

    # Verify that the disposition string provided in `config.py` is valid for
    # this real estate. For example, bezrealitky has dispositions up to 7+1
    # whereas sreality has only up to 6+1.
    @classmethod
    def verify_disp_str(cls, disp_str: str):
        raise NotImplementedError

    # Convert the value the API uses to the string we use.
    @classmethod
    def api_to_disp_str(cls, api_disp):
        raise NotImplementedError

    # Convert the disposition string we use to the value the API uses.
    @classmethod
    def disp_str_to_api(cls, disp_str: str):
        raise NotImplementedError


# A site-specific listing.
#
# This is the root class that has to be implemented by all scrapers. As such,
# the class variables here can be matched against in `config.filters` as they
# are guaranteed to be present.
class ListingRoot:
    def __init__(self, **kwargs):
        # Site specific identifier for the estate.
        self.id: int = None

        # Site specific geographical location of the estate.
        self.location: str = None

        # Disposition of the estate in the form our script uses.
        self.disposition: str = None

        # Area of the estate in square meters.
        self.area: int = None

        # Site specific price of the estate, usually in czk.
        self.price: int = None

        # Site specific URL of the state.
        self.url: str = None

    def __str__(self):
        return f"{self.disposition:>4}" +\
               f" | {self.area:>3}m²" +\
               f" | {self.price:>5},-" +\
               f" | {self.location}"


# The site-specific scraper.
#
# This is the root class that has to be implemented by all scrapers. As such,
# these functions are guaranteed to be present and can be called anywhere within
# the script.
class ScraperRoot:
    # `regions`      = list of site/api-specific regions
    # `dispositions` = list of dispositions
    # `price`        = minimum and maximum prices to retain
    # `area`         = minimum and maximum area in square meters to retain
    def __init__(self, regions: List[str], dispositions: [DispositionsRoot],
                 price=(None, None), area=(None, None)):
        raise NotImplementedError

    # Invoke the scraper and get listings.
    def scrape(self) -> List[ListingRoot]:
        raise NotImplementedError

    # Query the site's geolocator to convert our `config.region` strings into
    # a representation the site will understand.
    # The return value is `(original_query, result)`
    @classmethod
    def query_region(cls, original_query: str) -> Tuple[str, Optional[str]]:
        raise NotImplementedError
