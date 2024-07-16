def farm_visit():
    task_id_view = 'farm_view'
    access_permission_view = check_role(task_id_view)
    if (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))
        
    response.title = 'Farm View'
    
    c_id = session.cid

    btn_filter_farm = request.vars.btn_filter
    btn_all = request.vars.btn_filter_all
    btn_download = request.vars.btn_download
    reqPage = len(request.args)
    if btn_filter_farm:
        session.btn_filter_farm = btn_filter_farm
        session.search_type = str(request.vars.search_type).strip()
        search_value = str(request.vars.search_value).strip().upper()
        reqPage = 0
        
        
        if (session.search_type == 'Date'):
            try:
                searchValue_farm=datetime.datetime.strptime(str(search_value),'%Y-%m-%d').strftime('%Y-%m-%d')
            except:
                searchValue_farm=''
                
        session.search_value=search_value
        
    elif btn_all:
        session.btn_filter_farm = None
        session.searchType_farm = None
        session.search_value = None
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
    qset = qset(db.sm_farm.cid == c_id)

            
    if (session.btn_filter_farm):
        if (session.search_type== 'FarmName'):
            search_value=str(session.search_value).split('|')[0]
            qset = qset(db.sm_farm.farm_name == search_value)
            search_value_id=str(session.search_value).split('|')[1]
            qset = qset(db.sm_farm.farm_id == search_value_id)

        elif (session.searchType_farm == 'Owner'):
            searchValue=str(session.searchValue_farm).split('|')[0]
            qset = qset(db.sm_farm.owner_name == searchValue)
                
    records = qset.select(db.sm_farm.ALL, groupby=db.sm_farm.id, orderby=~db.sm_farm.farm_id, limitby=limitby)
    totalCount=qset.count()


    return dict(records=records,totalCount=totalCount, page=page, items_per_page=items_per_page)


def download_farm_list():

    c_id = session.cid
    btn_download = request.vars.btn_download
    btn_filter_prescription = request.vars.btn_filter
    btn_all = request.vars.btn_filter_all

    if btn_filter_prescription:
        session.btn_filter_prescription = btn_filter_prescription
        session.searchType_prescription = str(request.vars.search_type).strip()
        searchValue_prescription = str(request.vars.search_value).strip().upper()


        if (session.searchType_prescription == 'Date'):
            try:
                searchValue_prescription=datetime.datetime.strptime(str(searchValue_prescription),'%Y-%m-%d').strftime('%Y-%m-%d')
            except:
                searchValue_prescription=''

        session.searchValue_prescription=searchValue_prescription

    elif btn_all:
        session.btn_filter_prescription = None
        session.searchType_prescription = None
        session.searchValue_prescription = None

    qset=db()
    qset = qset(db.sm_prescription_head.cid == c_id)

    if (session.btn_filter_prescription):
        if (session.searchType_prescription == 'DocID'):
            searchValue=str(session.searchValue_prescription).split('|')[0]
            qset = qset(db.sm_prescription_head.doctor_name == searchValue)

        elif (session.searchType_prescription == 'SubmitBy'):
            searchValue=str(session.searchValue_prescription).split('|')[0]
            qset = qset(db.sm_prescription_head.submit_by_name == searchValue)

        elif (session.searchType_prescription == 'Date'):
            qset = qset(db.sm_prescription_head.submit_date == session.searchValue_prescription)

    if btn_download:
        search_month = str(request.vars.search_month).strip()
        from_date=first_currentDate
        current_year=str(from_date).split('-')[0]
#         return current_year
        if search_month=='JAN':
            from_date=current_year+'-01-01'
            to_date=current_year+'-02-01'
        if search_month=='FEB':
            from_date=current_year+'-02-01'
            to_date=current_year+'-03-01'
        if search_month=='MAR':
            from_date=current_year+'-03-01'
            to_date=current_year+'-04-01'
        if search_month=='APR':
            from_date=current_year+'-04-01'
            to_date=current_year+'-05-01'
        if search_month=='MAY':
            from_date=current_year+'-05-01'
            to_date=current_year+'-06-01'
        if search_month=='JUN':
            from_date=current_year+'-06-01'
            to_date=current_year+'-07-01'
        if search_month=='JUL':
            from_date=current_year+'-07-01'
            to_date=current_year+'-08-01'
        if search_month=='AUG':
            from_date=current_year+'-08-01'
            to_date=current_year+'-09-01'
        if search_month=='SEP':
            from_date=current_year+'-09-01'
            to_date=current_year+'-10-01'
        if search_month=='OCT':
            from_date=current_year+'-10-01'
            to_date=current_year+'-11-01'
        if search_month=='NOV':
            from_date=current_year+'-11-01'
            to_date=current_year+'-12-01'
        if search_month=='DEC':
            current_yearD=int(current_year)+1
            from_date=current_year+'-12-01'
            to_date=str(current_yearD)+'-01-01'
        if search_month!='':
            qset=db()
            qset = qset(db.sm_prescription_head.cid == c_id)
            qset = qset(db.sm_prescription_head.submit_date >= from_date)
            qset = qset(db.sm_prescription_head.submit_date < to_date)
            qset = qset(db.sm_prescription_details.cid == c_id)
            qset = qset(db.sm_prescription_details.sl == db.sm_prescription_head.sl)

    records = qset.select(db.sm_prescription_head.ALL, groupby=db.sm_prescription_head.submit_date, orderby=~db.sm_prescription_head.sl)
    myString='Prescription\n\n'
    myString+='Date,Doctor Name, Submit By ID, Submit By Name' \
              '\n'
    for rec in records:
        submit_date=str(rec.submit_date)
        doctor_name=str(rec.doctor_name).replace(',', ' ')
        submit_by_id=str(rec.submit_by_id).replace(',', ' ')
        submit_by_name=str(rec.submit_by_name).replace(',', ' ')


        myString+=str(submit_date)+','+str(doctor_name)+','+str(submit_by_id)+','+str(submit_by_name)+'\n'

    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_prescription.csv'
    return str(myString)
#===========Rima end========
#------------------------
def farm_details_1():
    # task_id_view = 'farm_view'
    # access_permission_view = check_role(task_id_view)
    # if (task_id_view == False):
    #     session.flash = 'Access is Denied !'
    #     redirect (URL('prescription_list'))
        
    #   ---------------------
    response.title = 'Prescription Details'
    
    c_id = session.cid
    
    page = request.args(0)
    rowid = request.args(1)
    
    headRow = db((db.sm_prescription_head.cid == c_id) & (db.sm_prescription_head.id == rowid)).select(db.sm_prescription_head.ALL, limitby=(0, 1))
    if not headRow:
        session.flash = 'Invalid request'
        redirect (URL('prescription_list'))
    else: 
        hsl=headRow[0].sl
        
        detailsRow = db((db.sm_prescription_details.cid == c_id) & (db.sm_prescription_details.sl == hsl)).select(db.sm_prescription_details.ALL)
        
    return dict(page=page, headRow=headRow,detailsRow=detailsRow)

def farm_details():
    # task_id='visitM'
    # access_permission=check_role(task_id)
    # if (access_permission==False):
    #     session.flash='Access is Denied'
    #     redirect (URL('default','home'))

    response.title='Farm Details'
    cid=session.cid

    farm_id=request.vars.farm_id
#    return SL
    outletID=''
    outletName=''
    outletEx=''
    visitDate=''
    repID=''
    repName=''
    startTime=''
    endTime=''
    channel=''
    farmRow=db((db.sm_farm.cid==cid)&(db.sm_farm.farm_id==farm_id)).select(db.sm_farm.ALL,limitby=(0,1))
#    return visitRow

    if farmRow:
        farm_id=farmRow[0].farm_id
        farm_name=farmRow[0].farm_name
        latitude=farmRow[0].latitude
        longitude=farmRow[0].longitude
        image=farmRow[0].image
        farm_type=farmRow[0].farm_type
        owner_name=farmRow[0].owner_name
        address=farmRow[0].address
        medicine=farmRow[0].medicine
        manger_name=farmRow[0].manger_name
        consultant_name=farmRow[0].consultant_name
        category=farmRow[0].category


        birds_animal=farmRow[0].birds_animal
        rearing_housing=farmRow[0].rearing_housing
        feeding=farmRow[0].feeding
        watering=farmRow[0].watering
        brooding=farmRow[0].brooding
        poandsSize=farmRow[0].poandsSize
        status=farmRow[0].status
        anniversary=farmRow[0].anniversary

        dob=farmRow[0].dob


    else:
        redirect (URL('farm_visit'))


    #  Set text for filter
    reqPage=len(request.args)
    #--------paging
    if reqPage:
        page=int(request.args[0])

    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging


    return dict(farmRow=farmRow,farm_id=farm_id,farm_name=farm_name,latitude=latitude,longitude=longitude,image=image,farm_type=farm_type,owner_name=owner_name,address=address,medicine=medicine,manger_name=manger_name,consultant_name=consultant_name,category=category,birds_animal=birds_animal,rearing_housing=rearing_housing,feeding=feeding,watering=watering,page=page,items_per_page=items_per_page,brooding=brooding,poandsSize=poandsSize,status=status,anniversary=anniversary,dob=dob)

