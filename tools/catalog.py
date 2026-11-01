#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fifty Fifty Magazine - Editorial Photo Catalog & Route Indexer
Enables quick retrieval of photos by Country, City, POI, Route Segment, Tags, and Visual Type.
Used when planning itineraries (hành trình tuyến điểm) and composing articles.
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

CATALOG_PATH = Path(__file__).resolve().parent.parent / "data" / "photo-catalog.json"

def load_catalog():
    if not CATALOG_PATH.exists():
        return []
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_catalog(data):
    CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def search_photos(country=None, city=None, route=None, tag=None, poi=None, query=None):
    catalog = load_catalog()
    results = []
    
    for item in catalog:
        match = True
        if country and item.get("country", "").lower() != country.lower():
            match = False
        if city and item.get("city", "").lower() != city.lower():
            match = False
        if route and route.lower() not in item.get("route_segment", "").lower():
            match = False
        if poi and poi.lower() not in item.get("poi", "").lower():
            match = False
        if tag:
            tags = [t.lower() for t in item.get("tags", [])]
            if tag.lower() not in tags:
                match = False
        if query:
            q = query.lower()
            haystack = " ".join([
                item.get("id", ""),
                item.get("caption", ""),
                item.get("poi", ""),
                item.get("city", ""),
                item.get("country", ""),
                " ".join(item.get("tags", []))
            ]).lower()
            if q not in haystack:
                match = False
        
        if match:
            results.append(item)
    return results

def main():
    parser = argparse.ArgumentParser(description="Fifty Fifty Magazine Photo Catalog")
    subparsers = parser.add_subparsers(dest="command")
    
    # Search command
    search_p = subparsers.add_parser("search", help="Search photos in catalog")
    search_p.add_argument("--country", "-c", help="Country code (vn, la, th, kh, etc.)")
    search_p.add_argument("--city", help="City name (e.g. vientiane, bangkok, hanoi)")
    search_p.add_argument("--route", "-r", help="Route segment (e.g. ha-giang-loop, vientiane-1-day)")
    search_p.add_argument("--tag", "-t", help="Tag (e.g. temple, food, sunset, reclining-buddha)")
    search_p.add_argument("--poi", help="Point of Interest (e.g. pha-that-luang)")
    search_p.add_argument("--query", "-q", help="Free text search query")
    search_p.add_argument("--format", choices=["table", "markdown", "json"], default="table")
    
    # Stats command
    subparsers.add_parser("stats", help="Display catalog stats")
    
    args = parser.parse_args()
    
    if args.command == "search":
        items = search_photos(args.country, args.city, args.route, args.tag, args.poi, args.query)
        print(f"\nFound {len(items)} matching photos:\n" + "="*60)
        
        if args.format == "json":
            print(json.dumps(items, ensure_ascii=False, indent=2))
        elif args.format == "markdown":
            for it in items:
                print(f"![{it.get('caption', '')}]({it.get('url', '')})")
                print(f"*{it.get('caption', '')}* — `#{' #'.join(it.get('tags', []))}`\n")
        else:
            for it in items:
                print(f"[{it['id']}] ({it['country'].upper()} / {it['city']})")
                print(f"  POI:   {it.get('poi')}")
                print(f"  Route: {it.get('route_segment')}")
                print(f"  Tags:  {', '.join(it.get('tags', []))}")
                print(f"  URL:   {it.get('url')}")
                print(f"  Desc:  {it.get('caption')}")
                print("-" * 60)
                
    elif args.command == "stats":
        catalog = load_catalog()
        print(f"\nFifty Fifty Magazine - Photo Catalog Stats")
        print(f"Total indexed photos: {len(catalog)}")
        
        countries = {}
        cities = {}
        all_tags = set()
        routes = set()
        
        for it in catalog:
            c = it.get("country", "unknown")
            countries[c] = countries.get(c, 0) + 1
            ct = it.get("city", "unknown")
            cities[ct] = cities.get(ct, 0) + 1
            for t in it.get("tags", []):
                all_tags.add(t)
            if it.get("route_segment"):
                routes.add(it.get("route_segment"))
                
        print("\nBy Country:")
        for k, v in countries.items():
            print(f"  - {k.upper()}: {v} photos")
            
        print("\nBy Destination / City:")
        for k, v in sorted(cities.items()):
            print(f"  - {k}: {v} photos")
            
        print(f"\nIndexed Route Segments ({len(routes)}):")
        for r in sorted(routes):
            print(f"  * {r}")
            
        print(f"\nTotal unique tags: {len(all_tags)}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
