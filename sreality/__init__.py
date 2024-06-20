from classes import *
import requests
from urllib.parse import quote_plus, urlencode


class Dispositions(DispositionsRoot):
    @classmethod
    def disp_str_to_api(cls, disp_str: str):
        nrooms = int(disp_str[0]) * 2
        match disp_str.lower()[-2:]:
            case "kk":
                return nrooms
            case "+1":
                return nrooms + 1
            case _:
                raise ValueError("incorrect disposition")

    @classmethod
    def api_to_disp_str(cls, api_disp: int):
        disp_rooms = int(api_disp / 2)
        if disp_rooms % 2 == 0:
            return f"{disp_rooms}+kk"
        return f"{disp_rooms}+1"

    @classmethod
    def verify_disp_str(cls, disp_str: str):
        try:
            nrooms, disp_type = disp_str.lower().split("+")
            valid_nrooms = int(nrooms) > 0 and int(nrooms) < 7
            valid_type = disp_type == "kk" or disp_type == "1"
            return valid_nrooms and valid_type
        except:
            return false


def min_max(var=(None, None)):
    res  = str(var[0]) if var[0] else "0"
    res += f"|{var[1]}" if var[1] else ""
    return res


class Listing(ListingRoot):
    def __init__(self, **kwargs):
        self.id = kwargs['hash_id']
        self.disposition = Dispositions.api_to_disp_str(
                kwargs['seo']['category_sub_cb'])
        self.location = kwargs['locality']
        self.area = kwargs['name'].split('(')[0].split()[-2]
        self.price = kwargs['price']
        self.images = [i['href'] for i in kwargs['_links']['images']]
        self.url  = "https://www.sreality.cz/detail/pronajem/byt/"
        self.url += f"{self.disposition}/{kwargs['seo']['locality']}/{self.id}"

    def get_images(self):
        return self.images

    def scrape_images(self):
        # XXX: This doesn't "scrape" the images per se, just replaces their
        # url with a higher resolution watermarked image
        x = '?fl=res,1920,1080,1|wrm,/watermark/sreality.png,10|shr,,20|jpg,90'
        for (idx, img) in enumerate(self.images):
            img  = img.split('?')[0]
            img += x
            self.images[idx] = img
        return self.images


class Scraper(ScraperRoot):
    def __init__(self, regions, dispositions: Dispositions,
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

    @classmethod
    def query_region(cls, query: str) -> str:
        url = "https://www.sreality.cz/api/v1/localities/suggest?limit=1"
        query = quote_plus(query)
        req = requests.get(f"{url}&phrase={query}")

        # TODO: handle request and parse errors
        return req.json()['results'][0]['userData']['district_id']

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

        # TODO: the first estate tends to be some shitter. investigate.
        return [Listing(**i) for i in req.json()['_embedded']['estates']]
