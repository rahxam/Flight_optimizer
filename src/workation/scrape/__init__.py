"""Google-Flights-Abfragen: URL-Bau, Query-Matrix, optionaler Scraper."""

from .urls import google_flights_url, multicity_url, oneway_url, roundtrip_url

__all__ = ["google_flights_url", "oneway_url", "roundtrip_url", "multicity_url"]
