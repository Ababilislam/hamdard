#level Transfer

#============================= 

def level_transfer(): 
    
    #----------
    response.title='Device Registration'
    
    #----------
    btn_transfer=request.vars.btn_transfer
    checkbox=request.vars.checkbox
    if btn_transfer and checkbox==None:
        response.flash='Please Confirm First'  
        
    if btn_transfer and checkbox!=None:
#        return checkbox
        level_id=str(request.vars.level_id).strip().upper()
        under_level_id=str(request.vars.under_level_id).strip().upper()
#        return level_id
        if ((level_id != '') and (under_level_id != '')):
            level_check=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id==level_id)).select(db.sm_level.ALL,limitby=(0,1))
            under_level_check=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id==under_level_id)).select(db.sm_level.ALL,limitby=(0,1))
#            return level_check
            
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
                    
#                return level0_under_level
                if (int(depth_level)==int(depth_under_level)+1):
#                    return 'haha'
                    if (depth_level>0):
#                        return depth_level
                        if (depth_level==1):
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level)
#                            return db._lastsql
                           
                            
                            
                            
                            child_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level1==level_id) ).update(level0=level0_under_level)
                            
#                            return db._lastsql
                            
                        if (depth_level==2):
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level)
                            child_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level2==level_id) ).update(level0=level0_under_level,level1=level1_under_level)
                               
                        if (depth_level==3):
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level,level3=level3_under_level)
                            child_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level3==level_id) ).update(level0=level0_under_level,level1=level1_under_level,level2=level2_under_level)
                                
                        if (depth_level==4):
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level,level3=level3_under_level)
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level4 == level_id)).update(level0=level0_under_level,level1=level1_under_level,level2=level2_under_level,level3=level3_under_level)
                            
                        if (depth_level==5):
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level,level3=level3_under_level,level4=level4_under_level)
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level5 == level_id)).update(level0=level0_under_level,level1=level1_under_level,level2=level2_under_level,level3=level3_under_level,level4=level4_under_level)
                            
                        if (depth_level==6):
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level,level3=level3_under_level,level4=level4_under_level,level5=level5_under_level)
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level6 == level_id)).update(level0=level0_under_level,level1=level1_under_level,level2=level2_under_level,level3=level3_under_level,level4=level4_under_level,level5=level5_under_level)   
                        
                        if (depth_level==7):
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level,level3=level3_under_level,level4=level4_under_level,level5=level5_under_level,level6=level6_under_level)
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level7 == level_id)).update(level0=level0_under_level,level1=level1_under_level,level2=level2_under_level,level3=level3_under_level,level4=level4_under_level,level5=level5_under_level,level6=level6_under_level)    
                        if (depth_level==8):
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id == level_id)).update(parent_level_id=under_level_id,level0=level0_under_level,level1=level1_under_level,level3=level3_under_level,level4=level4_under_level,level5=level5_under_level,level6=level6_under_level,level7=level7_under_level)
                            parent_update=db((db.sm_level.cid==session.cid) & (db.sm_level.level8 == level_id)).update(level0=level0_under_level,level1=level1_under_level,level2=level2_under_level,level3=level3_under_level,level4=level4_under_level,level5=level5_under_level,level6=level6_under_level,level7=level7_under_level)
                            
                        response.flash='Transfered Successfully'    
                    
                else:
                     response.flash='Error: Transfer can be done in the same level only'    
            else:
                response.flash='Error: Invalid Level ID'
        else:
            response.flash='Error: Invalid Transfer Request'          
    else:
        pass                
    return dict()
 
