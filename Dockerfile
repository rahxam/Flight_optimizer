# Playwright-Image bringt Node und ein passendes Chromium schon mit - das ist der
# fragilste Teil eines Scraper-Setups und hier bereits geloest.
FROM mcr.microsoft.com/playwright:v1.49.1-jammy

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    TZ=Atlantic/Canary

RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 python3-yaml tzdata sqlite3 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Node-Abhaengigkeiten zuerst, damit der Layer-Cache bei Codeaenderungen haelt.
COPY package.json package-lock.json* ./
RUN npm install --omit=dev --no-audit --no-fund

COPY src/ ./src/
COPY data/ ./data/
COPY scripts/ ./scripts/
COPY docs/ ./docs/
COPY docker/entrypoint.sh ./docker/entrypoint.sh
RUN chmod +x ./docker/entrypoint.sh

# Scrape-Rohdaten und die SQLite-Historie leben im Volume.
VOLUME ["/app/data/prices"]

ENTRYPOINT ["./docker/entrypoint.sh"]
