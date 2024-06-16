from classes import *
import requests
from urllib.parse import quote_plus, urlencode

# TODO: 13 pokoj | 47 atypicky
def dispositions(min_disp: int = 1, max_disp: int = 6) -> str:
    dispositions = []
    for disp in range(min_disp, min(max_disp + 1, 6)):
        dispositions.append(disp * 2)
        dispositions.append(disp * 2 + 1)
    return dispositions


def query_region(query: str) -> str:
    url = "https://www.sreality.cz/api/v1/localities/suggest?limit=1"
    query = quote_plus(query)
    req = requests.get(f"{url}&phrase={query}")

    # TODO: handle request and parse errors
    return req.json()['results'][0]['userData']['district_id']


def min_max(var=(None, None)):
    res  = str(var[0]) if var[0] else "0"
    res += f"|{var[1]}" if var[1] else ""
    return res


class Listing(ListingRoot):
    def __init__(self, **kwargs):
        self.ident = kwargs['hash_id']
        self.disposition = "" # TODO
        self.area = kwargs['name'].split()[-2]
        self.price = kwargs['price']
        self.images = None

    # TODO: images


class Scraper(ScraperRoot):
    def __init__(self, regions, dispositions,
                 price=(None, None), area=(None, None)):
        # flats only, no houses. fuck seznam. can't believe i worked there.
        # number of rooms for flats is stored in `category_sub_cb`
        # number of rooms for houses is stored in something else entirely :D
        self.per_page = 999
        self.locality_district_id = '|'.join([str(i) for i in regions])
        self.category_main_cb = 1  # flats
        self.category_sub_cb = '|'.join([str(i) for i in dispositions])
        self.category_type_cb = 2  # rent
        self.czk_price_summary_order2 = min_max(price)
        self.usable_area = min_max(area)


    def scrape(self) -> [Listing]:
        url = "https://www.sreality.cz/api/cs/v2/estates"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
        }

        # TODO: handle request and parse errors
        with requests.Session() as session:
            req = requests.Request('GET', url, headers=headers)
            prepared = req.prepare()
            prepared.url += '?' + urlencode(vars(self), safe='|')
            req = session.send(prepared)

        return [Listing(**i) for i in req.json()['_embedded']['estates']]
