
def transfer_doc_area():
    cid=session.cid
    response.title='Transfer Doc Area'
#     return 'dfgf'
    btn_transfer_doc=request.vars.btn_transfer_doc
    checkbox=request.vars.checkbox
    confirm_d=request.vars.confirm_d
    areaname=''
    errorFlag=0
   
    if errorFlag==0 and btn_transfer_doc=='Submit':
        if confirm_d!='CONFIRM':
            errorFlag=1
            session.flash='Please enter confirm passowerd' 
            redirect (URL('transfer_doc_area','transfer_doc_area'))
        if checkbox==None:
            errorFlag=1
            session.flash='Please Confirm First' 
            redirect (URL('transfer_doc_area','transfer_doc_area'))
            
            
            
        old_area_id=str(request.vars.old_area_id).strip().upper()
        area_id=str(request.vars.new_area_id).strip().upper()
        depot_id=str(request.vars.new_depot_id).strip().upper()

        
         
        if ((old_area_id == '') or (area_id == '')):
            session.flash='Please enter old and new area' 
            redirect (URL('transfer_doc_area','transfer_doc_area'))
        else:
            if (depot_id != '') :
                areaname=''
                areaRow=db((db.sm_level.cid == cid)  and (db.sm_level.level_id == area_id)).select(db.sm_level.level_name, limitby=(0,1))
#                 return areaRow
                if areaRow:
                    areaname=areaRow[0].level_name
                     
                if areaname=='':
                    session.flash='Please enter valid Area' 
                    errorFlag=1
                
            if errorFlag==0:
                
                if (depot_id != '' ) :
                    updateStr="""update sm_doctor set pharma_route='"""+area_id+"""' where pharma_route='"""+old_area_id+"""' """
                    updateBoth=db.executesql(updateStr)
                    
                    updateAreaStr="""update sm_doctor_area set area_id='"""+area_id+"""',area_name='"""+areaname+"""',depot_id='"""+depot_id+"""' where area_id='"""+old_area_id+"""' """
                    updateAreaBoth=db.executesql(updateAreaStr)
  
                else:
                    updateStr="""update sm_doctor set pharma_route='"""+area_id+"""' where pharma_route='"""+old_area_id+"""' """
                    updateBoth=db.executesql(updateStr)
                    
                    updateAreaStr="""update sm_doctor_area set area_id='"""+area_id+"""' where area_id='"""+old_area_id+"""' """                    
                    updateAreaBoth=db.executesql(updateAreaStr)
                    
                session.flash='Transfered Successfully'

                redirect (URL('transfer_doc_area','transfer_doc_area'))

    return dict()