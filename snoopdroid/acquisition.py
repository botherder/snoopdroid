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
import shutil
from usb1 import USBErrorBusy

from adb import adb_commands
from adb import sign_m2crypto

from snoopdroid.ui import PullProgress, info, highlight
from snoopdroid.utils import get_sha256

class Package(object):
    def __init__(self, name, files=None):
        self.name = name
        self.files = files or []

class Acquisition(object):
    def __init__(self, storage_folder=None):
        self.device = None
        self.packages = []
        self.storage_folder = storage_folder

    def __clean_output(self, output):
        return output.strip().replace("package:", "")

    def connect(self):
        signer = sign_m2crypto.M2CryptoSigner(os.path.expanduser('~/.android/adbkey'))
        self.device = adb_commands.AdbCommands()

        try:
            self.device.ConnectDevice(rsa_keys=[signer])
        except USBErrorBusy:
            print("ERROR: device is busy, maybe run `adb kill-server` and try again.")
            sys.exit(-1)
        except TypeError:
            print("ERROR: you might not have adb keys yet. Try to launch `adb devices` first.")
            sys.exit(-1)

    def disconnect(self):
        self.device.Close()

    def reconnect(self):
        print(info("Reconnecting ..."))
        self.disconnect()
        self.connect()

    def get_packages(self):
        print(info("Retrieving package names ..."))

        output = self.device.Shell("pm list packages")
        for line in output.split("\n"):
            package_name = self.__clean_output(line)
            if package_name == "":
                continue

            if package_name not in self.packages:
                self.packages.append(Package(package_name))

        print(info("There are {} packages installed on the device.".format(len(self.packages))))
        print("")

    def pull_packages(self):
        print(info("Downloading packages from device. This might take some time ..."))
        print("")

        storage_folder_apk = os.path.join(self.storage_folder, "apks")
        if not os.path.exists(storage_folder_apk):
            os.mkdir(storage_folder_apk)

        total_packages = len(self.packages)
        counter = 0
        for package in self.packages:
            counter += 1
            print("[{}/{}] Package: {}".format(counter, total_packages, highlight(package.name)))

            try:
                output = self.device.Shell("pm path {}".format(package.name))
                output = self.__clean_output(output)
                if not output:
                    continue
            except Exception as e:
                print("ERROR: Failed to get path of package {}: {}".format(package.name, e))
                self.reconnect()
                continue

            # Sometimes the package path contains multiple lines for multiple apks.
            # We loop through each line and download each file.
            for path in output.split("\n"):
                path = path.strip()
                print("Downloading {} ...".format(path))

                try:
                    with PullProgress(unit='B', unit_divisor=1024, unit_scale=True, miniters=1) as pp:
                        data = self.device.Pull(path, progress_callback=pp.update_to)
                except Exception as e:
                    print("ERROR: Failed to pull package file from {}: {}".format(path, e))
                    self.reconnect()
                    continue

                # We try to extract the apk name for this package.
                file_name = ""
                if "==/" in path:
                    file_name = "_" + path.split("==/")[1].replace(".apk", "")

                # We store the apk to disk.
                file_path = os.path.join(storage_folder_apk, "{}{}.apk".format(package.name, file_name))
                with open(file_path, "wb") as handle:
                    handle.write(data)

                # We add the apk metadata to the package object.
                package.files.append({
                    "path": path,
                    "stored_path": file_path,
                    "sha256": get_sha256(file_path),
                })

            print("")

    def run(self):
        self.connect()

        self.get_packages()
        self.pull_packages()

        self.disconnect()
