
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

    response.title = 'Doctor Visit'
    

    comRows = db((db.sm_settings.cid == session.cid) & (db. sm_settings.s_key == 'COM_NAME')).select(db.sm_settings.field1, limitby=(0, 1))
    if comRows:
        company_name=comRows[0].field1         
        session.company_name=company_name
        

    c_id = session.cid

    search_form =SQLFORM(db.sm_search_date)
    
    btn_dcrRegion=request.vars.btn_dcrRegion
    btn_dcrRegionD=request.vars.btn_dcrRegionD
    btn_dcrFm=request.vars.btn_dcrFm
    btn_dcrFmD=request.vars.btn_dcrFmD
    btn_dcrTeritory=request.vars.btn_dcrTeritory
    btn_dcrMso=request.vars.btn_dcrMso
    btn_dcrMsoD=request.vars.btn_dcrMsoD
    btn_dcrVisit=request.vars.btn_dcrVisit
    btn_dcrTeritoryD=request.vars.btn_dcrTeritoryD
    btn_dcrDoc=request.vars.btn_dcrDoc
    btn_dcrDocD=request.vars.btn_dcrDocD
    
    
    btn_dcrSummary=request.vars.btn_dcrSummary
    btn_dcrSummaryD=request.vars.btn_dcrSummaryD
    btn_dcrVSummary=request.vars.btn_dcrVSummary
    btn_dcrVSummaryD=request.vars.btn_dcrVSummaryD
    btn_dcrVSummarProduct=request.vars.btn_dcrVSummarProduct
    btn_dcrVSummarProductD=request.vars.btn_dcrVSummarProductD
    
    btn_prSummary=request.vars.btn_prSummary
    btn_prSummaryD=request.vars.btn_prSummaryD
    
    btn_tourSummary=request.vars.btn_tourSummary
    btn_tourSummaryD=request.vars.btn_tourSummaryD
    
    
#     return btn_dcrMsoD
    if (btn_dcrRegion or btn_dcrRegionD or btn_dcrFm or btn_dcrFmD or btn_dcrTeritory or btn_dcrMso or btn_dcrMsoD or btn_dcrVisit or btn_dcrTeritoryD or btn_dcrDoc or btn_dcrDocD or btn_dcrSummary or btn_dcrSummaryD or btn_dcrVSummary or btn_dcrVSummaryD or btn_dcrVSummarProduct or btn_dcrVSummarProductD or btn_prSummary or btn_prSummaryD or btn_tourSummary or btn_tourSummaryD):
        date_from=request.vars.from_dt_3
        date_to=request.vars.to_dt_3
        
        depot=str(request.vars.sales_depot_id_SC)
        rsm_SC=str(request.vars.rsm_SC)
        fm_SC=str(request.vars.fm_SC)
        tr_SC=str(request.vars.tr_SC)
        mso=str(request.vars.mso_id_sales).replace(",","").replace("['","").replace("']","").replace("''","")
        doc_idname=str(request.vars.doc_id_sales).replace(",","").replace("['","").replace("']","").replace("''","")
        
        product=str(request.vars.product)
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
              
        
            if btn_dcrRegion:
                redirect (URL('dcrRsm',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name,brand=brand,category=category,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            if btn_dcrRegionD:
                redirect (URL('dcrRsmD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name,brand=brand,category=category,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            if btn_dcrFm:
                redirect (URL('dcrFm',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name,brand=brand,category=category,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            if btn_dcrFmD:
                redirect (URL('dcrFmD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name,brand=brand,category=category,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            if btn_dcrTeritory:
                redirect (URL('dcrTeritory',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name,brand=brand,category=category,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            if btn_dcrMso:
                redirect (URL('dcrMso',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name,brand=brand,category=category,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            if btn_dcrMsoD:
                redirect (URL('dcrMsoD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name,brand=brand,category=category,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            if btn_dcrVisit:
                redirect (URL('dcrVisit',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name,brand=brand,category=category,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            if btn_dcrTeritoryD:
                redirect (URL('dcrTeritoryD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name,brand=brand,category=category,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            if btn_dcrDoc:
                redirect (URL('dcrDoc',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name,brand=brand,category=category,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            if btn_dcrDocD:
                redirect (URL('dcrDocD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name,brand=brand,category=category,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            if btn_dcrSummary:
                redirect (URL('dcrSummary',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name,brand=brand,category=category,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            if btn_dcrSummaryD:
                redirect (URL('dcrSummaryD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name,brand=brand,category=category,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            if btn_dcrVSummary:
                redirect (URL('dcrVSummary',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name,brand=brand,category=category,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            if btn_dcrVSummaryD:
                redirect (URL('dcrVSummaryD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name,brand=brand,category=category,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            if btn_dcrVSummarProduct:
                redirect (URL('dcrVSummaryProduct',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name,brand=brand,category=category,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            if btn_dcrVSummarProductD:
                redirect (URL('dcrVSummaryProductD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name,brand=brand,category=category,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            if btn_prSummary:
                redirect (URL('prSummary',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name,brand=brand,category=category,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            if btn_prSummaryD:
                redirect (URL('prSummaryD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name,brand=brand,category=category,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            if btn_tourSummary:
                redirect (URL('tourSummary',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name,brand=brand,category=category,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            if btn_tourSummaryD:
                redirect (URL('tourSummaryD',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name,brand=brand,category=category,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))       
    return dict(search_form=search_form)

#---------------------------- Reports
def dcrRsm():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

   

    c_id = session.cid
    response.title='RSM Summary'    
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

    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 

   
   
    
#     return date_from
    qset = db()
    qset = qset(db.sm_doc_visit_sample.cid == c_id)
    qset = qset(db.sm_doc_visit_sample.visit_date >= date_from)
    qset = qset(db.sm_doc_visit_sample.visit_date < date_to_m)
    
    
    if (depot_id!=''):
        qset = qset(db.sm_doc_visit_sample.depot_id == depot_id)

    if (rsm_id!=''):
        qset = qset(db.sm_doc_visit_sample.level1_id == rsm_id)
    if (fm_id!=''):
        qset = qset(db.sm_doc_visit_sample.level2_id == fm_id)
    if (tr_id!=''):
        qset = qset(db.sm_doc_visit_sample.route_id == tr_id)
    if (product_id!=''):
        qset = qset(db.sm_doc_visit_sample.item_id == product_id)
    if (brand!=''):
        qset = qset(db.sm_doc_visit_sample.item_brand == brand)
    if (category!=''):
        qset = qset(db.sm_doc_visit_sample.item_cat == category)
    if (mso_id!=''):
        qset = qset(db.sm_doc_visit_sample.rep_id == mso_id)
    if (doc!=''):
        qset = qset(db.sm_doc_visit_sample.doc_id == doc)
    
    
   
    records = qset.select(db.sm_doc_visit_sample.ALL,(db.sm_doc_visit_sample.qty).sum(), orderby= db.sm_doc_visit_sample.level1_id|db.sm_doc_visit_sample.item_name,groupby= db.sm_doc_visit_sample.level1_id|db.sm_doc_visit_sample.item_id)
#     return db._lastsql
#     return records
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,brand=brand,category=category,product_id=product_id,product_name=product_name,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)

def dcrRsmD():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

   

    c_id = session.cid
    response.title='RSM Summary'    
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
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 

   
   
    
#     return date_from
    qset = db()
    qset = qset(db.sm_doc_visit_sample.cid == c_id)
    qset = qset(db.sm_doc_visit_sample.visit_date >= date_from)
    qset = qset(db.sm_doc_visit_sample.visit_date < date_to_m)
    
    
    if (depot_id!=''):
        qset = qset(db.sm_doc_visit_sample.depot_id == depot_id)

    if (rsm_id!=''):
        qset = qset(db.sm_doc_visit_sample.level1_id == rsm_id)
    if (fm_id!=''):
        qset = qset(db.sm_doc_visit_sample.level2_id == fm_id)
    if (tr_id!=''):
        qset = qset(db.sm_doc_visit_sample.route_id == tr_id)
    if (product_id!=''):
        qset = qset(db.sm_doc_visit_sample.item_id == product_id)
    if (brand!=''):
        qset = qset(db.sm_doc_visit_sample.item_brand == brand)
    if (category!=''):
        qset = qset(db.sm_doc_visit_sample.item_cat == category)
    if (mso_id!=''):
        qset = qset(db.sm_doc_visit_sample.rep_id == mso_id)
    if (doc!=''):
        qset = qset(db.sm_doc_visit_sample.doc_id == doc)
    
    
    
   
    records = qset.select(db.sm_doc_visit_sample.ALL,(db.sm_doc_visit_sample.qty).sum(), orderby= db.sm_doc_visit_sample.level1_id|db.sm_doc_visit_sample.item_name,groupby= db.sm_doc_visit_sample.level1_id|db.sm_doc_visit_sample.item_id)
    myString='DateRange,'+date_from+','+date_to+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
    myString+='FM,'+fm_id+'|'+fm_name+'\n'
    myString+='RT,'+tr_id+'|'+tr_name+'\n'
    myString+='MSO,'+mso_id+'|'+mso_name+'\n'
    myString+='Product,'+product_id+'|'+product_name+'\n'
    myString+='Category,'+category+'\n'
    myString+='Doctor,'+doc+'|'+doc_name+'\n\n'

        
    myString+='RSM  ,  ItemID   , ItemName  ,  A/B/C  ,  Sample Used (Qty)\n'
    
    
    for record in records:
        myString+=str(record[db.sm_doc_visit_sample.level1_id])+','+str(record[db.sm_doc_visit_sample.item_id])+','+str(record[db.sm_doc_visit_sample.item_name])+','+str(record[db.sm_doc_visit_sample.item_cat])+','+str(record[(db.sm_doc_visit_sample.qty).sum()])+'\n'
         
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=RSM_Summary.csv'   
    return str(myString)

def dcrFm():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

   

    c_id = session.cid
    response.title='Fm Summary'    
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
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 

   
   
    
#     return date_from
    qset = db()
    qset = qset(db.sm_doc_visit_sample.cid == c_id)
    qset = qset(db.sm_doc_visit_sample.visit_date >= date_from)
    qset = qset(db.sm_doc_visit_sample.visit_date < date_to_m)
    
    
    if (depot_id!=''):
        qset = qset(db.sm_doc_visit_sample.depot_id == depot_id)

    if (rsm_id!=''):
        qset = qset(db.sm_doc_visit_sample.level1_id == rsm_id)
    if (fm_id!=''):
        qset = qset(db.sm_doc_visit_sample.level2_id == fm_id)
    if (tr_id!=''):
        qset = qset(db.sm_doc_visit_sample.route_id == tr_id)
    if (product_id!=''):
        qset = qset(db.sm_doc_visit_sample.item_id == product_id)
    if (brand!=''):
        qset = qset(db.sm_doc_visit_sample.item_brand == brand)
    if (category!=''):
        qset = qset(db.sm_doc_visit_sample.item_cat == category)   
    if (mso_id!=''):
        qset = qset(db.sm_doc_visit_sample.rep_id == mso_id)
    if (doc!=''):
        qset = qset(db.sm_doc_visit_sample.doc_id == doc)
    
   
    records = qset.select(db.sm_doc_visit_sample.ALL,(db.sm_doc_visit_sample.qty).sum(), orderby= db.sm_doc_visit_sample.level1_id|db.sm_doc_visit_sample.level2_id|db.sm_doc_visit_sample.item_name,groupby= db.sm_doc_visit_sample.level1_id|db.sm_doc_visit_sample.level2_id|db.sm_doc_visit_sample.item_id)
#     return db._lastsql
#     return records
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,brand=brand,category=category,product_id=product_id,product_name=product_name,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)
def dcrFmD():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

   

    c_id = session.cid
    response.title='Fm Summary'    
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
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 

   
   
    
#     return date_from
    qset = db()
    qset = qset(db.sm_doc_visit_sample.cid == c_id)
    qset = qset(db.sm_doc_visit_sample.visit_date >= date_from)
    qset = qset(db.sm_doc_visit_sample.visit_date < date_to_m)
    
    
    if (depot_id!=''):
        qset = qset(db.sm_doc_visit_sample.depot_id == depot_id)

    if (rsm_id!=''):
        qset = qset(db.sm_doc_visit_sample.level1_id == rsm_id)
    if (fm_id!=''):
        qset = qset(db.sm_doc_visit_sample.level2_id == fm_id)
    if (tr_id!=''):
        qset = qset(db.sm_doc_visit_sample.route_id == tr_id)
    if (product_id!=''):
        qset = qset(db.sm_doc_visit_sample.item_id == product_id)
    if (brand!=''):
        qset = qset(db.sm_doc_visit_sample.item_brand == brand)
    if (category!=''):
        qset = qset(db.sm_doc_visit_sample.item_cat == category)   
    if (mso_id!=''):
        qset = qset(db.sm_doc_visit_sample.rep_id == mso_id)
    if (doc!=''):
        qset = qset(db.sm_doc_visit_sample.doc_id == doc)
    
   
    records = qset.select(db.sm_doc_visit_sample.ALL,(db.sm_doc_visit_sample.qty).sum(), orderby= db.sm_doc_visit_sample.level1_id|db.sm_doc_visit_sample.level2_id|db.sm_doc_visit_sample.item_name,groupby= db.sm_doc_visit_sample.level1_id|db.sm_doc_visit_sample.level2_id|db.sm_doc_visit_sample.item_id)
    myString='DateRange,'+date_from+','+date_to+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
    myString+='FM,'+fm_id+'|'+fm_name+'\n'
    myString+='RT,'+tr_id+'|'+tr_name+'\n'
    myString+='MSO,'+mso_id+'|'+mso_name+'\n'
    myString+='Product,'+product_id+'|'+product_name+'\n'
    myString+='Category,'+category+'\n'
    myString+='Doctor,'+doc+'|'+doc_name+'\n\n'

        
    myString+='RSM  ,  FM  ,  ItemID   , ItemName  ,  A/B/C  ,  Sample Used (Qty)\n'
    
    
    for record in records:
        myString+=str(record[db.sm_doc_visit_sample.level1_id])+','+str(record[db.sm_doc_visit_sample.level2_id])+','+str(record[db.sm_doc_visit_sample.item_id])+','+str(record[db.sm_doc_visit_sample.item_name])+','+str(record[db.sm_doc_visit_sample.item_cat])+','+str(record[(db.sm_doc_visit_sample.qty).sum()])+'\n'
         
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=Fm_Summary.csv'   
    return str(myString) 
    
    
    
    
def dcrTeritory():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

   

    c_id = session.cid
    response.title='TR Summary'    
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
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 

   
   
    
#     return date_from
    qset = db()
    qset = qset(db.sm_doc_visit_sample.cid == c_id)
    qset = qset(db.sm_doc_visit_sample.visit_date >= date_from)
    qset = qset(db.sm_doc_visit_sample.visit_date < date_to_m)
    
    
    if (depot_id!=''):
        qset = qset(db.sm_doc_visit_sample.depot_id == depot_id)
    if (rsm_id!=''):
        qset = qset(db.sm_doc_visit_sample.level1_id == rsm_id)
    if (fm_id!=''):
        qset = qset(db.sm_doc_visit_sample.level2_id == fm_id)
    if (tr_id!=''):
        qset = qset(db.sm_doc_visit_sample.route_id == tr_id)
    if (product_id!=''):
        qset = qset(db.sm_doc_visit_sample.item_id == product_id)
    if (brand!=''):
        qset = qset(db.sm_doc_visit_sample.item_brand == brand)
    if (category!=''):
        qset = qset(db.sm_doc_visit_sample.item_cat == category)
    if (mso_id!=''):
        qset = qset(db.sm_doc_visit_sample.rep_id == mso_id)
    if (doc!=''):
        qset = qset(db.sm_doc_visit_sample.doc_id == doc)
    
    
   
    records = qset.select(db.sm_doc_visit_sample.ALL,(db.sm_doc_visit_sample.qty).sum(), orderby= db.sm_doc_visit_sample.level1_id|db.sm_doc_visit_sample.level2_id|db.sm_doc_visit_sample.route_id|db.sm_doc_visit_sample.item_name ,groupby= db.sm_doc_visit_sample.level1_id|db.sm_doc_visit_sample.level2_id|db.sm_doc_visit_sample.route_id|db.sm_doc_visit_sample.item_id)
#     return db._lastsql
#     return records
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,brand=brand,category=category,product_id=product_id,product_name=product_name,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)

def dcrTeritoryD():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

   

    c_id = session.cid
    response.title='TR Summary'    
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
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 

   
   
    
#     return date_from
    qset = db()
    qset = qset(db.sm_doc_visit_sample.cid == c_id)
    qset = qset(db.sm_doc_visit_sample.visit_date >= date_from)
    qset = qset(db.sm_doc_visit_sample.visit_date < date_to_m)
    
    
    if (depot_id!=''):
        qset = qset(db.sm_doc_visit_sample.depot_id == depot_id)

    if (rsm_id!=''):
        qset = qset(db.sm_doc_visit_sample.level1_id == rsm_id)
    if (fm_id!=''):
        qset = qset(db.sm_doc_visit_sample.level2_id == fm_id)
    if (tr_id!=''):
        qset = qset(db.sm_doc_visit_sample.route_id == tr_id)
    if (product_id!=''):
        qset = qset(db.sm_doc_visit_sample.item_id == product_id)
    if (brand!=''):
        qset = qset(db.sm_doc_visit_sample.item_brand == brand)
    if (category!=''):
        qset = qset(db.sm_doc_visit_sample.item_cat == category)
    if (mso_id!=''):
        qset = qset(db.sm_doc_visit_sample.rep_id == mso_id)
    if (doc!=''):
        qset = qset(db.sm_doc_visit_sample.doc_id == doc)
    
    
   
    records = qset.select(db.sm_doc_visit_sample.ALL,(db.sm_doc_visit_sample.qty).sum(), orderby= db.sm_doc_visit_sample.level1_id|db.sm_doc_visit_sample.level2_id|db.sm_doc_visit_sample.route_id|db.sm_doc_visit_sample.item_name ,groupby= db.sm_doc_visit_sample.level1_id|db.sm_doc_visit_sample.level2_id|db.sm_doc_visit_sample.route_id|db.sm_doc_visit_sample.item_id)
#     return records
    #REmove , from record.Cause , means new column in excel    
    myString='DateRange,'+date_from+','+date_to+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
    myString+='FM,'+fm_id+'|'+fm_name+'\n'
    myString+='RT,'+tr_id+'|'+tr_name+'\n'
    myString+='MSO,'+mso_id+'|'+mso_name+'\n'
    myString+='Product,'+product_id+'|'+product_name+'\n'
    myString+='Category,'+category+'\n'
    myString+='Doctor,'+doc+'|'+doc_name+'\n\n'

        
    myString+='RSM  ,  FM  ,  TR   , TR Desc ,     ItemID   , ItemName  ,  A/B/C  ,  Sample Used (Qty)\n'
    
    
    for record in records:
        myString+=str(record[db.sm_doc_visit_sample.level1_id])+','+str(record[db.sm_doc_visit_sample.level2_id])+','+str(record[db.sm_doc_visit_sample.route_id])+','+str(record[db.sm_doc_visit_sample.trDesc])+','+str(record[db.sm_doc_visit_sample.item_id])+','+str(record[db.sm_doc_visit_sample.item_name])+','+str(record[db.sm_doc_visit_sample.item_cat])+','+str(record[(db.sm_doc_visit_sample.qty).sum()])+'\n'
         
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=TR_Summary.csv'   
    return str(myString) 


def dcrMso():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

   

    c_id = session.cid
    response.title='MSO Summary'    
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
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 

   
   
    
#     return date_from
    qset = db()
    qset = qset(db.sm_doc_visit_sample.cid == c_id)
    qset = qset(db.sm_doc_visit_sample.visit_date >= date_from)
    qset = qset(db.sm_doc_visit_sample.visit_date < date_to_m)
    
    
    if (depot_id!=''):
        qset = qset(db.sm_doc_visit_sample.depot_id == depot_id)

    if (rsm_id!=''):
        qset = qset(db.sm_doc_visit_sample.level1_id == rsm_id)
    if (fm_id!=''):
        qset = qset(db.sm_doc_visit_sample.level2_id == fm_id)
    if (tr_id!=''):
        qset = qset(db.sm_doc_visit_sample.route_id == tr_id)
    if (product_id!=''):
        qset = qset(db.sm_doc_visit_sample.item_id == product_id)
    if (brand!=''):
        qset = qset(db.sm_doc_visit_sample.item_brand == brand)
    if (category!=''):
        qset = qset(db.sm_doc_visit_sample.item_cat == category)
    
    if (mso_id!=''):
        qset = qset(db.sm_doc_visit_sample.rep_id == mso_id)
    if (doc!=''):
        qset = qset(db.sm_doc_visit_sample.doc_id == doc)
    
   
    records = qset.select(db.sm_doc_visit_sample.ALL,(db.sm_doc_visit_sample.qty).sum(), orderby= db.sm_doc_visit_sample.level1_id|db.sm_doc_visit_sample.level2_id|db.sm_doc_visit_sample.route_id|db.sm_doc_visit_sample.rep_id|db.sm_doc_visit_sample.item_name ,groupby= db.sm_doc_visit_sample.level1_id|db.sm_doc_visit_sample.level2_id|db.sm_doc_visit_sample.route_id|db.sm_doc_visit_sample.rep_id|db.sm_doc_visit_sample.item_id)
#     return db._lastsql
#     return records
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,brand=brand,category=category,product_id=product_id,product_name=product_name,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)

def dcrMsoD():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

   

    c_id = session.cid
    response.title='MSO Summary'    
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
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 

   
   
    
#     return date_from
    qset = db()
    qset = qset(db.sm_doc_visit_sample.cid == c_id)
    qset = qset(db.sm_doc_visit_sample.visit_date >= date_from)
    qset = qset(db.sm_doc_visit_sample.visit_date < date_to_m)
    
    
    if (depot_id!=''):
        qset = qset(db.sm_doc_visit_sample.depot_id == depot_id)

    if (rsm_id!=''):
        qset = qset(db.sm_doc_visit_sample.level1_id == rsm_id)
    if (fm_id!=''):
        qset = qset(db.sm_doc_visit_sample.level2_id == fm_id)
    if (tr_id!=''):
        qset = qset(db.sm_doc_visit_sample.route_id == tr_id)
    if (product_id!=''):
        qset = qset(db.sm_doc_visit_sample.item_id == product_id)
    if (brand!=''):
        qset = qset(db.sm_doc_visit_sample.item_brand == brand)
    if (category!=''):
        qset = qset(db.sm_doc_visit_sample.item_cat == category)
    
    if (mso_id!=''):
        qset = qset(db.sm_doc_visit_sample.rep_id == mso_id)
    if (doc!=''):
        qset = qset(db.sm_doc_visit_sample.doc_id == doc)
    
   
    records = qset.select(db.sm_doc_visit_sample.ALL,(db.sm_doc_visit_sample.qty).sum(), orderby= db.sm_doc_visit_sample.level1_id|db.sm_doc_visit_sample.level2_id|db.sm_doc_visit_sample.route_id|db.sm_doc_visit_sample.rep_id|db.sm_doc_visit_sample.item_name ,groupby= db.sm_doc_visit_sample.level1_id|db.sm_doc_visit_sample.level2_id|db.sm_doc_visit_sample.route_id|db.sm_doc_visit_sample.rep_id|db.sm_doc_visit_sample.item_id)
#     return db._lastsql
#     return records
        #REmove , from record.Cause , means new column in excel    
    myString='DateRange,'+date_from+','+date_to+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
    myString+='FM,'+fm_id+'|'+fm_name+'\n'
    myString+='RT,'+tr_id+'|'+tr_name+'\n'
    myString+='MSO,'+mso_id+'|'+mso_name+'\n'
    myString+='Product,'+product_id+'|'+product_name+'\n'
    myString+='Category,'+category+'\n'
    myString+='Doctor,'+doc+'|'+doc_name+'\n\n'

        
    myString+='RSM  ,  FM  ,  TR   , TR Desc ,   MSOID,MSOName , ItemID   , ItemName  ,  A/B/C  ,  Sample Used (Qty)\n'
    
    
    for record in records:
        myString+=str(record[db.sm_doc_visit_sample.level1_id])+','+str(record[db.sm_doc_visit_sample.level2_id])+','+str(record[db.sm_doc_visit_sample.route_id])+','+str(record[db.sm_doc_visit_sample.trDesc])+','+str(record[db.sm_doc_visit_sample.rep_id])+','+str(record[db.sm_doc_visit_sample.rep_name])+','+str(record[db.sm_doc_visit_sample.item_id])+','+str(record[db.sm_doc_visit_sample.item_name])+','+str(record[db.sm_doc_visit_sample.item_cat])+','+str(record[(db.sm_doc_visit_sample.qty).sum()])+'\n'
         
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=MSO_Summary.csv'   
    return str(myString) 


def dcrDoc():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

   

    c_id = session.cid
    response.title='Doc Summary'    
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
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 

   
   
    
#     return date_from
    qset = db()
    qset = qset(db.sm_doc_visit_sample.cid == c_id)
    qset = qset(db.sm_doc_visit_sample.visit_date >= date_from)
    qset = qset(db.sm_doc_visit_sample.visit_date < date_to_m)
    
    
    if (depot_id!=''):
        qset = qset(db.sm_doc_visit_sample.depot_id == depot_id)

    if (rsm_id!=''):
        qset = qset(db.sm_doc_visit_sample.level1_id == rsm_id)
    if (fm_id!=''):
        qset = qset(db.sm_doc_visit_sample.level2_id == fm_id)
    if (tr_id!=''):
        qset = qset(db.sm_doc_visit_sample.route_id == tr_id)
    if (product_id!=''):
        qset = qset(db.sm_doc_visit_sample.item_id == product_id)
    if (brand!=''):
        qset = qset(db.sm_doc_visit_sample.item_brand == brand)
    if (category!=''):
        qset = qset(db.sm_doc_visit_sample.item_cat == category)
    
    if (mso_id!=''):
        qset = qset(db.sm_doc_visit_sample.rep_id == mso_id)
    if (doc!=''):
        qset = qset(db.sm_doc_visit_sample.doc_id == doc)
    
   
    records = qset.select(db.sm_doc_visit_sample.ALL,(db.sm_doc_visit_sample.qty).sum(), orderby= db.sm_doc_visit_sample.level1_id|db.sm_doc_visit_sample.level2_id|db.sm_doc_visit_sample.route_id|db.sm_doc_visit_sample.doc_id|db.sm_doc_visit_sample.item_name ,groupby= db.sm_doc_visit_sample.level1_id|db.sm_doc_visit_sample.level2_id|db.sm_doc_visit_sample.route_id|db.sm_doc_visit_sample.doc_id|db.sm_doc_visit_sample.item_id)
#     return db._lastsql
#     return records
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,brand=brand,category=category,product_id=product_id,product_name=product_name,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)

def dcrDocD():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

   

    c_id = session.cid
    response.title='Doc Summary'    
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
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 

   
   
    
#     return date_from
    qset = db()
    qset = qset(db.sm_doc_visit_sample.cid == c_id)
    qset = qset(db.sm_doc_visit_sample.visit_date >= date_from)
    qset = qset(db.sm_doc_visit_sample.visit_date < date_to_m)
    
    
    if (depot_id!=''):
        qset = qset(db.sm_doc_visit_sample.depot_id == depot_id)

    if (rsm_id!=''):
        qset = qset(db.sm_doc_visit_sample.level1_id == rsm_id)
    if (fm_id!=''):
        qset = qset(db.sm_doc_visit_sample.level2_id == fm_id)
    if (tr_id!=''):
        qset = qset(db.sm_doc_visit_sample.route_id == tr_id)
    if (product_id!=''):
        qset = qset(db.sm_doc_visit_sample.item_id == product_id)
    if (brand!=''):
        qset = qset(db.sm_doc_visit_sample.item_brand == brand)
    if (category!=''):
        qset = qset(db.sm_doc_visit_sample.item_cat == category)
    
    if (mso_id!=''):
        qset = qset(db.sm_doc_visit_sample.rep_id == mso_id)
    if (doc!=''):
        qset = qset(db.sm_doc_visit_sample.doc_id == doc)
    
   
    records = qset.select(db.sm_doc_visit_sample.ALL,(db.sm_doc_visit_sample.qty).sum(), orderby= db.sm_doc_visit_sample.level1_id|db.sm_doc_visit_sample.level2_id|db.sm_doc_visit_sample.route_id|db.sm_doc_visit_sample.doc_id|db.sm_doc_visit_sample.item_name ,groupby= db.sm_doc_visit_sample.level1_id|db.sm_doc_visit_sample.level2_id|db.sm_doc_visit_sample.route_id|db.sm_doc_visit_sample.doc_id|db.sm_doc_visit_sample.item_id)
    
    
    myString='DateRange,'+date_from+','+date_to+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
    myString+='FM,'+fm_id+'|'+fm_name+'\n'
    myString+='RT,'+tr_id+'|'+tr_name+'\n'
    myString+='MSO,'+mso_id+'|'+mso_name+'\n'
    myString+='Product,'+product_id+'|'+product_name+'\n'
    myString+='Category,'+category+'\n'
    myString+='Doctor,'+doc+'|'+doc_name+'\n\n'
    myString+='RSM  ,  FM  ,  TR   , TR Desc ,   DocID,DocName , ItemID   , ItemName  ,  A/B/C  ,  Sample Used (Qty)\n'
        
        
    for record in records:
        myString+=str(record[db.sm_doc_visit_sample.level1_id])+','+str(record[db.sm_doc_visit_sample.level2_id])+','+str(record[db.sm_doc_visit_sample.route_id])+','+str(record[db.sm_doc_visit_sample.trDesc])+','+str(record[db.sm_doc_visit_sample.doc_id])+','+str(record[db.sm_doc_visit_sample.doc_name])+','+str(record[db.sm_doc_visit_sample.item_id])+','+str(record[db.sm_doc_visit_sample.item_name])+','+str(record[db.sm_doc_visit_sample.item_cat])+','+str(record[(db.sm_doc_visit_sample.qty).sum()])+'\n'
         
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=Doc_Summary.csv'   
    return str(myString) 

def dcrVisit():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

   

    c_id = session.cid
    response.title='NationalSummary'    
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
    doc=str(request.vars.doc).strip()
    doc_name=str(request.vars.doc_name).strip()
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1) 

   
   
    
#     return date_from
    qset = db()
    qset = qset(db.sm_doc_visit_sample.cid == c_id)
    qset = qset(db.sm_doc_visit_sample.visit_date >= date_from)
    qset = qset(db.sm_doc_visit_sample.visit_date < date_to_m)
    
    
    if (depot_id!=''):
        qset = qset(db.sm_doc_visit_sample.depot_id == depot_id)

    if (rsm_id!=''):
        qset = qset(db.sm_doc_visit_sample.level1_id == rsm_id)
    if (fm_id!=''):
        qset = qset(db.sm_doc_visit_sample.level2_id == fm_id)
    if (tr_id!=''):
        qset = qset(db.sm_doc_visit_sample.route_id == tr_id)
    if (product_id!=''):
        qset = qset(db.sm_doc_visit_sample.item_id == product_id)
    if (brand!=''):
        qset = qset(db.sm_doc_visit_sample.item_brand == brand)
    if (category!=''):
        qset = qset(db.sm_doc_visit_sample.item_cat == category)
    if (doc!=''):
        qset = qset(db.sm_doc_visit_sample.doc_id == doc)
    
    
    
   
    records = qset.select(db.sm_doc_visit_sample.ALL, orderby= db.sm_doc_visit_sample.level1_id|db.sm_doc_visit_sample.level2_id|db.sm_doc_visit_sample.route_id|db.sm_doc_visit_sample.visit_sl|db.sm_doc_visit_sample.item_name)
#     return db._lastsql
#     return records
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,brand=brand,category=category,product_id=product_id,product_name=product_name,doc=doc,doc_name=doc_name)
    
  
def dcrSummary():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

   

    c_id = session.cid
    response.title='Doc Summary'    
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

   
   
    
#     return date_from
    qset = db()
    qset = qset(db.sm_doctor_visit.cid == c_id)
    qset = qset(db.sm_doctor_visit.visit_date >= date_from)
    qset = qset(db.sm_doctor_visit.visit_date < date_to_m)
    qset = qset(db.sm_level.cid == c_id)
    qset = qset(db.sm_doctor_visit.route_id == db.sm_level.level_id)
    qset = qset(db.sm_level.is_leaf == 1)

    
    if (depot_id!=''):
        qset = qset(db.sm_doctor_visit.depot_id == depot_id)

    if (rsm_id!=''):
        qset = qset(db.sm_doctor_visit.level1_id == rsm_id)
    if (fm_id!=''):
        qset = qset(db.sm_doctor_visit.level2_id == fm_id)
    if (tr_id!=''):
        qset = qset(db.sm_doctor_visit.route_id == tr_id)
    if (doc!=''):
        qset = qset(db.sm_doctor_visit.doc_id == doc)
#     if (product_id!=''):
#         qset = qset(db.sm_doctor_visit.item_id == product_id)
#     if (brand!=''):
#         qset = qset(db.sm_doctor_visit.item_brand == brand)
#     if (category!=''):
#         qset = qset(db.sm_doctor_visit.item_cat == category)
    
    if (len(mso_id)>3):
        qset = qset(db.sm_doctor_visit.rep_id == mso_id)
    
   
    records = qset.select(db.sm_doctor_visit.level1_id,db.sm_doctor_visit.level2_id,db.sm_doctor_visit.route_id,db.sm_level.territory_des,db.sm_doctor_visit.rep_id,db.sm_doctor_visit.rep_name,db.sm_doctor_visit.id.count(), orderby= db.sm_doctor_visit.level1_id|db.sm_doctor_visit.level2_id|db.sm_doctor_visit.route_id|db.sm_doctor_visit.rep_id|db.sm_doctor_visit.rep_name ,groupby= db.sm_doctor_visit.level1_id|db.sm_doctor_visit.level2_id|db.sm_doctor_visit.route_id|db.sm_doctor_visit.rep_id|db.sm_doctor_visit.rep_name)
#     return db._lastsql
#     return records
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,brand=brand,category=category,product_id=product_id,product_name=product_name,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)

def dcrSummaryD():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

   

    c_id = session.cid
    response.title='Doc Summary'    
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

   
   
    
#     return date_from
    qset = db()
    qset = qset(db.sm_doctor_visit.cid == c_id)
    qset = qset(db.sm_doctor_visit.visit_date >= date_from)
    qset = qset(db.sm_doctor_visit.visit_date < date_to_m)
    qset = qset(db.sm_level.cid == c_id)
    qset = qset(db.sm_doctor_visit.route_id == db.sm_level.level_id)
    qset = qset(db.sm_level.is_leaf == 1)

    
    if (depot_id!=''):
        qset = qset(db.sm_doctor_visit.depot_id == depot_id)

    if (rsm_id!=''):
        qset = qset(db.sm_doctor_visit.level1_id == rsm_id)
    if (fm_id!=''):
        qset = qset(db.sm_doctor_visit.level2_id == fm_id)
    if (tr_id!=''):
        qset = qset(db.sm_doctor_visit.route_id == tr_id)
    if (doc!=''):
        qset = qset(db.sm_doctor_visit.doc_id == doc)
#     if (product_id!=''):
#         qset = qset(db.sm_doctor_visit.item_id == product_id)
#     if (brand!=''):
#         qset = qset(db.sm_doctor_visit.item_brand == brand)
#     if (category!=''):
#         qset = qset(db.sm_doctor_visit.item_cat == category)
    
    if (len(mso_id)>3):
        qset = qset(db.sm_doctor_visit.rep_id == mso_id)
    
   
    records = qset.select(db.sm_doctor_visit.level1_id,db.sm_doctor_visit.level2_id,db.sm_doctor_visit.route_id,db.sm_level.territory_des,db.sm_doctor_visit.rep_id,db.sm_doctor_visit.rep_name,db.sm_doctor_visit.id.count(), orderby= db.sm_doctor_visit.level1_id|db.sm_doctor_visit.level2_id|db.sm_doctor_visit.route_id|db.sm_doctor_visit.rep_id|db.sm_doctor_visit.rep_name ,groupby= db.sm_doctor_visit.level1_id|db.sm_doctor_visit.level2_id|db.sm_doctor_visit.route_id|db.sm_doctor_visit.rep_id|db.sm_doctor_visit.rep_name)
    
   
    
    myString='DateRange,'+date_from+','+date_to+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
    myString+='FM,'+fm_id+'|'+fm_name+'\n'
    myString+='RT,'+tr_id+'|'+tr_name+'\n'
    myString+='MSO,'+mso_id+'|'+mso_name+'\n'
#     myString+='Product,'+product_id+'|'+product_name+'\n'
#     myString+='Category,'+category+'\n'
    myString+='Doctor,'+doc+'|'+doc_name+'\n\n'
    myString+='RSM  ,  FM  ,  TR   , TR Desc ,   MSO,MSOName , DCR Count\n'
        
    
    for record in records:
            myString+=str(record[db.sm_doctor_visit.level1_id])+','+str(record[db.sm_doctor_visit.level2_id])+','+str(record[db.sm_doctor_visit.route_id])+','+str(record[db.sm_level.territory_des])+','+str(record[db.sm_doctor_visit.rep_id])+','+str(record[db.sm_doctor_visit.rep_name])+','+str(record[db.sm_doctor_visit.id.count()])+'\n'
             
        #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=DCR_Summary.csv'   
    return str(myString)

def dcrVSummary():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

   

    c_id = session.cid
    response.title='Doc Summary'    
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
    if ((len(mso_id)<4) and (tr_id=='')):
        session.flash = 'Please select TR or MSO'
        redirect (URL(c='dcr_report', f='index'))
   
    
#     return date_from
    qset = db()
    qset = qset(db.sm_doctor_visit.cid == c_id)
    qset = qset(db.sm_doctor_visit.visit_date >= date_from)
    qset = qset(db.sm_doctor_visit.visit_date < date_to_m)
    qset = qset(db.sm_level.cid == c_id)
    qset = qset(db.sm_level.level_id == db.sm_doctor_visit.route_id)
#     qset = qset(db.sm_doc_visit_sample.visit_date >= date_from)
#     qset = qset(db.sm_doc_visit_sample.visit_date < date_to_m)
    
    if (depot_id!=''):
        qset = qset(db.sm_doctor_visit.depot_id == depot_id)

    if (rsm_id!=''):
        qset = qset(db.sm_doctor_visit.level1_id == rsm_id)
    if (fm_id!=''):
        qset = qset(db.sm_doctor_visit.level2_id == fm_id)
    if (tr_id!=''):
        qset = qset(db.sm_doctor_visit.route_id == tr_id)
    if (doc!=''):
        qset = qset(db.sm_doctor_visit.doc_id == doc)
#     if (product_id!=''):
#         qset = qset(db.sm_doctor_visit.item_id == product_id)
#     if (brand!=''):
#         qset = qset(db.sm_doctor_visit.item_brand == brand)
#     if (category!=''):
#         qset = qset(db.sm_doctor_visit.item_cat == category)
    
    if (len(mso_id)>3):
        qset = qset(db.sm_doctor_visit.rep_id == mso_id)
    
    records = qset.select(db.sm_doctor_visit.id,db.sm_doctor_visit.visit_dtime,db.sm_doctor_visit.depot_id,db.sm_doctor_visit.note,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.doc_name,db.sm_doctor_visit.level1_id,db.sm_doctor_visit.level2_id,db.sm_doctor_visit.route_id,db.sm_level.territory_des,db.sm_doctor_visit.rep_id,db.sm_doctor_visit.rep_name,db.sm_doctor_visit.giftnsample,groupby=db.sm_doctor_visit.depot_id|db.sm_doctor_visit.level1_id|db.sm_doctor_visit.level2_id|db.sm_doctor_visit.route_id|db.sm_level.territory_des|db.sm_doctor_visit.rep_id|db.sm_doctor_visit.rep_name|db.sm_doctor_visit.doc_id|db.sm_doctor_visit.doc_name|db.sm_doctor_visit.note|db.sm_doctor_visit.id|db.sm_doctor_visit.visit_dtime|db.sm_doctor_visit.giftnsample, orderby= db.sm_doctor_visit.id|db.sm_doctor_visit.visit_dtime)
    
#     records = qset.select(db.sm_doctor_visit.id,db.sm_doctor_visit.visit_dtime,db.sm_doctor_visit.depot_id,db.sm_doctor_visit.note,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.doc_name,db.sm_doctor_visit.level1_id,db.sm_doctor_visit.level2_id,db.sm_doctor_visit.route_id,db.sm_doc_visit_sample.trDesc,db.sm_doctor_visit.rep_id,db.sm_doctor_visit.rep_name,db.sm_doctor_visit.giftnsample,groupby=db.sm_doctor_visit.depot_id|db.sm_doctor_visit.level1_id|db.sm_doctor_visit.level2_id|db.sm_doctor_visit.route_id|db.sm_doc_visit_sample.trDesc|db.sm_doctor_visit.rep_id|db.sm_doctor_visit.rep_name|db.sm_doctor_visit.doc_id|db.sm_doctor_visit.doc_name|db.sm_doctor_visit.note|db.sm_doctor_visit.id|db.sm_doctor_visit.visit_dtime|db.sm_doctor_visit.giftnsample, orderby= db.sm_doctor_visit.depot_id|db.sm_doctor_visit.level1_id|db.sm_doctor_visit.level2_id|db.sm_doctor_visit.route_id|db.sm_doc_visit_sample.trDesc|db.sm_doctor_visit.rep_id|db.sm_doctor_visit.rep_name|db.sm_doctor_visit.doc_id|db.sm_doctor_visit.doc_name|db.sm_doctor_visit.note|db.sm_doctor_visit.id|db.sm_doctor_visit.visit_dtime|db.sm_doctor_visit.giftnsample)
#     return records
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,brand=brand,category=category,product_id=product_id,product_name=product_name,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)


def dcrVSummaryProduct():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

   

    c_id = session.cid
    response.title='Doc Summary'    
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
    if ((len(product_id)<1) and (product_id=='')):
        session.flash = 'Please select product'
        redirect (URL(c='dcr_report', f='index'))
   
    
#     return date_from
    qset = db()
    qset = qset(db.sm_doc_visit_prop.cid == c_id)
    qset = qset(db.sm_doc_visit_prop.visit_date >= date_from)
    qset = qset(db.sm_doc_visit_prop.visit_date < date_to_m)

    
    if (depot_id!=''):
        qset = qset(db.sm_doc_visit_prop.depot_id == depot_id)

    if (rsm_id!=''):
        qset = qset(db.sm_doc_visit_prop.level1_id == rsm_id)
    if (fm_id!=''):
        qset = qset(db.sm_doc_visit_prop.level2_id == fm_id)
    if (tr_id!=''):
        qset = qset(db.sm_doc_visit_prop.route_id == tr_id)
    if (doc!=''):
        qset = qset(db.sm_doc_visit_prop.doc_id == doc)
    if (product_id!=''):
        qset = qset(db.sm_doc_visit_prop.item_id == product_id)
    if (brand!=''):
        qset = qset(db.sm_doc_visit_prop.item_brand == brand)
    if (category!=''):
        qset = qset(db.sm_doc_visit_prop.item_cat == category)
    
    if (len(mso_id)>3):
        qset = qset(db.sm_doc_visit_prop.rep_id == mso_id)
    
    records = qset.select(db.sm_doc_visit_prop.level1_id,db.sm_doc_visit_prop.level2_id,db.sm_doc_visit_prop.route_id,db.sm_doc_visit_prop.rep_id,db.sm_doc_visit_prop.rep_name,db.sm_doc_visit_prop.id.count(), orderby= db.sm_doc_visit_prop.level1_id|db.sm_doc_visit_prop.level2_id|db.sm_doc_visit_prop.route_id|db.sm_doc_visit_prop.rep_id|db.sm_doc_visit_prop.rep_name ,groupby= db.sm_doc_visit_prop.rep_id)
#     return db._lastsql
#     records = qset.select(db.sm_doctor_visit.id,db.sm_doctor_visit.visit_dtime,db.sm_doctor_visit.depot_id,db.sm_doctor_visit.note,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.doc_name,db.sm_doctor_visit.level1_id,db.sm_doctor_visit.level2_id,db.sm_doctor_visit.route_id,db.sm_doc_visit_sample.trDesc,db.sm_doctor_visit.rep_id,db.sm_doctor_visit.rep_name,db.sm_doctor_visit.giftnsample,groupby=db.sm_doctor_visit.depot_id|db.sm_doctor_visit.level1_id|db.sm_doctor_visit.level2_id|db.sm_doctor_visit.route_id|db.sm_doc_visit_sample.trDesc|db.sm_doctor_visit.rep_id|db.sm_doctor_visit.rep_name|db.sm_doctor_visit.doc_id|db.sm_doctor_visit.doc_name|db.sm_doctor_visit.note|db.sm_doctor_visit.id|db.sm_doctor_visit.visit_dtime|db.sm_doctor_visit.giftnsample, orderby= db.sm_doctor_visit.depot_id|db.sm_doctor_visit.level1_id|db.sm_doctor_visit.level2_id|db.sm_doctor_visit.route_id|db.sm_doc_visit_sample.trDesc|db.sm_doctor_visit.rep_id|db.sm_doctor_visit.rep_name|db.sm_doctor_visit.doc_id|db.sm_doctor_visit.doc_name|db.sm_doctor_visit.note|db.sm_doctor_visit.id|db.sm_doctor_visit.visit_dtime|db.sm_doctor_visit.giftnsample)
#     return records
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,brand=brand,category=category,product_id=product_id,product_name=product_name,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)
def dcrVSummaryProductD():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

   

    c_id = session.cid
    response.title='Doc Summary'    
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
    if ((len(product_id)<1) and (product_id=='')):
        session.flash = 'Please select product'
        redirect (URL(c='dcr_report', f='index'))
   
    
#     return date_from
    qset = db()
    qset = qset(db.sm_doc_visit_prop.cid == c_id)
    qset = qset(db.sm_doc_visit_prop.visit_date >= date_from)
    qset = qset(db.sm_doc_visit_prop.visit_date < date_to_m)

    
    if (depot_id!=''):
        qset = qset(db.sm_doc_visit_prop.depot_id == depot_id)

    if (rsm_id!=''):
        qset = qset(db.sm_doc_visit_prop.level1_id == rsm_id)
    if (fm_id!=''):
        qset = qset(db.sm_doc_visit_prop.level2_id == fm_id)
    if (tr_id!=''):
        qset = qset(db.sm_doc_visit_prop.route_id == tr_id)
    if (doc!=''):
        qset = qset(db.sm_doc_visit_prop.doc_id == doc)
    if (product_id!=''):
        qset = qset(db.sm_doc_visit_prop.item_id == product_id)
    if (brand!=''):
        qset = qset(db.sm_doc_visit_prop.item_brand == brand)
    if (category!=''):
        qset = qset(db.sm_doc_visit_prop.item_cat == category)
    
    if (len(mso_id)>3):
        qset = qset(db.sm_doc_visit_prop.rep_id == mso_id)
    
    records = qset.select(db.sm_doc_visit_prop.level1_id,db.sm_doc_visit_prop.level2_id,db.sm_doc_visit_prop.route_id,db.sm_doc_visit_prop.rep_id,db.sm_doc_visit_prop.rep_name,db.sm_doc_visit_prop.id.count(), orderby= db.sm_doc_visit_prop.level1_id|db.sm_doc_visit_prop.level2_id|db.sm_doc_visit_prop.route_id|db.sm_doc_visit_prop.rep_id|db.sm_doc_visit_prop.rep_name ,groupby= db.sm_doc_visit_prop.rep_id)
    
    myString='DateRange,'+date_from+','+date_to+'\n'
    myString+='Depot/Branch,'+depot_id+'|'+depot_name+'\n'
    myString+='RSM,'+rsm_id+'|'+rsm_name+'\n'
    myString+='FM,'+fm_id+'|'+fm_name+'\n'
    myString+='RT,'+tr_id+'|'+tr_name+'\n'
    myString+='MSO,'+mso_id+'|'+mso_name+'\n'
    myString+='Product,'+product_id+'|'+product_name+'\n'
    myString+='Category,'+category+'\n'
    myString+='Doctor,'+doc+'|'+doc_name+'\n\n'
    myString+='RSM  ,  FM  ,  TR  ,  MSO  ,  MSO Name  ,  DCR Count\n'
        
    
    for record in records:
            myString+=str(record[db.sm_doc_visit_prop.level1_id])+','+str(record[db.sm_doc_visit_prop.level2_id])+','+str(record[db.sm_doc_visit_prop.route_id])+','+str(record[db.sm_doc_visit_prop.rep_id])+','+str(record[db.sm_doc_visit_prop.rep_name])+','+str(record[db.sm_doc_visit_prop.id.count()])+'\n'
             
        #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=DCR_Summary_Product.csv'   
    return str(myString)


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
        qset = qset(db.sm_prescription_head.reg_id == rsm_id)
    if (fm_id!=''):
        qset = qset(db.sm_prescription_head.tl_id == fm_id)
    if (tr_id!=''):
        qset = qset(db.sm_prescription_head.area_id == tr_id)
    if (doc!=''):
        qset = qset(db.sm_prescription_head.doctor_id == doc)
#     if (product_id!=''):
#         qset = qset(db.sm_prescription_details.medicine_id == product_id)
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
#     return qset_other
    
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,brand=brand,category=category,product_id=product_id,product_name=product_name,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name,selfSbmittedByList=selfSbmittedByList,selfSbmittedByCountList=selfSbmittedByCountList,otherSbmittedByList=otherSbmittedByList,otherSbmittedByCountList=otherSbmittedByCountList,unknownSbmittedByList=unknownSbmittedByList,unknownSbmittedByCountList=unknownSbmittedByCountList)


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


# ======================Tour==========================
def tourSummary():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

   

    c_id = session.cid
    response.title='Tour Summary'    
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
#     if ((len(rsm_id)<1) and (fm_id<1) and (tr_id<1) and (doc<1) and (product_id<1) and (mso_id<1)):
#         session.flash = 'Please select RSM or FM or TR or product or submitted by'
#         redirect (URL(c='dcr_report', f='index'))
   
    
#     return date_from
    qset=db()
    qset = qset(db.sm_doctor_visit_plan.cid == c_id)
    qset = qset(db.sm_microunion.cid == c_id)
    qset = qset(db.sm_doctor_visit_plan.route_id == db.sm_microunion.microunion_id)
    qset = qset(db.sm_doctor_visit_plan.schedule_date     >= date_from)
    qset = qset(db.sm_doctor_visit_plan.schedule_date     <= date_to)
    if (rsm_id!=''):
        qset = qset(db.sm_microunion.level1 == rsm_id)
    if (fm_id!=''):
        qset = qset(db.sm_microunion.level2 == fm_id)
    if (tr_id!=''):
        qset = qset(db.sm_microunion.area_id == tr_id)
    records = qset.select(db.sm_microunion.level1,db.sm_microunion.level1_name,db.sm_microunion.level2,db.sm_microunion.level2_name,db.sm_microunion.area_id,db.sm_microunion.area_name,db.sm_doctor_visit_plan.rep_id,db.sm_doctor_visit_plan.rep_name,db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.status,db.sm_doctor_visit_plan.schedule_date, orderby=db.sm_doctor_visit_plan.rep_name|db.sm_doctor_visit_plan.schedule_date,groupby= db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.route_id|db.sm_doctor_visit_plan.route_name)
#     return records
    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,brand=brand,category=category,product_id=product_id,product_name=product_name,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)


