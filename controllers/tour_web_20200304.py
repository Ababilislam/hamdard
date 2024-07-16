from random import randint
import urllib2
import calendar
import urllib
import time


def month_name (number):
    if number == 1:
        return "January"
    elif number == 2:
        return "February"
    elif number == 3:
        return "March"
    elif number == 4:
        return "April"
    elif number == 5:
        return "May"
    elif number == 6:
        return "June"
    elif number == 7:
        return "July"
    elif number == 8:
        return "August"
    elif number == 9:
        return "September"
    elif number == 10:
        return "October"
    elif number == 11:
        return "November"
    elif number == 12:
        return "December"


def days_in_month(year, month):
    """
    Inputs:
      year  - an integer between datetime.MINYEAR and datetime.MAXYEAR
              representing the year
      month - an integer between 1 and 12 representing the month

    Returns:
      The number of days in the input month.
    """

    #if month is december, we proceed to next year
    def month_december(month):
        if month > 12:
            return month-12  #minus 12 if cross year.
        else:
            return month

    #if month is december, we proceed to next year
    def year_december(year, month):
        if month > 12:
            return year + 1
        else:
            return year

    #verify if month/year is valid
    if (month < 1) or (month > 12):
        return ("please enter a valid month")
    elif (year < 1) or (year > 9999):
        return ("please enter a valid year between 1 - 9999")
    else:
        #subtract current month from next month then get days
        date1 = (datetime.date(year_december(year, month+1), month_december(month+1), 1) - datetime.date(year, month, 1)).days
        return (date1)
# Unscheduled
# http://127.0.0.1:8000/lscmreporting/syncmobile/?cid=LSCRM&rep_id=1001&rep_pass=123&synccode=7048&market_id=M000003

def tourShow_web():   
    import datetime 
    retStatus = ''   
    sDate=''      
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()    
    monthPass = str(request.vars.monthPass).strip()
    
    session.cid = cid
    session.rep_id = rep_id
    session.password = password
    
    session.monthPass = monthPass
    
    if (session.monthPass=='This'):
        checkDate=first_currentDate
    else:
                
        Dcheck=int(str(current_date).split('-')[2].split(' ')[0])-2
        todayDate = datetime.date.today()
        
        if (todayDate - todayDate.replace(day=1)).days > Dcheck:
            x= todayDate + datetime.timedelta(25)
            x.replace(day=1)            
            checkDate1 = str(x)
            
        else:
            checkDate1= todayDate.replace(day=1)
        checkDate=checkDate1.split('-')[0]+'-'  +checkDate1.split('-')[1]  +'-01'

        
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.user_type, limitby=(0, 1))

    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = repRow[0].user_type
    
    
    draft_info = db((db.sm_doctor_visit_plan.cid==cid)  &(db.sm_doctor_visit_plan.rep_id==session.rep_id) & (db.sm_doctor_visit_plan.first_date==checkDate)).select(db.sm_doctor_visit_plan.status, orderby=db.sm_doctor_visit_plan.id,limitby=(0,1))

    status='Draft'    
    if draft_info:
        status=draft_info[0].status
        
    strValueMorning=''            
   
    draft_infoAll = db((db.sm_doctor_visit_plan.cid==cid)  &(db.sm_doctor_visit_plan.rep_id==session.rep_id) & (db.sm_doctor_visit_plan.first_date==checkDate)  & (db.sm_doctor_visit_plan.status==status) &((db.sm_doctor_visit_plan.note=='Morning') | (db.sm_doctor_visit_plan.note==''))).select(db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.schedule_date, orderby=db.sm_doctor_visit_plan.schedule_date)

    for draft_infoAll in draft_infoAll:
        route_name = draft_infoAll.route_name   
        sDate=str(draft_infoAll.schedule_date)
        route_id=draft_infoAll.route_id
        
        if route_name=='':
            route_name=route_id
            strValueMorning=strValueMorning+'<'+sDate+'>'+route_name

        
        if ((status=='Done') or (status=='Submitted') or (status=='Confirmed') or (status=='Draft') ):
            docStr='Doctor'
            clStr='Client'
            frStr='Farm'
            docInfo=''
            clInfo=''
            frInfo=''
            
            rowDoctor = db((db.sm_doctor_day_plan.cid==cid)  &(db.sm_doctor_day_plan.rep_id==session.rep_id) & (db.sm_doctor_day_plan.area_id==route_id) & (db.sm_doctor_day_plan.plan_date==sDate)  &(db.sm_doctor_day_plan.visit_time=='Morning') ).select(db.sm_doctor_day_plan.doc_name,db.sm_doctor_day_plan.doc_id, orderby=db.sm_doctor_day_plan.doc_name)
#             return rowDoctor
            for rowDoctor in rowDoctor:
                docInfo = str(rowDoctor.doc_name)+'-'+str(rowDoctor.doc_id) 
                docStr= docStr+' '+docInfo+','
     
            rowClient = db((db.sm_client_day_plan.cid==cid)  &(db.sm_client_day_plan.rep_id==session.rep_id) & (db.sm_client_day_plan.area_id==route_id) & (db.sm_client_day_plan.plan_date==sDate)  &(db.sm_client_day_plan.visit_time=='Morning') ).select(db.sm_client_day_plan.client_name,db.sm_client_day_plan.client_id, orderby=db.sm_client_day_plan.client_name)
            for rowClient in rowClient:
                clInfo = str(rowClient.client_name)+'-'+str(rowClient.client_id) 
                clStr= clStr+' '+clInfo+','
                               
            rowFarm = db((db.sm_farm_day_plan.cid==cid)  &(db.sm_farm_day_plan.rep_id==session.rep_id) & (db.sm_farm_day_plan.area_id==route_id) & (db.sm_farm_day_plan.plan_date==sDate)  & (db.sm_farm_day_plan.visit_time=='Morning') ).select(db.sm_farm_day_plan.farm_name,db.sm_farm_day_plan.farm_id, orderby=db.sm_farm_day_plan.farm_name)
            for rowFarm in rowFarm:
                frInfo = str(rowFarm.farm_name)+'-'+str(rowFarm.farm_id) 
                frStr= frStr+' '+frInfo+','  
                    
            strValueMorning=strValueMorning+'<'+sDate+'>'+route_name+'<rdrd> '+docStr+'<rdrd> '+clStr+'<rdrd> '+frStr
        else:     
            strValueMorning=strValueMorning+'<'+sDate+'>'+route_name+'<rdrd> '+docStr+'<rdrd> '+clStr+'<rdrd> '+frStr
    
#     return  strValueMorning        
    
    strValueMorningE=''
    
    draft_infoAllE = db((db.sm_doctor_visit_plan.cid==cid)  &(db.sm_doctor_visit_plan.rep_id==session.rep_id) & (db.sm_doctor_visit_plan.first_date==checkDate) & (db.sm_doctor_visit_plan.status==status)&(db.sm_doctor_visit_plan.note=='Evening')).select(db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.schedule_date, orderby=db.sm_doctor_visit_plan.schedule_date)
    
    for draft_infoAllE in draft_infoAllE:
        route_name = draft_infoAllE.route_name   
        sDate=str(draft_infoAllE.schedule_date)
        route_id=draft_infoAllE.route_id

        if route_name=='':
            route_name=route_id
            strValueMorningE=strValueMorningE+'<'+sDate+'>'+route_name
         
        if ((status=='Done') or (status=='Submitted') or (status=='Confirmed') or (status=='Draft')):
            
            docStrE='Doctor'
            clStrE='Client'
            frStrE='Farm'           
            docInfoE=''
            clInfoE=''
            frInfoE=''
            
            
            rowDoctorE = db((db.sm_doctor_day_plan.cid==cid)  &(db.sm_doctor_day_plan.rep_id==session.rep_id) & (db.sm_doctor_day_plan.area_id==route_id) & (db.sm_doctor_day_plan.plan_date==sDate)  &(db.sm_doctor_day_plan.visit_time=='Evening') ).select(db.sm_doctor_day_plan.doc_name,db.sm_doctor_day_plan.doc_id, orderby=db.sm_doctor_day_plan.doc_name)
#             return rowDoctorE
            for rowDoctorE in rowDoctorE:
                docInfoE = str(rowDoctorE.doc_name)+'-'+str(rowDoctorE.doc_id) 
                docStrE=docStrE+' '+docInfoE+','
                
            rowClient = db((db.sm_client_day_plan.cid==cid)  &(db.sm_client_day_plan.rep_id==session.rep_id) & (db.sm_client_day_plan.area_id==route_id) & (db.sm_client_day_plan.plan_date==sDate)  &(db.sm_client_day_plan.visit_time=='Evening') ).select(db.sm_client_day_plan.client_name,db.sm_client_day_plan.client_id, orderby=db.sm_client_day_plan.client_name)
            
            for rowClient in rowClient:
                clInfoE = str(rowClient.client_name)+'-'+str(rowClient.client_id) 
                clStrE=clStrE+' '+clInfoE+','
                
            rowFarm = db((db.sm_farm_day_plan.cid==cid)  &(db.sm_farm_day_plan.rep_id==session.rep_id) & (db.sm_farm_day_plan.area_id==route_id) & (db.sm_farm_day_plan.plan_date==sDate)  &(db.sm_farm_day_plan.visit_time=='Evening') ).select(db.sm_farm_day_plan.farm_name,db.sm_farm_day_plan.farm_id, orderby=db.sm_farm_day_plan.farm_name)

            for rowFarm in rowFarm:
                frInfoE = str(rowFarm.farm_name)+'-'+str(rowFarm.farm_id) 
                frStrE=frStrE+' '+frInfoE+','
#                 return frStrE
            strValueMorningE=strValueMorningE+'<'+sDate+'>'+route_name+'<rdrd> '+docStrE+'<rdrd> '+clStrE+'<rdrd> '+frStrE

        else:     
            strValueMorningE=strValueMorningE+'<'+sDate+'>'+route_name+' <rdrd>'+docStrE+'<rdrd> '+clStrE+'<rdrd> '+frStrE
               
               
          
#     return strValueMorningE
    
    
    if user_type=='rep':
        session.userType='rep'
        userdepth=3
        repareaList=[]
        marketRows = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.rep_id == rep_id)).select(db.sm_rep_area.area_id, db.sm_rep_area.area_name, orderby=db.sm_rep_area.area_name, groupby=db.sm_rep_area.area_id)
        for marketRow in marketRows:
            area_id = marketRow.area_id
            area_name = marketRow.area_name
            repareaList.append(area_id)
        marketTourRows = db((db.sm_microunion.cid==cid)  &(db.sm_microunion.area_id.belongs(repareaList))).select(db.sm_microunion.microunion_id,db.sm_microunion.microunion_name, orderby=db.sm_microunion.microunion_name, groupby=db.sm_microunion.microunion_id|db.sm_microunion.microunion_name)
        session.userdepth = userdepth
    else:
        session.userType='sup'
        marketTourRows1 = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id)).select(db.sm_supervisor_level.level_id , db.sm_supervisor_level.level_name , db.sm_supervisor_level.level_depth_no,orderby=db.sm_supervisor_level.level_name, groupby=db.sm_supervisor_level.level_id)
#         return marketTourRows1
        areaList=[]
        for marketRowmarketTourRows1 in marketTourRows1:
            session.userdepth = marketRowmarketTourRows1.level_depth_no
            level='level'+str(marketRowmarketTourRows1.level_depth_no)+'_id'
            areaList.append(marketRowmarketTourRows1.level_id)
            supLevel='level'+str(session.userdepth)
        
        if int(session.userdepth)>0:
            marketTourRows=db((db.sm_level.cid == cid)& (db.sm_level.is_leaf == '1') & (db.sm_level[supLevel].belongs(areaList)) ).select(db.sm_level.level_id,db.sm_level.level_name,orderby=db.sm_level.level_id)
#             return marketTourRows
        else:
            marketTourRows=db((db.sm_level.cid == cid)& (db.sm_level.depth == '1') & (db.sm_level[supLevel].belongs(areaList)) ).select(db.sm_level.level_id,db.sm_level.level_name,orderby=db.sm_level.level_id)
                
    
#     ========Next Month
    DateTour=first_currentDate
    
    Dcheck=int(str(current_date).split('-')[2].split(' ')[0])-2
#     return Dcheck
    if monthPass=='Next':
        todayDate = datetime.date.today()
#         return (todayDate - todayDate.replace(day=1)).days
        if (todayDate - todayDate.replace(day=1)).days > Dcheck:
            x= todayDate + datetime.timedelta(25)
            x.replace(day=1)
            
            nextMaont = str(x)
        else:
            nextMaont= todayDate.replace(day=1)
        DateTour= nextMaont
#     return DateTour
    session.DateTour = DateTour
    monthGet=str(DateTour).split('-')[1]
    yearGet=str(DateTour).split('-')[0]
    
    month=int(monthGet)
    year=int(yearGet)
    monthDay=0
    days_month=0
    days_month= days_in_month(year, month)
    
    monthShow=''
    monthShow= month_name(month)
    session.days_month=days_month
    
#     return session.days_month
#  =========================Show Draf or Submitted====================
 
    
    setDateG=str(yearGet)+'-'+str(monthGet)
 
#     return setDateG
 
#     return marketTourRows
 
#     return strValueMorningE
    userSin=''
    
    return dict(marketTourRows=marketTourRows,sDate=sDate,days_month=days_month,monthShow=monthShow,setDateG=setDateG,status=status,strValueMorning=strValueMorning,strValueMorningE=strValueMorningE,userSin=userSin)
    
    
# ===================Tour Done=======

def tourSubmit():
    
    retStatus = ''
    cid=session.cid
    rep_id=session.rep_id
    password=session.password
    
    monthPass=session.monthPass
    DateTour=session.DateTour
    
    submitStrMorning=str(request.vars.submitStrMorning).strip()
    
    submitStrEvening=str(request.vars.submitStrEvening).strip()
    days_month=str(request.vars.submitStrEvening).strip()
    
    errorFlag=1
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.user_type,db.sm_rep.name, limitby=(0, 1))
    
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = repRow[0].user_type
        rep_name = repRow[0].name
        
        errorFlag=0
        

    if errorFlag==0:
        submitStrMorningList=submitStrMorning.split('<rd>')
        submitStrEveningList=submitStrEvening.split('<rd>')        
        tourArrayList_m = []
        tourArrayList = []
        i=0
        errorFlag=0
        current_date_check=int(str(current_date).split('-')[2])

        while i < len(submitStrMorningList)-1:
            submitStrMorningListSingle=submitStrMorningList[i]
            if (session.monthPass=='This'):
                if ((submitStrMorningListSingle=='') and (submitStrEveningList[i]=='') and (current_date_check <= i)):
                    errorFlag=1
            else:
                if ((submitStrMorningListSingle=='') and (submitStrEveningList[i]=='')):
                    errorFlag=1

                
            mSingleList=submitStrMorningListSingle.split('<fd>')
            i=i+1
            schedule_date=str(DateTour).split('-')[0]+'-'+str(DateTour).split('-')[1]+'-'+str(i)
            first_date=str(DateTour).split('-')[0]+'-'+str(DateTour).split('-')[1]+'-01'
            
            
            
            m=0

            while m < len(mSingleList):
                
                route_nameG=mSingleList[m].split('<fd>')[0]
                if route_nameG!='':
                    try:
                        route_name=route_nameG.split('|')[1]
                        route_id=route_nameG.split('|')[0]
                    except:
                        route_name=''
                        route_id=route_nameG
                    
                    ins_dict = {'cid':cid, 'rep_id':rep_id,'rep_name':rep_name, 'first_date':first_date, 'schedule_date':schedule_date, 'route_id':route_id, 'note':'Morning','status':'Submitted','field2':session.userdepth}
                    tourArrayList_m.append(ins_dict)
                    
                m=m+1
            
            
        
        i=0
        errorFlagEvening=0
        while i < len(submitStrEveningList)-1:
            submitStrEveningListSingle=submitStrEveningList[i]
            
            mSingleList=submitStrEveningListSingle.split('<fd>')
            i=i+1
            schedule_date=str(DateTour).split('-')[0]+'-'+str(DateTour).split('-')[1]+'-'+str(i)
            first_date=str(DateTour).split('-')[0]+'-'+str(DateTour).split('-')[1]+'-01'
            
            
            
            m=0

            while m < len(mSingleList):
                
                route_nameG=mSingleList[m].split('<fd>')[0]
                if route_nameG!='':
                    try:
                        route_name=route_nameG.split('|')[1]
                        route_id=route_nameG.split('|')[0]
                    except:
                        route_name=''
                        route_id=route_nameG
                    
                    ins_dict = {'cid':cid, 'rep_id':rep_id,'rep_name':rep_name, 'first_date':first_date, 'schedule_date':schedule_date, 'route_id':route_id, 'note':'Evening','status':'Submitted','field2':session.userdepth}
                    tourArrayList.append(ins_dict)
                m=m+1
        
        
        if ((errorFlag==1)):
                return 'Incomplete'        
        if ((len(tourArrayList_m) > 0) or (len(tourArrayList > 0))):
            delete_doc_area=db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id) & (db.sm_doctor_visit_plan.first_date == first_date)).delete()
            db.sm_doctor_visit_plan.bulk_insert(tourArrayList_m)
            db.sm_doctor_visit_plan.bulk_insert(tourArrayList)
                    
        if user_type=='rep':                             
            insStr="update sm_doctor_visit_plan p,sm_microunion m set p.route_name=m.microunion_name where m.cid=p.cid and m.microunion_id = p.route_id"                    
            insRun=db.executesql(insStr)               
        else:
            insStrSup="update sm_doctor_visit_plan p,sm_level l set p.route_name=l.level_name where l.cid=p.cid and l.level_id = p.route_id"                 
            insRun=db.executesql(insStrSup)
        
        return 'Success'





# ==============================================
# http://127.0.0.1:8000/lscmreporting/syncmobile/getClientInfo?cid=LSCRM&rep_id=101&rep_pass=123&synccode=5771&client_id=1
# getting route,merchandizing,client information
# def tourSubmit():
#     retStatus = ''
# #     return 'assf'
#     cid=session.cid
#     rep_id=session.rep_id
#     password=session.password
#     
#     monthPass=session.monthPass
#     DateTour=session.DateTour
#     
#     submitStrMorning=str(request.vars.submitStrMorning).strip()
#     submitStrEvening=str(request.vars.submitStrEvening).strip()
#     days_month=str(request.vars.submitStrEvening).strip()
#     
#     if monthPass=='This':
#         first_date=first_currentDate
#     if monthPass=='Next':
#         Dcheck=1
#         todayDate = datetime.date.today()
#         todayDate = datetime.date.today()  
#         x= todayDate + datetime.timedelta(25)
#         x.replace(day=1)
#         
#         nextMaont = str(x)
#         first_date=str(nextMaont).split('-')[0]+'-'+str(nextMaont).split('-')[1]+'-01'
#     
# #     return first_date
#     errorFlag=1
#     repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.user_type,db.sm_rep.name, limitby=(0, 1))
# #     return repRow
#     if not repRow:
#        retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
#        return retStatus
#     else:
#         user_type = repRow[0].user_type
#         rep_name = repRow[0].name
# 
#         updateStatus=db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id) & (db.sm_doctor_visit_plan.first_date == first_date)& (db.sm_doctor_visit_plan.status == 'Done')).update(status = 'Submitted')
#         
#         updateStatusClient=db((db.sm_client_day_plan.cid == cid) & (db.sm_client_day_plan.rep_id == rep_id) & (db.sm_client_day_plan.first_date == first_date)& (db.sm_client_day_plan.status == 'Done')).update(status = 'Submitted')
#         
#         updateStatusDoctor=db((db.sm_doctor_day_plan.cid == cid) & (db.sm_doctor_day_plan.rep_id == rep_id) & (db.sm_doctor_day_plan.first_date == first_date)& (db.sm_doctor_day_plan.status == 'Done')).update(status = 'Submitted')
# #         return db._lastsql
# 
#         return 'Success'
    
    
def tourSave():
    retStatus = ''
    
    cid=session.cid
    rep_id=session.rep_id
    password=session.password
    
    monthPass=session.monthPass
    DateTour=session.DateTour
    
    submitStrMorning=str(request.vars.submitStrMorning).strip()
    submitStrEvening=str(request.vars.submitStrEvening).strip()
    
    errorFlag=1
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.user_type,db.sm_rep.name, limitby=(0, 1))
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = repRow[0].user_type
        rep_name = repRow[0].name
        
        errorFlag=0
        
    
    
    if errorFlag==0:
        submitStrMorningList=submitStrMorning.split('<rd>')
#         return submitStrMorning
        tourArrayList = []
        
        i=0
        while i < len(submitStrMorningList)-1:
            submitStrMorningListSingle=submitStrMorningList[i]
            mSingleList=submitStrMorningListSingle.split('<fd>')
            i=i+1
            schedule_date=str(DateTour).split('-')[0]+'-'+str(DateTour).split('-')[1]+'-'+str(i)
            first_date=str(DateTour).split('-')[0]+'-'+str(DateTour).split('-')[1]+'-01'
            
            
            
            m=0
#             return len(mSingleList)
            while m < len(mSingleList):
                
                route_nameG=mSingleList[m].replace('undefined','').split('<fd>')[0]
                
                if route_nameG!='':
#                     return route_nameG
                    route_name=route_nameG.split('|')[1]
                    route_id=route_nameG.split('|')[0]
                    
#                     route_name=''
#                     route_id=route_nameG
                    
                    ins_dict = {'cid':cid, 'rep_id':rep_id,'rep_name':rep_name, 'first_date':first_date, 'schedule_date':schedule_date, 'route_id':route_id, 'route_name':route_name, 'note':'Morning','status':'Draft','field2':session.userdepth}
                    tourArrayList.append(ins_dict)
#                     insStr="update sm_doctor_visit_plan p,sm_level l set p.route_name=l.level_name where  p.rep_id=rep_id and p.first_date=first_date and l.cid=p.cid and l.level_id = p.route_id and p.route_name=''"
#                     insRun=db.executesql(insStr)
                m=m+1
    
        
        
        
        submitStrEveningList=submitStrEvening.split('<rd>')
        i=0
        while i < len(submitStrEveningList)-1:
            submitStrEveningListSingle=submitStrEveningList[i]
            mSingleList=submitStrEveningListSingle.split('<fd>')
            i=i+1
            schedule_date=str(DateTour).split('-')[0]+'-'+str(DateTour).split('-')[1]+'-'+str(i)
            first_date=str(DateTour).split('-')[0]+'-'+str(DateTour).split('-')[1]+'-01'
            
            
            
            m=0
#             return len(mSingleList)
            while m < len(mSingleList):
                
                route_nameG=mSingleList[m].split('<fd>')[0]
#                 return route_nameG
                if route_nameG!='':
                    route_name=route_nameG.split('|')[1]
                    route_id=route_nameG.split('|')[0]
                    
#                     route_name=''
#                     route_id=route_nameG
                    
                    ins_dict = {'cid':cid, 'rep_id':rep_id, 'first_date':first_date, 'schedule_date':schedule_date, 'route_id':route_id, 'route_name':route_name, 'note':'Evening','status':'Draft','field2':session.userdepth}
                    tourArrayList.append(ins_dict)
                m=m+1
        if len(tourArrayList) > 0:
            delete_doc_area=db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id) & (db.sm_doctor_visit_plan.first_date == first_date)).delete()
            db.sm_doctor_visit_plan.bulk_insert(tourArrayList)
            
            insStr="update sm_doctor_visit_plan p,sm_level l set p.route_name=l.level_name where  p.rep_id=rep_id and p.first_date=first_date and l.cid=p.cid and l.level_id = p.route_id and p.route_name=''"
            insRun=db.executesql(insStr)
            return 'Success' 



def tourShowSup_web():
        
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    session.cid=cid
    session.repTour=rep_id
    
    if rep_id=='NONE':
        rep_id = str(request.args[0])
        cid = str(request.args[1])
        session.repTour=rep_id
                    
    DateTour=str(first_currentDate).split(' ')[0]

    
#     draft_info_sup = db((db.sm_doctor_visit_plan.cid==cid)  &(db.sm_doctor_visit_plan.rep_id==session.rep_id) & (db.sm_doctor_visit_plan.first_date==DateTour)).select(db.sm_doctor_visit_plan.status, orderby=db.sm_doctor_visit_plan.id,limitby=(0,1))
#     status='Draft'   
#     if draft_info_sup:
#         status=draft_info[0].status   

#     return str(rep_id)+'  '+str(cid)+'  '+str(DateTour)

    tourThisMorning = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id) & (db.sm_doctor_visit_plan.first_date == DateTour) & (db.sm_doctor_visit_plan.note == 'Morning') & ((db.sm_doctor_visit_plan.status == 'Confirmed') | (db.sm_doctor_visit_plan.status == 'Submitted'))).select(db.sm_doctor_visit_plan.ALL,orderby=db.sm_doctor_visit_plan.schedule_date)    

    tourThisEvening = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id) & (db.sm_doctor_visit_plan.first_date == DateTour) & (db.sm_doctor_visit_plan.note == 'Evening') & ((db.sm_doctor_visit_plan.status == 'Confirmed') | (db.sm_doctor_visit_plan.status == 'Submitted'))).select(db.sm_doctor_visit_plan.ALL,orderby=db.sm_doctor_visit_plan.schedule_date)


#     tourNext = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id) & (db.sm_doctor_visit_plan.first_date == DateTourNext) ).select(db.sm_doctor_visit_plan.ALL,orderby=db.sm_doctor_visit_plan.schedule_date)
    
    strThisMorning=''
    s_datePast=''
    T_status=''
    
    for tourThisMorning in tourThisMorning:
        s_date=str(tourThisMorning.schedule_date)
        route_id=str(tourThisMorning.route_id)
        routeName=str(tourThisMorning.route_name)        
        T_status=str(tourThisMorning.status)
        sDate=s_date

        
        if ((T_status=='Confirmed') or (T_status=='Submitted')):                        
            
            docStr='Doctor'
            clStr='Client'
            frStr='Farm'       
            
            rowDoctor = db((db.sm_doctor_day_plan.cid==cid)  &(db.sm_doctor_day_plan.rep_id==rep_id) & (db.sm_doctor_day_plan.area_id==route_id) & (db.sm_doctor_day_plan.plan_date==sDate)  &(db.sm_doctor_day_plan.visit_time=='Morning') ).select(db.sm_doctor_day_plan.doc_name,db.sm_doctor_day_plan.doc_id, orderby=db.sm_doctor_day_plan.doc_name)
            
            for rowDoctor in rowDoctor:
                docInfo = str(rowDoctor.doc_name)+'-'+str(rowDoctor.doc_id)                 
                docStr=docStr+docInfo+','        
                
            
            rowClient = db((db.sm_client_day_plan.cid==cid)  &(db.sm_client_day_plan.rep_id==rep_id) & (db.sm_client_day_plan.area_id==route_id) & (db.sm_client_day_plan.plan_date==sDate)  &(db.sm_client_day_plan.visit_time=='Morning') ).select(db.sm_client_day_plan.client_name,db.sm_client_day_plan.client_id, orderby=db.sm_client_day_plan.client_name)
            for rowClient in rowClient:
                clInfo = str(rowClient.client_name)+'-'+str(rowClient.client_id) 
                clStr=clStr+clInfo+','
            
            
            rowFarm = db((db.sm_farm_day_plan.cid==cid)  &(db.sm_farm_day_plan.rep_id==session.rep_id) & (db.sm_farm_day_plan.area_id==route_id) & (db.sm_farm_day_plan.plan_date==sDate)  &(db.sm_farm_day_plan.visit_time=='Evening') ).select(db.sm_farm_day_plan.farm_name,db.sm_farm_day_plan.farm_id, orderby=db.sm_farm_day_plan.farm_name)
            for rowFarm in rowFarm:
                frInfo = str(rowFarm.farm_name)+'-'+str(rowFarm.farm_id) 
                frStr=frStr+frInfo+','
               
            routeShow=routeName+'|'+route_id+' '+docStr+' '+clStr+' '+frStr
            
        else:
            routeShow=routeName+'|'+route_id+' '+docStr+' '+clStr+' '+frStr
            
        if s_date!=s_datePast:
            strThisMorning=strThisMorning+'<rd>'+s_date
            
        strThisMorning=strThisMorning+routeShow+','
        s_datePast=s_date

#         return strThisMorning
    
    strThisEvening=''
    s_datePast=''
    for tourThisEvening in tourThisEvening:
        
        s_date=str(tourThisEvening.schedule_date)
        route_id=str(tourThisEvening.route_id)
        routeName=str(tourThisEvening.route_name)
        routeShow=routeName+'|'+route_id
        sDate=s_date
        
        if ((T_status=='Confirmed') or (T_status=='Submitted')):  
            
            docStrE='Doctor'
            clStrE='Client'
            frStrE='Farm' 
            
            rowDoctorE = db((db.sm_doctor_day_plan.cid==cid)  &(db.sm_doctor_day_plan.rep_id==rep_id) & (db.sm_doctor_day_plan.area_id==route_id) & (db.sm_doctor_day_plan.plan_date==sDate)  &(db.sm_doctor_day_plan.visit_time=='Evening') ).select(db.sm_doctor_day_plan.doc_name,db.sm_doctor_day_plan.doc_id, orderby=db.sm_doctor_day_plan.doc_name)
#             return rowDoctorE
            for rowDoctorE in rowDoctorE:
                docInfoE = str(rowDoctorE.doc_name)+'-'+str(rowDoctorE.doc_id) 
                docStrE=docStrE+docInfoE+','
                

            
            rowClientE = db((db.sm_client_day_plan.cid==cid)  &(db.sm_client_day_plan.rep_id==rep_id) & (db.sm_client_day_plan.area_id==route_id) & (db.sm_client_day_plan.plan_date==sDate)  &(db.sm_client_day_plan.visit_time=='Evening') ).select(db.sm_client_day_plan.client_name,db.sm_client_day_plan.client_id, orderby=db.sm_client_day_plan.client_name)

            for rowClientE in rowClientE:
                clInfoE = str(rowClientE.client_name)+'-'+str(rowClientE.client_id) 
                clStrE=clStrE+clInfoE+','
               
            rowFarmE = db((db.sm_farm_day_plan.cid==cid)  &(db.sm_farm_day_plan.rep_id==session.rep_id) & (db.sm_farm_day_plan.area_id==route_id) & (db.sm_farm_day_plan.plan_date==sDate)  &(db.sm_farm_day_plan.visit_time=='Evening') ).select(db.sm_farm_day_plan.farm_name,db.sm_farm_day_plan.farm_id, orderby=db.sm_farm_day_plan.farm_name)
            
            for rowFarmE in rowFarmE:
                frInfoE = str(rowFarmE.farm_name)+'-'+str(rowFarmE.farm_id) 
                frStrE=frStrE+frInfoE+','
#                 return frStrE
            
            routeShowE=routeName+'|'+route_id+' '+docStrE+' '+clStrE+' '+frStrE
            
        else:
            routeShowE=routeName+'|'+route_id+' '+docStrE+' '+clStrE+' '+frStrE
                 
        
        if s_date!=s_datePast:
            strThisEvening=strThisEvening+'<rd>'+s_date
            
        strThisEvening=strThisEvening+routeShowE+','
        s_datePast=s_date


    monthGet=str(DateTour).split('-')[1]
    yearGet=str(DateTour).split('-')[0]
    
    month=int(monthGet)
    year=int(yearGet)
    monthDay=0
    days_month=0
    days_month= days_in_month(year, month)
    
    monthShow= month_name(month)
#     return strThisEvening
    return dict(strThisMorning=strThisMorning,strThisEvening=strThisEvening,days_month=days_month,monthShow=monthShow,T_status=T_status)
    
    
   

def tourShowSup_webNext():
    
    cid=session.cid
    rep_id=session.repTour
        
    Dcheck=int(str(current_date).split('-')[2].split(' ')[0])-2
    todayDate = datetime.date.today()
#         return Dcheck
    if (todayDate - todayDate.replace(day=1)).days > Dcheck:
        
        x= todayDate + datetime.timedelta(25)
        x.replace(day=1)
        
        nextMaont = str(x)
    else:
        nextMaont= todayDate.replace(day=1)
    DateTourNext= nextMaont.split('-')[0]+'-'+nextMaont.split('-')[1]+'-01'
    
#     DateTour=DateTourNext    
        
#     return DateTourNext    
    
#     return cid
    tourThisMorning = db( (db.sm_doctor_visit_plan.rep_id == rep_id) & (db.sm_doctor_visit_plan.first_date == DateTourNext)& (db.sm_doctor_visit_plan.note == 'Morning') & ((db.sm_doctor_visit_plan.status == 'Confirmed') | (db.sm_doctor_visit_plan.status == 'Submitted'))).select(db.sm_doctor_visit_plan.ALL,orderby=db.sm_doctor_visit_plan.schedule_date)
    tourThisEvening = db( (db.sm_doctor_visit_plan.rep_id == rep_id) & (db.sm_doctor_visit_plan.first_date == DateTourNext)& (db.sm_doctor_visit_plan.note == 'Evening') & ((db.sm_doctor_visit_plan.status == 'Confirmed') | (db.sm_doctor_visit_plan.status == 'Submitted'))).select(db.sm_doctor_visit_plan.ALL,orderby=db.sm_doctor_visit_plan.schedule_date)
#     return tourThisMorning
#     return tourThisMorning
#     return DateTour
#     tourNext = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id) & (db.sm_doctor_visit_plan.first_date == DateTourNext) ).select(db.sm_doctor_visit_plan.ALL,orderby=db.sm_doctor_visit_plan.schedule_date)
    
    strThisMorning=''
    s_datePast=''
    T_status=''
    for tourThisMorning in tourThisMorning:
        s_date=str(tourThisMorning.schedule_date)
        route_id=str(tourThisMorning.route_id)
        routeName=str(tourThisMorning.route_name)
        T_status=str(tourThisMorning.status)
        sDate=s_date
        
        if ((T_status=='Confirmed') or (T_status=='Submitted')): 
        
            docStr='Doctor'
            clStr='Client'
            frStr='Farm'  
            
            rowDoctor = db((db.sm_doctor_day_plan.rep_id==rep_id) & (db.sm_doctor_day_plan.area_id==route_id) & (db.sm_doctor_day_plan.plan_date==sDate)  &(db.sm_doctor_day_plan.visit_time=='Morning') ).select(db.sm_doctor_day_plan.doc_name,db.sm_doctor_day_plan.doc_id, orderby=db.sm_doctor_day_plan.doc_name)
            #         return rowDoctor
            for rowDoctor in rowDoctor:
                docInfo = str(rowDoctor.doc_name)+'-'+str(rowDoctor.doc_id) 
                docStr=docStr+docInfo+','        
            
            rowClient = db((db.sm_client_day_plan.rep_id==rep_id) & (db.sm_client_day_plan.area_id==route_id) & (db.sm_client_day_plan.plan_date==sDate)  &(db.sm_client_day_plan.visit_time=='Morning') ).select(db.sm_client_day_plan.client_name,db.sm_client_day_plan.client_id, orderby=db.sm_client_day_plan.client_name)
            for rowClient in rowClient:
                clInfo = str(rowClient.client_name)+'-'+str(rowClient.client_id) 
                clStr=clStr+clInfo+','
            
            rowFarm = db((db.sm_farm_day_plan.cid==cid)  &(db.sm_farm_day_plan.rep_id==session.rep_id) & (db.sm_farm_day_plan.area_id==route_id) & (db.sm_farm_day_plan.plan_date==sDate)  &(db.sm_farm_day_plan.visit_time=='Evening') ).select(db.sm_farm_day_plan.farm_name,db.sm_farm_day_plan.farm_id, orderby=db.sm_farm_day_plan.farm_name)
            for rowFarm in rowFarm:
                frInfo = str(rowFarm.farm_name)+'-'+str(rowFarm.farm_id)
                frStr=frStr+frInfo+','
            
            routeShow=routeName+'|'+route_id+' '+docStr+' '+clStr+' '+frStr
        
        else:
            routeShow=routeName+'|'+route_id+' '+docStr+' '+clStr+' '+frStr
        
        
        if s_date!=s_datePast:
            strThisMorning=strThisMorning+'<rd>'+s_date
        
        strThisMorning=strThisMorning+routeShow+','
        s_datePast=s_date
#     return strThisMorning
    
    
    strThisEvening=''
    s_datePast=''
    for tourThisEvening in tourThisEvening:
        s_date=str(tourThisEvening.schedule_date)
        route_id=str(tourThisEvening.route_id)
        routeName=str(tourThisEvening.route_name)
        routeShow=routeName+'|'+route_id
        sDate=s_date
        
        if ((T_status=='Confirmed') or (T_status=='Submitted')): 
        
            docStrE='Doctor'
            clStrE='Client'
            frStrE='Farm' 
            rowDoctor = db((db.sm_doctor_day_plan.rep_id==rep_id) & (db.sm_doctor_day_plan.area_id==route_id) & (db.sm_doctor_day_plan.plan_date==sDate)  &(db.sm_doctor_day_plan.visit_time=='Evening') ).select(db.sm_doctor_day_plan.doc_name,db.sm_doctor_day_plan.doc_id, orderby=db.sm_doctor_day_plan.doc_name)

            for rowDoctor in rowDoctor:
                docInfo = str(rowDoctor.doc_name)+'-'+str(rowDoctor.doc_id) 
                docStrE=docStrE+docInfo+','

            
            rowClient = db((db.sm_client_day_plan.rep_id==rep_id) & (db.sm_client_day_plan.area_id==route_id) & (db.sm_client_day_plan.plan_date==sDate)  &(db.sm_client_day_plan.visit_time=='Evening') ).select(db.sm_client_day_plan.client_name,db.sm_client_day_plan.client_id, orderby=db.sm_client_day_plan.client_name)
            for rowClient in rowClient:
                clInfo = str(rowClient.client_name)+'-'+str(rowClient.client_id) 
                clStrE=clStrE+clInfo+','
                
            rowFarmE = db((db.sm_farm_day_plan.cid==cid)  &(db.sm_farm_day_plan.rep_id==session.rep_id) & (db.sm_farm_day_plan.area_id==route_id) & (db.sm_farm_day_plan.plan_date==sDate)  &(db.sm_farm_day_plan.visit_time=='Evening') ).select(db.sm_farm_day_plan.farm_name,db.sm_farm_day_plan.farm_id, orderby=db.sm_farm_day_plan.farm_name)
            
            for rowFarmE in rowFarmE:
                frInfoE = str(rowFarmE.farm_name)+'-'+str(rowFarmE.farm_id) 
                frStrE=frStrE+frInfoE+','

            
            routeShowE=routeName+'|'+route_id+' '+docStrE+' '+clStrE+' '+frStrE
        
        else:
            routeShowE=routeName+'|'+route_id+' '+docStrE+' '+clStrE+' '+frStrE
        
        if s_date!=s_datePast:
            strThisEvening=strThisEvening+'<rd>'+s_date
        
        strThisEvening=strThisEvening+routeShowE+','
        s_datePast=s_date
        
        
        
    monthGet=str(DateTourNext).split('-')[1]
    yearGet=str(DateTourNext).split('-')[0]
    setDateG=str(yearGet)+'-'+str(monthGet)
    
    month=int(monthGet)
    year=int(yearGet)
    monthDay=0
    days_month=0
    days_month= days_in_month(year, month)
    
    monthShow= month_name(month)
    
    return dict(strThisMorning=strThisMorning,strThisEvening=strThisEvening,days_month=days_month,monthShow=monthShow,DateTourNext=DateTourNext,T_status=T_status,setDateG=setDateG)
    
    
    
def tourAccept():
#     cid=session.cid
    rep_id=session.repTour
    Month_get = str(request.vars.mothAcc).strip()
    thisM_fdate=str(first_currentDate).split(' ')[0]
    
    if Month_get=='Next':
        Dcheck=1
        todayDate = datetime.date.today()
        todayDate = datetime.date.today()  
        x= todayDate + datetime.timedelta(25)
        x.replace(day=1)
        
        nextMaont = str(x)
        thisM_fdate=str(nextMaont).split('-')[0]+'-'+str(nextMaont).split('-')[1]+'-01'
#     return thisM_fdate
#     return rep_id
    tourThisEvening = db( (db.sm_doctor_visit_plan.rep_id == rep_id) & (db.sm_doctor_visit_plan.first_date == thisM_fdate)& (db.sm_doctor_visit_plan.status == 'Submitted')).update(status='Confirmed')
#     tourThisEvening=db( (db.sm_doctor_visit_plan.rep_id == rep_id) & (db.sm_doctor_visit_plan.first_date == thisM_fdate)).select(db.sm_doctor_visit_plan.ALL)
#     return tourThisEvening
    tourThisClient = db( (db.sm_client_day_plan.rep_id == rep_id) & (db.sm_client_day_plan.first_date == thisM_fdate) & (db.sm_client_day_plan.status == 'Submitted')).update(status='Confirmed')
    tourThisDoctor = db( (db.sm_doctor_day_plan.rep_id == rep_id) & (db.sm_doctor_day_plan.first_date == thisM_fdate)& (db.sm_doctor_day_plan.status == 'Submitted')).update(status='Confirmed')
    
    
    return 'Success'
    
    
     
  
def tourReject():
    cid=session.cid
    rep_id=session.repTour
    thisM_fdate=str(first_currentDate).split(' ')[0]
    Month_get = str(request.vars.mothAcc).strip()
    
    if Month_get=='Next':
        Dcheck=1
        todayDate = datetime.date.today()
        todayDate = datetime.date.today()  
        x= todayDate + datetime.timedelta(25)
        x.replace(day=1)
        
        nextMaont = str(x)
        thisM_fdate=str(nextMaont).split('-')[0]+'-'+str(nextMaont).split('-')[1]+'-01'
    
    tourThisEvening = db((db.sm_doctor_visit_plan.rep_id == rep_id) & (db.sm_doctor_visit_plan.first_date == thisM_fdate)& (db.sm_client_day_plan.status == 'Submitted')).update(status='Draft')
    tourThisClient = db((db.sm_client_day_plan.rep_id == rep_id) & (db.sm_client_day_plan.first_date == thisM_fdate) & (db.sm_client_day_plan.status == 'Submitted')).update(status='Draft')
    tourThisDoctor = db((db.sm_doctor_day_plan.rep_id == rep_id) & (db.sm_doctor_day_plan.first_date == thisM_fdate)& (db.sm_doctor_day_plan.status == 'Submitted')).update(status='Draft')
    
    
    
    return 'Success'
    
    
    
    
    
    
    
    
#  ==========================Nazma==========================   
    
#  http://127.0.0.1:8000/kpl/tour_web/kpl_visit_details?cid=kpl&uid=A036&u_pass=123&report_person=123


# http://127.0.0.1:8000/kpl/tour_web/kpl_visit_details?cid=kpl&uid=F0259&u_pass=1234&report_person=123

def kpl_visit_details():
    response.title = 'Show Map'

    
    cid=session.cid
    uid=session.uid
    password=session.password

    check_Rows=db((db.sm_rep.cid==cid) & (db.sm_rep.rep_id==uid)  & (db.sm_rep.password==password)  & (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.user_type,limitby=(0,1))
#     return db._lastsql
    if check_Rows:
        rep_id=check_Rows[0].rep_id
        name=check_Rows[0].name
        user_type=check_Rows[0].user_type
        
        session.user_id = rep_id
        session.user_name = name
        session.user_type = user_type

    if session.user_type == 'rep' :
        pass
    
    else:
        level_idList=[]
        depthList=[]        
        levelList=[]
        
        supLevelRows=db((db.sm_supervisor_level.cid==cid) & (db.sm_supervisor_level.sup_id==uid)).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no,limitby=(0,1))
#         return supLevelRows
        for supRow in supLevelRows:
            level_id=supRow.level_id
            depthNo=supRow.level_depth_no
            level_idList.append(level_id)            
            level = 'level' + str(depthNo)

#             level_dcr = 'level' + str(depthNo)+'_id'
            
#             return level

            areaList=[]

#             Nadira Apu below sql
#             levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_id)).select(db.sm_level.level_id, orderby=db.sm_level.level_id,limitby=(0,1))
            levelRows = db((db.sm_level.cid == cid) & (db.sm_level.parent_level_id.belongs(level_idList) )).select(db.sm_level.level_id, orderby=db.sm_level.level_id)

#             return db._lastsql
            for levelRow in levelRows:
                territoryid = levelRow.level_id            
                areaList.append(territoryid)

#             User Details Start

#             return areaList
            qset_user_dcr = db()
            qset_user_dcr = qset_user_dcr(db.sm_doctor_visit.cid == cid)
            qset_user_dcr = qset_user_dcr(db.sm_doctor_visit.rep_id == uid)
            qset_user_dcr = qset_user_dcr(db.sm_doctor_visit.route_id.belongs(areaList))
            order_head_user_dcr_records = qset_user_dcr.count()


            qset_user_rx = db()
            qset_user_rx = qset_user_rx(db.sm_prescription_head.cid == cid)
            qset_user_rx = qset_user_rx(db.sm_prescription_head.submit_by_id == uid)
            qset_user_rx = qset_user_rx(db.sm_prescription_head.area_id.belongs(areaList))
#             order_head_user_records = qset_user.select(db.sm_order_head.id.count(), orderby=db.sm_order_head.id)
            order_head_user_rx_records = qset_user_rx.count()



            qset_user = db()
            qset_user = qset_user(db.sm_order_head.cid == cid)
            qset_user = qset_user(db.sm_order_head.rep_id == uid)
            qset_user = qset_user(db.sm_order_head.area_id.belongs(areaList))
#             order_head_user_records = qset_user.select(db.sm_order_head.id.count(), orderby=db.sm_order_head.id)
            order_head_user_records = qset_user.count()




            qset_user_detail = db()
            qset_user_detail = qset_user_detail(db.sm_order.cid == cid)
            qset_user_detail = qset_user_detail(db.sm_order.rep_id == uid)
            qset_user_detail = qset_user_detail(db.sm_order.area_id.belongs(areaList))
            order_user_detail_records = qset_user_detail.select((db.sm_order.quantity*db.sm_order.price).sum(), orderby=db.sm_order.id)



#             Team Details Start



            qset_team_dcr = db()
            qset_team_dcr = qset_team_dcr(db.sm_doctor_visit.cid == cid)
            qset_team_dcr = qset_team_dcr(db.sm_doctor_visit.rep_id != uid)
            qset_team_dcr = qset_team_dcr(db.sm_doctor_visit.route_id.belongs(areaList))
            order_head_team_dcr_records = qset_team_dcr.count()





            qset_team_rx = db()
            qset_team_rx = qset_team_rx(db.sm_prescription_head.cid == cid)
            qset_team_rx = qset_team_rx(db.sm_prescription_head.submit_by_id != uid)
            qset_team_rx = qset_team_rx(db.sm_prescription_head.area_id.belongs(areaList))
#             order_head_user_records = qset_user.select(db.sm_order_head.id.count(), orderby=db.sm_order_head.id)
            order_head_team_rx_records = qset_team_rx.count()


                
            qset = db()
            qset = qset(db.sm_order_head.cid == cid)    
            qset = qset(db.sm_order_head.rep_id != uid)
            qset = qset(db.sm_order_head.area_id.belongs(areaList))
#             order_head_records = qset.select(db.sm_order_head.id.count(), orderby=db.sm_order_head.id)
            order_head_records = qset.count()

            qset_detail = db()
            qset_detail = qset_detail(db.sm_order.cid == cid)    
            qset_detail = qset_detail(db.sm_order.rep_id != uid)
            qset_detail = qset_detail(db.sm_order.area_id.belongs(areaList))
            order_detail_records = qset_detail.select((db.sm_order.quantity*db.sm_order.price).sum(), orderby=db.sm_order.id)
#             return db._lastsql
#             return order_detail_records

            return dict(order_head_user_dcr_records=order_head_user_dcr_records,order_head_user_records=order_head_user_records, order_user_detail_records=order_user_detail_records, order_head_user_rx_records=order_head_user_rx_records,order_head_records=order_head_records,order_detail_records=order_detail_records,order_head_team_rx_records=order_head_team_rx_records,order_head_team_dcr_records=order_head_team_dcr_records)




# http://127.0.0.1:8000/kpl/tour_web/kpl_all_member_visit_details?cid=kpl&uid=A036&u_pass=123&report_person=123


#latest below
# 127.0.0.1:8000/kpl/tour_web/kpl_all_member_visit_details?cid=kpl&uid=A037&u_pass=1234&report_person=123


def teamShow_web():
    response.title = 'Visit Details'

    cid = request.vars.cid
    session.cid = cid
    uid = request.vars.rep_id
    session.uid = uid    
    password = request.vars.rep_pass
    session.password = password    


    check_Rows=db((db.sm_rep.cid==cid) & (db.sm_rep.rep_id==uid)  & (db.sm_rep.password==password)  & (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.user_type,limitby=(0,1))
#     return db._lastsql
    if check_Rows:
        rep_id=check_Rows[0].rep_id
        name=check_Rows[0].name
        user_type=check_Rows[0].user_type
        
        session.user_id = rep_id
        session.user_name = name
        session.user_type = user_type

    if session.user_type == 'rep' :
        pass
    
    else:
        level_idList=[]
        depthList=[]        
        levelList=[]
        
        supLevelRows=db((db.sm_supervisor_level.cid==cid) & (db.sm_supervisor_level.sup_id==uid)).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no)
#         return supLevelRows
        for supRow in supLevelRows:
            level_id=supRow.level_id
            depthNo=supRow.level_depth_no
#             return depthNo
            level_idList.append(level_id)
            depthList.append(depthNo)
            
            level = 'level' + str(depthNo)
            



        areaList=[]
        levelRows = db((db.sm_level.cid == cid) & (db.sm_level.parent_level_id.belongs(level_idList) )).select(db.sm_level.level_id, orderby=db.sm_level.level_id)
#             return levelRows
#             return db._lastsql
        for levelRow in levelRows:
            territoryid = levelRow.level_id            
            areaList.append(territoryid)

        rsm_Rows = db((db.sm_supervisor_level.cid == cid)  &  (db.sm_supervisor_level.level_id.belongs(areaList) )).select(db.sm_supervisor_level.sup_id, db.sm_supervisor_level.sup_name, orderby=db.sm_supervisor_level.sup_id)
        am_Rows=''
#             return db._lastsql
        return dict(am_Rows=am_Rows,rsm_Rows=rsm_Rows)


def amndShow_web():    
    import datetime 
    retStatus = ''
    
    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()
    password = str(request.vars.rep_pass).strip()    
    monthPass = str(request.vars.monthPass).strip()    
    session.cid = cid
    session.rep_id = rep_id
    session.password = password    
    session.monthPass = monthPass
    
    if (session.monthPass=='This'):
        checkDate=first_currentDate
    else:
        Dcheck=int(str(current_date).split('-')[2].split(' ')[0])-2
        todayDate = datetime.date.today()

        if (todayDate - todayDate.replace(day=1)).days > Dcheck:
            x= todayDate + datetime.timedelta(25)
            x.replace(day=1)
            
            checkDate1 = str(x)
        else:
            checkDate1= todayDate.replace(day=1)
        checkDate=checkDate1.split('-')[0]+'-'  +checkDate1.split('-')[1]  +'-01'

  
    userSin=''
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.user_type,db.sm_rep.note, limitby=(0, 1))
#     return repRow
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = repRow[0].user_type
        userSin=repRow[0].note
        
    draft_info = db((db.sm_doctor_visit_plan.cid==cid)  &(db.sm_doctor_visit_plan.rep_id==session.rep_id) & (db.sm_doctor_visit_plan.first_date==checkDate)).select(db.sm_doctor_visit_plan.status, orderby=db.sm_doctor_visit_plan.id,limitby=(0,1))

    status='Draft'
    
    if draft_info:
        status=draft_info[0].status
    strValueMorning=''    

        
    strValueMorning=''
    draft_infoAll = db((db.sm_doctor_visit_plan.cid==cid)  &(db.sm_doctor_visit_plan.rep_id==session.rep_id) & (db.sm_doctor_visit_plan.first_date==checkDate)  & (db.sm_doctor_visit_plan.status==status) &((db.sm_doctor_visit_plan.note=='Morning') | (db.sm_doctor_visit_plan.note==''))).select(db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.schedule_date, orderby=db.sm_doctor_visit_plan.id)
#         return db._lastsql
    for draft_infoAll in draft_infoAll:
        route_name = draft_infoAll.route_name   
        sDate=str(draft_infoAll.schedule_date)
        strValueMorning=strValueMorning+'<'+sDate+'>'+route_name
        
    strValueMorningE=''
    draft_infoAllE = db((db.sm_doctor_visit_plan.cid==cid)  &(db.sm_doctor_visit_plan.rep_id==session.rep_id) & (db.sm_doctor_visit_plan.first_date==checkDate) & (db.sm_doctor_visit_plan.status==status)&(db.sm_doctor_visit_plan.note=='Evening')).select(db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.schedule_date, orderby=db.sm_doctor_visit_plan.id)
#         return db._lastsql
    for draft_infoAllE in draft_infoAllE:
        route_name = draft_infoAllE.route_name   
        sDate=str(draft_infoAllE.schedule_date)
        
        strValueMorningE=strValueMorningE+'<'+sDate+'>'+route_name
               
#     return strValueMorningE

# =================startamd==============

    if userSin=='SIN':
        if user_type=='rep':
            session.userType='rep'
            userdepth=3
            repareaList=[]
            marketTourRows = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.rep_id == rep_id)).select(db.sm_rep_area.area_id, db.sm_rep_area.area_name, orderby=db.sm_rep_area.area_name, groupby=db.sm_rep_area.area_id)

            session.userdepth = userdepth
        else:
            session.userType='sup'
            marketTourRows1 = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id)).select(db.sm_supervisor_level.level_id , db.sm_supervisor_level.level_name , db.sm_supervisor_level.level_depth_no,orderby=db.sm_supervisor_level.level_name, groupby=db.sm_supervisor_level.level_id)
            areaList=[]
            for marketRowmarketTourRows1 in marketTourRows1:
                session.userdepth = marketRowmarketTourRows1.level_depth_no
                level='level'+str(marketRowmarketTourRows1.level_depth_no)+'_id'
                areaList.append(marketRowmarketTourRows1.level_id)
                supLevel='level'+str(session.userdepth)
            if int(session.userdepth)>0:
                marketTourRows=db((db.sm_level.cid == cid)& (db.sm_level.is_leaf == '1') & (db.sm_level[supLevel].belongs(areaList)) ).select(db.sm_level.level_id,db.sm_level.level_name,orderby=db.sm_level.level_id)
    
            else:
                marketTourRows=db((db.sm_level.cid == cid)& (db.sm_level.depth == '1') & (db.sm_level[supLevel].belongs(areaList)) ).select(db.sm_level.level_id,db.sm_level.level_name,orderby=db.sm_level.level_id)
                     
    
    else:     
        if user_type=='rep':
            session.userType='rep'
            userdepth=3
            repareaList=[]
            marketRows = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.rep_id == rep_id)).select(db.sm_rep_area.area_id, db.sm_rep_area.area_name, orderby=db.sm_rep_area.area_name, groupby=db.sm_rep_area.area_id)
            for marketRow in marketRows:
                area_id = marketRow.area_id
                area_name = marketRow.area_name
                repareaList.append(area_id)
            marketTourRows = db((db.sm_microunion.cid==cid)  &(db.sm_microunion.area_id.belongs(repareaList))).select(db.sm_microunion.microunion_id,db.sm_microunion.microunion_name, orderby=db.sm_microunion.microunion_name, groupby=db.sm_microunion.microunion_id|db.sm_microunion.microunion_name)
            session.userdepth = userdepth
        else:
            session.userType='sup'
            marketTourRows1 = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id)).select(db.sm_supervisor_level.level_id , db.sm_supervisor_level.level_name , db.sm_supervisor_level.level_depth_no,orderby=db.sm_supervisor_level.level_name, groupby=db.sm_supervisor_level.level_id)
            areaList=[]
            for marketRowmarketTourRows1 in marketTourRows1:
                session.userdepth = marketRowmarketTourRows1.level_depth_no
                level='level'+str(marketRowmarketTourRows1.level_depth_no)+'_id'
                areaList.append(marketRowmarketTourRows1.level_id)
                supLevel='level'+str(session.userdepth)
            if int(session.userdepth)>0:
                marketTourRows=db((db.sm_level.cid == cid)& (db.sm_level.is_leaf == '1') & (db.sm_level[supLevel].belongs(areaList)) ).select(db.sm_level.level_id,db.sm_level.level_name,orderby=db.sm_level.level_id)
    
            else:
                marketTourRows=db((db.sm_level.cid == cid)& (db.sm_level.depth == '1') & (db.sm_level[supLevel].belongs(areaList)) ).select(db.sm_level.level_id,db.sm_level.level_name,orderby=db.sm_level.level_id)
                     
        
#     ========Next Month
    DateTour=first_currentDate
    
    Dcheck=int(str(current_date).split('-')[2].split(' ')[0])-2
#     return Dcheck
    if monthPass=='Next':
        todayDate = datetime.date.today()
#         return (todayDate - todayDate.replace(day=1)).days
        if (todayDate - todayDate.replace(day=1)).days > Dcheck:
            x= todayDate + datetime.timedelta(25)
            x.replace(day=1)
            
            nextMaont = str(x)
        else:
            nextMaont= todayDate.replace(day=1)
        DateTour= nextMaont
#         return DateTour
    session.DateTour = DateTour
    monthGet=str(DateTour).split('-')[1]
    yearGet=str(DateTour).split('-')[0]
    
    month=int(monthGet)
    year=int(yearGet)
    monthDay=0
    days_month=0
    days_month= days_in_month(year, month)
    
    monthShow=''
    monthShow= month_name(month)
    session.days_month=days_month
    
#     return session.days_month
#  =========================Show Draf or Submitted====================
 
    
    setDateG=str(yearGet)+'-'+str(monthGet)
 
#     return setDateG
#     return marketTourRows 
#     return monthShow
    
    return dict(marketTourRows=marketTourRows,days_month=days_month,monthShow=monthShow,setDateG=setDateG,status=status,strValueMorning=strValueMorning,strValueMorningE=strValueMorningE,userSin=userSin)
    
def amndCheck():
    cid=session.cid 
    rep_id=session.rep_id
    checkDate=str(request.vars.check_date).strip()
    session.checkDate=checkDate
#     return cid
    if checkDate!='':
        strValueMorning=''
        strValueMorningE=''
        draft_infoAll = db((db.sm_doctor_visit_plan.cid==cid)  &(db.sm_doctor_visit_plan.rep_id==session.rep_id) & (db.sm_doctor_visit_plan.schedule_date==checkDate)   &((db.sm_doctor_visit_plan.note=='Morning') | (db.sm_doctor_visit_plan.note==''))).select(db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.status, orderby=db.sm_doctor_visit_plan.id)
#         return db._lastsql
        
        for draft_infoAll in draft_infoAll:
            route_name = draft_infoAll.route_name   
            sDate=str(draft_infoAll.schedule_date)
            if strValueMorning=='':
                strValueMorning=route_name
            else:
                strValueMorning=strValueMorning+','+route_name
            
        strValueMorningE=''
        draft_infoAllE = db((db.sm_doctor_visit_plan.cid==cid)  &(db.sm_doctor_visit_plan.rep_id==session.rep_id) & (db.sm_doctor_visit_plan.schedule_date==checkDate) &(db.sm_doctor_visit_plan.note=='Evening')).select(db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.status, orderby=db.sm_doctor_visit_plan.id)
    #         return db._lastsql
        for draft_infoAllE in draft_infoAllE:
            route_name = draft_infoAllE.route_name   
            sDate=str(draft_infoAllE.schedule_date)
            if strValueMorningE=='':
                strValueMorningE=route_name
            else:
                strValueMorningE=strValueMorningE+','+route_name
        showStr=''
        if strValueMorning!='':
            showStr=showStr+'Morning: '+strValueMorning
        if strValueMorningE!='':
            showStr=showStr+'<br><span style="color:#09F"> Evening: '+strValueMorningE+'</span>'
        return showStr
    else:
        return 'blank'
            
        
def amndSubmit():
    retStatus = ''
#     return 'assf'
    cid=session.cid
    rep_id=session.rep_id
    password=session.password
    
    submitStrMorning=str(request.vars.submitStrMorning).strip()
    submitStrEvening=str(request.vars.submitStrEvening).strip()
    amndDate=request.vars.amndDate
#     return amndDate
    
    schedule_date=amndDate
    
    first_date=str(schedule_date).split('-')[0]+'-'+str(schedule_date).split('-')[1]+'-01'
#     return first_date
    
    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.user_type,db.sm_rep.name, limitby=(0, 1))
#     return repRow
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = repRow[0].user_type
        rep_name = repRow[0].name
        
        
        submitStrMorningList=submitStrMorning.split('<rd>')
        submitStrEveningList=submitStrEvening.split('<rd>')
        tourArrayList = []
        i=0
        errorFlag=0
        current_date_check=int(str(current_date).split('-')[2])
#         return current_date_check
        while i < len(submitStrMorningList)-1:
            submitStrMorningListSingle=submitStrMorningList[i]
            if (session.monthPass=='This'):
                if ((submitStrMorningListSingle=='') and (submitStrEveningList[i]=='') and (current_date_check <= i)):
#                     return i
                    errorFlag=1
            else:
                if ((submitStrMorningListSingle=='') and (submitStrEveningList[i]=='')):
                    errorFlag=1
#                     return i
                
            mSingleList=submitStrMorningListSingle.split('<fd>')
#             return mSingleList 
            i=i+1
            
            m=0
            while m < len(mSingleList):
                
                route_nameG=mSingleList[m]
               
                if route_nameG!='':
                    route_name=''
                    route_id=route_nameG
                    ins_dict = {'cid':cid, 'rep_id':rep_id,'rep_name':rep_name, 'first_date':first_date, 'schedule_date':schedule_date, 'route_id':route_id, 'route_name':route_name, 'note':'Morning','status':'CReq','field2':session.userdepth}
                    tourArrayList.append(ins_dict)
                    
                m=m+1
        
        i=0
        errorFlagEvening=0
        while i < len(submitStrEveningList)-1:
            submitStrEveningListSingle=submitStrEveningList[i]
            
            mSingleList=submitStrEveningListSingle.split('<fd>')
            i=i+1
            
            m=0
            while m < len(mSingleList):
                route_nameG=mSingleList[m]
                if route_nameG!='':
                    route_name=''
                    route_id=route_nameG
                    ins_dict = {'cid':cid, 'rep_id':rep_id,'rep_name':rep_name, 'first_date':first_date, 'schedule_date':schedule_date, 'route_id':route_id, 'route_name':route_name, 'note':'Evening','status':'CReq','field2':session.userdepth}
                    tourArrayList.append(ins_dict)
                m=m+1
        if ((errorFlag==0) ):
                return 'Incomplete'
        if len(tourArrayList) > 0:
            delete_doc_area=db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id) & (db.sm_doctor_visit_plan.schedule_date == schedule_date) & (db.sm_doctor_visit_plan.status == 'CReq')).delete()
            delete_doc_areainsrt=db.sm_doctor_visit_plan.bulk_insert(tourArrayList)
            
            insStr="update sm_doctor_visit_plan p,sm_level l set p.route_name=l.level_name where  p.rep_id=rep_id and p.first_date=first_date and l.cid=p.cid and l.level_id = p.route_id and p.route_name=''"
#             return insStr
            insRun=db.executesql(insStr)
            
            return 'Success'  

        
        
def repPendingCancel_web():
    
    cid = request.vars.cid
    session.cid = cid
    uid = request.vars.rep_id
    session.uid = uid    
    password = request.vars.rep_pass
    session.password = password    
    session.depthNo_user = ''
    pendingfo=''
    check_Rows=db((db.sm_rep.cid==cid) & (db.sm_rep.rep_id==uid)  & (db.sm_rep.password==password)  & (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.user_type,limitby=(0,1))
#     return db._lastsql
    if check_Rows:
        rep_id=check_Rows[0].rep_id
        name=check_Rows[0].name
        user_type=check_Rows[0].user_type        
        session.user_id = rep_id
        session.user_name = name
        session.user_type = user_type
    
    else :
        session.flash='Access is Denied !'
    
    if session.user_type == 'rep' :
        pass
    
    else:
        level_idList=[]
        depthList=[]        
        levelList=[]
        areaList = []
        session.msg_1 = ''
        supLevelRows=db((db.sm_supervisor_level.cid==cid) & (db.sm_supervisor_level.sup_id==uid)).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no)
#         return supLevelRows
        for supRow in supLevelRows:
            level_id=supRow.level_id
            depthNo=supRow.level_depth_no
            session.depthNo_user=depthNo
#             return depthNo
            level_idList.append(level_id)
#             depthList.append(depthNo)
            
#             level = 'level' + str(depthNo)
#         return  session.depthNo   
        
        supLevel='level'+str(depthNo)
        levelRows=db((db.sm_level.cid == cid)& (db.sm_level.is_leaf == '1') & (db.sm_level[supLevel].belongs(level_idList)) ).select(db.sm_level.level_id,orderby=db.sm_level.level_id)

        for levelRow in levelRows:
            territoryid = levelRow.level_id
            areaList.append(territoryid)

        

        pendingfo = db((db.sm_doctor_visit_plan.cid==cid)  &(db.sm_doctor_visit_plan.route_id.belongs(areaList)) & (db.sm_doctor_visit_plan.status=='CReq') &(db.sm_doctor_visit_plan.schedule_date> current_date)).select(db.sm_doctor_visit_plan.rep_id,db.sm_doctor_visit_plan.rep_name,db.sm_doctor_visit_plan.schedule_date, orderby=db.sm_doctor_visit_plan.schedule_date, groupby=db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.schedule_date)
#         return pendingfo
#     for draft_infoAllE in draft_infoAllE:
    
     
    return dict(pendingfo=pendingfo)  

def tourPending():
    rep_id = request.args[0]
    s_date = request.args[1]
    
    pendingfo = db((db.sm_doctor_visit_plan.cid==session.cid)  &(db.sm_doctor_visit_plan.rep_id==rep_id) & (db.sm_doctor_visit_plan.status=='CReq') &(db.sm_doctor_visit_plan.schedule_date== s_date)).select(db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.note, orderby=~db.sm_doctor_visit_plan.note)
    
    return dict(pendingfo=pendingfo,s_date=s_date,rep_id=rep_id)  

def amndApprove():
    rep_id = request.vars.amndRep
    s_date = request.vars.amndDate
    
    deletePPlan = db((db.sm_doctor_visit_plan.cid==session.cid)  &(db.sm_doctor_visit_plan.rep_id==rep_id) & (db.sm_doctor_visit_plan.status=='Confirmed') &(db.sm_doctor_visit_plan.schedule_date== s_date)).delete()
    updatePlan = db((db.sm_doctor_visit_plan.cid==session.cid)  &(db.sm_doctor_visit_plan.rep_id==rep_id) & (db.sm_doctor_visit_plan.status=='CReq') &(db.sm_doctor_visit_plan.schedule_date== s_date)).update(status='Confirmed')
    return 'Success'
    
    
def amndReject():
    rep_id = request.vars.amndRep
    s_date = request.vars.amndDate
    
    
    updatePlan = db((db.sm_doctor_visit_plan.cid==session.cid)  &(db.sm_doctor_visit_plan.rep_id==rep_id) & (db.sm_doctor_visit_plan.status=='CReq') &(db.sm_doctor_visit_plan.schedule_date== s_date)).update(status='Cancelled')
    return 'Success'   


# ==============Shima
def add_day_doc():   

#     territoryCode=request.vars.territoryCode
#     cid=request.vars.cid
#     user=request.vars.user
#     password=request.vars.password
#     session.cid=cid
#     session.user=user
#     session.password=password

    submit_date=request.vars.submit_date
    territory_code=request.vars.territoryCode
    visit_time=request.vars.visit_time
    
    
    
    session.visit_time= visit_time
    session.plan_date= submit_date
    session.territory_code=territory_code
#     return session.territory_code

    recRows=db((db.sm_doctor_area.cid==session.cid) & (db.sm_doctor_area.area_id==territory_code)).select(db.sm_doctor_area.doc_id, db.sm_doctor_area.doc_name,  groupby = db.sm_doctor_area.doc_id, orderby=db.sm_doctor_area.doc_name)
    # return  db._lastsql
    docStr = ''
    for row in recRows:
        doc_id= str(row.doc_id).strip()

        doc_name=str(row.doc_name).strip()

        if docStr=='':
            docStr = str(doc_name) +'|'+ str(doc_id)

        else:
            docStr=docStr+'<rdrd>'+ str(doc_name)+'|'+ str(doc_id)
#     return docStr        
    return dict(docStr=docStr)

def insertDoc():

    cid=session.cid
    user_id=session.rep_id
    password=session.password
    territory_code=session.territory_code
    plan_date=session.plan_date
    visit_time=session.visit_time
#     return plan_date
    docListNew=str(request.vars.docListNew).strip()
#     return docListNew
    doc_single_rt=''
    rep_name= ''
    area_name=''
    first_dateGet=str(plan_date).split('-')[0]+'-'+str(plan_date).split('-')[1]+'-01'
#     return first_dateGet
    if (docListNew=='') :
           
        return 'Failed<rdrd>Please Select Doctor'
      
    else:
#         return territory_code
        repRows=db((db.sm_rep_area.cid==cid)&(db.sm_rep_area.rep_id==user_id)&(db.sm_rep_area.area_id==territory_code)).select(db.sm_rep_area.rep_id,db.sm_rep_area.rep_name,db.sm_rep_area.area_id, db.sm_rep_area.area_name, orderby=db.sm_rep_area.rep_id)
        
        for row in repRows:
            rep_id= str(row.rep_id).strip()
            rep_name= str(row.rep_name).strip()
            area_id= str(row.area_id).strip()
            area_name= str(row.area_name).strip()


#         return rep_name
        docListNew_S=urllib2.unquote(docListNew)
        doc_datalist = docListNew_S.split(',', docListNew_S.count(','))
        i = 0
        validDocList = []
        validDocDict = {}
        resultSuccess=''
        resultFailed=''
       
        while i < docListNew_S.count(',')  :
            doc_single = doc_datalist[i]
            doc_single_list = doc_single.split('<fd>', doc_single.count('<fd>'))
            doc_name = str(doc_single_list[0]).strip()
            doc_id = str(doc_single_list[1]).strip()
            
            
            
            repRows=db((db.sm_doctor_day_plan.cid==cid)&(db.sm_doctor_day_plan.area_id==area_id)&(db.sm_doctor_day_plan.doc_id==doc_id)&(db.sm_doctor_day_plan.plan_date==plan_date)&(db.sm_doctor_day_plan.visit_time==visit_time)).select(db.sm_doctor_day_plan.ALL, orderby=db.sm_doctor_day_plan.doc_id)
    #         return repRows
            if repRows:
                if resultFailed=='':
                    resultFailed =str(doc_id)
                else:
                    resultFailed =resultFailed+','+str(doc_id)

            else:
                
                validDocDict = {'cid':cid, 'rep_id':user_id, 'rep_name':rep_name, 'area_id':territory_code,'area_name':area_name,'doc_id':doc_id, 'doc_name':doc_name, 'first_date':first_dateGet,'plan_date':plan_date, 'visit_time':visit_time}
                validDocList.append(validDocDict)
                if resultSuccess=='':
                    resultSuccess =str(doc_id)
                else:
                    resultSuccess =resultSuccess+','+str(doc_id)
                
            i = i + 1
             
             
        if len(validDocList) > 0:
            doctor_insert = db.sm_doctor_day_plan.bulk_insert(validDocList)
            
        

        if resultFailed!='' and resultSuccess!='':
            return 'Success<rdrd>Success: '+str(resultSuccess)+' Already exist:'+str(resultFailed)
        elif resultFailed!='' and resultSuccess=='':
            return 'Success<rdrd> Already exist:'+str(resultFailed)
        elif resultFailed=='' and resultSuccess!='':
            return 'Success<rdrd> Success: '+str(resultSuccess)
        else:
            return 'Success<rdrd> '
     
# ==========Client   

def add_day_Client():   

    submit_date=request.vars.submit_date
    territory_code=request.vars.territoryCode
    visit_time=request.vars.visit_time
    
    session.visit_time= visit_time
    session.plan_date= submit_date
    session.territory_code=territory_code
#     return session.territory_code

    recRows=db(db.sm_client.area_id==territory_code).select(db.sm_client.client_id, db.sm_client.name,  groupby = db.sm_client.client_id, orderby=db.sm_client.name)
    # return  db._lastsql
    clientStr = ''
    for row in recRows:
        client_id= str(row.client_id).strip()

        name=str(row.name).strip()

        if clientStr=='':
            clientStr = str(name) +'|'+ str(client_id)

        else:
            clientStr=clientStr+'<rdrd>'+ str(name)+'|'+ str(client_id)

    return dict(clientStr=clientStr)

def insertClient():

    cid=session.cid
    user_id=session.rep_id
    password=session.password
    territory_code=session.territory_code
    plan_date=session.plan_date
    visit_time=session.visit_time
    
    clntListNew=str(request.vars.clntListNew).strip()
#     return docListNew
    clnt_single_rt=''
    rep_name= ''
    area_name=''
    first_dateGet=str(plan_date).split('-')[0]+'-'+str(plan_date).split('-')[1]+'-01'
    if (clntListNew=='') :
           
        return 'Failed<rdrd>Please Select Client'
      
    else:
        
        repRows=db((db.sm_rep_area.cid==cid)&(db.sm_rep_area.rep_id==user_id)&(db.sm_rep_area.area_id==territory_code)).select(db.sm_rep_area.rep_id,db.sm_rep_area.rep_name,db.sm_rep_area.area_id, db.sm_rep_area.area_name, orderby=db.sm_rep_area.rep_id)
#         return db._lastsql
        for row in repRows:
            rep_id= str(row.rep_id).strip()
            rep_name= str(row.rep_name).strip()
            area_id= str(row.area_id).strip()
            area_name= str(row.area_name).strip()


#         return rep_name
        clntListNew_S=urllib2.unquote(clntListNew)
        clnt_datalist = clntListNew_S.split(',', clntListNew_S.count(','))
        i = 0
        validClntList = []
        validClntDict = {}
        resultSuccess=''
        resultFailed=''
       
        while i < clntListNew_S.count(',')  :
            clnt_single = clnt_datalist[i]
            clnt_single_list = clnt_single.split('<fd>', clnt_single.count('<fd>'))
            name = str(clnt_single_list[0]).strip()
            client_id = str(clnt_single_list[1]).strip()
            
            
            
            repRows=db((db.sm_client_day_plan.cid==cid)&(db.sm_client_day_plan.area_id==area_id)&(db.sm_client_day_plan.client_id==client_id)&(db.sm_client_day_plan.plan_date==plan_date)&(db.sm_client_day_plan.visit_time==visit_time)).select(db.sm_client_day_plan.ALL, orderby=db.sm_client_day_plan.client_id)
    #         return repRows
            if repRows:
                if resultFailed=='':
                    resultFailed =str(client_id)
                else:
                    resultFailed =resultFailed+','+str(client_id)

            else:
                validClntDict = {'cid':cid, 'rep_id':user_id, 'rep_name':rep_name, 'area_id':territory_code,'area_name':area_name,'client_id':client_id,'client_name':name, 'first_date':first_dateGet, 'plan_date':plan_date, 'visit_time':visit_time}
                validClntList.append(validClntDict)
                if resultSuccess=='':
                    resultSuccess =str(client_id)
                else:
                    resultSuccess =resultSuccess+','+str(client_id)
                
            i = i + 1
             
             
        if len(validClntList) > 0:
            clnt_insert = db.sm_client_day_plan.bulk_insert(validClntList)
            
        

        if resultFailed!='' and resultSuccess!='':
            return 'Success<rdrd>Success: '+str(resultSuccess)+' Already exist:'+str(resultFailed)
        elif resultFailed!='' and resultSuccess=='':
            return 'Success<rdrd> Already exist:'+str(resultFailed)
        elif resultFailed=='' and resultSuccess!='':
            return 'Success<rdrd> Success: '+str(resultSuccess)
        else:
            return 'Success<rdrd> '
        
        
        