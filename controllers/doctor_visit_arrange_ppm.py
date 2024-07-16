# http://127.0.0.1:8000/HAMDARD/doctor_visit_arrange/doctor_visit_arrange
#====================== Doctor Visit

from random import randint


      
def doctor_visit_arrangePPM_test():
    c_id='HAMDARD'
    limitby=(0,50)
    qset=db()
    qset=qset(db.sm_doctor_visit.cid==c_id)
    qset=qset((db.sm_doctor_visit.field2==0))# or (db.sm_doctor_visit.field2==0))
#     qset=qset(db.sm_doctor_visit.giftnsample!='')
    qset=qset(db.sm_doctor_visit.visit_date>='2022-09-01')
    # qset=qset(db.sm_doctor_visit.id > 69312688)
    records=qset.select(db.sm_doctor_visit.ALL,orderby=db.sm_doctor_visit.id,limitby=limitby)
    if records:
        pass
    else:
        qset=db()
        qset=qset(db.sm_doctor_visit.cid==c_id)
        qset=qset((db.sm_doctor_visit.field2==1))# or (db.sm_doctor_visit.field2==0))
    #     qset=qset(db.sm_doctor_visit.giftnsample!='')
        qset=qset(db.sm_doctor_visit.visit_date>='2022-09-01')
        # qset=qset(db.sm_doctor_visit.id > 69312688)
        records=qset.select(db.sm_doctor_visit.ALL,orderby=db.sm_doctor_visit.id,limitby=limitby)
#     records=qset.select(db.sm_doctor_visit.ALL,orderby=db.sm_doctor_visit.id)
    # return db._lastsql
    idList=[]
    showList=''
    sampinsDict={}
    sampinsList=[]
    propinsDict={}
    propinsList=[]
    giftinsDict={}
    giftinsList=[]
    ppminsDict={}
    ppminsList=[]
#     return records
    for record in records:
        cid =record.cid
        rep_id =record.rep_id
        rep_name=str(record.rep_name).replace("'","")
        doc_id=record.doc_id
        doc_name=str(record.doc_name).replace("'","")
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
                        
# #                 ppm==============
#                 return ppmList
                if str(dataList[3])!='' and len(ppmList)>0:
                    ppmitemID=''
                    ppmitemName=''
                    for q in range(len(ppmList)):
                        ppmDataList=str(ppmList[q]).split(',')
                        if len(ppmDataList)==3:
                            ppmitemID=ppmDataList[0]
                            ppmitemName=ppmDataList[1]
                              
                            ppminsDict={'cid':c_id,'rep_id':rep_id,'rep_name':rep_name,'doc_id':doc_id,'doc_name':doc_name,'route_id':route_id,'route_name':route_name,'depot_id':depot_id,'depot_name':depot_name,'level2_id':level2_id,'level2_name':level2_name,'level1_id':level1_id,'level1_name':level1_name,'level0_id':level0_id,'level0_name':level0_name, 'visited_flag':visited_flag,'visit_sl':visit_sl,'visit_date':visit_date,'item_id':ppmitemID,'item_name':ppmitemName}
                            ppminsList.append(ppminsDict)  
                            
    if records:   
#         return len(ppminsList)
        if len(ppminsList) > 0:
            inPpm=db.sm_doc_visit_ppm.bulk_insert(ppminsList) 
    
#             records_retS="update  sm_doc_visit_ppm, sm_level  set   sm_doc_visit_ppm.trDesc=sm_level.territory_des WHERE  sm_doc_visit_ppm.cid = sm_level.cid AND  sm_doc_visit_ppm.route_id = sm_level.level_id  AND     sm_level.is_leaf=1 AND      sm_doc_visit_ppm.trDesc='';"
#             records_ret=db.executesql(records_retS)
    
        planRecords=db((db.sm_doctor_visit.cid==c_id)& (db.sm_doctor_visit.id.belongs(idList)) ).update(field2=2)
        # return len(idList)
        
        
         
        return 'SUCCESS'      

    
# ==============================Sampl update==============   

def doctor_visit_sample_update_test():
    records_retS="update sm_doc_visit_sample, sm_item  set  sm_doc_visit_sample.item_brand=sm_item.manufacturer,sm_doc_visit_sample.item_cat=sm_item.category_id  WHERE sm_doc_visit_sample.cid = sm_item.cid AND sm_doc_visit_sample.item_id = sm_item.item_id  AND     sm_doc_visit_sample.item_brand='';"
    records_ret=db.executesql(records_retS)
    records_retS="update sm_doc_visit_sample, sm_level  set  sm_doc_visit_sample.trDesc=sm_level.territory_des WHERE sm_doc_visit_sample.cid = sm_level.cid AND sm_doc_visit_sample.route_id = sm_level.level_id  AND     sm_level.is_leaf=1 AND     sm_doc_visit_sample.trDesc='';"
    records_ret=db.executesql(records_retS)
    return 'SUCCESS'

    
#   =========================================      
def doctor_visit_arrange_SP_tr_test():     
    c_id='HAMDARD'

    records_S="update sm_doctor_visit, sm_level  set  sm_doctor_visit.special_territory_code=sm_level.special_territory_code  WHERE sm_doctor_visit.cid='"+c_id +"' and sm_doctor_visit.special_territory_code='' and sm_doctor_visit.field1=1 & sm_level.cid='"+c_id+"' and  sm_level.is_leaf=1 and sm_level.special_territory_code!='' and sm_level.level_id=sm_doctor_visit.route_id;"
#     return records_S
    records=db.executesql(records_S)
    records_S1="update sm_doctor_visit, sm_level  set  sm_doctor_visit.special_fm_code=sm_level.level2,sm_doctor_visit.special_rsm_code=sm_level.level1,sm_doctor_visit.field1=2  WHERE sm_doctor_visit.cid='"+c_id +"' and sm_doctor_visit.special_territory_code!='' and sm_doctor_visit.field1=1 & sm_level.cid='"+c_id+"' and  sm_level.is_leaf=1 and sm_level.level_id=sm_doctor_visit.special_territory_code;"
#     return records_S1
    recordsS1=db.executesql(records_S)

    return "SUCCESS"