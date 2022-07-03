import numpy as np
import numpy_financial as npf
import pandas as pd

def costs(elec_type, elec_size, PPA_size, water_annual, elec_cost, develop_cost, sp_land_cost, energy_cost, OM_cost, water_cost, installation_cost, indirect_cost, PPA_type, customized_from, customized_to,footprint, year_stack,horizon,WACC):

    ## CAPEX ##
    #Direct
    sp_CAPEX_container    = elec_cost/1000                                   #USD/W
    sp_CAPEX_development  = develop_cost/1000                                #USD/W
    sp_CAPEX_installation = installation_cost/1000                           #USD/W
    sp_CAPEX_indirect     = indirect_cost/elec_size/1000/1000                     #USD/W

    sp_CAPEX_breakdown=pd.Series({'Electrolyzer':sp_CAPEX_container,'Development':sp_CAPEX_development, 'Installation':sp_CAPEX_installation,'Indirect':sp_CAPEX_indirect})

    sp_tot_CAPEX_elec    = sp_CAPEX_container + sp_CAPEX_development + sp_CAPEX_installation + sp_CAPEX_indirect       #USD/W
    CAPEX                = (elec_size*sp_tot_CAPEX_elec*10**6)              #USD

    ## OPEX ##
    land_cost_year       = sp_land_cost*(footprint*0.0001)                  #USD

    #Hours of operation
    if PPA_type == "24/7":
        hours = 8760-(7*24)    #Detenido una semana por año. Factor de planta implícito
    else:
        hours = (customized_to - customized_from)*365   #No hay factor de mantención
    
    #Type of degradation
    if elec_type == "PEM":
        elec_cost_dec = 0.00667           #Electrolyzer cost decrease - Disminución anual del 1%
    #elif elec_type == "ALK":
        #elec_cost_dec = 0.01
    #else:
    
    #Annual Operational costs
    tot_energy_cost    = energy_cost*PPA_size*hours
    OM_electrolyzer    = OM_cost*elec_size*10**3     #Costo específico (USD/kW/year) * tamaño (MW)* conversión
    water_cost_annual=np.array(water_annual.values[0]*water_cost)
    #Cost of replacements
    stack_replacement_cost=np.zeros(horizon)
    for i in year_stack:            #calcula el costo del stack replacement de acuerdo al año en que se realiza
        stack_replacement_cost[i]=(((1-i*elec_cost_dec)*elec_size*sp_CAPEX_container*10**6))

    annualized_replacecost=-npf.pmt(WACC,horizon,npf.npv(WACC,stack_replacement_cost))

    OPEX_annual=tot_energy_cost+OM_electrolyzer+water_cost_annual[0]+land_cost_year+annualized_replacecost
    sp_CAPEX_breakdown=pd.Series({'Electrolyzer':sp_CAPEX_container,'Development':sp_CAPEX_development, 'Installation':sp_CAPEX_installation,'Indirect':sp_CAPEX_indirect})
    sp_CAPEX_breakdown=sp_CAPEX_breakdown*10**6 
    sp_OPEX_breakdown=pd.Series({'Energy':(tot_energy_cost),'OM':(OM_electrolyzer), 'water':(water_cost_annual[0]),'land':(land_cost_year),'Replacements':(annualized_replacecost)})

    return CAPEX, OPEX_annual, tot_energy_cost, OM_electrolyzer, water_cost_annual, stack_replacement_cost, land_cost_year,sp_CAPEX_breakdown,sp_OPEX_breakdown