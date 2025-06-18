"""
Configuration constants for LVMeteo library.
"""

from typing import Dict

# API Configuration
API_BASE_URL: str = 'https://data.gov.lv/dati/api/3/action/datastore_search_sql'
DEFAULT_TIMEOUT: int = 30
DEFAULT_CURL_PATH: str = 'curl'


class RESOURCE_URLS:
    meteo_operational = '17460efb-ae99-4d1d-8144-1068f184b05f'  # meteo_operativie
    meteo_archive = '339f73e4-20cf-4cea-be65-dcfd4b3b742c'  # meteo_arhivs
    meteo_archive_avg = 'ecc62e27-2071-483c-bca9-5e53d979faa8'  # meteo_arhivs_avg
    hydro_operational = 'de5f06e9-6f44-497d-8ec2-72a2483608e8'  # hidro_operative
    hydro_archive = 'a90de53b-e8b6-4cda-97c4-ecb86fbafc2d'  # hidro_arhivs
    weather_phenomena_operational = '77da5b2b-ebe2-4b94-963d-8a92364a3937'  # paradibas_operative
    weather_phenomena_archive = '05b4dc26-016c-478a-a5e1-afa74bd83c06'  # paradibas_arhivs
    meteo_stations = 'c32c7afd-0d05-44fd-8b24-1de85b4bf11d'
    hydro_stations = '93fd5e2c-20c4-496e-a920-ff29bda20383'  # hidro_stations
    meteo_params = '38b462ac-08b9-4168-9d6e-cbaedc2e775d'
    hydro_params = '714ab60d-d93e-4403-b76d-2fb865d15d63'  # hidro_params


class MeteoTable:
    def __init__(self, name: str, table_name: str):
        self.name = name
        self.table_name = table_name


class METEO_TABLES:
    meteo_operational = MeteoTable('Meteoroloģiskie operatīvie dati', RESOURCE_URLS.meteo_operational)  # meteo_operativie
    meteo_archive = MeteoTable('Meteoroloģiskie arhīva dati (Faktiskie)', RESOURCE_URLS.meteo_archive)  # meteo_arhivs
    meteo_archive_avg = MeteoTable('Meteoroloģiskie arhīva dati (AVG, MIN, MAX)', RESOURCE_URLS.meteo_archive_avg)  # meteo_arhivs_avg
    hydro_operational = MeteoTable('Hidroloģiskie operatīvie dati', RESOURCE_URLS.hydro_operational)  # hidro_operative
    hydro_archive = MeteoTable('Hidroloģiskie operatīvie dati', RESOURCE_URLS.hydro_archive)  # hidro_arhivs
    weather_phenomena_operational = MeteoTable('Laika parādību operatīvie dati', RESOURCE_URLS.weather_phenomena_operational)  # paradibas_operative
    weather_phenomena_archive = MeteoTable('Laika parādību arhīva dati', RESOURCE_URLS.weather_phenomena_archive)  # paradibas_arhivs


# Column mapping for station data
STATION_COLUMNS: Dict[str, str] = {
    'station_id': 'STATION_ID',
    'name': 'NAME',
    'WMO_id': 'WMO_ID',
    'begin_date': 'BEGIN_DATE',
    'end_date': 'END_DATE',
    'longitude': 'GEOGR1',
    'latitude': 'GEOGR2',
    'elevation': 'ELEVATION',
    'elevation_pressure': 'ELEVATION_PRESSURE'
}

# Column mapping for meteorological data
DATA_COLUMNS: Dict[str, str] = {
    'station_id': 'STATION_ID',
    'param': 'ABBREVIATION',
    'date': 'DATETIME',
    'value': 'VALUE'
}

# Column mapping for parameter metadata
PARAM_COLUMNS: Dict[str, str] = {
    'param_id': 'ABBREVIATION',
    'description_EN': 'EN_DESCRIPTION',
    'description_LV': 'LV_DESCRIPTION',
    'scale': 'SCALE',
    'lower_limit': 'LOWER_LIMIT',
    'upper_limit': 'UPPER_LIMIT',
    'unit': 'MEASUREMENT_UNIT'
}
