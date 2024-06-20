# Dispositions are in the form of
# 1kk, 1+1, 2kk, 2+2 etc.
class DispositionsRoot:
    def __init__(self, disp_list=[]):
        self.inner = set(self.disp_str_to_api(disp) for disp in disp_list)

    def __iter__(self):
        return iter(self.inner)

    def add(self, disp_str: str):
        self.inner.add(self.disp_str_to_api(disp_str))

    def remove(self, disp_str: str):
        self.inner.remove(self.disp_str_to_api(disp_str))

    @classmethod
    def api_to_disp_str(cls, api_disp):
        raise NotImplementedError

    @classmethod
    def disp_str_to_api(cls, disp_str: str):
        raise NotImplementedError


class ListingRoot:
    def __init__(self, **kwargs):
        self.id = None
        self.disposition = None
        self.area = None
        self.price = None
        self.images = None
        self.url = None

    def __str__(self):
        return f"{self.disposition:>4}" +\
               f" | {self.area:>3}m²" +\
               f" | {self.price:>5},-" +\
               f" | {self.location}"

    def get_images(self):
        raise NotImplementedError

    def scrape_images(self):
        raise NotImplementedError


class ScraperRoot:
    def __init__(self, regions, dispositions: [DispositionsRoot],
                 price=(None, None), area=(None, None)):
        raise NotImplementedError

    def scrape(self) -> ListingRoot:
        raise NotImplementedError
