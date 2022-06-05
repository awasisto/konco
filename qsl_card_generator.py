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

import os

from PIL import Image, ImageDraw, ImageFont

from model import Contact
from operator_name_source import OperatorNameSource


class QslCardGenerator:

    class TextConfig:

        def __init__(
                self,
                x: int,
                y: int,
                vertical_alignment: str,
                horizontal_alignment: str,
                font_path: str,
                font_size: int,
                font_color: str,
        ):
            self.x = x
            self.y = y
            self.vertical_alignment = vertical_alignment
            self.horizontal_alignment = horizontal_alignment
            self.font_path = font_path
            self.font_size = font_size
            self.font_color = font_color

        def is_valid(self):
            return self.x is not None and self.x >= 0 and \
                   self.y is not None and self.y >= 0 and \
                   self.vertical_alignment is not None and self.vertical_alignment in ('top', 'center', 'bottom') and \
                   self.horizontal_alignment is not None and self.horizontal_alignment in ('left', 'center', 'right') and \
                   self.font_path is not None and self.font_path != '' and \
                   self.font_size is not None and self.font_size >= 0 and \
                   self.font_color is not None and self.font_color != ''

    def __init__(
            self,
            template_file_path: str,
            output_folder_path: str,
            utc_date_text_config: TextConfig,
            utc_date_format: str,
            utc_day_text_config: TextConfig,
            utc_month_text_config: TextConfig,
            utc_year_text_config: TextConfig,
            utc_time_text_config: TextConfig,
            utc_time_format: str,
            callsign_text_config: TextConfig,
            frequency_mhz_text_config: TextConfig,
            frequency_mhz_fractional_digits: int,
            mode_text_config: TextConfig,
            rst_text_config: TextConfig,
            operator_name_text_config: TextConfig,
            operator_name_case: str,
            operator_name_source: OperatorNameSource,
    ):
        self.template_file_path = template_file_path
        self.output_folder_path = output_folder_path
        self.utc_date_text_config = utc_date_text_config
        self.utc_date_format = utc_date_format
        self.utc_day_text_config = utc_day_text_config
        self.utc_month_text_config = utc_month_text_config
        self.utc_year_text_config = utc_year_text_config
        self.utc_time_text_config = utc_time_text_config
        self.utc_time_format = utc_time_format
        self.callsign_text_config = callsign_text_config
        self.frequency_mhz_text_config = frequency_mhz_text_config
        self.frequency_mhz_fractional_digits = frequency_mhz_fractional_digits
        self.mode_text_config = mode_text_config
        self.rst_text_config = rst_text_config
        self.operator_name_text_config = operator_name_text_config
        self.operator_name_case = operator_name_case
        self.operator_name_source = operator_name_source

    def generate(self, contact: Contact):
        image = Image.open(self.template_file_path).convert('RGB')

        if self.utc_date_text_config.is_valid() and self.utc_date_format != '':
            text = contact.datetime_utc.strftime(self.utc_date_format)
            QslCardGenerator._draw(image, text, self.utc_date_text_config)

        if self.utc_day_text_config.is_valid():
            text = str(contact.datetime_utc.day)
            QslCardGenerator._draw(image, text, self.utc_day_text_config)

        if self.utc_month_text_config.is_valid():
            text = str(contact.datetime_utc.month)
            QslCardGenerator._draw(image, text, self.utc_month_text_config)

        if self.utc_year_text_config.is_valid():
            text = str(contact.datetime_utc.year)
            QslCardGenerator._draw(image, text, self.utc_year_text_config)

        if self.utc_time_text_config.is_valid():
            text = contact.datetime_utc.strftime(self.utc_time_format)
            QslCardGenerator._draw(image, text, self.utc_time_text_config)

        if self.callsign_text_config.is_valid():
            text = contact.callsign.replace('0', u'\u00d8')
            QslCardGenerator._draw(image, text, self.callsign_text_config)

        if self.frequency_mhz_text_config.is_valid() and self.frequency_mhz_fractional_digits > 0:
            text = f'{contact.frequency_mhz:.{self.frequency_mhz_fractional_digits}f}'
            QslCardGenerator._draw(image, text, self.frequency_mhz_text_config)

        if self.mode_text_config.is_valid():
            text = contact.mode
            QslCardGenerator._draw(image, text, self.mode_text_config)

        if self.rst_text_config.is_valid():
            text = contact.rst
            QslCardGenerator._draw(image, text, self.rst_text_config)

        if self.operator_name_text_config.is_valid() and self.operator_name_case in ('upper', 'title'):
            operator_name = self.operator_name_source.lookup(contact.callsign)
            text = ''
            if self.operator_name_case == 'upper':
                text = operator_name.upper()
            elif self.operator_name_case == 'title':
                text = operator_name.title()
            QslCardGenerator._draw(image, text, self.operator_name_text_config)

        if not os.path.exists(self.output_folder_path):
            os.makedirs(self.output_folder_path)

        output_file_path = f'{self.output_folder_path}/{contact.callsign}_{contact.datetime_utc.strftime("%Y%m%d%H%M%S")}.png'

        image.save(output_file_path)

    @staticmethod
    def _draw(image: Image, text: str, text_config: TextConfig):
        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype(text_config.font_path, size=text_config.font_size)

        text_width, text_height = draw.textsize(text, font=font)

        x: int
        y: int

        if text_config.horizontal_alignment == 'left':
            x = text_config.x
        elif text_config.horizontal_alignment == 'center':
            x = text_config.x - text_width / 2
        elif text_config.horizontal_alignment == 'right':
            x = text_config.x - text_width
        else:
            return

        if text_config.vertical_alignment == 'top':
            y = text_config.y
        elif text_config.vertical_alignment == 'center':
            y = text_config.y - text_height / 2
        elif text_config.vertical_alignment == 'bottom':
            y = text_config.y - text_height
        else:
            return

        draw.text((x, y), text, fill=text_config.font_color, font=font)
