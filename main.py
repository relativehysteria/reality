#!/usr/bin/env python

from concurrent.futures import ThreadPoolExecutor
import bezrealitky
import sreality

# regions = [bezrealitky.query_region("okres Brno-město"),
#            bezrealitky.query_region("okres Brno-venkov"),]
# dispositions = ["DISP_3_1"] + bezrealitky.dispositions(4)
#
# scraper = bezrealitky.Scraper(regions, dispositions)
# listings = scraper.scrape()
#
# #net_pool = ThreadPoolExecutor(max_workers=10)
# #net_pool.map(bezrealitky.Listing.scrape_images, listings)
#
# for listing in listings:
#     print(f"{listing:>4}" +
#           f" | {listing.area:>3}m" +
#           f" | {listing.price:>5},-")
#
# print(f"{len(listings)} available")

################################################################################

regions = [sreality.query_region("okres Brno-město"),
           sreality.query_region("okres Brno-venkov"),]
dispositions = [6] + sreality.dispositions(4)

scraper = sreality.Scraper(regions, dispositions)
listings = scraper.scrape()

#net_pool = ThreadPoolExecutor(max_workers=10)
#net_pool.map(sreality.Listing.scrape_images, listings)

for listing in listings:
    print(f"{listing.disposition:>4}" +
          f" | {listing.area:>3}m" +
          f" | {listing.price:>5},-")
