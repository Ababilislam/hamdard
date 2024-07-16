import time

#http://w02.yeapps.com/hamdard/auto_acehivement_process_area_wise/process_area_wise
#http://127.0.0.1:8000/hamdard/auto_acehivement_process_area_wise/process_area_wise?month_first_date=
def process_area_wise():
    cid='HAMDARD'
    month_first_date=request.vars.month_first_date
    if month_first_date=='':
        month_first_date=str(first_currentDate)[:10]
    else:
        month_first_date=month_first_date

    acheivementList=[]
    acheivementSql='Select invoice_ym_date,area_id,item_id,sum(quantity) as achQty from sm_invoice where cid="'+cid+'" and invoice_ym_date="'+str(month_first_date)+'" and status="Invoiced" group by invoice_ym_date,area_id,item_id;'
    acheivementList=db.executesql(acheivementSql,as_dict=True)
    #return str(acheivementSql)
    if len(acheivementList)>0:
        for i in range(len(acheivementList)):
            acheivementListStr=acheivementList[i]
            
            invoice_ym_date=str(acheivementListStr['invoice_ym_date'])
            area_id=str(acheivementListStr['area_id'])
            item_id=str(acheivementListStr['item_id'])
            achQty=str(acheivementListStr['achQty'])

            updateSqlRows="update target_vs_achievement_route_item set achievement_qty='"+str(achQty)+"' WHERE cid='"+cid+"' AND first_date='"+str(invoice_ym_date)+"' AND territory_id = '"+str(area_id)+"' AND item_id = '"+str(item_id)+"';"
            updateRows=db.executesql(updateSqlRows)
    
    return 'Done'

