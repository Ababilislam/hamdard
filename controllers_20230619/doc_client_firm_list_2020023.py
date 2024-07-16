import urllib2


# http://127.0.0.1:8000/novivo/doc_client_farm_list/doc_client_farm?cid=novivo&rep=it03&password=1234&sync=260&date=2019-12-05&time=morning&area_id=DEMO
def doc_client_farm():
	setDate=str(request.vars.setDate).strip()#.upper()
	setTime=str(request.vars.setTime).strip()#.upper()
	area=str(request.vars.area).strip()#.upper()
	this_val=str(request.vars.this_val).strip()#.upper()
	return dict(setDate=setDate,setTime=setTime,area=area,this_val=this_val)


def docsearch():
	
	cid=str(request.vars.cid).strip().upper()
	rep_id=str(request.vars.rep_id).strip().upper()
	rep_pass=str(request.vars.rep_pass).strip()
	area_name=request.vars.area_id
	setDate=request.vars.setDate
	setTime=request.vars.setTime
	month_pass=request.vars.month_pass

	area_id=''
	repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == rep_pass) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.user_type,db.sm_rep.note, limitby=(0, 1))
	if not repRow:
	   retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
	   return retStatus
	else:
		mc_Rows=db((db.sm_microunion.cid==cid)&(db.sm_microunion.microunion_name==area_name)).select(db.sm_microunion.area_id,limitby=(0,1))
# 		return mc_Rows
		    
		docStr = ''
		if mc_Rows:
		    area_id=mc_Rows[0].area_id
		
		
		docRows=db((db.sm_doctor_area.cid==cid)&(db.sm_doctor_area.area_id==area_id)).select(db.sm_doctor_area.doc_id, db.sm_doctor_area.doc_name,  groupby = db.sm_doctor_area.doc_id, orderby=db.sm_doctor_area.doc_name)
		    
		docStr = ''
		for docRows in docRows:
		    doc_id= str(docRows.doc_id).strip()
		    # return doc_id

		    doc_name=str(docRows.doc_name).strip()

		    if docStr=='':
		        docStr = str(doc_name) +'|'+ str(doc_id)

		    else:
		        docStr +='rdrd'+ str(doc_name)+'|'+ str(doc_id)
		        
		doc_check_Rows=db((db.sm_doctor_day_plan.cid==cid) &(db.sm_doctor_day_plan.rep_id==rep_id) & (db.sm_doctor_day_plan.plan_date==setDate) ).select(db.sm_doctor_day_plan.doc_id, db.sm_doctor_day_plan.doc_name)
		    
		doc_checkStr = ''
		for doc_check_Rows in doc_check_Rows:
		    doc_c_id= str(doc_check_Rows.doc_id).strip()
		    # return doc_id

		    doc_c_name=str(doc_check_Rows.doc_name).strip()

		    if doc_checkStr=='':
		        doc_checkStr = str(doc_c_name) +'|'+ str(doc_c_id)

		    else:
		        doc_checkStr +='rdrd'+ str(doc_c_name)+'|'+ str(doc_c_id)
		
		
		return docStr+'<syncdata>'+doc_checkStr



def insertDoc():
	
	
	docListNew=str(request.vars.docListNew).strip()#.upper()
	
	cid=str(request.vars.cid).strip().upper()
	rep_id=str(request.vars.rep_id).strip().upper()
	rep_pass=str(request.vars.rep_pass).strip()
	area_name=request.vars.area_id
	setDate=request.vars.setDate
	setTime=request.vars.setTime
	month_pass=request.vars.month_pass
	this_val=str(request.vars.this_val).strip()
	area_id=''
	repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == rep_pass) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.user_type,db.sm_rep.note, limitby=(0, 1))
	if not repRow:
	   retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
	   return retStatus
	else:
		mc_Rows=db((db.sm_microunion.cid==cid)&(db.sm_microunion.microunion_name==area_name)).select(db.sm_microunion.area_id,limitby=(0,1))
# 		return mc_Rows
		    
		docStr = ''
		if mc_Rows:
		    area_id=mc_Rows[0].area_id
	
	
 	resultSuccess=''
 	resultFailed=''
 	repAreaCheckRow=''
	repName=''
	get_month=''
	
	repAreaCheckRow = db((db.sm_doctor_visit_plan.cid == cid)  & (db.sm_doctor_visit_plan.rep_id == rep_id) & (db. sm_doctor_visit_plan.route_id == area_id)).select(db.sm_doctor_visit_plan.rep_name,db. sm_doctor_visit_plan.route_name, limitby=(0, 1))			
	if repAreaCheckRow:
		repName=repAreaCheckRow[0].rep_name
	
  	

	if (this_val=='This'):
	    first_date=str(first_currentDate).split(' ')[0]

	else:
	    todayDate = datetime.date.today()
	    first_date1 = str(todayDate + datetime.timedelta(days=30))
	    first_date=first_date1.split('-')[0]+'-'  +first_date1.split('-')[1]  +'-01'

	if (docListNew=='') :
		return 'Failed<rdrd>Please Select Doctor'
	else:
		db((db.sm_doctor_day_plan.cid==cid) &(db.sm_doctor_day_plan.rep_id==rep_id) & (db.sm_doctor_day_plan.plan_date==setDate)).delete()
		docListNewG=docListNew.split(',')
	   
	for i in range(len(docListNewG)):
		docListNewGet = docListNewG[i]
		docID = docListNewGet.split('|')[0]
		docName = docListNewGet.split('|')[1]
		insRows=db.sm_doctor_day_plan.insert(cid=cid,rep_id=rep_id,rep_name=repName,area_id=area_id,area_name=area_name,doc_id=docID,doc_name=docName,plan_date=setDate,visit_time=setTime,field1=area_id,first_date=first_date)
		    
		if insRows:
		    if resultSuccess=='':
		        resultSuccess =str(docListNewGet)
		    else:
		        resultSuccess =resultSuccess+','+str(docListNewGet)
		else:
		    pass

	if resultFailed!='' and resultSuccess!='':
	    return 'Success<rdrd>Success: '+str(resultSuccess)+' Already exist:'+str(resultFailed)
	elif resultFailed!='' and resultSuccess=='':
	    return 'Success<rdrd> Already exist:'+str(resultFailed)
	elif resultFailed=='' and resultSuccess!='':
	    return 'Success<rdrd> Success: '+str(resultSuccess)
	else:
	    return 'Success<rdrd> '


	    
        

# =============================== END DOCTOR =========================



def clientsearch():
	cid=str(request.vars.cid).strip().upper()
	rep_id=str(request.vars.rep_id).strip().upper()
	rep_pass=str(request.vars.rep_pass).strip()
	area_name=request.vars.area_id
	setDate=request.vars.setDate
	setTime=request.vars.setTime
	month_pass=request.vars.month_pass
	area_id=''
	repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == rep_pass) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.user_type,db.sm_rep.note, limitby=(0, 1))
# 	return repRow
	if not repRow:
	   retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
	   return retStatus
	else:
		mc_Rows=db((db.sm_microunion.cid==cid)&(db.sm_microunion.microunion_name==area_name)).select(db.sm_microunion.area_id,limitby=(0,1))
# 		return mc_Rows
		    
		docStr = ''
		if mc_Rows:
		    area_id=mc_Rows[0].area_id
		

	
		clientRows=db((db.sm_client.cid==cid)&(db.sm_client.area_id==area_id)).select(db.sm_client.client_id, db.sm_client.name,  groupby = db.sm_client.client_id, orderby=db.sm_client.client_id)
		# return clientRows
		clientStr = ''
		for clientRows in clientRows:
			client_id= str(clientRows.client_id).strip()
			# return client_id

			name=str(clientRows.name).strip()

			if clientStr=='':
				clientStr = str(name) +'|'+ str(client_id)

			else:
				clientStr +='rdrd'+ str(name)+'|'+ str(client_id)
		
		
		client_check_Rows=db((db.sm_client_day_plan.cid==cid) &(db.sm_client_day_plan.rep_id==rep_id) & (db.sm_client_day_plan.plan_date==setDate)).select(db.sm_client_day_plan.client_id, db.sm_client_day_plan.client_name)
		    
		client_checkStr = ''
		for client_check_Rows in client_check_Rows:
		    client_c_id= str(client_check_Rows.client_id).strip()
		    # return doc_id

		    client_c_name=str(client_check_Rows.client_name).strip()

		    if client_checkStr=='':
		        client_checkStr = str(client_c_name) +'|'+ str(client_c_id)

		    else:
		        client_checkStr +='rdrd'+ str(client_c_name)+'|'+ str(client_c_id)
		
		
		return clientStr+'<syncdata>'+client_checkStr
		
# 		return clientStr





def insertclient():

	cid=str(request.vars.cid).strip().upper()
	rep_id=str(request.vars.rep_id).strip().upper()
	rep_pass=str(request.vars.rep_pass).strip()
	area_name=request.vars.area_id
	setDate=request.vars.setDate
	setTime=request.vars.setTime
	month_pass=request.vars.month_pass
	this_val=str(request.vars.this_val).strip()


	clientListNew=str(request.vars.clientListNew).strip()



	resultSuccess=''
	resultFailed=''
	repCheckRow=''
	areaCheckRow=''

	area_id=''
	repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == rep_pass) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.user_type,db.sm_rep.note, limitby=(0, 1))
# 	return repRow
	if not repRow:
	   retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
	   return retStatus
	else:
		mc_Rows=db((db.sm_microunion.cid==cid)&(db.sm_microunion.microunion_name==area_name)).select(db.sm_microunion.area_id,limitby=(0,1))
# 		return mc_Rows
		    
		docStr = ''
		if mc_Rows:
		    area_id=mc_Rows[0].area_id


	repCheckRow = db((db.sm_rep.cid == cid) & (db. sm_rep.rep_id == rep_id) & (db. sm_rep.password == rep_pass)).select(db.sm_rep.name, limitby=(0, 1))			
	if repCheckRow:
		repName=repCheckRow[0].name

	if (this_val=='This'):
	    first_date=str(first_currentDate).split(' ')[0]

	else:
	    todayDate = datetime.date.today()
	    first_date1 = str(todayDate + datetime.timedelta(days=30))
	    first_date=first_date1.split('-')[0]+'-'  +first_date1.split('-')[1]  +'-01'


	if (clientListNew=='') :
	    return 'Failed<rdrd>Please Select Client'
	else:
		db((db.sm_client_day_plan.cid==cid) &(db.sm_client_day_plan.rep_id==rep_id) & (db.sm_client_day_plan.plan_date==setDate)).delete()
		clientListNewG=clientListNew.split(',')
		   
		for i in range(len(clientListNewG)):
			clientListNewGet = clientListNewG[i]
			
			clientID = clientListNewGet.split('|')[0]
			clientName = clientListNewGet.split('|')[1]
			insRows=db.sm_client_day_plan.insert(cid=cid,rep_id=rep_id,rep_name=repName,area_id=area_id,area_name=area_name,client_id=clientID,client_name=clientName,plan_date=setDate,visit_time=setTime,first_date=first_date)
			    
			if insRows:
			    if resultSuccess=='':
			        resultSuccess =str(clientListNewGet)
			    else:
			        resultSuccess =resultSuccess+','+str(clientListNewGet)
			else:
			    pass
		
		if resultFailed!='' and resultSuccess!='':
		    return 'Success<rdrd>Success: '+str(resultSuccess)+' Already exist:'+str(resultFailed)
		elif resultFailed!='' and resultSuccess=='':
		    return 'Success<rdrd> Already exist:'+str(resultFailed)
		elif resultFailed=='' and resultSuccess!='':
		    return 'Success<rdrd> Success: '+str(resultSuccess)
		else:
		    return 'Success<rdrd> '
        


# ===================== END CLIEMT ========================




		
def farmsearch():
	
	cid=str(request.vars.cid).strip().upper()
	rep_id=str(request.vars.rep_id).strip().upper()
	rep_pass=str(request.vars.rep_pass).strip()
	area_name=request.vars.area_id
	setDate=request.vars.setDate
	setTime=request.vars.setTime
	month_pass=request.vars.month_pass
	
	area_id=''
	repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == rep_pass) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.user_type,db.sm_rep.note, limitby=(0, 1))
	if not repRow:
	   retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
	   return retStatus
	else:
		mc_Rows=db((db.sm_microunion.cid==cid)&(db.sm_microunion.microunion_name==area_name)).select(db.sm_microunion.area_id,limitby=(0,1))
# 		return mc_Rows
		    
		docStr = ''
		if mc_Rows:
		    area_id=mc_Rows[0].area_id
		    
		farmRows=db((db.sm_farm.cid==cid) & (db.sm_farm.route==area_id)).select(db.sm_farm.farm_id, db.sm_farm.farm_name,  groupby = db.sm_farm.farm_id, orderby=db.sm_farm.farm_id)
		    
		farmStr = ''
		for farmRows in farmRows:
		    farm_id= str(farmRows.farm_id).strip()
		    # return client_id

		    farm_name=str(farmRows.farm_name).strip()

		    if farmStr=='':
		        farmStr = str(farm_name) +'|'+ str(farm_id)

		    else:
		        farmStr +='rdrd'+ str(farm_name)+'|'+ str(farm_id)
# 		return farmStr

		farm_check_Rows=db((db.sm_farm_day_plan.cid==cid)  &(db.sm_farm_day_plan.rep_id==rep_id) & (db.sm_farm_day_plan.plan_date==setDate)).select(db.sm_farm_day_plan.farm_id, db.sm_farm_day_plan.farm_name)
		    
		farm_checkStr = ''
		for farm_check_Rows in farm_check_Rows:
		    farm_c_id= str(farm_check_Rows.farm_id).strip()
		    # return doc_id

		    farm_c_name=str(farm_check_Rows.farm_name).strip()

		    if farm_checkStr=='':
		        farm_checkStr = str(farm_c_name) +'|'+ str(farm_c_id)

		    else:
		        farm_checkStr +='rdrd'+ str(farm_c_name)+'|'+ str(farm_c_id)
		
		
		return farmStr+'<syncdata>'+farm_checkStr






def farmclient():

	cid=str(request.vars.cid).strip().upper()
	rep_id=str(request.vars.rep_id).strip().upper()
	rep_pass=str(request.vars.rep_pass).strip()
	area_name=request.vars.area_id
	setDate=request.vars.setDate
	setTime=request.vars.setTime
	month_pass=request.vars.month_pass
	this_val=str(request.vars.this_val).strip()

	
	farmListNew=str(request.vars.farmListNew).strip()
	
	resultSuccess=''
	resultFailed=''
	repCheckRow=''
	areaCheckRow=''
	repName=''
	
	area_id=''
	repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == rep_pass) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.user_type,db.sm_rep.note, limitby=(0, 1))
# 	return repRow
	if not repRow:
	   retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
	   return retStatus
	else:
		mc_Rows=db((db.sm_microunion.cid==cid)&(db.sm_microunion.microunion_name==area_name)).select(db.sm_microunion.area_id,limitby=(0,1))
# 		return mc_Rows
		    
		docStr = ''
		if mc_Rows:
		    area_id=mc_Rows[0].area_id


	repCheckRow = db((db.sm_rep.cid == cid) & (db. sm_rep.rep_id == rep_id) & (db. sm_rep.password == rep_pass)).select(db.sm_rep.name, limitby=(0, 1))			
	if repCheckRow:
		repName=repCheckRow[0].name

	if (this_val=='This'):
	    first_date=str(first_currentDate).split(' ')[0]

	else:
	    todayDate = datetime.date.today()
	    first_date1 = str(todayDate + datetime.timedelta(days=30))
	    first_date=first_date1.split('-')[0]+'-'  +first_date1.split('-')[1]  +'-01'


	if (farmListNew=='') :
	    return 'Failed<rdrd>Please Select Farm'
	else:
		db((db.sm_farm_day_plan.cid==cid) &(db.sm_farm_day_plan.rep_id==rep_id) & (db.sm_farm_day_plan.plan_date==setDate)).delete()
		farmListNewG=farmListNew.split(',')
		   
		for i in range(len(farmListNewG)):
			farmListNewGet = farmListNewG[i]
			
			farmID = farmListNewGet.split('|')[0]
			farmName = farmListNewGet.split('|')[1]
			insRows=db.sm_farm_day_plan.insert(cid=cid,rep_id=rep_id,rep_name=repName,area_id=area_id,area_name=area_name,farm_id=farmID,farm_name=farmName,plan_date=setDate,visit_time=setTime,first_date=first_date)
			    
			if insRows:
			    if resultSuccess=='':
			        resultSuccess =str(farmListNewGet)
			    else:
			        resultSuccess =resultSuccess+','+str(farmListNewGet)
			else:
			    pass
		
		if resultFailed!='' and resultSuccess!='':
		    return 'Success<rdrd>Success: '+str(resultSuccess)+' Already exist:'+str(resultFailed)
		elif resultFailed!='' and resultSuccess=='':
		    return 'Success<rdrd> Already exist:'+str(resultFailed)
		elif resultFailed=='' and resultSuccess!='':
		    return 'Success<rdrd> Success: '+str(resultSuccess)
		else:
		    return 'Success<rdrd> '
        

