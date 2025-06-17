# LVMeteo

A Python library for accessing meteorological and hydrological data from the Latvian open data portal (data.gov.lv).

## Description

This library provides  access to hydrometeorological data by [Latvian Environment, Geology and Meteorology Centre](https://videscentrs.lvgmc.lv/) from Latvia's official open data portal (https://data.gov.lv/dati/eng/dataset/hidrometeorologiskie-noverojumi). It allows you to retrieve:

- Meteorological operational data
- Meteorological archive data (actual and statistical)  
- Hydrological operational and archive data
- Weather phenomena data
- Station information and parameters

## Installation

### Install from source (development):

```bash
pip install -e .
```

### Install from distribution:

First, create a distribution package:

```bash
python setup.py sdist
```

This creates a `dist/lvmeteo-0.1.0.tar.gz` file. Install it with:

```bash
pip install dist/lvmeteo-0.1.0.tar.gz
```

## Quick Start

```python
import datetime
from lvmeteo.meteodata import get_lv_meteo_data, lv_meteo_tables

# Get temperature data 
parameters = ['HTDRY', 'HATMN', 'HATMX']  # Temperature parameters
stations = ['RIGASLU', 'RIDM99MS', 'RILP99PA']  
enddate = datetime.datetime.now()
startdate = enddate - datetime.timedelta(days=30)

df = get_lv_meteo_data(
    lv_meteo_tables.meteo_archive_avg.table_name,
    stations, 
    parameters,
    startdate, 
    enddate
)

print(df)
```

## Available Data Tables

- **meteo_operational**: Real-time meteorological data (meteo_operativie)
- **meteo_archive**: Historical meteorological data - actual values (meteo_arhivs)
- **meteo_archive_avg**: Historical meteorological data - averages, min, max (meteo_arhivs_avg)
- **hydro_operational**: Real-time hydrological data (hidro_operative)
- **hydro_archive**: Historical hydrological data (hidro_arhivs)
- **weather_phenomena_operational**: Real-time weather phenomena (paradibas_operative)
- **weather_phenomena_archive**: Historical weather phenomena (paradibas_arhivs)

## Main Functions

### `get_lv_meteo_data(table, stations, parameters, startdate, enddate)`

Retrieve meteorological data for specified stations and parameters.

**Parameters:**
- `table`: Table identifier from `lv_meteo_tables`
- `stations`: List of station IDs or single station ID
- `parameters`: List of parameter codes or single parameter code
- `startdate`: Start date (datetime object)
- `enddate`: End date (datetime object)

### `get_lv_meteo_stations()`

Get list of all meteorological stations with their metadata.

### `get_lv_hidro_stations()`

Get list of all hydrological stations with their metadata.

### `get_lv_meteo_params()`

Get list of all available meteorological parameters.

### `get_lv_hidro_params()`

Get list of all available hydrological parameters.

### Configuration

All configuration constants are available in `lvmeteo.config`:

- `API_BASE_URL` - Base URL for the data API
- `METEO_TABLES` - Class with available meteorological tables as attributes
- `RESOURCE_URLS` - Class with resource identifiers for all data tables as attributes
- `STATION_COLUMNS` - Column mappings for station data
- `DATA_COLUMNS` - Column mappings for meteorological data
- `PARAM_COLUMNS` - Column mappings for parameter metadata

Access table information using class attributes:
```python
from lvmeteo.config import METEO_TABLES, RESOURCE_URLS

# Access table name and description
table_name = METEO_TABLES.meteo_archive_avg.table_name
table_description = METEO_TABLES.meteo_archive_avg.name

# Access resource URLs
resource_id = RESOURCE_URLS.meteo_operational
```

## Examples

See the `examples/` directory for comprehensive usage examples:

- `basic_usage.py` - Complete demonstration of all library features

## Error Handling

The library provides custom exceptions for better error handling:

- `APIError` - API request failures
- `DataNotFoundError` - No data found for query
- `ValidationError` - Invalid input parameters


## Requirements

- Python >= 3.7
- pandas >= 1.0.0
- requests >= 2.20.0

## License

This project is licensed under the MIT License.

## Data Source

Data is provided by the Latvian Environment, Geology and Meteorology Centre through the official open data portal at data.gov.lv.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.