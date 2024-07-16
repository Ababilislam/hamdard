# http://127.0.0.1:8000/skf/doctor_visit_arrange/doctor_visit_arrange
#====================== Doctor Visit

from random import randint


#---------------------------- ADD
def invoiceCteamArrange():
    c_id='SKF'
    records_retS="update sm_invoice, sm_level  set  sm_invoice.special_rsm_code=sm_level.level1,sm_invoice.special_fm_code=sm_level.level2  WHERE sm_invoice.cid = sm_level.cid AND sm_invoice.special_territory_code = sm_level.level_id  AND     sm_invoice.special_territory_code!='' AND sm_invoice.special_rsm_code='' AND sm_invoice.special_fm_code='';"
    records_ret=db.executesql(records_retS)
    records_retS="update sm_invoice_head, sm_level  set  sm_invoice_head.special_rsm_code=sm_level.level1,sm_invoice_head.special_fm_code=sm_level.level2  WHERE sm_invoice_head.cid = sm_level.cid AND sm_invoice_head.special_territory_code = sm_level.level_id  AND     sm_invoice_head.special_territory_code!='' AND sm_invoice_head.special_rsm_code='' AND sm_invoice_head.special_fm_code='';"
    records_ret=db.executesql(records_retS)
    return 'SUCCESS'                          
        