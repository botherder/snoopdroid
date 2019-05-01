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

from tqdm import tqdm
from colorama import init
from termcolor import colored

def logo():
    print("                                   _           _     _      ")
    print("                                  | |         (_)   | |     ")
    print("   ___ _ __   ___   ___  _ __   __| |_ __ ___  _  __| |     ")
    print("  / __| '_ \\ / _ \\ / _ \\| '_ \\ / _` | '__/ _ \\| |/ _` |")
    print("  \\__ \\ | | | (_) | (_) | |_) | (_| | | | (_) | | (_| |   ")
    print("  |___/_| |_|\\___/ \\___/| .__/ \\__,_|_|  \\___/|_|\\__,_|")
    print("                        | |                                 ")
    print("                        |_|                                 ")
    print("                                                            ")


class PullProgress(tqdm):
    def update_to(self, file_name, current, total):
        if total is not None:
            self.total = total
        self.update(current - self.n)

init(autoreset=True)

def info(text):
    return colored("***", "cyan", attrs=["bold",]) + " " + text

def error(text):
    return colored("!!!", "red", attrs=["bold",]) + " Error: " + text

def highlight(text):
    return colored(text, "cyan", attrs=["bold",])

def green(text):
    return colored(text, "green", attrs=["bold",])

def red(text):
    return colored(text, "red", attrs=["bold",])
