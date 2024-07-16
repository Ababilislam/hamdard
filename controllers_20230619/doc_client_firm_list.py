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
# 	return area_name
	setDate=request.vars.setDate
	setTime=request.vars.setTime
	month_pass=request.vars.month_pass
	area_id=''
	user_type=''
	repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == rep_pass) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.user_type,db.sm_rep.note, limitby=(0, 1))
	if not repRow:
	   retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
	   return retStatus
	else:					     
		user_type = repRow[0].user_type		
		if user_type=='rep':			
			mc_Rows=db((db.sm_microunion.cid==cid)&(db.sm_microunion.microunion_name==area_name)).select(db.sm_microunion.area_id,limitby=(0,1))   					
# 			return mc_Rows
			docStr = ''
			if mc_Rows:
			    area_id=mc_Rows[0].area_id
			    							
			docRows=db((db.sm_doctor_area.cid==cid)&(db.sm_doctor_area.area_id==area_id)).select(db.sm_doctor_area.doc_id, db.sm_doctor_area.doc_name,  groupby = db.sm_doctor_area.doc_id, orderby=db.sm_doctor_area.doc_name)		    
# 			return docRows
			docStr = ''
			for docRows in docRows:
			    doc_id= str(docRows.doc_id).strip()
			    doc_name=str(docRows.doc_name).strip()	
			    if docStr=='':
			        docStr = str(doc_name) +'|'+ str(doc_id)	
			    else:
			        docStr +='rdrd'+ str(doc_name)+'|'+ str(doc_id)

			doc_check_Rows=db((db.sm_doctor_day_plan.cid==cid) & (db.sm_doctor_day_plan.rep_id==rep_id)  & (db.sm_doctor_day_plan.area_name==area_name) & (db.sm_doctor_day_plan.plan_date==setDate) & (db.sm_doctor_day_plan.visit_time==setTime)).select(db.sm_doctor_day_plan.doc_id, db.sm_doctor_day_plan.doc_name)		    
#   			return doc_check_Rows
			doc_checkStr = ''
			for doc_check_Rows in doc_check_Rows:
			    doc_c_id= str(doc_check_Rows.doc_id).strip()	
			    doc_c_name=str(doc_check_Rows.doc_name).strip()			
			    if doc_checkStr=='':
			        doc_checkStr = str(doc_c_name) +'|'+ str(doc_c_id)			
			    else:
			        doc_checkStr +='rdrd'+ str(doc_c_name)+'|'+ str(doc_c_id)
						
			return docStr+'<syncdata>'+doc_checkStr
		
		
		else: 
			session.userType='sup'					
			sup_Rows=db((db.sm_level.cid==cid)&(db.sm_level.level_name==area_name)).select(db.sm_level.level_id,limitby=(0,1))   					
			docStr = ''
			if sup_Rows:
			    area_id=sup_Rows[0].level_id
							
			docRows=db((db.sm_doctor_area.cid==cid)&(db.sm_doctor_area.area_id==area_id)).select(db.sm_doctor_area.doc_id, db.sm_doctor_area.doc_name,  groupby = db.sm_doctor_area.doc_id, orderby=db.sm_doctor_area.doc_name)		    			
			docStr = ''
			for docRows in docRows:
			    doc_id= str(docRows.doc_id).strip()
			    doc_name=str(docRows.doc_name).strip()
			
			    if docStr=='':
			        docStr = str(doc_name) +'|'+ str(doc_id)
			
			    else:
			        docStr +='rdrd'+ str(doc_name)+'|'+ str(doc_id)
		
			doc_check_Rows=db((db.sm_doctor_day_plan.cid==cid) &(db.sm_doctor_day_plan.rep_id==rep_id)  & (db.sm_doctor_day_plan.area_name==area_name) & (db.sm_doctor_day_plan.plan_date==setDate) & (db.sm_doctor_day_plan.visit_time==setTime) ).select(db.sm_doctor_day_plan.doc_id, db.sm_doctor_day_plan.doc_name)		    
			
			doc_checkStr = ''
			for doc_check_Rows in doc_check_Rows:
			    doc_c_id= str(doc_check_Rows.doc_id).strip()	
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
#  	return area_name
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
		user_type = repRow[0].user_type		        		
		if user_type=='rep':			            			
			mc_Rows=db((db.sm_microunion.cid==cid)&(db.sm_microunion.microunion_name==area_name)).select(db.sm_microunion.microunion_id,limitby=(0,1))		    
			docStr = ''
			if mc_Rows:
			    area_id=mc_Rows[0].microunion_id
			    
		 	resultSuccess=''
		 	resultFailed=''
		 	repAreaCheckRow=''
			repName=''
			get_month=''
			
			repAreaCheckRow = db((db.sm_doctor_visit_plan.cid == cid)  & (db.sm_doctor_visit_plan.rep_id == rep_id) & (db.sm_doctor_visit_plan.route_id == area_id)).select(db.sm_doctor_visit_plan.rep_name,db.sm_doctor_visit_plan.route_name, limitby=(0, 1))						
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
				db((db.sm_doctor_day_plan.cid==cid) &(db.sm_doctor_day_plan.rep_id==rep_id) & (db.sm_doctor_day_plan.area_name==area_name) & (db.sm_doctor_day_plan.plan_date==setDate) & (db.sm_doctor_day_plan.visit_time==setTime)).delete()
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
		
		else:            	    	
			session.userType='sup'					
			sup_Rows=db((db.sm_level.cid==cid)&(db.sm_level.level_name==area_name)).select(db.sm_level.level_id,limitby=(0,1))   					
			docStr = ''
			if sup_Rows:
				area_id=sup_Rows[0].level_id
			
			resultSuccess=''
			resultFailed=''
			repAreaCheckRow=''
			repName=''
			get_month=''
			
			repAreaCheckRow = db((db.sm_doctor_visit_plan.cid == cid)  & (db.sm_doctor_visit_plan.rep_id == rep_id)  & (db.sm_doctor_day_plan.area_name==area_name)).select(db.sm_doctor_visit_plan.rep_name,db.sm_doctor_visit_plan.route_name, limitby=(0, 1))			

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
				db((db.sm_doctor_day_plan.cid==cid) &(db.sm_doctor_day_plan.rep_id==rep_id) & (db.sm_doctor_day_plan.area_id==area_id) & (db.sm_doctor_day_plan.plan_date==setDate)& (db.sm_doctor_day_plan.visit_time==setTime)).delete()
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
	if not repRow:
	   retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
	   return retStatus
	else:
		user_type = repRow[0].user_type				
		if user_type=='rep':
			mc_Rows=db((db.sm_microunion.cid==cid)&(db.sm_microunion.microunion_name==area_name)).select(db.sm_microunion.area_id,limitby=(0,1))		    
			
			clientStr = ''
			if mc_Rows:
			    area_id=mc_Rows[0].area_id
			
			clientRows=db((db.sm_client.cid==cid)&(db.sm_client.area_id==area_id)).select(db.sm_client.client_id, db.sm_client.name,  groupby = db.sm_client.client_id, orderby=db.sm_client.client_id)
			clientStr = ''
			for clientRows in clientRows:
				client_id= str(clientRows.client_id).strip()	
				name=str(clientRows.name).strip()	
				if clientStr=='':
					clientStr = str(name) +'|'+ str(client_id)	
				else:
					clientStr +='rdrd'+ str(name)+'|'+ str(client_id)
			
			
			client_check_Rows=db((db.sm_client_day_plan.cid==cid) &(db.sm_client_day_plan.rep_id==rep_id) & (db.sm_client_day_plan.area_name==area_name) & (db.sm_client_day_plan.plan_date==setDate)& (db.sm_client_day_plan.visit_time==setTime)).select(db.sm_client_day_plan.client_id, db.sm_client_day_plan.client_name)			    
			client_checkStr = ''
			for client_check_Rows in client_check_Rows:
			    client_c_id= str(client_check_Rows.client_id).strip()	
			    client_c_name=str(client_check_Rows.client_name).strip()
	
			    if client_checkStr=='':
			        client_checkStr = str(client_c_name) +'|'+ str(client_c_id)
	
			    else:
			        client_checkStr +='rdrd'+ str(client_c_name)+'|'+ str(client_c_id)
						
			return clientStr+'<syncdata>'+client_checkStr		

		else: 
			session.userType='sup'					
			sup_Rows=db((db.sm_level.cid==cid)&(db.sm_level.level_name==area_name)).select(db.sm_level.level_id,limitby=(0,1))   					
			clientStr = ''
			if sup_Rows:
				area_id=sup_Rows[0].level_id
			
			clientRows=db((db.sm_client.cid==cid)&(db.sm_client.area_id==area_id)).select(db.sm_client.client_id, db.sm_client.name,  groupby = db.sm_client.client_id, orderby=db.sm_client.client_id)
			clientStr = ''
			for clientRows in clientRows:
				client_id= str(clientRows.client_id).strip()
				name=str(clientRows.name).strip()
				
				if clientStr=='':
					clientStr = str(name) +'|'+ str(client_id)
				
				else:
					clientStr +='rdrd'+ str(name)+'|'+ str(client_id)
			
			
			client_check_Rows=db((db.sm_client_day_plan.cid==cid) &(db.sm_client_day_plan.rep_id==rep_id) & (db.sm_client_day_plan.area_name==area_name) & (db.sm_client_day_plan.plan_date==setDate)& (db.sm_client_day_plan.visit_time==setTime)).select(db.sm_client_day_plan.client_id, db.sm_client_day_plan.client_name)			    
			client_checkStr = ''
			for client_check_Rows in client_check_Rows:
				client_c_id= str(client_check_Rows.client_id).strip()
				client_c_name=str(client_check_Rows.client_name).strip()
			
				if client_checkStr=='':
					client_checkStr = str(client_c_name) +'|'+ str(client_c_id)
				
				else:
					client_checkStr +='rdrd'+ str(client_c_name)+'|'+ str(client_c_id)
			
			return clientStr+'<syncdata>'+client_checkStr


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
	if not repRow:
	   retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
	   return retStatus
	else:
		user_type = repRow[0].user_type		        		
		if user_type=='rep':			            			
			mc_Rows=db((db.sm_microunion.cid==cid)&(db.sm_microunion.microunion_name==area_name)).select(db.sm_microunion.microunion_id,limitby=(0,1))		    
			clientStr = ''
			if mc_Rows:
			  	area_id=mc_Rows[0].microunion_id

			repCheckRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db. sm_rep.password == rep_pass)).select(db.sm_rep.name, limitby=(0, 1))			
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
				db((db.sm_client_day_plan.cid==cid) &(db.sm_client_day_plan.rep_id==rep_id) & (db.sm_client_day_plan.area_name==area_name) & (db.sm_client_day_plan.plan_date==setDate)& (db.sm_client_day_plan.visit_time==setTime)).delete()
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

		else:            	    	
			session.userType='sup'					
			sup_Rows=db((db.sm_level.cid==cid)&(db.sm_level.level_name==area_name)).select(db.sm_level.level_id,limitby=(0,1))   					
			docStr = ''
			if sup_Rows:
				area_id=sup_Rows[0].level_id
		
			repCheckRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == rep_pass)).select(db.sm_rep.name, limitby=(0, 1))			
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
				db((db.sm_client_day_plan.cid==cid) &(db.sm_client_day_plan.rep_id==rep_id)  & (db.sm_client_day_plan.area_name==area_name) &  (db.sm_client_day_plan.plan_date==setDate) & (db.sm_client_day_plan.visit_time==setTime)).delete()
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
		user_type = repRow[0].user_type		
		if user_type=='rep':			
			mc_Rows=db((db.sm_microunion.cid==cid)&(db.sm_microunion.microunion_name==area_name)).select(db.sm_microunion.area_id,limitby=(0,1))   					        
			
			if mc_Rows:
			    area_id=mc_Rows[0].area_id

			farmRows=db((db.sm_farm.cid==cid) & (db.sm_farm.route==area_id)).select(db.sm_farm.farm_id, db.sm_farm.farm_name, groupby = db.sm_farm.farm_id, orderby=db.sm_farm.farm_id)		    			
			farmStr = ''
			for farmRows in farmRows:
			    farm_id= str(farmRows.farm_id).strip()
			    farm_name=str(farmRows.farm_name).strip()
	
			    if farmStr=='':
			        farmStr = str(farm_name) +'|'+ str(farm_id)
			    else:
			        farmStr +='rdrd'+ str(farm_name)+'|'+ str(farm_id)
	
			farm_check_Rows=db((db.sm_farm_day_plan.cid==cid)  & (db.sm_farm_day_plan.rep_id==rep_id)  & (db.sm_farm_day_plan.area_name==area_name) & (db.sm_farm_day_plan.plan_date==setDate) & (db.sm_farm_day_plan.visit_time==setTime)).select(db.sm_farm_day_plan.farm_id, db.sm_farm_day_plan.farm_name)		    
			farm_checkStr = ''
			
			for farm_check_Rows in farm_check_Rows:
			    farm_c_id= str(farm_check_Rows.farm_id).strip()
			    farm_c_name=str(farm_check_Rows.farm_name).strip()
	
			    if farm_checkStr=='':
			        farm_checkStr = str(farm_c_name) +'|'+ str(farm_c_id)
			    else:
			        farm_checkStr +='rdrd'+ str(farm_c_name)+'|'+ str(farm_c_id)
					
			return farmStr+'<syncdata>'+farm_checkStr

		else: 
			session.userType='sup'					
			sup_Rows=db((db.sm_level.cid==cid)&(db.sm_level.level_name==area_name)).select(db.sm_level.level_id,limitby=(0,1))   					
 					
			if sup_Rows:
				area_id=sup_Rows[0].level_id
				
			farmRows=db((db.sm_farm.cid==cid) & (db.sm_farm.route==area_id)).select(db.sm_farm.farm_id, db.sm_farm.farm_name,  groupby = db.sm_farm.farm_id, orderby=db.sm_farm.farm_id)		    
			farmStr = ''
			for farmRows in farmRows:
				farm_id= str(farmRows.farm_id).strip()
				farm_name=str(farmRows.farm_name).strip()
			
			if farmStr=='':
				farmStr = str(farm_name) +'|'+ str(farm_id)
			else:
				farmStr +='rdrd'+ str(farm_name)+'|'+ str(farm_id)
			
			farm_check_Rows=db((db.sm_farm_day_plan.cid==cid)  &(db.sm_farm_day_plan.rep_id==rep_id) & (db.sm_farm_day_plan.area_name==area_name) & (db.sm_farm_day_plan.plan_date==setDate) & (db.sm_farm_day_plan.visit_time==setTime)).select(db.sm_farm_day_plan.farm_id, db.sm_farm_day_plan.farm_name)		    
			farm_checkStr = ''
			farm_c_name = ''
			farm_c_id = ''
			for farm_check_Rows in farm_check_Rows:
				farm_c_id= str(farm_check_Rows.farm_id).strip()
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
	if not repRow:
	   retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
	   return retStatus
	else:
		
		user_type = repRow[0].user_type		        		
		if user_type=='rep':			
			mc_Rows=db((db.sm_microunion.cid==cid)&(db.sm_microunion.microunion_name==area_name)).select(db.sm_microunion.microunion_id,limitby=(0,1))
			if mc_Rows:
			    area_id=mc_Rows[0].microunion_id
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
				db((db.sm_farm_day_plan.cid==cid) &(db.sm_farm_day_plan.rep_id==rep_id) & (db.sm_farm_day_plan.area_name==area_name) & (db.sm_farm_day_plan.plan_date==setDate)& (db.sm_farm_day_plan.visit_time==setTime)).delete()
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
		else:
			session.userType='sup'					
			sup_Rows=db((db.sm_level.cid==cid)&(db.sm_level.level_name==area_name)).select(db.sm_level.level_id,limitby=(0,1))   					
			if sup_Rows:
				area_id=sup_Rows[0].level_id
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
				db((db.sm_farm_day_plan.cid==cid) &(db.sm_farm_day_plan.rep_id==rep_id) & (db.sm_farm_day_plan.area_name==area_name) & (db.sm_farm_day_plan.plan_date==setDate) & (db.sm_farm_day_plan.visit_time==setTime)).delete()
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