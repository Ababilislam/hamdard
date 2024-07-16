
# http://127.0.0.1:8000/ibn_report/sm_ff_activity_status_cron/sm_ff_activity_status_insert_ff?dateget=2018-03-05
def sm_ff_activity_status_insert_ff_Day():
#     cid= 'ACME' 
    cid= 'IBNSINA'   
    response.title='trDLoad'
    dateget=request.vars.dateget
    current_date=str(date_fixed)[0:10]
    if dateget!='0':
        current_date=str(dateget).strip()
    deleteInvStr="delete from sm_ff_activity_status WHERE  rpt_date ='"+str(current_date)+"' and cid ='"+str(cid)+"'  ;"
    deleteInv=db.executesql(deleteInvStr)

    
    
    
    rep_areaStr="""SELECT cid,'"""+str(current_date)+"""' as field1,rep_id,rep_name,area_id,area_name FROM sm_rep_area 
                where  cid ='"""+str(cid)+"""'   GROUP BY `rep_id` ORDER BY `rep_id` ASC"""
              
    strfffActivity="""INSERT INTO  sm_ff_activity_status (cid,rpt_date,rep_id,rep_name,level3_id,level3_name) """+rep_areaStr
    
    ffInsert=db.executesql(strfffActivity)    
    return 'Success'
    


def sm_ff_activity_status_insert_ff_Regular():
#     cid= 'ACME' 
    cid= 'IBNSINA'   
    response.title='trDLoad'
    dateget=request.vars.dateget
    current_date=str(date_fixed)[0:10]
    if dateget!='0':
        current_date=str(dateget).strip()
    rep_areaDStr="""INSERT INTO  sm_ff_activity_status (cid,rpt_date,rep_id,rep_name,level3_id,level3_name) 
Select cid,'"""+str(current_date)+"""'as visit_date,rep_id,rep_name,route_id,route_name FROM sm_doctor_visit where visit_date='"""+str(current_date)+"""' and rep_id NOT IN ( Select rep_id from sm_ff_activity_status where rpt_date ='"""+str(current_date)+"""') group by rep_id"""
    rep_areaDStrInsert=db.executesql(rep_areaDStr) 
    
    
    rep_areaOStr="""INSERT INTO  sm_ff_activity_status (cid,rpt_date,rep_id,rep_name,level3_id,level3_name) 
Select cid,'"""+str(current_date)+"""'as order_date,rep_id,rep_name,area_id,area_name FROM sm_order_head where order_date='"""+str(current_date)+"""' and rep_id NOT IN ( Select rep_id from sm_ff_activity_status where rpt_date ='"""+str(current_date)+"""') group by rep_id"""
    rep_areaOStrInsert=db.executesql(rep_areaOStr)
    

    ff_levelStr="""update  sm_ff_activity_status f,sm_level l set f.level0_id=l.level0 ,f.level0_name=l.level0_name ,f.level1_id=l.level1 ,f.level1_name=l.level1_name ,f.level2_id=l.level2 ,f.level2_name=l.level2_name 
                where  f.cid=l.cid  and f.level3_id=l.level_id and l.is_leaf='1'""" 
    ffLevel=db.executesql(ff_levelStr)

    return 'Success'
    






# http://127.0.0.1:8000/ibn_report/sm_ff_activity_status_cron/sm_ff_activity_order_insert_ff?dateget=2018-03-05
def sm_ff_activity_order_insert_ff():
    current_date=str(date_fixed)[0:10]
    dateget=request.vars.dateget
    if dateget!='0':
        current_date=str(dateget).strip()
    deleteStr="TRUNCATE sm_ff_activity_status_count ;"
    deleteRun=db.executesql(deleteStr)
    
    insStr="INSERT INTO  sm_ff_activity_status_count (rep_id, t_count,order_date) SELECT rep_id, COUNT(ID),order_date   FROM sm_order_head WHERE cid='IBNSINA' AND order_date='"+str(current_date)+"' GROUP BY rep_id;"
    insRun=db.executesql(insStr)
    return 'Success'

# http://127.0.0.1:8000/ibn_report/sm_ff_activity_status_cron/sm_ff_activity_order_update_ff
def sm_ff_activity_order_update_ff():
    updateStr="UPDATE sm_ff_activity_status f, sm_ff_activity_status_count c SET f.order_count = c.`t_count` WHERE f.rep_id = c.`rep_id` and f.rpt_date = c.`order_date`;"
    updateRun=db.executesql(updateStr)
    return 'Success'

# http://127.0.0.1:8000/ibn_report/sm_ff_activity_status_cron/sm_ff_activity_doc_insert_ff?dateget=2018-03-05
def sm_ff_activity_doc_insert_ff():
    current_date=str(date_fixed)[0:10]
    dateget=request.vars.dateget
    if dateget!='0':
        current_date=str(dateget).strip()
    deleteStr="TRUNCATE sm_ff_activity_status_count ;"
    deleteRun=db.executesql(deleteStr)
    
    insStr="INSERT INTO  sm_ff_activity_status_count (rep_id, t_count,order_date) SELECT rep_id, COUNT(id),visit_date FROM sm_doctor_visit WHERE cid='IBNSINA' AND visit_date='"+str(current_date)+"' GROUP BY rep_id;"
    insRun=db.executesql(insStr)
    return 'Success'

# http://127.0.0.1:8000/ibn_report/sm_ff_activity_status_cron/sm_ff_activity_doc_update_ff
def sm_ff_activity_doc_update_ff():
    updateStr="UPDATE sm_ff_activity_status f, sm_ff_activity_status_count c SET f.dcr_count = c.`t_count` WHERE f.rep_id = c.`rep_id` and f.rpt_date = c.`order_date`;"
    updateRun=db.executesql(updateStr)
    return 'Success'















#http://127.0.0.1:8000/ibn_report/sm_ff_activity_status_cron/sm_ff_activity_status_insert_order
def sm_ff_activity_status_insert_order():
    
    cid= 'IBNSINA'   

    rep_idList=''
    rep_ff_odr_asc_Str="""SELECT rep_id  from sm_ff_activity_status 
                where  cid ='"""+str(cid)+"""' and field2 ='0' group by rep_id
                order by rep_id asc limit 20"""
#    return rep_ff_odr_asc_Str
    rep_ordrAs=db.executesql(rep_ff_odr_asc_Str,as_dict = True)
    for rep_ordrAs in rep_ordrAs:
        rep_id_list=rep_ordrAs['rep_id']
        if rep_idList=='':
            rep_idList = "'"+rep_id_list+"'"
        else:
            rep_idList += ','+"'"+rep_id_list+"'"
  
    




         
    rep_odr_desc_Str="""SELECT order_datetime ,rep_id,area_id,order_date  from sm_order_head 
                where  cid ='"""+str(cid)+"""' and rep_id in ("""+rep_idList+""")  and order_date= '"""+str(current_date)+"""'  group by rep_id,area_id
                order by order_datetime DESC """
    ordrDes=db.executesql(rep_odr_desc_Str,as_dict = True)
    for ordrDes in ordrDes: 
        try:
            rep_id_order=ordrDes['rep_id']
        except:
            rep_id_order=''
        try:
            order_datetime=ordrDes['order_datetime']
        except:
            order_datetime=''
        try:
            area_id=ordrDes['area_id']
        except:
            area_id=''
        try:
            order_date=ordrDes['order_date']
        except:
            order_date=''
          
          
        try:
            last_ordr_Str="""update  sm_ff_activity_status set first_order_time='"""+str(order_datetime)+"""' where cid ='"""+str(cid)+"""' and rep_id='"""+str(rep_id_order)+"""' and level3_id='"""+str(area_id)+"""' and  rpt_date='"""+str(order_date)+"""' """ 
            orderDscStr=db.executesql(last_ordr_Str)
        except:
            pass
        
    update_ordr_Str="""update  sm_ff_activity_status set field2 ='1' where cid ='"""+str(cid)+"""' and rep_id in ("""+rep_idList+""")  """
    updateStr=db.executesql(update_ordr_Str)
    return 'SuccessOrder'



#http://127.0.0.1:8000/ibn_report/sm_ff_activity_status_cron/sm_ff_activity_status_insert_dcr
def sm_ff_activity_status_insert_dcr():
    
    cid= 'IBNSINA'   

    rep_idList=''
    rep_ff_dcr_asc_Str="""SELECT rep_id  from sm_ff_activity_status 
                where  cid ='"""+str(cid)+"""' and  field2 ='1'  group by rep_id
                order by rep_id asc limit 20"""
   # return rep_ff_dcr_asc_Str
    rep_dcrAs=db.executesql(rep_ff_dcr_asc_Str,as_dict = True)
    for rep_dcrAs in rep_dcrAs:
        rep_id_list=rep_dcrAs['rep_id']
        if rep_idList=='':
            rep_idList = "'"+rep_id_list+"'"
        else:
            rep_idList += ','+"'"+rep_id_list+"'"

    


#desc    
    
    rep_dcr_desc_Str="""SELECT rep_id,doc_id,doc_name,visit_dtime,level3_id,visit_date  from sm_doctor_visit 
                where  cid ='"""+str(cid)+"""'  and rep_id in ("""+rep_idList+""")  and visit_date= '"""+str(current_date)+"""'  group by rep_id,level3_id,visit_dtime  
                order by visit_dtime desc """


  #  return rep_dcr_desc_Str
    dcrdsc=db.executesql(rep_dcr_desc_Str,as_dict = True)

    
    for dcrdsc in dcrdsc:
        try:
            rep_id=dcrdsc['rep_id']
        except:
            rep_id=''
        try:
            doc_id=dcrdsc['doc_id']
        except:
            doc_id=''
        try:
            doc_name=dcrdsc['doc_name']
        except:
            doc_name=''
        try:
            visit_dtime=dcrdsc['visit_dtime']
        except:
            visit_dtime=''
        try:
            level3_id=dcrdsc['level3_id']
        except:
            level3_id=''
        try:
            visit_date=dcrAcs['visit_date']
        except:
            visit_date=''

        try:
            last_dcr_Str="""update  sm_ff_activity_status set first_visit_doc_id='"""+str(doc_id)+"""',first_visit_doc_name='"""+str(doc_name)+"""' , first_visit_doc_date='"""+str(visit_dtime)+"""' where cid ='"""+str(cid)+"""' and rep_id='"""+str(rep_id)+"""'   and level3_id='"""+str(level3_id)+"""'  and  rpt_date='"""+str(visit_date)+"""' """
            dcrDscStr=db.executesql(last_dcr_Str)
      #      return dcrDscStr
        except:
            pass
    
    update_dcr_Str="""update  sm_ff_activity_status set field2 ='2' where cid ='"""+str(cid)+"""' and rep_id in ("""+rep_idList+""")  and  field2 ='1'  """
#     return update_dcr_Str
    updateStr=db.executesql(update_dcr_Str)
    return 'SuccessDoctor' 

# 2018/03/06

#http://127.0.0.1:8000/ibn_report/sm_ff_activity_status_cron/sm_ff_activity_status_count



#Cont
def sm_ff_activity_status_count():    
#     datePass = '12/05/2017'
    cid = 'IBNSINA'
#     count_orderStr= """update sm_ff_activity_status F,sm_order_head O  set F.order_count = (select COUNT(id) from sm_order_head where sm_order_head.cid = sm_ff_activity_status.cid and sm_order_head.rep_id= sm_ff_activity_status.rep_id and sm_order_head.area_id =sm_ff_activity_status.level3_id and sm_ff_activity_status.cid ='"""+str(cid)+"""' and  sm_ff_activity_status.rpt_date =sm_order_head.order_date)"""
    
    count_orderStr= """update sm_ff_activity_status F,sm_order_head O  set F.order_count =  COUNT(O.id) where O.cid = F.cid and O.rep_id= F.rep_id and O.area_id =F.level3_id and  F.cid ='"""+str(cid)+"""' and  F.rpt_date =O.order_date and F.rpt_date='"""+str(current_date)+""" ' """
#     return count_orderStr
    countOrder=db.executesql(count_orderStr)


    count_dcrStr= """update sm_ff_activity_status set dcr_count = (select COUNT(id) from sm_doctor_visit where sm_doctor_visit.cid = sm_ff_activity_status.cid and sm_doctor_visit.rep_id= sm_ff_activity_status.rep_id and sm_doctor_visit.level3_id =sm_ff_activity_status.level3_id and sm_ff_activity_status.cid ='"""+str(cid)+"""' and  sm_ff_activity_status.rpt_date =sm_doctor_visit.visit_date)"""
    countDcr=db.executesql(count_dcrStr)
    return 'Success Count'




           
