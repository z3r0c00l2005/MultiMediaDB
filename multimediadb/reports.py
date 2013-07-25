from geraldo import Report, landscape, ReportBand, ObjectValue, SystemField, BAND_WIDTH, Label, ReportGroup, SubReport, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
import os

class TypesReport(Report):
    title = 'Aircraft Types list'
    author = 'AgustaWestland'
    
    page_size = landscape(A4)
    margin_left = 2*cm
    margin_top = 0.5*cm
    margin_right = 0.5*cm
    margin_bottom = 0.5*cm
    
    class band_page_header(ReportBand):
        height = 2*cm
        elements = [
        Image(left=0*cm, top=0.1*cm, width=5*cm, height=3*cm,filename=os.path.join(os.path.dirname(__file__), 'AW_Logo.jpg')),
            SystemField(expression='%(report_title)s', top=0.1*cm, left=0*cm, width=BAND_WIDTH,
                style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER}),
            SystemField(expression=u'Page %(page_number)d of %(page_count)d', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            ]
        borders = {'bottom': True}

    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
            Label(text='THSS', top=0.1*cm),
            SystemField(expression=u'Printed %(now:%d %b %Y)s at %(now:%H:%M)s', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            ]
        borders = {'top': True}

    class band_detail(ReportBand):
        height = 0.5*cm
    
    groups = [
        ReportGroup(attribute_name = 'name',
            band_header = ReportBand(
                height = 0.7*cm,
                auto_expand_height = True,
                elements = [
                    ObjectValue(attribute_name='name', left=0, top=0.1*cm, width=20*cm,
                        get_value=lambda instance: 'Aircraft Type: ' + (instance.name) + ' - ' + (instance.description),
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 12})
                    ],
                borders = {'bottom': True},
                )
            ),
        ]
    subreports = [
        SubReport(
            queryset_string = '%(object)s.aircraftsystem_set.all()',
            detail_band = ReportBand(
                height=0.5*cm,
                auto_expand_height = True,
                elements=[
                    ObjectValue(attribute_name='name', top=0, left=1*cm),
                    ObjectValue(attribute_name='description', top=0, left=5*cm),
                    ]
                ),
        ),
    ]





class SystemReport(Report):
    title = 'Type'
    author = 'AgustaWestland'

    page_size = landscape(A4)
    margin_left = 2*cm
    margin_top = 0.5*cm
    margin_right = 0.5*cm
    margin_bottom = 0.5*cm
    
    class band_page_header(ReportBand):
        height = 2*cm
        elements = [
        Image(left=0*cm, top=0.1*cm, width=5*cm, height=3*cm,filename=os.path.join(os.path.dirname(__file__), 'AW_Logo.jpg')),
            SystemField(expression='%(report_title)s'+' - '+'%(var:actype)s', top=0.1*cm, left=0*cm, width=BAND_WIDTH,
                style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER}),
            SystemField(expression=u'Page %(page_number)d of %(page_count)d', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            ]
        borders = {'bottom': True}

    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
            Label(text='THSS', top=0.1*cm),
            SystemField(expression=u'Printed %(now:%d %b %Y)s at %(now:%H:%M)s', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            ]
        borders = {'top': True}

    class band_detail(ReportBand):
        height = 0.5*cm
    
    groups = [
        ReportGroup(attribute_name = 'name',
            band_header = ReportBand(
                height = 0.7*cm,
                auto_expand_height = True,
                elements = [
                    ObjectValue(attribute_name='name', left=0, top=0.1*cm, width=20*cm,
                        get_value=lambda instance: 'System: ' + (instance.name) + ' - ' + (instance.description),
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 12})
                    ],
                borders = {'bottom': True},
                )
            ),
        ]
    subreports = [
        SubReport(
            queryset_string = '%(object)s.systemgraphic_set.all()',
            detail_band = ReportBand(
                height=0.5*cm,
                auto_expand_height = True,
                elements=[
                    ObjectValue(attribute_name='media_label', top=0, left=1*cm),
                    ObjectValue(attribute_name='description', top=0, left=10*cm),
                    ]
                ),
        ),
    ]

