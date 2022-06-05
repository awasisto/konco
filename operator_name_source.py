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

import time
import traceback

import requests
from bs4 import BeautifulSoup


class OperatorNameSource:

    def lookup(self, callsign: str) -> str:
        pass


class SdppiOperatorNameSource(OperatorNameSource):

    def lookup(self, callsign: str) -> str:
        name = ''
        while name == '':
            try:
                response = requests.get(f'https://iar-ikrap.postel.go.id/registrant/searchDataIar/?callsign={callsign}', timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.json(), 'html.parser')
                    name = soup.select_one('div:nth-child(2)').text
                else:
                    print(f'{callsign} - status code: {response.status_code}')
                    time.sleep(10)
            except:
                traceback.print_exc()
                time.sleep(10)
        return name
