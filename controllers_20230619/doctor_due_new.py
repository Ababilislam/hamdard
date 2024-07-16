# ========================================================================================================

######################################## 24/08/2017  Nazma

# def doctorDueInsert():
#     cid= 'SKF'   
#     ins_dict = ''
#     ins_list = []
#     inCountList = ''
#     dateId = ''
#     dueRecords =     ''
#     current_date1 = str(current_date)
# 
#     date_to_m=datetime.datetime.strptime(str(current_date1),'%Y-%m-%d') 
#     date_to_m=date_to_m - datetime.timedelta(days = 1)  
#     date_to_m= str(date_to_m)[0:10]
#     
#  # Bulk_insert
#         #   ----------------------
# 
#     ins_dict= {'cid':cid, 'rpt_date':date_to_m , 'status' : 'Due' }
#     ins_list.append(ins_dict)
# 
#     
#     if len(ins_list) > 0:
#     #Bulk insert
#         inCountList=db.doctor_due.bulk_insert(ins_list)

#     return 'Success'
           
############### 12/09/2017

def docReportInsert():
        cid= 'IBNSINA'   
        response.title='trDLoad'
        y_month=''
#         dueRows=db((db.doctor_due.cid==cid) & (db.doctor_due.status=='Due')).select(db.doctor_due.cid,db.doctor_due.rpt_date,db.doctor_due.status,orderby=db.doctor_due.rpt_date,limitby=(0,1))
#         if dueRows:
#             visit_date=str(dueRows[0].rpt_date)
#             visit_date_month=str(dueRows[0].rpt_date).split('-')[0]+'-'+str(dueRows[0].rpt_date).split('-')[1]
#             y_month=str(visit_date_month)
        

        qset=db()
        qset=qset((db.sm_doctor_visit.cid==cid)  & (db.sm_doctor_visit.r_flag==0))
        DoctorVisitRows=qset.select(db.sm_doctor_visit.cid,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.doc_name,db.sm_doctor_visit.visit_date,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.level1_id,db.sm_doctor_visit.level1_name,db.sm_doctor_visit.level2_id,db.sm_doctor_visit.level2_name,orderby=db.sm_doctor_visit.doc_id|db.sm_doctor_visit.route_id,groupby=db.sm_doctor_visit.doc_id|db.sm_doctor_visit.route_id,limitby=(0,10))
        
        for DoctorVisitRows in DoctorVisitRows:
            cid=DoctorVisitRows.cid
            doc_id=DoctorVisitRows.doc_id
            doc_name=DoctorVisitRows.doc_name    
            rsm_id=DoctorVisitRows.level1_id
            rsm_name=DoctorVisitRows.level1_name
            fm_id=DoctorVisitRows.level2_id
            fm_name=DoctorVisitRows.level2_name
            tr_id=DoctorVisitRows.route_id
            tr_name=DoctorVisitRows.route_name
            visit_date=DoctorVisitRows.visit_date
            
            visit_date_month=str(visit_date).split('-')[0]+'-'+str(visit_date).split('-')[1]
            y_month=str(visit_date_month)
            
            qsetD=db()
            qsetD=qsetD((db.sm_doc_visit_report.cid==cid) & (db.sm_doc_visit_report.y_month==y_month) & (db.sm_doc_visit_report.tr==tr_id) & (db.sm_doc_visit_report.doc==doc_id))
            DRows=qsetD.select(db.sm_doc_visit_report.doc,limitby=(0,1))
            if DRows:
                pass
            else:
                insDoc=db.sm_doc_visit_report.insert(cid=cid,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr=tr_id,tr_name=tr_name,y_month=y_month,rpt_date=visit_date,doc=doc_id,doc_name=doc_name)
            updater_flag=db((db.sm_doctor_visit.cid==cid) & (db.sm_doctor_visit.visit_date==visit_date) & (db.sm_doctor_visit.doc_id==doc_id) & (db.sm_doctor_visit.route_id==tr_id) & (db.sm_doctor_visit.r_flag==0)).update(r_flag=1)
        
        
#         qsetS=db()
#         qsetS=qsetS((db.sm_doctor_visit.cid==cid) & (db.sm_doctor_visit.visit_date==visit_date) & (db.sm_doctor_visit.r_flag==''))
#         SRows=qsetS.select(db.sm_doctor_visit.cid,orderby=db.sm_doctor_visit.doc_id|db.sm_doctor_visit.route_id,groupby=db.sm_doctor_visit.doc_id|db.sm_doctor_visit.route_id,limitby=(0,10))
#         if not SRows:
#             db((db.doctor_due.cid==cid) & (db.doctor_due.status=='Due')).update(status='Done')   
        
        
        return "Success"



def docReportUpdate():
    cid= 'IBNSINA'   
    response.title='trDLoad'
    y_month=''
    DRows=db((db.sm_doctor_visit.cid==cid) &  (db.sm_doctor_visit.r_flag==1)  ).select(db.sm_doctor_visit.cid.count(),db.sm_doctor_visit.doc_id,db.sm_doctor_visit.visit_date,db.sm_doctor_visit.route_id,db.sm_doctor_visit.level1_id,db.sm_doctor_visit.level2_id,orderby=db.sm_doctor_visit.doc_id|db.sm_doctor_visit.route_id|db.sm_doctor_visit.visit_date,groupby=db.sm_doctor_visit.doc_id|db.sm_doctor_visit.route_id|db.sm_doctor_visit.visit_date,limitby=(0,10))
#     return DRows
    vCount=0
    for DRows in DRows:
        doc_id=str(DRows[db.sm_doctor_visit.doc_id])
        tr=str(DRows[db.sm_doctor_visit.route_id])
        visit_date=str(DRows[db.sm_doctor_visit.visit_date])
        visit_date_month=str(visit_date).split('-')[0]+'-'+str(visit_date).split('-')[1]
        y_month=str(visit_date_month)
        vCount=DRows[db.sm_doctor_visit.cid.count()]
        
        daF=int((visit_date).split('-')[2])
        dayInsert='d_'+str(daF)
        docStr_update="""update  sm_doc_visit_report  set """+dayInsert+"""='"""+str(vCount)+"""'  where cid ='"""+str(cid)+"""' and y_month='"""+str(y_month) +"""' and doc='"""+str(doc_id)+"""' and  tr='"""+str(tr)+ """'"""   
#         return docStr_update
        up_visit=db.executesql(docStr_update)
#         return 'Nadira'
        db((db.sm_doctor_visit.cid==cid) &  (db.sm_doctor_visit.r_flag==1)  & (db.sm_doctor_visit.visit_date==visit_date) & (db.sm_doctor_visit.doc_id==doc_id)  & (db.sm_doctor_visit.route_id==tr) ).update(r_flag=2)
#         return db._lastsql
    return 'Success'
    
    
    


def clReportInsert():
        cid= 'IBNSINA'   
        response.title='trDLoad'
        y_month=''
        order_date = ''
#        r_flag = 0
#         dueRows=db((db.doctor_due.cid==cid) & (db.doctor_due.status=='Due')).select(db.doctor_due.cid,db.doctor_due.rpt_date,db.doctor_due.status,orderby=db.doctor_due.rpt_date,limitby=(0,1))
#         if dueRows:
#             visit_date=str(dueRows[0].rpt_date)
#             visit_date_month=str(dueRows[0].rpt_date).split('-')[0]+'-'+str(dueRows[0].rpt_date).split('-')[1]
#             y_month=str(visit_date_month)
        
#        clReportInsert =  ''
        qset=db()
        qset=qset((db.sm_order_head.cid==cid)  & (db.sm_order_head.r_flag==0))
#        DoctorVisitRows=qset.select(db.sm_order_head.cid,db.sm_order_head.client_id,db.sm_order_head.client_name,db.sm_order_head.order_date,db.sm_order_head.area_id,db.sm_order_head.area_name,db.sm_order_head.level1_id,db.sm_order_head.level1_name,db.sm_order_head.level2_id,db.sm_order_head.level2_name,orderby=db.sm_order_head.client_id|db.sm_order_head.area_id,groupby=db.sm_order_head.client_id|db.sm_order_head.area_id,limitby=(0,10))
        DoctorVisitRows=qset.select(db.sm_order_head.cid,db.sm_order_head.client_id,db.sm_order_head.client_name,db.sm_order_head.order_date,db.sm_order_head.area_id,db.sm_order_head.area_name,db.sm_order_head.level1_id,db.sm_order_head.level1_name,db.sm_order_head.level2_id,db.sm_order_head.level2_name,db.sm_order_head.r_flag,orderby=db.sm_order_head.client_id|db.sm_order_head.area_id,groupby=db.sm_order_head.client_id|db.sm_order_head.area_id,limitby=(0,10))
#        return DoctorVisitRows
        for DoctorVisitRows in DoctorVisitRows:
            cid=DoctorVisitRows.cid
            client_id=DoctorVisitRows.client_id
            client_name=DoctorVisitRows.client_name    
            rsm_id=DoctorVisitRows.level1_id
            rsm_name=DoctorVisitRows.level1_name
            fm_id=DoctorVisitRows.level2_id
            fm_name=DoctorVisitRows.level2_name
            tr_id=DoctorVisitRows.area_id
            tr_name=DoctorVisitRows.area_name
 
            r_flag=DoctorVisitRows.r_flag
#            return r_flag
            order_date=DoctorVisitRows.order_date
#             return order_date
            order_date_month=str(order_date).split('-')[0]+'-'+str(order_date).split('-')[1]
            y_month=str(order_date_month)
#            return r_flag
            qsetD=db()
            qsetD=qsetD((db.sm_client_visit_report.cid==cid) & (db.sm_client_visit_report.y_month==y_month) & (db.sm_client_visit_report.tr==tr_id) & (db.sm_client_visit_report.client_id==client_id))
            DRows=qsetD.select(db.sm_client_visit_report.client_id,limitby=(0,1))
#            return DRows
            if DRows:
                pass
            else:
#                return r_flag
                insDoc=db.sm_client_visit_report.insert(cid=cid,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tr=tr_id,tr_name=tr_name,y_month=y_month,rpt_date=order_date,client_id=client_id,client_name=client_name)
#                return r_flag
            updater_flag=db((db.sm_order_head.cid==cid) & (db.sm_order_head.order_date==order_date) & (db.sm_order_head.client_id==client_id) & (db.sm_order_head.area_id==tr_id) & (db.sm_order_head.r_flag==0)).update(r_flag=1)
#                 return db._lastsql
        
#         qsetS=db()
#         qsetS=qsetS((db.sm_doctor_visit.cid==cid) & (db.sm_doctor_visit.visit_date==visit_date) & (db.sm_doctor_visit.r_flag==''))
#         SRows=qsetS.select(db.sm_doctor_visit.cid,orderby=db.sm_doctor_visit.doc_id|db.sm_doctor_visit.route_id,groupby=db.sm_doctor_visit.doc_id|db.sm_doctor_visit.route_id,limitby=(0,10))
#         if not SRows:
#             db((db.doctor_due.cid==cid) & (db.doctor_due.status=='Due')).update(status='Done')   
        
#        return db._lastsql
        return "Success"



def clReportUpdate():
    cid= 'IBNSINA'   
    response.title='trDLoad'
    y_month=''
    DRows=db((db.sm_order_head.cid==cid) &  (db.sm_order_head.r_flag==1)  ).select(db.sm_order_head.cid.count(),db.sm_order_head.client_id,db.sm_order_head.order_date,db.sm_order_head.area_id,db.sm_order_head.level1_id,db.sm_order_head.level2_id,orderby=db.sm_order_head.client_id|db.sm_order_head.area_id|db.sm_order_head.order_date,groupby=db.sm_order_head.client_id|db.sm_order_head.area_id|db.sm_order_head.order_date,limitby=(0,10))
#    return db._lastsql
    vCount=0
    for DRows in DRows:
        client_id=str(DRows[db.sm_order_head.client_id])
        tr=str(DRows[db.sm_order_head.area_id])
        order_date=str(DRows[db.sm_order_head.order_date])
        order_date_month=str(order_date).split('-')[0]+'-'+str(order_date).split('-')[1]
        y_month=str(order_date_month)
        vCount=DRows[db.sm_order_head.cid.count()]
        
#        return client_id
        daF=int((order_date).split('-')[2])
        dayInsert='d_'+str(daF)
        docStr_update="""update  sm_client_visit_report  set """+dayInsert+"""='"""+str(vCount)+"""'  where cid ='"""+str(cid)+"""' and y_month='"""+str(y_month) +"""' and client_id='"""+str(client_id)+"""' and  tr='"""+str(tr)+ """'"""   
#        return docStr_update
        up_visit=db.executesql(docStr_update)
#         return 'Nadira'
        db((db.sm_order_head.cid==cid) &  (db.sm_order_head.r_flag==1)  & (db.sm_order_head.order_date==order_date) & (db.sm_order_head.client_id==client_id)  & (db.sm_order_head.area_id==tr) ).update(r_flag=2)
#         return db._lastsql
    return 'Success'
    

# http://127.0.0.1:8000/demo/doctor_due_new/clReportAmountUpdate/?cid='IBNSINA'&datePass=2017-10-14
def clReportAmountUpdate():
    cid= str(request.vars.cid).strip().upper()
    datePass = str(request.vars.datePass).strip().upper()

    if datePass=='0':
        date_to=current_date
        date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
        datePass=date_to_m - datetime.timedelta(days = 1) 
    
    y_month=''
    A_get= str(datePass).split('-')[2]
    a_month=A_get= str(datePass).split('-')[1]
    if int(A_get)<10:
        A_get=A_get.replace('0','')
    A_get_final='a_'+A_get
    
    if int(a_month)<10 and len(a_month)<2:
        a_month='0'+a_month
    
    if int(A_get)<10 and len(A_get)<2:
        A_get='0'+A_get
    
    y_month=str(datePass).split('-')[0]+'-'+a_month
    report_date=y_month+'-'+A_get
#     return report_date
#     CRows=db((db.sm_client_visit_report.cid==cid) &  (db.sm_client_visit_report.y_month==y_month) & (db.sm_client_visit_report.A_get_final=='') ).select(db.sm_client_visit_report.client_id,db.sm_client_visit_report.tr,orderby=db.sm_client_visit_report.client_id|db.sm_client_visit_report.tr,groupby=db.sm_client_visit_report.client_id|db.sm_client_visit_report.tr,limitby=(0,10))
    
   

    CRowsS="""select  client_id,tr from sm_client_visit_report  where cid ="""+str(cid)+""" and y_month='"""+str(y_month) +"""' and """+A_get_final+"""=''  ORDER by client_id limit 10"""
#     return CRowsS
    CRows=db.executesql(CRowsS)   
    
    vAmount=0    
    for CRows in CRows:  
        client_id=str(CRows.client_id)
        tr=str(CRows.area_id)
        
        CRows=db((db.sm_order.cid==cid) &  (db.sm_order.client_id==client_id)  &  (db.sm_order.area_id==tr)  &  (db.sm_order.order_date==report_date)  ).select((db.sm_order.price*db.sm_order.quantity).sum(),limitby=(0,1))
        
        vAmount=CRows[(db.sm_order.price*db.sm_order.quantity).sum()]
        
        docStr_update="""update  sm_client_visit_report  set """+A_get_final+"""='"""+str(vCount)+"""'  where cid ='"""+str(cid)+"""' and y_month='"""+str(y_month) +"""' and client_id='"""+str(client_id)+"""' and  tr='"""+str(tr)+ """'"""
        return docStr_update
        up_visit=db.executesql(docStr_update)   
    return "Success"


