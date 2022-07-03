import numpy as np

def monthly_plot(H2_hourly):
    t8 = 28*24
    t0 = 30*24
    t1 = 31*24
    jan = H2_hourly[0][0:t1]
    feb = H2_hourly[0][t1:t1+t8]
    mar = H2_hourly[0][t1+t8:2*t1+t8]
    apr = H2_hourly[0][2*t1+t8:2*t1+t8+t0]
    may = H2_hourly[0][2*t1+t8+t0:3*t1+t8+t0]
    jun = H2_hourly[0][3*t1+t8+t0:3*t1+t8+2*t0]
    jul = H2_hourly[0][3*t1+t8+2*t0:4*t1+t8+2*t0]
    aug = H2_hourly[0][4*t1+t8+2*t0:5*t1+t8+2*t0]
    sep = H2_hourly[0][5*t1+t8+2*t0:5*t1+t8+3*t0]
    oct = H2_hourly[0][5*t1+t8+3*t0:6*t1+t8+3*t0]
    nov = H2_hourly[0][6*t1+t8+3*t0:6*t1+t8+4*t0]
    dec = H2_hourly[0][6*t1+t8+4*t0:7*t1+t8+4*t0]

    monthly_plot_data = dict()
    
    months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    year = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]
    
    for i in range(len(year)):
        monthly_plot_data[months[i]]=sum(year[i])
    
    return monthly_plot_data

def energy_performance(energy,H2,horizon):
    energy_performance_data = dict()
    Energy_perf_LC=sum(energy)/H2
    years=np.linspace(1,horizon,horizon)
    for i in range(len(years)):
        energy_performance_data[str(years[i])] = Energy_perf_LC.values[0][i]
    return(energy_performance_data)

#YEARLY PRODUCTION IN 20 YEARS
def yearly_plot(H2_annual):
    yearly_plot_data = dict()
    for i in range (H2_annual.size):
        yearly_plot_data[str(i+1)] = float(str(H2_annual[i]).split()[1])
    return yearly_plot_data

#ECONOMIC PERFORMANCE
def lcoh_plot(LCOH_data):
    lcoh_plot_data = dict()
    for key, value in LCOH_data.items():
        if value > 0:
            lcoh_plot_data[key] = value
    return lcoh_plot_data