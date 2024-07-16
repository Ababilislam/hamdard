from random import randint
import time

#Validation for level
def level_validation(form):
    cid=session.cid
    
    level_id=str(form.vars.level_id).strip().upper()    
    level_name_row=str(form.vars.level_name).strip().upper()
    level_name=check_special_char(level_name_row)
    
    depth=int(form.vars.depth)
    
    is_leaf='0'
    company_levelDepth=session.levleDepth
    if int(depth)==int(company_levelDepth):
        is_leaf='1'
        
    #---------------------
    if is_leaf=='1':
        territory_des=str(request.vars.territory_des).strip().upper()
        if not(territory_des=='' or territory_des==None):
            territory_des=check_special_char(territory_des)
            form.vars.territory_des=territory_des
            
        special_territory_code=str(request.vars.special_territory_code).strip().upper()
        if not(special_territory_code=='' or special_territory_code==None):
            special_territory_code=check_special_char_id(special_territory_code)
            form.vars.special_territory_code=special_territory_code
    
    #-------------------
    rows_check=db((db.sm_level.cid==cid) & (db.sm_level.level_id==level_id)).select(db.sm_level.level_id,limitby=(0,1))
    if rows_check:
        form.errors.level_id=''
        response.flash='Level ID already exist,please choose a new'
    else:
        rows_check2=db((db.sm_level.cid==cid) & (db.sm_level.level_name==level_name)).select(db.sm_level.level_id,limitby=(0,1))
        if rows_check2:
            form.errors.level_name=''    
            response.flash='Level Name already exist,please choose a new'        
        else:            
            #Set 0 to 8 level based on level depth
            if depth==0:
                form.vars.level0=level_id
                form.vars.level0_name=level_name
            elif depth==1:
                form.vars.level1=level_id
                form.vars.level1_name=level_name
            elif depth==2:
                form.vars.level2=level_id
                form.vars.level2_name=level_name
            elif depth==3:
                form.vars.level3=level_id
                form.vars.level3_name=level_name
            elif depth==4:
                form.vars.level4=level_id
                form.vars.level4_name=level_name
            elif depth==5:
                form.vars.level5=level_id
                form.vars.level5_name=level_name
            elif depth==6:
                form.vars.level6=level_id
                form.vars.level6_name=level_name
            elif depth==7:
                form.vars.level7=level_id
                form.vars.level7_name=level_name
            elif depth==8:
                form.vars.level8=level_id
                form.vars.level7_name=level_name
                
                
            form.vars.level_id=level_id
            form.vars.level_name=level_name
            
#8 level fixed for level.Maximum level should be 8 or less 
def level():
    #Check access permission
    #----------Task assaign----------
    task_id='rm_workingarea_manage'
    task_id_view='rm_workingarea_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    response.title='Area Structure'
    
    #===================================================variables
    cid=session.cid
    
    #get_company_levelDepth from sm_settings
    company_levelDepth=session.levleDepth
    parentLevelId= request.args(0)
    
    parentLevelName=''
    parentLevelDepth=0
    level0=''
    level0_name=''
    level1=''
    level1_name=''
    level2=''
    level2_name=''
    level3=''
    level3_name=''
    level4=''
    level4_name=''
    level5=''
    level5_name=''
    level6=''
    level6_name=''
    level7=''
    level7_name=''
    level8=''
    level8_name=''
    
    depth=0
    is_leaf='0'
    
    
    #parent level id search
    if parentLevelId==None or parentLevelId=='':
        parentLevelId='0'
    else:
        parentRecords=db((db.sm_level.cid==cid) & (db.sm_level.level_id==parentLevelId)).select(db.sm_level.ALL,limitby=(0,1))
        if parentRecords:
            parentLevelName = str(parentRecords[0].level_name)
            parentLevelDepth = parentRecords[0].depth
            
            level0 = str(parentRecords[0].level0)
            level0_name = str(parentRecords[0].level0_name)
            level1 = str(parentRecords[0].level1)
            level1_name = str(parentRecords[0].level1_name)
            level2 = str(parentRecords[0].level2)
            level2_name = str(parentRecords[0].level2_name)
            level3 = str(parentRecords[0].level3)
            level3_name = str(parentRecords[0].level3_name)
            level4 = str(parentRecords[0].level4)
            level4_name = str(parentRecords[0].level4_name)
            level5 = str(parentRecords[0].level5)
            level5_name = str(parentRecords[0].level5_name)
            level6 = str(parentRecords[0].level6)
            level6_name = str(parentRecords[0].level6_name)
            level7 = str(parentRecords[0].level7)
            level7_name = str(parentRecords[0].level7_name)
            level8 = str(parentRecords[0].level8)
            level8_name = str(parentRecords[0].level8_name)
            
            depth=int(parentLevelDepth)+1
    
    #if current depth and company depth same then is_leaf=1 that means last level
    if int(depth)==int(company_levelDepth):
        is_leaf='1'
        
    
    #=================================================== Entry Form
    #'level0','level0_name','level1','level1_name','level2','level2_name','level3','level3_name','level4','level4_name','level5','level5_name','level6','level6_name','level8','level8_name',
    
    form =SQLFORM(db.sm_level,
          fields=['level_id','level_name','territory_des','special_territory_code'],
          submit_button='Save'
        )
    
    form.vars.cid=cid
    form.vars.parent_level_id=parentLevelId
    form.vars.parent_level_name=parentLevelName
    form.vars.depth=depth
    form.vars.is_leaf=is_leaf
    
    form.vars.level0=level0
    form.vars.level0_name=level0_name
    form.vars.level1=level1
    form.vars.level1_name=level1_name
    form.vars.level2=level2
    form.vars.level2_name=level2_name
    form.vars.level3=level3
    form.vars.level3_name=level3_name
    form.vars.level4=level4
    form.vars.level4_name=level4_name
    form.vars.level5=level5
    form.vars.level5_name=level5_name
    form.vars.level6=level6
    form.vars.level6_name=level6_name
    form.vars.level7=level7
    form.vars.level7_name=level7_name
    form.vars.level8=level8
    form.vars.level8_name=level8_name
    
    #Insert after validation
    if form.accepts(request.vars,session,onvalidation=level_validation):            
        level_id=form.vars.level_id
        level_name=form.vars.level_name
        
        sqlStr="update sm_level set level"+str(depth)+"='"+str(level_id)+"',level"+str(depth)+"_name='"+str(level_name)+"' where cid='"+str(cid)+"' and level_id ='"+str(level_id)+"'"
        db.executesql(sqlStr)
        
        response.flash = 'Submitted Successfully'       
        
    
    #========================================================= Update and Delete
    btn_edit=request.vars.btn_edit
    btn_delete=request.vars.btn_delete
    
    if btn_edit or btn_delete:
        rowid=str(request.vars.rowid).strip()
        level_id=str(request.vars.level_id).strip()
        
        #Delete part
        if btn_delete!=None:            
            usedCheckRow=db((db.sm_level.cid==cid) & (db.sm_level.parent_level_id==level_id)).select(db.sm_level.level_id,limitby=(0,1))       
            if usedCheckRow:
                response.flash='First delete child level'
            else:                
                #Check level is used in rep area
                usedCheckRow_reparea=db((db.sm_rep_area.cid==cid) & (db.sm_rep_area.area_id==level_id)).select(db.sm_rep_area.area_id,limitby=(0,1))       
                if usedCheckRow_reparea:
                    response.flash='Already used in MSO-Territory'
                else:
                    #Check level is used in rep area
                    usedCheckRow_sup=db((db.sm_supervisor_level.cid==cid) & (db.sm_supervisor_level.level_id==level_id)).select(db.sm_supervisor_level.sup_id,limitby=(0,1))       
                    if usedCheckRow_sup:
                        response.flash='Already used in Supervisor-Level'
                    else:
                        usedCheckRow_client=db((db.sm_client.cid==cid) & (db.sm_client.area_id==level_id)).select(db.sm_client.area_id,limitby=(0,1))       
                        if usedCheckRow_client:
                            response.flash='Already used in Customer'
                        else:
                            db((db.sm_level.cid==cid) & (db.sm_level.id==rowid) & (db.sm_level.level_id == level_id)).delete()
                            response.flash='Deleted Successfully'
        #update part
        elif btn_edit:
            #----------
            level_name=str(request.vars.level_name).strip().upper()
            level_name=check_special_char(level_name)
            
            territory_des=str(request.vars.territory_des).strip().upper()
            if territory_des=='NONE':
                territory_des=''
            else:
                territory_des=check_special_char(territory_des)
                
            special_territory_code=str(request.vars.special_territory_code).strip().upper()
            if special_territory_code=='NONE':
                special_territory_code=''
            else:
                special_territory_code=check_special_char_id(special_territory_code)
            #----
            
            
            checkRowLevel=db((db.sm_level.cid==cid) & (db.sm_level.level_id==level_id)).select(db.sm_level.depth,limitby=(0,1))
            if not checkRowLevel:
                response.flash='Invalid request'
            else:
                level_depth=checkRowLevel[0].depth
                
                rows_check2=db((db.sm_level.cid==cid)& (db.sm_level.id!=rowid) & (db.sm_level.level_name==level_name)).select(db.sm_level.level_id,limitby=(0,1))
                if rows_check2:
                    response.flash='Level Name already exist, please choose a new'
                else:
                    db((db.sm_level.cid==cid) & (db.sm_level.id == rowid)).update(level_name=level_name,territory_des=territory_des,special_territory_code=special_territory_code)
                    db((db.sm_level.cid==cid) & (db.sm_level.parent_level_id == level_id)).update(parent_level_name=level_name)
                    db.executesql("update sm_level set level"+str(level_depth)+"_name='"+str(level_name)+"' where cid = '" + str(cid) +"' and level"+str(level_depth)+"='"+ str(level_id)+"'") 
                    
                    db((db.sm_rep_area.cid==cid) & (db.sm_rep_area.area_id == level_id)).update(area_name=level_name)
                    db((db.sm_supervisor_level.cid==cid) & (db.sm_supervisor_level.level_id==level_id)).update(level_name=level_name)
                    
                    response.flash='Updated successfully'
    
    # ==================================== show records
    records=db((db.sm_level.cid==cid)&(db.sm_level.parent_level_id==parentLevelId)).select(db.sm_level.ALL,orderby=db.sm_level.level_id) 
    
    #=============== Billal (for auto level code/ID)
    # Starting Code get from levle name settings that is starting with a character(a-z)
    setLevelId=''
    firstChar=''
    codeLength=0
    levelSettings=db((db.level_name_settings.cid==cid)&(db.level_name_settings.depth==depth)).select(db.level_name_settings.starting_code,limitby=(0,1))
    if levelSettings:
        setLevelId=str(levelSettings[0].starting_code).upper()
        firstChar=str(setLevelId[0:1]).strip()
        codeLength=len(setLevelId[1:])
    
    
    #----------- 
    levelCodeRow=db((db.sm_level.cid==cid)&(db.sm_level.depth==depth)).select(db.sm_level.level_id,orderby=~db.sm_level.level_id,limitby=(0,1))
    if levelCodeRow:            
        try:
            if str(levelCodeRow[0].level_id)[0:1]==firstChar and len(str(levelCodeRow[0].level_id)[1:])==codeLength:
                level_idStr=str(levelCodeRow[0].level_id)[1:]
                maxLevelID=int(level_idStr)+1
                setLevelId=firstChar+str(maxLevelID).zfill(codeLength)                
        except:
            pass
    #================ end Billal
    
    return dict(form=form,records=records,parentLevelId=parentLevelId,is_leaf=is_leaf,setLevelId=setLevelId,access_permission=access_permission,access_permission_view=access_permission_view,depth=depth,level0=level0,level0_name=level0_name,level1=level1,level1_name=level1_name,level2=level2,level2_name=level2_name,
                level3=level3,level3_name=level3_name,level4=level4,level4_name=level4_name,level5=level5,level5_name=level5_name,level6=level6,level6_name=level6_name,level7=level7,level7_name=level7_name)    


def level_back_button():
    task_id='rm_workingarea_manage'
    task_id_view='rm_workingarea_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    
    levelId= request.args(0)
    cid=session.cid
    
    records_parent=db((db.sm_level.cid==cid) & (db.sm_level.level_id==levelId)).select(db.sm_level.parent_level_id,limitby=(0,1))
    parentLevelId=''
    if not records_parent :
        session.flash='Invalid request'
    else:
        parentLevelId=records_parent[0].parent_level_id 
    
    redirect (URL(c='level',f='level',args=[parentLevelId]))


#=============================== Area List
def area_list():
    c_id=session.cid
    response.title='Working Area'
   #----------Task assaign----------
    task_id='rm_workingarea_manage'
    task_id_view='rm_workingarea_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    #---------------------------
    if session.showLevelForDepot=='YES':# if admin user
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging
    
    parentRecords=db((db.sm_level.cid==c_id)&(db.sm_level.is_leaf=='0')).select(db.sm_level.level_id,db.sm_level.level_name)
    
    records=db((db.sm_level.cid==c_id)&(db.sm_level.is_leaf=='1')&(db.sm_level.depot_id==session.depot_id)).select(db.sm_level.ALL,orderby=db.sm_level.level_name,limitby=limitby)
    
    return dict(records=records,parentRecords=parentRecords,page=page,items_per_page=items_per_page)



def download_level():
    c_id=session.cid
    records=''
    myString='Area Structure\n\n'
    myString+=session.level0Name+','+session.level1Name+','+session.level2Name+','+session.level3Name+','+session.level4Name+','+session.level5Name+','+session.level6Name+','+session.level7Name+'\n'
    
    levelList=[]
    levelRecords=db(db.sm_level.cid==c_id).select(db.sm_level.ALL,orderby=db.sm_level.level_name)
    levelList=levelRecords.as_list()
    
    records1=db((db.sm_level.cid==c_id)&(db.sm_level.parent_level_id=='0')).select(db.sm_level.ALL,orderby=db.sm_level.level_name)
    for row1 in records1:
        level_id_1=row1.level_id
        level_name_1=row1.level_name
        
        myString+=str(level_name_1)+'-'+str(level_id_1)+'\n'
        
        for i in range(len(levelList)):
            levelData=levelList[i]
            level_id_2=levelData['level_id']
            level_name_2=levelData['level_name']
            territory_des_2=levelData['territory_des']
            special_territory_code_2=levelData['special_territory_code']
            parent_level_id_2=levelData['parent_level_id']
            if (parent_level_id_2==level_id_1):    
                myString+=','+str(level_name_2)+'-'+str(level_id_2)+','+str(territory_des_2)+','+str(special_territory_code_2)+'\n'
                
                for i in range(len(levelList)):
                    levelData=levelList[i]
                    level_id_3=levelData['level_id']
                    level_name_3=levelData['level_name']
                    territory_des_3=levelData['territory_des']
                    special_territory_code_3=levelData['special_territory_code']
                    parent_level_id_3=levelData['parent_level_id']
                    if (parent_level_id_3==level_id_2):    
                        myString+=',,'+str(level_name_3)+'-'+str(level_id_3)+','+str(territory_des_3)+','+str(special_territory_code_3)+'\n'

                        for i in range(len(levelList)):
                            levelData=levelList[i]
                            level_id_4=levelData['level_id']
                            level_name_4=levelData['level_name']
                            territory_des_4=levelData['territory_des']
                            special_territory_code_4=levelData['special_territory_code']
                            parent_level_id_4=levelData['parent_level_id']
                            if (parent_level_id_4==level_id_3):    
                                myString+=',,,'+str(level_name_4)+'-'+str(level_id_4)+','+str(territory_des_4)+','+str(special_territory_code_4)+'\n'
                                
                                for i in range(len(levelList)):
                                    levelData=levelList[i]
                                    level_id_5=levelData['level_id']
                                    level_name_5=levelData['level_name']
                                    territory_des_5=levelData['territory_des']
                                    special_territory_code_5=levelData['special_territory_code']
                                    parent_level_id_5=levelData['parent_level_id']
                                    if (parent_level_id_5==level_id_4):    
                                        myString+=',,,,'+str(level_name_5)+'-'+str(level_id_5)+','+str(territory_des_5)+','+str(special_territory_code_5)+'\n'
                                        
                                        for i in range(len(levelList)):
                                            levelData=levelList[i]
                                            level_id_6=levelData['level_id']
                                            level_name_6=levelData['level_name']
                                            territory_des_6=levelData['territory_des']
                                            special_territory_code_6=levelData['special_territory_code']
                                            parent_level_id_6=levelData['parent_level_id']
                                            if (parent_level_id_6==level_id_5):    
                                                myString+=',,,,,'+str(level_name_6)+'-'+str(level_id_6)+','+str(territory_des_6)+','+str(special_territory_code_6)+'\n'
                                                
                                                for i in range(len(levelList)):
                                                    levelData=levelList[i]
                                                    level_id_7=levelData['level_id']
                                                    level_name_7=levelData['level_name']
                                                    territory_des_7=levelData['territory_des']
                                                    special_territory_code_7=levelData['special_territory_code']
                                                    parent_level_id_7=levelData['parent_level_id']
                                                    if (parent_level_id_7==level_id_6):    
                                                        myString+=',,,,,,'+str(level_name_7)+'-'+str(level_id_7)+','+str(territory_des_7)+','+str(special_territory_code_7)+'\n'
                                                
                                                
    #-----------                                
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_level.csv'   
    return str(myString)



def download_level_classic():
    c_id=session.cid
    records=''
    myString='Area Structure\n\n'
    myString+=session.level0Name+' Name,'+session.level0Name+' ID,'+session.level1Name+' Name,'+session.level1Name+' Code,'+session.level2Name+' Name,'+session.level2Name+' Code,'+session.level3Name+' Name,'+session.level3Name +'\n'
    
    
    max = db.sm_level.depth.max()
    maxDepth = db(db.sm_level.cid==c_id).select(max).first()[max]
    
    
    levelList=[]
    levelRecords=db(db.sm_level.cid==c_id).select(db.sm_level.ALL,orderby=db.sm_level.level_name)
    levelList=levelRecords.as_list()
    
    records1=db((db.sm_level.cid==c_id)&(db.sm_level.parent_level_id=='0')).select(db.sm_level.ALL,orderby=db.sm_level.level_name)
    for row1 in records1:
        level_id_1=row1.level_id
        level_name_1=row1.level_name
        
        if maxDepth==0:
            myString+=str(level_name_1)+','+str(level_id_1)+'\n'
        else:
            pass
        
        for i in range(len(levelList)):
            levelData=levelList[i]
            level_id_2=levelData['level_id']
            level_name_2=levelData['level_name']
            territory_des_2=levelData['territory_des']
            special_territory_code_2=levelData['special_territory_code']
            parent_level_id_2=levelData['parent_level_id']
            if (parent_level_id_2==level_id_1):    
                
                if maxDepth==1:
                    myString+=str(level_name_1)+','+str(level_id_1)+','+str(level_name_2)+','+str(level_id_2)+','+str(territory_des_2)+','+str(special_territory_code_2)+'\n'
                else:
                    pass
                
                for i in range(len(levelList)):
                    levelData=levelList[i]
                    level_id_3=levelData['level_id']
                    level_name_3=levelData['level_name']
                    territory_des_3=levelData['territory_des']
                    special_territory_code_3=levelData['special_territory_code']
                    parent_level_id_3=levelData['parent_level_id']
                    if (parent_level_id_3==level_id_2):
                        
                        if maxDepth==2: 
                            myString+=str(level_name_1)+','+str(level_id_1)+','+str(level_name_2)+','+str(level_id_2)+','+str(level_name_3)+','+str(level_id_3)+','+str(territory_des_3)+','+str(special_territory_code_3)+'\n'
                        else:
                            pass
                        
                        for i in range(len(levelList)):
                            levelData=levelList[i]
                            level_id_4=levelData['level_id']
                            level_name_4=levelData['level_name']
                            territory_des_4=levelData['territory_des']
                            special_territory_code_4=levelData['special_territory_code']
                            parent_level_id_4=levelData['parent_level_id']
                            if (parent_level_id_4==level_id_3):    
                                
                                if maxDepth==3:
                                    myString+=str(level_name_1)+','+str(level_id_1)+','+str(level_name_2)+','+str(level_id_2)+','+str(level_name_3)+','+str(level_id_3)+','+str(level_name_4)+','+str(level_id_4)+','+str(territory_des_4)+','+str(special_territory_code_4)+'\n'
                                else:
                                    pass
                            
                                for i in range(len(levelList)):
                                    levelData=levelList[i]
                                    level_id_5=levelData['level_id']
                                    level_name_5=levelData['level_name']
                                    territory_des_5=levelData['territory_des']
                                    special_territory_code_5=levelData['special_territory_code']
                                    parent_level_id_5=levelData['parent_level_id']
                                    if (parent_level_id_5==level_id_4):    
                                        
                                        if maxDepth==4:
                                            myString+=str(level_name_1)+','+str(level_id_1)+','+str(level_name_2)+','+str(level_id_2)+','+str(level_name_3)+','+str(level_id_3)+','+str(level_name_4)+','+str(level_id_4)+','+str(level_name_5)+','+str(level_id_5)+','+str(territory_des_5)+','+str(special_territory_code_5)+'\n'
                                        else:
                                            pass
                                
                                        for i in range(len(levelList)):
                                            levelData=levelList[i]
                                            level_id_6=levelData['level_id']
                                            level_name_6=levelData['level_name']
                                            territory_des_6=levelData['territory_des']
                                            special_territory_code_6=levelData['special_territory_code']
                                            parent_level_id_6=levelData['parent_level_id']
                                            if (parent_level_id_6==level_id_5):  
                                                
                                                if maxDepth==5:  
                                                    myString+=str(level_name_1)+','+str(level_id_1)+','+str(level_name_2)+','+str(level_id_2)+','+str(level_name_3)+','+str(level_id_3)+','+str(level_name_4)+','+str(level_id_4)+','+str(level_name_5)+','+str(level_id_5)+','+str(level_name_6)+','+str(level_id_6)+','+str(territory_des_6)+','+str(special_territory_code_6)+'\n'
                                                else:
                                                    pass
                                
                                                for i in range(len(levelList)):
                                                    levelData=levelList[i]
                                                    level_id_7=levelData['level_id']
                                                    level_name_7=levelData['level_name']
                                                    territory_des_7=levelData['territory_des']
                                                    special_territory_code_7=levelData['special_territory_code']
                                                    parent_level_id_7=levelData['parent_level_id']
                                                    if (parent_level_id_7==level_id_6):
                                                        
                                                        if maxDepth==6: 
                                                            myString+=str(level_name_1)+','+str(level_id_1)+','+str(level_name_2)+','+str(level_id_2)+','+str(level_name_3)+','+str(level_id_3)+','+str(level_name_4)+','+str(level_id_4)+','+str(level_name_5)+','+str(level_id_5)+','+str(level_name_6)+','+str(level_id_6)+','+str(level_name_7)+','+str(level_id_7)+','+str(territory_des_7)+','+str(special_territory_code_7)+'\n'
                                                        else:
                                                            pass
                                                
    #-----------                                
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_working_area_classic.csv'   
    return str(myString)
#def download_level():
#    c_id=session.cid
#    records=''
#    myString='Working Area\n'
#    
#    levelList=[]
#    levelRecords=db(db.sm_level.cid==c_id).select(db.sm_level.ALL,orderby=db.sm_level.level_name)
#    levelList=levelRecords.as_list()
#    
#    records1=db((db.sm_level.cid==c_id)&(db.sm_level.parent_level_id=='0')).select(db.sm_level.ALL,orderby=db.sm_level.level_name)
#    for row1 in records1:
#        level_id_1=row1.level_id
#        level_name_1=row1.level_name
#        
#        myString+=str(level_name_1)+'-'+str(level_id_1)+'\n'
#        
#        for i in range(len(levelList)):
#            levelData=levelList[i]
#            level_id_2=levelData['level_id']
#            level_name_2=str(levelData['level_name']).replace(',', ';')
#            parent_level_id_2=levelData['parent_level_id']
#            if (parent_level_id_2==level_id_1):    
#                myString+=','+str(level_name_2)+'-'+str(level_id_2)+'\n'
#                
#                for i in range(len(levelList)):
#                    levelData=levelList[i]
#                    level_id_3=levelData['level_id']
#                    level_name_3=str(levelData['level_name']).replace(',', ';')
#                    parent_level_id_3=levelData['parent_level_id']
#                    if (parent_level_id_3==level_id_2):    
#                        myString+=',,'+str(level_name_3)+'-'+str(level_id_3)+'\n'
#
#                        for i in range(len(levelList)):
#                            levelData=levelList[i]
#                            level_id_4=levelData['level_id']
#                            level_name_4=str(levelData['level_name']).replace(',', ';')
#                            parent_level_id_4=levelData['parent_level_id']
#                            if (parent_level_id_4==level_id_3):    
#                                myString+=',,,'+str(level_name_4)+'-'+str(level_id_4)+'\n'
#                                
#                                for i in range(len(levelList)):
#                                    levelData=levelList[i]
#                                    level_id_5=levelData['level_id']
#                                    level_name_5=str(levelData['level_name']).replace(',', ';')
#                                    parent_level_id_5=levelData['parent_level_id']
#                                    if (parent_level_id_5==level_id_4):    
#                                        myString+=',,,,'+str(level_name_5)+'-'+str(level_id_5)+'\n'
#                                        
#                                        for i in range(len(levelList)):
#                                            levelData=levelList[i]
#                                            level_id_6=levelData['level_id']
#                                            level_name_6=str(levelData['level_name']).replace(',', ';')
#                                            parent_level_id_6=levelData['parent_level_id']
#                                            if (parent_level_id_6==level_id_5):    
#                                                myString+=',,,,,'+str(level_name_6)+'-'+str(level_id_6)+'\n'
#                                                
#                                                for i in range(len(levelList)):
#                                                    levelData=levelList[i]
#                                                    level_id_7=levelData['level_id']
#                                                    level_name_7=str(levelData['level_name']).replace(',', ';')
#                                                    parent_level_id_7=levelData['parent_level_id']
#                                                    if (parent_level_id_7==level_id_6):    
#                                                        myString+=',,,,,,'+str(level_name_7)+'-'+str(level_id_7)+'\n'
#                                                
#                                                
#    #-----------                                
#    import gluon.contenttype
#    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
#    response.headers['Content-disposition'] = 'attachment; filename=download_level.csv'   
#    return str(myString)
#
#
#def download_level_classic():
#    c_id=session.cid
#    records=''
#    myString='Working Area\n\n'
#    myString+='Level0 Name,Level0 Code,Level1 Name,Level1 Code,Level2 Name, Level2 Code,Level3 Name,Level3 Code\n'
#    
#    
#    max = db.sm_level.depth.max()
#    maxDepth = db(db.sm_level.cid==c_id).select(max).first()[max]
#    
#        
#    levelList=[]
#    levelRecords=db(db.sm_level.cid==c_id).select(db.sm_level.ALL,orderby=db.sm_level.level_name)
#    levelList=levelRecords.as_list()
#    
#    records1=db((db.sm_level.cid==c_id)&(db.sm_level.parent_level_id=='0')).select(db.sm_level.ALL,orderby=db.sm_level.level_name)
#    for row1 in records1:
#        level_id_1=row1.level_id
#        level_name_1=row1.level_name
#        
#        if maxDepth==0:
#            myString+=str(level_name_1)+','+str(level_id_1)+'\n'
#        else:
#            pass
#        
#        for i in range(len(levelList)):
#            levelData=levelList[i]
#            level_id_2=levelData['level_id']
#            level_name_2=str(levelData['level_name']).replace(',', ';')
#            parent_level_id_2=levelData['parent_level_id']
#            if (parent_level_id_2==level_id_1):    
#                
#                if maxDepth==1:
#                    myString+=str(level_name_1)+','+str(level_id_1)+','+str(level_name_2)+','+str(level_id_2)+'\n'
#                else:
#                    pass
#                
#                for i in range(len(levelList)):
#                    levelData=levelList[i]
#                    level_id_3=levelData['level_id']
#                    level_name_3=str(levelData['level_name']).replace(',', ';')
#                    parent_level_id_3=levelData['parent_level_id']
#                    if (parent_level_id_3==level_id_2):
#                        
#                        if maxDepth==2: 
#                            myString+=str(level_name_1)+','+str(level_id_1)+','+str(level_name_2)+','+str(level_id_2)+','+str(level_name_3)+','+str(level_id_3)+'\n'
#                        else:
#                            pass
#                        
#                        for i in range(len(levelList)):
#                            levelData=levelList[i]
#                            level_id_4=levelData['level_id']
#                            level_name_4=str(levelData['level_name']).replace(',', ';')
#                            parent_level_id_4=levelData['parent_level_id']
#                            if (parent_level_id_4==level_id_3):    
#                                
#                                if maxDepth==3:
#                                    myString+=str(level_name_1)+','+str(level_id_1)+','+str(level_name_2)+','+str(level_id_2)+','+str(level_name_3)+','+str(level_id_3)+','+str(level_name_4)+','+str(level_id_4)+'\n'
#                                else:
#                                    pass
#                            
#                                for i in range(len(levelList)):
#                                    levelData=levelList[i]
#                                    level_id_5=levelData['level_id']
#                                    level_name_5=str(levelData['level_name']).replace(',', ';')
#                                    parent_level_id_5=levelData['parent_level_id']
#                                    if (parent_level_id_5==level_id_4):    
#                                        
#                                        if maxDepth==4:
#                                            myString+=str(level_name_1)+','+str(level_id_1)+','+str(level_name_2)+','+str(level_id_2)+','+str(level_name_3)+','+str(level_id_3)+','+str(level_name_4)+','+str(level_id_4)+','+str(level_name_5)+','+str(level_id_5)+'\n'
#                                        else:
#                                            pass
#                                
#                                        for i in range(len(levelList)):
#                                            levelData=levelList[i]
#                                            level_id_6=levelData['level_id']
#                                            level_name_6=str(levelData['level_name']).replace(',', ';')
#                                            parent_level_id_6=levelData['parent_level_id']
#                                            if (parent_level_id_6==level_id_5):  
#                                                
#                                                if maxDepth==5:  
#                                                    myString+=str(level_name_1)+','+str(level_id_1)+','+str(level_name_2)+','+str(level_id_2)+','+str(level_name_3)+','+str(level_id_3)+','+str(level_name_4)+','+str(level_id_4)+','+str(level_name_5)+','+str(level_id_5)+','+str(level_name_6)+','+str(level_id_6)+'\n'
#                                                else:
#                                                    pass
#                                
#                                                for i in range(len(levelList)):
#                                                    levelData=levelList[i]
#                                                    level_id_7=levelData['level_id']
#                                                    level_name_7=str(levelData['level_name']).replace(',', ';')
#                                                    parent_level_id_7=levelData['parent_level_id']
#                                                    if (parent_level_id_7==level_id_6):
#                                                        
#                                                        if maxDepth==6: 
#                                                            myString+=str(level_name_1)+','+str(level_id_1)+','+str(level_name_2)+','+str(level_id_2)+','+str(level_name_3)+','+str(level_id_3)+','+str(level_name_4)+','+str(level_id_4)+','+str(level_name_5)+','+str(level_id_5)+','+str(level_name_6)+','+str(level_id_6)+','+str(level_name_7)+','+str(level_id_7)+'\n'
#                                                        else:
#                                                            pass
#                                                
#    #-----------                                
#    import gluon.contenttype
#    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
#    response.headers['Content-disposition'] = 'attachment; filename=download_working_area_classic.csv'   
#    return str(myString)




##-----------------------------area tree 

def level_search():    
    
    level_search=str(request.vars.level_search).strip().upper()
    session.level_search=level_search
    parentID=request.args(0) 
    
    if (level_search!=''):
        searchValue=str(level_search).split('|')[0]
        
        level_check=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id==searchValue)).select(db.sm_level.parent_level_id,limitby=(0,1))
        if level_check:
            parentID=level_check[0].parent_level_id
            
            redirect (URL(c='level',f='level',args=[parentID]))
            
        else:
            session.flash = 'Invalid level ID '+str(searchValue)
            redirect (URL(c='level',f='level',args=[parentID]))
    else:
        session.flash = 'Required level ID '
        redirect (URL(c='level',f='level',args=[parentID]))

#level bathch uplaod with depot
def level_batch_upload():
    task_id='rm_workingarea_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    response.title='Level Batch upload'
    
    c_id=session.cid
    uploadDepth=request.vars.uploadDepth
    
    if (uploadDepth=='' or uploadDepth==None):
        session.flash='Need Depth value'
        redirect (URL(c='utility_mrep',f='utility'))
    
    btn_upload=request.vars.btn_upload    
    count_inserted=0
    count_error=0
    error_str=''
    total_row=0
    if btn_upload=='Upload':        
        excel_data=str(request.vars.excel_data)
        inserted_count=0
        error_count=0
        error_list=[]
        row_list=excel_data.split( '\n')
        total_row=len(row_list)
        
        depot_list_exist=[]

        ins_list=[]
        ins_dict={}
        
        #--------------- depth check
        firstDpth=False
        lastDpth=False
        middleDepth=False
        if int(uploadDepth)==0:
            firstDpth=True
        else:
            settDepth=0
            settDpthRows=db((db.sm_settings.cid==c_id) & (db.sm_settings.s_key=='LEVEL_DEPTH')).select(db.sm_settings.s_value,limitby=(0,1))
            if settDpthRows:
                settDepth=int(settDpthRows[0].s_value)
            
            if int(uploadDepth)==settDepth:
                lastDpth=True
            else:
                middleDepth==True
                
        #---------- valid depot list                            
        depotRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.status=='ACTIVE')).select(db.sm_depot.depot_id,orderby=db.sm_depot.depot_id)
        depot_list_exist=depotRows.as_list()
        
        #   --------------------     
        for i in range(total_row):
            if i>=100:
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')            
            
            if len(coloum_list)==4:
                level_ID_excel=check_special_char_id(str(coloum_list[0]).strip().upper())
                level_Name_excel=check_special_char(str(coloum_list[1]).strip().upper())
                plevel_ID_excel=check_special_char_id(str(coloum_list[2]).strip().upper())
                depotID_excel=str(coloum_list[3]).strip().upper()
                
                depotIdvalue='-'
                isLeaf='0'
                
                try:
                    fieldValFlag=True
                    valid_depot=False
                    
                    if firstDpth==True:
                        if level_ID_excel=='' or level_Name_excel=='':
                            fieldValFlag=False
                        else:
                            plevel_ID_excel='0'
                            
                    elif middleDepth==True:
                        if level_ID_excel=='' or level_Name_excel=='' or plevel_ID_excel=='':
                            fieldValFlag=False
                    
                    elif lastDpth==True:
                        if level_ID_excel=='' or level_Name_excel=='' or plevel_ID_excel=='':# or depotID_excel==''
                            fieldValFlag=False
                        else:
                            for i in range(len(depot_list_exist)):
                                myRowData=depot_list_exist[i]                                
                                depot_id=myRowData['depot_id']                        
                                if (str(depot_id).strip()==str(depotID_excel).strip()):
                                    valid_depot=True
                                    depotIdvalue=depot_id
                                    break
                            isLeaf='1'
                    
                    #-----------------
                    if fieldValFlag==True:
                        if (lastDpth==True and valid_depot==False):
                            error_data=row_data+'(Invalid Depot ID)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:                        
                            #------------------------------- Depth 0
                            if int(uploadDepth)==0:
                                level_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==level_ID_excel)).select(db.sm_level.level_id,limitby=(0,1))
                                if not level_rows:                                                                
                                    db.sm_level.insert(cid=c_id,level_id=level_ID_excel,level_name=level_Name_excel,parent_level_id=plevel_ID_excel,parent_level_name='',is_leaf=isLeaf,depot_id=depotIdvalue,depth=uploadDepth,level0=level_ID_excel,level0_name=level_Name_excel)         
                                    count_inserted+=1
                                    continue
                                else:
                                    error_data=row_data+'(Already Exist)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                            
                            #------------------------------ Depth 1 
                            elif int(uploadDepth)==1:                                
                                level_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==level_ID_excel)).select(db.sm_level.level_id,limitby=(0,1))
                                if not level_rows:
                                    parent_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==plevel_ID_excel)).select(db.sm_level.level0,db.sm_level.level0_name,limitby=(0,1))
                                    if parent_rows:
                                        level0=parent_rows[0].level0
                                        level0_name=parent_rows[0].level0_name
                                        
                                        db.sm_level.insert(cid=c_id,level_id=level_ID_excel,level_name=level_Name_excel,parent_level_id=plevel_ID_excel,parent_level_name=level0_name,is_leaf=isLeaf,depot_id=depotIdvalue,depth=uploadDepth,level0=level0,level0_name=level0_name,level1=level_ID_excel,level1_name=level_Name_excel)         
                                        count_inserted+=1
                                        continue
                                        
                                    else:
                                        error_data=row_data+'(Invalid Patent ID)\n'
                                        error_str=error_str+error_data
                                        count_error+=1
                                        continue
                                else:
                                    error_data=row_data+'(Already Exist)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                            
                            #------------------------------ Depth 2 
                            elif int(uploadDepth)==2:                                
                                level_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==level_ID_excel)).select(db.sm_level.level_id,limitby=(0,1))
                                if not level_rows:
                                    parent_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==plevel_ID_excel)).select(db.sm_level.level0,db.sm_level.level0_name,db.sm_level.level1,db.sm_level.level1_name,limitby=(0,1))
                                    if parent_rows:
                                        level0=parent_rows[0].level0
                                        level0_name=parent_rows[0].level0_name
                                        level1=parent_rows[0].level1
                                        level1_name=parent_rows[0].level1_name
                                        
                                        db.sm_level.insert(cid=c_id,level_id=level_ID_excel,level_name=level_Name_excel,parent_level_id=plevel_ID_excel,parent_level_name=level1_name,is_leaf=isLeaf,depot_id=depotIdvalue,depth=uploadDepth,level0=level0,level0_name=level0_name,level1=level1,level1_name=level1_name,level2=level_ID_excel,level2_name=level_Name_excel)         
                                        count_inserted+=1
                                        continue
                                        
                                    else:
                                        error_data=row_data+'(Invalid Patent ID)\n'
                                        error_str=error_str+error_data
                                        count_error+=1
                                        continue
                                else:
                                    error_data=row_data+'(Already Exist)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                            
                            #------------------------------ Depth 3 
                            elif int(uploadDepth)==3:                                
                                level_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==level_ID_excel)).select(db.sm_level.level_id,limitby=(0,1))
                                if not level_rows:
                                    parent_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==plevel_ID_excel)).select(db.sm_level.level0,db.sm_level.level0_name,db.sm_level.level1,db.sm_level.level1_name,db.sm_level.level2,db.sm_level.level2_name,limitby=(0,1))
                                    if parent_rows:
                                        level0=parent_rows[0].level0
                                        level0_name=parent_rows[0].level0_name
                                        level1=parent_rows[0].level1
                                        level1_name=parent_rows[0].level1_name
                                        level2=parent_rows[0].level2
                                        level2_name=parent_rows[0].level2_name
                                        
                                        db.sm_level.insert(cid=c_id,level_id=level_ID_excel,level_name=level_Name_excel,parent_level_id=plevel_ID_excel,parent_level_name=level2_name,is_leaf=isLeaf,depot_id=depotIdvalue,depth=uploadDepth,level0=level0,level0_name=level0_name,level1=level1,level1_name=level1_name,level2=level2,level2_name=level2_name,level3=level_ID_excel,level3_name=level_Name_excel)         
                                        count_inserted+=1
                                        continue
                                        
                                    else:
                                        error_data=row_data+'(Invalid Patent ID)\n'
                                        error_str=error_str+error_data
                                        count_error+=1
                                        continue
                                else:
                                    error_data=row_data+'(Already Exist)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                            
                            #------------------------------ Depth 4 
                            elif int(uploadDepth)==4:                                
                                level_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==level_ID_excel)).select(db.sm_level.level_id,limitby=(0,1))
                                if not level_rows:
                                    parent_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==plevel_ID_excel)).select(db.sm_level.level0,db.sm_level.level0_name,db.sm_level.level1,db.sm_level.level1_name,db.sm_level.level2,db.sm_level.level2_name,db.sm_level.level3,db.sm_level.level3_name,limitby=(0,1))
                                    if parent_rows:
                                        level0=parent_rows[0].level0
                                        level0_name=parent_rows[0].level0_name
                                        level1=parent_rows[0].level1
                                        level1_name=parent_rows[0].level1_name
                                        level2=parent_rows[0].level2
                                        level2_name=parent_rows[0].level2_name
                                        level3=parent_rows[0].level3
                                        level3_name=parent_rows[0].level3_name
                                        
                                        db.sm_level.insert(cid=c_id,level_id=level_ID_excel,level_name=level_Name_excel,parent_level_id=plevel_ID_excel,parent_level_name=level3_name,is_leaf=isLeaf,depot_id=depotIdvalue,depth=uploadDepth,level0=level0,level0_name=level0_name,level1=level1,level1_name=level1_name,level2=level2,level2_name=level2_name,level3=level3,level3_name=level3_name,level4=level_ID_excel,level4_name=level_Name_excel)         
                                        count_inserted+=1
                                        continue
                                        
                                    else:
                                        error_data=row_data+'(Invalid Patent ID)\n'
                                        error_str=error_str+error_data
                                        count_error+=1
                                        continue
                                else:
                                    error_data=row_data+'(Already Exist)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                            
                            #------------------------------ Depth 5 
                            elif int(uploadDepth)==5:                                
                                level_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==level_ID_excel)).select(db.sm_level.level_id,limitby=(0,1))
                                if not level_rows:
                                    parent_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==plevel_ID_excel)).select(db.sm_level.level0,db.sm_level.level0_name,db.sm_level.level1,db.sm_level.level1_name,db.sm_level.level2,db.sm_level.level2_name,db.sm_level.level3,db.sm_level.level3_name,db.sm_level.level4,db.sm_level.level4_name,limitby=(0,1))
                                    if parent_rows:
                                        level0=parent_rows[0].level0
                                        level0_name=parent_rows[0].level0_name
                                        level1=parent_rows[0].level1
                                        level1_name=parent_rows[0].level1_name
                                        level2=parent_rows[0].level2
                                        level2_name=parent_rows[0].level2_name
                                        level3=parent_rows[0].level3
                                        level3_name=parent_rows[0].level3_name
                                        level4=parent_rows[0].level4
                                        level4_name=parent_rows[0].level4_name
                                        
                                        db.sm_level.insert(cid=c_id,level_id=level_ID_excel,level_name=level_Name_excel,parent_level_id=plevel_ID_excel,parent_level_name=level4_name,is_leaf=isLeaf,depot_id=depotIdvalue,depth=uploadDepth,level0=level0,level0_name=level0_name,level1=level1,level1_name=level1_name,level2=level2,level2_name=level2_name,level3=level3,level3_name=level3_name,level4=level4,level4_name=level4_name,level5=level_ID_excel,level5_name=level_Name_excel)         
                                        count_inserted+=1
                                        continue
                                        
                                    else:
                                        error_data=row_data+'(Invalid Patent ID)\n'
                                        error_str=error_str+error_data
                                        count_error+=1
                                        continue
                                else:
                                    error_data=row_data+'(Already Exist)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                            
                            #------------------------------ Depth 6 
                            elif int(uploadDepth)==6:                                
                                level_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==level_ID_excel)).select(db.sm_level.level_id,limitby=(0,1))
                                if not level_rows:
                                    parent_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==plevel_ID_excel)).select(db.sm_level.level0,db.sm_level.level0_name,db.sm_level.level1,db.sm_level.level1_name,db.sm_level.level2,db.sm_level.level2_name,db.sm_level.level3,db.sm_level.level3_name,db.sm_level.level4,db.sm_level.level4_name,db.sm_level.level5,db.sm_level.level5_name,limitby=(0,1))
                                    if parent_rows:
                                        level0=parent_rows[0].level0
                                        level0_name=parent_rows[0].level0_name
                                        level1=parent_rows[0].level1
                                        level1_name=parent_rows[0].level1_name
                                        level2=parent_rows[0].level2
                                        level2_name=parent_rows[0].level2_name
                                        level3=parent_rows[0].level3
                                        level3_name=parent_rows[0].level3_name
                                        level4=parent_rows[0].level4
                                        level4_name=parent_rows[0].level4_name
                                        level5=parent_rows[0].level5
                                        level5_name=parent_rows[0].level5_name
                                        
                                        db.sm_level.insert(cid=c_id,level_id=level_ID_excel,level_name=level_Name_excel,parent_level_id=plevel_ID_excel,parent_level_name=level5_name,is_leaf=isLeaf,depot_id=depotIdvalue,depth=uploadDepth,level0=level0,level0_name=level0_name,level1=level1,level1_name=level1_name,level2=level2,level2_name=level2_name,level3=level3,level3_name=level3_name,level4=level4,level4_name=level4_name,level5=level5,level5_name=level5_name,level6=level_ID_excel,level6_name=level_Name_excel)         
                                        count_inserted+=1
                                        continue
                                        
                                    else:
                                        error_data=row_data+'(Invalid Patent ID)\n'
                                        error_str=error_str+error_data
                                        count_error+=1
                                        continue
                                else:
                                    error_data=row_data+'(Already Exist)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                            
                            #------------------------------ Depth 7 
                            elif int(uploadDepth)==7:                                
                                level_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==level_ID_excel)).select(db.sm_level.level_id,limitby=(0,1))
                                if not level_rows:
                                    parent_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==plevel_ID_excel)).select(db.sm_level.level0,db.sm_level.level0_name,db.sm_level.level1,db.sm_level.level1_name,db.sm_level.level2,db.sm_level.level2_name,db.sm_level.level3,db.sm_level.level3_name,db.sm_level.level4,db.sm_level.level4_name,db.sm_level.level5,db.sm_level.level5_name,db.sm_level.level6,db.sm_level.level6_name,limitby=(0,1))
                                    if parent_rows:
                                        level0=parent_rows[0].level0
                                        level0_name=parent_rows[0].level0_name
                                        level1=parent_rows[0].level1
                                        level1_name=parent_rows[0].level1_name
                                        level2=parent_rows[0].level2
                                        level2_name=parent_rows[0].level2_name
                                        level3=parent_rows[0].level3
                                        level3_name=parent_rows[0].level3_name
                                        level4=parent_rows[0].level4
                                        level4_name=parent_rows[0].level4_name
                                        level5=parent_rows[0].level5
                                        level5_name=parent_rows[0].level5_name
                                        level6=parent_rows[0].level6
                                        level6_name=parent_rows[0].level6_name
                                        
                                        db.sm_level.insert(cid=c_id,level_id=level_ID_excel,level_name=level_Name_excel,parent_level_id=plevel_ID_excel,parent_level_name=level6_name,is_leaf=isLeaf,depot_id=depotIdvalue,depth=uploadDepth,level0=level0,level0_name=level0_name,level1=level1,level1_name=level1_name,level2=level2,level2_name=level2_name,level3=level3,level3_name=level3_name,level4=level4,level4_name=level4_name,level5=level5,level5_name=level5_name,level6=level6,level6_name=level6_name,level7=level_ID_excel,level7_name=level_Name_excel)         
                                        count_inserted+=1
                                        continue
                                        
                                    else:
                                        error_data=row_data+'(Invalid Patent ID)\n'
                                        error_str=error_str+error_data
                                        count_error+=1
                                        continue
                                else:
                                    error_data=row_data+'(Already Exist)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                            
                            #------------------------------ Depth 8 
                            elif int(uploadDepth)==8:                                
                                level_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==level_ID_excel)).select(db.sm_level.level_id,limitby=(0,1))
                                if not level_rows:
                                    parent_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==plevel_ID_excel)).select(db.sm_level.level0,db.sm_level.level0_name,db.sm_level.level1,db.sm_level.level1_name,db.sm_level.level2,db.sm_level.level2_name,db.sm_level.level3,db.sm_level.level3_name,db.sm_level.level4,db.sm_level.level4_name,db.sm_level.level5,db.sm_level.level5_name,db.sm_level.level6,db.sm_level.level6_name,db.sm_level.level7,db.sm_level.level7_name,limitby=(0,1))
                                    if parent_rows:
                                        level0=parent_rows[0].level0
                                        level0_name=parent_rows[0].level0_name
                                        level1=parent_rows[0].level1
                                        level1_name=parent_rows[0].level1_name
                                        level2=parent_rows[0].level2
                                        level2_name=parent_rows[0].level2_name
                                        level3=parent_rows[0].level3
                                        level3_name=parent_rows[0].level3_name
                                        level4=parent_rows[0].level4
                                        level4_name=parent_rows[0].level4_name
                                        level5=parent_rows[0].level5
                                        level5_name=parent_rows[0].level5_name
                                        level6=parent_rows[0].level6
                                        level6_name=parent_rows[0].level6_name
                                        level7=parent_rows[0].level7
                                        level7_name=parent_rows[0].level7_name
                                        
                                        db.sm_level.insert(cid=c_id,level_id=level_ID_excel,level_name=level_Name_excel,parent_level_id=plevel_ID_excel,parent_level_name=level7_name,is_leaf=isLeaf,depot_id=depotIdvalue,depth=uploadDepth,level0=level0,level0_name=level0_name,level1=level1,level1_name=level1_name,level2=level2,level2_name=level2_name,level3=level3,level3_name=level3_name,level4=level4,level4_name=level4_name,level5=level5,level5_name=level5_name,level6=level6,level6_name=level6_name,level7=level7,level7_name=level7_name,level8=level_ID_excel,level8_name=level_Name_excel)         
                                        count_inserted+=1
                                        continue
                                    else:
                                        error_data=row_data+'(Invalid Patent ID)\n'
                                        error_str=error_str+error_data
                                        count_error+=1
                                        continue
                                else:
                                    error_data=row_data+'(Already Exist)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue                    
                    else:
                        error_data=row_data+'(Required value)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                except:
                    error_data=row_data+'(error in process!)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue                
            else:
                error_data=row_data+'(4 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
    
    return dict(count_inserted=count_inserted,uploadDepth=uploadDepth,count_error=count_error,error_str=error_str,total_row=total_row)
    

def level_batch_upload_without_depot():
    task_id='rm_workingarea_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    response.title='Level Batch upload'
    
    c_id=session.cid
    uploadDepth=request.vars.uploadDepth
    
    if (uploadDepth=='' or uploadDepth==None):
        session.flash='Need Depth value'
        redirect (URL(c='utility_mrep',f='utility'))
    
    btn_upload=request.vars.btn_upload    
    count_inserted=0
    count_error=0
    error_str=''
    total_row=0
    if btn_upload=='Upload':        
        excel_data=str(request.vars.excel_data)
        inserted_count=0
        error_count=0
        error_list=[]
        row_list=excel_data.split( '\n')
        total_row=len(row_list)
        
        depot_list_exist=[]

        ins_list=[]
        ins_dict={}
        
        #--------------- depth check
        firstDpth=False
        lastDpth=False
        middleDepth=False
        if int(uploadDepth)==0:
            firstDpth=True
        else:
            settDepth=0
            settDpthRows=db((db.sm_settings.cid==c_id) & (db.sm_settings.s_key=='LEVEL_DEPTH')).select(db.sm_settings.s_value,limitby=(0,1))
            if settDpthRows:
                settDepth=int(settDpthRows[0].s_value)
            
            if int(uploadDepth)==settDepth:
                lastDpth=True
            else:
                middleDepth==True
                
        #---------- valid depot list                            
#        depotRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.status=='ACTIVE')).select(db.sm_depot.depot_id,orderby=db.sm_depot.depot_id)
#        depot_list_exist=depotRows.as_list()
        
        #   --------------------     
        for i in range(total_row):
            if i>=100:
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')            
            
            if len(coloum_list)==3:
                level_ID_excel=check_special_char_id(str(coloum_list[0]).strip().upper())
                level_Name_excel=check_special_char(str(coloum_list[1]).strip().upper())
                plevel_ID_excel=check_special_char_id(str(coloum_list[2]).strip().upper())
                #depotID_excel=str(coloum_list[3]).strip().upper()
                
                depotIdvalue='-'
                isLeaf='0'
                
                try:
                    fieldValFlag=True
                    valid_depot=False
                    
                    if firstDpth==True:
                        if level_ID_excel=='' or level_Name_excel=='':
                            fieldValFlag=False
                        else:
                            plevel_ID_excel='0'
                            
                    elif middleDepth==True:
                        if level_ID_excel=='' or level_Name_excel=='' or plevel_ID_excel=='':
                            fieldValFlag=False
                    
                    elif lastDpth==True:
                        if level_ID_excel=='' or level_Name_excel=='' or plevel_ID_excel=='':# or depotID_excel==''
                            fieldValFlag=False
                        else:
#                            for i in range(len(depot_list_exist)):
#                                myRowData=depot_list_exist[i]                                
#                                depot_id=myRowData['depot_id']                        
#                                if (str(depot_id).strip()==str(depotID_excel).strip()):
#                                    valid_depot=True
#                                    depotIdvalue=depot_id
#                                    break
                            isLeaf='1'
                    
                    #-----------------
                    if fieldValFlag==True:
#                        if (lastDpth==True and valid_depot==False):
#                            error_data=row_data+'(Invalid Depot ID)\n'
#                            error_str=error_str+error_data
#                            count_error+=1
#                            continue
#                        else:
                        
                        #------------------------------- Depth 0
                        if int(uploadDepth)==0:
                            level_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==level_ID_excel)).select(db.sm_level.level_id,limitby=(0,1))
                            if not level_rows:                                                                
                                db.sm_level.insert(cid=c_id,level_id=level_ID_excel,level_name=level_Name_excel,parent_level_id=plevel_ID_excel,parent_level_name='',is_leaf=isLeaf,depot_id=depotIdvalue,depth=uploadDepth,level0=level_ID_excel,level0_name=level_Name_excel)         
                                count_inserted+=1
                                continue
                            else:
                                error_data=row_data+'(Already Exist)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                        
                        #------------------------------ Depth 1 
                        elif int(uploadDepth)==1:                                
                            level_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==level_ID_excel)).select(db.sm_level.level_id,limitby=(0,1))
                            if not level_rows:
                                parent_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==plevel_ID_excel)).select(db.sm_level.level0,db.sm_level.level0_name,limitby=(0,1))
                                if parent_rows:
                                    level0=parent_rows[0].level0
                                    level0_name=parent_rows[0].level0_name
                                    
                                    db.sm_level.insert(cid=c_id,level_id=level_ID_excel,level_name=level_Name_excel,parent_level_id=plevel_ID_excel,parent_level_name=level0_name,is_leaf=isLeaf,depot_id=depotIdvalue,depth=uploadDepth,level0=level0,level0_name=level0_name,level1=level_ID_excel,level1_name=level_Name_excel,)         
                                    count_inserted+=1
                                    continue
                                    
                                else:
                                    error_data=row_data+'(Invalid Patent ID)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                            else:
                                error_data=row_data+'(Already Exist)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                        
                        #------------------------------ Depth 2 
                        elif int(uploadDepth)==2:                                
                            level_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==level_ID_excel)).select(db.sm_level.level_id,limitby=(0,1))
                            if not level_rows:
                                parent_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==plevel_ID_excel)).select(db.sm_level.level0,db.sm_level.level0_name,db.sm_level.level1,db.sm_level.level1_name,limitby=(0,1))
                                if parent_rows:
                                    level0=parent_rows[0].level0
                                    level0_name=parent_rows[0].level0_name
                                    level1=parent_rows[0].level1
                                    level1_name=parent_rows[0].level1_name
                                    
                                    db.sm_level.insert(cid=c_id,level_id=level_ID_excel,level_name=level_Name_excel,parent_level_id=plevel_ID_excel,parent_level_name=level1_name,is_leaf=isLeaf,depot_id=depotIdvalue,depth=uploadDepth,level0=level0,level0_name=level0_name,level1=level1,level1_name=level1_name,level2=level_ID_excel,level2_name=level_Name_excel)         
                                    count_inserted+=1
                                    continue
                                    
                                else:
                                    error_data=row_data+'(Invalid Patent ID)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                            else:
                                error_data=row_data+'(Already Exist)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                        
                        #------------------------------ Depth 3 
                        elif int(uploadDepth)==3:                                
                            level_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==level_ID_excel)).select(db.sm_level.level_id,limitby=(0,1))
                            if not level_rows:
                                parent_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==plevel_ID_excel)).select(db.sm_level.level0,db.sm_level.level0_name,db.sm_level.level1,db.sm_level.level1_name,db.sm_level.level2,db.sm_level.level2_name,limitby=(0,1))
                                if parent_rows:
                                    level0=parent_rows[0].level0
                                    level0_name=parent_rows[0].level0_name
                                    level1=parent_rows[0].level1
                                    level1_name=parent_rows[0].level1_name
                                    level2=parent_rows[0].level2
                                    level2_name=parent_rows[0].level2_name
                                    
                                    db.sm_level.insert(cid=c_id,level_id=level_ID_excel,level_name=level_Name_excel,parent_level_id=plevel_ID_excel,parent_level_name=level2_name,is_leaf=isLeaf,depot_id=depotIdvalue,depth=uploadDepth,level0=level0,level0_name=level0_name,level1=level1,level1_name=level1_name,level2=level2,level2_name=level2_name,level3=level_ID_excel,level3_name=level_Name_excel)         
                                    count_inserted+=1
                                    continue
                                    
                                else:
                                    error_data=row_data+'(Invalid Patent ID)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                            else:
                                error_data=row_data+'(Already Exist)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                        
                        #------------------------------ Depth 4 
                        elif int(uploadDepth)==4:                                
                            level_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==level_ID_excel)).select(db.sm_level.level_id,limitby=(0,1))
                            if not level_rows:
                                parent_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==plevel_ID_excel)).select(db.sm_level.level0,db.sm_level.level0_name,db.sm_level.level1,db.sm_level.level1_name,db.sm_level.level2,db.sm_level.level2_name,db.sm_level.level3,db.sm_level.level3_name,limitby=(0,1))
                                if parent_rows:
                                    level0=parent_rows[0].level0
                                    level0_name=parent_rows[0].level0_name
                                    level1=parent_rows[0].level1
                                    level1_name=parent_rows[0].level1_name
                                    level2=parent_rows[0].level2
                                    level2_name=parent_rows[0].level2_name
                                    level3=parent_rows[0].level3
                                    level3_name=parent_rows[0].level3_name
                                    
                                    db.sm_level.insert(cid=c_id,level_id=level_ID_excel,level_name=level_Name_excel,parent_level_id=plevel_ID_excel,parent_level_name=level3_name,is_leaf=isLeaf,depot_id=depotIdvalue,depth=uploadDepth,level0=level0,level0_name=level0_name,level1=level1,level1_name=level1_name,level2=level2,level2_name=level2_name,level3=level3,level3_name=level3_name,level4=level_ID_excel,level4_name=level_Name_excel)         
                                    count_inserted+=1
                                    continue
                                    
                                else:
                                    error_data=row_data+'(Invalid Patent ID)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                            else:
                                error_data=row_data+'(Already Exist)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                        
                        #------------------------------ Depth 5 
                        elif int(uploadDepth)==5:                                
                            level_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==level_ID_excel)).select(db.sm_level.level_id,limitby=(0,1))
                            if not level_rows:
                                parent_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==plevel_ID_excel)).select(db.sm_level.level0,db.sm_level.level0_name,db.sm_level.level1,db.sm_level.level1_name,db.sm_level.level2,db.sm_level.level2_name,db.sm_level.level3,db.sm_level.level3_name,db.sm_level.level4,db.sm_level.level4_name,limitby=(0,1))
                                if parent_rows:
                                    level0=parent_rows[0].level0
                                    level0_name=parent_rows[0].level0_name
                                    level1=parent_rows[0].level1
                                    level1_name=parent_rows[0].level1_name
                                    level2=parent_rows[0].level2
                                    level2_name=parent_rows[0].level2_name
                                    level3=parent_rows[0].level3
                                    level3_name=parent_rows[0].level3_name
                                    level4=parent_rows[0].level4
                                    level4_name=parent_rows[0].level4_name
                                    
                                    db.sm_level.insert(cid=c_id,level_id=level_ID_excel,level_name=level_Name_excel,parent_level_id=plevel_ID_excel,parent_level_name=level4_name,is_leaf=isLeaf,depot_id=depotIdvalue,depth=uploadDepth,level0=level0,level0_name=level0_name,level1=level1,level1_name=level1_name,level2=level2,level2_name=level2_name,level3=level3,level3_name=level3_name,level4=level4,level4_name=level4_name,level5=level_ID_excel,level5_name=level_Name_excel)         
                                    count_inserted+=1
                                    continue
                                    
                                else:
                                    error_data=row_data+'(Invalid Patent ID)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                            else:
                                error_data=row_data+'(Already Exist)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                        
                        #------------------------------ Depth 6 
                        elif int(uploadDepth)==6:                                
                            level_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==level_ID_excel)).select(db.sm_level.level_id,limitby=(0,1))
                            if not level_rows:
                                parent_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==plevel_ID_excel)).select(db.sm_level.level0,db.sm_level.level0_name,db.sm_level.level1,db.sm_level.level1_name,db.sm_level.level2,db.sm_level.level2_name,db.sm_level.level3,db.sm_level.level3_name,db.sm_level.level4,db.sm_level.level4_name,db.sm_level.level5,db.sm_level.level5_name,limitby=(0,1))
                                if parent_rows:
                                    level0=parent_rows[0].level0
                                    level0_name=parent_rows[0].level0_name
                                    level1=parent_rows[0].level1
                                    level1_name=parent_rows[0].level1_name
                                    level2=parent_rows[0].level2
                                    level2_name=parent_rows[0].level2_name
                                    level3=parent_rows[0].level3
                                    level3_name=parent_rows[0].level3_name
                                    level4=parent_rows[0].level4
                                    level4_name=parent_rows[0].level4_name
                                    level5=parent_rows[0].level5
                                    level5_name=parent_rows[0].level5_name
                                    
                                    db.sm_level.insert(cid=c_id,level_id=level_ID_excel,level_name=level_Name_excel,parent_level_id=plevel_ID_excel,parent_level_name=level5_name,is_leaf=isLeaf,depot_id=depotIdvalue,depth=uploadDepth,level0=level0,level0_name=level0_name,level1=level1,level1_name=level1_name,level2=level2,level2_name=level2_name,level3=level3,level3_name=level3_name,level4=level4,level4_name=level4_name,level5=level5,level5_name=level5_name,level6=level_ID_excel,level6_name=level_Name_excel)         
                                    count_inserted+=1
                                    continue
                                    
                                else:
                                    error_data=row_data+'(Invalid Patent ID)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                            else:
                                error_data=row_data+'(Already Exist)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                        
                        #------------------------------ Depth 7
                        elif int(uploadDepth)==7:
                            level_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==level_ID_excel)).select(db.sm_level.level_id,limitby=(0,1))
                            if not level_rows:
                                parent_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==plevel_ID_excel)).select(db.sm_level.level0,db.sm_level.level0_name,db.sm_level.level1,db.sm_level.level1_name,db.sm_level.level2,db.sm_level.level2_name,db.sm_level.level3,db.sm_level.level3_name,db.sm_level.level4,db.sm_level.level4_name,db.sm_level.level5,db.sm_level.level5_name,db.sm_level.level6,db.sm_level.level6_name,limitby=(0,1))
                                if parent_rows:
                                    level0=parent_rows[0].level0
                                    level0_name=parent_rows[0].level0_name
                                    level1=parent_rows[0].level1
                                    level1_name=parent_rows[0].level1_name
                                    level2=parent_rows[0].level2
                                    level2_name=parent_rows[0].level2_name
                                    level3=parent_rows[0].level3
                                    level3_name=parent_rows[0].level3_name
                                    level4=parent_rows[0].level4
                                    level4_name=parent_rows[0].level4_name
                                    level5=parent_rows[0].level5
                                    level5_name=parent_rows[0].level5_name
                                    level6=parent_rows[0].level6
                                    level6_name=parent_rows[0].level6_name
                                    
                                    db.sm_level.insert(cid=c_id,level_id=level_ID_excel,level_name=level_Name_excel,parent_level_id=plevel_ID_excel,parent_level_name=level6_name,is_leaf=isLeaf,depot_id=depotIdvalue,depth=uploadDepth,level0=level0,level0_name=level0_name,level1=level1,level1_name=level1_name,level2=level2,level2_name=level2_name,level3=level3,level3_name=level3_name,level4=level4,level4_name=level4_name,level5=level5,level5_name=level5_name,level6=level6,level6_name=level6_name,level7=level_ID_excel,level7_name=level_Name_excel)         
                                    count_inserted+=1
                                    continue
                                else:
                                    error_data=row_data+'(Invalid Patent ID)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                            else:
                                error_data=row_data+'(Already Exist)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                        
                        #------------------------------ Depth 8
                        elif int(uploadDepth)==8:
                            level_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==level_ID_excel)).select(db.sm_level.level_id,limitby=(0,1))
                            if not level_rows:
                                parent_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==plevel_ID_excel)).select(db.sm_level.level0,db.sm_level.level0_name,db.sm_level.level1,db.sm_level.level1_name,db.sm_level.level2,db.sm_level.level2_name,db.sm_level.level3,db.sm_level.level3_name,db.sm_level.level4,db.sm_level.level4_name,db.sm_level.level5,db.sm_level.level5_name,db.sm_level.level6,db.sm_level.level6_name,db.sm_level.level7,db.sm_level.level7_name,limitby=(0,1))
                                if parent_rows:
                                    level0=parent_rows[0].level0
                                    level0_name=parent_rows[0].level0_name
                                    level1=parent_rows[0].level1
                                    level1_name=parent_rows[0].level1_name
                                    level2=parent_rows[0].level2
                                    level2_name=parent_rows[0].level2_name
                                    level3=parent_rows[0].level3
                                    level3_name=parent_rows[0].level3_name
                                    level4=parent_rows[0].level4
                                    level4_name=parent_rows[0].level4_name
                                    level5=parent_rows[0].level5
                                    level5_name=parent_rows[0].level5_name
                                    level6=parent_rows[0].level6
                                    level6_name=parent_rows[0].level6_name
                                    level7=parent_rows[0].level7
                                    level7_name=parent_rows[0].level7_name
                                    
                                    db.sm_level.insert(cid=c_id,level_id=level_ID_excel,level_name=level_Name_excel,parent_level_id=plevel_ID_excel,parent_level_name=level7_name,is_leaf=isLeaf,depot_id=depotIdvalue,depth=uploadDepth,level0=level0,level0_name=level0_name,level1=level1,level1_name=level1_name,level2=level2,level2_name=level2_name,level3=level3,level3_name=level3_name,level4=level4,level4_name=level4_name,level5=level5,level5_name=level5_name,level6=level6,level6_name=level6_name,level7=level7,level7_name=level7_name,level8=level_ID_excel,level8_name=level_Name_excel)         
                                    count_inserted+=1
                                    continue
                                else:
                                    error_data=row_data+'(Invalid Patent ID)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                            else:
                                error_data=row_data+'(Already Exist)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                    else:
                        error_data=row_data+'(Required value)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                except:
                    error_data=row_data+'(error in process!)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
            else:
                error_data=row_data+'(3 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
    
    return dict(count_inserted=count_inserted,uploadDepth=uploadDepth,count_error=count_error,error_str=error_str,total_row=total_row)

#======================= Report Home

# List
def area_team_upload_list():
    #----------Task assaign----------
    task_id='rm_workingarea_manage'
    task_id_view='rm_workingarea_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    #   ---------------------
    response.title='Area-Team List'
    
    #------------------- Clean
    btn_clean=request.vars.btn_clean
    if btn_clean:
        check_clean_confirm=request.vars.check_clean_confirm
        if check_clean_confirm!='YES':
            response.flash='Required checked confirmation'
        else:
            db.sm_area_team_temp.truncate()
#             db.sm_level.truncate()
#             db.sm_rep.truncate()
#             db.sm_rep_area.truncate()
#             db.sm_supervisor_level.truncate()            
            response.flash='Data cleaned successfully'
            
    #------------------filter
    btn_filter_area_team=request.vars.btn_filter
    btn_filter_area_team_all=request.vars.btn_filter_all
    reqPage=len(request.args)
    if btn_filter_area_team:
        session.btn_filter_area_team=btn_filter_area_team
        session.search_type_area_team=request.vars.search_type
        session.search_value_area_team=str(request.vars.search_value).strip().upper()
        reqPage=0
    elif btn_filter_area_team_all:
        session.btn_filter_area_team=None
        session.search_type_area_team=None
        session.search_value_area_team=None
        reqPage=0
        
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging    
    
    qset=db()
    qset=qset(db.sm_area_team_temp.cid==session.cid)
    
    if session.btn_filter_area_team:        
        if (session.search_type_area_team=='MsoID'):
            searchValue=str(session.search_value_area_team).split('|')[0]            
            qset=qset(db.sm_area_team_temp.mso_id==str(searchValue).strip())
            
        elif (session.search_type_area_team=='RouteID'):
            searchValue=str(session.search_value_area_team).split('|')[0]
            qset=qset(db.sm_area_team_temp.territory_id==searchValue)
            
        elif (session.search_type_area_team=='SpecialTerritory'):
            searchValue=str(session.search_value_area_team).split('|')[0]         
            qset=qset(db.sm_area_team_temp.special_territory_code==searchValue)
        
        elif (session.search_type_area_team=='Status'):
            try:
                searchValue=int(session.search_value_area_team)
            except:
                searchValue=''
              
            qset=qset(db.sm_area_team_temp.second_part_flag==searchValue)
            
        elif (session.search_type_area_team=='YearMonth'):
            try:
                searchValue=datetime.datetime.strptime(str(session.search_value_area_team)+'-01','%Y-%m-%d')
                qset=qset(db.sm_area_team_temp.firstdate==searchValue)
            except:
                response.flash='Invalid Year-Month'
            
    records=qset.select(db.sm_area_team_temp.ALL,orderby=db.sm_area_team_temp.id,limitby=limitby)
    totalCount=qset.count()
    
    return dict(records=records,totalCount=totalCount,page=page,items_per_page=items_per_page,access_permission=access_permission,access_permission_view=access_permission_view)

#area_team_batch_upload
def area_team_batch_upload():
    task_id='rm_workingarea_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    response.title='Area-Team Batch upload'
    
    c_id=session.cid
    btn_upload=request.vars.btn_upload    
    count_inserted=0
    count_error=0
    error_str=''
    total_row=0
    if btn_upload=='Upload':
        year_month=request.vars.year_month
        try:
            ym_date=str(year_month)[0:7]+'-01'
            firstDate=datetime.datetime.strptime(str(ym_date),'%Y-%m-%d')
            session.year_month_areateambatchup=year_month            
        except:
            firstDate=''
        
          
        excel_data=str(request.vars.excel_data)
        inserted_count=0
        error_count=0
        error_list=[]
        row_list=excel_data.split( '\n')
        total_row=len(row_list)
        
        client_list_excel=[]
        client_list_exist=[]
        client_category_exist=[]
        depot_exist=[]
        
        excelList=[]
        
        area_list_excel=[]
        existLevel_list=[]
        
        ins_list=[]
        ins_dict={}
        
        if firstDate=='':
            response.flash='Required valid month'
        else:
            #   --------------------
            for i in range(total_row):
                if i>=1000:
                    break
                else:
                    row_data=row_list[i]
                coloum_list=row_data.split( '\t')
                
                if len(coloum_list)!=23:
                    error_data=row_data+'(23 columns need in a row)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                else:
                    zoneID_ex=str(coloum_list[0]).strip().upper()
                    zoneID_ex=check_special_char_id(zoneID_ex)
                    zoneName_ex=str(coloum_list[1]).strip()
                    zoneName_ex=check_special_char(zoneName_ex)        
                    
                    regionID_ex=str(coloum_list[2]).strip().upper()
                    regionID_ex=check_special_char_id(regionID_ex)
                    regionName_ex=str(coloum_list[3]).strip()
                    regionName_ex=check_special_char(regionName_ex)    
                    
                    areaID_ex=str(coloum_list[4]).strip().upper()
                    areaID_ex=check_special_char_id(areaID_ex)
                    areaName_ex=str(coloum_list[5]).strip()
                    areaName_ex=check_special_char(areaName_ex)    
                    
                    territoryID_ex=str(coloum_list[6]).strip().upper()
                    territoryID_ex=check_special_char_id(territoryID_ex)
                    territoryName_ex=str(coloum_list[7]).strip()
                    territoryName_ex=check_special_char(territoryName_ex)    
                    territoryDes_ex=str(coloum_list[8]).strip()
                    territoryDes_ex=check_special_char(territoryDes_ex)   
                    
                    specialTerritoryCode_ex=str(coloum_list[9]).strip().upper()
                    specialTerritoryCode_ex=check_special_char_id(specialTerritoryCode_ex)
                    
                    zmID_ex=str(coloum_list[10]).strip().upper()
                    zmID_ex=check_special_char_id(zmID_ex)
                    zmName_ex=str(coloum_list[11]).strip()
                    zmName_ex=check_special_char(zmName_ex)
                    zmMobile_ex=str(coloum_list[12]).strip()
                    
                    rsmID_ex=str(coloum_list[13]).strip().upper()
                    rsmID_ex=check_special_char_id(rsmID_ex)
                    rsmName_ex=str(coloum_list[14]).strip()
                    rsmName_ex=check_special_char(rsmName_ex)
                    rsmMobile_ex=str(coloum_list[15]).strip()
                    
                    fmID_ex=str(coloum_list[16]).strip().upper()
                    fmID_ex=check_special_char_id(fmID_ex)
                    fmName_ex=str(coloum_list[17]).strip()
                    fmName_ex=check_special_char(fmName_ex)
                    fmMobile_ex=str(coloum_list[18]).strip()
                    
                    msoID_ex=str(coloum_list[19]).strip().upper()
                    msoID_ex=check_special_char_id(msoID_ex)
                    msoName_ex=str(coloum_list[20]).strip()
                    msoName_ex=check_special_char(msoName_ex)
                    msoMobile_ex=str(coloum_list[21]).strip()                
                    msoCategory_ex=str(coloum_list[22]).strip().upper()
                    
                    if (zoneName_ex=='' or regionName_ex=='' or areaName_ex=='' or territoryName_ex=='' or msoID_ex=='' or msoName_ex=='' or msoCategory_ex==''):
                        error_data=row_data+'(Must value required)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:
                        if msoCategory_ex=='C':
                            if specialTerritoryCode_ex=='':
                                specialTerritoryCode_ex=territoryID_ex
                                
                        if zmMobile_ex!='':
                            try:
                                zmMobile_ex=int(zmMobile_ex)
                            except:
                                error_data=row_data+'(Invalid ZM mobile)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                        else:
                            zmMobile_ex=0
                            
                        if rsmMobile_ex!='':
                            try:
                                rsmMobile_ex=int(rsmMobile_ex)
                            except:
                                error_data=row_data+'(Invalid RSM mobile)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                        else:
                            rsmMobile_ex=0
                            
                        if fmMobile_ex!='':
                            try:
                                fmMobile_ex=int(fmMobile_ex)
                            except:
                                error_data=row_data+'(Invalid FM mobile)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                        else:
                            fmMobile_ex=0
                            
                        if msoMobile_ex!='':
                            try:
                                msoMobile_ex=int(msoMobile_ex)
                            except:
                                error_data=row_data+'(Invalid MSO mobile)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                        else:
                            msoMobile_ex=0
                            
                        if msoCategory_ex not in ['A','B','Z','C'] :
                            error_data=row_data+'(Invalid MSO category )\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                            
                        #-----------
                        try:
                            ins_dict= {'cid':c_id,'firstdate':firstDate,'zone_id':zoneID_ex,'zone_name':zoneName_ex,'region_id':regionID_ex,'region_name':regionName_ex,'area_id':areaID_ex,'area_name':areaName_ex,'territory_id':territoryID_ex,'territory_name':territoryName_ex,'territory_des':territoryDes_ex,'special_territory_code':specialTerritoryCode_ex,
                                       'zm_id':zmID_ex,'zm_name':zmName_ex,'zm_mobile_no':zmMobile_ex,'rsm_id':rsmID_ex,'rsm_name':rsmName_ex,'rsm_mobile_no':rsmMobile_ex,'fm_id':fmID_ex,'fm_name':fmName_ex,'fm_mobile_no':fmMobile_ex,'mso_id':msoID_ex,'mso_name':msoName_ex,'mso_mobile_no':msoMobile_ex,'mso_category':msoCategory_ex}
                            ins_list.append(ins_dict)
                            count_inserted+=1
                        except:
                            error_data=row_data+'(error in process!)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
            
            if error_str=='':
                error_str='No error'
                
            if len(ins_list) > 0:
                inCountList=db.sm_area_team_temp.bulk_insert(ins_list)    
    
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)


#===================================== Download
def download_area_team():
    task_id='rm_workingarea_manage'
    task_id_view='rm_workingarea_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    #   ---------------------
    c_id=session.cid
    records=''
    
    qset=db()
    qset=qset(db.sm_area_team_temp.cid==c_id)
    
    if session.btn_filter_area_team:        
        if (session.search_type_area_team=='MsoID'):
            searchValue=str(session.search_value_area_team).split('|')[0]            
            qset=qset(db.sm_area_team_temp.mso_id==str(searchValue).strip())
            
        elif (session.search_type_area_team=='RouteID'):
            searchValue=str(session.search_value_area_team).split('|')[0]
            qset=qset(db.sm_area_team_temp.territory_id==searchValue)
            
        elif (session.search_type_area_team=='SpecialTerritory'):
            searchValue=str(session.search_value_area_team).split('|')[0]         
            qset=qset(db.sm_area_team_temp.special_territory_code==searchValue)
                
        elif (session.search_type_area_team=='Status'):            
            qset=qset(db.sm_area_team_temp.second_part_flag==session.search_value_area_team)
        
        elif (session.search_type_area_team=='YearMonth'):
            try:
                searchValue=datetime.datetime.strptime(str(session.search_value_area_team)+'-01','%Y-%m-%d')
                qset=qset(db.sm_area_team_temp.firstdate==searchValue)
            except:
                response.flash='Invalid Year-Month'
                
    records=qset.select(db.sm_area_team_temp.ALL,orderby=db.sm_area_team_temp.id)
    
    #---------
    myString='Area-Team List \n\n'
    myString+='Month,ZoneID,ZoneName,RegionID,RegionName,AreaID,AreaName,TerritoryID,TerritoryName,TerritoryDescription,SpecialTerritoryCode,ZM ID,ZM Name,ZM Mobile,RSM ID,RSM Name,RSM Mobile,FM ID,FM Name,FM Mobile,MSO ID,MSO Name,MSO Mobile,MSO Category,Status\n'
    for rec in records:
        firstdate=str(rec.firstdate.strftime('%b-%Y'))
        zone_id=str(rec.zone_id)
        zone_name=str(rec.zone_name).replace(',', ' ')
        region_id=str(rec.region_id)
        region_name=str(rec.region_name).replace(',', ' ')
        area_id=str(rec.area_id)
        area_name=str(rec.area_name).replace(',', ' ')
        territory_id=str(rec.territory_id)
        territory_name=str(rec.territory_name).replace(',', ' ')
        territory_des=str(rec.territory_des).replace(',', ' ')
        special_territory_code=str(rec.special_territory_code)
        zm_id=str(rec.zm_id)
        zm_name=str(rec.zm_name).replace(',', ' ')
        zm_mobile_no=str(rec.zm_mobile_no)
        rsm_id=str(rec.rsm_id)
        rsm_name=str(rec.rsm_name).replace(',', ' ')
        rsm_mobile_no=str(rec.rsm_mobile_no)
        fm_id=str(rec.fm_id)
        fm_name=str(rec.fm_name).replace(',', ' ')
        fm_mobile_no=str(rec.fm_mobile_no)
        mso_id=str(rec.mso_id)
        mso_name=str(rec.mso_name).replace(',', ' ')
        mso_mobile_no=str(rec.mso_mobile_no)
        mso_category=str(rec.mso_category)
        status=str(rec.second_part_flag)
        
        myString+=firstdate+','+zone_id+','+zone_name+','+region_id+','+region_name+','+area_id+','+area_name+','+territory_id+','+territory_name+','+territory_des+','+special_territory_code+','+\
        zm_id+','+zm_name+','+zm_mobile_no+','+rsm_id+','+rsm_name+','+rsm_mobile_no+','+fm_id+','+fm_name+','+fm_mobile_no+','+mso_id+','+mso_name+','+mso_mobile_no+','+mso_category+','+status+'\n'
        
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_area_team.csv'   
    return str(myString)
    
#===================================== Download
def backup_team_structure(firstDate,schedule_date):
    
    #   ---------------------
    c_id=session.cid
    currentMonth=firstDate
    currentDate=schedule_date
    records=''
    
    records=db((db.sm_level.cid==c_id)&(db.sm_level.is_leaf=='1')&(db.sm_rep_area.cid==c_id)&(db.sm_level.level_id==db.sm_rep_area.area_id)&(db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==db.sm_rep_area.rep_id)).select(db.sm_level.ALL,db.sm_rep_area.rep_id,db.sm_rep.name,db.sm_rep.mobile_no,db.sm_rep_area.rep_category,orderby=db.sm_rep_area.rep_category|db.sm_rep_area.rep_id|db.sm_level.level_id)
    supervisorRows=db((db.sm_rep.cid==c_id)&(db.sm_rep.user_type=='sup')&(db.sm_supervisor_level.cid==c_id)&(db.sm_rep.rep_id==db.sm_supervisor_level.sup_id)).select(db.sm_supervisor_level.level_id,db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.mobile_no,orderby=db.sm_rep.rep_id)
    
    #---------    
    structureList=[]
    dictData={}
    for rec in records:        
        zone_id=str(rec.sm_level.level0).strip()
        zone_name=str(rec.sm_level.level0_name).replace(',', ' ')
        region_id=str(rec.sm_level.level1).strip()
        region_name=str(rec.sm_level.level1_name).replace(',', ' ')
        area_id=str(rec.sm_level.level2).strip()
        area_name=str(rec.sm_level.level2_name).replace(',', ' ')
        territory_id=str(rec.sm_level.level_id).strip()
        territory_name=str(rec.sm_level.level_name).replace(',', ' ')
        territory_des=str(rec.sm_level.territory_des).replace(',', ' ')
        special_territory_code=str(rec.sm_level.special_territory_code)
        
        mso_id=str(rec.sm_rep_area.rep_id).strip()
        mso_name=str(rec.sm_rep.name).strip()
        mso_mobile_no=str(rec.sm_rep.mobile_no).strip()
        mso_category=str(rec.sm_rep_area.rep_category).strip()
                
        zm_id=''
        zm_name=''
        zm_mobile_no=''        
        for row0 in supervisorRows:
            sup_level_id=str(row0.sm_supervisor_level.level_id).strip()
            sup_id=str(row0.sm_rep.rep_id)
            sup_name=str(row0.sm_rep.name)
            sup_mobile_no=str(row0.sm_rep.mobile_no)        
            if zone_id==sup_level_id:
                zm_id=sup_id
                zm_name=sup_name
                zm_mobile_no=sup_mobile_no
                break
        #-----------------
        rsm_id=''
        rsm_name=''
        rsm_mobile_no=''
        for row1 in supervisorRows:
            sup_level_id=str(row1.sm_supervisor_level.level_id).strip()
            sup_id=str(row1.sm_rep.rep_id)
            sup_name=str(row1.sm_rep.name)
            sup_mobile_no=str(row1.sm_rep.mobile_no)          
            if region_id==sup_level_id:
                rsm_id=sup_id
                rsm_name=sup_name
                rsm_mobile_no=sup_mobile_no
                break
        
        #-----------------
        fm_id=''
        fm_name=''
        fm_mobile_no=''
        for row2 in supervisorRows:
            sup_level_id=str(row2.sm_supervisor_level.level_id).strip()
            sup_id=str(row2.sm_rep.rep_id)
            sup_name=str(row2.sm_rep.name)
            sup_mobile_no=str(row2.sm_rep.mobile_no)        
            if area_id==sup_level_id:
                fm_id=sup_id
                fm_name=sup_name
                fm_mobile_no=sup_mobile_no
                break
        
        dictData={'cid':c_id,'firstdate':currentMonth,'currentdate':currentDate,'zone_id':zone_id,'zone_name':zone_name,'region_id':region_id,'region_name':region_name,'area_id':area_id,'area_name':area_name,'territory_id':territory_id,'territory_name':territory_name,'territory_des':territory_des,'special_territory_code':special_territory_code,
                  'zm_id':zm_id,'zm_name':zm_name,'zm_mobile_no':zm_mobile_no,'rsm_id':rsm_id,'rsm_name':rsm_name,'rsm_mobile_no':rsm_mobile_no,'fm_id':fm_id,'fm_name':fm_name,'fm_mobile_no':fm_mobile_no,
                  'mso_id':mso_id,'mso_name':mso_name,'mso_mobile_no':mso_mobile_no,'mso_category':mso_category}
                
        structureList.append(dictData)
        
    if len(structureList)>0:        
        db((db.sm_area_team_temp_backup.cid==c_id)&(db.sm_area_team_temp_backup.firstdate==currentMonth)).delete()
        db.sm_area_team_temp_backup.bulk_insert(structureList)
        session.flash='Successfully Done'
    else:
        session.flash='Data not available'
    
    return 'Completed'
    

# List
def area_team_backup_list():
    #----------Task assaign----------
    task_id='rm_workingarea_manage'
    task_id_view='rm_workingarea_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    #   ---------------------
    response.title='Area-Team Backup List'
    
    #------------------filter
    btn_filter_area_team_backup=request.vars.btn_filter
    btn_filter_area_team_backup_all=request.vars.btn_filter_all
    reqPage=len(request.args)
    if btn_filter_area_team_backup:
        session.btn_filter_area_team_backup=btn_filter_area_team_backup
        session.search_yearMonth_backup=request.vars.search_yearMonth
        session.search_type_area_team_backup=request.vars.search_type
        session.search_value_area_team_backup=str(request.vars.search_value).strip().upper()
        reqPage=0
    elif btn_filter_area_team_backup_all:
        session.btn_filter_area_team_backup=None
        session.search_yearMonth_backup=None
        session.search_type_area_team_backup=None
        session.search_value_area_team_backup=None
        reqPage=0
        
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging    
    
    qset=db()
    qset=qset(db.sm_area_team_temp_backup.cid==session.cid)
    
    if session.btn_filter_area_team_backup:
        if not (session.search_yearMonth_backup=='' or session.search_yearMonth_backup==None):
            try:
                searchValue=datetime.datetime.strptime(str(session.search_yearMonth_backup)+'-01','%Y-%m-%d')
                qset=qset(db.sm_area_team_temp_backup.firstdate==searchValue)
            except:
                response.flash='Invalid Year-Month'+session.search_yearMonth_backup
                session.search_yearMonth_backup=None
                
        
        if (session.search_type_area_team_backup=='MsoID'):
            searchValue=str(session.search_value_area_team_backup).split('|')[0]            
            qset=qset(db.sm_area_team_temp_backup.mso_id==str(searchValue).strip())
            
        elif (session.search_type_area_team_backup=='RouteID'):
            searchValue=str(session.search_value_area_team_backup).split('|')[0]
            qset=qset(db.sm_area_team_temp_backup.territory_id==searchValue)
            
        elif (session.search_type_area_team_backup=='SpecialTerritory'):
            searchValue=str(session.search_value_area_team_backup).split('|')[0]         
            qset=qset(db.sm_area_team_temp_backup.special_territory_code==searchValue)
            
    records=qset.select(db.sm_area_team_temp_backup.ALL,orderby=~db.sm_area_team_temp_backup.firstdate|db.sm_area_team_temp_backup.id,limitby=limitby)
    totalCount=qset.count()
    
    return dict(records=records,totalCount=totalCount,page=page,items_per_page=items_per_page,access_permission=access_permission,access_permission_view=access_permission_view)
    
#===================================== Download
def download_area_team_backup_details():
    task_id='rm_workingarea_manage'
    task_id_view='rm_workingarea_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    #   ---------------------
    c_id=session.cid
    
    qset=db()
    qset=qset(db.sm_area_team_temp_backup.cid==c_id)
    
    if session.btn_filter_area_team_backup:
        if not (session.search_yearMonth_backup=='' or session.search_yearMonth_backup==None):
            try:
                searchValue=datetime.datetime.strptime(str(session.search_yearMonth_backup)+'-01','%Y-%m-%d')
                qset=qset(db.sm_area_team_temp_backup.firstdate==searchValue)
            except:
                session.search_yearMonth_backup=None
                session.flash='Invalid Year-Month'  
                redirect (URL('area_team_backup_list'))
        else:
            session.flash='Required Filter by Month'    
            redirect (URL('area_team_backup_list'))
            
    else:
        session.flash='Required Filter by Month'    
        redirect (URL('area_team_backup_list'))
        
    records=qset.select(db.sm_area_team_temp_backup.ALL,orderby=db.sm_area_team_temp_backup.id)
    
    #---------
    myString='Team Structure (Backup)\n'
    myString+='Month:'+str(session.search_yearMonth_backup)+'\n\n'
    
    myString+='ZoneID,ZoneName,RegionID,RegionName,AreaID,AreaName,TerritoryID,TerritoryName,TerritoryDescription,SpecialTerritoryCode,ZM ID,ZM Name,ZM Mobile,RSM ID,RSM Name,RSM Mobile,FM ID,FM Name,FM Mobile,MSO ID,MSO Name,MSO Mobile,MSO Category\n'
    for rec in records:        
        zone_id=str(rec.zone_id).strip()
        zone_name=str(rec.zone_name).replace(',', ' ')
        region_id=str(rec.region_id).strip()
        region_name=str(rec.region_name).replace(',', ' ')
        area_id=str(rec.area_id).strip()
        area_name=str(rec.area_name).replace(',', ' ')
        territory_id=str(rec.territory_id).strip()
        territory_name=str(rec.territory_name).replace(',', ' ')
        territory_des=str(rec.territory_des).replace(',', ' ')
        special_territory_code=str(rec.special_territory_code)
        
        zm_id=str(rec.zm_id).strip()
        zm_name=str(rec.zm_name).replace(',', ' ')
        zm_mobile_no=str(rec.zm_mobile_no).strip()
        
        rsm_id=str(rec.rsm_id).strip()
        rsm_name=str(rec.rsm_name).replace(',', ' ')
        rsm_mobile_no=str(rec.rsm_mobile_no).strip()
        
        fm_id=str(rec.fm_id).strip()
        fm_name=str(rec.fm_name).replace(',', ' ')
        fm_mobile_no=str(rec.fm_mobile_no).strip()
        
        mso_id=str(rec.mso_id).strip()
        mso_name=str(rec.mso_name).strip().replace(',', ' ')
        mso_mobile_no=str(rec.mso_mobile_no).strip()
        mso_category=str(rec.mso_category).strip()
        
        myString+=zone_id+','+zone_name+','+region_id+','+region_name+','+area_id+','+area_name+','+territory_id+','+territory_name+','+territory_des+','+special_territory_code+','+\
        zm_id+','+zm_name+','+zm_mobile_no+','+rsm_id+','+rsm_name+','+rsm_mobile_no+','+fm_id+','+fm_name+','+fm_mobile_no+','+mso_id+','+mso_name+','+mso_mobile_no+','+mso_category+'\n'
    
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_team_structure_backup_details.csv'   
    return str(myString)


#===================================== Download
def x_download_area_team_backup_summary():
    task_id='rm_workingarea_manage'
    task_id_view='rm_workingarea_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    #   ---------------------
    c_id=session.cid
    
    qset=db()
    qset=qset(db.sm_area_team_temp_backup.cid==c_id)
    
    if session.btn_filter_area_team_backup:
        if not (session.search_yearMonth_backup=='' or session.search_yearMonth_backup==None):
            try:
                searchValue=datetime.datetime.strptime(str(session.search_yearMonth_backup)+'-01','%Y-%m-%d')
                qset=qset(db.sm_area_team_temp_backup.firstdate==searchValue)
            except:
                session.search_yearMonth_backup=None
                session.flash='Invalid Year-Month'  
                redirect (URL('area_team_backup_list'))
        else:
            session.flash='Required Filter by Month'    
            redirect (URL('area_team_backup_list'))
            
    else:
        session.flash='Required Filter by Month'    
        redirect (URL('area_team_backup_list'))
    
    qset1=qset(db.sm_area_team_temp_backup.mso_category!='C')#A,B
    records1=qset1.select(db.sm_area_team_temp_backup.ALL,orderby=db.sm_area_team_temp_backup.mso_id|db.sm_area_team_temp_backup.territory_id)
    
    cRows="select a.* from sm_area_team_temp_backup a where a.mso_category='C' and a.territory_id not in (select b.territory_id from sm_area_team_temp_backup b where b.mso_category!='C' and a.special_territory_code=b.special_territory_code)"
    cRowsList=db.executesql(cRows,as_dict = True) 
    
    #---------
    myString='Team Structure (Backup)\n'
    myString+='Month:'+str(session.search_yearMonth_backup)+'\n\n'
    
    #-------A,B group
    myString+='ZoneID,ZoneName,RegionID,RegionName,AreaID,AreaName,TerritoryID,TerritoryName,TerritoryDescription,SpecialTerritoryCode,ZM ID,ZM Name,ZM Mobile,RSM ID,RSM Name,RSM Mobile,FM ID,FM Name,FM Mobile,MSO ID,MSO Name,MSO Mobile,MSO Category\n'
    for rec in records1:        
        zone_id=str(rec.zone_id).strip()
        zone_name=str(rec.zone_name).replace(',', ' ')
        region_id=str(rec.region_id).strip()
        region_name=str(rec.region_name).replace(',', ' ')
        area_id=str(rec.area_id).strip()
        area_name=str(rec.area_name).replace(',', ' ')
        territory_id=str(rec.territory_id).strip()
        territory_name=str(rec.territory_name).replace(',', ' ')
        territory_des=str(rec.territory_des).replace(',', ' ')
        special_territory_code=str(rec.special_territory_code)
        
        zm_id=str(rec.zm_id).strip()
        zm_name=str(rec.zm_name).replace(',', ' ')
        zm_mobile_no=str(rec.zm_mobile_no).strip()
        
        rsm_id=str(rec.rsm_id).strip()
        rsm_name=str(rec.rsm_name).replace(',', ' ')
        rsm_mobile_no=str(rec.rsm_mobile_no).strip()
        
        fm_id=str(rec.fm_id).strip()
        fm_name=str(rec.fm_name).replace(',', ' ')
        fm_mobile_no=str(rec.fm_mobile_no).strip()
        
        mso_id=str(rec.mso_id).strip()
        mso_name=str(rec.mso_name).strip().replace(',', ' ')
        mso_mobile_no=str(rec.mso_mobile_no).strip()
        mso_category=str(rec.mso_category).strip()
        
        myString+=zone_id+','+zone_name+','+region_id+','+region_name+','+area_id+','+area_name+','+territory_id+','+territory_name+','+territory_des+','+special_territory_code+','+\
        zm_id+','+zm_name+','+zm_mobile_no+','+rsm_id+','+rsm_name+','+rsm_mobile_no+','+fm_id+','+fm_name+','+fm_mobile_no+','+mso_id+','+mso_name+','+mso_mobile_no+','+mso_category+'\n'
    
    #---- C group
    for i in range(len(cRowsList)):
        cDictData=cRowsList[i]
        
        zone_id=str(cDictData['zone_id']).strip()
        zone_name=str(cDictData['zone_name']).strip().replace(',', ' ')
        region_id=str(cDictData['region_id']).strip()
        region_name=str(cDictData['region_name']).strip().replace(',', ' ')
        area_id=str(cDictData['area_id']).strip()
        area_name=str(cDictData['area_name']).strip().replace(',', ' ')
        territory_id=str(cDictData['territory_id']).strip()
        territory_name=str(cDictData['territory_name']).strip().replace(',', ' ')
        territory_des=str(cDictData['territory_des']).strip()
        special_territory_code=str(cDictData['special_territory_code']).strip()
        zm_id=str(cDictData['zm_id']).strip()
        zm_name=str(cDictData['zm_name']).strip().replace(',', ' ')
        zm_mobile_no=str(cDictData['zm_mobile_no']).strip()
        rsm_id=str(cDictData['rsm_id']).strip()
        rsm_name=str(cDictData['rsm_name']).strip().replace(',', ' ')
        rsm_mobile_no=str(cDictData['rsm_mobile_no']).strip()
        fm_id=str(cDictData['fm_id']).strip()
        fm_name=str(cDictData['fm_name']).strip().replace(',', ' ')
        fm_mobile_no=str(cDictData['fm_mobile_no']).strip()
        mso_id=str(cDictData['mso_id']).strip()
        mso_name=str(cDictData['mso_name']).strip().replace(',', ' ')
        mso_mobile_no=str(cDictData['mso_mobile_no']).strip()
        mso_category=str(cDictData['mso_category']).strip()
        
        myString+=zone_id+','+zone_name+','+region_id+','+region_name+','+area_id+','+area_name+','+territory_id+','+territory_name+','+territory_des+','+special_territory_code+','+\
        zm_id+','+zm_name+','+zm_mobile_no+','+rsm_id+','+rsm_name+','+rsm_mobile_no+','+fm_id+','+fm_name+','+fm_mobile_no+','+mso_id+','+mso_name+','+mso_mobile_no+','+mso_category+'\n'
    
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_team_structure_backup_summary.csv'   
    return str(myString)


#===================================== Download
def x_download_team_structure_2():
    task_id='rm_workingarea_manage'
    task_id_view='rm_workingarea_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    #   ---------------------
    c_id=session.cid
    currentMonth=first_currentDate
    currentDate=current_date
    records=''
    
    records=db((db.sm_level.cid==c_id)&(db.sm_level.is_leaf=='1')&(db.sm_rep_area.cid==c_id)&(db.sm_level.level_id==db.sm_rep_area.area_id)&(db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==db.sm_rep_area.rep_id)).select(db.sm_level.ALL,db.sm_rep_area.rep_id,db.sm_rep.name,db.sm_rep.mobile_no,db.sm_rep_area.rep_category,orderby=db.sm_rep_area.rep_category|db.sm_rep_area.rep_id|db.sm_level.level_id)
    
    supervisorRows=db((db.sm_rep.cid==c_id)&(db.sm_rep.user_type=='sup')&(db.sm_supervisor_level.cid==c_id)&(db.sm_rep.rep_id==db.sm_supervisor_level.sup_id)).select(db.sm_supervisor_level.level_id,db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.mobile_no,orderby=db.sm_rep.rep_id)
    
    #---------
    myString='Team Structure\n'
    myString+='Date:'+str(current_date)+'\n\n'
    
    structureList=[]
    dictData={}
    myString+='ZoneID,ZoneName,RegionID,RegionName,AreaID,AreaName,TerritoryID,TerritoryName,TerritoryDescription,SpecialTerritoryCode,ZM ID,ZM Name,ZM Mobile,RSM ID,RSM Name,RSM Mobile,FM ID,FM Name,FM Mobile,MSO ID,MSO Name,MSO Mobile,MSO Category\n'
    for rec in records:        
        zone_id=str(rec.sm_level.level0).strip()
        zone_name=str(rec.sm_level.level0_name).replace(',', ' ')
        region_id=str(rec.sm_level.level1).strip()
        region_name=str(rec.sm_level.level1_name).replace(',', ' ')
        area_id=str(rec.sm_level.level2).strip()
        area_name=str(rec.sm_level.level2_name).replace(',', ' ')
        territory_id=str(rec.sm_level.level_id).strip()
        territory_name=str(rec.sm_level.level_name).replace(',', ' ')
        territory_des=str(rec.sm_level.territory_des).replace(',', ' ')
        special_territory_code=str(rec.sm_level.special_territory_code)
        
        mso_id=str(rec.sm_rep_area.rep_id).strip()
        mso_name=str(rec.sm_rep.name).strip()
        mso_mobile_no=str(rec.sm_rep.mobile_no).strip()
        mso_category=str(rec.sm_rep_area.rep_category).strip()
                
        zm_id=''
        zm_name=''
        zm_mobile_no=''        
        for row0 in supervisorRows:
            sup_level_id=str(row0.sm_supervisor_level.level_id).strip()
            sup_id=str(row0.sm_rep.rep_id)
            sup_name=str(row0.sm_rep.name)
            sup_mobile_no=str(row0.sm_rep.mobile_no)        
            if zone_id==sup_level_id:
                zm_id=sup_id
                zm_name=sup_name
                zm_mobile_no=sup_mobile_no
                break
        #-----------------
        rsm_id=''
        rsm_name=''
        rsm_mobile_no=''
        for row1 in supervisorRows:
            sup_level_id=str(row1.sm_supervisor_level.level_id).strip()
            sup_id=str(row1.sm_rep.rep_id)
            sup_name=str(row1.sm_rep.name)
            sup_mobile_no=str(row1.sm_rep.mobile_no)          
            if region_id==sup_level_id:
                rsm_id=sup_id
                rsm_name=sup_name
                rsm_mobile_no=sup_mobile_no
                break
        
        #-----------------
        fm_id=''
        fm_name=''
        fm_mobile_no=''
        for row2 in supervisorRows:
            sup_level_id=str(row2.sm_supervisor_level.level_id).strip()
            sup_id=str(row2.sm_rep.rep_id)
            sup_name=str(row2.sm_rep.name)
            sup_mobile_no=str(row2.sm_rep.mobile_no)        
            if area_id==sup_level_id:
                fm_id=sup_id
                fm_name=sup_name
                fm_mobile_no=sup_mobile_no
                break
        
        dictData={'cid':c_id,'firstdate':currentMonth,'currentdate':currentDate,'zone_id':zone_id,'zone_name':zone_name,'region_id':region_id,'region_name':region_name,'area_id':area_id,'area_name':area_name,'territory_id':territory_id,'territory_name':territory_name,'territory_des':territory_des,'special_territory_code':special_territory_code,
                  'zm_id':zm_id,'zm_name':zm_name,'zm_mobile_no':zm_mobile_no,'rsm_id':rsm_id,'rsm_name':rsm_name,'rsm_mobile_no':rsm_mobile_no,'fm_id':fm_id,'fm_name':fm_name,'fm_mobile_no':fm_mobile_no,
                  'mso_id':mso_id,'mso_name':mso_name,'mso_mobile_no':mso_mobile_no,'mso_category':mso_category}
        
        structureList.append(dictData)
        
    if len(structureList)>0:        
        db((db.sm_area_team_temp_download.cid==c_id)&(db.sm_area_team_temp_download.firstdate==currentMonth)).delete()
        db.sm_area_team_temp_download.bulk_insert(structureList)
    
#         myString+=zone_id+','+zone_name+','+region_id+','+region_name+','+area_id+','+area_name+','+territory_id+','+territory_name+','+territory_des+','+special_territory_code+','+\
#         zm_id+','+zm_name+','+zm_mobile_no+','+rsm_id+','+rsm_name+','+rsm_mobile_no+','+fm_id+','+fm_name+','+fm_mobile_no+','+mso_id+','+mso_name+','+mso_mobile_no+','+mso_category+'\n'
    
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_team_structure.csv'   
    return str(myString)



#get last level id

def area_team_process_home():   
    #----------Task assaign----------
    task_id='rm_workingarea_manage'
    task_id_view='rm_workingarea_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    #-----------------------
    c_id=session.cid
    
    response.title='Process-Team structure'
    
    #------------------------- Delete process
    btn_delete_process=request.vars.btn_delete_process
    if btn_delete_process:
        pRowId=str(request.vars.pRowId).strip()
        
        if pRowId=='':
            response.flash='Invalid request'
        else:
            existRow=db((db.sm_area_team_process_schedule.cid==c_id)&(db.sm_area_team_process_schedule.status=='0')&(db.sm_area_team_process_schedule.id==pRowId)).select(db.sm_area_team_process_schedule.id,limitby=(0,1))
            if not existRow:
                response.flash='Pending record not available'
            else:
                db((db.sm_area_team_process_schedule.cid==c_id)&(db.sm_area_team_process_schedule.status=='0')&(db.sm_area_team_process_schedule.id==pRowId)).delete()
                response.flash='Process request deleted successfully'
    
    #------------------------- check authorization
    btn_authorization=request.vars.btn_authorization
    if btn_authorization:
        auth_pin=str(request.vars.auth_pin).strip()
        
        if auth_pin=='abc123admin321cba':
            session.authorization_pin=auth_pin
            response.flash='Authorization OK'
        else:
            session.authorization_pin=''
            response.flash='Invalid PIN'
            
    #------------------------    
    search_form =SQLFORM(db.sm_search_date)
    
    btn_verification=request.vars.btn_verification
    if btn_verification:
        schedule_date=request.vars.to_dt
        try:
            scheduleDate=datetime.datetime.strptime(str(schedule_date),'%Y-%m-%d')
            ym_date=str(scheduleDate)[0:7]+'-01'
        except:
            scheduleDate=''
            
        if scheduleDate=='':
            response.flash='Invalid Schedule date'
        else:
#             currentDate=datetime.datetime.strptime(str(current_date),'%Y-%m-%d')
#             scheduleDate=datetime.datetime.strptime(str(schedule_date),'%Y-%m-%d')
#             if scheduleDate<currentDate:
#                 formProcess.errors.schedule_date=''
#                 response.flash='Previous date not allowed'
#             else:
            processRecords=db((db.sm_area_team_process_schedule.cid==c_id)&(db.sm_area_team_process_schedule.first_date==ym_date)).select(db.sm_area_team_process_schedule.first_date,limitby=(0,1))
            if processRecords:
                response.flash='Already submitted schedule in this month for processing'
            else:
                preProcessRecords=db((db.sm_area_team_process_schedule.cid==c_id)&(db.sm_area_team_process_schedule.first_date>ym_date)).select(db.sm_area_team_process_schedule.first_date,limitby=(0,1))
                if preProcessRecords:
                    response.flash='Previous processing not allowed'
                else:
                    existRecords=db((db.sm_area_team_temp.cid==c_id)&(db.sm_area_team_temp.firstdate==ym_date)).select(db.sm_area_team_temp.firstdate,limitby=(0,1))
                    if not existRecords:
                        response.flash='Temporary Data not available in '+scheduleDate.strftime('%b-%Y')
                    else:      
                        try:
                            db.sm_area_team_process_schedule.insert(cid=c_id,first_date=ym_date,schedule_date=scheduleDate,notes='Pending')
                            
                            response.flash='Submitted successfully for processing'                            
                        except:
                            response.flash='Error in varification '
    
    #--------------------------- show records
    if request.vars.page==None or request.vars.page=='':
        page=0
    else:
        page=int(request.vars.page)
    #----------paging
    if (page > 0):
        page=page
    else:
        page=0
    items_per_page=12
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #----------end paging    
    
    # show records
    records=db(db.sm_area_team_process_schedule.cid==c_id).select(db.sm_area_team_process_schedule.ALL,orderby=~db.sm_area_team_process_schedule.first_date,limitby=limitby)
    
    #--------------------- Year-month
    yearMonthRecords=db((db.sm_area_team_process_schedule.cid==c_id)&(db.sm_area_team_process_schedule.status=='1')).select(db.sm_area_team_process_schedule.ALL,orderby=~db.sm_area_team_process_schedule.first_date)
    
    #------------------------- use for disable button during pending or process started
    pendingRecords=db((db.sm_area_team_process_schedule.cid==c_id)&(db.sm_area_team_process_schedule.status!='1')).select(db.sm_area_team_process_schedule.ALL,limitby=(0,1))
    
    #---------------------------
    return dict(search_form=search_form,records=records,yearMonthRecords=yearMonthRecords,pendingRecords=pendingRecords,page=page,items_per_page=items_per_page,access_permission=access_permission)
    
#=======================
def delete_area_team_process(): 
    c_id=session.cid
    
    btn_reset=request.vars.btn_reset  
    ymValueType=request.vars.ymValueType
    first_date=''
    try:
        first_date=datetime.datetime.strptime(str(ymValueType),'%Y-%m-%d')
    except:
        first_date=''
    
    if first_date=='' or first_date==None:
        session.flash='Select valid Year-Month'
    else:
        if btn_reset:
            cmb_cancel=request.vars.cmb_cancel
            if (cmb_cancel!='confirm_cancel'):
                session.flash='Please check confirmaion !'
            else:
                #--------- delete exist data
                db((db.sm_area_team_temp_backup.cid==c_id)&(db.sm_area_team_temp_backup.firstdate==first_date)).delete()
                db((db.sm_area_team_process_schedule.cid==c_id) & (db.sm_area_team_process_schedule.first_date==first_date)).delete()
                
                session.flash='Deleted Successfully'
    
    redirect(URL('area_team_process_home'))


def getLastLevelID(c_id,depth):
    # Starting Code get from level name settings that is starting with a character(a-z)
    
    cid=c_id
    depthNo=depth
    
    setLevelId=''
    firstChar=''
    codeLength=0
    levelSettings=db((db.level_name_settings.cid==cid)&(db.level_name_settings.depth==depthNo)).select(db.level_name_settings.starting_code,limitby=(0,1))
    if levelSettings:
        setLevelId=str(levelSettings[0].starting_code).upper()
        firstChar=setLevelId[0:1]
        codeLength=len(setLevelId[1:])
    
    #----------- 
    levelCodeRow=db((db.sm_level.cid==cid)&(db.sm_level.depth==depthNo)).select(db.sm_level.level_id,orderby=~db.sm_level.level_id,limitby=(0,1))
    if levelCodeRow:
        try:
            if str(levelCodeRow[0].level_id)[0:1]==firstChar and len(str(levelCodeRow[0].level_id)[1:])==codeLength:
                level_idStr=str(levelCodeRow[0].level_id)[1:]
                maxLevelID=int(level_idStr)+1
                setLevelId=firstChar+str(maxLevelID).zfill(codeLength)
        except:
           pass
        
    return setLevelId

#manual
#http://127.0.0.1:8000/mrepskf/level/process_area_team_manual?process_date=2016-02-06
def process_area_team_manual_step1():
    c_id=session.cid
    
    process_date=request.vars.process_date
    
    try:
        currentDate=datetime.datetime.strptime(str(process_date),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        return 'Invalid request'
        
    #----------------------------------
    processRecords=db((db.sm_area_team_process_schedule.cid==c_id)&(db.sm_area_team_process_schedule.status=='0')&(db.sm_area_team_process_schedule.schedule_date==currentDate)).select(db.sm_area_team_process_schedule.ALL,orderby=db.sm_area_team_process_schedule.first_date,limitby=(0,1))
    if not processRecords:
        return 'Process Not available'
    else:
        first_date=processRecords[0].first_date
        schedule_date=processRecords[0].schedule_date
        
        processRecords[0].update_record(status='2',notes='Step-1 Process running...')
        
        #--------- clean existing data        
        db.sm_level.truncate()
        db.sm_rep.truncate()
        db.sm_rep_area.truncate()
        db.sm_supervisor_level.truncate()
        
        #=========================== First Part
        #--------Zone Part
        zoneRecords=db(db.sm_area_team_temp.zone_flag == 0).select(db.sm_area_team_temp.cid,db.sm_area_team_temp.zone_id,db.sm_area_team_temp.zone_name,orderby=~db.sm_area_team_temp.zone_id|db.sm_area_team_temp.zone_name,groupby=db.sm_area_team_temp.cid|db.sm_area_team_temp.zone_id|db.sm_area_team_temp.zone_name)
        for zoneRecord in zoneRecords:
            c_id=zoneRecord.cid
            zone_id=str(zoneRecord.zone_id).strip().upper()
            zone_name=str(zoneRecord.zone_name).strip().upper()
            
            depthNo=0
            isLeaf='0'
            
            #Zone id set
            if zone_id=='':
                setLevelId=getLastLevelID(c_id,depthNo)
            else:
                setLevelId=zone_id
                
            #----
            errorFlag=False
            errorMsg=''
            levelIdRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==setLevelId)).select(db.sm_level.level_id,limitby=(0,1))
            if levelIdRow:
                errorFlag=True
                errorMsg='Zone ID already exist'
            else:
                levelNameRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_name.upper()==zone_name)).select(db.sm_level.level_id,limitby=(0,1))
                if levelNameRow:
                    errorFlag=True
                    errorMsg='Zone Name already exist'
                else:
                    pass
            
            #-----
            if errorFlag==True:
                db(db.sm_area_team_temp.zone_name.upper() == zone_name).update(zone_flag=2,des=errorMsg)
            else:
                level0=setLevelId
                level0_name=zone_name
                
                db.sm_level.insert(cid=c_id,level_id=setLevelId,level_name=zone_name,parent_level_id='0',parent_level_name='',is_leaf=isLeaf,depot_id='',depth=depthNo,level0=level0,level0_name=level0_name)
                
                if zone_id=='':
                    db(db.sm_area_team_temp.zone_name.upper() == zone_name).update(zone_id=setLevelId,zone_flag=1)
                else:
                    db(db.sm_area_team_temp.zone_name.upper() == zone_name).update(zone_flag=1)
                    
        #--------Region Part
        regionRecords=db((db.sm_area_team_temp.zone_flag == 1)&(db.sm_area_team_temp.region_flag == 0)).select(db.sm_area_team_temp.cid,db.sm_area_team_temp.zone_id,db.sm_area_team_temp.zone_name,db.sm_area_team_temp.region_id,db.sm_area_team_temp.region_name,orderby=~db.sm_area_team_temp.region_id|db.sm_area_team_temp.region_name,groupby=db.sm_area_team_temp.cid|db.sm_area_team_temp.zone_id|db.sm_area_team_temp.zone_name|db.sm_area_team_temp.region_id|db.sm_area_team_temp.region_name)
        for regionRecord in regionRecords:
            c_id=regionRecord.cid
            zone_id=str(regionRecord.zone_id).strip().upper()
            zone_name=str(regionRecord.zone_name).strip().upper()
            region_id=str(regionRecord.region_id).strip().upper()
            region_name=str(regionRecord.region_name).strip().upper()
            
            depthNo=1
            isLeaf='0'
            
            #Region id set
            if region_id=='':
                setLevelId=getLastLevelID(c_id,depthNo)
            else:
                setLevelId=region_id
                
            #----
            errorFlag=False
            errorMsg=''
            levelIdRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==setLevelId)).select(db.sm_level.level_id,limitby=(0,1))
            if levelIdRow:
                errorFlag=True
                errorMsg='Region ID already exist'
            else:
                levelNameRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_name.upper()==region_name)).select(db.sm_level.level_id,limitby=(0,1))
                if levelNameRow:
                    errorFlag=True
                    errorMsg='Region Name already exist'
                else:
                    pass
            
            #-----
            if errorFlag==True:
                db(db.sm_area_team_temp.region_name.upper() == region_name).update(region_flag=2,des=errorMsg)
            else:                
                level0=zone_id
                level0_name=zone_name
                level1=setLevelId
                level1_name=region_name
                
                db.sm_level.insert(cid=c_id,level_id=setLevelId,level_name=region_name,parent_level_id=zone_id,parent_level_name=zone_name,is_leaf=isLeaf,depot_id='',depth=depthNo,level0=level0,level0_name=level0_name,level1=level1,level1_name=level1_name)
                
                if region_id=='':
                    db(db.sm_area_team_temp.region_name.upper() == region_name).update(region_id=setLevelId,region_flag=1)
                else:
                    db(db.sm_area_team_temp.region_name.upper() == region_name).update(region_flag=1)
        
        time.sleep(1)
        
        #--------Area Part
        areaRecords=db((db.sm_area_team_temp.region_flag == 1)&(db.sm_area_team_temp.area_flag == 0)).select(db.sm_area_team_temp.cid,db.sm_area_team_temp.zone_id,db.sm_area_team_temp.zone_name,db.sm_area_team_temp.region_id,db.sm_area_team_temp.region_name,db.sm_area_team_temp.area_id,db.sm_area_team_temp.area_name,orderby=~db.sm_area_team_temp.area_id|db.sm_area_team_temp.area_name,groupby=db.sm_area_team_temp.cid|db.sm_area_team_temp.zone_id|db.sm_area_team_temp.zone_name|db.sm_area_team_temp.region_id|db.sm_area_team_temp.region_name|db.sm_area_team_temp.area_id|db.sm_area_team_temp.area_name)
        for areaRecord in areaRecords:
            c_id=areaRecord.cid
            zone_id=str(areaRecord.zone_id).strip().upper()
            zone_name=str(areaRecord.zone_name).strip().upper()
            region_id=str(areaRecord.region_id).strip().upper()
            region_name=str(areaRecord.region_name).strip().upper()
            area_id=str(areaRecord.area_id).strip().upper()
            area_name=str(areaRecord.area_name).strip().upper()
            
            depthNo=2
            isLeaf='0'
            
            #Area id set
            if area_id=='':
                setLevelId=getLastLevelID(c_id,depthNo)
            else:
                setLevelId=area_id
                
            #----
            errorFlag=False
            errorMsg=''
            levelIdRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==setLevelId)).select(db.sm_level.level_id,limitby=(0,1))
            if levelIdRow:
                errorFlag=True
                errorMsg='Area ID already exist'
            else:
                levelNameRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_name.upper()==area_name)).select(db.sm_level.level_id,limitby=(0,1))
                if levelNameRow:
                    errorFlag=True
                    errorMsg='Area Name already exist'
                else:
                    pass
            
            #-----
            if errorFlag==True:
                db(db.sm_area_team_temp.area_name.upper() == area_name).update(area_flag=2,des=errorMsg)
            else:                
                level0=zone_id
                level0_name=zone_name
                level1=region_id
                level1_name=region_name
                level2=setLevelId
                level2_name=area_name
                
                db.sm_level.insert(cid=c_id,level_id=setLevelId,level_name=area_name,parent_level_id=region_id,parent_level_name=region_name,is_leaf=isLeaf,depot_id='',depth=depthNo,level0=level0,level0_name=level0_name,level1=level1,level1_name=level1_name,level2=level2,level2_name=level2_name)
                
                if area_id=='':
                    db(db.sm_area_team_temp.area_name.upper() == area_name).update(area_id=setLevelId,area_flag=1)
                else:
                    db(db.sm_area_team_temp.area_name.upper() == area_name).update(area_flag=1)
        
        time.sleep(1)
        
        #--------Territory Part
        territoryRecords=db((db.sm_area_team_temp.area_flag == 1)&(db.sm_area_team_temp.territory_flag == 0)).select(db.sm_area_team_temp.cid,db.sm_area_team_temp.zone_id,db.sm_area_team_temp.zone_name,db.sm_area_team_temp.region_id,db.sm_area_team_temp.region_name,db.sm_area_team_temp.area_id,db.sm_area_team_temp.area_name,db.sm_area_team_temp.territory_id,db.sm_area_team_temp.territory_name,db.sm_area_team_temp.territory_des,db.sm_area_team_temp.special_territory_code,orderby=~db.sm_area_team_temp.territory_id|db.sm_area_team_temp.territory_name,groupby=db.sm_area_team_temp.cid|db.sm_area_team_temp.zone_id|db.sm_area_team_temp.zone_name|db.sm_area_team_temp.region_id|db.sm_area_team_temp.region_name|db.sm_area_team_temp.area_id|db.sm_area_team_temp.area_name|db.sm_area_team_temp.territory_id|db.sm_area_team_temp.territory_name)
        for territoryRecord in territoryRecords:
            c_id=territoryRecord.cid
            zone_id=str(territoryRecord.zone_id).strip().upper()
            zone_name=str(territoryRecord.zone_name).strip().upper()
            region_id=str(territoryRecord.region_id).strip().upper()
            region_name=str(territoryRecord.region_name).strip().upper()
            area_id=str(territoryRecord.area_id).strip().upper()
            area_name=str(territoryRecord.area_name).strip().upper()
            territory_id=str(territoryRecord.territory_id).strip().upper()
            territory_name=str(territoryRecord.territory_name).strip().upper()
            territory_des=str(territoryRecord.territory_des).strip().upper()
            special_territory_code=str(territoryRecord.special_territory_code).strip().upper()
            
            depthNo=3
            isLeaf='1'
            
            #Area id set
            if territory_id=='':
                setLevelId=getLastLevelID(c_id,depthNo)
            else:
                setLevelId=territory_id
                
            #----
            errorFlag=False
            errorMsg=''
            levelIdRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==setLevelId)).select(db.sm_level.level_id,limitby=(0,1))
            if levelIdRow:
                errorFlag=True
                errorMsg='Territory ID already exist'
            else:
                levelNameRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_name.upper()==territory_name)).select(db.sm_level.level_id,limitby=(0,1))
                if levelNameRow:
                    errorFlag=True
                    errorMsg='Territory Name already exist'
                else:
                    pass
            
            #-----
            if errorFlag==True:
                db(db.sm_area_team_temp.territory_name.upper() == territory_name).update(territory_flag=2,des=errorMsg)
            else:                
                level0=zone_id
                level0_name=zone_name
                level1=region_id
                level1_name=region_name
                level2=area_id
                level2_name=area_name
                level3=setLevelId
                level3_name=territory_name
                
                db.sm_level.insert(cid=c_id,level_id=setLevelId,level_name=territory_name,parent_level_id=area_id,parent_level_name=area_name,is_leaf=isLeaf,depot_id='',depth=depthNo,level0=level0,level0_name=level0_name,level1=level1,level1_name=level1_name,level2=level2,level2_name=level2_name,level3=level3,level3_name=level3_name,territory_des=territory_des,special_territory_code=special_territory_code)
                
                if territory_id=='':
                    db(db.sm_area_team_temp.territory_name.upper() == territory_name).update(territory_id=setLevelId,territory_flag=1,first_part_flag=1)
                else:
                    db(db.sm_area_team_temp.territory_name.upper() == territory_name).update(territory_flag=1,first_part_flag=1)
        
        #------------
        processRecords[0].update_record(status='3',notes='Step-1 processe completed')
        db.commit()
        
        return 'Step-1 completed'
    
def process_area_team_manual_step2():
    c_id=session.cid
    
    process_date=request.vars.process_date
    
    try:
        currentDate=datetime.datetime.strptime(str(process_date),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        return 'Invalid request'
        
    #----------------------------------
    processRecords=db((db.sm_area_team_process_schedule.cid==c_id)&(db.sm_area_team_process_schedule.status=='3')&(db.sm_area_team_process_schedule.schedule_date==currentDate)).select(db.sm_area_team_process_schedule.ALL,orderby=db.sm_area_team_process_schedule.first_date,limitby=(0,1))
    if not processRecords:
        return 'Process Not available'
    else:
        first_date=processRecords[0].first_date
        schedule_date=processRecords[0].schedule_date
        
        processRecords[0].update_record(status='4',notes='Step-2 Process running...')
        
        #=========================== Second Part
        #--------ZM (Zonal Manager) Part
        zmRecords=db((db.sm_area_team_temp.first_part_flag == 1)&(db.sm_area_team_temp.zm_flag == 0)).select(db.sm_area_team_temp.cid,db.sm_area_team_temp.zone_id,db.sm_area_team_temp.zone_name,db.sm_area_team_temp.zm_id,db.sm_area_team_temp.zm_name,db.sm_area_team_temp.zm_mobile_no,orderby=db.sm_area_team_temp.zone_id|db.sm_area_team_temp.zm_id,groupby=db.sm_area_team_temp.cid|db.sm_area_team_temp.zone_id|db.sm_area_team_temp.zone_name|db.sm_area_team_temp.zm_id|db.sm_area_team_temp.zm_name)
        for zmRecord in zmRecords:
            c_id=zmRecord.cid
            zone_id=str(zmRecord.zone_id).strip().upper()
            zone_name=str(zmRecord.zone_name).strip().upper()
            zm_id=str(zmRecord.zm_id).strip().upper()
            zm_name=str(zmRecord.zm_name).strip()
            mobile_no=zmRecord.zm_mobile_no
            
            try:
                mobile_no=int(mobile_no)
                if len(str(mobile_no))!=13:
                    mobile_no=0
            except:
                mobile_no=0
            
            randNumber=randint(1001, 9999)
            depthNo=0
            
            #------- error Check
            errorFlag=False
            errorMsg=''
            if not(zm_id=='' or zm_name==''):    
                ffLevelRow1=db((db.sm_supervisor_level.cid==c_id)&(db.sm_supervisor_level.sup_id==zm_id)).select(db.sm_supervisor_level.level_depth_no,limitby=(0,1))
                if ffLevelRow1:
                    level_depth_no=ffLevelRow1[0].level_depth_no
                    if level_depth_no!=depthNo:
                        errorFlag=True
                        errorMsg='Require existing and current level-depth same for ZM'
            
            if (zm_id=='' and zm_name!='') or (zm_id!='' and zm_name==''):
                errorFlag=True
                errorMsg='ZM ID or Name one is blank'
            
            #-----
            if errorFlag==True:
                db((db.sm_area_team_temp.zone_id == zone_id)&(db.sm_area_team_temp.zm_id == zm_id)).update(zm_flag=2,des=errorMsg)
            else:                
                #---- Supervisor
                if not (zm_id=='' or zm_name==''):       
                    ffRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==zm_id)).select(db.sm_rep.rep_id,limitby=(0,1))
                    if not ffRow:                
                        if mobile_no==0:
                            status='INACTIVE'
                        else:
                            compMobRecords=db((db.sm_comp_mobile.cid==c_id) & (db.sm_comp_mobile.mobile_no == mobile_no)).select(db.sm_comp_mobile.mobile_no,limitby=(0,1))
                            if not compMobRecords:
                                status='INACTIVE'
                                mobile_no=0
                                #db.sm_comp_mobile.insert(cid=c_id,mobile_no=mobile_no,user_type='sup')
                            else:                        
                                status='ACTIVE'
                        
                        db.sm_rep.insert(cid=c_id,rep_id=zm_id,name=zm_name,mobile_no=mobile_no,password=randNumber,status=status,user_type='sup')
                
                    #---- Supervisor-Level
                    ffLevelRow2=db((db.sm_supervisor_level.cid==c_id)&(db.sm_supervisor_level.sup_id==zm_id)&(db.sm_supervisor_level.level_id==zone_id)).select(db.sm_supervisor_level.sup_id,limitby=(0,1))
                    if not ffLevelRow2:
                        db.sm_supervisor_level.insert(cid=c_id,sup_id=zm_id,sup_name=zm_name,level_id=zone_id,level_name=zone_name,level_depth_no=depthNo)
                
                #----------      
                db((db.sm_area_team_temp.zone_id == zone_id)&(db.sm_area_team_temp.zm_id == zm_id)).update(zm_flag=1)
        
        
        #--------RSM (Regional Sales Manager) Part
        rsmRecords=db((db.sm_area_team_temp.zm_flag == 1)&(db.sm_area_team_temp.rsm_flag == 0)).select(db.sm_area_team_temp.cid,db.sm_area_team_temp.region_id,db.sm_area_team_temp.region_name,db.sm_area_team_temp.rsm_id,db.sm_area_team_temp.rsm_name,db.sm_area_team_temp.rsm_mobile_no,orderby=db.sm_area_team_temp.region_id|db.sm_area_team_temp.rsm_id,groupby=db.sm_area_team_temp.cid|db.sm_area_team_temp.region_id|db.sm_area_team_temp.region_name|db.sm_area_team_temp.rsm_id|db.sm_area_team_temp.rsm_name)
        for rsmRecord in rsmRecords:
            c_id=rsmRecord.cid
            region_id=str(rsmRecord.region_id).strip().upper()
            region_name=str(rsmRecord.region_name).strip().upper()
            rsm_id=str(rsmRecord.rsm_id).strip().upper()
            rsm_name=str(rsmRecord.rsm_name).strip()
            mobile_no=rsmRecord.rsm_mobile_no
            
            try:
                mobile_no=int(mobile_no)
                if len(str(mobile_no))!=13:
                    mobile_no=0                
            except:
                mobile_no=0
            
            randNumber=randint(1001, 9999)
            depthNo=1
            
            #error check
            errorFlag=False
            errorMsg=''
            if not (rsm_id=='' or rsm_name==''):
                ffLevelRow1=db((db.sm_supervisor_level.cid==c_id)&(db.sm_supervisor_level.sup_id==rsm_id)).select(db.sm_supervisor_level.level_depth_no,limitby=(0,1))
                if ffLevelRow1:
                    level_depth_no=ffLevelRow1[0].level_depth_no
                    if level_depth_no!=depthNo:
                        errorFlag=True
                        errorMsg='Require existing and current level-depth same for RSM'
            
            if (rsm_id=='' and rsm_name!='') or (rsm_id!='' and rsm_name==''):
                errorFlag=True
                errorMsg='RSM ID or Name one is blank'
                
            
            if errorFlag==True:
                db((db.sm_area_team_temp.region_id == region_id)&(db.sm_area_team_temp.rsm_id == rsm_id)).update(rsm_flag=2,des=errorMsg)
            else:
                #---- Supervisor
                if not (rsm_id=='' or rsm_name==''):         
                    ffRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==rsm_id)).select(db.sm_rep.rep_id,limitby=(0,1))
                    if not ffRow:                
                        if mobile_no==0:
                            status='INACTIVE'
                        else:
                            compMobRecords=db((db.sm_comp_mobile.cid==c_id) & (db.sm_comp_mobile.mobile_no == mobile_no)).select(db.sm_comp_mobile.mobile_no,limitby=(0,1))
                            if not compMobRecords:
                                status='INACTIVE'
                                mobile_no=0
                                #db.sm_comp_mobile.insert(cid=c_id,mobile_no=mobile_no,user_type='sup')
                            else:                        
                                status='ACTIVE'
                        
                        db.sm_rep.insert(cid=c_id,rep_id=rsm_id,name=rsm_name,mobile_no=mobile_no,password=randNumber,status=status,user_type='sup')
                
                    #---- Supervisor-Level                
                    ffLevelRow2=db((db.sm_supervisor_level.cid==c_id)&(db.sm_supervisor_level.sup_id==rsm_id)&(db.sm_supervisor_level.level_id==region_id)).select(db.sm_supervisor_level.sup_id,limitby=(0,1))
                    if not ffLevelRow2:
                        db.sm_supervisor_level.insert(cid=c_id,sup_id=rsm_id,sup_name=rsm_name,level_id=region_id,level_name=region_name,level_depth_no=depthNo)
                
                #--------------
                db((db.sm_area_team_temp.region_id == region_id)&(db.sm_area_team_temp.rsm_id == rsm_id)).update(rsm_flag=1)
        
        #--------FM (Field Manager/ Area Sales Manager) Part
        fmRecords=db((db.sm_area_team_temp.rsm_flag == 1)&(db.sm_area_team_temp.fm_flag == 0)).select(db.sm_area_team_temp.cid,db.sm_area_team_temp.area_id,db.sm_area_team_temp.area_name,db.sm_area_team_temp.fm_id,db.sm_area_team_temp.fm_name,db.sm_area_team_temp.fm_mobile_no,orderby=db.sm_area_team_temp.area_id|db.sm_area_team_temp.fm_id,groupby=db.sm_area_team_temp.cid|db.sm_area_team_temp.area_id|db.sm_area_team_temp.area_name|db.sm_area_team_temp.fm_id|db.sm_area_team_temp.fm_name)
        for fmRecord in fmRecords:
            c_id=fmRecord.cid
            area_id=str(fmRecord.area_id).strip().upper()
            area_name=str(fmRecord.area_name).strip().upper()
            fm_id=str(fmRecord.fm_id).strip().upper()
            fm_name=str(fmRecord.fm_name).strip()
            mobile_no=fmRecord.fm_mobile_no
            
            try:
                mobile_no=int(mobile_no)
                if len(str(mobile_no))!=13:
                    mobile_no=0                
            except:
                mobile_no=0
            
            randNumber=randint(1001, 9999)
            depthNo=2
            
            #error check
            errorFlag=False
            errorMsg=''
            if not(fm_id=='' or fm_name==''):
                ffLevelRow1=db((db.sm_supervisor_level.cid==c_id)&(db.sm_supervisor_level.sup_id==fm_id)).select(db.sm_supervisor_level.level_depth_no,limitby=(0,1))
                if ffLevelRow1:
                    level_depth_no=ffLevelRow1[0].level_depth_no
                    if level_depth_no!=depthNo:
                        errorFlag=True
                        errorMsg='Require existing and current level-depth same for FM'
            
            if (fm_id=='' and fm_name!='') or (fm_id!='' and fm_name==''):
                errorFlag=True
                errorMsg='FM ID or Name one is blank'
            
            if errorFlag==True:                
                db((db.sm_area_team_temp.area_id == area_id)&(db.sm_area_team_temp.fm_id == fm_id)).update(fm_flag=2,des=errorMsg)
            else:                
                #---- Supervisor
                if not(fm_id=='' or fm_name==''):
                    ffRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==fm_id)).select(db.sm_rep.rep_id,limitby=(0,1))
                    if not ffRow:                
                        if mobile_no==0:
                            status='INACTIVE'
                        else:
                            compMobRecords=db((db.sm_comp_mobile.cid==c_id) & (db.sm_comp_mobile.mobile_no == mobile_no)).select(db.sm_comp_mobile.mobile_no,limitby=(0,1))
                            if not compMobRecords:
                                status='INACTIVE'
                                mobile_no=0
                                #db.sm_comp_mobile.insert(cid=c_id,mobile_no=mobile_no,user_type='sup')
                            else:                        
                                status='ACTIVE'
                        
                        db.sm_rep.insert(cid=c_id,rep_id=fm_id,name=fm_name,mobile_no=mobile_no,password=randNumber,status=status,user_type='sup')
                
                    #---- Supervisor-Level                
                    ffLevelRow2=db((db.sm_supervisor_level.cid==c_id)&(db.sm_supervisor_level.sup_id==fm_id)&(db.sm_supervisor_level.level_id==area_id)).select(db.sm_supervisor_level.sup_id,limitby=(0,1))
                    if not ffLevelRow2:
                        db.sm_supervisor_level.insert(cid=c_id,sup_id=fm_id,sup_name=fm_name,level_id=area_id,level_name=area_name,level_depth_no=depthNo)
                
                #----------
                db((db.sm_area_team_temp.area_id == area_id)&(db.sm_area_team_temp.fm_id == fm_id)).update(fm_flag=1)
        #------------
        processRecords[0].update_record(status='5',notes='Step-2 processe completed')
        db.commit()
        
        return 'Step-2 completed'
        
def process_area_team_manual_step3():
    c_id=session.cid
    
    process_date=request.vars.process_date
    
    try:
        currentDate=datetime.datetime.strptime(str(process_date),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        return 'Invalid request'
        
    #----------------------------------
    processRecords=db((db.sm_area_team_process_schedule.cid==c_id)&(db.sm_area_team_process_schedule.status=='5')&(db.sm_area_team_process_schedule.schedule_date==currentDate)).select(db.sm_area_team_process_schedule.ALL,orderby=db.sm_area_team_process_schedule.first_date,limitby=(0,1))
    if not processRecords:
        return 'Process Not available'        
    else:
        first_date=processRecords[0].first_date
        schedule_date=processRecords[0].schedule_date
        #status='6',
        processRecords[0].update_record(notes='Step-3 Process running...')
        
        
        loopCount=0
        #--------MSO (Market Sales Officer) Part
        msoRecords=db((db.sm_area_team_temp.fm_flag == 1)&(db.sm_area_team_temp.mso_flag == 0)).select(db.sm_area_team_temp.cid,db.sm_area_team_temp.mso_id,db.sm_area_team_temp.mso_name,db.sm_area_team_temp.mso_mobile_no,db.sm_area_team_temp.mso_category,db.sm_area_team_temp.territory_id,db.sm_area_team_temp.territory_name,db.sm_area_team_temp.special_territory_code,orderby=db.sm_area_team_temp.mso_id|~db.sm_area_team_temp.mso_category|db.sm_area_team_temp.territory_id,groupby=db.sm_area_team_temp.cid|db.sm_area_team_temp.mso_id|db.sm_area_team_temp.mso_name|db.sm_area_team_temp.mso_mobile_no|db.sm_area_team_temp.mso_category|db.sm_area_team_temp.territory_id|db.sm_area_team_temp.territory_name|db.sm_area_team_temp.special_territory_code,limitby=(0,30))
        if not msoRecords:
            processRecords[0].update_record(status='7',notes='Step-3 process completed')
            db.commit()
            
            return 'Step-3 completed'
        else:        
            for msoRecord in msoRecords:
                c_id=msoRecord.cid            
                mso_id=str(msoRecord.mso_id).strip().upper()
                mso_name=str(msoRecord.mso_name).strip()
                mobile_no=msoRecord.mso_mobile_no
                mso_category=str(msoRecord.mso_category).strip().upper()
                territory_id=str(msoRecord.territory_id).strip().upper()
                territory_name=str(msoRecord.territory_name).strip().upper()
                special_territory_code=str(msoRecord.special_territory_code).strip().upper()
                
                try:
                    mobile_no=int(mobile_no)
                    if len(str(mobile_no))!=13:
                        mobile_no=0                
                except:
                    mobile_no=0
                
                randNumber=randint(1001, 9999)
                depthNo=2
                
                #----------- error check
                errorFlag=False
                errorMsg=''
                if mso_category not in ['A','B','Z','C']:
                    errorFlag=True
                    errorMsg='Invalid Category, Required A or B or Z or C'
                
                if errorFlag==True:                
                    db((db.sm_area_team_temp.territory_id == territory_id)&(db.sm_area_team_temp.mso_id == mso_id)).update(mso_flag=2,des=errorMsg)
                else:                
                    #---- Rep
                    ffRow=''
                    ffRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.rep_id,limitby=(0,1))
                    if not ffRow:                
                        if mobile_no==0:
                            status='INACTIVE'
                        else:
                            compMobRecords=db((db.sm_comp_mobile.cid==c_id) & (db.sm_comp_mobile.mobile_no == mobile_no)).select(db.sm_comp_mobile.mobile_no,limitby=(0,1))
                            if not compMobRecords:
                                status='INACTIVE'
                                mobile_no=0
                                #db.sm_comp_mobile.insert(cid=c_id,mobile_no=mobile_no,user_type='sup')
                            else:                        
                                status='ACTIVE'
                        
                        db.sm_rep.insert(cid=c_id,rep_id=mso_id,name=mso_name,mobile_no=mobile_no,password=randNumber,status=status,user_type='rep')
                        
                    #---- Rep-Route
                    validDataFlag=True
                    if mso_category in ['A','B','Z']:
                        ffLevelRow2=''
                        ffLevelRow2=db((db.sm_rep_area.cid==c_id)&(db.sm_rep_area.rep_id==mso_id)&(db.sm_rep_area.area_id==territory_id)).select(db.sm_rep_area.rep_category,limitby=(0,1))
                        if not ffLevelRow2:
                            db.sm_rep_area.insert(cid=c_id,rep_id=mso_id,rep_name=mso_name,area_id=territory_id,area_name=territory_name,rep_category=mso_category)
                        else:
                            existCatagory=ffLevelRow2[0].rep_category
                            errorMsg='MSO same territory already exist, existing category '+str(existCatagory)
                            db((db.sm_area_team_temp.territory_id == territory_id)&(db.sm_area_team_temp.mso_id == mso_id)&(db.sm_area_team_temp.mso_category == mso_category)).update(mso_flag=2,des=errorMsg)
                            validDataFlag=False
                    else:
                        repAreaList=[]
                        specialTerrRows=db((db.sm_area_team_temp.fm_flag == 1)&(db.sm_area_team_temp.special_territory_code == special_territory_code)).select(db.sm_area_team_temp.territory_id,db.sm_area_team_temp.territory_name,groupby=db.sm_area_team_temp.territory_id|db.sm_area_team_temp.territory_name)
                        for specialTerrRow in specialTerrRows:
                            territoryId=str(specialTerrRow.territory_id)
                            territoryName=str(specialTerrRow.territory_name)
                            
                            ffLevelRow2=''
                            ffLevelRow2=db((db.sm_rep_area.cid==c_id)&(db.sm_rep_area.rep_id==mso_id)&(db.sm_rep_area.area_id==territoryId)).select(db.sm_rep_area.rep_id,limitby=(0,1))
                            if not ffLevelRow2:
                                db.sm_rep_area.insert(cid=c_id,rep_id=mso_id,rep_name=mso_name,area_id=territoryId,area_name=territoryName,rep_category=mso_category)
                                validDataFlag=True
                            else:
                                continue
                        
                        specialTerrRows=''
                        
                    if validDataFlag==True:
                        db((db.sm_area_team_temp.territory_id == territory_id)&(db.sm_area_team_temp.mso_id == mso_id)&(db.sm_area_team_temp.mso_category == mso_category)).update(mso_flag=1,second_part_flag=1)
                    else:
                        continue
                
                #---------------
                loopCount+=1
                if loopCount==10:
                    loopCount=0
                    time.sleep(1)
                    
            #-----------
            #processRecords[0].update_record(status='7',notes='Step-3 process completed')
            db.commit()
        
            return 'Step-3 running, request again'

def process_area_team_manual_step4():
    c_id=session.cid
    
    process_date=request.vars.process_date
    
    try:
        currentDate=datetime.datetime.strptime(str(process_date),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        return 'Invalid request'
        
    #----------------------------------
    processRecords=db((db.sm_area_team_process_schedule.cid==c_id)&(db.sm_area_team_process_schedule.status=='7')&(db.sm_area_team_process_schedule.schedule_date==currentDate)).select(db.sm_area_team_process_schedule.ALL,orderby=db.sm_area_team_process_schedule.first_date,limitby=(0,1))
    if not processRecords:
        return 'Process Not available'
    else:
        first_date=processRecords[0].first_date
        schedule_date=processRecords[0].schedule_date
        
        processRecords[0].update_record(status='8',notes='Step-4 Process running...')
        
        callBackup=backup_team_structure(first_date,schedule_date)
        
        #------------
        processRecords[0].update_record(status='1',notes='Processed successfully')
        db.commit()
    
    return 'All Process completed successfully'
    
    
def process_area_team_manual_step_bak():
    c_id=session.cid
    
    process_date=request.vars.process_date
    
    try:
        currentDate=datetime.datetime.strptime(str(process_date),'%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        session.flash='Invalid request'
        redirect (URL('area_team_process_home'))
        
    #----------------------------------
    processRecords=db((db.sm_area_team_process_schedule.cid==c_id)&(db.sm_area_team_process_schedule.status=='0')&(db.sm_area_team_process_schedule.schedule_date==currentDate)).select(db.sm_area_team_process_schedule.ALL,orderby=db.sm_area_team_process_schedule.first_date,limitby=(0,1))
    if not processRecords:
        session.flash='Process Not available'
        redirect (URL('area_team_process_home'))
    else:
        first_date=processRecords[0].first_date
        schedule_date=processRecords[0].schedule_date
        
        processRecords[0].update_record(status='2',notes='Process running...')
        
        #--------- clean existing data        
        db.sm_level.truncate()
        db.sm_rep.truncate()
        db.sm_rep_area.truncate()
        db.sm_supervisor_level.truncate()
        
        #=========================== First Part
        #--------Zone Part
        zoneRecords=db(db.sm_area_team_temp.zone_flag == 0).select(db.sm_area_team_temp.cid,db.sm_area_team_temp.zone_id,db.sm_area_team_temp.zone_name,orderby=~db.sm_area_team_temp.zone_id|db.sm_area_team_temp.zone_name,groupby=db.sm_area_team_temp.cid|db.sm_area_team_temp.zone_id|db.sm_area_team_temp.zone_name)
        for zoneRecord in zoneRecords:
            c_id=zoneRecord.cid
            zone_id=str(zoneRecord.zone_id).strip().upper()
            zone_name=str(zoneRecord.zone_name).strip().upper()
            
            depthNo=0
            isLeaf='0'
            
            #Zone id set
            if zone_id=='':
                setLevelId=getLastLevelID(c_id,depthNo)
            else:
                setLevelId=zone_id
                
            #----
            errorFlag=False
            errorMsg=''
            levelIdRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==setLevelId)).select(db.sm_level.level_id,limitby=(0,1))
            if levelIdRow:
                errorFlag=True
                errorMsg='Zone ID already exist'
            else:
                levelNameRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_name.upper()==zone_name)).select(db.sm_level.level_id,limitby=(0,1))
                if levelNameRow:
                    errorFlag=True
                    errorMsg='Zone Name already exist'
                else:
                    pass
            
            #-----
            if errorFlag==True:
                db(db.sm_area_team_temp.zone_name.upper() == zone_name).update(zone_flag=2,des=errorMsg)
            else:
                level0=setLevelId
                level0_name=zone_name
                
                db.sm_level.insert(cid=c_id,level_id=setLevelId,level_name=zone_name,parent_level_id='0',parent_level_name='',is_leaf=isLeaf,depot_id='',depth=depthNo,level0=level0,level0_name=level0_name)
                
                if zone_id=='':
                    db(db.sm_area_team_temp.zone_name.upper() == zone_name).update(zone_id=setLevelId,zone_flag=1)
                else:
                    db(db.sm_area_team_temp.zone_name.upper() == zone_name).update(zone_flag=1)
                    
        #--------Region Part
        regionRecords=db((db.sm_area_team_temp.zone_flag == 1)&(db.sm_area_team_temp.region_flag == 0)).select(db.sm_area_team_temp.cid,db.sm_area_team_temp.zone_id,db.sm_area_team_temp.zone_name,db.sm_area_team_temp.region_id,db.sm_area_team_temp.region_name,orderby=~db.sm_area_team_temp.region_id|db.sm_area_team_temp.region_name,groupby=db.sm_area_team_temp.cid|db.sm_area_team_temp.zone_id|db.sm_area_team_temp.zone_name|db.sm_area_team_temp.region_id|db.sm_area_team_temp.region_name)
        for regionRecord in regionRecords:
            c_id=regionRecord.cid
            zone_id=str(regionRecord.zone_id).strip().upper()
            zone_name=str(regionRecord.zone_name).strip().upper()
            region_id=str(regionRecord.region_id).strip().upper()
            region_name=str(regionRecord.region_name).strip().upper()
            
            depthNo=1
            isLeaf='0'
            
            #Region id set
            if region_id=='':
                setLevelId=getLastLevelID(c_id,depthNo)
            else:
                setLevelId=region_id
                
            #----
            errorFlag=False
            errorMsg=''
            levelIdRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==setLevelId)).select(db.sm_level.level_id,limitby=(0,1))
            if levelIdRow:
                errorFlag=True
                errorMsg='Region ID already exist'
            else:
                levelNameRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_name.upper()==region_name)).select(db.sm_level.level_id,limitby=(0,1))
                if levelNameRow:
                    errorFlag=True
                    errorMsg='Region Name already exist'
                else:
                    pass
            
            #-----
            if errorFlag==True:
                db(db.sm_area_team_temp.region_name.upper() == region_name).update(region_flag=2,des=errorMsg)
            else:                
                level0=zone_id
                level0_name=zone_name
                level1=setLevelId
                level1_name=region_name
                
                db.sm_level.insert(cid=c_id,level_id=setLevelId,level_name=region_name,parent_level_id=zone_id,parent_level_name=zone_name,is_leaf=isLeaf,depot_id='',depth=depthNo,level0=level0,level0_name=level0_name,level1=level1,level1_name=level1_name)
                
                if region_id=='':
                    db(db.sm_area_team_temp.region_name.upper() == region_name).update(region_id=setLevelId,region_flag=1)
                else:
                    db(db.sm_area_team_temp.region_name.upper() == region_name).update(region_flag=1)
        
        time.sleep(1)
        
        #--------Area Part
        areaRecords=db((db.sm_area_team_temp.region_flag == 1)&(db.sm_area_team_temp.area_flag == 0)).select(db.sm_area_team_temp.cid,db.sm_area_team_temp.zone_id,db.sm_area_team_temp.zone_name,db.sm_area_team_temp.region_id,db.sm_area_team_temp.region_name,db.sm_area_team_temp.area_id,db.sm_area_team_temp.area_name,orderby=~db.sm_area_team_temp.area_id|db.sm_area_team_temp.area_name,groupby=db.sm_area_team_temp.cid|db.sm_area_team_temp.zone_id|db.sm_area_team_temp.zone_name|db.sm_area_team_temp.region_id|db.sm_area_team_temp.region_name|db.sm_area_team_temp.area_id|db.sm_area_team_temp.area_name)
        for areaRecord in areaRecords:
            c_id=areaRecord.cid
            zone_id=str(areaRecord.zone_id).strip().upper()
            zone_name=str(areaRecord.zone_name).strip().upper()
            region_id=str(areaRecord.region_id).strip().upper()
            region_name=str(areaRecord.region_name).strip().upper()
            area_id=str(areaRecord.area_id).strip().upper()
            area_name=str(areaRecord.area_name).strip().upper()
            
            depthNo=2
            isLeaf='0'
            
            #Area id set
            if area_id=='':
                setLevelId=getLastLevelID(c_id,depthNo)
            else:
                setLevelId=area_id
                
            #----
            errorFlag=False
            errorMsg=''
            levelIdRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==setLevelId)).select(db.sm_level.level_id,limitby=(0,1))
            if levelIdRow:
                errorFlag=True
                errorMsg='Area ID already exist'
            else:
                levelNameRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_name.upper()==area_name)).select(db.sm_level.level_id,limitby=(0,1))
                if levelNameRow:
                    errorFlag=True
                    errorMsg='Area Name already exist'
                else:
                    pass
            
            #-----
            if errorFlag==True:
                db(db.sm_area_team_temp.area_name.upper() == area_name).update(area_flag=2,des=errorMsg)
            else:                
                level0=zone_id
                level0_name=zone_name
                level1=region_id
                level1_name=region_name
                level2=setLevelId
                level2_name=area_name
                
                db.sm_level.insert(cid=c_id,level_id=setLevelId,level_name=area_name,parent_level_id=region_id,parent_level_name=region_name,is_leaf=isLeaf,depot_id='',depth=depthNo,level0=level0,level0_name=level0_name,level1=level1,level1_name=level1_name,level2=level2,level2_name=level2_name)
                
                if area_id=='':
                    db(db.sm_area_team_temp.area_name.upper() == area_name).update(area_id=setLevelId,area_flag=1)
                else:
                    db(db.sm_area_team_temp.area_name.upper() == area_name).update(area_flag=1)
        
        time.sleep(1)
        
        #--------Territory Part
        territoryRecords=db((db.sm_area_team_temp.area_flag == 1)&(db.sm_area_team_temp.territory_flag == 0)).select(db.sm_area_team_temp.cid,db.sm_area_team_temp.zone_id,db.sm_area_team_temp.zone_name,db.sm_area_team_temp.region_id,db.sm_area_team_temp.region_name,db.sm_area_team_temp.area_id,db.sm_area_team_temp.area_name,db.sm_area_team_temp.territory_id,db.sm_area_team_temp.territory_name,db.sm_area_team_temp.territory_des,db.sm_area_team_temp.special_territory_code,orderby=~db.sm_area_team_temp.territory_id|db.sm_area_team_temp.territory_name,groupby=db.sm_area_team_temp.cid|db.sm_area_team_temp.zone_id|db.sm_area_team_temp.zone_name|db.sm_area_team_temp.region_id|db.sm_area_team_temp.region_name|db.sm_area_team_temp.area_id|db.sm_area_team_temp.area_name|db.sm_area_team_temp.territory_id|db.sm_area_team_temp.territory_name|db.sm_area_team_temp.territory_des|db.sm_area_team_temp.special_territory_code)
        for territoryRecord in territoryRecords:
            c_id=territoryRecord.cid
            zone_id=str(territoryRecord.zone_id).strip().upper()
            zone_name=str(territoryRecord.zone_name).strip().upper()
            region_id=str(territoryRecord.region_id).strip().upper()
            region_name=str(territoryRecord.region_name).strip().upper()
            area_id=str(territoryRecord.area_id).strip().upper()
            area_name=str(territoryRecord.area_name).strip().upper()
            territory_id=str(territoryRecord.territory_id).strip().upper()
            territory_name=str(territoryRecord.territory_name).strip().upper()
            territory_des=str(territoryRecord.territory_des).strip().upper()
            special_territory_code=str(territoryRecord.special_territory_code).strip().upper()
            
            depthNo=3
            isLeaf='1'
            
            #Area id set
            if territory_id=='':
                setLevelId=getLastLevelID(c_id,depthNo)
            else:
                setLevelId=territory_id
                
            #----
            errorFlag=False
            errorMsg=''
            levelIdRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==setLevelId)).select(db.sm_level.level_id,limitby=(0,1))
            if levelIdRow:
                errorFlag=True
                errorMsg='Territory ID already exist'
            else:
                levelNameRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_name.upper()==territory_name)).select(db.sm_level.level_id,limitby=(0,1))
                if levelNameRow:
                    errorFlag=True
                    errorMsg='Territory Name already exist'
                else:
                    pass
            
            #-----
            if errorFlag==True:
                db(db.sm_area_team_temp.territory_name.upper() == territory_name).update(territory_flag=2,des=errorMsg)
            else:                
                level0=zone_id
                level0_name=zone_name
                level1=region_id
                level1_name=region_name
                level2=area_id
                level2_name=area_name
                level3=setLevelId
                level3_name=territory_name
                
                db.sm_level.insert(cid=c_id,level_id=setLevelId,level_name=territory_name,parent_level_id=area_id,parent_level_name=area_name,is_leaf=isLeaf,depot_id='',depth=depthNo,level0=level0,level0_name=level0_name,level1=level1,level1_name=level1_name,level2=level2,level2_name=level2_name,level3=level3,level3_name=level3_name,territory_des=territory_des,special_territory_code=special_territory_code)
                
                if territory_id=='':
                    db(db.sm_area_team_temp.territory_name.upper() == territory_name).update(territory_id=setLevelId,territory_flag=1,first_part_flag=1)
                else:
                    db(db.sm_area_team_temp.territory_name.upper() == territory_name).update(territory_flag=1,first_part_flag=1)
        
        #------------
        processRecords[0].update_record(notes='Area processe completed, Team process running...')
        time.sleep(1)
        
        #=========================== Second Part
        #--------ZM (Zonal Manager) Part
        zmRecords=db((db.sm_area_team_temp.first_part_flag == 1)&(db.sm_area_team_temp.zm_flag == 0)).select(db.sm_area_team_temp.cid,db.sm_area_team_temp.zone_id,db.sm_area_team_temp.zone_name,db.sm_area_team_temp.zm_id,db.sm_area_team_temp.zm_name,db.sm_area_team_temp.zm_mobile_no,orderby=db.sm_area_team_temp.zone_id|db.sm_area_team_temp.zm_id,groupby=db.sm_area_team_temp.cid|db.sm_area_team_temp.zone_id|db.sm_area_team_temp.zone_name|db.sm_area_team_temp.zm_id|db.sm_area_team_temp.zm_name|db.sm_area_team_temp.zm_mobile_no)
        for zmRecord in zmRecords:
            c_id=zmRecord.cid
            zone_id=str(zmRecord.zone_id).strip().upper()
            zone_name=str(zmRecord.zone_name).strip().upper()
            zm_id=str(zmRecord.zm_id).strip().upper()
            zm_name=str(zmRecord.zm_name).strip()
            mobile_no=zmRecord.zm_mobile_no
            
            try:
                mobile_no=int(mobile_no)
                if len(str(mobile_no))!=13:
                    mobile_no=0
            except:
                mobile_no=0
            
            randNumber=randint(1001, 9999)
            depthNo=0
            
            #------- error Check
            errorFlag=False
            errorMsg=''
            if not(zm_id=='' or zm_name==''):    
                ffLevelRow1=db((db.sm_supervisor_level.cid==c_id)&(db.sm_supervisor_level.sup_id==zm_id)).select(db.sm_supervisor_level.level_depth_no,limitby=(0,1))
                if ffLevelRow1:
                    level_depth_no=ffLevelRow1[0].level_depth_no
                    if level_depth_no!=depthNo:
                        errorFlag=True
                        errorMsg='Require existing and current level-depth same for ZM'
            
            if (zm_id=='' and zm_name!='') or (zm_id!='' and zm_name==''):
                errorFlag=True
                errorMsg='ZM ID or Name one is blank'
            
            #-----
            if errorFlag==True:
                db((db.sm_area_team_temp.zone_id == zone_id)&(db.sm_area_team_temp.zm_id == zm_id)).update(zm_flag=2,des=errorMsg)
            else:                
                #---- Supervisor
                if not (zm_id=='' or zm_name==''):       
                    ffRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==zm_id)).select(db.sm_rep.rep_id,limitby=(0,1))
                    if not ffRow:                
                        if mobile_no==0:
                            status='INACTIVE'
                        else:
                            compMobRecords=db((db.sm_comp_mobile.cid==c_id) & (db.sm_comp_mobile.mobile_no == mobile_no)).select(db.sm_comp_mobile.mobile_no,limitby=(0,1))
                            if not compMobRecords:
                                status='INACTIVE'
                                mobile_no=0
                                #db.sm_comp_mobile.insert(cid=c_id,mobile_no=mobile_no,user_type='sup')
                            else:                        
                                status='ACTIVE'
                        
                        db.sm_rep.insert(cid=c_id,rep_id=zm_id,name=zm_name,mobile_no=mobile_no,password=randNumber,status=status,user_type='sup')
                
                    #---- Supervisor-Level
                    ffLevelRow2=db((db.sm_supervisor_level.cid==c_id)&(db.sm_supervisor_level.sup_id==zm_id)&(db.sm_supervisor_level.level_id==zone_id)).select(db.sm_supervisor_level.sup_id,limitby=(0,1))
                    if not ffLevelRow2:
                        db.sm_supervisor_level.insert(cid=c_id,sup_id=zm_id,sup_name=zm_name,level_id=zone_id,level_name=zone_name,level_depth_no=depthNo)
                
                #----------      
                db((db.sm_area_team_temp.zone_id == zone_id)&(db.sm_area_team_temp.zm_id == zm_id)).update(zm_flag=1)
        
        
        #--------RSM (Regional Sales Manager) Part
        rsmRecords=db((db.sm_area_team_temp.zm_flag == 1)&(db.sm_area_team_temp.rsm_flag == 0)).select(db.sm_area_team_temp.cid,db.sm_area_team_temp.region_id,db.sm_area_team_temp.region_name,db.sm_area_team_temp.rsm_id,db.sm_area_team_temp.rsm_name,db.sm_area_team_temp.rsm_mobile_no,orderby=db.sm_area_team_temp.region_id|db.sm_area_team_temp.rsm_id,groupby=db.sm_area_team_temp.cid|db.sm_area_team_temp.region_id|db.sm_area_team_temp.region_name|db.sm_area_team_temp.rsm_id|db.sm_area_team_temp.rsm_name|db.sm_area_team_temp.rsm_mobile_no)
        for rsmRecord in rsmRecords:
            c_id=rsmRecord.cid
            region_id=str(rsmRecord.region_id).strip().upper()
            region_name=str(rsmRecord.region_name).strip().upper()
            rsm_id=str(rsmRecord.rsm_id).strip().upper()
            rsm_name=str(rsmRecord.rsm_name).strip()
            mobile_no=rsmRecord.rsm_mobile_no
            
            try:
                mobile_no=int(mobile_no)
                if len(str(mobile_no))!=13:
                    mobile_no=0                
            except:
                mobile_no=0
            
            randNumber=randint(1001, 9999)
            depthNo=1
            
            #error check
            errorFlag=False
            errorMsg=''
            if not (rsm_id=='' or rsm_name==''):
                ffLevelRow1=db((db.sm_supervisor_level.cid==c_id)&(db.sm_supervisor_level.sup_id==rsm_id)).select(db.sm_supervisor_level.level_depth_no,limitby=(0,1))
                if ffLevelRow1:
                    level_depth_no=ffLevelRow1[0].level_depth_no
                    if level_depth_no!=depthNo:
                        errorFlag=True
                        errorMsg='Require existing and current level-depth same for RSM'
            
            if (rsm_id=='' and rsm_name!='') or (rsm_id!='' and rsm_name==''):
                errorFlag=True
                errorMsg='RSM ID or Name one is blank'
                
            
            if errorFlag==True:
                db((db.sm_area_team_temp.region_id == region_id)&(db.sm_area_team_temp.rsm_id == rsm_id)).update(rsm_flag=2,des=errorMsg)
            else:
                #---- Supervisor
                if not (rsm_id=='' or rsm_name==''):         
                    ffRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==rsm_id)).select(db.sm_rep.rep_id,limitby=(0,1))
                    if not ffRow:                
                        if mobile_no==0:
                            status='INACTIVE'
                        else:
                            compMobRecords=db((db.sm_comp_mobile.cid==c_id) & (db.sm_comp_mobile.mobile_no == mobile_no)).select(db.sm_comp_mobile.mobile_no,limitby=(0,1))
                            if not compMobRecords:
                                status='INACTIVE'
                                mobile_no=0
                                #db.sm_comp_mobile.insert(cid=c_id,mobile_no=mobile_no,user_type='sup')
                            else:                        
                                status='ACTIVE'
                        
                        db.sm_rep.insert(cid=c_id,rep_id=rsm_id,name=rsm_name,mobile_no=mobile_no,password=randNumber,status=status,user_type='sup')
                
                    #---- Supervisor-Level                
                    ffLevelRow2=db((db.sm_supervisor_level.cid==c_id)&(db.sm_supervisor_level.sup_id==rsm_id)&(db.sm_supervisor_level.level_id==region_id)).select(db.sm_supervisor_level.sup_id,limitby=(0,1))
                    if not ffLevelRow2:
                        db.sm_supervisor_level.insert(cid=c_id,sup_id=rsm_id,sup_name=rsm_name,level_id=region_id,level_name=region_name,level_depth_no=depthNo)
                
                #--------------
                db((db.sm_area_team_temp.region_id == region_id)&(db.sm_area_team_temp.rsm_id == rsm_id)).update(rsm_flag=1)
        
        #--------FM (Field Manager/ Area Sales Manager) Part
        fmRecords=db((db.sm_area_team_temp.rsm_flag == 1)&(db.sm_area_team_temp.fm_flag == 0)).select(db.sm_area_team_temp.cid,db.sm_area_team_temp.area_id,db.sm_area_team_temp.area_name,db.sm_area_team_temp.fm_id,db.sm_area_team_temp.fm_name,db.sm_area_team_temp.fm_mobile_no,orderby=db.sm_area_team_temp.area_id|db.sm_area_team_temp.fm_id,groupby=db.sm_area_team_temp.cid|db.sm_area_team_temp.area_id|db.sm_area_team_temp.area_name|db.sm_area_team_temp.fm_id|db.sm_area_team_temp.fm_name|db.sm_area_team_temp.fm_mobile_no)
        for fmRecord in fmRecords:
            c_id=fmRecord.cid
            area_id=str(fmRecord.area_id).strip().upper()
            area_name=str(fmRecord.area_name).strip().upper()
            fm_id=str(fmRecord.fm_id).strip().upper()
            fm_name=str(fmRecord.fm_name).strip()
            mobile_no=fmRecord.fm_mobile_no
            
            try:
                mobile_no=int(mobile_no)
                if len(str(mobile_no))!=13:
                    mobile_no=0                
            except:
                mobile_no=0
            
            randNumber=randint(1001, 9999)
            depthNo=2
            
            #error check
            errorFlag=False
            errorMsg=''
            if not(fm_id=='' or fm_name==''):
                ffLevelRow1=db((db.sm_supervisor_level.cid==c_id)&(db.sm_supervisor_level.sup_id==fm_id)).select(db.sm_supervisor_level.level_depth_no,limitby=(0,1))
                if ffLevelRow1:
                    level_depth_no=ffLevelRow1[0].level_depth_no
                    if level_depth_no!=depthNo:
                        errorFlag=True
                        errorMsg='Require existing and current level-depth same for FM'
            
            if (fm_id=='' and fm_name!='') or (fm_id!='' and fm_name==''):
                errorFlag=True
                errorMsg='FM ID or Name one is blank'
            
            if errorFlag==True:                
                db((db.sm_area_team_temp.area_id == area_id)&(db.sm_area_team_temp.fm_id == fm_id)).update(fm_flag=2,des=errorMsg)
            else:                
                #---- Supervisor
                if not(fm_id=='' or fm_name==''):
                    ffRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==fm_id)).select(db.sm_rep.rep_id,limitby=(0,1))
                    if not ffRow:                
                        if mobile_no==0:
                            status='INACTIVE'
                        else:
                            compMobRecords=db((db.sm_comp_mobile.cid==c_id) & (db.sm_comp_mobile.mobile_no == mobile_no)).select(db.sm_comp_mobile.mobile_no,limitby=(0,1))
                            if not compMobRecords:
                                status='INACTIVE'
                                mobile_no=0
                                #db.sm_comp_mobile.insert(cid=c_id,mobile_no=mobile_no,user_type='sup')
                            else:                        
                                status='ACTIVE'
                        
                        db.sm_rep.insert(cid=c_id,rep_id=fm_id,name=fm_name,mobile_no=mobile_no,password=randNumber,status=status,user_type='sup')
                
                    #---- Supervisor-Level                
                    ffLevelRow2=db((db.sm_supervisor_level.cid==c_id)&(db.sm_supervisor_level.sup_id==fm_id)&(db.sm_supervisor_level.level_id==area_id)).select(db.sm_supervisor_level.sup_id,limitby=(0,1))
                    if not ffLevelRow2:
                        db.sm_supervisor_level.insert(cid=c_id,sup_id=fm_id,sup_name=fm_name,level_id=area_id,level_name=area_name,level_depth_no=depthNo)
                
                #----------
                db((db.sm_area_team_temp.area_id == area_id)&(db.sm_area_team_temp.fm_id == fm_id)).update(fm_flag=1)
                
        #--------MSO (Market Sales Officer) Part
        msoRecords=db((db.sm_area_team_temp.fm_flag == 1)&(db.sm_area_team_temp.mso_flag == 0)).select(db.sm_area_team_temp.cid,db.sm_area_team_temp.mso_id,db.sm_area_team_temp.mso_name,db.sm_area_team_temp.mso_mobile_no,db.sm_area_team_temp.mso_category,db.sm_area_team_temp.territory_id,db.sm_area_team_temp.territory_name,db.sm_area_team_temp.special_territory_code,orderby=db.sm_area_team_temp.mso_id|~db.sm_area_team_temp.mso_category|db.sm_area_team_temp.territory_id,groupby=db.sm_area_team_temp.cid|db.sm_area_team_temp.mso_id|db.sm_area_team_temp.mso_name|db.sm_area_team_temp.mso_mobile_no|db.sm_area_team_temp.mso_category|db.sm_area_team_temp.territory_id|db.sm_area_team_temp.territory_name|db.sm_area_team_temp.special_territory_code)
        for msoRecord in msoRecords:
            c_id=msoRecord.cid            
            mso_id=str(msoRecord.mso_id).strip().upper()
            mso_name=str(msoRecord.mso_name).strip()
            mobile_no=msoRecord.mso_mobile_no
            mso_category=str(msoRecord.mso_category).strip().upper()
            territory_id=str(msoRecord.territory_id).strip().upper()
            territory_name=str(msoRecord.territory_name).strip().upper()
            special_territory_code=str(msoRecord.special_territory_code).strip().upper()
            
            try:
                mobile_no=int(mobile_no)
                if len(str(mobile_no))!=13:
                    mobile_no=0                
            except:
                mobile_no=0
            
            randNumber=randint(1001, 9999)
            depthNo=2
            
            #----------- error check
            errorFlag=False
            errorMsg=''
            if mso_category not in ['A','B','Z','C']:
                errorFlag=True
                errorMsg='Invalid Category, Required A or B or Z or C'
            
            if errorFlag==True:                
                db((db.sm_area_team_temp.territory_id == territory_id)&(db.sm_area_team_temp.mso_id == mso_id)).update(mso_flag=2,des=errorMsg)
            else:                
                #---- Rep            
                ffRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.rep_id,limitby=(0,1))
                if not ffRow:                
                    if mobile_no==0:
                        status='INACTIVE'
                    else:
                        compMobRecords=db((db.sm_comp_mobile.cid==c_id) & (db.sm_comp_mobile.mobile_no == mobile_no)).select(db.sm_comp_mobile.mobile_no,limitby=(0,1))
                        if not compMobRecords:
                            status='INACTIVE'
                            mobile_no=0
                            #db.sm_comp_mobile.insert(cid=c_id,mobile_no=mobile_no,user_type='sup')
                        else:                        
                            status='ACTIVE'
                    
                    db.sm_rep.insert(cid=c_id,rep_id=mso_id,name=mso_name,mobile_no=mobile_no,password=randNumber,status=status,user_type='rep')
                    
                #---- Rep-Route
                validDataFlag=True
                if mso_category in ['A','B','Z']:
                    ffLevelRow2=db((db.sm_rep_area.cid==c_id)&(db.sm_rep_area.rep_id==mso_id)&(db.sm_rep_area.area_id==territory_id)).select(db.sm_rep_area.rep_category,limitby=(0,1))
                    if not ffLevelRow2:
                        db.sm_rep_area.insert(cid=c_id,rep_id=mso_id,rep_name=mso_name,area_id=territory_id,area_name=territory_name,rep_category=mso_category)
                    else:
                        existCatagory=ffLevelRow2[0].rep_category
                        errorMsg='MSO same territory already exist, existing category '+str(existCatagory)
                        db((db.sm_area_team_temp.territory_id == territory_id)&(db.sm_area_team_temp.mso_id == mso_id)&(db.sm_area_team_temp.mso_category == mso_category)).update(mso_flag=2,des=errorMsg)
                        validDataFlag=False
                else:
                    repAreaList=[]
                    specialTerrRows=db((db.sm_area_team_temp.fm_flag == 1)&(db.sm_area_team_temp.special_territory_code == special_territory_code)).select(db.sm_area_team_temp.territory_id,db.sm_area_team_temp.territory_name,groupby=db.sm_area_team_temp.territory_id|db.sm_area_team_temp.territory_name)
                    for specialTerrRow in specialTerrRows:
                        territoryId=str(specialTerrRow.territory_id)
                        territoryName=str(specialTerrRow.territory_name)
                        
                        ffLevelRow2=db((db.sm_rep_area.cid==c_id)&(db.sm_rep_area.rep_id==mso_id)&(db.sm_rep_area.area_id==territoryId)).select(db.sm_rep_area.rep_id,limitby=(0,1))
                        if not ffLevelRow2:
                            db.sm_rep_area.insert(cid=c_id,rep_id=mso_id,rep_name=mso_name,area_id=territoryId,area_name=territoryName,rep_category=mso_category)
                            validDataFlag=True
                        else:
                            continue
                
                if validDataFlag==True:
                    db((db.sm_area_team_temp.territory_id == territory_id)&(db.sm_area_team_temp.mso_id == mso_id)&(db.sm_area_team_temp.mso_category == mso_category)).update(mso_flag=1,second_part_flag=1)
                    
        #-----------
        time.sleep(1)
        
        callBackup=backup_team_structure(first_date,schedule_date)
        
        #------------
        processRecords[0].update_record(status='1',notes='Processed successfully')
        db.commit()
    
    session.flash='Processed successfully'
    redirect (URL('area_team_process_home'))
#Cron
#http://127.0.0.1:8000/mrepskf/level/process_area_team
def process_area_team():
    currentDate=current_date
         
    #----------------------------------
    processRecords=db((db.sm_area_team_process_schedule.status=='0')&(db.sm_area_team_process_schedule.schedule_date==currentDate)).select(db.sm_area_team_process_schedule.ALL,orderby=db.sm_area_team_process_schedule.first_date,limitby=(0,1))
    if not processRecords:
        return 'Process Not available'
    else:
        c_id=processRecords[0].cid
        first_date=processRecords[0].first_date
        schedule_date=processRecords[0].schedule_date
        
        processRecords[0].update_record(status='2',notes='Process running...')
        
        #--------- clean existing data        
        db.sm_level.truncate()
        db.sm_rep.truncate()
        db.sm_rep_area.truncate()
        db.sm_supervisor_level.truncate()
        
        
        #=========================== First Part
        #--------Zone Part
        zoneRecords=db(db.sm_area_team_temp.zone_flag == 0).select(db.sm_area_team_temp.cid,db.sm_area_team_temp.zone_id,db.sm_area_team_temp.zone_name,orderby=~db.sm_area_team_temp.zone_id|db.sm_area_team_temp.zone_name,groupby=db.sm_area_team_temp.cid|db.sm_area_team_temp.zone_id|db.sm_area_team_temp.zone_name)
        for zoneRecord in zoneRecords:
            c_id=zoneRecord.cid
            zone_id=str(zoneRecord.zone_id).strip().upper()
            zone_name=str(zoneRecord.zone_name).strip().upper()
            
            depthNo=0
            isLeaf='0'
            
            #Zone id set
            if zone_id=='':
                setLevelId=getLastLevelID(c_id,depthNo)
            else:
                setLevelId=zone_id
                
            #----
            errorFlag=False
            errorMsg=''
            levelIdRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==setLevelId)).select(db.sm_level.level_id,limitby=(0,1))
            if levelIdRow:
                errorFlag=True
                errorMsg='Zone ID already exist'
            else:
                levelNameRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_name.upper()==zone_name)).select(db.sm_level.level_id,limitby=(0,1))
                if levelNameRow:
                    errorFlag=True
                    errorMsg='Zone Name already exist'
                else:
                    pass
            
            #-----
            if errorFlag==True:
                db(db.sm_area_team_temp.zone_name.upper() == zone_name).update(zone_flag=2,des=errorMsg)
            else:
                level0=setLevelId
                level0_name=zone_name
                
                db.sm_level.insert(cid=c_id,level_id=setLevelId,level_name=zone_name,parent_level_id='0',parent_level_name='',is_leaf=isLeaf,depot_id='',depth=depthNo,level0=level0,level0_name=level0_name)
                
                if zone_id=='':
                    db(db.sm_area_team_temp.zone_name.upper() == zone_name).update(zone_id=setLevelId,zone_flag=1)
                else:
                    db(db.sm_area_team_temp.zone_name.upper() == zone_name).update(zone_flag=1)
                    
        #--------Region Part
        regionRecords=db((db.sm_area_team_temp.zone_flag == 1)&(db.sm_area_team_temp.region_flag == 0)).select(db.sm_area_team_temp.cid,db.sm_area_team_temp.zone_id,db.sm_area_team_temp.zone_name,db.sm_area_team_temp.region_id,db.sm_area_team_temp.region_name,orderby=~db.sm_area_team_temp.region_id|db.sm_area_team_temp.region_name,groupby=db.sm_area_team_temp.cid|db.sm_area_team_temp.zone_id|db.sm_area_team_temp.zone_name|db.sm_area_team_temp.region_id|db.sm_area_team_temp.region_name)
        for regionRecord in regionRecords:
            c_id=regionRecord.cid
            zone_id=str(regionRecord.zone_id).strip().upper()
            zone_name=str(regionRecord.zone_name).strip().upper()
            region_id=str(regionRecord.region_id).strip().upper()
            region_name=str(regionRecord.region_name).strip().upper()
            
            depthNo=1
            isLeaf='0'
            
            #Region id set
            if region_id=='':
                setLevelId=getLastLevelID(c_id,depthNo)
            else:
                setLevelId=region_id
                
            #----
            errorFlag=False
            errorMsg=''
            levelIdRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==setLevelId)).select(db.sm_level.level_id,limitby=(0,1))
            if levelIdRow:
                errorFlag=True
                errorMsg='Region ID already exist'
            else:
                levelNameRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_name.upper()==region_name)).select(db.sm_level.level_id,limitby=(0,1))
                if levelNameRow:
                    errorFlag=True
                    errorMsg='Region Name already exist'
                else:
                    pass
            
            #-----
            if errorFlag==True:
                db(db.sm_area_team_temp.region_name.upper() == region_name).update(region_flag=2,des=errorMsg)
            else:                
                level0=zone_id
                level0_name=zone_name
                level1=setLevelId
                level1_name=region_name
                
                db.sm_level.insert(cid=c_id,level_id=setLevelId,level_name=region_name,parent_level_id=zone_id,parent_level_name=zone_name,is_leaf=isLeaf,depot_id='',depth=depthNo,level0=level0,level0_name=level0_name,level1=level1,level1_name=level1_name)
                
                if region_id=='':
                    db(db.sm_area_team_temp.region_name.upper() == region_name).update(region_id=setLevelId,region_flag=1)
                else:
                    db(db.sm_area_team_temp.region_name.upper() == region_name).update(region_flag=1)
        
        time.sleep(1)
        
        #--------Area Part
        areaRecords=db((db.sm_area_team_temp.region_flag == 1)&(db.sm_area_team_temp.area_flag == 0)).select(db.sm_area_team_temp.cid,db.sm_area_team_temp.zone_id,db.sm_area_team_temp.zone_name,db.sm_area_team_temp.region_id,db.sm_area_team_temp.region_name,db.sm_area_team_temp.area_id,db.sm_area_team_temp.area_name,orderby=~db.sm_area_team_temp.area_id|db.sm_area_team_temp.area_name,groupby=db.sm_area_team_temp.cid|db.sm_area_team_temp.zone_id|db.sm_area_team_temp.zone_name|db.sm_area_team_temp.region_id|db.sm_area_team_temp.region_name|db.sm_area_team_temp.area_id|db.sm_area_team_temp.area_name)
        for areaRecord in areaRecords:
            c_id=areaRecord.cid
            zone_id=str(areaRecord.zone_id).strip().upper()
            zone_name=str(areaRecord.zone_name).strip().upper()
            region_id=str(areaRecord.region_id).strip().upper()
            region_name=str(areaRecord.region_name).strip().upper()
            area_id=str(areaRecord.area_id).strip().upper()
            area_name=str(areaRecord.area_name).strip().upper()
            
            depthNo=2
            isLeaf='0'
            
            #Area id set
            if area_id=='':
                setLevelId=getLastLevelID(c_id,depthNo)
            else:
                setLevelId=area_id
                
            #----
            errorFlag=False
            errorMsg=''
            levelIdRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==setLevelId)).select(db.sm_level.level_id,limitby=(0,1))
            if levelIdRow:
                errorFlag=True
                errorMsg='Area ID already exist'
            else:
                levelNameRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_name.upper()==area_name)).select(db.sm_level.level_id,limitby=(0,1))
                if levelNameRow:
                    errorFlag=True
                    errorMsg='Area Name already exist'
                else:
                    pass
            
            #-----
            if errorFlag==True:
                db(db.sm_area_team_temp.area_name.upper() == area_name).update(area_flag=2,des=errorMsg)
            else:                
                level0=zone_id
                level0_name=zone_name
                level1=region_id
                level1_name=region_name
                level2=setLevelId
                level2_name=area_name
                
                db.sm_level.insert(cid=c_id,level_id=setLevelId,level_name=area_name,parent_level_id=region_id,parent_level_name=region_name,is_leaf=isLeaf,depot_id='',depth=depthNo,level0=level0,level0_name=level0_name,level1=level1,level1_name=level1_name,level2=level2,level2_name=level2_name)
                
                if area_id=='':
                    db(db.sm_area_team_temp.area_name.upper() == area_name).update(area_id=setLevelId,area_flag=1)
                else:
                    db(db.sm_area_team_temp.area_name.upper() == area_name).update(area_flag=1)
        
        time.sleep(1)
        
        #--------Territory Part
        territoryRecords=db((db.sm_area_team_temp.area_flag == 1)&(db.sm_area_team_temp.territory_flag == 0)).select(db.sm_area_team_temp.cid,db.sm_area_team_temp.zone_id,db.sm_area_team_temp.zone_name,db.sm_area_team_temp.region_id,db.sm_area_team_temp.region_name,db.sm_area_team_temp.area_id,db.sm_area_team_temp.area_name,db.sm_area_team_temp.territory_id,db.sm_area_team_temp.territory_name,db.sm_area_team_temp.territory_des,db.sm_area_team_temp.special_territory_code,orderby=~db.sm_area_team_temp.territory_id|db.sm_area_team_temp.territory_name,groupby=db.sm_area_team_temp.cid|db.sm_area_team_temp.zone_id|db.sm_area_team_temp.zone_name|db.sm_area_team_temp.region_id|db.sm_area_team_temp.region_name|db.sm_area_team_temp.area_id|db.sm_area_team_temp.area_name|db.sm_area_team_temp.territory_id|db.sm_area_team_temp.territory_name|db.sm_area_team_temp.territory_des|db.sm_area_team_temp.special_territory_code)
        for territoryRecord in territoryRecords:
            c_id=territoryRecord.cid
            zone_id=str(territoryRecord.zone_id).strip().upper()
            zone_name=str(territoryRecord.zone_name).strip().upper()
            region_id=str(territoryRecord.region_id).strip().upper()
            region_name=str(territoryRecord.region_name).strip().upper()
            area_id=str(territoryRecord.area_id).strip().upper()
            area_name=str(territoryRecord.area_name).strip().upper()
            territory_id=str(territoryRecord.territory_id).strip().upper()
            territory_name=str(territoryRecord.territory_name).strip().upper()
            territory_des=str(territoryRecord.territory_des).strip().upper()
            special_territory_code=str(territoryRecord.special_territory_code).strip().upper()
            
            depthNo=3
            isLeaf='1'
            
            #Area id set
            if territory_id=='':
                setLevelId=getLastLevelID(c_id,depthNo)
            else:
                setLevelId=territory_id
                
            #----
            errorFlag=False
            errorMsg=''
            levelIdRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==setLevelId)).select(db.sm_level.level_id,limitby=(0,1))
            if levelIdRow:
                errorFlag=True
                errorMsg='Territory ID already exist'
            else:
                levelNameRow=db((db.sm_level.cid==c_id)&(db.sm_level.level_name.upper()==territory_name)).select(db.sm_level.level_id,limitby=(0,1))
                if levelNameRow:
                    errorFlag=True
                    errorMsg='Territory Name already exist'
                else:
                    pass
            
            #-----
            if errorFlag==True:
                db(db.sm_area_team_temp.territory_name.upper() == territory_name).update(territory_flag=2,des=errorMsg)
            else:                
                level0=zone_id
                level0_name=zone_name
                level1=region_id
                level1_name=region_name
                level2=area_id
                level2_name=area_name
                level3=setLevelId
                level3_name=territory_name
                
                db.sm_level.insert(cid=c_id,level_id=setLevelId,level_name=territory_name,parent_level_id=area_id,parent_level_name=area_name,is_leaf=isLeaf,depot_id='',depth=depthNo,level0=level0,level0_name=level0_name,level1=level1,level1_name=level1_name,level2=level2,level2_name=level2_name,level3=level3,level3_name=level3_name,territory_des=territory_des,special_territory_code=special_territory_code)
                
                if territory_id=='':
                    db(db.sm_area_team_temp.territory_name.upper() == territory_name).update(territory_id=setLevelId,territory_flag=1,first_part_flag=1)
                else:
                    db(db.sm_area_team_temp.territory_name.upper() == territory_name).update(territory_flag=1,first_part_flag=1)
        
        #------------
        processRecords[0].update_record(notes='Area processe completed, Team process running...')
        time.sleep(2)
        
        #=========================== Second Part
        #--------ZM (Zonal Manager) Part
        zmRecords=db((db.sm_area_team_temp.first_part_flag == 1)&(db.sm_area_team_temp.zm_flag == 0)).select(db.sm_area_team_temp.cid,db.sm_area_team_temp.zone_id,db.sm_area_team_temp.zone_name,db.sm_area_team_temp.zm_id,db.sm_area_team_temp.zm_name,db.sm_area_team_temp.zm_mobile_no,orderby=db.sm_area_team_temp.zone_id|db.sm_area_team_temp.zm_id,groupby=db.sm_area_team_temp.cid|db.sm_area_team_temp.zone_id|db.sm_area_team_temp.zone_name|db.sm_area_team_temp.zm_id|db.sm_area_team_temp.zm_name|db.sm_area_team_temp.zm_mobile_no)
        for zmRecord in zmRecords:
            c_id=zmRecord.cid
            zone_id=str(zmRecord.zone_id).strip().upper()
            zone_name=str(zmRecord.zone_name).strip().upper()
            zm_id=str(zmRecord.zm_id).strip().upper()
            zm_name=str(zmRecord.zm_name).strip()
            mobile_no=zmRecord.zm_mobile_no
            
            try:
                mobile_no=int(mobile_no)
                if len(str(mobile_no))!=13:
                    mobile_no=0
            except:
                mobile_no=0
            
            randNumber=randint(1001, 9999)
            depthNo=0
            
            #------- error Check
            errorFlag=False
            errorMsg=''
            if not(zm_id=='' or zm_name==''):    
                ffLevelRow1=db((db.sm_supervisor_level.cid==c_id)&(db.sm_supervisor_level.sup_id==zm_id)).select(db.sm_supervisor_level.level_depth_no,limitby=(0,1))
                if ffLevelRow1:
                    level_depth_no=ffLevelRow1[0].level_depth_no
                    if level_depth_no!=depthNo:
                        errorFlag=True
                        errorMsg='Require existing and current level-depth same for ZM'
            
            if (zm_id=='' and zm_name!='') or (zm_id!='' and zm_name==''):
                errorFlag=True
                errorMsg='ZM ID or Name one is blank'
            
            #-----
            if errorFlag==True:
                db((db.sm_area_team_temp.zone_id == zone_id)&(db.sm_area_team_temp.zm_id == zm_id)).update(zm_flag=2,des=errorMsg)
            else:                
                #---- Supervisor
                if not (zm_id=='' or zm_name==''):       
                    ffRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==zm_id)).select(db.sm_rep.rep_id,limitby=(0,1))
                    if not ffRow:                
                        if mobile_no==0:
                            status='INACTIVE'
                        else:
                            compMobRecords=db((db.sm_comp_mobile.cid==c_id) & (db.sm_comp_mobile.mobile_no == mobile_no)).select(db.sm_comp_mobile.mobile_no,limitby=(0,1))
                            if not compMobRecords:
                                status='INACTIVE'
                                mobile_no=0
                                #db.sm_comp_mobile.insert(cid=c_id,mobile_no=mobile_no,user_type='sup')
                            else:                        
                                status='ACTIVE'
                        
                        db.sm_rep.insert(cid=c_id,rep_id=zm_id,name=zm_name,mobile_no=mobile_no,password=randNumber,status=status,user_type='sup')
                
                    #---- Supervisor-Level
                    ffLevelRow2=db((db.sm_supervisor_level.cid==c_id)&(db.sm_supervisor_level.sup_id==zm_id)&(db.sm_supervisor_level.level_id==zone_id)).select(db.sm_supervisor_level.sup_id,limitby=(0,1))
                    if not ffLevelRow2:
                        db.sm_supervisor_level.insert(cid=c_id,sup_id=zm_id,sup_name=zm_name,level_id=zone_id,level_name=zone_name,level_depth_no=depthNo)
                
                #----------      
                db((db.sm_area_team_temp.zone_id == zone_id)&(db.sm_area_team_temp.zm_id == zm_id)).update(zm_flag=1)
        
        
        #--------RSM (Regional Sales Manager) Part
        rsmRecords=db((db.sm_area_team_temp.zm_flag == 1)&(db.sm_area_team_temp.rsm_flag == 0)).select(db.sm_area_team_temp.cid,db.sm_area_team_temp.region_id,db.sm_area_team_temp.region_name,db.sm_area_team_temp.rsm_id,db.sm_area_team_temp.rsm_name,db.sm_area_team_temp.rsm_mobile_no,orderby=db.sm_area_team_temp.region_id|db.sm_area_team_temp.rsm_id,groupby=db.sm_area_team_temp.cid|db.sm_area_team_temp.region_id|db.sm_area_team_temp.region_name|db.sm_area_team_temp.rsm_id|db.sm_area_team_temp.rsm_name|db.sm_area_team_temp.rsm_mobile_no)
        for rsmRecord in rsmRecords:
            c_id=rsmRecord.cid
            region_id=str(rsmRecord.region_id).strip().upper()
            region_name=str(rsmRecord.region_name).strip().upper()
            rsm_id=str(rsmRecord.rsm_id).strip().upper()
            rsm_name=str(rsmRecord.rsm_name).strip()
            mobile_no=rsmRecord.rsm_mobile_no
            
            try:
                mobile_no=int(mobile_no)
                if len(str(mobile_no))!=13:
                    mobile_no=0                
            except:
                mobile_no=0
            
            randNumber=randint(1001, 9999)
            depthNo=1
            
            #error check
            errorFlag=False
            errorMsg=''
            if not (rsm_id=='' or rsm_name==''):
                ffLevelRow1=db((db.sm_supervisor_level.cid==c_id)&(db.sm_supervisor_level.sup_id==rsm_id)).select(db.sm_supervisor_level.level_depth_no,limitby=(0,1))
                if ffLevelRow1:
                    level_depth_no=ffLevelRow1[0].level_depth_no
                    if level_depth_no!=depthNo:
                        errorFlag=True
                        errorMsg='Require existing and current level-depth same for RSM'
            
            if (rsm_id=='' and rsm_name!='') or (rsm_id!='' and rsm_name==''):
                errorFlag=True
                errorMsg='RSM ID or Name one is blank'
                
            
            if errorFlag==True:
                db((db.sm_area_team_temp.region_id == region_id)&(db.sm_area_team_temp.rsm_id == rsm_id)).update(rsm_flag=2,des=errorMsg)
            else:
                #---- Supervisor
                if not (rsm_id=='' or rsm_name==''):         
                    ffRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==rsm_id)).select(db.sm_rep.rep_id,limitby=(0,1))
                    if not ffRow:                
                        if mobile_no==0:
                            status='INACTIVE'
                        else:
                            compMobRecords=db((db.sm_comp_mobile.cid==c_id) & (db.sm_comp_mobile.mobile_no == mobile_no)).select(db.sm_comp_mobile.mobile_no,limitby=(0,1))
                            if not compMobRecords:
                                status='INACTIVE'
                                mobile_no=0
                                #db.sm_comp_mobile.insert(cid=c_id,mobile_no=mobile_no,user_type='sup')
                            else:                        
                                status='ACTIVE'
                        
                        db.sm_rep.insert(cid=c_id,rep_id=rsm_id,name=rsm_name,mobile_no=mobile_no,password=randNumber,status=status,user_type='sup')
                
                    #---- Supervisor-Level                
                    ffLevelRow2=db((db.sm_supervisor_level.cid==c_id)&(db.sm_supervisor_level.sup_id==rsm_id)&(db.sm_supervisor_level.level_id==region_id)).select(db.sm_supervisor_level.sup_id,limitby=(0,1))
                    if not ffLevelRow2:
                        db.sm_supervisor_level.insert(cid=c_id,sup_id=rsm_id,sup_name=rsm_name,level_id=region_id,level_name=region_name,level_depth_no=depthNo)
                
                #--------------
                db((db.sm_area_team_temp.region_id == region_id)&(db.sm_area_team_temp.rsm_id == rsm_id)).update(rsm_flag=1)
        
        #--------FM (Field Manager/ Area Sales Manager) Part
        fmRecords=db((db.sm_area_team_temp.rsm_flag == 1)&(db.sm_area_team_temp.fm_flag == 0)).select(db.sm_area_team_temp.cid,db.sm_area_team_temp.area_id,db.sm_area_team_temp.area_name,db.sm_area_team_temp.fm_id,db.sm_area_team_temp.fm_name,db.sm_area_team_temp.fm_mobile_no,orderby=db.sm_area_team_temp.area_id|db.sm_area_team_temp.fm_id,groupby=db.sm_area_team_temp.cid|db.sm_area_team_temp.area_id|db.sm_area_team_temp.area_name|db.sm_area_team_temp.fm_id|db.sm_area_team_temp.fm_name|db.sm_area_team_temp.fm_mobile_no)
        for fmRecord in fmRecords:
            c_id=fmRecord.cid
            area_id=str(fmRecord.area_id).strip().upper()
            area_name=str(fmRecord.area_name).strip().upper()
            fm_id=str(fmRecord.fm_id).strip().upper()
            fm_name=str(fmRecord.fm_name).strip()
            mobile_no=fmRecord.fm_mobile_no
            
            try:
                mobile_no=int(mobile_no)
                if len(str(mobile_no))!=13:
                    mobile_no=0                
            except:
                mobile_no=0
            
            randNumber=randint(1001, 9999)
            depthNo=2
            
            #error check
            errorFlag=False
            errorMsg=''
            if not(fm_id=='' or fm_name==''):
                ffLevelRow1=db((db.sm_supervisor_level.cid==c_id)&(db.sm_supervisor_level.sup_id==fm_id)).select(db.sm_supervisor_level.level_depth_no,limitby=(0,1))
                if ffLevelRow1:
                    level_depth_no=ffLevelRow1[0].level_depth_no
                    if level_depth_no!=depthNo:
                        errorFlag=True
                        errorMsg='Require existing and current level-depth same for FM'
            
            if (fm_id=='' and fm_name!='') or (fm_id!='' and fm_name==''):
                errorFlag=True
                errorMsg='FM ID or Name one is blank'
            
            if errorFlag==True:                
                db((db.sm_area_team_temp.area_id == area_id)&(db.sm_area_team_temp.fm_id == fm_id)).update(fm_flag=2,des=errorMsg)
            else:                
                #---- Supervisor
                if not(fm_id=='' or fm_name==''):
                    ffRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==fm_id)).select(db.sm_rep.rep_id,limitby=(0,1))
                    if not ffRow:                
                        if mobile_no==0:
                            status='INACTIVE'
                        else:
                            compMobRecords=db((db.sm_comp_mobile.cid==c_id) & (db.sm_comp_mobile.mobile_no == mobile_no)).select(db.sm_comp_mobile.mobile_no,limitby=(0,1))
                            if not compMobRecords:
                                status='INACTIVE'
                                mobile_no=0
                                #db.sm_comp_mobile.insert(cid=c_id,mobile_no=mobile_no,user_type='sup')
                            else:                        
                                status='ACTIVE'
                        
                        db.sm_rep.insert(cid=c_id,rep_id=fm_id,name=fm_name,mobile_no=mobile_no,password=randNumber,status=status,user_type='sup')
                
                    #---- Supervisor-Level                
                    ffLevelRow2=db((db.sm_supervisor_level.cid==c_id)&(db.sm_supervisor_level.sup_id==fm_id)&(db.sm_supervisor_level.level_id==area_id)).select(db.sm_supervisor_level.sup_id,limitby=(0,1))
                    if not ffLevelRow2:
                        db.sm_supervisor_level.insert(cid=c_id,sup_id=fm_id,sup_name=fm_name,level_id=area_id,level_name=area_name,level_depth_no=depthNo)
                
                #----------
                db((db.sm_area_team_temp.area_id == area_id)&(db.sm_area_team_temp.fm_id == fm_id)).update(fm_flag=1)
        
        #--------MSO (Market Sales Officer) Part
        msoRecords=db((db.sm_area_team_temp.fm_flag == 1)&(db.sm_area_team_temp.mso_flag == 0)).select(db.sm_area_team_temp.cid,db.sm_area_team_temp.mso_id,db.sm_area_team_temp.mso_name,db.sm_area_team_temp.mso_mobile_no,db.sm_area_team_temp.mso_category,db.sm_area_team_temp.territory_id,db.sm_area_team_temp.territory_name,db.sm_area_team_temp.special_territory_code,orderby=db.sm_area_team_temp.mso_id|~db.sm_area_team_temp.mso_category|db.sm_area_team_temp.territory_id,groupby=db.sm_area_team_temp.cid|db.sm_area_team_temp.mso_id|db.sm_area_team_temp.mso_name|db.sm_area_team_temp.mso_mobile_no|db.sm_area_team_temp.mso_category|db.sm_area_team_temp.territory_id|db.sm_area_team_temp.territory_name|db.sm_area_team_temp.special_territory_code)
        for msoRecord in msoRecords:
            c_id=msoRecord.cid            
            mso_id=str(msoRecord.mso_id).strip().upper()
            mso_name=str(msoRecord.mso_name).strip()
            mobile_no=msoRecord.mso_mobile_no
            mso_category=str(msoRecord.mso_category).strip().upper()
            territory_id=str(msoRecord.territory_id).strip().upper()
            territory_name=str(msoRecord.territory_name).strip().upper()
            special_territory_code=str(msoRecord.special_territory_code).strip().upper()
            
            try:
                mobile_no=int(mobile_no)
                if len(str(mobile_no))!=13:
                    mobile_no=0                
            except:
                mobile_no=0
            
            randNumber=randint(1001, 9999)
            depthNo=2
            
            #----------- error check
            errorFlag=False
            errorMsg=''
            if mso_category not in ['A','B','Z','C']:
                errorFlag=True
                errorMsg='Invalid Category, Required A or B or Z or C'
            
            if errorFlag==True:                
                db((db.sm_area_team_temp.territory_id == territory_id)&(db.sm_area_team_temp.mso_id == mso_id)).update(mso_flag=2,des=errorMsg)
            else:                
                #---- Rep            
                ffRow=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id==mso_id)).select(db.sm_rep.rep_id,limitby=(0,1))
                if not ffRow:                
                    if mobile_no==0:
                        status='INACTIVE'
                    else:
                        compMobRecords=db((db.sm_comp_mobile.cid==c_id) & (db.sm_comp_mobile.mobile_no == mobile_no)).select(db.sm_comp_mobile.mobile_no,limitby=(0,1))
                        if not compMobRecords:
                            status='INACTIVE'
                            mobile_no=0
                            #db.sm_comp_mobile.insert(cid=c_id,mobile_no=mobile_no,user_type='sup')
                        else:                        
                            status='ACTIVE'
                    
                    db.sm_rep.insert(cid=c_id,rep_id=mso_id,name=mso_name,mobile_no=mobile_no,password=randNumber,status=status,user_type='rep')
                    
                #---- Rep-Route
                validDataFlag=True
                if mso_category in ['A','B','Z']:
                    ffLevelRow2=db((db.sm_rep_area.cid==c_id)&(db.sm_rep_area.rep_id==mso_id)&(db.sm_rep_area.area_id==territory_id)).select(db.sm_rep_area.rep_category,limitby=(0,1))
                    if not ffLevelRow2:
                        db.sm_rep_area.insert(cid=c_id,rep_id=mso_id,rep_name=mso_name,area_id=territory_id,area_name=territory_name,rep_category=mso_category)
                    else:
                        existCatagory=ffLevelRow2[0].rep_category
                        errorMsg='MSO same territory already exist, existing category '+str(existCatagory)
                        db((db.sm_area_team_temp.territory_id == territory_id)&(db.sm_area_team_temp.mso_id == mso_id)&(db.sm_area_team_temp.mso_category == mso_category)).update(mso_flag=2,des=errorMsg)
                        validDataFlag=False
                else:
                    repAreaList=[]
                    specialTerrRows=db((db.sm_area_team_temp.fm_flag == 1)&(db.sm_area_team_temp.special_territory_code == special_territory_code)).select(db.sm_area_team_temp.territory_id,db.sm_area_team_temp.territory_name,groupby=db.sm_area_team_temp.territory_id|db.sm_area_team_temp.territory_name)
                    for specialTerrRow in specialTerrRows:
                        territoryId=str(specialTerrRow.territory_id)
                        territoryName=str(specialTerrRow.territory_name)
                        
                        ffLevelRow2=db((db.sm_rep_area.cid==c_id)&(db.sm_rep_area.rep_id==mso_id)&(db.sm_rep_area.area_id==territoryId)).select(db.sm_rep_area.rep_id,limitby=(0,1))
                        if not ffLevelRow2:
                            db.sm_rep_area.insert(cid=c_id,rep_id=mso_id,rep_name=mso_name,area_id=territoryId,area_name=territoryName,rep_category=mso_category)
                            validDataFlag=True
                        else:
                            continue
                
                if validDataFlag==True:
                    db((db.sm_area_team_temp.territory_id == territory_id)&(db.sm_area_team_temp.mso_id == mso_id)&(db.sm_area_team_temp.mso_category == mso_category)).update(mso_flag=1,second_part_flag=1)
                    
        #-----------
        time.sleep(1)
        
        callBackup=backup_team_structure(first_date,schedule_date)
        
        #------------
        processRecords[0].update_record(status='1',notes='Completed',updated_by='SYSTEM')
        db.commit()
        
    return 'Done'


#def level_batch_upload_old():
#    task_id='rm_workingarea_manage'
#    access_permission=check_role(task_id)
#    if (access_permission==False):
#        session.flash='Access is Denied !'
#        redirect (URL('default','home'))
#        
#    response.title='Level Batch upload'
#    
#    c_id=session.cid
#    uploadDepth=request.vars.uploadDepth
#    
#    if (uploadDepth=='' or uploadDepth==None):
#        session.flash='Need Depth value'
#        redirect (URL(c='utility_mrep',f='utility'))
#    
#    btn_upload=request.vars.btn_upload    
#    count_inserted=0
#    count_error=0
#    error_str=''
#    total_row=0
#    if btn_upload=='Upload':        
#        excel_data=str(request.vars.excel_data)
#        inserted_count=0
#        error_count=0
#        error_list=[]
#        row_list=excel_data.split( '\n')
#        total_row=len(row_list)
#        
#        depot_list_exist=[]
#
#        ins_list=[]
#        ins_dict={}
#        
#        #--------------- depth check
#        firstDpth=False
#        lastDpth=False
#        middleDepth=False
#        if int(uploadDepth)==0:
#            firstDpth=True
#        else:
#            settDepth=0
#            settDpthRows=db((db.sm_settings.cid==c_id) & (db.sm_settings.s_key=='LEVEL_DEPTH')).select(db.sm_settings.s_value,limitby=(0,1))
#            if settDpthRows:
#                settDepth=int(settDpthRows[0].s_value)
#            
#            if int(uploadDepth)==settDepth:
#                lastDpth=True
#            else:
#                middleDepth==True
#        
#        
#        #---------- valid depot list                            
#        depotRows=db((db.sm_depot.cid==c_id)&(db.sm_depot.status=='ACTIVE')).select(db.sm_depot.depot_id,orderby=db.sm_depot.depot_id)
#        depot_list_exist=depotRows.as_list()
#        
#        #   --------------------     
#        for i in range(total_row):
#            if i>=100: 
#                break
#            else:
#                row_data=row_list[i]
#            coloum_list=row_data.split( '\t')            
#
#            if len(coloum_list)==4:
#                level_ID_excel=check_special_char_id(str(coloum_list[0]).strip().upper())
#                level_Name_excel=check_special_char(str(coloum_list[1]).strip())
#                plevel_ID_excel=check_special_char_id(str(coloum_list[2]).strip().upper())
#                depotID_excel=str(coloum_list[3]).strip().upper()
#                
#                depotIdvalue='-'
#                isLeaf='0'
#                
#                try:
#                    fieldValFlag=True
#                    valid_depot=False
#                    
#                    if firstDpth==True:
#                        if level_ID_excel=='' or level_Name_excel=='':
#                            fieldValFlag=False
#                        else:
#                            plevel_ID_excel='0'
#                            
#                    elif middleDepth==True:
#                        if level_ID_excel=='' or level_Name_excel=='' or plevel_ID_excel=='':
#                            fieldValFlag=False
#                    
#                    elif lastDpth==True:
#                        if level_ID_excel=='' or level_Name_excel=='' or plevel_ID_excel=='' or depotID_excel=='':
#                            fieldValFlag=False
#                        else:
#                            for i in range(len(depot_list_exist)):
#                                myRowData=depot_list_exist[i]                                
#                                depot_id=myRowData['depot_id']                        
#                                if (str(depot_id).strip()==str(depotID_excel).strip()):
#                                    valid_depot=True
#                                    depotIdvalue=depot_id
#                                    break
#                            isLeaf='1'
#                            
#                    
#                    #-----------------
#                    if fieldValFlag==True:
#                        if (lastDpth==True and valid_depot==False):
#                            error_data=row_data+'(Invalid Depot ID)\n'
#                            error_str=error_str+error_data
#                            count_error+=1
#                            continue
#                        else:                        
#                            #------------------------------- Depth 0
#                            if int(uploadDepth)==0:
#                                level_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==level_ID_excel)).select(db.sm_level.level_id,limitby=(0,1))
#                                if not level_rows:
#                                    db.sm_level.insert(cid=c_id,level_id=level_ID_excel,level_name=level_Name_excel,parent_level_id=plevel_ID_excel,is_leaf=isLeaf,depot_id=depotIdvalue,depth=uploadDepth,level0=level_ID_excel)         
#                                    count_inserted+=1
#                                    continue
#                                else:
#                                    error_data=row_data+'(Already Exist)\n'
#                                    error_str=error_str+error_data
#                                    count_error+=1
#                                    continue
#                            
#                            #------------------------------ Depth 1 
#                            elif int(uploadDepth)==1:                                
#                                level_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==level_ID_excel)).select(db.sm_level.level_id,limitby=(0,1))
#                                if not level_rows:
#                                    parent_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==plevel_ID_excel)).select(db.sm_level.level0,limitby=(0,1))
#                                    if parent_rows:
#                                        level0=parent_rows[0].level0
#                                        
#                                        db.sm_level.insert(cid=c_id,level_id=level_ID_excel,level_name=level_Name_excel,parent_level_id=plevel_ID_excel,is_leaf=isLeaf,depot_id=depotIdvalue,depth=uploadDepth,level0=level0,level1=level_ID_excel)         
#                                        count_inserted+=1
#                                        continue
#                                        
#                                    else:
#                                        error_data=row_data+'(Invalid Patent ID)\n'
#                                        error_str=error_str+error_data
#                                        count_error+=1
#                                        continue
#                                else:
#                                    error_data=row_data+'(Already Exist)\n'
#                                    error_str=error_str+error_data
#                                    count_error+=1
#                                    continue
#                            
#                            #------------------------------ Depth 2 
#                            elif int(uploadDepth)==2:                                
#                                level_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==level_ID_excel)).select(db.sm_level.level_id,limitby=(0,1))
#                                if not level_rows:
#                                    parent_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==plevel_ID_excel)).select(db.sm_level.level0,db.sm_level.level1,limitby=(0,1))
#                                    if parent_rows:
#                                        level0=parent_rows[0].level0
#                                        level1=parent_rows[0].level1
#                                        
#                                        db.sm_level.insert(cid=c_id,level_id=level_ID_excel,level_name=level_Name_excel,parent_level_id=plevel_ID_excel,is_leaf=isLeaf,depot_id=depotIdvalue,depth=uploadDepth,level0=level0,level1=level1,level2=level_ID_excel)         
#                                        count_inserted+=1
#                                        continue
#                                        
#                                    else:
#                                        error_data=row_data+'(Invalid Patent ID)\n'
#                                        error_str=error_str+error_data
#                                        count_error+=1
#                                        continue
#                                else:
#                                    error_data=row_data+'(Already Exist)\n'
#                                    error_str=error_str+error_data
#                                    count_error+=1
#                                    continue
#                            
#                            #------------------------------ Depth 3 
#                            elif int(uploadDepth)==3:                                
#                                level_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==level_ID_excel)).select(db.sm_level.level_id,limitby=(0,1))
#                                if not level_rows:
#                                    parent_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==plevel_ID_excel)).select(db.sm_level.level0,db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
#                                    if parent_rows:
#                                        level0=parent_rows[0].level0
#                                        level1=parent_rows[0].level1
#                                        level2=parent_rows[0].level2
#                                        
#                                        db.sm_level.insert(cid=c_id,level_id=level_ID_excel,level_name=level_Name_excel,parent_level_id=plevel_ID_excel,is_leaf=isLeaf,depot_id=depotIdvalue,depth=uploadDepth,level0=level0,level1=level1,level2=level2,level3=level_ID_excel)         
#                                        count_inserted+=1
#                                        continue
#                                        
#                                    else:
#                                        error_data=row_data+'(Invalid Patent ID)\n'
#                                        error_str=error_str+error_data
#                                        count_error+=1
#                                        continue
#                                else:
#                                    error_data=row_data+'(Already Exist)\n'
#                                    error_str=error_str+error_data
#                                    count_error+=1
#                                    continue
#                            
#                            #------------------------------ Depth 4 
#                            elif int(uploadDepth)==4:                                
#                                level_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==level_ID_excel)).select(db.sm_level.level_id,limitby=(0,1))
#                                if not level_rows:
#                                    parent_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==plevel_ID_excel)).select(db.sm_level.level0,db.sm_level.level1,db.sm_level.level2,db.sm_level.level3,limitby=(0,1))
#                                    if parent_rows:
#                                        level0=parent_rows[0].level0
#                                        level1=parent_rows[0].level1
#                                        level2=parent_rows[0].level2
#                                        level3=parent_rows[0].level3
#                                        
#                                        db.sm_level.insert(cid=c_id,level_id=level_ID_excel,level_name=level_Name_excel,parent_level_id=plevel_ID_excel,is_leaf=isLeaf,depot_id=depotIdvalue,depth=uploadDepth,level0=level0,level1=level1,level2=level2,level3=level3,level4=level_ID_excel)         
#                                        count_inserted+=1
#                                        continue
#                                        
#                                    else:
#                                        error_data=row_data+'(Invalid Patent ID)\n'
#                                        error_str=error_str+error_data
#                                        count_error+=1
#                                        continue
#                                else:
#                                    error_data=row_data+'(Already Exist)\n'
#                                    error_str=error_str+error_data
#                                    count_error+=1
#                                    continue
#                            
#                            #------------------------------ Depth 5 
#                            elif int(uploadDepth)==5:                                
#                                level_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==level_ID_excel)).select(db.sm_level.level_id,limitby=(0,1))
#                                if not level_rows:
#                                    parent_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==plevel_ID_excel)).select(db.sm_level.level0,db.sm_level.level1,db.sm_level.level2,db.sm_level.level3,db.sm_level.level4,limitby=(0,1))
#                                    if parent_rows:
#                                        level0=parent_rows[0].level0
#                                        level1=parent_rows[0].level1
#                                        level2=parent_rows[0].level2
#                                        level3=parent_rows[0].level3
#                                        level4=parent_rows[0].level4
#                                        
#                                        db.sm_level.insert(cid=c_id,level_id=level_ID_excel,level_name=level_Name_excel,parent_level_id=plevel_ID_excel,is_leaf=isLeaf,depot_id=depotIdvalue,depth=uploadDepth,level0=level0,level1=level1,level2=level2,level3=level3,level4=level4,level5=level_ID_excel)         
#                                        count_inserted+=1
#                                        continue
#                                        
#                                    else:
#                                        error_data=row_data+'(Invalid Patent ID)\n'
#                                        error_str=error_str+error_data
#                                        count_error+=1
#                                        continue
#                                else:
#                                    error_data=row_data+'(Already Exist)\n'
#                                    error_str=error_str+error_data
#                                    count_error+=1
#                                    continue
#                            
#                            #------------------------------ Depth 6 
#                            elif int(uploadDepth)==6:                                
#                                level_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==level_ID_excel)).select(db.sm_level.level_id,limitby=(0,1))
#                                if not level_rows:
#                                    parent_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==plevel_ID_excel)).select(db.sm_level.level0,db.sm_level.level1,db.sm_level.level2,db.sm_level.level3,db.sm_level.level4,db.sm_level.level5,limitby=(0,1))
#                                    if parent_rows:
#                                        level0=parent_rows[0].level0
#                                        level1=parent_rows[0].level1
#                                        level2=parent_rows[0].level2
#                                        level3=parent_rows[0].level3
#                                        level4=parent_rows[0].level4
#                                        level5=parent_rows[0].level5
#                                        
#                                        db.sm_level.insert(cid=c_id,level_id=level_ID_excel,level_name=level_Name_excel,parent_level_id=plevel_ID_excel,is_leaf=isLeaf,depot_id=depotIdvalue,depth=uploadDepth,level0=level0,level1=level1,level2=level2,level3=level3,level4=level4,level5=level5,level6=level_ID_excel)         
#                                        count_inserted+=1
#                                        continue
#                                        
#                                    else:
#                                        error_data=row_data+'(Invalid Patent ID)\n'
#                                        error_str=error_str+error_data
#                                        count_error+=1
#                                        continue
#                                else:
#                                    error_data=row_data+'(Already Exist)\n'
#                                    error_str=error_str+error_data
#                                    count_error+=1
#                                    continue
#                            
#                            #------------------------------ Depth 7 
#                            elif int(uploadDepth)==7:                                
#                                level_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==level_ID_excel)).select(db.sm_level.level_id,limitby=(0,1))
#                                if not level_rows:
#                                    parent_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==plevel_ID_excel)).select(db.sm_level.level0,db.sm_level.level1,db.sm_level.level2,db.sm_level.level3,db.sm_level.level4,db.sm_level.level5,db.sm_level.level6,limitby=(0,1))
#                                    if parent_rows:
#                                        level0=parent_rows[0].level0
#                                        level1=parent_rows[0].level1
#                                        level2=parent_rows[0].level2
#                                        level3=parent_rows[0].level3
#                                        level4=parent_rows[0].level4
#                                        level5=parent_rows[0].level5
#                                        level6=parent_rows[0].level6
#                                        
#                                        db.sm_level.insert(cid=c_id,level_id=level_ID_excel,level_name=level_Name_excel,parent_level_id=plevel_ID_excel,is_leaf=isLeaf,depot_id=depotIdvalue,depth=uploadDepth,level0=level0,level1=level1,level2=level2,level3=level3,level4=level4,level5=level5,level6=level6,level7=level_ID_excel)         
#                                        count_inserted+=1
#                                        continue
#                                        
#                                    else:
#                                        error_data=row_data+'(Invalid Patent ID)\n'
#                                        error_str=error_str+error_data
#                                        count_error+=1
#                                        continue
#                                else:
#                                    error_data=row_data+'(Already Exist)\n'
#                                    error_str=error_str+error_data
#                                    count_error+=1
#                                    continue
#                            
#                            #------------------------------ Depth 8 
#                            elif int(uploadDepth)==8:                                
#                                level_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==level_ID_excel)).select(db.sm_level.level_id,limitby=(0,1))
#                                if not level_rows:
#                                    parent_rows=db((db.sm_level.cid==c_id)&(db.sm_level.level_id==plevel_ID_excel)).select(db.sm_level.level0,db.sm_level.level1,db.sm_level.level2,db.sm_level.level3,db.sm_level.level4,db.sm_level.level5,db.sm_level.level6,db.sm_level.level7,limitby=(0,1))
#                                    if parent_rows:
#                                        level0=parent_rows[0].level0
#                                        level1=parent_rows[0].level1
#                                        level2=parent_rows[0].level2
#                                        level3=parent_rows[0].level3
#                                        level4=parent_rows[0].level4
#                                        level5=parent_rows[0].level5
#                                        level6=parent_rows[0].level6
#                                        level7=parent_rows[0].level7
#                                        
#                                        db.sm_level.insert(cid=c_id,level_id=level_ID_excel,level_name=level_Name_excel,parent_level_id=plevel_ID_excel,is_leaf=isLeaf,depot_id=depotIdvalue,depth=uploadDepth,level0=level0,level1=level1,level2=level2,level3=level3,level4=level4,level5=level5,level6=level6,level7=level7,level8=level_ID_excel)         
#                                        count_inserted+=1
#                                        continue
#                                        
#                                    else:
#                                        error_data=row_data+'(Invalid Patent ID)\n'
#                                        error_str=error_str+error_data
#                                        count_error+=1
#                                        continue
#                                else:
#                                    error_data=row_data+'(Already Exist)\n'
#                                    error_str=error_str+error_data
#                                    count_error+=1
#                                    continue
#                                
#                            
#                    else:
#                        error_data=row_data+'(Required value)\n'
#                        error_str=error_str+error_data
#                        count_error+=1
#                        continue
#
#                except:
#                    error_data=row_data+'(error in process!)\n'
#                    error_str=error_str+error_data
#                    count_error+=1
#                    continue
#                
#            else:
#                error_data=row_data+'(4 columns need in a row)\n'
#                error_str=error_str+error_data
#                count_error+=1
#                continue
#
##        return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)        
#    
#    return dict(count_inserted=count_inserted,uploadDepth=uploadDepth,count_error=count_error,error_str=error_str,total_row=total_row)
