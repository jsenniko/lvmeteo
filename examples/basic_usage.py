#!/usr/bin/env python3
"""
Example usage of LVMeteo library for retrieving Latvian meteorological data.

This example demonstrates how to:
1. Get meteorological data for specific stations and parameters
2. Retrieve station metadata
3. Get parameter information
4. Execute custom SQL queries
"""

import datetime
from lvmeteo import (
    get_lv_meteo_data,
    get_lv_meteo_stations,
    get_lv_hidro_stations,
    get_lv_meteo_params,
    get_lv_hidro_params,
    get_fromsql,
    lv_meteo_tables
)


def main():
    """Main example function demonstrating various library features."""
    
    # Define parameters and stations for data retrieval
    parameters = ['HTDRY', 'HATMN', 'HATMX']  # Temperature parameters
    stations = ['RIGASLU', 'RIDM99MS', 'RILP99PA']  # Riga area stations
    
    # Set date range - last 30 days
    enddate = datetime.datetime.now()
    startdate = enddate - datetime.timedelta(days=30)
    
    print("=== LVMeteo Library Example ===\n")
    
    # Example 1: Get meteorological archive data (averages)
    print("1. Retrieving meteorological archive data (AVG, MIN, MAX)...")
    try:
        df_meteo = get_lv_meteo_data(
            lv_meteo_tables.meteo_archive_avg.table_name, 
            stations, 
            parameters, 
            startdate, 
            enddate
        )
        print(f"   Retrieved data shape: {df_meteo.shape}")
        print(f"   Data preview:\n{df_meteo.head()}\n")
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Example 2: Get meteorological stations
    print("2. Retrieving meteorological stations...")
    try:
        df_stations = get_lv_meteo_stations()
        print(f"   Total stations: {len(df_stations)}")
        print(f"   Station columns: {list(df_stations.columns)}")
        print(f"   Sample stations:\n{df_stations.head()[['name', 'latitude', 'longitude']]}\n")
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Example 3: Get hydrological stations
    print("3. Retrieving hydrological stations...")
    try:
        df_hydro_stations = get_lv_hidro_stations()
        print(f"   Total hydro stations: {len(df_hydro_stations)}")
        print(f"   Sample hydro stations:\n{df_hydro_stations.head()[['name', 'latitude', 'longitude']]}\n")
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Example 4: Get meteorological parameters
    print("4. Retrieving meteorological parameters...")
    try:
        df_params = get_lv_meteo_params()
        print(f"   Total parameters: {len(df_params)}")
        print(f"   Sample parameters:\n{df_params.head()[['description_EN', 'unit']]}\n")
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Example 5: Get hydrological parameters
    print("5. Retrieving hydrological parameters...")
    try:
        df_hydro_params = get_lv_hidro_params()
        print(f"   Total hydro parameters: {len(df_hydro_params)}")
        print(f"   Sample hydro parameters:\n{df_hydro_params.head()[['description_EN', 'unit']]}\n")
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Example 6: Weather phenomena data
    print("6. Retrieving weather phenomena data...")
    try:
        phenomena_params = ['PHENO']
        df_phenomena = get_lv_meteo_data(
            lv_meteo_tables.weather_phenomena_archive.table_name, 
            stations, 
            phenomena_params, 
            startdate, 
            enddate
        )
        print(f"   Weather phenomena data shape: {df_phenomena.shape}")
        if not df_phenomena.empty:
            print(f"   Data preview:\n{df_phenomena.head()}\n")
        else:
            print("   No weather phenomena data found for the specified period.\n")
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Example 7: Custom SQL query
    print("7. Executing custom SQL query...")
    try:
        table = lv_meteo_tables.meteo_archive.table_name
        sql = f'''SELECT "ABBREVIATION", avg("VALUE") as avg_value, count(*) as count 
                  FROM "{table}" 
                  GROUP BY "ABBREVIATION" 
                  ORDER BY count DESC 
                  LIMIT 10'''
        
        df_custom = get_fromsql(sql)
        print(f"   Custom query results:\n{df_custom}\n")
    except Exception as e:
        print(f"   Error: {e}\n")
    
    print("=== Example completed ===")


if __name__ == '__main__':
    main()