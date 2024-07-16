def transfer_area():
    cid=session.cid
    response.title='Transfer Area'

    btn_transfer_area=request.vars.btn_transfer_area
    checkbox=request.vars.checkbox
    confirm_r=request.vars.confirm_r
    depotname=''
    store_name=''
    errorFlag=0
   
    if errorFlag==0 and btn_transfer_area=='Submit':
        if confirm_r!='CONFIRM':
            errorFlag=1
            session.flash='Please enter confirm passowerd' 
            redirect (URL('client_transfer','transfer_area'))
        if checkbox==None:
            errorFlag=1
            session.flash='Please Confirm First' 
            redirect (URL('client_transfer','transfer_area'))
            
            
            
        old_area_id=str(request.vars.old_area_id).strip().upper()
        area_id=str(request.vars.new_area_id).strip().upper()
        depot_id=str(request.vars.new_depot_id).strip().upper()
        store_id=str(request.vars.new_store_id).strip().upper()
        
        # store_id=depot_id+'1'
        
        
        
         
        if ((old_area_id == '') or (area_id == '')):
            session.flash='Please enter old and new area' 
            redirect (URL('client_transfer','transfer_area'))
        else:
            if (depot_id != '') :
                
#                 select depot name from sm_depot based on depot ID
                depotname=''
                depotRow=db((db.sm_depot.cid == cid)  and (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.name, limitby=(0,1))
                if depotRow:
                    depotname=depotRow[0].name
                    
                store_name=''
                storeRow=db((db.sm_depot_store.cid == cid)  and (db.sm_depot_store.store_id == store_id)).select(db.sm_depot_store.store_name, limitby=(0,1))
                if storeRow:
                    store_name=storeRow[0].store_name    
#                 return   depotname  
                if depotname=='':
                    session.flash='Please enter valid Depot and Store' 
                    errorFlag=1
                
            if errorFlag==0:
                
                if (depot_id != '' ) :
#                     return depotname
                    updateBothStr="""update sm_client set area_id='"""+area_id+"""',depot_id='"""+depot_id+"""',depot_name='"""+depotname+"""',store_id='"""+store_id+"""',store_name='"""+store_name+"""',updated_on='"""+str(datetime_fixed)+"""',updated_by='"""+str(session.user_id)+"""' where area_id='"""+old_area_id+"""' """
#                     return updateBothStr
                    updateBoth=db.executesql(updateBothStr)
#                     return depot_id
                   
                else:
                    updateBothStr="""update sm_client set area_id='"""+area_id+"""',updated_on='"""+str(datetime_fixed)+"""',updated_by='"""+str(session.user_id)+"""' where area_id='"""+old_area_id  +"""' """
                    
#                     return updateBothStr
                    updateBoth=db.executesql(updateBothStr)
                    
                session.flash='Transfered Successfully'

                redirect (URL('client_transfer','transfer_area'))

    return dict()