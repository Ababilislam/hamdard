from random import randint
import urllib.parse
import calendar
import urllib
import time
import datetime

# http://127.0.0.1:8000/hamdard/product_wise_order_invoice/product_wise_order_invoice_url?cid=HAMDARD&rep_id=9010&rep_pass=1234

# http://127.0.0.1:8000/hamdard/product_wise_order_invoice/product_wise_order_invoice_url?cid=HAMDARD&rep_id=itzm&rep_pass=1234
# http://127.0.0.1:8000/hamdard/product_wise_order_invoice/product_wise_order_invoice_url?cid=HAMDARD&rep_id=9001&rep_pass=1234
# http://127.0.0.1:8000/hamdard/product_wise_order_invoice/product_wise_order_invoice_url?cid=HAMDARD&rep_id=9011&rep_pass=1234


#=================================================================
# ========================= INDEX FUNCTION START ==================================

def product_wise_order_invoice_url():
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

    session.from_date = from_date
    session.to_date = to_date
    
    division_count = []
    zone_count = []
    area_count = []
    territory_count = []

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

        level_area_list = []
        zlevel_list=[]
        division_list = []
        zone_list = []
        area_list = []
        market_list = []
        territory_list_count = []
        if user_type=='rep':
            repAreaRows = db((db.sm_rep_area.cid == c_id) & (db.sm_rep_area.rep_id == rep_id)).select(db.sm_rep_area.area_id,db.sm_rep_area.area_name,orderby=db.sm_rep_area.area_id)
            # return db._lastsql
            if not repAreaRows:
                response.flash = 'Rep Territory Not Available'
            else:
                for rRow in repAreaRows:
                    area_id=rRow.area_id
                    area_name = rRow.area_name
                    dictData = {'area_id': area_id, 'area_name': area_name}
                    level_area_list.append(dictData)
                    territory_count.append(area_id)
            session.division_count = 1
            session.zone_count = 1
            session.area_count = 1
            active_markets_list = activeMaeketList()
            active_markets =   list(set(active_markets_list).intersection(territory_count))
            session.territory_count = len(active_markets)
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

        if user_type=='sup':
            zLevelRows=db((db.sm_supervisor_level.cid==c_id) & (db.sm_supervisor_level.sup_id==rep_id)).select(db.sm_supervisor_level.level_depth_no,db.sm_supervisor_level.level_id)
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
                    level3_Rows = db((db.sm_level.cid == c_id) & (db.sm_level.level0.belongs(z_level_list)) & (db.sm_level.is_leaf == '1') ).select(db.sm_level.level0,db.sm_level.level0_name, orderby=db.sm_level.level0,groupby=db.sm_level.level0)
                    for d_Row1 in level3_Rows:
                        division_id = d_Row1.level0
                        division_name = d_Row1.level0_name
                        dictData2 = {'division_id': division_id, 'division_name': division_name}
                        division_list.append(dictData2)

                if level_depth_no == 1:
                    level3_Rows = db((db.sm_level.cid == c_id) & (db.sm_level.level1.belongs(z_level_list)) & (db.sm_level.depth == 1)).select(db.sm_level.level1, db.sm_level.level1_name,orderby=db.sm_level.level1,groupby=db.sm_level.level1)
                    for d_Row1 in level3_Rows:
                        zone_id = d_Row1.level1
                        zone_name = d_Row1.level1_name
                        dictData2 = {'zone_id': zone_id, 'zone_name': zone_name}
                        zone_list.append(dictData2)
                
                if level_depth_no==2:
                    level3_Rows = db((db.sm_level.cid == c_id) & (db.sm_level.level2.belongs(z_level_list)) & (db.sm_level.depth == 2) ).select(db.sm_level.level2,db.sm_level.level2_name, orderby=db.sm_level.level2,groupby=db.sm_level.level2)
                    for d_Row1 in level3_Rows:
                        area_id = d_Row1.level2
                        area_name = d_Row1.level2_name
                        dictData2 = {'area_id': area_id, 'area_name': area_name}
                        area_list.append(dictData2)

            session.zlevel_list=zlevel_list
            session.division_list=division_list
            session.zone_list=zone_list
            session.area_list=area_list

        # ============ SUPERVISOR ===========
        if user_type=='sup':
            sLevelRows=db((db.sm_supervisor_level.cid==c_id) & (db.sm_supervisor_level.sup_id==rep_id)).select(db.sm_supervisor_level.level_depth_no,db.sm_supervisor_level.level_id)
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

                if level_depth_no == 1:
                    level3_Rows = db((db.sm_level.cid == c_id) & (db.sm_level.level1.belongs(s_level_list))).select(db.sm_level.level0,db.sm_level.level0_name,db.sm_level.level1,db.sm_level.level2,db.sm_level.level3, orderby=db.sm_level.level_id,groupby=db.sm_level.level_id|db.sm_level.level0|db.sm_level.level1|db.sm_level.level2|db.sm_level.level3)   
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

            session.level_list=level_list
            session.division_count = len(set(division_count)) 
            session.zone_count = len(set(zone_count))
            session.area_count = len(set(area_count))
            active_markets_list = activeMaeketList()
            active_markets =   list(set(active_markets_list).intersection(territory_count))
            session.territory_count = len(active_markets)

        level_area_id_list = []
        for i in range(len(level_area_list)):
            level_area_str = level_area_list[i]
            level_area_id_list.append(level_area_str['area_id'])
        session.level_area_id_list = level_area_id_list
        
    redirect(URL(c='product_wise_order_invoice', f='home'))

# ========================= INDEX FUNCTION END ==================================


# ========================= HOME FUNCTION START=================================
  
def home():
    if session.cid=='' or session.cid==None:
        redirect(URL(c='report_seen_rx_mobile',f='index'))
    c_id = session.cid
    division_list = session.division_list
    zone_list = session.zone_list
    area_list = session.area_list
    zlevel_list = session.zlevel_list
    level_area_list = session.level_area_list
    seen_rx_type_list = session.seen_rx_type_list
    level_list = session.level_list
    user_type = session.user_type
    search_item_id_name=session.search_item_id_name
    from_date = str(request.vars.from_date)
    to_date = str(request.vars.to_date)
    rec_item = db(db.seen_rx_brand.cid == session.cid).select(db.seen_rx_brand.brand_name, orderby=db.seen_rx_brand.brand_name,groupby=db.seen_rx_brand.brand_name)
    btn_report=request.vars.btn_report
    btn_reset = request.vars.btn_reset

    basket_type_record_sql = "SELECT cat_type_id from sm_category_type where cid = '"+str(c_id)+"' and type_name = 'ITEM_CATEGORY' group by cat_type_id ;"
    basket_type_record = db.executesql(basket_type_record_sql, as_dict = True)

    product_record_sql = "SELECT item_id, name from sm_item where cid = '"+str(c_id)+"' and status ='ACTIVE' group by item_id order by name asc;"
    # return product_record_sql
    product_record = db.executesql(product_record_sql, as_dict = True)
    
    doctor_type_record =''
    item_condition = ''
    invoice_condition = ''
    record_show = False
    get_order_invocie_records = {}
    client_list = []
    product_cover = 0
    if btn_report=='Show' :
        session.from_date = from_date
        session.to_date = to_date
        division_id_name = str(request.vars.pr_region4).strip().replace('None','')
        zone_id_name = str(request.vars.pr_zone4).strip().replace('None','')
        area_id_name = str(request.vars.pr_area4).strip().replace('None','')
        territory_id_name = str(request.vars.pr_territory4).strip().replace('None','')
        pocket_market_id_name = str(request.vars.pr_pocket_market4).strip().replace('None','')
        product_category = str(request.vars.item_category).strip().replace('None','')
        item_id_name = str(request.vars.item_id).strip().replace('None','')
        # return item_id_name
        
        # item_ID= str(request.vars.item_id).strip().split('|')[0].replace('None','').replace("[","").replace(" ","").replace("]","").replace("'","")
        # item_id_name = str(request.vars.item_id).strip().split('|')[0]
        item_ID= str(request.vars.item_id).strip().replace("[","").replace("'","").replace("]","")
        item_id_name =str(item_ID).strip().split(',')
        only_item_id = []
        for i in item_id_name:
            item_id =str(i).strip().split('|')[0]
            only_item_id.append(item_id)

        session.division = division_id_name
        session.zone = zone_id_name
        session.area = area_id_name
        session.territory = territory_id_name
        session.pocket_market = pocket_market_id_name
        session.product_category = product_category
        session.item_id = item_id_name
        # return item_id
        try:
            division = str(request.vars.pr_region4).split('|')[0].replace('None','')
            zone = str(request.vars.pr_zone4).split('|')[0].replace('None','')
            area = str(request.vars.pr_area4).split('|')[0].replace('None','')
            territory = str(request.vars.pr_territory4).split('|')[0].replace('None','')
            pocket_market = str(request.vars.pr_pocket_market4).split('|')[0].replace('None','')
            item_id = tuple(only_item_id)
            # return item_id
            # item_id = str(request.vars.item_id).replace("[", "").replace("]", "").replace('"', "").split('|')
            # return item_id
        except:
            division = ''
            zone = ''
            area = ''
            territory = ''
            pocket_market = ''
            item_id = ''
        
        if division != '':
            if division == 'National':
                invoice_condition += f"AND level0_id in ('D1','D2','D3','D4')"
            else:
                invoice_condition += f"AND level0_id = '{division}'"
        if zone != '':
            invoice_condition += f"AND level1_id = '{zone}'"
        if area != '':
            invoice_condition += f"AND level2_id = '{area}'"
        if territory != '':
            invoice_condition += f"AND level3_id = '{territory}'"
        if pocket_market != '':
            invoice_condition += f"AND client_id in(SELECT client_id FROM sm_client WHERE cid = '{c_id}' and p_market_id = '{pocket_market}' GROUP BY client_id)"
            # get_client_list=f"SELECT client_id FROM sm_client where cid = '{c_id}' and p_market_id = '{pocket_market}' GROUP BY client_id;"
            # # return get_client_list
            # get_client = db.executesql(get_client_list, as_dict = True)
            # for c in range(len(get_client)):
            #     client_rec = get_client[c]
            #     client_id = str(client_rec['client_id'])
            #     client_list.append(client_id)
            # client_list = str(client_list).replace('[','').replace(']','').replace("''","'")
            # invoice_condition += f"AND client_id in('{client_list}')"
        if product_category != '':
            item_condition += f"AND category_id = '{product_category}'"
        if len(item_id) == 1:
            if item_id[0] == 'None':
                item_id =''
            else:
                item_condition += f"AND item_id = '{item_id[0]}'"
        if item_id != '' and len(item_id) > 1:
            item_condition += f"AND item_id IN {item_id}"
        record_show = True

    if btn_reset == 'Reset':
        session.sch_level_search = ''
        session.sch_zone_search = ''
        session.sch_area_search = ''
        session.sch_territory = ''
        session.sch_rx_type_search = ''
        session.search_item_id_name_search = ''
        session.division = ''
        session.zone = ''
        session.area = ''
        session.territory = ''
        session.pocket_market = ''
        session.product_category = ''
        session.item_id = ''
        session.from_date = ''
        session.to_date = ''
        today = datetime.date.today()
        session.from_date= today.replace(day=1)
        session.to_date = current_date


        # from_date = session.from_dt
        record_show = False

    if record_show == True:
        get_order_invoice_records_sql = f"""
        SELECT 
            s.item_id as item_id, 
            s.name as name, 
            s.`category_id` as basket, 
            SUM(t.order_count) AS order_count, 
            SUM(t.order_amount) AS order_amount, 
            SUM(t.invoice_count) AS invoice_count, 
            SUM(t.invoice_amount) AS invoice_amount
        FROM 
            (
        SELECT 
            item_id as item_id, 
            name AS product, 
            category_id AS basket, 
            SUM(0) AS order_count, 
            SUM(0) AS order_amount, 
            SUM(0) AS invoice_count, 
            SUM(0) AS invoice_amount
        FROM 
            sm_item 
        WHERE 
            cid = 'HAMDARD'
            {item_condition}
            AND status = 'ACTIVE'
        GROUP BY 
            item_id 

        UNION 

        SELECT 
            item_id as item_id, 
            item_name AS product, 
            category_id AS basket, 
            #COUNT(DISTINCT sl) AS order_count,
            SUM(quantity) AS order_count,
            SUM(quantity * price) AS order_amount, 
            SUM(0) AS invoice_count, 
            SUM(0) AS invoice_amount
        FROM 
            sm_order 
        WHERE 
            cid = '{c_id}' 
            AND status = 'Submitted' 
            AND order_date BETWEEN '{from_date}' AND '{to_date}' 
            {item_condition}
            {invoice_condition}
        GROUP BY 
            item_id 
        UNION 
        SELECT 
            item_id AS item_id, 
            item_name AS product, 
            category_id AS basket, 
            SUM(0) AS order_count, 
            SUM(0) AS order_amount, 
            #COUNT(DISTINCT sl) AS invoice_count,
            SUM(quantity) AS invoice_count,
            SUM(actual_tp * quantity) AS invoice_amount
        FROM 
            sm_invoice
        WHERE 
            cid = '{c_id}' 
            AND status = 'INVOICED' 
            AND order_datetime BETWEEN '{from_date}' AND '{to_date}'
            {item_condition}
            {invoice_condition}
        GROUP BY 
            item_id 
        ) AS t
        JOIN 
            sm_item AS s ON s.item_id = t.item_id
        GROUP BY 
            s.item_id, 
            s.name
        ORDER BY 
            basket asc,
            name; """
        # return get_order_invoice_records_sql
        get_order_invocie_records = db.executesql(get_order_invoice_records_sql, as_dict = True)

        product_cover = 0
        for i in range(len(get_order_invocie_records)):
            get_order_invocie_record = get_order_invocie_records[i]
            product_name = get_order_invocie_record['name']
            order_count = get_order_invocie_record['order_count']
            if order_count > 0 :
                product_cover += 1


    return dict(cid=session.cid,rep_id=session.user_id,rep_pass=session.rep_pass,rec_item=rec_item,search_item_id_name=search_item_id_name,user_type=user_type,zlevel_list=zlevel_list,level_list=level_list,level_area_list=level_area_list,seen_rx_type_list=seen_rx_type_list, division_list= division_list, zone_list = zone_list, doctor_type_record = doctor_type_record, area_list = area_list, basket_type_record=basket_type_record, product_record=product_record, get_order_invocie_records=get_order_invocie_records, product_cover=product_cover)

# ========================= HOME FUNCTION END=================================



# ========================= AUTO COMPLETE FUNCTION START =================================

def get_zone():
    retStr=''
    c_id = session.cid
    try:
        region=str(request.vars.region).split('|')[0]
    except:
        region = str(request.vars.region)
    if region == 'National':
        region = ['D1', 'D2', 'D3', 'D4']
        records=db((db.sm_level.cid == c_id)&(db.sm_level.level0.belongs(region))&(db.sm_level.depth == 1)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
    else:
        records=db((db.sm_level.cid == c_id)&(db.sm_level.level0== region)&(db.sm_level.depth == 1)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)

    # return db._lastsql
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
    try:
        zone=str(request.vars.zone).split('|')[0]
    except:
        zone = ''
    
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
    # return c_id
    # region=str(request.vars.region)
    # zone=str(request.vars.zone)
    try:
        area=str(request.vars.area).split('|')[0]
    except:
        area = ''
    
    records=db((db.sm_level.cid == c_id)&(db.sm_level.level2 == area)&(db.sm_level.depth == 3)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
    # return db._lastsql
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
    try:
        territory=str(request.vars.territory).split('|')[0]
    except:
        territory = ''
    
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


# ========================= AUTO COMPLETE FUNCTION FOR ITEM START =================================

def get_active_item():
    retStr=''
    c_id = session.cid
    try:
        category_id=str(request.vars.category_id)
    except:
        category_id = ''
    # return category_id
    if category_id != '':
        records=db((db.sm_item.cid == c_id) & (db.sm_item.category_id == category_id) & (db.sm_item.status == 'ACTIVE')).select(db.sm_item.item_id, db.sm_item.name,orderby=db.sm_item.name)
    else:
        records=db((db.sm_item.cid == c_id)& (db.sm_item.status == 'ACTIVE')).select(db.sm_item.item_id, db.sm_item.name, orderby=db.sm_item.name)
    # return db._lastsql
    for row in records:
        item_id=str(row.item_id)
        item_name=str(row.name)
        
        if retStr=='':
            retStr=item_id+'|'+item_name
        else:
            retStr+=','+item_id+'|'+item_name
        
    return retStr





def activeMaeketList():
    c_id = session.cid
    market_count_sql = f"select market_id from active_market_list where cid ='{c_id}' and status='ACTIVE';"
    market_count = db.executesql(market_count_sql,as_dict = True)
    m_id =[]
    for i in range(len(market_count)):
        x = market_count[i]['market_id']
        m_id.append(x)
    return m_id
# ========================= AUTO COMPLETE FUNCTION FOR ITEM END =================================
#=================================================================


# def get_roduct_list():
#     c_id=session.cid

#     product_record_sql = "SELECT item_id, name from sm_item where cid = '"+str(c_id)+"' and status ='ACTIVE' group by item_id order by name asc;"
#     product_record = db.executesql(product_record_sql, as_dict = True)

   
#     product_str=''
#     for product_record in product_record:
#         item_id = product_record.item_id
#         name = product_record.name
#         if product_str=='':
#             product_str=name+'|'+item_id
#         else:
#             product_str=product_str+","+name+'|'+item_id
#     return product_str



