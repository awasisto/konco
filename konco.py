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

import configparser
import sys
import threading

from contact_source import N1mmBroadcastContactSource
from operator_name_source import SdppiOperatorNameSource
from qsl_card_generator import QslCardGenerator


config = configparser.RawConfigParser(inline_comment_prefixes=';')
config.read(sys.argv[1])


def config_get_int_or_default(section: configparser.SectionProxy, option: str, default: int) -> int:
    try:
        return int(section[option])
    except ValueError:
        return default


template_file_path = config['qsl_card']['template_file_path']

output_folder_path = config['qsl_card']['output_folder_path']

utc_date_text_config = QslCardGenerator.TextConfig(
    config_get_int_or_default(config['qsl_card'], 'utc_date_x', -1),
    config_get_int_or_default(config['qsl_card'], 'utc_date_y', -1),
    config['qsl_card']['utc_date_vertical_alignment'],
    config['qsl_card']['utc_date_horizontal_alignment'],
    config['qsl_card']['utc_date_font_path'],
    config_get_int_or_default(config['qsl_card'], 'utc_date_font_size', -1),
    config['qsl_card']['utc_date_font_color'],
)

utc_date_format = config['qsl_card']['utc_date_format']

utc_day_text_config = QslCardGenerator.TextConfig(
    config_get_int_or_default(config['qsl_card'], 'utc_day_x', -1),
    config_get_int_or_default(config['qsl_card'], 'utc_day_y', -1),
    config['qsl_card']['utc_day_vertical_alignment'],
    config['qsl_card']['utc_day_horizontal_alignment'],
    config['qsl_card']['utc_day_font_path'],
    config_get_int_or_default(config['qsl_card'], 'utc_day_font_size', -1),
    config['qsl_card']['utc_day_font_color'],
)

utc_month_text_config = QslCardGenerator.TextConfig(
    config_get_int_or_default(config['qsl_card'], 'utc_month_x', -1),
    config_get_int_or_default(config['qsl_card'], 'utc_month_y', -1),
    config['qsl_card']['utc_month_vertical_alignment'],
    config['qsl_card']['utc_month_horizontal_alignment'],
    config['qsl_card']['utc_month_font_path'],
    config_get_int_or_default(config['qsl_card'], 'utc_month_font_size', -1),
    config['qsl_card']['utc_month_font_color'],
)

utc_year_text_config = QslCardGenerator.TextConfig(
    config_get_int_or_default(config['qsl_card'], 'utc_year_x', -1),
    config_get_int_or_default(config['qsl_card'], 'utc_year_y', -1),
    config['qsl_card']['utc_year_vertical_alignment'],
    config['qsl_card']['utc_year_horizontal_alignment'],
    config['qsl_card']['utc_year_font_path'],
    config_get_int_or_default(config['qsl_card'], 'utc_year_font_size', -1),
    config['qsl_card']['utc_year_font_color'],
)

utc_time_text_config = QslCardGenerator.TextConfig(
    config_get_int_or_default(config['qsl_card'], 'utc_time_x', -1),
    config_get_int_or_default(config['qsl_card'], 'utc_time_y', -1),
    config['qsl_card']['utc_time_vertical_alignment'],
    config['qsl_card']['utc_time_horizontal_alignment'],
    config['qsl_card']['utc_time_font_path'],
    config_get_int_or_default(config['qsl_card'], 'utc_time_font_size', -1),
    config['qsl_card']['utc_time_font_color'],
)

utc_time_format = config['qsl_card']['utc_time_format']

callsign_text_config = QslCardGenerator.TextConfig(
    config_get_int_or_default(config['qsl_card'], 'callsign_x', -1),
    config_get_int_or_default(config['qsl_card'], 'callsign_y', -1),
    config['qsl_card']['callsign_vertical_alignment'],
    config['qsl_card']['callsign_horizontal_alignment'],
    config['qsl_card']['callsign_font_path'],
    config_get_int_or_default(config['qsl_card'], 'callsign_font_size', -1),
    config['qsl_card']['callsign_font_color'],
)

frequency_mhz_text_config = QslCardGenerator.TextConfig(
    config_get_int_or_default(config['qsl_card'], 'frequency_mhz_x', -1),
    config_get_int_or_default(config['qsl_card'], 'frequency_mhz_y', -1),
    config['qsl_card']['frequency_mhz_vertical_alignment'],
    config['qsl_card']['frequency_mhz_horizontal_alignment'],
    config['qsl_card']['frequency_mhz_font_path'],
    config_get_int_or_default(config['qsl_card'], 'frequency_mhz_font_size', -1),
    config['qsl_card']['frequency_mhz_font_color'],
)

frequency_mhz_fractional_digits = config_get_int_or_default(config['qsl_card'], 'frequency_mhz_fractional_digits', -1)

mode_text_config = QslCardGenerator.TextConfig(
    config_get_int_or_default(config['qsl_card'], 'mode_x', -1),
    config_get_int_or_default(config['qsl_card'], 'mode_y', -1),
    config['qsl_card']['mode_vertical_alignment'],
    config['qsl_card']['mode_horizontal_alignment'],
    config['qsl_card']['mode_font_path'],
    config_get_int_or_default(config['qsl_card'], 'mode_font_size', -1),
    config['qsl_card']['mode_font_color'],
)

rst_text_config = QslCardGenerator.TextConfig(
    config_get_int_or_default(config['qsl_card'], 'rst_x', -1),
    config_get_int_or_default(config['qsl_card'], 'rst_y', -1),
    config['qsl_card']['rst_vertical_alignment'],
    config['qsl_card']['rst_horizontal_alignment'],
    config['qsl_card']['rst_font_path'],
    config_get_int_or_default(config['qsl_card'], 'rst_font_size', -1),
    config['qsl_card']['rst_font_color'],
)

operator_name_text_config = QslCardGenerator.TextConfig(
    config_get_int_or_default(config['qsl_card'], 'operator_name_x', -1),
    config_get_int_or_default(config['qsl_card'], 'operator_name_y', -1),
    config['qsl_card']['operator_name_vertical_alignment'],
    config['qsl_card']['operator_name_horizontal_alignment'],
    config['qsl_card']['operator_name_font_path'],
    config_get_int_or_default(config['qsl_card'], 'operator_name_font_size', -1),
    config['qsl_card']['operator_name_font_color'],
)

operator_name_case = config['qsl_card']['operator_name_case'].lower()

qsl_card_generator = QslCardGenerator(
    template_file_path,
    output_folder_path,
    utc_date_text_config,
    utc_date_format,
    utc_day_text_config,
    utc_month_text_config,
    utc_year_text_config,
    utc_time_text_config,
    utc_time_format,
    callsign_text_config,
    frequency_mhz_text_config,
    frequency_mhz_fractional_digits,
    mode_text_config,
    rst_text_config,
    operator_name_text_config,
    operator_name_case,
    SdppiOperatorNameSource(),
)

contact_source = N1mmBroadcastContactSource(
    on_contact_received=lambda contact: threading.Thread(target=qsl_card_generator.generate, args=[contact]).start(),
    listen_address=config['n1mm']['listen_address'],
    listen_port=config['n1mm'].getint('listen_port'),
    n1mm_address=config['n1mm']['n1mm_address'],
)

try:
    contact_source.start()
finally:
    contact_source.stop()