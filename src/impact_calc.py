from climada.engine import Impact
from climada.entity import ImpactFuncSet, ImpfTropCyclone

def calculate_impact(hazard, exposure):
    """
    Calculates impact.
    
    Returns:
    - climada.engine.Impact object
    """
    # Define Impact Function
    impf_set = ImpactFuncSet()
    
    # Use a standard TC impact function (e.g., Emanuelle 2011)
    # We can fetch standard ones or create one.
    # ImpfTropCyclone.from_api() is a good way if available, 
    # otherwise we create a simple sigmoid or similar.
    
    # Let's try to get a standard one provided by CLIMADA
    # Using Emanuel 2011 function which is standard for USA
    impf_tc = ImpfTropCyclone.from_emanuel_usa(impf_id=1)
    
    # Ensure the hazard type matches
    impf_tc.haz_type = 'TC' 
    impf_tc.id = 1
    
    impf_set.append(impf_tc)
    
    # Ensure exposure has the correct impact function id mapping
    # Assuming 'TC' is the hazard type
    if 'impf_TC' not in exposure.gdf.columns:
        exposure.gdf['impf_TC'] = 1
    
    imp = Impact()
    imp.calc(exposure, impf_set, hazard)
    return imp
