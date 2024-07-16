
import urllib.parse
import datetime

# http://127.0.0.1:8000/hamdard/client_coverage_report/client_coverage_url?cid=Hamdard&rep_id=7206&rep_pass=55555

# http://127.0.0.1:8000/hamdard/client_coverage_report/client_coverage_url?cid=Hamdard&rep_id=itzm&rep_pass=1234       0
# http://127.0.0.1:8000/hamdard/client_coverage_report/client_coverage_url?cid=Hamdard&rep_id=9011&rep_pass=1234       1
# http://127.0.0.1:8000/hamdard/client_coverage_report/client_coverage_url?cid=Hamdard&rep_id=6987&rep_pass=1981       1
# http://127.0.0.1:8000/hamdard/client_coverage_report/client_coverage_url?cid=Hamdard&rep_id=9001&rep_pass=1234       3

# http://w05.yeapps.com/hamdard/client_coverage_report/client_coverage_url?cid=Hamdard&rep_id=7206&rep_pass=55555
# http://w05.yeapps.com/hamdard/client_coverage_report/client_coverage_url?cid=Hamdard&rep_id=9011&rep_pass=1234
# http://w05.yeapps.com/hamdard/client_coverage_report/client_coverage_url?cid=Hamdard&rep_id=6987&rep_pass=1981



#========================= CLIENT COVERAGE URL FUNCTION ==========================#

def client_coverage_url():
    session.btn_filter = None
    session.btn_all = None
    session.btn_filter=None
    session.levelIdstr=''
    session.divisionIdstr=''
    session.zoneIdstr=''
    session.areaIdstr=''
    session.category_nameIdstr=''
    session.item_nameIdstr=''
    session.searchType_coverage=''
    session.searchValue_coverage=''
    session.category_name = ''
    session.sql = ''

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()    
    rep_pass = str(request.vars.rep_pass).strip()
        
    session.cid = cid 
    session.rep_id = rep_id 
    session.rep_pass = rep_pass 

    # cid =  session.cid
    # rep_id = session.rep_id
    # rep_pass = session.rep_pass

    date_from = current_date
    now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    date_ton = now + datetime.timedelta(days = 1)
    date_to = str(date_ton).split(' ')[0]

    session.from_dt = date_from
    session.to_date = date_from

    btn_filter = request.vars.btn_filter
    btn_all = request.vars.btn_all
    reqPage = len(request.args)
    
    # levelId_name = ''
    # division_name = ''
    depth = 0
    level_id = ''
    level = ''
    level_list_str = []
    level_id_str = ''
    area_id_list = []
    area_id_str = ''

    check_user_type_sql = "SELECT user_type FROM sm_rep WHERE cid = '"+cid+"' and rep_id = '"+str(rep_id)+"' group by rep_id limit 1 ;"
    check_user_type = db.executesql(check_user_type_sql, as_dict = True)

    for c in range(len(check_user_type)):
        user_rec = check_user_type[c]
        user_type = user_rec["user_type"]

    session.user_type = user_type
    
    if user_type == 'rep':
        depth = 3
    
    else:
        check_sup_level_sql = "SELECT level_depth_no,level_id FROM sm_supervisor_level where cid = '"+cid+"' and sup_id = '"+str(rep_id)+"' group by sup_id limit 1 ; "
        check_sup_level = db.executesql(check_sup_level_sql, as_dict = True)

        for s in range(len(check_sup_level)):
            user_depth_rec = check_sup_level[s]
            depth = user_depth_rec["level_depth_no"]
            level_id = user_depth_rec["level_id"]
            level = 'level' +str(depth)
            level_list_str.append(level_id)

        level_id_str = str(level_list_str).replace('[', '').replace(']', '')
        session.level_id = level_id

        if depth == 0 :
            levelRecord_str_sql = 'select level_id from sm_level where cid = "'+cid+'" and level0 in ('+level_id_str+') and  is_leaf=1 group by level3 order by level_name ;'

        if depth == 1 :
            levelRecord_str_sql = 'select level_id from sm_level where cid = "'+cid+'" and level1 in ('+level_id_str+') and  is_leaf=1 group by level3 order by level_name ;'
            
        if depth == 2 :
            levelRecord_str_sql = 'select level_id from sm_level where cid = "'+cid+'" and level2 in ('+level_id_str+') and  is_leaf=1 group by level3 order by level_name ;'
           
        levelRecord_str = db.executesql(levelRecord_str_sql, as_dict=True)

        for l in range(len(levelRecord_str)):
            levelRecordsStr = levelRecord_str[l]
            area_id = str(levelRecordsStr['level_id'])
            area_id_list.append(area_id)

        area_id_str = str(area_id_list).replace('[', '').replace(']', '')

    session.depth = depth
    session.area_id_str = area_id_str

    divisionIdstr = ''
    levelIdstr = ''
    zoneIdstr = ''
    areaIdstr = ''
    repIdstr = ''
    clientIdstr = ''
    category_nameIdstr = ''
    # item_nameIdstr = ''
    
    if btn_filter:
        category_name = str(request.vars.category_name)
        searchType_coverage = str(request.vars.search_type).strip()
        searchValue_coverage = str(request.vars.search_value).strip().upper()

        session.searchType_coverage = searchType_coverage
        session.searchValue_coverage = searchValue_coverage

        # if (session.date_from!=''  and session.date_to != ''):
            # qset = qset((db.sm_prescription_seen_head.submit_date >= session.date_from) & (db.sm_prescription_seen_head.submit_date <= session.date_to))
            # qset = qset(db.sm_prescription_seen_head.submit_date <= session.date_to)
        
        if (session.searchType_coverage == 'RegionID'):
            # searchValue=str(session.searchValue_coverage).split('|')[0]
            try:
                divisionIdstr = str(session.searchValue_coverage).split('|')[0]
            except:
                divisionIdstr = ''
            # qset = qset(db.sm_prescription_seen_head.zone_id == searchValue)

        elif (session.searchType_coverage == 'ZoneID'):
            # searchValue=str(session.searchValue_coverage).split('|')[0]
            try:
                zoneIdstr = str(session.searchValue_coverage).split('|')[0]
            except:
                zoneIdstr = ''
            # qset = qset(db.sm_prescription_seen_head.reg_id == searchValue)

        elif (session.searchType_coverage == 'TlID'):
            try:
                areaIdstr = str(session.searchValue_coverage).split('|')[0]
            except:
                areaIdstr = ''

        elif (session.searchType_coverage == 'RouteID'):
            # searchValue=str(session.searchValue_coverage).split('|')[0]
            try: 
                levelIdstr = str(session.searchValue_coverage).split('|')[0]
            except:
                levelIdstr = ''
            # qset = qset(db.sm_prescription_seen_head.tl_id == searchValue)

        # elif (session.searchType_coverage == 'RouteID'):
        #     searchValue=str(session.searchValue_coverage).split('|')[0]
            # qset = qset(db.sm_prescription_seen_head.area_id == searchValue)
            
        elif (session.searchType_coverage == 'RepID'):
            searchValue=str(session.searchValue_coverage).split('|')[0]
            try: 
                repIdstr = str(session.searchValue_coverage).split('|')[0]
            except:
                repIdstr = ''
            # qset = qset(db.sm_prescription_seen_head.submit_by_id == searchValue)

        elif (session.searchType_coverage == 'ClientID'):
            searchValue=str(session.searchValue_coverage).split('|')[0]
            try: 
                clientIdstr = str(session.searchValue_coverage).split('|')[0]
            except:
                clientIdstr = ''

        if (category_name!='' or category_name!=None or category_name!='None'):
            try:
                category_nameIdstr = str(category_name).split('|')[0]
            except:
                category_nameIdstr = category_name
        
        session.btn_filter = btn_filter
        session.levelIdstr = levelIdstr
        session.divisionIdstr = divisionIdstr
        session.zoneIdstr = zoneIdstr
        session.areaIdstr = areaIdstr
        session.repIdstr = repIdstr
        session.clientIdstr = clientIdstr
        session.category_nameIdstr = category_nameIdstr
        # session.item_nameIdstr=item_nameIdstr
        # session.division_name = division_name
        # session.zone_name = zone_name
        # session.area_name = area_name
        session.levelId_name = searchValue_coverage
        session.category_name = category_name
        
        from_dt = str(request.vars.to_dt_2).strip().upper()
        to_date= str(request.vars.to_dt_3).strip().upper()
        dateFlag=True
        
        try:
            from_dt=datetime.datetime.strptime(str(from_dt),'%Y-%m-%d')
            to_date=datetime.datetime.strptime(str(to_date),'%Y-%m-%d')
            session.from_dt=str(from_dt).split(' ')[0]
            session.to_date=str(to_date).split(' ')[0]
        except:
            session.from_dt=''
            session.to_date=''
            dateFlag=False

        reqPage=0
   
    elif btn_all:
        session.btn_filter=None
        session.btn_all=btn_all
        session.from_dt=date_from
        session.to_date=date_from
        session.levelIdstr=''
        session.divisionIdstr=''
        session.zoneIdstr=''
        session.areaIdstr=''
        session.category_nameIdstr=''
        session.item_nameIdstr=''
        session.searchType_coverage=''
        session.searchValue_coverage=''
        # session.division_name = ''
        # session.zone_name = ''
        # session.area_name = ''
        # session.levelId_name = ''
        session.category_name = ''
        session.sql = ''
        reqPage=0

    redirect(URL(c='client_coverage_report',f='client_coverage_rpt'))


#========================= CLIENT COVERAGE FUNCTION ==========================#

def client_coverage_rpt():   
    response.title = 'Client Coverage'

    cid = session.cid 
    rep_id = session.rep_id 
    rep_pass = session.rep_pass    
    date_from = session.from_dt    
    date_to = session.to_date
    levelIdstr = session.levelIdstr
    divisionIdstr = session.divisionIdstr
    zoneIdstr = session.zoneIdstr
    areaIdstr = session.areaIdstr
    repIdstr = session.repIdstr
    clientIdstr = session.clientIdstr
    category_nameIdstr = session.category_nameIdstr
    
    btn_filter = request.vars.btn_filter        
    btn_all = request.vars.btn_all
    # vChecklist = []
    # vCountList = []
    # data_list = []
    # records_ov = ''
    # invRecords = ''
    total_client = 0  
    unique_client_cover_show = 0  
    unique_client_cover_per = 0  
    total_scheduled_client = 0
    total_actual_client_call = 0 
    # area_ids_str=''
    data_rec = {}

    #--------paging
    # reqPage=len(request.args)

    # if reqPage:
    #     page=int(request.args[0])
    # else:
    #     page=0

    # items_per_page = 5
    # # items_per_page=100
    # limitby=(page*items_per_page,(page+1)*items_per_page)
    #--------end paging 
    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == rep_pass)  & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
    
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = str(repRow[0].user_type)
        # records_ov=''  

        #=============Total Client===============
        if (user_type=='rep'):
            repAreaRow = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.rep_id == rep_id)).select(db.sm_rep_area.area_id,orderby=db.sm_rep_area.area_id,groupby=db.sm_rep_area.area_id)
            
            if not repAreaRow:
               retStatus = 'FAILED<SYNCDATA>Invalid Area'
               return retStatus
            else:
                rp_areaList=[]
                repAreaStr=''
                for repAreaRow in repAreaRow:
                    repArea_id=repAreaRow.area_id
                    rp_areaList.append(repArea_id)
                    if repAreaStr=='':
                        repAreaStr="'"+str(repArea_id)+"'"
                    else:
                        repAreaStr=repAreaStr+",'"+str(repArea_id)+"'" 

            condition=""
            condition="and area_id IN ("+str(repAreaStr)+")" 

            clientRecords_str = "SELECT count(client_id) as total_client FROM sm_client WHERE cid = '" + str(cid) + "' " + condition + " AND status = 'ACTIVE' GROUP BY client_id ;"
            # return clientRecords_str
            clientRecords = db.executesql(clientRecords_str, as_dict=True)
            total_client = 0
            for i in range(len(clientRecords)):
                clientRecords_str = clientRecords[i]               
                total_client = clientRecords_str['total_client']
            
        else:                
            levelList = []
            marketList = []
            spicial_codeList = []
            marketStr = ''
            
            SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)
            
            for SuplevelRows in SuplevelRows:
                Suplevel_id = SuplevelRows.level_id
                depth = SuplevelRows.level_depth_no
                level = 'level' + str(depth)
                if Suplevel_id not in levelList:
                    levelList.append(Suplevel_id)
            
            for i in range(len(levelList)):
                levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)

                for levelRow in levelRows:
                    level_id = levelRow.level_id
                    if marketStr=='':
                        marketStr="'"+str(level_id)+"'"
                    else:
                        marketStr=marketStr+",'"+str(level_id)+"'"
            
            condition=''
            condition=condition+" AND area_id IN ("+str(marketStr)+")"
        
        if ((session.btn_filter) and (session.date_from!='') and (session.date_to!='')):
            condition_c = ''    
            condition_d = ''
            condition_o = ''    
            condition_catagory = ''
            territory_id_list=''
            
            if divisionIdstr != '':
                condition_d = " AND level0_id =  '"+str(divisionIdstr)+"'"
                levelRows = db((db.sm_level.cid == cid)& (db.sm_level.level0 == divisionIdstr)&(db.sm_level.is_leaf==1) ).select(db.sm_level.level3,db.sm_level.level3_name)
                
                for levelRow in levelRows:
                    level_id = levelRow.level3
                    if territory_id_list=='':
                        territory_id_list="'"+str(level_id)+"'"
                    else:
                        territory_id_list=territory_id_list+",'"+str(level_id)+"'"  
            
            if zoneIdstr != '':
                condition_d += " AND level1_id =  '"+str(zoneIdstr)+"'"
                levelRows = db((db.sm_level.cid == cid)& (db.sm_level.level1 == zoneIdstr)&(db.sm_level.is_leaf==1) ).select(db.sm_level.level3,db.sm_level.level3_name)
                for levelRow in levelRows:
                    level_id = levelRow.level3
                    if territory_id_list=='':
                        territory_id_list="'"+str(level_id)+"'"
                    else:
                        territory_id_list=territory_id_list+",'"+str(level_id)+"'" 
            
            if areaIdstr != '':
                condition_d += " AND level2_id =  '"+str(areaIdstr)+"'"
                levelRows = db((db.sm_level.cid == cid)& (db.sm_level.level2 == areaIdstr)&(db.sm_level.is_leaf==1) ).select(db.sm_level.level3,db.sm_level.level3_name)
                for levelRow in levelRows:
                    level_id = levelRow.level3
                    if territory_id_list=='':
                        territory_id_list="'"+str(level_id)+"'"
                    else:
                        territory_id_list=territory_id_list+",'"+str(level_id)+"'" 

            if levelIdstr != '':
                condition_d += " AND level3_id =  '"+str(levelIdstr)+"'"

                if territory_id_list != '' :
                    territory_id_list += territory_id_list+",'"+str(levelIdstr)+"'"
                else:
                    territory_id_list = "'"+str(levelIdstr)+"'"

            if repIdstr != '':
                condition_d += " AND rep_id =  '"+str(repIdstr)+"'"

                # find area list under mso_id
                area_sql = "SELECT rep_id, area_id FROM sm_rep_area WHERE cid = '"+str(cid)+"' "+condition_d+";"
                area_rec = db.executesql(area_sql, as_dict = True)

                # area_ids_str += "(" + ", ".join("'" + str(area_rec[i]['area_id']) + "'" for i in range(len(area_rec))) + ")"
                # return area_ids_str

                for i in range(len(area_rec)):
                    area_data = area_rec[i]
                    area_id = area_data['area_id']

                    if territory_id_list != '' :
                        territory_id_list += territory_id_list+",'"+str(area_id)+"'"
                    else:
                        territory_id_list = "'"+str(area_id)+"'"

            if clientIdstr != '':
                condition_d += " AND client_id =  '"+str(clientIdstr)+"'"

                # find area under client
                area_sql = "SELECT client_id, area_id FROM sm_client WHERE cid = '"+str(cid)+"' "+condition_d+" AND status = 'ACTIVE';"
                area_rec = db.executesql(area_sql, as_dict = True)

                for i in range(len(area_rec)):
                    area_data = area_rec[i]
                    area_id = area_data['area_id']

                    if territory_id_list != '' :
                        territory_id_list += territory_id_list+",'"+str(area_id)+"'"
                    else:
                        territory_id_list = "'"+str(area_id)+"'"
                
            if category_nameIdstr != '':
                if condition_d == '':
                    condition_d = condition
                condition_d += " AND cl_category_id LIKE '%" +str(category_nameIdstr)+"%'"
                condition_c += " AND category_id LIKE '%"+str(category_nameIdstr)+"%'"
                condition_o += " AND client_cat LIKE '%"+str(category_nameIdstr)+"%'"

            if territory_id_list != '':
                condition_c += " AND area_id in ("+str(territory_id_list)+")"
                condition_o += " AND area_id in ("+str(territory_id_list)+")"
            else:
                condition_c += condition 
                condition_o += condition
            
            # return condition_c
            #============= TOTAL Client Cover ===============
            if condition_c != '':
                clientRecords_str = "SELECT count(client_id) as total_client FROM sm_client WHERE cid = '" + str(cid) + "' " + condition_c + " AND status = 'ACTIVE' GROUP BY client_id ;"
                # return clientRecords_str
                clientRecords = db.executesql(clientRecords_str, as_dict=True)
                total_client = 0
                for i in range(len(clientRecords)):
                    clientRecords_str = clientRecords[i]               
                    total_client=total_client+1
            
            else:
                clientRecords_str = "SELECT count(client_id) as total_client FROM sm_client WHERE cid = '" + str(cid) + "' " + condition + " AND status = 'ACTIVE' GROUP BY client_id ;"
                clientRecords = db.executesql(clientRecords_str, as_dict=True)
               
                total_client = 0
                for i in range(len(clientRecords)):
                    clientRecords_str = clientRecords[i]               
                    total_client=total_client+1

            #============= Unique Client Cover ===============
            if condition_d != '':
                client_RecordsStr = "SELECT count(distinct(client_id)) as unique_client_cover FROM sm_invoice_head WHERE cid = '" + str(cid) + "'   AND invoice_date >= '" + str(date_from) + "' AND invoice_date <= '" + str(date_to) + "' " + condition_d + " AND return_count!='1' AND status = 'Invoiced' GROUP BY client_id;"
                client_Records = db.executesql(client_RecordsStr, as_dict=True)
               
                unique_client_cover_show = 0
                for i in range(len(client_Records)):
                    unique_client_cover_show=unique_client_cover_show+1
            
            else:
                client_RecordsStr = "SELECT count(distinct(client_id)) as unique_client_cover  FROM sm_invoice_head WHERE cid = '" + str(cid) + "'  AND invoice_date >= '" + str(date_from) + "' AND invoice_date <= '" + str(date_to) + "' " + condition + "  AND return_count!='1' AND status = 'Invoiced' GROUP BY client_id;"
                client_Records = db.executesql(client_RecordsStr, as_dict=True)

                unique_client_cover_show = 0
                for i in range(len(client_Records)):
                    unique_client_cover_show=unique_client_cover_show+1                            
            
            #============= Client Cover Percentage =============== 
            try: 
                unique_client_cover= (float(unique_client_cover_show) / float(total_client))
                unique_client_cover_p=float(unique_client_cover*100)
                unique_client_cover_per=round((unique_client_cover_p),2)
            except:
                unique_client_cover_per=0
                pass

            total_outlet_covered = 0
            total_scheduled_client = 0
            total_actual_client_call = 0
            client_id = ''
            client_id_str = ''
            
            data_rec_sql = f"""SELECT 
                    COALESCE(inv.total_inv_count, 0) AS total_inv_count,
                    inv_client_rec.area_id,
                    COALESCE(inv_client_rec.total_client, 0) AS total_client,
                    COALESCE(outlet_rec.total_outlet_covered, 0) AS total_outlet_covered,
                    outlet_rec.depot_id,
                    outlet_rec.depot_name,
                    outlet_rec.level0_id,
                    outlet_rec.level0_name,
                    outlet_rec.level1_id,
                    outlet_rec.level1_name,
                    outlet_rec.level2_id,
                    outlet_rec.level2_name,
                    outlet_rec.level3_id,
                    outlet_rec.level3_name,
                    outlet_rec.client_id,
                    outlet_rec.client_name,
                    outlet_rec.rep_id,
                    outlet_rec.rep_name,
                    outlet_rec.order_date
                FROM 
                    (
                        SELECT 
                            COUNT(client_id) AS total_inv_count,
                            level3_id
                        FROM 
                            sm_invoice_head
                        WHERE 
                            cid = '{cid}' 
                            AND invoice_date >= '{str(date_from)}' 
                            AND invoice_date <= '{str(date_to)}' 
                            AND return_count != '1' 
                            AND status = 'Invoiced' 
                            {condition_d}
                        GROUP BY 
                            level3_id
                    ) AS inv
                RIGHT JOIN 
                    (
                        SELECT 
                            COUNT(id) AS total_client,
                            area_id
                        FROM 
                            sm_client
                        WHERE 
                            cid = '{cid}' 
                            {condition_c}
                            AND status = 'ACTIVE' 
                        GROUP BY 
                            area_id
                    ) AS inv_client_rec
                ON 
                    inv.level3_id = inv_client_rec.area_id
                RIGHT JOIN
                    (
                        SELECT
                            COUNT(DISTINCT(client_id)) as total_outlet_covered,
                            depot_id,
                            depot_name,
                            level0_id,
                            level0_name,
                            level1_id,
                            level1_name,
                            level2_id,
                            level2_name,
                            level3_id,
                            level3_name,
                            client_id,
                            client_name,
                            rep_id,
                            rep_name,
                            order_date
                        FROM
                            sm_order_head
                        WHERE
                            cid = '{cid}'
                            AND order_date >= '{str(date_from)}'
                            AND order_date <= '{str(date_to)}'
                            {condition_o}
                            AND status = 'Invoiced'
                            AND (visit_type = 'Scheduled' OR visit_type = 'Unscheduled')
                        GROUP BY
                            level3_id
                    ) AS outlet_rec
                ON
                    inv_client_rec.area_id = outlet_rec.level3_id
                ORDER BY 
                    total_inv_count DESC;"""
            data_rec = db.executesql(data_rec_sql, as_dict=True)
            
            session.sql = data_rec_sql

            # return dict(cid=cid,rep_id=rep_id,rep_pass=rep_pass,total_client=total_client,unique_client_cover_show=unique_client_cover_show,unique_client_cover_per=unique_client_cover_per,data_list=data_list,total_actual_client_call=total_actual_client_call,total_scheduled_client=total_scheduled_client,data_rec=data_rec)

        else:
            #=============TOTAL Client Cover===============
            clientRecords_str = "SELECT count(client_id) as total_client FROM sm_client WHERE cid = '" + str(cid) + "' " + condition + " AND status = 'ACTIVE' GROUP BY client_id ;"
            clientRecords = db.executesql(clientRecords_str, as_dict=True)
           
            total_client = 0
            for i in range(len(clientRecords)):
                clientRecords_str = clientRecords[i]               
                total_client=total_client+1

            #=============Unique Client Cover===============
            
            client_RecordsStr = "SELECT count(distinct(client_id)) as unique_client_cover  FROM sm_invoice_head WHERE cid = '" + str(cid) + "'  AND invoice_date >= '" + str(date_from) + "' AND invoice_date <= '" + str(date_to) + "' " + condition + "  AND return_count!='1' AND status = 'Invoiced' GROUP BY client_id;"
            client_Records = db.executesql(client_RecordsStr, as_dict=True)

            unique_client_cover_show = 0
            for i in range(len(client_Records)):
                unique_client_cover_show=unique_client_cover_show+1                            

            #=============Client Cover Percentage=============== 
            try: 
                unique_client_cover= (float(unique_client_cover_show) / float(total_client))
                unique_client_cover_p=float(unique_client_cover*100)
                unique_client_cover_per=round((unique_client_cover_p),2)
            except:
                unique_client_cover_per=0
                pass

            # ============ Client/Invoice ==============
        
        # if not ((session.btn_filter) and (levelIdstr=='')and (divisionIdstr=='')and (zoneIdstr=='')and (areaIdstr=='')and (category_nameIdstr=='')):
        # if session.btn_all : 
        #     sql_str="SELECT client_id,name FROM sm_client WHERE cid = '"+ str(cid) +"' AND area_id = '" + str(levelIdstr) + "' AND status = 'ACTIVE' GROUP BY client_id order by name;"                    
        #     records_ov=db.executesql(sql_str,as_dict = True)    

        #     inv_count = 0   
        #     invRecords_str = "SELECT count(client_id) as total_inv_count,level3_id,client_id,invoice_date FROM sm_invoice_head WHERE cid = '" + str(cid) + "'  AND invoice_date >= '" + str(date_from) + "' AND invoice_date <= '" + str(date_to) + "' AND area_id = '" + str(levelIdstr) + "'  AND return_count!='1' AND status = 'Invoiced' GROUP BY client_id;"
        #     invRecords = db.executesql(invRecords_str, as_dict=True)
            
        #     invRecords_str_single= ''            
        #     for i in range(len(invRecords)):
        #         invRecords_str_single = invRecords[i]
        #         vCount=invRecords_str_single['total_inv_count']
        #         vCheck=str(invRecords_str_single['client_id']) 
        #         vChecklist.append(vCheck)
        #         vCountList.append(vCount)  
    
        # return dict(cid=cid,rep_id=rep_id,rep_pass=rep_pass,records_ov=records_ov,total_client=total_client,unique_client_cover_show=unique_client_cover_show,unique_client_cover_per=unique_client_cover_per,vChecklist=vChecklist,vCountList=vCountList, invRecords=invRecords,data_list=data_list,total_actual_client_call=total_actual_client_call,total_scheduled_client=total_scheduled_client,data_rec=data_rec)

        return dict(cid=cid,rep_id=rep_id,rep_pass=rep_pass,total_client=total_client,unique_client_cover_show=unique_client_cover_show,unique_client_cover_per=unique_client_cover_per,total_actual_client_call=total_actual_client_call,total_scheduled_client=total_scheduled_client,data_rec=data_rec)



#============================================== Download

def download_data():
    cid = session.cid
    
    myString='Client Coverage Report\n\n'
    myString+='Division ID,Division Name,Zone ID,Zone Name,Area ID,Area Name,Branch ID,Branch Name,Market ID,Market Name,MSO ID, MSO Name,Inv. Count,Total Client,Client Covered,Coverage(%)\n'

    division_id = ''
    division_name = ''
    zone_id = ''
    zone_name = ''
    area_id = ''
    area_name = ''
    branch_id = ''
    branch_name = ''
    mso_id = ''
    mso_name = ''
    market_id = ''
    market_name = ''
    inv_count = 0
    total_client = 0
    client_covered = 0
    coverage = 0.00

    # return myString
    # return 'test it is : '+str(session.sql)

    if session.sql != '' and session.sql != 'None' and session.sql != None:
        data_rec_sql = session.sql
        data_rec = db.executesql(data_rec_sql, as_dict=True)

        if len(data_rec) != 0:
            for i in range(len(data_rec)):
                data = data_rec[i]
                division_id = data['level0_id']
                division_name = data['level0_name']
                zone_id = data['level1_id']
                zone_name = data['level1_name']
                area_id = data['level2_id']
                area_name = data['level2_name']
                branch_id = data['depot_id']
                branch_name = data['depot_name']
                market_id = data['level3_id']
                market_name = data['level3_name']
                mso_id = data['rep_id']
                mso_name = data['rep_name']
                inv_count = data['total_inv_count']
                total_client = data['total_client']
                client_covered = data['total_outlet_covered']
                coverage = float((float(client_covered)/float(total_client))*100)
                coverage = round((coverage),2)

                # Create string for csv download
                myString+=str(division_id)+','+str(division_name)+','+str(zone_id)+','+str(zone_name)+','+str(area_id)+','+str(area_name)+','+str(branch_id)+','+str(branch_name)+','+str(market_id)+','+str(market_name)+','+str(mso_id)+','+str(mso_name)+','+str(inv_count)+','+str(total_client)+','+str(client_covered)+','+str(coverage)+'\n'

    else:
        myString+=str(division_id)+','+str(division_name)+','+str(zone_id)+','+str(zone_name)+','+str(area_id)+','+str(area_name)+','+str(branch_id)+','+str(branch_name)+','','','','','',''\n'
    
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=client_coverage_report.csv'   
    return str(myString)



#========================= GET TERRITORY FUNCTION ==========================#

def get_territory():
    lvlStr = ''
    cid = session.cid
    rep_id = str(request.vars.rep_id).strip().upper()
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id)  & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = str(repRow[0].user_type).upper()
   
    qset=db()
    qset=qset(db.sm_level.cid==session.cid)

    if user_type == 'SUP':  
        level_rep = repRow[0].level_id
        depth = repRow[0].field2
        level = 'level' + str(depth)
        # return level
        levelList=[]
        SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)
        # return SuplevelRows
        
        levelStr=''
        for SuplevelRows in SuplevelRows:
            Suplevel_id = SuplevelRows.level_id
            depth = SuplevelRows.level_depth_no
            level = 'level' + str(depth)#+'_id'
            if Suplevel_id not in levelList:
                levelList.append(Suplevel_id)
                if levelStr=='':
                    levelStr="'"+str(Suplevel_id)+"'"
                else:
                    levelStr=levelStr+",'"+str(Suplevel_id)+"'" 
            # return levelStr
        marketStr=''
        marketStrList=[]
        for i in range(len(levelList)):

            if (level=='level0'):
                levelRows = db((db.sm_level.cid == cid) &(db.sm_level.depth == '3') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code,groupby=db.sm_level.level_id,orderby=db.sm_level.level_name)
                # return levelRows
            if (level=='level1'):
                levelRows = db((db.sm_level.cid == cid) &(db.sm_level.depth == '3')& (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code,groupby=db.sm_level.level_id,orderby=db.sm_level.level_name)
                        
            if (level=='level2'):
                levelRows = db((db.sm_level.cid == cid)  &(db.sm_level.depth == '3') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code,groupby=db.sm_level.level_id,orderby=db.sm_level.level_name)
            # return levelRows

            # levelRows = db((db.sm_level.cid == cid) & (db.sm_level.level_id.belongs(session.level_idList))).select(db.sm_level.level0, db.sm_level.level0_name, orderby=db.sm_level.level0_name, groupby=db.sm_level.level0)
            for row in levelRows:
                level_id = str(row.level_id)
                name = str(row.level_name).replace('|', ' ').replace(',', ' ')
                
                if lvlStr == '':
                    lvlStr = name + '|' + level_id 
                else:
                    lvlStr += ',' + name + '|' +  level_id 
            
    else:
        rows = db((db.sm_rep_area.cid == cid)  & (db.sm_rep_area.rep_id == rep_id)).select(db.sm_rep_area.area_id, db.sm_rep_area.area_name, groupby=db.sm_rep_area.area_id ,orderby=db.sm_rep_area.area_name)
        for row in rows:
            level_id = str(row.area_id)
            name = str(row.area_name).replace('|', ' ').replace(',', ' ')
            
            if lvlStr == '':
                lvlStr = name + '|' + level_id 
            else:
                lvlStr += ',' + name + '|' +  level_id 
            
    return lvlStr

        
    
#========================= GET DIVISION FUNCTION ==========================#
    
def get_division():
    divstr=''
    level_list = []
    level_depth_no = 0
    c_id = session.cid
    sup_id = str(request.vars.sup_id)
    get_sup_level_id_sql = "SELECT level_id, level_depth_no FROM sm_supervisor_level where cid = '"+c_id+"' and sup_id = '"+str(sup_id)+"' group by level_id ;"
    get_sup_level_id =db.executesql(get_sup_level_id_sql, as_dict =True)
    for s in range(len(get_sup_level_id)):
        levelRecords_str = get_sup_level_id[s]               
        level_depth_no = levelRecords_str['level_depth_no']
        level_id = levelRecords_str['level_id']
        level_list.append(level_id)

    level_list = str(level_list).replace('[', '').replace(']', '')

    get_level_sql = "SELECT level0, level0_name FROM sm_level where cid  = '"+c_id+"' and level0 in ("+level_list+") group by level0"
    get_level =db.executesql(get_level_sql, as_dict =True)
    for l in range(len(get_level)):
        level_0_Records_str = get_level[l]               
        level0 = level_0_Records_str['level0']
        level0_name = level_0_Records_str['level0_name']
        
        if divstr=='':
            divstr= level0 +'|'+ level0_name
        else:
            divstr+= ','+ level0 +'|'+ level0_name
    
    return divstr


#========================= GET ZONE FUNCTION ==========================#


def get_zone():
    zonestr=''
    level_list = []
    level_depth_no = 0
    c_id = session.cid
    sup_id = str(request.vars.sup_id)
    get_sup_level_id_sql = "SELECT level_id, level_depth_no FROM sm_supervisor_level where cid = '"+c_id+"' and sup_id = '"+str(sup_id)+"' group by level_id ;"
    get_sup_level_id =db.executesql(get_sup_level_id_sql, as_dict =True)
    for s in range(len(get_sup_level_id)):
        levelRecords_str = get_sup_level_id[s]               
        level_depth_no = levelRecords_str['level_depth_no']
        level_id = levelRecords_str['level_id']
        level_list.append(level_id)

    level_list = str(level_list).replace('[', '').replace(']', '')
    if level_depth_no == 0 :
        get_level_sql = "SELECT level1, level1_name FROM sm_level where cid  = '"+c_id+"' and level0 in ("+level_list+") group by level1"
    elif level_depth_no == 1 :
        get_level_sql = "SELECT level1, level1_name FROM sm_level where cid  = '"+c_id+"' and level1 in ("+level_list+") group by level1"
   
    get_level =db.executesql(get_level_sql, as_dict =True)
    for l in range(len(get_level)):
        level_0_Records_str = get_level[l]               
        level1 = level_0_Records_str['level1']
        level1_name = level_0_Records_str['level1_name']
        
        if zonestr=='':
            zonestr= level1 +'|'+ level1_name
        else:
            zonestr+= ','+ level1 +'|'+ level1_name
    
    return zonestr



#========================= GET AREA FUNCTION ==========================#
    

def get_area():
    areastr=''
    level_list = []
    level_depth_no = 0
    c_id = session.cid
    sup_id = str(request.vars.sup_id)
    get_sup_level_id_sql = "SELECT level_id, level_depth_no FROM sm_supervisor_level where cid = '"+c_id+"' and sup_id = '"+str(sup_id)+"' group by level_id ;"
    get_sup_level_id =db.executesql(get_sup_level_id_sql, as_dict =True)
    for s in range(len(get_sup_level_id)):
        levelRecords_str = get_sup_level_id[s]               
        level_depth_no = levelRecords_str['level_depth_no']
        level_id = levelRecords_str['level_id']
        level_list.append(level_id)

    level_list = str(level_list).replace('[', '').replace(']', '')
    if level_depth_no == 0 :
        get_level_sql = "SELECT level2, level2_name FROM sm_level where cid  = '"+c_id+"' and level0 in ("+level_list+") group by level2"
    elif level_depth_no == 1 :
        get_level_sql = "SELECT level2, level2_name FROM sm_level where cid  = '"+c_id+"' and level1 in ("+level_list+") group by level2"
    elif level_depth_no == 2 :
        get_level_sql = "SELECT level2, level2_name FROM sm_level where cid  = '"+c_id+"' and level2 in ("+level_list+") group by level2"
    
    get_level =db.executesql(get_level_sql, as_dict =True)
    for l in range(len(get_level)):
        level_0_Records_str = get_level[l]               
        level2 = level_0_Records_str['level2']
        level2_name = level_0_Records_str['level2_name']
        
        if areastr=='':
            areastr= level2 +'|'+ level2_name
        else:
            areastr+= ','+ level2 +'|'+ level2_name
    
    return areastr



#========================= GET CLIENT CATEGORIY FUNCTION ==========================#

    
# def get_client_category():
#     categorystr=''
#     c_id = session.cid
    
#     records=db((db.sm_client.cid == c_id)).select(db.sm_client.category_id, db.sm_client.category_name, groupby= db.sm_client.category_id, orderby=db.sm_client.category_id)
#     for row in records:
#         category_id=str(row.category_id)
#         category_name=str(row.category_name)
        
#         if categorystr=='':
#             categorystr= category_id +'|'+ category_name
#         else:
#             categorystr+= ','+ category_id +'|'+ category_name
    
#     return categorystr


#========================= GET ALL ITEM FUNCTION ==========================#

def get_item():
    item_str=''
    c_id = session.cid
    
    records=db((db.sm_item.cid == c_id) & (db.sm_item.status == 'ACTIVE')).select(db.sm_item.item_id, db.sm_item.name, groupby= db.sm_item.item_id, orderby=db.sm_item.item_id)
    # return db._lastsql
    for row in records:
        item_id=str(row.item_id)
        name=str(row.name)
        
        if item_str=='':
            item_str= item_id +'|'+ name
        else:
            item_str+= ','+ item_id +'|'+ name

    return item_str

def get_all_client_list():
    retStr = ''
    cid = session.cid
    # depot = request.vars.depot
    
    rows = db((db.sm_client.cid == cid) & (db.sm_client.status == 'ACTIVE')).select(db.sm_client.client_id, db.sm_client.name, orderby=db.sm_client.name)
    
    for row in rows:
        client_id = str(row.client_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')

        if retStr == '':
            retStr = client_id + '|' + name
        else:
            retStr += ',' + client_id + '|' + name
            
    return retStr