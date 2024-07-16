
import urllib2
import calendar

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)
def deduct_months(sourcedate, months):
    month = sourcedate.month - 1 - months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)

def dashboard():
    if (session.cid == '' or session.user_id == '' or session.cid == None or session.user_id == None):
        redirect(URL('index'))
    
    #----------------
    response.title = 'Dashboard'
    #-----------------
    #temp
    #current_date='2015-04-30'
    first_currentDate = datetime.datetime.strptime(str(current_date)[0:7] + '-01', '%Y-%m-%d')
        
    #-----------------
    cid = session.cid
    
    currentMonth = first_currentDate.strftime('%b - %Y')
    firstDate = first_currentDate
    
    lastMonth = deduct_months(firstDate, 1)    
    prevMonth=deduct_months(firstDate, 2)
    
    currentdate = datetime.datetime.strptime(str(current_date), '%Y-%m-%d')
    
    yesterday=datetime.datetime.strptime(str(current_date), '%Y-%m-%d')-datetime.timedelta(days=1)
    prevday2=datetime.datetime.strptime(str(current_date), '%Y-%m-%d')-datetime.timedelta(days=2)
    prevday3=datetime.datetime.strptime(str(current_date), '%Y-%m-%d')-datetime.timedelta(days=3)
    prevday4=datetime.datetime.strptime(str(current_date), '%Y-%m-%d')-datetime.timedelta(days=4)
    prevday5=datetime.datetime.strptime(str(current_date), '%Y-%m-%d')-datetime.timedelta(days=5)
    prevday6=datetime.datetime.strptime(str(current_date), '%Y-%m-%d')-datetime.timedelta(days=6)
    prevday7=datetime.datetime.strptime(str(current_date), '%Y-%m-%d')-datetime.timedelta(days=7)
    prevday8=datetime.datetime.strptime(str(current_date), '%Y-%m-%d')-datetime.timedelta(days=8)
    prevday9=datetime.datetime.strptime(str(current_date), '%Y-%m-%d')-datetime.timedelta(days=9)
    
    showLevelName = ''
    showLevelValue = ''
    
    #-------------------
    regionName=''
    regionID=''
    areaName=''
    areaID=''
    territoryName=''
    territoryID=''
    marketName=''
    marketID=''
    
    depthNo = 0
    levelId = 0
    levelName = ''
    depth = -1
    
    if session.user_type=='Supervisor':
        btn_click = 'Yes'
    else:
        btn_click = request.vars.btn_click
    
    if btn_click:
        if session.user_type=='Supervisor':
            levelId = request.vars.levelId
            if levelId=='' or levelId==None:
                levelId=session.level_id
            else:
                levelCheck = db((db.sm_level.cid == cid) & (db.sm_level.level_id == levelId)).select(db.sm_level.depth,limitby=(0, 1))
                if not levelCheck:
                    levelId=session.level_id
                else:
                    depthCheck=levelCheck[0].depth
                    if int(depthCheck)<=int(session.depthNo):
                        levelId=session.level_id
                    else:
                        pass
        
        else:
            levelId = request.vars.levelId
            
        if levelId=='':
            levelId = 0
        else:
            levelRow = db((db.sm_level.cid == cid) & (db.sm_level.level_id == levelId)).select(db.sm_level.level_name, db.sm_level.depth,db.sm_level.level0,db.sm_level.level1,db.sm_level.level2, limitby=(0, 1))
            if levelRow:
                showLevel = levelRow[0].level_name
                depth = levelRow[0].depth
                
                regionID=levelRow[0].level0
                areaID=levelRow[0].level1
                territoryID=levelRow[0].level2
                
                if depth == 0:
                    regionName = showLevel
                    showLevelValue = regionName
                elif depth == 1:
                    regionName = db((db.sm_level.cid == cid) & (db.sm_level.level_id == regionID)).select(db.sm_level.level_name,limitby=(0, 1))[0].level_name
                    
                    areaName=showLevel
                    showLevelValue = areaName
                elif depth == 2:
                    regionName = db((db.sm_level.cid == cid) & (db.sm_level.level_id == regionID)).select(db.sm_level.level_name,limitby=(0, 1))[0].level_name
                    areaName = db((db.sm_level.cid == cid) & (db.sm_level.level_id == areaID)).select(db.sm_level.level_name,limitby=(0, 1))[0].level_name
                    
                    territoryName=showLevel
                    showLevelValue = territoryName
                elif depth == 3:
                    regionName = db((db.sm_level.cid == cid) & (db.sm_level.level_id == regionID)).select(db.sm_level.level_name,limitby=(0, 1))[0].level_name
                    areaName = db((db.sm_level.cid == cid) & (db.sm_level.level_id == areaID)).select(db.sm_level.level_name,limitby=(0, 1))[0].level_name
                    territoryName = db((db.sm_level.cid == cid) & (db.sm_level.level_id == territoryID)).select(db.sm_level.level_name,limitby=(0, 1))[0].level_name
                                        
                    marketName=showLevel
                    showLevelValue = marketName
    
    
    if depth == -1:
        levelName = session.level0Name#'Region'
        showLevelName = 'National'
    elif depth == 0:
        levelName = session.level1Name#'Area'
        showLevelName = session.level0Name
    elif depth == 1:
        levelName = session.level2Name#'Territory'
        showLevelName = session.level1Name
        
    elif depth == 2:
        levelName = session.level3Name#'Market'
        showLevelName = session.level2Name
        
    elif depth == 3:
        levelName = session.level4Name#'Outlet'
        showLevelName = session.level3Name
        
        
    levelRows = db((db.sm_level.cid == cid) & (db.sm_level.parent_level_id == levelId)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
    
    #-----------------    
    callVsOrderList=[]
    orderVolumeList=[]
    doctorScheduleVsExceList=[]
    
    retailerDistrbList=[]
    spoDistrbList=[]
    categoryRetailerList=[]
    retailerUpdateList=[]
    recordDictData={'CallToday':0,'CallYesterday':0,'CallThisMonth':0,'OrderToday':0,'OrderYesterday':0,'OrderThisMonth':0,'OrderAmtToday':0,'OrderAmtYesterday':0,'OrderAmtThisMonth':0,'DocSchedToday':0,'DocSchedYesterday':0,'DocSchedThisMonth':0,'DocVisitToday':0,'DocVisitYesterday':0,'DocVisitThisMonth':0}
    
    regionRecordShowList = []
    regionRecordList = []
    
    levelDepthFlag=True
    if levelName == session.level0Name:#'Region'        
        #====================== visit Call
        qsetV=db()
        qsetV=qsetV((db.sm_level.cid == cid)&(db.sm_level.is_leaf == '1'))        
        qsetV=qsetV(db.sm_order_head.cid==cid)
        qsetV=qsetV(db.sm_order_head.area_id==db.sm_level.level_id)
        
        #=================== order
        qsetOrder=db()
        qsetOrder=qsetOrder((db.sm_level.cid == cid)&(db.sm_level.is_leaf == '1'))        
        qsetOrder=qsetOrder(db.sm_order.cid==cid)
        qsetOrder=qsetOrder(db.sm_order.area_id==db.sm_level.level_id)
        
        #=================== Doctor
        if session.setting_doctor==1:
            qsetDoctor=db()
            qsetDoctor=qsetDoctor((db.sm_level.cid == cid)&(db.sm_level.is_leaf == '1'))        
            qsetDoctor=qsetDoctor(db.sm_doctor_visit.cid==cid)
            qsetDoctor=qsetDoctor(db.sm_doctor_visit.route_id==db.sm_level.level_id)
        
    elif levelName == session.level1Name:#'Area':
        qsetV=db()
        qsetV=qsetV((db.sm_level.cid == cid)&(db.sm_level.is_leaf == '1'))       
        qsetV=qsetV(db.sm_level.level0 == regionID) 
        qsetV=qsetV(db.sm_order_head.cid==cid)
        qsetV=qsetV(db.sm_order_head.area_id==db.sm_level.level_id)
        
        #=================== order
        qsetOrder=db()
        qsetOrder=qsetOrder((db.sm_level.cid == cid)&(db.sm_level.is_leaf == '1'))    
        qsetOrder=qsetOrder(db.sm_level.level0 == regionID)    
        qsetOrder=qsetOrder(db.sm_order.cid==cid)
        qsetOrder=qsetOrder(db.sm_order.area_id==db.sm_level.level_id)
        
        #=================== Doctor
        if session.setting_doctor==1:
            qsetDoctor=db()
            qsetDoctor=qsetDoctor((db.sm_level.cid == cid)&(db.sm_level.is_leaf == '1'))
            qsetDoctor=qsetDoctor(db.sm_level.level0 == regionID)
            qsetDoctor=qsetDoctor(db.sm_doctor_visit.cid==cid)
            qsetDoctor=qsetDoctor(db.sm_doctor_visit.route_id==db.sm_level.level_id)
        
    elif levelName == session.level2Name:#'Territory':
        qsetV=db()
        qsetV=qsetV((db.sm_level.cid == cid)&(db.sm_level.is_leaf == '1'))       
        qsetV=qsetV(db.sm_level.level0 == regionID) 
        qsetV=qsetV(db.sm_level.level1 == areaID)
        qsetV=qsetV(db.sm_order_head.cid==cid)
        qsetV=qsetV(db.sm_order_head.area_id==db.sm_level.level_id)
        
        #=================== order
        qsetOrder=db()
        qsetOrder=qsetOrder((db.sm_level.cid == cid)&(db.sm_level.is_leaf == '1'))    
        qsetOrder=qsetOrder(db.sm_level.level0 == regionID)   
        qsetOrder=qsetOrder(db.sm_level.level1 == areaID) 
        qsetOrder=qsetOrder(db.sm_order.cid==cid)
        qsetOrder=qsetOrder(db.sm_order.area_id==db.sm_level.level_id)
        
        #=================== Doctor
        if session.setting_doctor==1:
            qsetDoctor=db()
            qsetDoctor=qsetDoctor((db.sm_level.cid == cid)&(db.sm_level.is_leaf == '1'))
            qsetDoctor=qsetDoctor(db.sm_level.level0 == regionID)
            qsetDoctor=qsetDoctor(db.sm_level.level1 == areaID)
            qsetDoctor=qsetDoctor(db.sm_doctor_visit.cid==cid)
            qsetDoctor=qsetDoctor(db.sm_doctor_visit.route_id==db.sm_level.level_id)
        
    elif levelName == session.level3Name:#'Market':        
        #====================== visit Call
        qsetV=db()
        qsetV=qsetV((db.sm_level.cid == cid)&(db.sm_level.is_leaf == '1'))       
        qsetV=qsetV(db.sm_level.level0 == regionID) 
        qsetV=qsetV(db.sm_level.level1 == areaID)
        qsetV=qsetV(db.sm_level.level2 == territoryID)
        qsetV=qsetV(db.sm_order_head.cid==cid)
        qsetV=qsetV(db.sm_order_head.area_id==db.sm_level.level_id)
        
        #=================== order
        qsetOrder=db()
        qsetOrder=qsetOrder((db.sm_level.cid == cid)&(db.sm_level.is_leaf == '1'))    
        qsetOrder=qsetOrder(db.sm_level.level0 == regionID)   
        qsetOrder=qsetOrder(db.sm_level.level1 == areaID) 
        qsetOrder=qsetOrder(db.sm_level.level2 == territoryID) 
        qsetOrder=qsetOrder(db.sm_order.cid==cid)
        qsetOrder=qsetOrder(db.sm_order.area_id==db.sm_level.level_id)
        
        #=================== Doctor
        if session.setting_doctor==1:
            qsetDoctor=db()
            qsetDoctor=qsetDoctor((db.sm_level.cid == cid)&(db.sm_level.is_leaf == '1'))
            qsetDoctor=qsetDoctor(db.sm_level.level0 == regionID)
            qsetDoctor=qsetDoctor(db.sm_level.level1 == areaID)
            qsetDoctor=qsetDoctor(db.sm_level.level2 == territoryID) 
            qsetDoctor=qsetDoctor(db.sm_doctor_visit.cid==cid)
            qsetDoctor=qsetDoctor(db.sm_doctor_visit.route_id==db.sm_level.level_id)
        
    elif levelName == session.level4Name:#'Outlet':
        qsetV=db()
        qsetV=qsetV((db.sm_level.cid == cid)&(db.sm_level.is_leaf == '1'))       
        qsetV=qsetV(db.sm_level.level0 == regionID) 
        qsetV=qsetV(db.sm_level.level1 == areaID)
        qsetV=qsetV(db.sm_level.level2 == territoryID)
        qsetV=qsetV(db.sm_level.level3 == marketID)
        qsetV=qsetV(db.sm_order_head.cid==cid)
        qsetV=qsetV(db.sm_order_head.area_id==db.sm_level.level_id)
        
        #=================== order
        qsetOrder=db()
        qsetOrder=qsetOrder((db.sm_level.cid == cid)&(db.sm_level.is_leaf == '1'))    
        qsetOrder=qsetOrder(db.sm_level.level0 == regionID)   
        qsetOrder=qsetOrder(db.sm_level.level1 == areaID)
        qsetOrder=qsetOrder(db.sm_level.level2 == territoryID)
        qsetOrder=qsetOrder(db.sm_level.level3 == marketID) 
        qsetOrder=qsetOrder(db.sm_order.cid==cid)
        qsetOrder=qsetOrder(db.sm_order.area_id==db.sm_level.level_id)
        
        #=================== Doctor
        if session.setting_doctor==1:
            qsetDoctor=db()
            qsetDoctor=qsetDoctor((db.sm_level.cid == cid)&(db.sm_level.is_leaf == '1'))
            qsetDoctor=qsetDoctor(db.sm_level.level0 == regionID)
            qsetDoctor=qsetDoctor(db.sm_level.level1 == areaID)
            qsetDoctor=qsetDoctor(db.sm_level.level2 == territoryID)
            qsetDoctor=qsetDoctor(db.sm_level.level3 == marketID)
            qsetDoctor=qsetDoctor(db.sm_doctor_visit.cid==cid)
            qsetDoctor=qsetDoctor(db.sm_doctor_visit.route_id==db.sm_level.level_id)
        
    else:
        levelDepthFlag=False
    
    
    if levelDepthFlag==True:
        #-----This month
        qset1=qsetV(db.sm_order_head.ym_date==firstDate)        
        number_ofVisitRet1 = qset1.count()
        recordDictData['CallThisMonth']=number_ofVisitRet1
        
        #---------- Today
        qsetToday1=qsetV(db.sm_order_head.order_date==currentdate)        
        number_ofVisitRetqsetToday1 = qsetToday1.count()
        recordDictData['CallToday']=number_ofVisitRetqsetToday1
        
        #---------- Yesterday
        qsetPrevday1=qsetV(db.sm_order_head.order_date==yesterday)        
        number_ofVisitRetPrevday1 = qsetPrevday1.count()
        recordDictData['CallYesterday']=number_ofVisitRetPrevday1
        
        #---------- prev 2
        qsetPrevday2=qsetV(db.sm_order_head.order_date==prevday2)        
        number_ofVisitRetPrevday2 = qsetPrevday2.count()
        
        #----------  prev 3
        qsetPrevday3=qsetV(db.sm_order_head.order_date==prevday3)        
        number_ofVisitRetPrevday3 = qsetPrevday3.count()
        
        #----------  prev 4
        qsetPrevday4=qsetV(db.sm_order_head.order_date==prevday4)        
        number_ofVisitRetPrevday4 = qsetPrevday4.count()
        
        #----------  prev 5
        qsetPrevday5=qsetV(db.sm_order_head.order_date==prevday5)        
        number_ofVisitRetPrevday5 = qsetPrevday5.count()
        
        #----------  prev 6
        qsetPrevday6=qsetV(db.sm_order_head.order_date==prevday6)        
        number_ofVisitRetPrevday6 = qsetPrevday6.count()
        
        #----------  prev 7
        qsetPrevday7=qsetV(db.sm_order_head.order_date==prevday7)        
        number_ofVisitRetPrevday7 = qsetPrevday7.count()
        
        #----------  prev 8
        qsetPrevday8=qsetV(db.sm_order_head.order_date==prevday8)        
        number_ofVisitRetPrevday8 = qsetPrevday8.count()
        
        #----------  prev 9
        qsetPrevday9=qsetV(db.sm_order_head.order_date==prevday9)        
        number_ofVisitRetPrevday9 = qsetPrevday9.count()
        
        
        #=================== order
        #------ This Month
        qsetOrder1=qsetOrder(db.sm_order.ym_date==firstDate)
        
        orderRecords1 = qsetOrder1.select(db.sm_order.vsl,groupby=db.sm_order.vsl)
        number_ofOrderRet1 = len(orderRecords1)
        recordDictData['OrderThisMonth']=number_ofOrderRet1        
        #-- OrderVolume This Month  
        orderRecordsVol1 = qsetOrder1.select(db.sm_order.quantity,db.sm_order.price)
        ordVol1Total=0
        for ordVol1 in orderRecordsVol1:
            quantity1=ordVol1.quantity
            price1=ordVol1.price            
            ordVol1Total+=int(quantity1)*float(price1)
        
        ordVol1Total=round(ordVol1Total,2)
        recordDictData['OrderAmtThisMonth']=ordVol1Total
        
        
        #------ Today
        qsetOrderToday1=qsetOrder(db.sm_order.order_date==current_date)
        
        orderRecordsToday1 = qsetOrderToday1.select(db.sm_order.vsl,groupby=db.sm_order.vsl)
        number_ofOrderRetToday1 = len(orderRecordsToday1)
        recordDictData['OrderToday']=number_ofOrderRetToday1        
        #-- OrderVolume today
        orderRecordsVolToday1 = qsetOrderToday1.select(db.sm_order.quantity,db.sm_order.price)        
        ordVolTotalT1=0
        for ordVolT1 in orderRecordsVolToday1:
            quantityT1=ordVolT1.quantity
            priceT1=ordVolT1.price            
            ordVolTotalT1+=int(quantityT1)*float(priceT1)        
        ordVolTotalT1=round(ordVolTotalT1,2)
        recordDictData['OrderAmtToday']=ordVolTotalT1
        
        #------ Yesterday
        qsetOrderPrev1=qsetOrder(db.sm_order.order_date==yesterday)
        
        orderRecordsrPrev1 = qsetOrderPrev1.select(db.sm_order.vsl,groupby=db.sm_order.vsl)
        number_ofOrderRetrPrev1 = len(orderRecordsrPrev1)
        recordDictData['OrderYesterday']=number_ofOrderRetrPrev1        
        #-- OrderVolume yesterday
        orderRecordsVolPrev1 = qsetOrderPrev1.select(db.sm_order.quantity,db.sm_order.price)        
        ordVolTotalT2=0
        for ordVolPrev1 in orderRecordsVolPrev1:
            quantityPrev1=ordVolPrev1.quantity
            pricePrev1=ordVolPrev1.price            
            ordVolTotalT2+=int(quantityPrev1)*float(pricePrev1)        
        ordVolTotalT2=round(ordVolTotalT2,2)
        recordDictData['OrderAmtYesterday']=ordVolTotalT2
                
        #------ prevday2
        qsetOrderPrev2=qsetOrder(db.sm_order.order_date==prevday2)
        
        orderRecordsrPrev2 = qsetOrderPrev2.select(db.sm_order.vsl,groupby=db.sm_order.vsl)
        number_ofOrderRetrPrev2 = len(orderRecordsrPrev2)      
        #-- OrderVolume yesterday
        orderRecordsVolPrev2 = qsetOrderPrev2.select(db.sm_order.quantity,db.sm_order.price)        
        ordVolTotalPT2=0
        for ordVolPrev2 in orderRecordsVolPrev2:
            quantityPrev2=ordVolPrev2.quantity
            pricePrev2=ordVolPrev2.price            
            ordVolTotalPT2+=int(quantityPrev2)*float(pricePrev2)        
        ordVolTotalPT2=round(ordVolTotalPT2,2)
        
        #------ prevday3
        qsetOrderPrev3=qsetOrder(db.sm_order.order_date==prevday3)
        
        orderRecordsrPrev3 = qsetOrderPrev3.select(db.sm_order.vsl,groupby=db.sm_order.vsl)
        number_ofOrderRetrPrev3 = len(orderRecordsrPrev3)    
        #-- OrderVolume 
        orderRecordsVolPrev3 = qsetOrderPrev3.select(db.sm_order.quantity,db.sm_order.price)        
        ordVolTotalPT3=0
        for ordVolPrev3 in orderRecordsVolPrev3:
            quantityPrev3=ordVolPrev3.quantity
            pricePrev3=ordVolPrev3.price            
            ordVolTotalPT3+=int(quantityPrev3)*float(pricePrev3)        
        ordVolTotalPT3=round(ordVolTotalPT3,2)
        
        #------ prevday4
        qsetOrderPrev4=qsetOrder(db.sm_order.order_date==prevday4)
        
        orderRecordsrPrev4 = qsetOrderPrev4.select(db.sm_order.vsl,groupby=db.sm_order.vsl)
        number_ofOrderRetrPrev4 = len(orderRecordsrPrev4)     
        #-- OrderVolume 
        orderRecordsVolPrev4 = qsetOrderPrev4.select(db.sm_order.quantity,db.sm_order.price)        
        ordVolTotalPT4=0
        for ordVolPrev4 in orderRecordsVolPrev4:
            quantityPrev4=ordVolPrev4.quantity
            pricePrev4=ordVolPrev4.price            
            ordVolTotalPT4+=int(quantityPrev4)*float(pricePrev4)        
        ordVolTotalPT4=round(ordVolTotalPT4,2)
        
        #------ prevday5
        qsetOrderPrev5=qsetOrder(db.sm_order.order_date==prevday5)
        
        orderRecordsrPrev5 = qsetOrderPrev5.select(db.sm_order.vsl,groupby=db.sm_order.vsl)
        number_ofOrderRetrPrev5 = len(orderRecordsrPrev5)      
        #-- OrderVolume 
        orderRecordsVolPrev5 = qsetOrderPrev5.select(db.sm_order.quantity,db.sm_order.price)        
        ordVolTotalPT5=0
        for ordVolPrev5 in orderRecordsVolPrev5:
            quantityPrev5=ordVolPrev5.quantity
            pricePrev5=ordVolPrev5.price            
            ordVolTotalPT5+=int(quantityPrev5)*float(pricePrev5)        
        ordVolTotalPT5=round(ordVolTotalPT5,2)
        
        #------ prevday6
        qsetOrderPrev6=qsetOrder(db.sm_order.order_date==prevday6)
        
        orderRecordsrPrev6 = qsetOrderPrev6.select(db.sm_order.vsl,groupby=db.sm_order.vsl)
        number_ofOrderRetrPrev6 = len(orderRecordsrPrev6)   
        #-- OrderVolume 
        orderRecordsVolPrev6 = qsetOrderPrev6.select(db.sm_order.quantity,db.sm_order.price)        
        ordVolTotalPT6=0
        for ordVolPrev6 in orderRecordsVolPrev6:
            quantityPrev6=ordVolPrev6.quantity
            pricePrev6=ordVolPrev6.price            
            ordVolTotalPT6+=int(quantityPrev6)*float(pricePrev6)        
        ordVolTotalPT6=round(ordVolTotalPT6,2)
        
        #------ prevday7
        qsetOrderPrev7=qsetOrder(db.sm_order.order_date==prevday7)
        
        orderRecordsrPrev7 = qsetOrderPrev7.select(db.sm_order.vsl,groupby=db.sm_order.vsl)
        number_ofOrderRetrPrev7 = len(orderRecordsrPrev7)      
        #-- OrderVolume 
        orderRecordsVolPrev7 = qsetOrderPrev7.select(db.sm_order.quantity,db.sm_order.price)        
        ordVolTotalPT7=0
        for ordVolPrev7 in orderRecordsVolPrev7:
            quantityPrev7=ordVolPrev7.quantity
            pricePrev7=ordVolPrev7.price            
            ordVolTotalPT7+=int(quantityPrev7)*float(pricePrev7)        
        ordVolTotalPT7=round(ordVolTotalPT7,2)
        
        #------ prevday8
        qsetOrderPrev8=qsetOrder(db.sm_order.order_date==prevday8)
        
        orderRecordsrPrev8 = qsetOrderPrev8.select(db.sm_order.vsl,groupby=db.sm_order.vsl)
        number_ofOrderRetrPrev8 = len(orderRecordsrPrev8)      
        #-- OrderVolume 
        orderRecordsVolPrev8 = qsetOrderPrev8.select(db.sm_order.quantity,db.sm_order.price)        
        ordVolTotalPT8=0
        for ordVolPrev8 in orderRecordsVolPrev8:
            quantityPrev8=ordVolPrev8.quantity
            pricePrev8=ordVolPrev8.price            
            ordVolTotalPT8+=int(quantityPrev8)*float(pricePrev8)        
        ordVolTotalPT8=round(ordVolTotalPT8,2)
        
        #------ prevday9
        qsetOrderPrev9=qsetOrder(db.sm_order.order_date==prevday9)
        
        orderRecordsrPrev9 = qsetOrderPrev9.select(db.sm_order.vsl,groupby=db.sm_order.vsl)
        number_ofOrderRetrPrev9 = len(orderRecordsrPrev9)    
        #-- OrderVolume
        orderRecordsVolPrev9 = qsetOrderPrev9.select(db.sm_order.quantity,db.sm_order.price)        
        ordVolTotalPT9=0
        for ordVolPrev9 in orderRecordsVolPrev9:
            quantityPrev9=ordVolPrev9.quantity
            pricePrev9=ordVolPrev9.price            
            ordVolTotalPT9+=int(quantityPrev9)*float(pricePrev9)        
        ordVolTotalPT9=round(ordVolTotalPT9,2)
        
        #============== Doctor
        #-- Doctor This Month
        if session.setting_doctor==1:
            qsetDoctor1=qsetDoctor(db.sm_doctor_visit.visit_firstdate==firstDate)
            
            number_ofDoctor1 = qsetDoctor1.count()
            recordDictData['DocVisitThisMonth']=number_ofDoctor1
            
            #------ Today
            qsetDoctor1=qsetDoctor(db.sm_doctor_visit.visit_date==current_date)
             
            number_ofdoctorRecordsToday1 = qsetDoctor1.count()
            recordDictData['DocVisitToday']=number_ofdoctorRecordsToday1
            
            #------ Yesterday
            qsetDoctorPrev1=qsetDoctor(db.sm_doctor_visit.visit_date==yesterday)
            
            number_ofDoctorPrev1 = qsetDoctorPrev1.count()
            recordDictData['DocVisitYesterday']=number_ofDoctorPrev1
            
            #------ prevday2
            qsetDoctorPrev2=qsetDoctor(db.sm_doctor_visit.visit_date==prevday2)        
            number_ofDoctorPrev2 = qsetDoctorPrev2.count()
            
            #------ prevday3
            qsetDoctorPrev3=qsetDoctor(db.sm_doctor_visit.visit_date==prevday3)        
            number_ofDoctorPrev3 = qsetDoctorPrev3.count()
            
            #------ prevday4
            qsetDoctorPrev4=qsetDoctor(db.sm_doctor_visit.visit_date==prevday4)        
            number_ofDoctorPrev4 = qsetDoctorPrev4.count()
            
            #------ prevday5
            qsetDoctorPrev5=qsetDoctor(db.sm_doctor_visit.visit_date==prevday5)        
            number_ofDoctorPrev5 = qsetDoctorPrev5.count()
            
            #------ prevday6
            qsetDoctorPrev6=qsetDoctor(db.sm_doctor_visit.visit_date==prevday6)        
            number_ofDoctorPrev6 = qsetDoctorPrev6.count()
            
            #------ prevday7
            qsetDoctorPrev7=qsetDoctor(db.sm_doctor_visit.visit_date==prevday7)        
            number_ofDoctorPrev7 = qsetDoctorPrev7.count()
            
            #------ prevday8
            qsetDoctorPrev8=qsetDoctor(db.sm_doctor_visit.visit_date==prevday8)        
            number_ofDoctorPrev8 = qsetDoctorPrev8.count()
            
            #------ prevday9
            qsetDoctorPrev9=qsetDoctor(db.sm_doctor_visit.visit_date==prevday9)        
            number_ofDoctorPrev9 = qsetDoctorPrev9.count()
        
        #------------------ Call vs Order
        callVsOrderList.append({'Day':datetime.datetime.strftime(prevday9,'%d-%m-%Y'), 'Call':int(number_ofVisitRetPrevday9), 'Order':int(number_ofOrderRetrPrev9)})
        callVsOrderList.append({'Day':datetime.datetime.strftime(prevday8,'%d-%m-%Y'), 'Call':int(number_ofVisitRetPrevday8), 'Order':int(number_ofOrderRetrPrev8)})
        callVsOrderList.append({'Day':datetime.datetime.strftime(prevday7,'%d-%m-%Y'), 'Call':int(number_ofVisitRetPrevday7), 'Order':int(number_ofOrderRetrPrev7)})
        callVsOrderList.append({'Day':datetime.datetime.strftime(prevday6,'%d-%m-%Y'), 'Call':int(number_ofVisitRetPrevday6), 'Order':int(number_ofOrderRetrPrev6)})
        callVsOrderList.append({'Day':datetime.datetime.strftime(prevday5,'%d-%m-%Y'), 'Call':int(number_ofVisitRetPrevday5), 'Order':int(number_ofOrderRetrPrev5)})
        callVsOrderList.append({'Day':datetime.datetime.strftime(prevday4,'%d-%m-%Y'), 'Call':int(number_ofVisitRetPrevday4), 'Order':int(number_ofOrderRetrPrev4)})
        callVsOrderList.append({'Day':datetime.datetime.strftime(prevday3,'%d-%m-%Y'), 'Call':int(number_ofVisitRetPrevday3), 'Order':int(number_ofOrderRetrPrev3)})
        callVsOrderList.append({'Day':datetime.datetime.strftime(prevday2,'%d-%m-%Y'), 'Call':int(number_ofVisitRetPrevday2), 'Order':int(number_ofOrderRetrPrev2)})
        callVsOrderList.append({'Day':datetime.datetime.strftime(yesterday,'%d-%m-%Y'), 'Call':int(number_ofVisitRetPrevday1), 'Order':int(number_ofOrderRetrPrev1)})
        callVsOrderList.append({'Day':datetime.datetime.strftime(currentdate,'%d-%m-%Y'), 'Call':int(number_ofVisitRetqsetToday1), 'Order':int(number_ofOrderRetToday1)})
        
        orderVolumeList.append({'Day':datetime.datetime.strftime(prevday9,'%d-%m-%Y'), 'Amount':float(ordVolTotalPT9)})
        orderVolumeList.append({'Day':datetime.datetime.strftime(prevday8,'%d-%m-%Y'), 'Amount':float(ordVolTotalPT8)})
        orderVolumeList.append({'Day':datetime.datetime.strftime(prevday7,'%d-%m-%Y'), 'Amount':float(ordVolTotalPT7)})
        orderVolumeList.append({'Day':datetime.datetime.strftime(prevday6,'%d-%m-%Y'), 'Amount':float(ordVolTotalPT6)})
        orderVolumeList.append({'Day':datetime.datetime.strftime(prevday5,'%d-%m-%Y'), 'Amount':float(ordVolTotalPT5)})
        orderVolumeList.append({'Day':datetime.datetime.strftime(prevday4,'%d-%m-%Y'), 'Amount':float(ordVolTotalPT4)})
        orderVolumeList.append({'Day':datetime.datetime.strftime(prevday3,'%d-%m-%Y'), 'Amount':float(ordVolTotalPT3)})
        orderVolumeList.append({'Day':datetime.datetime.strftime(prevday2,'%d-%m-%Y'), 'Amount':float(ordVolTotalPT2)})        
        orderVolumeList.append({'Day':datetime.datetime.strftime(yesterday,'%d-%m-%Y'), 'Amount':float(ordVolTotalT2)})
        orderVolumeList.append({'Day':datetime.datetime.strftime(currentdate,'%d-%m-%Y'), 'Amount':float(ordVolTotalT1)})
        
        #====== Doctor
        if session.setting_doctor==1:
            doctorScheduleVsExceList.append({'Day':datetime.datetime.strftime(prevday9,'%d-%m-%Y'), 'Visit':int(number_ofDoctorPrev9)})
            doctorScheduleVsExceList.append({'Day':datetime.datetime.strftime(prevday8,'%d-%m-%Y'), 'Visit':int(number_ofDoctorPrev8)})
            doctorScheduleVsExceList.append({'Day':datetime.datetime.strftime(prevday7,'%d-%m-%Y'), 'Visit':int(number_ofDoctorPrev7)})
            doctorScheduleVsExceList.append({'Day':datetime.datetime.strftime(prevday6,'%d-%m-%Y'), 'Visit':int(number_ofDoctorPrev6)})
            doctorScheduleVsExceList.append({'Day':datetime.datetime.strftime(prevday5,'%d-%m-%Y'), 'Visit':int(number_ofDoctorPrev5)})
            doctorScheduleVsExceList.append({'Day':datetime.datetime.strftime(prevday4,'%d-%m-%Y'), 'Visit':int(number_ofDoctorPrev4)})
            doctorScheduleVsExceList.append({'Day':datetime.datetime.strftime(prevday3,'%d-%m-%Y'), 'Visit':int(number_ofDoctorPrev3)})
            doctorScheduleVsExceList.append({'Day':datetime.datetime.strftime(prevday2,'%d-%m-%Y'), 'Visit':int(number_ofDoctorPrev2)})        
            doctorScheduleVsExceList.append({'Day':datetime.datetime.strftime(yesterday,'%d-%m-%Y'), 'Visit':int(number_ofDoctorPrev1)})
            doctorScheduleVsExceList.append({'Day':datetime.datetime.strftime(currentdate,'%d-%m-%Y'), 'Visit':int(number_ofdoctorRecordsToday1)})
        
        
        
    #----------------
    #salesCallCount = db((db.sm_order_head.cid == session.cid)&(db.sm_order_head.ym_date == firstDate)).count()
    
    return dict(recordDictData=recordDictData,showLevelName=showLevelName,showLevelValue=showLevelValue,regionName=regionName,areaName=areaName,territoryName=territoryName,marketName=marketName,regionID=regionID,areaID=areaID,territoryID=territoryID,marketID=marketID, depth=depth, levelName=levelName, levelRows=levelRows, orderVolumeList=orderVolumeList, regionRecordShowList=regionRecordShowList, regionRecordList=regionRecordList, currentMonth=currentMonth,retailerDistrbList=retailerDistrbList,spoDistrbList=spoDistrbList,callVsOrderList=callVsOrderList,doctorScheduleVsExceList=doctorScheduleVsExceList)


