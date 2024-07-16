
import urllib2
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)



def sba_outlet_activities():

    task_id = 'sba_outlet_activities_Manage'
    task_id_view = 'sba_outlet_activities_View_settings'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if access_permission == False and access_permission_view == False:
        session.flash = 'Access is Denied'
        redirect(URL('default', 'home'))


    response.title = 'Outlet Target'

    btn_filter = request.vars.btn_filter
    btn_all = request.vars.btn_all
    reqPage = len(request.args)
    search_form = SQLFORM(db.sm_search_date)

    usagesTown = request.vars.usagesTown
    if (usagesTown != ''):
        usagesTownList = str(usagesTown).split('|')
        if len(usagesTownList) > 1:
            session.sba_visit_towncode_out = usagesTownList[1]
        else:
            session.sba_visit_towncode_out = usagesTown
    if session.sba_visit_towncode_out == None:
        session.sba_visit_towncode_out = ''

    if btn_filter:
        session.btn_filter = btn_filter
        session.searchTypeSBA_outlet_act = str(request.vars.searchTypeSBA_outlet_act).strip()
        session.searchValueSBA_outlet_act = str(request.vars.searchValueSBA_outlet_act).strip()


        if session.searchTypeSBA_Visit_list=='RepId':
            fflist=session.searchValueSBA_outlet_act.split('|')
            if len(fflist)>=1:
                session.searchValueSBA_outlet_act=fflist[0]


        elif session.searchTypeSBA_outlet_act == 'RepMobile':
            ff_list = session.searchValueSBA_outlet_act
            if len(ff_list) == 10:
                session.searchValueSBA_outlet_act = '880' + ff_list
            elif len(ff_list) == 11:
                session.searchValueSBA_outlet_act = '88' + ff_list
            else:
                session.searchValueSBA_outlet_act = ff_list
        elif session.searchTypeSBA_outlet_act == 'shopperMobile':
            ff_list = session.searchValueSBA_outlet_act
            if len(ff_list) == 10:
                session.searchValueSBA_outlet_act = '880' + ff_list
            elif len(ff_list) == 11:
                session.searchValueSBA_outlet_act = '88' + ff_list
            else:
                session.searchValueSBA_outlet_act = ff_list

        elif session.searchTypeSBA_outlet_act == 'town_code':
            townlistS = session.searchValueSBA_outlet_act
            townlist = session.searchValueSBA_outlet_act.split('|')
            if len(townlist) > 1:
                session.searchValueSBA_outlet_act = townlist[1]
            else:
                session.searchValueSBA_outlet_act = townlistS

        elif session.searchTypeSBA_outlet_act == 'route':
            routelist = session.searchValueSBA_outlet_act.split('|')
            if len(routelist) >= 1:
                session.searchValueSBA_outlet_act = routelist[0]

        elif session.searchTypeSBA_outlet_act == 'outlet_code':
            routelist = session.searchValueSBA_outlet_act.split('|')
            if len(routelist) >= 1:
                session.searchValueSBA_outlet_act = routelist[0]
        elif session.searchTypeSBA_outlet_act == 'sllist':
            sllist = session.searchValueSBA_outlet_act.split('|')
            if len(sllist) >= 1:
                session.searchValueSBA_outlet_act = sllist[0]
        else:
            session.searchValueSBA_outlet_act = session.searchValueSBA_outlet_act
        reqPage=0

    elif btn_all:
        session.btn_filter = None
        session.searchTypeSBA_outlet_act = None
        session.searchValueSBA_outlet_act = None
        session.sba_visit_towncode_out=''

        reqPage = 0
        region = ''



    # --------paging
    if reqPage:
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = session.items_per_page
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # --------end paging

    townList = []
    town_code = str(session.town_code)[1:-1].split('|')
    if len(town_code) > 1:
        for i in range(len(town_code)):
            townList.append(town_code[i])

    qset = db()
    if session.town_code != '':
        if session.town_code != 'ALL':
            if len(town_code) > 1:
                qset = qset(db.sb_outlet_activities_visit.town_code.belongs(townList))
            else:
                qset = qset(db.sb_outlet_activities_visit.town_code == session.town_code)

    if ((session.btn_filter) and (session.sba_visit_towncode_out!='')):
        qset=qset(db.sb_outlet_activities.town_code==session.sba_visit_towncode_out)

    # if (session.from_DtSBA_visit != '' and session.to_DtSBA_visit != ''):
    #     endDate = datetime.datetime.strptime(str(session.to_DtSBA_visit), '%Y-%m-%d')
    #     endDT = endDate + datetime.timedelta(days=1)
    #     qset = qset((db.sb_outlet_activities_visit.created_on >= session.from_DtSBA_visit) & (db.sb_outlet_activities_visit.created_on < endDT))

    if ((session.btn_filter) and (session.searchTypeSBA_outlet_act=='RepId')):
        qset=qset(db.sb_outlet_activities.cm_id==session.searchValueSBA_outlet_act)

    if ((session.btn_filter) and (session.searchTypeSBA_outlet_act == 'RepMobile')):
        qset = qset(db.sb_outlet_activities.cm_mobile_no == session.searchValueSBA_outlet_act)

    if ((session.btn_filter) and (session.searchTypeSBA_outlet_act=='town_code')):
        qset=qset(db.sb_outlet_activities.town_code==session.searchValueSBA_outlet_act)

    # if ((session.btn_filter) and (session.searchTypeSBA_Visit_list == 'shopperMobile')):
    #     qset = qset(db.sb_outlet_activities_visit.cm_mobile_no == session.searchValueSBA_Visit_list)

    if ((session.btn_filter) and (session.searchTypeSBA_outlet_act == 'route')):
        qset = qset(db.sb_outlet_activities.route == session.searchValueSBA_outlet_act)

    if ((session.btn_filter) and (session.searchTypeSBA_outlet_act == 'outlet_code')):
        qset = qset(db.sb_outlet_activities.outlet_code == session.searchValueSBA_outlet_act)


    if ((session.btn_filter) and (session.searchTypeSBA_outlet_act == 'sllist')):
        qset = qset(db.sb_outlet_activities.id == session.searchValueSBA_outlet_act)


    records = qset.select(db.sb_outlet_activities.month,db.sb_outlet_activities.id,db.sb_outlet_activities.cm_id,db.sb_outlet_activities.cm_name,db.sb_outlet_activities.cm_mobile_no,db.sb_outlet_activities.region,db.sb_outlet_activities.territory_name,db.sb_outlet_activities.town_code,db.sb_outlet_activities.town_name,db.sb_outlet_activities.route,db.sb_outlet_activities.outlet_code,db.sb_outlet_activities.outlet_name, orderby=~db.sb_outlet_activities.id, limitby=limitby)

    recCount = 0
    recCountRec = qset.select(db.sb_outlet_activities.id.count(), limitby=(0, 1))
    if recCountRec:
        recCount = recCountRec[0][db.sb_outlet_activities.id.count()]
    return dict(access_permission=access_permission,search_form=search_form,records=records, page=page, items_per_page=items_per_page, recCount=recCount)


def download_SBA_outlet_activities():
    records=''
    #Create query based on search type

    townList = []
    town_code = str(session.town_code)[1:-1].split('|')
    if len(town_code) > 1:
        for i in range(len(town_code)):
            townList.append(town_code[i])



    qset = db()
    if session.town_code != '':
        if session.town_code != 'ALL':
            if len(town_code) > 1:
                qset = qset(db.sb_outlet_activities_visit.town_code.belongs(townList))
            else:
                qset = qset(db.sb_outlet_activities_visit.town_code == session.town_code)

    if ((session.btn_filter) and (session.sba_visit_towncode_out!='')):
        qset=qset(db.sb_outlet_activities.town_code==session.sba_visit_towncode_out)


    if ((session.btn_filter) and (session.searchTypeSBA_outlet_act=='RepId')):
        qset=qset(db.sb_outlet_activities.cm_id==session.searchValueSBA_outlet_act)

    if ((session.btn_filter) and (session.searchTypeSBA_outlet_act == 'RepMobile')):
        qset = qset(db.sb_outlet_activities.cm_mobile_no == session.searchValueSBA_outlet_act)

    if ((session.btn_filter) and (session.searchTypeSBA_outlet_act=='town_code')):
        qset=qset(db.sb_outlet_activities.town_code==session.searchValueSBA_outlet_act)

    if ((session.btn_filter) and (session.searchTypeSBA_outlet_act == 'route')):
        qset = qset(db.sb_outlet_activities.route == session.searchValueSBA_outlet_act)

    if ((session.btn_filter) and (session.searchTypeSBA_outlet_act == 'outlet_code')):
        qset = qset(db.sb_outlet_activities.outlet_code == session.searchValueSBA_outlet_act)


    if ((session.btn_filter) and (session.searchTypeSBA_outlet_act == 'sllist')):
        qset = qset(db.sb_outlet_activities.id == session.searchValueSBA_outlet_act)


    records = qset.select(db.sb_outlet_activities.id,db.sb_outlet_activities.cm_id,db.sb_outlet_activities.cm_name,db.sb_outlet_activities.cm_mobile_no,db.sb_outlet_activities.region,db.sb_outlet_activities.territory_name,db.sb_outlet_activities.town_code,db.sb_outlet_activities.town_name,db.sb_outlet_activities.route,db.sb_outlet_activities.outlet_code,db.sb_outlet_activities.outlet_name,db.sb_outlet_activities.month,db.sb_outlet_activities.v_target,db.sb_outlet_activities.v_ach,db.sb_outlet_activities.v_ach_persent,db.sb_outlet_activities.v_total_balance,db.sb_outlet_activities.p_sku_target,db.sb_outlet_activities.p_sku_ach,db.sb_outlet_activities.p_sku_ach_persent,db.sb_outlet_activities.p_sku_total_balance,db.sb_outlet_activities.innov_place_target,db.sb_outlet_activities.innov_place_ach,db.sb_outlet_activities.innov_place_ach_persent,db.sb_outlet_activities.innov_place_total_balance,db.sb_outlet_activities.innov_sku_detail,groupby=~db.sb_outlet_activities.id)

    myString = 'Outlet Target\n'

    myString += 'ID,CC ID,CC Name,CC Mobile,Region,Territory,Town Code,Town Name,Route,Outlet Code,Outlet Name,Month,Visit_target,Visit_ach,Visit_ach_persent,Visit_total_balance,p_sku_target,p_sku_ach,p_sku_ach_persent,p_sku_total_balance,innov_place_target,innov_place_ach,innov_place_ach_persent,innov_place_total_balance,innov_sku_detail\n'
    # Replace coma from records. because coma means new Column
    for rec in records:

        id = str(rec.id)
        rep_id = str(rec.cm_id)
        rep_name = str(rec.cm_name)
        mobile_no = str(rec.cm_mobile_no)
        region = str(rec.region)
        territory_name = str(rec.territory_name)
        route = str(rec.route)
        town_code = str(rec.town_code)
        town_name = str(rec.town_name)
        outlet_code = str(rec.outlet_code)
        outlet_name = str(rec.outlet_name)
        month = str(rec.month)
        v_target = str(rec.v_target)
        v_ach = str(rec.v_ach)
        v_ach_persent = str(rec.v_ach_persent)
        v_total_balance = str(rec.v_total_balance)
        p_sku_target = str(rec.p_sku_target)
        p_sku_ach = str(rec.p_sku_ach)
        p_sku_ach_persent = str(rec.p_sku_ach_persent)
        p_sku_total_balance = str(rec.p_sku_total_balance)
        innov_place_target = str(rec.innov_place_target)
        innov_place_ach = str(rec.innov_place_ach)
        innov_place_ach_persent = str(rec.innov_place_ach_persent)
        innov_place_total_balance = str(rec.innov_place_total_balance)

        innov_sku_detail = str(rec.innov_sku_detail)


        myString += id + ',' + rep_id + ',' + rep_name + ',' + mobile_no+ ',' + region+ ',' + territory_name+','+town_code +',' +town_name + ',' + route  + ',' + outlet_code+',' + outlet_name+',' + month+',' + v_target+',' + v_ach+',' + v_ach_persent+',' + v_total_balance+',' + p_sku_target+',' + p_sku_ach+',' + p_sku_ach_persent+',' + p_sku_total_balance+',' + innov_place_target+',' + innov_place_ach+',' + innov_place_ach_persent+',' + innov_place_total_balance+',' + innov_sku_detail+ '\n'


    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_SBA_Outlet_Target.csv'
    return str(myString)



def sba_outlet_batch_upload():

    response.title = 'Outlet Target Batch Upload'

    btn_upload = request.vars.btn_upload
    upload_checkbox = request.vars.upload_checkbox
    count_inserted = 0
    count_error = 0
    error_str = ''
    total_row = 0
    outlet_list_excel = []
    channel_list_excel=[]
    slab_list_excel=[]
    if btn_upload == 'Upload/Update' and upload_checkbox=='upload_checkbox':

        excel_data = str(request.vars.excel_data)
        inserted_count = 0
        error_count = 0
        error_list = []
        row_list = excel_data.split('\n')
        total_row = len(row_list)

        outlet_code_list_excel = []
        ins_list = []
        ins_dict = {}

        for j in range(total_row):
            if j >= 1000:
                break
            else:
                row_data = row_list[j]
                coloum_list = row_data.split('\t')

                outletCode2 = str(coloum_list[0]).strip().upper()
                outlet_code = check_special_char_id(outletCode2)
                outlet_code_list_excel.append(outlet_code)


        # main loop
        for i in range(total_row):
            if i >= 1000:
                break
            else:
                row_data = row_list[i]
                coloum_list = row_data.split('\t')

                if len(coloum_list) != 16:
                    error_data = row_data + '(16 columns need in a row)\n'
                    error_str = error_str + error_data
                    count_error += 1
                    continue
                else:

                    outletCode2 = str(coloum_list[0]).strip().upper()
                    outlet_code = check_special_char_id(outletCode2)


                    cc_id2 = str(coloum_list[1]).strip().upper()
                    cm_id = check_special_char_id(cc_id2)
                    month2 = str(coloum_list[2]).strip()
                    month = check_special_char(month2)
                    v_target = str(coloum_list[3])
                    v_ach = str(coloum_list[4])
                    v_ach_persent = str(coloum_list[5])
                    v_total_balance = str(coloum_list[6])
                    p_sku_target = str(coloum_list[7])

                    p_sku_ach = str(coloum_list[8])
                    p_sku_ach_persent = str(coloum_list[9])
                    p_sku_total_balance = str(coloum_list[10])
                    innov_place_target = str(coloum_list[11])
                    innov_place_ach = str(coloum_list[12])
                    innov_place_ach_persent = str(coloum_list[13])
                    innov_place_total_balance = str(coloum_list[14])
                    innov_sku_detail = str(coloum_list[15])

                    excel_duplicate_flag = False

                    outlet_count = outlet_code_list_excel.count(outlet_code)
                    if outlet_count >1:
                        excel_duplicate_flag = True
                    # return excel_duplicate_flag
                    if excel_duplicate_flag ==True:
                        error_data = row_data + '(Duplicate outlet code in excel)\n'
                        error_str = error_str + error_data
                        count_error += 1
                        continue

                    cm_name = ''
                    cm_mobile_no = ''
                    recordCM = db((db.sm_rep.rep_id == cm_id) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_name, db.sm_rep.mobile)

                    if recordCM:
                        cm_name = recordCM[0].rep_name
                        cm_mobile_no = recordCM[0].mobile

                    else:
                        error_data = row_data + '(CC ID Not Found)\n'
                        error_str = error_str + error_data
                        # return 'efgh'
                        count_error += 1
                        continue

                    outlet_name=''
                    town_code=''
                    town_name=''
                    area=''
                    territory_name=''
                    route=''
                    region=''
                    recordOutlet = db(db.sb_pjp.outlet_code == outlet_code).select(db.sb_pjp.area,db.sb_pjp.route,db.sb_pjp.region,db.sb_pjp.unique_cluster_name,db.sb_pjp.territory_name,db.sb_pjp.town_name,db.sb_pjp.town_code,db.sb_pjp.outlet_name)

                    if recordOutlet:
                        outlet_name = recordOutlet[0].outlet_name
                        town_code = recordOutlet[0].town_code
                        town_name = recordOutlet[0].town_name
                        area = recordOutlet[0].area
                        territory_name = recordOutlet[0].territory_name
                        route = recordOutlet[0].route
                        region = recordOutlet[0].region

                    else:
                        error_data = row_data + '(Outlet Not Found)\n'
                        error_str = error_str + error_data
                        # return 'efgh'
                        count_error += 1
                        continue

                    recordExt = db(db.sb_outlet_activities.outlet_code == outlet_code).select(db.sb_outlet_activities.id)

                    if recordExt:
                        db(db.sb_outlet_activities.outlet_code == outlet_code).update(cm_id=cm_id,cm_name=cm_name,cm_mobile_no=cm_mobile_no,town_code=town_code,town_name=town_name,area=area,territory_name=territory_name,route=route,region=region,outlet_code=outlet_code,outlet_name=outlet_name,month=month,v_target=v_target,v_ach=v_ach,v_ach_persent=v_ach_persent,v_total_balance=v_total_balance,p_sku_target=p_sku_target,p_sku_ach=p_sku_ach,p_sku_ach_persent=p_sku_ach_persent,p_sku_total_balance=p_sku_total_balance,innov_place_target=innov_place_target,innov_place_ach=innov_place_ach,innov_place_ach_persent=innov_place_ach_persent,innov_place_total_balance=innov_place_total_balance,innov_sku_detail=innov_sku_detail)
                        count_inserted += 1

                    else:
                        try:
                            # ins_dict = {'cm_id':cm_id,'cm_name':cm_name,'cm_mobile_no':cm_mobile_no,'town_code':town_code,'town_name':town_name,'area':area,'territory_name':territory_name,'route':route,'region':region,'outlet_code':outlet_code,'outlet_name':outlet_name,'month':month,'v_target':v_target,'v_ach':v_ach,'v_ach_persent':v_ach_persent,'v_total_balance':v_total_balance,'p_sku_target':p_sku_target,'p_sku_ach':p_sku_ach,'p_sku_ach_persent':p_sku_ach_persent,'p_sku_total_balance':p_sku_total_balance,'innov_place_target':innov_place_target,'innov_place_ach':innov_place_ach,'innov_place_ach_persent':innov_place_ach_persent,'innov_place_total_balance':innov_place_total_balance,'innov_sku_detail':innov_sku_detail}
                            ins_dict = {'cm_id':cm_id,'cm_name':cm_name,'cm_mobile_no':cm_mobile_no,'town_code':town_code,'town_name':town_name,'area':area,'territory_name':territory_name,'route':route,'region':region,'outlet_code':outlet_code,'outlet_name':outlet_name,'month':month,'v_target':v_target,'v_ach':v_ach,'v_ach_persent':v_ach_persent,'v_total_balance':v_total_balance,'p_sku_target':p_sku_target,'p_sku_ach':p_sku_ach,'p_sku_ach_persent':p_sku_ach_persent,'p_sku_total_balance':p_sku_total_balance,'innov_place_target':innov_place_target,'innov_place_ach':innov_place_ach,'innov_place_ach_persent':innov_place_ach_persent,'innov_place_total_balance':innov_place_total_balance,'innov_sku_detail':innov_sku_detail}

                            ins_list.append(ins_dict)

                            # townCodeExcel.append(town_code)
                            count_inserted += 1

                        except:
                            error_data = row_data + '(error in process)\n'
                            error_str = error_str + error_data
                            count_error += 1
                            continue

        if error_str == '':
            error_str = 'No error'

        if len(ins_list) > 0:
            # Bulk insert
            inCountList = db.sb_outlet_activities.bulk_insert(ins_list)

    btn_clean = request.vars.btn_clean
    backup_checkbox = request.vars.backup_checkbox

    if btn_clean == 'Clean Outlet' and backup_checkbox == 'backup_checkbox':

        excel_data = str(request.vars.excel_data)
        inserted_count = 0
        error_count = 0
        error_list = []
        row_list = excel_data.split('\n')
        total_row = len(row_list)

        ins_list = []
        ins_dict = {}

        # main loop
        for i in range(total_row):
            if i >= 1000:
                break
            else:

                row_data = row_list[i]
                coloum_list = row_data.split('\t')

                if len(coloum_list) != 1:

                    error_data = row_data + '(Outlet Code 1 column need in a row)\n'
                    error_str = error_str + error_data
                    count_error += 1
                    continue
                else:

                    outletCode2 = str(coloum_list[0]).strip().upper()
                    outlet_code = check_special_char_id(outletCode2)
                    db(db.sb_outlet_activities.outlet_code == outlet_code).delete()
                    count_inserted += 1

                    continue


    btn_backup = request.vars.btn_backup
    backup_year = request.vars.salary_year
    backup_month = request.vars.salary_month
    if btn_backup and backup_year != '' and backup_month != '':
        # records=db((db.w_pjp_backup.year==backup_year) & (db.w_pjp_backup.month==backup_month)).select(db.w_pjp_backup.id)
        # if records:
        #     response.flash = 'Already Backup PJP' +'-'+ backup_month +'-'+ backup_year
        # else:

        imported_pjp_for_back = "INSERT INTO sb_outlet_activities_backup (year,month_backup,cm_id,cm_name,cm_mobile_no,town_code,town_name,area,territory_name,route,region,outlet_code,outlet_name,month,v_target,v_ach,v_ach_persent,v_total_balance,p_sku_target,p_sku_ach,p_sku_ach_persent,p_sku_total_balance,innov_place_target,innov_place_ach,innov_place_ach_persent,innov_place_total_balance,innov_sku_detail,field1,field2,note,outlet_created_on,outlet_created_by,outlet_updated_on,outlet_updated_by,created_by) SELECT '" + backup_year + "' as year, '" + backup_month + "' as month_backup,cm_id,cm_name,cm_mobile_no,town_code,town_name,area,territory_name,route,region,outlet_code,outlet_name,month,v_target,v_ach,v_ach_persent,v_total_balance,p_sku_target,p_sku_ach,p_sku_ach_persent,p_sku_total_balance,innov_place_target,innov_place_ach,innov_place_ach_persent,innov_place_total_balance,innov_sku_detail,field1,field2,note,created_on as outlet_created_on,created_by as outlet_created_by,updated_on as outlet_updated_on,updated_by as outlet_updated_by,'" + session.user_id + "' as created_by FROM sb_outlet_activities"
        db.executesql(imported_pjp_for_back)
        response.flash = 'Outlet Backup Successfully'

    if btn_backup and (backup_year == '' or backup_month == ''):
        response.flash = 'Please Select Year and Month'

    recYear = db().select(db.year.year, groupby=db.year.year, orderby=~db.year.year)

    return dict(recYear=recYear,count_inserted=count_inserted,count_error=count_error, error_str=error_str, total_row=total_row)

def sba_outlet_activities_details():

    syncCode = 0
    syncCodeCheck = db(db.sm_user.user_id == session.user_id).select(db.sm_user.sync_code, limitby=(0, 1))
    if syncCodeCheck:
        syncCode = syncCodeCheck[0][db.sm_user.sync_code]

    if (session.sync_codeCheck != syncCode):
        session.flash = 'Unauthorized User Please Reset Your Password'
        redirect(URL('default', 'index'))

    response.title = 'Outlet Target Details'

    page = request.args(0)
    visitsl = request.args(1)
    records = db(db.sb_outlet_activities.id == visitsl).select(db.sb_outlet_activities_visit.endTime,db.sb_outlet_activities_visit.startTime, db.sb_outlet_activities_visit.shop_imageName,db.sb_outlet_activities_visit.whichSkinCleansing,db.sb_outlet_activities_visit.skinCleansing, db.sb_outlet_activities_visit.whichOralCare,db.sb_outlet_activities_visit.oralCare, db.sb_outlet_activities_visit.whichHairCare,db.sb_outlet_activities_visit.hairCare, db.sb_outlet_activities_visit.whichFaceWash,db.sb_outlet_activities_visit.faceWash,db.sb_outlet_activities_visit.whichFaceCream,db.sb_outlet_activities_visit.faceCream,db.sb_outlet_activities_visit.id, db.sb_outlet_activities_visit.visitsl,db.sb_outlet_activities_visit.cm_id, db.sb_outlet_activities_visit.cm_name,db.sb_outlet_activities_visit.cm_mobile_no, db.sb_outlet_activities_visit.region,db.sb_outlet_activities_visit.territory_name, db.sb_outlet_activities_visit.town_code,db.sb_outlet_activities_visit.town_name, db.sb_outlet_activities_visit.route,db.sb_outlet_activities_visit.outletcode, db.sb_outlet_activities_visit.outletname,db.sb_outlet_activities_visit.visitDate, db.sb_outlet_activities_visit.latLong)

    recordsDetails = db(db.sb_outlet_activities_visit_details.visitsl == visitsl).select(db.sb_outlet_activities_visit_details.posmCode,db.sb_outlet_activities_visit_details.boardCondition,db.sb_outlet_activities_visit_details.sb_height,db.sb_outlet_activities_visit_details.sb_width,db.sb_outlet_activities_visit_details.a_qty,db.sb_outlet_activities_visit_details.light,db.sb_outlet_activities_visit_details.posm_imageName)
    # return recordsDetails
    return dict(recordRows=records,recordsDetails=recordsDetails,page=page,rowID=visitsl)


def sba_pjp_outlet_batch_upload():

    response.title = 'SBA PJP Outlet Batch Upload'
    btn_upload = request.vars.btn_upload
    upload_checkbox = request.vars.upload_checkbox

    btn_backup = request.vars.btn_backup
    count_inserted = 0
    count_error = 0
    error_str = ''
    total_row = 0
    if btn_upload == 'Upload/Update' and upload_checkbox=='upload_checkbox':
        excel_data = str(request.vars.excel_data)
        inserted_count = 0
        error_count = 0
        error_list = []
        outlet_list_excel = []
        outlet_list_excel_db = []
        row_list = excel_data.split('\n')
        total_row = len(row_list)
        ins_list = []
        ins_dict = {}
        rep_list_excel=[]
        rep_list_exceldb=[]
        #   ----------------------
        day_list=[]
        day_records = db().select(db.pjp_days.day, groupby=db.pjp_days.day)

        for row in day_records:
            day = row.day
            day_list.append(day)

        rep_list = []
        drep_records = db(db.sm_rep.status=='ACTIVE').select(db.sm_rep.rep_id, groupby=db.sm_rep.rep_id)

        for row2 in drep_records:
            rep_id = row2.rep_id
            rep_list.append(rep_id)

        for i in range(total_row):
            if i >= 5000:
                break
            else:
                row_data = row_list[i]
                coloum_list = row_data.split('\t')
                if len(coloum_list) == 22:
                    outlet_list_excel.append(str(coloum_list[6]).strip().upper())
                    rep_list_excel.append(str(coloum_list[9]).strip().upper())

        existRows = db((db.sb_pjp.outlet_code.belongs(outlet_list_excel))).select(db.sb_pjp.outlet_code,orderby=db.sb_pjp.outlet_code)
        outlet_list_excel_db = existRows.as_list()


        # main loop
        for i in range(total_row):
            if i >= 5000:
                break
            else:
                row_data = row_list[i]
                coloum_list = row_data.split('\t')

                if len(coloum_list) != 22:
                    error_data = row_data + '(21 columns need in a row)\n'
                    error_str = error_str + error_data
                    count_error += 1
                    continue
                else:
                    region2 = str(coloum_list[0]).strip().upper()
                    region = check_special_char(region2)

                    area2 = str(coloum_list[1]).strip().upper()
                    area = check_special_char(area2)

                    territory_name2 = str(coloum_list[2]).strip().upper()
                    territory_name = check_special_char(territory_name2)

                    town_code_xl2 = str(coloum_list[3]).strip()
                    town_code = check_special_char_id(town_code_xl2)
                    town_name_xl2 = str(coloum_list[4]).strip()
                    town_name = check_special_char(town_name_xl2)

                    route2 = str(coloum_list[5]).strip()
                    route = check_special_char(route2)

                    outlet_code_xl2 = str(coloum_list[6]).strip()
                    outlet_code = check_special_char_id(outlet_code_xl2)
                    outlet_name_xl2 = str(coloum_list[7]).strip()
                    outlet_name = check_special_char(outlet_name_xl2)

                    cluster_name_xl2 = str(coloum_list[8]).strip()
                    unique_cluster_name = check_special_char(cluster_name_xl2)

                    wmaID_xl2 = str(coloum_list[9]).strip().upper()
                    wma_id = check_special_char_id(wmaID_xl2)
                    wma_name_xl = str(coloum_list[10]).strip()
                    wma_name = check_special_char(wma_name_xl)

                    wma_mobile_no = str(coloum_list[11]).strip()

                    channel_xl2 = str(coloum_list[12]).strip()
                    channel = check_special_char(channel_xl2)

                    serviceday_1XL = str(coloum_list[13]).strip().upper()
                    serviceday_1 = check_special_char(serviceday_1XL)

                    serviceday_2XL = str(coloum_list[14]).strip().upper()
                    serviceday_2 = check_special_char(serviceday_2XL)

                    serviceday_3XL = str(coloum_list[15]).strip().upper()
                    serviceday_3 = check_special_char(serviceday_3XL)

                    wk1 = str(coloum_list[17]).strip().upper()
                    wk2 = str(coloum_list[18]).strip().upper()
                    wk3 = str(coloum_list[19]).strip().upper()
                    wk4 = str(coloum_list[20]).strip().upper()
                    status = str(coloum_list[21]).strip().upper()


                    if (wma_id not in rep_list):
                        error_data = row_data + '(Invalid CC ID)\n'
                        error_str = error_str + error_data
                        count_error += 1
                        continue

                    day_1_flag = False
                    day_2_flag = False
                    day_3_flag = False


                    # return serviceday_2
                    if (serviceday_1 !='') and (serviceday_1 not in day_list):
                        day_1_flag = True
                        # break

                    if (serviceday_2 !='') and (serviceday_2 not in day_list):
                        day_2_flag = True
                        # break
                    if (serviceday_3 !='') and (serviceday_3 not in day_list):
                        day_3_flag = True
                        # break
                    if serviceday_1 =='' and serviceday_2=='' and serviceday_3=='':
                        error_data = row_data + '(Required Serviceday)\n'
                        error_str = error_str + error_data
                        count_error += 1
                        continue
                    else:
                        if day_1_flag == True:
                            error_data = row_data + '(Invalid serviceday_1)\n'
                            error_str = error_str + error_data
                            count_error += 1
                            continue
                        if day_2_flag == True:
                            error_data = row_data + '(Invalid serviceday_2)\n'
                            error_str = error_str + error_data
                            count_error += 1
                            continue
                        if day_3_flag == True:
                            error_data = row_data + '(Invalid serviceday_3)\n'
                            error_str = error_str + error_data
                            count_error += 1
                            continue

                    wk1_flag = False
                    if wk1 == '0' or wk1 == '1':
                        wk1_flag = True

                    wk2_flag = False
                    if wk2 == '0' or wk2 == '1':
                        wk2_flag = True

                    wk3_flag = False
                    if wk3 == '0' or wk3 == '1':
                        wk3_flag = True

                    wk4_flag = False
                    if wk4 == '0' or wk4 == '1':
                        wk4_flag = True

                    if wk1_flag == False:
                        error_data = row_data + '(Invalid wk1)\n'
                        error_str = error_str + error_data
                        count_error += 1
                        continue
                    if wk2_flag == False:
                        error_data = row_data + '(Invalid wk2)\n'
                        error_str = error_str + error_data
                        count_error += 1
                        continue
                    if wk3_flag == False:
                        error_data = row_data + '(Invalid wk3)\n'
                        error_str = error_str + error_data
                        count_error += 1
                        continue
                    if wk4_flag == False:
                        error_data = row_data + '(Invalid wk4)\n'
                        error_str = error_str + error_data
                        count_error += 1
                        continue

                    visitfrequency = int(wk1) + int(wk2) + int(wk3) + int(wk4)

                    # records = db(db.sb_pjp.outlet_code == outlet_code).select(db.sb_pjp.outlet_code)
                    outlet_codeDB =''
                    for i in range(len(outlet_list_excel_db)):
                        myRowData1 = outlet_list_excel_db[i]
                        outlet_codeDB = myRowData1['outlet_code']

                    if (str(outlet_codeDB).strip() == str(outlet_code).strip()):
                        db(db.sb_pjp.outlet_code == outlet_code).update(area=area,route=route,channel=channel,region=region,territory_name=territory_name,town_code=town_code,town_name=town_name,outlet_code=outlet_code,outlet_name=outlet_name,unique_cluster_name=unique_cluster_name,wma_id=wma_id,wma_name=wma_name,wma_mobile_no=wma_mobile_no,serviceday_1=serviceday_1,serviceday_2=serviceday_2,serviceday_3=serviceday_3,visitfrequency=visitfrequency,wk1=wk1,wk2=wk2,wk3=wk3,wk4=wk4,status=status)
                        count_inserted += 1
                        # continue
                    else:

                        try:
                            ins_dict = {'area':area,'route':route,'region':region,'territory_name':territory_name,'town_code':town_code,'town_name':town_name,'outlet_code':outlet_code,'outlet_name':outlet_name,'unique_cluster_name':unique_cluster_name,'wma_id':wma_id,'wma_name':wma_name,'wma_mobile_no':wma_mobile_no,'channel':channel,'serviceday_1':serviceday_1,'serviceday_2':serviceday_2,'serviceday_3':serviceday_3,'visitfrequency':visitfrequency,'wk1':wk1,'wk2':wk2,'wk3':wk3,'wk4':wk4, 'status':status}
                            ins_list.append(ins_dict)
                            count_inserted += 1
                        except:
                            error_data = row_data + '(Error in process)\n'
                            error_str = error_str + error_data
                            count_error += 1
                            continue
        # return str(ins_dict)
        if error_str == '':
            error_str = 'No error'

        if len(ins_list) > 0:
            # Bulk insert
            inCountList = db.sb_pjp.bulk_insert(ins_list)


    btn_clean = request.vars.btn_clean
    backup_checkbox = request.vars.backup_checkbox

    if btn_clean == 'Clean Outlet' and backup_checkbox == 'backup_checkbox':

        excel_data = str(request.vars.excel_data)
        inserted_count = 0
        error_count = 0
        error_list = []
        row_list = excel_data.split('\n')
        total_row = len(row_list)

        ins_list = []
        ins_dict = {}

        # main loop
        for i in range(total_row):
            if i >= 5000:
                break
            else:

                row_data = row_list[i]
                coloum_list = row_data.split('\t')

                if len(coloum_list) != 1:

                    error_data = row_data + '(Outlet Code 1 column need in a row)\n'
                    error_str = error_str + error_data
                    count_error += 1
                    continue
                else:

                    outletCode2 = str(coloum_list[0]).strip().upper()
                    outlet_code = check_special_char_id(outletCode2)
                    db(db.sb_pjp.outlet_code == outlet_code).delete()
                    count_inserted += 1

                    continue

    backup_year = request.vars.salary_year
    backup_month = request.vars.salary_month
    if btn_backup and backup_year !='' and backup_month !='':
        # records=db((db.w_pjp_backup.year==backup_year) & (db.w_pjp_backup.month==backup_month)).select(db.w_pjp_backup.id)
        # if records:
        #     response.flash = 'Already Backup PJP' +'-'+ backup_month +'-'+ backup_year
        # else:

        imported_pjp_for_back = "INSERT INTO sb_pjp_backup (year,month,region,area,territory_name,town_code,town_name,route,outlet_code,outlet_name,unique_cluster_name,wma_id,wma_name,wma_mobile_no,channel,serviceday_1,serviceday_2,serviceday_3,visitfrequency,wk1,wk2,wk3,wk4,errorflag,status,field1,field2,note,pjp_created_on,pjp_created_by,pjp_updated_on,pjp_updated_by,created_by) SELECT '" + backup_year + "' as year, '" + backup_month + "' as month,region,area,territory_name,town_code,town_name,route,outlet_code,outlet_name,unique_cluster_name,wma_id,wma_name,wma_mobile_no,channel,serviceday_1,serviceday_2,serviceday_3,visitfrequency,wk1,wk2,wk3,wk4,errorflag,status,field1,field2,note,created_on as pjp_created_on,created_by as pjp_created_by,updated_on as pjp_updated_on,updated_by as pjp_updated_by,'" + session.user_id + "' as created_by FROM sb_pjp"
        db.executesql(imported_pjp_for_back)
        response.flash = 'PJP Backup Successfully'

    if btn_backup and (backup_year == '' or backup_month == ''):

        response.flash =  'Please Select Year and Month'


    recYear = db().select(db.year.year, groupby=db.year.year, orderby=~db.year.year)

    return dict(recYear=recYear,count_inserted=count_inserted, count_error=count_error, error_str=error_str,total_row=total_row)


def knorr_outlet():
    task_id = 'knorr_outlet_Manage'
    task_id_view = 'knorr_outlet_View'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if access_permission == False and access_permission_view == False:
        session.flash = 'Access is Denied'
        redirect(URL('default', 'home'))

    response.title = 'SO Outlet'

    #  ---------------Filter---------------#

    btn_filter = request.vars.btn_filter
    btn_all = request.vars.btn_all
    reqPage = len(request.args)

    if btn_filter:
        session.btn_filter = btn_filter
        session.searchType_knorr = str(request.vars.searchType_knorr).strip()
        session.searchValue_knorr = str(request.vars.searchValue_knorr).strip()

        if session.searchType_knorr == 'RepId':
            idlist = session.searchValue_knorr.split('|')
            if len(idlist) >= 1:
                session.searchValue_knorr = idlist[0]
        elif session.searchType_knorr == 'outlet_code':
            outletCode = session.searchValue_knorr.split('|')
            if len(outletCode) >= 1:
                session.searchValue_knorr = outletCode[0]

        elif session.searchType_knorr == 'territory_name':
            territoryName = session.searchValue_knorr.split('|')
            if len(territoryName) >= 1:
                session.searchValue_knorr = territoryName[0]

        elif session.searchType_knorr == 'region':
            territoryName = session.searchValue_knorr.split('|')
            if len(territoryName) >= 1:
                session.searchValue_knorr = territoryName[0]

        elif session.searchType_knorr == 'route_name':
            territoryName = session.searchValue_knorr.split('|')
            if len(territoryName) >= 1:
                session.searchValue_knorr = territoryName[0]

        elif session.searchType_knorr == 'townNnameSearch':
            territoryNameAll =session.searchValue_knorr
            territoryName = session.searchValue_knorr.split('|')
            if len(territoryName) > 1:
                session.searchValue_knorr = territoryName[1]
            else:
                session.searchValue_knorr = territoryNameAll

        elif session.searchType_knorr == 'status':
            status = session.searchValue_knorr.split('|')
            if len(status) >= 1:
                session.searchValue_knorr = status[0]
        else:
            session.searchValue_knorr = session.searchValue_knorr

        reqPage = 0

    elif btn_all:
        session.btn_filter = None
        session.searchType_knorr = None
        session.searchValue_knorr = None
        reqPage = 0
    # #-----------------------Filter End----------------#f

    if reqPage:
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = session.items_per_page
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # --------end paging

    townList = []
    town_code = str(session.town_code)[1:-1].split('|')
    if len(town_code) > 1:
        for i in range(len(town_code)):
            townList.append(town_code[i])

    #recCount=0
    qset=db()
    if session.town_code!='':
        if session.town_code!='ALL':
            if len(town_code)>1:
                qset = qset(db.knorr_outlet.area_id.belongs(townList))
            else:
                qset = qset(db.knorr_outlet.area_id==session.town_code)


    if ((session.btn_filter) and (session.searchType_knorr == 'outlet_code')):
        qset = qset(db.knorr_outlet.outlet_id == session.searchValue_knorr)
    elif ((session.btn_filter) and (session.searchType_knorr == 'RepId')):
        qset = qset(db.knorr_outlet.field1 == session.searchValue_knorr)
    elif((session.btn_filter) and (session.searchType_knorr == 'town')):
         qset = qset(db.knorr_outlet.area_id == session.searchValue_knorr)

    elif ((session.btn_filter) and (session.searchType_knorr == 'sllist')):
        qset = qset(db.knorr_outlet.id == session.searchValue_knorr)

    elif ((session.btn_filter) and (session.searchType_knorr == 's_status')):
        qset = qset(db.knorr_outlet.status == session.searchValue_knorr)
    else:
        session.filterBy = None

    records = qset.select(db.knorr_outlet.id,db.knorr_outlet.field1,db.knorr_outlet.name,db.knorr_outlet.outlet_id,db.knorr_outlet.area_id,db.knorr_outlet.address,db.knorr_outlet.status, orderby=~db.knorr_outlet.id,limitby=limitby)
    recCount=0
    recCountRec =qset.select(db.knorr_outlet.id.count(), limitby=(0,1))
    if recCountRec:
        recCount=recCountRec[0][db.knorr_outlet.id.count()]

    return dict(access_permission=access_permission,records=records, page=page,items_per_page=items_per_page,recCount=recCount)


def knore_outlet_download():
    townList = []
    town_code = str(session.town_code)[1:-1].split('|')
    if len(town_code) > 1:
        for i in range(len(town_code)):
            townList.append(town_code[i])

    # recCount=0
    qset = db()
    if session.town_code != '':
        if session.town_code != 'ALL':
            if len(town_code) > 1:
                qset = qset(db.knorr_outlet.area_id.belongs(townList))
            else:
                qset = qset(db.knorr_outlet.area_id == session.town_code)

    if ((session.btn_filter) and (session.searchType_knorr == 'outlet_code')):
        qset = qset(db.knorr_outlet.outlet_id == session.searchValue_knorr)
    elif ((session.btn_filter) and (session.searchType_knorr == 'RepId')):
        qset = qset(db.knorr_outlet.field1 == session.searchValue_knorr)
    elif ((session.btn_filter) and (session.searchType_knorr == 'town')):
        qset = qset(db.knorr_outlet.area_id == session.searchValue_knorr)

    elif ((session.btn_filter) and (session.searchType_knorr == 'sllist')):
        qset = qset(db.knorr_outlet.id == session.searchValue_knorr)

    elif ((session.btn_filter) and (session.searchType_knorr == 's_status')):
        qset = qset(db.knorr_outlet.status == session.searchValue_knorr)
    else:
        session.filterBy = None

    records = qset.select(db.knorr_outlet.id, db.knorr_outlet.field1, db.knorr_outlet.name, db.knorr_outlet.outlet_id,db.knorr_outlet.area_id, db.knorr_outlet.address, db.knorr_outlet.status,orderby=~db.knorr_outlet.id)


    myString = 'SO Outlet\n'

    myString += 'SL,Outlet Code,Outlet Name,Area,Address,SO ID,Status\n'

    for rec in records:
        id = str(rec.id)
        rep_id = str(rec.field1)
        outlet_id = str(rec.outlet_id)
        outlet_name = str(rec.name)
        area_id = str(rec.area_id)
        address = str(rec.address)
        status = str(rec.status)



        myString += id + ',' + outlet_id+ ',' + outlet_name + ',' + area_id + ',' + address+ ',' + rep_id  +',' + status + '\n'
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_SO_Outlet.csv'
    return str(myString)




def knorr_outlet_batch_upload():

    response.title = 'SBA PJP Outlet Batch Upload'
    btn_upload = request.vars.btn_upload
    upload_checkbox = request.vars.upload_checkbox

    btn_backup = request.vars.btn_backup
    count_inserted = 0
    count_error = 0
    error_str = ''
    total_row = 0
    if btn_upload == 'Upload/Update' and upload_checkbox=='upload_checkbox':
        excel_data = str(request.vars.excel_data)
        inserted_count = 0
        error_count = 0
        error_list = []
        outlet_list_excel = []
        outlet_list_excel_db = []
        row_list = excel_data.split('\n')
        total_row = len(row_list)
        ins_list = []
        ins_dict = {}
        rep_list_excel=[]
        rep_list_exceldb=[]
        #   ----------------------

        rep_list = []
        drep_records = db(db.sm_rep.status=='ACTIVE').select(db.sm_rep.rep_id, groupby=db.sm_rep.rep_id)

        for row2 in drep_records:
            rep_id = row2.rep_id
            rep_list.append(rep_id)

        for i in range(total_row):
            if i >= 1000:
                break
            else:
                row_data = row_list[i]
                coloum_list = row_data.split('\t')
                if len(coloum_list) == 6:
                    outlet_list_excel.append(str(coloum_list[0]).strip().upper())
                    # rep_list_excel.append(str(coloum_list[4]).strip().upper())

        existRows = db((db.knorr_outlet.outlet_id.belongs(outlet_list_excel))&(db.knorr_outlet.status=='ACTIVE')).select(db.knorr_outlet.outlet_id,db.knorr_outlet.field1,orderby=db.knorr_outlet.outlet_id)
        outlet_list_excel_db = existRows.as_list()


        # main loop
        for i in range(total_row):
            if i >= 1000:
                break
            else:
                row_data = row_list[i]
                coloum_list = row_data.split('\t')

                if len(coloum_list) != 6:
                    error_data = row_data + '(6 columns need in a row)\n'
                    error_str = error_str + error_data
                    count_error += 1
                    continue
                else:
                    outlet_id2 = str(coloum_list[0]).strip().upper()
                    outlet_id = check_special_char_id(outlet_id2)

                    name2 = str(coloum_list[1]).strip().upper()
                    name = check_special_char(name2)

                    area2 = str(coloum_list[2]).strip().upper()
                    area = check_special_char(area2)

                    address2 = str(coloum_list[3]).strip()
                    address = check_special_char(address2)

                    rep_id = str(coloum_list[4]).strip().upper()

                    status2 = str(coloum_list[5]).strip()
                    status = check_special_char(status2)
                    cid = 'UNIKNORR'

                    if (rep_id not in rep_list):
                        error_data = row_data + '(Invalid SO ID)\n'
                        error_str = error_str + error_data
                        count_error += 1
                        continue


                    outlet_codeDB =''
                    for i in range(len(outlet_list_excel_db)):
                        myRowData1 = outlet_list_excel_db[i]
                        outlet_codeDB = myRowData1['outlet_id']
                        field1db = myRowData1['field1']
                    # return outlet_codeDB
                    if (str(outlet_codeDB) == str(outlet_id) and str(field1db) == str(rep_id)):
                        error_data = row_data + '(Duplicate Outlet and SO)\n'
                        error_str = error_str + error_data
                        # return 'efgh'
                        count_error += 1
                        continue

                    try:
                        ins_dict = {'cid':cid,'outlet_id':outlet_id,'name':name,'area_id':area,'status':status,'address':address,'field1':rep_id}
                        ins_list.append(ins_dict)
                        count_inserted += 1
                    except:
                        error_data = row_data + '(Error in process)\n'
                        error_str = error_str + error_data
                        count_error += 1
                        continue
        # return str(ins_dict)
        if error_str == '':
            error_str = 'No error'

        if len(ins_list) > 0:
            # Bulk insert
            inCountList = db.knorr_outlet.bulk_insert(ins_list)


    btn_clean = request.vars.btn_clean
    backup_checkbox = request.vars.backup_checkbox

    if btn_clean == 'Clean Outlet' and backup_checkbox == 'backup_checkbox':

        excel_data = str(request.vars.excel_data)
        inserted_count = 0
        error_count = 0
        error_list = []
        row_list = excel_data.split('\n')
        total_row = len(row_list)

        ins_list = []
        ins_dict = {}

        # main loop
        for i in range(total_row):
            if i >= 1000:
                break
            else:

                row_data = row_list[i]
                coloum_list = row_data.split('\t')

                if len(coloum_list) == 0:

                    error_data = row_data + '(Minimum 1 column need in a row)\n'
                    error_str = error_str + error_data
                    count_error += 1
                    continue
                elif len(coloum_list) == 2:

                    outletCode2 = str(coloum_list[0]).strip().upper()
                    outlet_code = check_special_char_id(outletCode2)

                    rep_id2 = str(coloum_list[1]).strip().upper()
                    rep_id = check_special_char_id(rep_id2)
                    records =  db((db.knorr_outlet.outlet_id == outlet_code)&(db.knorr_outlet.field1==rep_id)).select(db.knorr_outlet.id)
                    if records:

                        db((db.knorr_outlet.outlet_id == outlet_code)&(db.knorr_outlet.field1==rep_id)).update(status='INACTIVE')
                        count_inserted += 1
                    else:
                        error_data = row_data + '(Not Found)\n'
                        error_str = error_str + error_data
                        # return 'efgh'
                        count_error += 1
                        continue
                elif len(coloum_list) == 1:

                    outletCode2 = str(coloum_list[0]).strip().upper()
                    outlet_code = check_special_char_id(outletCode2)


                    records = db(db.knorr_outlet.outlet_id == outlet_code).select(db.knorr_outlet.id)
                    if records:

                        db(db.knorr_outlet.outlet_id == outlet_code).update(status='INACTIVE')
                        count_inserted += 1
                    else:
                        error_data = row_data + '(Not Found)\n'
                        error_str = error_str + error_data
                        # return 'efgh'
                        count_error += 1
                        continue


    return dict(count_inserted=count_inserted, count_error=count_error, error_str=error_str,total_row=total_row)
