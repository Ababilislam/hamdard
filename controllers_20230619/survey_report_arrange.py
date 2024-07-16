# http://127.0.0.1:8000/skf/doctor_visit_arrange/doctor_visit_arrange
#====================== Doctor Visit

from random import randint


#---------------------------- ADD
def survey_arrange():
    c_id='SKF'

    qset=db()
    qset=qset(db.sm_prescription_head.cid==c_id)
    qset=qset(db.sm_prescription_head.field2==0)
    qset=qset(db.sm_prescription.cid==c_id)
    qset=qset(db.sm_prescription_head.sl==db.sm_prescription.sl)
    

    limitby=(0,100)
    records=qset.select(db.sm_doctor_visit.ALL,orderby=db.sm_doctor_visit.id,limitby=limitby)
    return records
    sampinsDict={}
    sampinsList=[]

    for record in records:
        cid =record.cid
        rep_id =record.rep_id
        rep_name=record.rep_name
        doc_id=record.doc_id
        doc_name=record.doc_name
        route_id=record.route_id
        route_name=record.route_name
        depot_id=record.depot_id
        depot_name=''#record.depot_name
        level2_id=record.level2_id
        level2_name=record.level2_name
        level1_id=record.level1_id
        level1_name=record.level1_name
        level0_id=record.level0_id
        level0_name=record.level0_name
        visited_flag=''# record.visited_flag
        visit_sl=record.id
        visit_date=record.visit_date
        status=''
        idList.append(visit_sl) 
        showList=showList+','+str(visit_sl)
        if record.giftnsample!='' : 
            dataList=str(record.giftnsample).split('rdsep')
            if len(dataList)==4:
                propList=str(dataList[0]).split('fdsep')
                giftList=str(dataList[1]).split('fdsep')
                sampleList=str(dataList[2]).split('fdsep')
                ppmList=str(dataList[3]).split('fdsep')



    if records:
        if len(propinsList) > 0:
            inProp=db.sm_doc_visit_prop.bulk_insert(propinsList) 
            records_retS="update sm_doc_visit_prop, sm_item  set  sm_doc_visit_prop.item_brand=sm_item.manufacturer,sm_doc_visit_prop.item_cat=sm_item.category_id  WHERE sm_doc_visit_prop.cid = sm_item.cid AND sm_doc_visit_prop.item_id = sm_item.item_id  AND     sm_doc_visit_prop.item_brand='';"
            records_ret=db.executesql(records_retS)
#             return 'prop'
#         return len(sampinsList)
        if len(sampinsList) >0:
            inSample=db.sm_doc_visit_sample.bulk_insert(sampinsList) 
            records_retS="update sm_doc_visit_sample, sm_item  set  sm_doc_visit_sample.item_brand=sm_item.manufacturer,sm_doc_visit_sample.item_cat=sm_item.category_id  WHERE sm_doc_visit_sample.cid = sm_item.cid AND sm_doc_visit_sample.item_id = sm_item.item_id  AND     sm_doc_visit_sample.item_brand='';"
            records_ret=db.executesql(records_retS)
            records_retS="update sm_doc_visit_sample, sm_level  set  sm_doc_visit_sample.trDesc=sm_level.territory_des WHERE sm_doc_visit_sample.cid = sm_level.cid AND sm_doc_visit_sample.route_id = sm_level.level_id  AND     sm_level.is_leaf=1 AND     sm_doc_visit_sample.trDesc='';"
            records_ret=db.executesql(records_retS)
#             return 'Sample'
        if len(giftinsList) > 0:
            inGift=db.sm_doc_visit_gift.bulk_insert(giftinsList) 
#             return 'Gift'
#         if len(ppminsList) > 0:
# #             return'sdasdas'
#             inPpm=db.sm_doc_visit_ppm.bulk_insert(ppminsDict) 
#             return 'PPPM'
        planRecords=db((db.sm_doctor_visit.cid==c_id)& (db.sm_doctor_visit.id.belongs(idList)) ).update(field2=1)
        
        
        
         
        return 'SUCCESS'                    
    

        