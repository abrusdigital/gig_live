from odoo import models
from datetime import datetime



class AnalysisReportXls(models.AbstractModel):
    _name = 'report.analysis_report.report_analysis_xls'
    _inherit = 'report.report_xlsx.abstract'


    def generate_xlsx_report(self, workbook, data, lines):
        print("lines",lines)
        print("kkkkkkkkkkkkkkkkk",lines.customer_id.name)
        print("Dataaaaaaaaaaaa",data)       
        format1 = workbook.add_format({'font_size': 11, 'align': 'vcenter', 'bold': True})
        format2 = workbook.add_format({'font_size': 10, 'align': 'vcenter'})
        sheet = workbook.add_worksheet('Analysis Report')
        sheet.set_column(1, 0, 30)
        sheet.set_column(6, 0, 30)
        sheet.set_column(6, 1, 30)
        sheet.set_column(6, 2, 30)
        sheet.set_column(6, 3, 30)
        sheet.set_column(6, 6, 30)
        # sheet.set_column(1, 0, 20)
        # sheet.set_column(1, 0, 20)
        # sheet.set_column(1, 0, 20)
        # sheet.set_column(1, 0, 20)
        # sheet.set_column(1, 0, 20)
        sheet.write(1,0, 'Customer:',format1)
        sheet.write(1, 1, lines.customer_id.name, format2)
        sheet.write(2,0, 'Area/Zone:',format1)
        sheet.write(2, 1, lines.area_id.name, format2)
        sheet.write(3,0, 'Building:',format1)
        sheet.write(3, 1, lines.building_id.name, format2)
        
        table_header_left = workbook.add_format(
            {'bg_color': 'black', 'align': 'left', 'font_size': 12,
                'font_color': 'white'})
        table_row_left = workbook.add_format(
            {'align': 'left', 'font_size': 12, 'border': 1})
        table_header_right = workbook.add_format(
                {'bg_color': 'black', 'align': 'right', 'font_size': 12,
                    'font_color': 'white', 'border': 1})
        table_row_right = workbook.add_format(
                {'align': 'right', 'font_size': 12, 'border': 1})        
        table_left = workbook.add_format(
                {'align': 'left', 'bold': True, 'border': 1})
        table_right = workbook.add_format(
                {'align': 'right', 'bold': True, 'border': 1})
        
        
        sheet.write(6, 0, 'Ticket Number', table_header_left)
        sheet.write(6, 1, 'Ticket Name', table_header_right)
        sheet.write(6, 2, 'Ticket Created On', table_header_right)
        sheet.write(6, 3, 'Assigned To', table_header_right)
        sheet.write(6, 4, 'Current Status', table_header_right)
        
        if lines.customer_id:
            rec_data = self.env['helpdesk.ticket'].search([('partner_id', '=', lines.customer_id.id),
                                                            ('create_date','>=',lines['from_date']),('create_date','<=',lines['to_date']),
                                                            ],
                                                            order='id  asc')
            if lines.customer_id and lines.area_id:
                rec_data = self.env['helpdesk.ticket'].search([('partner_id','=',lines.customer_id.id),
                                                               ('create_date','>=',lines['from_date']),('create_date','<=',lines['to_date']),
                                                               ('area_id','=',lines.area_id.id)],order='id  asc')
            if lines.customer_id and lines.building_id:
                rec_data = self.env['helpdesk.ticket'].search([('partner_id','=',lines.customer_id.id),
                                                               ('create_date','>=',lines['from_date']),('create_date','<=',lines['to_date']),
                                                               ('building_id','=',lines.building_id.id)],order='id  asc')
        else:
            rec_data = self.env['helpdesk.ticket'].search([])
        i=7  
        for line in rec_data:
            print(line.create_date)
            print(line._origin.id,"000000000000000000000000000000000")
            sheet.write(i, 0, "#%d"%line._origin.id, table_row_left)
            sheet.write(i, 1, line.name, table_row_left)
            sheet.write(i, 3, line.user_id.name, table_row_left)
            sheet.write(i, 4, line.stage_id.name, table_row_left)
            create_date = datetime.strptime(str(line.create_date), '%Y-%m-%d %H:%M:%S.%f').strftime('%d/%m/%Y')
            sheet.write(i, 2, create_date, table_row_left)
            i = i+1

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
            