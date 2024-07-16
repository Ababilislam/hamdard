# ------------------TARGET route and item wise --------------------------
def validation_target_route_item(form):
    cid = session.cid

    year = str(request.vars.year).strip()
    month = str(request.vars.month).strip()

    if year == '' or month == '':
        form.errors.client_id = ''
        response.flash = 'Valid Year-Month required'
    else:
        first_date = year + '-' + month + '-01'

        territory_id = str(request.vars.territory_id).upper().split('-')[0]
        item_id = str(request.vars.item_id).upper().split('-')[0]
        target_qty = request.vars.target_qty

        rows_check = db((db.target_vs_achievement_route_item.cid == cid) & (db.target_vs_achievement_route_item.first_date == first_date) & (
                    db.target_vs_achievement_route_item.territory_id == territory_id) & (
                                    db.target_vs_achievement_route_item.item_id == item_id)).select(
            db.target_vs_achievement_route_item.item_id, limitby=(0, 1))
        if rows_check:
            form.errors.client_id = ''
            response.flash = 'already exist'
        else:
            levelRecords = db((db.sm_level.cid == cid) & (db.sm_level.client_id == territory_id) & (
                        db.sm_level.depth == 3)).select(db.sm_level.name, db.sm_level.level2,
                                                                 db.sm_level.depot_id, limitby=(0, 1))
            if not levelRecords:
                form.errors.territory_id = ''
                response.flash = 'Invalid Route!'
            else:
                itemRecords = db((db.sm_item.cid == cid) & (db.sm_item.item_id == item_id)).select(db.sm_item.item_id,
                                                                                                   db.sm_item.name,
                                                                                                   limitby=(0, 1))
                if not itemRecords:
                    form.errors.client_id = ''
                    response.flash = 'Invalid Item ID!'
                else:
                    if target_qty < 0:
                        form.errors.target_qty = 'Valid Qty required'
                        response.flash = 'Invalid Item ID!'
                    else:
                        client_name = clientRecords[0].name
                        area_id = clientRecords[0].area_id
                        depot_id = clientRecords[0].depot_id

                        item_name = itemRecords[0].name

                        level0_id = ''
                        level1_id = ''
                        level2_id = ''
                        routeRow = db((db.sm_level.cid == cid) & (db.sm_level.level_id == area_id) & (
                                    db.sm_level.is_leaf == '1')).select(db.sm_level.level_name, db.sm_level.level0,
                                                                        db.sm_level.level1, db.sm_level.level2,
                                                                        limitby=(0, 1))
                        if routeRow:
                            market_name = routeRow[0].level_name
                            level0_id = routeRow[0].level0
                            level1_id = routeRow[0].level1
                            level2_id = routeRow[0].level2

                        form.vars.cid = cid
                        form.vars.first_date = first_date
                        form.vars.target_date = first_date

                        #form.vars.client_id = client_id
                        #form.vars.client_name = client_name

                        form.vars.item_id = item_id
                        form.vars.item_name = item_name

                        form.vars.region_id = level0_id
                        form.vars.area_id = level1_id
                        form.vars.territory_id = level2_id
                        #form.vars.market_id = area_id
                        form.vars.depot_id = depot_id


def target_add_route_item():
    task_id = 'rm_target_manage'
    task_id_view = 'rm_target_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect(URL('default', 'home'))

    response.title = 'Target'
    cid = session.cid

    # db.target_vs_achievement.depot_id.requires=IS_IN_DB(db((db.sm_depot.cid==cid)&(db.sm_depot.status=='ACTIVE')),db.sm_depot.depot_id,orderby=db.sm_depot.depot_id)
    form = SQLFORM(db.target_vs_achievement_route_item,
                   fields=['territory_id', 'item_id', 'target_qty'],
                   submit_button='Save'
                   )
    form.vars.cid = cid
    form.vars.target_qty = ''
    if form.accepts(request.vars, session, onvalidation=validation_target_route_item):
        response.flash = 'Submitted Successfully'

    # Cancelled
    btn_delete = request.vars.btn_delete
    if btn_delete:
        record_id = request.args[1]
        check_cancel = request.vars.check_cancel
        if check_cancel != 'YES':
            response.flash = 'Check Confirmation Required'
        else:
            taRecords = db((db.target_vs_achievement_route_item.cid == cid) & (db.target_vs_achievement_route_item.id == record_id) & (
                        db.target_vs_achievement_route_item.achievement_qty == 0)).select(db.target_vs_achievement_route_item.id,
                                                                               limitby=(0, 1))
            if taRecords:
                taRecords[0].delete_record()
            else:
                response.flash = 'Invalid request'

    # ------------------------
    btn_filter_target = request.vars.btn_filter
    btn_all = request.vars.btn_all
    reqPage = len(request.args)
    if btn_filter_target:
        session.btn_filter_target = btn_filter_target
        session.searchType_target = str(request.vars.searchType).strip()
        session.searchValue_target = str(request.vars.searchValue).strip()
        reqPage = 0
    elif btn_all:
        session.btn_filter_target = None
        session.searchType_target = None
        session.searchValue_target = None
        reqPage = 0

    # --------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # --------end paging

    qset = db()
    qset = qset(db.target_vs_achievement_route_item.cid == cid)

    if session.user_type == 'Depot':
        qset = qset(db.target_vs_achievement_route_item.depot_id == session.depot_id)

    if ((session.btn_filter_target) and (session.searchType_target == 'RouteID')):
        qset = qset(db.target_vs_achievement_route_item.territory_id == session.searchValue_target)


    records = qset.select(db.target_vs_achievement_route_item.ALL,
                          orderby=~db.target_vs_achievement_route_item.first_date | db.target_vs_achievement_route_item.territory_id | db.target_vs_achievement_route_item.item_id,
                          limitby=limitby)

    return dict(form=form, records=records, page=page, items_per_page=items_per_page,
                access_permission=access_permission)


# ----------------

def target_batch_upload_route_item():
    task_id = 'rm_target_manage'
    task_id_view = 'rm_target_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect(URL('default', 'home'))

    response.title = 'Target Batch Upload'

    c_id = session.cid

    btn_upload = request.vars.btn_upload
    btn_clean = request.vars.btn_clean

    if btn_clean:
        year = request.vars.clean_year
        month = request.vars.clean_month
        territory_id = str(request.vars.clean_route).upper().split('-')[0]

        if year == '' or month == '':
            response.flash = 'Valid Year-Month required'
        else:
            if territory_id=='':
                response.flash = 'Valid Route required'
            else:
                first_date = year + '-' + month + '-01'
                territory_id = str(request.vars.clean_route).upper().split('-')[0]

                db((db.target_vs_achievement_route_item.cid == c_id) & (db.target_vs_achievement_route_item.first_date == first_date) & (db.target_vs_achievement_route_item.territory_id == territory_id)).delete()

                response.flash = 'Successfully Updated'



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

        route_list_excel = []
        route_list_exist = []
        itemid_list_excel = []
        itemid_list_exist = []

        for i in range(total_row):
            if i >= 500:
                break
            else:
                row_data = row_list[i]
                coloum_list = row_data.split('\t')
                if len(coloum_list) == 4:
                    routeIdExcel = str(coloum_list[1]).strip().upper()
                    itemIdExcel = str(coloum_list[2]).strip().upper()
                    if routeIdExcel not in route_list_excel:
                        route_list_excel.append(routeIdExcel)
                    if itemIdExcel not in itemid_list_excel:
                        itemid_list_excel.append(itemIdExcel)

        #        create client list
        existRouteRows = db((db.sm_level.cid == c_id) & (db.sm_level.level_id.belongs(route_list_excel)) & (
                    db.sm_level.depth == 3)).select(db.sm_level.level_id,db.sm_level.level2, db.sm_level.depot_id,
                                                             orderby=db.sm_level.level_id)
        route_list_exist = existRouteRows.as_list()

        #        create rep list
        existItemRows = db((db.sm_item.cid == c_id) & (db.sm_item.item_id.belongs(itemid_list_excel))).select(
            db.sm_item.item_id, db.sm_item.name, orderby=db.sm_item.item_id)
        itemid_list_exist = existItemRows.as_list()

        #   --------------------
        for i in range(total_row):
            if i >= 500:
                break
            else:
                row_data = row_list[i]
            coloum_list = row_data.split('\t')

            if len(coloum_list) != 4:
                error_data = row_data + '(4 columns need in a row)\n'
                error_str = error_str + error_data
                count_error += 1
                continue
            else:
                date_ex = str(coloum_list[0]).strip()
                routeID_ex = str(coloum_list[1]).strip().upper()
                item_id_ex = str(coloum_list[2]).strip().upper()
                targetqty_ex = str(coloum_list[3]).strip()

                if (date_ex == '' or routeID_ex == '' or item_id_ex == '' or targetqty_ex == ''):
                    error_data = row_data + '(Must value required)\n'
                    error_str = error_str + error_data
                    count_error += 1
                    continue
                else:
                    try:
                        date_ex = datetime.datetime.strptime(date_ex, '%Y-%m-%d')
                    except:
                        error_data = row_data + '(Invalid date)\n'
                        error_str = error_str + error_data
                        count_error += 1
                        continue

                    try:
                        targetqty = int(targetqty_ex)
                        if targetqty <= 0:
                            error_data = row_data + '(Invalid Target)\n'
                            error_str = error_str + error_data
                            count_error += 1
                            continue

                    except:
                        error_data = row_data + '(Invalid Target)\n'
                        error_str = error_str + error_data
                        count_error += 1
                        continue

                    # -----------------------
                    valid_item = False
                    valid_route = False

                    firstDate = str(date_ex)[0:7] + '-01'
                    itemName = ''
                    route_depotId=''

                    for i in range(len(route_list_exist)):
                        myRowData2 = route_list_exist[i]
                        route_id = myRowData2['level_id']
                        if (str(route_id).strip() == str(routeID_ex).strip()):
                            valid_route = True
                            route_depotId=myRowData2['depot_id']
                            break

                    if valid_route == True:  # ---------- check valid client
                        # ----------- check valid spo
                        for i in range(len(itemid_list_exist)):
                            myRowData1 = itemid_list_exist[i]
                            item_id = myRowData1['item_id']
                            if (str(item_id).strip() == str(item_id_ex).strip()):
                                valid_item = True
                                itemName = myRowData1['name']
                                break

                    # -----------------
                    if (valid_route == False):
                        error_data = row_data + '(Invalid Route)\n'
                        error_str = error_str + error_data
                        count_error += 1
                        continue
                    else:
                        if valid_item == False:
                            error_data = row_data + '(Invalid Item)\n'
                            error_str = error_str + error_data
                            count_error += 1
                            continue
                        else:
                            existRow = db((db.target_vs_achievement_route_item.cid == c_id) & (
                                        db.target_vs_achievement_route_item.first_date == firstDate) & (
                                                      db.target_vs_achievement_route_item.territory_id == routeID_ex) & (
                                                      db.target_vs_achievement_route_item.item_id == item_id_ex)).select(
                                db.target_vs_achievement_route_item.item_id, limitby=(0, 1))
                            if existRow:
                                error_data = row_data + '(Already exist)\n'
                                error_str = error_str + error_data
                                count_error += 1
                                continue
                            else:

                                level0_id = ''
                                level0_name = ''
                                level1_id = ''
                                level1_name = ''
                                level2_id = ''
                                level2_name = ''
                                level3_name = ''
                                routeRow = db((db.sm_level.cid == c_id) & (db.sm_level.level_id == routeID_ex) & (
                                            db.sm_level.is_leaf == '1')).select(db.sm_level.level_name,
                                                                                db.sm_level.level0,db.sm_level.level0_name, db.sm_level.level1,db.sm_level.level1_name,
                                                                                db.sm_level.level2,db.sm_level.level2_name, limitby=(0, 1))
                                if routeRow:
                                    level0_id = routeRow[0].level0
                                    level0_name = routeRow[0].level0_name
                                    level1_id = routeRow[0].level1
                                    level1_name = routeRow[0].level1_name
                                    level2_id = routeRow[0].level2
                                    level2_name = routeRow[0].level2_name
                                    level3_name = routeRow[0].level_name

                                price=0
                                category_id=''
                                priceRows=db((db.sm_item.cid == c_id) & (db.sm_item.item_id==item_id_ex)).select(db.sm_item.price,db.sm_item.category_id,limitby=(0,1))
                                if priceRows:
                                    price=priceRows[0].price
                                    category_id = priceRows[0].category_id

                                try:
                                    db.target_vs_achievement_route_item.insert(cid=c_id, first_date=firstDate, target_date=date_ex,
                                                                    item_id=item_id_ex, item_name=itemName,price=price,category_id=category_id,zone_id=level0_id,zone_name=level0_name,
                                                                    region_id=level1_id,region_name=level1_name, area_id=level2_id,area_name=level2_name,
                                                                    territory_id=routeID_ex,territory_name=level3_name,depot_id=route_depotId, target_qty=targetqty)
                                    count_inserted += 1
                                except:
                                    error_data = row_data + '(error in process!)\n'
                                    error_str = error_str + error_data
                                    count_error += 1
                                    continue

        if error_str == '':
            error_str = 'No error'

    return dict(count_inserted=count_inserted, count_error=count_error, error_str=error_str, total_row=total_row)


#------------------TARGET--------------------------
def validation_target(form):
    cid=session.cid
    
    year=str(request.vars.year).strip()
    month=str(request.vars.month).strip()
    
    if year=='' or month=='':
        form.errors.client_id=''                
        response.flash='Valid Year-Month required'
    else:
        first_date=year+'-'+month+'-01'
        
        client_id=str(request.vars.client_id).upper().split('-')[0]
        item_id=str(request.vars.item_id).upper().split('-')[0]
        target_qty=request.vars.target_qty
        
        rows_check=db((db.target_vs_achievement.cid==cid) & (db.target_vs_achievement.first_date==first_date)& (db.target_vs_achievement.client_id==client_id)& (db.target_vs_achievement.item_id==item_id)).select(db.target_vs_achievement.item_id,limitby=(0,1))
        if rows_check:
            form.errors.client_id=''
            response.flash = 'already exist'
        else:
            clientRecords=db((db.sm_client.cid==cid) & (db.sm_client.client_id==client_id)& (db.sm_client.status=='ACTIVE')).select(db.sm_client.name,db.sm_client.area_id,db.sm_client.depot_id,limitby=(0,1))
            if not clientRecords:
                form.errors.client_id=''                
                response.flash='Invalid Client ID!'
            else:
                itemRecords=db((db.sm_item.cid==cid)&(db.sm_item.item_id==item_id)).select(db.sm_item.item_id,db.sm_item.name,limitby=(0,1))
                if not itemRecords:
                    form.errors.client_id=''                
                    response.flash='Invalid Item ID!'
                else:
                    if target_qty<0:
                        form.errors.target_qty='Valid Qty required'                
                        response.flash='Invalid Item ID!'
                    else:
                        client_name=clientRecords[0].name
                        area_id=clientRecords[0].area_id
                        depot_id=clientRecords[0].depot_id
                        
                        item_name=itemRecords[0].name
                        
                        level0_id=''
                        level1_id=''
                        level2_id=''
                        routeRow=db((db.sm_level.cid==cid) & (db.sm_level.level_id==area_id) & (db.sm_level.is_leaf=='1')).select(db.sm_level.level_name,db.sm_level.level0,db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
                        if routeRow:
                            market_name=routeRow[0].level_name
                            level0_id=routeRow[0].level0
                            level1_id=routeRow[0].level1
                            level2_id=routeRow[0].level2
                        
                        form.vars.cid=cid
                        form.vars.first_date=first_date
                        form.vars.target_date=first_date
                        
                        form.vars.client_id=client_id
                        form.vars.client_name=client_name
                        
                        form.vars.item_id=item_id
                        form.vars.item_name=item_name
                                                
                        form.vars.region_id=level0_id
                        form.vars.area_id=level1_id
                        form.vars.territory_id=level2_id
                        form.vars.market_id=area_id
                        form.vars.depot_id=depot_id
                        
                        
def target_add():
    task_id='rm_target_manage'
    task_id_view='rm_target_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (task_id_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    response.title='Target'
    cid=session.cid
    
    #db.target_vs_achievement.depot_id.requires=IS_IN_DB(db((db.sm_depot.cid==cid)&(db.sm_depot.status=='ACTIVE')),db.sm_depot.depot_id,orderby=db.sm_depot.depot_id)
    form =SQLFORM(db.target_vs_achievement,
                  fields=['client_id','item_id','target_qty'],
                  submit_button='Save'
                )
    form.vars.cid=cid
    form.vars.target_qty=''
    if form.accepts(request.vars,session,onvalidation=validation_target):
       response.flash = 'Submitted Successfully'
    
    
    #Cancelled
    btn_delete=request.vars.btn_delete
    if btn_delete:
        record_id=request.args[1]
        check_cancel=request.vars.check_cancel
        if check_cancel!='YES':
            response.flash='Check Confirmation Required'
        else:
            taRecords=db((db.target_vs_achievement.cid==cid)& (db.target_vs_achievement.id==record_id) & (db.target_vs_achievement.achievement_qty==0)).select(db.target_vs_achievement.id,limitby=(0,1))
            if taRecords:
                taRecords[0].delete_record()
            else:
                response.flash='Invalid request'
                
    #------------------------
    btn_filter_target=request.vars.btn_filter
    btn_all=request.vars.btn_all
    reqPage=len(request.args)    
    if btn_filter_target:
        session.btn_filter_target=btn_filter_target
        session.searchType_target=str(request.vars.searchType).strip()
        session.searchValue_target=str(request.vars.searchValue).strip()
        reqPage=0
    elif btn_all:
        session.btn_filter_target=None
        session.searchType_target=None
        session.searchValue_target=None
        reqPage=0
    
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging    
    
    qset=db()
    qset=qset(db.target_vs_achievement.cid==cid)
    
    if session.user_type=='Depot':
        qset=qset(db.target_vs_achievement.depot_id==session.depot_id)
        
        
    if ((session.btn_filter_target) and (session.searchType_target=='ClientID')):
        qset=qset(db.target_vs_achievement.client_id==session.searchValue_target)  
    
    elif ((session.btn_filter_target) and (session.searchType_target=='Status')):
        qset=qset(db.target_vs_achievement.status==session.searchValue_target)  
        
    records=qset.select(db.target_vs_achievement.ALL,orderby=~db.target_vs_achievement.first_date|db.target_vs_achievement.client_id|db.target_vs_achievement.item_id,limitby=limitby)
    
    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)


#----------------

def target_batch_upload():
    task_id = 'rm_target_manage'
    task_id_view = 'rm_target_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect(URL('default', 'home'))
    
    response.title='Target Batch Upload'
    
    c_id=session.cid
    
    btn_upload=request.vars.btn_upload    
    count_inserted=0
    count_error=0
    error_str=''
    total_row=0
    if btn_upload=='Upload':        
        excel_data=str(request.vars.excel_data)
        inserted_count=0
        error_count=0
        error_list=[]
        row_list=excel_data.split( '\n')
        total_row=len(row_list)
        
        client_list_excel=[]
        client_list_exist=[]
        itemid_list_excel=[]
        itemid_list_exist=[]
        
                
        for i in range(total_row):
            if i>=50:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==4:
                    clientIdExcel=str(coloum_list[1]).strip().upper()
                    itemIdExcel=str(coloum_list[2]).strip().upper()
                    if clientIdExcel not in client_list_excel:
                        client_list_excel.append(clientIdExcel)
                    if itemIdExcel not in itemid_list_excel:
                        itemid_list_excel.append(itemIdExcel)
        
        
        #        create client list
        existClientRows=db((db.sm_client.cid==c_id)&(db.sm_client.client_id.belongs(client_list_excel))&(db.sm_client.status=='ACTIVE')).select(db.sm_client.client_id,db.sm_client.name,db.sm_client.area_id,db.sm_client.depot_id,orderby=db.sm_client.client_id)
        client_list_exist=existClientRows.as_list()
        
        #        create rep list
        existItemRows=db((db.sm_item.cid==c_id)&(db.sm_item.item_id.belongs(itemid_list_excel))).select(db.sm_item.item_id,db.sm_item.name,orderby=db.sm_item.item_id)
        itemid_list_exist=existItemRows.as_list()            
        
        #   --------------------     
        for i in range(total_row):
            if i>=50: 
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')            
            
            if len(coloum_list)!=4:
                error_data=row_data+'(4 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
            else:
                date_ex=str(coloum_list[0]).strip()                
                clID_ex=str(coloum_list[1]).strip().upper()
                item_id_ex=str(coloum_list[2]).strip().upper()
                targetqty_ex=str(coloum_list[3]).strip()
                
                
                if (date_ex=='' or clID_ex=='' or item_id_ex=='' or targetqty_ex==''):
                    error_data=row_data+'(Must value required)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                else:                                        
                    try:
                        date_ex=datetime.datetime.strptime(date_ex,'%Y-%m-%d')
                    except:
                        error_data=row_data+'(Invalid date)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    
                    
                    try:
                        targetqty=int(targetqty_ex)
                        if targetqty<=0:
                            error_data=row_data+'(Invalid Target)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        
                    except:
                        error_data=row_data+'(Invalid Target)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                        
                    
                    #-----------------------
                    valid_item=False
                    valid_client=False
                    
                    firstDate=str(date_ex)[0:7]+'-01'                    
                    clientName=''
                    itemName=''
                    client_areaId=''
                    client_depotId=''
                    
                    for i in range(len(client_list_exist)):
                        myRowData2=client_list_exist[i]                        
                        client_id=myRowData2['client_id']                            
                        if (str(client_id).strip()==str(clID_ex).strip()):
                            valid_client=True
                            clientName=myRowData2['name']
                            client_areaId=myRowData2['area_id']
                            client_depotId=myRowData2['depot_id']
                            break
                    
                    if valid_client==True:#---------- check valid client
                        #----------- check valid spo                                                      
                        for i in range(len(itemid_list_exist)):
                            myRowData1=itemid_list_exist[i]                                
                            item_id=myRowData1['item_id']
                            if (str(item_id).strip()==str(item_id_ex).strip()):
                                valid_item=True
                                itemName=myRowData1['name']
                                break
                    
                    #-----------------
                    if(valid_client==False):
                        error_data=row_data+'(Invalid Client/Retailer)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue                        
                    else:
                        if valid_item==False:
                            error_data=row_data+'(Invalid Item)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:
                            existRow=db((db.target_vs_achievement.cid==c_id) & (db.target_vs_achievement.first_date==firstDate)& (db.target_vs_achievement.client_id==clID_ex)& (db.target_vs_achievement.item_id==item_id_ex)).select(db.target_vs_achievement.item_id,limitby=(0,1))
                            if existRow :
                                error_data=row_data+'(Already exist)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                            else:
                                
                                level0_id=''
                                level1_id=''
                                level2_id=''
                                routeRow=db((db.sm_level.cid==c_id) & (db.sm_level.level_id==client_areaId) & (db.sm_level.is_leaf=='1')).select(db.sm_level.level_name,db.sm_level.level0,db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
                                if routeRow:
                                    market_name=routeRow[0].level_name
                                    level0_id=routeRow[0].level0
                                    level1_id=routeRow[0].level1
                                    level2_id=routeRow[0].level2
                                    
                                try:
                                    db.target_vs_achievement.insert(cid=c_id,first_date=firstDate,target_date=date_ex,client_id=clID_ex,client_name=clientName,item_id=item_id_ex,item_name=itemName,region_id=level0_id,area_id=level1_id,territory_id=level2_id,market_id=client_areaId,depot_id=client_depotId,target_qty=targetqty)
                                    count_inserted+=1
                                except:
                                    error_data=row_data+'(error in process!)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue            
        
        if error_str=='':
            error_str='No error'
            
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)

def lifting_plan_add():
    task_id='rm_liftingplan_manage'
    task_id_view='rm_liftingplan_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (task_id_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    response.title='Lifting Plan'
    cid=session.cid
    
    
    #Cancelled
    btn_delete=request.vars.btn_delete
    if btn_delete:
        record_id=request.args[1]
        check_cancel=request.vars.check_cancel
        if check_cancel!='YES':
            response.flash='Check Confirmation Required'
        else:
            taRecords=db((db.lifting_plan.cid==cid)& (db.lifting_plan.id==record_id)).select(db.lifting_plan.id,limitby=(0,1))
            if taRecords:
                taRecords[0].delete_record()
            else:
                response.flash='Invalid request'
                
    #------------------------
    btn_filter_lp=request.vars.btn_filter
    btn_all=request.vars.btn_all
    reqPage=len(request.args)    
    if btn_filter_lp:
        session.btn_filter_lp=btn_filter_lp
        session.searchType_lp=str(request.vars.searchType).strip()
        session.searchValue_lp=str(request.vars.searchValue).strip()
        reqPage=0
    elif btn_all:
        session.btn_filter_lp=None
        session.searchType_lp=None
        session.searchValue_lp=None
        reqPage=0
    
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging    
    
    qset=db()
    qset=qset(db.lifting_plan.cid==cid)
    if session.user_type=='Depot':
        qset=qset(db.lifting_plan.distributor_id==session.depot_id)
    
    
    if ((session.btn_filter_lp) and (session.searchType_lp=='DistributorID')):
        if session.user_type!='Depot':
            qset=qset(db.lifting_plan.distributor_id==session.searchValue_lp)  
    
    elif ((session.btn_filter_lp) and (session.searchType_lp=='SuperDepotID')):
        qset=qset(db.lifting_plan.super_depot_id==session.searchValue_lp)  
        
    records=qset.select(db.lifting_plan.ALL,orderby=~db.lifting_plan.first_date|db.lifting_plan.distributor_id,limitby=limitby)
    
    return dict(records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)


#---------------------------- EDIT
#def lifting_plan_details():
#    task_id='rm_liftingplan_manage'
#    task_id_view='rm_liftingplan_view'
#    access_permission=check_role(task_id)
#    access_permission_view=check_role(task_id_view)
#    if (access_permission==False) and (task_id_view==False):
#        session.flash='Access is Denied !'
#        redirect (URL('default','home'))
#        
#    #   --------------------- 
#    response.title='Lifting Plan Details'
#    
#    c_id=session.cid
#    
#    page=request.args(0)
#    rowID=request.args(1)
#    
#    
#    records=db((db.lifting_plan.cid==c_id)&(db.lifting_plan.id==rowID)).select(db.lifting_plan.ALL,limitby=(0,1))
#    if not records:
#        session.flash = 'Invalid request'
#        redirect(URL('lifting_plan_add',args=[page]))
#    else:
#        pass
#    
#    return dict(page=page,records=records,rowID=rowID)

#----------------
def lifting_plan_batch_upload():
    task_id='rm_liftingplan_manage'
    access_permission=check_role(task_id)
    if access_permission==False:
        session.flash='Access is Denied !'
        redirect (URL('lifting_plan_add'))
    
    response.title='Lifting Plan Batch Upload'
    
    c_id=session.cid
    
    btn_upload=request.vars.btn_upload    
    count_inserted=0
    count_error=0
    error_str=''
    total_row=0
    if btn_upload=='Upload':        
        excel_data=str(request.vars.excel_data)
        inserted_count=0
        error_count=0
        error_list=[]
        row_list=excel_data.split( '\n')
        total_row=len(row_list)
        
        mode_list_excel=[]
        mode_list_exist=[]
        
        
        for i in range(total_row):
            if i>=10:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==35:
                    modeExcel=str(coloum_list[3]).strip().upper()
                    if modeExcel not in mode_list_excel:
                        mode_list_excel.append(modeExcel)
                    
        
        #        mode list
        modeRows=db((db.sm_category_type.cid==c_id)&(db.sm_category_type.type_name=='LIFTING_MODE')).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id)
        mode_list_exist=modeRows.as_list()
        
        #   --------------------     
        for i in range(total_row):
            if i>=10: 
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')            
            
            if len(coloum_list)!=35:
                error_data=row_data+'(35 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
            else:
                date_ex=str(coloum_list[0]).strip()                
                distId_ex=str(coloum_list[1]).strip().upper()
                depot_id_ex=str(coloum_list[2]).strip().upper()
                mode_ex=str(coloum_list[3]).strip().upper()
                
                try:
                    t1_ex=int(coloum_list[4])
                except:
                    t1_ex=0                
                try:
                    t2_ex=int(coloum_list[5])
                except:
                    t2_ex=0
                try:
                    t3_ex=int(coloum_list[6])
                except:
                    t3_ex=0
                try:
                    t4_ex=int(coloum_list[7])
                except:
                    t4_ex=0
                try:
                    t5_ex=int(coloum_list[8])
                except:
                    t5_ex=0
                try:
                    t6_ex=int(coloum_list[9])
                except:
                    t6_ex=0
                try:
                    t7_ex=int(coloum_list[10])
                except:
                    t7_ex=0
                try:
                    t8_ex=int(coloum_list[11])
                except:
                    t8_ex=0
                try:
                    t9_ex=int(coloum_list[12])
                except:
                    t9_ex=0
                try:
                    t10_ex=int(coloum_list[13])
                except:
                    t10_ex=0
                
                try:
                    t11_ex=int(coloum_list[14])
                except:
                    t11_ex=0
                try:
                    t12_ex=int(coloum_list[15])
                except:
                    t12_ex=0
                try:
                    t13_ex=int(coloum_list[16])
                except:
                    t13_ex=0
                try:
                    t14_ex=int(coloum_list[17])
                except:
                    t14_ex=0
                try:
                    t15_ex=int(coloum_list[18])
                except:
                    t15_ex=0
                try:
                    t16_ex=int(coloum_list[19])
                except:
                    t16_ex=0
                try:
                    t17_ex=int(coloum_list[20])
                except:
                    t17_ex=0
                try:
                    t18_ex=int(coloum_list[21])
                except:
                    t18_ex=0
                try:
                    t19_ex=int(coloum_list[22])
                except:
                    t19_ex=0
                try:
                    t20_ex=int(coloum_list[23])
                except:
                    t20_ex=0
                
                try:
                    t21_ex=int(coloum_list[24])
                except:
                    t21_ex=0
                try:
                    t22_ex=int(coloum_list[25])
                except:
                    t22_ex=0
                try:
                    t23_ex=int(coloum_list[26])
                except:
                    t23_ex=0
                try:
                    t24_ex=int(coloum_list[27])
                except:
                    t24_ex=0
                try:
                    t25_ex=int(coloum_list[28])
                except:
                    t25_ex=0
                try:
                    t26_ex=int(coloum_list[29])
                except:
                    t26_ex=0
                try:
                    t27_ex=int(coloum_list[30])
                except:
                    t27_ex=0
                try:
                    t28_ex=int(coloum_list[31])
                except:
                    t28_ex=0
                try:
                    t29_ex=int(coloum_list[32])
                except:
                    t29_ex=0
                try:
                    t30_ex=int(coloum_list[33])
                except:
                    t30_ex=0
                try:
                    t31_ex=int(coloum_list[34])
                except:
                    t31_ex=0
                
                if (date_ex=='' or distId_ex=='' or depot_id_ex=='' or mode_ex==''):
                    error_data=row_data+'(Must value required)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                else:                                        
                    try:
                        date_ex=datetime.datetime.strptime(date_ex,'%Y-%m-%d')
                    except:
                        error_data=row_data+'(Invalid date)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    
                    #-----------------------
                    valid_mode=False
                    
                    firstDate=str(date_ex)[0:7]+'-01'                    
                    clientName=''
                    itemName=''
                    
                    #----------- check valid spo                                                      
                    for i in range(len(mode_list_exist)):
                        myRowData1=mode_list_exist[i]                                
                        modeCat_id=myRowData1['cat_type_id']
                        if (str(modeCat_id).strip()==str(mode_ex).strip()):
                            valid_mode=True
                            break
                    
                    #-----------------
                    if(valid_mode==False):
                        error_data=row_data+'(Invalid Mode)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue                        
                    else:
                        existPartyRow=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==distId_ex)& (db.sm_depot.depot_category=='DISTRIBUTOR')& (db.sm_depot.status=='ACTIVE')).select(db.sm_depot.name,limitby=(0,1))
                        if not existPartyRow:
                            error_data=row_data+'(Invalid Distributor/Party ID)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:
                            existDepotRow=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==depot_id_ex)& (db.sm_depot.depot_category=='DEPOT')& (db.sm_depot.status=='ACTIVE')).select(db.sm_depot.name,limitby=(0,1))
                            if not existDepotRow:
                                error_data=row_data+'(Invalid Depot ID)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                            else:
                            
                                existRow=db((db.lifting_plan.cid==c_id) & (db.lifting_plan.first_date==firstDate)& (db.lifting_plan.distributor_id==distId_ex)& (db.lifting_plan.super_depot_id==depot_id_ex)& (db.lifting_plan.mode==mode_ex)).select(db.lifting_plan.id,limitby=(0,1))
                                if existRow :
                                    error_data=row_data+'(Already exist)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                                else:
                                    #Create insert list
                                    distName=existPartyRow[0].name
                                    depotName=existDepotRow[0].name
                                    
                                    try:
                                        db.lifting_plan.insert(cid=c_id,first_date=firstDate,plan_date=date_ex,distributor_id=distId_ex,distributor_name=distName,super_depot_id=depot_id_ex,super_depot_name=depotName,mode=mode_ex,t_1=t1_ex,t_2=t2_ex,t_3=t3_ex,t_4=t4_ex,t_5=t5_ex,t_6=t6_ex,t_7=t7_ex,t_8=t8_ex,t_9=t9_ex,t_10=t10_ex,
                                                               t_11=t11_ex,t_12=t12_ex,t_13=t13_ex,t_14=t14_ex,t_15=t15_ex,t_16=t16_ex,t_17=t17_ex,t_18=t18_ex,t_19=t19_ex,t_20=t20_ex,t_21=t21_ex,t_22=t22_ex,t_23=t23_ex,t_24=t24_ex,t_25=t25_ex,t_26=t26_ex,t_27=t27_ex,t_28=t28_ex,t_29=t29_ex,t_30=t30_ex,t_31=t31_ex)
                                        count_inserted+=1
                                    except:
                                        error_data=row_data+'(error in process!)\n'
                                        error_str=error_str+error_data
                                        count_error+=1
                                        continue            
        
        if error_str=='':
            error_str='No error'
            
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)


#Validation for catagory
def validation_lifting_mode(form):    
    category_id=str(request.vars.cat_type_id).strip().upper()
    if ((category_id!='') and (session.cid!='')):
        rows_check=db((db.sm_category_type.cid==session.cid) & (db.sm_category_type.type_name=='LIFTING_MODE') &(db.sm_category_type.cat_type_id==category_id)).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id,limitby=(0,1))
        if rows_check:
            form.errors.cat_type_id=''
            response.flash = 'please choose a new '
        else:
            form.vars.cid=session.cid
            form.vars.type_name='LIFTING_MODE'
            form.vars.cat_type_id=category_id

def lifting_mode():
    task_id='rm_liftingplan_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    # ---------------------
    response.title='Lifting Mode'
    
    
    form =SQLFORM(db.sm_category_type,
                  fields=['cat_type_id'],
                  submit_button='Save'          
                  )
    
    #Insert with validation
    if form.accepts(request.vars,session,onvalidation=validation_lifting_mode):
       response.flash = 'Saved Successfully'
    
    #--------------------------------
    btn_delete=request.vars.btn_delete
    record_id=request.vars.record_id
    
    #If catagorey not in item it can be delete
    if btn_delete:
        record_id=request.args[1]
        category_id=request.args[2]
        db((db.sm_category_type.id==record_id)&(db.sm_category_type.type_name=='LIFTING_MODE')).delete()
        
    
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging
    
    records=db((db.sm_category_type.cid==session.cid)& (db.sm_category_type.type_name=='LIFTING_MODE')).select(db.sm_category_type.ALL,orderby=db.sm_category_type.cat_type_id,limitby=limitby)
    
    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)
    

def validation_ff_target_add(form):
    cid=session.cid
    
    year=str(request.vars.year).strip()
    month=str(request.vars.month).strip()
    
    if year=='' or month=='':
        form.errors.client_id=''                
        response.flash='Valid Year-Month required'
    else:
        first_date=year+'-'+month+'-01'
        target_year=int(year)
        target_month=int(month)
        
        rep_id=str(request.vars.rep_id).upper().split('|')[0]        
        target_amount=request.vars.target_amount
        
        if session.user_type=='Supervisor' or session.user_type=='Depot':
            repList=[]
            
            if session.user_type=='Supervisor':
                reparearows = db((db.sm_rep_area.cid == cid)&(db.sm_rep_area.area_id.belongs(session.marketList))).select(db.sm_rep_area.rep_id,groupby=db.sm_rep_area.rep_id)
            else:
                reparearows = db((db.sm_rep_area.cid == cid)&(db.sm_rep_area.depot_id == session.depot_id)).select(db.sm_rep_area.rep_id,groupby=db.sm_rep_area.rep_id)
                
            for reprow in reparearows:
                repList.append(reprow.rep_id)
            
            if rep_id not in repList:
                repRow=''
            else:            
                repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.user_type == 'rep')).select(db.sm_rep.name, limitby=(0, 1))
            
        else:
            repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.user_type == 'rep')).select(db.sm_rep.name, limitby=(0, 1))
        
        
        if not repRow:
            form.errors.rep_id='Invalid Rep'
        else:
            if target_amount<0:
                form.errors.target_amount='Invalid amount'
            else:
                rep_name=repRow[0].name
                   
                #------------
                rows_check=db((db.target_vs_achievement_field_force.cid==cid) & (db.target_vs_achievement_field_force.first_date==first_date)& (db.target_vs_achievement_field_force.rep_id==rep_id)).select(db.target_vs_achievement_field_force.id,limitby=(0,1))
                if rows_check:
                    rows_check[0].update_record(target_amount=target_amount)
                    
                    form.errors.rep_id=''
                    response.flash = 'Target Updated'
                    
                else:                    
                    form.vars.cid=cid
                    form.vars.first_date=first_date
                    form.vars.target_year=target_year
                    form.vars.target_month=target_month                   
                    
                    form.vars.rep_id=rep_id
                    form.vars.rep_name=rep_name
                    form.vars.target_amount=target_amount
                    
                    
                    
def field_force_target_add():
    task_id='rm_ff_target_manage'
    task_id_view='rm_ff_target_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (task_id_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    response.title='Field Force Target'
    cid=session.cid
    
    #db.target_vs_achievement.depot_id.requires=IS_IN_DB(db((db.sm_depot.cid==cid)&(db.sm_depot.status=='ACTIVE')),db.sm_depot.depot_id,orderby=db.sm_depot.depot_id)
    form =SQLFORM(db.target_vs_achievement_field_force,
                  fields=['rep_id','target_amount'],
                  submit_button='Save'
                )
    form.vars.cid=cid
    if form.accepts(request.vars,session,onvalidation=validation_ff_target_add):
       response.flash = 'Submitted Successfully'
    
    
    #Cancelled
    btn_delete=request.vars.btn_delete
    if btn_delete:
        record_id=request.args[1]
        check_cancel=request.vars.check_cancel
        if check_cancel!='YES':
            response.flash='Check Confirmation Required'
        else:
            taRecords=db((db.target_vs_achievement_field_force.cid==cid)& (db.target_vs_achievement_field_force.id==record_id) & (db.target_vs_achievement_field_force.achievement_amount==0)).select(db.target_vs_achievement_field_force.id,limitby=(0,1))
            if taRecords:
                taRecords[0].delete_record()
            else:
                response.flash='Invalid request'
                
    #------------------------
    btn_filter_target=request.vars.btn_filter
    btn_all=request.vars.btn_all
    reqPage=len(request.args)    
    if btn_filter_target:
        session.btn_filter_target=btn_filter_target
        session.searchType_target=str(request.vars.searchType).strip()
        session.searchValue_target=str(request.vars.searchValue).strip()
        reqPage=0
    elif btn_all:
        session.btn_filter_target=None
        session.searchType_target=None
        session.searchValue_target=None
        reqPage=0
    
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page*10
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging    
    
    qset=db()
    qset=qset(db.target_vs_achievement_field_force.cid==cid)
    
    #---- supervisor
    if session.user_type=='Supervisor' or session.user_type=='Depot':
        repList=[]            
        if session.user_type=='Supervisor':
            reparearows = db((db.sm_rep_area.cid == cid)&(db.sm_rep_area.area_id.belongs(session.marketList))).select(db.sm_rep_area.rep_id,groupby=db.sm_rep_area.rep_id)
        else:
            reparearows = db((db.sm_rep_area.cid == cid)&(db.sm_rep_area.depot_id == session.depot_id)).select(db.sm_rep_area.rep_id,groupby=db.sm_rep_area.rep_id)
            
        for reprow in reparearows:
            repList.append(reprow.rep_id)
            
        qset=qset(db.target_vs_achievement_field_force.rep_id.belongs(repList))
    else:
        pass
    #----
    
    if ((session.btn_filter_target) and (session.searchType_target=='RepID')):
        qset=qset(db.target_vs_achievement_field_force.rep_id==str(session.searchValue_target).split('|')[0])  
    
    elif ((session.btn_filter_target) and (session.searchType_target=='YearMonth')):
        monthFlag=True
        try:
            deleteYearMonth=str(session.searchValue_target)+'-01'
            deleteMonth=datetime.datetime.strptime(deleteYearMonth,'%Y-%m-%d')
            deleteMonthFDate=deleteMonth.strftime('%Y-%m-%d')
        except:
            monthFlag=False
            
        if monthFlag==True:
            qset=qset(db.target_vs_achievement_field_force.first_date==deleteMonthFDate)
        else:
            response.flash='Invalid Year-Month'
            
    records=qset.select(db.target_vs_achievement_field_force.ALL,orderby=~db.target_vs_achievement_field_force.first_date|db.target_vs_achievement_field_force.rep_name,limitby=limitby)
    totalCount=qset.count()
    
    
    return dict(form=form,records=records,totalCount=totalCount,page=page,items_per_page=items_per_page,access_permission=access_permission)
    

#----------------
def field_force_target_batch_upload():
    task_id='rm_ff_target_manage'
    access_permission=check_role(task_id)
    if access_permission==False:
        session.flash='Access is Denied !'
        redirect (URL('field_force_target_add'))
        
    response.title='Field Force Target Batch Upload'
    
    c_id=session.cid
    
    btn_upload=request.vars.btn_upload
    btn_delete=request.vars.btn_delete
    
    
    count_inserted=0
    count_error=0
    error_str=''
    total_row=0
    
    if btn_delete:
        delete_check=request.vars.delete_check
        deleteYearMonth=str(request.vars.deleteYearMonth).strip()
        
        if delete_check!='YES':
            response.flash='Confirmation Required'            
        else:
            if deleteYearMonth=='':
                response.flash='Required Year-Month'                
            else:
                monthFlag=True
                try:
                    deleteYearMonth=str(deleteYearMonth)+'-01'                    
                    deleteMonth=datetime.datetime.strptime(deleteYearMonth,'%Y-%m-%d')
                    deleteMonthFDate=deleteMonth.strftime('%Y-%m-%d')
                except:
                    monthFlag=False
                
                
                if monthFlag==True:
                                        
                    rows=db((db.target_vs_achievement_field_force.cid==c_id)&(db.target_vs_achievement_field_force.first_date==deleteMonthFDate)).select(db.target_vs_achievement_field_force.id,limitby=(0,1))
                    if not rows:
                        response.flash='Data not available'
                    else:
                        db((db.target_vs_achievement_field_force.cid==c_id)&(db.target_vs_achievement_field_force.first_date==deleteMonthFDate)).delete()
                        response.flash='Data cleaned successfully of the month '+str(deleteMonth.strftime('%Y-%b'))
                else:
                    response.flash='Required valid Year-Month'
    
    elif btn_upload=='Upload':        
        excel_data=str(request.vars.excel_data)
        inserted_count=0
        error_count=0
        error_list=[]
        row_list=excel_data.split( '\n')
        total_row=len(row_list)
        
        rep_list_excel=[]
        rep_list_exist=[]
        
        for i in range(total_row):
            if i>=500:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==3:
                    repIdExcel=str(coloum_list[1]).strip().upper()
                    if repIdExcel not in rep_list_excel:
                        rep_list_excel.append(repIdExcel)
        
        #        create client list
        existClientRows=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id.belongs(rep_list_excel))&(db.sm_rep.user_type == 'rep')).select(db.sm_rep.rep_id,db.sm_rep.name,orderby=db.sm_rep.rep_id)
        rep_list_exist=existClientRows.as_list()
        
        #   --------------------     
        for i in range(total_row):
            if i>=500: 
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')            
            
            if len(coloum_list)!=3:
                error_data=row_data+'(3 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
            else:
                date_ex=str(coloum_list[0]).strip()                
                repID_ex=str(coloum_list[1]).strip().upper()                
                targetAmt_ex=str(coloum_list[2]).strip()
                
                if (date_ex=='' or repID_ex=='' or targetAmt_ex==''):
                    error_data=row_data+'(Must value required)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                else:             
                    try:
                        date_ex=datetime.datetime.strptime(date_ex,'%Y-%m-%d')
                    except:
                        error_data=row_data+'(Invalid date)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                                        
                    try:
                        targetAmt=int(targetAmt_ex)
                        if targetAmt<=0:
                            error_data=row_data+'(Invalid Target Amount)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        
                    except:
                        error_data=row_data+'(Invalid Target Amount)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    
                    #-----------------------   2015-05-26                 
                    valid_rep=False
                    
                    firstDate=str(date_ex)[0:7]+'-01'
                    target_year=int(str(date_ex)[0:4])
                    target_month=int(str(date_ex)[5:7])
                    
                    repName=''
                    
                    for i in range(len(rep_list_exist)):
                        myRowData2=rep_list_exist[i]                        
                        repid=myRowData2['rep_id']                            
                        if (str(repid).strip()==str(repID_ex).strip()):
                            valid_rep=True
                            repName=myRowData2['name']
                            break
                    
                    #-----------------
                    if(valid_rep==False):
                        error_data=row_data+'(Invalid Rep)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue                        
                    else:                        
                        existRow=db((db.target_vs_achievement_field_force.cid==c_id) & (db.target_vs_achievement_field_force.first_date==firstDate)& (db.target_vs_achievement_field_force.rep_id==repID_ex)).select(db.target_vs_achievement_field_force.id,limitby=(0,1))
                        if existRow :
                            error_data=row_data+'(Already exist)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:                            
                            try:
                                db.target_vs_achievement_field_force.insert(cid=c_id,first_date=firstDate,target_year=target_year,target_month=target_month,rep_id=repID_ex,rep_name=repName,target_amount=targetAmt)
                                count_inserted+=1
                            except:
                                error_data=row_data+'(error in process!)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue            
        
        if error_str=='':
            error_str='No error'
            
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)

#=================== target weight
def validation_ff_target_add_weight(form):
    cid=session.cid
    
    year=str(request.vars.year).strip()
    month=str(request.vars.month).strip()
    
    if year=='' or month=='':
        form.errors.client_id=''                
        response.flash='Valid Year-Month required'
    else:
        first_date=year+'-'+month+'-01'
        target_year=int(year)
        target_month=int(month)
        
        rep_id=str(request.vars.rep_id).upper().split('|')[0]        
        target_weight=request.vars.target_weight
        category_id_sp=request.vars.category_id_sp
        
        if session.user_type=='Supervisor' or session.user_type=='Depot':
            repList=[]
            
            if session.user_type=='Supervisor':
                reparearows = db((db.sm_rep_area.cid == cid)&(db.sm_rep_area.area_id.belongs(session.marketList))).select(db.sm_rep_area.rep_id,groupby=db.sm_rep_area.rep_id)
            else:
                reparearows = db((db.sm_rep_area.cid == cid)&(db.sm_rep_area.depot_id == session.depot_id)).select(db.sm_rep_area.rep_id,groupby=db.sm_rep_area.rep_id)
                
            for reprow in reparearows:
                repList.append(reprow.rep_id)
            
            if rep_id not in repList:
                repRow=''
            else:            
                repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.user_type == 'rep')).select(db.sm_rep.name, limitby=(0, 1))
            
        else:
            repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.user_type == 'rep')).select(db.sm_rep.name, limitby=(0, 1))
        
        
        if not repRow:
            form.errors.rep_id='Invalid Rep'
        else:
            if target_weight<0:
                form.errors.target_weight='Invalid Weight'
            else:
                rep_name=repRow[0].name
                
                #distributor
                distributorRows=db((db.sm_rep_area.cid==cid)&(db.sm_rep_area.rep_id == rep_id)&(db.sm_level.cid==cid)&(db.sm_level.level_id==db.sm_rep_area.area_id)&(db.sm_level.depth==3)&(db.sm_level.depot_id!='-')).select(db.sm_level.ALL,limitby=(0,1))
                
                if not distributorRows:
                    form.errors.target_amount=''
                    response.flash='Required valid distributor'
                else:
                    depot_id=distributorRows[0][db.sm_level.depot_id]
                    level0=distributorRows[0][db.sm_level.level0]
                    level0_name=distributorRows[0][db.sm_level.level0_name]
                    level1=distributorRows[0][db.sm_level.level1]
                    level1_name=distributorRows[0][db.sm_level.level1_name]
                    level2=distributorRows[0][db.sm_level.level2]
                    level2_name=distributorRows[0][db.sm_level.level2_name]
                    level3=distributorRows[0][db.sm_level.level3]
                    level3_name=distributorRows[0][db.sm_level.level3_name]
                    
                    
                    #------------
                    rows_check=db((db.target_vs_achievement_ff_cat_wise.cid==cid) & (db.target_vs_achievement_ff_cat_wise.first_date==first_date)& (db.target_vs_achievement_ff_cat_wise.rep_id==rep_id)& (db.target_vs_achievement_ff_cat_wise.category_id_sp==category_id_sp)).select(db.target_vs_achievement_ff_cat_wise.id,limitby=(0,1))
                    if rows_check:
                        rows_check[0].update_record(target_weight=target_weight)
                        
                        form.errors.rep_id=''
                        response.flash = 'Target Updated'                    
                    else:
                        chkItemCatSp=db((db.sm_item.cid==cid)&(db.sm_item.category_id_sp==category_id_sp)).select(db.sm_item.weight_type,limitby=(0,1))
                        
                        if not chkItemCatSp:
                            form.errors.rep_id=''
                            response.flash = 'Invalid Base Category'
                        else:
                            weight_type=chkItemCatSp[0].weight_type                        
                                            
                            form.vars.cid=cid
                            form.vars.first_date=first_date
                            form.vars.target_year=target_year
                            form.vars.target_month=target_month
                            form.vars.depot_id=depot_id
                            
                            form.vars.rep_id=rep_id
                            form.vars.rep_name=rep_name
                            form.vars.target_weight=target_weight
                            form.vars.category_id_sp=category_id_sp
                            form.vars.weight_type=weight_type
                            
                            form.vars.level0=level0
                            form.vars.level0_name=level0_name
                            form.vars.level1=level1
                            form.vars.level1_name=level1_name
                            form.vars.level2=level2
                            form.vars.level2_name=level2_name
                            form.vars.level3=level3
                            form.vars.level3_name=level3_name
                            
                
                    
def field_force_target_add_weight():
    task_id='rm_ff_target_manage'
    task_id_view='rm_ff_target_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (task_id_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    response.title='Field Force Target'
    cid=session.cid
    

    db.target_vs_achievement_ff_cat_wise.category_id_sp.requires=IS_IN_DB(db((db.sm_category_type.cid==cid)&(db.sm_category_type.type_name=='ITEM_CATEGORY_CLASS')),db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id)
    
    form =SQLFORM(db.target_vs_achievement_ff_cat_wise,
                  fields=['depot_id','rep_id','category_id_sp','target_weight','weight_type'],
                  submit_button='Save'
                )
    form.vars.cid=cid
    if form.accepts(request.vars,session,onvalidation=validation_ff_target_add_weight):
       response.flash = 'Submitted Successfully'
    
    
    #Cancelled
    btn_delete=request.vars.btn_delete
    if btn_delete:
        record_id=request.args[1]
        check_cancel=request.vars.check_cancel
        if check_cancel!='YES':
            response.flash='Check Confirmation Required'
        else:
            taRecords=db((db.target_vs_achievement_ff_cat_wise.cid==cid)& (db.target_vs_achievement_ff_cat_wise.id==record_id) & (db.target_vs_achievement_ff_cat_wise.achievement_weight==0)).select(db.target_vs_achievement_ff_cat_wise.id,limitby=(0,1))
            if taRecords:
                taRecords[0].delete_record()
            else:
                response.flash='Invalid request'
                
    #------------------------
    btn_filter_target=request.vars.btn_filter
    btn_all=request.vars.btn_all
    reqPage=len(request.args)    
    if btn_filter_target:
        session.btn_filter_target=btn_filter_target
        session.searchType_target=str(request.vars.searchType).strip()
        session.searchValue_target=str(request.vars.searchValue).strip()
        reqPage=0
    elif btn_all:
        session.btn_filter_target=None
        session.searchType_target=None
        session.searchValue_target=None
        reqPage=0
    
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page*10
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging    
    
    qset=db()
    qset=qset(db.target_vs_achievement_ff_cat_wise.cid==cid)
    
    #---- supervisor
    if session.user_type=='Supervisor' or session.user_type=='Depot':
        repList=[]            
        if session.user_type=='Supervisor':
            reparearows = db((db.sm_rep_area.cid == cid)&(db.sm_rep_area.area_id.belongs(session.marketList))).select(db.sm_rep_area.rep_id,groupby=db.sm_rep_area.rep_id)
        else:
            reparearows = db((db.sm_rep_area.cid == cid)&(db.sm_rep_area.depot_id == session.depot_id)).select(db.sm_rep_area.rep_id,groupby=db.sm_rep_area.rep_id)
            
        for reprow in reparearows:
            repList.append(reprow.rep_id)
            
        qset=qset(db.target_vs_achievement_ff_cat_wise.rep_id.belongs(repList))
    else:
        pass
    #----
    
    if ((session.btn_filter_target) and (session.searchType_target=='RepID')):
        qset=qset(db.target_vs_achievement_ff_cat_wise.rep_id==str(session.searchValue_target).split('|')[0])  
    
    elif ((session.btn_filter_target) and (session.searchType_target=='YearMonth')):
        monthFlag=True
        try:
            deleteYearMonth=str(session.searchValue_target)+'-01'
            deleteMonth=datetime.datetime.strptime(deleteYearMonth,'%Y-%m-%d')
            deleteMonthFDate=deleteMonth.strftime('%Y-%m-%d')
        except:
            monthFlag=False
            
        if monthFlag==True:
            qset=qset(db.target_vs_achievement_ff_cat_wise.first_date==deleteMonthFDate)
        else:
            response.flash='Invalid Year-Month'
            
    records=qset.select(db.target_vs_achievement_ff_cat_wise.ALL,orderby=~db.target_vs_achievement_ff_cat_wise.first_date|~db.target_vs_achievement_ff_cat_wise.id|db.target_vs_achievement_ff_cat_wise.rep_name,limitby=limitby)
    
    totalCount=qset.count()
    
    
    return dict(form=form,records=records,totalCount=totalCount,page=page,items_per_page=items_per_page,access_permission=access_permission)
    

#----------------
def field_force_target_batch_upload_weight():
    task_id='rm_ff_target_manage'
    access_permission=check_role(task_id)
    if access_permission==False:
        session.flash='Access is Denied !'
        redirect (URL('field_force_target_add'))
        
    response.title='Field Force Target Weight Batch Upload'
    
    c_id=session.cid
    
    btn_upload=request.vars.btn_upload
    btn_delete=request.vars.btn_delete
    
    
    count_inserted=0
    count_error=0
    error_str=''
    total_row=0
    
    if btn_delete:
        delete_check=request.vars.delete_check
        deleteYearMonth=str(request.vars.deleteYearMonth).strip()
        
        if delete_check!='YES':
            response.flash='Confirmation Required'            
        else:
            if deleteYearMonth=='':
                response.flash='Required Year-Month'                
            else:
                monthFlag=True
                try:
                    deleteYearMonth=str(deleteYearMonth)+'-01'                    
                    deleteMonth=datetime.datetime.strptime(deleteYearMonth,'%Y-%m-%d')
                    deleteMonthFDate=deleteMonth.strftime('%Y-%m-%d')
                except:
                    monthFlag=False
                
                
                if monthFlag==True:
                                        
                    rows=db((db.target_vs_achievement_ff_cat_wise.cid==c_id)&(db.target_vs_achievement_ff_cat_wise.first_date==deleteMonthFDate)).select(db.target_vs_achievement_ff_cat_wise.id,limitby=(0,1))
                    if not rows:
                        response.flash='Data not available'
                    else:
                        db((db.target_vs_achievement_ff_cat_wise.cid==c_id)&(db.target_vs_achievement_ff_cat_wise.first_date==deleteMonthFDate)).delete()
                        response.flash='Data cleaned successfully of the month '+str(deleteMonth.strftime('%Y-%b'))
                else:
                    response.flash='Required valid Year-Month'
    
    elif btn_upload=='Upload':        
        excel_data=str(request.vars.excel_data)
        inserted_count=0
        error_count=0
        error_list=[]
        row_list=excel_data.split( '\n')
        total_row=len(row_list)
        
        rep_list_excel=[]
        rep_list_exist=[]
        
        for i in range(total_row):
            if i>=500:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==4:
                    repIdExcel=str(coloum_list[1]).strip().upper()
                    if repIdExcel not in rep_list_excel:
                        rep_list_excel.append(repIdExcel)
        
        #        create client list
        existClientRows=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id.belongs(rep_list_excel))&(db.sm_rep.user_type == 'rep')).select(db.sm_rep.rep_id,db.sm_rep.name,orderby=db.sm_rep.rep_id)
        rep_list_exist=existClientRows.as_list()
        
        #   --------------------     
        for i in range(total_row):
            if i>=500: 
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')            
            
            if len(coloum_list)!=4:
                error_data=row_data+'(4 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
            else:
                date_ex=str(coloum_list[0]).strip()                
                repID_ex=str(coloum_list[1]).strip().upper()                
                target_weight_ex=str(coloum_list[2]).strip()
                cat_id_sp_ex=str(coloum_list[3]).strip()
                
                
                if (date_ex=='' or repID_ex=='' or target_weight_ex=='' or cat_id_sp_ex==''):
                    error_data=row_data+'(Must value required)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                else:
                    #weight_type
                    weight_type=''
                    itemRows=db((db.sm_item.cid==c_id)&(db.sm_item.category_id_sp == cat_id_sp_ex)).select(db.sm_item.weight_type,limitby=(0,1))
                    if itemRows:
                        weight_type=itemRows[0].weight_type
                        
                    #distributor
                    depot_id='-'
                    level0=''
                    level0_name=''
                    level1=''
                    level1_name=''
                    level2=''
                    level2_name=''
                    level3=''
                    level3_name=''
                        
                    distributorRows=db((db.sm_rep_area.cid==c_id)&(db.sm_rep_area.rep_id == repID_ex)&(db.sm_level.cid==c_id)&(db.sm_level.level_id==db.sm_rep_area.area_id)&(db.sm_level.depth==3)&(db.sm_level.depot_id!='-')).select(db.sm_level.depot_id,db.sm_level.level0,db.sm_level.level0_name,db.sm_level.level1,db.sm_level.level1_name,db.sm_level.level2,db.sm_level.level2_name,db.sm_level.level3,db.sm_level.level3_name,limitby=(0,1))
                    #return distributorRows
                    if distributorRows:
                        level0=distributorRows[0][db.sm_level.level0]
                        level0_name=distributorRows[0][db.sm_level.level0_name]
                        level1=distributorRows[0][db.sm_level.level1]
                        level1_name=distributorRows[0][db.sm_level.level1_name]
                        level2=distributorRows[0][db.sm_level.level2]
                        level2_name=distributorRows[0][db.sm_level.level2_name]
                        level3=distributorRows[0][db.sm_level.level3]
                        level3_name=distributorRows[0][db.sm_level.level3_name]
                        depot_id=distributorRows[0][db.sm_level.depot_id]
                                 
                    try:
                        date_ex=datetime.datetime.strptime(date_ex,'%Y-%m-%d')
                    except:
                        error_data=row_data+'(Invalid date)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                                        
                    try:
                        target_weight=float(target_weight_ex)
                        if target_weight<=0:
                            error_data=row_data+'(Invalid Target Weight)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        
                    except:
                        error_data=row_data+'(Invalid Target Weight)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    
                    #-----------------------   2015-05-26                 
                    valid_rep=False
                    
                    firstDate=str(date_ex)[0:7]+'-01'
                    target_year=int(str(date_ex)[0:4])
                    target_month=int(str(date_ex)[5:7])
                    
                    repName=''
                    
                    for i in range(len(rep_list_exist)):
                        myRowData2=rep_list_exist[i]                        
                        repid=myRowData2['rep_id']                            
                        if (str(repid).strip()==str(repID_ex).strip()):
                            valid_rep=True
                            repName=myRowData2['name']
                            break
                    
                    #-----------------
                    if(valid_rep==False):
                        error_data=row_data+'(Invalid Rep)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue                        
                    else:                        
                        existRow=db((db.target_vs_achievement_ff_cat_wise.cid==c_id) & (db.target_vs_achievement_ff_cat_wise.first_date==firstDate)& (db.target_vs_achievement_ff_cat_wise.rep_id==repID_ex)& (db.target_vs_achievement_ff_cat_wise.category_id_sp==cat_id_sp_ex)).select(db.target_vs_achievement_ff_cat_wise.id,limitby=(0,1))
                        if existRow :
                            error_data=row_data+'(Already exist)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:                            
                            try:
                                db.target_vs_achievement_ff_cat_wise.insert(cid=c_id,first_date=firstDate,target_year=target_year,target_month=target_month,depot_id=depot_id,rep_id=repID_ex,category_id_sp=cat_id_sp_ex,rep_name=repName,target_weight=target_weight,weight_type=weight_type,level0=level0,level0_name=level0_name,level1=level1,level1_name=level1_name,level2=level2,level2_name=level2_name,level3=level3,level3_name=level3_name)
                                count_inserted+=1
                            except:
                                error_data=row_data+'(error in process!)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue            
        
        if error_str=='':
            error_str='No error'
            
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)

