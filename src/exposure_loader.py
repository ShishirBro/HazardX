from climada.entity import Exposures
# Use direct function import to avoid module confusion
from climada.entity.exposures.litpop.nightlight import load_nasa_nl_shape
import climada.util.coordinates as u_coord
from shapely.geometry import box
import pandas as pd
import numpy as np
import geopandas as gpd
import os
from pathlib import Path

def get_florida_exposure(cache_dir="data"):
    """
    Generates exposure for Florida using ONLY Nightlight data (Black Marble).
    Avoids Population data download issues (GPW).
    
    Returns:
    - climada.entity.Exposures object
    """
    Path(cache_dir).mkdir(parents=True, exist_ok=True)
    filename = os.path.join(cache_dir, "exposure_fl_nightlight.hdf5")
    
    if os.path.exists(filename):
        print(f"Loading exposure from {filename}")
        return Exposures.from_hdf5(filename)
    
    print("Generating new exposure data from Nightlights (ignoring Population)...")
    
    # Florida Bounding Box
    # LonMin, LatMin, LonMax, LatMax
    min_lon, min_lat, max_lon, max_lat = -87.63, 24.52, -80.03, 31.00
    fl_poly = box(min_lon, min_lat, max_lon, max_lat)
    
    # Load Nightlight Data (automatically downloads if needed)
    # Returns (numpy_array, metadata_dict)
    print("Loading Black Marble data...")
    nl_data, meta = load_nasa_nl_shape(fl_poly, year=2016)
    
    # Create Coordinates
    transform = meta['transform']
    width = meta['width']
    height = meta['height']
    
    # raster_to_meshgrid returns 2D arrays of lon, lat
    lon_2d, lat_2d = u_coord.raster_to_meshgrid(transform, width, height)
    
    # Flatten
    val_flat = nl_data.flatten()
    lon_flat = lon_2d.flatten()
    lat_flat = lat_2d.flatten()
    
    # Create DataFrame
    df = pd.DataFrame({
        'latitude': lat_flat,
        'longitude': lon_flat,
        'value': val_flat
    })
    
    # Filter out zero/nan values
    # Also filter out very low light to reduce size
    df = df[df['value'] > 0.1]
    
    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame(
        df, 
        geometry=gpd.points_from_xy(df.longitude, df.latitude),
        crs=meta['crs']
    )
    
    # Total Value Scaling
    # Estimate Florida Total Exposure ~ 3.5 Trillion USD (produced capital)
    total_value_usd = 3.5e12 
    total_intensity = gdf['value'].sum()
    
    if total_intensity > 0:
        gdf['value'] = (gdf['value'] / total_intensity) * total_value_usd
        print(f"Exposure scaled to {total_value_usd:,.0f} USD based on nightlight intensity.")
    else:
        print("Warning: No nightlight intensity found. Exposure value is 0.")
    
    # Assign metadata
    exp = Exposures(gdf)
    exp.ref_year = 2016
    exp.value_unit = 'USD'
    
    # Set proper metadata for raster reconstruction if needed
    exp.meta = {
        "width": width,
        "height": height,
        "crs": meta['crs'],
        "transform": transform
    }
    
    exp.check()
    exp.write_hdf5(filename)
    
    return exp
