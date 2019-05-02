# -*- coding: utf-8 -*-
#
# Snoopdroid
#
# Copyright (C) 2019 Claudio Guarnieri <https://nex.sx>
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

def get_virustotal_report(hashes):
    apikey = "233f22e200ca5822bd91103043ccac138b910db79f29af5616a9afe8b6f215ad"
    url = "https://www.virustotal.com/partners/sysinternals/file-reports?apikey={}".format(apikey)

    items = []
    for sha256 in hashes:
        items.append({
            "hash": sha256,
            "image_path": "unknown",
            "creation_datetime": "unknown",
        })
    headers = {"User-Agent": "VirusTotal", "Content-Type": "application/json"}
    res = requests.post(url, headers=headers, json=items)

    if res.status_code == 200:
        report = res.json()
        return report["data"]

    return None

def virustotal_lookup(packages):
    print(info("Looking up all extracted files on " + highlight("VirusTotal") + " (www.virustotal.com)."))
    print("")

    detections = {}

    def virustotal_query(batch):
        report = get_virustotal_report(batch)
        if report:
            for entry in report:
                if entry["hash"] not in detections and entry["found"] == True:
                    detections[entry["hash"]] = entry["detection_ratio"]

    with Halo(text="", spinner="bouncingBar") as spinner:
        batch = []
        for package in packages:
            for file in package.files:
                batch.append(file["sha256"])
                if len(batch) == 25:
                    spinner.text = "Looking up first 25 apps..."

                    virustotal_query(batch)
                    batch = []

        if batch:
            spinner.text = "Looking up remaining files..."
            virustotal_query(batch)

        spinner.succeed("Completed!")

    table_data = []
    table_data.append(["Package name", "File path", "Detections"])

    for package in packages:
        for file in package.files:
            row = [package.name, file["stored_path"],]

            if file["sha256"] in detections:
                detection = detections[file["sha256"]]
                positives = detection.split("/")[0]
                if int(positives) > 0:
                    row.append(red(detection))
                else:
                    row.append(detection)
            else:
                row.append("not found")

            table_data.append(row)

    print("")

    table = AsciiTable(table_data)
    print(table.table)
