import os
import sys
import argparse
import datetime

from .ui import info, logo
from .acquisition import Acquisition
from .virustotal import virustotal_lookup
from .koodous import koodous_lookup

def main():
    parser = argparse.ArgumentParser(description="Extract information from Android device")
    parser.add_argument("--storage", default=os.getcwd(), help="Specify a different base folder to store the acquisition")
    parser.add_argument("--virustotal", default=None, help="Check packages on VirusTotal and specify API key")
    parser.add_argument("--virustotal-rate", default=4, help="Set the number of requests to VirusTotal per minute according to your account's quota")
    parser.add_argument("--koodous", action="store_true", help="Check packages on Koodous.com")
    parser.add_argument("--all", action="store_true", help="Run all available checks")
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

        if args.virustotal or args.all:
            virustotal_lookup(args.virustotal, args.virustotal_rate, acq.packages)

        if args.koodous or args.all:
            koodous_lookup(acq.packages)
    except KeyboardInterrupt:
        print("")
        sys.exit(-1)

if __name__ == "__main__":
    main()
