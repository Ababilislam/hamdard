
import urllib.parse

# http://127.0.0.1:8000/hamdard/client_coverage/client_coverage_url?cid=Hamdard&rep_id=7206&rep_pass=55555

# http://127.0.0.1:8000/hamdard/client_coverage/client_coverage_url?cid=Hamdard&rep_id=itzm&rep_pass=1234       0
# http://127.0.0.1:8000/hamdard/client_coverage/client_coverage_url?cid=Hamdard&rep_id=9011&rep_pass=1234       1
# http://127.0.0.1:8000/hamdard/client_coverage/client_coverage_url?cid=Hamdard&rep_id=6987&rep_pass=1981      1
# http://127.0.0.1:8000/hamdard/client_coverage/client_coverage_url?cid=Hamdard&rep_id=9001&rep_pass=1234       3

# http://w05.yeapps.com/hamdard/client_coverage/client_coverage_url?cid=Hamdard&rep_id=7206&rep_pass=55555
# http://w05.yeapps.com/hamdard/client_coverage/client_coverage_url?cid=Hamdard&rep_id=9011&rep_pass=1234
# http://w05.yeapps.com/hamdard/client_coverage/client_coverage_url?cid=Hamdard&rep_id=6987&rep_pass=1981




#========================= CLIENT COVERAGE URL FUNCTION ==========================#

def client_coverage_url():
    session.btn_filter=None
    session.btn_all=None
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()    
    rep_pass = str(request.vars.rep_pass).strip()
        
    session.cid = cid 
    session.rep_id = rep_id 
    session.rep_pass = rep_pass     

    date_from=current_date
    now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    date_ton=now + datetime.timedelta(days = 1)
    date_to=str(date_ton).split(' ')[0]

    session.from_dt=date_from
    session.to_date=date_from

    btn_filter=request.vars.btn_filter
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    
    levelId_name=''
    division_name=''
    depth = 0
    level_id = ''
    level = ''
    level_list_str = []
    level_id_str =''
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
    
    if btn_filter:
        division_name = str(request.vars.division_name).strip().upper().replace('NONE','')
        zone_name = str(request.vars.zone_name).strip().upper().replace('NONE','')
        area_name = str(request.vars.area_name).strip().upper().replace('NONE','')
        levelId_name = str(request.vars.levelId_name).strip().upper().replace('NONE','')
        category_name = str(request.vars.category_name).strip().upper().replace('NONE','')
        item_name = str(request.vars.item_name).strip().upper().replace('NONE','')

        if (division_name!='' or division_name!=None or division_name!='None'):
            try:
                divisionIdstr = str(division_name).split('|')[0]
            except:
                divisionIdstr = division_name

        if (zone_name!='' or zone_name!=None or zone_name!='None'):
            try:
                zoneIdstr = str(zone_name).split('|')[0]
            except:
                zoneIdstr = zone_name

        if (area_name!='' or area_name!=None or area_name!='None'):
            try:
                areaIdstr = str(area_name).split('|')[0]
            except:
                areaIdstr = area_name

        if (levelId_name!='' or levelId_name!=None or levelId_name!='None'):
            try:
                levelIdstr = str(levelId_name).split('|')[1]
            except:
                levelIdstr = levelId_name

        if (category_name!='' or category_name!=None or category_name!='None'):
            try:
                category_nameIdstr = str(category_name).split('|')[0]
            except:
                category_nameIdstr = category_name

        if (item_name!='' or item_name!=None or item_name!='None'):
            try:
                item_nameIdstr = str(item_name).split('|')[0]
            except:
                item_nameIdstr=''
        
        session.btn_filter=btn_filter
        session.levelIdstr=levelIdstr
        session.divisionIdstr=divisionIdstr
        session.zoneIdstr=zoneIdstr
        session.areaIdstr=areaIdstr
        session.category_nameIdstr=category_nameIdstr
        session.item_nameIdstr=item_nameIdstr
        session.division_name = division_name
        session.zone_name = zone_name
        session.area_name = area_name
        session.levelId_name = levelId_name
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
        session.division_name = ''
        session.zone_name = ''
        session.area_name = ''
        session.levelId_name = ''
        session.category_name = ''
        reqPage=0

    redirect(URL(c='client_coverage',f='client_coverage'))


#========================= CLIENT COVERAGE FUNCTION ==========================#


def client_coverage():    
    response.title = 'Client Coverage'
    cid = session.cid 
    rep_id = session.rep_id 
    rep_pass = session.rep_pass    
    date_from=session.from_dt    
    date_to=session.to_date
    levelIdstr=session.levelIdstr
    divisionIdstr=session.divisionIdstr
    zoneIdstr=session.zoneIdstr
    areaIdstr=session.areaIdstr
    category_nameIdstr=session.category_nameIdstr
    item_nameIdstr=session.item_nameIdstr
    
    btn_filter=request.vars.btn_filter        
    btn_all=request.vars.btn_all
    vChecklist=[]
    vCountList=[]
    records_ov = ''
    invRecords = ''
    total_client=0  
    unique_client_cover_show=0  
    unique_client_cover_per=0 
    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == rep_pass)  & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = str(repRow[0].user_type)
        records_ov=''  

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
            levelList=[]
            marketList=[]
            spicial_codeList=[]
            marketStr=''
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
                

            if category_nameIdstr != '':
                if condition_d == '':
                    condition_d = condition
                condition_d += " AND cl_category_id LIKE '%" +str(category_nameIdstr)+"%'"
                condition_c += " AND category_id LIKE '%"+str(category_nameIdstr)+"%'"

            if territory_id_list != '':
                condition_c += " AND area_id in ("+str(territory_id_list)+")"
            else:
                condition_c += condition 

            #============= TOTAL Client Cover===============
            if condition_c != '':
                clientRecords_str = "SELECT count(client_id) as total_client FROM sm_client WHERE cid = '" + str(cid) + "' " + condition_c + " AND status = 'ACTIVE' GROUP BY client_id ;"
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


            #=============Unique Client Cover===============
            if condition_d != '':
                client_RecordsStr = "SELECT count(distinct(client_id)) as unique_client_cover  FROM sm_invoice_head WHERE cid = '" + str(cid) + "'   AND invoice_date >= '" + str(date_from) + "' AND invoice_date <= '" + str(date_to) + "' " + condition_d + " AND return_count!='1' AND status = 'Invoiced' GROUP BY client_id;"
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

            #=============Client Cover Percentage=============== 
            try: 
                unique_client_cover= (float(unique_client_cover_show) / float(total_client))
                unique_client_cover_p=float(unique_client_cover*100)
                unique_client_cover_per=round((unique_client_cover_p),2)
            except:
                unique_client_cover_per=0
                pass

            sql_str="SELECT client_id,name FROM sm_client WHERE cid = '"+ str(cid) +"' "+condition_c+"  AND status = 'ACTIVE' GROUP BY client_id order by name;"
            records_ov=db.executesql(sql_str,as_dict = True)    

            inv_count = 0   
            invRecords_str = "SELECT count(client_id) as total_inv_count,level3_id,client_id,client_name, invoice_date FROM sm_invoice_head WHERE cid = '" + str(cid) + "'  AND invoice_date >= '" + str(date_from) + "' AND invoice_date <= '" + str(date_to) + "' "+condition_d+" AND return_count!='1' AND status = 'Invoiced' GROUP BY client_id order by total_inv_count desc ;"
            invRecords = db.executesql(invRecords_str, as_dict=True)

            invRecords_str_single= ''            
            for i in range(len(invRecords)):
                invRecords_str_single = invRecords[i]
                vCount=invRecords_str_single['total_inv_count']
                vCheck=str(invRecords_str_single['client_id']) 
                vChecklist.append(vCheck)
                vCountList.append(vCount)  

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
        if session.btn_all : 
            sql_str="SELECT client_id,name FROM sm_client WHERE cid = '"+ str(cid) +"' AND area_id = '" + str(levelIdstr) + "' AND status = 'ACTIVE' GROUP BY client_id order by name;"                    
            records_ov=db.executesql(sql_str,as_dict = True)    

            inv_count = 0   
            invRecords_str = "SELECT count(client_id) as total_inv_count,level3_id,client_id,invoice_date FROM sm_invoice_head WHERE cid = '" + str(cid) + "'  AND invoice_date >= '" + str(date_from) + "' AND invoice_date <= '" + str(date_to) + "' AND area_id = '" + str(levelIdstr) + "'  AND return_count!='1' AND status = 'Invoiced' GROUP BY client_id;"
            invRecords = db.executesql(invRecords_str, as_dict=True)
            
            invRecords_str_single= ''            
            for i in range(len(invRecords)):
                invRecords_str_single = invRecords[i]
                vCount=invRecords_str_single['total_inv_count']
                vCheck=str(invRecords_str_single['client_id']) 
                vChecklist.append(vCheck)
                vCountList.append(vCount)  
 
    return dict(cid=cid,rep_id=rep_id,rep_pass=rep_pass,records_ov=records_ov,total_client=total_client,unique_client_cover_show=unique_client_cover_show,unique_client_cover_per=unique_client_cover_per,vChecklist=vChecklist,vCountList=vCountList, invRecords=invRecords)



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

    
def get_client_category():
    categorystr=''
    c_id = session.cid
    
    records=db((db.sm_client.cid == c_id)).select(db.sm_client.category_id, db.sm_client.category_name, groupby= db.sm_client.category_id, orderby=db.sm_client.category_id)
    # return db._lastsql
    for row in records:
        category_id=str(row.category_id)
        category_name=str(row.category_name)
        
        if categorystr=='':
            categorystr= category_id +'|'+ category_name
        else:
            categorystr+= ','+ category_id +'|'+ category_name
    
    return categorystr


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

