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
from setuptools import setup

description = "Extract all apks from an Android device and check for malicious apps"

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as handle:
    long_description = handle.read()

requires = (
    "rsa",
    "tqdm",
    "halo",
    "requests",
    "terminaltables",
    "adb",
)

setup(
    name="snoopdroid",
    version="1.4",
    author="Claudio Guarnieri",
    author_email="nex@nex.sx",
    description=description,
    long_description=long_description,

    scripts=["bin/snoopdroid",],
    install_requires=requires,
    packages=["snoopdroid",],
    
    zip_safe=False,

    keywords="security android",
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Security",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: Android",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Environment :: Console",
    ],
)
