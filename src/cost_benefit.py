from climada.engine import CostBenefit
from climada.entity import DiscRates, Entity
import numpy as np

def perform_cost_benefit(hazard, exposure, impf_set, measure_set):
    """
    Performs cost benefit analysis.
    
    Returns:
    - climada.engine.CostBenefit object
    """
    # Define Discount Rates
    # 2% discount rate over 50 years (extending range to cover 2016 start)
    rates = DiscRates()
    # IMPORTANT: years must be a numpy array for CLIMADA's internal indexing to work correctly
    rates.years = np.arange(2016, 2073)
    rates.rates = np.full(len(rates.years), 0.02)
    
    # Bundle into Entity
    # Note: Entity expects exposures, disc_rates, measures, impact_funcs
    ent = Entity()
    ent.exposures = exposure
    ent.disc_rates = rates
    ent.measures = measure_set
    ent.impact_funcs = impf_set
    
    # Check entity
    ent.check()
    
    # Initialize CostBenefit
    cb = CostBenefit()
    
    # Calculate
    cb.calc(hazard, ent, save_imp=True)
    
    return cb
