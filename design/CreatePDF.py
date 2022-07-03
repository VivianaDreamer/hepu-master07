from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('RobotoLT', 'apps/static/assets/pdf/Roboto-Light.ttf'))
pdfmetrics.registerFont(TTFont('Roboto', 'apps/static/assets/pdf/Roboto-Regular.ttf'))

from .templatetags.custom_aprox import list_formater, lcoh_display, number_format

def render_pdf(design) -> HttpResponse:
        c = []
        c.append(Image("apps/static/assets/pdf/head1.png",width=585, height=175))
        c.append(Spacer(1,3))
        c.append(Image("apps/static/assets/pdf/head2.png", width=585, height=53))
        c.append(Spacer(1,10))

        data= [['General'],]
        t=Table(data,1*[160*mm], 1*[6*mm])
        t.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),

                        ('FONT', (0, 0), (-1, -1), 'Roboto')
                        ]))

        c.append(t)

        data= [['Project Name', str(design.project_name)],
                ['Location', str(design.location)],
                ['Start of Production', str(design.cod)],
                ['Years of Operation', str(design.horizon)]]
        t=Table(data,2*[40*mm], 4*[6*mm])
        t.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ('FONT', (0, 0), (-1, -1), 'RobotoLT')
                        ]))
        c.append(t)

        c.append(Spacer(1,8))

        data= [['Technical Specifications'],]
        t=Table(data,1*[160*mm], 1*[6*mm])
        t.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),

                        ('FONT', (0, 0), (-1, -1), 'Roboto')
                        ]))

        c.append(t)

        data= [['Energy supply', str(design.op_type)],
                ['NominalPower [MW]', str(design.nom_power)],
                ['Electrolyzer type', str(design.elec_type)],
                ['Electrolyzer nominal power [MW]', str(design.elec_size)],
                ['Min. electrolyzer efficiency before replacement [%]', str(design.eff_replacement)],
                ['Water supply', str(design.water_type)],
                ['System footprint [m²/MW]', str(design.sp_footprint)],]
        t=Table(data,2*[80*mm], 7*[6*mm])
        t.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ('FONT', (0, 0), (-1, -1), 'RobotoLT')
                        ]))

        c.append(t)
        c.append(Spacer(1,10))

        data= [['Costs and Financial Inputs'],]
        t=Table(data,1*[160*mm], 1*[6*mm])
        t.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),

                        ('FONT', (0, 0), (-1, -1), 'Roboto')
                        ]))

        c.append(t)

        data= [['CAPEX'],]
        t=Table(data,1*[160*mm], 1*[6*mm])
        t.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),

                        ('FONT', (0, 0), (-1, -1), 'RobotoLT')
                        ]))

        c.append(t)

        data= [['Sp Electrolyzer and BoP cost [USD/kW]', str(design.elec_cost)],
                ['Sp Development cost [USD/kW]', str(design.develop_cost)],
                ['Installation cost [USD/kW]', str(design.installation_cost)],
                ['Indirect costs [USD/project]', str(design.indirect_cost)]]
        t=Table(data,2*[80*mm], 4*[6*mm])
        t.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ('FONT', (0, 0), (-1, -1), 'RobotoLT')
                        ]))

        c.append(t)

        data= [['OPEX'],]
        t=Table(data,1*[160*mm], 1*[6*mm])
        t.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),

                        ('FONT', (0, 0), (-1, -1), 'RobotoLT')
                        ]))

        c.append(t)

        data= [['Energy cost [USD/MWh]', str(design.energy_cost)],
                ['O&M [USD/kW/year]', str(design.om)],
                ['Water cost [USD/m3]', str(design.water_cost)],
                ['Land cost [USD/ha/year]', str(design.land_cost)]]
        t=Table(data,2*[80*mm], 4*[6*mm])
        t.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ('FONT', (0, 0), (-1, -1), 'RobotoLT')
                        ]))

        c.append(t)

        data= [['Finance'],]
        t=Table(data,1*[160*mm], 1*[6*mm])
        t.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),

                        ('FONT', (0, 0), (-1, -1), 'RobotoLT')
                        ]))

        c.append(t)

        data= [['Equity discount rate [%]', str(design.equity_discount_rate)],
                ['Debt [%]', str(design.debt)],
                ['Debt term [years]', str(design.debt_term)],
                ['Interest Rate [%]', str(design.interest_rate)],
                ['First category Tax [%]', str(design.first_category_tax)],]
        t=Table(data,2*[80*mm], 5*[6*mm])
        t.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ('FONT', (0, 0), (-1, -1), 'RobotoLT')
                        ]))

        c.append(t)

        c.append(Spacer(1,10))
        c.append(Image("apps/static/assets/pdf/head3.png", width=585, height=36))
        c.append(Spacer(1,10))

        data=[['Hydrogen production [tons/year]', number_format(design.results.hydrogen_production)],
                ['Oxygen production [tons/year]', number_format(design.results.oxigen_production)],
                ['Energy consumption [GWh/year]', number_format(design.results.energy_consumption)],
                ['Electrolyzer load factor [%]', number_format(design.results.load_factor)],
                ['Average sp. energy consumption [kWh/kgH2]',number_format(design.results.average_energy_consumption)],
                ['Water consumption [m3/year]',number_format(design.results.water_consumption)],
                ['Energy curtailed [GWh/year]',number_format(design.results.curtailed_energy)],
                ['Energy cost [USD/year]',number_format(design.results.energy_cost)],
                ['Water cost [USD/year]',number_format(design.results.water_cost)]]
        t=Table(data,2*[80*mm], 9*[6*mm])
        t.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ('FONT', (0, 0), (-1, -1), 'RobotoLT')
                        ]))
        c.append(t)

        c.append(Spacer(1,20))
        c.append(Image("apps/static/assets/pdf/head4.png", width=585, height=36))
        c.append(Spacer(1,10))

        lcoh_data = design.results.lcoh_data

        data=[['CAPEX [USD/kgH2]', lcoh_display(lcoh_data,'CAPEX')],
                ['Energy [USD/kgH2]', lcoh_display(lcoh_data,'Energy')],
                ['O&M [USD/kgH2]', lcoh_display(lcoh_data,'O&M')],
                ['Water [USD/kgH2]', lcoh_display(lcoh_data,'Water')],
                ['Land [USD/kgH2]',lcoh_display(lcoh_data,'Land')],
                ['Replacements [USD/kgH2]',lcoh_display(lcoh_data,'Replacements')]]
        t=Table(data,2*[80*mm], 6*[6*mm])
        t.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ('FONT', (0, 0), (-1, -1), 'RobotoLT')
                        ]))
        c.append(t)

        c.append(Spacer(1,20))
        c.append(Image("apps/static/assets/pdf/head5.png", width=585, height=36))
        c.append(Spacer(1,10))

        data=[['Total Capex', number_format(design.results.capex_tot)],
                ['Present Cost of energy for life cycle [USD]', number_format(design.results.nvp_energy_cost)],
                ['Present Cost of O&M for life cycle [USD]', number_format(design.results.nvp_om)],
                ['Present Cost of water for life cycle [USD]', number_format(design.results.nvp_water)],
                ['Present Cost of land for life cycle [USD]',number_format(design.results.nvp_land)],
                ['Present Cost of replacements [USD]',number_format(design.results.present_stack_replacements)],
                ['Stacks replacements [#]',number_format(design.results.stack_replacements)],
                ['Year of replacements',list_formater(design.results.year_of_replacements)],
                ['WACC',number_format(design.results.wacc)],
                ['LCOH [USD/kgH2]',number_format(design.results.lcoh)]]
        t=Table(data,2*[80*mm], 10*[6*mm])
        t.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ('FONT', (0, 0), (-1, -1), 'RobotoLT')
                        ]))
        c.append(t)

        c.append(Spacer(1,100))
        c.append(Image("apps/static/assets/pdf/head6.png",width=585, height=93))


        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "inline; report.pdf"

        SimpleDocTemplate(response, pagesize=A4,
                        rightMargin=0, leftMargin=0,
                        topMargin=10, bottomMargin=20).build(c)
        
        return response