import pandas as pd
import numpy as np

from .PEMEL import PEM
#from ALKEL import ALK
#from SOECEL import SOEC

## General project definitions
def PPA_simulation(PPA_size, cust_from, cust_to):
    energy_day   = pd.Series(np.ones(24))          #Dayly energy vector
    energy_input = pd.Series(np.ones(0))         #Yearly energy vector
    
    #EXPLICAR FORMATO HORARIO

    for h in range(0,24):                                      #Edit energy_day vector
        if h >= cust_from and h <= cust_to:
            energy_day[h]= PPA_size
        else:
            energy_day[h] = 0.0

    for i in range (365):                                     #Edit yearly energy vector                     
        energy_input = pd.concat([energy_input,energy_day])     #Creates a size=8760 vector
    energy_input=pd.DataFrame(energy_input)
    return (energy_input)
   
def Onsite_simulation(file):
    energy_input = pd.read_csv(file,header=None, encoding='UTF-8')
    file.close()
    return energy_input

def degradation(elec_type):
    if elec_type == "PEM":
        elec = PEM
    #elif elec_type == "ALK":
        #elec = ALK
    #else:
        #elec = SOEC

    deg_elec = (elec.deg)  #El punto hace que busque deg dentro de la variable elec, la cual está asociada a algún tipo de electrolizador
    

    return float(deg_elec)


#define replacements
