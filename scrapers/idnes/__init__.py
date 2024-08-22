from classes import *
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urlencode
from dataclasses import dataclass


class Dispositions(DispositionsRoot):
    @classmethod
    def disp_str_to_api(cls, disp_str: str):
        return disp_str.lower().replace("kk", "k").replace("+", "")

    @classmethod
    def api_to_disp_str(cls, api_disp: str):
        api_disp = api_disp.replace("kk", "k").replace("+", "")
        disp_str = api_disp[0] + '+' + api_disp[1]
        return disp_str.lower().replace("k", "kk").uppwer()

    @classmethod
    def verify_disp_str(cls, disp_str: str):
        try:
            nrooms, disp_type = disp_str.lower().split("+")
            valid_nrooms = int(nrooms) > 0 and int(nrooms) < 7
            valid_type = disp_type == "kk" or disp_type == "1"
            return valid_nrooms and valid_type
        except:
            return false

    def get_formatted(self) -> [str]:
        formatted = []
        for (idx, disp) in enumerate(self.inner):
            formatted.append(f"s-qc[subtypeFlat][{idx}]={disp}")
        return formatted


@dataclass
class Listing(ListingRoot):
    id: int
    disposition: str
    location: str
    area: int
    price: int
    url: str


class Scraper(ScraperRoot):
    def __init__(self, regions, dispositions: Dispositions,
                 price=(None, None), area=(None, None)):
        self.regions = '&s-l=' + ';'.join(regions)
        self.dispositions = '&' + '&'.join(dispositions.get_formatted())
        self.price_min = f"&s-qc[priceMin][{price[0]}]" if price[0] else ""
        self.price_max = f"&s-qc[priceMax][{price[1]}]" if price[1] else ""
        self.area_min = f"&s-qc[usableAreaMin][{area[0]}]" if area[0] else ""
        self.area_max = f"&s-qc[usableAreaMax][{area[1]}]" if area[1] else ""

    @classmethod
    def query_region(cls, query: str) -> str:
        url  = "https://reality.idnes.cz/admin.api/autocomplete-locality"
        url += "?fe=1&types[0]=OKRES&types[1]=OBEC"
        query = quote_plus(query)
        req = requests.get(f"{url}&string={query}")

        # TODO: handle request and parse errors
        data     = req.json()[0]
        req_type = data["type"]
        req_id   = data["id"]
        return f"{req_type}-{req_id}"

    def scrape(self) -> [Listing]:
        url  = f"https://reality.idnes.cz/s/pronajem/byty/?"
        url += ''.join(vars(self).values())

        req = requests.get(url)

        # Get the number of pages that we'll have to scrape
        soup = BeautifulSoup(req.text, features="lxml")
        n_pages = [i for i in soup.find(
            class_="paginator paging mt--20 mb-45 text-center m-auto")]
        n_pages = int(n_pages[-4].text)

        # We scraped the first page already; save it and scrape the rest
        page_soups = [soup]
        for page in range(1, n_pages):
            req = requests.get(url + f"&page={page}")

            if req.ok:
                page_soups.append(BeautifulSoup(req.text, features="lxml"))
            else:
                print(f"idnes scraping failed for page {page}")

        # Go through each of the soups and get the listings
        listings = []
        for soup in page_soups:
            # Get the listing entries
            entries = soup.find_all(
                class_="grid__cell size--t-4-12 size--m-6-12 size--s-12-12")

            # Go through each entry
            for entry in entries:
                # Skip ads
                if entry.find(class_="c-products__item-advertisment"):
                    continue

                # Get the info required for `Listing`

                url = entry.find(class_="c-products__link")['href']
                ident = int(url.strip('/').split('/')[-1], 16)

                info = entry.find(class_="c-products__title").text.split()
                disp = info[2]
                area = int(info[3])

                location = entry.find(class_="c-products__info").text.strip()

                # Skip listings with unlisted prices
                price = entry.find(class_="c-products__price").text.split()[:-1]
                try:
                    price = int(''.join(price))
                except:
                    continue

                # Save the listing
                listings.append(Listing(
                    id=ident, disposition=disp, area=area, price=price,
                    url=url, location=location))

        return listings
