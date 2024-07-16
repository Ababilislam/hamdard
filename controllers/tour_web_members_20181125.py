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
        pass
    
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
#         return  session.depthNo   
        if session.depthNo_user != 2 :
            levelRows = db((db.sm_level.cid == cid) & (db.sm_level.parent_level_id.belongs(level_idList) )).select(db.sm_level.level_id, orderby=db.sm_level.level_id)
            for levelRow in levelRows:
                territoryid = levelRow.level_id
                areaList.append(territoryid)
        else:
            repRows = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.area_id.belongs(level_idList) )).select(db.sm_rep_area.area_id, orderby=db.sm_rep_area.area_id)
            for repRow in repRows:
                territoryid = repRow.area_id
                areaList.append(territoryid)
        
        step_Rows_1 = db((db.sm_supervisor_level.cid == cid)  &  (db.sm_supervisor_level.level_id.belongs(areaList) )   &  (db.sm_supervisor_level.sup_id != uid)).select(db.sm_supervisor_level.sup_id, db.sm_supervisor_level.sup_name, orderby=db.sm_supervisor_level.sup_id)
        if not step_Rows_1:
            session.msg_1 = 'No members available !'        

        
        
        return dict(step_Rows_1 = step_Rows_1)
                
def members_step_2():
    response.title = 'TEAM LIST'
    cid=session.cid
    uid=session.uid
    password=session.password
    memId_1 = request.args[0]
    memName_1 = request.args[1]
    sup_name = ''
    session.depthNo_member=''
#     return memName_1
   
    
#     return memId_1

    check_Rows=db((db.sm_rep.cid==cid) & (db.sm_rep.rep_id==uid)  & (db.sm_rep.password==password)  & (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.user_type,limitby=(0,1))
#     return db._lastsql
    if check_Rows:
        rep_id=check_Rows[0].rep_id
        name=check_Rows[0].name
        user_type=check_Rows[0].user_type
        
        session.user_type = user_type
#     return recRsmId
    else :
        session.flash='Access is Denied !'
    
    
    if session.user_type == 'rep' :
        pass
    
    else:
        level_idList=[]
        depthList=[]        
        levelList=[]
        areaList = []
        session.msg  = ''
        if memId_1 != '':
            supLevelRows=db((db.sm_supervisor_level.cid==cid) & (db.sm_supervisor_level.sup_id==memId_1)).select(db.sm_supervisor_level.sup_name,db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no)
#             return supLevelRows
            for supRow in supLevelRows:
                level_id=supRow.level_id
                depthNo=supRow.level_depth_no
                session.depthNo_member=depthNo
                sup_name=supRow.sup_name
    
    #                 return session.depthNo_member
                level_idList.append(level_id)
                level = 'level' + str(depthNo)
                
            if session.depthNo_member <= 2 :
#                 return '1'
                levelRows = db((db.sm_level.cid == cid) & (db.sm_level.parent_level_id.belongs(level_idList) )).select(db.sm_level.level_id, orderby=db.sm_level.level_id)
#                 return levelRows
                for levelRow in levelRows:
                    territoryid = levelRow.level_id
                    areaList.append(territoryid)
#                     return territoryid
#                 step_Rows_2_sup = db((db.sm_supervisor_level.cid == cid)  &  (db.sm_supervisor_level.level_id.belongs(areaList) )).select(db.sm_supervisor_level.sup_id, db.sm_supervisor_level.sup_name, orderby=db.sm_supervisor_level.sup_id)
            else:
                pass
#                 return '2'
#                 step_Rows_2_rep_area = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.area_id.belongs(level_idList) )).select(db.sm_rep_area.rep_id, db.sm_rep_area.rep_name, db.sm_rep_area.area_id, orderby=db.sm_rep_area.area_id)
#                 for step_Rows_2_rep_area in step_Rows_2_rep_area:
#                     territoryid = step_Rows_2_rep_area.area_id
#                     areaList.append(territoryid)
#             return len(level_idList)
            if session.depthNo_member < 2 :
                s_type='Sup'
                step_Rows_2 = db((db.sm_supervisor_level.cid == cid)  &  (db.sm_supervisor_level.level_id.belongs(areaList))   &  (db.sm_supervisor_level.sup_id != memId_1)).select(db.sm_supervisor_level.sup_id, db.sm_supervisor_level.sup_name, orderby=db.sm_supervisor_level.sup_id)
                if not step_Rows_2:
                    session.msg = 'No members available !'      
            else:
                s_type='Rep'
                step_Rows_2 = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.area_id.belongs(areaList) )).select(db.sm_rep_area.rep_id, db.sm_rep_area.rep_name, db.sm_rep_area.area_id, orderby=db.sm_rep_area.area_id)

            return dict(step_Rows_2=step_Rows_2,memId_1=memId_1,memName_1=memName_1,sup_name=sup_name,s_type=s_type)


def kpl_visit_details():
    response.title = 'Report'
    cid=session.cid 
    uid=session.uid     
    password=session.password     
     

    check_Rows=db((db.sm_rep.cid==cid) & (db.sm_rep.rep_id==uid)  & (db.sm_rep.password==password)  & (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.user_type,limitby=(0,1))
#     return db._lastsql
#     return check_Rows
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
        pass
    
    else:
        level_idList=[]
        depthList=[]        
        levelList=[]
        areaList=[]
        supLevelRows=db((db.sm_supervisor_level.cid==cid) & (db.sm_supervisor_level.sup_id==uid)).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no)
#         return supLevelRows
        for supRow in supLevelRows:
            level_id=supRow.level_id
            depthNo=supRow.level_depth_no
            level_idList.append(level_id)            
            level = 'level' + str(depthNo)
            
#             return level

            if depthNo != 2 :
#                 return '1'                


                levelRows = db((db.sm_level.cid == cid) & (db.sm_level.parent_level_id.belongs(level_idList) )).select(db.sm_level.level_id, orderby=db.sm_level.level_id)
    
    #             return db._lastsql
                for levelRow in levelRows:
                    territoryid = levelRow.level_id            
                    areaList.append(territoryid)
                    
                    
            else :
#                 return '2'
                repRows = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.area_id.belongs(level_idList) )).select(db.sm_rep_area.area_id, orderby=db.sm_rep_area.area_id)
                for repRow in repRows:
                    territoryid = repRow.area_id            
                    areaList.append(territoryid)
                
#             return areaList
    #             User Details Start
    
    #             return areaList
            qset_user_dcr = db()
            qset_user_dcr = qset_user_dcr(db.sm_doctor_visit.cid == cid)
            qset_user_dcr = qset_user_dcr(db.sm_doctor_visit.rep_id == uid)
            qset_user_dcr = qset_user_dcr(db.sm_doctor_visit.route_id.belongs(areaList))
            order_head_user_dcr_records = qset_user_dcr.count()


            qset_user_rx = db()
            qset_user_rx = qset_user_rx(db.sm_prescription_head.cid == cid)
            qset_user_rx = qset_user_rx(db.sm_prescription_head.submit_by_id == uid)
            qset_user_rx = qset_user_rx(db.sm_prescription_head.area_id.belongs(areaList))
            order_head_user_rx_records = qset_user_rx.count()


            qset_user = db()
            qset_user = qset_user(db.sm_order_head.cid == cid)
            qset_user = qset_user(db.sm_order_head.rep_id == uid)
            qset_user = qset_user(db.sm_order_head.area_id.belongs(areaList))
            order_head_user_records = qset_user.count()


            qset_user_detail = db()
            qset_user_detail = qset_user_detail(db.sm_order.cid == cid)
            qset_user_detail = qset_user_detail(db.sm_order.rep_id == uid)
            qset_user_detail = qset_user_detail(db.sm_order.area_id.belongs(areaList))
            order_user_detail_records = qset_user_detail.select((db.sm_order.quantity*db.sm_order.price).sum(), orderby=db.sm_order.id)



#             Team Details Start


            qset_team_dcr = db()
            qset_team_dcr = qset_team_dcr(db.sm_doctor_visit.cid == cid)
            qset_team_dcr = qset_team_dcr(db.sm_doctor_visit.rep_id != uid)
            qset_team_dcr = qset_team_dcr(db.sm_doctor_visit.route_id.belongs(areaList))
            order_head_team_dcr_records = qset_team_dcr.count()



            qset_team_rx = db()
            qset_team_rx = qset_team_rx(db.sm_prescription_head.cid == cid)
            qset_team_rx = qset_team_rx(db.sm_prescription_head.submit_by_id != uid)
            qset_team_rx = qset_team_rx(db.sm_prescription_head.area_id.belongs(areaList))
            order_head_team_rx_records = qset_team_rx.count()


                
            qset = db()
            qset = qset(db.sm_order_head.cid == cid)    
            qset = qset(db.sm_order_head.rep_id != uid)
            qset = qset(db.sm_order_head.area_id.belongs(areaList))
            order_head_records = qset.count()

            qset_detail = db()
            qset_detail = qset_detail(db.sm_order.cid == cid)    
            qset_detail = qset_detail(db.sm_order.rep_id != uid)
            qset_detail = qset_detail(db.sm_order.area_id.belongs(areaList))
            order_detail_records = qset_detail.select((db.sm_order.quantity*db.sm_order.price).sum(), orderby=db.sm_order.id)
#             return db._lastsql
#             return order_detail_records

            return dict(order_head_user_dcr_records=order_head_user_dcr_records,order_head_user_records=order_head_user_records, order_user_detail_records=order_user_detail_records, order_head_user_rx_records=order_head_user_rx_records,order_head_records=order_head_records,order_detail_records=order_detail_records,order_head_team_rx_records=order_head_team_rx_records,order_head_team_dcr_records=order_head_team_dcr_records)


def kpl_visit_details_members():
    response.title = 'Report'
    cid=session.cid
    uid=session.uid
    password=session.password
    memId_1 = request.args[0]
    memName_1 = request.args[1]
    report_person = memId_1
    
#     return memId_1

    check_Rows=db((db.sm_rep.cid==cid) & (db.sm_rep.rep_id==uid)  & (db.sm_rep.password==password)  & (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.user_type,limitby=(0,1))
#     return db._lastsql
    if check_Rows:
        rep_id=check_Rows[0].rep_id
        name=check_Rows[0].name
        user_type=check_Rows[0].user_type
        
        session.user_type = user_type
#     return recRsmId

    else :
        session.flash='Access is Denied !'

    
    
    if session.user_type == 'rep' :
        pass
    
    else:
        level_idList=[]
        depthList=[]        
        levelList=[]
        areaList = []
        areaList_under = []
        mpo_Rows = ''
        if memId_1 != '':
            supLevelRows=db((db.sm_supervisor_level.cid==cid) & (db.sm_supervisor_level.sup_id==memId_1)).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no)
    #         return supLevelRows
            for supRow in supLevelRows:
                level_id=supRow.level_id
                depthNo=supRow.level_depth_no
                session.depthNo_member=depthNo
    
    #                 return session.depthNo_member
                level_idList.append(level_id)
                level = 'level' + str(depthNo)
    
            if session.depthNo_member <= 2 :
#                 return '1'
                levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level].belongs(level_idList) )).select(db.sm_level.level_id, orderby=db.sm_level.level_id)
                for levelRow in levelRows:
                    territoryid = levelRow.level_id
                    areaList.append(territoryid)
                    
                levelRows_under = db((db.sm_level.cid == cid) & (db.sm_level.parent_level_id.belongs(level_idList) )).select(db.sm_level.level_id, orderby=db.sm_level.level_id)
#                 return levelRows_under
                for levelRows_under in levelRows_under:
                    territoryid = levelRow.level_id
                    areaList_under.append(territoryid)
                    
                    
                
                
                
            else:
                pass
            
            
            
            teamList=[]
            if session.depthNo_member < 2 :
                levelRows_t = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.level_id.belongs(areaList_under))).select(db.sm_supervisor_level.sup_id, orderby=db.sm_supervisor_level.sup_id)
                for levelRows_t in levelRows_t:
                    t_id = levelRows_t.sup_id
                    teamList.append(t_id)
            else:
                levelRows_t = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.area_id.belongs(areaList_under))).select(db.sm_rep_area.rep_id, orderby=db.sm_rep_area.rep_id)
                for levelRows_t in levelRows_t:
                    t_id = levelRows_t.rep_id
                    teamList.append(t_id)
                
                

            
#             return areaList
            qset_user_dcr = db()
            qset_user_dcr = qset_user_dcr(db.sm_doctor_visit.cid == cid)
            qset_user_dcr = qset_user_dcr(db.sm_doctor_visit.rep_id == report_person)
            qset_user_dcr = qset_user_dcr(db.sm_doctor_visit.route_id.belongs(areaList))
            order_head_user_dcr_records = qset_user_dcr.count()
    
    
            qset_user_rx = db()
            qset_user_rx = qset_user_rx(db.sm_prescription_head.cid == cid)
            qset_user_rx = qset_user_rx(db.sm_prescription_head.submit_by_id == report_person)
            qset_user_rx = qset_user_rx(db.sm_prescription_head.area_id.belongs(areaList))
            order_head_user_rx_records = qset_user_rx.count()
            
    
    
            qset_user = db()
            qset_user = qset_user(db.sm_order_head.cid == cid)
            qset_user = qset_user(db.sm_order_head.rep_id == report_person)
            qset_user = qset_user(db.sm_order_head.area_id.belongs(areaList))
            order_head_user_records = qset_user.count()
    
    
    
    
            qset_user_detail = db()
            qset_user_detail = qset_user_detail(db.sm_order.cid == cid)
            qset_user_detail = qset_user_detail(db.sm_order.rep_id == report_person)
            qset_user_detail = qset_user_detail(db.sm_order.area_id.belongs(areaList))
            order_user_detail_records = qset_user_detail.select((db.sm_order.quantity*db.sm_order.price).sum(), orderby=db.sm_order.id)
    
    
    
    #             Team Details Start
    
    
    
            qset_team_dcr = db()
            qset_team_dcr = qset_team_dcr(db.sm_doctor_visit.cid == cid)
            qset_team_dcr = qset_team_dcr(db.sm_doctor_visit.rep_id != report_person)
            qset_team_dcr = qset_team_dcr(db.sm_doctor_visit.route_id.belongs(areaList))
            order_head_team_dcr_records = qset_team_dcr.count()
    
            
            qset_team_rx = db()
            qset_team_rx = qset_team_rx(db.sm_prescription_head.cid == cid)
            qset_team_rx = qset_team_rx(db.sm_prescription_head.submit_by_id != report_person)
            if session.depthNo_member==0:
                qset_team_rx = qset_team_rx(db.sm_prescription_head.area_id.belongs(areaList))
            if session.depthNo_member==1:    
                qset_team_rx = qset_team_rx(db.sm_prescription_head.submit_by_id.belongs(teamList))
            
            
            order_head_team_rx_records = qset_team_rx.count()
    
            
                
            qset = db()
            qset = qset(db.sm_order_head.cid == cid)    
            qset = qset(db.sm_order_head.rep_id != report_person)
            qset = qset(db.sm_order_head.area_id.belongs(areaList))
            order_head_records = qset.count()
    
            qset_detail = db()
            qset_detail = qset_detail(db.sm_order.cid == cid)    
            qset_detail = qset_detail(db.sm_order.rep_id != report_person)
            qset_detail = qset_detail(db.sm_order.area_id.belongs(areaList))
            order_detail_records = qset_detail.select((db.sm_order.quantity*db.sm_order.price).sum(), orderby=db.sm_order.id)

            return dict(memId_1=memId_1,memName_1=memName_1,order_head_user_dcr_records=order_head_user_dcr_records,order_head_user_records=order_head_user_records, order_user_detail_records=order_user_detail_records, order_head_user_rx_records=order_head_user_rx_records,order_head_records=order_head_records,order_detail_records=order_detail_records,order_head_team_rx_records=order_head_team_rx_records,order_head_team_dcr_records=order_head_team_dcr_records)    



















