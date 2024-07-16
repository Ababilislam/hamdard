
#====================== Doctor Visit

from random import randint

#------------------------
def prescription_list():
    task_id_view = 'rm_doctor_visit_view'
    access_permission_view = check_role(task_id_view)
    if (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))
        
    response.title = 'Seen Prescription List'
    
    c_id = session.cid
    #   ---------------------
    
    #  ---------------filter-------
    btn_filter_prescription = request.vars.btn_filter
    btn_all = request.vars.btn_filter_all
    btn_download = request.vars.btn_download
    reqPage = len(request.args)
    if btn_filter_prescription:
        session.btn_filter_prescription = btn_filter_prescription
        session.searchType_prescription = str(request.vars.search_type).strip()
        searchValue_prescription = str(request.vars.search_value).strip().upper()
        reqPage = 0
        
        
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
    qset = qset(db.sm_prescription_seen_head.cid == c_id)
    
    #---- supervisor
#    if session.user_type=='Supervisor':
#        level_id=session.level_id
#        depthNo=session.depthNo
#        level = 'level' + str(depthNo)
#        
#        qset=qset((db.sm_level.cid==session.cid)&(db.sm_level.is_leaf=='1')& (db.sm_level[level] == level_id)&(db.sm_level.level_id==db.sm_doctor_area.area_id))
#        
#    else:
#        qset=qset((db.sm_level.cid==session.cid)&(db.sm_level.is_leaf=='1')&(db.sm_level.level_id==db.sm_doctor_area.area_id))
    
    #---- 
#    if session.user_type=='Depot':
#        qset=qset(db.sm_prescription_seen_head.depot_id==session.depot_id)
    #----
    
    
            
    if (session.btn_filter_prescription):
        if (session.searchType_prescription == 'SL'):
            searchValue=str(session.searchValue_prescription)
            qset = qset(db.sm_prescription_seen_head.sl == searchValue)
            
        elif (session.searchType_prescription == 'DocID'):
            searchValue=str(session.searchValue_prescription).split('|')[0]
            qset = qset(db.sm_prescription_seen_head.doctor_id == searchValue)
        
        elif (session.searchType_prescription == 'RegionID'):
            searchValue=str(session.searchValue_prescription).split('|')[0]
            qset = qset(db.sm_prescription_seen_head.zone_id == searchValue)

        elif (session.searchType_prescription == 'ZoneID'):
            searchValue=str(session.searchValue_prescription).split('|')[0]
            qset = qset(db.sm_prescription_seen_head.reg_id == searchValue)

        elif (session.searchType_prescription == 'TlID'):
            searchValue=str(session.searchValue_prescription).split('|')[0]
            qset = qset(db.sm_prescription_seen_head.tl_id == searchValue)

        elif (session.searchType_prescription == 'RouteID'):
            searchValue=str(session.searchValue_prescription).split('|')[0]
            qset = qset(db.sm_prescription_seen_head.area_id == searchValue)
            
        elif (session.searchType_prescription == 'RepID'):
            searchValue=str(session.searchValue_prescription).split('|')[0]
            qset = qset(db.sm_prescription_seen_head.submit_by_id == searchValue)
            
        elif (session.searchType_prescription == 'Date'):
            qset = qset(db.sm_prescription_seen_head.submit_date == session.searchValue_prescription)
                
    records = qset.select(db.sm_prescription_seen_head.id,db.sm_prescription_seen_head.sl,db.sm_prescription_seen_head.created_on,db.sm_prescription_seen_head.doctor_id,db.sm_prescription_seen_head.doctor_name,db.sm_prescription_seen_head.zone_id,db.sm_prescription_seen_head.zone_name,db.sm_prescription_seen_head.reg_id,db.sm_prescription_seen_head.reg_name,db.sm_prescription_seen_head.tl_id,db.sm_prescription_seen_head.tl_name,db.sm_prescription_seen_head.area_id,db.sm_prescription_seen_head.area_name,db.sm_prescription_seen_head.submit_by_id,db.sm_prescription_seen_head.submit_by_name,db.sm_prescription_seen_head.rx_type,db.sm_prescription_seen_head.lat_long, orderby=~db.sm_prescription_seen_head.sl, limitby=limitby)
    totalCount=qset.count()

#     ============Download
    if btn_download:
        search_month = str(request.vars.search_month).strip()
        if search_month=='': 
            response.flash='Required Month'
        else:        
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
                recordList=[]
                sql = "(SELECT a.submit_date as submit_date,a.sl as sl,a.zone_id as level0,a.zone_name as level0_name,a.reg_id as level1,a.reg_name as level1_name,a.tl_id as level2,a.tl_name as level2_name,a.area_id as level3,a.area_name as level3_name,a.doctor_id as doctor_id,a.doctor_name as doctor_name,a.submit_by_id as submit_by_id,a.submit_by_name as submit_by_name,a.rx_type as rx_type,b.medicine_name as medicine_name FROM `sm_prescription_seen_head` a,`sm_prescription_seen_details` b WHERE  a.cid='" + c_id + "' and a.submit_date>='" + from_date + "' and a.submit_date<'" + to_date + "' and a.cid=b.cid and a.sl=b.sl order by submit_date desc)"
                recordList = db.executesql(sql, as_dict=True)
                                
                search_month1=datetime.datetime.strptime(str(from_date), '%Y-%m-%d').strftime('%B %Y')

                myString='Prescription:,'+str(search_month1)+' \n\n'
                myString+='Date  ,SL,  Region ID,  Region Name,Zone ID,  Zone Name, Area ID, Area Name ,Teritory ID, Teritory Name , Doctor ID, Doctor Name,  SubmitBy ID, Submit By Name, Rx Type, Brand Name,\n' #medicineID, medicineName, medType
                
                for i in range(len(recordList)):
                    recordListStr=recordList[i] 
                    
                    submit_date=recordListStr['submit_date']
                    sl=recordListStr['sl']
                    level0=recordListStr['level0']
                    level0_name=recordListStr['level0_name']
                    level1=recordListStr['level1']
                    level1_name=recordListStr['level1_name']
                    level2=recordListStr['level2']
                    level2_name=recordListStr['level2_name']
                    level3=recordListStr['level3']
                    level3_name=recordListStr['level3_name']
                    doctor_id=recordListStr['doctor_id']
                    doctor_name=recordListStr['doctor_name']
                    submit_by_id=recordListStr['submit_by_id']
                    submit_by_name=recordListStr['submit_by_name']
                    rx_type=recordListStr['rx_type']
                    medicine_name=recordListStr['medicine_name']
                                
                    myString+=str(submit_date)+','+str(sl)+','+str(level0)+','+str(level0_name)+','+str(level1)+','+str(level1_name)+','+str(level2)+','+str(level2_name)+','+str(level3)+','+str(level3_name)+','+str(doctor_id)+','+str(doctor_name)+','+str(submit_by_id)+','+str(submit_by_name)+','+str(rx_type)+','+str(medicine_name)+'\n'
                    #-----------
    
                import gluon.contenttype
                response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
                response.headers['Content-disposition'] = 'attachment; filename=download_prescription_seen.csv'
                return str(myString)
    
    
    
    
    return dict(records=records,totalCount=totalCount, page=page, items_per_page=items_per_page)


#------------------------
def prescription_details():
    task_id_view = 'rm_doctor_visit_view'
    access_permission_view = check_role(task_id_view)
    if (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL('prescription_list'))
        
    #   ---------------------
    response.title = 'Prescription Details'
    
    c_id = session.cid
    
    page = request.args(0)
    rowid = request.args(1)
    
    repRows=[]
    detailsRow=[]
    headRow = db((db.sm_prescription_seen_head.cid == c_id) & (db.sm_prescription_seen_head.id == rowid)).select(db.sm_prescription_seen_head.sl,db.sm_prescription_seen_head.doctor_id,db.sm_prescription_seen_head.doctor_name,db.sm_prescription_seen_head.area_id,db.sm_prescription_seen_head.area_name,db.sm_prescription_seen_head.created_on,db.sm_prescription_seen_head.submit_by_name,db.sm_prescription_seen_head.submit_by_id,db.sm_prescription_seen_head.rx_type,db.sm_prescription_seen_head.image_name, limitby=(0, 1))
    if not headRow:
        session.flash = 'Invalid request'
        redirect (URL('prescription_list'))
    else: 
        hsl=headRow[0].sl
        submit_by_id=headRow[0].submit_by_id
        
        repRows = db((db.sm_rep.cid == c_id) & (db.sm_rep.rep_id == submit_by_id)).select(db.sm_rep.mobile_no,limitby=(0,1))
                
        detailsRow = db((db.sm_prescription_seen_details.cid == c_id) & (db.sm_prescription_seen_details.sl == hsl)).select(db.sm_prescription_seen_details.medicine_name)
        
    return dict(page=page, headRow=headRow,detailsRow=detailsRow,repRows=repRows)

