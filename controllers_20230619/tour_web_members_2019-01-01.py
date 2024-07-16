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
    

                level_idList.append(level_id)
                level = 'level' + str(depthNo)
#             return session.depthNo_member     
#             if session.depthNo_member == 2 :

            levelRows = db((db.sm_level.cid == cid) & (db.sm_level.parent_level_id.belongs(level_idList) )).select(db.sm_level.level_id, orderby=db.sm_level.level_id)
#             return levelRows
            for levelRow in levelRows:
                territoryid = levelRow.level_id
                areaList.append(territoryid)

          
            
            step_Rows_2=''
            if session.depthNo_member < 2 :
                s_type='Sup'
#                 return session.depthNo_member
                step_Rows_2 = db((db.sm_supervisor_level.cid == cid)  &  (db.sm_supervisor_level.level_id.belongs(areaList))   &  (db.sm_supervisor_level.sup_id != memId_1)).select(db.sm_supervisor_level.sup_id, db.sm_supervisor_level.sup_name, orderby=db.sm_supervisor_level.sup_id)
                if not step_Rows_2:
                    session.msg = 'No members available !'      
            else:
                s_type='Rep'
                step_Rows_2 = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.area_id.belongs(areaList) )).select(db.sm_rep_area.rep_id, db.sm_rep_area.rep_name, db.sm_rep_area.area_id, orderby=db.sm_rep_area.area_id)
#                 return step_Rows_2
            
            return dict(step_Rows_2=step_Rows_2,memId_1=memId_1,memName_1=memName_1,sup_name=sup_name,s_type=s_type)


def kpl_visit_details():
    response.title = 'Report'
    cid=session.cid 
    uid=session.uid     
    password=session.password     
     

    check_Rows=db((db.sm_rep.cid==cid) & (db.sm_rep.rep_id==uid)  & (db.sm_rep.password==password)  & (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.user_type,limitby=(0,1))
#     return uid
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
            

        repRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level].belongs(level_idList) )).select(db.sm_level.level_id, orderby=db.sm_level.level_id , groupby=db.sm_level.level_id)
#         return repRows
        for repRow in repRows:
            territoryid = repRow.level_id            
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
    
#             if session.depthNo_member <= 2 :
#                 return '1'
            levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level].belongs(level_idList) )).select(db.sm_level.level_id, orderby=db.sm_level.level_id)
#             return levelRows
            for levelRow in levelRows:
                territoryid = levelRow.level_id
                areaList.append(territoryid)
                    
#                 levelRows_under = db((db.sm_level.cid == cid) & (db.sm_level.parent_level_id.belongs(level_idList) )).select(db.sm_level.level_id, orderby=db.sm_level.level_id)
# #                 return levelRows_under
#                 for levelRows_under in levelRows_under:
#                     territoryid = levelRow.level_id
#                     areaList_under.append(territoryid)
                    
                    
                
                
                
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
#             if session.depthNo_member==0:
            qset_team_rx = qset_team_rx(db.sm_prescription_head.area_id.belongs(areaList))
#             if session.depthNo_member==1:    
#                 qset_team_rx = qset_team_rx(db.sm_prescription_head.submit_by_id.belongs(teamList))
            
            
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










# ===================Nazma===========================
# 127.0.0.1:8000/kpl/tour_web_members/kpl_visit_details_members_map?cid=KPL&uid=IT03&rep_pass=1234&report_person=123
def kpl_visit_details_members_map():
    
    response.title = 'Report'
#     return session.teamlListArray
    response.title = 'Report'
    cid=session.cid
    uid=session.uid
    password=session.password
    memId_1 = request.args[0]
    memName_1 = request.args[1]
    report_person = memId_1
    cid='ABC' 
#     return memId_1

    check_Rows=db((db.sm_rep.cid==cid) & (db.sm_rep.rep_id==uid)   & (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.user_type,limitby=(0,1))
#     return db._lastsql
    if check_Rows:
        rep_id=check_Rows[0].rep_id
        name=check_Rows[0].name
        user_type=check_Rows[0].user_type
        
        session.user_type = user_type
#     return recRsmId

    else :
        session.flash='Access is Denied !'

    
#     return session.user_type
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
#             return memId_1
            supLevelRows=db((db.sm_supervisor_level.cid==cid) & (db.sm_supervisor_level.sup_id==memId_1)).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no)
#             return supLevelRows
            level=''
            for supRow in supLevelRows:
                level_id=supRow.level_id
                depthNo=supRow.level_depth_no
                session.depthNo_member=depthNo
    
    #                 return session.depthNo_member
                level_idList.append(level_id)
                level = 'level' + str(depthNo)
    
#             if session.depthNo_member <= 2 :
#                 return '1'
#             return level   
            levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level].belongs(level_idList) )).select(db.sm_level.level_id, orderby=db.sm_level.level_id)
#             return levelRows
            for levelRow in levelRows:
                territoryid = levelRow.level_id
                areaList_under.append(territoryid)
                    
#                 levelRows_under = db((db.sm_level.cid == cid) & (db.sm_level.parent_level_id.belongs(level_idList) )).select(db.sm_level.level_id, orderby=db.sm_level.level_id)
# #                 return levelRows_under
#                 for levelRows_under in levelRows_under:
#                     territoryid = levelRow.level_id
#                     areaList_under.append(territoryid)
                    
                 
                
                
                
            else:
                pass
            
            
            
            teamList=[]
#             if session.depthNo_member < 2 :
#                 levelRows_t = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.level_id.belongs(areaList_under))).select(db.sm_supervisor_level.sup_id, orderby=db.sm_supervisor_level.sup_id)
#                 for levelRows_t in levelRows_t:
#                     t_id = levelRows_t.sup_id
#                     teamList.append(t_id)
#             else:

            levelRows_t = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.area_id.belongs(areaList_under))).select(db.sm_rep_area.rep_id, orderby=db.sm_rep_area.rep_id)
            
            
            
            for levelRows_t in levelRows_t:
                t_id = levelRows_t.rep_id
                teamList.append(t_id)
                    
                    
#             return len(teamList)       
                    
#     teamlListArray = []
#     teamlListArray_1 = session.teamlListArray
#     teamlListArray_2 = session.teamlListArray_2
#     if teamlListArray_1 != '':
#         teamlListArray = teamlListArray_1
#         
#     else:
#         teamlListArray = teamlListArray_2
    
    
    point_viewT=''




#     check_Rows=db((db.sm_rep.cid==cid) & (db.sm_rep.rep_id==uid)  & (db.sm_rep.password==password)  & (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.user_type,limitby=(0,1))
# 
# #     return check_Rows
# 
# #     return db._lastsql
#     if check_Rows:
#         rep_id=check_Rows[0].rep_id
#         name=check_Rows[0].name
#         user_type=check_Rows[0].user_type
# 
#         session.user_type = user_type
# #     return recRsmId
# 
#     else :
#         session.flash='Access is Denied !'
# 
# #             return areaList
    
    if teamList != '':
    
        qset_user_dcr = db()
        qset_user_dcr = qset_user_dcr(db.sm_doctor_visit.cid == cid)
    #     return db._lastsql
#         qset_user_dcr = qset_user_dcr(db.sm_doctor_visit.rep_id == uid)
        qset_user_dcr = qset_user_dcr(db.sm_doctor_visit.rep_id.belongs(teamList))
        qset_user_dcr = qset_user_dcr((db.sm_doctor_visit.latitude != '') and (db.sm_doctor_visit.longitude != ''))
    
        records = qset_user_dcr.select(db.sm_doctor_visit.ALL, groupby = db.sm_doctor_visit.rep_id, orderby=~db.sm_doctor_visit.id)
        return records

        if records :
            middle = 2
        
            map_string_in = ''
            start_flag = 0
            map_string = ''
            map_string_name = ''
            map_string_name_in = ''
            center_point = ''
            c = 0
            x = 0
            for row in records:
        
                c = c + 1
                point_view = str(row.latitude)+','+str(row.longitude )
        
                if ((point_view!='0,0') & (point_view!='')):
        
        
        
                    show_str ="Doctor: " + str(row.doc_id) + "(" + str(row.doc_name ) + ")</br>" + "Member: " + str(row.rep_id) + "(" + str(row.rep_name ) + ")</br>" +"Latitude: " + str(row.latitude) + "</br>" + "Longitude: " + str(row.longitude)
                    
                    
                    time_show = show_str
        
        #                 return time_show
        
        
                    center_point = point_view
                    if (c == middle):
                        center_point = point_view
            #            return str(point_view)
                    if (start_flag == 0):
                        map_string_in = map_string_in + 'new google.maps.LatLng(' + str(point_view) + ')'
                        map_string_name = map_string_name + str(time_show) + "," + str(point_view) + ',' + str(x) + 'rdrd'
        
                        start_flag = 1
                    else:
                        map_string_in = map_string_in + ',new google.maps.LatLng(' + str(point_view) + ')'
                        map_string_name = map_string_name + str(time_show) + "," + str(point_view) + ',' + str(x) + 'rdrd'
        
                    x = x + 1
        
            map_string = '[' + map_string_in + ']'
        #     return map_string_name
        #     return  map_string
            if (map_string_name == ''):
                response.flash = 'Result Not Available'
                map_string=''
                map_string_name=''
                center_point=''
        
#             return map_string_name
            return dict(map_string=map_string, map_string_name=map_string_name, center_point=center_point )








