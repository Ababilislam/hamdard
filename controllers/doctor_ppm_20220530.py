
from random import randint
#---------------------------- ADD VALIDATION
def validation_gift_add(form):
    c_id = session.cid
    gift_id = str(form.vars.gift_id).strip().upper()
    gift_name = str(form.vars.gift_name).replace('|', ' ').strip().upper()

    #------- check duplicate
    existRows = db((db.sm_doctor_ppm.cid == c_id) & (db.sm_doctor_ppm.gift_id == gift_id)).select(db.sm_doctor_ppm.gift_id, limitby=(0, 1))
    if existRows:
        form.errors.gift_id = 'already exist'
    else:
        form.vars.gift_id = gift_id
        form.vars.gift_name = gift_name

#---------------------------- ADD
def gift_add():
    task_id = 'rm_doctor_manage'
    task_id_view = 'rm_doctor_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (access_permission_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

    response.title = 'PPM Item'

    c_id = session.cid

    #   ---------------------
    form = SQLFORM(db.sm_doctor_ppm,
                  fields=['gift_id', 'gift_name', 'des', 'status'],
                  submit_button='Save'
                  )

    form.vars.cid = c_id
    if form.accepts(request.vars, session, onvalidation=validation_gift_add):
       response.flash = 'Submitted Successfully'

    #  ---------------filter-------
    btn_filter_gift = request.vars.btn_filter
    btn_all = request.vars.btn_filter_all
    reqPage = len(request.args)
    if btn_filter_gift:
        session.btn_filter_gift = btn_filter_gift
        session.searchType_gift = str(request.vars.search_type).strip()
        session.searchValue_gift = str(request.vars.search_value).strip().upper()
        reqPage = 0
    elif btn_all:
        session.btn_filter_gift = None
        session.searchType_gift = None
        session.searchValue_gift = None
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
    qset = qset(db.sm_doctor_ppm.cid == c_id)
    if (session.btn_filter_gift):

        if (session.searchType_gift == 'GiftID'):
            qset = qset(db.sm_doctor_ppm.gift_id == session.searchValue_gift)

        elif (session.searchType_gift == 'Status'):
            qset = qset(db.sm_doctor_ppm.status == session.searchValue_gift)

    records = qset.select(db.sm_doctor_ppm.ALL, orderby=db.sm_doctor_ppm.gift_name, limitby=limitby)

    return dict(form=form, records=records, page=page, items_per_page=items_per_page, access_permission=access_permission)


#---------------------------- EDIT VALIDATION
def validation_gift_edit(form):
    c_id = session.cid
    gift_name = str(form.vars.gift_name).strip().upper().replace('|', ' ')
    form.vars.gift_name = gift_name

#---------------------------- EDIT
def gift_edit():
    task_id = 'rm_doctor_manage'
    access_permission = check_role(task_id)
    if (access_permission == False):
        session.flash = 'Access is Denied !'
        redirect (URL('gift_add'))
        
    #   ---------------------
    response.title = 'PPM -Edit'
    
    c_id = session.cid
    
    page = request.args(0)
    rowID = request.args(1)
    giftID = request.args(2)

    record = db.sm_doctor_ppm(rowID) or redirect(URL('gift_add'))

    form = SQLFORM(db.sm_doctor_ppm,
                  record=record,
                  deletable=True,
                  fields=['gift_name', 'des', 'status'],
                  submit_button='Update'
                  )

    if form.accepts(request.vars, session, onvalidation=validation_gift_edit):
        response.flash = 'Updated Successfully'
        redirect(URL('gift_add', args=[page]))

    return dict(form=form, page=page, giftID=giftID, rowID=rowID)


#===================================== Download
def download_gift():
    #----------Task assaign----------
    task_id = 'rm_doctor_manage'
    task_id_view = 'rm_doctor_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (access_permission_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL('gift_add'))

    #   ---------------------

    c_id = session.cid

    qset = db()
    qset = qset(db.sm_doctor_ppm.cid == c_id)
    if (session.btn_filter_gift):

        if (session.searchType_gift == 'GiftID'):
            qset = qset(db.sm_doctor_ppm.gift_id == session.searchValue_gift)

        elif (session.searchType_gift == 'Status'):
            qset = qset(db.sm_doctor_ppm.status == session.searchValue_gift)

    records = qset.select(db.sm_doctor_ppm.ALL, orderby=db.sm_doctor_ppm.gift_name)

    #---------
    myString = 'PPM List\n\n'
    myString += 'PPM ID,Name,Description,Status\n'
    for rec in records:
        giftId = str(rec.gift_id)
        giftName = str(rec.gift_name).replace(',', ' ')
        des = str(rec.des).replace(',', ' ')
        status = str(rec.status)

        myString += giftId + ',' + giftName + ',' + des + ',' + status + '\n'

    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_ppm.csv'
    return str(myString)

def batch_upload_gift():
    task_id = 'rm_doctor_manage'
    access_permission = check_role(task_id)
    if (access_permission == False):
        session.flash = 'Access is Denied !'
        redirect (URL('gift_add'))

    #----------
    response.title = 'PPM Batch Upload'

    c_id = session.cid

    btn_upload = request.vars.btn_upload
    count_inserted = 0
    count_error = 0
    error_str = ''
    total_row = 0
    if btn_upload == 'Upload':
        excel_data = str(request.vars.excel_data)
        inserted_count = 0
        error_count = 0
        error_list = []
        row_list = excel_data.split('\n')
        total_row = len(row_list)

        gift_list_excel = []
        gift_list_exist = []
        excelList = []

        ins_list = []
        ins_dict = {}

        for i in range(total_row):
            if i >= 30:
                break
            else:
                row_data = row_list[i]
                coloum_list = row_data.split('\t')
                if len(coloum_list) == 3:
                    gift_list_excel.append(str(coloum_list[0]).strip().upper())

        #        create client list
        existClientRows = db((db.sm_doctor_ppm.cid == c_id) & (db.sm_doctor_ppm.gift_id.belongs(gift_list_excel))).select(db.sm_doctor_ppm.gift_id, orderby=db.sm_doctor_ppm.gift_id)
        gift_list_exist = existClientRows.as_list()

        #   --------------------
        for i in range(total_row):
            if i >= 30:
                break
            else:
                row_data = row_list[i]
            coloum_list = row_data.split('\t')

            if len(coloum_list) == 3:
                gift_id = str(coloum_list[0]).strip().upper()
                gift_name = str(coloum_list[1]).strip().upper().replace('|', ' ')
                des = str(coloum_list[2]).strip()
                status = 'ACTIVE'
                
                if not(gift_id == '' or gift_name == ''):
                    try:
                        duplicate_gift = False

                        #----------- check duplicate
                        for i in range(len(gift_list_exist)):
                            myRowData = gift_list_exist[i]
                            strpk1GftId = myRowData['gift_id']
                            if (str(strpk1GftId).strip() == gift_id):
                                duplicate_gift = True
                                break

                        #-----------------
                        if(duplicate_gift == False):
                            if gift_id not in excelList:
                                excelList.append(gift_id)

                                # Create insert list
                                ins_dict = {'cid':c_id, 'gift_id':gift_id, 'gift_name':gift_name, 'des':des, 'status':status}
                                ins_list.append(ins_dict)
                                count_inserted += 1
                            else:
                                error_data = row_data + '(duplicate in excel!)\n'
                                error_str = error_str + error_data
                                count_error += 1
                                continue
                        else:
                            error_data = row_data + '(duplicate PPM ID)\n'
                            error_str = error_str + error_data
                            count_error += 1
                            continue

                    except:
                        error_data = row_data + '(error in process)\n'
                        error_str = error_str + error_data
                        count_error += 1
                        continue
                else:
                    error_data = row_data + '(PPM ID and name needed)\n'
                    error_str = error_str + error_data
                    count_error += 1
                    continue
            else:
                error_data = row_data + '(3 columns need in a row)\n'
                error_str = error_str + error_data
                count_error += 1
                continue

        if error_str == '':
            error_str = 'No error'

        if len(ins_list) > 0:
            inCountList = db.sm_doctor_ppm.bulk_insert(ins_list)

    return dict(count_inserted=count_inserted, count_error=count_error, error_str=error_str, total_row=total_row)


#=============================

