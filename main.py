#!/usr/bin/env python

from concurrent.futures import ThreadPoolExecutor
import bezrealitky
import sreality

def get_listings(regions, dispositions):
    pool = ThreadPoolExecutor(max_workers=10)

    br_regions = pool.map(bezrealitky.Scraper.query_region, regions.copy())
    sr_regions = pool.map(sreality.Scraper.query_region, regions.copy())

    br_dispositions = bezrealitky.Dispositions(dispositions.copy())
    br_scraper = bezrealitky.Scraper(list(br_regions), br_dispositions)
    br_listings = pool.submit(bezrealitky.Scraper.scrape, br_scraper)

    sr_dispositions = sreality.Dispositions(dispositions.copy())
    sr_scraper = sreality.Scraper(list(sr_regions), sr_dispositions)
    sr_listings = pool.submit(sreality.Scraper.scrape, sr_scraper)

    # these are meant to run in the background; we don't care about their resulst
    pool.map(bezrealitky.Listing.scrape_images, br_listings.result())
    pool.map(sreality.Listing.scrape_images, sr_listings.result())

    br_listings = br_listings.result()
    sr_listings = sr_listings.result()
    all_listings = list(br_listings) + list(sr_listings)

    return all_listings

if __name__ == "__main__":
    regions = ["okres Brno-město", "okres Brno-venkov"]
    dispositions = ["1+kk", "1+1"]

    for listing in get_listings(regions, dispositions):
        print(listing)
