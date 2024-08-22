# Dispositions are in the form of
# 1+kk, 1+1, 2+kk, 2+2 etc.
class DispositionsRoot:
    def __init__(self, disp_list=[]):
        self.inner = set()

        for disp in disp_list:
            self.add(disp)

    def __iter__(self):
        return iter(self.inner)

    def add(self, disp_str: str):
        assert self.verify_disp_str(disp_str), \
                f"Invalid disposition string: {disp_str}"
        self.inner.add(self.disp_str_to_api(disp_str))

    def remove(self, disp_str: str):
        assert self.verify_disp_str(disp_str), \
                f"Invalid disposition string: {disp_str}"
        self.inner.remove(self.disp_str_to_api(disp_str))

    @classmethod
    def verify_disp_str(cls, disp_str: str):
        raise NotImplementedError

    @classmethod
    def api_to_disp_str(cls, api_disp):
        raise NotImplementedError

    @classmethod
    def disp_str_to_api(cls, disp_str: str):
        raise NotImplementedError


class ListingRoot:
    def __init__(self, **kwargs):
        self.id: int = None
        self.location: str = None
        self.disposition: str = None
        self.area: int = None
        self.price: int = None
        self.url: str = None

    def __str__(self):
        return f"{self.disposition:>4}" +\
               f" | {self.area:>3}m²" +\
               f" | {self.price:>5},-" +\
               f" | {self.location}"


class ScraperRoot:
    def __init__(self, regions, dispositions: [DispositionsRoot],
                 price=(None, None), area=(None, None)):
        raise NotImplementedError

    def scrape(self) -> ListingRoot:
        raise NotImplementedError

    @classmethod
    def query_region(cls, query: str) -> str:
        raise NotImplementedError
