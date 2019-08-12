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

import os
import yaml

from terminaltables import AsciiTable

from .ui import info, highlight, error

def known_bad(packages):
    print(info("Looking for known bad packages installed"))
    print("")

    yaml_path = os.path.join(os.path.dirname(__file__), "data", "knownbad.yaml")
    if not os.path.exists(yaml_path):
        print(error("I can not find the `knownbad.yaml` file at {}. Have you installed Snoopdroid correctly?".format(yaml_path)))
        return

    with open(yaml_path) as handle:
        baddies = yaml.load(handle)

    found_baddies = []
    for package in packages:
        for baddy in baddies:
            if package.name.lower() == baddy["package"].lower():
                found_baddies.append(baddy)

    if not found_baddies:
        print(info("Nothing found."))
        return

    print(highlight("I found matches with known bad applications!"))

    table_data = []
    table_data.append(["Package name", "Malware Name", "Tags", "Reference"])

    for found_baddy in found_baddies:
        table_data.append([
            found_baddy["package"],
            found_baddy["name"],
            ", ".join(found_baddy["tags"]),
            found_baddy["reference"]
        ])

    table = AsciiTable(table_data)
    print(table.table)
