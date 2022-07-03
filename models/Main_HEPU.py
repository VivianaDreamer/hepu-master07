import numpy as np
import pandas as pd

from .simulation import PPA_simulation, Onsite_simulation, degradation
from .costs import costs
from .cashflow import cashflow, WACC
from .outputs import deg_outputs, PEMSEC
from .plots import energy_performance, lcoh_plot, monthly_plot, yearly_plot

def _process_hours(design):
    if design.op_type    == "PPA":
        if design.ppa_type == "24/7":        
            customized_from = "00:00"
            customized_to   = "24:00"
        else:                                           
            customized_from = design.customized_from
            customized_to   = design.customized_to
        customized_from = int(customized_from [: customized_from.find (":")])
        customized_to   = int(customized_to   [: customized_to.find   (":")])
    else:
        customized_from = 0  
        customized_to   = 24
    return customized_from, customized_to

def main(design):

    customized_from, customized_to = _process_hours(design)

    #internal function (not user defined)
    WACC_value   = WACC(design.equity_discount_rate/100, design.debt/100, design.interest_rate/100, design.first_category_tax/100)

    ### 2. SIMULATION ###
    deg_elec   =   degradation(design.elec_type)

    if design.op_type == "PPA":
        energy_input = PPA_simulation(design.nom_power, customized_from, customized_to)
    else:
        energy_input = Onsite_simulation(design.o_s_gen)

    #Technical simulation
    [E_cons,Load_factor, E_curtailment, H2_hourly, H2_annual, O2_hourly, O2_annual,water_hourly,water_annual,year_stack_replacements, footprint] = deg_outputs(energy_input, design.elec_type, design.elec_size, design.horizon, deg_elec, design.water_type, design.eff_replacement, design.sp_footprint, customized_from, customized_to)
    #Cost calculation
    [CAPEX_tot,OPEX_Y, tot_energy_cost, OM_electrolyzer, water_cost_annual, stack_replacement,land_cost_year,sp_CAPEX_breakdown,sp_OPEX_breakdown] = costs(design.elec_type, design.elec_size, design.nom_power, water_annual, design.elec_cost, design.develop_cost, design.land_cost, design.energy_cost, design.om, design.water_cost, design.installation_cost, design.indirect_cost, design.ppa_type, customized_from, customized_to, footprint, year_stack_replacements,design.horizon, WACC_value)
    #Financial analysis
    [LCOH, Cost_vectors_data, NPC_data, LCOH_data]=cashflow(CAPEX_tot, H2_annual, WACC_value, tot_energy_cost, OM_electrolyzer, water_cost_annual, stack_replacement, land_cost_year, design.horizon)


    monthly_plot_data = monthly_plot(H2_hourly)
    energy_plot_data = energy_performance(energy_input[0],H2_annual,design.horizon)
    yearly_plot_data = yearly_plot(H2_annual)
    lcoh_plot_data = lcoh_plot(LCOH_data)

    data = {
        'hydrogen_production':round(float(H2_annual[0]),2), 
        'oxigen_production':round(float(O2_annual[0]),2), 
        'energy_consumption':round(float(sum(E_cons))/1000,2),
        'load_factor': round(Load_factor,2),
        'average_energy_consumption': round(float(sum(E_cons))/H2_annual[0][0],2),
        'water_consumption':round(float(water_annual[0]),2), 
        'curtailed_energy':round(float(sum(E_curtailment))/1000,2),
        'energy_cost':Cost_vectors_data["Energy [USD]"][0],
        'water_cost': round(Cost_vectors_data["Water [USD]"][0],2),
        'total_capex':round(NPC_data[0],2),
        'nvp_energy_cost': round(float(NPC_data[1]),2),
        'nvp_om': round(float(NPC_data[2]),2),
        'nvp_water': round(float(NPC_data[3]),2),
        'nvp_land': round(float(NPC_data[4]),2),
        'present_stack_replacements':round(NPC_data[5],2), 
        'present_total_cost':round(sum(NPC_data),2), 
        'stack_replacements':len(year_stack_replacements), 
        'year_of_replacements':str(year_stack_replacements),
        'wacc': round(WACC_value,2),
        'lcoh':round(LCOH,2),
        'monthly_plot_data':str(monthly_plot_data),
        'energy_plot_data':str(energy_plot_data),
        'yearly_plot_data':str(yearly_plot_data),
        'lcoh_data':str(lcoh_plot_data),
        'h2_annual':np.array2string(H2_annual.to_numpy(), separator=','),
        'water_consumption_data':np.array2string(water_annual.to_numpy(), separator=','),
        'npc_data':str(NPC_data.to_dict()),
        'lcoh_down_data':str(LCOH_data.to_dict()),
        'capex_breakdown':sp_CAPEX_breakdown.to_dict(),
        'capex_tot':round(CAPEX_tot,1),
        'opex_breakdown':sp_OPEX_breakdown.to_dict(),
        'opex_tot':round(OPEX_Y,2)
    }

    return data

def deg_outputs_h2hourly(object) -> pd.DataFrame:
    customized_from, customized_to = _process_hours(object)
    deg_elec   =   degradation(object.elec_type)
    if object.op_type == "PPA":
        energy_input = PPA_simulation(object.nom_power, customized_from, customized_to)
    else:
        energy_input = Onsite_simulation(object.o_s_gen)
    if object.elec_type == "PEM":
        SEC   = PEMSEC           #define specific energy consumption according to electrolyzer
        P_min = 0.1              #as a percentage of Pnom
        P_max = 1.0              #idem
    P_max                  = P_max*object.elec_size
    P_min                  = P_min*object.elec_size
    E_cons                 = energy_input*1
    E_cons[E_cons < P_min] = 0.0
    E_cons[E_cons > P_max] = P_max
    E_cons                 = E_cons    
    H2_output              = E_cons.apply(lambda x: (x/(SEC(x/(object.elec_size))) ))    
    year_stack             = list()                 #Lista que almacena el año en donde se realiza el reemplazo
    deg_annual_list        = list()             #Crea una lista que guarde la degradación anual 
    count= 0           
    for i in range(0, object.horizon):
        hours              = (customized_to - customized_from) * count * 365     #Horas anuales de uso
        deg_annual         = deg_elec*hours/8760                                 #Calcula la degradación anual según las horas de uso
        if deg_annual      >= (1-object.eff_replacement/100):                           #Verifica que la degradación anual no supere el 20%
            year_stack.append(i)                                                 #Guarda el año de reemplazo
            count          = 1                                                   #Vuelve el contador a cero
            deg_annual_list.append(0.0)                                          #Reemplaza el electrolizador y su degradación vuelve a 0
            continue
        else:
            deg_annual_list.append(deg_annual)  
        count +=1  
    H2_hourly = pd.DataFrame(np.zeros([8760, object.horizon]))    #Hour, horizon
    for i in range (0, object.horizon):
        H2_hourly[i] = np.array(H2_output*(1-deg_annual_list[i]))  #TONS/H
    return H2_hourly

def energy_input_download(object)->pd.Series:
    customized_from, customized_to = _process_hours(object)
    return PPA_simulation(object.nom_power, customized_from, customized_to)

def cost_data(design)->pd.DataFrame:

    customized_from, customized_to = _process_hours(design)

    #internal function (not user defined)
    WACC_value   = WACC(design.equity_discount_rate/100, design.debt/100, design.interest_rate/100, design.first_category_tax/100)

    ### 2. SIMULATION ###
    deg_elec   =   degradation(design.elec_type)

    if design.op_type == "PPA":
        energy_input = PPA_simulation(design.nom_power, customized_from, customized_to)
    else:
        energy_input = Onsite_simulation(design.o_s_gen)

    #Technical simulation
    [E_cons,Load_factor, E_curtailment, H2_hourly, H2_annual, O2_hourly, O2_annual,water_hourly,water_annual,year_stack_replacements, footprint] = deg_outputs(energy_input, design.elec_type, design.elec_size, design.horizon, deg_elec, design.water_type, design.eff_replacement, design.sp_footprint, customized_from, customized_to)
    #Cost calculation
    [CAPEX_tot,OPEX_Y, tot_energy_cost, OM_electrolyzer, water_cost_annual, stack_replacement,land_cost_year,sp_CAPEX_breakdown,sp_OPEX_breakdown] = costs(design.elec_type, design.elec_size, design.nom_power, water_annual, design.elec_cost, design.develop_cost, design.land_cost, design.energy_cost, design.om, design.water_cost, design.installation_cost, design.indirect_cost, design.ppa_type, customized_from, customized_to, footprint, year_stack_replacements,design.horizon, WACC_value)
    #Financial analysis
    [LCOH, Cost_vectors_data, NPC_data, LCOH_data]=cashflow(CAPEX_tot, H2_annual, WACC_value, tot_energy_cost, OM_electrolyzer, water_cost_annual, stack_replacement, land_cost_year, design.horizon)

    return Cost_vectors_data