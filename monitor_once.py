import json, os, sys, requests

URL = "https://prestoservice.eventpipe.com/events/3e7bc4d0-5679-4218-8cef-ee9bfe77006e/details"
topic = os.environ["NTFY_TOPIC"]
payload = json.loads(os.environ["PAYLOAD_JSON"])

def notify(title, msg, priority):
    requests.post(
        f"https://ntfy.sh/{topic}",
        data=msg.encode("utf-8"),
        headers={"Title": title, "Priority": priority},
        timeout=30,
    )

try:
    r = requests.post(URL, json=payload, headers={"Accept": "application/json"}, timeout=30)
    r.raise_for_status()
    status = r.json().get("hotel", {}).get("availabilityType")
    print("availability:", status)
except Exception as e:
    print("error:", e)
    notify("Hotel monitor error", "Check failed. payload may have expired.", "default")
    sys.exit(1)

if status != "SOLD_OUT":
    notify("Signia room status changed!", f"Status is now {status}. Check the booking site now.", "urgent")
