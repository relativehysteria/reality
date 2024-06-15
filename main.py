#!/usr/bin/env python

from concurrent.futures import ThreadPoolExecutor
import bezrealitky

regions = [bezrealitky.query_osm("okres Brno-město"),
           bezrealitky.query_osm("okres Brno-venkov"),]
dispositions = ["DISP_3_1"] + bezrealitky.dispositions(4)

scraper = bezrealitky.Scraper(regions, dispositions)
listings = scraper.scrape()

# net_pool = ThreadPoolExecutor(max_workers=10)
# net_pool.map(bezrealitky.Listing.scrape_images, listings)

for listing in listings:
    print(f"{listing.disposition[5:].replace('_', '+'):>4}" +
          f" | {listing.surface:>3}m" +
          f" | {listing.price + listing.charges:>5},-")

print(f"{len(listings)} available")
