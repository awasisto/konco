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

import socket
import traceback
from datetime import datetime

import xmltodict

from model import Contact


class ContactSource:

    def __init__(self, on_contact_received):
        self.on_contact_received = on_contact_received

    def start(self):
        pass

    def stop(self):
        pass


class N1mmBroadcastContactSource(ContactSource):

    def __init__(self, on_contact_received, listen_address: str, listen_port: int, n1mm_address: str):
        super().__init__(on_contact_received)
        self.listen_address = listen_address
        self.listen_port = listen_port
        self.n1mm_address = n1mm_address
        self.running = False

    def start(self):
        if not self.running:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((self.listen_address, self.listen_port))

            self.running = True

            while True:
                try:
                    n1mm_data, addr = sock.recvfrom(65535)

                    if addr[0] == self.n1mm_address:
                        n1mm_contact = xmltodict.parse(n1mm_data.decode('utf-8'))['contactinfo']

                        datetime_utc = datetime.strptime(n1mm_contact['timestamp'], '%Y-%m-%d %H:%M:%S')
                        callsign = n1mm_contact['call']
                        frequency_mhz = float(n1mm_contact['rxfreq']) / 10000.0
                        mode = n1mm_contact['mode']
                        rst = n1mm_contact['rcv']

                        contact = Contact(
                            datetime_utc,
                            callsign,
                            frequency_mhz,
                            mode,
                            rst,
                        )

                        if self.on_contact_received is not None and self.running:
                            self.on_contact_received(contact)
                except:
                    traceback.print_exc()

    def stop(self):
        self.running = False
