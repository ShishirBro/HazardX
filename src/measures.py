from climada.entity import Measure, MeasureSet, ImpfTropCyclone
import numpy as np

def get_measures(exposure, impf_set):
    """
    Defines adaptation measures and updates the impact function set with resilient functions.
    
    Returns:
    - climada.entity.MeasureSet
    - updated climada.entity.ImpactFuncSet
    """
    meas_set = MeasureSet()
    
    # Measure 1: Mangroves (Ecosystem based adaptation)
    # Assumption: Reduces damage by being a buffer.
    # Implementation: Uses a modified impact function (ID 2) which has lower damage ratios.
    
    # Create resilient impact function
    base_impf = impf_set.get_func(haz_type='TC', fun_id=1)
    
    # Create a copy and modify
    impf_mangrove = ImpfTropCyclone()
    impf_mangrove.haz_type = 'TC'
    impf_mangrove.id = 2
    impf_mangrove.name = 'TC Wind with Mangroves'
    impf_mangrove.intensity_unit = base_impf.intensity_unit
    # Reduce damage by 20% for example
    impf_mangrove.mdd = base_impf.mdd * 0.8
    impf_mangrove.paa = base_impf.paa
    impf_mangrove.intensity = base_impf.intensity
    
    impf_set.append(impf_mangrove)
    
    meas_mangrove = Measure(
        name='Mangroves',
        cost=5e6, # Fixed cost example
        haz_type='TC',
        # Divide by 255 to normalize RGB to 0-1 range
        color_rgb=np.array([26, 148, 49]) / 255, 
        imp_fun_map='1to2' # Explicit mapping: Use Impact Function 1 -> 2
    )
    
    # Measure 2: Building Retrofit (Grey infrastructure)
    # Reduces damage significantly for lower wind speeds
    impf_retrofit = ImpfTropCyclone()
    impf_retrofit.haz_type = 'TC'
    impf_retrofit.id = 3
    impf_retrofit.name = 'TC Wind Retrofitted'
    impf_retrofit.intensity_unit = base_impf.intensity_unit
    impf_retrofit.mdd = base_impf.mdd * 0.5
    impf_retrofit.paa = base_impf.paa
    impf_retrofit.intensity = base_impf.intensity
    
    impf_set.append(impf_retrofit)
    
    meas_retrofit = Measure(
        name='Retrofitting',
        cost=1e8, # Expensive
        haz_type='TC',
        # Divide by 255 to normalize RGB to 0-1 range
        color_rgb=np.array([128, 128, 128]) / 255, 
        imp_fun_map='1to3' # Explicit mapping: Use Impact Function 1 -> 3
    )
    
    meas_set.append(meas_mangrove)
    meas_set.append(meas_retrofit)
    
    return meas_set, impf_set
