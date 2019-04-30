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

import os
import sys
import argparse
import datetime

from ui import info, logo
from acquisition import Acquisition
from virustotal import virustotal_lookup

def main():
    parser = argparse.ArgumentParser(description="Extract information from Android device")
    parser.add_argument("--storage", default=os.getcwd(), help="Specify a different base folder to store the acquisition")
    parser.add_argument("--virustotal", default=None, help="Check packages on VirusTotal and specify API key")
    parser.add_argument("--virustotal-rate", default=4, help="Set the number of requests to VirusTotal per minute according to your account's quota")
    args = parser.parse_args()

    # TODO: Need to come up with a better folder name.
    acq_folder = datetime.datetime.now().isoformat().split(".")[0].replace(":", "")
    storage_folder = os.path.join(args.storage, acq_folder)

    if not os.path.exists(storage_folder):
        os.mkdir(storage_folder)

    logo()

    print(info("Starting acquisition at folder {}\n".format(storage_folder)))

    try:
        acq = Acquisition(storage_folder)
        acq.run()

        if args.virustotal:
            virustotal_lookup(args.virustotal, args.virustotal_rate, acq.packages)
    except KeyboardInterrupt:
        sys.exit(-1)

if __name__ == "__main__":
    main()
