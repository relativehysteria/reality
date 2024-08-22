from . import queries
from classes import *
import requests
from urllib.parse import quote_plus

GRAPH_URL = "https://api.bezrealitky.cz/graphql/"

class Dispositions(DispositionsRoot):
    @classmethod
    def disp_str_to_api(cls, disp_str: str):
        disp_str = disp_str.replace('+', '_').upper()
        return f"DISP_{disp_str}"

    @classmethod
    def api_to_disp_str(cls, api_disp: str):
        return api_disp.replace("DISP_", "").replace("_", '+').lower()

    @classmethod
    def verify_disp_str(cls, disp_str: str):
        try:
            nrooms, disp_type = disp_str.lower().split("+")
            valid_nrooms = int(nrooms) > 0 and int(nrooms) < 8
            valid_type = disp_type == "kk" or disp_type == "1"
            return valid_nrooms and valid_type
        except:
            return False


class Listing(ListingRoot):
    def __init__(self, **kwargs):
        self.id = int(kwargs['id'])
        self.disposition = Dispositions.api_to_disp_str(kwargs['disposition'])
        self.location = kwargs['address']
        self.area = int(kwargs['surface'])
        self.price = int(kwargs['price'])
        self.charges = kwargs['charges']
        self.url  = "https://www.bezrealitky.cz/nemovitosti-byty-domy/"
        self.url += kwargs['uri']
        self.images = None
        self.mainImageUrl = None
        if kwargs['mainImageUrl']:
            self.mainImageUrl = kwargs['mainImageUrl']['url']

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
    def __init__(self, regions, dispositions: Dispositions,
                 price=(None, None), area=(None, None), petFriendly=False):
        self.limit = 0
        self.locale = "CS"
        self.offerType = ["PRONAJEM"]
        self.estateType = ["BYT", "DUM"]
        self.disposition = list(dispositions.inner)
        self.regionOsmIds = regions
        self.roommate = False
        self.location = "exact"
        self.petFriendly = petFriendly
        self.currency = "CZK"
        self.priceFrom = price[0]
        self.priceTo = price[1]
        self.surfaceFrom = area[0]
        self.surfaceTo = area[1]

    @classmethod
    def query_region(cls, query: str) -> str:
        url = "https://autocomplete.bezrealitky.cz/autocomplete?size=1"
        query = quote_plus(query)
        req = requests.get(f"{url}&q={query}")

        # TODO: handle request and parse errors
        data = req.json()
        props = data['features'][0]['properties']
        osm_type = props['osm_type']
        osm_id   = props['osm_id']
        return f"{osm_type}{osm_id}"

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
