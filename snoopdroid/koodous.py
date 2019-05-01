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

import requests

from halo import Halo
from terminaltables import AsciiTable

from .ui import info, highlight, green, red

def get_koodous_report(sha256):
    url = "https://api.koodous.com/apks/{}".format(sha256)
    res = requests.get(url)
    return res.json()

def koodous_lookup(packages):
    print(info("Looking up all extracted files on " + highlight("Koodous") + " (www.koodous.com)."))
    print(info("This might take a while..."))
    print("")

    table_data = []
    table_data.append(["Package name", "File path", "Trusted", "Detected", "Rating"])

    with Halo(text="", spinner="bouncingBar") as spinner:
        total_packages = len(packages)
        counter = 0
        for package in packages:
            counter += 1

            spinner.text = "Looking up {} [{}/{}]".format(package.name, counter, total_packages)

            for file in package.files:
                report = get_koodous_report(file["sha256"])

                if "package_name" in report:
                    trusted = "no"
                    if report["trusted"]:
                        trusted = green("yes")

                    detected = "no"
                    if report["detected"]:
                        detected = red("yes")

                    rating = "0"
                    if int(report["rating"]) < 0:
                        rating = red(str(report["rating"]))

                    row = [package.name, file["stored_path"], trusted, detected, rating]
                else:
                    row = [package.name, file["stored_path"], "", "", ""]

                table_data.append(row)

        spinner.succeed("Completed!")

    print("")

    table = AsciiTable(table_data)
    print(table.table)
