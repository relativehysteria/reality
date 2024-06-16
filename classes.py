class ListingRoot:
    def __init__(self, **kwargs):
        self.ident = None
        self.dispositin = None
        self.area = None
        self.price = None
        self.images = None

    def __str__(self):
        return str(vars(self))

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
