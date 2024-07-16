
def update_ho():
    db((db.sm_invoice.cid=='IDL') & (db.sm_invoice.delivery_date > '2012-08-23')).update(ho_status='0')
    db((db.sm_invoice_head.cid=='IDL') & (db.sm_invoice_head.delivery_date > '2012-08-23')).update(ho_status='0')
    return dict(message='success')