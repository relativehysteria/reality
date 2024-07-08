regions = ["okres Brno-město"]

dispositions = ["1+kk", "1+1", "2+kk", "2+1", "3+kk", "3+1", "4+kk", "4+1"]

filters = [
    lambda listing: listing.area > 40,
    lambda listing: listing.price < 20000,
]

browser = "firefox"
