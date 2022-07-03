# VRB from cgi import print_arguments
import numpy as np
import numpy_financial as npf
import pandas as pd


def WACC(disc_rate, debt, int_rate, tax):
    return (debt*int_rate*(1-tax)+(1-debt)*disc_rate)


def cashflow(CAPEX, output_yearly, WACC, tot_energy_cost, OM_electrolyzer, water_cost_annual, V_stack_replacement,land_cost_year, horizon):
    T                      = len(output_yearly.columns)   #years of analysis   
    
    #annual cost vectors to create cashflow. All numpy arrays
    V_CAPEX                = np.zeros(T)
    V_CAPEX[0]             = CAPEX                           #CAPEX is a vector lenght T, with value diff than zero only in year 0
    V_energy_cost          = np.repeat(tot_energy_cost,T)
    V_OM                   = np.repeat(OM_electrolyzer,T)
    V_water_cost           = water_cost_annual
    V_land                 = np.repeat(land_cost_year,T)

    Cost_vectors_data      = {'CAPEX [USD]'               : V_CAPEX, 
                              'Energy [USD]'              : V_energy_cost,
                              'OM [USD]'                  : V_OM, 
                              'Water [USD]'               : V_water_cost,
                              'Cost of land [USD]'        : V_land,
                              'Cost of replacements [USD]': V_stack_replacement,}
    Cost_vectors_data      = pd.DataFrame(Cost_vectors_data)

    #Calculate the single value "Net present cost" per item using the previous vectors and WACC
    NPV_energy_cost        = npf.npv(WACC,V_energy_cost)
    NPV_OM                 = npf.npv(WACC, V_OM)    
    NPV_water              = npf.npv(WACC, V_water_cost)
    NPV_land               = npf.npv(WACC, V_land)
    NPV_stack_replacements = npf.npv(WACC,V_stack_replacement)
    NPV_tot_cost           = (CAPEX+NPV_energy_cost+NPV_OM+NPV_water+NPV_stack_replacements)  
    
    NPC_data               = {'Total CAPEX [USD]'                        : CAPEX, 
                              'Total Present Cost of energy [USD]'       : NPV_energy_cost,
                              'Total Present Cost of O&M [USD]'          : NPV_OM, 
                              'Total Present Cost of water [USD]'        : NPV_water,
                              'Total Present Cost of land [USD]'         : NPV_land,
                              'Total Present Cost of replacements [USD]' : NPV_stack_replacements}
    NPC_data               = pd.Series(NPC_data)

    #LCOH total and LCOH breakdown per item
    NPV_output  = npf.npv(WACC, (np.array(output_yearly)*10**3).reshape(horizon)) #kg of H2 -> Entender desde la fórmula de LCOH
    LCOH_CAPEX  = CAPEX/NPV_output
    LCOH_energy = NPV_energy_cost/NPV_output                  #Desgranar el NPV_cost en CAPEX, NPV.energy_cost, NPV.OM_ cost y NPV.water_cost. Su sumatoria debe ser igual al LCO_X
    LCOH_OM     = NPV_OM/NPV_output
    LCOH_water  = NPV_water/NPV_output
    LCOH_land   = NPV_land/NPV_output
    LCOH_stack  = NPV_stack_replacements/NPV_output
    LCOH        = (LCOH_CAPEX+LCOH_energy+LCOH_OM+LCOH_water+LCOH_stack)
    
    LCOH_data   = {'CAPEX'       : LCOH_CAPEX, 
                   'Energy'      : LCOH_energy,
                   'O&M'         : LCOH_OM,
                   'Water'       : LCOH_water,
                   'Land'        : LCOH_land,
                   'Replacements': LCOH_stack}
    LCOH_data   =pd.Series(LCOH_data)
    
    return LCOH, Cost_vectors_data, NPC_data, LCOH_data




    