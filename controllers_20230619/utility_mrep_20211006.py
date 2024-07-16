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
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level,level2=level2_under_level,level3=level3_under_level, parent_level_name=under_level_name,level0_name=level0_under_level_name,level1_name=level1_under_level_name,level2_name=level2_under_level_name,level3_name=level3_under_level_name)
                            child_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level3==level_id) ).update(level0=level0_under_level,level1=level1_under_level,level2=level2_under_level, level0_name=level0_under_level_name,level1_name=level1_under_level_name,level2_name=level2_under_level_name)
                                
                        if (depth_level==4):
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level,level3=level3_under_level, parent_level_name=under_level_name,level0_name=level0_under_level_name,level1_name=level1_under_level_name,level3_name=level3_under_level_name)
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level4 == level_id)).update(level0=level0_under_level,level1=level1_under_level,level2=level2_under_level,level3=level3_under_level, level0_name=level0_under_level_name,level1_name=level1_under_level_name,level2_name=level2_under_level_name,level3_name=level3_under_level_name)
                            
                        if (depth_level==5):
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level,level3=level3_under_level,level4=level4_under_level, parent_level_name=under_level_name_id,level0_name=level0_under_level_name,level1_name=level1_under_level_name,level3_name=level3_under_level_name,level4_name=level4_under_level_name,level2=level2_under_level,level2_name=level2_under_level_name)
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level5 == level_id)).update(level0=level0_under_level,level1=level1_under_level,level2=level2_under_level,level3=level3_under_level,level4=level4_under_level, level0_name=level0_under_level_name,level1_name=level1_under_level_name,level2_name=level2_under_level_name,level3_name=level3_under_level_name,level4_name=level4_under_level_name)
                            
                        if (depth_level==6):
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level,level3=level3_under_level,level4=level4_under_level,level5=level5_under_level, parent_level_name=under_level_name,level0_name=level0_under_level_name,level1_name=level1_under_level_name,level3_name=level3_under_level_name,level4_name=level4_under_level_name,level5_name=level5_under_level_name,level2=level2_under_level,level2_name=level2_under_level_name)
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level6 == level_id)).update(level0=level0_under_level,level1=level1_under_level,level2=level2_under_level,level3=level3_under_level,level4=level4_under_level,level5=level5_under_level, level0_name=level0_under_level_name,level1_name=level1_under_level_name,level2_name=level2_under_level_name,level3_name=level3_under_level_name,level4_name=level4_under_level_name,level5_name=level5_under_level_name)   
                        
                        if (depth_level==7):
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level,level3=level3_under_level,level4=level4_under_level,level5=level5_under_level,level6=level6_under_level, parent_level_name=under_level_name,level0_name=level0_under_level_name,level1_name=level1_under_level_name,level3_name=level3_under_level_name,level4_name=level4_under_level_name,level5_name=level5_under_level_name,level6_name=level6_under_level_name,level2=level2_under_level,level2_name=level2_under_level_name)
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level7 == level_id)).update(level0=level0_under_level,level1=level1_under_level,level2=level2_under_level,level3=level3_under_level,level4=level4_under_level,level5=level5_under_level,level6=level6_under_level, level0_name=level0_under_level_name,level1_name=level1_under_level_name,level2_name=level2_under_level_name,level3_name=level3_under_level_name,level4_name=level4_under_level_name,level5_name=level5_under_level_name,level6_name=level6_under_level_name)    
                        if (depth_level==8):
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level,level3=level3_under_level,level4=level4_under_level,level5=level5_under_level,level6=level6_under_level,level7=level7_under_level, parent_level_name=under_level_name,level0_name=level0_under_level_name,level1_name=level1_under_level_name,level3_name=level3_under_level_name,level4_name=level4_under_level_name,level5_name=level5_under_level_name,level6_name=level6_under_level_name,level7_name=level7_under_level_name,level2=level2_under_level,level2_name=level2_under_level_name)
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
    cid=session.cid
#     cid = 'NOVIVO'
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
        session.flash='Successfully Prepared'        
    else:
        session.flash='Error in process'
        
    redirect (URL('utility_mrep','utility_settings'))
    
#------------- clean function call
def branch_data_clean_request():
    import urllib
    
    if (session.user_type!='Admin'):
        session.flash='Access is denied'
        redirect(URL('utility_settings'))
    
    c_id=session.cid
    
    btn_clean_branch_data=request.vars.btn_clean_branch_data
    if btn_clean_branch_data:
        clean_branch_id=request.vars.clean_branch_id
        clean_password=request.vars.clean_password
        clean_checkbox=request.vars.clean_checkbox
        
        if (clean_branch_id=='' or clean_password=='' or clean_checkbox!='YES'):
            session.flash='Required All Value'
        else:
            depotCheck=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==clean_branch_id)).select(db.sm_depot.name,limitby=(0,1))
            if not depotCheck:
                session.flash='Invalid Branch ID'
            else:
                clean_branch_name=depotCheck[0].name
                #-----------------------
                if clean_password!='sdf23423dfdg343fdgfd':
                    session.flash='Invalid Password'
                else:
                    depotid=str(clean_branch_id)
                    
                    requisitionHead=db((db.sm_requisition_head.cid==c_id)&(db.sm_requisition_head.depot_id==depotid)).delete()
                    requisitionDetails=db((db.sm_requisition.cid==c_id)&(db.sm_requisition.depot_id==depotid)).delete()
                    
                    issueHead=db((db.sm_issue_head.cid==c_id)&(db.sm_issue_head.depot_id==depotid)).delete()
                    issueDetails=db((db.sm_issue.cid==c_id)&(db.sm_issue.depot_id==depotid)).delete()
                    
                    receiveHead=db((db.sm_receive_head.cid==c_id)&(db.sm_receive_head.depot_id==depotid)).delete()
                    receiveDetails=db((db.sm_receive.cid==c_id)&(db.sm_receive.depot_id==depotid)).delete()
                    
                    damageHead=db((db.sm_damage_head.cid==c_id)&(db.sm_damage_head.depot_id==depotid)).delete()
                    damageDetails=db((db.sm_damage.cid==c_id)&(db.sm_damage.depot_id==depotid)).delete()
                    
                    disputeHead=db((db.sm_transaction_dispute_head.cid==c_id)&(db.sm_transaction_dispute_head.depot_id==depotid)).delete()
                    disputeDetails=db((db.sm_transaction_dispute.cid==c_id)&(db.sm_transaction_dispute.depot_id==depotid)).delete()
                    
                    #--------------
                    orderHead=db((db.sm_order_head.cid==c_id)&(db.sm_order_head.depot_id==depotid)).update(status='Invoiced',flag_data='1',field2=1)
                    orderDetails=db((db.sm_order.cid==c_id)&(db.sm_order.depot_id==depotid)).update(status='Invoiced',flag_data='1',field2=1)
                    
                    invoiceHead=db((db.sm_invoice_head.cid==c_id)&(db.sm_invoice_head.depot_id==depotid)).delete()
                    invoiceDetails=db((db.sm_invoice.cid==c_id)&(db.sm_invoice.depot_id==depotid)).delete()
                    
                    returnHead=db((db.sm_return_head.cid==c_id)&(db.sm_return_head.depot_id==depotid)).delete()
                    returnDetails=db((db.sm_return.cid==c_id)&(db.sm_return.depot_id==depotid)).delete()
                    returnCancel=db((db.sm_return_cancel.cid==c_id)&(db.sm_return_cancel.depot_id==depotid)).delete() #new
                    
                    tpRulesTemp=db((db.sm_tp_rules_temp_process.cid==c_id)&(db.sm_tp_rules_temp_process.depot_id==depotid)).delete()
                    tpRulesManualTemp=db((db.sm_tp_rules_temp_process_manual.cid==c_id)&(db.sm_tp_rules_temp_process_manual.depot_id==depotid)).delete()
                    
                    payment=db((db.sm_payment_collection.cid==c_id)&(db.sm_payment_collection.depot_id==depotid)).delete()
                    
                    stock=db((db.sm_depot_stock_balance.cid==c_id)&(db.sm_depot_stock_balance.depot_id==depotid)).update(quantity=0,block_qty=0)
                    
                    rptTransaction=db((db.sm_rpt_transaction.cid==c_id)&(db.sm_rpt_transaction.depot_id==depotid)).delete() #new
                    
                    ledgerSql="delete FROM `sm_transaction` WHERE `reference` like('"+depotid+"%')"
                    db.executesql(ledgerSql)
                    
                    urlRes='Data clean: Requisition,Issue,Receive,Damage,Dispute,Invoice,Return,Payment,Ledger; Data update: Order and stock '
                    session.flash='Branch ID:'+str(depotid)+', Branch Name:'+str(clean_branch_name)+'. '+urlRes
                    
                    #-------------------------
                    
    redirect(URL('utility_settings'))


def national_data_clean_request():
    import urllib

    if (session.user_type != 'Admin'):
        session.flash = 'Access is denied'
        redirect(URL('utility_settings'))

    c_id = session.cid

    btn_clean_data_n = request.vars.btn_clean_data_n
    if btn_clean_data_n:
        clean_password_n = request.vars.clean_password_n
        clean_checkbox_n = request.vars.clean_checkbox_n

        if clean_password_n == '' or clean_checkbox_n != 'Confirm':
            session.flash = 'Required All Value'
        else:
            # -----------------------
            if clean_password_n != 'sdf23423dfd343fdfd923':
                session.flash = 'Invalid Password'
            else:
                requisitionHead = db(db.sm_requisition_head.cid == c_id).delete()
                requisitionDetails = db(db.sm_requisition.cid == c_id).delete()

                issueHead = db(db.sm_issue_head.cid == c_id).delete()
                issueDetails = db(db.sm_issue.cid == c_id).delete()

                receiveHead = db(db.sm_receive_head.cid == c_id).delete()
                receiveDetails = db(db.sm_receive.cid == c_id).delete()

                damageHead = db(db.sm_damage_head.cid == c_id).delete()
                damageDetails = db(db.sm_damage.cid == c_id).delete()

                disputeHead = db(db.sm_transaction_dispute_head.cid == c_id).delete()
                disputeDetails = db(db.sm_transaction_dispute.cid == c_id).delete()

                # --------------
                orderHead = db(db.sm_order_head.cid == c_id).update(status='Invoiced', flag_data='1', field2=1)
                orderDetails = db(db.sm_order.cid == c_id).update(status='Invoiced', flag_data='1', field2=1)

                invoiceHead = db(db.sm_invoice_head.cid == c_id).delete()
                invoiceDetails = db(db.sm_invoice.cid == c_id).delete()

                returnHead = db(db.sm_return_head.cid == c_id).delete()
                returnDetails = db(db.sm_return.cid == c_id).delete()
                returnCancel = db(db.sm_return_cancel.cid == c_id).delete()  # new

                tpRulesTemp = db(db.sm_tp_rules_temp_process.cid == c_id).delete()
                tpRulesManualTemp = db(db.sm_tp_rules_temp_process_manual.cid == c_id).delete()

                payment = db(db.sm_payment_collection.cid == c_id).delete()

                stock = db(db.sm_depot_stock_balance.cid == c_id).update(quantity=0, block_qty=0)

                rptTransaction = db(db.sm_rpt_transaction.cid == c_id).delete()  # new

                ledgerSql = "delete FROM `sm_transaction` WHERE `cid` ='" + c_id + "'"
                db.executesql(ledgerSql)

                urlRes = 'Data clean: Requisition,Issue,Receive,Damage,Dispute,Invoice,Return,Payment,Ledger; Data update: Order and stock '
                session.flash = urlRes

                    # -------------------------

    redirect(URL('utility_settings'))


#------------- clean function call
def branch_data_clean_request_bak():
    import urllib
    
    if (session.user_type!='Admin'):
        session.flash='Access is denied'
        redirect(URL('utility_settings'))
    
    c_id=session.cid
    
    
    cleanpath='utility/clean_depot_data?'
    #-------
    hostName=request.env.http_host
    appName=request.application
    baseUrl='http://'+str(hostName)+'/'+str(appName)+'/'+cleanpath
    #-----
    
    btn_clean_branch_data=request.vars.btn_clean_branch_data
    if btn_clean_branch_data:
        clean_branch_id=request.vars.clean_branch_id
        clean_password=request.vars.clean_password
        clean_checkbox=request.vars.clean_checkbox
        
        if (clean_branch_id=='' or clean_password=='' or clean_checkbox!='YES'):
            session.flash='Required All Value'
        else:            
            depotCheck=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==clean_branch_id) & (db.sm_depot.depot_category=='DEPOT')).select(db.sm_depot.name,limitby=(0,1))
            if not depotCheck:
                session.flash='Invalid Branch ID'
            else:
                clean_branch_name=depotCheck[0].name
                
                urlPath=str(baseUrl) +'cid='+str(c_id)+'&depotid='+str(clean_branch_id)+'&password='+str(clean_password)
                
                urlRes = urllib.urlopen(urlPath).read()                        
                if urlRes!='':
                    session.flash='Branch ID:'+str(clean_branch_id)+', Branch Name:'+str(clean_branch_name)+'. '+urlRes
                else:
                    session.flash='Error in process'
    
    redirect(URL('utility_settings'))


#=======================Set Prescription Liist
def set_prescription_list():
    
#     c_id = 'NOVIVO'
    c_id=session.cid
    
    productStr_A = ''
    recordstring_A="SELECT item_id,name FROM `sm_item_prescription` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'A%' ORDER BY `name` ASC"
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
    recordstring_B="SELECT * FROM `sm_item_prescription` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'B%' ORDER BY `name` ASC"
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
    recordstring_C="SELECT * FROM `sm_item_prescription` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'C%' ORDER BY `name` ASC"
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
    recordstring_D="SELECT * FROM `sm_item_prescription` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'D%' ORDER BY `name` ASC"
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
    recordstring_E="SELECT * FROM `sm_item_prescription` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'E%' ORDER BY `name` ASC"
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
    recordstring_F="SELECT * FROM `sm_item_prescription` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'F%' ORDER BY `name` ASC"
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
    recordstring_G="SELECT * FROM `sm_item_prescription` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'G%' ORDER BY `name` ASC"
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
    recordstring_H="SELECT * FROM `sm_item_prescription` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'H%' ORDER BY `name` ASC"
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
    recordstring_I="SELECT * FROM `sm_item_prescription` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'I%' ORDER BY `name` ASC"
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
    recordstring_J="SELECT * FROM `sm_item_prescription` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'J%' ORDER BY `name` ASC"
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
    recordstring_K="SELECT * FROM `sm_item_prescription` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'K%' ORDER BY `name` ASC"
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
    recordstring_L="SELECT * FROM `sm_item_prescription` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'L%' ORDER BY `name` ASC"
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
    recordstring_M="SELECT * FROM `sm_item_prescription` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'M%' ORDER BY `name` ASC"
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
    recordstring_N="SELECT * FROM `sm_item_prescription` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'N%' ORDER BY `name` ASC"
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
    recordstring_O="SELECT * FROM `sm_item_prescription` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'O%' ORDER BY `name` ASC"
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
    recordstring_P="SELECT * FROM `sm_item_prescription` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'P%' ORDER BY `name` ASC"
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
    recordstring_Q="SELECT * FROM `sm_item_prescription` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'Q%' ORDER BY `name` ASC"
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
    recordstring_R="SELECT * FROM `sm_item_prescription` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'R%' ORDER BY `name` ASC"
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
    recordstring_S="SELECT * FROM `sm_item_prescription` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'S%' ORDER BY `name` ASC"
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
    recordstring_T="SELECT * FROM `sm_item_prescription` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'T%' ORDER BY `name` ASC"
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
    recordstring_U="SELECT * FROM `sm_item_prescription` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'U%' ORDER BY `name` ASC"
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
    recordstring_V="SELECT * FROM `sm_item_prescription` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'V%' ORDER BY `name` ASC"
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
    recordstring_W="SELECT * FROM `sm_item_prescription` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'W%' ORDER BY `name` ASC"
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
    recordstring_X="SELECT * FROM `sm_item_prescription` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'X%' ORDER BY `name` ASC"
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
    recordstring_Y="SELECT * FROM `sm_item_prescription` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'Y%' ORDER BY `name` ASC"
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
    recordstring_Z="SELECT * FROM `sm_item_prescription` WHERE cid = '"+ c_id +"' AND status = 'ACTIVE' AND `name` LIKE 'Z%' ORDER BY `name` ASC"
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
    
    return productStr
    
           
    item_update=db((db.sm_company_settings.cid==c_id)).update(item_list_mobile=productStr)
    
    if (item_update>0):
        session.flash='Successfully Prepared'        
    else:
        session.flash='Error in process'
                 
    redirect (URL('utility_mrep','utility_settings'))



#===========17_10_2019===Jolly===========

#====== http://127.0.0.1:8000/kpl/tour_summary/tour_summary_insert_cron?first_date=2019-10-01


def tour_summary_insert_cron(): 
    
    import datetime
    import time
    cid=session.cid
    get_month=str(request.vars.get_month)    
    
    if (get_month=='This'):
        checkDate=str(first_currentDate).split(' ')[0]

    else:
        todayDate = datetime.date.today()
        checkDate1 = str(todayDate + datetime.timedelta(days=30))
        checkDate=checkDate1.split('-')[0]+'-'  +checkDate1.split('-')[1]  +'-01'

     
    if get_month=='':                    
         session.flash='Please Select Month'           
    
    else:
        deleteStr="TRUNCATE z_tour_info ;"
        deleteRun=db.executesql(deleteStr)
        
        insertSql="INSERT INTO  z_tour_info (cid,rep_id,rep_name,note,user_type,firstdate) SELECT cid,rep_id ,name,note,user_type,'"+checkDate+"' as note FROM sm_rep"    
        db.executesql(insertSql)
         
        updateSql="""UPDATE z_tour_info z, sm_supervisor_level s set z.field1=s.level_depth_no  where z.cid=s.cid and z.rep_id=s.sup_id """        
        db.executesql(updateSql)
        
        updateSql21="""UPDATE z_tour_info z, sm_doctor_visit_plan v set z.tour_status=v.status where z.cid=v.cid and z.rep_id=v.rep_id and z.firstdate=v.first_date"""    
        db.executesql(updateSql21)
        
        
        
        #         =====================Level update  
        
        
        updateSql11="""UPDATE z_tour_info z, sm_rep_area r set z.territory_id=r.area_id,z.territory_name=r.area_name where z.cid=r.cid and z.rep_id=r.rep_id """
        db.executesql(updateSql11)
        
        #s
        updateSql11S="""UPDATE z_tour_info z, sm_rep_area r set z.territory_id=r.area_id,z.territory_name=r.area_name where z.cid=r.cid and z.rep_id=r.rep_id and r.field2=1"""
        db.executesql(updateSql11S)

        errorF=1
        updateSql1="""UPDATE z_tour_info z, sm_level l set z.zone_id=l.level0,z.zone_name=l.level0_name,z.region_id=l.level1,z.region_name=l.level1_name,z.area_id=l.level2,z.area_name=l.level2_name where z.cid=l.cid and z.territory_id=l.level_id and l.is_leaf=1"""    
        updateSqlex1= db.executesql(updateSql1)
        
        #s
        updateSql1S="""UPDATE z_tour_info z, sm_level l set z.zone_id=l.level0,z.zone_name=l.level0_name,z.region_id=l.level1,z.region_name=l.level1_name,z.area_id=l.level2,z.area_name=l.level2_name where z.cid=l.cid and z.territory_id=l.level_id and l.field2=1 and l.is_leaf=1"""    
        updateSqlex1= db.executesql(updateSql1S)
        
        errorF=0

        if errorF==0:

            updateSql2="""UPDATE z_tour_info z, sm_supervisor_level s set z.area_id=s.level_id,z.area_name=s.level_name where z.cid=s.cid and z.rep_id=s.sup_id and z.field1=2 """    
            updateSqlex2=db.executesql(updateSql2)
            
            #s
            updateSql2S="""UPDATE z_tour_info z, sm_supervisor_level s set z.area_id=s.level_id,z.area_name=s.level_name where z.cid=s.cid and z.rep_id=s.sup_id and s.field2=1 and z.field1=2 """    
            updateSqlex2=db.executesql(updateSql2S)
            
            errorF=0
            
            if errorF==0:   
                updateSql3="""UPDATE z_tour_info z, sm_supervisor_level s set z.region_id=s.level_id,z.region_name=s.level_name where z.cid=s.cid and z.rep_id=s.sup_id and z.field1=1 """     
                db.executesql(updateSql3)
                
                #s
                updateSql3S="""UPDATE z_tour_info z, sm_supervisor_level s set z.region_id=s.level_id,z.region_name=s.level_name where z.cid=s.cid and z.rep_id=s.sup_id and s.field2=1 and z.field1=1 """    
                db.executesql(updateSql3S)
                
                errorF=0
                
                if errorF==0:   
                    updateSqlzone="""UPDATE z_tour_info z, sm_supervisor_level s set z.zone_id=s.level_id,z.zone_name=s.level_name where z.cid=s.cid and z.rep_id=s.sup_id and z.field1=0 """
                    db.executesql(updateSqlzone)
                    
                    #s
                    updateSqlzoneS="""UPDATE z_tour_info z, sm_supervisor_level s set z.zone_id=s.level_id,z.zone_name=s.level_name where z.cid=s.cid and z.rep_id=s.sup_id and s.field2=1 and z.field1=0 """
                    db.executesql(updateSqlzoneS)
                    
                    errorF=0
                
                    if errorF==0:  
                        updateSqlzone1="""UPDATE z_tour_info z, sm_level s set z.zone_id=s.level0,z.zone_name=s.level0_name where z.cid=s.cid and z.region_id=s.level_id and z.field1=1 """
                        db.executesql(updateSqlzone1)
                        
                        #s
                        updateSqlzone1S="""UPDATE z_tour_info z, sm_level s set z.zone_id=s.level0,z.zone_name=s.level0_name where z.cid=s.cid and z.region_id=s.level_id and s.field2=1 and z.field1=1 """
                        db.executesql(updateSqlzone1S)
                        
                        errorF=0
                
                        if errorF==0:  
                            updateSqlzone2="""UPDATE z_tour_info z, sm_level s set z.zone_id=s.level0,z.zone_name=s.level0_name,z.region_id=s.level1,z.region_name=s.level1_name where z.cid=s.cid and z.area_id=s.level2 and z.field1=2 """
                            db.executesql(updateSqlzone2) 
                            
                            #s
                            updateSqlzone2S="""UPDATE z_tour_info z, sm_level s set z.zone_id=s.level0,z.zone_name=s.level0_name,z.region_id=s.level1,z.region_name=s.level1_name where z.cid=s.cid and z.area_id=s.level2 and s.field2=1 and z.field1=2 """
                            db.executesql(updateSqlzone2S)                            
                            
                            session.flash='Updated Successfully'
                            redirect (URL('utility_mrep', 'utility_settings'))
#                             =================
                        else:
                            return 'Failed'
                        
                    else:
                        return 'Failed'
                    
                else:
                    return 'Failed'
                
            else:
                return 'Failed'

                             
        

def set_sample_list():
    cid=session.cid

    
    
    # return cid
    productStr = ''
    productRows = db((db.sm_doctor_sample.cid == cid) & (db.sm_doctor_sample.status == 'ACTIVE')).select(db.sm_doctor_sample.item_id, db.sm_doctor_sample.name, orderby=db.sm_doctor_sample.name)
    # return productRows
    for productRow in productRows:
        item_id = productRow.item_id       
        name = str(productRow.name).replace(".","").replace(",","")
        price_amt = ''
        vat_amt=''
        price_get=''
        price=''
        recRow_str=''

        
        if productStr == '':
            productStr = str(item_id) + '<fd>' + str(name) + '<fd>' + str(price) + '<fd>' + str(recRow_str)+'<fd>'+str(vat_amt)
        else:
            productStr += '<rd>' + str(item_id) + '<fd>' + str(name) + '<fd>' + str(price) + '<fd>' + str(recRow_str)+'<fd>'+str(vat_amt)
     
    return productStr
    item_update=db((db.sm_company_settings.cid==cid)).update(note=productStr)
    
    if (item_update>0):
        session.flash='Successfully Prepared'        
    else:
        session.flash='Error in process'
        
    redirect (URL('utility_mrep','utility_settings'))   
    

def branch_client_transfer():
    import urllib
    
    if (session.user_type!='Admin'):
        session.flash='Access is denied'
        redirect(URL('utility_settings'))
        
    c_id=session.cid
    
    btn_trans_client_branch_data=request.vars.btn_trans_client_branch_data
    if btn_trans_client_branch_data:
        transfer_client_id_list=request.vars.transfer_client_id_list
        transfer_branch_id=request.vars.transfer_branch_id
        transfer_store_id=request.vars.transfer_store_id
        transfer_password=request.vars.transfer_password
        transfer_checkbox=request.vars.transfer_checkbox
        
        if (transfer_client_id_list=='' or transfer_branch_id=='' or transfer_store_id=='' or transfer_password=='' or transfer_checkbox!='Confirm'):
            session.flash='Required All Value accurately'
        else:
            transfer_client_id_str=''
            transfer_client_id_list = transfer_client_id_list.split('\n')
            
            for i in range(len(transfer_client_id_list)):
                client_id=str(transfer_client_id_list[i]).strip()
                if client_id!='':
                    if transfer_client_id_str=='':
                        transfer_client_id_str="'"+client_id+"'"
                    else:
                        transfer_client_id_str+=",'"+client_id+"'"
            
            depotCheck=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==transfer_branch_id)).select(db.sm_depot.name,limitby=(0,1))
            if not depotCheck:
                session.flash='Invalid Branch ID'
            else:
                transfer_branch_name=str(depotCheck[0].name)
                
                storeCheck=db((db.sm_depot_store.cid==c_id) & (db.sm_depot_store.depot_id==transfer_branch_id) & (db.sm_depot_store.store_id==transfer_store_id)).select(db.sm_depot_store.store_name,limitby=(0,1))
                if not storeCheck:
                    session.flash='Invalid Branch Store ID'
                else:
                    transfer_store_name=str(storeCheck[0].store_name)
                
                #-----------------------
                if transfer_password!='sdf23423dfdg343fdgfdz':
                    session.flash='Invalid Password'
                else:
                    depotid=str(transfer_branch_id)
                    
                    sql="update `sm_client` set depot_id='"+depotid+"',depot_name='"+transfer_branch_name+"',store_id='"+transfer_store_id+"',store_name='"+transfer_store_name+"' WHERE cid='"+c_id+"' and client_id in ("+transfer_client_id_str+");"
                    db.executesql(sql)
                    
                    session.flash='Updated successfully in Client'    
                    
                    #-------------------------                    
    redirect(URL('utility_settings'))
    