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
    records_update="update sm_farm  set  anniversary='1900-01-01' WHERE cid=cid and anniversary ='0000-00-00';"
    records_update_run=db.executesql(records_update)
    
    records_update1="update sm_farm  set  dob='1900-01-01' WHERE cid=cid and dob ='0000-00-00';"
    records_update_run1=db.executesql(records_update1)
    
#     visit_update = db((db.sm_farm.cid == cid) & (db.sm_farm.anniversary is NULL)   ).update(anniversary='1900-01-01')
    return dict(records=records,totalCount=totalCount, page=page, items_per_page=items_per_page)

#===========08_02_2020_start========

def download_farm_list():
    
    c_id = session.cid
    qset=db()
    qset = qset(db.sm_farm.cid == c_id)

            
    if (session.btn_filter_farm):
        if (session.search_type== 'FarmName'):
            search_value=str(session.search_value).split('|')[0]
            qset = qset(db.sm_farm.farm_name == search_value)
            search_value_id=str(session.search_value).split('|')[1]
            qset = qset(db.sm_farm.farm_id == search_value_id)



    records = qset.select(db.sm_farm.farm_id,db.sm_farm.farm_name,db.sm_farm.farm_type,db.sm_farm.owner_name,db.sm_farm.address,db.sm_farm.manger_name,db.sm_farm.consultant_name,db.sm_farm.category,db.sm_farm.birds_animal,db.sm_farm.rearing_housing,db.sm_farm.feeding,db.sm_farm.watering,db.sm_farm.brooding,db.sm_farm.poandsSize,db.sm_farm.status,db.sm_farm.anniversary,db.sm_farm.dob,db.sm_farm.medicine, groupby=db.sm_farm.id, orderby=~db.sm_farm.farm_id)
    myString='Farm\n\n'
    myString+='Farm ID, Farm Name, Farm Type, Owner Name, Address, Manager Name, Consultant Name, Category, Birds/Animal, Housing, Feeding, Watering, Brooding, Ponds Size, Status, Anniversary, Date Of Birth, Medicine ' \
              '\n'
    for rec in records:
        farm_id=str(rec.farm_id)
        farm_name=str(rec.farm_name).replace(',', ' ')
        farm_type=str(rec.farm_type).replace(',', ' ')
        owner_name=str(rec.owner_name).replace(',', ' ')
        address=str(rec.address).replace(',', ' ')
        manger_name=str(rec.manger_name).replace(',', ' ')
        consultant_name=str(rec.consultant_name).replace(',', ' ')
        category=str(rec.category).replace(',', ' ')
        birds_animal=str(rec.birds_animal)
        rearing_housing=str(rec.rearing_housing)
        feeding=str(rec.feeding)
        watering=str(rec.watering)
        brooding=str(rec.brooding)
        poandsSize=str(rec.poandsSize)
        status=str(rec.status)
        anniversary=str(rec.anniversary)
        dob=str(rec.dob)
        medicine=str(rec.medicine)  
        
        if address=='None':
            address=''
        if manger_name=='None':
            manger_name=''
        if consultant_name=='None':
            consultant_name=''
        if category=='None':
            category=''
        if birds_animal=='None':
            birds_animal=''
        if rearing_housing=='None':
            rearing_housing=''
        if feeding=='None':
            feeding=''
        if watering=='None':
            watering=''
        if brooding=='None':
            brooding=''
        if poandsSize=='None':
            poandsSize=''
        if status=='None':
            status=''
        if anniversary=='None':
            anniversary=''
        if anniversary=='1900-01-01':
            anniversary=''
        if dob=='1900-01-01':
            dob=''
        if dob=='None':
            dob=''
        if medicine=='None':
            medicine=''
       

        
        
        
        

        myString+=str(farm_id)+','+str(farm_name)+','+str(farm_type)+','+str(owner_name)+','+str(address)+','+str(manger_name)+','+str(consultant_name)+','+str(category)+','+str(birds_animal)+','+str(rearing_housing)+','+str(feeding)+','+str(watering)+','+str(brooding)+','+str(poandsSize)+','+str(status)+','+str(anniversary)+','+str(dob)+','+str(medicine)+'\n'

    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_farm.csv'
    return str(myString)

#===========08_02_2020_end========



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

