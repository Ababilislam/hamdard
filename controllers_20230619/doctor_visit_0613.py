
#====================== Doctor Visit

from random import randint
#---------------------------- ADD VALIDATION
def validation_doctor_visit_add(form):
    c_id = session.cid
    doc_id = str(form.vars.doc_id).strip().upper()
    rep_id = str(form.vars.rep_id).strip().upper()

    docName = ''
    doctorRows = db((db.sm_doctor.cid == c_id) & (db.sm_doctor.doc_id == doc_id)).select(db.sm_doctor.doc_name, limitby=(0, 1))
    if not doctorRows:
        form.errors.doc_id = 'Invalid doctor'
    else:
        docName = doctorRows[0].doc_name

        #---
        fieldForce_name = ''
        fieldForceRow = db((db.sm_rep.cid == c_id) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.name, limitby=(0, 1))
        if not fieldForceRow:
            form.errors.rep_id = 'Invalid field force'
        else:
            fieldForce_name = fieldForceRow[0].name

            form.vars.doc_id = doc_id
            form.vars.doc_name = docName
            form.vars.rep_id = rep_id
            form.vars.rep_name = fieldForce_name
            form.vars.ho_status = '0'
            form.vars.visit_dtime = datetime_fixed
            form.vars.visit_date = current_date

#---------------------------- ADD
def doctor_visit_add():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

    response.title = 'Doctor Visit'

    c_id = session.cid

    #   ---------------------
    form = SQLFORM(db.sm_doctor_visit,
                  fields=['doc_id', 'rep_id', 'feedback'],
                  submit_button='Save'
                  )

    form.vars.cid = c_id
    if form.accepts(request.vars, session, onvalidation=validation_doctor_visit_add):
       response.flash = 'Submitted Successfully'

    #  ---------------filter-------
    btn_filter_docvisit = request.vars.btn_filter
    btn_all = request.vars.btn_filter_all
    reqPage = len(request.args)
    if btn_filter_docvisit:
        session.btn_filter_docvisit = btn_filter_docvisit
        session.searchType_docvisit = str(request.vars.search_type).strip()
        session.searchValue_docvisit = str(request.vars.search_value).strip().upper()
        reqPage = 0

        if session.searchType_docvisit == 'Date':
            try:
                datetime.datetime.strptime(session.searchValue_docvisit, '%Y-%m-%d')
            except:
                session.searchValue_docvisit = ''
                response.flash = 'Invalid date format'
                
    elif btn_all:
        session.btn_filter_docvisit = None
        session.searchType_docvisit = None
        session.searchValue_docvisit = None
        reqPage = 0
        
    #--------paging
    if reqPage:
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = session.items_per_page
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    #--------end paging
    
    qset = db()
    qset = qset(db.sm_doctor_visit.cid == c_id)
    
    #---- supervisor
    if session.user_type=='Supervisor':
        level_id=session.level_id
        depthNo=session.depthNo
        level = 'level' + str(depthNo)
        
        qset=qset((db.sm_level.cid==session.cid)&(db.sm_level.is_leaf=='1')& (db.sm_level[level] == level_id)&(db.sm_level.level_id==db.sm_doctor_visit.route_id))
        
    else:
        qset=qset((db.sm_level.cid==session.cid)&(db.sm_level.is_leaf=='1')&(db.sm_level.level_id==db.sm_doctor_visit.route_id))
        
    #-----
    if session.user_type == 'Depot':
        qset = qset(db.sm_doctor_visit.depot_id == session.depot_id)
        
    #----
    if (session.btn_filter_docvisit):
        if (session.searchType_docvisit == 'DocID'):
            searchValue=str(session.searchValue_docvisit).split('|')[0]
            qset = qset(db.sm_doctor_visit.doc_id == searchValue)
            
        elif (session.searchType_docvisit == 'DepotID'):
            if session.user_type != 'Depot':
                searchValue=str(session.searchValue_docvisit).split('|')[0]
                qset = qset(db.sm_doctor_visit.depot_id == searchValue)
                
        elif (session.searchType_docvisit == 'RepID'):
            searchValue=str(session.searchValue_docvisit).split('|')[0]
            qset = qset(db.sm_doctor_visit.rep_id == searchValue)
            
        elif (session.searchType_docvisit == 'Date'):
            qset = qset(db.sm_doctor_visit.visit_date == session.searchValue_docvisit)
            
        elif (session.searchType_docvisit == 'HoStatus'):
            qset = qset(db.sm_doctor_visit.ho_status == session.searchValue_docvisit)
            
    records = qset.select(db.sm_doctor_visit.ALL, orderby= ~db.sm_doctor_visit.visit_dtime, limitby=limitby)
    totalCount=qset.count()
    
    return dict(form=form, records=records,totalCount=totalCount, page=page, items_per_page=items_per_page, access_permission=access_permission)
    
    
#---------------------------- Show visit
def preview_doctor_visit():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL('doctor_visit_add'))

    #   ---------------------
    response.title = 'Preview -Doctor Visit'

    c_id = session.cid

    page = request.args(0)
    docID = request.args(1)
    repID = request.args(2)
    depot = request.args(3)
    route = request.args(4)

    docname = request.vars.doc
    repname = request.vars.rep
    vsitdate = request.vars.vsitdt
    feedback = request.vars.feedbk
    detaildata = str(request.vars.dtldata).strip()

    proposedList = []
    giftList = []
    sampleList = []
    ppmList = []
    
    if detaildata != '':
        dataList = detaildata.split('rdsep')
        if len(dataList) == 4:
            proposedStr = dataList[0]
            giftStr = dataList[1]
            sampleStr = dataList[2]
            ppmStr = dataList[3]
            
#            return ppmStr
            #------ proposed part
            if proposedStr != '':
                itemList = proposedStr.split('fdsep')
                for i in range(len(itemList)):
                    itemIdName = str(itemList[i]).strip()

                    itemIdList = itemIdName.split(',')
                    if len(itemIdList) == 2:
                        itemID = itemIdList[0]
                        itemName = itemIdList[1]

                        itemDict = {'itemID':itemID, 'itemName':itemName}
                        proposedList.append(itemDict)

            #------ gift part
            if giftStr != '':
                gftList = giftStr.split('fdsep')
                for i in range(len(gftList)):
                    gftIdQty = str(gftList[i]).strip()

                    gftIdList = gftIdQty.split(',')
                    if len(gftIdList) == 3:
                        gftID = gftIdList[0]
                        gftName = gftIdList[1]
                        gftQty = gftIdList[2]

                        gftDict = {'gftID':gftID, 'gftName':gftName, 'gftQty':gftQty}
                        giftList.append(gftDict)

            #------ sample part
            if sampleStr != '':
                smpList = sampleStr.split('fdsep')
                for i in range(len(smpList)):
                    smpIdQty = str(smpList[i]).strip()

                    smpIdList = smpIdQty.split(',')
                    if len(smpIdList) == 3:
                        smpID = smpIdList[0]
                        smpName = smpIdList[1]
                        smpQty = smpIdList[2]

                        smpDict = {'smpID':smpID, 'smpName':smpName, 'smpQty':smpQty}
                        sampleList.append(smpDict)
        #------ gift part
            if ppmStr != '':
#                return ppmStr
                ppmList_1 = ppmStr.split('fdsep')
#                return len(ppmList)
                for i in range(len(ppmList_1)):
                    ppmIdQty = str(ppmList_1[i]).strip()
    
                    ppmIdList = ppmIdQty.split(',')
                    if len(ppmIdList) == 3:
                        ppmID = ppmIdList[0]
                        ppmName = ppmIdList[1]
                        ppmQty = ppmIdList[2]
    
                        ppmDict = {'ppmID':ppmID, 'ppmName':ppmName, 'ppmQty':ppmQty}
                        ppmList.append(ppmDict)
#                return len(ppmList)

#    return len(ppmList)
    return dict(docID=docID, repID=repID, docname=docname, repname=repname, vsitdate=vsitdate, depot=depot, route=route, feedback=feedback, proposedList=proposedList, giftList=giftList, sampleList=sampleList, ppmList=ppmList)


#====================
# cid.v.doctorid..proposed item..gift item..sample item..notes

# cid.v.doctorid..itemid1,itemid2,itemid3..giftid,qty.giftid,qty..sampleID,sampleQty..notes
# http://127.0.0.1:8000/mreporting/doctor_visit/sms_doctor_visit_submit?password=Compaq510DuoDuo&mob=8801719078552&cid=CONCORD&msg=CON.V.D00001..ACET,ACUP,ACUT..G0001,1.G0002,2..ACUP,4.ACUT,2..Item ACUT work properly
def sms_doctor_visit_submit():
    pass_get = request.vars.password
    mobile = request.vars.mob
    cid = request.vars.cid
    my_str = request.vars.msg
    msg_start = 'START'
    if (pass_get != 'Compaq510DuoDuo'):
        return msg_start + "Unauthorized sms"
    else:
        if my_str == '' or my_str == None:
            return msg_start + "Invalid sms"
        else:
            cidValue = str(cid).strip()
            errorFlag = 0
            errorMsg = ''
            dblSep = '..'
            myStrList = my_str.split(dblSep, my_str.count(dblSep))
            inboxData = str(my_str)
            if len(myStrList) != 5:
                errorFlag = 1
                errorMsg = 'Error in SMS format. Please contact with system admin for correct format.'
            else:
                try:
                    basicPart = str(myStrList[0]).strip().upper()
                    proposedPart = str(myStrList[1]).strip().upper()
                    giftPart = str(myStrList[2]).strip().upper()
                    samplePart = str(myStrList[3]).strip().upper()
                    notesPart = str(myStrList[4]).strip().upper()
                    doctorID = ''
                    docName = ''
                    routeID = ''
                    depotID = ''
                    fieldForceId = ''
                    fieldForce_name = ''
                    basicList = basicPart.split('.')
                    if len(basicList) != 3:
                        errorFlag = 1
                        errorMsg = 'Error in SMS format. Please contact with system admin for correct format.'
                    else:
                        typeValue = str(basicList[1]).strip()
                        doctorID = str(basicList[2]).strip()
                        if typeValue != 'V':
                            errorFlag = 1
                            errorMsg = 'Error in SMS format. Please contact with system admin for correct format.'
                        else:
                            doctorRows = db((db.sm_doctor.cid == cidValue) & (db.sm_doctor.doc_id == doctorID) & (db.sm_doctor.status == 'ACTIVE')).select(db.sm_doctor.doc_name, limitby=(0, 1))
                            if not doctorRows:
                                errorFlag = 1
                                errorMsg = 'Invalid doctor'
                            else:
                                docName = doctorRows[0].doc_name
                                fieldForceRow = db((db.sm_rep.cid == cidValue) & (db.sm_rep.mobile_no == mobile) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id, db.sm_rep.name, db.sm_rep.depot_id, limitby=(0, 1))
                                if not fieldForceRow:
                                    errorFlag = 1
                                    errorMsg = 'Invalid field force'
                                else:
                                    fieldForceId = fieldForceRow[0].rep_id
                                    fieldForce_name = fieldForceRow[0].name
                                    depotID = fieldForceRow[0].depot_id
                                    settRows = db((db.sm_settings.cid == cidValue) & (db.sm_settings.s_key == 'DOCTOR_ROUTE_CHECK') & (db.sm_settings.s_value == 'YES')).select(db.sm_settings.s_value, limitby=(0, 1))
                                    if settRows:
                                        docRouteRows = db((db.sm_doctor_area.cid == cidValue) & (db.sm_doctor_area.doc_id == doctorID)).select(db.sm_doctor_area.area_id, db.sm_doctor_area.area_name, limitby=(0, 1))
                                        if not docRouteRows:
                                            errorFlag = 1
                                            errorMsg = 'Invalid route for the doctor'
                                        else:
                                            routeID = docRouteRows[0].area_id
                                    else:
                                        pass
                        #----- proposed part
                        proposedStr = ''
                        if errorFlag == 0:
                            if proposedPart != '':
                                itemRows = db(db.sm_item.cid == cidValue).select(db.sm_item.item_id, db.sm_item.name, db.sm_item.category_id, orderby=db.sm_item.item_id)
                                propItemList = proposedPart.split(',')
                                for i in range(len(propItemList)):
                                    itemID = str(propItemList[i]).strip()
                                    validItemId = False
                                    for itemRow in itemRows:
                                        itemId = str(itemRow.item_id).strip()
                                        itemName = itemRow.name
                                        if itemId == itemID:
                                            validItemId = True
                                            break
                                    if validItemId == False:
                                        itemRows = ''
                                        errorFlag = 1
                                        errorMsg = 'Invalid Item ID %s' % (itemID)
                                        break
                                    else:
                                        if proposedStr == '':
                                            proposedStr = itemID + ',' + str(itemName).replace(',', ' ')
                                        else:
                                            proposedStr += 'fdsep' + itemID + ',' + str(itemName).replace(',', ' ')
                                itemRows = ''
                        #------------- gift part
                        giftStr = ''
                        if errorFlag == 0:
                            if giftPart != '':
                                giftRows = db((db.sm_doctor_gift.cid == cidValue)).select(db.sm_doctor_gift.gift_id, db.sm_doctor_gift.gift_name)
                                giftList = giftPart.split('.')
                                for i in range(len(giftList)):
                                    gftIdQty = str(giftList[i]).strip()
                                    gftIdList = gftIdQty.split(',')
                                    if len(gftIdList) != 2:
                                        giftRows = ''
                                        errorFlag = 1
                                        errorMsg = 'Invalid gift,quantity format in SMS'
                                        break
                                    else:
                                        gftID = str(gftIdList[0]).strip()
                                        validGift = False
                                        for gftRow in giftRows:
                                            giftId = str(gftRow.gift_id).strip()
                                            giftName = gftRow.gift_name
                                            if giftId == gftID:
                                                validGift = True
                                                break
                                        if validGift == False:
                                            giftRows = ''
                                            errorFlag = 1
                                            errorMsg = 'Invalid gift ID %s' % (gftID)
                                            break
                                        else:
                                            gftQty = gftIdList[1]
                                            if gftQty.isdigit():
                                                pass
                                            else:
                                                giftRows = ''
                                                errorFlag = 1
                                                errorMsg = 'Invalid quantity for gift ID %s' % (gftID)
                                                break

                                            if giftStr == '':
                                                giftStr = gftID + ',' + str(giftName).replace(',', ' ') + ',' + str(gftQty)
                                            else:
                                                giftStr += 'fdsep' + gftID + ',' + str(giftName).replace(',', ' ') + ',' + str(gftQty)
                                giftRows = ''
                        #----- sample part
                        sampleStr = ''
                        if errorFlag == 0:
                            if samplePart != '':
                                sampleRows = db(db.sm_item.cid == cidValue).select(db.sm_item.item_id, db.sm_item.name, db.sm_item.category_id, orderby=db.sm_item.item_id)
                                sampleList = samplePart.split('.')
                                for i in range(len(sampleList)):
                                    smpIdQty = str(sampleList[i]).strip()
                                    smpIdList = smpIdQty.split(',')
                                    if len(smpIdList) != 2:
                                        sampleRows = ''
                                        errorFlag = 1
                                        errorMsg = 'Invalid sample,quantity format in SMS'
                                        break
                                    else:
                                        smpID = str(smpIdList[0]).strip()
                                        validSample = False
                                        for smpRow in sampleRows:
                                            smpId = str(smpRow.item_id).strip()
                                            smpName = smpRow.name
                                            if smpId == smpID:
                                                validSample = True
                                                break

                                        if validSample == False:
                                            sampleRows = ''
                                            errorFlag = 1
                                            errorMsg = 'Invalid sample ID %s' % (smpID)
                                            break
                                        else:
                                            smpQty = smpIdList[1]
                                            if smpQty.isdigit():
                                                pass
                                            else:
                                                sampleRows = ''
                                                errorFlag = 1
                                                errorMsg = 'Invalid quantity for sample ID %s' % (smpID)
                                                break

                                            if sampleStr == '':
                                                sampleStr = smpID + ',' + str(smpName).replace(',', ' ') + ',' + str(smpQty)
                                            else:
                                                sampleStr += 'fdsep' + smpID + ',' + str(smpName).replace(',', ' ') + ',' + str(smpQty)
                                sampleRows = ''
                except:
                    errorFlag = 1
                    errorMsg = 'Error in Process.'

            #=================Get sl for inbox
            sl_inbox = 0
            rows_check = db(db.sm_doctor_inbox.cid == cidValue).select(db.sm_doctor_inbox.sl, orderby= ~db.sm_doctor_inbox.sl, limitby=(0, 1))
            if rows_check:
                last_sl = int(rows_check[0].sl)
                sl_inbox = last_sl + 1
            else:
                sl_inbox = 1
            if errorFlag == 1:
                inbox_insert = db.sm_doctor_inbox.insert(cid=cidValue, sl=sl_inbox, mobile_no=mobile, sms=inboxData, status='ERROR', error_in_sms=errorMsg)
                return msg_start + errorMsg
            else:
                if (proposedStr == '' and giftStr == '' and sampleStr == ''):
                    itemngiftnsample = ''
                else:
                    itemngiftnsample = proposedStr + 'rdsep' + giftStr + 'rdsep' + sampleStr
                insRes = db.sm_doctor_visit.insert(cid=cidValue, doc_id=doctorID, doc_name=docName, rep_id=fieldForceId, rep_name=fieldForce_name, feedback=notesPart, ho_status='0', route_id=routeID, depot_id=depotID, visit_dtime=datetime_fixed, visit_date=current_date, giftnsample=itemngiftnsample)
                if insRes:
                    inbox_insert = db.sm_doctor_inbox.insert(cid=cidValue, sl=sl_inbox, mobile_no=mobile, sms=inboxData, status='SUCCESS')
                    return str(msg_start) + 'Success'
                else:
                    return str(msg_start) + 'Error in process'
    return ''

def doctor_inbox():
    task_id = 'rm_doctor_inbox_manage'
    access_permission = check_role(task_id)
    if (access_permission == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

    response.title = 'Doctor-Inbox'

    c_id = session.cid

    #======================
    #------------------------
    btn_filter_docinb = request.vars.btn_filter
    btn_all = request.vars.btn_all
    argslen = len(request.args)

    if btn_filter_docinb:
        session.btn_filter_docinb = btn_filter_docinb
        session.search_type_docinb = request.vars.search_type
        session.search_value_docinb = request.vars.search_value
        argslen = 0

    elif btn_all:
        session.search_type_docinb = None
        session.search_value_docinb = None
        argslen = 0

    #--------paging
    if argslen:
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = session.items_per_page
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    #--------end paging

    # Set text for filter

    qset = db()
    qset = qset(db.sm_doctor_inbox.cid == c_id)

    if (session.btn_filter_docinb):
        if (session.search_type_docinb == 'MobileNo'):
            qset = qset(db.sm_doctor_inbox.mobile_no == session.search_value_docinb)

        elif (session.search_type_docinb == 'Status'):
            qset = qset(db.sm_doctor_inbox.status == str(session.search_value_docinb).strip().upper())


    records = qset.select(db.sm_doctor_inbox.ALL, orderby= ~db.sm_doctor_inbox.id, limitby=limitby)

    #------------------------------------ filter end--------------------

    return dict(records=records, page=page, items_per_page=items_per_page, access_permission=access_permission)
    #---------------end  ---------------------


#visit plan
def doctor_visit_plan():
    #----------Task assaign----------
    task_id='rm_doctor_visit_plan_manage'
    task_id_view='rm_doctor_visit_plan_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    #   ---------------------
    response.title='Doctor Visit Plan'
    cid=session.cid
    
    #If catagorey not in item it can be delete
    btn_approved_filter=request.vars.btn_approved_filter
    btn_approved=request.vars.btn_approved
    if btn_approved_filter or btn_approved:  
        yearValue=request.vars.yearValue
        monthValue=request.vars.monthValue      
        spo_idname=request.vars.spo_idname
        
        if (yearValue=='' or monthValue=='' or spo_idname==''):
            response.flash='Value Required'
        else:
            if btn_approved_filter:
                spo_id=str(spo_idname).split('|')[0]
                if spo_id=='':
                    response.flash='Invalid SPO'
                else:
                    validRep=True
                    if session.user_type=='Supervisor': #not used because supervisor also have visit plan
                        if spo_id!=session.user_id:                        
                            repAreaRow=db((db.sm_rep_area.cid==cid) & (db.sm_rep_area.rep_id==spo_id) & (db.sm_rep_area.area_id.belongs(session.marketList))).select(db.sm_rep_area.rep_id,limitby=(0,1))
                            if not repAreaRow:
                                response.flash='SPO-Client/Retailer not available'
                                validRep=False
                    
                    if validRep==True:                    
                        session.yearValue=yearValue
                        session.monthValue=monthValue
                        session.spo_idname=spo_idname
                        session.spo_id=spo_id
                        
                        session.btn_approved_filter=btn_approved_filter
                        session.btn_filter_vp=None
                        session.search_type_vp=None
                        session.search_value_vp=None
    
    #Cancelled
#    btn_delete=request.vars.btn_delete
#    if btn_delete:
#        record_id=request.args[1]
#        check_cancel=request.vars.check_cancel
#        if check_cancel!='YES':
#            response.flash='Check Confirmation Required'
#        else:
#            planRecords=db((db.sm_visit_plan.cid==cid)& (db.sm_visit_plan.id==record_id) & (db.sm_visit_plan.status=='Submitted')).select(db.sm_visit_plan.id,limitby=(0,1))
#            if planRecords:
#                planRecords[0].update_record(status='Cancelled')
#            else:
#                response.flash='Invalid request'
    
    #------------------filter
    btn_filter_vp=request.vars.btn_filter
    btn_filter_vp_all=request.vars.btn_all
    reqPage=len(request.args)
    if btn_filter_vp:
        session.btn_filter_vp=btn_filter_vp
        session.search_type_vp=request.vars.search_type
        session.search_value_vp=str(request.vars.search_value).strip().upper()
        
        session.btn_approved_filter=None
        session.yearValue=None
        session.monthValue=None
        session.spo_idname=None
        session.spo_id=None
        
        reqPage=0
        
    elif btn_filter_vp_all:
        session.btn_filter_vp=None
        session.search_type_vp=None
        session.search_value_vp=None
        
        session.btn_approved_filter=None
        session.yearValue=None
        session.monthValue=None
        session.spo_idname=None
        session.spo_id=None
        
        reqPage=0
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=30
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging    
    
    qset=db()
    qset=qset(db.sm_doctor_visit_plan.cid==cid)
    if session.user_type=='Depot':
        qset=qset(db.sm_doctor_visit_plan.depot_id==session.depot_id)    
    else:
        if (session.btn_filter_vp and session.search_type_vp=='DepotID'):
            searchValue=str(session.search_value_vp).split('|')[0]
            qset=qset(db.sm_doctor_visit_plan.depot_id==searchValue)
    
    
    #---- supervisor
    if session.user_type=='Supervisor':
        qset=qset(db.sm_doctor_visit_plan.route_id.belongs(session.marketList))
    else:
        pass
    #----
    
    if session.btn_filter_vp:
        if (session.search_type_vp=='RepID'):
            searchValue=str(session.search_value_vp).split('|')[0]
            qset=qset(db.sm_doctor_visit_plan.rep_id==searchValue)
            
        elif (session.search_type_vp=='DoctorID'):
            searchValue=str(session.search_value_vp).split('|')[0]
            qset=qset(db.sm_doctor_visit_plan.doc_id==searchValue)
            
        elif (session.search_type_vp=='AreaID'):
            searchValue=str(session.search_value_vp).split('|')[0]
            qset=qset(db.sm_doctor_visit_plan.route_id==searchValue)
            
        elif (session.search_type_vp=='Status'):
            qset=qset(db.sm_doctor_visit_plan.status==session.search_value_vp)
            
        elif (session.search_type_vp=='VisitedFlag'):
            try:
                searchValue=int(session.search_value_vp) 
            except:
                searchValue=''
            
            qset=qset(db.sm_doctor_visit_plan.visited_flag==searchValue)
    
    elif session.btn_approved_filter:
        first_date=str(session.yearValue)+'-'+str(session.monthValue)+'-01'
        rep_id=session.spo_id
        qset=qset((db.sm_doctor_visit_plan.first_date==first_date)&(db.sm_doctor_visit_plan.rep_id==rep_id))
        
        if btn_approved:
            planRecords=qset(db.sm_doctor_visit_plan.status=='Submitted').count()
            if planRecords>0:
                updateRecords=qset(db.sm_doctor_visit_plan.status=='Submitted').update(status='Approved')
            else:
                response.flash='Data not available'
                
    records=qset.select(db.sm_doctor_visit_plan.ALL,orderby=~db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.doc_id,limitby=limitby) 
    
    return dict(records=records,page=page,items_per_page=items_per_page,access_permission=access_permission,access_permission_view=access_permission_view)
    
#=== Not completed because of checking rep and doctor route
def doctor_visit_plan_batch_upload():
    task_id='rm_doctor_visit_plan_manage'
    access_permission=check_role(task_id)
    if access_permission==False:
        session.flash='Access is Denied !'
        redirect (URL('doctor_visit_plan'))
    
    response.title='Visit Plan Batch Upload'
    
    c_id=session.cid
    
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
        
        rep_list_excel=[]
        doctor_list_excel=[]
        doctor_list_exist=[]
        rep_list_exist=[]
        
        excelList=[]
        
        area_list_excel=[]
        existLevel_list=[]
        
        ins_list=[]
        ins_dict={}
        
        for i in range(total_row):
            if i>=30:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==3:
                    rep_list_excel.append(str(coloum_list[1]).strip().upper())
                    doctor_list_excel.append(str(coloum_list[2]).strip().upper())
        
        #        create rep list
        existRepRows=db((db.sm_rep.cid==c_id)&(db.sm_rep.rep_id.belongs(rep_list_excel))&(db.sm_rep.status=='ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.depot_id,orderby=db.sm_rep.rep_id)
        rep_list_exist=existRepRows.as_list()            
        
        #        create client list        
        existClientRows=db((db.sm_doctor.cid==c_id)&(db.sm_doctor.doc_id.belongs(doctor_list_excel))&(db.sm_doctor.status=='ACTIVE')).select(db.sm_doctor.doc_id,db.sm_doctor.doc_name,orderby=db.sm_doctor.doc_id)
        doctor_list_exist=existClientRows.as_list()
        
        #   --------------------
        for i in range(total_row):
            if i>=30:
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')
            
            if len(coloum_list)!=3:
                error_data=row_data+'(3 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
            else:
                date_ex=str(coloum_list[0]).strip()
                spo_id_ex=str(coloum_list[1]).strip().upper()
                docID_ex=str(coloum_list[2]).strip().upper()
                
                if (docID_ex=='' or spo_id_ex==''):
                    error_data=row_data+'(Must value required)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                else:                                        
                    try:
                        date_ex=datetime.datetime.strptime(date_ex,'%Y-%m-%d')
                    except:
                        error_data=row_data+'(Invalid date)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    
                    #-----------------------
                    valid_rep=False
                    valid_doctor=False
                    
                    firstDate=str(date_ex)[0:7]+'-01'
                    repName=''
                    depot_id=''
                    doctorName=''
                    area_id=''
                    
                    #----------- check valid spo                                                      
                    for i in range(len(rep_list_exist)):
                        myRowData1=rep_list_exist[i]                                
                        rep_id=myRowData1['rep_id']
                        if (str(rep_id).strip()==str(spo_id_ex).strip()):
                            valid_rep=True
                            repName=myRowData1['name']
                            depot_id=myRowData1['depot_id']
                            break
                    
                    if valid_rep==True:#---------- check valid client
                        for i in range(len(doctor_list_exist)):
                            myRowData2=doctor_list_exist[i]                        
                            client_id=myRowData2['doc_id']                            
                            if (str(client_id).strip()==str(docID_ex).strip()):
                                valid_doctor=True
                                doctorName=myRowData2['doc_name']                  
                                break
                    
                    #------------
#                    if session.user_type=='Supervisor':
#                        repAreaRow=db((db.sm_rep_area.cid==c_id) & (db.sm_rep_area.rep_id==spo_id_ex) & (db.sm_rep_area.area_id.belongs(session.marketList))).select(db.sm_rep_area.rep_id,limitby=(0,1))
#                        if not repAreaRow:
#                            error_data=row_data+'(SPO not accessed!)\n'
#                            error_str=error_str+error_data
#                            count_error+=1
#                            continue
#                        else:
#                            pass
#                        
#                        #----
#                        sueprvisorMarketList=session.marketList
#                        if area_id not in sueprvisorMarketList:
#                            error_data=row_data+'(Retailer not accessed!)\n'
#                            error_str=error_str+error_data
#                            count_error+=1
#                            continue
#                        else:
#                            pass
#                    else:
#                        pass
                    #-----------
                    
                    
                    #--- Upload Pending because of rep-market and doctor-market checking and if rep multiple route but doctor multiple route not value doctor which route
                    
                    if valid_doctor==True:#---------- check valid spo-market
                        
                        rep_areaRow=db((db.sm_rep_area.cid==c_id) & (db.sm_rep_area.rep_id==spo_id_ex)).select(db.sm_rep_area.area_id,limitby=(0,1))
                        if not rep_areaRow :
                            error_data=row_data+'(Rep-Client/Retailer required)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:
                            area_id=rep_areaRow[0].area_id                            
                            if session.user_type=='Supervisor':
                                if area_id not in session.marketList:
                                    error_data=row_data+'(Unauthorized Rep)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue
                    
                    #-----------------
                    if(valid_rep==False):
                        error_data=row_data+'(Invalid Rep)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue                        
                    else:
                        if valid_doctor==False:
                            error_data=row_data+'(Invalid Doctor)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:
                            existRow=db((db.sm_doctor_visit_plan.cid==c_id) & (db.sm_doctor_visit_plan.rep_id==spo_id_ex) & (db.sm_doctor_visit_plan.schedule_date==date_ex) & (db.sm_doctor_visit_plan.doc_id==docID_ex) & (db.sm_doctor_visit_plan.status!='Cancelled')).select(db.sm_doctor_visit_plan.rep_id,limitby=(0,1))    
                            if existRow :
                                error_data=row_data+'(Already exist)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                            else:
                                #Create insert list
                                routeRow=db((db.sm_level.cid==c_id) & (db.sm_level.level_id==area_id) & (db.sm_level.is_leaf=='1')).select(db.sm_level.level_name,db.sm_level.level0,db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
                                if not routeRow:
                                    error_data=row_data+'(Invalid Market in Doctor)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue                                
                                else:
                                    market_name=routeRow[0].level_name                                    
                                    level0_id=routeRow[0].level0
                                    level1_id=routeRow[0].level1
                                    level2_id=routeRow[0].level2
                                    
                                    level0_name=''                    
                                    level1_name=''
                                    level2_name=''
                                    
#                                    depotRow=db((db.sm_depot.cid==c_id) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.name,limitby=(0,1))
#                                    if depotRow:
#                                        depot_name=depotRow[0].name
                                    
                                    level0Row=db((db.sm_level.cid==c_id) & (db.sm_level.level_id==level0_id) & (db.sm_level.is_leaf=='0')).select(db.sm_level.level_name,limitby=(0,1))
                                    if level0Row:
                                        level0_name=level0Row[0].level_name
                                        
                                    level1Row=db((db.sm_level.cid==c_id) & (db.sm_level.level_id==level1_id) & (db.sm_level.is_leaf=='0')).select(db.sm_level.level_name,limitby=(0,1))
                                    if level1Row:
                                        level1_name=level1Row[0].level_name
                                        
                                    level2Row=db((db.sm_level.cid==c_id) & (db.sm_level.level_id==level2_id) & (db.sm_level.is_leaf=='0')).select(db.sm_level.level_name,limitby=(0,1))
                                    if level2Row:
                                        level2_name=level2Row[0].level_name
                                        
                                try:
                                    ins_dict= {'cid':c_id,'rep_id':spo_id_ex,'rep_name':repName,'first_date':firstDate,'schedule_date':date_ex,'doc_id':docID_ex,'doc_name':clientName,'route_id':area_id,'route_name':market_name,'depot_id':depot_id,
                                               'depot_name':depot_name,'level2_id':level2_id,'level2_name':level2_name,'level1_id':level1_id,'level1_name':level1_name,'level0_id':level0_id,'level0_name':level0_name}
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
            inCountList=db.sm_doctor_visit_plan.bulk_insert(ins_list)             
            
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)
def download_doctor_visit_plan():
    task_id='rm_doctor_visit_plan_manage'
    task_id_view='rm_doctor_visit_plan_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('doctor_visit_plan'))      
    
    #   ---------------------
    c_id=session.cid
    
    records=''
    qset=db()
    qset=qset(db.sm_doctor_visit_plan.cid==c_id)
    if session.user_type=='Depot':
        qset=qset(db.sm_doctor_visit_plan.depot_id==session.depot_id)    
    else:
        if (session.btn_filter_vp and session.search_type_vp=='DepotID'):
            searchValue=str(session.search_value_vp).split('|')[0]
            qset=qset(db.sm_doctor_visit_plan.depot_id==searchValue)
    
    
    #---- supervisor
    if session.user_type=='Supervisor':
        qset=qset(db.sm_doctor_visit_plan.route_id.belongs(session.marketList))
    else:
        pass
    #----
    
    if session.btn_filter_vp:
        if (session.search_type_vp=='DoctorID'):
            searchValue=str(session.search_value_vp).split('|')[0]
            qset=qset(db.sm_doctor_visit_plan.doc_id==searchValue)
            
        elif (session.search_type_vp=='AreaID'):
            searchValue=str(session.search_value_vp).split('|')[0]
            qset=qset(db.sm_doctor_visit_plan.route_id==searchValue)
        
        else:
            session.flash='Need filter by Year-Month-Rep or Doctor'
            redirect(URL('doctor_visit_plan'))
    
    elif session.btn_approved_filter:
        first_date=str(session.yearValue)+'-'+str(session.monthValue)+'-01'
        rep_id=session.spo_id
        qset=qset((db.sm_doctor_visit_plan.first_date==first_date)&(db.sm_doctor_visit_plan.rep_id==rep_id))
         
    else:
        session.flash='Need filter by Year-Month-Rep or Doctor'
        redirect(URL('doctor_visit_plan'))
    
    records=qset.select(db.sm_doctor_visit_plan.ALL,orderby=~db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.rep_id|db.sm_doctor_visit_plan.doc_id) 
    
    #---------
    myString='Doctor Visit Plan \n\n'
    myString+='Schedule date,Rep ID,Rep Name,Doctor ID,Doctor Name,Market ID,Market Name,Depot ID,Depot Name,Visited?,Visit Sl,Visit Date,Status\n'
    for rec in records:
        schedule_date=str(rec.schedule_date)
        rep_id=str(rec.rep_id)
        rep_name=str(rec.rep_name).replace(',', ' ')
        doc_id=str(rec.doc_id)
        doc_name=str(rec.doc_name).replace(',', ' ')
        route_id=str(rec.route_id)
        route_name=str(rec.route_name).replace(',', ' ')
        
        depot_id=str(rec.depot_id)
        depot_name=str(rec.depot_name).replace(',', ' ')
        visited_flag=str(rec.visited_flag)
        visit_sl=str(rec.visit_sl)
        visit_date=str(rec.visit_date)
        status=str(rec.status)
        
        myString+=schedule_date+','+rep_id+','+rep_name+','+client_id+','+client_name+','+route_id+','+route_name+','+depot_id+','+depot_name+','+visited_flag+','+visit_sl+','+visit_date+','+status+'\n'
        
    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_doctor_visit_plan.csv'   
    return str(myString)


#visit plan
def doctor_visit_plan_approve():
    #----------Task assaign----------
    task_id='rm_doctor_visit_plan_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('doctor_visit_plan'))
    
    #   ---------------------
    response.title='Doctor Visit Plan Approve'
    cid=session.cid
    
    #If catagorey not in item it can be delete
    btn_approved_filter=request.vars.btn_approved_filter    
    btn_filter_vp_all=request.vars.btn_all
    
    btn_approved=request.vars.btn_approved
    btn_delete=request.vars.btn_delete
    
    if btn_approved_filter:  
        yearValue=request.vars.yearValue
        monthValue=request.vars.monthValue      
        spo_idname=request.vars.spo_idname
        
        if (yearValue=='' or monthValue=='' or spo_idname==''):
            response.flash='Value Required'
        else:
            spo_id=str(spo_idname).split('-')[0]
            if spo_id=='':
                response.flash='Invalid SPO'
            else:
                validRep=True
                if session.user_type=='Supervisor': #not used because supervisor also have visit plan
                    if spo_id!=session.user_id:                        
                        repAreaRow=db((db.sm_rep_area.cid==cid) & (db.sm_rep_area.rep_id==spo_id) & (db.sm_rep_area.area_id.belongs(session.marketList))).select(db.sm_rep_area.rep_id,limitby=(0,1))
                        if not repAreaRow:
                            response.flash='SPO-Client/Retailer not available'
                            validRep=False
                
                if validRep==True:
                    session.yearValue=yearValue
                    session.monthValue=monthValue
                    session.spo_idname=spo_idname
                    session.spo_id=spo_id
                    
                    session.btn_approved_filter=btn_approved_filter
                    session.btn_filter_vp=None
                    session.search_type_vp=None
                    session.search_value_vp=None
    
    elif btn_filter_vp_all:
        session.btn_filter_vp=None
        session.search_type_vp=None
        session.search_value_vp=None
        
        session.btn_approved_filter=None
        session.yearValue=None
        session.monthValue=None
        session.spo_idname=None
        session.spo_id=None
    
    
    #Approve or Cancelled
    if btn_approved or btn_delete:
        vslList=[]
        vslList=request.vars.vslList
        
        if vslList==None:
            response.flash='need checked record'            
        else:            
            idList=[]
            for i in range(len(vslList)):
                req_id=str(vslList[i]).strip()        
                if req_id=='0':            
                    continue
                
                idList.append(req_id)
               
            if len(idList)>0:
                if btn_approved:
                    planRecords=db((db.sm_doctor_visit_plan.cid==cid)& (db.sm_doctor_visit_plan.id.belongs(idList)) & (db.sm_doctor_visit_plan.status=='Submitted')).update(status='Approved')
                    response.flash=str(planRecords)+ ' Records approved successfully'
                
                elif btn_delete:
                    planRecords=db((db.sm_doctor_visit_plan.cid==cid)& (db.sm_doctor_visit_plan.id.belongs(idList)) & (db.sm_doctor_visit_plan.status=='Submitted')).update(status='Cancelled')
                    response.flash=str(planRecords)+ ' Records Cancelled successfully'
            
            else:
                response.flash='Checked required'
    
    #--------
    records=''
    
    if session.btn_approved_filter:
        first_date=str(session.yearValue)+'-'+str(session.monthValue)+'-01'
        rep_id=session.spo_id
        
        qset=db()
        qset=qset(db.sm_doctor_visit_plan.cid==cid)
        if session.user_type=='Depot':
            qset=qset(db.sm_doctor_visit_plan.depot_id==session.depot_id)    
        
        #---- supervisor
        if session.user_type=='Supervisor':
            qset=qset(db.sm_doctor_visit_plan.route_id.belongs(session.marketList))
        else:
            pass
        #----
        
        qset=qset((db.sm_doctor_visit_plan.first_date==first_date)&(db.sm_doctor_visit_plan.rep_id==rep_id))
        
        records=qset.select(db.sm_doctor_visit_plan.ALL,orderby=~db.sm_doctor_visit_plan.schedule_date|db.sm_doctor_visit_plan.doc_id) 
    
    yearMonth=''
    if not(session.yearValue=='' or session.yearValue==None or session.monthValue=='' or session.monthValue==None):
        first_date=str(session.yearValue)+'-'+str(session.monthValue)+'-01'
        
        yearMonth=datetime.datetime.strptime(first_date,'%Y-%m-%d').strftime('%Y-%b')
        
        
    return dict(records=records,yearMonth=yearMonth,access_permission=access_permission)




#------------------------
def prescription_list():
    task_id_view = 'rm_doctor_visit_view'
    access_permission_view = check_role(task_id_view)
    if (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))
        
    response.title = 'Prescription List'
    
    c_id = session.cid
    #   ---------------------
    
    #  ---------------filter-------
    btn_filter_prescription = request.vars.btn_filter
    btn_all = request.vars.btn_filter_all
    reqPage = len(request.args)
    if btn_filter_prescription:
        session.btn_filter_prescription = btn_filter_prescription
        session.searchType_prescription = str(request.vars.search_type).strip()
        searchValue_prescription = str(request.vars.search_value).strip().upper()
        reqPage = 0
        
        
        if (session.searchType_prescription == 'Date'):
            try:
                searchValue_prescription=datetime.datetime.strptime(str(searchValue_prescription),'%Y-%m-%d').strftime('%Y-%m-%d')
            except:
                searchValue_prescription=''
                
        session.searchValue_prescription=searchValue_prescription
        
    elif btn_all:
        session.btn_filter_prescription = None
        session.searchType_prescription = None
        session.searchValue_prescription = None
        reqPage = 0
        
    #--------paging
    if reqPage:
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = session.items_per_page
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    #--------end paging

    qset=db()
    qset = qset(db.sm_prescription_head.cid == c_id)
    
    #---- supervisor
#    if session.user_type=='Supervisor':
#        level_id=session.level_id
#        depthNo=session.depthNo
#        level = 'level' + str(depthNo)
#        
#        qset=qset((db.sm_level.cid==session.cid)&(db.sm_level.is_leaf=='1')& (db.sm_level[level] == level_id)&(db.sm_level.level_id==db.sm_doctor_area.area_id))
#        
#    else:
#        qset=qset((db.sm_level.cid==session.cid)&(db.sm_level.is_leaf=='1')&(db.sm_level.level_id==db.sm_doctor_area.area_id))
    
    #---- 
#    if session.user_type=='Depot':
#        qset=qset(db.sm_prescription_head.depot_id==session.depot_id)
    #----
    
    
            
    if (session.btn_filter_prescription):
        if (session.searchType_prescription == 'DocID'):
            searchValue=str(session.searchValue_prescription).split('|')[1]
            qset = qset(db.sm_prescription_head.doctor_name == searchValue)
        
        elif (session.searchType_prescription == 'RepID'):
            searchValue=str(session.searchValue_prescription).split('|')[0]
            qset = qset(db.sm_prescription_head.submit_by_id == searchValue)
            
        elif (session.searchType_prescription == 'Date'):
            qset = qset(db.sm_prescription_head.submit_date == session.searchValue_prescription)
                
    records = qset.select(db.sm_prescription_head.ALL, orderby=~db.sm_prescription_head.sl, limitby=limitby)    
    totalCount=qset.count()
    
    
    return dict(records=records,totalCount=totalCount, page=page, items_per_page=items_per_page)


#------------------------
def prescription_details():
    task_id_view = 'rm_doctor_visit_view'
    access_permission_view = check_role(task_id_view)
    if (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL('prescription_list'))
        
    #   ---------------------
    response.title = 'Prescription Details'
    
    c_id = session.cid
    
    page = request.args(0)
    rowid = request.args(1)
    
    headRow = db((db.sm_prescription_head.cid == c_id) & (db.sm_prescription_head.id == rowid)).select(db.sm_prescription_head.ALL, limitby=(0, 1))
    if not headRow:
        session.flash = 'Invalid request'
        redirect (URL('prescription_list'))
    else: 
        hsl=headRow[0].sl
        
        detailsRow = db((db.sm_prescription_details.cid == c_id) & (db.sm_prescription_details.sl == hsl)).select(db.sm_prescription_details.ALL)
        
    return dict(page=page, headRow=headRow,detailsRow=detailsRow)





