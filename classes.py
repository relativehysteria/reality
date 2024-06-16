class ListingRoot:
    def __init__(self, **kwargs):
        self.id = None
        self.disposition = None
        self.area = None
        self.price = None
        self.images = None

    def __str__(self):
        return f"{self.disposition:>4}" +\
               f" | {self.area:>3}m" +\
               f" | {self.price:>5},-" +\
               f" | {self.location}"

    def get_images(self):
        raise NotImplementedError

    def scrape_images(self):
        raise NotImplementedError


class ScraperRoot:
    def __init__(self, regions, dispositions,
                 price=(None, None), area=(None, None)):
        raise NotImplementedError

    def scrape(self) -> ListingRoot:
        raise NotImplementedError
