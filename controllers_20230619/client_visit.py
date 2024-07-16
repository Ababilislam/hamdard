
#visit plan
def visit_plan():
    #----------Task assaign----------
    task_id='rm_visit_plan_manage'
    task_id_view='rm_visit_plan_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    #   ---------------------
    response.title='Visit Plan'
    cid=session.cid
    
    #If catagorey not in item it can be delete
    btn_approved_filter=request.vars.btn_approved_filter
    btn_approved=request.vars.btn_approved
    if btn_approved_filter or btn_approved:  
        yearValue=request.vars.yearValue
        monthValue=request.vars.monthValue      
        spo_idname=request.vars.spo_idname
        
        if (yearValue=='' or monthValue=='' or spo_idname==''):
            response.flash='Value Required'
        else:
            if btn_approved_filter:
                spo_id=str(spo_idname).split('|')[0]
                if spo_id=='':
                    response.flash='Invalid SPO'
                else:
                    validRep=True
                    if session.user_type=='Supervisor': #not used because supervisor also have visit plan
                        if spo_id!=session.user_id:                        
                            repAreaRow=db((db.sm_rep_area.cid==cid) & (db.sm_rep_area.rep_id==spo_id) & (db.sm_rep_area.area_id.belongs(session.marketList))).select(db.sm_rep_area.rep_id,limitby=(0,1))
                            if not repAreaRow:
                                response.flash='SPO-Client/Retailer not available'
                                validRep=False
                    
                    if validRep==True:                    
                        session.yearValue=yearValue
                        session.monthValue=monthValue
                        session.spo_idname=spo_idname
                        session.spo_id=spo_id
                        
                        session.btn_approved_filter=btn_approved_filter
                        session.btn_filter_vp=None
                        session.search_type_vp=None
                        session.search_value_vp=None
    
    #Cancelled
    btn_delete=request.vars.btn_delete
    if btn_delete:
        record_id=request.args[1]
        check_cancel=request.vars.check_cancel
        if check_cancel!='YES':
            response.flash='Check Confirmation Required'
        else:
            planRecords=db((db.sm_visit_plan.cid==cid)& (db.sm_visit_plan.id==record_id) & (db.sm_visit_plan.status=='Submitted')).select(db.sm_visit_plan.id,limitby=(0,1))
            if planRecords:
                planRecords[0].update_record(status='Cancelled')
            else:
                response.flash='Invalid request'
    
    #------------------filter
    btn_filter_vp=request.vars.btn_filter
    btn_filter_vp_all=request.vars.btn_all
    reqPage=len(request.args)
    if btn_filter_vp:
        session.btn_filter_vp=btn_filter_vp
        session.search_type_vp=request.vars.search_type
        session.search_value_vp=str(request.vars.search_value).strip().upper()
        
        session.btn_approved_filter=None
        session.yearValue=None
        session.monthValue=None
        session.spo_idname=None
        session.spo_id=None
        
        reqPage=0
        
    elif btn_filter_vp_all:
        session.btn_filter_vp=None
        session.search_type_vp=None
        session.search_value_vp=None
        
        session.btn_approved_filter=None
        session.yearValue=None
        session.monthValue=None
        session.spo_idname=None
        session.spo_id=None
        
        reqPage=0
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=30
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging    
    
    qset=db()
    qset=qset(db.sm_visit_plan.cid==cid)
    if session.user_type=='Depot':
        qset=qset(db.sm_visit_plan.depot_id==session.depot_id)    
    else:
        if (session.btn_filter_vp and session.search_type_vp=='DepotID'):
            searchValue=str(session.search_value_vp).split('|')[0]
            qset=qset(db.sm_visit_plan.depot_id==searchValue)
    
    
    #---- supervisor
    if session.user_type=='Supervisor':
        qset=qset(db.sm_visit_plan.route_id.belongs(session.marketList))
    else:
        pass
    #----
    
    if session.btn_filter_vp:
        if (session.search_type_vp=='RepID'):
            searchValue=str(session.search_value_vp).split('|')[0]
            qset=qset(db.sm_visit_plan.rep_id==searchValue)
            
        elif (session.search_type_vp=='ClientID'):
            searchValue=str(session.search_value_vp).split('|')[0]
            qset=qset(db.sm_visit_plan.client_id==searchValue)
            
        elif (session.search_type_vp=='AreaID'):
            searchValue=str(session.search_value_vp).split('|')[0]
            qset=qset(db.sm_visit_plan.route_id==searchValue)
            
        elif (session.search_type_vp=='Status'):
            qset=qset(db.sm_visit_plan.status==session.search_value_vp)
            
        elif (session.search_type_vp=='VisitedFlag'):
            try:
                searchValue=int(session.search_value_vp) 
            except:
                searchValue=''
            
            qset=qset(db.sm_visit_plan.visited_flag==searchValue)
    
    elif session.btn_approved_filter:
        first_date=str(session.yearValue)+'-'+str(session.monthValue)+'-01'
        rep_id=session.spo_id
        qset=qset((db.sm_visit_plan.first_date==first_date)&(db.sm_visit_plan.rep_id==rep_id))
        
        if btn_approved:
            planRecords=qset(db.sm_visit_plan.status=='Submitted').count()
            if planRecords>0:
                updateRecords=qset(db.sm_visit_plan.status=='Submitted').update(status='Approved')
            else:
                response.flash='Data not available'
                
    records=qset.select(db.sm_visit_plan.ALL,orderby=~db.sm_visit_plan.schedule_date|db.sm_visit_plan.rep_id|db.sm_visit_plan.client_id,limitby=limitby) 
    
    return dict(records=records,page=page,items_per_page=items_per_page,access_permission=access_permission,access_permission_view=access_permission_view)
    
    
def visit_plan_batch_upload():
    task_id='rm_visit_plan_manage'
    access_permission=check_role(task_id)
    if access_permission==False:
        session.flash='Access is Denied !'
        redirect (URL('visit_plan'))
    
    response.title='Visit Plan Batch Upload'
    
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
        
        rep_list_excel=[]
        client_list_excel=[]
        client_list_exist=[]
        rep_list_exist=[]
        
        excelList=[]
        
        area_list_excel=[]
        existLevel_list=[]
        
        ins_list=[]
        ins_dict={}
        
        for i in range(total_row):
            if i>=30:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==3:
                    rep_list_excel.append(str(coloum_list[1]).strip().upper())
                    client_list_excel.append(str(coloum_list[2]).strip().upper())
        
        #        create rep list
        existRepRows=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id.belongs(rep_list_excel))&(db.sm_rep.status=='ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,orderby=db.sm_rep.rep_id)
        rep_list_exist=existRepRows.as_list()            
        
        #        create client list        
        existClientRows=db((db.sm_client.cid==c_id)&(db.sm_client.client_id.belongs(client_list_excel))&(db.sm_client.status=='ACTIVE')).select(db.sm_client.client_id,db.sm_client.name,db.sm_client.area_id,db.sm_client.depot_id,db.sm_client.depot_name,orderby=db.sm_client.client_id)
        client_list_exist=existClientRows.as_list()
        
        #   --------------------     
        for i in range(total_row):
            if i>=30: 
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
                spo_id_ex=str(coloum_list[1]).strip().upper()
                clID_ex=str(coloum_list[2]).strip().upper()
                
                if (clID_ex=='' or spo_id_ex==''):
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
                    valid_rep=False
                    valid_client=False
                    
                    firstDate=str(date_ex)[0:7]+'-01'
                    repName=''
                    depot_id=''
                    clientName=''
                    area_id=''
                    
                    #----------- check valid spo                                                      
                    for i in range(len(rep_list_exist)):
                        myRowData1=rep_list_exist[i]                                
                        rep_id=myRowData1['rep_id']
                        if (str(rep_id).strip()==str(spo_id_ex).strip()):
                            valid_rep=True
                            repName=myRowData1['name']
                            break
                    
                    if valid_rep==True:#---------- check valid client
                        for i in range(len(client_list_exist)):
                            myRowData2=client_list_exist[i]                        
                            client_id=myRowData2['client_id']                            
                            if (str(client_id).strip()==str(clID_ex).strip()):
                                valid_client=True
                                clientName=myRowData2['name']
                                area_id=myRowData2['area_id']
                                depot_id=myRowData2['depot_id']
                                depot_name=myRowData2['depot_name']                           
                                break
                    
                    #------------
                    if session.user_type=='Supervisor':
                        repAreaRow=db((db.sm_rep_area.cid==c_id) & (db.sm_rep_area.rep_id==spo_id_ex) & (db.sm_rep_area.area_id.belongs(session.marketList))).select(db.sm_rep_area.rep_id,limitby=(0,1))
                        if not repAreaRow:
                            error_data=row_data+'(SPO not accessed!)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:
                            pass
                        
                        #----
                        sueprvisorMarketList=session.marketList
                        if area_id not in sueprvisorMarketList:
                            error_data=row_data+'(Retailer not accessed!)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:
                            pass
                    else:
                        pass
                    #-----------
                    
                    if valid_client==True:#---------- check valid spo-market                            
                        rep_areaRow=db((db.sm_rep_area.cid==c_id) & (db.sm_rep_area.rep_id==spo_id_ex) & (db.sm_rep_area.client_id==clID_ex)).select(db.sm_rep_area.rep_id,limitby=(0,1))    
                        if not rep_areaRow :
                            error_data=row_data+'(SPO-Client/Retailer required)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:
                            pass
                    
                    #-----------------
                    if(valid_rep==False):
                        error_data=row_data+'(Invalid SPO)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue                        
                    else:
                        if valid_client==False:
                            error_data=row_data+'(Invalid Retailer)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:
                            existRow=db((db.sm_visit_plan.cid==c_id) & (db.sm_visit_plan.rep_id==spo_id_ex) & (db.sm_visit_plan.schedule_date==date_ex) & (db.sm_visit_plan.client_id==clID_ex) & (db.sm_visit_plan.status!='Cancelled')).select(db.sm_visit_plan.rep_id,limitby=(0,1))    
                            if existRow :
                                error_data=row_data+'(Already exist)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                            else:
                                #Create insert list
                                routeRow=db((db.sm_level.cid==c_id) & (db.sm_level.level_id==area_id) & (db.sm_level.is_leaf=='1')).select(db.sm_level.level_name,db.sm_level.level0,db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
                                if not routeRow:
                                    error_data=row_data+'(Invalid Market in client)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue                                
                                else:
                                    market_name=routeRow[0].level_name                                    
                                    level0_id=routeRow[0].level0
                                    level1_id=routeRow[0].level1
                                    level2_id=routeRow[0].level2
                                    
                                    level0_name=''                    
                                    level1_name=''
                                    level2_name=''
                                    
#                                    depotRow=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
#                                    if depotRow:
#                                        depot_name=depotRow[0].name
                                        
                                    level0Row=db((db.sm_level.cid==c_id) & (db.sm_level.level_id==level0_id) & (db.sm_level.is_leaf=='0')).select(db.sm_level.level_name,limitby=(0,1))
                                    if level0Row:
                                        level0_name=level0Row[0].level_name
                                        
                                    level1Row=db((db.sm_level.cid==c_id) & (db.sm_level.level_id==level1_id) & (db.sm_level.is_leaf=='0')).select(db.sm_level.level_name,limitby=(0,1))
                                    if level1Row:
                                        level1_name=level1Row[0].level_name
                                        
                                    level2Row=db((db.sm_level.cid==c_id) & (db.sm_level.level_id==level2_id) & (db.sm_level.is_leaf=='0')).select(db.sm_level.level_name,limitby=(0,1))
                                    if level2Row:
                                        level2_name=level2Row[0].level_name
                                        
                                try:
                                    ins_dict= {'cid':c_id,'rep_id':spo_id_ex,'rep_name':repName,'first_date':firstDate,'schedule_date':date_ex,'client_id':clID_ex,'client_name':clientName,'route_id':area_id,'route_name':market_name,'depot_id':depot_id,
                                               'depot_name':depot_name,'level2_id':level2_id,'level2_name':level2_name,'level1_id':level1_id,'level1_name':level1_name,'level0_id':level0_id,'level0_name':level0_name}
                                    ins_list.append(ins_dict)                               
                                    count_inserted+=1
                                except:
                                    error_data=row_data+'(error in process!)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue            
        
        if error_str=='':
            error_str='No error'
        
        if len(ins_list) > 0:
            inCountList=db.sm_visit_plan.bulk_insert(ins_list)             
            
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)


def download_visit_plan():
    task_id='rm_visit_plan_manage'
    task_id_view='rm_visit_plan_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('visit_plan'))      
    
    #   ---------------------
    c_id=session.cid
    
    records=''
    qset=db()
    qset=qset(db.sm_visit_plan.cid==c_id)
    if session.user_type=='Depot':
        qset=qset(db.sm_visit_plan.depot_id==session.depot_id)    
    else:
        if (session.btn_filter_vp and session.search_type_vp=='DepotID'):
            searchValue=str(session.search_value_vp).split('|')[0]
            qset=qset(db.sm_visit_plan.depot_id==searchValue)
    
    
    #---- supervisor
    if session.user_type=='Supervisor':
        qset=qset(db.sm_visit_plan.route_id.belongs(session.marketList))
    else:
        pass
    #----
    
    if session.btn_filter_vp:
        if (session.search_type_vp=='ClientID'):
            searchValue=str(session.search_value_vp).split('|')[0]
            qset=qset(db.sm_visit_plan.client_id==searchValue)
            
        elif (session.search_type_vp=='AreaID'):
            searchValue=str(session.search_value_vp).split('|')[0]
            qset=qset(db.sm_visit_plan.route_id==searchValue)
            
        elif (session.search_type_vp=='VisitedFlag'):            
            try:
                searchValue=int(session.search_value_vp) 
            except:
                searchValue=''
            
            qset=qset(db.sm_visit_plan.visited_flag==searchValue)
        
        elif (session.search_type_vp=='DepotID'):
            pass
        
        else:
            session.flash='Need filter'
            redirect(URL('visit_plan'))
        
    else:
        session.flash='Need filter'
        redirect(URL('visit_plan'))
    
    records=qset.select(db.sm_visit_plan.ALL,orderby=~db.sm_visit_plan.schedule_date|db.sm_visit_plan.rep_id|db.sm_visit_plan.client_id) 
    
    #---------
    myString='Visit Plan \n\n'
    myString+='Schedule date,SPO ID,SPO Name,Retailer ID,Retailer Name,Market ID,Market Name,Depot ID,Depot Name,Visited?,Visit Sl,Visit Date\n'
    for rec in records:
        schedule_date=str(rec.schedule_date)
        rep_id=str(rec.rep_id)
        rep_name=str(rec.rep_name).replace(',', ' ')
        client_id=str(rec.client_id)
        client_name=str(rec.client_name).replace(',', ' ')
        route_id=str(rec.route_id)
        route_name=str(rec.route_name).replace(',', ' ')
        
        depot_id=str(rec.depot_id)
        depot_name=str(rec.depot_name).replace(',', ' ')
        visited_flag=str(rec.visited_flag)
        visit_sl=str(rec.visit_sl)
        visit_date=str(rec.visit_date)
        
        myString+=schedule_date+','+rep_id+','+rep_name+','+client_id+','+client_name+','+route_id+','+route_name+','+depot_id+','+depot_name+','+visited_flag+','+visit_sl+','+visit_date+'\n'
        
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_visit_plan.csv'   
    return str(myString)
    
#visit plan
def visit_details():
    #----------Task assaign----------
    task_id='rm_visit_manage'
    task_id_view='rm_visit_list_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))        
    
    #   ---------------------    
    response.title='Visit Details'
    cid=session.cid
    
    #----
    page=int(request.args[0])
    SL=request.vars.vsl
    
    
    visitRow=db((db.sm_order_head.cid==cid)&(db.sm_order_head.id==SL)).select(db.sm_order_head.ALL,limitby=(0,1))
    if not visitRow:
        redirect (URL('order_invoice','order'))#visit list
    
    #-------- 
    marketInfoRows=db((db.visit_market_info.cid==cid)&(db.visit_market_info.SL==SL)).select(db.visit_market_info.ALL,orderby=db.visit_market_info.brand_name)
    orderInfoRows=db((db.sm_order.cid==cid)&(db.sm_order.vsl==SL)).select(db.sm_order.ALL,orderby=db.sm_order.item_name)
    visitMarcRows=db((db.visit_merchandising.cid==cid)&(db.visit_merchandising.SL==SL)).select(db.visit_merchandising.ALL,orderby=db.visit_merchandising.m_item_id)
    
    #----------    
    return dict(SL=SL,visitRow=visitRow,marketInfoRows=marketInfoRows,orderInfoRows=orderInfoRows,visitMarcRows=visitMarcRows,page=page)


#complain
def complain():
    #----------Task assaign----------
    task_id='rm_feedback_manage'
    task_id_view='rm_feedback_manage'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    #   --------------------- 
    response.title='Feedback'   
    cid=session.cid
    
    #------------------filter
    btn_filter_comp=request.vars.btn_filter
    btn_filter_comp_all=request.vars.btn_all
    reqPage=len(request.args)
    if btn_filter_comp:
        session.btn_filter_comp=btn_filter_comp
        session.search_type_comp=request.vars.search_type
        session.search_value_comp=str(request.vars.search_value).strip()
        
        reqPage=0
        
    elif btn_filter_comp_all:
        session.btn_filter_comp=None
        session.search_type_comp=None
        session.search_value_comp=None
        
        reqPage=0
    
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=30
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging    
    
    qset=db()
    qset=qset(db.complain.cid==cid)
    
    
    #---- supervisor
    if session.user_type=='Supervisor':
        repList=[]
        reprows = db((db.sm_rep_area.cid == cid)&(db.sm_rep_area.area_id.belongs(session.marketList))).select(db.sm_rep_area.rep_id,groupby=db.sm_rep_area.rep_id)
        for reprow in reprows:
            repList.append(reprow.rep_id)
        
        qset=qset(db.complain.submitted_by_id.belongs(repList))
        
    else:
        if session.user_type=='Depot':
            repList=[]            
            reprows = db((db.sm_rep_area.cid == cid)&(db.sm_rep_area.depot_id==session.depot_id)).select(db.sm_rep_area.rep_id,groupby=db.sm_rep_area.rep_id)
            for reprow in reprows:
                repList.append(reprow.rep_id)
            
            qset=qset(db.complain.submitted_by_id.belongs(repList))
            
        else:
            pass
    #----
    
    if session.btn_filter_comp:
        if (session.search_type_comp=='SubmitBy'):
            searchValue=str(session.search_value_comp).split('|')[0]
            qset=qset(db.complain.submitted_by_id==searchValue)
            
        elif (session.search_type_comp=='ComplainFrom'):
            searchValue=str(session.search_value_comp).split('|')[0]
            qset=qset(db.complain.complain_from==searchValue)
            
        elif (session.search_type_comp=='ComplainType'):
            searchValue=str(session.search_value_comp).split('|')[0]
            qset=qset(db.complain.complain_type==searchValue)
        
        elif (session.search_type_comp=='Status'):
            qset=qset(db.complain.status==session.search_value_comp)
        
        elif (session.search_type_comp=='Action'):
            qset=qset(db.complain.action==session.search_value_comp)
        
        
    records=qset.select(db.complain.ALL,orderby=~db.complain.id,limitby=limitby) 
    
    return dict(records=records,page=page,items_per_page=items_per_page,access_permission=access_permission,access_permission_view=access_permission_view)

def complain_update():
    task_id='rm_feedback_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied'
        redirect (URL('complain'))   
    
    response.title='Feedback Update'
    cid=session.cid
    
    
    page=request.args(0)
    rowid=request.args(1)    
    
    record= db.complain(rowid)
    
    db.complain.reply_msg.requires=IS_NOT_EMPTY()
    db.complain.action.requires=IS_IN_SET(('Pending','Resolved'))
    
    form =SQLFORM(db.complain,
                  record=record,
                  deletable=True,
                  fields=['reply_msg','action'],
                  submit_button='Update'
                  )
    
    #--------------
    if form.accepts(request.vars, session):
        response.flash = 'Updated Successfully'
        redirect(URL('complain',args=[page]))
    
    submit_date=''
    submitted_by_id=''
    submitted_by_name=''
    complain_from=''
    ref=''
    complain_type=''
    des=''
    action=''
    
    complainRows=db((db.complain.cid==cid) & (db.complain.id==rowid)).select(db.complain.ALL,limitby=(0,1))
    if complainRows:
        submit_date=complainRows[0].submit_date
        submitted_by_id=complainRows[0].submitted_by_id
        submitted_by_name=complainRows[0].submitted_by_name
        complain_from=complainRows[0].complain_from
        ref=complainRows[0].ref
        complain_type=complainRows[0].complain_type
        des=complainRows[0].des
        action=complainRows[0].action
        
    return dict(form=form,submit_date=submit_date,submitted_by_id=submitted_by_id,submitted_by_name=submitted_by_name,complain_from=complain_from,ref=ref,complain_type=complain_type,des=des,action=action,page=page)


#task

def validation_task(form):
    cid=session.cid
    
    spo_id=str(request.vars.spo_id).strip().upper().split('|')[0]
    
    dateFlag=True
    try:
        task_datetime=datetime.datetime.strptime(str(request.vars.task_datetime),'%Y-%m-%d %H:%M:%S')
    except:
        dateFlag=False
    
    if dateFlag==False:
        form.errors.task_datetime='Invalid Date'
    else:
        #---- supervisor
        if session.user_type=='Supervisor':
            rows_check = db((db.sm_rep_area.cid == cid)&(db.sm_rep_area.rep_id == spo_id)&(db.sm_rep_area.area_id.belongs(session.marketList))).select(db.sm_rep_area.rep_id,groupby=db.sm_rep_area.rep_id)
            if not rows_check:
                pass
            else:
                rows_check=db((db.sm_rep.cid==cid) & (db.sm_rep.rep_id==spo_id)).select(db.sm_rep.name,limitby=(0,1))
            
        else:
            rows_check=db((db.sm_rep.cid==cid) & (db.sm_rep.rep_id==spo_id)).select(db.sm_rep.name,limitby=(0,1))    
        
        if not rows_check :
            form.errors.spo_id='Invalid SPO'
        else:
            spo_name=rows_check[0].name
            
            form.vars.spo_id=spo_id
            form.vars.spo_name=spo_name
            form.vars.task_date=task_datetime
       
def task():
    #----------Task assaign----------
    task_id='rm_task_manage'
    task_id_view='rm_task_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))        
    
    #   --------------------- 
    response.title='Task'   
    cid=session.cid
    
    #------------------filter
    btn_filter_task=request.vars.btn_filter
    btn_filter_task_all=request.vars.btn_all
    reqPage=len(request.args)
    if btn_filter_task:
        session.btn_filter_task=btn_filter_task
        session.search_type_task=request.vars.search_type
        session.search_value_task=str(request.vars.search_value).strip()
        
        reqPage=0
        
    elif btn_filter_task_all:
        session.btn_filter_task=None
        session.search_type_task=None
        session.search_value_task=None
        
        reqPage=0
    
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=30
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging    
    
    db.task.task_type.requires=IS_IN_DB(db((db.sm_category_type.cid == session.cid)&(db.sm_category_type.type_name=='TASK_TYPE')),db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id)
    form =SQLFORM(db.task,
                  fields=['task_type','spo_id','task','task_datetime'],
                  submit_button='Save'       
                  )
    
    form.vars.cid=cid
    if form.accepts(request.vars,session,onvalidation=validation_task):
       response.flash = 'Submitted Successfully'
    
    
    #-------------    
    qset=db()
    qset=qset(db.task.cid==cid)
    
    
    #---- supervisor
    if session.user_type=='Supervisor':
        repList=[]
        reprows = db((db.sm_rep_area.cid == cid)&(db.sm_rep_area.area_id.belongs(session.marketList))).select(db.sm_rep_area.rep_id,groupby=db.sm_rep_area.rep_id)
        for reprow in reprows:
            repList.append(reprow.rep_id)
        
        qset=qset(db.task.spo_id.belongs(repList))
        
    else:
        if session.user_type=='Depot':
            repList=[]            
            reprows = db((db.sm_rep_area.cid == cid)&(db.sm_rep_area.depot_id==session.depot_id)).select(db.sm_rep_area.rep_id,groupby=db.sm_rep_area.rep_id)
            for reprow in reprows:
                repList.append(reprow.rep_id)
            
            qset=qset(db.task.spo_id.belongs(repList))
            
        else:
            pass
    
    #----
    
    if session.btn_filter_task:
        if (session.search_type_task=='SpoID'):
            searchValue=str(session.search_value_task).split('|')[0]
            qset=qset(db.task.spo_id==searchValue)
        
        elif (session.search_type_task=='TaskType'):
            searchValue=str(session.search_value_task).split('|')[0]
            qset=qset(db.task.task_type==searchValue)
        
        elif (session.search_type_task=='Status'):
            qset=qset(db.task.status==session.search_value_task)
        
    records=qset.select(db.task.ALL,orderby=~db.task.id,limitby=limitby) 
    
    return dict(form=form,records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)
    
    
    
