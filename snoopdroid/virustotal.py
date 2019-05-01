#!/usr/bin/env python3
# Snoopdroid
# Copyright (C) 2019  Claudio Guarnieri
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import time
import requests

from halo import Halo
from terminaltables import AsciiTable

from .ui import info, highlight, red

def get_virustotal_report(apikey, sha256):
    url = "https://www.virustotal.com/vtapi/v2/file/report?apikey={apikey}&resource={resource}"
    res = requests.get(url.format(apikey=apikey, resource=sha256))
    return res.json()

def virustotal_lookup(apikey, rate, packages):
    delay = 60 / rate

    total_files = 0
    for package in packages:
        total_files += len(package.files)

    eta = delay * total_files

    print(info("Looking up all extracted files on " + highlight("VirusTotal") + " (www.virustotal.com)."))
    print(info("This will take about {} seconds...".format(eta)))
    print("")

    table_data = []
    table_data.append(["Package name", "File path", "Detections"])

    with Halo(text="", spinner="bouncingBar") as spinner:
        total_packages = len(packages)
        counter = 0
        for package in packages:
            counter += 1

            spinner.text = "Looking up {} [{}/{}]".format(package.name, counter, total_packages)

            for file in package.files:
                while True:
                    try:
                        report = get_virustotal_report(apikey, file["sha256"])
                        test = report["response_code"]
                    except Exception as e:
                        time.sleep(delay)
                        continue
                    else:
                        break

                row = [package.name, file["stored_path"],]

                if report["response_code"] == 0:
                    row.append("")
                else:
                    detections = "{}/{}".format(report["positives"], report["total"])
                    if report["positives"] > 0:
                        detections = red(detections)

                    row.append(detections)

                table_data.append(row)

                time.sleep(delay)

        spinner.succeed("Completed!")

    print("")

    table = AsciiTable(table_data)
    print(table.table)
