
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
    
    date_wise_visit_count=request.vars.date_wise_visit_count
    dcr_count_visit_count=request.vars.dcr_count_visit_count
    
    dcr_day_count=request.vars.dcr_day_count
    
    dcr_sum=request.vars.dcr_sum
    client_sum=request.vars.client_sum
    
    
#     return btn_dcrMsoD
    if (btn_dcrRegion or btn_dcrRegionD or btn_dcrFm or btn_dcrFmD or btn_dcrTeritory or btn_dcrMso or btn_dcrMsoD or btn_dcrVisit or btn_dcrTeritoryD or btn_dcrDoc or btn_dcrDocD or btn_dcrSummary or btn_dcrSummaryD or btn_dcrVSummary or btn_dcrVSummaryD or btn_dcrVSummarProduct or btn_dcrVSummarProductD or btn_prSummary or btn_prSummaryD or date_wise_visit_count or dcr_count_visit_count or dcr_day_count):
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
        if dateDiff>90 and not dcr_day_count:
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
            
            if dcr_day_count:
                redirect (URL('dcr_day_count',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name,brand=brand,category=category,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            
            if date_wise_visit_count:
                redirect (URL('dcrSummaryDateWiseVisitCount',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name,brand=brand,category=category,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            if dcr_count_visit_count:
                redirect (URL('dcrCountVisitCount',vars=dict(date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,product_id=product_id,product_name=product_name,brand=brand,category=category,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)))
            
    if (dcr_sum or client_sum):
        yearGet=request.vars.yearGet
        monthGet=request.vars.monthGet
        tr_SC2= request.vars.tr_SC2
           
        if ((yearGet=='') or (monthGet=='') or (tr_SC2=='')):
            response.flash="Please Select Year ,Month And Tr"
        else:
            if dcr_sum:
                redirect (URL('dcr_sum',vars=dict(yearGet=yearGet,monthGet=monthGet,tr_SC2=tr_SC2)))
            if client_sum:
                redirect (URL('client_sum',vars=dict(yearGet=yearGet,monthGet=monthGet,tr_SC2=tr_SC2)))
            
#         flagRep=0
#         reportShow=''
#             recRep=db((db.sm_doc_visit_report.cid == cid) & (db.sm_doc_visit_report.y_month == year_month)  & (db.sm_doc_visit_report.tr==se_market_report)).select(db.sm_doc_visit_report.ALL, orderby=db.sm_doc_visit_report.tr)
           
#             
#             reportShow=reportShow+'<tr>'
#             reportShow=reportShow+'<td style="background-color:#FFC">'+str(recRep.doc)+'<td style="background-color:#FFC">'+str(recRep.doc_name)+'</td>'+'<td>'+str(d_1)+'</td>'+'<td>'+str(d_2)+'</td>'+'<td>'+str(d_3)+'</td>'+'<td>'+str(d_4)+'</td>'+'<td>'+str(d_5)+'</td>'+'<td>'+str(d_6)+'</td>'+'<td>'+str(d_7)+'</td>'+'<td>'+str(d_8)+'</td>'+'<td>'+str(d_9)+'</td>'+'<td>'+str(d_10)+'</td>'+'<td>'+str(d_11)+'</td>'+'<td>'+str(d_12)+'</td>'+'<td>'+str(d_13)+'</td>'+'<td>'+str(d_14)+'</td>'+'<td>'+str(d_15)+'</td>'+'<td>'+str(d_16)+'</td>'+'<td>'+str(d_17)+'</td>'+'<td>'+str(d_18)+'</td>'+'<td>'+str(d_19)+'</td>'+'<td>'+str(d_20)+'</td>'+'<td>'+str(d_21)+'</td>'+'<td>'+str(d_22)+'</td>'+'<td>'+str(d_23)+'</td>'+'<td>'+str(d_24)+'</td>'+'<td>'+str(d_25)+'</td>'+'<td>'+str(d_26)+'</td>'+'<td>'+str(d_27)+'</td>'+'<td>'+str(d_28)+'</td>'+'<td>'+str(d_29)+'</td>'+'<td>'+str(d_30)+'</td>'+'<td>'+str(d_31)+'</td>'+'<td style="background-color:#FFC">'+str(total)+'</td>'
#             reportShow=reportShow+'</tr>'
#     #             return total
#     #         reportShow=reportShow+'<tr>'
#     #         reportShow=reportShow+'<td>'+str(recRep.rsm_id)+'<td>'+str(recRep.rsm_name)+'</td>'+'<td>'+str(recRep.fm_id)+'<td>'+str(recRep.fm_name)+'</td>'+'<td>'+str(recRep.tr)+'<td>'+str(recRep.tr_name)+'</td>'+'<td>'+str(recRep.doc)+'<td>'+str(recRep.doc_name)+'</td>'+'<td>'+str(recRep.d_1)+'</td>'+'<td>'+str(recRep.d_2)+'</td>'+'<td>'+str(recRep.d_3)+'</td>'+'<td>'+str(recRep.d_4)+'</td>'+'<td>'+str(recRep.d_5)+'</td>'+'<td>'+str(recRep.d_6)+'</td>'+'<td>'+str(recRep.d_7)+'</td>'+'<td>'+str(recRep.d_8)+'</td>'+'<td>'+str(recRep.d_9)+'</td>'+'<td>'+str(recRep.d_10)+'</td>'+'<td>'+str(recRep.d_11)+'</td>'+'<td>'+str(recRep.d_12)+'</td>'+'<td>'+str(recRep.d_13)+'</td>'+'<td>'+str(recRep.d_14)+'</td>'+'<td>'+str(recRep.d_15)+'</td>'+'<td>'+str(recRep.d_16)+'</td>'+'<td>'+str(recRep.d_17)+'</td>'+'<td>'+str(recRep.d_18)+'</td>'+'<td>'+str(recRep.d_19)+'</td>'+'<td>'+str(recRep.d_20)+'</td>'+'<td>'+str(recRep.d_21)+'</td>'+'<td>'+str(recRep.d_22)+'</td>'+'<td>'+str(recRep.d_23)+'</td>'+'<td>'+str(recRep.d_24)+'</td>'+'<td>'+str(recRep.d_25)+'</td>'+'<td>'+str(recRep.d_26)+'</td>'+'<td>'+str(recRep.d_27)+'</td>'+'<td>'+str(recRep.d_28)+'</td>'+'<td>'+str(recRep.d_29)+'</td>'+'<td>'+str(recRep.d_30)+'</td>'+'<td>'+str(recRep.d_31)+'</td>'+'<td>'+str(total)+'</td>'
#     #         reportShow=reportShow+'</tr>'
#         
#         reportShow=reportShow+'</table>'   
                     
    return dict(search_form=search_form)
def dcr_sum():
    yearGet=request.vars.yearGet
    monthGet=request.vars.monthGet
    tr_SC2= request.vars.tr_SC2
    year_month=str(yearGet)+'-'+str(monthGet) 
    se_market_report=tr_SC2.split('|')[0]
    cid=session.cid
    rsm=''
    fm=''
    tr=''
    docTr=0
    recRepDoc=db((db.sm_doctor_area.cid == cid) & (db.sm_doctor_area.area_id == se_market_report)).select(db.sm_doctor_area.id.count(), limitby=(0,1))
    if recRepDoc:
        docTr=recRepDoc[0][db.sm_doctor_area.id.count()]
    
    
    recordDocStr="Select doc_id, doc_name FROM sm_doctor_area where doc_id NOT IN ( Select doc from sm_doc_visit_report where tr ='"+str(se_market_report)+"' and y_month='"+str(year_month)+"') and area_id='"+str(se_market_report)+"'"
    recordDoc=db.executesql(recordDocStr,as_dict = True)
    
    
#     db((db.sm_doctor_area.cid == cid) & (db.sm_doc_visit_report.cid == cid)  & (db.sm_doc_visit_report.doc!= db.sm_doctor_area.doc_id)  & (db.sm_doctor_area.area_id==se_market_report)& (db.sm_doc_visit_report.tr==se_market_report) & (db.sm_doc_visit_report.y_month == year_month)  ).select(db.sm_doctor_area.doc_id,db.sm_doctor_area.doc_name, orderby=db.sm_doctor_area.doc_name , groupby=db.sm_doctor_area.doc_id)
#     return db._lastsql
#     return recordDoc
    
    records=db((db.sm_doc_visit_report.cid == cid) & (db.sm_doc_visit_report.y_month == year_month)  & (db.sm_doc_visit_report.tr==se_market_report)).select(db.sm_doc_visit_report.ALL, orderby=db.sm_doc_visit_report.tr)
    for rec in records:
        rsm=str(rec.rsm_name)+' | '+str(rec.rsm_id)
        fm=str(rec.fm_name)+' | '+str(rec.fm_id)
        tr=str(rec.tr_name)+' | '+str(rec.tr)
    
    
    if monthGet=='01':monthGet='Jan'
    if monthGet=='02':monthGet='Feb'
    if monthGet=='03':monthGet='Mar'
    if monthGet=='04':monthGet='Apr'
    if monthGet=='05':monthGet='May'
    if monthGet=='06':monthGet='Jun'
    if monthGet=='07':monthGet='Jul'
    if monthGet=='08':monthGet='Aug'
    if monthGet=='09':monthGet='Sep'
    if monthGet=='10':monthGet='Oct'
    if monthGet=='11':monthGet='Nov'
    if monthGet=='12':monthGet='Dec'
    
    
    
    return dict(records=records,yearGet=yearGet,monthGet=monthGet,tr_SC2=tr_SC2,rsm=rsm,fm=fm,tr=tr,docTr=docTr,recordDoc=recordDoc)

def client_sum():
    yearGet=request.vars.yearGet
    monthGet=request.vars.monthGet
    tr_SC2= request.vars.tr_SC2
    year_month=str(yearGet)+'-'+str(monthGet) 
    se_market_report=tr_SC2.split('|')[0]
    cid=session.cid
#     cid='IBNSINA'
    rsm=''
    fm=''
    tr=''
    recRepDoc=db((db.sm_client.cid == cid) & (db.sm_client.area_id == se_market_report)).select(db.sm_client.id.count(), limitby=(0,1))
    docTr=0
    if recRepDoc:
        docTr=recRepDoc[0][db.sm_client.id.count()]
    records=db((db.sm_client_visit_report.cid == cid) & (db.sm_client_visit_report.y_month == year_month)  & (db.sm_client_visit_report.tr==se_market_report)).select(db.sm_client_visit_report.ALL, orderby=db.sm_client_visit_report.tr)
    for rec in records:
        rsm=str(rec.rsm_name)+' | '+str(rec.rsm_id)
        fm=str(rec.fm_name)+' | '+str(rec.fm_id)
        tr=str(rec.tr_name)+' | '+str(rec.tr)
    
    
    if monthGet=='01':monthGet='Jan'
    if monthGet=='02':monthGet='Feb'
    if monthGet=='03':monthGet='Mar'
    if monthGet=='04':monthGet='Apr'
    if monthGet=='05':monthGet='May'
    if monthGet=='06':monthGet='Jun'
    if monthGet=='07':monthGet='Jul'
    if monthGet=='08':monthGet='Aug'
    if monthGet=='09':monthGet='Sep'
    if monthGet=='10':monthGet='Oct'
    if monthGet=='11':monthGet='Nov'
    if monthGet=='12':monthGet='Dec'
    
    recordDocStr="Select client_id, name FROM sm_client where client_id NOT IN ( Select client_id from sm_client_visit_report where tr ='"+str(se_market_report)+"' and y_month='"+str(year_month)+"') and area_id='"+str(se_market_report)+"'"
#     return recordDocStr
    recordDoc=db.executesql(recordDocStr,as_dict = True)
    
    return dict(records=records,yearGet=yearGet,monthGet=monthGet,tr_SC2=tr_SC2,rsm=rsm,fm=fm,tr=tr,docTr=docTr,recordDoc=recordDoc)
    
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
    response.title='Visit Summary'    
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

#Faisal
def dcrSummaryDateWiseVisitCount():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

   

    c_id = session.cid
    response.title='DCR Summary Date wise '    
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
    
    if (len(mso_id)>3):
        qset = qset(db.sm_doctor_visit.rep_id == mso_id)
    
   
    records = qset.select(db.sm_doctor_visit.level1_id,db.sm_doctor_visit.level2_id,db.sm_doctor_visit.route_id,db.sm_level.territory_des,db.sm_doctor_visit.rep_id,db.sm_doctor_visit.rep_name,db.sm_doctor_visit.visit_date,db.sm_doctor_visit.id.count(), orderby= db.sm_doctor_visit.level1_id|db.sm_doctor_visit.level2_id|db.sm_doctor_visit.route_id|db.sm_doctor_visit.rep_id|db.sm_doctor_visit.rep_name|db.sm_doctor_visit.visit_date,groupby= db.sm_doctor_visit.level1_id|db.sm_doctor_visit.level2_id|db.sm_doctor_visit.route_id|db.sm_doctor_visit.rep_id|db.sm_doctor_visit.rep_name|db.sm_doctor_visit.visit_date)

    return dict(records=records,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,brand=brand,category=category,product_id=product_id,product_name=product_name,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)

def dcrCountVisitCount():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

   

    c_id = session.cid
    response.title='DCR Summary'    
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
    date_to_m=str(date_to_m + datetime.timedelta(days = 1) )

       
    condition=''
    if (depot_id!=''):            
        condition=condition+"AND depot_id = '"+str(depot_id)+"'"  
    if (rsm_id!=''):            
        condition=condition+"AND level1_id = '"+str(rsm_id)+"'"  
    if (fm_id!=''):            
        condition=condition+"AND level2_id = '"+str(fm_id)+"'"  
    if (tr_id!=''):            
        condition=condition+"AND route_id = '"+str(tr_id)+"'"  
    if (doc!=''):            
        condition=condition+"AND doc_id = '"+str(doc)+"'"  
    if (mso_id!=''):            
        condition=condition+"AND rep_id = '"+str(mso_id)+"'"  
            
        
    dateRecords="SELECT sm_doctor_visit.level1_id as level1_id,sm_doctor_visit.level2_id as level2_id,sm_doctor_visit.route_id as route_id,sm_level.territory_des as territory_des,sm_doctor_visit.rep_id as rep_id,sm_doctor_visit.rep_name as rep_name,count(distinct(sm_doctor_visit.visit_date)) as visit_date,count(sm_doctor_visit.id) as id FROM sm_doctor_visit,sm_level WHERE ((sm_doctor_visit.cid = '"+c_id+"') AND (sm_doctor_visit.visit_date >= '"+date_from+"') AND  (sm_doctor_visit.visit_date < '"+date_to_m+"') AND (sm_level.cid='"+c_id+"') AND (sm_doctor_visit.route_id = sm_level.level_id) AND (sm_level.is_leaf = 1) "+condition+") GROUP BY sm_doctor_visit.level1_id,sm_doctor_visit.level2_id,sm_doctor_visit.route_id,sm_doctor_visit.rep_id,sm_doctor_visit.rep_name ORDER BY sm_doctor_visit.level1_id,sm_doctor_visit.level2_id,sm_doctor_visit.route_id,sm_doctor_visit.rep_id,sm_doctor_visit.rep_name;"

    recordList=db.executesql(dateRecords,as_dict = True)     


    return dict(recordList=recordList,date_from=date_from,date_to=date_to,depot_id=depot_id,depot_name=depot_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr_id=tr_id,tr_name=tr_name,brand=brand,category=category,product_id=product_id,product_name=product_name,mso_id=mso_id,mso_name=mso_name,doc=doc,doc_name=doc_name)


#End Faisal

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
    response.title='DCR'    
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
    if (doc!=''):
        qset = qset(db.sm_doc_visit_sample.doc_id == doc)
    if (product_id!=''):
        qset = qset(db.sm_doc_visit_sample.item_id == product_id)
    if (brand!=''):
        qset = qset(db.sm_doc_visit_sample.item_brand == brand)
    if (category!=''):
        qset = qset(db.sm_doc_visit_sample.item_cat == category)
    
    if (len(mso_id)>3):
        qset = qset(db.sm_doc_visit_sample.rep_id == mso_id)
    
    records = qset.select(db.sm_doc_visit_sample.level1_id,db.sm_doc_visit_sample.level2_id,db.sm_doc_visit_sample.route_id,db.sm_doc_visit_sample.rep_id,db.sm_doc_visit_sample.rep_name,db.sm_doc_visit_sample.id.count(), orderby= db.sm_doc_visit_sample.level1_id|db.sm_doc_visit_sample.level2_id|db.sm_doc_visit_sample.route_id|db.sm_doc_visit_sample.rep_id|db.sm_doc_visit_sample.rep_name ,groupby= db.sm_doc_visit_sample.rep_id)
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
# =====================================================

def dcr_day_count():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

   

    c_id = session.cid
    response.title='dcr_day_count'    
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
    qset = qset(db.sm_doctor_visit.cid == c_id)
    qset = qset(db.sm_doctor_visit.visit_date >= date_from)
    qset = qset(db.sm_doctor_visit.visit_date <= date_to)
#     qset = qset(db.sm_prescription_details.cid == c_id)
#     qset = qset(db.sm_prescription_details.sl == db.sm_prescription_head.sl)

    if (rsm_id!=''):
        qset = qset(db.sm_doctor_visit.level1_id == rsm_id)
    if (fm_id!=''):
        qset = qset(db.sm_doctor_visit.level2_id == fm_id)
    if (tr_id!=''):
        qset = qset(db.sm_doctor_visit.route_id == tr_id)
#     if (doc!=''):
#         qset = qset(db.sm_prescription_head.doctor_id == doc)
#     if (product_id!=''):
#         qset = qset(db.sm_prescription_details.medicine_id == product_id)
    if (len(mso_id)>3):
        qset = qset(db.sm_doctor_visit.rep_id == mso_id)
    
    
    records = qset.select(db.sm_doctor_visit.doc_id,db.sm_doctor_visit.doc_name,db.sm_doctor_visit.visit_date,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name, orderby=db.sm_doctor_visit.visit_date|db.sm_doctor_visit.doc_id,groupby= db.sm_doctor_visit.visit_date|db.sm_doctor_visit.doc_id)
    
    
    myString='DateRange,'+date_from+','+date_to+'\n'
    myString+='MSO,'+mso_id+'|'+mso_name+'\n'
    myString+='Area,'+tr_id+'|'+tr_name+'\n'
    myString+='FM,'+fm_id+'|'+fm_name+'\n'
    myString+='Reg,'+rsm_id+'|'+rsm_name+'\n\n'
    
    myString+='doctorID  ,  doctorName ,AreaID, AreaName ,  Date  ,  Visit\n'
    for record in records:
        doctorID=str(record.doc_id)
        doctorName=str(record.doc_name)
        Date=str(record.visit_date)
        route_id=str(record.route_id)
        route_name=str(record.route_name)
        Visit='1'
        
        myString+=doctorID+','+doctorName+','+route_id+','+route_name+','+Date+','+Visit+'\n'
         
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=dcr.csv'   
    return str(myString)