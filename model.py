# Copyright (C) 2022 Andika Wasisto
#
# konco is free software: you can redistribute it and/or modify it under the
# terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# konco is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for
# more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with konco.  If not, see <https://www.gnu.org/licenses/>.

from datetime import datetime


class Contact:

    def __init__(
            self,
            datetime_utc: datetime,
            callsign: str,
            frequency_mhz: float,
            mode: str,
            rst: str,
    ):
        self.datetime_utc = datetime_utc
        self.callsign = callsign
        self.frequency_mhz = frequency_mhz
        self.mode = mode
        self.rst = rst
