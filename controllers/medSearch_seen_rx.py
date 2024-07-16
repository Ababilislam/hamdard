def validation_med_add(form):
    c_id = session.cid
    brand = check_special_char(form.vars.brand).strip()
    generic = check_special_char(form.vars.generic).strip()
    strength = check_special_char(form.vars.strength).strip()
    company=check_special_char(form.vars.company).strip()
    
    form.vars.name = str(brand)+' '+str(generic)+' '+str(strength)+' '+str(company)
    

def med_add():
    task_id = 'rm_doctor_manage'
    task_id_view = 'rm_doctor_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (access_permission_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='doctor_list'))

    
    c_id = session.cid
    response.title='Medicine'
    
    #  ---------------filter-------
    btn_filter_med = request.vars.btn_filter
    btn_all = request.vars.btn_filter_all
    btn_delete = request.vars.btn_delete
    reqPage = len(request.args)
    
    if btn_filter_med:
        session.btn_filter_med = btn_filter_med
        session.searchType_med = str(request.vars.search_type).strip()
        session.searchValue_med = str(request.vars.search_value).strip()
        reqPage = 0
    elif btn_all:
        session.btn_filter_med = None
        session.searchType_med = None
        session.searchValue_med = None
        reqPage = 0
    
    
    if btn_delete:
        record_id=request.args[1]        
        db((db.medicine_list.id==record_id)).delete()    
        response.flash='Update Successfully'
    
        
    #--------paging
    if reqPage:
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = session.items_per_page
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    #--------end paging


    form = SQLFORM(db.medicine_list,
                  fields=['brand', 'generic', 'strength', 'formation', 'company'],
                  submit_button='Save'
                  )


    if form.accepts(request.vars, session, onvalidation=validation_med_add):
       response.flash = 'Submitted Successfully'

   
    qset = db()    
    if (session.btn_filter_med):
        if (session.searchType_med == 'medBrand'):
            searchValue=str(session.searchValue_med).strip()          
            qset = qset(db.medicine_list.brand.contains(searchValue))
        
        elif (session.searchType_med == 'medGeneric'):
            searchValue=str(session.searchValue_med).strip()          
            qset = qset(db.medicine_list.generic==searchValue)
            
    records =qset.select(db.medicine_list.id,db.medicine_list.brand,db.medicine_list.generic,db.medicine_list.strength,db.medicine_list.formation,db.medicine_list.company, orderby=db.medicine_list.brand,limitby=limitby)            
    recordCountRows=qset.select(db.medicine_list.id.count())
    recordCount=0
    if recordCountRows:
       recordCount=recordCountRows[0][db.medicine_list.id.count()]
    
    return dict(records=records,form=form,page=page,items_per_page=items_per_page,recordCount=recordCount)

def mdicineDownload_bak(): 
    
    qset = db()    
    if (session.btn_filter_med):
        if (session.searchType_med == 'medBrand'):
            searchValue=str(session.searchValue_med).strip()          
            qset = qset(db.medicine_list.brand.contains(searchValue))
        
        elif (session.searchType_med == 'medGeneric'):
            searchValue=str(session.searchValue_med).strip()          
            qset = qset(db.medicine_list.generic==searchValue)
    
    records = qset.select(db.medicine_list.ALL,orderby=db.medicine_list.brand)
    

    myString='Medicine List \n\n'
    myString+='Brand,Generic,Strength,Formation,Company\n'
    for rec in records:
        #name=str(rec.name)
        brand=str(rec.brand)
        generic=str(rec.generic)
        strength=str(rec.strength)
        formation=str(rec.formation)
        company=str(rec.company)
        
        
        myString+=brand+','+generic+','+strength+','+formation+','+company+'\n'
        
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_medicine.csv'   
    return str(myString)

#def search_medicine():
#    searchValue=str(request.vars.searchValue)
#    
#    keywordStr=''
#        
#    keywordRows=db(db.medicine_list.name.contains(searchValue)).select(db.medicine_list.ALL, orderby=db.medicine_list.brand, limitby=(0, 50))
#    
#    for row in keywordRows:
#        id =   str(row.id)
#        name =   str(row.name)
#        brandName =  str(row.brand)
#        genericName = str(row.generic)
#        strength = str(row.strength)
#        formation = str(row.formation)
#        company = str(row.company)
#        
#        if keywordStr == '':
#            keywordStr = id+' | '+name+' | '+brandName+' | '+genericName+' | '+strength+' | '+formation+' | '+company
#        else:
#            keywordStr += '||' +id+' | '+name+' | '+brandName+' | '+genericName+' | '+strength+' | '+formation+' | '+company
#    
#    return keywordStr


def search_doctor():
    cid=str(request.vars.cid)
    region=str(request.vars.region)
    area=str(request.vars.area)
    tr=str(request.vars.tr)
    category=str(request.vars.category)
    searchValue=str(request.vars.searchValue)
    uid = str(request.vars.uid)

    repTrList=[]
    if tr == '':
        repAreaRows = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.rep_id == uid)).select(db.sm_rep_area.area_id, orderby=db.sm_rep_area.area_id)
        for rRow in repAreaRows:
            area_id=rRow.area_id
            repTrList.append(area_id)


    trList=[]
    lebelRows=db((db.sm_level.cid==cid)&(db.sm_level.parent_level_id==area)).select(db.sm_level.level_id)
    for row in lebelRows:
        trList.append(row.level_id)
        
         
    docStr='' 
    qset=db()
    qset=qset(db.sm_doctor.cid == cid)
    qset = qset(db.sm_doctor.status == 'ACTIVE')
    qset=qset(db.sm_doctor_area.cid == cid)    
    qset=qset(db.sm_doctor_area.doc_id == db.sm_doctor.doc_id)

    if category!='':
        qset=qset(db.sm_doctor.doctors_category == category)        
    
    if area!='':
        qset=qset(db.sm_doctor_area.area_id.belongs(trList))
        
    if tr!='':
        qset=qset(db.sm_doctor_area.area_id == tr)
    else:
        if len(repTrList)>0:
            qset = qset(db.sm_doctor_area.area_id.belongs(repTrList))
        

    if searchValue!='':
        qset=qset((db.sm_doctor_area.doc_name.contains(searchValue))|(db.sm_doctor_area.address.contains(searchValue)) )
        
        docRows = qset.select(db.sm_doctor_area.doc_id,db.sm_doctor_area.doc_name,db.sm_doctor_area.address,db.sm_doctor_area.area_id,orderby=db.sm_doctor_area.doc_name,limitby=(0,100))
    else:      
        docRows = qset.select(db.sm_doctor_area.doc_id,db.sm_doctor_area.doc_name,db.sm_doctor_area.address,db.sm_doctor_area.area_id,orderby=db.sm_doctor_area.doc_name)

    for row in docRows:
        doc_id =   str(row.doc_id)
        doc_name =   str(row.doc_name)
        address =  str(row.address)
        area_id=str(row.area_id)
        
        if docStr == '':
            docStr = doc_id+' | '+doc_name+' | '+address+' | '+area_id
        else:
            docStr += '||' +doc_id+' | '+doc_name+' | '+address+' | '+area_id
    
    return docStr

