
def home():

	response.title = "Tour Plan"

	btn_tour_plan_details_page=request.vars.btn_tour_plan_details_page
	btn_tour_plan_details_page_d=request.vars.btn_tour_plan_details_page_d
	# return date
	date_from = request.vars.date_from
	date_to = request.vars.date_to
	pr_ff = request.vars.ff_id
	if date_from=='' or date_from == 'None' or date_to=='' or date_to == 'None':
		session.flash= "Please select a Date range"
		redirect(URL('home'))
    # return pr_ff
	# return date_from
    # pr_ff=request.vars.pr_ff
    # return pr_ff

	if btn_tour_plan_details_page:
		redirect (URL('tour_plan_details_page',vars=dict(date_from=date_from, date_to=date_to, pr_ff=pr_ff )))

	if btn_tour_plan_details_page_d:
		redirect (URL('tour_plan_details_page_download',vars=dict(date_from=date_from, date_to=date_to, pr_ff=pr_ff )))
	            

	return dict()




################################# 	TOUR PLAN SHOW ####################################

def tour_plan():

	import datetime
	date_from=request.vars.date_from
	date_to=request.vars.date_to
	# return date_from,date_to

	today = datetime.date.today()
	first_day = today.replace(day=1)
	session.first_day = first_day
	cid = session.cid
	id_condition = ''
	status_condition = ''
	level_condition = ''

	get_month=str(first_day).split('-')[1]
	if  int(get_month)==1:
		session.show_month=	'JAN'
	if  int(get_month)==2:
		session.show_month=	'FEB'
	if  int(get_month)==3:
		session.show_month=	'MAR'
	if  int(get_month)==4:
		session.show_month=	'APR'
	if  int(get_month)==5:
		session.show_month=	'MAY'
	if  int(get_month)==6:
		session.show_month=	'JUN'
	if  int(get_month)==7:
		session.show_month=	'JUL'
	if  int(get_month)==8:
		session.show_month=	'AUG'
	if  int(get_month)==9:
		session.show_month=	'SEP'
	if  int(get_month)==10:
		session.show_month=	'OCT'
	if  int(get_month)==11:
		session.show_month=	'NOV'
	if  int(get_month)==12:
		session.show_month=	'DEC'

	# return cid
	response.title = "Tour Plan"

	search_type = str(request.vars.search_type).strip()
	select_item = str(request.vars.select_item).strip().upper()
	# return select_item
	filter_button = str(request.vars.filter_btn).strip()
	session.filter_button = filter_button
	all_button = str(request.vars.all_btn).strip()


	
	id_condition = ''

	if session.filter_button == 'Filter':
		session.search_type=search_type
		session.select_item=select_item
		if session.search_type == "ID/Name" and session.select_item != "":
			session.select_item = session.select_item.split('|')[0]
			id_condition = " and rep_id = '"+str(session.select_item)+"'"

		elif session.search_type == "Status" and session.select_item != "":
			if session.select_item=='APPROVED':
				status='CONFIRMED'
				status_condition = " and status = '"+str(status)+"'"

			elif select_item=='AMND':
				status='CREQ'
				status_condition = " and status = '"+str(status)+"'"

			elif select_item=='PENDING':
				status='SUBMITTED'
				status_condition = " and status = '"+str(status)+"'"

		elif session.search_type == "Level" and session.select_item != "":
			if session.select_item=='DIVISION':
				level_depth_no= 0
				level_condition = " and level_depth_no = '"+str(level_depth_no)+"'"

			elif select_item=='ZONE':
				level_depth_no= 1
				level_condition = " and level_depth_no = '"+str(level_depth_no)+"'"

			elif select_item=='AREA':
				level_depth_no='SUBMITTED'
				level_condition = " and level_depth_no = '"+str(level_depth_no)+"'"
			# return condition

		# elif session.search_type == "Name" and session.select_item != "":
		# 	# return select_item
		# 	condition = " and name = '"+str(session.select_item)+"'"
		elif session.search_type == "Month" and session.select_item != "":
			month_list='JAN,FEB,MAR,APR,MAY,JUNE,JULY,AUG,SEP,OCT,NOV,DEC'
			# return session.search_type +'   '+session.select_item
			# return month_list.find(session.select_item)
			if (month_list.find(session.select_item))==-1:
				session.flash='Please enter valid Month'
			else:
				if select_item=='JAN':
					session.first_day=str(first_day).split('-')[0]+'-'+'01-01'
				if select_item=='FEB':
					session.first_day=str(first_day).split('-')[0]+'-'+'02-01'
				if select_item=='MAR':
					session.first_day=str(first_day).split('-')[0]+'-'+'03-01'
				if select_item=='APR':
					session.first_day=str(first_day).split('-')[0]+'-'+'04-01'
				if select_item=='MAY':
					session.first_day=str(first_day).split('-')[0]+'-'+'05-01'
				if select_item=='JUNE':
					session.first_day=str(first_day).split('-')[0]+'-'+'06-01'
				if select_item=='JUL':
					session.first_day=str(first_day).split('-')[0]+'-'+'07-01'
				if select_item=='AUG':
					session.first_day=str(first_day).split('-')[0]+'-'+'08-01'
				if select_item=='SEP':
					session.first_day=str(first_day).split('-')[0]+'-'+'09-01'
				if select_item=='OCT':
					session.first_day=str(first_day).split('-')[0]+'-'+'10-01'
				if select_item=='NOV':
					session.first_day=str(first_day).split('-')[0]+'-'+'11-01'
				if select_item=='DEC':
					session.first_day=str(first_day).split('-')[0]+'-'+'12-01'
				session.show_month=	select_item
	
	# return 	session.first_day
	if (all_button=='All'):
		session.filter_button == ''
		session.search_type=''
		session.select_item=''
		session.first_day=first_day


	active_rep_sql = "select rep_id, name, user_type, status from sm_rep where cid = '"+str(cid)+"' "+ id_condition+" and status = 'ACTIVE' ;"
	# return active_rep_sql
	active_rep = db.executesql(active_rep_sql, as_dict=True) 
	session.id_condition = id_condition
	session.status_condition = status_condition
	session.level_condition=level_condition
	# return session.first_day
	return dict(active_rep= active_rep)






################################# 	TOUR PLAN DOWNLOAD ################################




def tour_plan_list_Download():

	response.title = "Tour Plan Download"
	cid = session.cid
	id_condition=session.id_condition
	level_condition = session.level_condition
	status_condition=session.status_condition
	first_day = session.first_day
	# return status_condition

	search_type = str(request.vars.search_type).strip()
	select_item = str(request.vars.select_item).strip().upper()
	# return select_item
	filter_button = str(request.vars.filter_btn).strip()
	session.filter_button = filter_button
	# all_button = str(request.vars.all_btn).strip()

	myString = 'Tour Plan List \n\n'
	myString += ' ID , Name, Level Name, Level, Status  \n'
	total=0
	attTime = ''
	totalCount = 0
	level_name = ''
	status = ''
	level_name_str = ''

	active_rep_sql = "select rep_id, name, user_type, status from sm_rep where cid = '"+str(cid)+"' "+ id_condition+" and status = 'ACTIVE' group by rep_id ;"
	# return active_rep_sql
	active_rep = db.executesql(active_rep_sql, as_dict=True) 

	for i in range(len(active_rep)):
		records_ov_dict = active_rep[i]  
		rep_id = str(records_ov_dict["rep_id"])
		name = str(records_ov_dict["name"])
		user_type = str(records_ov_dict["user_type"])


		if user_type == 'sup':
			sup_level_sql = "select level_name,level_depth_no from sm_supervisor_level where cid = '"+str(session.cid)+"' and sup_id = '"+str(rep_id)+"' ;"
			# return sup_level_sql
			sup_level = db.executesql(sup_level_sql, as_dict = True)
			for j in range(len(sup_level)):
				records_dict = sup_level[j]  
				level = str(records_dict["level_name"])
				level_depth_no = str(records_dict["level_depth_no"])

				if level_depth_no == '0':
					level_name = 'DIVISION'
				elif level_depth_no == '1':
					level_name = 'ZONE'
				elif level_depth_no == '2':
					level_name = 'AREA'


		else:
			rep_level_sql = "select area_name from sm_rep_area where cid = '"+str(session.cid)+"' and rep_id = '"+str(rep_id)+"' ;"
			rep_level = db.executesql(rep_level_sql, as_dict = True)
			for k in range(len(rep_level)):
				rep_records_dict = rep_level[k]  
				level = str(rep_records_dict["area_name"])
				level_name = 'FF'


		get_stauts_sql =  "select status from sm_doctor_visit_plan where cid = '"+str(session.cid)+"' and rep_id = '"+str(rep_id)+"'  and  first_date = '"+str(first_day)+"' "+status_condition+" ;"
		get_status = db.executesql(get_stauts_sql, as_dict = True)

		status='NOT SUBMITTED'
		for a in range(len(get_status)):
			records_ov_dict_stauts = get_status[a]  
			status = str(records_ov_dict_stauts["status"]).upper()

			if status=='CONFIRMED':
				status='APPROVED'

			elif status=='CREQ':
				status='AMND'

			elif status=='SUBMITTED':
				status='PENDING'

		# myString += str(rep_id) + ',' +str(name) + ',' +str(level_name) + ',' +str(level) + ',' +str(status) + '\n'

		if session.search_type=='Level':
			# return str(session.select_item)+'---'+str(level_name)
			if level_name==session.select_item:
				myString += str(rep_id) + ',' +str(name) + ',' +str(level_name) + ',' +str(level) + ',' +str(status) + '\n'


		
		elif session.search_type=='Status':
			# return status
			if status==session.select_item:
				myString += str(rep_id) + ',' +str(name) + ',' +str(level_name) + ',' +str(level) + ',' +str(status) + '\n'

	
		else:		
			myString += str(rep_id) + ',' +str(name) + ',' +str(level_name) + ',' +str(level) + ',' +str(status) + '\n'
    	

	import gluon.contenttype
	response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
	response.headers['Content-disposition'] = 'attachment; filename=Tour Plan List.csv'
	return str(myString)







################################# 	TOUR PLAN DETAILS ################################

def tour_plan_details():

	cid = session.cid
	response.title = "Tour Plan Details"
	# return "tour plan details"
	import datetime
	# today = datetime.date.today()
	# first_day = today.replace(day=1)
	# session.first_day = first_day

	rep_id = request.args(0)
	rep_name = request.args(1)
	level = request.args(2)


	from_date = str(request.vars.from_dt)
	to_date = str(request.vars.to_dt)
	session.from_date = from_date
	session.to_date = to_date
	# return from_date,to_date
	# return session.rep_id
	filter_button=str(request.vars.btn_filter).strip()
	# return filter_button
	all_button=str(request.vars.ALL).strip()

	condition = ''

	session.rep_id = rep_id
	return dict(rep_id = rep_id,cid = cid,condition = condition,rep_name=rep_name,level=level)



def tour_plan_details_list_Download():

	cid = session.cid
	# return cid
	import datetime
	today = datetime.date.today()
	first_day = today.replace(day=1)
	session.first_day = first_day

	myString = 'Tour Plan Details \n\n'
	myString += ' Date, Morning, Type, Evening, Type  \n'
	total=0
	attTime = ''
	totalCount = 0
	# rep_id = request.args(0)
	# return session.rep_id
	morning_level = ''
	data = {}
	merged_data = {}
	
	type_ev=''
	rname =''
	rname_e =''

	morning_tour_plan_sql = "select id, rep_id, rep_name, schedule_date, route_id, note from sm_doctor_visit_plan where cid = '"+str(cid)+"' and rep_id = '"+str(session.rep_id)+"' and  first_date = '"+str(session.first_day)+"' and note = 'Morning'  order by schedule_date"
	morning_tour_plan = db.executesql(morning_tour_plan_sql, as_dict=True)


	for i in range(len(morning_tour_plan)):
		invRecords_str_single = morning_tour_plan[i]
		date = str(invRecords_str_single['schedule_date'])

		morning_data_sql = "select route_id, route_name from sm_doctor_visit_plan where cid = '"+str(cid)+"' and rep_id = '"+str(session.rep_id)+"' and  schedule_date = '"+str(date)+"' and note = 'Morning'"
		morning_record = db.executesql(morning_data_sql, as_dict=True)
		morning_str=''
		for m in range(len(morning_record)):
			m_str_single = morning_record[m]
			rname = str(m_str_single['route_name'])
			if rname!='':
				route_id = str(m_str_single['route_id'])+'|'+rname
			else:
				route_id = str(m_str_single['route_id'])+'|'+rname

			if morning_str=='':
				morning_str=route_id
			else:
				morning_str=morning_str+'| '+route_id

		type_morning=''	
		if morning_str.find('| HQ')!=-1:
			type_morning='HQ'

		if morning_str.find('| EHQ')!=-1:
			if type_morning!='':
				type_morning=type_morning+'|'+'EHQ'
			else:
				type_morning='EHQ'

		if morning_str.find('| NS')!=-1:
			if type_morning!='':
				type_morning=type_morning+'|'+'NS'
			else:
				type_morning='NS'

		if morning_str=='HQ':
			type_morning='HQ'

		if morning_str=='EHQ':
			type_morning='EHQ'

		if morning_str=='NS':
			type_morning='NS'

		evening_data_sql = "select route_id, route_name from sm_doctor_visit_plan where cid = '"+str(cid)+"' and rep_id = '"+str(session.rep_id)+"' and  schedule_date = '"+str(date)+"' and note = 'Evening'"
		# return evening_data_sql
		evening_record = db.executesql(evening_data_sql, as_dict=True)
		evening_str=''

		for n in range(len(evening_record)):
			m_str_single = evening_record[n]
			rname_e = str(m_str_single['route_name'])
			if rname_e!='':
				route_id_e = str(m_str_single['route_id'])+'|'+rname_e
			else:
				route_id_e = str(m_str_single['route_id'])+'|'+rname_e

			if evening_str=='':
				evening_str=route_id_e
			else:
				evening_str=evening_str+'| '+route_id_e

		type_ev = ''
		if evening_str.find('| HQ')!=-1:
			type_ev='HQ'

		if evening_str.find('| EHQ')!=-1:
			if type_ev!='':
				type_ev=type_ev+'|'+'EHQ'
			else:
				type_ev='EHQ'

		if evening_str.find('| NS')!=-1:
			if type_ev!='':
				type_ev=type_ev+'|'+'NS'
			else:
				type_ev='NS'


		if evening_str=='HQ':
			type_ev='HQ'

		if evening_str=='EHQ':
			type_ev='EHQ'

		if evening_str=='NS':
			type_ev='NS'

		myString += str(date) + ',' +str(morning_str) + ',' +str(type_morning) + ',' +str(evening_str) + ',' +str(type_ev) + '\n'
    
    # return myString
	import gluon.contenttype
	response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
	response.headers['Content-disposition'] = 'attachment; filename=Tour Plan Details_List.csv'
	return str(myString)





##################################### TOUR PLAN DETAILS PAGE ####################################


def tour_plan_details_page():

	import datetime
	cid=session.cid
	# return cid
	date_from=request.vars.date_from
	date_to=request.vars.date_to
	# return date_from
	pr_ff = str(request.vars.ff_id).split('|')[0]
	# return pr_ff

	# return date_from,date_to
	date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
	date_to_m=date_to_m + datetime.timedelta(days = 1)
	# return date_to_m

	pr_region=request.vars.pr_region
	pr_zone=request.vars.pr_zone
	pr_ff=request.vars.pr_ff
	pr_area=request.vars.pr_area
	pr_territory=request.vars.pr_territory

	ff_id=str(request.vars.ff_id).strip()
	from_date = str(request.vars.from_date).strip()
	to_date = str(request.vars.to_date).strip()
	# return ff_id

	# filter_button = str(request.vars.filter_btn).strip()
	# session.filter_button = filter_button
	# all_button = str(request.vars.all_btn).strip()
	# session.all_button = all_button

	# if session.filter_button == 'Filter':
	# 	redirect (URL('tour_plan_details_page',vars=dict(from_date=from_date, to_date=to_date, pr_ff=pr_ff )))
	    
	qset=db()
	qset=qset(db.sm_doctor_visit_plan.cid == cid)
	qset = qset(db.sm_doctor_visit_plan.schedule_date >= date_from)
	qset = qset(db.sm_doctor_visit_plan.schedule_date < date_to_m)
	qset = qset(db.sm_doctor_visit_plan.status == 'Confirmed')  


	if pr_ff!='':
	    qset=qset(db.sm_doctor_visit_plan.rep_id == (pr_ff).split('|')[0])

	records=qset.select(db.sm_doctor_visit_plan.rep_id,db.sm_doctor_visit_plan.rep_name,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.note,db.sm_doctor_visit_plan.status, orderby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.rep_id, groupby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.rep_id)
	# return db._lastsql

	return dict(cid = cid, records=records,date_from=date_from,date_to=date_to, date_to_m=date_to_m,pr_region=pr_region,pr_zone=pr_zone,pr_ff=pr_ff,pr_area=pr_area,pr_territory=pr_territory)




##################################### TOUR PLAN DETAILS PAGE DOWNLOAD ####################################

def tour_plan_details_page_download():

	import datetime
	cid=session.cid
	# return cid
	date_from=request.vars.date_from
	date_to=request.vars.date_to
	# return date_from
	pr_ff = request.vars.pr_ff
	# return pr_ff

	# return date_from,date_to
	date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
	date_to_m=date_to_m + datetime.timedelta(days = 1)
	# return date_to_m
	# return "hello"
	myString = 'Tour Plan Details Page Download \n\n'
	myString += ' Date, Name of MPO, Morning, Type, Evening, Type  \n'
	total=0
	attTime = ''
	totalCount = 0
	type_morning=''
	type_ev=''

	qset=db()
	qset=qset(db.sm_doctor_visit_plan.cid == cid)
	qset = qset(db.sm_doctor_visit_plan.schedule_date >= date_from)
	qset = qset(db.sm_doctor_visit_plan.schedule_date < date_to_m)
	qset = qset(db.sm_doctor_visit_plan.status == 'Confirmed')  


	if pr_ff!='':
		qset=qset(db.sm_doctor_visit_plan.rep_id == (pr_ff).split('|')[0])

	# return pr_ff
	records=qset.select(db.sm_doctor_visit_plan.rep_id,db.sm_doctor_visit_plan.rep_name,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.note,db.sm_doctor_visit_plan.status, orderby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.rep_id, groupby=db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.rep_id)
	# return db._lastsql
	for rec in records:
		schedule_date= rec.schedule_date
		rep_id = rec.rep_id
		rep_name= rec.rep_name+'|'+rec.rep_id

		morning_data_sql = "select route_id,route_name from sm_doctor_visit_plan where cid = '"+str(cid)+"' and  schedule_date = '"+str(schedule_date)+"' and note = 'Morning' and  rep_id='"+str(rep_id)+"'"
		#=morning_data_sql
		morning_record = db.executesql(morning_data_sql, as_dict=True)
		morning_route=''
		for m in range(len(morning_record)):
		    m_str_single = morning_record[m]
		    route_id=str(m_str_single['route_id'])
		    rname=str(m_str_single['route_name'])
		    if morning_route=='':
		        morning_route=route_id+'|'+rname
		    
		    else:
		        morning_route=morning_route+'| '+route_id+'|'+rname

		type_morning=''
		if morning_route.find('| HQ')!=-1:
			type_morning='HQ'

		if morning_route.find('| EHQ')!=-1:
			if type_morning!='':
				type_morning=type_morning+'|'+'EHQ'
			else:
				type_morning='EHQ'

		if morning_route.find('| NS')!=-1:
			if type_morning!='':
				type_morning=type_morning+'|'+'NS'
			else:
				type_morning='NS'

		if morning_route=='HQ':
			type_morning='HQ'

		if morning_route=='EHQ':
			type_morning='EHQ'

		if morning_route=='NS':
			type_morning='NS'

		evening_data_sql = "select route_id,route_name from sm_doctor_visit_plan where cid = '"+str(cid)+"' and  schedule_date = '"+str(schedule_date)+"' and note = 'Evening' and  rep_id='"+str(rep_id)+"'"
		#=evening_data_sql
		evening_record = db.executesql(evening_data_sql, as_dict=True)
		evening_route=''
		for m in range(len(evening_record)):
		    m_str_single = evening_record[m]
		    route_id=str(m_str_single['route_id'])
		    rname=str(m_str_single['route_name'])
		    if evening_route=='':
		        evening_route=route_id+'|'+rname
		    
		    else:
		        evening_route=evening_route+'| '+route_id+'|'+rname

		type_ev = ''
		if evening_route.find('| HQ')!=-1:
			type_ev='HQ'

		if evening_route.find('| EHQ')!=-1:
			if type_ev!='':
				type_ev=type_ev+'|'+'EHQ'
			else:
				type_ev='EHQ'

		if evening_route.find('| NS')!=-1:
			if type_ev!='':
				type_ev=type_ev+'|'+'NS'
			else:
				type_ev='NS'


		if evening_route=='HQ':
			type_ev='HQ'

		if evening_route=='EHQ':
			type_ev='EHQ'

		if evening_route=='NS':
			type_ev='NS'

		myString+=str(schedule_date)+','+str(rep_name)+','+str(morning_route)+','+str(type_morning)+','+str(evening_route)+','+str(type_ev)+'\n'


	import gluon.contenttype
	response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
	response.headers['Content-disposition'] = 'attachment; filename=Tour Plan Details Page.csv'   
	return str(myString)


	# return dict()