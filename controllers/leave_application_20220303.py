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

    leave_type=  db((db.sm_leave_type.cid == cid)).select(db.sm_leave_type.ALL, groupby=db.sm_leave_type.leave_type)    
    
    # return leave_type    

    return dict(search_form=search_form,cid=cid,rep_id=rep_id,password=password,leave_type=leave_type)



def leave_application_submit():           
    
    search_form =SQLFORM(db.sm_search_date)
    cid = str(request.vars.cid).strip().upper()
    rep_id=str(request.vars.rep_id).strip().upper()    
    password=str(request.vars.password).strip()

    l_fromDate=request.vars.from_dt_2
    l_toDate=request.vars.to_dt_2
    leaveDayVal=request.vars.leaveDayVal
    leave_type=request.vars.leave_type
    leave_cause=request.vars.leave_cause
    
    btn_leave_application=request.vars.btn_leave_application
    
    # currentMonth=first_currentDate
    
    # checkLtype=  db((db.sm_leave_type.cid == cid) & (db.sm_leave_type.leave_type == leave_type)).select(db.sm_leave_type.total_leave,limitby=(0, 1))
    # if checkLtype:
    #     total_leave=checkLtype[0].total_leave

    
    # checkLeave=  db((db.sm_leave_application.cid == cid) & (db.sm_leave_application.emp_id == rep_id)  & (db.sm_leave_application.leave_type == leave_type) & (db.sm_leave_application.first_date == currentMonth) ).select(db.sm_leave_application.ALL, orderby=db.sm_leave_application.emp_id)
    # if checkLeave:
    #     checkLeave=checkLeave[0].total_leave
    

    # available_leave=total_leave-checkLeave
    # return available_leave

    emp_name=''
    checkRep=  db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id)  & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.password,limitby=(0, 1))

    if checkRep: 
        emp_name=checkRep[0].name       
    else:
        response.flash='Invalid Authorization.'
    
    if (btn_leave_application) :
             
                                    
            # return leave_cause
            
            if ((str(l_fromDate)!='') & (str(l_toDate)!='') & (str(leave_type)!='')):
                try:
                    db.sm_leave_application.insert(cid=cid,from_date=l_fromDate,to_date=l_toDate,emp_id=rep_id,emp_name=emp_name,total_leave=leaveDayVal,leave_type=leave_type,note=leave_cause)  
                    session.flash='Submitted Successfully.'                
                except:
                    session.flash='Process Error'
                
            else:
                session.flash='Please select Date & Leave type'

    else:
        session.flash='Please select Date & Leave type'        
    
    redirect(URL(c='leave_application',f='leave_application'))
    # return dict (available_leave=available_leave)

def get_available_leave():
    retStr = ''
    leave_type=request.vars.leaveType_id
    rep_id=str(request.vars.repId).strip().upper()
    c_id=str(request.vars.cId).strip().upper() 
    
    currentMonth=first_currentDate
    
    totalLeave=''
    checkLtype=  db((db.sm_leave_type.cid == c_id) & (db.sm_leave_type.leave_type == leave_type)).select(db.sm_leave_type.ALL,limitby=(0, 1))    
    
    if checkLtype:
        totalLeave=checkLtype[0].total_leave
        
    
    checkLeave=  db ((db.sm_leave_application.cid == c_id) & (db.sm_leave_application.leave_type == leave_type)  & (db.sm_leave_application.emp_id == rep_id) ).select((db.sm_leave_application.total_leave).sum(), groupby=db.sm_leave_application.emp_id)    
    for record in checkLeave:
        checkLeave=int(record[(db.sm_leave_application.total_leave).sum()])  
    
           
    if int(totalLeave)==0:
        available_leave='-'

    else:
        available_leave=(int(totalLeave)-int(checkLeave))

        if available_leave==0:
            available_leave='-' 
        else:
            pass
    
    if retStr == '':
        retStr = available_leave
    else:
        retStr += ',' + available_leave

    
    return retStr

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
                leave_req = db((db.sm_leave_application.cid == cid)  &  (db.sm_leave_application.emp_id.belongs(supList)) &  (db.sm_leave_application.divisional_head_status=='' )  ).select(db.sm_leave_application.emp_id, db.sm_leave_application.emp_name, db.sm_leave_application.from_date,db.sm_leave_application.to_date,db.sm_leave_application.total_leave, db.sm_leave_application.leave_type, db.sm_leave_application.id, orderby=db.sm_leave_application.emp_id|db.sm_leave_application.created_on)                                                
                # return db._lastsql
                if not leave_req:
                    session.msg_1 = 'No Leave Request!' 


            if session.depthNo_user == 1  :     
                leave_req = db((db.sm_leave_application.cid == cid)  &  (db.sm_leave_application.emp_id.belongs(supList))  &  (db.sm_leave_application.zonal_head_status =='' )  ).select(db.sm_leave_application.emp_id, db.sm_leave_application.emp_name, db.sm_leave_application.from_date,db.sm_leave_application.to_date,db.sm_leave_application.total_leave, db.sm_leave_application.leave_type,db.sm_leave_application.id ,  orderby=db.sm_leave_application.emp_id|db.sm_leave_application.created_on)                                                
                if not leave_req:
                    session.msg_1 = 'No Leave Request!'           

              
            
            

            # =========Approve=========
            
            if session.depthNo_user == 0  :    
                
                app_req = db((db.sm_leave_application.cid == cid)  &  (db.sm_leave_application.zonal_head_id.belongs(supList)) &  (db.sm_leave_application.divisional_head_status=='')  &  (db.sm_leave_application.zonal_head_status=='Approved')   ).select(db.sm_leave_application.emp_id, db.sm_leave_application.emp_name, db.sm_leave_application.from_date,db.sm_leave_application.to_date,db.sm_leave_application.total_leave, db.sm_leave_application.leave_type, db.sm_leave_application.id,  orderby=db.sm_leave_application.emp_id|db.sm_leave_application.created_on)                                                            
                
                if not app_req:
                    session.msg_1 = 'Nothing pending for approval.'


            if session.depthNo_user == 1  :    
                app_req = db((db.sm_leave_application.cid == cid)  &  (db.sm_leave_application.ared_head_id.belongs(supList))  &  (db.sm_leave_application.zonal_head_status=='') &  (db.sm_leave_application.area_head_status=='Approved') ).select(db.sm_leave_application.emp_id, db.sm_leave_application.emp_name, db.sm_leave_application.from_date,db.sm_leave_application.to_date,db.sm_leave_application.total_leave, db.sm_leave_application.leave_type, db.sm_leave_application.id,  orderby=db.sm_leave_application.emp_id|db.sm_leave_application.created_on)                                                            
                # return db._lastsql
                if not app_req:
                    session.msg = 'Nothing pending for approval.'    


        
        else:    
            rep_Rows = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.area_id.belongs(areaList) )).select(db.sm_rep_area.rep_id, db.sm_rep_area.rep_name, db.sm_rep_area.area_id, orderby=db.sm_rep_area.area_id)
            
            for rep_Row in rep_Rows:
                repId = rep_Row.rep_id
                repList.append(repId)

            leave_req = db((db.sm_leave_application.cid == cid)  &  (db.sm_leave_application.emp_id.belongs(repList))  & (db.sm_leave_application.area_head_status == '')  ).select(db.sm_leave_application.emp_id, db.sm_leave_application.emp_name, db.sm_leave_application.from_date,db.sm_leave_application.to_date,db.sm_leave_application.total_leave, db.sm_leave_application.leave_type, db.sm_leave_application.id,  orderby=db.sm_leave_application.emp_id|db.sm_leave_application.created_on)                                    
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
    memId_1_id=str(request.vars.memId_1_id)

    
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


    recordRows = db((db.sm_leave_application.cid == cid)  &  (db.sm_leave_application.emp_id==rep_id ) &  (db.sm_leave_application.id==memId_1_id )).select(db.sm_leave_application.ALL, orderby=db.sm_leave_application.emp_id)
    # return recordRows
    for recordRow in recordRows:
        record_id = recordRow.id
        emp_id = recordRow.emp_id
        emp_name = recordRow.emp_name
        from_date = recordRow.from_date
        to_date = recordRow.to_date
        total_leave = recordRow.total_leave
        leave_type = recordRow.leave_type

        ared_head_id = recordRow.ared_head_id
        ared_head_name = recordRow.ared_head_name
        leave_req_reason = recordRow.note
        
   
    return dict(depthNo=depthNo,cid=cid,uid=uid,u_name=u_name,ared_head_id=ared_head_id,ared_head_name=ared_head_name,u_pass=u_pass,rep_id=rep_id,rep_name=rep_name,emp_id=emp_id,emp_name=emp_name,from_date=from_date,to_date=to_date,total_leave=total_leave,leave_type=leave_type,record_id=record_id,leave_req_reason=leave_req_reason)

def leave_application_confirm():              
    
    cid = str(request.vars.cid).strip().upper()    
    uid=str(request.vars.uid).strip().upper()
    u_pass=str(request.vars.u_pass).strip().upper()
    depth=str(request.vars.depth).strip().upper()
   
    memId_1=str(request.vars.rep_id).strip().upper()
    memName_1=str(request.vars.rep_name).strip().upper()
    memId_1_id=str(request.vars.record_id).strip()
    

    from_dt_2=str(request.vars.from_dt_2).strip().upper()
    to_dt_2=str(request.vars.to_dt_2).strip().upper()
    total_leave=str(request.vars.leaveDayVal).strip().upper()

    
    btn_approve_application=request.vars.btn_approve_application
    btn_reject_application=request.vars.btn_reject_application
    
    checkRep=  db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == uid) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.password,limitby=(0, 1))
    # return checkRep
    if checkRep: 
        u_name=checkRep[0].name
        
        if btn_approve_application:            
                        
            if depth== '2'  :  
                
                statusConfirm = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == memId_1) & (db.sm_leave_application.id == memId_1_id)).update(from_date=from_dt_2,to_date=to_dt_2,total_leave=total_leave,ared_head_id=uid,ared_head_name=u_name,area_head_status='Approved')            
                 
                session.flash='Approved Successfully.'    
                
            if depth== '1'  :                    
                statusConfirm = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == memId_1) & (db.sm_leave_application.id == memId_1_id)).update(from_date=from_dt_2,to_date=to_dt_2,total_leave=total_leave,zonal_head_id=uid,zonal_head_name=u_name,zonal_head_status='Approved')            
                session.flash='Approved Successfully.' 
                                   

            if depth== '0' :                
                statusConfirm = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == memId_1) & (db.sm_leave_application.id == memId_1_id)).update(from_date=from_dt_2,to_date=to_dt_2,total_leave=total_leave,divisional_head_id=uid,divisional_head_name=u_name,divisional_head_status='Approved')            
                session.flash='Approved Successfully.'


        if btn_reject_application:            
            if depth== '2'  :  
                
                statusConfirm = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == memId_1) & (db.sm_leave_application.id == memId_1_id)).update(from_date=from_dt_2,to_date=to_dt_2,total_leave=total_leave,ared_head_id=uid,ared_head_name=u_name,area_head_status='Rejected')                             
                session.flash='Rejected Successfully.'    
                
            if depth== '1'  :                    
                statusConfirm = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == memId_1) & (db.sm_leave_application.id == memId_1_id)).update(from_date=from_dt_2,to_date=to_dt_2,total_leave=total_leave,zonal_head_id=uid,zonal_head_name=u_name,zonal_head_status='Rejected')            
                session.flash='Rejected Successfully.' 
                                   

            if depth== '0' :                
                statusConfirm = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == memId_1) & (db.sm_leave_application.id == memId_1_id)).update(from_date=from_dt_2,to_date=to_dt_2,total_leave=total_leave,divisional_head_id=uid,divisional_head_name=u_name,divisional_head_status='Rejected')            
                session.flash='Rejected Successfully.'

    else:
        session.flash='Invalid Authorization.'   

    # return 'g'
        
    redirect(URL(c='leave_application',f='leave_application_approval',vars=dict(cid=cid,memId_1=memId_1,memId_1_id=memId_1_id,memName_1=memName_1,u_name=u_name,u_pass=u_pass,uid=uid)))

def leave_application_approval_p():               
    
    cid = str(request.vars.cid).strip().upper()
    uid= str(request.vars.uid)
    u_name= str(request.vars.u_name)
    u_pass= str(request.vars.u_pass)

    rep_id = str(request.vars.memId_r)
    rep_name = str(request.vars.memName_r)
    memId_r_id = str(request.vars.memId_r_id)
    # return memId_r_id
    
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


    recordRows = db((db.sm_leave_application.cid == cid)  &  (db.sm_leave_application.emp_id==rep_id ) &  (db.sm_leave_application.id==memId_r_id )).select(db.sm_leave_application.ALL, orderby=db.sm_leave_application.emp_id)
    # return recordRows
    for recordRow in recordRows:
        record_id = recordRow.id
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
        leave_req_reason = recordRow.note

    return dict(zonal_head_id=zonal_head_id,zonal_head_name=zonal_head_name,depthNo=depthNo,cid=cid,uid=uid,u_name=u_name,ared_head_id=ared_head_id,ared_head_name=ared_head_name,u_pass=u_pass,rep_id=rep_id,rep_name=rep_name,emp_id=emp_id,emp_name=emp_name,from_date=from_date,to_date=to_date,total_leave=total_leave,leave_type=leave_type,record_id=record_id,leave_req_reason=leave_req_reason)




def leave_application_confirm_p():              
    
    cid = str(request.vars.cid).strip().upper()    
    uid=str(request.vars.uid).strip().upper()
    u_pass=str(request.vars.u_pass).strip().upper()
    depth=str(request.vars.depth).strip().upper()
   
    memId_r=str(request.vars.rep_id).strip().upper()
    memName_r=str(request.vars.rep_name).strip().upper()
    memId_r_id=str(request.vars.record_id).strip()
    
    from_dt_2=str(request.vars.from_dt_2).strip().upper()
    to_dt_2=str(request.vars.to_dt_2).strip().upper()
    total_leave=str(request.vars.leaveDayVal).strip().upper()
    
    
    btn_approve_application=request.vars.btn_approve_application
    btn_reject_application=request.vars.btn_reject_application
    
    checkRep=  db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == uid) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.password,limitby=(0, 1))
    
    # return checkRep
    if checkRep: 
        u_name=checkRep[0].name
        
        if btn_approve_application:            
            
            if depth== '2'  :  
                
                statusConfirm = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == memId_r) & (db.sm_leave_application.id == memId_r_id)).update(from_date=from_dt_2,to_date=to_dt_2,total_leave=total_leave,ared_head_id=uid,ared_head_name=u_name,area_head_status='Approved')                             
                session.flash='Approved Successfully.'    
                
            if depth== '1'  :                     
                statusConfirm = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == memId_r) & (db.sm_leave_application.id == memId_r_id)).update(from_date=from_dt_2,to_date=to_dt_2,total_leave=total_leave,zonal_head_id=uid,zonal_head_name=u_name,zonal_head_status='Approved')            
                session.flash='Approved Successfully.' 
                   
                
            if depth== '0' :                
                statusConfirm = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == memId_r) & (db.sm_leave_application.id == memId_r_id)).update(from_date=from_dt_2,to_date=to_dt_2,total_leave=total_leave,divisional_head_id=uid,divisional_head_name=u_name,divisional_head_status='Approved')            
                session.flash='Approved Successfully.'


        if btn_reject_application:            
            
            if depth== '2'  :  
                
                statusConfirm = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == memId_r) & (db.sm_leave_application.id == memId_r_id)).update(from_date=from_dt_2,to_date=to_dt_2,total_leave=total_leave,ared_head_id=uid,ared_head_name=u_name,area_head_status='Rejected')                             
                session.flash='Rejected Successfully.'    
                
            if depth== '1'  :                     
                statusConfirm = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == memId_r) & (db.sm_leave_application.id == memId_r_id)).update(from_date=from_dt_2,to_date=to_dt_2,total_leave=total_leave,zonal_head_id=uid,zonal_head_name=u_name,zonal_head_status='Rejected')            
                session.flash='Rejected Successfully.' 
                   
                
            if depth== '0' :                
                statusConfirm = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == memId_r) & (db.sm_leave_application.id == memId_r_id)).update(from_date=from_dt_2,to_date=to_dt_2,total_leave=total_leave,divisional_head_id=uid,divisional_head_name=u_name,divisional_head_status='Rejected')            
                session.flash='Rejected Successfully.'


            # statusConfirm = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == memId_r) & (db.sm_leave_application.id == memId_r_id)).update(from_date=from_dt_2,to_date=to_dt_2,total_leave=total_leave,ared_head_id=uid,ared_head_name=u_name,area_head_status='Rejected')              
            # session.flash='Rejected Successfully.'

    else:
        session.flash='Invalid Authorization.'   

    # return 'g'
        
    redirect(URL(c='leave_application',f='leave_application_approval_p',vars=dict(cid=cid,memId_r=memId_r,memId_r_id=memId_r_id,memName_r=memName_r,u_name=u_name,u_pass=u_pass,uid=uid)))




# http://127.0.0.1:8000/skf/leave_application/director_approveList?cid=SKF&director_id=1101
 # http://127.0.0.1:8000/skf/leave_application/director_approveList?cid=SKF&rep_id=1101&rep_pass=123

def approveListDDM():                  

    cid = str(request.vars.cid).strip().upper()    
    d_director_id=str(request.vars.rep_id).strip().upper()
    d_pass=str(request.vars.rep_pass).strip().upper()

    session.msg_1 = ''
    leave_req=''
    director_pass=''
    
    checkSettings=  db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'd_sales_director') & (db.sm_settings.s_value == d_director_id) ).select(db.sm_settings.s_value, limitby=(0, 1))
    # return checkSettings
    if checkSettings:
        director_id=checkSettings[0].s_value
        
        checkRep=  db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == director_id) & (db.sm_rep.status == 'ACTIVE') & (db.sm_rep.password == d_pass) ).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.password,limitby=(0, 1))        
        if checkRep: 
            director_pass=checkRep[0].password
            
            leave_req = db((db.sm_leave_application.cid == cid) & (db.sm_leave_application.divisional_head_status == 'Approved') & (db.sm_leave_application.ddm_status == '')  ).select(db.sm_leave_application.emp_id, db.sm_leave_application.emp_name, db.sm_leave_application.from_date,db.sm_leave_application.to_date,db.sm_leave_application.total_leave, db.sm_leave_application.leave_type, db.sm_leave_application.id, orderby=db.sm_leave_application.emp_id|db.sm_leave_application.created_on)                                               
            if not leave_req:
                session.msg_1 = 'Nothing pending for approval.' 
    else :
        session.flash='Access is Denied !'        
        
    return dict(leave_req=leave_req,director_id=director_id,director_pass=director_pass)


def leave_application_approval_ddm():               
    
    cid = str(request.vars.cid).strip().upper()
    uid= str(request.vars.memId_1)
    u_name= str(request.vars.memName_1)
    
    director_id= str(request.vars.director_id)
    director_pass= str(request.vars.director_pass)
    
    memId_1_id= str(request.vars.memId_1_id)
    # return memId_1_id    
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
    record_id=''
    leave_req_reason=''

    recordRows = db((db.sm_leave_application.cid == cid)  &  (db.sm_leave_application.emp_id==uid)  &  (db.sm_leave_application.divisional_head_status=='Approved') &  (db.sm_leave_application.id==memId_1_id)).select(db.sm_leave_application.ALL, orderby=db.sm_leave_application.emp_id)
    # return recordRows
    for recordRow in recordRows:
        record_id = recordRow.id        
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
        leave_req_reason = recordRow.note

    return dict(director_id=director_id,director_pass=director_pass,zonal_head_id=zonal_head_id,zonal_head_name=zonal_head_name,depthNo=depthNo,cid=cid,uid=uid,u_name=u_name,ared_head_id=ared_head_id,ared_head_name=ared_head_name,emp_id=emp_id,emp_name=emp_name,from_date=from_date,to_date=to_date,total_leave=total_leave,leave_type=leave_type,record_id=record_id,leave_req_reason=leave_req_reason)


def leave_application_ddmConfirm():              

    cid = str(request.vars.cid).strip().upper()    
    director_id=str(request.vars.director_id).strip().upper()
    director_pass=str(request.vars.director_pass).strip().upper()
    
    memId_1=str(request.vars.emp_id).strip().upper()
    memName_1=str(request.vars.emp_name).strip().upper()
    memId_1_id=str(request.vars.record_id).strip()
    # return record_id
    
    btn_approve_application=request.vars.btn_approve_application
    btn_reject_application=request.vars.btn_reject_application
    
    checkRep=  db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == director_id) & (db.sm_rep.status == 'ACTIVE') & (db.sm_rep.password == director_pass) ).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.password,limitby=(0, 1))
    # return checkRep
    if checkRep: 

        if btn_approve_application:                        
            from_dt_2=str(request.vars.from_dt_2).strip().upper()
            to_dt_2=str(request.vars.to_dt_2).strip().upper()
            total_leave=str(request.vars.leaveDayVal).strip().upper()
            
            statusConfirm = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == memId_1) & (db.sm_leave_application.id == memId_1_id) & (db.sm_leave_application.director_marktng_status == '')).update(from_date=from_dt_2,to_date=to_dt_2,total_leave=total_leave,ddm_id=director_id,ddm_status='Approved')            
            session.flash='Approved Successfully.'
            redirect(URL(c='leave_application',f='leave_application_approval_d',vars=dict(cid=cid,director_id=director_id,director_pass=director_pass,memId_1=memId_1,memId_1_id=memId_1_id,memName_1=memName_1)))

            
        if btn_reject_application: 

            statusConfirm = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == memId_1)& (db.sm_leave_application.id == memId_1_id) ).update(ddm_id=director_id,ddm_status='Rejected')              
            session.flash='Rejected Successfully.'
            redirect(URL(c='leave_application',f='leave_application_approval_ddm',vars=dict(cid=cid,director_id=director_id,director_pass=director_pass,memId_1=memId_1,memId_1_id=memId_1_id,memName_1=memName_1)))
    else:
        session.flash='Invalid Authorization.'

# http://127.0.0.1:8000/skf/leave_application/director_approveList?cid=SKF&rep_id=1101&rep_pass=123

def director_approveList():                      
    
    cid = str(request.vars.cid).strip().upper()    
    director_id=str(request.vars.rep_id).strip().upper()
    d_pass=str(request.vars.rep_pass).strip().upper()
    
    session.msg_1 = ''
    leave_req=''
    director_pass=''
    
    checkSettings=  db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'sales_director') & (db.sm_settings.s_value == director_id) ).select(db.sm_settings.s_value, limitby=(0, 1))
    if checkSettings:
        director_id=checkSettings[0].s_value
        
        checkRep=  db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == director_id) & (db.sm_rep.status == 'ACTIVE') & (db.sm_rep.password == d_pass) ).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.password,limitby=(0, 1))        
        if checkRep: 
            director_pass=checkRep[0].password
            
            leave_req = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.ddm_status == 'Approved') & (db.sm_leave_application.director_marktng_status == '')  ).select(db.sm_leave_application.emp_id, db.sm_leave_application.emp_name, db.sm_leave_application.from_date,db.sm_leave_application.to_date,db.sm_leave_application.total_leave, db.sm_leave_application.leave_type, db.sm_leave_application.id, orderby=db.sm_leave_application.emp_id|db.sm_leave_application.created_on)                                   
            
            if not leave_req:
                session.msg_1 = 'Nothing pending for approval.' 
    else :
        session.flash='Access is Denied !'        
        
    return dict(leave_req=leave_req,director_id=director_id,director_pass=director_pass)


def leave_application_approval_d():               
    
    cid = str(request.vars.cid).strip().upper()
    uid= str(request.vars.memId_1)
    u_name= str(request.vars.memName_1)
    
    director_id= str(request.vars.director_id)
    director_pass= str(request.vars.director_pass)
    
    memId_1_id= str(request.vars.memId_1_id)
    # return memId_1_id
    
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
    record_id=''
    leave_req_reason=''
    recordRows = db((db.sm_leave_application.cid == cid)  &  (db.sm_leave_application.emp_id==uid)  &  (db.sm_leave_application.ddm_status=='Approved') &  (db.sm_leave_application.id==memId_1_id)).select(db.sm_leave_application.ALL, orderby=db.sm_leave_application.emp_id)
    # return recordRows
    for recordRow in recordRows:
        record_id = recordRow.id
        
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
        
        leave_req_reason = recordRow.note

    return dict(director_id=director_id,director_pass=director_pass,zonal_head_id=zonal_head_id,zonal_head_name=zonal_head_name,depthNo=depthNo,cid=cid,uid=uid,u_name=u_name,ared_head_id=ared_head_id,ared_head_name=ared_head_name,emp_id=emp_id,emp_name=emp_name,from_date=from_date,to_date=to_date,total_leave=total_leave,leave_type=leave_type,record_id=record_id,leave_req_reason=leave_req_reason)



def leave_application_dConfirm():              

    cid = str(request.vars.cid).strip().upper()    
    director_id=str(request.vars.director_id).strip().upper()
    director_pass=str(request.vars.director_pass).strip().upper()
    
    memId_1=str(request.vars.emp_id).strip().upper()
    memName_1=str(request.vars.emp_name).strip().upper()
    memId_1_id=str(request.vars.record_id).strip()
    # return record_id
    
    btn_approve_application=request.vars.btn_approve_application
    btn_reject_application=request.vars.btn_reject_application
    
    checkRep=  db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == director_id) & (db.sm_rep.status == 'ACTIVE') & (db.sm_rep.password == director_pass) ).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.password,limitby=(0, 1))
    # return checkRep
    if checkRep: 

        if btn_approve_application:            
            
            from_dt_2=str(request.vars.from_dt_2).strip().upper()
            to_dt_2=str(request.vars.to_dt_2).strip().upper()
            total_leave=str(request.vars.leaveDayVal).strip().upper()
            
            statusConfirm = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == memId_1) & (db.sm_leave_application.id == memId_1_id) & (db.sm_leave_application.director_marktng_status == '')).update(from_date=from_dt_2,to_date=to_dt_2,total_leave=total_leave,director_id=director_id,director_marktng_status='Approved')            
            session.flash='Approved Successfully.'
            redirect(URL(c='leave_application',f='leave_application_approval_d',vars=dict(cid=cid,director_id=director_id,director_pass=director_pass,memId_1=memId_1,memId_1_id=memId_1_id,memName_1=memName_1)))

            
        if btn_reject_application:            
            statusConfirm = db((db.sm_leave_application.cid == cid)  & (db.sm_leave_application.emp_id == memId_1)& (db.sm_leave_application.id == memId_1_id) ).update(director_id=director_id,director_marktng_status='Rejected')              
            session.flash='Rejected Successfully.'
            redirect(URL(c='leave_application',f='leave_application_approval_d',vars=dict(cid=cid,director_id=director_id,director_pass=director_pass,memId_1=memId_1,memId_1_id=memId_1_id,memName_1=memName_1)))
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




# http://127.0.0.1:8000/skf/leave_application/approve_reject_notice?cid=SKF&rep_id=IT03&rep_pass=123   



def approve_reject_notice():               
    
    cid = str(request.vars.cid).strip().upper()
        
    rep_id = str(request.vars.rep_id)
    password = str(request.vars.rep_pass)

    
    check_Rows=db((db.sm_rep.cid==cid) & (db.sm_rep.rep_id==rep_id)  & (db.sm_rep.password==password)  & (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.user_type,limitby=(0,1))
    
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
        depthNo='3'
    else:
        supLevelRows=db((db.sm_supervisor_level.cid==cid) & (db.sm_supervisor_level.sup_id==rep_id)).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no)                
        for supRow in supLevelRows:
            level_id=supRow.level_id
            depthNo=supRow.level_depth_no

    recordRows = db((db.sm_leave_application.cid == cid)  &  (db.sm_leave_application.emp_id==rep_id )).select(db.sm_leave_application.ALL,limitby=(0, 20))

    
    return dict(recordRows=recordRows,depthNo=depthNo)

    # return dict(cid=cid,emp_id=emp_id,emp_name=emp_name,from_date=from_date,to_date=to_date,total_leave=total_leave,leave_type=leave_type,ared_head_id=ared_head_id,ared_head_name=ared_head_name,area_head_status=area_head_status,zonal_head_id=zonal_head_id,zonal_head_name=zonal_head_name,zonal_head_status=zonal_head_status,divisional_head_id=divisional_head_id,divisional_head_name=divisional_head_name,divisional_head_status=divisional_head_status,director_id=director_id,director_name=director_name,director_marktng_status=director_marktng_status)
