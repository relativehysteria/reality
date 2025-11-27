#!/usr/bin/env python

from sys import stderr
from types import ModuleType
from typing import Optional, Tuple, List
from os import system, name as system_name
from concurrent.futures import ThreadPoolExecutor
import importlib
import pkgutil
import json
import config

def get_listings_future(
    module: ModuleType,
    pool: ThreadPoolExecutor,
    provided_regs: List[str],
    dispositions: List[str]
) -> Optional[Tuple[ModuleType, ThreadPoolExecutor]]:
    mod_name = module.__name__.replace("scrapers.", "")

    # Query regions ids, dispositions and build the scraper, in parallel
    regions = pool.map(module.Scraper.query_region, provided_regs.copy())
    dispositions = module.Dispositions(dispositions.copy())

    # Print out the regions we weren't able to scrape
    regions = [i for i in regions]
    parsed = set(i[0] for i in regions if i[1] is not None)
    provided = set(provided_regs)
    for reg in (provided - parsed):
        print(f'{mod_name}: Couldn\'t find estates in "{reg}".', file=stderr)

    # Retain the regions we actually parsed
    regions = [i[1] for i in regions if i[1] is not None]

    # If there are no regions whatsoever, bail out
    if len(regions) == 0:
        print(f"{mod_name}: No regions could be scraped.", file=stderr)
        return None

    # Start scraping and return the listings together with the module
    # from which the scraper was imported
    scraper = module.Scraper(list(regions), dispositions)
    listings_future = pool.submit(module.Scraper.scrape, scraper)
    return (module, listings_future)


def get_listings(regs, disps):
    # Build the threadpool to use in scraping
    pool = ThreadPoolExecutor(max_workers=10)

    # Dynamically import scraper modules
    package = importlib.import_module("scrapers")
    modules = [
        importlib.import_module(f"{package.__name__}.{name}")
        for _, name, _ in pkgutil.iter_modules(package.__path__)
        if name in config.enabled_scrapers
    ]

    # Collect the futures of the scraper tasks
    futures = [pool.submit(get_listings_future, m, pool, regs, disps)
               for m in modules]
    futures = [i.result() for i in futures if i.result() is not None]


    # Invoke the tasks and save the results
    listings = {}
    for (module, future) in futures:
        module_name = module.__name__.split('.')[-1]
        listings[module_name] = future.result()

    # Return the scraped results
    return listings


def read_db(db_path):
    # Make sure the database exists
    with open(db_path, 'a') as f:
        pass

    # Read the data
    with open(db_path) as f:
        data = f.read()

    # If the database is empty, return an empty dict, else return data
    if data != "":
        return json.loads(data)
    return {}


def write_db(data, db_path):
    # Only write down the IDs
    ids = {}
    for key in data.keys():
        ids[key] = [i.id for i in data[key]]
    with open(db_path, 'w') as f:
        json.dump(ids, f)


def get_new_listings(new, old):
    new_listings = {}

    for key in new.keys():
        # Create dictionaries to map IDs to objects for quick lookup
        new_listings_dict = {obj.id: obj for obj in new[key]}
        old_ids = set(i for i in old[key]) if key in old else set()

        # Calculate new listings and store them
        new_ids = set(new_listings_dict.keys()) - old_ids
        new_listings[key] = [new_listings_dict[i] for i in new_ids]

    return new_listings


if __name__ == "__main__":
    DB_NAME = "ids.txt"

    # Get new data, load old data and check new IDs
    print("it's free real estate...")
    new_data = get_listings(config.regions, config.dispositions)
    old_data = read_db(DB_NAME)
    new_listings = get_new_listings(new_data, old_data)

    # Filter the listings
    for f in config.filters:
        for key in new_listings:
            new_listings[key] = list(filter(f, new_listings[key]))

    # Open the listings in a browser, in parallel
    for reality in new_listings:
        if len(new_listings[reality]) == 0:
            continue

        # If we're on windows, we have to prepend "exec"
        exec_string = f"{config.browser}"
        if system_name == "nt":
            exec_string = f"exec {sys_string}"

        # Open the listings in parallel
        with ThreadPoolExecutor() as executor:
            def process_listing(obj):
                system(f"{exec_string} {obj.url}")

            executor.map(process_listing, new_listings[reality])

    # Write the data down
    write_db(new_data, DB_NAME)
