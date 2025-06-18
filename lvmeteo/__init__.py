"""
LVMeteo - A Python library for accessing Latvian meteorological data from data.gov.lv

This library provides easy access to meteorological and hydrological data
from the Latvian open data portal.
"""

from .meteodata import (
    lv_meteo_tables,
    get_lv_meteo_data,
    get_lv_meteo_stations,
    get_lv_hidro_stations,
    get_lv_meteo_params,
    get_lv_hidro_params,
    get_fromsql
)
from .exceptions import (
    LVMeteoError,
    APIError,
    DataNotFoundError,
    ValidationError,
    ConfigurationError
)
from .config import (
    METEO_TABLES,
    RESOURCE_URLS,
    STATION_COLUMNS,
    DATA_COLUMNS,
    PARAM_COLUMNS
)

__version__ = "0.1.0"
__author__ = "Juris Seņņikovs"
__email__ = ""
__description__ = "A Python library for accessing Latvian meteorological data from Latvia's Open Data portal"

__all__ = [
    'lv_meteo_tables',
    'get_lv_meteo_data',
    'get_lv_meteo_stations',
    'get_lv_hidro_stations',
    'get_lv_meteo_params',
    'get_lv_hidro_params',
    'get_fromsql',
    'LVMeteoError',
    'APIError',
    'DataNotFoundError',
    'ValidationError',
    'ConfigurationError',
    'METEO_TABLES',
    'RESOURCE_URLS',
    'STATION_COLUMNS',
    'DATA_COLUMNS',
    'PARAM_COLUMNS'
]
