from random import randint
import urllib2
import calendar
import urllib
import time



# 127.0.0.1:8000/kpl/tour_web_members/teamShow_web?cid=kpl&rep_id=it002&rep_pass=1234&report_person=123


def teamShow_web():
    response.title = 'TEAM LIST'

    cid = request.vars.cid
    session.cid = cid
    uid = request.vars.rep_id
    session.uid = uid    
    password = request.vars.rep_pass
    session.password = password    
    session.depthNo_user = ''

    check_Rows=db((db.sm_rep.cid==cid) & (db.sm_rep.rep_id==uid)  & (db.sm_rep.password==password)  & (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.user_type,limitby=(0,1))
#     return db._lastsql
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

        return dict()
    
    else:
        level_idList=[]
        depthList=[]        
        levelList=[]
        areaList = []
        session.msg_1 = ''
        supLevelRows=db((db.sm_supervisor_level.cid==cid) & (db.sm_supervisor_level.sup_id==uid)).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no)
#         return supLevelRows
        for supRow in supLevelRows:
            level_id=supRow.level_id
            depthNo=supRow.level_depth_no
            session.depthNo_user=depthNo
#             return depthNo
            level_idList.append(level_id)
#             depthList.append(depthNo)
            
            level = 'level' + str(depthNo)
#         return  session.depthNo_user   
#         if session.depthNo_user != 2 :
        levelRows = db((db.sm_level.cid == cid) & (db.sm_level.parent_level_id.belongs(level_idList) )).select(db.sm_level.level_id, orderby=db.sm_level.level_id)
        for levelRow in levelRows:
            territoryid = levelRow.level_id
            areaList.append(territoryid)
#         else:
#             repRows = db((db.sm_level.cid == cid) & (db.sm_level.parent_level_id.belongs(level_idList) )).select(db.sm_level.level_id, orderby=db.sm_level.level_id)
#             for repRow in repRows:
#                 territoryid = repRow.area_id
#                 areaList.append(territoryid)
        if session.depthNo_user != 2 :
            step_Rows_1 = db((db.sm_supervisor_level.cid == cid)  &  (db.sm_supervisor_level.level_id.belongs(areaList) )   &  (db.sm_supervisor_level.sup_id != uid)).select(db.sm_supervisor_level.sup_id, db.sm_supervisor_level.sup_name, orderby=db.sm_supervisor_level.sup_id)
            if not step_Rows_1:
                session.msg_1 = 'No members available !'    
        else:    
            step_Rows_1 = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.area_id.belongs(areaList) )).select(db.sm_rep_area.rep_id, db.sm_rep_area.rep_name, db.sm_rep_area.area_id, orderby=db.sm_rep_area.area_id)
#             step_Rows_1 = db((db.sm_supervisor_level.cid == cid)  &  (db.sm_supervisor_level.level_id.belongs(areaList) )   &  (db.sm_supervisor_level.sup_id != uid)).select(db.sm_supervisor_level.sup_id, db.sm_supervisor_level.sup_name, orderby=db.sm_supervisor_level.sup_id)
            if not step_Rows_1:
                session.msg_1 = 'No members available !'  
        
#         return step_Rows_1
        return dict(step_Rows_1 = step_Rows_1)
                
                





