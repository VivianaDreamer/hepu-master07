import pandas as pd
import numpy as np        

def deg_outputs(energy_input, elec_type, elec_size, horizon, deg_elec, water_type, eff_replacement,sp_footprint, customized_from=0, customized_to=24):

    if elec_type == "PEM":
        SEC   = PEMSEC           #define specific energy consumption according to electrolyzer
        P_min = 0.1              #as a percentage of Pnom
        P_max = 1.0              #idem
    #elif elec_type == "ALK":
        #SEC = ALKSEC()
    #else:
        #SEC = SOECSEC()

    P_max                  = P_max*elec_size
    P_min                  = P_min*elec_size
    E_cons                 = energy_input*1
    E_cons[E_cons < P_min] = 0.0
    E_cons[E_cons > P_max] = P_max
    Tot_E_cons             = sum(np.array(energy_input))[0]
    Load_factor            = Tot_E_cons/(elec_size*8760)
    E_curtailment          = energy_input-E_cons
    
    H2_output              = E_cons.apply(lambda x: (x/(SEC(x/(elec_size)))))

    year_stack             = list()                 #Lista que almacena el año en donde se realiza el reemplazo
    deg_annual_list        = list()                 #Crea una lista que guarde la degradación anual 
    count= 0           
    for i in range(0, horizon):
        hours              = (customized_to - customized_from) * count * 365     #Horas anuales de uso
        deg_annual         = deg_elec*hours/8760                                 #Calcula la degradación anual según las horas de uso
        if deg_annual      >= (1-eff_replacement/100):                           #Verifica que la degradación anual no supere el 20%
            year_stack.append(i)                                                 #Guarda el año de reemplazo
            count          = 1                                                   #Vuelve el contador a cero
            deg_annual_list.append(0.0)                                          #Reemplaza el electrolizador y su degradación vuelve a 0
            continue
        else:
            deg_annual_list.append(deg_annual)  
        count +=1  


    H2_hourly = pd.DataFrame(np.zeros([8760, horizon]))    #Hour, horizon
    H2_annual = pd.DataFrame(np.zeros([1, horizon]))       #Year generation
    for i in range (0, horizon):
        H2_hourly[i] = np.array(H2_output*(1-deg_annual_list[i]))  #TONS/H
        H2_annual[i] = sum(H2_hourly[i])    #TONS/A
    
    O2_hourly=H2_hourly*8
    O2_annual=H2_annual*8
    
    if water_type == "Tap":
        sp_watercons = 15                           #lts/kg H2
    else:                                          #Consumo demi water
        sp_watercons =  10   
    Water_hourly=sp_watercons*H2_hourly
    Water_annual=sp_watercons*H2_annual

    footprint=sp_footprint*elec_size                #m2

    return (E_cons,Load_factor, E_curtailment, H2_hourly, H2_annual,O2_hourly,O2_annual,Water_hourly,Water_annual, year_stack,footprint)


#ELIMINA ARCHIVO PEMSEC Y DEFINE NUEVAS FUNCIONES PEMSEC, ALKSEC Y SOECSEC \n
# QUE LLAMA DE ACUERDO AL TIPO DE ELECTROLIZADOR


def PEMSEC(P):
    X=[ 1.28522563e+05, -9.22330022e+05,  2.87420548e+06, -5.10063121e+06,
        5.68181718e+06, -4.12993761e+06,  1.97322293e+06, -6.09150653e+05,
        1.16176849e+05, -1.25043804e+04,  6.75350725e+02]
     #kWh/kg*(kg/Nm3)=kWh/Nm3
    tot_sp_consumption= (X[0]*P**10 + X[1]*P**9 + X[2]*P**8 + X[3]*P**7 + X[4]*P**6 + X[5]*P**5 + X[6]*P**4 + X[7]*P**3 + X[8]*P**2 + X[9]*P +X[10])
    return tot_sp_consumption

#def ALKSEC(P):
    #return tot_sp_consumption

#def SOECSEC(P):
    #return tot_sp_consumption