### Start commands:

```bash
docker compose run --rm -e LOG_FILE=logs/scraper-sell.log scraper python -m scraper.main --sell --new

docker compose run --rm -e LOG_FILE=logs/scraper-lease.log scraper python -m scraper.main --lease --new
```

