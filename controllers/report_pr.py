
#====================== Doctor Visit

from random import randint

#---------------------------- ADD
def index():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

    response.title = 'Prescription Report'
    

    comRows = db((db.sm_settings.cid == session.cid) & (db. sm_settings.s_key == 'COM_NAME')).select(db.sm_settings.field1, limitby=(0, 1))
    if comRows:
        company_name=comRows[0].field1         
        session.company_name=company_name
        

    c_id = session.cid

    search_form =SQLFORM(db.sm_search_date)
    
    
    btn_prSummary=request.vars.btn_prSummary
    btn_prSummaryD=request.vars.btn_prSummaryD
    
    btn_prNewRSMSummary=request.vars.btn_prNewRSMSummary
    
    btn_prNewSummary=request.vars.btn_prNewSummary
    btn_drSummary=request.vars.btn_drSummary
    btn_zeroDrList=request.vars.btn_zeroDrList
    btn_regSummary=request.vars.btn_regSummary
    btn_ProSummary=request.vars.btn_ProSummary
    
    btn_prdSummary=request.vars.btn_prdSummary
    
    btn_regionSummary=request.vars.btn_regionSummary
    btn_tlSummary=request.vars.btn_tlSummary
    btn_areaSummary=request.vars.btn_areaSummary
    btn_mpoSummary=request.vars.btn_mpoSummary

    if (btn_mpoSummary or btn_areaSummary or btn_tlSummary or btn_regionSummary or btn_regSummary or btn_prSummary or btn_prSummaryD or btn_prNewSummary or btn_prNewRSMSummary or btn_drSummary or btn_zeroDrList or btn_ProSummary ):
        date_from=request.vars.from_dt_3
        date_to=request.vars.to_dt_3
        
        depot=str(request.vars.sales_depot_id_SC)
        rsm_SC=''#str(request.vars.rsm_SC)
        fm_SC=''#str(request.vars.fm_SC)
        tr_SC=''#str(request.vars.tr_SC)
        mso=''#str(request.vars.mso_id_sales).replace(",","").replace("['","").replace("']","").replace("''","")
        doc_idname=''#str(request.vars.doc_id_sales).replace(",","").replace("['","").replace("']","").replace("''","")
        
        product=''#str(request.vars.product)
        brand=str(request.vars.brand)
        category=str(request.vars.category)
        
        if (len(mso) < 4):
            mso=''
            
            
        brand=brand
        category=category
        
        
        depot_id=depot
        depot_name=''
        
        
        dateFlag=True
        #           return 'asfsaf'
        try:
            from_dt2=datetime.datetime.strptime(str(date_from),'%Y-%m-%d')
        except:
            dateFlag=False
        
        
        if ((depot!='') & (depot.find('|') != -1)):             
            depot_id=depot.split('|')[0].upper().strip()
            depot_name=depot.split('|')[1].strip()
            
        else:
            depot_id=depot
            depot_name=''
        
        
        if ((product!='')) : 
            product_id=product.split('|')[0].upper().strip()
            product_name=product.split('|')[1].strip()
        else:
            product_id=product
            product_name=''    
        if ((rsm_SC!='')) : 
            rsm_id=rsm_SC.split('|')[0].upper().strip()
            rsm_name=rsm_SC.split('|')[1].strip()
        else:
            rsm_id=rsm_SC
            rsm_name=''
        if ((fm_SC!='') & (fm_SC.find('|') != -1)) : 
            fm_id=fm_SC.split('|')[0].upper().strip()
            fm_name=fm_SC.split('|')[1].strip()
        else:
            fm_id=fm_SC
            fm_name=''
        if ((tr_SC!='') & (tr_SC.find('|') != -1)) : 
            tr_id=tr_SC.split('|')[0].upper().strip()
            tr_name=tr_SC.split('|')[1].strip()
        else:
            tr_id=tr_SC
            tr_name=''
        if ((mso!='') & (mso.find('|') != -1)) :  
            mso_id=mso.split('|')[0].upper().strip()
            mso_name=mso.split('|')[1].strip()
        else:
              mso_id=mso
              mso_name=''
        
        if ((doc_idname!='') & (doc_idname.find('|') != -1)) :  
            doc=doc_idname.split('|')[0].upper().strip()
            doc_name=doc_idname.split('|')[1].strip()
        else:
              doc=doc_idname
              doc_name=''
        
#         return mso_id
        dateDiff=0
        dateFlag=True
        try:
          from_dt2=datetime.datetime.strptime(str(date_from),'%Y-%m-%d')
          to_dt2=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 

          if from_dt2>to_dt2:
             dateFlag=False
        except:
            dateFlag=False
    
        if dateFlag==False:
            response.flash="Invalid Date Range"
        else:            
            dateDiff=(to_dt2-from_dt2).days
        if dateDiff>90:
            response.flash="Maximum 90 days allowed between Date Range"
            dateFlag=False
        if ((depot!='') & (depot.find('|') != -1)):             
                depot_id=depot.split('|')[0].upper().strip()
                depot_name=depot.split('|')[1].strip()
                user_depot_address=''
                if session.user_type!='Depot': 
                    depotRows = db((db.sm_depot.cid == session.cid) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.name,db.sm_depot.depot_category,db.sm_depot.field1, limitby=(0, 1))
                    if depotRows:
                        user_depot_address=depotRows[0].field1         
                        session.user_depot_address=user_depot_address
        else:
             session.user_depot_address='' 
#         return    dateFlag  
        if dateFlag!=False:
            
            if btn_prSummary:
                redirect (URL('prSummary',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name,brand=brand,category=category,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            if btn_prSummaryD:
                redirect (URL('prSummaryD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name,brand=brand,category=category,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            
            if btn_prNewRSMSummary:
                redirect (URL('prNewRSMSummary',vars=dict(date_from=date_from,date_to=date_to,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            
            if btn_prNewSummary:
                redirect (URL('prNewSummary',vars=dict(date_from=date_from,date_to=date_to,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            
            if btn_drSummary:
                redirect (URL('drSummary',vars=dict(date_from=date_from,date_to=date_to,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            if btn_zeroDrList:
                redirect (URL('zeroDrList',vars=dict(date_from=date_from,date_to=date_to,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            if btn_regSummary:
                redirect (URL('regSummary',vars=dict(date_from=date_from,date_to=date_to,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            
            if btn_ProSummary:
                redirect (URL('productWiseSummary',vars=dict(date_from=date_from,date_to=date_to,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            
            if btn_regionSummary:
                redirect (URL('regionWiseSummary',vars=dict(date_from=date_from,date_to=date_to,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            if btn_tlSummary:
                redirect (URL('tlWiseSummary',vars=dict(date_from=date_from,date_to=date_to,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            if btn_areaSummary:
                redirect (URL('areaWiseSummary',vars=dict(date_from=date_from,date_to=date_to,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            if btn_mpoSummary:
                redirect (URL('mpoWiseSummary',vars=dict(date_from=date_from,date_to=date_to,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            
            
            
    
    if btn_prdSummary:
            dateFlag=True
            from_dt_get=str(request.vars.from_dt_2).strip()
            try:
              date_from=datetime.datetime.strptime(str(from_dt_get),'%Y-%m-%d')
              date_to=date_from + datetime.timedelta(days = 1) 

            except:
                dateFlag=False
           
            if dateFlag==True:
                redirect (URL('prdSummary',vars=dict(date_from=date_from,date_to=date_to)))
    return dict(search_form=search_form)

#---------------------------- Reports

def mpoWiseSummary():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))
    

    c_id = session.cid
    response.title='MPO Wise Summary'    
    date_from=request.vars.date_from
    date_to_get=request.vars.date_to
  
    
    qset=db()
    qset = qset(db.sm_prescription_head.cid == c_id)
    qset = qset(db.sm_prescription_head.submit_date >= date_from)
    qset = qset(db.sm_prescription_head.submit_date <= date_to_get)
    
    
    records = qset.select(db.sm_prescription_head.reg_id,db.sm_prescription_head.reg_name,db.sm_prescription_head.tl_id,db.sm_prescription_head.tl_name,db.sm_prescription_head.area_id,db.sm_prescription_head.area_name,db.sm_prescription_head.submit_by_id,db.sm_prescription_head.submit_by_name,db.sm_prescription_head.id.count(),orderby=db.sm_prescription_head.reg_id|db.sm_prescription_head.tl_id|db.sm_prescription_head.area_id|db.sm_prescription_head.submit_by_id,groupby= db.sm_prescription_head.reg_id|db.sm_prescription_head.tl_id|db.sm_prescription_head.area_id|db.sm_prescription_head.submit_by_id)
    
    return dict(records=records,date_from=date_from,date_to=date_to_get)

def areaWiseSummary():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))
    

    c_id = session.cid
    response.title='Territory Wise Summary'    
    date_from=request.vars.date_from
    date_to_get=request.vars.date_to
  
    
    qset=db()
    qset = qset(db.sm_prescription_head.cid == c_id)
    qset = qset(db.sm_prescription_head.submit_date >= date_from)
    qset = qset(db.sm_prescription_head.submit_date <= date_to_get)
    
    
    records = qset.select(db.sm_prescription_head.reg_id,db.sm_prescription_head.reg_name,db.sm_prescription_head.tl_id,db.sm_prescription_head.tl_name,db.sm_prescription_head.area_id,db.sm_prescription_head.area_name,db.sm_prescription_head.id.count(),orderby=db.sm_prescription_head.reg_id|db.sm_prescription_head.tl_id|db.sm_prescription_head.area_id,groupby= db.sm_prescription_head.reg_id|db.sm_prescription_head.tl_id|db.sm_prescription_head.area_id)
    
    return dict(records=records,date_from=date_from,date_to=date_to_get)

def tlWiseSummary():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))
    

    c_id = session.cid
    response.title='Area Wise Summary'    
    date_from=request.vars.date_from
    date_to_get=request.vars.date_to
  
    
    qset=db()
    qset = qset(db.sm_prescription_head.cid == c_id)
    qset = qset(db.sm_prescription_head.submit_date >= date_from)
    qset = qset(db.sm_prescription_head.submit_date <= date_to_get)
    
    
    records = qset.select(db.sm_prescription_head.reg_id,db.sm_prescription_head.reg_name,db.sm_prescription_head.tl_id,db.sm_prescription_head.tl_name,db.sm_prescription_head.id.count(),orderby=db.sm_prescription_head.reg_id|db.sm_prescription_head.tl_id,groupby= db.sm_prescription_head.reg_id|db.sm_prescription_head.tl_id)
    
    return dict(records=records,date_from=date_from,date_to=date_to_get)

def regionWiseSummary():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))
    

    c_id = session.cid
    response.title='Region Wise Summary'    
    date_from=request.vars.date_from
    date_to_get=request.vars.date_to
  
    
#    date_to_2=datetime.datetime.strptime(str(date_to_get),'%Y-%m-%d')
#    date_to_1=date_to_2 + datetime.timedelta(days = 1) 
#       
#    date_to=str(date_to_1)[0:10]
   
   
    qset=db()
    qset = qset(db.sm_prescription_head.cid == c_id)
    qset = qset(db.sm_prescription_head.submit_date >= date_from)
    qset = qset(db.sm_prescription_head.submit_date <= date_to_get)
    
    
    records = qset.select(db.sm_prescription_head.reg_id,db.sm_prescription_head.reg_name,db.sm_prescription_head.id.count(),orderby=db.sm_prescription_head.reg_id,groupby= db.sm_prescription_head.reg_id)
    
    return dict(records=records,date_from=date_from,date_to=date_to_get)

def productWiseSummary():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))
    

    c_id = session.cid
    response.title='Product Wise Summary'    
    date_from=request.vars.date_from
    date_to_get=request.vars.date_to
  
    
    date_to_2=datetime.datetime.strptime(str(date_to_get),'%Y-%m-%d')
    date_to_1=date_to_2 + datetime.timedelta(days = 1) 
       
    date_to=str(date_to_1)[0:10]
   
   
    qset=db()
    qset = qset(db.sm_prescription_details.cid == c_id)
    qset = qset(db.sm_prescription_details.submit_date >= date_from)
    qset = qset(db.sm_prescription_details.submit_date < date_to)
    qset = qset(db.sm_prescription_details.med_type =='Self')
    records = qset.select(db.sm_prescription_details.medicine_id,db.sm_prescription_details.medicine_name,db.sm_prescription_details.id.count(),orderby=db.sm_prescription_details.medicine_id,groupby= db.sm_prescription_details.medicine_id)
    
    return dict(records=records,date_from=date_from,date_to=date_to_get)

    

def prSummary():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))
    

    c_id = session.cid
    response.title='Prescription Summary'    
    date_from=request.vars.date_from
    date_to_get=request.vars.date_to
  
    
    date_to_2=datetime.datetime.strptime(str(date_to_get),'%Y-%m-%d')
    date_to_1=date_to_2 + datetime.timedelta(days = 1) 
       
    date_to=str(date_to_1)[0:10]
   
   
#     updateTableStr="update sm_prescription_head a, sm_prescription_details d set d.submit_date =a.submit_date,d.first_date=a.first_date,d.submit_by_id=a.submit_by_id,d.submit_by_name=a.submit_by_name,d.user_type=a.user_type,d.doctor_id=a.doctor_id,d.doctor_name=a.doctor_name,d.image_name=a.image_name,d.image_path=a.image_path,d.lat_long=a.lat_long,d.area_id=a.area_id,d.area_name=a.area_name,d.tl_id=a.tl_id,d.tl_name=a.tl_name,d.reg_id=a.reg_id,d.reg_name=a.reg_name where d.submit_by_id='' and a.cid=d.cid and a.sl=d.sl;"
#     updateTable=db.executesql(updateTableStr) 
   
   
    qset=db()
    qset = qset(db.sm_prescription_head.cid == c_id)
    qset = qset(db.sm_prescription_head.submit_date >= date_from)
    qset = qset(db.sm_prescription_head.submit_date < date_to)
    records = qset.select(db.sm_prescription_head.reg_id,db.sm_prescription_head.reg_name,db.sm_prescription_head.tl_id,db.sm_prescription_head.tl_name,db.sm_prescription_head.area_id,db.sm_prescription_head.area_name,db.sm_prescription_head.submit_by_id,db.sm_prescription_head.submit_by_name,db.sm_prescription_head.sl.count(),db.sm_prescription_head.doctor_id,db.sm_prescription_head.doctor_name, orderby=db.sm_prescription_head.submit_by_id|db.sm_prescription_head.area_id,groupby= db.sm_prescription_head.submit_by_id|db.sm_prescription_head.area_id)
    
#     return db._lastsql
# ==============MPO List
    mpoNameList=[]
    mpoIdList=[]
    levelIDList=[]
    records_mpoS="SELECT  sup_id, sup_name, level_id FROM sm_supervisor_level WHERE cid = '"+ c_id +"'  and level_depth_no=1 GROUP BY  level_id order by level_id;"
#     return records_mpoS
    records_mpo=db.executesql(records_mpoS,as_dict = True) 
    for records_mpo in records_mpo:
        levelID=records_mpo['level_id']
        mpoID=records_mpo['sup_id']
        mpoName=records_mpo['sup_name']
        mpoNameList.append(mpoName)
        mpoIdList.append(mpoID)
        levelIDList.append(levelID)

        
# selfprescriptionCount==============================  
       
    records_selfPS="SELECT  count(distinct(sm_prescription_details.sl)) as medCount,sm_prescription_details.sl, sm_prescription_details.submit_by_id as submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.submit_by_id,sm_prescription_details.area_id order by sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id;"
    
    #return records_selfPS
    records_selfP=db.executesql(records_selfPS,as_dict = True) 
    selfCountList=[]
    selfCountCheckList=[]

    for records_selfP in records_selfP:
        selfSubId=records_selfP['submit_by_id']
        selfDocId=records_selfP['doctor_id']
        selfAreaId=records_selfP['area_id']
        selfMedCount=records_selfP['medCount']
#         pCheck=selfSubId+'.'+selfDocId+'.'+selfAreaId
        pCheck=selfSubId+'.'+selfAreaId
        selfCountCheckList.append(pCheck)
        selfCountList.append(selfMedCount)
 
# selfproductCount==============================  
       
#     records_selfPrS="SELECT  count(distinct(sm_prescription_details.medicine_id)) as medCount,sm_prescription_details.sl, sm_prescription_head.submit_by_id as submit_by_id,sm_prescription_head.doctor_id,sm_prescription_head.area_id FROM sm_prescription_head,sm_prescription_details WHERE sm_prescription_head.cid = '"+ c_id +"' and sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_head.submit_date >= '"+ date_from +"' and sm_prescription_head.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' and sm_prescription_head.sl =sm_prescription_details.sl GROUP BY  sm_prescription_head.submit_by_id,sm_prescription_head.doctor_id,sm_prescription_head.area_id order by sm_prescription_head.submit_by_id,sm_prescription_head.doctor_id,sm_prescription_head.area_id;"
    records_selfPrS="SELECT  count(sm_prescription_details.medicine_id) as medCount,sm_prescription_details.sl, sm_prescription_details.submit_by_id as submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.submit_by_id,sm_prescription_details.area_id order by sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id;"
#     return records_selfPrS
    records_selfPr=db.executesql(records_selfPrS,as_dict = True) 
    selfPrCountList=[]
    selfPrCountCheckList=[]
 
    for records_selfPr in records_selfPr:
        selfPrSubId=records_selfPr['submit_by_id']
        selfPrDocId=records_selfPr['doctor_id']
        selfPrAreaId=records_selfPr['area_id']
        selfPrMedCount=records_selfPr['medCount']
#         prCheck=selfPrSubId+'.'+selfPrDocId+'.'+selfPrAreaId
        prCheck=selfPrSubId+'.'+selfPrAreaId
        
        selfPrCountList.append(selfPrMedCount)  
        selfPrCountCheckList.append(prCheck)       
# selfproductUnique==============================  
       
    records_selfPNS="SELECT  distinct(sm_prescription_details.medicine_id) as medicine_id,sm_prescription_details.medicine_name, sm_prescription_details.submit_by_id as submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.submit_by_id,sm_prescription_details.area_id,sm_prescription_details.medicine_id order by sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id,sm_prescription_details.medicine_id;"
#     return records_selfPNS
    records_selfPN=db.executesql(records_selfPNS,as_dict = True) 
    selfProductList=[]
    selfProductDict={}
    selfSubIdPast=''
    selfDocIdPast=''
    selfAreaIdPast=''
    selfMedNameStr=''
    medName=''
    for records_selfPN in records_selfPN:
        flaStart=1
        selfSubId=records_selfPN['submit_by_id']
        selfDocId=records_selfPN['doctor_id']
        selfAreaId=records_selfPN['area_id']
        selfMedName=records_selfPN['medicine_name']
        if ((selfSubIdPast!=selfSubId) or (selfDocIdPast!=selfDocId) or (selfAreaIdPast!=selfAreaId)):
#             selfMedNameStr=selfMedNameStr+'<'+str(selfSubId) +'.'+str(selfDocId) +'.'+ str(selfAreaId)+'>'
            selfMedNameStr=selfMedNameStr+'<'+str(selfSubId) +'.'+ str(selfAreaId)+'>'
            flaStart=0
        if flaStart==0:
            selfMedNameStr=selfMedNameStr+str(selfMedName)
        else:
            selfMedNameStr=selfMedNameStr+','+str(selfMedName)
        selfSubIdPast=selfSubId
        selfDocIdPast=selfDocId
        selfAreaIdPast=selfAreaId
    selfMedNameStr=selfMedNameStr+'<'
    
    
#     =======================product Count=======
       
    records_selfPNS="SELECT  distinct(sm_prescription_details.medicine_id),count(sm_prescription_details.medicine_id) as medicine_idCount,sm_prescription_details.medicine_name, sm_prescription_details.submit_by_id as submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.submit_by_id,sm_prescription_details.area_id,sm_prescription_details.medicine_id order by sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id,sm_prescription_details.medicine_id;"
#     return records_selfPNS
    records_selfPN=db.executesql(records_selfPNS,as_dict = True) 
    selfProductList=[]
    selfProductDict={}
    selfSubIdPast=''
    selfDocIdPast=''
    selfAreaIdPast=''
    selfMedNameStr=''
    medName=''
    for records_selfPN in records_selfPN:
        flaStart=1
        selfSubId=records_selfPN['submit_by_id']
        selfDocId=records_selfPN['doctor_id']
        selfAreaId=records_selfPN['area_id']
        selfMedName=records_selfPN['medicine_name']
        medCount=records_selfPN['medicine_idCount']
        if ((selfSubIdPast!=selfSubId)  or (selfAreaIdPast!=selfAreaId)):
#             selfMedNameStr=selfMedNam00tr+'<'+str(selfSubId) +'.'+str(selfDocId) +'.'+ str(selfAreaId)+'>'
            selfMedNameStr=selfMedNameStr+'<'+str(selfSubId) +'.'+ str(selfAreaId)+'>'
            flaStart=0
        if flaStart==0:
            selfMedNameStr=selfMedNameStr+str(selfMedName)+'['+str(medCount)+']'
        else:
            selfMedNameStr=selfMedNameStr+','+str(selfMedName)+'['+str(medCount)+']'
        selfSubIdPast=selfSubId
        selfDocIdPast=selfDocId
        selfAreaIdPast=selfAreaId
    selfMedNameStr=selfMedNameStr+'<'        
  

    
    return dict(records=records,date_from=date_from,date_to=date_to_get,mpoNameList=mpoNameList, mpoIdList=mpoIdList,selfCountCheckList=selfCountCheckList,selfCountList=selfCountList,selfPrCountList=selfPrCountList,selfPrCountCheckList=selfPrCountCheckList, levelIDList=levelIDList,selfMedNameStr=selfMedNameStr)



def prSummaryD():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

   

    c_id = session.cid
    response.title='Prescription Summary'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    depot_id=str(request.vars.depot_id).strip()
    depot_name=str(request.vars.depot_name).strip()    
    
    rsm_id=str(request.vars.rsm_id).strip()
    rsm_name=str(request.vars.rsm_name).strip()
    fm_id=str(request.vars.fm_id).strip()
    fm_name=str(request.vars.fm_name).strip()
    tr_id=str(request.vars.tr_id).strip()
    tr_name=str(request.vars.tr_name).strip()
    product_id=str(request.vars.product_id).strip()
    product_name=str(request.vars.product_name).strip()
    brand=str(request.vars.brand).strip()
    category=str(request.vars.category).strip()
    mso_id=str(request.vars.mso_id).strip()
    mso_name=str(request.vars.mso_name).strip()
    doc=str(request.vars.doc).strip()
    doc_name=str(request.vars.doc_name).strip()
#     return mso_id
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 
    
#     return len(mso_id)
    if ((len(rsm_id)<1) and (fm_id<1) and (tr_id<1) and (doc<1) and (product_id<1) and (mso_id<1)):
        session.flash = 'Please select RSM or FM or TR or product or submitted by'
        redirect (URL(c='dcr_report', f='index'))
   
    
#     return date_from
    qset=db()
    qset = qset(db.sm_prescription_head.cid == c_id)
    qset = qset(db.sm_prescription_head.submit_date >= date_from)
    qset = qset(db.sm_prescription_head.submit_date <= date_to)
#     qset = qset(db.sm_prescription_details.cid == c_id)
#     qset = qset(db.sm_prescription_details.sl == db.sm_prescription_head.sl)

    if (rsm_id!=''):
        qset = qset(db.sm_prescription_head.reg_id == reg_id)
    if (fm_id!=''):
        qset = qset(db.sm_prescription_head.tl_id == fm_id)
    if (tr_id!=''):
        qset = qset(db.sm_prescription_head.area_id == tr_id)
    if (doc!=''):
        qset = qset(db.sm_prescription_head.doctor_id == doc)
    if (product_id!=''):
        qset = qset(db.sm_prescription_details.medicine_id == product_id)
    if (len(mso_id)>3):
        qset = qset(db.sm_prescription_head.submit_by_id == mso_id)
    
    
    records = qset.select(db.sm_prescription_head.reg_id,db.sm_prescription_head.reg_name,db.sm_prescription_head.tl_id,db.sm_prescription_head.tl_name,db.sm_prescription_head.area_id,db.sm_prescription_head.area_name,db.sm_prescription_head.submit_by_id,db.sm_prescription_head.submit_by_name,db.sm_prescription_head.sl.count(), orderby=db.sm_prescription_head.sl,groupby= db.sm_prescription_head.submit_by_id)
    
    # Self==============================  
    qset_self=db()
    qset_self = qset_self(db.sm_prescription_head.cid == c_id)
    qset_self = qset_self(db.sm_prescription_head.submit_date >= date_from)
    qset_self = qset_self(db.sm_prescription_head.submit_date < date_to)
    qset_self = qset_self(db.sm_prescription_details.cid == c_id)
    qset_self = qset_self(db.sm_prescription_details.sl == db.sm_prescription_head.sl)
    qset_self = qset_self(db.sm_prescription_details.med_type == 'SELF')
   
    if (rsm_id!=''):
        qset_self = qset_self(db.sm_prescription_head.reg_id == rsm_id)
    if (fm_id!=''):
        qset_self = qset_self(db.sm_prescription_head.tl_id == fm_id)
    if (tr_id!=''):
        qset_self = qset_self(db.sm_prescription_head.area_id == tr_id)
    if (doc!=''):
        qset_self = qset_self(db.sm_prescription_head.doctor_id == doc)
#     if (product_id!=''):
#         qset = qset(db.sm_prescription_details.medicine_id == product_id)
    if (len(mso_id)>3):
        qset_self = qset_self(db.sm_prescription_head.submit_by_id == mso_id)
       
    records_self = qset_self.select(db.sm_prescription_head.submit_by_id,db.sm_prescription_details.sl.count(), orderby=db.sm_prescription_details.sl,groupby= db.sm_prescription_head.submit_by_id)
    selfSbmittedByCountList=[]
    selfSbmittedByList=[]
    for records_self in records_self:
        selfSubId=records_self[db.sm_prescription_head.submit_by_id]
        selfSubCount=records_self[db.sm_prescription_details.sl.count()]
        selfSbmittedByList.append(selfSubId)
        selfSbmittedByCountList.append(selfSubCount)
        
        
        
    
    
    
# OTHER==============================  
    qset_other=db()
    qset_other = qset_other(db.sm_prescription_head.cid == c_id)
    qset_other = qset_other(db.sm_prescription_head.submit_date >= date_from)
    qset_other = qset_other(db.sm_prescription_head.submit_date < date_to)
    qset_other = qset_other(db.sm_prescription_details.cid == c_id)
    qset_other = qset_other(db.sm_prescription_details.sl == db.sm_prescription_head.sl)
    qset_other = qset_other(db.sm_prescription_details.med_type == 'OTHER')
   
    if (rsm_id!=''):
        qset_other = qset_other(db.sm_prescription_head.reg_id == rsm_id)
    if (fm_id!=''):
        qset_other = qset_other(db.sm_prescription_head.tl_id == fm_id)
    if (tr_id!=''):
        qset_other = qset_other(db.sm_prescription_head.area_id == tr_id)
    if (doc!=''):
        qset_other = qset_other(db.sm_prescription_head.doctor_id == doc)
#     if (product_id!=''):
#         qset = qset(db.sm_prescription_details.medicine_id == product_id)
    if (len(mso_id)>3):
        qset_other = qset_other(db.sm_prescription_head.submit_by_id == mso_id)
       
    records_other = qset_other.select(db.sm_prescription_head.submit_by_id,db.sm_prescription_details.sl.count(), orderby=db.sm_prescription_details.sl,groupby= db.sm_prescription_head.submit_by_id)
    otherSbmittedByCountList=[]
    otherSbmittedByList=[]
    for records_other in records_other:
        otherSubId=records_other[db.sm_prescription_head.submit_by_id]
        otherSubCount=records_other[db.sm_prescription_details.sl.count()]
        otherSbmittedByList.append(otherSubId)
        otherSbmittedByCountList.append(otherSubCount)
 
# Unknown==============================  
    qset_unknown=db()
    qset_unknown = qset_unknown(db.sm_prescription_head.cid == c_id)
    qset_unknown = qset_unknown(db.sm_prescription_head.submit_date >= date_from)
    qset_unknown = qset_unknown(db.sm_prescription_head.submit_date < date_to)
    qset_unknown = qset_unknown(db.sm_prescription_details.cid == c_id)
    qset_unknown = qset_unknown(db.sm_prescription_details.sl == db.sm_prescription_head.sl)
    qset_unknown = qset_unknown(db.sm_prescription_details.medicine_id == '')
   
    if (rsm_id!=''):
        qset_unknown = qset_unknown(db.sm_prescription_head.reg_id == rsm_id)
    if (fm_id!=''):
        qset_unknown = qset_unknown(db.sm_prescription_head.tl_id == fm_id)
    if (tr_id!=''):
        qset_unknown = qset_unknown(db.sm_prescription_head.area_id == tr_id)
    if (doc!=''):
        qset_unknown = qset_unknown(db.sm_prescription_head.doctor_id == doc)
#     if (product_id!=''):
#         qset = qset(db.sm_prescription_details.medicine_id == product_id)
    if (len(mso_id)>3):
        qset_unknown = qset_unknown(db.sm_prescription_head.submit_by_id == mso_id)
       
    records_unknown = qset_unknown.select(db.sm_prescription_head.submit_by_id,db.sm_prescription_details.sl.count(), orderby=db.sm_prescription_details.sl,groupby= db.sm_prescription_head.submit_by_id)
    unknownSbmittedByCountList=[]
    unknownSbmittedByList=[]
    for records_unknown in records_unknown:
        unknownSubId=records_unknown[db.sm_prescription_head.submit_by_id]
        unknownSubCount=records_unknown[db.sm_prescription_details.sl.count()]
        unknownSbmittedByList.append(unknownSubId)
        unknownSbmittedByCountList.append(unknownSubCount)
    
    
    myString='DateRange,'+date_from+','+date_to+'\n'
#     myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
    myString+='FM,'+fm_id+'|'+fm_name+'\n'
    myString+='RT,'+tr_id+'|'+tr_name+'\n'
    myString+='MSO,'+mso_id+'|'+mso_name+'\n'
    myString+='Product,'+product_id+'|'+product_name+'\n'
#     myString+='Category,'+category+'\n'
    myString+='Doctor,'+doc+'|'+doc_name+'\n\n'
    myString+='RSM  ,  FM  ,  TR  ,  Submitted by ID  ,  Submitted by Name ,   Prescriptiom Count,OwnBrand,OtherBrand,Others\n'
    for record in records:
        selfCount=0
        otherCount=0
        unknownCount=0
        submit_by_id=record[db.sm_prescription_head.submit_by_id]
        if [s for s in selfSbmittedByList if submit_by_id in s]:
            index_element = selfSbmittedByList.index(submit_by_id)   
            selfCount=selfSbmittedByCountList[index_element]
        if [s for s in otherSbmittedByList if submit_by_id in s]:
            index_element = otherSbmittedByList.index(submit_by_id) 
            otherCount=otherSbmittedByCountList[index_element]
        if [s for s in unknownSbmittedByList if submit_by_id in s]:
            index_element = unknownSbmittedByList.index(submit_by_id)
            unknownCount=unknownSbmittedByCountList[index_element]
        myString+=str(record[db.sm_prescription_head.reg_id])+','+str(record[db.sm_prescription_head.tl_id])+','+str(record[db.sm_prescription_head.area_id])+','+str(record[db.sm_prescription_head.submit_by_id])+','+str(record[db.sm_prescription_head.sl.count()])+','+str(selfCount)+','+str(otherCount)+','+str(unknownCount)+'\n'
         
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=Prescription_Summary.csv'   
    return str(myString)


#===Faisal========Pr Summary===============

def prNewRSMSummary():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))
    

    c_id = session.cid
    response.title='RSM Wise Prescription Summary'    
    date_from=request.vars.date_from
    date_to_get=request.vars.date_to
  
    
    date_to_2=datetime.datetime.strptime(str(date_to_get),'%Y-%m-%d')
    date_to_1=date_to_2 + datetime.timedelta(days = 1) 
       
    date_to=str(date_to_1)[0:10]
    
    rsm_id=str(request.vars.rsm_id).strip()
    
   
#    condition=''
#    
#    if (rsm_id!=''):
#        condition=condition+" AND depot_id = '"+str(depot_id)+"'"
#    
#    if (rsm_id!=''):
#        qset = qset(db.sm_prescription_head.tl_id == rsm_id)
        
#     if (fm_id!=''):
#         qset = qset(db.sm_prescription_head.tl_id == rsm_id)    
#    if (mso_id!=''):
#        qset = qset(db.sm_prescription_head.submit_by_id == mso_id)
        
    
    rsmSql="SELECT b.area_id as areaID,a.sup_id as rsmID, a.sup_name as rsmName,b.sl as presSl,0 as selfPresCount,0 as selfMedCount  FROM sm_supervisor_level a, sm_prescription_details b  WHERE a.cid = '"+ c_id +"' and submit_date>='"+date_from+"' and submit_date<='"+date_to_get+"'  and a.sup_id=b.tl_id and a.level_depth_no=1"
    selfMedSql="SELECT b.area_id as areaID,sup_id as rsmID,sup_name as rsmName,b.sl as presSl,b.sl as selfPresCount,b.medicine_id as selfMedCount FROM sm_supervisor_level a, sm_prescription_details b  WHERE a.cid = '"+ c_id +"' and submit_date>='"+date_from+"' and submit_date<='"+date_to_get+"' and med_type='Self'  and a.sup_id=b.tl_id and a.level_depth_no=1"
    
    records="select areaID,rsmID,rsmName,count(distinct(presSl)) as presCount,count(distinct(selfPresCount))-1 as selfPresCount,count(distinct(selfMedCount))-1 as selfMedCount  from ("+rsmSql+" union all "+selfMedSql+") p group by areaID,rsmID order by areaID,rsmID;"
    
    records=db.executesql(records,as_dict = True) 
    
    return dict(records=records,date_from=date_from,date_to=date_to_get)
    
#    records = qset.select(db.sm_prescription_head.reg_id,db.sm_prescription_head.reg_name,db.sm_prescription_head.tl_id,db.sm_prescription_head.tl_name,db.sm_prescription_head.area_id,db.sm_prescription_head.area_name,db.sm_prescription_head.submit_by_id,db.sm_prescription_head.submit_by_name,db.sm_prescription_head.sl.count(),db.sm_prescription_head.doctor_id,db.sm_prescription_head.doctor_name, orderby=db.sm_prescription_head.tl_id,groupby= db.sm_prescription_head.tl_id)
#    
#    #return db._lastsql
## ==============MPO List
#    mpoNameList=[]
#    mpoIdList=[]
#    levelIDList=[]
#    records_mpoS="SELECT sup_id, sup_name, level_id FROM sm_supervisor_level WHERE cid = '"+ c_id +"'  and level_depth_no=1 group by sup_name order by sup_id;"
##    return records_mpoS
#    records_mpo=db.executesql(records_mpoS,as_dict = True) 
#    for records_mpo in records_mpo:
#        levelID=records_mpo['level_id']
#        mpoID=records_mpo['sup_id']
#        mpoName=records_mpo['sup_name']
#        mpoNameList.append(mpoName)
#        mpoIdList.append(mpoID)
#        levelIDList.append(levelID)
#
#        
## selfprescriptionCount==============================  
#       
#    records_selfPS="SELECT  count(distinct(sm_prescription_details.sl)) as medCount,sm_prescription_details.sl, sm_prescription_details.submit_by_id as submit_by_id,sm_prescription_details.doctor_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.tl_id order by sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id;"
#    
##     return records_selfPS
#    records_selfP=db.executesql(records_selfPS,as_dict = True) 
#    selfCountList=[]
#    selfCountCheckList=[]
#
#    for records_selfP in records_selfP:
#        selfSubId=records_selfP['submit_by_id']
#        selfDocId=records_selfP['doctor_id']
##         selfAreaId=records_selfP['area_id']
#        selfMedCount=records_selfP['medCount']
##         pCheck=selfSubId+'.'+selfDocId+'.'+selfAreaId
#        pCheck=selfSubId#+'.'+selfAreaId
#        selfCountCheckList.append(pCheck)
#        selfCountList.append(selfMedCount)
#        
## selfproductCount==============================  
#       
##     records_selfPrS="SELECT  count(distinct(sm_prescription_details.medicine_id)) as medCount,sm_prescription_details.sl, sm_prescription_head.submit_by_id as submit_by_id,sm_prescription_head.doctor_id,sm_prescription_head.area_id FROM sm_prescription_head,sm_prescription_details WHERE sm_prescription_head.cid = '"+ c_id +"' and sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_head.submit_date >= '"+ date_from +"' and sm_prescription_head.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' and sm_prescription_head.sl =sm_prescription_details.sl GROUP BY  sm_prescription_head.submit_by_id,sm_prescription_head.doctor_id,sm_prescription_head.area_id order by sm_prescription_head.submit_by_id,sm_prescription_head.doctor_id,sm_prescription_head.area_id;"
#    records_selfPrS="SELECT  count(sm_prescription_details.medicine_id) as medCount,sm_prescription_details.sl, sm_prescription_details.submit_by_id as submit_by_id,sm_prescription_details.doctor_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.tl_id order by sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id;"
##     return records_selfPrS
#    records_selfPr=db.executesql(records_selfPrS,as_dict = True) 
#    selfPrCountList=[]
#    selfPrCountCheckList=[]
# 
#    for records_selfPr in records_selfPr:
#        selfPrSubId=records_selfPr['submit_by_id']
#        selfPrDocId=records_selfPr['doctor_id']
##         selfPrAreaId=records_selfPr['area_id']
#        selfPrMedCount=records_selfPr['medCount']
##         prCheck=selfPrSubId+'.'+selfPrDocId+'.'+selfPrAreaId
#        prCheck=selfPrSubId#+'.'+selfPrAreaId
#        
#        selfPrCountList.append(selfPrMedCount)  
#        selfPrCountCheckList.append(prCheck)   
#        
#        
## selfproductUnique==============================  
#       
#    records_selfPNS="SELECT  distinct(sm_prescription_details.medicine_id) as medicine_id,sm_prescription_details.medicine_name, sm_prescription_details.tl_id as submit_by_id,sm_prescription_details.doctor_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.tl_id,sm_prescription_details.medicine_id order by sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.medicine_id;"
##     return records_selfPNS
#    records_selfPN=db.executesql(records_selfPNS,as_dict = True) 
#    selfProductList=[]
#    selfProductDict={}
#    selfSubIdPast=''
#    selfDocIdPast=''
#    selfAreaIdPast=''
#    selfMedNameStr=''
#    medName=''
#    for records_selfPN in records_selfPN:
#        flaStart=1
#        selfSubId=records_selfPN['submit_by_id']
#        selfDocId=records_selfPN['doctor_id']
##         selfAreaId=records_selfPN['area_id']
#        selfMedName=records_selfPN['medicine_name']
#        if ((selfSubIdPast!=selfSubId) or (selfDocIdPast!=selfDocId) ):
##             selfMedNameStr=selfMedNameStr+'<'+str(selfSubId) +'.'+str(selfDocId) +'.'+ str(selfAreaId)+'>'
#            selfMedNameStr=selfMedNameStr+'<'+str(selfSubId) +'>'
#            flaStart=0
#        if flaStart==0:
#            selfMedNameStr=selfMedNameStr+str(selfMedName)
#        else:
#            selfMedNameStr=selfMedNameStr+','+str(selfMedName)
#        selfSubIdPast=selfSubId
#        selfDocIdPast=selfDocId
##         selfAreaIdPast=selfAreaId
#    selfMedNameStr=selfMedNameStr+'<'
#    
#    
##     =======================product Count=======
#       
#    records_selfPNS="SELECT  distinct(sm_prescription_details.medicine_id),count(sm_prescription_details.medicine_id) as medicine_idCount,sm_prescription_details.medicine_name, sm_prescription_details.tl_id as submit_by_id,sm_prescription_details.doctor_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.tl_id,sm_prescription_details.medicine_id order by sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.medicine_id;"
##     return records_selfPNS
#    records_selfPN=db.executesql(records_selfPNS,as_dict = True) 
#    selfProductList=[]
#    selfProductDict={}
#    selfSubIdPast=''
#    selfDocIdPast=''
#    selfAreaIdPast=''
#    selfMedNameStr=''
#    medName=''
#    for records_selfPN in records_selfPN:
#        flaStart=1
#        selfSubId=records_selfPN['submit_by_id']
#        selfDocId=records_selfPN['doctor_id']
##         selfAreaId=records_selfPN['area_id']
#        selfMedName=records_selfPN['medicine_name']
#        medCount=records_selfPN['medicine_idCount']
#        if (selfSubIdPast!=selfSubId):
##             selfMedNameStr=selfMedNam00tr+'<'+str(selfSubId) +'.'+str(selfDocId) +'.'+ str(selfAreaId)+'>'
#            selfMedNameStr=selfMedNameStr+'<'+str(selfSubId) +'>'
#            flaStart=0
#        if flaStart==0:
#            selfMedNameStr=selfMedNameStr+str(selfMedName)+'['+str(medCount)+']'
#        else:
#            selfMedNameStr=selfMedNameStr+','+str(selfMedName)+'['+str(medCount)+']'
#        selfSubIdPast=selfSubId
#        selfDocIdPast=selfDocId
##         selfAreaIdPast=selfAreaId
#    selfMedNameStr=selfMedNameStr+'<'        
#  
#
#    
#    return dict(records=records,date_from=date_from,date_to=date_to_get,mpoNameList=mpoNameList, mpoIdList=mpoIdList,selfCountCheckList=selfCountCheckList,selfCountList=selfCountList,selfPrCountList=selfPrCountList,selfPrCountCheckList=selfPrCountCheckList, levelIDList=levelIDList,selfMedNameStr=selfMedNameStr)



def prNewSummary():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))
    

    c_id = session.cid
    response.title='MSO Wise Prescription Summary'    
    date_from=request.vars.date_from
    date_to_get=request.vars.date_to
  
    
    date_to_2=datetime.datetime.strptime(str(date_to_get),'%Y-%m-%d')
    date_to_1=date_to_2 + datetime.timedelta(days = 1) 
       
    date_to=str(date_to_1)[0:10]
    
#     rsm_id=str(request.vars.rsm_id).strip()
#     fm_id=str(request.vars.fm_id).strip()
    mso_id=str(request.vars.mso_id).strip()
    
   
#     updateTableStr="update sm_prescription_head a, sm_prescription_details d set d.submit_date =a.submit_date,d.first_date=a.first_date,d.submit_by_id=a.submit_by_id,d.submit_by_name=a.submit_by_name,d.user_type=a.user_type,d.doctor_id=a.doctor_id,d.doctor_name=a.doctor_name,d.image_name=a.image_name,d.image_path=a.image_path,d.lat_long=a.lat_long,d.area_id=a.area_id,d.area_name=a.area_name,d.tl_id=a.tl_id,d.tl_name=a.tl_name,d.reg_id=a.reg_id,d.reg_name=a.reg_name where d.submit_by_id='' and a.cid=d.cid and a.sl=d.sl;"
#     updateTable=db.executesql(updateTableStr) 
    
   
    qset=db()
    qset = qset(db.sm_prescription_head.cid == c_id)
    qset = qset(db.sm_prescription_head.submit_date >= date_from)
    qset = qset(db.sm_prescription_head.submit_date < date_to)
    
#     if (rsm_id!=''):
#         qset = qset(db.sm_prescription_head.tl_id == rsm_id)
#     if (fm_id!=''):
#         qset = qset(db.sm_prescription_head.tl_id == rsm_id)    
    if (mso_id!=''):
        qset = qset(db.sm_prescription_head.submit_by_id == mso_id)
        
    records = qset.select(db.sm_prescription_head.reg_id,db.sm_prescription_head.reg_name,db.sm_prescription_head.tl_id,db.sm_prescription_head.tl_name,db.sm_prescription_head.area_id,db.sm_prescription_head.area_name,db.sm_prescription_head.submit_by_id,db.sm_prescription_head.submit_by_name,db.sm_prescription_head.sl.count(),db.sm_prescription_head.doctor_id,db.sm_prescription_head.doctor_name, orderby=db.sm_prescription_head.submit_by_id,groupby= db.sm_prescription_head.submit_by_id)
    
#     return db._lastsql
# ==============MPO List
    mpoNameList=[]
    mpoIdList=[]
    levelIDList=[]
    records_mpoS="SELECT sup_id, sup_name, level_id FROM sm_supervisor_level WHERE cid = '"+ c_id +"'  and level_depth_no=1 group by sup_name order by sup_id;"
#     return records_mpoS
    records_mpo=db.executesql(records_mpoS,as_dict = True) 
    for records_mpo in records_mpo:
        levelID=records_mpo['level_id']
        mpoID=records_mpo['sup_id']
        mpoName=records_mpo['sup_name']
        mpoNameList.append(mpoName)
        mpoIdList.append(mpoID)
        levelIDList.append(levelID)

        
# selfprescriptionCount==============================  
       
    records_selfPS="SELECT  count(distinct(sm_prescription_details.sl)) as medCount,sm_prescription_details.sl, sm_prescription_details.submit_by_id as submit_by_id,sm_prescription_details.doctor_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.submit_by_id order by sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id;"
    
#     return records_selfPS
    records_selfP=db.executesql(records_selfPS,as_dict = True) 
    selfCountList=[]
    selfCountCheckList=[]

    for records_selfP in records_selfP:
        selfSubId=records_selfP['submit_by_id']
        selfDocId=records_selfP['doctor_id']
#         selfAreaId=records_selfP['area_id']
        selfMedCount=records_selfP['medCount']
#         pCheck=selfSubId+'.'+selfDocId+'.'+selfAreaId
        pCheck=selfSubId#+'.'+selfAreaId
        selfCountCheckList.append(pCheck)
        selfCountList.append(selfMedCount)
        
# selfproductCount==============================  
       
#     records_selfPrS="SELECT  count(distinct(sm_prescription_details.medicine_id)) as medCount,sm_prescription_details.sl, sm_prescription_head.submit_by_id as submit_by_id,sm_prescription_head.doctor_id,sm_prescription_head.area_id FROM sm_prescription_head,sm_prescription_details WHERE sm_prescription_head.cid = '"+ c_id +"' and sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_head.submit_date >= '"+ date_from +"' and sm_prescription_head.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' and sm_prescription_head.sl =sm_prescription_details.sl GROUP BY  sm_prescription_head.submit_by_id,sm_prescription_head.doctor_id,sm_prescription_head.area_id order by sm_prescription_head.submit_by_id,sm_prescription_head.doctor_id,sm_prescription_head.area_id;"
    records_selfPrS="SELECT  count(sm_prescription_details.medicine_id) as medCount,sm_prescription_details.sl, sm_prescription_details.submit_by_id as submit_by_id,sm_prescription_details.doctor_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.submit_by_id order by sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id;"
#     return records_selfPrS
    records_selfPr=db.executesql(records_selfPrS,as_dict = True) 
    selfPrCountList=[]
    selfPrCountCheckList=[]
 
    for records_selfPr in records_selfPr:
        selfPrSubId=records_selfPr['submit_by_id']
        selfPrDocId=records_selfPr['doctor_id']
#         selfPrAreaId=records_selfPr['area_id']
        selfPrMedCount=records_selfPr['medCount']
#         prCheck=selfPrSubId+'.'+selfPrDocId+'.'+selfPrAreaId
        prCheck=selfPrSubId#+'.'+selfPrAreaId
        
        selfPrCountList.append(selfPrMedCount)  
        selfPrCountCheckList.append(prCheck)   
        
        
# selfproductUnique==============================  
       
    records_selfPNS="SELECT  distinct(sm_prescription_details.medicine_id) as medicine_id,sm_prescription_details.medicine_name, sm_prescription_details.submit_by_id as submit_by_id,sm_prescription_details.doctor_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.submit_by_id,sm_prescription_details.medicine_id order by sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.medicine_id;"
#     return records_selfPNS
    records_selfPN=db.executesql(records_selfPNS,as_dict = True) 
    selfProductList=[]
    selfProductDict={}
    selfSubIdPast=''
    selfDocIdPast=''
    selfAreaIdPast=''
    selfMedNameStr=''
    medName=''
    for records_selfPN in records_selfPN:
        flaStart=1
        selfSubId=records_selfPN['submit_by_id']
        selfDocId=records_selfPN['doctor_id']
#         selfAreaId=records_selfPN['area_id']
        selfMedName=records_selfPN['medicine_name']
        if ((selfSubIdPast!=selfSubId) or (selfDocIdPast!=selfDocId) ):
#             selfMedNameStr=selfMedNameStr+'<'+str(selfSubId) +'.'+str(selfDocId) +'.'+ str(selfAreaId)+'>'
            selfMedNameStr=selfMedNameStr+'<'+str(selfSubId) +'>'
            flaStart=0
        if flaStart==0:
            selfMedNameStr=selfMedNameStr+str(selfMedName)
        else:
            selfMedNameStr=selfMedNameStr+','+str(selfMedName)
        selfSubIdPast=selfSubId
        selfDocIdPast=selfDocId
#         selfAreaIdPast=selfAreaId
    selfMedNameStr=selfMedNameStr+'<'
    
    
#     =======================product Count=======
       
    records_selfPNS="SELECT  distinct(sm_prescription_details.medicine_id),count(sm_prescription_details.medicine_id) as medicine_idCount,sm_prescription_details.medicine_name, sm_prescription_details.submit_by_id as submit_by_id,sm_prescription_details.doctor_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.submit_by_id,sm_prescription_details.medicine_id order by sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.medicine_id;"
#     return records_selfPNS
    records_selfPN=db.executesql(records_selfPNS,as_dict = True) 
    selfProductList=[]
    selfProductDict={}
    selfSubIdPast=''
    selfDocIdPast=''
    selfAreaIdPast=''
    selfMedNameStr=''
    medName=''
    for records_selfPN in records_selfPN:
        flaStart=1
        selfSubId=records_selfPN['submit_by_id']
        selfDocId=records_selfPN['doctor_id']
#         selfAreaId=records_selfPN['area_id']
        selfMedName=records_selfPN['medicine_name']
        medCount=records_selfPN['medicine_idCount']
        if (selfSubIdPast!=selfSubId):
#             selfMedNameStr=selfMedNam00tr+'<'+str(selfSubId) +'.'+str(selfDocId) +'.'+ str(selfAreaId)+'>'
            selfMedNameStr=selfMedNameStr+'<'+str(selfSubId) +'>'
            flaStart=0
        if flaStart==0:
            selfMedNameStr=selfMedNameStr+str(selfMedName)+'['+str(medCount)+']'
        else:
            selfMedNameStr=selfMedNameStr+','+str(selfMedName)+'['+str(medCount)+']'
        selfSubIdPast=selfSubId
        selfDocIdPast=selfDocId
#         selfAreaIdPast=selfAreaId
    selfMedNameStr=selfMedNameStr+'<'        
  

    
    return dict(records=records,date_from=date_from,date_to=date_to_get,mpoNameList=mpoNameList, mpoIdList=mpoIdList,selfCountCheckList=selfCountCheckList,selfCountList=selfCountList,selfPrCountList=selfPrCountList,selfPrCountCheckList=selfPrCountCheckList, levelIDList=levelIDList,selfMedNameStr=selfMedNameStr)


def drSummary():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))
    

    c_id = session.cid
    response.title='Doctor Wise Prescription Summary'    
    date_from=request.vars.date_from
    date_to_get=request.vars.date_to
  
    
    date_to_2=datetime.datetime.strptime(str(date_to_get),'%Y-%m-%d')
    date_to_1=date_to_2 + datetime.timedelta(days = 1) 
       
    date_to=str(date_to_1)[0:10]
    
    doc=str(request.vars.doc).strip()
   

    qset=db()
    qset = qset(db.sm_prescription_details.cid == c_id)
    qset = qset(db.sm_prescription_details.submit_date >= date_from)
    qset = qset(db.sm_prescription_details.submit_date < date_to)
    
    if doc!='':
        qset = qset(db.sm_prescription_details.doctor_id == doc)        

    records = qset.select(db.sm_prescription_details.reg_id,db.sm_prescription_details.reg_name,db.sm_prescription_details.tl_id,db.sm_prescription_details.tl_name,db.sm_prescription_details.area_id,db.sm_prescription_details.area_name,db.sm_prescription_details.submit_by_id,db.sm_prescription_details.submit_by_name,db.sm_prescription_details.sl.count(),db.sm_prescription_details.doctor_id,db.sm_prescription_details.doctor_id.count(),db.sm_prescription_details.doctor_name,db.sm_prescription_details.zero_doc_count.sum(), orderby=db.sm_prescription_details.submit_by_id,groupby= db.sm_prescription_details.submit_by_id|db.sm_prescription_details.doctor_id)
    
      
    
#     return db._lastsql
# ==============MPO List
    mpoNameList=[]
    mpoIdList=[]
    levelIDList=[]
    records_mpoS="SELECT  sup_id, sup_name, level_id FROM sm_supervisor_level WHERE cid = '"+ c_id +"'  and level_depth_no=1 GROUP BY  level_id order by level_id;"
#     return records_mpoS
    records_mpo=db.executesql(records_mpoS,as_dict = True) 
    for records_mpo in records_mpo:
        levelID=records_mpo['level_id']
        mpoID=records_mpo['sup_id']
        mpoName=records_mpo['sup_name']
        mpoNameList.append(mpoName)
        mpoIdList.append(mpoID)
        levelIDList.append(levelID)

        
# selfprescriptionCount==============================  
       
    records_selfPS="SELECT  count(distinct(sm_prescription_details.sl)) as medCount,sm_prescription_details.sl, sm_prescription_details.submit_by_id as submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id order by sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id;"
    
#     return records_selfPS
    records_selfP=db.executesql(records_selfPS,as_dict = True) 
    selfCountList=[]
    selfCountCheckList=[]

    for records_selfP in records_selfP:
        selfSubId=records_selfP['submit_by_id']
        selfDocId=records_selfP['doctor_id']
        selfAreaId=records_selfP['area_id']
        selfMedCount=records_selfP['medCount']
        pCheck=selfSubId+'.'+selfDocId+'.'+selfAreaId
        selfCountCheckList.append(pCheck)
        selfCountList.append(selfMedCount)
 
# selfproductCount==============================  
       
#     records_selfPrS="SELECT  count(distinct(sm_prescription_details.medicine_id)) as medCount,sm_prescription_details.sl, sm_prescription_head.submit_by_id as submit_by_id,sm_prescription_head.doctor_id,sm_prescription_head.area_id FROM sm_prescription_head,sm_prescription_details WHERE sm_prescription_head.cid = '"+ c_id +"' and sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_head.submit_date >= '"+ date_from +"' and sm_prescription_head.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' and sm_prescription_head.sl =sm_prescription_details.sl GROUP BY  sm_prescription_head.submit_by_id,sm_prescription_head.doctor_id,sm_prescription_head.area_id order by sm_prescription_head.submit_by_id,sm_prescription_head.doctor_id,sm_prescription_head.area_id;"
    records_selfPrS="SELECT  count(sm_prescription_details.medicine_id) as medCount,sm_prescription_details.sl, sm_prescription_details.submit_by_id as submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id order by sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id;"
#     return records_selfPrS
    records_selfPr=db.executesql(records_selfPrS,as_dict = True) 
    selfPrCountList=[]
    selfPrCountCheckList=[]
 
    for records_selfPr in records_selfPr:
        selfPrSubId=records_selfPr['submit_by_id']
        selfPrDocId=records_selfPr['doctor_id']
        selfPrAreaId=records_selfPr['area_id']
        selfPrMedCount=records_selfPr['medCount']
        prCheck=selfPrSubId+'.'+selfPrDocId+'.'+selfPrAreaId
        
        selfPrCountList.append(selfPrMedCount)  
        selfPrCountCheckList.append(prCheck)       
# selfproductUnique==============================  
       
    records_selfPNS="SELECT  distinct(sm_prescription_details.medicine_id) as medicine_id,sm_prescription_details.medicine_name, sm_prescription_details.submit_by_id as submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.medicine_id order by sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.medicine_id;"
#     return records_selfPNS
    records_selfPN=db.executesql(records_selfPNS,as_dict = True) 
    selfProductList=[]
    selfProductDict={}
    selfSubIdPast=''
    selfDocIdPast=''
    selfAreaIdPast=''
    selfMedNameStr=''
    medName=''
    for records_selfPN in records_selfPN:
        flaStart=1
        selfSubId=records_selfPN['submit_by_id']
        selfDocId=records_selfPN['doctor_id']
        selfAreaId=records_selfPN['area_id']
        selfMedName=records_selfPN['medicine_name']
        if ((selfSubIdPast!=selfSubId) or (selfDocIdPast!=selfDocId) or (selfAreaIdPast!=selfAreaId)):
            selfMedNameStr=selfMedNameStr+'<'+str(selfSubId) +'.'+str(selfDocId) +'.'+ str(selfAreaId)+'>'
            flaStart=0
        if flaStart==0:
            selfMedNameStr=selfMedNameStr+str(selfMedName)
        else:
            selfMedNameStr=selfMedNameStr+','+str(selfMedName)
        selfSubIdPast=selfSubId
        selfDocIdPast=selfDocId
        selfAreaIdPast=selfAreaId
    selfMedNameStr=selfMedNameStr+'<'
    
    
#     =======================product Count=======
       
    records_selfPNS="SELECT  distinct(sm_prescription_details.medicine_id),count(sm_prescription_details.medicine_id) as medicine_idCount,sm_prescription_details.medicine_name, sm_prescription_details.submit_by_id as submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.medicine_id order by sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.medicine_id;"
#     return records_selfPNS
    records_selfPN=db.executesql(records_selfPNS,as_dict = True) 
    selfProductList=[]
    selfProductDict={}
    selfSubIdPast=''
    selfDocIdPast=''
    selfAreaIdPast=''
    selfMedNameStr=''
    medName=''
    for records_selfPN in records_selfPN:
        flaStart=1
        selfSubId=records_selfPN['submit_by_id']
        selfDocId=records_selfPN['doctor_id']
        selfAreaId=records_selfPN['area_id']
        selfMedName=records_selfPN['medicine_name']
        medCount=records_selfPN['medicine_idCount']
        if ((selfSubIdPast!=selfSubId) or (selfDocIdPast!=selfDocId) or (selfAreaIdPast!=selfAreaId)):
            selfMedNameStr=selfMedNameStr+'<'+str(selfSubId) +'.'+str(selfDocId) +'.'+ str(selfAreaId)+'>'
            flaStart=0
        if flaStart==0:
            selfMedNameStr=selfMedNameStr+str(selfMedName)+'['+str(medCount)+']'
        else:
            selfMedNameStr=selfMedNameStr+','+str(selfMedName)+'['+str(medCount)+']'
        selfSubIdPast=selfSubId
        selfDocIdPast=selfDocId
        selfAreaIdPast=selfAreaId
    selfMedNameStr=selfMedNameStr+'<'
    
    
    return dict(records=records,date_from=date_from,date_to=date_to_get,mpoNameList=mpoNameList, mpoIdList=mpoIdList,selfCountCheckList=selfCountCheckList,selfCountList=selfCountList,selfPrCountList=selfPrCountList,selfPrCountCheckList=selfPrCountCheckList, levelIDList=levelIDList,selfMedNameStr=selfMedNameStr)



#==Faisal======Zero Doctor List===========
def zeroDrUpdate():
    
    db((db.sm_prescription_details.med_type=='SELF')&(db.sm_prescription_details.zero_doc_count==0)).update(zero_doc_count=1)
    
    updateTableStr="update sm_prescription_head a, sm_prescription_details d set d.submit_date =a.submit_date,d.first_date=a.first_date,d.submit_by_id=a.submit_by_id,d.submit_by_name=a.submit_by_name,d.user_type=a.user_type,d.doctor_id=a.doctor_id,d.doctor_name=a.doctor_name,d.image_name=a.image_name,d.image_path=a.image_path,d.lat_long=a.lat_long,d.area_id=a.area_id,d.area_name=a.area_name,d.tl_id=a.tl_id,d.tl_name=a.tl_name,d.reg_id=a.reg_id,d.reg_name=a.reg_name where d.submit_by_id='' and a.cid=d.cid and a.sl=d.sl;"
    updateTable=db.executesql(updateTableStr) 
    
    return 'Success'      
        
    
        
def zeroDrList():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))
    

    c_id = session.cid
    response.title='Zero Doctor List'    
    date_from=request.vars.date_from
    date_to_get=request.vars.date_to
  
    
    date_to_2=datetime.datetime.strptime(str(date_to_get),'%Y-%m-%d')
    date_to_1=date_to_2 + datetime.timedelta(days = 1) 
       
    date_to=str(date_to_1)[0:10]
    
   
    doc=str(request.vars.doc).strip()
   
    qset=db()
    qset = qset(db.sm_prescription_details.cid == c_id)
    qset = qset(db.sm_prescription_details.submit_date >= date_from)
    qset = qset(db.sm_prescription_details.submit_date < date_to)
    
    if doc!='':
       qset = qset(db.sm_prescription_details.doctor_id == doc)      
    
    records = qset.select(db.sm_prescription_details.reg_id,db.sm_prescription_details.reg_name,db.sm_prescription_details.tl_id,db.sm_prescription_details.tl_name,db.sm_prescription_details.area_id,db.sm_prescription_details.area_name,db.sm_prescription_details.submit_by_id,db.sm_prescription_details.submit_by_name,db.sm_prescription_details.sl.count(),db.sm_prescription_details.doctor_id,db.sm_prescription_details.doctor_name,db.sm_prescription_details.zero_doc_count.sum(), orderby=db.sm_prescription_details.submit_by_id, groupby= db.sm_prescription_details.doctor_id)
    
    
    return db._lastsql
    #     return db._lastsql
# ==============MPO List
    mpoNameList=[]
    mpoIdList=[]
    levelIDList=[]
    records_mpoS="SELECT  sup_id, sup_name, level_id FROM sm_supervisor_level WHERE cid = '"+ c_id +"'  and level_depth_no=1 GROUP BY  level_id order by level_id;"
#     return records_mpoS
    records_mpo=db.executesql(records_mpoS,as_dict = True) 
    for records_mpo in records_mpo:
        levelID=records_mpo['level_id']
        mpoID=records_mpo['sup_id']
        mpoName=records_mpo['sup_name']
        mpoNameList.append(mpoName)
        mpoIdList.append(mpoID)
        levelIDList.append(levelID)
        
    
           
# selfprescriptionCount==============================  
       
    records_selfPS="SELECT  count(distinct(sm_prescription_details.sl)) as medCount,sm_prescription_details.sl, sm_prescription_details.submit_by_id as submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.doctor_id order by sm_prescription_details.submit_by_id;"
    
#     return records_selfPS
    records_selfP=db.executesql(records_selfPS,as_dict = True) 
    selfCountList=[]
    selfCountCheckList=[]

    for records_selfP in records_selfP:
        selfSubId=records_selfP['submit_by_id']
        selfDocId=records_selfP['doctor_id']
        selfAreaId=records_selfP['area_id']
        selfMedCount=records_selfP['medCount']
#         pCheck=selfSubId+'.'+selfDocId+'.'+selfAreaId
        pCheck=selfSubId+'.'+selfAreaId
        selfCountCheckList.append(pCheck)
        selfCountList.append(selfMedCount)
    
    
    
# selfproductCount==============================  
       
#     records_selfPrS="SELECT  count(distinct(sm_prescription_details.medicine_id)) as medCount,sm_prescription_details.sl, sm_prescription_head.submit_by_id as submit_by_id,sm_prescription_head.doctor_id,sm_prescription_head.area_id FROM sm_prescription_head,sm_prescription_details WHERE sm_prescription_head.cid = '"+ c_id +"' and sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_head.submit_date >= '"+ date_from +"' and sm_prescription_head.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' and sm_prescription_head.sl =sm_prescription_details.sl GROUP BY  sm_prescription_head.submit_by_id,sm_prescription_head.doctor_id,sm_prescription_head.area_id order by sm_prescription_head.submit_by_id,sm_prescription_head.doctor_id,sm_prescription_head.area_id;"
    records_selfPrS="SELECT  count(sm_prescription_details.medicine_id) as medCount,sm_prescription_details.sl, sm_prescription_details.submit_by_id as submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.doctor_id order by sm_prescription_details.submit_by_id;"
#     return records_selfPrS
    records_selfPr=db.executesql(records_selfPrS,as_dict = True) 
    selfPrCountList=[]
    selfPrCountCheckList=[]
 
    for records_selfPr in records_selfPr:
        selfPrSubId=records_selfPr['submit_by_id']
        selfPrDocId=records_selfPr['doctor_id']
        selfPrAreaId=records_selfPr['area_id']
        selfPrMedCount=records_selfPr['medCount']
#         prCheck=selfPrSubId+'.'+selfPrDocId+'.'+selfPrAreaId
        prCheck=selfPrSubId+'.'+selfPrAreaId
        
        selfPrCountList.append(selfPrMedCount)  
        selfPrCountCheckList.append(prCheck)       
# selfproductUnique==============================  
       
    records_selfPNS="SELECT  distinct(sm_prescription_details.medicine_id) as medicine_id,sm_prescription_details.medicine_name, sm_prescription_details.submit_by_id as submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.doctor_id,sm_prescription_details.medicine_id order by sm_prescription_details.submit_by_id;"
#     return records_selfPNS
    records_selfPN=db.executesql(records_selfPNS,as_dict = True) 
    selfProductList=[]
    selfProductDict={}
    selfSubIdPast=''
    selfDocIdPast=''
    selfAreaIdPast=''
    selfMedNameStr=''
    medName=''
    for records_selfPN in records_selfPN:
        flaStart=1
        selfSubId=records_selfPN['submit_by_id']
        selfDocId=records_selfPN['doctor_id']
        selfAreaId=records_selfPN['area_id']
        selfMedName=records_selfPN['medicine_name']
        if ((selfSubIdPast!=selfSubId) or (selfDocIdPast!=selfDocId) or (selfAreaIdPast!=selfAreaId)):
#             selfMedNameStr=selfMedNameStr+'<'+str(selfSubId) +'.'+str(selfDocId) +'.'+ str(selfAreaId)+'>'
            selfMedNameStr=selfMedNameStr+'<'+str(selfSubId) +'.'+ str(selfAreaId)+'>'
            flaStart=0
        if flaStart==0:
            selfMedNameStr=selfMedNameStr+str(selfMedName)
        else:
            selfMedNameStr=selfMedNameStr+','+str(selfMedName)
        selfSubIdPast=selfSubId
        selfDocIdPast=selfDocId
        selfAreaIdPast=selfAreaId
    selfMedNameStr=selfMedNameStr+'<'
    
    
#     =======================product Count=======
       
    records_selfPNS="SELECT  distinct(sm_prescription_details.medicine_id),count(sm_prescription_details.medicine_id) as medicine_idCount,sm_prescription_details.medicine_name, sm_prescription_details.submit_by_id as submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.doctor_id,sm_prescription_details.medicine_id order by sm_prescription_details.submit_by_id;"
#     return records_selfPNS
    records_selfPN=db.executesql(records_selfPNS,as_dict = True) 
    selfProductList=[]
    selfProductDict={}
    selfSubIdPast=''
    selfDocIdPast=''
    selfAreaIdPast=''
    selfMedNameStr=''
    medName=''
    for records_selfPN in records_selfPN:
        flaStart=1
        selfSubId=records_selfPN['submit_by_id']
        selfDocId=records_selfPN['doctor_id']
        selfAreaId=records_selfPN['area_id']
        selfMedName=records_selfPN['medicine_name']
        medCount=records_selfPN['medicine_idCount']
        if ((selfSubIdPast!=selfSubId)  or (selfAreaIdPast!=selfAreaId)):
#             selfMedNameStr=selfMedNam00tr+'<'+str(selfSubId) +'.'+str(selfDocId) +'.'+ str(selfAreaId)+'>'
            selfMedNameStr=selfMedNameStr+'<'+str(selfSubId) +'.'+ str(selfAreaId)+'>'
            flaStart=0
        if flaStart==0:
            selfMedNameStr=selfMedNameStr+str(selfMedName)+'['+str(medCount)+']'
        else:
            selfMedNameStr=selfMedNameStr+','+str(selfMedName)+'['+str(medCount)+']'
        selfSubIdPast=selfSubId
        selfDocIdPast=selfDocId
        selfAreaIdPast=selfAreaId
    selfMedNameStr=selfMedNameStr+'<'        
  
    
    
    
    
    return dict(records=records,date_from=date_from,date_to=date_to_get,mpoNameList=mpoNameList, mpoIdList=mpoIdList,selfCountCheckList=selfCountCheckList,selfCountList=selfCountList,selfPrCountList=selfPrCountList,selfPrCountCheckList=selfPrCountCheckList, levelIDList=levelIDList,selfMedNameStr=selfMedNameStr)


# #====Faisal====Region wise summary====
def regSummary():
     task_id = 'rm_doctor_visit_manage'
     task_id_view = 'rm_doctor_visit_view'
     access_permission = check_role(task_id)
     access_permission_view = check_role(task_id_view)
     if (access_permission == False) and (task_id_view == False):
         session.flash = 'Access is Denied !'
         redirect (URL(c='default', f='home'))
     
 
     c_id = session.cid
     response.title='Doctor Wise Prescription Summary'    
     date_from=request.vars.date_from
     date_to_get=request.vars.date_to
   
     
     date_to_2=datetime.datetime.strptime(str(date_to_get),'%Y-%m-%d')
     date_to_1=date_to_2 + datetime.timedelta(days = 1) 
        
     date_to=str(date_to_1)[0:10]
     
     doc=str(request.vars.doc).strip()
    
 
     qset=db()
     qset = qset(db.sm_prescription_details.cid == c_id)
     qset = qset(db.sm_prescription_details.submit_date >= date_from)
     qset = qset(db.sm_prescription_details.submit_date < date_to)
     
     if doc!='':
         qset = qset(db.sm_prescription_details.doctor_id == doc)        
 
     records = qset.select(db.sm_prescription_details.reg_id,db.sm_prescription_details.reg_name,db.sm_prescription_details.tl_id,db.sm_prescription_details.tl_name,db.sm_prescription_details.area_id,db.sm_prescription_details.area_name,db.sm_prescription_details.submit_by_id,db.sm_prescription_details.submit_by_name,db.sm_prescription_details.sl.count(),db.sm_prescription_details.doctor_id,db.sm_prescription_details.doctor_id.count(),db.sm_prescription_details.doctor_name,db.sm_prescription_details.zero_doc_count.sum(), orderby=db.sm_prescription_details.submit_by_id,groupby= db.sm_prescription_details.submit_by_id|db.sm_prescription_details.reg_id)
     
       
     
 #     return db._lastsql
 # ==============MPO List
     mpoNameList=[]
     mpoIdList=[]
     levelIDList=[]
     records_mpoS="SELECT  sup_id, sup_name, level_id FROM sm_supervisor_level WHERE cid = '"+ c_id +"'  and level_depth_no=1 GROUP BY  level_id order by level_id;"
 #     return records_mpoS
     records_mpo=db.executesql(records_mpoS,as_dict = True) 
     for records_mpo in records_mpo:
         levelID=records_mpo['level_id']
         mpoID=records_mpo['sup_id']
         mpoName=records_mpo['sup_name']
         mpoNameList.append(mpoName)
         mpoIdList.append(mpoID)
         levelIDList.append(levelID)
 
         
 # selfprescriptionCount==============================  
        
     records_selfPS="SELECT  count(distinct(sm_prescription_details.sl)) as medCount,sm_prescription_details.sl, sm_prescription_details.submit_by_id as submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.submit_by_id,sm_prescription_details.reg_id order by sm_prescription_details.submit_by_id,sm_prescription_details.reg_id;"
     
#     return records_selfPS
     records_selfP=db.executesql(records_selfPS,as_dict = True) 
     selfCountList=[]
     selfCountCheckList=[]
 
     for records_selfP in records_selfP:
         selfSubId=records_selfP['submit_by_id']
         selfDocId=records_selfP['doctor_id']
         selfAreaId=records_selfP['area_id']
         selfMedCount=records_selfP['medCount']
         pCheck=selfSubId+'.'+selfDocId+'.'+selfAreaId
         selfCountCheckList.append(pCheck)
         selfCountList.append(selfMedCount)
  
 # selfproductCount==============================  
        
 #     records_selfPrS="SELECT  count(distinct(sm_prescription_details.medicine_id)) as medCount,sm_prescription_details.sl, sm_prescription_head.submit_by_id as submit_by_id,sm_prescription_head.doctor_id,sm_prescription_head.area_id FROM sm_prescription_head,sm_prescription_details WHERE sm_prescription_head.cid = '"+ c_id +"' and sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_head.submit_date >= '"+ date_from +"' and sm_prescription_head.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' and sm_prescription_head.sl =sm_prescription_details.sl GROUP BY  sm_prescription_head.submit_by_id,sm_prescription_head.doctor_id,sm_prescription_head.area_id order by sm_prescription_head.submit_by_id,sm_prescription_head.doctor_id,sm_prescription_head.area_id;"
     records_selfPrS="SELECT  count(sm_prescription_details.medicine_id) as medCount,sm_prescription_details.sl, sm_prescription_details.submit_by_id as submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.submit_by_id,sm_prescription_details.reg_id order by sm_prescription_details.submit_by_id,sm_prescription_details.reg_id;"
 #     return records_selfPrS
     records_selfPr=db.executesql(records_selfPrS,as_dict = True) 
     selfPrCountList=[]
     selfPrCountCheckList=[]
  
     for records_selfPr in records_selfPr:
         selfPrSubId=records_selfPr['submit_by_id']
         selfPrDocId=records_selfPr['doctor_id']
         selfPrAreaId=records_selfPr['area_id']
         selfPrMedCount=records_selfPr['medCount']
         prCheck=selfPrSubId+'.'+selfPrDocId+'.'+selfPrAreaId
         
         selfPrCountList.append(selfPrMedCount)  
         selfPrCountCheckList.append(prCheck)       
 # selfproductUnique==============================  
        
     records_selfPNS="SELECT  distinct(sm_prescription_details.medicine_id) as medicine_id,sm_prescription_details.medicine_name, sm_prescription_details.submit_by_id as submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.submit_by_id,sm_prescription_details.reg_id,sm_prescription_details.medicine_id order by sm_prescription_details.submit_by_id,sm_prescription_details.reg_id,sm_prescription_details.medicine_id;"
 #     return records_selfPNS
     records_selfPN=db.executesql(records_selfPNS,as_dict = True) 
     selfProductList=[]
     selfProductDict={}
     selfSubIdPast=''
     selfDocIdPast=''
     selfAreaIdPast=''
     selfMedNameStr=''
     medName=''
     for records_selfPN in records_selfPN:
         flaStart=1
         selfSubId=records_selfPN['submit_by_id']
         selfDocId=records_selfPN['doctor_id']
         selfAreaId=records_selfPN['area_id']
         selfMedName=records_selfPN['medicine_name']
         if ((selfSubIdPast!=selfSubId) or (selfDocIdPast!=selfDocId) or (selfAreaIdPast!=selfAreaId)):
             selfMedNameStr=selfMedNameStr+'<'+str(selfSubId) +'.'+str(selfDocId) +'.'+ str(selfAreaId)+'>'
             flaStart=0
         if flaStart==0:
             selfMedNameStr=selfMedNameStr+str(selfMedName)
         else:
             selfMedNameStr=selfMedNameStr+','+str(selfMedName)
         selfSubIdPast=selfSubId
         selfDocIdPast=selfDocId
         selfAreaIdPast=selfAreaId
     selfMedNameStr=selfMedNameStr+'<'
     
     
 #     =======================product Count=======
        
     records_selfPNS="SELECT  distinct(sm_prescription_details.medicine_id),count(sm_prescription_details.medicine_id) as medicine_idCount,sm_prescription_details.medicine_name, sm_prescription_details.submit_by_id as submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.submit_by_id,sm_prescription_details.reg_id,sm_prescription_details.medicine_id order by sm_prescription_details.submit_by_id,sm_prescription_details.reg_id,sm_prescription_details.medicine_id;"
 #     return records_selfPNS
     records_selfPN=db.executesql(records_selfPNS,as_dict = True) 
     selfProductList=[]
     selfProductDict={}
     selfSubIdPast=''
     selfDocIdPast=''
     selfAreaIdPast=''
     selfMedNameStr=''
     medName=''
     for records_selfPN in records_selfPN:
         flaStart=1
         selfSubId=records_selfPN['submit_by_id']
         selfDocId=records_selfPN['doctor_id']
         selfAreaId=records_selfPN['area_id']
         selfMedName=records_selfPN['medicine_name']
         medCount=records_selfPN['medicine_idCount']
         if ((selfSubIdPast!=selfSubId) or (selfDocIdPast!=selfDocId) or (selfAreaIdPast!=selfAreaId)):
             selfMedNameStr=selfMedNameStr+'<'+str(selfSubId) +'.'+str(selfDocId) +'.'+ str(selfAreaId)+'>'
             flaStart=0
         if flaStart==0:
             selfMedNameStr=selfMedNameStr+str(selfMedName)+'['+str(medCount)+']'
         else:
             selfMedNameStr=selfMedNameStr+','+str(selfMedName)+'['+str(medCount)+']'
         selfSubIdPast=selfSubId
         selfDocIdPast=selfDocId
         selfAreaIdPast=selfAreaId
     selfMedNameStr=selfMedNameStr+'<'
     
     
     return dict(records=records,date_from=date_from,date_to=date_to_get,mpoNameList=mpoNameList, mpoIdList=mpoIdList,selfCountCheckList=selfCountCheckList,selfCountList=selfCountList,selfPrCountList=selfPrCountList,selfPrCountCheckList=selfPrCountCheckList, levelIDList=levelIDList,selfMedNameStr=selfMedNameStr)



# ========================PRD Summary==============

def prdSummary():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

   

    c_id = session.cid
    response.title='Prescription Summary'    
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    
#     return mso_id
#    updateTableStr="update sm_prescription_head a, sm_prescription_details d set d.submit_date =a.submit_date,d.first_date=a.first_date,d.submit_by_id=a.submit_by_id,d.submit_by_name=a.submit_by_name,d.user_type=a.user_type,d.doctor_id=a.doctor_id,d.doctor_name=a.doctor_name,d.image_name=a.image_name,d.image_path=a.image_path,d.lat_long=a.lat_long,d.area_id=a.area_id,d.area_name=a.area_name,d.tl_id=a.tl_id,d.tl_name=a.tl_name,d.reg_id=a.reg_id,d.reg_name=a.reg_name where d.submit_by_id='' and a.cid=d.cid and a.sl=d.sl;"
#    updateTable=db.executesql(updateTableStr) 
    
    qset=db()
    qset = qset(db.sm_prescription_head.cid == c_id)
    qset = qset(db.sm_prescription_head.submit_date >= date_from)
    qset = qset(db.sm_prescription_head.submit_date < date_to)
    records = qset.select(db.sm_prescription_head.reg_id,db.sm_prescription_head.reg_name,db.sm_prescription_head.tl_id,db.sm_prescription_head.tl_name,db.sm_prescription_head.area_id,db.sm_prescription_head.area_name,db.sm_prescription_head.submit_by_id,db.sm_prescription_head.submit_by_name,db.sm_prescription_head.sl.count(),db.sm_prescription_head.doctor_id,db.sm_prescription_head.doctor_name, orderby=db.sm_prescription_head.submit_by_id|db.sm_prescription_head.area_id,groupby= db.sm_prescription_head.submit_by_id|db.sm_prescription_head.doctor_id|db.sm_prescription_head.area_id)
    
#    return db._lastsql
# ==============MPO List
    mpoNameList=[]
    mpoIdList=[]
    levelIDList=[]
    records_mpoS="SELECT  sup_id, sup_name, level_id FROM sm_supervisor_level WHERE cid = '"+ c_id +"'  and level_depth_no=1 GROUP BY  level_id order by level_id;"
#     return records_mpoS
    records_mpo=db.executesql(records_mpoS,as_dict = True) 
    for records_mpo in records_mpo:
        levelID=records_mpo['level_id']
        mpoID=records_mpo['sup_id']
        mpoName=records_mpo['sup_name']
        mpoNameList.append(mpoName)
        mpoIdList.append(mpoID)
        levelIDList.append(levelID)

        
# selfprescriptionCount==============================  
       
    records_selfPS="SELECT  count(distinct(sm_prescription_details.sl)) as medCount,sm_prescription_details.sl, sm_prescription_details.submit_by_id as submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id order by sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id;"
    
#     return records_selfPS
    records_selfP=db.executesql(records_selfPS,as_dict = True) 
    selfCountList=[]
    selfCountCheckList=[]

    for records_selfP in records_selfP:
        selfSubId=records_selfP['submit_by_id']
        selfDocId=records_selfP['doctor_id']
        selfAreaId=records_selfP['area_id']
        selfMedCount=records_selfP['medCount']
        pCheck=selfSubId+'.'+selfDocId+'.'+selfAreaId
        selfCountCheckList.append(pCheck)
        selfCountList.append(selfMedCount)
 
# selfproductCount==============================  
       
#     records_selfPrS="SELECT  count(distinct(sm_prescription_details.medicine_id)) as medCount,sm_prescription_details.sl, sm_prescription_head.submit_by_id as submit_by_id,sm_prescription_head.doctor_id,sm_prescription_head.area_id FROM sm_prescription_head,sm_prescription_details WHERE sm_prescription_head.cid = '"+ c_id +"' and sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_head.submit_date >= '"+ date_from +"' and sm_prescription_head.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' and sm_prescription_head.sl =sm_prescription_details.sl GROUP BY  sm_prescription_head.submit_by_id,sm_prescription_head.doctor_id,sm_prescription_head.area_id order by sm_prescription_head.submit_by_id,sm_prescription_head.doctor_id,sm_prescription_head.area_id;"
    records_selfPrS="SELECT  count(sm_prescription_details.medicine_id) as medCount,sm_prescription_details.sl, sm_prescription_details.submit_by_id as submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id order by sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id;"
#     return records_selfPrS
    records_selfPr=db.executesql(records_selfPrS,as_dict = True) 
    selfPrCountList=[]
    selfPrCountCheckList=[]
 
    for records_selfPr in records_selfPr:
        selfPrSubId=records_selfPr['submit_by_id']
        selfPrDocId=records_selfPr['doctor_id']
        selfPrAreaId=records_selfPr['area_id']
        selfPrMedCount=records_selfPr['medCount']
        prCheck=selfPrSubId+'.'+selfPrDocId+'.'+selfPrAreaId
        
        selfPrCountList.append(selfPrMedCount)  
        selfPrCountCheckList.append(prCheck)       
# selfproductUnique==============================  
       
    records_selfPNS="SELECT  distinct(sm_prescription_details.medicine_id) as medicine_id,sm_prescription_details.medicine_name, sm_prescription_details.submit_by_id as submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id,sm_prescription_details.medicine_id order by sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id,sm_prescription_details.medicine_id;"
#     return records_selfPNS
    records_selfPN=db.executesql(records_selfPNS,as_dict = True) 
    selfProductList=[]
    selfProductDict={}
    selfSubIdPast=''
    selfDocIdPast=''
    selfAreaIdPast=''
    selfMedNameStr=''
    medName=''
    for records_selfPN in records_selfPN:
        flaStart=1
        selfSubId=records_selfPN['submit_by_id']
        selfDocId=records_selfPN['doctor_id']
        selfAreaId=records_selfPN['area_id']
        selfMedName=records_selfPN['medicine_name']
        if ((selfSubIdPast!=selfSubId) or (selfDocIdPast!=selfDocId) or (selfAreaIdPast!=selfAreaId)):
            selfMedNameStr=selfMedNameStr+'<'+str(selfSubId) +'.'+str(selfDocId) +'.'+ str(selfAreaId)+'>'
            flaStart=0
        if flaStart==0:
            selfMedNameStr=selfMedNameStr+str(selfMedName)
        else:
            selfMedNameStr=selfMedNameStr+','+str(selfMedName)
        selfSubIdPast=selfSubId
        selfDocIdPast=selfDocId
        selfAreaIdPast=selfAreaId
    selfMedNameStr=selfMedNameStr+'<'
    
    
#     =======================product Count=======
       
    records_selfPNS="SELECT  distinct(sm_prescription_details.medicine_id),count(sm_prescription_details.medicine_id) as medicine_idCount,sm_prescription_details.medicine_name, sm_prescription_details.submit_by_id as submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id FROM sm_prescription_details WHERE sm_prescription_details.cid = '"+ c_id +"' and sm_prescription_details.submit_date >= '"+ date_from +"' and sm_prescription_details.submit_date < '"+ date_to +"' and sm_prescription_details.med_type = 'SELF' GROUP BY  sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id,sm_prescription_details.medicine_id order by sm_prescription_details.submit_by_id,sm_prescription_details.doctor_id,sm_prescription_details.area_id,sm_prescription_details.medicine_id;"
#     return records_selfPNS
    records_selfPN=db.executesql(records_selfPNS,as_dict = True) 
    selfProductList=[]
    selfProductDict={}
    selfSubIdPast=''
    selfDocIdPast=''
    selfAreaIdPast=''
    selfMedNameStr=''
    medName=''
    for records_selfPN in records_selfPN:
        flaStart=1
        selfSubId=records_selfPN['submit_by_id']
        selfDocId=records_selfPN['doctor_id']
        selfAreaId=records_selfPN['area_id']
        selfMedName=records_selfPN['medicine_name']
        medCount=records_selfPN['medicine_idCount']
        if ((selfSubIdPast!=selfSubId) or (selfDocIdPast!=selfDocId) or (selfAreaIdPast!=selfAreaId)):
            selfMedNameStr=selfMedNameStr+'<'+str(selfSubId) +'.'+str(selfDocId) +'.'+ str(selfAreaId)+'>'
            flaStart=0
        if flaStart==0:
            selfMedNameStr=selfMedNameStr+str(selfMedName)+'['+str(medCount)+']'
        else:
            selfMedNameStr=selfMedNameStr+','+str(selfMedName)+'['+str(medCount)+']'
        selfSubIdPast=selfSubId
        selfDocIdPast=selfDocId
        selfAreaIdPast=selfAreaId
    selfMedNameStr=selfMedNameStr+'<'
    
    
    return dict(records=records,date_from=date_from,mpoNameList=mpoNameList, mpoIdList=mpoIdList,selfCountCheckList=selfCountCheckList,selfCountList=selfCountList,selfPrCountList=selfPrCountList,selfPrCountCheckList=selfPrCountCheckList, levelIDList=levelIDList,selfMedNameStr=selfMedNameStr)

