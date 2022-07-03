import math
import numpy as np

class PEM:
#PEM electrolyzer stack and cell characterisitcs
    R = 8.314                   #Ideal gas constant [J/mol/K]
    F = 96485                   #Faraday's constant [C]
    A = 680                     #Area of cell [cm^2]
    N_cells = 102               #Number of cells
    Alpha = 0.5                 #Transfer coefficient
    il= 6                       #Limiting current density [A/cm^2]
    lm = 1.78*10**(-2)          #Membrane thickness [cm]
    lambdam = 20                #Membrane hydration parameter
    roughness_an=7.23*10**(2)   #roughness factor [cm^2/cm^2]
    roughness_cat= 2.33*10**(2) #roughness factor[cm^2/cm^2]
    i0ref_an=2.3*10**(-7)       #anode exchange current density at the reference temperature [A/cm^2]
    i0ref_cat=1*10**(-3)        #cathode exchange current density at the reference temperature [A/cm^2]
    vthn=1.481                  #thermobeutral voltage [V]
    MmH2O=18                    #water molar mass [g/mol]
    rhoH2O=997                  #water density [kg/m^3]
    Ea_an=76000                 #anode activation energy [J/mol]
    Ea_cat=4300                 #cathode activation energy [J/mol]
    Tref=298                    #reference temperature [K]
    

    Vtn=1.481                   #thermal V
    eff_i=0.96                  #faraday efficiency
    HHV=141800                  #J/g
    Pref=250
    
    OH=80*10**3                 #Operational hours
    deg=(0.2/(60*10**3))*8760   #Annual degradation for 24/7

    #Saturation pressure of water
    def PsatH2O(self,Tk):
        Tc=Tk-273.15
        PsatH2O=610*10**(-5)*math.exp((Tc/(Tc+238.3))*17.2694) #[bar]
        return PsatH2O

    #Ernst Potential
    def ENernst(self,Tk,pres):
        a=PEM()
        pcat= 1.7                          #pressure at the cathode [bar]
        pan=pres                           #pressure at the anode [bar]
        ppH2=pan-a.PsatH2O(Tk)             #partial pressure Hydrogen [bar]
        ppO2=pcat-a.PsatH2O(Tk)            #partial pressure Oxygen [bar]
        E=1.229-0.9*10**(-3)*(Tk-298)      #standard potential reversible [V]
        Gf_liq=E*2*a.F;                    #Gibbs free energy [J/mol]
        ENernst=Gf_liq/(2*a.F) - ((a.R*Tk)*math.log(a.PsatH2O(Tk)/(ppH2     *(ppO2**0.5))))/(2*a.F) #[V]
        return ENernst

    #Activation overpotential
    def VAct(self,Tk,I):
        a=PEM
        io_an=a.roughness_an*a.i0ref_an*math.exp(-(a.Ea_an/a.R)*(1/Tk-1/353))          #[A/cm^2]
        io_cat=a.roughness_cat*a.i0ref_cat*math.exp(-(a.Ea_cat/a.R)*(1/Tk-1/353))      #[A/cm^2]
        c =a.R*Tk/(a.Alpha*a.F)
        b1=math.asinh((I/a.A)/(2*io_an))
        b2=math.asinh((I/a.A)/(2*io_cat))
        Vact=c*(b1+b2)                             # [V]
        return Vact

    #Ohmic protonic overpotential
    def VOhm(self,Tk,I):
        a=PEM
        r=a.lm * 1 / (( 0.005139 *a.lambdam + 0.00326 )* math.exp(1267*(1/303-1/Tk))) #[Ohm*cm^2]
        VOhm = ((I/a.A)*r)   #[V]
        return VOhm

    #Concentration overpotential 
    def VConc(self,Tk,I):
        a=PEM
        VConc = a.R*Tk/(2*a.F)*(1+1/a.Alpha)*math.log(a.il/(a.il-(I/a.A))) #[V]
        return VConc

    #Cell voltage 
    def Vcell(self,Tk,I,P):
        Vcell=self.ENernst(Tk,P)+self.VAct(Tk,I)+self.VOhm(Tk,I)+self.VConc(Tk,I)
        return Vcell
    
    #Efficiency of cell
    def Cell_eff(self,Tk,I,P):
        eff_v=self.Vtn/self.Vcell(Tk,I,P)
        eff_cell=eff_v*self.eff_i
        return eff_cell
    
    #Hydrogen prodution per cell in grams per second
    def H2_cell_gen(self,Tk,I,P):
        Pin=self.Vcell(Tk,I,P)*I
        Pout=self.Cell_eff(Tk,I,P)*Pin
        H2=Pout/self.HHV # g/s
        return H2

    #Stack voltage
    def VStack(self,Tk,I,P):
        Stackvoltage=self.Vcell(Tk,I,P)*self.N_cells*0.99
        return Stackvoltage
    
    #Hydrogen prodution per stack in kilograms per hours
    def H2_stack_gen(self,Tk,I,P):
        H2=(self.H2_cell_gen(Tk,I,P)*self.N_cells)*3600/1000 # kg/hour
        return H2

    def sp_Stack_power(self,Tk,I,P):
            Pstack=self.VStack(Tk,I,P)*I/1000 #kW
            return Pstack


    #Hydrogen specific consumption per stack kWh/kg
    def sp_Stack_cons(self,Tk,I,P):
        Pstack=self.VStack(Tk,I,P)*I/1000 #kW
        H2=self.H2_stack_gen(Tk,I,P)   #kg/h
        Sp_cons=Pstack/H2                 #kWh/kg
        return Sp_cons

    #Balance of plant consumption
    def sp_BOP_power(self,Tk,I,P):
        Water_pump   =5               #kW/(220kW stack)
        Other_loads  =15              #kW/(220kW stack)
        Paras_loss   =20              #kW/(220kW stack)
        BoP=Water_pump+Other_loads+Paras_loss
        Pstack=I*self.VStack(Tk,I,P)/1000
        P=Pstack/self.Pref
        eff_BoP=(P)**(-0.721)   #[%] valid for operational range between 10%-110%     
        BoP_power=(P*BoP)*eff_BoP
        return BoP_power

    def sp_BOP_cons(self,Tk,I,P):
        H2=self.H2_stack_gen(Tk,I,P)   #  kg/h
        BoP_cons= self.sp_BOP_power(Tk,I,P)/H2      #kWh/kg
        return BoP_cons

    #Total system power
    def sp_tot_power(self,Tk,I,P):
        Pstack=I*self.VStack(Tk,I,P)/1000
        P_BoP=self.sp_BOP_power(Tk,I,P)
        tot_PEM_power=Pstack+P_BoP
        return tot_PEM_power

    #Total system consumption
    def sp_tot_cons(self,Tk,I,P):
        Sp_tot_PEM_cons=self.sp_Stack_cons(Tk,I,P)+self.sp_BOP_cons(Tk,I,P)
        return Sp_tot_PEM_cons


    #def bb_eff(self):
    def eff(self):
        Tref=273+80
        P=30
        iref=1.7
        i=np.linspace(0.01*iref,iref*1.2,100)
        I=self.A*i
        V_Pcons_tot=np.vectorize(self.sp_tot_cons)
        V_Power_tot=np.vectorize(self.sp_tot_power)
        Pin=V_Power_tot(Tref,I,P)
        Op_point=Pin/220
        Y=V_Pcons_tot(Tref,I,P)
        print(Op_point)
        print(Y)
        Z10=np.polyfit(Op_point,Y,10)
        return Z10
        
## Define function that reads takes input power, round it to 1 decimal returns the efficiency