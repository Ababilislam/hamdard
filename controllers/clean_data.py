# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#======================= Cron for clean data
def clean_company_data():
    import datetime
    compRows=db().select(db.sm_company_settings.cid,db.sm_company_settings.clean_Data,db.sm_company_settings.keep_history,orderby=db.sm_company_settings.cid)
    if compRows:
        for compRow in compRows:
            cid=str(compRow.cid).strip().upper()
            clean_Data=str(compRow.clean_Data).strip().upper()
            try:
                keep_history=int(compRow.keep_history)
            except:
                keep_history=0
                
            if (clean_Data=='YES' and keep_history!=0):
                fromData=datetime.datetime.now()-datetime.timedelta(days=keep_history)
                keep_date=str(fromData)[0:10]
                
                #---------- requisition
                reqHeadRecords=db((db.sm_requisition_head.cid==cid)&(db.sm_requisition_head.req_date<keep_date)).select(db.sm_requisition_head.id,limitby=(0, 500))
                for rec in reqHeadRecords:
                    db(db.sm_requisition_head.id==rec.id).delete()
                    
                reqRecords=db((db.sm_requisition.cid==cid)&(db.sm_requisition.req_date<keep_date)).select(db.sm_requisition.id,limitby=(0, 500))
                for rec in reqRecords:
                    db(db.sm_requisition.id==rec.id).delete()
                    
                #---------- issue
                issueHeadRecords=db((db.sm_issue_head.cid==cid)&(db.sm_issue_head.issue_date<keep_date)).select(db.sm_issue_head.id,limitby=(0, 500))
                for rec in issueHeadRecords:
                    db(db.sm_issue_head.id==rec.id).delete()
                    
                issueRecords=db((db.sm_issue.cid==cid)&(db.sm_issue.issue_date<keep_date)).select(db.sm_issue.id,limitby=(0, 500))
                for rec in issueRecords:
                    db(db.sm_issue.id==rec.id).delete()
                
                #---------- Receive
                recHeadRecords=db((db.sm_receive_head.cid==cid)&(db.sm_receive_head.receive_date<keep_date)).select(db.sm_receive_head.id,limitby=(0, 500))
                for rec in recHeadRecords:
                    db(db.sm_receive_head.id==rec.id).delete()
                    
                recRecords=db((db.sm_receive.cid==cid)&(db.sm_receive.receive_date<keep_date)).select(db.sm_receive.id,limitby=(0, 500))
                for rec in recRecords:
                    db(db.sm_receive.id==rec.id).delete()
                
                #---------- Damage
                damHeadRecords=db((db.sm_damage_head.cid==cid)&(db.sm_damage_head.damage_date<keep_date)).select(db.sm_damage_head.id,limitby=(0, 500))
                for rec in damHeadRecords:
                    db(db.sm_damage_head.id==rec.id).delete()
                    
                damRecords=db((db.sm_damage.cid==cid)&(db.sm_damage.damage_date<keep_date)).select(db.sm_damage.id,limitby=(0, 500))
                for rec in damRecords:
                    db(db.sm_damage.id==rec.id).delete()
                
                #---------- Order
                ordHeadRecords=db((db.sm_order_head.cid==cid)&(db.sm_order_head.order_date<keep_date)).select(db.sm_order_head.id,limitby=(0, 500))
                for rec in ordHeadRecords:
                    db(db.sm_order_head.id==rec.id).delete()
                    
                ordRecords=db((db.sm_order.cid==cid)&(db.sm_order.order_date<keep_date)).select(db.sm_order.id,limitby=(0, 500))
                for rec in ordRecords:
                    db(db.sm_order.id==rec.id).delete()
                
                #---------- Delivery
                delHeadRecords=db((db.sm_invoice_head.cid==cid)&(db.sm_invoice_head.delivery_date<keep_date)).select(db.sm_invoice_head.id,limitby=(0, 500))
                for rec in delHeadRecords:
                    db(db.sm_invoice_head.id==rec.id).delete()
                    
                delRecords=db((db.sm_invoice.cid==cid)&(db.sm_invoice.delivery_date<keep_date)).select(db.sm_invoice.id,limitby=(0, 500))
                for rec in delRecords:
                    db(db.sm_invoice.id==rec.id).delete()
                
                #---------- Return
                retHeadRecords=db((db.sm_return_head.cid==cid)&(db.sm_return_head.return_date<keep_date)).select(db.sm_return_head.id,limitby=(0, 500))
                for rec in retHeadRecords:
                    db(db.sm_return_head.id==rec.id).delete()
                    
                retRecords=db((db.sm_return.cid==cid)&(db.sm_return.return_date<keep_date)).select(db.sm_return.id,limitby=(0, 500))
                for rec in retRecords:
                    db(db.sm_return.id==rec.id).delete()
                
                #---------- Inbox
                keep_date=datetime.datetime.strptime(keep_date,'%Y-%m-%d')
                inboxRecords=db((db.sm_inbox.cid==cid)&(db.sm_inbox.sms_date<keep_date)).select(db.sm_inbox.id,limitby=(0, 500))
                for rec in inboxRecords:
                    db(db.sm_inbox.id==rec.id).delete()

    return 'ok'


    