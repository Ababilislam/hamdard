#level Transfer

#============================= 
def utility():
    task_id = 'rm_utility_manage'
    access_permission = check_role(task_id)
    if (access_permission == False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    response.title='Batch Process'
    c_id=session.cid
    
    #--------------------- 
    depot_transfer='NO'
    depot_settings_check=db((db.sm_settings.cid==c_id) & (db.sm_settings.s_key=='DEPOT_TRANSFER')).select(db.sm_settings.s_value,limitby=(0,1))
    for depot_settings_check in depot_settings_check :
        depot_transfer=depot_settings_check.s_value 
    
    
    #------------------ Show Last ID    
    showLastIDType=''
    showLastID=''
    
    #----------
    btn_show_lastID=request.vars.btn_show_lastID
    
    #---------------------
    if btn_show_lastID:
        showLastIDType=str(request.vars.showLastIDType).strip()
        if showLastIDType=='':
            response.title='Select Type'
        else:
            if showLastIDType=='DOCTOR':
                doctorRows=db(db.sm_doctor.cid==c_id).select(db.sm_doctor.doc_id,orderby=~db.sm_doctor.doc_id,limitby=(0,1))
                if doctorRows:
                    showLastID=doctorRows[0].doc_id
                    
            elif showLastIDType=='RETAILER':
                clientRows=db(db.sm_client.cid==c_id).select(db.sm_client.client_id,orderby=~db.sm_client.client_id,limitby=(0,1))
                if clientRows:
                    showLastID=clientRows[0].client_id
            
            elif showLastIDType=='REP':
                repRows=db((db.sm_rep.cid==c_id)&(db.sm_rep.user_type=='rep')).select(db.sm_rep.rep_id,orderby=~db.sm_rep.rep_id,limitby=(0,1))
                if repRows:
                    showLastID=repRows[0].rep_id
            
            elif showLastIDType=='SUPERVISOR':
                repRows=db((db.sm_rep.cid==c_id)&(db.sm_rep.user_type=='sup')).select(db.sm_rep.rep_id,orderby=~db.sm_rep.rep_id,limitby=(0,1))
                if repRows:
                    showLastID=repRows[0].rep_id
                    
    return dict(depot_transfer=depot_transfer,showLastIDType=showLastIDType,showLastID=showLastID,access_permission=access_permission)


def utility_settings():
    task_id = 'rm_utility_manage'
    access_permission = check_role(task_id)
    if (access_permission == False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    response.title='Utility'
    c_id=session.cid
    
    #--------------------- 
    depot_transfer='NO'
    depot_settings_check=db((db.sm_settings.cid==c_id) & (db.sm_settings.s_key=='DEPOT_TRANSFER')).select(db.sm_settings.s_value,limitby=(0,1))
    for depot_settings_check in depot_settings_check :
        depot_transfer=depot_settings_check.s_value 
    
    
    #------------------ Show Last ID    
    showLastIDType=''
    showLastID=''
    
    #----------
    btn_show_lastID=request.vars.btn_show_lastID
    
    #---------------------
    if btn_show_lastID:
        showLastIDType=str(request.vars.showLastIDType).strip()
        if showLastIDType=='':
            response.title='Select Type'
        else:
            if showLastIDType=='DOCTOR':
                doctorRows=db(db.sm_doctor.cid==c_id).select(db.sm_doctor.doc_id,orderby=~db.sm_doctor.doc_id,limitby=(0,1))
                if doctorRows:
                    showLastID=doctorRows[0].doc_id
                    
            elif showLastIDType=='RETAILER':
                clientRows=db(db.sm_client.cid==c_id).select(db.sm_client.client_id,orderby=~db.sm_client.client_id,limitby=(0,1))
                if clientRows:
                    showLastID=clientRows[0].client_id
            
            elif showLastIDType=='REP':
                repRows=db((db.sm_rep.cid==c_id)&(db.sm_rep.user_type=='rep')).select(db.sm_rep.rep_id,orderby=~db.sm_rep.rep_id,limitby=(0,1))
                if repRows:
                    showLastID=repRows[0].rep_id
            
            elif showLastIDType=='SUPERVISOR':
                repRows=db((db.sm_rep.cid==c_id)&(db.sm_rep.user_type=='sup')).select(db.sm_rep.rep_id,orderby=~db.sm_rep.rep_id,limitby=(0,1))
                if repRows:
                    showLastID=repRows[0].rep_id
                    
    return dict(depot_transfer=depot_transfer,showLastIDType=showLastIDType,showLastID=showLastID,access_permission=access_permission)
    

    
    
def level_transfer(): 
    
    #----------
    response.title='Level Transfer'
    
    #----------
    btn_transfer=request.vars.btn_transfer
    checkbox=request.vars.checkbox
    if btn_transfer and checkbox==None:
        session.flash='Please Confirm First'  
        
    if btn_transfer and checkbox!=None:
#        return checkbox
        level_id=str(request.vars.level_id).strip().upper()
        under_level_id=str(request.vars.under_level_id).strip().upper()
#        return level_id
        if ((level_id != '') and (under_level_id != '')):
            level_check=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id==level_id)).select(db.sm_level.ALL,limitby=(0,1))
            under_level_check=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id==under_level_id)).select(db.sm_level.ALL,limitby=(0,1))
#            return level_check
            if (under_level_check):
                under_level_name=under_level_check[0].level_name
                
            if (level_check):
                level_name=level_check[0].level_name
                
                
            if (level_check and under_level_check):
                for level_check in level_check :
                    depth_level=level_check.depth  
                    
                    level0_level=level_check.level0
                    level1_level=level_check.level1 
                    level2_level=level_check.level2 
                    level3_level=level_check.level3 
                    level4_level=level_check.level4  
                    level5_level=level_check.level5 
                    level6_level=level_check.level6 
                    level7_level=level_check.level7 
                    level8_level=level_check.level8
                    
                    level0_level_name=level_check.level0_name
                    level1_level_name=level_check.level1_name
                    level2_level_name=level_check.level2_name
                    level3_level_name=level_check.level3_name
                    level4_level_name=level_check.level4_name 
                    level5_level_name=level_check.level5_name
                    level6_level_name=level_check.level6_name
                    level7_level_name=level_check.level7_name
                    level8_level_name=level_check.level8_name 
                                 
                for under_level_check in under_level_check :
                    depth_under_level=under_level_check.depth  
#                    parent_level=under_level_check.parent_level_id
                    level0_under_level=under_level_check.level0
                    level1_under_level=under_level_check.level1 
                    level2_under_level=under_level_check.level2 
                    level3_under_level=under_level_check.level3 
                    level4_under_level=under_level_check.level4  
                    level5_under_level=under_level_check.level5 
                    level6_under_level=under_level_check.level6 
                    level7_under_level=under_level_check.level7 
                    level8_under_level=under_level_check.level8 
                    
                    level0_under_level_name=under_level_check.level0_name
                    level1_under_level_name=under_level_check.level1_name 
                    level2_under_level_name=under_level_check.level2_name 
                    level3_under_level_name=under_level_check.level3_name 
                    level4_under_level_name=under_level_check.level4_name  
                    level5_under_level_name=under_level_check.level5_name 
                    level6_under_level_name=under_level_check.level6_name 
                    level7_under_level_name=under_level_check.level7_name 
                    level8_under_level_name=under_level_check.level8_name
                    
#                return int(depth_level)
                if (int(depth_level)==int(depth_under_level)+1):
#                    return 'haha'
                    if (depth_level>0):
#                        return depth_level
                        if (depth_level==1):
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,parent_level_name=under_level_name,level0=level0_under_level,level0_name=level0_under_level_name)
#                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level)
#                            return db._lastsql
                           
                            
                            
                            
#                            child_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level1==level_id) ).update(level0=level0_under_level)
                            child_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level1==level_id) ).update(level0=level0_under_level,level0_name=level0_under_level_name)
                            
#                            return db._lastsql
                        if (depth_level==2):
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level, parent_level_name=under_level_id_name,level0_name=level0_under_level_name,level1_name=level1_under_level_name)
                            child_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level2==level_id) ).update(level0=level0_under_level,level1=level1_under_level, level0_name=level0_under_level_name,level1_name=level1_under_level_name)
                               
                        if (depth_level==3):
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level,level3=level3_under_level, parent_level_name=under_level_name,level0_name=level0_under_level_name,level1_name=level1_under_level_name,level3_name=level3_under_level_name)
                            child_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level3==level_id) ).update(level0=level0_under_level,level1=level1_under_level,level2=level2_under_level, level0_name=level0_under_level_name,level1_name=level1_under_level_name,level2_name=level2_under_level_name)
                                
                        if (depth_level==4):
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level,level3=level3_under_level, parent_level_name=under_level_name,level0_name=level0_under_level_name,level1_name=level1_under_level_name,level3_name=level3_under_level_name)
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level4 == level_id)).update(level0=level0_under_level,level1=level1_under_level,level2=level2_under_level,level3=level3_under_level, level0_name=level0_under_level_name,level1_name=level1_under_level_name,level2_name=level2_under_level_name,level3_name=level3_under_level_name)
                            
                        if (depth_level==5):
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level,level3=level3_under_level,level4=level4_under_level, parent_level_name=under_level_name_id,level0_name=level0_under_level_name,level1_name=level1_under_level_name,level3_name=level3_under_level_name,level4_name=level4_under_level_name)
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level5 == level_id)).update(level0=level0_under_level,level1=level1_under_level,level2=level2_under_level,level3=level3_under_level,level4=level4_under_level, level0_name=level0_under_level_name,level1_name=level1_under_level_name,level2_name=level2_under_level_name,level3_name=level3_under_level_name,level4_name=level4_under_level_name)
                            
                        if (depth_level==6):
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level,level3=level3_under_level,level4=level4_under_level,level5=level5_under_level, parent_level_name=under_level_name,level0_name=level0_under_level_name,level1_name=level1_under_level_name,level3_name=level3_under_level_name,level4_name=level4_under_level_name,level5_name=level5_under_level_name)
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level6 == level_id)).update(level0=level0_under_level,level1=level1_under_level,level2=level2_under_level,level3=level3_under_level,level4=level4_under_level,level5=level5_under_level, level0_name=level0_under_level_name,level1_name=level1_under_level_name,level2_name=level2_under_level_name,level3_name=level3_under_level_name,level4_name=level4_under_level_name,level5_name=level5_under_level_name)   
                        
                        if (depth_level==7):
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level,level3=level3_under_level,level4=level4_under_level,level5=level5_under_level,level6=level6_under_level, parent_level_name=under_level_name,level0_name=level0_under_level_name,level1_name=level1_under_level_name,level3_name=level3_under_level_name,level4_name=level4_under_level_name,level5_name=level5_under_level_name,level6_name=level6_under_level_name)
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level7 == level_id)).update(level0=level0_under_level,level1=level1_under_level,level2=level2_under_level,level3=level3_under_level,level4=level4_under_level,level5=level5_under_level,level6=level6_under_level, level0_name=level0_under_level_name,level1_name=level1_under_level_name,level2_name=level2_under_level_name,level3_name=level3_under_level_name,level4_name=level4_under_level_name,level5_name=level5_under_level_name,level6_name=level6_under_level_name)    
                        if (depth_level==8):
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level,level3=level3_under_level,level4=level4_under_level,level5=level5_under_level,level6=level6_under_level,level7=level7_under_level, parent_level_name=under_level_name,level0_name=level0_under_level_name,level1_name=level1_under_level_name,level3_name=level3_under_level_name,level4_name=level4_under_level_name,level5_name=level5_under_level_name,level6_name=level6_under_level_name,level7_name=level7_under_level_name)
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level8 == level_id)).update(level0=level0_under_level,level1=level1_under_level,level2=level2_under_level,level3=level3_under_level,level4=level4_under_level,level5=level5_under_level,level6=level6_under_level,level7=level7_under_level, level0_name=level0_under_level_name,level1_name=level1_under_level_name,level2_name=level2_under_level_name,level3_name=level3_under_level_name,level4_name=level4_under_level_name,level5_name=level5_under_level_name,level6_name=level6_under_level_name,level7_name=level7_under_level_name)
                               
#                        if (depth_level==2):
#                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level, parent_level_name=under_level_id_name,level0_name=level0_under_level_name,level1_name=level1_under_level_name)
#                            child_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level2==level_id) ).update(level0=level0_under_level,level1=level1_under_level, level0_name=level0_under_level_name,level1_name=level1_under_level_name)
##                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level)
##                            child_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level2==level_id) ).update(level0=level0_under_level,level1=level1_under_level)
#                               
#                        if (depth_level==3):
#                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level,level3=level3_under_level)
#                            child_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level3==level_id) ).update(level0=level0_under_level,level1=level1_under_level,level2=level2_under_level)
#                                
#                        if (depth_level==4):
#                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level,level3=level3_under_level)
#                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level4 == level_id)).update(level0=level0_under_level,level1=level1_under_level,level2=level2_under_level,level3=level3_under_level)
#                            
#                        if (depth_level==5):
#                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level,level3=level3_under_level,level4=level4_under_level)
#                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level5 == level_id)).update(level0=level0_under_level,level1=level1_under_level,level2=level2_under_level,level3=level3_under_level,level4=level4_under_level)
#                            
#                        if (depth_level==6):
#                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level,level3=level3_under_level,level4=level4_under_level,level5=level5_under_level)
#                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level6 == level_id)).update(level0=level0_under_level,level1=level1_under_level,level2=level2_under_level,level3=level3_under_level,level4=level4_under_level,level5=level5_under_level)   
#                        
#                        if (depth_level==7):
#                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level,level3=level3_under_level,level4=level4_under_level,level5=level5_under_level,level6=level6_under_level)
#                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level7 == level_id)).update(level0=level0_under_level,level1=level1_under_level,level2=level2_under_level,level3=level3_under_level,level4=level4_under_level,level5=level5_under_level,level6=level6_under_level)    
#                        if (depth_level==8):
#                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level,level3=level3_under_level,level4=level4_under_level,level5=level5_under_level,level6=level6_under_level,level7=level7_under_level)
#                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level8 == level_id)).update(level0=level0_under_level,level1=level1_under_level,level2=level2_under_level,level3=level3_under_level,level4=level4_under_level,level5=level5_under_level,level6=level6_under_level,level7=level7_under_level)
#                            
                        session.flash='Transfered Successfully'    
                    
                else:
                     session.flash='Please Check Area Properly'    
            else:
                session.flash='Please Check Area Properly'
        else:
            session.flash='Please Check Area Properly'          
    else:
        pass                
    
    redirect (URL('utility_mrep','utility'))
    
def depot_transfer(): 
    
    #----------
    response.title='Depot Transfer'
    
    #----------
    btn_transfer_depot=request.vars.btn_transfer_depot
    checkbox=request.vars.checkbox
    if btn_transfer_depot and checkbox==None:
        session.flash='Please Confirm First' 
        redirect (URL('utility_mrep','utility')) 
#    return 'nadira'    
    if btn_transfer_depot and checkbox!=None:
#        return checkbox
        depot_id=str(request.vars.depot_id).strip().upper()
        transfer_with_depot_id=str(request.vars.transfer_with_depot_id).strip().upper()
#        return 'level_id'
        if ((depot_id != '') and (transfer_with_depot_id != '')):
            if (depot_id==transfer_with_depot_id):
                session.flash='Please choose differnt depot ID for Transfer' 
                redirect (URL('utility_mrep','utility')) 
            depot_id_check=db((db.sm_depot.cid==session.cid) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.depot_category,limitby=(0,1))
            transfer_with_depot_id_check=db((db.sm_depot.cid==session.cid) & (db.sm_depot.depot_id==transfer_with_depot_id)).select(db.sm_depot.depot_category,limitby=(0,1))
#            return db._lastsql
            
            if (depot_id_check and transfer_with_depot_id_check):
                for depot_id_check in depot_id_check :
                    depot_id_check_catagory=depot_id_check.depot_category  
                    
                for transfer_with_depot_id_check in transfer_with_depot_id_check :
                    transfer_with_depot_id_check_catagory=transfer_with_depot_id_check.depot_category    
                
                if (depot_id_check_catagory == transfer_with_depot_id_check_catagory):  
                    # update client,rep,rep_area,level,depotsettings,--stockbalance    
                      client_update=db((db.sm_client.cid==session.cid) & (db.sm_client.depot_id == depot_id)).update(depot_id=transfer_with_depot_id)
                      rep_update=db((db.sm_rep.cid==session.cid) & (db.sm_rep.depot_id == depot_id)).update(depot_id=transfer_with_depot_id)
                      #rep_area_update=db((db.sm_rep_area.cid==session.cid) & (db.sm_rep_area.depot_id == depot_id)).update(depot_id=transfer_with_depot_id)
#                      return db._lastsql
                      
                      level_update=db((db.sm_level.cid==session.cid) & (db.sm_level.depot_id == depot_id)).update(depot_id=transfer_with_depot_id)
                      
                      # Update depot settings from and to
                      depot_settings_update=db((db.sm_depot_settings.cid==session.cid) & (db.sm_depot_settings.depot_id == depot_id)).update(depot_id=transfer_with_depot_id)
                      depot_settings_update=db((db.sm_depot_settings.cid==session.cid) & (db.sm_depot_settings.depot_id_from_to == depot_id)).update(depot_id_from_to=transfer_with_depot_id)
                      
                      # sm_depot_stock_balance
                      depot_settings_check=db((db.sm_settings.cid==session.cid) & (db.sm_settings.s_key=='STKTRANS_N_DPTTRANS')).select(db.sm_settings.s_value,limitby=(0,1))
                      depot_stock_transfer='NO'
                      for depot_settings_check in depot_settings_check :
                          depot_stock_transfer=depot_settings_check.s_value
                      if (depot_stock_transfer=='YES'):
                          depot_stock_balance_update=db((db.sm_depot_stock_balance.cid==session.cid) & (db.sm_depot_stock_balance.depot_id == depot_id)).update(depot_id=transfer_with_depot_id)
                      session.flash='Depot Transfered Successfully'    
                    
                else:
                     session.flash='Please Select Same Catagory Depot'    
            else:
                session.flash='Please Check Depot Properly'
        else:
            session.flash='Depot or Transfer Depot can not be blanked'          
    else:
        pass                
    
#    return 'nadira'
    redirect (URL('utility_mrep','utility'))    




#Not Used. using function at inbox
def sms_resubmit():
    import urllib
    
    if (session.user_type!='Admin'):
        session.flash='Access is denied'
        redirect(URL('utility'))
    
    c_id=session.cid
    
    search_date=SQLFORM(db.sm_search_date,
                  fields=['from_date']           
                  )
    
    smspath=''
    settRow=db((db.sm_settings.cid==c_id)&(db.sm_settings.s_key=='SMS_PATH')).select(db.sm_settings.s_value,limitby=(0,1))
    if not settRow:
        session.flash='Required settings'
        redirect(URL('utility'))
    else:
        smspath=str(settRow[0].s_value)
    
    #-------
    hostName=request.env.http_host
    appName=request.application
    baseUrl='http://'+str(hostName)+'/'+str(appName)+'/'+smspath
    #-----
    
    btn_resubmit=request.vars.btn_resubmit
    if btn_resubmit:        
        smsDate=request.vars.from_date
        returnflag='Yes'
        smsMobile=request.vars.smsMobile
        smsText=request.vars.smsText
        
        validDate=True
        try:
            smsdate= datetime.datetime.strptime(str(smsDate),'%Y-%m-%d %H:%M:%S')
        except:
            validDate=False
        
        if (smsDate=='' or smsMobile=='' or smsText==''):
            response.flash='Required Value'
        else:
            if validDate==False:
                response.flash='Invalid Date'
            else:
                validMobile=True
                try:
                    smsMobile= int(smsMobile)
                except:
                    validMobile=False
                
                if validMobile==False:
                    response.flash='Invalid Mobile'
                else:
                    mobileRow=db((db.sm_comp_mobile.cid==c_id)&(db.sm_comp_mobile.mobile_no==smsMobile)).select(db.sm_comp_mobile.mobile_no,limitby=(0,1))
                    if not mobileRow:
                        response.flash='Invalid Mobile'
                    else:                                    
                        urlPath=str(baseUrl) +'&smsdate='+str(smsdate)+'&returnflag='+str(returnflag)+ '&mob='+str(smsMobile)+'&cid='+str(c_id)+'&msg=.'+str(smsText)
                        
#                        return urlPath
                        
                        urlRes = urllib.urlopen(urlPath).read()                        
                        if urlRes!='':
                            response.flash=urlRes[5:]
                        else:
                            response.flash='Error in process'
                            
    return dict(search_date=search_date)
    
#http://127.0.0.1:8000/skf/utility_mrep/set_product_list
#http://c003.cloudapp.net/skf/utility_mrep/set_product_list


#=======================Set Product Liist

def set_product_list():
    
    cid = 'SKF'
    #     Special rate==================
    itemBonusList = []
    itemBonusList_str = []
    itemBonusRows = db((db.sm_promo_product_bonus_products.cid == cid) & (db.sm_promo_product_bonus_products.from_date <= current_date)  & (db.sm_promo_product_bonus_products.to_date >= current_date) & (db.sm_promo_product_bonus_products.status == 'ACTIVE') ).select(db.sm_promo_product_bonus_products.product_id,db.sm_promo_product_bonus_products.product_name, db.sm_promo_product_bonus_products.note, orderby=db.sm_promo_product_bonus_products.product_name)
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
    itemFlatRows = db((db.sm_promo_flat_rate.cid == cid)  & (db.sm_promo_flat_rate.status == 'ACTIVE') & (db.sm_promo_flat_rate.from_date <= current_date)  & (db.sm_promo_flat_rate.to_date >= current_date) ).select(db.sm_promo_flat_rate.product_id,db.sm_promo_flat_rate.product_name, db.sm_promo_flat_rate.min_qty, db.sm_promo_flat_rate.flat_rate, orderby=db.sm_promo_flat_rate.product_name)
    for itemFlatRows in itemFlatRows:
        product_id = itemFlatRows.product_id
        product_name = itemFlatRows.product_name
        flat_rate = itemFlatRows.flat_rate
        min_qty = itemFlatRows.min_qty      
        itemFlatList.append(str(product_id))
        itemFlatList_str.append('Flat:Min '+str(min_qty)+' Rate '+str(flat_rate))
    
    
    
    productStr = ''
    productRows = db(db.sm_item.cid == cid).select(db.sm_item.item_id, db.sm_item.name, db.sm_item.price, db.sm_item.vat_amt, orderby=db.sm_item.name)
    
    for productRow in productRows:
        item_id = productRow.item_id       
        name = productRow.name
        price_amt = productRow.price
        vat_amt=productRow.vat_amt
        price_get=float(price_amt)+float(vat_amt)
        price=round(price_get, 2)
        vat=round(float(vat_amt),2)
        
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
            productStr = str(item_id) + '<fd>' + str(name) + '<fd>' + str(price) + '<fd>' + str(recRow_str)+'<fd>'+str(vat)
        else:
            productStr += '<rd>' + str(item_id) + '<fd>' + str(name) + '<fd>' + str(price) + '<fd>' + str(recRow_str)+'<fd>'+str(vat)
     
#     return productStr
    item_update=db((db.sm_company_settings.cid==cid)).update(field1=productStr)
    
    if (item_update>0):
        session.flash='Successfully Prepared'        
    else:
        session.flash='Error in process'
                 
    redirect (URL('utility_mrep','utility_settings'))
    
    
