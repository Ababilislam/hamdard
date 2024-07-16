

from random import randint
#---------------------------- ADD VALIDATION
def validation_doctor_route_add(form):
    c_id = session.cid
    doc_id = str(form.vars.doc_id).strip().upper()
    area_id = str(form.vars.area_id).strip().upper()
    client_id = str(form.vars.client_id).strip().upper()

    #------- check duplicate
    existRows = db((db.sm_doctor_area.cid == c_id) & (db.sm_doctor_area.doc_id == doc_id) & (db.sm_doctor_area.area_id == area_id)).select(db.sm_doctor_area.doc_id, limitby=(0, 1))
    if existRows:
        form.errors.doc_id = ''
        response.flash = 'doctor-route, already exist'
    else:
        docName = ''
        doctorRows = db((db.sm_doctor.cid == c_id) & (db.sm_doctor.doc_id == doc_id)).select(db.sm_doctor.doc_name, limitby=(0, 1))
        if not doctorRows:
            form.errors.doc_id = 'Invalid doctor'
        else:
            docName = doctorRows[0].doc_name

            #---
            route_name = ''
            if session.user_type=='Depot':
                levelRow = db((db.sm_level.cid == c_id) & (db.sm_level.level_id == area_id) & (db.sm_level.is_leaf == '1') & (db.sm_level.depot_id == session.depot_id)).select(db.sm_level.level_name, db.sm_level.depot_id, limitby=(0, 1))
            else:
                levelRow = db((db.sm_level.cid == c_id) & (db.sm_level.level_id == area_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_name, db.sm_level.depot_id, limitby=(0, 1))
                
            if not levelRow:
                form.errors.area_id = 'Invalid route'
            else:
                route_name = levelRow[0].level_name
                depot_id = levelRow[0].depot_id
                
                if session.user_type=='Supervisor':
                    if depot_id not in session.distributorList:
                        form.errors.area_id = 'Invalid route'
                    else:
                        pass                    
                else:
                    pass
                
                #---
                if client_id != '':
                    client_area = ''
                    client_name = ''
                    clientRow = db((db.sm_client.cid == c_id) & (db.sm_client.client_id == client_id)).select(db.sm_client.area_id, db.sm_client.name, limitby=(0, 1))
                    if not clientRow:
                        form.errors.client_id = 'Invalid client'
                    else:
                        client_area = clientRow[0].area_id
                        client_name = clientRow[0].name
                        
                        if (client_area != area_id):
                            form.errors.client_id = 'Invalid client in the route'
                        else:
                            form.vars.client_id = client_id
                            form.vars.client_name = client_name
                else:
                    form.vars.client_id = ''
                    form.vars.client_name = ''

                form.vars.doc_id = doc_id
                form.vars.doc_name = docName
                form.vars.area_id = area_id
                form.vars.area_name = route_name
                form.vars.depot_id = depot_id

#---------------------------- ADD
def doctor_route_add():
    task_id = 'rm_doctor_manage'
    task_id_view = 'rm_doctor_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))
        
    response.title = 'Doctor Chamber/Route'
    
    c_id = session.cid
    #   ---------------------
    form = SQLFORM(db.sm_doctor_area,
                  fields=['doc_id', 'area_id', 'client_id', 'address','field2'],
                  submit_button='Save'
                  )

    form.vars.cid = c_id
    if form.accepts(request.vars, session, onvalidation=validation_doctor_route_add):
       response.flash = 'Submitted Successfully'
       
    #  ---------------filter-------
    btn_filter_docroute = request.vars.btn_filter
    btn_all = request.vars.btn_filter_all
    reqPage = len(request.args)
    if btn_filter_docroute:
        session.btn_filter_docroute = btn_filter_docroute
        session.searchType_docroute = str(request.vars.search_type).strip()
        session.searchValue_docroute = str(request.vars.search_value).strip().upper()
        reqPage = 0

    elif btn_all:
        session.btn_filter_docroute = None
        session.searchType_docroute = None
        session.searchValue_docroute = None
        reqPage = 0
        
    #--------paging
    if reqPage:
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = session.items_per_page
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    #--------end paging

    qset=db()
    qset = qset(db.sm_doctor_area.cid == c_id)
    
    #---- supervisor
    if session.user_type=='Supervisor':
        level_id=session.level_id
        depthNo=session.depthNo
        level = 'level' + str(depthNo)
        
        qset=qset((db.sm_level.cid==session.cid)&(db.sm_level.is_leaf=='1')& (db.sm_level[level] == level_id)&(db.sm_level.level_id==db.sm_doctor_area.area_id))
        
    else:
        qset=qset((db.sm_level.cid==session.cid)&(db.sm_level.is_leaf=='1')&(db.sm_level.level_id==db.sm_doctor_area.area_id))
    
    #---- 
    if session.user_type=='Depot':
        qset=qset(db.sm_doctor_area.depot_id==session.depot_id)
    #----
    
    if (session.btn_filter_docroute):
        if (session.searchType_docroute == 'DocID'):
            searchValue=str(session.searchValue_docroute).split('|')[0] 
            qset = qset(db.sm_doctor_area.doc_id == searchValue)
            
        elif (session.searchType_docroute == 'DepotID'):
            if session.user_type != 'Depot':
                searchValue=str(session.searchValue_docroute).split('|')[0] 
                qset = qset(db.sm_doctor_area.depot_id == searchValue)
                
        elif (session.searchType_docroute == 'RouteID'):
            searchValue=str(session.searchValue_docroute).split('|')[0]
            qset = qset(db.sm_doctor_area.area_id == searchValue)
        
        elif (session.searchType_docroute == 'Region'):
            searchValue=str(session.searchValue_docroute).split('|')[0]
            qset = qset(db.sm_level.level0==searchValue)
    
    records = qset.select(db.sm_doctor_area.ALL,db.sm_level.level0, orderby=db.sm_doctor_area.doc_id, limitby=limitby)
    totalCount=qset.count()
    
    return dict(form=form, records=records,totalCount=totalCount, page=page, items_per_page=items_per_page, access_permission=access_permission)

#---------------------------- ADD
def download_doctor_route():
    task_id = 'rm_doctor_manage'
    task_id_view = 'rm_doctor_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL('doctor_route_add'))
        
    
    c_id = session.cid
    #   ---------------------
    
    #  ---------------filter-------
    btn_filter_docroute = request.vars.btn_filter
    btn_all = request.vars.btn_filter_all
    reqPage = len(request.args)
    if btn_filter_docroute:
        session.btn_filter_docroute = btn_filter_docroute
        session.searchType_docroute = str(request.vars.search_type).strip()
        session.searchValue_docroute = str(request.vars.search_value).strip().upper()
        reqPage = 0

    elif btn_all:
        session.btn_filter_docroute = None
        session.searchType_docroute = None
        session.searchValue_docroute = None
        reqPage = 0

    #--------

    qset=db()
    qset = qset(db.sm_doctor_area.cid == c_id)
    
    #---- supervisor
    if session.user_type=='Supervisor':
        level_id=session.level_id
        depthNo=session.depthNo
        level = 'level' + str(depthNo)
        
        qset=qset((db.sm_level.cid==session.cid)&(db.sm_level.is_leaf=='1')& (db.sm_level[level] == level_id)&(db.sm_level.level_id==db.sm_doctor_area.area_id))
        
    else:
        qset=qset((db.sm_level.cid==session.cid)&(db.sm_level.is_leaf=='1')&(db.sm_level.level_id==db.sm_doctor_area.area_id))
    
    #---- 
    if session.user_type=='Depot':
        qset=qset(db.sm_doctor_area.depot_id==session.depot_id)  
    
    #---- 
    
    if (session.btn_filter_docroute):
        if (session.searchType_docroute == 'DocID'):
            searchValue=str(session.searchValue_docroute).split('|')[0] 
            qset = qset(db.sm_doctor_area.doc_id == searchValue)
            
        elif (session.searchType_docroute == 'DepotID'):
            if session.user_type != 'Depot':
                searchValue=str(session.searchValue_docroute).split('|')[0] 
                qset = qset(db.sm_doctor_area.depot_id == searchValue)
                
        elif (session.searchType_docroute == 'RouteID'):
            searchValue=str(session.searchValue_docroute).split('|')[0]
            qset = qset(db.sm_doctor_area.area_id == searchValue)
        
        elif (session.searchType_docroute == 'Region'):
            searchValue=str(session.searchValue_docroute).split('|')[0]
            qset = qset(db.sm_level.level0==searchValue)
    else:
        session.flash = 'Filter Required'
        redirect (URL('doctor_route_add'))
    
    qset=qset(db.sm_doctor.cid == c_id)
    qset=qset(db.sm_doctor.doc_id==db.sm_doctor_area.doc_id)
    
    records = qset.select(db.sm_doctor_area.ALL,db.sm_level.level0,db.sm_doctor.specialty,db.sm_doctor.attached_institution,db.sm_doctor.designation,db.sm_doctor.dob,db.sm_doctor.doctors_category, orderby=db.sm_doctor_area.doc_id)
    
    #---------
    myString='Doctor Chamber/Route List \n\n'
    myString+='Doctor ID,Doctor Name,Chamber/Route ID,Chamber/Route Name,Depot,RegionID,Chemist/Client ID,Chemist/Client Name,Address,Visit Frequency,Doctors Specialty,Doctors Attached Institution,Doctors Designation,Doctors DOB,Doctors Category\n'
    for rec in records:
        doc_id=str(rec.sm_doctor_area.doc_id)
        doc_name=str(rec.sm_doctor_area.doc_name).replace(',', ' ')
        area_id=str(rec.sm_doctor_area.area_id)
        area_name=str(rec.sm_doctor_area.area_name).replace(',', ' ')
        depot_id=str(rec.sm_doctor_area.depot_id)
        level0=str(rec.sm_level.level0)
        client_id=str(rec.sm_doctor_area.client_id)
        client_name=str(rec.sm_doctor_area.client_name).replace(',', ' ')
        address=str(rec.sm_doctor_area.address).replace(',', ' ')
        visit_frequency=str(rec.sm_doctor_area.field2)
        
        specialty=str(rec.sm_doctor.specialty).replace(',', ';')
        attached_institution=str(rec.sm_doctor.attached_institution).replace(',', ';')
        designation=str(rec.sm_doctor.designation).replace(',', ';')
        dob=str(rec.sm_doctor.dob).replace(',', ';')
        doctors_category=str(rec.sm_doctor.doctors_category).replace(',', ';')
        
        myString+=doc_id+','+doc_name+','+area_id+','+area_name+',`'+depot_id+','+level0+','+client_id+','+client_name+','+address+','+visit_frequency+','+specialty+','+attached_institution+','+designation+','+dob+','+doctors_category+'\n'
        
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_doctor_chamber.csv'   
    return str(myString)


#---------------------------- EDIT VALIDATION
def validation_doctor_route_edit(form):
    c_id = session.cid
    area_id = str(form.vars.area_id).strip().upper()
    client_id = str(form.vars.client_id).strip().upper()
    
    #---
    if client_id != '':
        client_area = ''
        client_name = ''
        
        clientRow = db((db.sm_client.cid == c_id) & (db.sm_client.client_id == client_id)).select(db.sm_client.area_id, db.sm_client.name, limitby=(0, 1))
        
        if not clientRow:
            form.errors.client_id = 'Invalid client'
        else:
            client_area = str(clientRow[0].area_id).strip()
            client_name = clientRow[0].name
            
            if (client_area != area_id):
                form.errors.client_id = 'Invalid client in the route'
            else:
                form.vars.client_id = client_id
                form.vars.client_name = client_name
    else:
        form.vars.client_id = ''
        form.vars.client_name = ''

#---------------------------- EDIT
def doctor_route_edit():
    task_id = 'rm_doctor_manage'
    access_permission = check_role(task_id)
    if (access_permission == False):
        session.flash = 'Access is Denied !'
        redirect (URL('doctor_route_add'))
        
    #   ---------------------
    response.title = 'Doctor Chamber/Route -Edit'
    
    c_id = session.cid
    
    page = request.args(0)
    rowID = request.args(1)
    docID = request.args(2)
    routeID = request.args(3)
    
    record = db.sm_doctor_area(rowID) or redirect(URL('doctor_route_add'))
    
    form = SQLFORM(db.sm_doctor_area,
                  record=record,
                  deletable=True,
                  fields=['area_id', 'client_id', 'address','field2'],
                  submit_button='Update'
                  )
    
    if form.accepts(request.vars, session, onvalidation=validation_doctor_route_edit):
        response.flash = 'Updated Successfully'
        redirect(URL('doctor_route_add', args=[page]))

    docRow = db((db.sm_doctor_area.cid == c_id) & (db.sm_doctor_area.doc_id == docID) & (db.sm_doctor_area.area_id == routeID)).select(db.sm_doctor_area.doc_name, db.sm_doctor_area.area_id, db.sm_doctor_area.area_name, db.sm_doctor_area.client_name, db.sm_doctor_area.depot_id, limitby=(0, 1))
    
    return dict(form=form, page=page, docID=docID, rowID=rowID, docRow=docRow)

#---------------------------- EDIT
def doctor_details():
    task_id = 'rm_doctor_manage'
    task_id_view = 'rm_doctor_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL('doctor_route_add'))
        
    #   ---------------------
    response.title = 'Doctor Details'
    
    c_id = session.cid
    
    page = request.args(0)
    docID = request.args(1)
    
    docRow = db((db.sm_doctor.cid == c_id) & (db.sm_doctor.doc_id == docID)).select(db.sm_doctor.ALL, limitby=(0, 1))
    if not docRow:
        session.flash = 'Invalid Doctor'
        redirect (URL('doctor_route_add'))
        
    docChamberRows = db((db.sm_doctor_area.cid == c_id) & (db.sm_doctor_area.doc_id == docID)).select(db.sm_doctor_area.ALL)
    if not docChamberRows:
        session.flash = 'Doctor Chamber not available'
        redirect (URL('doctor_route_add'))
    
    return dict(page=page, docRow=docRow,docChamberRows=docChamberRows)


def batch_upload_doctor_route():
    task_id = 'rm_doctor_manage'
    task_id_view = 'rm_doctor_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL('doctor_route_add'))

    #----------
    response.title = 'Doctor Route Batch Upload'

    c_id = session.cid

    btn_upload = request.vars.btn_upload
    count_inserted = 0
    count_error = 0
    error_str = ''
    total_row = 0
    if btn_upload == 'Upload':
        excel_data = str(request.vars.excel_data)
        inserted_count = 0
        error_count = 0
        error_list = []
        row_list = excel_data.split('\n')
        total_row = len(row_list)

        doc_list_excel = []
        docRoute_list_exist = []
        excelList = []
        compositefd3_list_excel = []

        route_list_excel = []
        client_list_excel = []

        doc_list_valid = []
        route_list_valid = []
        client_list_valid = []

        ins_list = []
        ins_dict = {}

        for i in range(total_row):
            if i >= 100:
                break
            else:
                row_data = row_list[i]
                coloum_list = row_data.split('\t')
                if len(coloum_list) == 4:
                    docID = str(coloum_list[0]).strip().upper()
                    if docID not in doc_list_excel:
                        doc_list_excel.append(docID)

                    routeID = str(coloum_list[1]).strip().upper()
                    if routeID not in route_list_excel:
                        route_list_excel.append(routeID)

                    clientID = str(coloum_list[2]).strip().upper()
                    if clientID not in client_list_excel:
                        client_list_excel.append(clientID)

        validDocRows = db((db.sm_doctor.cid == c_id) & (db.sm_doctor.doc_id.belongs(doc_list_excel))).select(db.sm_doctor.doc_id, db.sm_doctor.doc_name, orderby=db.sm_doctor.doc_id)
        doc_list_valid = validDocRows.as_list()
        
        #----------------------------
        if session.user_type=='Depot':
            validRouteRows = db((db.sm_level.cid == c_id) & (db.sm_level.level_id.belongs(route_list_excel)) & (db.sm_level.is_leaf == '1') & (db.sm_level.depot_id == session.depot_id)).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)
        else:
            validRouteRows = db((db.sm_level.cid == c_id) & (db.sm_level.level_id.belongs(route_list_excel)) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)
        route_list_valid = validRouteRows.as_list()
        
        #----------------------------
        if session.user_type=='Depot':
            validClientRows = db((db.sm_client.cid == c_id) & (db.sm_client.client_id.belongs(client_list_excel)) & (db.sm_client.depot_id == session.depot_id)).select(db.sm_client.client_id, db.sm_client.name,db.sm_client.area_id,  orderby=db.sm_client.client_id)
        else:
            validClientRows = db((db.sm_client.cid == c_id) & (db.sm_client.client_id.belongs(client_list_excel))).select(db.sm_client.client_id, db.sm_client.name,db.sm_client.area_id,  orderby=db.sm_client.client_id)
        client_list_valid = validClientRows.as_list()
        
        #   --------------------
        for i in range(total_row):
            if i >= 100:
                break
            else:
                row_data = row_list[i]
            coloum_list = row_data.split('\t')
            
            if len(coloum_list) == 4:
                doc_id = str(coloum_list[0]).strip().upper()
                route_id = str(coloum_list[1]).strip().upper()
                client_id = str(coloum_list[2]).strip().upper()
                address = str(coloum_list[3]).strip()

                if not(doc_id == '' or route_id == ''):
                    try:
                        duplicate_doc = False
                        
                        #----------- check duplicate
                        existRows = db((db.sm_doctor_area.cid == c_id) & (db.sm_doctor_area.doc_id == doc_id) & (db.sm_doctor_area.area_id == route_id)).select(db.sm_doctor_area.doc_id, limitby=(0, 1))
                        if existRows:
                            duplicate_doc = True
                            
                        #-----------------
                        if(duplicate_doc == False):
                            validDoctor = False
                            #----------- check doctor
                            for i in range(len(doc_list_valid)):
                                myRowData = doc_list_valid[i]
                                docId = myRowData['doc_id']
                                docName = myRowData['doc_name']
                                if (str(docId).strip() == doc_id):
                                    validDoctor = True
                                    break

                            if validDoctor == True:
                                validRoute = False
                                routeId=''
                                #----------- check route
                                for i in range(len(route_list_valid)):
                                    myRowData = route_list_valid[i]
                                    routeId = myRowData['level_id']
                                    route_name = myRowData['level_name']
                                    depot_id = myRowData['depot_id']
                                    if (str(routeId).strip() == route_id):
                                        if session.user_type=='Supervisor':
                                            if routeId in session.marketList:
                                                validRoute = True
                                                break
                                            else:
                                                continue
                                        else:
                                            validRoute = True
                                            break
                                
                                if validRoute == True:
                                    if client_id == '':
                                        insRes = db.sm_doctor_area.insert(cid=c_id, doc_id=doc_id, doc_name=docName, area_id=routeId, area_name=route_name, address=address, depot_id=depot_id)
                                        if insRes:
                                            count_inserted += 1
                                        else:
                                            error_data = row_data + '(process error)\n'
                                            error_str = error_str + error_data
                                            count_error += 1
                                            continue
                                        
                                    else:
                                        validClient = False
                                        #----------- check client
                                        for i in range(len(client_list_valid)):
                                            myRowData = client_list_valid[i]
                                            clientId = myRowData['client_id']
                                            client_name = myRowData['name']
                                            client_route = myRowData['area_id']
                                            if (str(clientId).strip() == client_id):                                                
                                                if str(client_route).strip() == str(routeId).strip():
                                                    validClient = True
                                                    break
                                                else:
                                                    continue                                                    
                                        
                                        if validClient == True:
                                            insRes = db.sm_doctor_area.insert(cid=c_id, doc_id=doc_id, doc_name=docName, area_id=routeId, area_name=route_name, client_id=clientId, client_name=client_name, address=address, depot_id=depot_id)
                                            if insRes:
                                                count_inserted += 1
                                            else:
                                                error_data = row_data + '(process error)\n'
                                                error_str = error_str + error_data
                                                count_error += 1
                                                continue
                                        else:
                                            error_data = row_data + '(invalid client)\n'
                                            error_str = error_str + error_data
                                            count_error += 1
                                            continue
                                else:
                                    error_data = row_data + '(invalid route)\n'
                                    error_str = error_str + error_data
                                    count_error += 1
                                    continue
                            else:
                                error_data = row_data + '(invalid doctor)\n'
                                error_str = error_str + error_data
                                count_error += 1
                                continue
                        else:
                            error_data = row_data + '(already exist)\n'
                            error_str = error_str + error_data
                            count_error += 1
                            continue
                    except:
                        error_data = row_data + '(error in process)\n'
                        error_str = error_str + error_data
                        count_error += 1
                        continue
                else:
                    error_data = row_data + '(DoctorID and RouteID needed)\n'
                    error_str = error_str + error_data
                    count_error += 1
                    continue
            else:
                error_data = row_data + '(4 columns need in a row)\n'
                error_str = error_str + error_data
                count_error += 1
                continue

        if error_str == '':
            error_str = 'No error'

    return dict(count_inserted=count_inserted, count_error=count_error, error_str=error_str, total_row=total_row)


#=============================

