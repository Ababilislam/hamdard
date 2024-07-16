
from random import randint
#---------------------------- ADD VALIDATION
def validation_sample_add(form):
    c_id = session.cid
    item_id = str(form.vars.item_id).strip().upper()
    name = str(form.vars.name).replace('|', ' ').strip().upper()

    #------- check duplicate
    existRows = db((db.sm_doctor_sample.cid == c_id) & (db.sm_doctor_sample.item_id == item_id)).select(db.sm_doctor_sample.item_id, limitby=(0, 1))
    if existRows:
        form.errors.item_id = 'already exist'
    else:
        form.vars.item_id = item_id
        form.vars.name = name

#---------------------------- ADD
def sample_add():
    task_id = 'rm_doctor_manage'
    task_id_view = 'rm_doctor_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (access_permission_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

    response.title = 'Sample Item'

    c_id = session.cid

    #   ---------------------
    form = SQLFORM(db.sm_doctor_sample,
                  fields=['item_id', 'name', 'des', 'status'],
                  submit_button='Save'
                  )

    form.vars.cid = c_id
    if form.accepts(request.vars, session,onvalidation=validation_sample_add): 
       response.flash = 'Submitted Successfully'

    #  ---------------filter-------
    btn_filter_sample = request.vars.btn_filter
    btn_all = request.vars.btn_filter_all
    reqPage = len(request.args)
    if btn_filter_sample:
       # return btn_filter_sample
        session.btn_filter_sample = btn_filter_sample
        session.searchType_sample = str(request.vars.search_type).strip()
        session.searchValue_sample = str(request.vars.search_value).strip().upper()
        reqPage = 0
    elif btn_all:
        # return btn_all
        session.btn_filter_sample = None
        session.searchType_sample = None
        session.searchValue_sample = None
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
    qset = qset(db.sm_doctor_sample.cid == c_id)
    if (session.btn_filter_sample):

        if (session.searchType_sample == 'ItemID'):
            qset = qset(db.sm_doctor_sample.item_id == session.searchValue_sample)

        elif (session.searchType_sample == 'Status'):
            qset = qset(db.sm_doctor_sample.status == session.searchValue_sample)

    records = qset.select(db.sm_doctor_sample.ALL, orderby=~db.sm_doctor_sample.item_id, limitby=limitby)

    return dict(form=form, records=records, page=page, items_per_page=items_per_page, access_permission=access_permission)


#---------------------------- EDIT VALIDATION
def validation_sample_edit(form):
    c_id = session.cid
    name = str(form.vars.name).strip().upper().replace('|', ' ')
    form.vars.name = name

#---------------------------- EDIT
def sample_edit():
    task_id = 'rm_doctor_manage'
    access_permission = check_role(task_id)
    if (access_permission == False):
        session.flash = 'Access is Denied !'
        redirect (URL('sample_add'))
        
    #   ---------------------
    response.title = 'Sample -Edit'
    
    c_id = session.cid
    
    page = request.args(0)
    rowID = request.args(1)
    itemID = request.args(2)

    record = db.sm_doctor_sample(rowID) or redirect(URL('sample_add'))

    form = SQLFORM(db.sm_doctor_sample,
                  record=record,
                  deletable=True,
                  fields=['name', 'des', 'status'],
                  submit_button='Update'
                  )

    if form.accepts(request.vars):#, session, onvalidation=validation_sapmle_edit):
        response.flash = 'Updated Successfully'
        redirect(URL('sample_add', args=[page]))

    return dict(form=form, page=page, itemID=itemID, rowID=rowID)


#===================================== Download
def download_sample():
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

def batch_upload_sample():
    task_id = 'rm_doctor_manage'
    access_permission = check_role(task_id)
    if (access_permission == False):
        session.flash = 'Access is Denied !'
        redirect (URL('sample_add'))

    #----------
    response.title = 'Sample Batch Upload'

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

        sample_list_excel = []
        sample_list_exist = []
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
                    sample_list_excel.append(str(coloum_list[0]).strip().upper())

        #        create client list
        existItemRows = db((db.sm_doctor_sample.cid == c_id) & (db.sm_doctor_sample.item_id.belongs(sample_list_excel))).select(db.sm_doctor_sample.item_id, orderby=db.sm_doctor_sample.item_id)
        sample_list_exist = existItemRows.as_list()

        #   --------------------
        for i in range(total_row):
            if i >= 30:
                break
            else:
                row_data = row_list[i]
            coloum_list = row_data.split('\t')

            if len(coloum_list) == 3:
                item_id = str(coloum_list[0]).strip().upper()
                name = str(coloum_list[1]).strip().upper().replace('|', ' ')
                des = str(coloum_list[2]).strip()
                status = 'ACTIVE'
                
                if not(item_id == '' or name == ''):
                    try:
                        duplicate_item = False

                        #----------- check duplicate
                        for i in range(len(sample_list_exist)):
                            myRowData = sample_list_exist[i]
                            strpk1GftId = myRowData['item_id']
                            if (str(strpk1GftId).strip() == item_id):
                                duplicate_item = True
                                break

                        #-----------------
                        if(duplicate_item == False):
                            if item_id not in excelList:
                                excelList.append(item_id)

                                # Create insert list
                                ins_dict = {'cid':c_id, 'item_id':item_id, 'name':name, 'des':des, 'status':status}
                                ins_list.append(ins_dict)
                                count_inserted += 1
                            else:
                                error_data = row_data + '(duplicate in excel!)\n'
                                error_str = error_str + error_data
                                count_error += 1
                                continue
                        else:
                            error_data = row_data + '(duplicate Sample ID)\n'
                            error_str = error_str + error_data
                            count_error += 1
                            continue

                    except:
                        error_data = row_data + '(error in process)\n'
                        error_str = error_str + error_data
                        count_error += 1
                        continue
                else:
                    error_data = row_data + '(Sample ID and name needed)\n'
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
            inCountList = db.sm_doctor_sample.bulk_insert(ins_list)

    return dict(count_inserted=count_inserted, count_error=count_error, error_str=error_str, total_row=total_row)


#=============================

