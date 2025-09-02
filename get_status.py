#!/home/timeglotch/Projects/SJSUParkingMonitor/.venv/bin/python3
import json
import requests
import urllib3
from bs4 import BeautifulSoup
import datetime
import argparse

#This script scrapes the SJSU parking status website for garage fullness information
#timestamps should be in the format "YYYY-MM-DD HH:MM:SS" in Pacific Time (where SJSU is located)

def get_garage_status(output="human"):
	url = "https://sjsuparkingstatus.sjsu.edu"
	urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
	response = requests.get(url, verify=False)
	soup = BeautifulSoup(response.content, "html.parser")
	garages = ["South", "West", "North", "South Campus"]
	results = {}
	for garage in garages:
		h2 = soup.find("h2", class_="garage__name", string=lambda s: s and garage in s)
		if h2:
			fullness_span = h2.find_next("span", class_="garage__fullness")
			if fullness_span:
				fullness = fullness_span.text.strip()
				if '%' in fullness:
					fullness = fullness.replace('%', '').strip()
				else: #if there is no percent, then fullness is the value "FULL" which should be 100%
					fullness = "100"
				results[garage] = fullness
			else:
				results[garage] = "Not found"
		else:
			results[garage] = "Not found"
	timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	if output == "csv":
		#format: timestamp, South, West, North, South Campus
		#garage fullness is an int from 0 - 100
		csv_values = [timestamp] + [results[garage] for garage in garages]
		return ",".join(csv_values)
	elif output == "json":
		#format: {"timestamp": "2025-09-02 15:36:19", "South": 90, "West": 84, "North": 83, "South Campus": 31}
		json_values = {"timestamp": timestamp}
		for garage in garages:
			json_values[garage] = results[garage]
		return json_values
	else: #if output == "human"
		lines = [f"Timestamp: {timestamp}"]
		for garage, fullness in results.items():
			lines.append(f"{garage} Garage: {fullness}")
		return "\n".join(lines)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--csv", action="store_true", help="CSV output")
	parser.add_argument("-j", "--json", action="store_true", help="JSON output")
	args = parser.parse_args()
	output = get_garage_status(output="csv" if args.csv else "json" if args.json else "human")
	print(output)