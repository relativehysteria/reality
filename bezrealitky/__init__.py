from . import queries
from classes import *
import requests
from urllib.parse import quote_plus

GRAPH_URL = "https://api.bezrealitky.cz/graphql/"


def dispositions(min_disp: int = 1, max_disp: int = 7) -> [str]:
    dispositions = []
    for disp in range(min_disp, min(max_disp + 1, 8)):
        dispositions.append(f"DISP_{disp}_1")
        dispositions.append(f"DISP_{disp}_KK")
    return dispositions


def query_region(query: str) -> str:
    url = "https://autocomplete.bezrealitky.cz/autocomplete?size=1"
    query = quote_plus(query)
    req = requests.get(f"{url}&q={query}")

    # TODO: handle request and parse errors
    data = req.json()
    props = data['features'][0]['properties']
    osm_type = props['osm_type']
    osm_id   = props['osm_id']
    return f"{osm_type}{osm_id}"


class Listing(ListingRoot):
    def __init__(self, **kwargs):
        self.ident = kwargs['id']
        self.disposition = kwargs['disposition'][5:].replace('_', '+')
        self.area = kwargs['surface']
        self.price = kwargs['price'] + kwargs['charges']
        self.images = None
        if self.mainImageUrl:
            self.mainImageUrl = self.mainImageUrl['url']

    def get_images(self):
        if self.images is not None:
            return self.images
        return self.scrape_images()

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


class Scraper(ScraperRoot):
    def __init__(self, regions, dispositions,
                 price=(None, None), area=(None, None), petFriendly=False):
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
        self.priceFrom = price[0]
        self.priceTo = price[1]
        self.surfaceFrom = area[0]
        self.surfaceTo = area[1]

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
