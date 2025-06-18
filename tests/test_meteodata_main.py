import datetime
import pytest
from lvmeteo import meteodata


def test_main_section_runs_without_exceptions():
    test_parameters = ['HTDRY']
    test_stations = ['RIGASLU']
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=1)

    # This should not raise any exception
    try:
        meteodata.get_lv_meteo_data(
            meteodata.lv_meteo_tables.meteo_operational.table_name,
            test_stations,
            test_parameters,
            start_date,
            end_date
        )
    except Exception as e:
        pytest.fail(f"Main section logic raised an exception: {e}")
