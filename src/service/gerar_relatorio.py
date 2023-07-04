from openpyxl import Workbook

def create_relatorio(list_info, path_output):
    workbook = Workbook()
    sheet = workbook.active
    for row in list_info:
        sheet.append(row)
        
    workbook.save(path_output)    
