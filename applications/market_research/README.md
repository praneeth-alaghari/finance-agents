# Market Research Application

This application provides market-level intelligence and macro/sector research that can be used independently or combined with the portfolio research application.

## What it does

- analyzes macroeconomic conditions
- tracks sector trends and momentum
- summarizes earnings for a set of companies or watchlists
- produces a reusable `MarketContext` for downstream portfolio analysis

## Typical workflow

1. Fetch market signals for a sector or watchlist.
2. Summarize macro indicators and sector rotation.
3. Produce company earnings notes for the selected universe.
4. Return a shared `MarketContext` object that other finance apps can consume.

## Why this matters

This app is intentionally reusable:
- it can run by itself as a research tool
- it can also feed the portfolio research app with market context when the user wants portfolio-specific recommendations.
