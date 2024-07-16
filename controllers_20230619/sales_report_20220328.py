from random import randint
import urllib2
import calendar
import urllib
import time


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)
def deduct_months(sourcedate, months):
    month = sourcedate.month - 1 - months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)



# =============================================
def sales_report_zm_0_url():

    # session.btn_filter=None
    # session.btn_all=None
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    user_type = str(request.vars.user_type).strip().upper()
    password = str(request.vars.password).strip()
    synccode = str(request.vars.synccode).strip()
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()
    se_item_report = str(request.vars.se_item_report).strip().upper()
    se_market_report = str(request.vars.se_market_report).strip().upper()
    level_id = str(request.vars.level_id).strip().upper()

    session.cid = cid
    session.rep_id = rep_id
    session.user_type = user_type
    session.password = password
    session.synccode = synccode
    session.rep_id_report = rep_id_report
    session.se_item_report = se_item_report
    session.se_market_report = se_market_report
    session.level_id = level_id


    date_from=current_date
    now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    date_ton=now + datetime.timedelta(days = 1)
    date_to=str(date_ton).split(' ')[0]

    session.from_dt=date_from
    session.to_date=date_from

   
    btn_filter=request.vars.btn_filter
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    if btn_filter:

        from_dt = str(request.vars.to_dt_2).strip().upper()
        to_date= str(request.vars.to_dt_3).strip().upper()
        session.btn_filter=btn_filter
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
        session.to_date=date_to
        reqPage=0

    redirect(URL(c='sales_report',f='sales_report_zm_0'))


def sales_report_zm_0():

    cid =session.cid 
    rep_id =session.rep_id 
    user_type =session.user_type 
    password =session.password 
    synccode =session.synccode 
    rep_id_report =session.rep_id_report 
    se_item_report =session.se_item_report 
    se_market_report =session.se_market_report 
    level_id =session.level_id 

    date_from=session.from_dt
    date_to=session.to_date
    # return session.btn_filter
   
    items_per_page=session.items_per_page
    search_form =SQLFORM(db.sm_search_date)


    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = str(repRow[0].user_type).upper()

    
    if (user_type == 'SUP'):
        level_rep = repRow[0].level_id
        depth = repRow[0].field2
        level = 'level' + str(depth)
        # return depth
    
    report_string=""
    
    report_str=""
    
    if (user_type=='SUP'):
       

        levelList=[]
        marketList=[]
        spicial_codeList=[]
        marketStr=''
        SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)
        # return SuplevelRows
        for SuplevelRows in SuplevelRows:
            Suplevel_id = SuplevelRows.level_id
            depth = SuplevelRows.level_depth_no
            level = 'level' + str(depth)
            # return level

            if Suplevel_id not in levelList:
                levelList.append(Suplevel_id)
        cTeam=0
        for i in range(len(levelList)):

            if (level=='level0'):
                levelRows = db((db.sm_level.cid == cid) &(db.sm_level.depth == '0') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
            if (level=='level1'):
                levelRows = db((db.sm_level.cid == cid) &(db.sm_level.depth == '1') &(db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
                        
            if (level=='level2'):
                levelRows = db((db.sm_level.cid == cid)  &(db.sm_level.depth == '2') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
            # return db._lastsql
            for levelRow in levelRows:
                level_id = levelRow.level_id
                # return level_id
                special_territory_code = levelRow.special_territory_code
                if level_id==special_territory_code:
                    cTeam=1

                if marketStr=='':
                    marketStr="'"+str(level_id)+"'"
                else:
                    marketStr=marketStr+",'"+str(level_id)+"'" 
            # return marketStr

            if cTeam==1:    
                if special_territory_code not in spicial_codeList:
                    if (special_territory_code !='' and level_id==special_territory_code):
                        spicial_codeList.append(special_territory_code)    
            
                    # levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.special_territory_code.belongs(spicial_codeList)) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)        
                    levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level.special_territory_code.belongs(spicial_codeList)) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)        

                    for levelSpecialRow in levelSpecialRows:
                        level_id = levelSpecialRow.level_id
                        if marketStr=='':
                            marketStr="'"+str(Suplevel_id)+"'"
                        else:
                            marketStr=marketStr+",'"+str(level_id)+"'" 

        # return marketStr                
        condition=''
        if (se_market_report!="ALL"):
            condition=condition+"AND level0_id = '"+str(se_market_report)+"'"
       
        condition=condition+" AND level0_id IN ("+str(marketStr)+")" 
       
        # return condition

        records_ov=[]
        if session.btn_filter:
            # return 'test' 
            if not(session.from_dt=='' and session.from_dt==None and session.to_date=='' and session.to_date==None):
           
                sql_str="SELECT  level0_id,  level0_name,area_id,  area_name,order_date FROM sm_order_head  WHERE cid = '"+ str(cid) +"' AND order_date >= '"+ str(session.from_dt)+"' AND order_date <= '"+ str(session.to_date) +"' "+ condition + " GROUP BY level0_id order by level0_name asc;"
                # return sql_str
                records_ov=db.executesql(sql_str,as_dict = True)
                date_from=session.from_dt
                date_to=session.to_date
            else:
                pass

        else:

            sql_str="SELECT level0_id,  level0_name,area_id,  area_name, order_date  FROM sm_order_head WHERE cid = '"+ str(cid) +"'  AND order_date = '"+ str(date_from) +"'  "+ condition + " GROUP BY level0_id order by level0_name asc;"
            records_ov=db.executesql(sql_str,as_dict = True)
        

    return dict(Suplevel_id=Suplevel_id,from_dt=date_from,date_to=date_to,cid=cid,rep_id=rep_id,password=password,synccode=synccode,se_market_report=se_market_report,records_ov=records_ov,search_form=search_form)






# ====================================================
def sales_report_zm_url():

    # session.btn_filter=None
    # session.btn_all=None
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    user_type = str(request.vars.user_type).strip().upper()
    password = str(request.vars.password).strip()
    synccode = str(request.vars.synccode).strip()
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()
    se_item_report = str(request.vars.se_item_report).strip().upper()
    se_market_report = str(request.vars.se_market_report).strip().upper()
    level_id = str(request.vars.level_id).strip().upper()
    level0_id = str(request.vars.level0_id).strip().upper()
    Suplevel_id = str(request.vars.Suplevel_id).strip().upper()

    # return level0_id


    session.cid = cid
    session.rep_id = rep_id
    session.user_type = user_type
    session.password = password
    session.synccode = synccode
    session.rep_id_report = rep_id_report
    session.se_item_report = se_item_report
    session.se_market_report = se_market_report
    session.level_id = level_id
    session.level0_id = level0_id
    session.Suplevel_id = Suplevel_id


    date_from=current_date
    now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    date_ton=now + datetime.timedelta(days = 1)
    date_to=str(date_ton).split(' ')[0]

    session.from_dt=date_from
    session.to_date=date_from

   
    btn_filter=request.vars.btn_filter
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    if btn_filter:

        from_dt = str(request.vars.to_dt_2).strip().upper()
        to_date= str(request.vars.to_dt_3).strip().upper()
        session.btn_filter=btn_filter
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
        session.to_date=date_to
        reqPage=0

    redirect(URL(c='sales_report',f='sales_report_zm'))


def sales_report_zm():

    cid =session.cid 
    rep_id =session.rep_id 
    user_type =session.user_type 
    password =session.password 
    synccode =session.synccode 
    rep_id_report =session.rep_id_report 
    se_item_report =session.se_item_report 
    se_market_report =session.se_market_report 
    level_id =session.level_id 
    level0_id = session.level0_id
    Suplevel_id=session.Suplevel_id
    if level0_id==None or level0_id=='None' or level0_id=='NONE':
        # return 'asdas'
        level0_id=Suplevel_id
    # return level0_id


    date_from=session.from_dt
    date_to=session.to_date
    # return session.btn_filter
   
    items_per_page=session.items_per_page
    search_form =SQLFORM(db.sm_search_date)


    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = str(repRow[0].user_type).upper()

    
    if (user_type == 'SUP'):
        SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)
        # return SuplevelRows
        for SuplevelRows in SuplevelRows:
            Suplevel_id = SuplevelRows.level_id
            depth = SuplevelRows.level_depth_no
            level = 'level' + str(depth)
        # return depth
    
    report_string=""
    
    report_str=""
    
    if (user_type=='SUP'):
       

        levelList=[]
        marketList=[]
        spicial_codeList=[]
        marketStr=''
        # return level0_id
        if (level=='level0'):
            # return session.level0_id
            levelList.append(level0_id)
            Suplevel_id=level0_id
            marketStr="'"+str(level0_id)+"'"
           
        else:
            SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)
            # return SuplevelRows
            for SuplevelRows in SuplevelRows:
                Suplevel_id = SuplevelRows.level_id
                depth = SuplevelRows.level_depth_no
                level = 'level' + str(depth)
                # return level

                if Suplevel_id not in levelList:
                    levelList.append(Suplevel_id)
        # return marketStr
        cTeam=0
        # return level
        for i in range(len(levelList)):

            if (level=='level0'):
                levelRows = db((db.sm_level.cid == cid) &(db.sm_level.depth == '1') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
                # return db._lastsql
            if (level=='level1'):
                levelRows = db((db.sm_level.cid == cid) &(db.sm_level.depth == '1') &(db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
                # return db._lastsql        
            if (level=='level2'):
                levelRows = db((db.sm_level.cid == cid)  &(db.sm_level.depth == '2') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
         
            for levelRow in levelRows:
                level_id = levelRow.level_id
                # return level_id
                special_territory_code = levelRow.special_territory_code
                if level_id==special_territory_code:
                    cTeam=1

                if marketStr=='':
                    marketStr="'"+str(level_id)+"'"
                else:
                    marketStr=marketStr+",'"+str(level_id)+"'" 
            # return marketStr

            if cTeam==1:    
                if special_territory_code not in spicial_codeList:
                    if (special_territory_code !='' and level_id==special_territory_code):
                        spicial_codeList.append(special_territory_code)    
            
                    # levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.special_territory_code.belongs(spicial_codeList)) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)        
                    levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level.special_territory_code.belongs(spicial_codeList)) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)        

                    for levelSpecialRow in levelSpecialRows:
                        level_id = levelSpecialRow.level_id
                        if marketStr=='':
                            marketStr="'"+str(Suplevel_id)+"'"
                        else:
                            marketStr=marketStr+",'"+str(level_id)+"'" 

                       
        condition=''
        if (se_market_report!="ALL"):
            condition=condition+"AND level1_id = '"+str(marketStr)+"'"


        condition=condition+" AND level1_id IN ("+str(marketStr)+")" 
       
        # return condition

        records_ov=[]
        if session.btn_filter:
            # return 'test' 
            if not(session.from_dt=='' and session.from_dt==None and session.to_date=='' and session.to_date==None):
           
                sql_str="SELECT  level1_id,  level1_name,area_id,  area_name,order_date FROM sm_order_head  WHERE cid = '"+ str(cid) +"' AND order_date >= '"+ str(session.from_dt)+"' AND order_date <= '"+ str(session.to_date) +"' "+ condition + " GROUP BY level1_id order by level1_name asc;"
                # return sql_str
                records_ov=db.executesql(sql_str,as_dict = True)
                date_from=session.from_dt
                date_to=session.to_date
            else:
                pass
        # elif session.btn_all:

        #     # sql_str="SELECT level1_id,  level1_name,area_id,  area_name, order_date  FROM sm_order_head WHERE cid = '"+ str(cid) +"'  AND order_date >= '"+ str(session.date_from) +"' AND order_date < '"+ str(session.to_date) +"'   "+ condition + " GROUP BY level1_id,order_date order by order_date desc;"
        #     sql_str="SELECT level1_id,  level1_name,area_id,  area_name, order_date  FROM sm_order_head WHERE cid = '"+ str(cid) +"'  AND order_date = '"+ str(date_from) +"' AND order_date < '"+ str(session.to_date) +"'   "+ condition + " GROUP BY level1_id,order_date order by order_date desc;"
        #     records_ov=db.executesql(sql_str,as_dict = True)
    
        else:

            sql_str="SELECT level1_id,  level1_name,area_id,  area_name, order_date  FROM sm_order_head WHERE cid = '"+ str(cid) +"'  AND order_date = '"+ str(date_from) +"'  "+ condition + " GROUP BY level1_id order by level1_name asc;"
            records_ov=db.executesql(sql_str,as_dict = True)
    
        # return sql_str
    return dict(Suplevel_id=Suplevel_id,from_dt=date_from,date_to=date_to,cid=cid,rep_id=rep_id,password=password,synccode=synccode,se_market_report=se_market_report,records_ov=records_ov,search_form=search_form)







def sales_report_rsm_url():

    session.btn_filter=None
    session.btn_all=None

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    user_type = str(request.vars.user_type).strip().upper()
    password = str(request.vars.password).strip()
    synccode = str(request.vars.synccode).strip()
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()
    se_item_report = str(request.vars.se_item_report).strip().upper()
    se_market_report = str(request.vars.se_market_report).strip().upper()
    level_id = str(request.vars.level_id).strip().upper()

    session.cid = cid 
    session.rep_id = rep_id 
    session.user_type = user_type 
    session.password = password 
    session.synccode = synccode 
    session.rep_id_report = rep_id_report 
    session.se_item_report = se_item_report 
    session.se_market_report = se_market_report 
    session.level_id = level_id 

    date_from=current_date
    # return date_from
    now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    date_ton=now + datetime.timedelta(days = 1)
    date_to=str(date_ton).split(' ')[0]

    session.from_dt=date_from
    session.to_date=date_from


    btn_filter=request.vars.btn_filter
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    levelId_name=''
    if btn_filter:

        levelId_name = str(request.vars.levelId_name).strip().upper()

        # return levelId_name
        if (levelId_name!='' or levelId_name!=None or levelId_name!='None'):
            try:
                levelIdstr = str(levelId_name).split('|')[1]
            except:
                levelIdstr=''

        session.btn_filter=btn_filter
        session.levelIdstr=levelIdstr
        
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
        session.to_date=date_to
        reqPage=0

    redirect(URL(c='sales_report',f='sales_report_rsm'))


def sales_report_rsm():

    cid  = session.cid 
    rep_id  = session.rep_id 
    user_type  = session.user_type 
    password  = session.password 
    synccode  = session.synccode 
    rep_id_report  = session.rep_id_report 
    se_item_report  = session.se_item_report 
    se_market_report  = session.se_market_report 
    level_id  = session.level_id 
    levelIdstr=session.levelIdstr
    # return levelIdstr

    date_from=current_date
    # return date_from
    now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    date_ton=now + datetime.timedelta(days = 1)
    date_to=str(date_ton).split(' ')[0]
    

    items_per_page=session.items_per_page
    search_form =SQLFORM(db.sm_search_date)
    

    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
    # return repRow
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = str(repRow[0].user_type).upper()

       # pass
    
    if (user_type == 'SUP'):
        level_rep = repRow[0].level_id
        depth = repRow[0].field2
        level = 'level' + str(depth)
        # return depth
    
    report_string=""
    
    report_str=""
    
 
    if (user_type=='SUP'):
       

        levelList=[]
        marketList=[]
        spicial_codeList=[]
        marketStr=''
        SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)
        for SuplevelRows in SuplevelRows:
            Suplevel_id = SuplevelRows.level_id
            depth = SuplevelRows.level_depth_no
            level = 'level' + str(depth)
            # return level

            if Suplevel_id not in levelList:
                levelList.append(Suplevel_id)
        cTeam=0
        for i in range(len(levelList)):

            if (level=='level0'):
                levelRows = db((db.sm_level.cid == cid)  &(db.sm_level.depth == '0') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
            #     # return '0'
            if (level=='level1'):
                levelRows = db((db.sm_level.cid == cid) &(db.sm_level.depth == '1') &(db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
                        
            if (level=='level2'):
                levelRows = db((db.sm_level.cid == cid)  &(db.sm_level.depth == '2') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)

            for levelRow in levelRows:
                level_id = levelRow.level_id
                # return level_id
                special_territory_code = levelRow.special_territory_code
                if level_id==special_territory_code:
                    cTeam=1

                if marketStr=='':
                    marketStr="'"+str(level_id)+"'"
                else:
                    marketStr=marketStr+",'"+str(level_id)+"'" 

            if cTeam==1:    
                if special_territory_code not in spicial_codeList:
                    if (special_territory_code !='' and level_id==special_territory_code):
                        spicial_codeList.append(special_territory_code)    
            
                    # levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.special_territory_code.belongs(spicial_codeList)) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)        
                    levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level.special_territory_code.belongs(spicial_codeList)) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)        

                    for levelSpecialRow in levelSpecialRows:
                        level_id = levelSpecialRow.level_id
                        if marketStr=='':
                            marketStr="'"+str(Suplevel_id)+"'"
                        else:
                            marketStr=marketStr+",'"+str(level_id)+"'" 

                       
        condition=''
        if (se_market_report!="ALL"):
            condition=condition+"AND route_id = '"+str(se_market_report)+"'"
       
        condition=condition+" AND level2_id IN ("+str(marketStr)+")" 
       
        # return condition

        records_ov=[]
        if session.btn_filter: 
            if not(session.from_dt=='' or session.from_dt==None or session.to_date=='' or session.to_date==None):
           
                sql_str="SELECT  level2_id,  level2_name,area_id,  area_name,order_date FROM sm_order_head  WHERE cid = '"+ str(cid) +"' AND order_date >= '"+ str(session.from_dt) +"' AND order_date <= '"+ str(session.to_date) +"' "+ condition + " GROUP BY level2_id,order_date order by order_date desc;"
                # return sql_str
                records_ov=db.executesql(sql_str,as_dict = True)
            else:
                pass
            if not(session.levelIdstr=='' or session.levelIdstr==None):
            
                sql_str="SELECT  level2_id,  level2_name,area_id,  area_name,order_date FROM sm_order_head  WHERE cid = '"+ str(cid) +"' AND  level2_id='"+ str(levelIdstr) +"' AND order_date >= '"+ str(session.from_dt) +"' AND order_date <= '"+ str(session.to_date) +"' GROUP BY area_id,order_date order by order_date desc;"
                # return sql_str
                records_ov=db.executesql(sql_str,as_dict = True)
            else:
                pass

        # elif session.btn_all:
        #     sql_str="SELECT level2_id,  level2_name,area_id,  area_name, order_date  FROM sm_order_head WHERE cid = '"+ str(cid) +"'  AND order_date  >=  '"+ str(session.from_dt) +"' AND order_date < '"+ str(session.to_date) +"' "+ condition + " GROUP BY level2_id,order_date order by order_date desc;"
        #     records_ov=db.executesql(sql_str,as_dict = True)
    
        else:
            sql_str="SELECT level2_id,  level2_name,area_id,  area_name, order_date  FROM sm_order_head WHERE cid = '"+ str(cid) +"'  AND order_date  =  '"+ str(session.from_dt) +"' "+ condition + " GROUP BY level2_id,order_date order by order_date desc;"
            records_ov=db.executesql(sql_str,as_dict = True)
    
        # return sql_str
    return dict(Suplevel_id=Suplevel_id,from_dt=date_from,date_to=date_to,cid=cid,rep_id=rep_id,password=password,synccode=synccode,se_market_report=se_market_report,records_ov=records_ov,search_form=search_form)





def sales_report_fm_url():

    # session.btn_filter=None
    # session.btn_all=None

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    user_type = str(request.vars.user_type).strip().upper()
    password = str(request.vars.password).strip()
    synccode = str(request.vars.synccode).strip()
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()
    se_item_report = str(request.vars.se_item_report).strip().upper()
    se_market_report = str(request.vars.se_market_report).strip().upper()
    level2_id = str(request.vars.level2_id).strip().upper()
    order_date = str(request.vars.order_date).strip().upper()
    # return level_id
    session.cid = cid 
    session.rep_id = rep_id 
    session.user_type = user_type 
    session.password = password 
    session.synccode = synccode 
    
    session.rep_id_report = rep_id_report 
    session.se_item_report = se_item_report 
    session.se_market_report = se_market_report 
    session.level2_id = level2_id 
    session.order_date = order_date 
    redirect(URL(c='sales_report',f='sales_report_fm'))


def sales_report_fm():
    cid = session.cid  
    rep_id = session.rep_id  
    user_type = session.user_type  
    password = session.password  
    synccode = session.synccode  

    rep_id_report = session.rep_id_report  
    se_item_report = session.se_item_report  
    se_market_report = session.se_market_report  
    level2_id = session.level2_id  
    order_date = session.order_date  

    date_from=current_date
    now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    date_ton=now + datetime.timedelta(days = 1)
    date_to=str(date_ton).split(' ')[0]
    # return date_to
    session.from_dt=date_from
    session.to_date=date_from

    btn_filter=request.vars.btn_filter
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    levelIdstr=''
    if btn_filter:
        levelId_name = str(request.vars.levelId_name).strip().upper()
        # session.levelId_name=levelId_name_g
        # levelId_name=session.levelId_name
        
        if (levelId_name!='' or levelId_name!=None or levelId_name!='None'):
            try:
                levelIdstr = str(levelId_name).split('|')[1]
            except:
                levelIdstr=''

        from_dt = str(request.vars.to_dt_2).strip().upper()
        to_date= str(request.vars.to_dt_3).strip().upper()
        session.btn_filter=btn_filter
        session.levelIdstr=levelIdstr
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
        
        reqPage=0
        
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    search_form =SQLFORM(db.sm_search_date)
    

    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
    # return repRow
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = str(repRow[0].user_type).upper()

       # pass
    
    if (user_type == 'SUP'):
        level_rep = repRow[0].level_id
        depth = repRow[0].field2
        level = 'level' + str(depth)
        # return depth
    
    report_string=""
    
    report_str=""
    
    if (user_type=='REP'):
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

       

        repAreaStr=''
        areaRows = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.rep_id == rep_id) ).select(db.sm_rep_area.area_id, orderby=~db.sm_rep_area.area_id)
        for areaRows in areaRows:
            area_id = areaRows.area_id
            if repAreaStr=='':
                repAreaStr="'"+str(area_id)+"'"
            else:
                repAreaStr=repAreaStr+",'"+str(area_id)+"'" 
            

        condition=""
        condition="and area_id IN ("+str(repAreaStr)+")" 
        # condition=condition+" and rep_id ='"+ str(rep_id) +"'"
        


        records_ov=[]
        if session.btn_filter:

            if not(session.levelIdstr=='' or session.levelIdstr==None):
                condition=condition+" AND  area_id='"+ str(levelIdstr) +"'" 


            if not(session.from_dt!='' and session.from_dt!=None and session.to_date!='' and session.to_date!=None):
           
                sql_str="SELECT  area_id,  area_name,order_date FROM sm_order_head  WHERE cid = '"+ str(cid) +"' AND order_date >= '"+ str(session.from_dt) +"' AND order_date <= '"+ str(session.to_date) +"' "+ condition + " GROUP BY area_id order by order_date desc,area_name asc ;"
                return sql_str
                records_ov=db.executesql(sql_str,as_dict = True)
            else:
                pass
        elif session.btn_all:
            sql_str="SELECT area_id,  area_name, order_date  FROM sm_order_head WHERE cid = '"+ str(cid) +"'  AND order_date = '"+ str(order_date) +"' "+ condition + " GROUP BY area_id order by order by order_date desc,area_name asc;"
            records_ov=db.executesql(sql_str,as_dict = True)
        else:
            sql_str="SELECT area_id,  area_name, order_date  FROM sm_order_head WHERE cid = '"+ str(cid) +"'  AND order_date = '"+ str(order_date) +"' "+ condition + " GROUP BY area_id order by order_date desc,area_name asc;"
            records_ov=db.executesql(sql_str,as_dict = True)

    if (user_type=='SUP'):


        levelList=[]
        marketList=[]
        spicial_codeList=[]
        marketStr=''
        SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)
        for SuplevelRows in SuplevelRows:
            Suplevel_id = SuplevelRows.level_id
            depth = SuplevelRows.level_depth_no
            level = 'level' + str(depth)
            # return level

            if Suplevel_id not in levelList:
                levelList.append(Suplevel_id)
        cTeam=0
        for i in range(len(levelList)):

            levelRows = db((db.sm_level.cid == cid)  &(db.sm_level.level_id == level2_id) & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
            #     # return '2'
            # if (level=='level3'):
            #     levelRows = db((db.sm_level.cid == cid) & (db.sm_level.depth == '3') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
            #     # return '3'
            
            # levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
            for levelRow in levelRows:
                level_id = levelRow.level_id
                # return level_id
                special_territory_code = levelRow.special_territory_code
                if level_id==special_territory_code:
                    cTeam=1

                if marketStr=='':
                    marketStr="'"+str(level_id)+"'"
                else:
                    marketStr=marketStr+",'"+str(level_id)+"'" 
            # return marketStr

            if cTeam==1:    
                if special_territory_code not in spicial_codeList:
                    if (special_territory_code !='' and level_id==special_territory_code):
                        spicial_codeList.append(special_territory_code)    
            
                    # levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.special_territory_code.belongs(spicial_codeList)) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)        
                    levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level.special_territory_code.belongs(spicial_codeList)) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)        

                    for levelSpecialRow in levelSpecialRows:
                        level_id = levelSpecialRow.level_id
                        if marketStr=='':
                            marketStr="'"+str(Suplevel_id)+"'"
                        else:
                            marketStr=marketStr+",'"+str(level_id)+"'" 

                       
        condition=''
        if (se_market_report!="ALL"):
            condition=condition+"AND route_id = '"+str(se_market_report)+"'"
       
        condition=condition+" AND level2_id IN ("+str(marketStr)+")" 
       
        # return condition

        records_ov=[]
        if session.btn_filter: 
            # return 'sfs'

            if not(session.levelIdstr=='' or session.levelIdstr==None):
                condition=condition+" AND  level3_id='"+ str(levelIdstr) +"'" 

            if not(session.from_dt=='' or session.from_dt==None or session.to_date=='' or session.to_date==None):

                sql_str="SELECT  level3_id,  level3_name,area_id,  area_name,order_date FROM sm_order_head  WHERE cid = '"+ str(cid) +"' AND order_date >= '"+ str(session.from_dt) +"' AND order_date <= '"+ str(session.to_date) +"' "+ str(condition) +" GROUP BY level3_id order by order_date desc,area_name asc;"
                # return sql_str
                records_ov=db.executesql(sql_str,as_dict = True)
            else:
                pass

        elif session.btn_all:
            sql_str="SELECT level3_id,  level3_name,area_id,  area_name, order_date  FROM sm_order_head WHERE cid = '"+ str(cid) +"'  AND order_date  =  '"+ str(session.from_dt) +"' "+ str(condition) +" GROUP BY level3_id order by order_date desc,area_name asc;"
            records_ov=db.executesql(sql_str,as_dict = True)
        else:
            # return 'sd'
            sql_str="SELECT level3_id,  level3_name,area_id,  area_name, order_date  FROM sm_order_head WHERE cid = '"+ str(cid) +"'  AND order_date  =  '"+ str(order_date) +"' "+ str(condition) +" GROUP BY level3_id order by order_date desc,area_name asc;"
            records_ov=db.executesql(sql_str,as_dict = True)


    return dict(level2_id=level2_id,from_dt=date_from,date_to=date_to,cid=cid,rep_id=rep_id,password=password,synccode=synccode,se_market_report=se_market_report,records_ov=records_ov,search_form=search_form)




def sales_report_zm_rsm_url():

    session.btn_filter=None
    session.btn_all=None
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    user_type = str(request.vars.user_type).strip().upper()
    password = str(request.vars.password).strip()
    synccode = str(request.vars.synccode).strip()
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()
    se_item_report = str(request.vars.se_item_report).strip().upper()
    se_market_report = str(request.vars.se_market_report).strip().upper()
    level1_id = str(request.vars.level1_id).strip().upper()
    order_date = str(request.vars.order_date).strip().upper()

    session.cid = cid
    session.rep_id = rep_id
    session.user_type = user_type
    session.password = password
    session.synccode = synccode
    session.rep_id_report = rep_id_report
    session.se_item_report = se_item_report
    session.se_market_report = se_market_report
    session.level1_id = level1_id
    session.order_date = order_date

    # return session.level1_id
    date_from=current_date
    # return date_from
    now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    date_ton=now + datetime.timedelta(days = 1)
    date_to=str(date_ton).split(' ')[0]
    # return date_to
    
    session.from_dt=date_from
    session.to_date=date_from

    btn_filter=request.vars.btn_filter
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    if btn_filter:
        session.btn_filter=btn_filter

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
        session.to_date=date_to
        reqPage=0


    redirect(URL(c='sales_report',f='sales_report_zm_rsm'))



def sales_report_zm_rsm():

    cid = session.cid
    rep_id = session.rep_id
    user_type = session.user_type
    password = session.password
    synccode = session.synccode
    rep_id_report = session.rep_id_report
    se_item_report = session.se_item_report
    se_market_report = session.se_market_report
    level1_id = session.level1_id
    order_date = session.order_date
    # return order_date

    date_from=session.from_dt
    date_to=session.to_date

    
        
    items_per_page=session.items_per_page
    search_form =SQLFORM(db.sm_search_date)
    

    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
    # return repRow
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = str(repRow[0].user_type).upper()

       # pass
    
    if (user_type == 'SUP'):
        level_rep = repRow[0].level_id
        depth = repRow[0].field2
        level = 'level' + str(depth)
        # return depth
    
    report_string=""
    
    report_str=""
    
    if (user_type=='REP'):
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

        

        repAreaStr=''
        areaRows = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.rep_id == rep_id) ).select(db.sm_rep_area.area_id, orderby=~db.sm_rep_area.area_id)
        for areaRows in areaRows:
            area_id = areaRows.area_id
            if repAreaStr=='':
                repAreaStr="'"+str(area_id)+"'"
            else:
                repAreaStr=repAreaStr+",'"+str(area_id)+"'" 
            

        condition=""
        condition="and area_id IN ("+str(repAreaStr)+")" 
        condition=condition+" and rep_id ='"+ str(rep_id) +"'"
        


        records_ov=[]
        if session.btn_filter:
            if not(session.from_dt=='' or session.from_dt==None or session.to_date=='' or session.to_date==None):
            

                sql_str="SELECT  area_id,  area_name,order_date FROM sm_order_head  WHERE cid = '"+ str(cid) +"' AND order_date >= '"+ str(session.from_dt) +"' AND order_date <= '"+ str(session.to_date) +"' "+ condition + " GROUP BY area_id order by order_date desc;"
                # return sql_str
                records_ov=db.executesql(sql_str,as_dict = True)
            else:
                pass
        elif session.btn_all:
            sql_str="SELECT area_id,  area_name, order_date  FROM sm_order_head WHERE cid = '"+ str(cid) +"'  AND order_date  >=  '"+ str(session.from_dt) +"' AND order_date < '"+ str(session.to_date) +"' "+ condition + " GROUP BY area_id order by order_date desc;"
            # return sql_str
            records_ov=db.executesql(sql_str,as_dict = True)

    if (user_type=='SUP'):
       

        levelList=[]
        marketList=[]
        spicial_codeList=[]
        marketStr=''
        SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)
        for SuplevelRows in SuplevelRows:
            Suplevel_id = SuplevelRows.level_id
            depth = SuplevelRows.level_depth_no
            level = 'level' + str(depth)
            # return level

            if Suplevel_id not in levelList:
                levelList.append(Suplevel_id)
        cTeam=0
        for i in range(len(levelList)):

            levelRows = db((db.sm_level.cid == cid)  &(db.sm_level.level_id == level1_id) & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
            #     # return '2'
            # if (level=='level3'):
            #     levelRows = db((db.sm_level.cid == cid) & (db.sm_level.depth == '3') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
            #     # return '3'
            
            # levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
            for levelRow in levelRows:
                level_id = levelRow.level_id
                # return level_id
                special_territory_code = levelRow.special_territory_code
                if level_id==special_territory_code:
                    cTeam=1

                if marketStr=='':
                    marketStr="'"+str(level_id)+"'"
                else:
                    marketStr=marketStr+",'"+str(level_id)+"'" 
            # return marketStr

            if cTeam==1:    
                if special_territory_code not in spicial_codeList:
                    if (special_territory_code !='' and level_id==special_territory_code):
                        spicial_codeList.append(special_territory_code)    
            
                    # levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.special_territory_code.belongs(spicial_codeList)) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)        
                    levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level.special_territory_code.belongs(spicial_codeList)) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)        

                    for levelSpecialRow in levelSpecialRows:
                        level_id = levelSpecialRow.level_id
                        if marketStr=='':
                            marketStr="'"+str(Suplevel_id)+"'"
                        else:
                            marketStr=marketStr+",'"+str(level_id)+"'" 

                       
        condition=''
        if (se_market_report!="ALL"):
            condition=condition+"AND route_id = '"+str(se_market_report)+"'"
       
        condition=condition+" AND level1_id IN ("+str(marketStr)+")" 
       
        # return condition
        # return order_date
        records_ov=[]
        if session.btn_filter: 
            if not(session.from_dt=='' or session.from_dt==None or session.to_date=='' or session.to_date==None):
            
                sql_str="SELECT  level2_id,  level2_name,area_id,  area_name,order_date FROM sm_order_head  WHERE cid = '"+ str(cid) +"' AND order_date >= '"+ str(session.from_dt) +"' AND order_date <= '"+ str(session.to_date) +"' AND level1_id = '"+ str(level1_id) +"' GROUP BY level2_id order by level2_name asc;"
                # return sql_str
                records_ov=db.executesql(sql_str,as_dict = True)
            else:
                pass

        elif session.btn_all: 
            sql_str="SELECT level2_id,  level2_name,area_id,  area_name, order_date  FROM sm_order_head WHERE cid = '"+ str(cid) +"'  AND order_date >= '"+ str(session.from_dt) +"' AND order_date < '"+ str(session.to_date) +"' AND level1_id = '"+ str(level1_id) +"' GROUP BY level2_id order by level2_name asc;"
            records_ov=db.executesql(sql_str,as_dict = True)
        else:
            sql_str="SELECT level2_id,  level2_name,area_id,  area_name, order_date  FROM sm_order_head WHERE cid = '"+ str(cid) +"'  AND order_date = '"+ str(order_date) +"'  AND level1_id = '"+ str(level1_id) +"' GROUP BY level2_id order by level2_name asc;"
            records_ov=db.executesql(sql_str,as_dict = True)
        # return sql_str

    return dict(level1_id=level1_id,from_dt=date_from,date_to=date_to,cid=cid,rep_id=rep_id,password=password,synccode=synccode,se_market_report=se_market_report,records_ov=records_ov,search_form=search_form)




def sales_report_detail_url():
    # session.btn_filter=None
    # session.btn_all=None
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    user_type = str(request.vars.user_type).strip().upper()
    password = str(request.vars.password).strip()
    synccode = str(request.vars.synccode).strip()
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()
    se_item_report = str(request.vars.se_item_report).strip().upper()
    se_market_report = str(request.vars.se_market_report).strip().upper()

    session.cid=cid
    session.rep_id=rep_id
    session.user_type=user_type
    session.password=password
    session.synccode=synccode
    session.rep_id_report=rep_id_report
    session.se_item_report=se_item_report
    session.se_market_report=se_market_report

    date_from=current_date
    now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    date_ton=now + datetime.timedelta(days = 1)
    date_to=str(date_ton).split(' ')[0]



    session.from_dt=date_from
    session.to_date=date_from


    btn_filter=request.vars.btn_filter
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    levelIdstr=''

    if btn_filter:
        levelId_name_g = str(request.vars.levelId_name).strip().upper()
        session.levelId_name=levelId_name_g
        levelId_name=session.levelId_name
        
        if (levelId_name!='' or levelId_name!=None or levelId_name!='None'):
            try:
                levelIdstr = str(levelId_name).split('|')[1]
            except:
                levelIdstr=''
        from_dt = str(request.vars.to_dt_2).strip().upper()
        to_date= str(request.vars.to_dt_3).strip().upper()
        session.btn_filter=btn_filter
        session.levelIdstr=levelIdstr
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
        session.to_date=date_to
        # return date_from

        # session.from_dt=str(from_dt).split(' ')[0]
        reqPage=0
        

    redirect(URL(c='sales_report',f='sales_report_detail'))



def sales_report_detail():

    cid=session.cid

    rep_id=session.rep_id
    user_type=session.user_type
    password=session.password
    synccode=session.synccode
    rep_id_report=session.rep_id_report
    se_item_report=session.se_item_report
    se_market_report=session.se_market_report
    levelIdstr=session.levelIdstr
    # return levelIdstr


    # cid = str(request.vars.cid).strip().upper()
    # rep_id = str(request.vars.rep_id).strip().upper()
    # user_type = str(request.vars.user_type).strip().upper()
    # password = str(request.vars.password).strip()
    # synccode = str(request.vars.synccode).strip()
    
    date_from=session.from_dt
    date_to=session.to_date
        
    items_per_page=session.items_per_page
    search_form =SQLFORM(db.sm_search_date)
    

    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
    # return repRow
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = str(repRow[0].user_type).upper()

       # pass
    
    if (user_type == 'SUP'):
        level_rep = repRow[0].level_id
        depth = repRow[0].field2
        level = 'level' + str(depth)
        # return depth
    
    report_string=""
    
    report_str=""
    
    if (user_type=='REP'):
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

        # dateFlag=''
        reqPage=len(request.args)
       

        repAreaStr=''
        areaRows = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.rep_id == rep_id)  ).select(db.sm_rep_area.area_id, orderby=~db.sm_rep_area.area_id)
        for areaRows in areaRows:
            area_id = areaRows.area_id
            if repAreaStr=='':
                repAreaStr="'"+str(area_id)+"'"
            else:
                repAreaStr=repAreaStr+",'"+str(area_id)+"'" 
            

        condition=""
        condition="and area_id IN ("+str(repAreaStr)+")" 

        condition=condition+" and rep_id ='"+ str(rep_id) +"'"
        


        records_ov=[]
        if session.btn_filter:

            if not(session.levelIdstr=='' or session.levelIdstr==None):
                condition=condition+" AND  area_id='"+ str(levelIdstr) +"'" 


            if not(session.from_dt=='' or session.from_dt==None or session.to_date=='' or session.to_date==None):
            
                sql_str="SELECT  area_id,  area_name,order_date FROM sm_order_head  WHERE cid = '"+ str(cid) +"' AND order_date >= '"+ str(session.from_dt).split(' ')[0] +"' AND order_date <= '"+ str(session.to_date) +"' "+ condition + " GROUP BY area_id order by order_date desc, area_name asc;"
                # return sql_str
                records_ov=db.executesql(sql_str,as_dict = True)
            else:
                pass
            # if not(session.levelIdstr=='' or session.levelIdstr==None):
            
            #     sql_str="SELECT  area_id,  area_name,order_date FROM sm_order_head  WHERE cid = '"+ str(cid)  +"'  AND  area_id='"+ str(levelIdstr) +"' GROUP BY area_id,order_date order by order_date desc;"
            #     # return sql_str
            #     records_ov=db.executesql(sql_str,as_dict = True)
            # else:
            #     pass
        elif session.btn_all:
            # return 'sa'
            sql_str="SELECT area_id, area_name, order_date  FROM sm_order_head WHERE cid = '"+ str(cid) +"'  AND order_date =  '"+ str(date_from) +"'  "+ condition + " GROUP BY area_id order by  area_name asc;"
            records_ov=db.executesql(sql_str,as_dict = True)
        else:
            sql_str="SELECT area_id, area_name, order_date  FROM sm_order_head WHERE cid = '"+ str(cid) +"'  AND order_date =  '"+ str(date_from) +"'  "+ condition + " GROUP BY area_id order by  area_name asc;"
            # return sql_str
            records_ov=db.executesql(sql_str,as_dict = True)
        # return sql_str
    if (user_type=='SUP'):
        dateFlag=''
        reqPage=len(request.args)

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
        cTeam=0
        for i in range(len(levelList)):
            levelRows = db((db.sm_level.cid == cid)  & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
            for levelRow in levelRows:
                level_id = levelRow.level_id
                special_territory_code = levelRow.special_territory_code
                if level_id==special_territory_code:
                    cTeam=1

                if marketStr=='':
                    marketStr="'"+str(level_id)+"'"
                else:
                    marketStr=marketStr+",'"+str(level_id)+"'" 
            if cTeam==1:    
                if special_territory_code not in spicial_codeList:
                    if (special_territory_code !='' and level_id==special_territory_code):
                        spicial_codeList.append(special_territory_code)    
            
                    levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level.special_territory_code.belongs(spicial_codeList)) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)        

                    for levelSpecialRow in levelSpecialRows:
                        level_id = levelSpecialRow.level_id
                        if marketStr=='':
                            marketStr="'"+str(Suplevel_id)+"'"
                        else:
                            marketStr=marketStr+",'"+str(level_id)+"'" 
                           
        condition=''
        if (se_market_report!="ALL"):
            condition=condition+"AND route_id = '"+str(se_market_report)+"'"
        # if (rep_id!=rep_id_report):
        # condition=condition+"AND rep_id = '"+str(rep_id)+"'"
        condition=condition+" AND area_id IN ("+str(marketStr)+")" 
      
       

        records_ov=[]
        if session.btn_filter:
            
            if not(session.from_dt=='' or session.from_dt==None or session.to_date=='' or session.to_date==None):
           
                sql_str="SELECT  area_id,  area_name,order_date FROM sm_order_head  WHERE cid = '"+ str(cid) +"' AND order_date >= '"+ str(session.from_dt).split(' ')[0] +"' AND order_date <= '"+ str(session.to_date) +"' "+ condition + " GROUP BY area_id,order_date order by order_date desc, area_name asc;"
                # return sql_str
                records_ov=db.executesql(sql_str,as_dict = True)
            pass

            if not(session.levelIdstr=='' or session.levelIdstr==None):
            
                sql_str="SELECT  area_id,  area_name,order_date FROM sm_order_head  WHERE cid = '"+ str(cid) +"'  AND  area_id='"+ str(levelIdstr) +"'  AND order_date >= '"+ str(session.from_dt).split(' ')[0] +"' AND order_date <= '"+ str(session.to_date) +"' GROUP BY area_id,order_date order by order_date desc, area_name asc;"
                # return sql_str
                records_ov=db.executesql(sql_str,as_dict = True)
            else:
                pass
        elif session.btn_all:
            sql_str="SELECT area_id,  area_name, order_date  FROM sm_order_head WHERE cid = '"+ str(cid) +"'  AND order_date  >=  '"+ str(date_from) +"' "+ condition + " GROUP BY area_id order by  area_name asc;"
            # return sql_str
            records_ov=db.executesql(sql_str,as_dict = True)
        else:
            sql_str="SELECT area_id,  area_name, order_date  FROM sm_order_head WHERE cid = '"+ str(cid) +"'  AND order_date  =  '"+ str(date_from) +"'  "+ condition + " GROUP BY area_id order by  area_name asc;"
            # return sql_str
            records_ov=db.executesql(sql_str,as_dict = True)

    return dict(from_dt=date_from,date_to=date_to,cid=cid,rep_id=rep_id,password=password,synccode=synccode,se_market_report=se_market_report,records_ov=records_ov,search_form=search_form)


def sales_report_area_wise_url():

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    user_type = str(request.vars.user_type).strip().upper()
    password = str(request.vars.password).strip()
    synccode = str(request.vars.synccode).strip()
    area_id = str(request.vars.area_id).strip()
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()
    se_item_report = str(request.vars.se_item_report).strip().upper()
    se_market_report = str(request.vars.se_market_report).strip().upper()
    # order_date=str(request.vars.order_date).strip()
    
    session.cid=cid
    session.rep_id=rep_id
    session.rep_id=rep_id
    session.user_type=user_type
    session.password=password
    session.synccode=synccode
    session.area_id=area_id

    session.rep_id_report=rep_id_report
    session.se_item_report=se_item_report
    session.se_market_report=se_market_report
    # session.order_date=order_date
    redirect(URL(c='sales_report',f='sales_report_area_wise'))



def sales_report_area_wise():
    cid=session.cid
    rep_id=session.rep_id
    user_type=session.user_type
    password=session.password
    synccode=session.synccode
    area_id=session.area_id

    rep_id_report=session.rep_id_report
    se_item_report=session.se_item_report
    se_market_report=session.se_market_report
    # return session.order_date
    order_date=session.order_date
    # return order_date
    
    
    now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    date_to=now + datetime.timedelta(days = 1)
    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = str(repRow[0].user_type).upper()

    
    if (user_type == 'SUP'):
        level_rep = repRow[0].level_id
        depth = repRow[0].field2
        level = 'level' + str(depth)
    
    report_string=""
    
    report_str=""
    
    if (user_type=='REP'):

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
        

        #    Sales Call====================
        # qset=db()
        # qset=qset((db.sm_order_head.cid == cid) )
        # qset=qset(db.sm_order_head.order_date == order_date)
        # qset=qset(db.sm_order_head.area_id==area_id)
        # records=qset.select(db.sm_order_head.sl)#.count())
        # # return db._lastsql
        # if records:
        #     sales_call=records[0][db.sm_order_head.sl.count()]
        
        # report_string=str(sales_call)
        #  Order Count  
        # qset_oc=db()
        # qset_oc=qset_oc((db.sm_order_head.cid == cid)  & (db.sm_order_head.field1 == 'ORDER')) 
        # qset_oc=qset_oc(db.sm_order_head.order_date == order_date)
        # qset_oc=qset_oc(db.sm_order_head.area_id==area_id)
        # records_oc=qset_oc.select(db.sm_order_head.sl.count())
        # # return db._lastsql
        # if records_oc:
        #     order_count=records_oc[0][db.sm_order_head.sl.count()]
        
        
        condition=""      
        # condition="and sm_order.area_id  IN ("+str(repAreaStr)+")"  
        
        condition="and sm_order.area_id  = '"+str(area_id) +"'"  
        condition="and sm_order.order_date  >= '"+str(session.from_dt) +"' and sm_order.order_date  <= '"+str(session.to_date) +"'"
        records_ov=[]
        sql_str="SELECT (sm_order.client_id) as client_id,(sm_order.client_name) as client_name,SUM((sm_order.price) * (sm_order.quantity)) as totalprice, sm_order.area_id as area_id, sm_order.vsl as vsl FROM sm_order WHERE sm_order.cid = '"+ str(cid)+"' and sm_order.rep_id ='"+ rep_id +"'" +condition+"  GROUP BY area_id,vsl ORDER BY `vsl` DESC  ;"
        # return sql_str
        records_ov=db.executesql(sql_str,as_dict = True)

    if (user_type=='SUP'):
       

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
        cTeam=0
        for i in range(len(levelList)):
            levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
            for levelRow in levelRows:
                level_id = levelRow.level_id
                special_territory_code = levelRow.special_territory_code
                if level_id==special_territory_code:
                    cTeam=1

                if marketStr=='':
                    marketStr="'"+str(level_id)+"'"
                else:
                    marketStr=marketStr+",'"+str(level_id)+"'" 
            if cTeam==1:    
                if special_territory_code not in spicial_codeList:
                    if (special_territory_code !='' and level_id==special_territory_code):
                        spicial_codeList.append(special_territory_code)    
            
                    levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level.special_territory_code.belongs(spicial_codeList)) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)        

                    for levelSpecialRow in levelSpecialRows:
                        level_id = levelSpecialRow.level_id
                        if marketStr=='':
                            marketStr="'"+str(Suplevel_id)+"'"
                        else:
                            marketStr=marketStr+",'"+str(level_id)+"'" 
        qset=db()
        qset=qset((db.sm_order_head.cid == cid) )
        qset=qset(db.sm_order_head.order_date == order_date)
        qset=qset(db.sm_order_head.area_id==area_id)
        records=qset.select(db.sm_order_head.sl.count())
        if records:
            sales_call=records[0][db.sm_order_head.sl.count()]
        
        report_string=str(sales_call)
        #  Order Count  
        qset_oc=db()
        qset_oc=qset_oc((db.sm_order_head.cid == cid)  & (db.sm_order_head.field1 == 'ORDER')) 
        qset_oc=qset_oc(db.sm_order_head.order_date == order_date)
        qset_oc=qset_oc(db.sm_order_head.area_id==area_id)
        records_oc=qset_oc.select(db.sm_order_head.sl.count())
        # return db._lastsql
        if records_oc:
            order_count=records_oc[0][db.sm_order_head.sl.count()]

        condition=''
        condition=condition+" AND area_id IN ("+str(marketStr)+")"  

        records_ov=[]
        sql_str="SELECT (sm_order.client_id) as client_id,(sm_order.client_name) as client_name,SUM((sm_order.price) * (sm_order.quantity)) as totalprice, sm_order.area_id as area_id, sm_order.vsl as vsl FROM sm_order WHERE sm_order.cid = '"+ str(cid) +"' and sm_order.area_id='"+ area_id+"' and sm_order.order_date='"+ order_date+"'   GROUP BY area_id,order_date,vsl ORDER BY vsl DESC  ;"

        records_ov=db.executesql(sql_str,as_dict = True)               


    order_date=''
    return dict(date_to=date_to,cid=cid,rep_id=rep_id,password=password,synccode=synccode,records_ov=records_ov,area_id=area_id,order_date=order_date)


def sales_report_slWise():
    cid = session.cid       
    rep_id = session.rep_id    
    user_type = session.user_type    
    password = session.password    
    synccode = session.synccode    
    area_id = session.area_id    
    vsl = session.vsl    
    client_id = session.client_id    

    order_date = session.order_date  
    

    now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    date_ton=now + datetime.timedelta(days = 1)
    date_to=str(date_ton).split(' ')[0]

        
    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = str(repRow[0].user_type).upper()

    
    if (user_type == 'SUP'):
        level_rep = repRow[0].level_id
        depth = repRow[0].field2
        level = 'level' + str(depth)
    
    report_string=""
    
    report_str=""
    
    if (user_type=='REP'):

        records_ov=[]
        sql_str="SELECT client_name,rep_id,rep_name,SUM(sm_order.quantity) as item_qty, sm_order.item_id as item_id,sm_order.item_name as item_name, sm_order.quantity as qty,((sm_order.price) * (sm_order.quantity)) as amnt, sm_order.vsl as vsl,sm_order.order_date as order_date FROM sm_order WHERE sm_order.cid = '"+ str(cid) +"' AND sm_order.vsl= '"+ str(vsl) +"' AND sm_order.area_id='"+str(area_id)+"' AND sm_order.client_id='"+str(client_id)+"'  GROUP BY sm_order.area_id,item_id;"
        # -- sql_str="SELECT client_name,rep_id,rep_name,SUM(sm_order.quantity) as item_qty, sm_order.item_id as item_id,sm_order.item_name as item_name, sm_order.quantity as qty,((sm_order.price) * (sm_order.quantity)) as amnt, sm_order.vsl as vsl,sm_order.order_date as order_date,(SELECT SUM((sm_order.price) * (sm_order.quantity))  FROM sm_order  WHERE sm_order.cid = '"+ str(cid) +"' AND sm_order.rep_id = '"+ str(rep_id) +"' AND sm_order.order_date = '"+ str(order_date) +"' AND sm_order.vsl= '"+ str(vsl) +"' AND sm_order.area_id='"+str(area_id)+"' AND sm_order.client_id='"+str(client_id)+"'  GROUP BY sm_order.area_id) as totalprice FROM sm_order WHERE sm_order.cid = '"+ str(cid) +"' AND sm_order.rep_id = '"+ str(rep_id) +"' AND sm_order.order_date = '"+ str(order_date) +"' AND sm_order.vsl= '"+ str(vsl) +"' AND sm_order.area_id='"+str(area_id)+"' AND sm_order.client_id='"+str(client_id)+"'  GROUP BY sm_order.area_id,item_id;"
        # return sql_str
        records_ov=db.executesql(sql_str,as_dict = True)
    if (user_type=='SUP'):

        records_ov=[]
        sql_str="SELECT client_name,rep_id,rep_name,SUM(sm_order.quantity) as item_qty, sm_order.item_id as item_id,sm_order.item_name as item_name, sm_order.quantity as qty,((sm_order.price) * (sm_order.quantity)) as amnt, sm_order.vsl as vsl,sm_order.order_date as order_date FROM sm_order WHERE sm_order.cid = '"+ str(cid) +"' AND sm_order.vsl= '"+ str(vsl) +"' AND sm_order.area_id='"+str(area_id)+"' AND sm_order.client_id='"+str(client_id)+"'  GROUP BY sm_order.area_id,item_id;"
        # return sql_str
        records_ov=db.executesql(sql_str,as_dict = True)
    # client_name=''
    for i in range(len(records_ov)):
      records_ov_dict=records_ov[i]  
      order_date=str(records_ov_dict["order_date"]) 
      client_name=str(records_ov_dict["client_name"]) 
      rep_id=str(records_ov_dict["rep_id"]) 
      rep_name=str(records_ov_dict["rep_name"]) 


    return dict(records_ov=records_ov,vsl=vsl,order_date=order_date,area_id=area_id,client_id=client_id,rep_id=rep_id)



def sales_report_slWise_url():

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    user_type = str(request.vars.user_type).strip().upper()
    password = str(request.vars.password).strip()
    synccode = str(request.vars.synccode).strip()
    area_id = str(request.vars.area_id).strip()
    vsl = str(request.vars.vsl).strip()
    client_id = str(request.vars.client_id).strip().upper()

    order_date=str(request.vars.order_date).strip()
    

    session.cid = cid
    session.rep_id = rep_id
    session.user_type = user_type
    session.password = password
    session.synccode = synccode
    session.area_id = area_id
    session.vsl = vsl
    session.client_id = client_id
    session.order_date = order_date

    redirect(URL(c='sales_report',f='sales_report_slWise'))
    




# ============================ DOCTOR =======================
# ============================ DOCTOR =======================


# ============================ DOCTOR =======================
# ============================ DOCTOR =======================

def salesDcr_report_zm_url():

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    user_type = str(request.vars.user_type).strip().upper()
    password = str(request.vars.password).strip()
    synccode = str(request.vars.synccode).strip()
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()
    # se_item_report = str(request.vars.se_item_report).strip().upper()
    # se_market_report = str(request.vars.se_market_report).strip().upper()
    # level_id = str(request.vars.level_id).strip().upper()

    session.cid = cid
    session.rep_id = rep_id
    session.user_type = user_type
    session.password = password
    session.synccode = synccode
    session.rep_id_report = rep_id_report
    # session.se_item_report = se_item_report
    # session.se_market_report = se_market_report
    # session.level_id = level_id
    # return session.rep_id

    

    redirect(URL(c='sales_report',f='salesDcr_report_zm'))



def salesDcr_report_zm():

    cid =session.cid 
    rep_id =session.rep_id 
    user_type =session.user_type 
    password =session.password
    synccode =session.synccode 
    rep_id_report =session.rep_id_report 
    rep_id_report =session.rep_id_report
    
    date_from=current_date
    now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    date_ton=now - datetime.timedelta(days = 1)
    date_to=str(date_ton).split(' ')[0]

    from_dt=''
    to_date=''

    btn_filter=request.vars.btn_filter
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    if btn_filter:

        from_dt = str(request.vars.from_dt).strip().upper()
        to_date= str(request.vars.to_dt).strip().upper()

        session.btn_filter=btn_filter
        reqPage=0
    elif btn_all:
        session.btn_filter=None
        reqPage=0
        
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    search_form =SQLFORM(db.sm_search_date)
    
    user_type = str(request.vars.user_type).strip().upper()

    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))

    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = str(repRow[0].user_type).upper()

       # pass
    
    if (user_type == 'SUP'):
        level_rep = repRow[0].level_id
        depth = repRow[0].field2
        level = 'level' + str(depth)

    report_string=""
    
    report_str=""

    dateFlag=''
    reqPage=len(request.args)
    dateFlag=True
    try:
        from_dt=datetime.datetime.strptime(str(to_dt_2),'%Y-%m-%d')
        to_dt=datetime.datetime.strptime(str(to_date),'%Y-%m-%d')
    except:
        dateFlag=False
    
    if (user_type=='REP'):
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
    

        qset=db()
        qset = qset(db.sm_doctor_visit.cid == cid)
        qset = qset(db.sm_doctor_visit.rep_id == rep_id)
        qset = qset(db.sm_doctor_visit.route_id.belongs(rp_areaList))
        qset = qset((db.sm_doctor_visit.visit_date <= date_from) and (db.sm_doctor_visit.visit_date > date_to))
       
        if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
            qset=qset((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))

        records = qset.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.doc_id,db.sm_doctor_visit.rep_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id)
        
        doc_id_list=[]
        visit_date_list=[]
        if records:
            for i in range(len(records)):
                recordListStr = records[i]
                doc_id = recordListStr[db.sm_doctor_visit.doc_id]

                visit_date = recordListStr[db.sm_doctor_visit.visit_date]
                doc_id_list.append(doc_id)
                visit_date_list.append(visit_date)
                

        qsetCount=db()
        qsetCount = qsetCount(db.sm_doctor_visit.cid == cid)
        qsetCount = qsetCount(db.sm_doctor_visit.rep_id == rep_id)
        qsetCount = qsetCount(db.sm_doctor_visit.giftnsample!='')
        qsetCount = qsetCount(db.sm_doctor_visit.route_id.belongs(rp_areaList))
        qsetCount = qsetCount((db.sm_doctor_visit.visit_date <= date_from) and (db.sm_doctor_visit.visit_date > date_to))
       
        if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
            qsetCount=qsetCount((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))

        recordsCount = qsetCount.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id)
        vChecklist=[]
        vCountList=[]
        for recordsCount in recordsCount:
            vCount=recordsCount[db.sm_doctor_visit.doc_id.count()]
            vCheck=str(recordsCount[db.sm_doctor_visit.rep_id])+'|'+str(recordsCount[db.sm_doctor_visit.visit_date])
            vChecklist.append(vCheck)
            vCountList.append(vCount)


    if (user_type=='SUP'):
        levelList=[]
        SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)

        levelStr=''
        for SuplevelRows in SuplevelRows:
            Suplevel_id = SuplevelRows.level_id
            depth = SuplevelRows.level_depth_no
            level = 'level' + str(depth)#+'_id'
            # return Suplevel_id
            if Suplevel_id not in levelList:
                levelList.append(Suplevel_id)
                if levelStr=='':
                    levelStr="'"+str(Suplevel_id)+"'"
                else:
                    levelStr=levelStr+",'"+str(Suplevel_id)+"'" 
        
        marketStr=''
        marketStrList=[]
       
        cTeam=0        
        for i in range(len(levelList)):
            if (level=='level0'):
                levelRows = db((db.sm_level.cid == cid) &(db.sm_level.depth == '0') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
            if (level=='level1'):
                levelRows = db((db.sm_level.cid == cid) &(db.sm_level.depth == '1') &(db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
                        
            if (level=='level2'):
                levelRows = db((db.sm_level.cid == cid)  &(db.sm_level.depth == '2') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
            
            for levelRow in levelRows:
                level_id = levelRow.level_id
                marketStrList.append(level_id)
                # return level_id
                special_territory_code = levelRow.special_territory_code
                if level_id==special_territory_code:
                    cTeam=1

                if marketStr=='':
                    marketStr="'"+str(level_id)+"'"
                else:
                    marketStr=marketStr+",'"+str(level_id)+"'" 
            # return marketStr

            if cTeam==1:    
                if special_territory_code not in spicial_codeList:
                    if (special_territory_code !='' and level_id==special_territory_code):
                        spicial_codeList.append(special_territory_code)    
            
                    # levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.special_territory_code.belongs(spicial_codeList)) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)        
                    levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level.special_territory_code.belongs(spicial_codeList)) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)        

                    for levelSpecialRow in levelSpecialRows:
                        level_id = levelSpecialRow.level_id
                        marketStrList.append(level_id)

                        if marketStr=='':
                            marketStr="'"+str(Suplevel_id)+"'"
                        else:
                            marketStr=marketStr+",'"+str(level_id)+"'" 


        # for i in range(len(levelList)):            
        #     levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
        #     for levelRow in levelRows:
        #         level_id = levelRow.level_id
        #         marketStrList.append(level_id)

        #         special_territory_code = levelRow.special_territory_code
        #         if level_id==special_territory_code:
        #             cTeam=1

        #         if marketStr=='':
        #             marketStr="'"+str(level_id)+"'"
        #         else:
        #             marketStr=marketStr+",'"+str(level_id)+"'"      

        # return date_to
        qset=db()
        qset = qset(db.sm_doctor_visit.cid == cid)
        qset = qset(db.sm_doctor_visit.level0_id.belongs(marketStrList))
       
        if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
            qset=qset((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))
        else:
            qset = qset((db.sm_doctor_visit.visit_date <= date_from) & (db.sm_doctor_visit.visit_date > date_to))

        records = qset.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.level0_id,db.sm_doctor_visit.level0_name,db.sm_doctor_visit.visit_date, orderby=~db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.level0_id)
        # return db._lastsql
        doc_id_list=[]
        visit_date_list=[]
        if records:
            for i in range(len(records)):
                recordListStr = records[i]
                doc_id = recordListStr[db.sm_doctor_visit.doc_id]

                visit_date = recordListStr[db.sm_doctor_visit.visit_date]
                doc_id_list.append(doc_id)
                visit_date_list.append(visit_date)
                

        qsetCount=db()
        qsetCount = qsetCount(db.sm_doctor_visit.cid == cid)
        qsetCount = qsetCount(db.sm_doctor_visit.giftnsample!='')
        qsetCount = qsetCount(db.sm_doctor_visit.level0_id.belongs(marketStrList))
        qsetCount = qsetCount((db.sm_doctor_visit.visit_date <= date_from) and (db.sm_doctor_visit.visit_date > date_to))
       
        if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
            qsetCount=qsetCount((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))

        recordsCount = qsetCount.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.level0_id,db.sm_doctor_visit.level0_name,db.sm_doctor_visit.visit_date, orderby=~db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.level0_id)
        vChecklist=[]
        vCountList=[]
        for recordsCount in recordsCount:
            vCount=recordsCount[db.sm_doctor_visit.doc_id.count()]
            vCheck=str(recordsCount[db.sm_doctor_visit.rep_id])+'|'+str(recordsCount[db.sm_doctor_visit.visit_date])
            vChecklist.append(vCheck)
            vCountList.append(vCount)

    return dict(doc_id_list=doc_id_list,records=records,date_to=date_to,cid=cid,rep_id=rep_id,password=password,synccode=synccode,vChecklist=vChecklist,vCountList=vCountList,search_form=search_form)


def salesDcr_report_rsm_url():

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    user_type = str(request.vars.user_type).strip().upper()
    password = str(request.vars.password).strip()
    synccode = str(request.vars.synccode).strip()
    try:
        route_id = str(request.vars.route_id).strip()
    except:
        route_id=''
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()
    # se_item_report = str(request.vars.se_item_report).strip().upper()
    # se_market_report = str(request.vars.se_market_report).strip().upper()
    # level_id = str(request.vars.level_id).strip().upper()

    session.cid = cid
    session.rep_id = rep_id
    session.user_type = user_type
    session.password = password
    session.synccode = synccode
    session.rep_id_report = rep_id_report
    session.route_id = route_id
    # session.se_item_report = se_item_report
    # session.se_market_report = se_market_report
    # session.level_id = level_id
    # return session.rep_id

    redirect(URL(c='sales_report',f='salesDcr_report_rsm'))


def salesDcr_report_rsm():
    cid =session.cid 
    rep_id =session.rep_id 
    user_type =session.user_type 
    password =session.password
    synccode =session.synccode 
    rep_id_report =session.rep_id_report 
    rep_id_report =session.rep_id_report
    
    date_from=current_date
    now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    date_ton=now - datetime.timedelta(days = 1)
    date_to=str(date_ton).split(' ')[0]

    from_dt=''
    to_date=''

    btn_filter=request.vars.btn_filter
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    
    if btn_filter:
        from_dt = str(request.vars.to_dt_2).strip().upper()
        to_date= str(request.vars.to_dt).strip().upper()
        session.btn_filter=btn_filter
        reqPage=0
    
    elif btn_all:
        session.btn_filter=None
        reqPage=0
        
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    search_form =SQLFORM(db.sm_search_date)
    
    user_type = str(request.vars.user_type).strip().upper()

    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
    # return repRow
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = str(repRow[0].user_type).upper()
       # pass
    
    if (user_type == 'SUP'):
        level_rep = repRow[0].level_id
        depth = repRow[0].field2
        level = 'level' + str(depth)

    report_string=""    
    report_str=""

    dateFlag=''
    reqPage=len(request.args)
    dateFlag=True
    try:
        from_dt=datetime.datetime.strptime(str(from_dt),'%Y-%m-%d')
        to_dt=datetime.datetime.strptime(str(to_date),'%Y-%m-%d')
    except:
        dateFlag=False
    
    if (user_type=='REP'):
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
    

        qset=db()
        qset = qset(db.sm_doctor_visit.cid == cid)
        qset = qset(db.sm_doctor_visit.rep_id == rep_id)
        qset = qset(db.sm_doctor_visit.route_id.belongs(rp_areaList))
        qset = qset((db.sm_doctor_visit.visit_date <= date_from) and (db.sm_doctor_visit.visit_date > date_to))
       
        if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
            qset=qset((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))

        records = qset.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.doc_id,db.sm_doctor_visit.rep_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id)
        # return db._lastsql
        doc_id_list=[]
        visit_date_list=[]
        if records:
            for i in range(len(records)):
                recordListStr = records[i]
                doc_id = recordListStr[db.sm_doctor_visit.doc_id]

                visit_date = recordListStr[db.sm_doctor_visit.visit_date]
                doc_id_list.append(doc_id)
                visit_date_list.append(visit_date)
                

        qsetCount=db()
        qsetCount = qsetCount(db.sm_doctor_visit.cid == cid)
        qsetCount = qsetCount(db.sm_doctor_visit.rep_id == rep_id)
        qsetCount = qsetCount(db.sm_doctor_visit.giftnsample!='')
        qsetCount = qsetCount(db.sm_doctor_visit.route_id.belongs(rp_areaList))
        qsetCount = qsetCount((db.sm_doctor_visit.visit_date <= date_from) and (db.sm_doctor_visit.visit_date > date_to))
       
        if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
            qsetCount=qsetCount((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))

        recordsCount = qsetCount.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id)
        vChecklist=[]
        vCountList=[]
        for recordsCount in recordsCount:
            vCount=recordsCount[db.sm_doctor_visit.doc_id.count()]
            vCheck=str(recordsCount[db.sm_doctor_visit.rep_id])+'|'+str(recordsCount[db.sm_doctor_visit.visit_date])
            vChecklist.append(vCheck)
            vCountList.append(vCount)


    if (user_type=='SUP'):
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
        
        marketStr=''
        marketStrList=[]
        
        cTeam=0        
        for i in range(len(levelList)):
            
            if (level=='level0'):
                levelRows = db((db.sm_level.cid == cid) &(db.sm_level.depth == '1') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
            
            if (level=='level1'):
                levelRows = db((db.sm_level.cid == cid) &(db.sm_level.depth == '1') &(db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
                        
            # if (level=='level2'):
            #     levelRows = db((db.sm_level.cid == cid)  &(db.sm_level.depth == '2') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
            
            for levelRow in levelRows:
                level_id = levelRow.level_id
                marketStrList.append(level_id)
                # return level_id
                special_territory_code = levelRow.special_territory_code
                if level_id==special_territory_code:
                    cTeam=1

                if marketStr=='':
                    marketStr="'"+str(level_id)+"'"
                else:
                    marketStr=marketStr+",'"+str(level_id)+"'" 
            # return marketStr

            if cTeam==1:    
                if special_territory_code not in spicial_codeList:
                    if (special_territory_code !='' and level_id==special_territory_code):
                        spicial_codeList.append(special_territory_code)    
            
                    # levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.special_territory_code.belongs(spicial_codeList)) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)        
                    levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level.special_territory_code.belongs(spicial_codeList)) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)        

                    for levelSpecialRow in levelSpecialRows:
                        level_id = levelSpecialRow.level_id
                        x
                        marketStrList.append(level_id)

                        if marketStr=='':
                            marketStr="'"+str(Suplevel_id)+"'"
                        else:
                            marketStr=marketStr+",'"+str(level_id)+"'"


        # for i in range(len(levelList)):
            
        #     levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
        #     for levelRow in levelRows:
        #         level_id = levelRow.level_id
        #         marketStrList.append(level_id)

        #         special_territory_code = levelRow.special_territory_code
        #         if level_id==special_territory_code:
        #             cTeam=1

        #         if marketStr=='':
        #             marketStr="'"+str(level_id)+"'"
        #         else:
        #             marketStr=marketStr+",'"+str(level_id)+"'"      


        qset=db()
        qset = qset(db.sm_doctor_visit.cid == cid)
        # qset = qset(db.sm_doctor_visit.level1_id.belongs(marketStrList))
        # return session.route_id
        # if session.route_id!='':
        #     qset = qset(db.sm_doctor_visit.level0_id == session.route_id)
        # else:
        qset = qset(db.sm_doctor_visit.level1_id.belongs(marketStrList))
        qset = qset((db.sm_doctor_visit.visit_date <= date_from) and (db.sm_doctor_visit.visit_date > date_to))
       

        # qset = qset((db.sm_doctor_visit.visit_date <= date_from) & (db.sm_doctor_visit.visit_date > date_to))
       
        if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
            qset=qset((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))

        records = qset.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.level1_id,db.sm_doctor_visit.level1_name,db.sm_doctor_visit.visit_date, orderby=~db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.level1_id)
        # return db._lastsql
        doc_id_list=[]
        visit_date_list=[]
        if records:
            for i in range(len(records)):
                recordListStr = records[i]
                doc_id = recordListStr[db.sm_doctor_visit.doc_id]

                visit_date = recordListStr[db.sm_doctor_visit.visit_date]
                doc_id_list.append(doc_id)
                visit_date_list.append(visit_date)
                

        qsetCount=db()
        qsetCount = qsetCount(db.sm_doctor_visit.cid == cid)
        qsetCount = qsetCount(db.sm_doctor_visit.giftnsample!='')
        if session.route_id!='':
            qsetCount = qsetCount(db.sm_doctor_visit.level0_id == session.route_id)
        else:
            qsetCount = qsetCount(db.sm_doctor_visit.level1_id.belongs(marketStrList))
        qsetCount = qsetCount((db.sm_doctor_visit.visit_date <= date_from) and (db.sm_doctor_visit.visit_date > date_to))
       
        if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
            qsetCount=qsetCount((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))

        recordsCount = qsetCount.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.level1_id,db.sm_doctor_visit.level1_name,db.sm_doctor_visit.visit_date, orderby=~db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.level1_id)
        # return db._lastsql
        vChecklist=[]
        vCountList=[]
        for recordsCount in recordsCount:
            vCount=recordsCount[db.sm_doctor_visit.doc_id.count()]
            vCheck=str(recordsCount[db.sm_doctor_visit.rep_id])+'|'+str(recordsCount[db.sm_doctor_visit.visit_date])
            vChecklist.append(vCheck)
            vCountList.append(vCount)

    return dict(doc_id_list=doc_id_list,records=records,date_to=date_to,cid=cid,rep_id=rep_id,password=password,synccode=synccode,vChecklist=vChecklist,vCountList=vCountList,search_form=search_form)


def salesDcr_report_fm_url():

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    user_type = str(request.vars.user_type).strip().upper()
    password = str(request.vars.password).strip()
    synccode = str(request.vars.synccode).strip()
    try:
        route_id = str(request.vars.route_id).strip()
    except:
        route_id=''
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()
    # se_item_report = str(request.vars.se_item_report).strip().upper()
    # se_market_report = str(request.vars.se_market_report).strip().upper()
    # level_id = str(request.vars.level_id).strip().upper()

    session.cid = cid
    session.rep_id = rep_id
    session.user_type = user_type
    session.password = password
    session.synccode = synccode
    session.rep_id_report = rep_id_report
    session.route_id = route_id

    # session.se_item_report = se_item_report
    # session.se_market_report = se_market_report
    # session.level_id = level_id
    # return session.rep_id

    redirect(URL(c='sales_report',f='salesDcr_report_fm'))


def salesDcr_report_fm():
    cid =session.cid 
    rep_id =session.rep_id 
    user_type =session.user_type 
    password =session.password
    synccode =session.synccode 
    rep_id_report =session.rep_id_report 
    rep_id_report =session.rep_id_report
    
    date_from=current_date
    now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    date_ton=now - datetime.timedelta(days = 1)
    date_to=str(date_ton).split(' ')[0]

    from_dt=''
    to_date=''

    btn_filter=request.vars.btn_filter
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    if btn_filter:

        from_dt = str(request.vars.from_dt).strip().upper()
        to_date= str(request.vars.to_dt).strip().upper()

        session.btn_filter=btn_filter
        reqPage=0
    elif btn_all:
        session.btn_filter=None
        reqPage=0
        
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    search_form =SQLFORM(db.sm_search_date)
    
    user_type = str(request.vars.user_type).strip().upper()

    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
    # return repRow
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = str(repRow[0].user_type).upper()

       # pass
    
    if (user_type == 'SUP'):
        level_rep = repRow[0].level_id
        depth = repRow[0].field2
        level = 'level' + str(depth)

    report_string=""
    
    report_str=""

    dateFlag=''
    reqPage=len(request.args)
    dateFlag=True
    try:
        from_dt=datetime.datetime.strptime(str(from_dt),'%Y-%m-%d')
        to_dt=datetime.datetime.strptime(str(to_date),'%Y-%m-%d')
    except:
        dateFlag=False
    
    if (user_type=='REP'):
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
    

        qset=db()
        qset = qset(db.sm_doctor_visit.cid == cid)
        qset = qset(db.sm_doctor_visit.rep_id == rep_id)
        if session.route_id!='':
            qset = qset(db.sm_doctor_visit.level1_id == session.route_id)
        else:
            qset = qset(db.sm_doctor_visit.route_id.belongs(rp_areaList))

        
        qset = qset((db.sm_doctor_visit.visit_date <= date_from) & (db.sm_doctor_visit.visit_date > date_to))
       
        if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
            qset=qset((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))

        records = qset.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.doc_id,db.sm_doctor_visit.rep_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id)
        # return db._lastsql
        doc_id_list=[]
        visit_date_list=[]
        if records:
            for i in range(len(records)):
                recordListStr = records[i]
                doc_id = recordListStr[db.sm_doctor_visit.doc_id]

                visit_date = recordListStr[db.sm_doctor_visit.visit_date]
                doc_id_list.append(doc_id)
                visit_date_list.append(visit_date)
                

        qsetCount=db()
        qsetCount = qsetCount(db.sm_doctor_visit.cid == cid)
        qsetCount = qsetCount(db.sm_doctor_visit.rep_id == rep_id)
        qsetCount = qsetCount(db.sm_doctor_visit.giftnsample!='')
        if session.route_id!='':
            qsetCount = qsetCount(db.sm_doctor_visit.level1_id == session.route_id)
        else:
            qsetCount = qsetCount(db.sm_doctor_visit.route_id.belongs(rp_areaList))
        qsetCount = qsetCount((db.sm_doctor_visit.visit_date <= date_from) & (db.sm_doctor_visit.visit_date > date_to))
       
        if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
            qsetCount=qsetCount((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))

        recordsCount = qsetCount.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id)
        # return db._lastsql
        vChecklist=[]
        vCountList=[]
        for recordsCount in recordsCount:
            vCount=recordsCount[db.sm_doctor_visit.doc_id.count()]
            vCheck=str(recordsCount[db.sm_doctor_visit.rep_id])+'|'+str(recordsCount[db.sm_doctor_visit.visit_date])
            vChecklist.append(vCheck)
            vCountList.append(vCount)


    if (user_type=='SUP'):
        levelList=[]
        SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)

        
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
        marketStr=''
        marketStrList=[]
        
        cTeam=0        
        for i in range(len(levelList)):
            
            if (level=='level0'):
                levelRows = db((db.sm_level.cid == cid) &(db.sm_level.depth == '2') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
            
            if (level=='level1'):
                levelRows = db((db.sm_level.cid == cid) &(db.sm_level.depth == '2') &(db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
                        
            # if (level=='level2'):
            #     levelRows = db((db.sm_level.cid == cid)  &(db.sm_level.depth == '2') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
            
            for levelRow in levelRows:
                level_id = levelRow.level_id
                marketStrList.append(level_id)
                # return level_id
                special_territory_code = levelRow.special_territory_code
                if level_id==special_territory_code:
                    cTeam=1

                if marketStr=='':
                    marketStr="'"+str(level_id)+"'"
                else:
                    marketStr=marketStr+",'"+str(level_id)+"'" 
            # return marketStr

            if cTeam==1:    
                if special_territory_code not in spicial_codeList:
                    if (special_territory_code !='' and level_id==special_territory_code):
                        spicial_codeList.append(special_territory_code)    
            
                    # levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.special_territory_code.belongs(spicial_codeList)) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)        
                    levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level.special_territory_code.belongs(spicial_codeList)) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)        

                    for levelSpecialRow in levelSpecialRows:
                        level_id = levelSpecialRow.level_id
                        x
                        marketStrList.append(level_id)

                        if marketStr=='':
                            marketStr="'"+str(Suplevel_id)+"'"
                        else:
                            marketStr=marketStr+",'"+str(level_id)+"'"


        # for i in range(len(levelList)):
            
        #     levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
        #     for levelRow in levelRows:
        #         level_id = levelRow.level_id
        #         marketStrList.append(level_id)

        #         special_territory_code = levelRow.special_territory_code
        #         if level_id==special_territory_code:
        #             cTeam=1

        #         if marketStr=='':
        #             marketStr="'"+str(level_id)+"'"
        #         else:
        #             marketStr=marketStr+",'"+str(level_id)+"'"      


        qset=db()
        qset = qset(db.sm_doctor_visit.cid == cid)
        if session.route_id!='':
            qset = qset(db.sm_doctor_visit.level1_id == session.route_id)
        else:
            qset = qset(db.sm_doctor_visit.level2_id.belongs(marketStrList))
        qset = qset((db.sm_doctor_visit.visit_date <= date_from) & (db.sm_doctor_visit.visit_date > date_to))
       
        if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
            qset=qset((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))

        records = qset.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.level2_id,db.sm_doctor_visit.level2_name,db.sm_doctor_visit.visit_date, orderby=~db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.level2_id)
        # return db._lastsql
        doc_id_list=[]
        visit_date_list=[]
        if records:
            for i in range(len(records)):
                recordListStr = records[i]
                doc_id = recordListStr[db.sm_doctor_visit.doc_id]

                visit_date = recordListStr[db.sm_doctor_visit.visit_date]
                doc_id_list.append(doc_id)
                visit_date_list.append(visit_date)
                

        qsetCount=db()
        qsetCount = qsetCount(db.sm_doctor_visit.cid == cid)
        qsetCount = qsetCount(db.sm_doctor_visit.giftnsample!='')
        if session.route_id!='':
            qsetCount = qsetCount(db.sm_doctor_visit.level1_id == session.route_id)
        else:
            qsetCount = qsetCount(db.sm_doctor_visit.level2_id.belongs(marketStrList))
        qsetCount = qsetCount((db.sm_doctor_visit.visit_date <= date_from) & (db.sm_doctor_visit.visit_date > date_to))
       
        if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
            qsetCount=qsetCount((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))

        recordsCount = qsetCount.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.level2_id,db.sm_doctor_visit.level2_name,db.sm_doctor_visit.visit_date, orderby=~db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.level2_id)
        vChecklist=[]
        vCountList=[]
        for recordsCount in recordsCount:
            vCount=recordsCount[db.sm_doctor_visit.doc_id.count()]
            vCheck=str(recordsCount[db.sm_doctor_visit.rep_id])+'|'+str(recordsCount[db.sm_doctor_visit.visit_date])
            vChecklist.append(vCheck)
            vCountList.append(vCount)

    return dict(doc_id_list=doc_id_list,records=records,date_to=date_to,cid=cid,rep_id=rep_id,password=password,synccode=synccode,vChecklist=vChecklist,vCountList=vCountList,search_form=search_form)


def slsRptDcr_area_wise_url():

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    user_type = str(request.vars.user_type).strip().upper()
    password = str(request.vars.password).strip()
    synccode = str(request.vars.synccode).strip()
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()    
    visit_date=str(request.vars.visit_date).strip()  
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()


    route_id =str(request.vars.route_id)
    visit_date=str(request.vars.visit_date).strip()  
    # se_item_report = str(request.vars.se_item_report).strip().upper()
    # se_market_report = str(request.vars.se_market_report).strip().upper()
    # level_id = str(request.vars.level_id).strip().upper()

    session.cid = cid
    session.rep_id = rep_id
    session.user_type = user_type
    session.password = password
    session.synccode = synccode
    session.rep_id_report = rep_id_report
    session.password = password
    session.route_id = route_id 
    session.visit_date = visit_date
    # session.se_item_report = se_item_report
    # session.se_market_report = se_market_report
    # session.level_id = level_id


    redirect(URL(c='sales_report',f='slsRptDcr_area_wise'))


# def slsRptDcr_area_wise():
#     cid =session.cid 
#     rep_id =session.rep_id 
#     user_type =session.user_type 
#     password =session.password
#     synccode =session.synccode 
#     rep_id_report =session.rep_id_report 
#     rep_id_report =session.rep_id_report
#     # return rep_id
#     date_from=current_date
#     now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
#     date_ton=now - datetime.timedelta(days = 7)
#     date_to=str(date_ton).split(' ')[0]

#     from_dt=''
#     to_date=''

#     btn_filter=request.vars.btn_filter
#     btn_all=request.vars.btn_all
#     reqPage=len(request.args)
#     if btn_filter:

#         from_dt = str(request.vars.from_dt).strip().upper()
#         to_date= str(request.vars.to_dt).strip().upper()

#         session.btn_filter=btn_filter
#         reqPage=0
#     elif btn_all:
#         session.btn_filter=None
#         reqPage=0
        
#     #--------paging
#     if reqPage:
#         page=int(request.args[0])
#     else:
#         page=0
#     items_per_page=session.items_per_page
#     search_form =SQLFORM(db.sm_search_date)
    
#     user_type = str(request.vars.user_type).strip().upper()

#     repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))

#     if not repRow:
#        retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
#        return retStatus
#     else:
#         user_type = str(repRow[0].user_type).upper()

#        # pass
    
#     if (user_type == 'SUP'):
#         level_rep = repRow[0].level_id
#         depth = repRow[0].field2
#         level = 'level' + str(depth)

#     report_string=""
    
#     report_str=""

#     dateFlag=''
#     reqPage=len(request.args)
#     dateFlag=True
#     try:
#         from_dt=datetime.datetime.strptime(str(from_dt),'%Y-%m-%d')
#         to_dt=datetime.datetime.strptime(str(to_date),'%Y-%m-%d')
#     except:
#         dateFlag=False
    
#     if (user_type=='REP'):
#         repAreaRow = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.rep_id == rep_id)).select(db.sm_rep_area.area_id,orderby=db.sm_rep_area.area_id,groupby=db.sm_rep_area.area_id)
#         if not repAreaRow:
#            retStatus = 'FAILED<SYNCDATA>Invalid Area'
#            return retStatus
#         else:

#             rp_areaList=[]
#             repAreaStr=''
#             for repAreaRow in repAreaRow:
#                 repArea_id=repAreaRow.area_id
#                 rp_areaList.append(repArea_id)
                
#                 if repAreaStr=='':
#                     repAreaStr="'"+str(repArea_id)+"'"
#                 else:
#                     repAreaStr=repAreaStr+",'"+str(repArea_id)+"'" 
    

#         qset=db()
#         qset = qset(db.sm_doctor_visit.cid == cid)
#         qset = qset(db.sm_doctor_visit.rep_id == rep_id)
#         qset = qset(db.sm_doctor_visit.route_id.belongs(rp_areaList))
#         qset = qset((db.sm_doctor_visit.visit_date <= date_from) and (db.sm_doctor_visit.visit_date > date_to))
       
#         if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
#             qset=qset((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))

#         records = qset.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.doc_id,db.sm_doctor_visit.rep_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id)
#         # return db._lastsql
#         doc_id_list=[]
#         visit_date_list=[]
#         if records:
#             for i in range(len(records)):
#                 recordListStr = records[i]
#                 doc_id = recordListStr[db.sm_doctor_visit.doc_id]

#                 visit_date = recordListStr[db.sm_doctor_visit.visit_date]
#                 doc_id_list.append(doc_id)
#                 visit_date_list.append(visit_date)
                

#         qsetCount=db()
#         qsetCount = qsetCount(db.sm_doctor_visit.cid == cid)
#         qsetCount = qsetCount(db.sm_doctor_visit.rep_id == rep_id)
#         qsetCount = qsetCount(db.sm_doctor_visit.giftnsample!='')
#         qsetCount = qsetCount(db.sm_doctor_visit.route_id.belongs(rp_areaList))
#         qsetCount = qsetCount((db.sm_doctor_visit.visit_date <= date_from) and (db.sm_doctor_visit.visit_date > date_to))
       
#         if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
#             qsetCount=qsetCount((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))

#         recordsCount = qsetCount.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id)
#         vChecklist=[]
#         vCountList=[]
#         for recordsCount in recordsCount:
#             vCount=recordsCount[db.sm_doctor_visit.doc_id.count()]
#             vCheck=str(recordsCount[db.sm_doctor_visit.rep_id])+'|'+str(recordsCount[db.sm_doctor_visit.visit_date])
#             vChecklist.append(vCheck)
#             vCountList.append(vCount)


#     if (user_type=='SUP'):
#         levelList=[]
#         SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)

        
#         levelStr=''
#         for SuplevelRows in SuplevelRows:
#             Suplevel_id = SuplevelRows.level_id
#             depth = SuplevelRows.level_depth_no
#             level = 'level' + str(depth)#+'_id'
#             if Suplevel_id not in levelList:
#                 levelList.append(Suplevel_id)
#                 if levelStr=='':
#                     levelStr="'"+str(Suplevel_id)+"'"
#                 else:
#                     levelStr=levelStr+",'"+str(Suplevel_id)+"'" 
#         marketStr=''
#         marketStrList=[]
        
#         cTeam=0        
#         for i in range(len(levelList)):
            
#             if (level=='level0'):
#                 levelRows = db((db.sm_level.cid == cid) &(db.sm_level.depth == '3') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
            
#             if (level=='level1'):
#                 levelRows = db((db.sm_level.cid == cid) &(db.sm_level.depth == '3') &(db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
                        
#             # if (level=='level2'):
#             #     levelRows = db((db.sm_level.cid == cid)  &(db.sm_level.depth == '2') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
            
#             for levelRow in levelRows:
#                 level_id = levelRow.level_id
#                 marketStrList.append(level_id)
#                 # return level_id
#                 special_territory_code = levelRow.special_territory_code
#                 if level_id==special_territory_code:
#                     cTeam=1

#                 if marketStr=='':
#                     marketStr="'"+str(level_id)+"'"
#                 else:
#                     marketStr=marketStr+",'"+str(level_id)+"'" 
#             # return marketStr

#             if cTeam==1:    
#                 if special_territory_code not in spicial_codeList:
#                     if (special_territory_code !='' and level_id==special_territory_code):
#                         spicial_codeList.append(special_territory_code)    
            
#                     # levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.special_territory_code.belongs(spicial_codeList)) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)        
#                     levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level.special_territory_code.belongs(spicial_codeList)) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)        

#                     for levelSpecialRow in levelSpecialRows:
#                         level_id = levelSpecialRow.level_id
#                         x
#                         marketStrList.append(level_id)

#                         if marketStr=='':
#                             marketStr="'"+str(Suplevel_id)+"'"
#                         else:
#                             marketStr=marketStr+",'"+str(level_id)+"'"


#         # for i in range(len(levelList)):
            
#         #     levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
#         #     for levelRow in levelRows:
#         #         level_id = levelRow.level_id
#         #         marketStrList.append(level_id)

#         #         special_territory_code = levelRow.special_territory_code
#         #         if level_id==special_territory_code:
#         #             cTeam=1

#         #         if marketStr=='':
#         #             marketStr="'"+str(level_id)+"'"
#         #         else:
#         #             marketStr=marketStr+",'"+str(level_id)+"'"      


#         qset=db()
#         qset = qset(db.sm_doctor_visit.cid == cid)
#         qset = qset(db.sm_doctor_visit.level3_id.belongs(marketStrList))
#         qset = qset((db.sm_doctor_visit.visit_date <= date_from) and (db.sm_doctor_visit.visit_date > date_to))
       
#         if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
#             qset=qset((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))

#         records = qset.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.level3_id,db.sm_doctor_visit.level3_name,db.sm_doctor_visit.visit_date, orderby=~db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.level3_id)
#         doc_id_list=[]
#         visit_date_list=[]
#         if records:
#             for i in range(len(records)):
#                 recordListStr = records[i]
#                 doc_id = recordListStr[db.sm_doctor_visit.doc_id]

#                 visit_date = recordListStr[db.sm_doctor_visit.visit_date]
#                 doc_id_list.append(doc_id)
#                 visit_date_list.append(visit_date)
                

#         qsetCount=db()
#         qsetCount = qsetCount(db.sm_doctor_visit.cid == cid)
#         qsetCount = qsetCount(db.sm_doctor_visit.giftnsample!='')
#         qsetCount = qsetCount(db.sm_doctor_visit.level3_id.belongs(marketStrList))
#         qsetCount = qsetCount((db.sm_doctor_visit.visit_date <= date_from) and (db.sm_doctor_visit.visit_date > date_to))
       
#         if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
#             qsetCount=qsetCount((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))

#         recordsCount = qsetCount.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.level3_id,db.sm_doctor_visit.level3_name,db.sm_doctor_visit.visit_date, orderby=~db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.level3_id)
#         vChecklist=[]
#         vCountList=[]
#         for recordsCount in recordsCount:
#             vCount=recordsCount[db.sm_doctor_visit.doc_id.count()]
#             vCheck=str(recordsCount[db.sm_doctor_visit.rep_id])+'|'+str(recordsCount[db.sm_doctor_visit.visit_date])
#             vChecklist.append(vCheck)
#             vCountList.append(vCount)

#     return dict(doc_id_list=doc_id_list,records=records,date_to=date_to,cid=cid,rep_id=rep_id,password=password,synccode=synccode,vChecklist=vChecklist,vCountList=vCountList,search_form=search_form)


def salesDcr_report_detail():

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.password).strip()
    synccode = str(request.vars.synccode).strip()
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()

    date_from=current_date
    now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    date_ton=now - datetime.timedelta(days = 7)
    date_to=str(date_ton).split(' ')[0]
    # return date_to

    from_dt=''
    to_date=''

    btn_filter=request.vars.btn_filter
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    if btn_filter:

        from_dt = str(request.vars.from_dt).strip().upper()
        to_date= str(request.vars.to_dt).strip().upper()

        session.btn_filter=btn_filter
        reqPage=0
    elif btn_all:
        session.btn_filter=None
        reqPage=0
        
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    search_form =SQLFORM(db.sm_search_date)
    
    user_type = str(request.vars.user_type).strip().upper()

    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = str(repRow[0].user_type).upper()

       # pass
    
    if (user_type == 'SUP'):
        level_rep = repRow[0].level_id
        depth = repRow[0].field2
        level = 'level' + str(depth)

    report_string=""
    
    report_str=""

    dateFlag=''
    reqPage=len(request.args)
    dateFlag=True
    try:
        from_dt=datetime.datetime.strptime(str(from_dt),'%Y-%m-%d')
        to_dt=datetime.datetime.strptime(str(to_date),'%Y-%m-%d')
    except:
        dateFlag=False
    
    if (user_type=='REP'):
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
    

        qset=db()
        qset = qset(db.sm_doctor_visit.cid == cid)
        qset = qset(db.sm_doctor_visit.rep_id == rep_id)
        qset = qset(db.sm_doctor_visit.route_id.belongs(rp_areaList))
        qset = qset((db.sm_doctor_visit.visit_date <= date_from) and (db.sm_doctor_visit.visit_date > date_to))
       
        if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
            qset=qset((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))

        records = qset.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.doc_id,db.sm_doctor_visit.rep_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id)
        doc_id_list=[]
        visit_date_list=[]
        if records:
            for i in range(len(records)):
                recordListStr = records[i]
                doc_id = recordListStr[db.sm_doctor_visit.doc_id]

                visit_date = recordListStr[db.sm_doctor_visit.visit_date]
                doc_id_list.append(doc_id)
                visit_date_list.append(visit_date)
                

        qsetCount=db()
        qsetCount = qsetCount(db.sm_doctor_visit.cid == cid)
        qsetCount = qsetCount(db.sm_doctor_visit.rep_id == rep_id)
        qsetCount = qsetCount(db.sm_doctor_visit.giftnsample!='')
        qsetCount = qsetCount(db.sm_doctor_visit.route_id.belongs(rp_areaList))
        qsetCount = qsetCount((db.sm_doctor_visit.visit_date <= date_from) and (db.sm_doctor_visit.visit_date > date_to))
       
        if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
            qsetCount=qsetCount((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))

        recordsCount = qsetCount.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id)
        vChecklist=[]
        vCountList=[]
        for recordsCount in recordsCount:
            vCount=recordsCount[db.sm_doctor_visit.doc_id.count()]
            vCheck=str(recordsCount[db.sm_doctor_visit.rep_id])+'|'+str(recordsCount[db.sm_doctor_visit.visit_date])
            vChecklist.append(vCheck)
            vCountList.append(vCount)


    if (user_type=='SUP'):
        levelList=[]
        SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)

        
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
        marketStr=''
        marketStrList=[]
        for i in range(len(levelList)):
            
            levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
            for levelRow in levelRows:
                level_id = levelRow.level_id
                marketStrList.append(level_id)

                special_territory_code = levelRow.special_territory_code
                if level_id==special_territory_code:
                    cTeam=1

                if marketStr=='':
                    marketStr="'"+str(level_id)+"'"
                else:
                    marketStr=marketStr+",'"+str(level_id)+"'"      


        qset=db()
        qset = qset(db.sm_doctor_visit.cid == cid)
        qset = qset(db.sm_doctor_visit.route_id.belongs(marketStrList))
        qset = qset((db.sm_doctor_visit.visit_date <= date_from) and (db.sm_doctor_visit.visit_date > date_to))
       
        if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
            qset=qset((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))

        records = qset.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=~db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id)
        doc_id_list=[]
        visit_date_list=[]
        if records:
            for i in range(len(records)):
                recordListStr = records[i]
                doc_id = recordListStr[db.sm_doctor_visit.doc_id]

                visit_date = recordListStr[db.sm_doctor_visit.visit_date]
                doc_id_list.append(doc_id)
                visit_date_list.append(visit_date)
                

        qsetCount=db()
        qsetCount = qsetCount(db.sm_doctor_visit.cid == cid)
        qsetCount = qsetCount(db.sm_doctor_visit.giftnsample!='')
        qsetCount = qsetCount(db.sm_doctor_visit.route_id.belongs(marketStrList))
        qsetCount = qsetCount((db.sm_doctor_visit.visit_date <= date_from) and (db.sm_doctor_visit.visit_date > date_to))
       
        if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
            qsetCount=qsetCount((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))

        recordsCount = qsetCount.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=~db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id)
        vChecklist=[]
        vCountList=[]
        for recordsCount in recordsCount:
            vCount=recordsCount[db.sm_doctor_visit.doc_id.count()]
            vCheck=str(recordsCount[db.sm_doctor_visit.rep_id])+'|'+str(recordsCount[db.sm_doctor_visit.visit_date])
            vChecklist.append(vCheck)
            vCountList.append(vCount)

    return dict(doc_id_list=doc_id_list,records=records,date_to=date_to,cid=cid,rep_id=rep_id,password=password,synccode=synccode,vChecklist=vChecklist,vCountList=vCountList,search_form=search_form)



def slsRptDcr_area_wise():
    cid =session.cid
    rep_id =session.rep_id
    password =session.password
    synccode =session.synccode
    route_id =session.route_id
    visit_date=session.visit_date
    # return visit_date
    route_id=''
    # cid = str(request.vars.cid).strip().upper()
    # rep_id = str(request.vars.rep_id).strip().upper()
    # password = str(request.vars.password).strip()
    # synccode = str(request.vars.synccode).strip()
    # route_id = str(request.vars.route_id).strip()
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()    
    user_type = str(request.vars.user_type).strip().upper()
    date_to = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    # date_to=now + datetime.timedelta(days = 1)
    # # return now
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
    # return repRow
    # return db._lastsql
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = str(repRow[0].user_type).upper()
    
    if (user_type == 'SUP'):
        level_rep = repRow[0].level_id
        depth = repRow[0].field2
        level = 'level' + str(depth)
    
    
    report_string=""    
    report_str=""
    
    if (user_type=='REP'):
        
        condition=""      
        condition="and s1.route_id='"+ str(route_id) +"' "        
        
        records_ov=[]
        sql_str="SELECT  COUNT(s1.doc_id)as doc_count,s1.doc_id as doc_id, s1.doc_name as doc_name,s1.id as id,s1.visit_dtime as visit_dtime,s1.giftnsample as giftnsample  FROM sm_doctor_visit as s1  WHERE s1.cid = '"+ str(cid) +"' AND s1.rep_id = '"+ str(rep_id) +"' AND s1.visit_date = '"+ str(visit_date) +"' "+ condition + " GROUP BY s1.route_id,s1.id;"
        records_ov=db.executesql(sql_str,as_dict = True)

    if (user_type=='SUP'):
        levelList=[]
        marketStr=''
        SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)
        for SuplevelRows in SuplevelRows:
            Suplevel_id = SuplevelRows.level_id
            depth = SuplevelRows.level_depth_no
            level = 'level' + str(depth)
            if Suplevel_id not in levelList:
                levelList.append(Suplevel_id)
        
        # cTeam=0
        # for i in range(len(levelList)):
        #     levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
        #     for levelRow in levelRows:
        #         level_id = levelRow.level_id
        #         special_territory_code = levelRow.special_territory_code
        #         if level_id==special_territory_code:
        #             cTeam=1

        #         if marketStr=='':
        #             marketStr="'"+str(level_id)+"'"
        #         else:
        #             marketStr=marketStr+",'"+str(level_id)+"'" 
            
        #     if cTeam==1:    
        #         if special_territory_code not in spicial_codeList:
        #             if (special_territory_code !='' and level_id==special_territory_code):
        #                 spicial_codeList.append(special_territory_code)    
            
        #             levelSpecialRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level.special_territory_code.belongs(spicial_codeList)) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id)        

        #             for levelSpecialRow in levelSpecialRows:
        #                 level_id = levelSpecialRow.level_id
        #                 if marketStr=='':
        #                     marketStr="'"+str(Suplevel_id)+"'"
        #                 else:
        #                     marketStr=marketStr+",'"+str(level_id)+"'"          
        
        condition=''
        if int(depth)==0:
            condition=condition+"AND level0_id IN ("+str(route_id)+") "
        if int(depth)==1:
            condition=condition+"AND level1_id IN ("+str(route_id)+") "
        if int(depth)==2:
            condition=condition+"AND level2_id IN ("+str(route_id)+") "

        # condition=condition+"AND route_id IN ("+str(route_id)+") "
        # return db._lastsql 
        records_ov=[]
        sql_str="SELECT  COUNT(dv.doc_id)as doc_count,dv.doc_id as doc_id, dv.doc_name as doc_name,dv.id as id,dv.visit_dtime as visit_dtime,dv.giftnsample as giftnsample,dv.route_id as route_id,route_name FROM sm_doctor_visit as dv  WHERE dv.cid = '"+ str(cid) +"'  AND dv.visit_date = '"+ str(visit_date) +"'  AND dv.level3_id = '"+ str(route_id) +"' GROUP BY dv.id"
        
        # qset = qset((db.sm_doctor_visit.visit_date <= date_from) and (db.sm_doctor_visit.visit_date > date_to))

        # return sql_str
        records_ov=db.executesql(sql_str,as_dict = True)

    return dict(date_to=date_to,cid=cid,rep_id=rep_id,password=password,synccode=synccode,records_ov=records_ov,route_id=route_id,visit_date=visit_date)



def sales_rptDcr_slWise():

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.password).strip()
    synccode = str(request.vars.synccode).strip()
    route_id = str(request.vars.route_id).strip()

    visit_date=str(request.vars.visit_date).strip()
    doc_id = str(request.vars.doc_id).strip().upper()

    rowid = str(request.vars.rowid).strip()

    now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    date_ton=now + datetime.timedelta(days = 1)
    date_to=str(date_ton).split(' ')[0]
    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = str(repRow[0].user_type).upper()

    
    if (user_type == 'SUP'):
        level_rep = repRow[0].level_id
        depth = repRow[0].field2
        level = 'level' + str(depth)
    
    report_string=""
    
    report_str=""
    
    if (user_type=='REP'):

        condition=""      
        condition="and s1.route_id='"+ str(route_id) +"' "

        records_ov=[]
        sql_str="SELECT  s1.id as rowid,s1.giftnsample as giftnsample  FROM sm_doctor_visit as s1  WHERE s1.cid = '"+ str(cid) +"' AND s1.rep_id = '"+ str(rep_id) +"' AND  s1.giftnsample !='' AND s1.visit_date = '"+ str(visit_date) +"' AND s1.id= '"+ str(rowid) +"' "+ condition + " GROUP BY s1.route_id,s1.id;"

        records_ov=db.executesql(sql_str,as_dict = True)

         

        records_ov=db.executesql(sql_str,as_dict = True)
    if (user_type=='SUP'):
        
        condition=''
        condition=condition+"AND route_id IN ("+str(route_id)+") "  

        records_ov=[]
        sql_str="SELECT  s1.id as rowid,s1.giftnsample as giftnsample  FROM sm_doctor_visit as s1  WHERE s1.cid = '"+ str(cid) +"' AND  s1.giftnsample !='' AND s1.visit_date = '"+ str(visit_date) +"' AND s1.id= '"+ str(rowid) +"' GROUP BY s1.route_id,s1.id;"

        records_ov=db.executesql(sql_str,as_dict = True)

    return dict(records_ov=records_ov,rowid=rowid,visit_date=visit_date,route_id=route_id,doc_id=doc_id)


def sales_rptDcr_zm():
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.password).strip()
    synccode = str(request.vars.synccode).strip()
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()

    date_from=current_date
    now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    date_ton=now - datetime.timedelta(days = 7)
    date_to=str(date_ton).split(' ')[0]
    # return date_to

    from_dt=''
    to_date=''

    btn_filter=request.vars.btn_filter
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    if btn_filter:

        from_dt = str(request.vars.from_dt).strip().upper()
        to_date= str(request.vars.to_dt).strip().upper()

        session.btn_filter=btn_filter
        reqPage=0
    elif btn_all:
        session.btn_filter=None
        reqPage=0
        
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    search_form =SQLFORM(db.sm_search_date)
    
    user_type = str(request.vars.user_type).strip().upper()

    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.sync_code == synccode) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = str(repRow[0].user_type).upper()

       # pass
    
    if (user_type == 'SUP'):
        level_rep = repRow[0].level_id
        depth = repRow[0].field2
        level = 'level' + str(depth)

    report_string=""
    
    report_str=""

    dateFlag=''
    reqPage=len(request.args)
    dateFlag=True
    try:
        from_dt=datetime.datetime.strptime(str(from_dt),'%Y-%m-%d')
        to_dt=datetime.datetime.strptime(str(to_date),'%Y-%m-%d')
    except:
        dateFlag=False
    
    if (user_type=='REP'):
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
    

        qset=db()
        qset = qset(db.sm_doctor_visit.cid == cid)
        qset = qset(db.sm_doctor_visit.rep_id == rep_id)
        qset = qset(db.sm_doctor_visit.route_id.belongs(rp_areaList))
        qset = qset((db.sm_doctor_visit.visit_date <= date_from) and (db.sm_doctor_visit.visit_date > date_to))
       
        if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
            qset=qset((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))

        records = qset.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.doc_id,db.sm_doctor_visit.rep_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id)
        doc_id_list=[]
        visit_date_list=[]
        if records:
            for i in range(len(records)):
                recordListStr = records[i]
                doc_id = recordListStr[db.sm_doctor_visit.doc_id]

                visit_date = recordListStr[db.sm_doctor_visit.visit_date]
                doc_id_list.append(doc_id)
                visit_date_list.append(visit_date)
                

        qsetCount=db()
        qsetCount = qsetCount(db.sm_doctor_visit.cid == cid)
        qsetCount = qsetCount(db.sm_doctor_visit.rep_id == rep_id)
        qsetCount = qsetCount(db.sm_doctor_visit.giftnsample!='')
        qsetCount = qsetCount(db.sm_doctor_visit.route_id.belongs(rp_areaList))
        qsetCount = qsetCount((db.sm_doctor_visit.visit_date <= date_from) and (db.sm_doctor_visit.visit_date > date_to))
       
        if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
            qsetCount=qsetCount((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))

        recordsCount = qsetCount.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id)
        vChecklist=[]
        vCountList=[]
        for recordsCount in recordsCount:
            vCount=recordsCount[db.sm_doctor_visit.doc_id.count()]
            vCheck=str(recordsCount[db.sm_doctor_visit.rep_id])+'|'+str(recordsCount[db.sm_doctor_visit.visit_date])
            vChecklist.append(vCheck)
            vCountList.append(vCount)


    if (user_type=='SUP'):
        levelList=[]
        SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)
        
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
        marketStr=''
        marketStrList=[]
        for i in range(len(levelList)):
            
            levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code)
            for levelRow in levelRows:
                level_id = levelRow.level_id
                marketStrList.append(level_id)

                special_territory_code = levelRow.special_territory_code
                if level_id==special_territory_code:
                    cTeam=1

                if marketStr=='':
                    marketStr="'"+str(level_id)+"'"
                else:
                    marketStr=marketStr+",'"+str(level_id)+"'"      

        qset=db()
        qset = qset(db.sm_doctor_visit.cid == cid)
        qset = qset(db.sm_doctor_visit.route_id.belongs(marketStrList))
        qset = qset((db.sm_doctor_visit.visit_date <= date_from) and (db.sm_doctor_visit.visit_date > date_to))
       
        if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
            qset=qset((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))

        records = qset.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=~db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id)
        doc_id_list=[]
        visit_date_list=[]
        if records:
            for i in range(len(records)):
                recordListStr = records[i]
                doc_id = recordListStr[db.sm_doctor_visit.doc_id]

                visit_date = recordListStr[db.sm_doctor_visit.visit_date]
                doc_id_list.append(doc_id)
                visit_date_list.append(visit_date)
                

        qsetCount=db()
        qsetCount = qsetCount(db.sm_doctor_visit.cid == cid)
        qsetCount = qsetCount(db.sm_doctor_visit.giftnsample!='')
        qsetCount = qsetCount(db.sm_doctor_visit.route_id.belongs(marketStrList))
        qsetCount = qsetCount((db.sm_doctor_visit.visit_date <= date_from) and (db.sm_doctor_visit.visit_date > date_to))
       
        if (from_dt and to_date)!='' and (from_dt and to_date)!=None:                    
            qsetCount=qsetCount((db.sm_doctor_visit.visit_date >= from_dt) & (db.sm_doctor_visit.visit_date < to_date))

        recordsCount = qsetCount.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=~db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id)
        vChecklist=[]
        vCountList=[]
        for recordsCount in recordsCount:
            vCount=recordsCount[db.sm_doctor_visit.doc_id.count()]
            vCheck=str(recordsCount[db.sm_doctor_visit.rep_id])+'|'+str(recordsCount[db.sm_doctor_visit.visit_date])
            vChecklist.append(vCheck)
            vCountList.append(vCount)



    return dict(doc_id_list=doc_id_list,records=records,date_to=date_to,cid=cid,rep_id=rep_id,password=password,synccode=synccode,vChecklist=vChecklist,vCountList=vCountList,search_form=search_form)







# =========== 20210606 End ==========
# =========== 20210606 End ==========




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

