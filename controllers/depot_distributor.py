# Controller
# http://127.0.0.1:8000/ipi_combined/depot_distributor/index

def index():
    cid=session.cid
    if (cid=='' or cid==None):
        # return 'dgngn'
        redirect (URL('default','index'))
    # return session.cid
    response.title='Depot Distributor'
    today = str(date_fixed)
    btn_submit = request.vars.submit
    btn_filter_item = request.vars.btn_filter_item
    btn_all = request.vars.btn_all
    reqPage = len(request.args)
    condition=""
    


    if btn_submit:
        # return "a"
        # return cid
        depot_ = str(request.vars.depot_id)
        if depot_!=None or depot_!="":
            try:
                depot_id = str(depot_).split("|")[0]
                depot_name = str(depot_).split("|")[1]
            except:
                depot_id = ""
                depot_name =""
        
        # return depot_id,depot_name
        # depot_id = session.depot_id
        dist_id = str(request.vars.dist_id)
        dist_name = str(request.vars.dist_name)
        disc_price = str(request.vars.dist_disc_percent)
        # return today
        # return f"depot_id ={depot_id} route_id = {route_id} route_name= {route_name} route_desc = {route_desc}"
        if (depot_id=='' ) or (dist_id=='') or (dist_name=="") or (disc_price=="") :

            session.flash = 'Required All Value'
            return redirect(URL('index'))
        # try:
        #     if disc_price.isdigit():
        #         print("ok")
        #     # if disc_price.isinstance(float)
        # except:
        #     session.flash = 'Required Discount price as a value'
        #     return redirect(URL('index'))
        if (float(disc_price)<0) :
            session.flash = 'Required Discount Price as a Positive Value'
            return redirect(URL('index'))
        
        check_depot_id = f"select depot_id,name from sm_depot where cid = '{cid}' and depot_id='{depot_id}';"
        # return check_depot_id
        chk_depot_query = db.executesql(check_depot_id,as_dict=True)
        if len(chk_depot_query)>0:
            check_depot_dist_already_exist_sql= f"select depot_id,depot_name,dist_id,dist_name from sm_depot_distributor where cid = '{cid}' and depot_id='{depot_id}' and dist_id='{dist_id}';"
            # return check_depot_dist_already_exist_sql
            chk_input_data_exists = db.executesql(check_depot_dist_already_exist_sql,as_dict=True)
            if len(chk_input_data_exists)>0:
                session.flash = 'depot and distributor already exists'
                return redirect(URL('index'))
            else:
                depot_info_insert = f"INSERT INTO `sm_depot_distributor` SET `cid` = '{cid}',`depot_id` = '{depot_id}',`depot_name` = '{depot_name}',`dist_id` = '{dist_id}',`dist_name` = '{dist_name}',`dist_disc_percent` = '{disc_price}',`created_on` = '{today}',`created_by` = '{session.user_id}';"
            # return depot_info_insert
                depot_query = db.executesql(depot_info_insert)
                session.flash = " Insert Successful"
            return redirect(URL('index'))

    # --------paging
    session.items_per_page = 20
    if reqPage:
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = session.items_per_page
    if(page==0):
        limitby = (page * items_per_page, (page + 1) * items_per_page)
    else:
        limitby = ((page* items_per_page), items_per_page)
    # --------end paging
    if btn_filter_item:
        item_id_filter = request.vars.item_id_filter
        route_id_filter = request.vars.route_id_filter
        # return item_id_filter
        # return route_id_filter
        condition = ''

        if item_id_filter !='':
            session.item_id_filter = item_id_filter
            try:
                item_id_filter = str(item_id_filter).split('|')[0]
            except:
                session.client_id_filter = ''
            condition = condition + " and depot_id = '"+str(item_id_filter)+"'"
        if route_id_filter !='':
            session.route_id_filter = route_id_filter
            try:
                route_id_filter = str(route_id_filter).split('|')[0]
            except:
                session.client_id_filter = ''
            condition = condition + " and dist_id = '"+str(route_id_filter)+"'"
        reqPage=0
        session.condition = condition
    if btn_all == "All":
        condition = ''
        session.item_id_filter = ''
        session.route_id_filter = ''
        session.condition = condition
        reqPage=0

    condition=session.condition
    if condition==None or condition=='None':
        condition=''
    # view query
    get_all_sql = f"SELECT * FROM `sm_depot_distributor` WHERE cid='{cid}' {condition} order by id desc limit %d, %d;" % limitby
    # return get_all_sql
    all_data = db.executesql(get_all_sql,as_dict=True)
    total_rec = len(db.executesql(f"SELECT * FROM `sm_depot_distributor` WHERE cid='{cid}' {condition} order by id desc;",as_dict=True))
    return dict(all_data=all_data,total_rec=total_rec,page=page,items_per_page=items_per_page)

    

    return locals()


def depot_entry_edit():
    c_id=session.cid
    if (c_id=='' or c_id==None):
        redirect (URL('default','index'))
    item_id =request.args(0)
    itm= request.vars.itm
    # return item_id,"+=",itm
    

    # return itm
    
    update_btn = request.vars.update_btn
    delete_btn = request.vars.delete_btn
    

    select_item_record_sql = f"SELECT * FROM sm_depot_distributor WHERE cid = '{c_id}' AND id ='"+str(item_id)+"' GROUP BY id LIMIT 1;"
    # return select_item_record_sql
    selected_item_record = db.executesql(select_item_record_sql, as_dict = True)
    # return 11

    # if len(selected_ret_record) != 0 :
    id=""
    depot_id =''
    depot_name=''
    dist_id=''
    dist_name=''
    dist_disc_percent=''
    created_on=''
    created_by=''
    updated_on=''
    updated_by=''

    for i in range(len(selected_item_record)):
        depot_distributor = selected_item_record[i]
        id = str(depot_distributor["id"])
        # print("id=",id)
        c_id = str(depot_distributor["cid"])
        depot_id = str(depot_distributor["depot_id"])
        depot_name = str(depot_distributor["depot_name"])
        dist_id = str(depot_distributor["dist_id"])
        dist_name = str(depot_distributor["dist_name"])
        dist_disc_percent = str(depot_distributor["dist_disc_percent"])
        created_on = str(depot_distributor["created_on"])
        created_by = str(depot_distributor["created_by"])
        updated_on = str(depot_distributor["updated_on"])
        updated_by = str(depot_distributor["updated_by"])
        
    
    
    if update_btn:
        item = str(request.vars.item_id)
        # return item
        dist_id = str(request.vars.dist_id)
        dist_name = str(request.vars.dist_name)
        dist_disc_percent = str(request.vars.dist_disc_percent)
        updated_on = str(date_fixed)
        updated_by = session.user_id
        # return  f"item:{item} route_no:{route_no} route_name:{route_name} route_desc:{route_des} updated_on: {updated_on} updated_by:{updated_by}"

        update_sql = f"UPDATE sm_depot_distributor SET dist_id = '{dist_id}', dist_name = '{dist_name}', dist_disc_percent = '{dist_disc_percent}', updated_on = '{updated_on}',updated_by = '{updated_by}' where id = '{item}';"
        # return update_sql
        up_date = db.executesql(update_sql)
        session.flash = 'Update Successfully!'

        redirect(URL('depot_distributor','index'))
    if delete_btn:
        item = str(request.vars.item_id)
        # return item
        delete_sql = f"DELETE FROM sm_depot_distributor WHERE cid = '{c_id}' AND id='{item}' LIMIT 1;"
        # return delete_sql
        delete = db.executesql(delete_sql)

        session.flash = 'Deleted Successfully!'

        redirect(URL('depot_distributor','index'))
            
    return dict(item_id=id,depot_id=depot_id,depot_name=depot_name,dist_id=dist_id,dist_name=dist_name,dist_disc_percent=dist_disc_percent,created_on=created_on,created_by=created_by,updated_on=updated_on,updated_by=updated_by)


def depot_Download():
    cid = session.cid
    if (cid=='' or cid==None):
        redirect (URL('default','index'))
    condition = ''
    condition = session.condition
    if condition==None or condition=='None':
        condition=''

    download_sql = "select * from sm_depot_distributor where cid = '"+cid+"' "+condition+" order by id desc;"
    download_records = db.executesql(download_sql, as_dict=True)
    
    myString = 'Depot \n\n'
    myString += 'Depot Id,Depot Name,Dist Id, Dist Name,Dist Discount Percent,Entry Date,Added By,Updated Date,Updated By,\n'
    total=0
    attTime = ''
    totalCount = 0

    for i in range(len( download_records)):
        recordsStr =  download_records[i]
        depot_id=str(recordsStr["depot_id"])
        depot_name=str(recordsStr["depot_name"])
        dist_id=str(recordsStr["dist_id"])
        dist_name=str(recordsStr["dist_name"])
        dist_disc_percent=str(recordsStr["dist_disc_percent"])
        created_on=str(recordsStr["created_on"])
        created_by=str(recordsStr["created_by"])
        updated_on=str(recordsStr["updated_on"])
        if updated_on=="" or updated_on=="None" or updated_on==None:
            updated_on=""
        updated_by=str(recordsStr["updated_by"])
        if updated_by=="" or updated_by=="None" or updated_by==None:
            updated_by=""
        # return str(created_on)

        myString += str(depot_id) + ',' + str(depot_name) + ',' + str(dist_id) + ',' + str(dist_name) + ',' + str(dist_disc_percent) + ',' + str(created_on) + ',' + str(created_by)+ ',' + str(updated_on)+ ',' + str(updated_by) +'\n'

    # Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_depot.csv'
    return str(myString)    

def depot_batch_upload():
    cid = session.cid
    if (cid=='' or cid==None):
        redirect (URL('default','index'))
    response.title = 'Depot Batch Upload'

    btn_upload = request.vars.btn_upload
    # return btn_upload
    count_inserted = 0
    count_error = 0
    error_str = ''
    total_row = 0
    slNo = 0
    # return "a"
    if btn_upload:
        # return "b"
        excel_data = str(request.vars.excel_data)
        inserted_count = 0
        error_count = 0
        error_list = []
        row_list = excel_data.split('\n')
        total_row = len(row_list)

        item_id_list_excel = []

        valid_item_id_list = []
        excelList = []

        ins_list = []
        ins_dict = {}
        # return total_row
        for i in range(total_row):
            # return 10
            if i >= 100:
                # return 101
                break
            else:
                row_data = row_list[i]
                coloum_list = row_data.split('\t')
                if len(coloum_list) == 6:
                    item_id_list_excel.append(str(coloum_list[0]).strip().upper())

        # create list
        for i in range(total_row):
            if i >= 100:
                break
            else:
                row_data = row_list[i]
            coloum_list = row_data.split('\t')

            if len(coloum_list) != 5:
                error_data = row_data + '(5 columns need in a row)\n'
                error_str = error_str + error_data
                count_error += 1
                continue
            else:

                # id_excel = str(coloum_list[0]).strip()
                dipot_id_excel = str(coloum_list[0]).strip()
                dep_id = dipot_id_excel.split("|")[0]
                dipot_name_excel = str(coloum_list[1]).strip()
                dist_id_excel = str(coloum_list[2]).strip()
                dist_name_excel = str(coloum_list[3]).strip()
                disc_price_excel = str(coloum_list[4]).strip()
                created_on = date_fixed
                created_by = session.user_id
                
                # return dipot_id_excel,"  :",dep_id
                try:
                    float_val = float(disc_price_excel)
                except ValueError:
                    error_data=row_data+'(Invalid Entry for Dist Discount Percentage)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue


                if (dipot_id_excel==''or dipot_id_excel == 'NONE' or dipot_id_excel==None) and (dipot_name_excel=='' or dipot_name_excel== 'NONE' or dipot_name_excel==None) and (dist_id_excel=='' or dist_id_excel == 'NONE' or dist_id_excel==None) and (dist_name_excel=='' or dist_name_excel == 'NONE' or dist_name_excel==None) and (disc_price_excel=='' or disc_price_excel == 'NONE' or disc_price_excel==None):
                    error_data=row_data+'(Required all value)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue 
                
                else:
                    
                    existCheckRows= " SELECT * FROM sm_depot_distributor WHERE cid='"+str(cid)+"' and depot_id = '"+dipot_id_excel+"' and dist_id='"+dist_id_excel+"';"
                    # return existCheckRows
                    existCheck = db.executesql(existCheckRows)
                    # return existCheck

                    if len(existCheck) > 0:
                        error_data=row_data+'(Duplicate Entry!!)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:
                        check_depot_id = f"select depot_id,name from sm_depot where cid = '{cid}' and depot_id='{dep_id}';"
                        chk_depot_query = db.executesql(check_depot_id,as_dict=True)
                        if len(chk_depot_query)>0:
                            # try:
                            insert_sql = "INSERT INTO sm_depot_distributor (cid,depot_id,depot_name,dist_id,dist_name,dist_disc_percent,created_on,created_by) VALUE ('"+str(cid)+"','"+str(dipot_id_excel)+"', '"+str(dipot_name_excel)+"','"+str(dist_id_excel)+"','"+str(dist_name_excel)+"', '"+str(disc_price_excel)+"','"+str(created_on)+"','"+str(created_by)+"');"
                            # return insert_sql
                            batch_insert_list = db.executesql(insert_sql)
                            # return batch_insert_list
                            count_inserted+=1
                            # except Exception as e:
                            #     error_str = 'Please do not insert special charachter.'
                            #     # return error_str
                        else:
                            error_data = row_data+" (this depot does not exists) \n"
                            error_str=error_str+error_data
                            count_error+=1

        if error_str == '':
            error_str = 'No error'

    return dict(count_inserted=count_inserted, count_error=count_error, error_str=error_str, total_row=total_row)




def get_route_id_list():
    c_id = session.cid
    if (c_id=='' or c_id==None):
        redirect (URL('default','index'))
    retStrs = ''
    itemlistRows_sql = "select dist_id,dist_name from sm_depot_distributor where cid = '"+c_id+"';"
    itemlistRows = db.executesql(itemlistRows_sql, as_dict=True)

    for i in range(len(itemlistRows)):
        item_list_dict=itemlistRows[i]   
        dist_id=str(item_list_dict["dist_id"])
        dist_name=str(item_list_dict["dist_name"])   
        if retStrs == '':
            retStrs = dist_id+'|'+dist_name
        else:
            retStrs += ',' + dist_id+'|'+dist_name
    
    return retStrs


def get_depot_id_list():
    c_id = session.cid
    if (c_id=='' or c_id==None):
        redirect (URL('default','index'))
    retStr = ''

    itemlistRows_sql = "select depot_id,name from sm_depot where cid = '"+c_id+"' group by depot_id;"
    # return itemlistRows_sql
    itemlistRows = db.executesql(itemlistRows_sql, as_dict=True)

    for i in range(len(itemlistRows)):
        item_list_dict=itemlistRows[i]   
        depot_id=str(item_list_dict["depot_id"])
        d_name=str(item_list_dict["name"])   
        if retStr == '':
            retStr = depot_id+'|'+d_name
        else:
            retStr += ',' + depot_id+'|'+d_name
    
    return retStr

def get_depot_id_list1():
    c_id = session.cid
    if (c_id=='' or c_id==None):
        redirect (URL('default','index'))
    refstr = ''

    itemlistRows_sql = "select depot_id,name from sm_depot where cid = '"+c_id+"' group by depot_id;"
    # return itemlistRows_sql
    itemlistRows = db.executesql(itemlistRows_sql, as_dict=True)

    for i in range(len(itemlistRows)):
        item_list_dict=itemlistRows[i]   
        depot_id=str(item_list_dict["depot_id"])
        d_name=str(item_list_dict["name"])   
        if refstr == '':
            refstr = depot_id+'|'+d_name
        else:
            refstr += ',' + depot_id+'|'+d_name
    
    return refstr



def get_dist_id_list_fr_depot():
    retStra = ''
    c_id = session.cid
    depot_id=str(request.vars.depot_id).split('|')[0]
    # print(depot_id)
    if (c_id=='' or c_id==None):
        redirect (URL('default','index'))
    
    if depot_id=="":
        itemlistRows_sql = "select dist_id,dist_name from sm_depot_distributor where cid = '"+c_id+"';"
        # return itemlistRows_sql
        # print(itemlistRows_sql)
        itemlistRows = db.executesql(itemlistRows_sql, as_dict=True)
    else:
        itemlistRows_sql = "select dist_id,dist_name from sm_depot_distributor where cid = '"+c_id+"' and depot_id='"+depot_id+"';"
        # return 
        # return itemlistRows_sql
        itemlistRows = db.executesql(itemlistRows_sql, as_dict=True)

    for i in range(len(itemlistRows)):
        item_list_dict=itemlistRows[i]   
        dist_id=str(item_list_dict["dist_id"])
        dist_name=str(item_list_dict["dist_name"])   
        if retStra == '':
            retStra = dist_id+'|'+dist_name
        else:
            retStra += ',' + dist_id+'|'+dist_name
    
    return retStra