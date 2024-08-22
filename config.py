regions = ["okres Brno-město", "okres Brno-venkov"]

dispositions = ["1+1", "2+kk", "2+1", "3+kk"]

filters = [
    lambda listing: listing.area > 40,
    lambda listing: listing.price < 21000,
]

browser = "firefox"
