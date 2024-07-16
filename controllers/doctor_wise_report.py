#http://w04.yeapps.com/skf/ppm_mark_mobile/index?cid=SKF&rep_id=TRRSM&rep_pass=3671

#rsm
#http://127.0.0.1:8000/skf_w04/ppm_mark_mobile/index?cid=SKF&rep_id=TRRSM&rep_pass=3671

#nsm
#http://127.0.0.1:8000/skf_w04/ppm_mark_mobile/index?cid=SKF&rep_id=TRNSM&rep_pass=7650

#rsm
# http://w05.yeapps.com/hamdard/report_seen_rx_mobile/home?cid=HAMDARD&rep_id=9010&rep_pass=1234

def index():
    c_id = request.vars.cid
    try:
        rep_id = request.vars.rep_id.upper()
        rep_pass = request.vars.rep_pass
        from_date =str(first_currentDate)[:10]
        to_date = current_date
        
    except:
        rep_id = session.rep_id
        rep_pass = session.rep_pass
        cid = session.c_id
        from_date = str(first_currentDate)[:10]
        to_date = current_date

    try:
        sch_level = request.vars.pr_region4
        # return sch_level
        sch_zone = request.vars.pr_zone4
        sch_area = request.vars.pr_area4
        sch_territory = request.vars.pr_territory4
        sch_pocket_market = request.vars.pr_pocket_market4
        sch_rx_type = request.vars.sch_rx_type
        search_item_id_name = str(request.vars.search_item_id_name).strip()
        from_date = request.vars.from_date
        to_date = request.vars.to_date
        if (from_date=='' or from_date== None or from_date== 'None'):
            from_date =str(first_currentDate)[:10]
            to_date = current_date

    except:
        sch_level = request.vars.pr_region4
        sch_zone = request.vars.pr_zone4
        sch_area = request.vars.pr_area4
        sch_territory = request.vars.pr_territory4
        sch_pocket_market = request.vars.pr_pocket_market4
        sch_rx_type = request.vars.sch_rx_type
        search_item_id_name = str(request.vars.search_item_id_name).strip()
        from_date =str(first_currentDate)[:10]
        to_date = current_date

    # return from_date
    session.from_date = from_date
    session.to_date = to_date
    session.sch_level_search = sch_level
    session.sch_zone_search = sch_zone
    session.sch_area_search = sch_area
    session.sch_territory = sch_territory
    session.sch_pocket_market = sch_pocket_market
    session.sch_rx_type_search = sch_rx_type
    session.search_item_id_name_search = search_item_id_name
    # return session.from_date
    btn_reset = request.vars.btn_reset
    session.btn_reset = btn_reset
    division_count = []
    zone_count = []
    area_count = []
    territory_count = []

    session.btn_report = 'YES'
    # ---------------------- rep check
    userRecords = db((db.sm_rep.cid == c_id) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == rep_pass) & (
                db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.id, db.sm_rep.name, db.sm_rep.user_type, limitby=(0, 1))
    
    if not userRecords:
        response.flash = 'Invalid/Inactive Supervisor'
    else:
        name = userRecords[0].name
        user_type = userRecords[0].user_type

        session.cid = c_id
        session.rep_id = rep_id
        session.user_id = rep_id
        session.user_type = user_type
        session.rep_pass=rep_pass

        # return user_type
        level_area_list = []
        zlevel_list=[]
        division_list = []
        zone_list = []
        area_list = []
        market_list = []
        territory_list_count = []
        if user_type=='rep':
            repAreaRows = db((db.sm_rep_area.cid == c_id) & (db.sm_rep_area.rep_id == rep_id)).select(db.sm_rep_area.area_id,db.sm_rep_area.area_name,orderby=db.sm_rep_area.area_id)

            if not repAreaRows:
                response.flash = 'Rep Territory Not Available'
            else:
                for rRow in repAreaRows:
                    area_id=rRow.area_id
                    area_name = rRow.area_name
                    # territory_list_count.apend(area_id)
                    dictData = {'area_id': area_id, 'area_name': area_name}
                    level_area_list.append(dictData)
                    territory_count.append(area_id)
            session.division_count = 1
            session.zone_count = 1
            session.area_count = 1        
            session.territory_count = len(territory_count)

                
        else:
            supLevelRows=db((db.sm_supervisor_level.cid==c_id) & (db.sm_supervisor_level.sup_id==rep_id)).select(db.sm_supervisor_level.level_depth_no,db.sm_supervisor_level.level_id)

            if not supLevelRows:
                response.flash = 'Supervisor Level Not Available'
            else:

                sup_level_id_list=[]
                level_depth_no=0
                
                for sRow in supLevelRows:
                    level_depth_no=sRow.level_depth_no
                    level_id=sRow.level_id
                    sup_level_id_list.append(level_id)
                    session.level_depth_no=level_depth_no
                if level_depth_no==0:
                    level3Rows = db((db.sm_level.cid == c_id) & (db.sm_level.level0.belongs(sup_level_id_list)) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level3,db.sm_level.level3_name, orderby=db.sm_level.level_id,groupby=db.sm_level.level3)

                    for dRow1 in level3Rows:
                        level_id = dRow1.level3
                        level_name = dRow1.level3_name

                        dictData = {'area_id': level_id, 'area_name': level_name}
                        level_area_list.append(dictData)

                if level_depth_no == 1:
                    level3Rows = db((db.sm_level.cid == c_id) & (db.sm_level.level1.belongs(sup_level_id_list)) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level3, db.sm_level.level3_name,orderby=db.sm_level.level_id,groupby=db.sm_level.level3)
                    # return db._lastsql
                    # return level3Rows
                    for dRow1 in level3Rows:
                        level_id = dRow1.level3
                        level_name = dRow1.level3_name

                        dictData = {'area_id': level_id, 'area_name': level_name}
                        level_area_list.append(dictData)

                elif level_depth_no==2:
                    level3Rows = db((db.sm_level.cid == c_id) & (db.sm_level.level2.belongs(sup_level_id_list)) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level3,db.sm_level.level3_name, orderby=db.sm_level.level_id,groupby=db.sm_level.level3)

                    for dRow1 in level3Rows:
                        level_id = dRow1.level3
                        level_name = dRow1.level3_name

                        dictData = {'area_id': level_id, 'area_name': level_name}
                        level_area_list.append(dictData)

        
        session.level_area_list=level_area_list
        # return session.level_area_list
        # return len(level_area_list)
        # ========Zone========
        
        if user_type=='sup':
            zLevelRows=db((db.sm_supervisor_level.cid==c_id) & (db.sm_supervisor_level.sup_id==rep_id)).select(db.sm_supervisor_level.level_depth_no,db.sm_supervisor_level.level_id)
            # return zLevelRows
            if not zLevelRows:
                response.flash = 'Zone Not Available'
            else:
                z_level_list=[]
                level_depth_no=0
                for sRow in supLevelRows:
                    level_depth_no=sRow.level_depth_no
                    level_id=sRow.level_id
                    z_level_list.append(level_id)

                zlevel_list=[]
                division_list = []
                zone_list = []
                area_list = []
                if level_depth_no==0: 
                    # return '5'                   
                    level3_Rows = db((db.sm_level.cid == c_id) & (db.sm_level.level0.belongs(z_level_list)) & (db.sm_level.is_leaf == '1') ).select(db.sm_level.level0,db.sm_level.level0_name, orderby=db.sm_level.level0,groupby=db.sm_level.level0)
                    # return level3_Rows
                    for d_Row1 in level3_Rows:
                        division_id = d_Row1.level0
                        division_name = d_Row1.level0_name
                        dictData2 = {'division_id': division_id, 'division_name': division_name}
                        division_list.append(dictData2)
                        # return zone_id
                if level_depth_no == 1:
                    level3_Rows = db((db.sm_level.cid == c_id) & (db.sm_level.level1.belongs(z_level_list)) & (db.sm_level.depth == 1)).select(db.sm_level.level1, db.sm_level.level1_name,orderby=db.sm_level.level1,groupby=db.sm_level.level1)
                    # return db._lastsql
                    for d_Row1 in level3_Rows:
                        zone_id = d_Row1.level1
                        zone_name = d_Row1.level1_name
                        dictData2 = {'zone_id': zone_id, 'zone_name': zone_name}
                        zone_list.append(dictData2)
                    # return zone_list
                
                if level_depth_no==2:

                    level3_Rows = db((db.sm_level.cid == c_id) & (db.sm_level.level2.belongs(z_level_list)) & (db.sm_level.depth == 2) ).select(db.sm_level.level2,db.sm_level.level2_name, orderby=db.sm_level.level2,groupby=db.sm_level.level2)               
                    # return z_level_list
                    for d_Row1 in level3_Rows:
                        area_id = d_Row1.level2
                        area_name = d_Row1.level2_name

                        dictData2 = {'area_id': area_id, 'area_name': area_name}
                        area_list.append(dictData2)

            session.zlevel_list=zlevel_list
            session.division_list=division_list
            session.zone_list=zone_list
            session.area_list=area_list
            # return session.zlevel_list
        else:
            pass

        # ============ TL ===========
        
        if user_type=='sup':
            # return 'n'
            sLevelRows=db((db.sm_supervisor_level.cid==c_id) & (db.sm_supervisor_level.sup_id==rep_id)).select(db.sm_supervisor_level.level_depth_no,db.sm_supervisor_level.level_id)
            # return sLevelRows
            if not sLevelRows:
                response.flash = 'Area Not Available'
            else:
                s_level_list=[]
                level_depth_no=0
                for sRow in supLevelRows:
                    level_depth_no=sRow.level_depth_no
                    level_id=sRow.level_id
                    s_level_list.append(level_id)

                level_list=[]
                if level_depth_no==0:                    
                    level3_Rows = db((db.sm_level.cid == c_id) & (db.sm_level.level0.belongs(s_level_list))).select(db.sm_level.level0,db.sm_level.level0_name,db.sm_level.level1,db.sm_level.level2,db.sm_level.level3, orderby=db.sm_level.level_id,groupby=db.sm_level.level_id|db.sm_level.level0|db.sm_level.level1|db.sm_level.level2|db.sm_level.level3)   
                    for d_Row1 in level3_Rows:
                        level0_id = d_Row1.level0
                        level1_id = d_Row1.level1
                        level2_id = d_Row1.level2
                        level3_id = d_Row1.level3
                        division_count.append(level0_id)
                        if str(level2_id) != '':
                            zone_count.append(level1_id)
                        if str(level2_id) != '':
                            area_count.append(level2_id)
                        if str(level3_id) != '':
                            territory_count.append(level3_id)
                            
                        # tl_name = d_Row1.level_name

                        # dictData1 = {'tl_id': tl_id, 'tl_name': tl_name}
                        # level_list.append(dictData1)

                if level_depth_no == 1:
                    level3_Rows = db((db.sm_level.cid == c_id) & (db.sm_level.level1.belongs(s_level_list))).select(db.sm_level.level0,db.sm_level.level0_name,db.sm_level.level1,db.sm_level.level2,db.sm_level.level3, orderby=db.sm_level.level_id,groupby=db.sm_level.level_id|db.sm_level.level0|db.sm_level.level1|db.sm_level.level2|db.sm_level.level3)   
                    # return db._lastsql
                    for d_Row1 in level3_Rows:
                        level0_id = d_Row1.level0
                        level1_id = d_Row1.level1
                        level2_id = d_Row1.level2
                        level3_id = d_Row1.level3
                        division_count.append(level0_id)
                        zone_count.append(level1_id)
                        if str(level2_id) != '':
                            area_count.append(level2_id)
                        if str(level3_id) != '':
                            territory_count.append(level3_id)

                        # dictData1 = {'tl_id': tl_id, 'tl_name': tl_name}
                        # level_list.append(dictData1)
                    # return level_list
                if level_depth_no==2:                                        
                    level3_Rows = db((db.sm_level.cid == c_id) & (db.sm_level.level2.belongs(s_level_list))).select(db.sm_level.level0,db.sm_level.level0_name,db.sm_level.level1,db.sm_level.level2,db.sm_level.level3, orderby=db.sm_level.level_id,groupby=db.sm_level.level_id|db.sm_level.level0|db.sm_level.level1|db.sm_level.level2|db.sm_level.level3)        
                    for d_Row1 in level3_Rows:
                        level0_id = d_Row1.level0
                        level1_id = d_Row1.level1
                        level2_id = d_Row1.level2
                        level3_id = d_Row1.level3
                        division_count.append(level0_id)
                        zone_count.append(level1_id)
                        area_count.append(level2_id)
                        if str(level3_id) != '':
                            territory_count.append(level3_id)

                        # dictData1 = {'tl_id': tl_id, 'tl_name': tl_name}
                        # level_list.append(dictData1)
            # return division_count
            session.level_list=level_list
            # return len(area_count)
            session.division_count = len(set(division_count)) 
            session.zone_count = len(set(zone_count))
            session.area_count = len(set(area_count))
            session.territory_count = len(set(territory_count))
        else:
            pass
 
 # =========RX Type=============

        seen_rx_type_list = []        
        rx_typeRows = db((db.seen_rx_type.cid == c_id) ).select(db.seen_rx_type.name,groupby=db.seen_rx_type.name)
        # return rx_typeRows
        if not rx_typeRows:
            response.flash = 'Rx Type Not Available'
        else:
            for rXRow in rx_typeRows:
                rXRow_name=rXRow.name                
                dictData = {'name': rXRow_name}
                seen_rx_type_list.append(dictData)

        session.seen_rx_type_list=seen_rx_type_list        
       
        level_area_id_list = []
        for i in range(len(level_area_list)):
            level_area_str = level_area_list[i]
            level_area_id_list.append(level_area_str['area_id'])

        session.level_area_id_list = level_area_id_list
        
    # return session.from_date
    # return level_area_list
    redirect(URL(c='doctor_wise_report', f='home'))

    # ===========================================================

  
def home():
    # return session.sch_level_search
    if session.cid=='' or session.cid==None:
        redirect(URL(c='report_seen_rx_mobile',f='index'))

    division_list = session.division_list
    zone_list = session.zone_list
    area_list = session.area_list
    # return zone_list
    zlevel_list = session.zlevel_list
    level_area_list = session.level_area_list
    seen_rx_type_list = session.seen_rx_type_list
    level_list = session.level_list
    user_type = session.user_type
    search_item_id_name=session.search_item_id_name

  
    rec_item = db(db.seen_rx_brand.cid == session.cid).select(db.seen_rx_brand.brand_name, orderby=db.seen_rx_brand.brand_name,groupby=db.seen_rx_brand.brand_name)
    btn_report=request.vars.btn_report
    btn_reset = session.btn_reset
    # return int(session.level_depth_no)
    doctor_type_record =''
    # doctor_type_record_sql = "SELECT doc_type_name from doc_type where cid = '"+str(session.cid)+"' group by doc_type_name"
    # doctor_type_record = db.executesql(doctor_type_record_sql, as_dict = True)

    if btn_report=='Show' :
        # return error_flag
        error_flag=0
        if (int(session.level_depth_no) > 0):
        # return 'sch_zone_search: '+ str(session.sch_zone_search)  +' sch_level_search: ' +str(session.sch_level_search) +'sch_area_search:' + str(session.sch_area_search)
            if (((str(session.sch_zone_search)=='') or (str(session.sch_zone_search)=='None') or (str(session.sch_zone_search)==None)) and ((str(session.sch_level_search)=='') or (str(session.sch_level_search)=='None') or (str(session.sch_level_search)==None)) and ((str(session.sch_area_search)=='') or  (str(session.sch_area_search)=='None') or (str(session.sch_area_search)==None)) ):
                error_flag=1
        if (error_flag==1):
            redirect(URL(f='index',vars=dict(cid=session.cid,rep_id=session.user_id,rep_pass=session.rep_pass)))

        session.flash ='Please select mandatory fields to show data.'

        rx_u_count=0
        rec_item=0
        search_item_id_name=search_item_id_name
        user_type=session.user_type
        records=''
        
        zlevel_list=[]
        level_list=[]
        level_area_list=[]
        seen_rx_type_list=[]
        recordsH=''
        # return recordsH
        redirect(URL(f='index',vars=dict(cid=session.cid,rep_id=session.user_id,rep_pass=session.rep_pass)))
    else:
        pass

    if btn_reset == 'Reset':
        # return 'reset button click'
        # session.from_date = ''
        # session.to_date = ''
        session.sch_level_search = ''
        session.sch_zone_search = ''
        session.sch_area_search = ''
        session.sch_territory = ''
        session.sch_rx_type_search = ''
        session.search_item_id_name_search = ''
        # doctor_recordsH = 0
        # rx_u_count = 0
        redirect(URL(f='index',vars=dict(cid=session.cid,rep_id=session.user_id,rep_pass=session.rep_pass)))
    
    from_date = current_date
    to_date = current_date

    from datetime import datetime
    d1 = datetime.strptime(str(from_date), "%Y-%m-%d")
    d2 = datetime.strptime(str(to_date), "%Y-%m-%d")

    delta = d2 - d1
    date_diff=delta.days
    if (int(date_diff)>31):
       redirect(URL(f='index',vars=dict(cid=session.cid,rep_id=session.user_id,rep_pass=session.rep_pass)))

    else:
        pass

    session.btn_report = 'YES'

    zone_name=''
    reg_name=''
    tl_name=''

    qset=db()
    qset=qset(db.sm_prescription_seen_details.cid == session.cid)
    qset=qset(db.sm_prescription_seen_head.cid == session.cid)
    qset=qset(db.sm_prescription_seen_head.sl == db.sm_prescription_seen_details.sl)
    qset=qset(db.sm_prescription_seen_head.area_id == db.sm_prescription_seen_details.area_id)
    
    if session.user_type=='rep':
        qset = qset(db.sm_prescription_seen_details.submit_by_id == session.rep_id)

    
    if session.from_date!='' and session.to_date!='':
        qset = qset((db.sm_prescription_seen_details.submit_date >= session.from_date) & (db.sm_prescription_seen_details.submit_date <= session.to_date))
    
    if session.sch_level_search!='' and session.sch_level_search!=None and session.sch_level_search!='None':
        qset = qset(db.sm_prescription_seen_head.zone_id==session.sch_level_search)

    if session.sch_zone_search!='' and session.sch_zone_search!=None and session.sch_zone_search!='None':
        qset = qset(db.sm_prescription_seen_head.reg_id==session.sch_zone_search)

    if session.sch_area_search!='' and session.sch_area_search!=None and session.sch_area_search!='None':
        qset = qset(db.sm_prescription_seen_head.tl_id==session.sch_area_search)

    if session.sch_territory!='' and session.sch_territory!=None and session.sch_territory!='None':
        qset = qset(db.sm_prescription_seen_details.area_id==session.sch_territory)
    
    # if (((str(session.sch_zone_search)=='') or (str(session.sch_zone_search)=='None') or (str(session.sch_zone_search)==None)) and ((str(session.sch_level_search)=='') or (str(session.sch_level_search)=='None') or (str(session.sch_level_search)==None)) and ((str(session.sch_area_search)=='') or (str(session.sch_area_search)=='None') or (str(session.sch_area_search)==None))):
    #     qset = qset(db.sm_prescription_seen_details.area_id.belongs(session.level_area_id_list))

    if session.sch_rx_type_search!='' and session.sch_rx_type_search!=None:
        qset = qset(db.sm_prescription_seen_head.rx_type.like('%'+session.sch_rx_type_search+'%',escape=None) )

    if session.search_item_id_name_search!='' and session.search_item_id_name_search!=None and session.search_item_id_name_searc!='None':
        qset = qset(db.sm_prescription_seen_details.medicine_name==session.search_item_id_name_search)

    records=qset.select(db.sm_prescription_seen_head.area_id, db.sm_prescription_seen_head.area_name,db.sm_prescription_seen_head.tl_name,db.sm_prescription_seen_head.reg_name,db.sm_prescription_seen_head.zone_name,db.sm_prescription_seen_head.rx_type,db.sm_prescription_seen_details.submit_by_id,db.sm_prescription_seen_details.submit_by_name,db.sm_prescription_seen_details.area_id,db.sm_prescription_seen_details.medicine_name,db.sm_prescription_seen_details.id.count(), db.sm_prescription_seen_details.doctor_id, db.sm_prescription_seen_details.doctor_name, groupby=db.sm_prescription_seen_details.doctor_id|db.sm_prescription_seen_details.submit_by_id,orderby=db.sm_prescription_seen_details.submit_by_id|db.sm_prescription_seen_details.doctor_id)
    # return db._lastsql

    qsetH = db()
    # qsetH = qsetH(db.sm_prescription_seen_head.cid == session.cid)

    if session.user_type=='rep':
        qsetH = qsetH(db.sm_prescription_seen_head.submit_by_id == session.rep_id)
   
    if session.from_date!='' and session.to_date!='':
        qsetH = qsetH((db.sm_prescription_seen_head.submit_date >= session.from_date) & (db.sm_prescription_seen_head.submit_date <= session.to_date))
        
    qsetH=qsetH(db.sm_prescription_seen_details.cid == session.cid)
    qsetH=qsetH(db.sm_prescription_seen_head.cid == session.cid)
    qsetH=qsetH(db.sm_prescription_seen_head.sl == db.sm_prescription_seen_details.sl)
    qsetH=qsetH(db.sm_prescription_seen_head.area_id == db.sm_prescription_seen_details.area_id)
    
    if session.user_type=='rep':
        qsetH = qsetH(db.sm_prescription_seen_details.submit_by_id == session.rep_id)

    if session.from_date!='' and session.to_date!='':
        qsetH = qsetH((db.sm_prescription_seen_details.submit_date >= session.from_date) & (db.sm_prescription_seen_details.submit_date <= session.to_date))
   
    if session.sch_level_search!='' and session.sch_level_search!=None and session.sch_level_search!='None':
        qsetH = qsetH(db.sm_prescription_seen_head.zone_id==session.sch_level_search)

    if session.sch_zone_search!='' and session.sch_zone_search!=None and session.sch_zone_search!='None':
        qsetH = qsetH(db.sm_prescription_seen_head.reg_id==session.sch_zone_search)

    if session.sch_area_search!='' and session.sch_area_search!=None and session.sch_area_search!='None':
        qsetH = qsetH(db.sm_prescription_seen_head.tl_id==session.sch_area_search)

    if session.sch_territory!='' and session.sch_territory!=None and session.sch_territory!='None':
        qsetH = qsetH(db.sm_prescription_seen_details.area_id==session.sch_territory) 

    if (((str(session.sch_zone_search)=='') or (str(session.sch_zone_search)=='None') or (str(session.sch_zone_search)==None)) and ((str(session.sch_level_search)=='') or (str(session.sch_level_search)=='None') or (str(session.sch_level_search)==None)) and ((str(session.sch_area_search)=='') or (str(session.sch_area_search)=='None') or (str(session.sch_area_search)==None))):
        qsetH = qsetH(db.sm_prescription_seen_details.area_id.belongs(session.level_area_id_list))

    # return session.sch_rx_type_search
    if session.sch_rx_type_search!='' and session.sch_rx_type_search!=None and session.sch_rx_type_search!='None':

        try:
            qsetH = qsetH(db.sm_prescription_seen_head.rx_type.like('%'+session.sch_rx_type_search+'%', escape=None))
            # return "ff"
            # qsetH =  (db.sm_prescription_seen_head.rx_type==session.sch_rx_type_search)
        except:
            pass

    if session.search_item_id_name_search!='' and session.search_item_id_name_search!=None and session.search_item_id_name_search!='None':
        qsetH = qsetH(db.sm_prescription_seen_details.medicine_name==session.search_item_id_name_search)
    # return qsetH
    doctor_recordsH = qsetH.select(db.sm_prescription_seen_details.doctor_id,distinct=True,groupby=db.sm_prescription_seen_details.doctor_id)
    # return db._lastsql
    doctor_recordsH = len(doctor_recordsH)

    record_sql = "select count(*)"

    qset_rx=db()
    # qset_rx=qset_rx(db.sm_prescription_seen_details.cid == session.cid)
    qset_rx=qset_rx(db.sm_prescription_seen_head.cid == session.cid)
    qset_rx=qset_rx(db.sm_prescription_seen_head.sl == db.sm_prescription_seen_details.sl)
    qset_rx=qset_rx(db.sm_prescription_seen_head.area_id == db.sm_prescription_seen_details.area_id)
    
    if session.user_type=='rep':
        qset_rx = qset_rx(db.sm_prescription_seen_details.submit_by_id == session.rep_id)

    if session.from_date!='' and session.to_date!='':
        qset_rx = qset_rx((db.sm_prescription_seen_details.submit_date >= session.from_date) & (db.sm_prescription_seen_details.submit_date <= session.to_date))
   
    if session.sch_level_search!='' and session.sch_level_search!=None and session.sch_level_search!='None':
        qset_rx = qset_rx(db.sm_prescription_seen_head.zone_id==session.sch_level_search)

    if session.sch_zone_search!='' and session.sch_zone_search!=None and session.sch_zone_search!='None':
        qset_rx = qset_rx(db.sm_prescription_seen_head.reg_id==session.sch_zone_search)

    if session.sch_area_search!='' and session.sch_area_search!=None and session.sch_area_search!='None':
        qset_rx = qset_rx(db.sm_prescription_seen_head.tl_id==session.sch_area_search)

    if session.sch_territory!='' and session.sch_territory!=None and session.sch_territory!='None':
        qset_rx = qset_rx(db.sm_prescription_seen_details.area_id==session.sch_territory)

    if (((str(session.sch_zone_search)=='') or (str(session.sch_zone_search)=='None') or (str(session.sch_zone_search)==None)) and ((str(session.sch_level_search)=='') or (str(session.sch_level_search)=='None') or (str(session.sch_level_search)==None)) and ((str(session.sch_area_search)=='') or (str(session.sch_area_search)=='None') or (str(session.sch_area_search)==None))):
        qset_rx = qset_rx(db.sm_prescription_seen_details.area_id.belongs(session.level_area_id_list))

    if session.sch_rx_type_search!='' and session.sch_rx_type_search!=None  and session.sch_rx_type_search!='None':
        qset_rx = qset_rx(db.sm_prescription_seen_head.rx_type.like('%'+session.sch_rx_type_search+'%', escape=None))

    if session.search_item_id_name_search!='' and session.search_item_id_name_search!=None and session.search_item_id_name_search!='None':
        qset_rx = qset_rx(db.sm_prescription_seen_details.medicine_name==session.search_item_id_name_search)

    rx_u_count = qset_rx.select(db.sm_prescription_seen_head.sl, distinct= True, groupby=db.sm_prescription_seen_head.sl)
    # return db._lastsql
    rx_u_count = len(rx_u_count)

    return dict(cid=session.cid,rep_id=session.user_id,rep_pass=session.rep_pass,rx_u_count=rx_u_count,rec_item=rec_item,search_item_id_name=search_item_id_name,user_type=user_type,records=records,doctor_recordsH=doctor_recordsH,zlevel_list=zlevel_list,level_list=level_list,level_area_list=level_area_list,seen_rx_type_list=seen_rx_type_list, division_list= division_list, zone_list = zone_list, doctor_type_record = doctor_type_record, area_list = area_list)



def doctor_wise_report_details():
    cid = session.cid
    response.title = 'Doctor Wise Report Details'
    from_date = session.from_date
    to_date = session.to_date
    submited_by_id = request.args(0)
    area_id = request.args(1)
    doctor_id = request.args(2)
    doc_type_name = request.args(3)
    doctor_name = request.args(4)
    # return submited_by_id, area_id, doctor_id, doc_type_name, doctor_name
    medicine_condition = ''
    medicine_name = str(session.search_item_id_name_search).replace('None','')
    if medicine_name != '':
        doctor_record_sql = "SELECT a.image_name as image, b.submit_date as submit_date, b.medicine_name as medicine_name  FROM sm_prescription_seen_head a INNER JOIN  sm_prescription_seen_details b ON a.cid = b.cid and a.sl = b.sl WHERE a.cid = '"+cid+"' and b.submit_by_id = '"+str(submited_by_id)+"' and b.area_id = '"+str(area_id)+"' and b.doctor_id = '"+str(doctor_id)+"' and b.medicine_name = '"+str(medicine_name)+"' and b.submit_date >= '"+from_date+"' and b.submit_date <= '"+to_date+"' order by b.submit_date ;"
    else:
        doctor_record_sql = "SELECT a.image_name as image, b.submit_date as submit_date, b.medicine_name as medicine_name  FROM sm_prescription_seen_head a INNER JOIN  sm_prescription_seen_details b ON a.cid = b.cid and a.sl = b.sl WHERE a.cid = '"+cid+"' and b.submit_by_id = '"+str(submited_by_id)+"' and b.area_id = '"+str(area_id)+"' and b.doctor_id = '"+str(doctor_id)+"' and b.submit_date >= '"+from_date+"' and b.submit_date <= '"+to_date+"' order by b.submit_date ;"
    doctor_records = db.executesql(doctor_record_sql, as_dict = True)

    return dict(doctor_records = doctor_records, doc_type_name = doc_type_name, doctor_name = doctor_name)


def prescription_view():
    cid = session.cid
    response.title = 'Prescription View'

    # Get the image URL from the request
    image_url = request.args(0)

    return dict(image_url=image_url)




def get_zone():
    retStr=''
    c_id = session.cid
    region=str(request.vars.region)
    
    records=db((db.sm_level.cid == c_id)&(db.sm_level.level0 == region)&(db.sm_level.depth == 1)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
    for row in records:
        level_id=str(row.level_id)
        level_name=str(row.level_name)
        
        if retStr=='':
            retStr=level_id+'<fd>'+level_name
        else:
            retStr+='<rd>'+level_id+'<fd>'+level_name
        
    
    return retStr

def get_area():
    retStr=''
    c_id = session.cid
    # region=str(request.vars.region)
    zone=str(request.vars.zone)
    
    records=db((db.sm_level.cid == c_id)&(db.sm_level.level1 == zone)&(db.sm_level.depth == 2)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
    # return db._lastsql
    for row in records:
        level_id=str(row.level_id)
        level_name=str(row.level_name)
        
        if retStr=='':
            retStr=level_id+'<fd>'+level_name
        else:
            retStr+='<rd>'+level_id+'<fd>'+level_name
        
    
    return retStr


def get_territory():
    retStr=''
    c_id = session.cid
    # region=str(request.vars.region)
    # zone=str(request.vars.zone)
    area=str(request.vars.area)
    
    records=db((db.sm_level.cid == c_id)&(db.sm_level.level2 == area)&(db.sm_level.depth == 3)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
    #return db._lastsql
    for row in records:
        level_id=str(row.level_id)
        level_name=str(row.level_name)
        
        if retStr=='':
            retStr=level_id+'<fd>'+level_name
        else:
            retStr+='<rd>'+level_id+'<fd>'+level_name
        
    
    return retStr


def get_pocket_market():
    retStr=''
    c_id = session.cid
    # region=str(request.vars.region)
    # zone=str(request.vars.zone)
    # area=str(request.vars.area)
    territory=str(request.vars.territory)
    
    records=db((db.sm_microunion.cid == c_id)&(db.sm_microunion.level3 == territory)).select(db.sm_microunion.microunion_id, db.sm_microunion.microunion_name, orderby=db.sm_microunion.microunion_name)
    # return db._lastsql
    for row in records:
        microunion_id=str(row.microunion_id)
        microunion_name=str(row.microunion_name)
        
        if retStr=='':
            retStr=microunion_id+'<fd>'+microunion_name
        else:
            retStr+='<rd>'+microunion_id+'<fd>'+microunion_name
        
    
    return retStr

