#!/usr/bin/env python3
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
import sys
import argparse
import datetime
import json

from .ui import info, logo
from .acquisition import Acquisition
from .virustotal import virustotal_lookup
from .koodous import koodous_lookup
from .knownbad import known_bad


def main():
    parser = argparse.ArgumentParser(description="Extract information from Android device")
    parser.add_argument("--storage", default=os.getcwd(), help="Specify a different base folder to store the acquisition")
    parser.add_argument("--limit", default=None, help="Set a limit to the number of packages to extract (mainly for debug purposes)")
    parser.add_argument("--all-apks", action="store_true", help="Extract all packages installed on the phone, even those marked as safe")
    parser.add_argument("--virustotal", action="store_true", help="Check packages on VirusTotal")
    parser.add_argument("--koodous", action="store_true", help="Check packages on Koodous")
    parser.add_argument("--all-checks", action="store_true", help="Run all available checks")
    parser.add_argument("--from-file", default=None, help="Instead of acquiring from phone, load an existing packages.json file for lookups (mainly for debug purposes)")
    args = parser.parse_args()

    if not args.from_file:
        # TODO: Need to come up with a better folder name.
        acq_folder = datetime.datetime.now().isoformat().split(".")[0].replace(":", "")
        storage_folder = os.path.join(args.storage, acq_folder)

        if not os.path.exists(storage_folder):
            os.mkdir(storage_folder)

        print(info("Starting acquisition at folder {}\n".format(storage_folder)))

    logo()

    try:
        if args.from_file:
            acq = Acquisition.fromJSON(args.from_file)
        else:
            acq = Acquisition(storage_folder=storage_folder,
                all_apks=args.all_apks, limit=args.limit)
            acq.run()

        packages = acq.packages
        if len(packages) == 0:
            return

        if args.virustotal or args.all_checks:
            results_vt = virustotal_lookup(packages)

        print("")

        if args.koodous or args.all_checks:
            results_koodous = koodous_lookup(packages)

        print("")

        results_known_bad = known_bad(packages)

        if not args.from_file:
            detections = {}
            if args.virustotal or args.all_checks:
                for r in results_vt:
                    detections[r] = {
                        'package': results_vt[r]['name'],
                        'virustotal': {
                            'found': results_vt[r]['found'],
                            'detection': results_vt[r]['detection']
                        }
                    }
            if args.koodous or args.all_checks:
                for sha256 in results_koodous:
                    if sha256 in detections:
                        detections[sha256]['koodous'] = {'detected': True}
                    else:
                        detections[sha256] = {
                            'package': results_koodous[sha256]['name'],
                            'koodous': {'detected': True}
                        }
            if results_known_bad:
                results_pkg = dict([(p['package'], p) for p in results_known_bad])
                for package in packages:
                    if package.name in results_pkg:
                        for file in package.files:
                            if file["sha256"] in detections:
                                detections[file["sha256"]]['known_bad'] = results_pkg[package.name]
                            else:
                                detections[file["sha256"]] = {
                                    'package': package.name,
                                    'known_bad': results_pkg[package.name]
                                }
            if detections != {}:
                json_path = os.path.join(storage_folder, "detections.json")
                with open(json_path, "w") as handle:
                    json.dump(detections, handle, indent=4)
    except KeyboardInterrupt:
        print("")
        sys.exit(-1)


if __name__ == "__main__":
    main()
