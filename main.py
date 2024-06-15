#!/usr/bin/env python

import bezrealitky

regions = [bezrealitky.query_osm("okres Brno-město"),
           bezrealitky.query_osm("okres Brno-venkov"),]

scraper = bezrealitky.Scraper(regions)
listings = scraper.scrape()

for listing in listings:
    print(f"{listing.disposition[5:].replace('_', '+'):>4}" +
          f" | {listing.surface:>3}m" +
          f" | {listing.price + listing.charges:<5},-")

print(f"{len(listings)} available")
