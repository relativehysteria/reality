regions = ["okres Brno-město", "okres Brno-venkov"]

dispositions = ["1+1", "2+kk"]

filters = [
    lambda listing: listing.area > 40,
    lambda listing: listing.price < 20000,
]

browser = "firefox"
