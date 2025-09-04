This project scrapes data from the sjsuparkingstatus, then presents it as a graph.

get_status.py can be run on the command line or imported as a python module. It scrapes the status, and returns it in json, csv, or as a human readable printout.

job.sh is run by a systemd timer everty 30 mins on my home server. It runs get_status.py, and then appends the result to garage_status_log.json. It then git commits and pushes.

The website, which is just index.html, is served by github pages.