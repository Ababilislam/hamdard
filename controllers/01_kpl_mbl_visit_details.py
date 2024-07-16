# http://127.0.0.1:8000/kpl/01_kpl_mbl_visit_details/kpl_visit_details?cid=kpl&uid=A036&u_pass=123&report_person=123


# http://127.0.0.1:8000/kpl/01_kpl_mbl_visit_details/kpl_visit_details?cid=kpl&uid=F0259&u_pass=1234&report_person=123

def kpl_visit_details():
    response.title = 'Show Map'

    cid = request.vars.cid
    uid = request.vars.uid
    password = request.vars.u_pass


    check_Rows=db((db.sm_rep.cid==cid) & (db.sm_rep.rep_id==uid)  & (db.sm_rep.password==password)  & (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.user_type,limitby=(0,1))
#     return db._lastsql
    if check_Rows:
        rep_id=check_Rows[0].rep_id
        name=check_Rows[0].name
        user_type=check_Rows[0].user_type
        
        session.user_id = rep_id
        session.user_name = name
        session.user_type = user_type

    if session.user_type == 'rep' :
        pass
    
    else:
        level_idList=[]
        depthList=[]        
        levelList=[]
        
        supLevelRows=db((db.sm_supervisor_level.cid==cid) & (db.sm_supervisor_level.sup_id==uid)).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no,limitby=(0,1))
#         return supLevelRows
        for supRow in supLevelRows:
            level_id=supRow.level_id
            depthNo=supRow.level_depth_no
            
#             level_idList.append(level_id)
#             depthList.append(depthNo)
            
            level = 'level' + str(depthNo)

#             level_dcr = 'level' + str(depthNo)+'_id'
            
#             return level

            areaList=[]

#             Nadira Apu below sql
            levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_id)).select(db.sm_level.level_id, orderby=db.sm_level.level_id,limitby=(0,1))
#             levelRows = db((db.sm_level.cid == cid) & (db.sm_level[level] == level_id)).select(db.sm_level.level_id, orderby=db.sm_level.level_id)

#             return db._lastsql
            for levelRow in levelRows:
                territoryid = levelRow.level_id            
                areaList.append(territoryid)

#             User Details Start


            qset_user_dcr = db()
            qset_user_dcr = qset_user_dcr(db.sm_doctor_visit.cid == cid)
            qset_user_dcr = qset_user_dcr(db.sm_doctor_visit.rep_id == uid)
            qset_user_dcr = qset_user_dcr(db.sm_doctor_visit.route_id.belongs(areaList))
            order_head_user_dcr_records = qset_user_dcr.count()


            qset_user_rx = db()
            qset_user_rx = qset_user_rx(db.sm_prescription_head.cid == cid)
            qset_user_rx = qset_user_rx(db.sm_prescription_head.submit_by_id == uid)
            qset_user_rx = qset_user_rx(db.sm_prescription_head.area_id.belongs(areaList))
#             order_head_user_records = qset_user.select(db.sm_order_head.id.count(), orderby=db.sm_order_head.id)
            order_head_user_rx_records = qset_user_rx.count()



            qset_user = db()
            qset_user = qset_user(db.sm_order_head.cid == cid)
            qset_user = qset_user(db.sm_order_head.rep_id == uid)
            qset_user = qset_user(db.sm_order_head.area_id.belongs(areaList))
#             order_head_user_records = qset_user.select(db.sm_order_head.id.count(), orderby=db.sm_order_head.id)
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
#             order_head_user_records = qset_user.select(db.sm_order_head.id.count(), orderby=db.sm_order_head.id)
            order_head_team_rx_records = qset_team_rx.count()


                
            qset = db()
            qset = qset(db.sm_order_head.cid == cid)    
            qset = qset(db.sm_order_head.rep_id != uid)
            qset = qset(db.sm_order_head.area_id.belongs(areaList))
#             order_head_records = qset.select(db.sm_order_head.id.count(), orderby=db.sm_order_head.id)
            order_head_records = qset.count()

            qset_detail = db()
            qset_detail = qset_detail(db.sm_order.cid == cid)    
            qset_detail = qset_detail(db.sm_order.rep_id != uid)
            qset_detail = qset_detail(db.sm_order.area_id.belongs(areaList))
            order_detail_records = qset_detail.select((db.sm_order.quantity*db.sm_order.price).sum(), orderby=db.sm_order.id)
#             return db._lastsql
#             return order_detail_records

            return dict(order_head_user_dcr_records=order_head_user_dcr_records,order_head_user_records=order_head_user_records, order_user_detail_records=order_user_detail_records, order_head_user_rx_records=order_head_user_rx_records,order_head_records=order_head_records,order_detail_records=order_detail_records,order_head_team_rx_records=order_head_team_rx_records,order_head_team_dcr_records=order_head_team_dcr_records)




# http://127.0.0.1:8000/kpl/01_kpl_mbl_visit_details/kpl_all_member_visit_details?cid=kpl&uid=A036&u_pass=123&report_person=123




def kpl_all_member_visit_details():
    response.title = 'Show Map'

    cid = request.vars.cid
    session.cid = cid
    uid = request.vars.uid
    session.uid = uid    
    password = request.vars.u_pass
    session.password = password    


    check_Rows=db((db.sm_rep.cid==cid) & (db.sm_rep.rep_id==uid)  & (db.sm_rep.password==password)  & (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.user_type,limitby=(0,1))
#     return db._lastsql
    if check_Rows:
        rep_id=check_Rows[0].rep_id
        name=check_Rows[0].name
        user_type=check_Rows[0].user_type
        
        session.user_id = rep_id
        session.user_name = name
        session.user_type = user_type

    if session.user_type == 'rep' :
        pass
    
    else:
        level_idList=[]
        depthList=[]        
        levelList=[]
        
        supLevelRows=db((db.sm_supervisor_level.cid==cid) & (db.sm_supervisor_level.sup_id==uid)).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no,limitby=(0,1))
#         return supLevelRows
        for supRow in supLevelRows:
            level_id=supRow.level_id
            depthNo=supRow.level_depth_no
            
            level_idList.append(level_id)
            depthList.append(depthNo)
            
            level = 'level' + str(depthNo)

#             level_dcr = 'level' + str(depthNo)+'_id'
            
#             return level

            areaList=[]

# (db.sm_doctor_visit.route_id.belongs(areaList)

#             Nadira Apu below sql
            levelRows = db((db.sm_level.cid == cid) & (db.sm_level.parent_level_id.belongs(level_idList) )).select(db.sm_level.level_id, orderby=db.sm_level.level_id,limitby=(0,1))
#             levelRows = db((db.sm_level.cid == cid) & (db.sm_level[level] == level_id)).select(db.sm_level.level_id, orderby=db.sm_level.level_id)
#             return levelRows
#             return db._lastsql
            for levelRow in levelRows:
                territoryid = levelRow.level_id            
                areaList.append(territoryid)

            am_Rows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.level_depth_no == 0) & (db.sm_supervisor_level.level_id.belongs(areaList) )).select(db.sm_supervisor_level.sup_id, db.sm_supervisor_level.sup_name, orderby=db.sm_supervisor_level.sup_id,limitby=(0,1))

#             return db._lastsql

            rsm_Rows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.level_depth_no == 1) & (db.sm_supervisor_level.level_id.belongs(areaList) )).select(db.sm_supervisor_level.sup_id, db.sm_supervisor_level.sup_name, orderby=db.sm_supervisor_level.sup_id,limitby=(0,1))


            return dict(am_Rows=am_Rows,rsm_Rows=rsm_Rows)


def rsm_fm_list():
    response.title = 'Show Map'
    cid=session.cid
    uid=session.uid
    password=session.password
    report_person=session.recRsmId
#     return report_person

    check_Rows=db((db.sm_rep.cid==cid) & (db.sm_rep.rep_id==uid)  & (db.sm_rep.password==password)  & (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.user_type,limitby=(0,1))
#     return db._lastsql
    if check_Rows:
        rep_id=check_Rows[0].rep_id
        name=check_Rows[0].name
        user_type=check_Rows[0].user_type
        
        session.user_id = rep_id
        session.user_name = name
        session.user_type = user_type

    if session.user_type == 'rep' :
        pass
    
    else:
        level_idList=[]
        depthList=[]        
        levelList=[]
        
        supLevelRows=db((db.sm_supervisor_level.cid==cid) & (db.sm_supervisor_level.sup_id==uid)).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no,limitby=(0,1))
#         return supLevelRows
        for supRow in supLevelRows:
            level_id=supRow.level_id
            depthNo=supRow.level_depth_no
            
            level_idList.append(level_id)
            depthList.append(depthNo)
            
            level = 'level' + str(depthNo)

#             level_dcr = 'level' + str(depthNo)+'_id'
            
#             return level

            areaList=[]

# (db.sm_doctor_visit.route_id.belongs(areaList)

#             Nadira Apu below sql
            levelRows = db((db.sm_level.cid == cid) & (db.sm_level.parent_level_id.belongs(level_idList) )).select(db.sm_level.level_id, orderby=db.sm_level.level_id,limitby=(0,1))
#             levelRows = db((db.sm_level.cid == cid) & (db.sm_level[level] == level_id)).select(db.sm_level.level_id, orderby=db.sm_level.level_id)
#             return levelRows
#             return db._lastsql
            for levelRow in levelRows:
                territoryid = levelRow.level_id            
                areaList.append(territoryid)

            rsm_Rows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.level_depth_no == 1) & (db.sm_supervisor_level.level_id.belongs(areaList)) & (db.sm_supervisor_level.sup_name == report_person)).select(db.sm_supervisor_level.sup_id, db.sm_supervisor_level.sup_name, orderby=db.sm_supervisor_level.sup_id,limitby=(0,1))
            if rsm_Rows:
                fm_Rows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.level_depth_no == 2) & (db.sm_supervisor_level.level_id.belongs(areaList)) ).select(db.sm_supervisor_level.sup_id, db.sm_supervisor_level.sup_name, orderby=db.sm_supervisor_level.sup_id,limitby=(0,1))
#                 return db._lastsql
                return fm_Rows


        