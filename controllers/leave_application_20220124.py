# http://127.0.0.1:8000/skf/leave_application/leave_application?cid=SKF&rep_id=IT03&rep_pass=123

import math
import os
import calendar
import urllib2

def leave_application():           
    search_form =SQLFORM(db.sm_search_date)
    
    cid = str(request.vars.cid).strip().upper()
    rep_id=str(request.vars.rep_id).strip().upper()
    password=str(request.vars.rep_pass).strip()

    return dict(search_form=search_form,cid=cid,rep_id=rep_id,password=password)



def leave_application_submit():           
    
    search_form =SQLFORM(db.sm_search_date)
    cid = str(request.vars.cid).strip().upper()
    rep_id=str(request.vars.rep_id).strip().upper()    
    password=str(request.vars.password).strip()
    btn_leave_application=request.vars.btn_leave_application

    l_fromDate=request.vars.from_dt_2


    l_toDate=request.vars.to_dt_2
   
    emp_name=''
    checkRep=  db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id)  & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.password,limitby=(0, 1))

    if checkRep: 
        emp_name=checkRep[0].name

        
    else:
        response.flash='Invalid Authorization.'
    
    if (btn_leave_application):
             
            leaveDayVal=request.vars.leaveDayVal
            leave_type=request.vars.leave_type                        
            
            if ((str(l_fromDate)=='') & (str(l_fromDate)=='')) :
                session.flash='Please select Date'
            else:

                try:
                    db.sm_leave_application.insert(cid=cid,from_date=l_fromDate,to_date=l_toDate,emp_id=rep_id,emp_name=emp_name,total_leave=leaveDayVal,leave_type=leave_type)  
                    session.flash='Submitted Successfully.'                
                except:
                    session.flash='Process Error'

    else:
        session.flash='Please select Date'        
    
    redirect(URL(c='leave_application',f='leave_application'))




# http://127.0.0.1:8000/skf/leave_application/approveList?cid=SKF&rep_id=ITFM&rep_pass=123

def approveList():
    response.title = 'Approve List'

    cid = request.vars.cid
    session.cid = cid
    uid = request.vars.rep_id
    session.uid = uid    
    password = request.vars.rep_pass
    session.password = password    
    
    check_Rows=db((db.sm_rep.cid==cid) & (db.sm_rep.rep_id==uid)  & (db.sm_rep.password==password)  & (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.user_type,limitby=(0,1))

    if check_Rows:
        rep_id=check_Rows[0].rep_id
        name=check_Rows[0].name
        user_type=check_Rows[0].user_type        
        session.user_id = rep_id
        session.user_name = name
        session.user_type = user_type
    
    else :
        session.flash='Access is Denied !'
    
    if session.user_type == 'rep' :
        leave_req=''

        return dict(leave_req = leave_req)
    
    else:
        level_idList=[]
        depthList=[]        
        levelList=[]
        areaList = []
        supList = []
        repList = []
        session.msg_1 = ''
        session.msg = ''
        supLevelRows=db((db.sm_supervisor_level.cid==cid) & (db.sm_supervisor_level.sup_id==uid)).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no)        
        
        for supRow in supLevelRows:
            level_id=supRow.level_id
            depthNo=supRow.level_depth_no

            session.depthNo_user=depthNo 
            level_idList.append(level_id) 
            
            level = 'level' + str(depthNo) 
        
        
        levelRows = db((db.sm_level.cid == cid) & (db.sm_level.parent_level_id.belongs(level_idList) )).select(db.sm_level.level_id, orderby=db.sm_level.level_id) 
        for levelRow in levelRows:
            territoryid = levelRow.level_id
            areaList.append(territoryid) 
        leave_req=''    
        app_req=''
        
        if session.depthNo_user != 2:                        
            sup_Rows = db((db.sm_supervisor_level.cid == cid)  &  (db.sm_supervisor_level.level_id.belongs(areaList) )).select(db.sm_supervisor_level.sup_id, db.sm_supervisor_level.sup_name,db.sm_supervisor_level.level_depth_no, orderby=db.sm_supervisor_level.sup_id)                        
            
            for sup_Row in sup_Rows:
                supId = sup_Row.sup_id
                supList.append(supId)
            
            # =========Leave Request=========

            if session.depthNo_user == 0  :     
                leave_req = db((db.sm_leave_application.cid == cid)  &  (db.sm_leave_application.emp_id.belongs(supList)) &  (db.sm_leave_application.divisional_head_status=='' )  ).select(db.sm_leave_application.emp_id, db.sm_leave_application.emp_name, orderby=db.sm_leave_application.emp_id)                                                
                # return db._lastsql
                if not leave_req:
                    session.msg_1 = 'No Leave Request!' 


            if session.depthNo_user == 1  :     
                leave_req = db((db.sm_leave_application.cid == cid)  &  (db.sm_leave_application.emp_id.belongs(supList))  &  (db.sm_leave_application.zonal_head_status =='' )  ).select(db.sm_leave_application.emp_id, db.sm_leave_application.emp_name, orderby=db.sm_leave_application.emp_id)                                                
                if not leave_req:
                    session.msg_1 = 'No Leave Request!'           

              
            
            

            # =========Approve=========
            
            if session.depthNo_user == 0  :    
                
                app_req = db((db.sm_leave_application.cid == cid)  &  (db.sm_leave_application.zonal_head_id.belongs(supList)) &  (db.sm_leave_application.divisional_head_status=='')  &  (db.sm_leave_application.zonal_head_status=='Approved')   ).select(db.sm_leave_application.emp_id, db.sm_leave_application.emp_name, orderby=db.sm_leave_application.emp_id)                                                            
                
                if not app_req:
                    session.msg_1 = 'Nothing pending for approval.'


            if session.depthNo_user == 1  :    
                app_req = db((db.sm_leave_application.cid == cid)  &  (db.sm_leave_application.ared_head_id.belongs(supList))  &  (db.sm_leave_application.zonal_head_status=='') &  (db.sm_leave_application.area_head_status=='Approved') ).select(db.sm_leave_application.emp_id, db.sm_leave_application.emp_name, orderby=db.sm_leave_application.emp_id)                                                            
                # return db._lastsql
                if not app_req:
                    session.msg = 'Nothing pending for approval.'    


        
        else:    
            rep_Rows = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.area_id.belongs(areaList) )).select(db.sm_rep_area.rep_id, db.sm_rep_area.rep_name, db.sm_rep_area.area_id, orderby=db.sm_rep_area.area_id)
            
            for rep_Row in rep_Rows:
                repId = rep_Row.rep_id
                repList.append(repId)

            leave_req = db((db.sm_leave_application.cid == cid)  &  (db.sm_leave_application.emp_id.belongs(repList))  & (db.sm_leave_application.area_head_status == '')  ).select(db.sm_leave_application.emp_id, db.sm_leave_application.emp_name, orderby=db.sm_leave_application.emp_id)                                    
            # return db._lastsql
            if not leave_req:
                session.msg_1 = 'Nothing pending for approval.'  
        # return depthNo
        return dict(leave_req = leave_req,app_req=app_req,depthNo=depthNo)


def leave_application_approval():               
    
    cid = str(request.vars.cid).strip().upper()
    uid= str(request.vars.uid)
    u_name= str(request.vars.u_name)
    u_pass= str(request.vars.u_pass)
    
    rep_id = str(request.vars.memId_1)
    rep_name = str(request.vars.memName_1)
    emp_id=''
    emp_name=''
    from_date=''
    to_date=''
    total_leave=''
    leave_type=''
    ared_head_id=''
    ared_head_name=''
    
    depthNo=''
    supLevelRows=db((db.sm_supervisor_level.cid==cid) & (db.sm_supervisor_level.sup_id==rep_id)).select(db.sm_supervisor_level.level_depth_no,limitby=(0,1))                
    if supLevelRows:
        depthNo=supLevelRows[0].level_depth_no


    recordRows = db((db.sm_leave_application.cid == cid)  &  (db.sm_leave_application.emp_id==rep_id )).select(db.sm_leave_application.ALL, orderby=db.sm_leave_application.emp_id)
    # return recordRows
    for recordRow in recordRows:
        emp_id = recordRow.emp_id
        emp_name = recordRow.emp_name
        from_date = recordRow.from_date
        to_date = recordRow.to_date
        total_leave = recordRow.total_leave
        leave_type = recordRow.leave_type

        ared_head_id = recordRow.ared_head_id
        ared_head_name = recordRow.ared_head_name
        # return ared_head_id
   
    return dict(depthNo=depthNo,cid=cid,uid=uid,u_name=u_name,ared_head_id=ared_head_id,ared_head_name=ared_head_name,u_pass=u_pass,rep_id=rep_id,rep_name=rep_name,emp_id=emp_id,emp_name=emp_name,from_date=from_date,to_date=to_date,total_leave=total_leave,leave_type=leave_type)


def leave_application_approval_p():               
    
    cid = str(request.vars.cid).strip().upper()
    uid= str(request.vars.uid)
    u_name= str(request.vars.u_name)
    u_pass= str(request.vars.u_pass)

    rep_id = str(request.vars.memId_r)
    rep_name = str(request.vars.memName_r)
    emp_id=''
    emp_name=''
    from_date=''
    to_date=''
    total_leave=''
    leave_type=''
    ared_head_id=''
    ared_head_name=''
    zonal_head_id=''
    zonal_head_name=''
    depthNo=''
    supLevelRows=db((db.sm_supervisor_level.cid==cid) & (db.sm_supervisor_level.sup_id==rep_id)).select(db.sm_supervisor_level.level_depth_no,limitby=(0,1))        
 
    if supLevelRows:
        depthNo=supLevelRows[0].level_depth_no


    recordRows = db((db.sm_leave_application.cid == cid)  &  (db.sm_leave_application.emp_id==rep_id )).select(db.sm_leave_application.ALL, orderby=db.sm_leave_application.emp_id)
    # return recordRossws
    for recordRow in recordRows:
        emp_id = recordRow.emp_id
        emp_name = recordRow.emp_name
        from_date = recordRow.from_date
        to_date = recordRow.to_date
        total_leave = recordRow.total_leave
        leave_type = recordRow.leave_type

        ared_head_id = recordRow.ared_head_id
        ared_head_name = recordRow.ared_head_name

        zonal_head_id = recordRow.zonal_head_id
        zonal_head_name = recordRow.zonal_head_name
      
    return dict(zonal_head_id=zonal_head_id,zonal_head_name=zonal_head_name,depthNo=depthNo,cid=cid,uid=uid,u_name=u_name,ared_head_id=ared_head_id,ared_head_name=ared_head_name,u_pass=u_pass,rep_id=rep_id,rep_name=rep_name,emp_id=emp_id,emp_name=emp_name,from_date=from_date,to_date=to_date,total_leave=total_leave,leave_type=leave_type)


def leave_application_confirm():              
    
    cid = str(request.vars.cid).strip().upper()    
    uid=str(request.vars.uid).strip().upper()
    u_pass=str(request.vars.u_pass).strip().upper()
    depth=str(request.vars.depth).strip().upper()
   
    rep_id=str(request.vars.rep_id).strip().upper()
    rep_name=str(request.vars.rep_name).strip().upper()
    
    btn_approve_application=request.vars.btn_approve_application
    btn_reject_application=request.vars.btn_reject_application
    
    checkRep=  db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == uid) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.password,limitby=(0, 1))
    # return checkRep
    if checkRep: 
        u_name=checkRep[0].name
        
        if btn_approve_application:            
            
            if depth== '2'  :                
                
                statusConfirm = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == rep_id)).update(ared_head_id=uid,ared_head_name=u_name,area_head_status='Approved')            
                session.flash='Approved Successfully.'          
    
            if depth== '1'  :                
                statusConfirm = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == rep_id)).update(zonal_head_id=uid,zonal_head_name=u_name,zonal_head_status='Approved')            
                session.flash='Approved Successfully.' 

            if depth== '0' :                
                statusConfirm = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == rep_id)).update(divisional_head_id=uid,divisional_head_name=u_name,divisional_head_status='Approved')            
                session.flash='Approved Successfully.'


        if btn_reject_application:            
            statusConfirm = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == rep_id)).update(ared_head_id=uid,ared_head_name=u_name,area_head_status='Rejected')              
            session.flash='Rejected Successfully.'

    else:
        session.flash='Invalid Authorization.'         
        
    redirect(URL(c='leave_application',f='leave_application_approval'))


# def leave_application_confirm():              
    
#     cid = str(request.vars.cid).strip().upper()    
#     uid=str(request.vars.uid).strip().upper()
#     u_pass=str(request.vars.u_pass).strip().upper()
#     depth=str(request.vars.depth).strip().upper()
   
#     rep_id=str(request.vars.rep_id).strip().upper()
#     rep_name=str(request.vars.rep_name).strip().upper()
    
#     btn_approve_application=request.vars.btn_approve_application
#     btn_reject_application=request.vars.btn_reject_application
    
#     checkRep=  db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == uid) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.password,limitby=(0, 1))
#     # return checkRep
#     if checkRep: 
#         u_name=checkRep[0].name
        
#         if btn_approve_application:            
            
#             if depth== '2'  :                
                
#                 statusConfirm = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == rep_id)).update(ared_head_id=uid,ared_head_name=u_name,area_head_status='Approved')            
#                 session.flash='Approved Successfully.'          
    
#             if depth== '1'  :                
#                 statusConfirm = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == rep_id)).update(zonal_head_id=uid,zonal_head_name=u_name,zonal_head_status='Approved')            
#                 session.flash='Approved Successfully.' 

#             if depth== '0' :                
#                 statusConfirm = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == rep_id)).update(divisional_head_id=uid,divisional_head_name=u_name,divisional_head_status='Approved')            
#                 session.flash='Approved Successfully.'


#         if btn_reject_application:            
#             statusConfirm = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == rep_id)).update(ared_head_id=uid,ared_head_name=u_name,area_head_status='Rejected')              
#             session.flash='Rejected Successfully.'

#     else:
#         session.flash='Invalid Authorization.'         
        
#     redirect(URL(c='leave_application',f='leave_application_confirm'))



# http://127.0.0.1:8000/skf/leave_application/director_approveList?cid=SKF&director_id=1101

def director_approveList():              
    
    cid = str(request.vars.cid).strip().upper()    
    director_id=str(request.vars.director_id).strip().upper()
    session.msg_1 = ''
    checkRep=  db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'sales_director') & (db.sm_settings.s_value == director_id) ).select(db.sm_settings.s_value, limitby=(0, 1))
   
    if checkRep: 
        leave_req = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.divisional_head_status == 'Approved') & (db.sm_leave_application.director_marktng_status == '')  ).select(db.sm_leave_application.emp_id, db.sm_leave_application.emp_name, orderby=db.sm_leave_application.emp_id)                                    
        # return leave_req

        if not leave_req:
            session.msg_1 = 'Nothing pending for approval.' 
    else :
        session.flash='Access is Denied !'        
        
    return dict(leave_req=leave_req,director_id=director_id)


def leave_application_approval_d():               
    
    cid = str(request.vars.cid).strip().upper()
    uid= str(request.vars.memId_1)
    u_name= str(request.vars.memName_1)
    u_pass= str(request.vars.u_pass)
    director_id= str(request.vars.director_id)
    
    emp_id=''
    emp_name=''
    from_date=''
    to_date=''
    total_leave=''
    leave_type=''
    ared_head_id=''
    ared_head_name=''
    zonal_head_id=''
    zonal_head_name=''
    depthNo=''
    

    recordRows = db((db.sm_leave_application.cid == cid)  &  (db.sm_leave_application.emp_id==uid)  &  (db.sm_leave_application.divisional_head_status=='Approved') ).select(db.sm_leave_application.ALL, orderby=db.sm_leave_application.emp_id)
    # return recordRows
    for recordRow in recordRows:
        emp_id = recordRow.emp_id
        emp_name = recordRow.emp_name
        from_date = recordRow.from_date
        to_date = recordRow.to_date
        total_leave = recordRow.total_leave
        leave_type = recordRow.leave_type

        ared_head_id = recordRow.ared_head_id
        ared_head_name = recordRow.ared_head_name

        zonal_head_id = recordRow.zonal_head_id
        zonal_head_name = recordRow.zonal_head_name
      
    return dict(director_id=director_id,zonal_head_id=zonal_head_id,zonal_head_name=zonal_head_name,depthNo=depthNo,cid=cid,uid=uid,u_name=u_name,ared_head_id=ared_head_id,ared_head_name=ared_head_name,u_pass=u_pass,emp_id=emp_id,emp_name=emp_name,from_date=from_date,to_date=to_date,total_leave=total_leave,leave_type=leave_type)



def leave_application_dConfirm():              

    cid = str(request.vars.cid).strip().upper()    
    director_id=str(request.vars.director_id).strip().upper()
    # return director_id
    u_pass=str(request.vars.u_pass).strip().upper()
    
    emp_id=str(request.vars.emp_id).strip().upper()
    emp_name=str(request.vars.emp_name).strip().upper()
    
    btn_approve_application=request.vars.btn_approve_application
    btn_reject_application=request.vars.btn_reject_application
    
    checkRep=  db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'sales_director') & (db.sm_settings.s_value == director_id) ).select(db.sm_settings.s_value, limitby=(0, 1))
   
    if checkRep: 

        if btn_approve_application:            
            
            statusConfirm = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == emp_id) & (db.sm_leave_application.director_marktng_status == '')).update(director_id=director_id,director_marktng_status='Approved')            
            # return statusConfirm
            session.flash='Approved Successfully.'
            redirect(URL(c='leave_application',f='leave_application_mail',vars=dict(cid=cid,emp_id=emp_id,emp_name=emp_name,director_id=director_id)))

        if btn_reject_application:            
            statusConfirm = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == emp_id)).update(director_id=director_id,director_marktng_status='Rejected')              
            session.flash='Rejected Successfully.'
            redirect(URL(c='leave_application',f='leave_application_approval_d'))
    else:
        session.flash='Invalid Authorization.'         
        

def leave_application_mail():              
    
    cid = str(request.vars.cid).strip().upper()    
    director_id=str(request.vars.director_id).strip().upper()
    emp_id=str(request.vars.emp_id).strip().upper()
    emp_name=''
    from_date=''
    to_date=''
    total_leave=''
    leave_type=''
    ared_head_id=''
    ared_head_name=''
    area_head_status=''
    zonal_head_id=''
    zonal_head_name=''
    zonal_head_status=''
    divisional_head_id=''
    divisional_head_name=''
    divisional_head_status=''
    director_id=''
    director_name=''
    director_marktng_status=''

    checkRow=  db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == emp_id)  & (db.sm_leave_application.director_marktng_status == 'Approved') ).select(db.sm_leave_application.ALL, limitby=(0, 1))
    # return checkRow
    if checkRow: 
        emp_id=checkRow[0].emp_id
        emp_name=checkRow[0].emp_name
        from_date=checkRow[0].from_date 
        to_date=checkRow[0].to_date        
        total_leave=checkRow[0].total_leave
        leave_type=checkRow[0].leave_type 
        ared_head_id=checkRow[0].ared_head_id
        ared_head_name=checkRow[0].ared_head_name
        area_head_status=checkRow[0].area_head_status
        zonal_head_id=checkRow[0].zonal_head_id
        zonal_head_name=checkRow[0].zonal_head_name
        zonal_head_status=checkRow[0].zonal_head_status 
        divisional_head_id=checkRow[0].divisional_head_id
        
        divisional_head_name=checkRow[0].divisional_head_name
        divisional_head_status=checkRow[0].divisional_head_status 
        director_id=checkRow[0].director_id
        director_name=checkRow[0].director_name
        director_marktng_status=checkRow[0].director_marktng_status 



    else :
        session.flash='Access is Denied !'        
        
    return dict(emp_id=emp_id,emp_name=emp_name,from_date=from_date,to_date=to_date,total_leave=total_leave,leave_type=leave_type,ared_head_id=ared_head_id,ared_head_name=ared_head_name,area_head_status=area_head_status,zonal_head_id=zonal_head_id,zonal_head_name=zonal_head_name,zonal_head_status=zonal_head_status,divisional_head_id=divisional_head_id,divisional_head_name=divisional_head_name,divisional_head_status=divisional_head_status,director_id=director_id,director_name=director_name,director_marktng_status=director_marktng_status)