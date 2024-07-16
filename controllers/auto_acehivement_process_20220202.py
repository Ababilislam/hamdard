import time


#http://127.0.0.1:8000/hamdard/auto_acehivement_process/process_sales_ad_route_item?req_date=2022-01-01

def process_sales_ad_route_item():
    cid='HAMDARD'
    req_date=request.vars.req_date
    if req_date=='':
        first_currentDate= str(datetime.datetime.strptime(str(current_date)[0:7] + '-01', '%Y-%m-%d'))[:10]
    else:
        first_currentDate=str(req_date)

    db.executesql("TRUNCATE temp_sales_ad_route_item;")
    db.executesql("update target_vs_achievement_route_item set achievement_qty=0 where cid='" + cid + "' and first_date='" + first_currentDate + "';")

    tranInvSql = "SELECT cid,invoice_ym_date as ym_date,'"+str(current_date)+"',category_id,item_id,sum(quantity-return_qty) as sales_qty,level0_id,level1_id,level2_id,level3_id,depot_id FROM `sm_invoice` WHERE cid='" + cid + "' and invoice_ym_date='" + first_currentDate + "' and `status`='Invoiced' group by level0_id,level1_id,level2_id,level3_id,category_id,item_id"

    #tranRetSql = "SELECT cid,ym_date,item_id,sum(quantity+bonus_qty)*-1 as sales_qty,level0_id,level1_id,level2_id,level3_id,depot_id FROM `sm_invoice` WHERE cid='" + cid + "' and ym_date='" + first_currentDate + "' and `status`='Returned' group by level0_id,level1_id,level2_id,level3_id,item_id" union all " + tranRetSql + "
    records = "insert into temp_sales_ad_route_item (cid,ym_date,process_date,category_id,item_id,sales_qty,level0_id,level1_id,level2_id,level3_id,depot_id) " + tranInvSql + ";"
    records = db.executesql(records)

    return 'Done1'

#http://127.0.0.1:8000/hamdard/auto_acehivement_process/update_acehivement?req_date=2022-01-01
def update_acehivement():
    cid = 'HAMDARD'
    req_date = request.vars.req_date
    if req_date == '':
        first_currentDate = str(datetime.datetime.strptime(str(current_date)[0:7] + '-01', '%Y-%m-%d'))[:10]
    else:
        first_currentDate = str(req_date)

    updateSqlRows="UPDATE target_vs_achievement_route_item a,temp_sales_ad_route_item b SET a.achievement_qty=b.sales_qty WHERE a.cid='"+cid+"' and a.first_date='"+first_currentDate+"' and a.cid = b.cid and a.first_date=b.ym_date and a.territory_id=b.level3_id AND a.category_id = b.category_id AND a.item_id = b.item_id;"
    updateRows=db.executesql(updateSqlRows)
    
    return 'Done2'
