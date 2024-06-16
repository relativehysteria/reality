#!/usr/bin/env python

from concurrent.futures import ThreadPoolExecutor
import bezrealitky
import sreality

pool = ThreadPoolExecutor(max_workers=10)


regions = ["okres Brno-město", "okres Brno-venkov"]
br_regions = pool.map(bezrealitky.query_region, regions.copy())
sr_regions = pool.map(sreality.query_region, regions.copy())

br_dispositions = ["DISP_3_1"] + bezrealitky.dispositions(4)
br_scraper = bezrealitky.Scraper(list(br_regions), br_dispositions)
br_listings = pool.submit(bezrealitky.Scraper.scrape, br_scraper)

sr_dispositions = [6] + sreality.dispositions(4)
sr_scraper = sreality.Scraper(list(sr_regions), sr_dispositions)
sr_listings = pool.submit(sreality.Scraper.scrape, sr_scraper)

# # these are meant to run in the background; we don't care about their results
# pool.map(bezrealitky.Listing.scrape_images, br_listings.result())
# pool.map(sreality.Listing.scrape_images, sr_listings.result())

br_listings = br_listings.result()
sr_listings = sr_listings.result()
all_listings = list(br_listings) + list(sr_listings)
all_listings.sort(key=lambda x: x.price)

for listing in all_listings:
    print(f"{listing.disposition:>4}" +
          f" | {listing.area:>3}m" +
          f" | {listing.price:>5},-" +
          f" | {listing.location}")
