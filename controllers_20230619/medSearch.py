def search_medicine():
    searchValue=str(request.vars.searchValue)
    
    keywordStr=''
        
    keywordRows=db((db.medicine_list.brand.contains(searchValue))).select(db.medicine_list.ALL, orderby=db.medicine_list.brand, limitby=(0, 50))
    
    for row in keywordRows:
        id =   str(row.id)
        name =   str(row.name)
        brandName =  str(row.brand)
        genericName = str(row.generic)
        strength = str(row.strength)
        formation = str(row.formation)
        company = str(row.company)
        
        if keywordStr == '':
            keywordStr = id+' | '+name+' | '+brandName+' | '+genericName+' | '+strength+' | '+formation+' | '+company
        else:
            keywordStr += '||' +id+' | '+name+' | '+brandName+' | '+genericName+' | '+strength+' | '+formation+' | '+company
    
    return keywordStr

def search_doctor():
    searchValue=str(request.vars.searchValue)
    
    keywordStr=''
        
    keywordRows=db((db.sm_doctor_area.doc_name.contains(searchValue))).select(db.sm_doctor_area.ALL, orderby=db.sm_doctor_area.doc_name, limitby=(0, 50))
    
    for row in keywordRows:  
        doctorId = str(row.doc_id)
        doctorName = str(row.doc_name)
        doctorAreaId = str(row.area_id)     
        address = str(row.address) 
        #introduction = str(row.introduction)      
        
        if keywordStr == '':
            keywordStr = doctorId+'-'+doctorName+'-'+doctorAreaId+'-'+address
        else:
            keywordStr += '||' + doctorId+'-'+doctorName+'-'+doctorAreaId+'-'+address
    
    return keywordStr