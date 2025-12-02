from climada.hazard import TCTracks, TropCyclone
from climada.util.api_client import Client
import numpy as np
import os
from pathlib import Path

def get_florida_hazard(year_range=(2000, 2020), cache_dir="data"):
    """
    Generates or loads Tropical Cyclone hazard for Florida.
    
    Parameters:
    - year_range: tuple of (start_year, end_year)
    - cache_dir: directory to store cached data
    
    Returns:
    - climada.hazard.TropCyclone object
    """
    Path(cache_dir).mkdir(parents=True, exist_ok=True)
    filename = os.path.join(cache_dir, f"hazard_fl_{year_range[0]}_{year_range[1]}.hdf5")
    
    if os.path.exists(filename):
        print(f"Loading hazard from {filename}")
        return TropCyclone.from_hdf5(filename)
    
    print("Generating new hazard data...")
    # Fetch tracks for North Atlantic (NA)
    # TCTracks.from_ibtracs_netcdf will download the dataset if not present
    tr_na = TCTracks.from_ibtracs_netcdf(basin='NA', year_range=year_range)
    
    # Filter for Florida roughly (bounding box)
    # Florida approx bounds: 24.5N to 31N, -87.6W to -80W
    # Adding a buffer to catch storms passing nearby
    box = (-90, 20, -75, 35) 
    
    # Create centroids for Florida
    from climada.hazard import Centroids
    centroids = Centroids.from_pnt_bounds(box, res=0.1)
    
    # Re-compute with specific centroids
    haz = TropCyclone.from_tracks(tr_na, centroids=centroids)
    
    # Check if we have events
    if haz.size == 0:
        print("No events found in this range/area.")
    
    # Ensure frequency is set correctly (Annual frequency)
    # If not set, assume uniform probability over the observation period
    if not hasattr(haz, 'frequency') or np.all(haz.frequency == 0):
        num_years = year_range[1] - year_range[0] + 1
        haz.frequency = np.ones(haz.size) / num_years
        
    haz.check()
    haz.write_hdf5(filename)
    return haz
