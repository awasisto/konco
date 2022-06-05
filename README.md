konco - kontes (contest) companion
==================================

An N1MM companion program for creating QSL cards automatically.

Requirements
------------
 - Python 3
 - N1MM

Running
-------

1. Run N1MM
2. Configure N1MM to broadcast contact data
3. Modify `config.conf`
4. Create Python virtual environment (recommended)

       python -m venv venv
       venv\Scripts\activate # Windows
       source venv/bin/activate # Linux

5. Install dependencies

       pip install -r requirements.txt

6. Run konco

       python konco.py config.conf

License
-------

    Copyright (C) 2022 Andika Wasisto
    
    konco is free software: you can redistribute it and/or modify it under the
    terms of the GNU Affero General Public License as published by the Free
    Software Foundation, either version 3 of the License, or (at your option)
    any later version.
    
    konco is distributed in the hope that it will be useful, but WITHOUT ANY
    WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
    FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for
    more details.
    
    You should have received a copy of the GNU Affero General Public License
    along with konco.  If not, see <https://www.gnu.org/licenses/>.
