import requests
from urllib.parse import quote_plus

GRAPH_QUERY = """
    query AdvertList(
        $locale: Locale!,
        $estateType: [EstateType],
        $offerType: [OfferType],
        $disposition: [Disposition],
        $regionOsmIds: [ID],
        $limit: Int = 0,
        $order: ResultOrder = TIMEORDER_DESC,
        $priceFrom: Int,
        $priceTo: Int,
        $surfaceFrom: Int,
        $surfaceTo: Int,
        $roommate: Boolean,
        $currency: Currency
    ) {
        listAdverts(
            offerType: $offerType
            estateType: $estateType
            disposition: $disposition
            limit: $limit
            regionOsmIds: $regionOsmIds
            order: $order
            priceFrom: $priceFrom
            priceTo: $priceTo
            surfaceFrom: $surfaceFrom
            surfaceTo: $surfaceTo
            roommate: $roommate
            currency: $currency
        ) {
            list {
                id
                disposition
                mainImageUrl: mainImage {
                    url(filter: RECORD_THUMB)
                }
                address(locale: $locale)
                surface
                tags(locale: $locale)
                price
                charges
                reserved
                gps {
                    lat
                    lng
                }
            }
        }
        actionList: listAdverts(
            offerType: $offerType
            estateType: $estateType
            disposition: $disposition
            regionOsmIds: $regionOsmIds
            order: $order
            priceFrom: $priceFrom
            priceTo: $priceTo
            surfaceFrom: $surfaceFrom
            surfaceTo: $surfaceTo
            roommate: $roommate
        ) {
            totalCount
        }
    }
"""


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

        if self.mainImageUrl:
            self.mainImageUrl = self.mainImageUrl['url']

    def __str__(self):
        return str(vars(self))


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


    def vars(self):
        assert self.disposition
        assert self.regionOsmIds

        for attr in [
            "priceFrom",
            "priceTo",
            "surfaceFrom",
            "surfaceTo",
            "petFriendly",
        ]:
            value = getattr(self, attr)
            assert value is None or isinstance(value, int)

        return { k: v for k, v in vars(self).items() if v is not None }


    def scrape(self) -> [Listing]:
        graph_url = "https://api.bezrealitky.cz/graphql/"
        headers = { "content-type": "application/json", }
        payload = {
            "operationName": "AdvertList",
            "variables": self.vars(),
            "query": GRAPH_QUERY,
        }
        # TODO: handle request and parse errors
        req = requests.post(graph_url, headers=headers, json=payload)
        return [Listing(**i) for i in req.json()['data']['listAdverts']['list']]
