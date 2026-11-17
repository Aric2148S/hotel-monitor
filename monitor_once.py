name: Hotel check
on:
  schedule:
    - cron: "*/5 * * * *"
  workflow_dispatch:
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install requests
      - run: python monitor_once.py
        env:
          NTFY_TOPIC: ${{ secrets.NTFY_TOPIC }}
          PAYLOAD_JSON: ${{ secrets.PAYLOAD_JSON }}
