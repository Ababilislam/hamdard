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
#         return Dcheck
        if (todayDate - todayDate.replace(day=1)).days > Dcheck:
            x= todayDate + datetime.timedelta(30)
            x.replace(day=1)
            
            checkDate1 = str(x)
        else:
            checkDate1= todayDate.replace(day=1)
        checkDate=checkDate1.split('-')[0]+'-'  +checkDate1.split('-')[1]  +'-01'
#         return checkDate

    
    

    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.user_type, limitby=(0, 1))
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = repRow[0].user_type
        
    draft_info = db((db.sm_doctor_visit_plan.cid==cid)  &(db.sm_doctor_visit_plan.rep_id==session.rep_id) & (db.sm_doctor_visit_plan.first_date==checkDate)).select(db.sm_doctor_visit_plan.status, orderby=db.sm_doctor_visit_plan.id,limitby=(0,1))
#     return draft_info
    status='Draft'
    
    if draft_info:
        status=draft_info[0].status
    strValueMorning=''    
#     if status=='Draft':
        
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
            x= todayDate + datetime.timedelta(30)
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
 
 
 
    
    return dict(marketTourRows=marketTourRows,days_month=days_month,monthShow=monthShow,setDateG=setDateG,status=status,strValueMorning=strValueMorning,strValueMorningE=strValueMorningE)
    
    



# http://127.0.0.1:8000/lscmreporting/syncmobile/getClientInfo?cid=LSCRM&rep_id=101&rep_pass=123&synccode=5771&client_id=1
# getting route,merchandizing,client information
def tourSubmit():
    retStatus = ''
#     return 'assf'
    cid=session.cid
    rep_id=session.rep_id
    password=session.password
    
    monthPass=session.monthPass
    DateTour=session.DateTour
    
    submitStrMorning=str(request.vars.submitStrMorning).strip()
    submitStrEvening=str(request.vars.submitStrEvening).strip()
    days_month=str(request.vars.submitStrEvening).strip()
    
#     return submitStrEvening
    errorFlag=1
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.user_type,db.sm_rep.name, limitby=(0, 1))
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = repRow[0].user_type
        rep_name = repRow[0].name
        
        errorFlag=0
        
    
#     return session.monthPass
    if errorFlag==0:
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
                    return i
                
            mSingleList=submitStrMorningListSingle.split('<fd>')
            i=i+1
            schedule_date=str(DateTour).split('-')[0]+'-'+str(DateTour).split('-')[1]+'-'+str(i)
            first_date=str(DateTour).split('-')[0]+'-'+str(DateTour).split('-')[1]+'-01'
            
            
            
            m=0
#             return len(mSingleList)
            while m < len(mSingleList):
                
                route_nameG=mSingleList[m]
               
                if route_nameG!='':
#                     route_name=route_nameG.split('|')[1]
#                     route_id=route_nameG.split('|')[0]
                    route_name=''
                    route_id=route_nameG
                    
                    ins_dict = {'cid':cid, 'rep_id':rep_id,'rep_name':rep_name, 'first_date':first_date, 'schedule_date':schedule_date, 'route_id':route_id, 'route_name':route_name, 'note':'Morning','status':'Submitted','field2':session.userdepth}
                    tourArrayList.append(ins_dict)
                m=m+1
    
        
        
        i=0
        errorFlagEvening=0
        while i < len(submitStrEveningList)-1:
            submitStrEveningListSingle=submitStrEveningList[i]
#             if (submitStrEveningListSingle==''):
#                 errorFlagEvening=1
            
            mSingleList=submitStrEveningListSingle.split('<fd>')
            i=i+1
            schedule_date=str(DateTour).split('-')[0]+'-'+str(DateTour).split('-')[1]+'-'+str(i)
            first_date=str(DateTour).split('-')[0]+'-'+str(DateTour).split('-')[1]+'-01'
            
            
            
            m=0
#             return len(mSingleList)
            while m < len(mSingleList):
                
                route_nameG=mSingleList[m]
#                 return route_nameG
                if route_nameG!='':
#                     route_name=route_nameG.split('|')[1]
#                     route_id=route_nameG.split('|')[0]
                    
                    route_name=''
                    route_id=route_nameG
                    
                    ins_dict = {'cid':cid, 'rep_id':rep_id,'rep_name':rep_name, 'first_date':first_date, 'schedule_date':schedule_date, 'route_id':route_id, 'route_name':route_name, 'note':'Evening','status':'Submitted'}
                    tourArrayList.append(ins_dict)
                m=m+1
        
        if ((errorFlag==1) ):
                return 'Incomplete'
        if len(tourArrayList) > 0:
            delete_doc_area=db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id) & (db.sm_doctor_visit_plan.first_date == first_date)).delete()
            db.sm_doctor_visit_plan.bulk_insert(tourArrayList)
            
            insStr="update sm_doctor_visit_plan p,sm_level l set p.route_name=l.level_name where  p.rep_id=rep_id and p.first_date=first_date and l.cid=p.cid and l.level_id = p.route_id and p.route_name=''"
#             return insStr
            insRun=db.executesql(insStr)
            
            return 'Success'
    
    
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
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.user_type, limitby=(0, 1))
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = repRow[0].user_type
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
                
                route_nameG=mSingleList[m].replace('undefined','')
                
                if route_nameG!='':
#                     return route_nameG
#                     route_name=route_nameG.split('|')[1]
#                     route_id=route_nameG.split('|')[0]
                    
                    route_name=''
                    route_id=route_nameG
                    
                    ins_dict = {'cid':cid, 'rep_id':rep_id, 'first_date':first_date, 'schedule_date':schedule_date, 'route_id':route_id, 'route_name':route_name, 'note':'Morning','status':'Draft'}
                    tourArrayList.append(ins_dict)
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
                
                route_nameG=mSingleList[m]
#                 return route_nameG
                if route_nameG!='':
#                     route_name=route_nameG.split('|')[1]
#                     route_id=route_nameG.split('|')[0]
                    
                    route_name=''
                    route_id=route_nameG
                    
                    ins_dict = {'cid':cid, 'rep_id':rep_id, 'first_date':first_date, 'schedule_date':schedule_date, 'route_id':route_id, 'route_name':route_name, 'note':'Evening','status':'Draft'}
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
    
    

    

#     return str(rep_id)+'  '+str(cid)+'  '+str(DateTour)
    tourThisMorning = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id) & (db.sm_doctor_visit_plan.first_date == DateTour)& (db.sm_doctor_visit_plan.note == 'Morning') & ((db.sm_doctor_visit_plan.status == 'Confirmed') | (db.sm_doctor_visit_plan.status == 'Submitted'))).select(db.sm_doctor_visit_plan.ALL,orderby=db.sm_doctor_visit_plan.schedule_date)
    tourThisEvening = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id) & (db.sm_doctor_visit_plan.first_date == DateTour)& (db.sm_doctor_visit_plan.note == 'Evening') & ((db.sm_doctor_visit_plan.status == 'Confirmed') | (db.sm_doctor_visit_plan.status == 'Submitted'))).select(db.sm_doctor_visit_plan.ALL,orderby=db.sm_doctor_visit_plan.schedule_date)
    
#     return tourThisMorning
#     return DateTour
#     tourNext = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id) & (db.sm_doctor_visit_plan.first_date == DateTourNext) ).select(db.sm_doctor_visit_plan.ALL,orderby=db.sm_doctor_visit_plan.schedule_date)
    
    strThisMorning=''
    s_datePast=''
    T_status=''
    for tourThisMorning in tourThisMorning:
        s_date=str(tourThisMorning.schedule_date)
        routeId=str(tourThisMorning.route_id)
        routeName=str(tourThisMorning.route_name)
        T_status=str(tourThisMorning.status)
        routeShow=routeName+'|'+routeId
        if s_date!=s_datePast:
            strThisMorning=strThisMorning+'<rd>'+s_date
        
        strThisMorning=strThisMorning+routeShow+','
        s_datePast=s_date
    
    
    
    strThisEvening=''
    s_datePast=''
    for tourThisEvening in tourThisEvening:
        s_date=str(tourThisEvening.schedule_date)
        routeId=str(tourThisEvening.route_id)
        routeName=str(tourThisEvening.route_name)
        routeShow=routeName+'|'+routeId
        if s_date!=s_datePast:
            strThisEvening=strThisEvening+'<rd>'+s_date
        
        strThisEvening=strThisEvening+routeShow+','
        s_datePast=s_date
        
    monthGet=str(DateTour).split('-')[1]
    yearGet=str(DateTour).split('-')[0]
    
    month=int(monthGet)
    year=int(yearGet)
    monthDay=0
    days_month=0
    days_month= days_in_month(year, month)
    
    monthShow= month_name(month)
    
    return dict(strThisMorning=strThisMorning,strThisEvening=strThisEvening,days_month=days_month,monthShow=monthShow,T_status=T_status)
    
    
   

def tourShowSup_webNext():
    cid=session.cid
    rep_id=session.repTour
    
    
    Dcheck=int(str(current_date).split('-')[2].split(' ')[0])-2
    todayDate = datetime.date.today()
#         return Dcheck
    if (todayDate - todayDate.replace(day=1)).days > Dcheck:
        
        x= todayDate + datetime.timedelta(30)
        x.replace(day=1)
        
        nextMaont = str(x)
    else:
        nextMaont= todayDate.replace(day=1)
    DateTourNext= nextMaont.split('-')[0]+'-'+nextMaont.split('-')[1]+'-01'
#     return DateTourNext    

    

        
    tourThisMorning = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id) & (db.sm_doctor_visit_plan.first_date == DateTourNext)& (db.sm_doctor_visit_plan.note == 'Morning') & ((db.sm_doctor_visit_plan.status == 'Confirmed') | (db.sm_doctor_visit_plan.status == 'Submitted'))).select(db.sm_doctor_visit_plan.ALL,orderby=db.sm_doctor_visit_plan.schedule_date)
    tourThisEvening = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id) & (db.sm_doctor_visit_plan.first_date == DateTourNext)& (db.sm_doctor_visit_plan.note == 'Evening') & ((db.sm_doctor_visit_plan.status == 'Confirmed') | (db.sm_doctor_visit_plan.status == 'Submitted'))).select(db.sm_doctor_visit_plan.ALL,orderby=db.sm_doctor_visit_plan.schedule_date)
#     return tourThisMorning
#     tourNext = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id) & (db.sm_doctor_visit_plan.first_date == DateTourNext) ).select(db.sm_doctor_visit_plan.ALL,orderby=db.sm_doctor_visit_plan.schedule_date)
    
    strThisMorning=''
    s_datePast=''
    T_status=''
    for tourThisMorning in tourThisMorning:
        s_date=str(tourThisMorning.schedule_date)
        routeId=str(tourThisMorning.route_id)
        routeName=str(tourThisMorning.route_name)
        T_status=str(tourThisMorning.status)
        routeShow=routeName+'|'+routeId
        if s_date!=s_datePast:
            strThisMorning=strThisMorning+'<rd>'+s_date
        
        strThisMorning=strThisMorning+routeShow+','
        s_datePast=s_date
    
    
    
    strThisEvening=''
    s_datePast=''
    for tourThisEvening in tourThisEvening:
        s_date=str(tourThisEvening.schedule_date)
        routeId=str(tourThisEvening.route_id)
        routeName=str(tourThisEvening.route_name)
        routeShow=routeName+'|'+routeId
        if s_date!=s_datePast:
            strThisEvening=strThisEvening+'<rd>'+s_date
        
        strThisEvening=strThisEvening+routeShow+','
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
#     return days_month
    return dict(strThisMorning=strThisMorning,strThisEvening=strThisEvening,days_month=days_month,monthShow=monthShow,DateTourNext=DateTourNext,T_status=T_status,setDateG=setDateG)
    
    
    
def tourAccept():
    cid=session.cid
    rep_id=session.repTour
    thisM_fdate=str(first_currentDate).split(' ')[0]
    
    tourThisEvening = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id) & (db.sm_doctor_visit_plan.first_date == thisM_fdate)).update(status='Confirmed')
    
    
    
    return 'Success'
    
    
     
  
def tourReject():
    cid=session.cid
    rep_id=session.repTour
    thisM_fdate=str(first_currentDate).split(' ')[0]
    
    tourThisEvening = db((db.sm_doctor_visit_plan.cid == cid) & (db.sm_doctor_visit_plan.rep_id == rep_id) & (db.sm_doctor_visit_plan.first_date == thisM_fdate)).update(status='Draft')
    
    
    
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
#         return Dcheck
        if (todayDate - todayDate.replace(day=1)).days > Dcheck:
            x= todayDate + datetime.timedelta(30)
            x.replace(day=1)
            
            checkDate1 = str(x)
        else:
            checkDate1= todayDate.replace(day=1)
        checkDate=checkDate1.split('-')[0]+'-'  +checkDate1.split('-')[1]  +'-01'
#         return checkDate

    
    

    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.user_type, limitby=(0, 1))
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = repRow[0].user_type
        
    draft_info = db((db.sm_doctor_visit_plan.cid==cid)  &(db.sm_doctor_visit_plan.rep_id==session.rep_id) & (db.sm_doctor_visit_plan.first_date==checkDate)).select(db.sm_doctor_visit_plan.status, orderby=db.sm_doctor_visit_plan.id,limitby=(0,1))
#     return draft_info
    status='Draft'
    
    if draft_info:
        status=draft_info[0].status
    strValueMorning=''    
#     if status=='Draft':
        
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
            x= todayDate + datetime.timedelta(30)
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
 
 
 
    
    return dict(marketTourRows=marketTourRows,days_month=days_month,monthShow=monthShow,setDateG=setDateG,status=status,strValueMorning=strValueMorning,strValueMorningE=strValueMorningE)
    
def amndCheck():
    cid=session.cid 
    rep_id=session.rep_id
    checkDate=str(request.vars.check_date).strip()
#     return cid
    if checkDate!='':
        strValueMorning=''
        strValueMorningE=''
        draft_infoAll = db((db.sm_doctor_visit_plan.cid==cid)  &(db.sm_doctor_visit_plan.rep_id==session.rep_id) & (db.sm_doctor_visit_plan.schedule_date==checkDate)   &((db.sm_doctor_visit_plan.note=='Morning') | (db.sm_doctor_visit_plan.note==''))).select(db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.status, orderby=db.sm_doctor_visit_plan.id)
#         return db._lastsql
        for draft_infoAll in draft_infoAll:
            route_name = draft_infoAll.route_name   
            sDate=str(draft_infoAll.schedule_date)
            strValueMorning=strValueMorning+'<'+sDate+'>'+route_name
            
        strValueMorningE=''
        draft_infoAllE = db((db.sm_doctor_visit_plan.cid==cid)  &(db.sm_doctor_visit_plan.rep_id==session.rep_id) & (db.sm_doctor_visit_plan.schedule_date==checkDate) &(db.sm_doctor_visit_plan.note=='Evening')).select(db.sm_doctor_visit_plan.route_name,db.sm_doctor_visit_plan.route_id,db.sm_doctor_visit_plan.schedule_date,db.sm_doctor_visit_plan.status, orderby=db.sm_doctor_visit_plan.id)
    #         return db._lastsql
        for draft_infoAllE in draft_infoAllE:
            route_name = draft_infoAllE.route_name   
            sDate=str(draft_infoAllE.schedule_date)
            strValueMorningE=strValueMorningE+'<'+sDate+'>'+route_name
        return strValueMorning+'<rdrd>'+strValueMorningE
    else:
        return 'blank'
            
        
    