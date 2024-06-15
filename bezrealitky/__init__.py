import requests
from . import queries
from urllib.parse import quote_plus

GRAPH_URL = "https://api.bezrealitky.cz/graphql/"


def dispositions(min_disp: int = 1, max_disp: int = 7) -> [str]:
    dispositions = []
    for disp in range(min_disp, min(max_disp, 7)):
        dispositions.append(f"DISP_{disp}_1")
        dispositions.append(f"DISP_{disp}_KK")
    return dispositions


def query_osm(query: str) -> str:
    url = "https://autocomplete.bezrealitky.cz/autocomplete?size=1"
    query = quote_plus(query)
    req = requests.get(f"{url}&q={query}")

    # TODO: handle request and parse errors
    data = req.json()
    props = data['features'][0]['properties']
    osm_type = props['osm_type']
    osm_id   = props['osm_id']
    return f"{osm_type}{osm_id}"


class Listing:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.images = None
        if self.mainImageUrl:
            self.mainImageUrl = self.mainImageUrl['url']

    def __str__(self):
        return str(vars(self))

    def scrape_images(self):
        headers = { "content-type": "application/json", }
        payload = {
            "operationName": "AdvertDetail",
            "variables": vars(self),
            "query": queries.IMAGES,
        }
        # TODO: handle request and parse errors
        req = requests.post(GRAPH_URL, headers=headers, json=payload)

        images = req.json()['data']['advert']['publicImages']
        self.images = [image['url'] for image in images]
        return self.images


class Scraper:
    def __init__(self, regions, dispositions=dispositions(), petFriendly=None,
                 priceFrom=None, priceTo=None,
                 surfaceFrom=None, surfaceTo=None):
        self.limit = 0
        self.locale = "CS"
        self.offerType = ["PRONAJEM"]
        self.estateType = ["BYT", "DUM"]
        self.disposition = dispositions
        self.regionOsmIds = regions
        self.roommate = False
        self.location = "exact"
        self.petFriendly = petFriendly
        self.currency = "CZK"
        self.priceFrom = priceFrom
        self.priceTo = priceTo
        self.surfaceFrom = surfaceFrom
        self.surfaceTo = surfaceTo

    def scrape(self) -> [Listing]:
        headers = { "content-type": "application/json", }
        payload = {
            "operationName": "AdvertList",
            "variables": vars(self),
            "query": queries.INITIAL,
        }
        # TODO: handle request and parse errors
        req = requests.post(GRAPH_URL, headers=headers, json=payload)
        return [Listing(**i) for i in req.json()['data']['listAdverts']['list']]
