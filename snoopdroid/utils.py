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

import hashlib
 
def get_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path,"rb") as handle:
        for byte_block in iter(lambda: handle.read(4096), b""):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()
