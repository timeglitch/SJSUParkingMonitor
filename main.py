import get_status

#run the get_garage_status function and append it to garage_status_log.json
import json

status = get_status.get_garage_status(output="json")
try:
    with open("garage_status_log.json", "r") as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    data = []
data.append(status)
with open("garage_status_log.json", "w") as f:
    json.dump(data, f, indent=2)

    
