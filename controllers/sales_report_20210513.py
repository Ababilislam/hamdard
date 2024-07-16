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


def sales_report_detail():

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.password).strip()
    synccode = str(request.vars.synccode).strip()
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()
    se_item_report = str(request.vars.se_item_report).strip().upper()
    se_market_report = str(request.vars.se_market_report).strip().upper()


    date_from=current_date
    now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    date_ton=now - datetime.timedelta(days = 7)
    date_to=str(date_ton).split(' ')[0]

    from_dt = str(request.vars.from_dt).strip().upper()
    to_date= str(request.vars.to_dt).strip().upper()


    btn_filter=request.vars.btn_filter
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    if btn_filter:
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

        dateFlag=''
        reqPage=len(request.args)
        dateFlag=True
        try:
            from_dt=datetime.datetime.strptime(str(from_dt),'%Y-%m-%d')
            to_dt=datetime.datetime.strptime(str(to_date),'%Y-%m-%d')
        except:
            dateFlag=False

        condition=""
        condition="and sm_order.area_id IN ("+str(repAreaStr)+")" 


        records_ov=[]
        if session.btn_filter:
            if (from_dt!='' and to_date!=''):

                sql_str="SELECT SUM((sm_order.price) * (sm_order.quantity)) as totalprice, sm_order.area_id as area_id, sm_order.area_name as area_name,sm_order.delivery_date as delivery_date,(SELECT count(sm_order_head.sl) FROM sm_order_head WHERE sm_order_head.cid = '"+ str(cid)+"' AND sm_order_head.rep_id = '"+ str(rep_id) +"' AND sm_order_head.delivery_date = sm_order.delivery_date) as visit_count,(SELECT count(sm_order_head.sl) FROM sm_order_head WHERE sm_order_head.cid = '"+ str(cid)+"' AND sm_order_head.rep_id = '"+ str(rep_id) +"' AND sm_order_head.field1='ORDER' AND sm_order_head.delivery_date = sm_order.delivery_date) as order_count FROM sm_order  WHERE sm_order.cid = '"+ str(cid) +"' AND sm_order.rep_id = '"+ str(rep_id) +"' AND sm_order.delivery_date > '"+ str(from_dt).split(' ')[0] +"' AND sm_order.delivery_date <= '"+ str(to_date) +"' "+ condition + " GROUP BY area_id,delivery_date;"

                records_ov=db.executesql(sql_str,as_dict = True)
            else:
                pass
        else:
            sql_str="SELECT SUM((sm_order.price) * (sm_order.quantity)) as totalprice, sm_order.area_id as area_id, sm_order.area_name as area_name,sm_order.delivery_date as delivery_date,(SELECT count(sm_order_head.sl) FROM sm_order_head WHERE sm_order_head.cid = '"+ str(cid)+"' AND sm_order_head.rep_id = '"+ str(rep_id) +"' AND sm_order_head.delivery_date = sm_order.delivery_date) as visit_count,(SELECT count(sm_order_head.sl) FROM sm_order_head WHERE sm_order_head.cid = '"+ str(cid)+"' AND sm_order_head.rep_id = '"+ str(rep_id) +"' AND sm_order_head.field1='ORDER' AND sm_order_head.delivery_date = sm_order.delivery_date) as order_count FROM sm_order WHERE sm_order.cid = '"+ str(cid) +"' AND sm_order.rep_id = '"+ str(rep_id) +"' AND sm_order.delivery_date <= '"+ str(date_from) +"' AND sm_order.delivery_date > '"+ str(date_to) +"' "+ condition + " GROUP BY area_id,delivery_date;"
        
            records_ov=db.executesql(sql_str,as_dict = True)

    if (user_type=='SUP'):
        dateFlag=''
        reqPage=len(request.args)
        dateFlag=True
        try:
            from_dt=datetime.datetime.strptime(str(from_dt),'%Y-%m-%d')
            to_dt=datetime.datetime.strptime(str(to_date),'%Y-%m-%d')
        except:
            dateFlag=False

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
                           
        condition=''
        if (se_market_report!="ALL"):
            condition=condition+"AND route_id = '"+str(se_market_report)+"'"
        # if (rep_id!=rep_id_report):
        # condition=condition+"AND rep_id = '"+str(rep_id)+"'"
        condition=condition+" AND area_id IN ("+str(marketStr)+")" 
      
       

        records_ov=[]
        if session.btn_filter:
            if (from_dt!='' and to_date!=''):

                sql_str="SELECT SUM((sm_order.price) * (sm_order.quantity)) as totalprice, sm_order.area_id as area_id, sm_order.area_name as area_name,sm_order.delivery_date as delivery_date,(SELECT count(sm_order_head.sl) FROM sm_order_head WHERE sm_order_head.cid = '"+ str(cid)+"'  AND sm_order_head.delivery_date = sm_order.delivery_date) as visit_count,(SELECT count(sm_order_head.sl) FROM sm_order_head WHERE sm_order_head.cid = '"+ str(cid)+"' AND sm_order_head.field1='ORDER' AND sm_order_head.delivery_date = sm_order.delivery_date) as order_count FROM sm_order  WHERE sm_order.cid = '"+ str(cid) +"' AND sm_order.delivery_date > '"+ str(from_dt).split(' ')[0] +"' AND sm_order.delivery_date <= '"+ str(to_date) +"' "+ condition + " GROUP BY area_id,delivery_date;"

                records_ov=db.executesql(sql_str,as_dict = True)
            else:
                pass
        else:
            sql_str="SELECT SUM((sm_order.price) * (sm_order.quantity)) as totalprice, sm_order.area_id as area_id, sm_order.area_name as area_name,sm_order.delivery_date as delivery_date,(SELECT count(sm_order_head.sl) FROM sm_order_head WHERE sm_order_head.cid = '"+ str(cid)+"'  AND sm_order_head.delivery_date = sm_order.delivery_date) as visit_count,(SELECT count(sm_order_head.sl) FROM sm_order_head WHERE sm_order_head.cid = '"+ str(cid)+"'  AND sm_order_head.field1='ORDER' AND sm_order_head.delivery_date = sm_order.delivery_date) as order_count FROM sm_order WHERE sm_order.cid = '"+ str(cid) +"'  AND sm_order.delivery_date <= '"+ str(date_from) +"' AND sm_order.delivery_date > '"+ str(date_to) +"' "+ condition + " GROUP BY area_id,delivery_date;"
            # return sql_str
            records_ov=db.executesql(sql_str,as_dict = True)
    

    return dict(date_to=date_to,cid=cid,rep_id=rep_id,password=password,synccode=synccode,se_market_report=se_market_report,records_ov=records_ov,search_form=search_form)


def sales_report_area_wise():

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.password).strip()
    synccode = str(request.vars.synccode).strip()
    area_id = str(request.vars.area_id).strip()
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()
    se_item_report = str(request.vars.se_item_report).strip().upper()
    se_market_report = str(request.vars.se_market_report).strip().upper()
    
    dlvry_date=str(request.vars.dlvry_date).strip()
    
    user_type = str(request.vars.user_type).strip().upper()
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
        qset=db()
        qset=qset((db.sm_order_head.cid == cid) & (db.sm_order_head.rep_id == rep_id))
        qset=qset(db.sm_order_head.delivery_date == dlvry_date)
        qset=qset(db.sm_order_head.area_id==area_id)
        records=qset.select(db.sm_order_head.sl.count())
        if records:
            sales_call=records[0][db.sm_order_head.sl.count()]
        
        report_string=str(sales_call)
        #  Order Count  
        qset_oc=db()
        qset_oc=qset_oc((db.sm_order_head.cid == cid) & (db.sm_order_head.rep_id == rep_id) & (db.sm_order_head.field1 == 'ORDER')) 
        qset_oc=qset_oc(db.sm_order_head.delivery_date == dlvry_date)
        qset_oc=qset_oc(db.sm_order_head.area_id==area_id)
        records_oc=qset_oc.select(db.sm_order_head.sl.count())
        # return db._lastsql
        if records_oc:
            order_count=records_oc[0][db.sm_order_head.sl.count()]
        
        
        condition=""      
        condition="and sm_order.area_id  IN ("+str(repAreaStr)+")"  
      
        records_ov=[]
        sql_str="SELECT (sm_order.client_id) as client_id,(sm_order.client_name) as client_name,SUM((sm_order.price) * (sm_order.quantity)) as totalprice, sm_order.area_id as area_id, sm_order.vsl as vsl FROM sm_order WHERE sm_order.cid = '"+ str(cid) +"' AND sm_order.rep_id = '"+ str(rep_id) +"' AND sm_order.delivery_date = '"+ str(dlvry_date) +"'  GROUP BY area_id,delivery_date,vsl;"

        records_ov=db.executesql(sql_str,as_dict = True)

    if (user_type=='SUP'):
        dateFlag=''
        reqPage=len(request.args)
        dateFlag=True
        try:
            from_dt=datetime.datetime.strptime(str(from_dt),'%Y-%m-%d')
            to_dt=datetime.datetime.strptime(str(to_date),'%Y-%m-%d')
        except:
            dateFlag=False

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
        qset=qset(db.sm_order_head.delivery_date == dlvry_date)
        qset=qset(db.sm_order_head.area_id==area_id)
        records=qset.select(db.sm_order_head.sl.count())
        if records:
            sales_call=records[0][db.sm_order_head.sl.count()]
        
        report_string=str(sales_call)
        #  Order Count  
        qset_oc=db()
        qset_oc=qset_oc((db.sm_order_head.cid == cid)  & (db.sm_order_head.field1 == 'ORDER')) 
        qset_oc=qset_oc(db.sm_order_head.delivery_date == dlvry_date)
        qset_oc=qset_oc(db.sm_order_head.area_id==area_id)
        records_oc=qset_oc.select(db.sm_order_head.sl.count())
        # return db._lastsql
        if records_oc:
            order_count=records_oc[0][db.sm_order_head.sl.count()]

        condition=''
        condition=condition+" AND area_id IN ("+str(marketStr)+")"  

        records_ov=[]
        sql_str="SELECT (sm_order.client_id) as client_id,(sm_order.client_name) as client_name,SUM((sm_order.price) * (sm_order.quantity)) as totalprice, sm_order.area_id as area_id, sm_order.vsl as vsl FROM sm_order WHERE sm_order.cid = '"+ str(cid) +"' AND sm_order.delivery_date = '"+ str(dlvry_date) +"'  GROUP BY area_id,delivery_date,vsl;"

        records_ov=db.executesql(sql_str,as_dict = True)               



    return dict(date_to=date_to,cid=cid,rep_id=rep_id,password=password,synccode=synccode,records_ov=records_ov,area_id=area_id,dlvry_date=dlvry_date)



def sales_report_slWise():

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.password).strip()
    synccode = str(request.vars.synccode).strip()
    area_id = str(request.vars.area_id).strip()
    vsl = str(request.vars.vsl).strip()
    client_id = str(request.vars.client_id).strip().upper()

    dlvry_date=str(request.vars.dlvry_date).strip()
    
    user_type = str(request.vars.user_type).strip().upper()
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
        sql_str="SELECT client_name,rep_id,rep_name,SUM(sm_order.quantity) as item_qty, sm_order.item_id as item_id,sm_order.item_name as item_name, sm_order.quantity as qty,((sm_order.price) * (sm_order.quantity)) as amnt, sm_order.vsl as vsl,sm_order.delivery_date as delivery_date,(SELECT SUM((sm_order.price) * (sm_order.quantity))  FROM sm_order  WHERE sm_order.cid = '"+ str(cid) +"' AND sm_order.rep_id = '"+ str(rep_id) +"' AND sm_order.delivery_date = '"+ str(dlvry_date) +"' AND sm_order.vsl= '"+ str(vsl) +"' AND sm_order.area_id='"+str(area_id)+"' AND sm_order.client_id='"+str(client_id)+"'  GROUP BY sm_order.area_id) as totalprice FROM sm_order WHERE sm_order.cid = '"+ str(cid) +"' AND sm_order.rep_id = '"+ str(rep_id) +"' AND sm_order.delivery_date = '"+ str(dlvry_date) +"' AND sm_order.vsl= '"+ str(vsl) +"' AND sm_order.area_id='"+str(area_id)+"' AND sm_order.client_id='"+str(client_id)+"'  GROUP BY sm_order.area_id,item_id;"

        records_ov=db.executesql(sql_str,as_dict = True)
    if (user_type=='SUP'):

        records_ov=[]
        sql_str="SELECT client_name,rep_id,rep_name,SUM(sm_order.quantity) as item_qty, sm_order.item_id as item_id,sm_order.item_name as item_name, sm_order.quantity as qty,((sm_order.price) * (sm_order.quantity)) as amnt, sm_order.vsl as vsl,sm_order.delivery_date as delivery_date,(SELECT SUM((sm_order.price) * (sm_order.quantity))  FROM sm_order  WHERE sm_order.cid = '"+ str(cid) +"'  AND sm_order.delivery_date = '"+ str(dlvry_date) +"' AND sm_order.vsl= '"+ str(vsl) +"' AND sm_order.area_id='"+str(area_id)+"' AND sm_order.client_id='"+str(client_id)+"'  GROUP BY sm_order.area_id) as totalprice FROM sm_order WHERE sm_order.cid = '"+ str(cid) +"' AND sm_order.delivery_date = '"+ str(dlvry_date) +"' AND sm_order.vsl= '"+ str(vsl) +"' AND sm_order.area_id='"+str(area_id)+"' AND sm_order.client_id='"+str(client_id)+"'  GROUP BY sm_order.area_id,item_id;"
        # return sql_str
        records_ov=db.executesql(sql_str,as_dict = True)
    # client_name=''
    for i in range(len(records_ov)):
      records_ov_dict=records_ov[i]  
      client_name=str(records_ov_dict["client_name"]) 
      rep_id=str(records_ov_dict["rep_id"]) 
      rep_name=str(records_ov_dict["rep_name"]) 


    return dict(records_ov=records_ov,vsl=vsl,dlvry_date=dlvry_date,area_id=area_id,client_id=client_id,rep_id=rep_id)

# ============================ DOCTOR =======================


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

        records = qset.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.doc_id,db.sm_doctor_visit.rep_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id|db.sm_doctor_visit.visit_date)
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

        recordsCount = qsetCount.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id|db.sm_doctor_visit.visit_date)
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

        records = qset.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=~db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id|db.sm_doctor_visit.visit_date)
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

        recordsCount = qsetCount.select(db.sm_doctor_visit.doc_id.count(),db.sm_doctor_visit.rep_id,db.sm_doctor_visit.doc_id,db.sm_doctor_visit.route_id,db.sm_doctor_visit.route_name,db.sm_doctor_visit.visit_date, orderby=~db.sm_doctor_visit.visit_date, groupby=db.sm_doctor_visit.route_id|db.sm_doctor_visit.visit_date)
        vChecklist=[]
        vCountList=[]
        for recordsCount in recordsCount:
            vCount=recordsCount[db.sm_doctor_visit.doc_id.count()]
            vCheck=str(recordsCount[db.sm_doctor_visit.rep_id])+'|'+str(recordsCount[db.sm_doctor_visit.visit_date])
            vChecklist.append(vCheck)
            vCountList.append(vCount)



    return dict(doc_id_list=doc_id_list,records=records,date_to=date_to,cid=cid,rep_id=rep_id,password=password,synccode=synccode,vChecklist=vChecklist,vCountList=vCountList,search_form=search_form)



def slsRptDcr_area_wise():

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.password).strip()
    synccode = str(request.vars.synccode).strip()
    route_id = str(request.vars.route_id).strip()
    
    rep_id_report = str(request.vars.rep_id_report).strip().upper()

    
    visit_date=str(request.vars.visit_date).strip()
    
    user_type = str(request.vars.user_type).strip().upper()
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

        
        condition=""      
        condition="and s1.route_id='"+ str(route_id) +"' "

        

        records_ov=[]
        sql_str="SELECT  COUNT(s1.doc_id)as doc_count,s1.doc_id as doc_id, s1.doc_name as doc_name,s1.id as id,s1.visit_dtime as visit_dtime,s1.giftnsample as giftnsample  FROM sm_doctor_visit as s1  WHERE s1.cid = '"+ str(cid) +"' AND s1.rep_id = '"+ str(rep_id) +"' AND s1.visit_date = '"+ str(visit_date) +"' "+ condition + " GROUP BY s1.route_id,s1.visit_date,s1.id;"
        records_ov=db.executesql(sql_str,as_dict = True)


    if (user_type=='SUP'):
        levelList=[]
        SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)

        

        condition=''
        condition=condition+"AND route_id IN ("+str(route_id)+") "
       
        records_ov=[]
        sql_str="SELECT  COUNT(s1.doc_id)as doc_count,s1.doc_id as doc_id, s1.doc_name as doc_name,s1.id as id,s1.visit_dtime as visit_dtime,s1.giftnsample as giftnsample  FROM sm_doctor_visit as s1  WHERE s1.cid = '"+ str(cid) +"'  AND s1.visit_date = '"+ str(visit_date) +"' AND s1.route_id = '"+ str(route_id) +"' GROUP BY s1.id"
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
        sql_str="SELECT  s1.id as rowid,s1.giftnsample as giftnsample  FROM sm_doctor_visit as s1  WHERE s1.cid = '"+ str(cid) +"' AND s1.rep_id = '"+ str(rep_id) +"' AND  s1.giftnsample !='' AND s1.visit_date = '"+ str(visit_date) +"' AND s1.id= '"+ str(rowid) +"' "+ condition + " GROUP BY s1.route_id,s1.visit_date,s1.id;"

        records_ov=db.executesql(sql_str,as_dict = True)

         

        records_ov=db.executesql(sql_str,as_dict = True)
    if (user_type=='SUP'):
        
        condition=''
        condition=condition+"AND route_id IN ("+str(route_id)+") "  

        records_ov=[]
        sql_str="SELECT  s1.id as rowid,s1.giftnsample as giftnsample  FROM sm_doctor_visit as s1  WHERE s1.cid = '"+ str(cid) +"' AND  s1.giftnsample !='' AND s1.visit_date = '"+ str(visit_date) +"' AND s1.id= '"+ str(rowid) +"' GROUP BY s1.route_id,s1.visit_date,s1.id;"

        records_ov=db.executesql(sql_str,as_dict = True)




    return dict(records_ov=records_ov,rowid=rowid,visit_date=visit_date,route_id=route_id,doc_id=doc_id)

# =========== 20210606 End ==========