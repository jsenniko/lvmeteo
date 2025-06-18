import datetime
import subprocess
from typing import Union, List, Dict, Any, Optional
import warnings
import logging
import pandas as pd
try:
    from .exceptions import APIError, DataNotFoundError, ValidationError
    from .config import (
        API_BASE_URL,
        DEFAULT_TIMEOUT,
        METEO_TABLES,
        RESOURCE_URLS,
        STATION_COLUMNS,
        DATA_COLUMNS,
        PARAM_COLUMNS
    )
except ImportError:
    from exceptions import APIError, DataNotFoundError, ValidationError
    from config import (
        API_BASE_URL,
        DEFAULT_TIMEOUT,
        METEO_TABLES,
        RESOURCE_URLS,
        STATION_COLUMNS,
        DATA_COLUMNS,
        PARAM_COLUMNS
    )

warnings.filterwarnings('ignore')

# Configure logging
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# Expose config constants for backward compatibility
base_url = API_BASE_URL
lv_meteo_tables = METEO_TABLES
station_dict = STATION_COLUMNS
data_dict = DATA_COLUMNS
param_dict = PARAM_COLUMNS


def create_lv_meteo_data_sql(
    table: str,
    stations: Union[str, List[str]],
    parameters: Union[str, List[str]],
    startdate: datetime.datetime,
    enddate: datetime.datetime
) -> str:
    """
    Create SQL query for retrieving meteorological data.

    Args:
        table: Table identifier from lv_meteo_tables
        stations: Station ID(s) to retrieve data for
        parameters: Parameter code(s) to retrieve
        startdate: Start date for data retrieval
        enddate: End date for data retrieval

    Returns:
        SQL query string

    Raises:
        ValidationError: If input parameters are invalid
    """
    # Input validation
    if not table:
        raise ValidationError("Table name cannot be empty")
    if not stations:
        raise ValidationError("Stations list cannot be empty")
    if not parameters:
        raise ValidationError("Parameters list cannot be empty")
    if not isinstance(startdate, datetime.datetime):
        raise ValidationError("Start date must be a datetime object")
    if not isinstance(enddate, datetime.datetime):
        raise ValidationError("End date must be a datetime object")
    if startdate >= enddate:
        raise ValidationError("Start date must be before end date")

    base_sql = """SELECT * from "{table}" WHERE "STATION_ID" in ({station_list}) and "ABBREVIATION" in ({parameter_list}) and "DATETIME" BETWEEN '{startdate}' and '{enddate}'"""

    # Normalize inputs to lists
    if not hasattr(parameters, '__iter__') or isinstance(parameters, (str, bytes)):
        parameters = [parameters]
    if not hasattr(stations, '__iter__') or isinstance(stations, (str, bytes)):
        stations = [stations]

    parameter_list = ",".join(map(lambda x: f"'{x}'", parameters))
    station_list = ",".join(map(lambda x: f"'{x}'", stations))

    sql = base_sql.format(
        table=table,
        parameter_list=parameter_list,
        station_list=station_list,
        startdate=startdate.isoformat(),
        enddate=enddate.isoformat()
    )

    logger.debug(f"Generated SQL query: {sql}")
    return sql


def get_response_from_lv_data(
    sql: str,
    use_curl: bool = False,
    curlExePath: str = 'curl'
) -> Dict[str, Any]:
    """
    Execute SQL query against LV open data API.

    Args:
        sql: SQL query to execute
        use_curl: Use curl instead of requests library
        curlExePath: Path to curl executable

    Returns:
        JSON response from API as dictionary

    Raises:
        ValidationError: If SQL query is empty
        APIError: If API request fails
    """
    if not sql:
        raise ValidationError("SQL query cannot be empty")

    logger.info(sql)

    try:
        if use_curl:
            options = [f'{curlExePath}', '-G',
                       '--data-urlencode', f"sql={sql}", API_BASE_URL]
            logger.debug(f"Using curl with options: {options}")
            rOutput = subprocess.check_output(
                options, shell=False, timeout=400, text=True)
            import json
            data = json.loads(rOutput)
            return data
        else:
            import requests
            logger.debug(f"Making request to {API_BASE_URL}")
            response = requests.get(API_BASE_URL, params=dict(
                sql=sql), timeout=DEFAULT_TIMEOUT)

            if response.ok:
                data = response.json()
                logger.debug("API request successful")
                return data
            else:
                error_msg = f"API request failed with status {response.status_code}: {response.text}"
                logger.error(error_msg)
                raise APIError(error_msg)

    except subprocess.TimeoutExpired as e:
        error_msg = f"Request timed out: {e}"
        logger.error(error_msg)
        raise APIError(error_msg) from e
    except subprocess.CalledProcessError as e:
        error_msg = f"Curl command failed: {e}"
        logger.error(error_msg)
        raise APIError(error_msg) from e
    except Exception as e:
        error_msg = f"Unexpected error during API request: {e}"
        logger.error(error_msg)
        raise APIError(error_msg) from e


def records_to_dataframe_raw(
    fields: List[Dict[str, Any]],
    records: List[Dict[str, Any]],
    columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Convert raw API records to pandas DataFrame with proper data types.

    Args:
        fields: Field metadata from API response
        records: Data records from API response
        columns: Optional list of columns to include

    Returns:
        DataFrame with properly typed columns
    """
    field_dict = {v['id']: v['type'] for v in fields}
    if columns is not None:
        df = pd.DataFrame([{k: v.get(k) for k in columns} for v in records])
    else:
        df = pd.DataFrame(records)
    for c in df.columns:
        vtype = field_dict.get(c, 'text')
        if vtype == 'text':
            df[c] = df[c].astype('str')
        elif vtype == 'numeric':
            df[c] = pd.to_numeric(df[c], errors='coerce')
        elif vtype == 'timestamp':
            df[c] = pd.to_datetime(df[c], errors='coerce')
    return df


def records_to_dataframe(
    column_dict: Dict[str, str],
    fields: List[Dict[str, Any]],
    records: List[Dict[str, Any]]
) -> pd.DataFrame:
    """
    Convert API records to DataFrame with renamed columns.

    Args:
        column_dict: Mapping of desired column names to API field names
        fields: Field metadata from API response
        records: Data records from API response

    Returns:
        DataFrame with renamed columns
    """
    df = records_to_dataframe_raw(
        fields, records, columns=column_dict.values())
    inv_dict = dict(zip(column_dict.values(), column_dict.keys()))
    df = df.rename(inv_dict, axis=1)
    return df


def get_lv_meteo_data(
    table: str,
    stations: Union[str, List[str]],
    parameters: Union[str, List[str]],
    startdate: datetime.datetime,
    enddate: datetime.datetime,
    use_curl: bool = False,
    curl_exe_path: str = 'curl'
) -> pd.DataFrame:
    """
    Retrieve meteorological data for specified stations and parameters.

    Args:
        table: Table identifier from lv_meteo_tables
        stations: Station ID(s) to retrieve data for
        parameters: Parameter code(s) to retrieve
        startdate: Start date for data retrieval
        enddate: End date for data retrieval
        use_curl: Use curl instead of requests library
        curlExePath: Path to curl executable

    Returns:
        DataFrame with meteorological data, indexed by date and unstacked by station/parameter

    Raises:
        ValidationError: If input parameters are invalid
        APIError: If API request fails
        DataNotFoundError: If no data found
    """
    try:
        sql = create_lv_meteo_data_sql(
            table, stations, parameters, startdate, enddate)
        data = get_response_from_lv_data(
            sql, use_curl=use_curl, curlExePath=curl_exe_path)

        if not data.get('success', False):
            error_msg = f"API returned unsuccessful response: {data.get('error', 'Unknown error')}"
            logger.error(error_msg)
            raise APIError(error_msg)

        result = data.get('result')
        if not result:
            raise DataNotFoundError("No result data returned from API")

        records = result.get('records', [])
        if not records:
            logger.warning("No records found for the specified criteria")
            return pd.DataFrame()

        logger.debug(f"Retrieved {len(records)} records")

        df = records_to_dataframe(DATA_COLUMNS, result['fields'], records)

        if 'date' in df.columns and not df.empty:
            df['date'] = pd.DatetimeIndex(df['date']).tz_localize('UTC')
            df = df.drop_duplicates(keep='first').set_index(
                ['station_id', 'param', 'date']).sort_index()
            df = df.unstack(level=['station_id', 'param'])['value']

        logger.debug(f"Processed data shape: {df.shape}")
        return df

    except (ValidationError, APIError, DataNotFoundError):
        raise
    except Exception as e:
        error_msg = f"Unexpected error processing meteorological data: {e}"
        logger.error(error_msg)
        raise APIError(error_msg) from e


# https://data.gov.lv/dati/dataset/40d80be5-0c09-47c4-80f3-fad4bec19f33/resource/93fd5e2c-20c4-496e-a920-ff29bda20383/download/hidrologiskas_noverojumu_stacijas.csv
# https://data.gov.lv/dati/dataset/40d80be5-0c09-47c4-80f3-fad4bec19f33/resource/c32c7afd-0d05-44fd-8b24-1de85b4bf11d/download/meteo_stacijas.csv
def get_lv_meteo_stations(**x) -> pd.DataFrame:
    """
    Get list of all meteorological stations with their metadata.

    Args:
        **x: Additional parameters passed to get_table

    Returns:
        DataFrame with meteorological stations indexed by station_id
    """
    return get_table(RESOURCE_URLS.meteo_stations, STATION_COLUMNS, index_col='station_id', **x)


def get_lv_hidro_stations(**x) -> pd.DataFrame:
    """
    Get list of all hydrological stations with their metadata.

    Args:
        **x: Additional parameters passed to get_table

    Returns:
        DataFrame with hydrological stations indexed by station_id
    """
    return get_table(RESOURCE_URLS.hydro_stations, STATION_COLUMNS, index_col='station_id', **x)


def get_table(
    table: str,
    fieldmap: Dict[str, str],
    index_col: Optional[str] = None,
    **x
) -> pd.DataFrame:
    """
    Get all data from a specific table.

    Args:
        table: Table identifier
        fieldmap: Mapping of column names to API field names
        index_col: Optional column to use as DataFrame index
        **x: Additional parameters passed to get_fromsql

    Returns:
        DataFrame with table data
    """
    sql = f"""SELECT * from "{table}" """
    return get_fromsql(sql, fieldmap, index_col=index_col, **x)


def get_fromsql(
    sql: str,
    fieldmap: Optional[Dict[str, str]] = None,
    index_col: Optional[str] = None,
    **x
) -> pd.DataFrame:
    """
    Execute custom SQL query and return results as DataFrame.

    Args:
        sql: SQL query to execute
        fieldmap: Optional mapping of column names to API field names
        index_col: Optional column to use as DataFrame index
        **x: Additional parameters passed to get_response_from_lv_data

    Returns:
        DataFrame with query results

    Raises:
        ValidationError: If SQL query is invalid
        APIError: If API request fails
        DataNotFoundError: If no data found
    """
    try:
        data = get_response_from_lv_data(sql, **x)

        if not data.get('success', False):
            error_msg = f"SQL query failed: {data.get('error', 'Unknown error')}"
            logger.error(error_msg)
            raise APIError(error_msg)

        result = data.get('result')
        if not result:
            raise DataNotFoundError("No result data returned from SQL query")

        records = result.get('records', [])
        if not records:
            logger.warning("No records found for SQL query")
            return pd.DataFrame()

        logger.debug(f"Retrieved {len(records)} records from SQL query")

        if fieldmap is not None:
            df = records_to_dataframe(fieldmap, result['fields'], records)
        else:
            df = records_to_dataframe_raw(result['fields'], records)

        if index_col is not None and not df.empty:
            if index_col not in df.columns:
                logger.warning(f"Index column '{index_col}' not found in data")
            else:
                df = df.set_index(index_col)

        return df

    except (ValidationError, APIError, DataNotFoundError):
        raise
    except Exception as e:
        error_msg = f"Unexpected error executing SQL query: {e}"
        logger.error(error_msg)
        raise APIError(error_msg) from e


# https://data.gov.lv/dati/dataset/40d80be5-0c09-47c4-80f3-fad4bec19f33/resource/38b462ac-08b9-4168-9d6e-cbaedc2e775d/download/meteo_parametri.csv
def get_lv_meteo_params(**x) -> pd.DataFrame:
    """
    Get list of all available meteorological parameters.

    Args:
        **x: Additional parameters passed to get_table

    Returns:
        DataFrame with meteorological parameters indexed by param_id
    """
    return get_table(RESOURCE_URLS.meteo_params, PARAM_COLUMNS, index_col='param_id', **x)


# https://data.gov.lv/dati/dataset/40d80be5-0c09-47c4-80f3-fad4bec19f33/resource/714ab60d-d93e-4403-b76d-2fb865d15d63/download/hidro_parametri.csv
def get_lv_hidro_params(**x) -> pd.DataFrame:
    """
    Get list of all available hydrological parameters.

    Args:
        **x: Additional parameters passed to get_table

    Returns:
        DataFrame with hydrological parameters indexed by param_id
    """
    return get_table(RESOURCE_URLS.hydro_params, PARAM_COLUMNS, index_col='param_id', **x)


if __name__ == '__main__':
    test_parameters = ['HTDRY', 'HATMN', 'HATMX']
    test_stations = ['RIGASLU', 'RIDM99MS', 'RILP99PA']
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=30)

    test_data = get_lv_meteo_data(
        lv_meteo_tables.meteo_archive_avg.table_name,
        test_stations, test_parameters, start_date, end_date
    )

    print(test_data)
