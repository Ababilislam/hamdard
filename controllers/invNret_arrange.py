# http://127.0.0.1:8000/skf/invNret_arrange/invNret_arrange
#====================== Doctor Visit

from random import randint


#---------------------------- ADD
def invNret_arrange():
#     c_id='SKF'


    records_invS="update sm_invoice, sm_item,sm_rep_area  set  sm_invoice.msoCategory=sm_rep_area.rep_category,sm_invoice.itembaseGroup=sm_item.category_id_sp  WHERE sm_invoice.cid = sm_item.cid AND sm_invoice.item_id = sm_item.item_id  AND sm_invoice.cid=sm_rep_area.cid AND sm_invoice.area_id=sm_rep_area.area_id AND sm_invoice.rep_id=sm_rep_area.rep_id;"
    records_inv=db.executesql(records_invS)

    records_retS="update sm_return, sm_item,sm_rep_area  set  sm_return.msoCategory=sm_rep_area.rep_category,sm_return.itembaseGroup=sm_item.category_id_sp  WHERE sm_return.cid = sm_item.cid AND sm_return.item_id = sm_item.item_id  AND sm_return.cid=sm_rep_area.cid AND sm_return.area_id=sm_rep_area.area_id AND sm_return.rep_id=sm_rep_area.rep_id;"
    records_ret=db.executesql(records_retS)
    
    return 'SUCCESS'                    
