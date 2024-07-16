#=====  sm_item   ==========

def sm_item_insert(): 
    
    deleteStr="TRUNCATE sm_item ;"
    deleteRun=db.executesql(deleteStr)
    
    insStr="INSERT INTO  sm_item (cid,item_id,name,des,category_id,price,created_on,status,unit_type,vat_amt,total_amt,item_carton) SELECT '"+'KPL'+"',P_CODE,P_DESC as BRAND_CODE,P_DESC,PROD_STAT,COMM_TP,ENTER_DT ,'"+'ACTIVE'+"','"+'UNIT'+"',COMM_VP,FLAT_RATE,PACK_SIZE FROM zkpl_product GROUP BY id,P_CODE;"

    insRun=db.executesql(insStr)
    
    
    
    return 'Success'


#=====  sm_item end  ==========
              
                
#====  sm_client ========

def sm_client_insert(): 
    deleteStr="TRUNCATE sm_client ;"
    deleteRun=db.executesql(deleteStr)
    
    insStr="INSERT INTO  sm_client (id,client_id,name,area_id,market_id,address,created_on,cid,status) SELECT id,CUST_CODE,CUST_NAME,MPO_CODE,MKT_CODE,RD_NAME,ENTER_DT,'"+'KPL'+"','ACTIVE' FROM zkpl_customer GROUP BY id,CUST_CODE;"
    insRun=db.executesql(insStr)
    return 'Success'

def sm_client_DIupdate():     
    insStrUpdate="UPDATE  sm_client c, zkpl_sd_mpo m set c.depot_id= m.DEPOT_CODE   where c.area_id=m.MPO_CODE ;"
    insRun=db.executesql(insStrUpdate)
    return 'Success'

def sm_client_DSupdate():     
    insStrUpdateS="UPDATE  sm_client c, sm_depot_store d set c.store_id= d.store_id ,c.store_name= d.store_name  where c.depot_id=d.depot_id;"
    insRun=db.executesql(insStrUpdateS)
    return 'Success'

def sm_client_DNupdate():     
    insStrUpdateDN="UPDATE  sm_client c, sm_depot d set c.depot_name= d.name   where c.depot_id=d.depot_id;"
    insRun=db.executesql(insStrUpdateDN)
    return 'Success'

                                         
# === sm_client end ===                                       
                                          
                                        
# ====== sm_level ==========
   # === am ===







def sm_levelam_insert(): 
    
    deleteStr="TRUNCATE temp_sm_level ;"
    deleteRun=db.executesql(deleteStr)
    
    insStr="INSERT INTO  temp_sm_level (id,level_id,level_name,level0,level0_name,parent_level_id,parent_level_name,is_leaf,depth,cid) SELECT id,AM_CODE,AM_AREA,AM_CODE,AM_AREA,'"+'0'+"','"+'-'+"','"+'0'+"','"+'0'+"','"+'KPL'+"' FROM zkpl_sd_am GROUP BY id,AM_CODE ;"
                                                                                                                                                                              
                                                                                                                                                                            
    insRun=db.executesql(insStr)
    return 'Success'


  # === rm ===


def sm_levelrm_insert(): 
    
    ff_levelStr="INSERT INTO  temp_sm_level (id,level_id,level_name,parent_level_id,level0,level1,level1_name,depth,is_leaf,cid) SELECT id,RM_CODE ,REGION ,AM_CODE ,AM_CODE ,RM_CODE ,REGION ,'"+'1'+"','"+'0'+"','"+'KPL'+"' FROM zkpl_sd_rm ;"
    ffLevel=db.executesql(ff_levelStr)

    return 'Success'



def sm_levelrm_update(): 
    
    insStr="""UPDATE temp_sm_level l ,zkpl_sd_am a set l.parent_level_name=a.AM_AREA ,l.level0_name=a.AM_AREA  where  l.parent_level_id=a.AM_CODE """

    db.executesql(insStr)
    
    return 'Success'


   # === fm ===

def sm_levelfm_insert(): 
    
    ff_levelStr="INSERT INTO  temp_sm_level (id,level_id,level_name,parent_level_id,level1,level2,level2_name,depth,is_leaf,cid) SELECT id,FM_CODE ,FM_AREA, RM_CODE, RM_CODE ,FM_CODE ,FM_AREA ,'"+'2'+"','"+'0'+"','"+'KPL'+"' FROM zkpl_sd_fm ;"
    ffLevel=db.executesql(ff_levelStr)

    return 'Success'

 
def sm_levelfm_update(): 

    insStr="""UPDATE temp_sm_level l ,zkpl_sd_rm r set l.level0=r.AM_CODE  where l.parent_level_id=r.RM_CODE """
    
    db.executesql(insStr)
      
    return 'Success'

def sm_levelfm1_update(): 

    
    insStr="""UPDATE temp_sm_level l ,zkpl_sd_am a set l.level0_name=a.AM_AREA  where l.level0=a.AM_CODE """

 
    db.executesql(insStr)
      
    return 'Success'

def sm_levelfm2_update(): 
 
    insStr="""UPDATE temp_sm_level l, zkpl_sd_rm r set l.parent_level_name=r.REGION ,l.level1_name=r.REGION where l.parent_level_id=r.RM_CODE  """
    
    db.executesql(insStr)
      
    return 'Success'

   
   # === mpo ===

def sm_levelmpo_insert(): 
     
    ff_levelStr="INSERT INTO  temp_sm_level (id,level_id,level_name,parent_level_id,level0,level1,level2,level3,level3_name,depth,is_leaf,cid) SELECT id,MPO_CODE ,TERRI_NAME,FM_CODE,AM_CODE,RM_CODE,FM_CODE,MPO_CODE,TERRI_NAME, '"+'3'+"','"+'1'+"','"+'KPL'+"' FROM zkpl_sd_mpo ;"
    db.executesql(ff_levelStr)
 
    return 'Success'   
 


def sm_levelmpo_update(): 
    
    insStr="""UPDATE temp_sm_level l ,zkpl_sd_fm f set l.parent_level_name=f.FM_AREA ,l.level2_name=f.FM_AREA  where l.parent_level_id=f.FM_CODE """
   
    db.executesql(insStr)
      
    return 'Success'


def sm_levelmpo1_update(): 
    

    insStr="""UPDATE temp_sm_level l ,zkpl_sd_rm r set l.level1_name=r.REGION  where l.level1=r.RM_CODE """

   
    db.executesql(insStr)
      
    return 'Success'


def sm_levelmpo2_update(): 

    insStr="""UPDATE temp_sm_level l ,zkpl_sd_am a set l.level0_name=a.AM_AREA  where l.level0=a.AM_CODE """
   
    db.executesql(insStr)
      
    return 'Success'




def sm_leveltemp_to_main(): 
    deleteStr="TRUNCATE sm_level ;"
    deleteRun=db.executesql(deleteStr)
    
    ff_levelStr="INSERT INTO  sm_level (id,cid,level_id,level_name,parent_level_id,parent_level_name,is_leaf,area_id_list,special_territory_code,depot_id,depth,level0,level0_name,level1,level1_name,level2,level2_name,level3,level3_name,level4,level4_name,level5,level5_name,level6,level6_name,level7,level7_name,level8,level8_name,territory_des,field1,field2,note,created_on,created_by,updated_on,updated_by) SELECT id,cid,level_id,level_name,parent_level_id,parent_level_name,is_leaf,area_id_list,special_territory_code,depot_id,depth,level0,level0_name,level1,level1_name,level2,level2_name,level3,level3_name,level4,level4_name,level5,level5_name,level6,level6_name,level7,level7_name,level8,level8_name,territory_des,field1,field2,note,created_on,created_by,updated_on,updated_by FROM temp_sm_level ;"
    db.executesql(ff_levelStr)
 
    return 'Success'   




#===== sm_level end  ======

#===== sm_depot  ======

def sm_depot_insert():
   
    deleteStr="TRUNCATE sm_depot ;"
    deleteRun=db.executesql(deleteStr)
    
    insStr="INSERT INTO  sm_depot (id,depot_id,name,cid,short_name,status,depot_category) SELECT id,DEPOT_CODE,DEPOT_DESC,'"+'KPL'+"',DEPOT_DESC as UPD_FLAG,'"+'ACTIVE'+"','"+'DEPOT'+"' FROM zkpl_sd_depot_new GROUP BY id;"

    insRun=db.executesql(insStr)
    
    
    
    deleteSStr="TRUNCATE sm_depot_store ;"
    deleteSRun=db.executesql(deleteSStr)
    insStrStore="INSERT INTO  sm_depot_store (id,depot_id,store_id,cid,store_name,store_type) SELECT id,DEPOT_CODE,concat(DEPOT_CODE,'001' ),'"+'KPL'+"',concat(DEPOT_DESC,'Store' ),'"+'SALES'+"' FROM zkpl_sd_depot_new GROUP BY id;"

    insRun=db.executesql(insStrStore)
    return 'Success'


#===== sm_depot end ======





# ===========Rep pass and syncode bakup================
def z_kpl_backup_insert():    
    deleteStr="TRUNCATE z_kpl_backup ;"
    deleteRun=db.executesql(deleteStr)
    
    insStr="INSERT INTO  z_kpl_backup (cid,rep_id,password,sync_code,online) SELECT cid,rep_id,password,sync_code,'"+'NO'+"' FROM sm_rep GROUP BY rep_id;"
    insRun=db.executesql(insStr)
    return 'Success'

# ======================================================
#===== sm_rep  ======

def sm_rep_insert():

    deleteStr="TRUNCATE sm_rep ;"
    deleteRun=db.executesql(deleteStr)
    
    insStr="INSERT INTO  sm_rep (id,rep_id,name,cid,password,user_type,status,mobile_no) SELECT id,EMP_CODE,EMP_OFFICE_NAME,'"+'KPL'+"','"+'1234'+"','"+'rep'+"','"+'INACTIVE'+"','"+'0'+"' FROM  zkpl_pmis_emp GROUP BY id;"


    insRun=db.executesql(insStr)
    return 'Success'


def sm_repam_update(): 

    insStr="""UPDATE sm_rep r ,zkpl_sd_am a set r.user_type='"""+'sup'+"""'  where r.rep_id=a.EMPNO """
    
   
    db.executesql(insStr)
      
    insStrMob="""UPDATE sm_rep r ,zkpl_sd_am a set r.mobile_no=concat('88',a.MOB_PHONE ) , r.status='ACTIVE'  where r.rep_id=a.EMPNO and a.MOB_PHONE!='None'"""  
    db.executesql(insStrMob)
    
    
      
    return 'Success'

def sm_reprm_update(): 

    insStr="""UPDATE sm_rep r ,zkpl_sd_rm rm set r.user_type='"""+'sup'+"""'  where r.rep_id=rm.EMPNO """
    
   
    db.executesql(insStr)
    
    
    insStrMob="""UPDATE sm_rep r ,zkpl_sd_rm rm set r.mobile_no=concat('88',rm.MOB_PHONE )  , r.status='ACTIVE'  where r.rep_id=rm.EMPNO and rm.MOB_PHONE!='None'"""  
    db.executesql(insStrMob)
    return 'Success'


def sm_repfm_update(): 

    insStr="""UPDATE sm_rep r ,zkpl_sd_fm fm set r.user_type='"""+'sup'+"""'  where r.rep_id=fm.EMPNO """
    
   
    db.executesql(insStr)
      
    insStrMob="""UPDATE sm_rep r ,zkpl_sd_fm fm set r.mobile_no=concat('88',fm.MOB_PHONE )  , r.status='ACTIVE'  where r.rep_id=fm.EMPNO and fm.MOB_PHONE!='None'"""  
    db.executesql(insStrMob)  
    
    return 'Success'


def sm_repmpo_update(): 
      
    insStrMob="""UPDATE sm_rep r ,zkpl_sd_mpo mpo set r.mobile_no=concat('88',mpo.MOB_PHONE )  , r.status='ACTIVE'  where r.rep_id=mpo.EMPNO and mpo.MOB_PHONE!='None'"""  
    db.executesql(insStrMob)  
    
    return 'Success'
#===== sm_rep end ======





#===== sm_supervisor_level ======

def sm_supervisor_levelam_insert():
    
    deleteStr="TRUNCATE sm_supervisor_level ;"
    deleteRun=db.executesql(deleteStr)
    
    insStr="INSERT INTO  sm_supervisor_level (id,sup_id,level_id,level_name,cid,level_depth_no) SELECT id,EMPNO,AM_CODE,AM_AREA,'"+'KPL'+"','"+'0'+"' FROM zkpl_sd_am GROUP BY id;"

    insRun=db.executesql(insStr)
    return 'Success'


def sm_supervisor_levelrm_insert():
   
    
    insStr="INSERT INTO  sm_supervisor_level (id,sup_id,level_id,level_name,cid,level_depth_no) SELECT id,EMPNO,RM_CODE,REGION,'"+'KPL'+"','"+'1'+"' FROM  zkpl_sd_rm GROUP BY id;"

    insRun=db.executesql(insStr)
    return 'Success'


def sm_supervisor_levelfm_insert():
   
    
    insStr="INSERT INTO  sm_supervisor_level (id,sup_id,level_id,level_name,cid,level_depth_no) SELECT id,EMPNO,FM_CODE,FM_AREA,'"+'KPL'+"','"+'2'+"' FROM  zkpl_sd_fm GROUP BY id;"

    insRun=db.executesql(insStr)
    return 'Success'




def sm_supervisor_level_update(): 
 
    insStr="""UPDATE sm_supervisor_level l , zkpl_pmis_emp e set l.sup_name=e.EMP_OFFICE_NAME  where l.sup_id=e.EMP_CODE """
    
    db.executesql(insStr)
       
    return 'Success'



#======   rep_area   ====

def sm_rep_area_insert():
      
    deleteStr="TRUNCATE sm_rep_area ;"
    deleteRun=db.executesql(deleteStr)
      
    insStr="INSERT INTO  sm_rep_area (id,rep_id,area_id,area_name,cid,rep_category) SELECT id,EMPNO,MPO_CODE,TERRI_NAME,'"+'KPL'+"','"+'A'+"' FROM zkpl_sd_mpo GROUP BY id;"
  
    insRun=db.executesql(insStr)
    return 'Success'


def sm_rep_area_update(): 
 
    insStr="""UPDATE sm_rep_area r , zkpl_pmis_emp e set r.rep_name=e.EMP_OFFICE_NAME  where r.rep_id=e.EMP_CODE """
    
    db.executesql(insStr)
       
    return 'Success'

#===== sm_supervisor_end ======


# ==========rep syncode and password update==============
def update_sm_rep():    
     
    zkplupdate="""UPDATE  sm_rep r, z_kpl_backup z set r.password=z.password, r.sync_code=z.sync_code  where r.rep_id=z.rep_id"""
    insRun=db.executesql(zkplupdate)
     
    return 'Success'

# ===================================================



# ===================Shima======================

def sm_doc_insert(): 
    deleteStr="TRUNCATE sm_doctor ;"
    deleteRun=db.executesql(deleteStr)
    
    insStr="INSERT INTO  sm_doctor (cid,doc_id,doc_name,degree,specialty,mobile,service_kol_dsc,status,created_on,updated_on,doctors_category) SELECT '"+'KPL'+"', DOC_CODE,DOC_NAME,DOC_DEGREE,DOC_SPCL,DOC_MOBILE,NOF_PAT,'"+'ACTIVE'+"',ENTER_DT,ENTER_DT,BENEFIT_CAT FROM  zkpl_doctor GROUP BY DOC_CODE;"
    insRun=db.executesql(insStr)
    return 'Success'

def sm_doc_area_insert(): 
    deleteStr="TRUNCATE sm_doctor_area ;"
    deleteRun=db.executesql(deleteStr)
    
    insStr="INSERT INTO  sm_doctor_area (cid,doc_id,doc_name,area_id,field1,address,status) SELECT '"+'KPL'+"',DOC_CODE,DOC_NAME,MPO_CODE,MPO_CODE,DOC_ADDR,'"+'ACTIVE'+"' FROM  zkpl_doctor GROUP BY DOC_CODE;"
    insRun=db.executesql(insStr)
    return 'Success'

def sm_doc_area_update():     
    insStrUpdateDN="""UPDATE  sm_doctor_area d, sm_level l set d.area_name=l.level_name,d.note=l.level_name  where d.area_id=l.level_id and l.is_leaf='1'"""
    insRun=db.executesql(insStrUpdateDN)
    return 'Success'

def sm_microunion_insert():    
    deleteStr="TRUNCATE sm_microunion ;"
    deleteRun=db.executesql(deleteStr)
    
    insStr="INSERT INTO  sm_microunion (cid,microunion_id,microunion_name,area_id,area_name) SELECT cid,area_id,area_name,area_id,area_name FROM sm_doctor_area GROUP BY doc_id;"
    insRun=db.executesql(insStr)
    return 'Success'


# ====================ShimaEnd========================









def set_product_list():
    
    cid = 'KPL'
    #     Special rate==================
    itemBonusList = []
    itemBonusList_str = []
    itemBonusRows = db((db.sm_promo_product_bonus_products.cid == cid) & (db.sm_promo_product_bonus_products.status == 'ACTIVE') & (db.sm_promo_product_bonus_products.from_date <= current_date)  & (db.sm_promo_product_bonus_products.to_date >= current_date) ).select(db.sm_promo_product_bonus_products.product_id,db.sm_promo_product_bonus_products.product_name, db.sm_promo_product_bonus_products.note, orderby=db.sm_promo_product_bonus_products.product_name)
    for itemBonusRows in itemBonusRows:
        product_id = itemBonusRows.product_id       
        note= itemBonusRows.note
        itemBonusList.append(str(product_id))
        itemBonusList_str.append(note)
        
#     Special rate==================
    itemSpecialList = []
    itemSpecialList_str = []
    itemSpecialRows = db((db.sm_promo_special_rate.cid == cid) & (db.sm_promo_special_rate.status == 'ACTIVE')  & (db.sm_promo_special_rate.from_date <= current_date)  & (db.sm_promo_special_rate.to_date >= current_date) ).select(db.sm_promo_special_rate.product_id,db.sm_promo_special_rate.product_name, db.sm_promo_special_rate.special_rate_tp, db.sm_promo_special_rate.special_rate_vat, db.sm_promo_special_rate.min_qty, orderby=db.sm_promo_special_rate.product_name)
    for itemSpecialRows in itemSpecialRows:
        
        product_id = itemSpecialRows.product_id       
        special_rate_tp = itemSpecialRows.special_rate_tp
        special_rate_vat = itemSpecialRows.special_rate_vat
        min_qty = itemSpecialRows.min_qty
#         return min_qty
        total= float(special_rate_tp)+float(special_rate_vat)
#         return total
        itemSpecialList.append(str(product_id))
#         itemSpecialList_str.append('Special:Min '+str(min_qty)+' TP ' +str(special_rate_tp)+' Vat'+str(special_rate_vat)+'='+str(total))
        itemSpecialList_str.append('Special:Min '+str(min_qty)+' CPP ' +str(total))
         

#     Flat rate==================
    itemFlatList = []
    itemFlatList_str = []
    itemFlatRows = db((db.sm_promo_flat_rate.cid == cid)  & (db.sm_promo_flat_rate.status == 'ACTIVE') & (db.sm_promo_flat_rate.from_date <= current_date)  & (db.sm_promo_flat_rate.to_date >= current_date) ).select(db.sm_promo_flat_rate.product_id,db.sm_promo_flat_rate.product_name, db.sm_promo_flat_rate.min_qty, db.sm_promo_flat_rate.flat_rate,db.sm_promo_flat_rate.vat, orderby=db.sm_promo_flat_rate.product_name)
    for itemFlatRows in itemFlatRows:
        product_id = itemFlatRows.product_id
        product_name = itemFlatRows.product_name
        flat_rate = float(itemFlatRows.flat_rate)+float(itemFlatRows.vat)
        
        min_qty = itemFlatRows.min_qty      
        itemFlatList.append(str(product_id))
        itemFlatList_str.append('Flat:Min '+str(min_qty)+' Rate '+str(flat_rate))
    
    
    
    productStr = ''
    productRows = db((db.sm_item.cid == cid) & (db.sm_item.status == 'ACTIVE') & (db.sm_item.category_id != 'BONUS')).select(db.sm_item.item_id, db.sm_item.name, db.sm_item.price, db.sm_item.vat_amt, orderby=db.sm_item.name)
    
    for productRow in productRows:
        item_id = productRow.item_id       
        name = str(productRow.name).replace(".","").replace(",","")
        price_amt = productRow.price
        vat_amt=productRow.vat_amt
        price_get=float(price_amt)+float(vat_amt)
        price=round(price_get, 2)
        
#         recRow=''
        recRow_str=''
        
        
#         ===========Bonus Rate
        recRowBonus=''
        recRowBonus_str=''
        if [s for s in itemBonusList if item_id in s]:
            index_element = itemBonusList.index(item_id)           
            recRowBonus=itemBonusList[index_element]
            recRowBonus_str=itemBonusList_str[index_element]
            recRowBonus_str=str(recRowBonus_str)+'&nbsp;'
#             return recRowBonus_str
#         ===========Special Rate
        recRowSpecial=''
        recRowSpecial_str=''
        if [s for s in itemSpecialList if item_id in s]:
            index_element = itemSpecialList.index(item_id)           
            recRowSpecial=itemSpecialList[index_element]
            recRowSpecial_str=itemSpecialList_str[index_element]
            recRowSpecial_str=str(recRowSpecial_str)+'&nbsp;'
        
#             ============Flat Rate
        recRowFlat=''
        recRowFlat_str=''
        if [f for f in itemFlatList if item_id in f]:
            index_element = itemFlatList.index(item_id)                        
            recRowFlat=itemFlatList[index_element]
            recRowFlat_str=itemFlatList_str[index_element]
            recRowFlat_str=str(recRowFlat_str)+'&nbsp;'


#             ============Product Bonus
        
        recRowFlat=''
        recRowFlat_str=''
        if [f for f in itemFlatList if item_id in f]:
            index_element = itemFlatList.index(item_id)                        
            recRowFlat=itemFlatList[index_element]
            recRowFlat_str=itemFlatList_str[index_element]
            recRowFlat_str=str(recRowFlat_str)+'&nbsp;'
            
        recRow_str= recRowBonus_str+recRowSpecial_str+ recRowFlat_str     
        
        if productStr == '':
            productStr = str(item_id) + '<fd>' + str(name) + '<fd>' + str(price) + '<fd>' + str(recRow_str)+'<fd>'+str(vat_amt)
        else:
            productStr += '<rd>' + str(item_id) + '<fd>' + str(name) + '<fd>' + str(price) + '<fd>' + str(recRow_str)+'<fd>'+str(vat_amt)
     
#     return productStr
    item_update=db((db.sm_company_settings.cid==cid)).update(field1=productStr)
    
    if (item_update>0):
        return 'Successfully Prepared'  
#         session.flash='Successfully Prepared'      
        
# =============Prescription

def set_prescription_list():
    
    c_id = 'KPL'

    
    productStr_A = ''
    recordstring_A="SELECT item_id,name FROM `sm_item` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'A%' ORDER BY `name` ASC"
    records_A=db.executesql(recordstring_A,as_dict = True) 
    for records_A in records_A:
        item_id_A = records_A['item_id']       
        name_A = str(records_A['name']).replace(".","").replace(",","")
        if productStr_A == '':
            productStr_A = str(item_id_A) + '<fd>' + str(name_A) 
        else:
            productStr_A += '<rd>' + str(item_id_A) + '<fd>' + str(name_A) 
    productStr_A='<ASTART>'+productStr_A+'<AEND>' 


    productStr_B = ''
    recordstring_B="SELECT * FROM `sm_item` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'B%' ORDER BY `name` ASC"
    records_B=db.executesql(recordstring_B,as_dict = True) 
    for records_B in records_B:
        item_id_B = records_B['item_id']     
        name_B = str(records_B['name']).replace(".","").replace(",","")
        if productStr_B == '':
            productStr_B = str(item_id_B) + '<fd>' + str(name_B) 
        else:
            productStr_B += '<rd>' + str(item_id_B) + '<fd>' + str(name_B) 
    productStr_B='<BSTART>'+productStr_B+'<BEND>' 
    
    productStr_C = ''
    recordstring_C="SELECT * FROM `sm_item` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'C%' ORDER BY `name` ASC"
    records_C=db.executesql(recordstring_C,as_dict = True) 
    for records_C in records_C:
        item_id_C = records_C['item_id']     
        name_C = str(records_C['name']).replace(".","").replace(",","")
        if productStr_C == '':
            productStr_C = str(item_id_C) + '<fd>' + str(name_C) 
        else:
            productStr_C += '<rd>' + str(item_id_C) + '<fd>' + str(name_C) 
    productStr_C='<CSTART>'+productStr_C+'<CEND>' 
#     return recordstring_C
    productStr_D = ''
    recordstring_D="SELECT * FROM `sm_item` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'D%' ORDER BY `name` ASC"
    records_D=db.executesql(recordstring_D,as_dict = True) 
    for records_D in records_D:
        item_id_D = records_D['item_id']     
        name_D = str(records_D['name']).replace(".","").replace(",","")
        if productStr_D == '':
            productStr_D = str(item_id_D) + '<fd>' + str(name_D) 
        else:
            productStr_D += '<rd>' + str(item_id_D) + '<fd>' + str(name_D) 
    productStr_D='<DSTART>'+productStr_D+'<DEND>'
    
    productStr_E = ''
    recordstring_E="SELECT * FROM `sm_item` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'E%' ORDER BY `name` ASC"
    records_E=db.executesql(recordstring_E,as_dict = True) 
    for records_E in records_E:
        item_id_E = records_E['item_id']     
        name_E = str(records_E['name']).replace(".","").replace(",","")
        if productStr_E == '':
            productStr_E = str(item_id_E) + '<fd>' + str(name_E) 
        else:
            productStr_E += '<rd>' + str(item_id_E) + '<fd>' + str(name_E) 
    productStr_E='<ESTART>'+productStr_E+'<EEND>'
    
    productStr_F = ''
    recordstring_F="SELECT * FROM `sm_item` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'F%' ORDER BY `name` ASC"
    records_F=db.executesql(recordstring_F,as_dict = True) 
    for records_F in records_F:
        item_id_F = records_F['item_id']     
        name_F = str(records_F['name']).replace(".","").replace(",","")
        if productStr_F == '':
            productStr_F = str(item_id_F) + '<fd>' + str(name_F) 
        else:
            productStr_F += '<rd>' + str(item_id_F) + '<fd>' + str(name_F) 
    productStr_F='<FSTART>'+productStr_F+'<FEND>'
    
    productStr_G = ''
    recordstring_G="SELECT * FROM `sm_item` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'G%' ORDER BY `name` ASC"
    records_G=db.executesql(recordstring_G,as_dict = True) 
    for records_G in records_G:
        item_id_G = records_G['item_id']     
        name_G = str(records_G['name']).replace(".","").replace(",","")
        if productStr_G == '':
            productStr_G = str(item_id_G) + '<fd>' + str(name_G) 
        else:
            productStr_G += '<rd>' + str(item_id_G) + '<fd>' + str(name_G) 
    productStr_G='<GSTART>'+productStr_G+'<GEND>'
    
    productStr_H = ''
    recordstring_H="SELECT * FROM `sm_item` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'H%' ORDER BY `name` ASC"
    records_H=db.executesql(recordstring_H,as_dict = True) 
    for records_H in records_H:
        item_id_H = records_H['item_id']     
        name_H = str(records_H['name']).replace(".","").replace(",","")
        if productStr_H == '':
            productStr_H = str(item_id_H) + '<fd>' + str(name_H) 
        else:
            productStr_H += '<rd>' + str(item_id_H) + '<fd>' + str(name_H) 
    productStr_H='<HSTART>'+productStr_H+'<HEND>'
    
    productStr_I = ''
    recordstring_I="SELECT * FROM `sm_item` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'I%' ORDER BY `name` ASC"
    records_I=db.executesql(recordstring_I,as_dict = True) 
    for records_I in records_I:
        item_id_I = records_I['item_id']     
        name_I = str(records_I['name']).replace(".","").replace(",","")
        if productStr_I == '':
            productStr_I = str(item_id_I) + '<fd>' + str(name_I) 
        else:
            productStr_I += '<rd>' + str(item_id_I) + '<fd>' + str(name_I) 
    productStr_I='<ISTART>'+productStr_I+'<IEND>'
    
    productStr_J = ''
    recordstring_J="SELECT * FROM `sm_item` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'J%' ORDER BY `name` ASC"
    records_J=db.executesql(recordstring_J,as_dict = True) 
    for records_J in records_J:
        item_id_J = records_J['item_id']     
        name_J = str(records_J['name']).replace(".","").replace(",","")
        if productStr_J == '':
            productStr_J = str(item_id_J) + '<fd>' + str(name_J) 
        else:
            productStr_J += '<rd>' + str(item_id_J) + '<fd>' + str(name_J) 
    productStr_J='<JSTART>'+productStr_J+'<JEND>'
    
    productStr_K = ''
    recordstring_K="SELECT * FROM `sm_item` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'K%' ORDER BY `name` ASC"
    records_K=db.executesql(recordstring_K,as_dict = True) 
    for records_K in records_K:
        item_id_K = records_K['item_id']     
        name_K = str(records_K['name']).replace(".","").replace(",","")
        if productStr_K == '':
            productStr_K = str(item_id_K) + '<fd>' + str(name_K) 
        else:
            productStr_K += '<rd>' + str(item_id_K) + '<fd>' + str(name_K) 
    productStr_K='<KSTART>'+productStr_K+'<KEND>'
#     return productStr_K
    productStr_L = ''
    recordstring_L="SELECT * FROM `sm_item` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'L%' ORDER BY `name` ASC"
    records_L=db.executesql(recordstring_L,as_dict = True) 
    for records_L in records_L:
        item_id_L = records_L['item_id']     
        name_L = str(records_L['name']).replace(".","").replace(",","")
        if productStr_L == '':
            productStr_L = str(item_id_L) + '<fd>' + str(name_L) 
        else:
            productStr_L += '<rd>' + str(item_id_L) + '<fd>' + str(name_L) 
    productStr_L='<LSTART>'+productStr_L+'<LEND>'
    
    productStr_M = ''
    recordstring_M="SELECT * FROM `sm_item` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'M%' ORDER BY `name` ASC"
    records_M=db.executesql(recordstring_M,as_dict = True) 
    for records_M in records_M:
        item_id_M = records_M['item_id']     
        name_M = str(records_M['name']).replace(".","").replace(",","")
        if productStr_M == '':
            productStr_M = str(item_id_M) + '<fd>' + str(name_M) 
        else:
            productStr_M += '<rd>' + str(item_id_M) + '<fd>' + str(name_M) 
    productStr_M='<MSTART>'+productStr_M+'<MEND>'
    
    productStr_N = ''
    recordstring_N="SELECT * FROM `sm_item` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'N%' ORDER BY `name` ASC"
    records_N=db.executesql(recordstring_N,as_dict = True) 
    for records_N in records_N:
        item_id_N = records_N['item_id']     
        name_N = str(records_N['name']).replace(".","").replace(",","")
        if productStr_N == '':
            productStr_N = str(item_id_N) + '<fd>' + str(name_N) 
        else:
            productStr_N += '<rd>' + str(item_id_N) + '<fd>' + str(name_N) 
    productStr_N='<NSTART>'+productStr_N+'<NEND>'
    
    productStr_O = ''
    recordstring_O="SELECT * FROM `sm_item` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'O%' ORDER BY `name` ASC"
    records_O=db.executesql(recordstring_O,as_dict = True) 
    for records_O in records_O:
        item_id_O = records_O['item_id']     
        name_O = str(records_O['name']).replace(".","").replace(",","")
        if productStr_O == '':
            productStr_O = str(item_id_O) + '<fd>' + str(name_O) 
        else:
            productStr_O += '<rd>' + str(item_id_O) + '<fd>' + str(name_O) 
    productStr_O='<OSTART>'+productStr_O+'<OEND>'
    
    productStr_P = ''
    recordstring_P="SELECT * FROM `sm_item` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'P%' ORDER BY `name` ASC"
    records_P=db.executesql(recordstring_P,as_dict = True) 
    for records_P in records_P:
        item_id_P = records_P['item_id']     
        name_P = str(records_P['name']).replace(".","").replace(",","")
        if productStr_P == '':
            productStr_P = str(item_id_P) + '<fd>' + str(name_P) 
        else:
            productStr_P += '<rd>' + str(item_id_P) + '<fd>' + str(name_P) 
    productStr_P='<PSTART>'+productStr_P+'<PEND>'
    
    productStr_Q = ''
    recordstring_Q="SELECT * FROM `sm_item` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'Q%' ORDER BY `name` ASC"
    records_Q=db.executesql(recordstring_Q,as_dict = True) 
    for records_Q in records_Q:
        item_id_Q = records_Q['item_id']     
        name_Q = str(records_Q['name']).replace(".","").replace(",","")
        if productStr_Q == '':
            productStr_Q = str(item_id_Q) + '<fd>' + str(name_Q) 
        else:
            productStr_Q += '<rd>' + str(item_id_Q) + '<fd>' + str(name_Q) 
    productStr_Q='<QSTART>'+productStr_Q+'<QEND>'
    
    productStr_R = ''
    recordstring_R="SELECT * FROM `sm_item` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'R%' ORDER BY `name` ASC"
    records_R=db.executesql(recordstring_R,as_dict = True) 
    for records_R in records_R:
        item_id_R = records_R['item_id']     
        name_R = str(records_R['name']).replace(".","").replace(",","")
        if productStr_R == '':
            productStr_R = str(item_id_R) + '<fd>' + str(name_R) 
        else:
            productStr_R += '<rd>' + str(item_id_R) + '<fd>' + str(name_R) 
    productStr_R='<RSTART>'+productStr_R+'<REND>'
    
    productStr_S = ''
    recordstring_S="SELECT * FROM `sm_item` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'S%' ORDER BY `name` ASC"
    records_S=db.executesql(recordstring_S,as_dict = True) 
    for records_S in records_S:
        item_id_S = records_S['item_id']     
        name_S = str(records_S['name']).replace(".","").replace(",","")
        if productStr_S == '':
            productStr_S = str(item_id_S) + '<fd>' + str(name_S) 
        else:
            productStr_S += '<rd>' + str(item_id_S) + '<fd>' + str(name_S) 
    productStr_S='<SSTART>'+productStr_S+'<SEND>'
    
    productStr_T = ''
    recordstring_T="SELECT * FROM `sm_item` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'T%' ORDER BY `name` ASC"
    records_T=db.executesql(recordstring_T,as_dict = True) 
    for records_T in records_T:
        item_id_T = records_T['item_id']     
        name_T = str(records_T['name']).replace(".","").replace(",","")
        if productStr_T == '':
            productStr_T = str(item_id_T) + '<fd>' + str(name_T) 
        else:
            productStr_T += '<rd>' + str(item_id_T) + '<fd>' + str(name_T) 
    productStr_T='<TSTART>'+productStr_T+'<TEND>'
    
    productStr_U = ''
    recordstring_U="SELECT * FROM `sm_item` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'U%' ORDER BY `name` ASC"
    records_U=db.executesql(recordstring_U,as_dict = True) 
    for records_U in records_U:
        item_id_U = records_U['item_id']     
        name_U = str(records_U['name']).replace(".","").replace(",","")
        if productStr_U == '':
            productStr_U = str(item_id_U) + '<fd>' + str(name_U) 
        else:
            productStr_U += '<rd>' + str(item_id_U) + '<fd>' + str(name_U) 
    productStr_U='<USTART>'+productStr_U+'<UEND>'
    
    productStr_V = ''
    recordstring_V="SELECT * FROM `sm_item` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'V%' ORDER BY `name` ASC"
    records_V=db.executesql(recordstring_V,as_dict = True) 
    for records_V in records_V:
        item_id_V = records_V['item_id']     
        name_V = str(records_V['name']).replace(".","").replace(",","")
        if productStr_V == '':
            productStr_V = str(item_id_V) + '<fd>' + str(name_V) 
        else:
            productStr_V += '<rd>' + str(item_id_V) + '<fd>' + str(name_V) 
    productStr_V='<VSTART>'+productStr_V+'<VEND>'
    
    productStr_W = ''
    recordstring_W="SELECT * FROM `sm_item` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'W%' ORDER BY `name` ASC"
    records_W=db.executesql(recordstring_W,as_dict = True) 
    for records_W in records_W:
        item_id_W = records_W['item_id']     
        name_W = str(records_W['name']).replace(".","").replace(",","")
        if productStr_W == '':
            productStr_W = str(item_id_W) + '<fd>' + str(name_W) 
        else:
            productStr_W += '<rd>' + str(item_id_W) + '<fd>' + str(name_W) 
    productStr_W='<WSTART>'+productStr_W+'<WEND>'
    
    productStr_X = ''
    recordstring_X="SELECT * FROM `sm_item` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'X%' ORDER BY `name` ASC"
    records_X=db.executesql(recordstring_X,as_dict = True) 
    for records_X in records_X:
        item_id_X = records_X['item_id']     
        name_X = str(records_X['name']).replace(".","").replace(",","")
        if productStr_X == '':
            productStr_X = str(item_id_X) + '<fd>' + str(name_X) 
        else:
            productStr_X += '<rd>' + str(item_id_X) + '<fd>' + str(name_X) 
    productStr_X='<XSTART>'+productStr_X+'<XEND>'
    
    productStr_Y = ''
    recordstring_Y="SELECT * FROM `sm_item` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'Y%' ORDER BY `name` ASC"
    records_Y=db.executesql(recordstring_Y,as_dict = True) 
    for records_Y in records_Y:
        item_id_Y = records_Y['item_id']     
        name_Y = str(records_Y['name']).replace(".","").replace(",","")
        if productStr_Y == '':
            productStr_Y = str(item_id_Y) + '<fd>' + str(name_Y) 
        else:
            productStr_Y += '<rd>' + str(item_id_Y) + '<fd>' + str(name_Y) 
    productStr_Y='<YSTART>'+productStr_Y+'<YEND>'
    
    productStr_Z = ''
    recordstring_Z="SELECT * FROM `sm_item` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'Z%' ORDER BY `name` ASC"
    records_Z=db.executesql(recordstring_Z,as_dict = True) 
    for records_Z in records_Z:
        item_id_Z = records_Z['item_id']     
        name_Z = str(records_Z['name']).replace(".","").replace(",","")
        if productStr_Z == '':
            productStr_Z = str(item_id_Z) + '<fd>' + str(name_Z) 
        else:
            productStr_Z += '<rd>' + str(item_id_Z) + '<fd>' + str(name_Z) 
    productStr_Z='<ZSTART>'+productStr_Z+'<ZEND>'
    
    
    
    productStr=productStr_A+productStr_B+productStr_C+productStr_D+productStr_E+productStr_F+productStr_G+productStr_H+productStr_I+productStr_J+productStr_K+productStr_L+productStr_M+productStr_N+productStr_O+productStr_P+productStr_Q+productStr_R+productStr_S+productStr_T+productStr_U+productStr_V+productStr_W+productStr_X+productStr_Y+productStr_Z
    
#     return productStr
    
           
    item_update=db((db.sm_company_settings.cid==c_id)).update(item_list_mobile=productStr)
    
    if (item_update>0):
        return 'Successfully Prepared'        
#     else:
#         session.flash='Error in process'
#                  
#     redirect (URL('utility_mrep','utility_settings'))



# =========================

def sm_doctor_gift_insert(): 
    
    deleteStr="TRUNCATE sm_doctor_gift ;"
    deleteRun=db.executesql(deleteStr)
    
    insStr="INSERT INTO sm_doctor_gift (cid, gift_id, gift_name, des, STATUS) SELECT 'KPL' AS cid, P_CODE, P_DESC, CONCAT( PACK_SIZE, '_', CC_SIZE) AS DES, 'ACTIVE' AS STATUS FROM zkpl_sample_product WHERE SAMP_TYPE ='G';"

    insRun=db.executesql(insStr)
    return 'Success'



def sm_doctor_ppm_insert(): 
    
    deleteStr="TRUNCATE sm_doctor_ppm ;"
    deleteRun=db.executesql(deleteStr)
    
    insStr="INSERT INTO sm_doctor_ppm (cid, gift_id, gift_name, des, STATUS) SELECT 'KPL' AS cid, P_CODE, P_DESC, CONCAT( PACK_SIZE, '_', CC_SIZE) AS DES, 'ACTIVE' AS STATUS FROM zkpl_sample_product WHERE SAMP_TYPE ='P'"

    insRun=db.executesql(insStr)
    return 'Success'


def sm_doctor_sample_insert(): 
    
    deleteStr="TRUNCATE sm_doctor_sample ;"
    deleteRun=db.executesql(deleteStr)
    
    insStr="INSERT INTO sm_doctor_sample (cid, item_id, NAME, des, STATUS) SELECT 'KPL' AS cid, P_CODE, P_DESC, CONCAT( PACK_SIZE, '_', CC_SIZE) AS DES, 'ACTIVE' AS STATUS FROM zkpl_sample_product WHERE SAMP_TYPE ='S'"

    insRun=db.executesql(insStr)
    return 'Success'







# Sample===========================================

def set_sample_list():
    
    cid = 'KPL'
    #     Special rate==================
    productStr=''
    itemBonusRows = db((db.sm_doctor_sample.cid == cid) & (db.sm_doctor_sample.status == 'ACTIVE') ).select(db.sm_doctor_sample.item_id,db.sm_doctor_sample.name, db.sm_doctor_sample.des, orderby=db.sm_doctor_sample.name)
    for itemBonusRows in itemBonusRows:
        item_id = itemBonusRows.item_id    
        name = itemBonusRows.name       
        des= itemBonusRows.des
        if productStr == '':
            productStr = str(item_id) + '<fd>' + str(name) + '<fd>' + str(des) 
        else:
            productStr = productStr+'<rd>' +str(item_id) + '<fd>' + str(name) + '<fd>' + str(des) 


    sample_update=db((db.sm_company_settings.cid==cid)).update(note=productStr)
    
    if (sample_update>0):
        return 'Successfully Prepared'  
    
    
  