

#-------------------------Check for sync----------------------------

def sync_check():
    my_str = request.args(0)

    my_str = get_decript(my_str)

    if my_str == '':
        fail = "failed";
        fail = get_encript(fail);
        return "<STARTSTART>" + fail + "<ENDEND>";
    elif (my_str != ""):
        separator_url = '<url>'
        cid = ''
        user_id = ''
        password = ''
        mac_get = ''
        depot_get = ''
        url_list = my_str.split(separator_url, my_str.count(separator_url))
        cid = url_list[0]
        user_type = url_list[1]
        user_id = url_list[2]
        password = url_list[3]
        mac_get = url_list[4]



        user_type_check = str(user_type).upper()
        depot_mac = 0
#        ====================if user type HO===============
        if (user_type_check == 'HO'):
            com_valid_user = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).select()
            if com_valid_user:
    #            return 'Valid user'

                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.s_value

                flag_mac = '0'
    #  Set mac in db
                if depot_mac == '0':
                    flag_mac = 1
                    mac_update = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).update(s_value=mac_get)
                elif(depot_mac != '0'):
                    check_mac = db((db.sm_settings.cid == str(cid)) & (db.sm_settings.s_key == password) & (db.sm_settings.s_value == mac_get)).select()
                    if check_mac:
                        flag_mac = 2
                    else:
                        fail = "failed";
    #                    fail = get_encript(fail)
                        return "<STARTSTART>" + fail + "<ENDEND>"
                else:
                    fail = "failed";
                    return "<STARTSTART>" + fail + "<ENDEND>"
            else:
                fail = "failed";
                return "<STARTSTART>" + fail + "<ENDEND>"
#========================if user type depot===================                
        else:
            com_valid_user = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password)).select()
            if com_valid_user:
                depot_mac = 0
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.mac

                flag_mac = '0'
    #  Set mac in db
                if depot_mac == '0':
                    flag_mac = 1
                    mac_update = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id)).update(mac=mac_get)
                elif(depot_mac != '0'):
                    check_mac = db((db.sm_depot.cid == str(cid)) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password) & (db.sm_depot.mac == mac_get)).select(db.sm_depot.mac)
#                    return db._lastsql
                    if check_mac:
                        flag_mac = 2
                    else:
                        fail = "failed";
                        return "<STARTSTART>" + fail + "<ENDEND>"
                else:
                        fail = "failed";
                        return "<STARTSTART>" + fail + "<ENDEND>"


#        return depot_mac    
        if(depot_mac == mac_get):

            query_day = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'SYNC_DAY')).select(db.sm_settings.s_value, limitby=(0, 1))
            day_value = ''
#            return db._lastsql
            for query_day in query_day:
                day_value = query_day.s_value
#            return db._lastsql

            query_count = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'SYNC_COUNT')).select(db.sm_settings.s_value, limitby=(0, 1))
            count_value = ''
            for query_count in query_count:
                count_value = query_count.s_value


            query_limit = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'SYNC_LIMIT')).select(db.sm_settings.s_value, limitby=(0, 1))
            limit_value = ''
            for query_limit in query_limit:
                limit_value = query_limit.s_value

            if (current_date != day_value):
                count_update = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == "SYNC_COUNT")).update(s_value="1")
                day_update = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == "SYNC_DAY")).update(s_value=current_date)

                return "<STARTSTART>" + "Success" + "<ENDEND>"
            elif ((current_date == day_value) & (int(count_value) <= int(limit_value))):
                count_update = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == "SYNC_COUNT")).update(s_value=int(count_value) + 1)
                return "<STARTSTART>" + "Success" + "<ENDEND>"
            else:
                return "<STARTSTART>" + "failed" + "<ENDEND>"
#            return "day"+str(day_value)+"date"+str(current_date)+"limit"+str(limit_value)+"count"+str(count_value)

#            return "day"+str(day_value)+"limit"+str(limit_value)+"count"+str(count_value)

        else :
            fail = "failed"

            return "<STARTSTART>" + fail + "<ENDEND>"



#-------------------------Sync----------------------------
#//http://localhost/mreport_depot/SyncDownload/request_data/Fast<url>nadira<url>nadira1234<url>1234<url>sm_attendance,sm_order,sm_delivery
#//http://localhost/mreport_003/syncdownload_download_manager/request_data/2840343044844939345044744139543452343443430433438447430393450447441395443430433438447430382383384385393450447441395382383384385393450447441395448442428430449449434443433430443432434377448442428444447433434447377448442428433434441438451434447454

def item():
    my_str = request.args(0)

    my_str = get_decript(my_str)

    if my_str == '':
        fail = "failed";
        fail = get_encript(fail);
        return "<STARTSTART>" + fail + "<ENDEND>";
    elif (my_str != ""):
        separator_url = '<url>'
        cid = ''
        user_id = ''
        password = ''
        mac_get = ''
        depot_get = ''
        url_list = my_str.split(separator_url, my_str.count(separator_url))
        cid = url_list[0]
        user_type = url_list[1]
        user_id = url_list[2]
        password = url_list[3]
        mac_get = url_list[4]



        user_type_check = str(user_type).upper()
        depot_mac = 0
#        ====================if user type HO===============
        if (user_type_check == 'HO'):
            com_valid_user = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).select()
            if com_valid_user:
    #            return 'Valid user'

                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.s_value

                flag_mac = '0'
    #  Set mac in db
                if depot_mac == '0':
                    flag_mac = 1
                    mac_update = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).update(s_value=mac_get)
                elif(depot_mac != '0'):
                    check_mac = db((db.sm_settings.cid == str(cid)) & (db.sm_settings.s_key == password) & (db.sm_settings.s_value == mac_get)).select()
                    if check_mac:
                        flag_mac = 2
                    else:
                        fail = "failed";
    #                    fail = get_encript(fail)
                        return "<STARTSTART>" + fail + "<ENDEND>"
                else:
                    fail = "failed";
                    return "<STARTSTART>" + fail + "<ENDEND>"
            else:
                fail = "failed";
                return "<STARTSTART>" + fail + "<ENDEND>"
#========================if user type depot===================                
        else:
            com_valid_user = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password)).select()
            if com_valid_user:
                depot_mac = 0
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.mac

                flag_mac = '0'
    #  Set mac in db
                if depot_mac == '0':
                    flag_mac = 1
                    mac_update = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id)).update(mac=mac_get)
                elif(depot_mac != '0'):
                    check_mac = db((db.sm_depot.cid == str(cid)) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password) & (db.sm_depot.mac == mac_get)).select(db.sm_depot.mac)
#                    return db._lastsql
                    if check_mac:
                        flag_mac = 2
                    else:
                        fail = "failed";
                        return "<STARTSTART>" + fail + "<ENDEND>"
                else:
                        fail = "failed";
                        return "<STARTSTART>" + fail + "<ENDEND>"


#        return depot_mac    
        if(depot_mac == mac_get):



            query_data = db((db.sm_item.cid == cid)).select(db.sm_item.ALL, orderby=db.sm_item.item_id)

            return_value = ''
#            return db._lastsql
            for row_query_data in query_data:
                return_value = str(return_value) + str(row_query_data.item_id) + "<fd>" + str(row_query_data.name) + "<fd>" + str(row_query_data.des) + "<fd>" + str(row_query_data.category_id) + "<fd>" + str(row_query_data.unit_type) + "<fd>" + str(row_query_data.manufacturer) + "<fd>" + str(row_query_data.price) + "<fd>" + str(row_query_data.dist_price) + "<fd><rd>"
#            return db._lastsql
            return "<STARTSTART>" + str(return_value) + "<ENDEND>"

        else :
            fail = "failed"

            return "<STARTSTART>" + fail + "<ENDEND>"



def rep():
    my_str = request.args(0)

    my_str = get_decript(my_str)

    if my_str == '':
        fail = "failed";
        fail = get_encript(fail);
        return "<STARTSTART>" + fail + "<ENDEND>";
    elif (my_str != ""):
        separator_url = '<url>'
        cid = ''
        user_id = ''
        password = ''
        mac_get = ''
        depot_get = ''
        url_list = my_str.split(separator_url, my_str.count(separator_url))
        cid = url_list[0]
        user_type = url_list[1]
        user_id = url_list[2]
        password = url_list[3]
        mac_get = url_list[4]



        user_type_check = str(user_type).upper()
        depot_mac = 0
#        ====================if user type HO===============

        if (user_type_check == 'HO'):
            com_valid_user = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).select()
            if com_valid_user:
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.s_value


        elif (user_type_check == 'DEPOT'):
            com_valid_user = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password)).select()
            if com_valid_user:
                depot_mac = 0
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.mac


        else:
            fail = "failed";
            return "<STARTSTART>" + fail + "<ENDEND>"


        if(depot_mac == mac_get):
            query_data = db((db.sm_rep.cid == cid)).select(db.sm_rep.ALL, orderby=db.sm_rep.rep_id)
            return_value = ''
#            return db._lastsql
            for row_query_data in query_data:
                return_value = str(return_value) + str(row_query_data.rep_id) + "<fd>" + str(row_query_data.name) + "<fd>" + str(row_query_data.mobile_no) + "<fd>" + str(row_query_data.status) + "<fd>" + str(row_query_data.depot_id) + "<fd>" + str(row_query_data.user_type) + "<fd>" + str(row_query_data.level_id) + "<fd><rd>"
#            return db._lastsql
            return "<STARTSTART>" + str(return_value) + "<ENDEND>"

        else :
            fail = "failed"

            return "<STARTSTART>" + fail + "<ENDEND>"




def level():
    my_str = request.args(0)

    my_str = get_decript(my_str)

    if my_str == '':
        fail = "failed";
        fail = get_encript(fail);
        return "<STARTSTART>" + fail + "<ENDEND>";
    elif (my_str != ""):
        separator_url = '<url>'
        cid = ''
        user_id = ''
        password = ''
        mac_get = ''
        depot_get = ''
        url_list = my_str.split(separator_url, my_str.count(separator_url))
        cid = url_list[0]
        user_type = url_list[1]
        user_id = url_list[2]
        password = url_list[3]
        mac_get = url_list[4]
        record_start_s = url_list[5]
        record_start = int(record_start_s)


        user_type_check = str(user_type).upper()
        depot_mac = 0
#        ====================if user type HO===============

        if (user_type_check == 'HO'):
            com_valid_user = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).select()
            if com_valid_user:
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.s_value


        elif (user_type_check == 'DEPOT'):
            com_valid_user = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password)).select()
            if com_valid_user:
                depot_mac = 0
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.mac


        else:
            fail = "failed";
            return "<STARTSTART>" + fail + "<ENDEND>"


        if(depot_mac == mac_get):
            limit = record_start + 500
#            query_data=db((db.sm_level.cid==cid)).select(db.sm_level.level_id,db.sm_level.level_name,db.sm_level.parent_level_id,db.sm_level.is_leaf,db.sm_level.depot_id,db.sm_level.depth,orderby=db.sm_level.level_id,limitby=(record_start,limit))                  
            query_data = db((db.sm_level.cid == cid)).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.parent_level_id, db.sm_level.is_leaf, db.sm_level.depot_id, db.sm_level.depth, limitby=(record_start, limit))
            return_value = ''
#            return db._lastsql
            for row_query_data in query_data:
                return_value = str(return_value) + str(row_query_data.level_id) + "<fd>" + str(row_query_data.level_name) + "<fd>" + str(row_query_data.parent_level_id) + "<fd>" + str(row_query_data.is_leaf) + "<fd>" + str(row_query_data.depot_id) + "<fd>" + str(row_query_data.depth) + "<fd><rd>"
#            return db._lastsql
            return "<STARTSTART>" + str(return_value) + "<ENDEND>"

        else :
            fail = "failed"

            return "<STARTSTART>" + fail + "<ENDEND>"


def depot():
    my_str = request.args(0)

    my_str = get_decript(my_str)

    if my_str == '':
        fail = "failed";
        fail = get_encript(fail);
        return "<STARTSTART>" + fail + "<ENDEND>";
    elif (my_str != ""):
        separator_url = '<url>'
        cid = ''
        user_id = ''
        password = ''
        mac_get = ''
        depot_get = ''
        url_list = my_str.split(separator_url, my_str.count(separator_url))
        cid = url_list[0]
        user_type = url_list[1]
        user_id = url_list[2]
        password = url_list[3]
        mac_get = url_list[4]



        user_type_check = str(user_type).upper()
        depot_mac = 0
#        ====================if user type HO===============

        if (user_type_check == 'HO'):
            com_valid_user = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).select()
            if com_valid_user:
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.s_value


        elif (user_type_check == 'DEPOT'):
            com_valid_user = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password)).select()
            if com_valid_user:
                depot_mac = 0
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.mac


        else:
            fail = "failed";
            return "<STARTSTART>" + fail + "<ENDEND>"


        if(depot_mac == mac_get):
            query_data = db((db.sm_depot.cid == cid)).select(db.sm_depot.depot_id, db.sm_depot.name, db.sm_depot.op_balance, db.sm_depot.note, db.sm_depot.depot_category, orderby=db.sm_depot.depot_id)
            return_value = ''
#            return db._lastsql
            for row_query_data in query_data:
                return_value = str(return_value) + str(row_query_data.depot_id) + "<fd>" + str(row_query_data.name) + "<fd>" + str(row_query_data.op_balance) + "<fd>" + str(row_query_data.note) + "<fd>" + str(row_query_data.depot_category) + "<fd><rd>"
#            return db._lastsql
            return "<STARTSTART>" + str(return_value) + "<ENDEND>"

        else :
            fail = "failed"

            return "<STARTSTART>" + fail + "<ENDEND>"


def reparea():
    my_str = request.args(0)

    my_str = get_decript(my_str)

    if my_str == '':
        fail = "failed";
        fail = get_encript(fail);
        return "<STARTSTART>" + fail + "<ENDEND>";
    elif (my_str != ""):
        separator_url = '<url>'
        cid = ''
        user_id = ''
        password = ''
        mac_get = ''
        depot_get = ''
        url_list = my_str.split(separator_url, my_str.count(separator_url))
        cid = url_list[0]
        user_type = url_list[1]
        user_id = url_list[2]
        password = url_list[3]
        mac_get = url_list[4]
        record_start_s = url_list[5]
        record_start = int(record_start_s)


        user_type_check = str(user_type).upper()
        depot_mac = 0
#        ====================if user type HO===============

        if (user_type_check == 'HO'):
            com_valid_user = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).select()
            if com_valid_user:
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.s_value


        elif (user_type_check == 'DEPOT'):
            com_valid_user = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password)).select()
            if com_valid_user:
                depot_mac = 0
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.mac


        else:
            fail = "failed";
            return "<STARTSTART>" + fail + "<ENDEND>"


        if(depot_mac == mac_get):
            limit = record_start + 500
            query_data = db((db.sm_rep_area.cid == cid)).select(db.sm_rep_area.rep_id, db.sm_rep_area.area_id, db.sm_rep_area.depot_id, db.sm_rep_area.rep_name, orderby=db.sm_rep_area.rep_id, limitby=(record_start, limit))
            return_value = ''
#            return db._lastsql
            for row_query_data in query_data:
                return_value = str(return_value) + str(row_query_data.rep_id) + "<fd>" + str(row_query_data.area_id) + "<fd>" + str(row_query_data.depot_id) + "<fd>" + str(row_query_data.rep_name) + "<fd><rd>"
#            return db._lastsql
            return "<STARTSTART>" + str(return_value) + "<ENDEND>"

        else :
            fail = "failed"

            return "<STARTSTART>" + fail + "<ENDEND>"



#--------------------------levelMetaData-----------------
def levelMetaData():
    my_str = request.args(0)

    my_str = get_decript(my_str)

    if my_str == '':
        fail = "failed";
        fail = get_encript(fail);
        return "<STARTSTART>" + fail + "<ENDEND>";
    elif (my_str != ""):
        separator_url = '<url>'
        cid = ''
        user_id = ''
        password = ''
        mac_get = ''
        depot_get = ''
        url_list = my_str.split(separator_url, my_str.count(separator_url))
        cid = url_list[0]
        user_type = url_list[1]
        user_id = url_list[2]
        password = url_list[3]
        mac_get = url_list[4]
        record_start_s = url_list[5]
        record_start = int(record_start_s)


        user_type_check = str(user_type).upper()
        depot_mac = 0
#        ====================if user type HO===============

        if (user_type_check == 'HO'):
            com_valid_user = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).select()
            if com_valid_user:
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.s_value


        elif (user_type_check == 'DEPOT'):
            com_valid_user = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password)).select()
            if com_valid_user:
                depot_mac = 0
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.mac


        else:
            fail = "failed";
            return "<STARTSTART>" + fail + "<ENDEND>"


        if(depot_mac == mac_get):
            limit = record_start + 500
            query_data = db((db.sm_level.cid == cid)).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.parent_level_id, db.sm_level.is_leaf, db.sm_level.depot_id, db.sm_level.depth, db.sm_level.level0, db.sm_level.level1, db.sm_level.level2, db.sm_level.level3, db.sm_level.level4, db.sm_level.level5, db.sm_level.level6, db.sm_level.level7, db.sm_level.level8, orderby=db.sm_level.level_id, limitby=(record_start, limit))
            return_value = ''
#            return db._lastsql
            for row_query_data in query_data:
                return_value = str(return_value) + str(row_query_data.level_id) + "<fd>" + str(row_query_data.level_name) + "<fd>" + str(row_query_data.parent_level_id) + "<fd>" + str(row_query_data.is_leaf) + "<fd>" + str(row_query_data.depot_id) + "<fd>" + str(row_query_data.depth) + "<fd>" + str(row_query_data.level0) + "<fd>" + str(row_query_data.level1) + "<fd>" + str(row_query_data.level2) + "<fd>" + str(row_query_data.level3) + "<fd>" + str(row_query_data.level4) + "<fd>" + str(row_query_data.level5) + "<fd>" + str(row_query_data.level6) + "<fd>" + str(row_query_data.level7) + "<fd>" + str(row_query_data.level8) + "<fd><rd>"
#            return db._lastsql
            return "<STARTSTART>" + str(return_value) + "<ENDEND>"

        else :
            fail = "failed"

            return "<STARTSTART>" + fail + "<ENDEND>"
#----------------------------Connect-----------------  


def get_data_limit():
    cid = str(request.args(0)).upper().strip()
    com_data_limit = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'LIMITBY')).select(db.sm_settings.s_value)
    limit = 0
    for com_data_limit in com_data_limit:
        limit = com_data_limit.s_value

    com_data_delay_time = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'DELAY_TIME')).select(db.sm_settings.s_value)
    delay_time = 0
    for com_data_delay_time in com_data_delay_time:
        delay_time = com_data_delay_time.s_value
    return str(limit) + "," + str(delay_time)

def get_table_dl():
    cid = str(request.args(0)).upper().strip()
    com_data_dl = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'TABLE-TO-DL')).select(db.sm_settings.s_value)
    table_dl = ''
    for com_data_dl in com_data_dl:
        table_dl = com_data_dl.s_value
    return table_dl

def requisition_data():
    my_str = request.args(0)

    my_str = get_decript(my_str)

    if my_str == '':
        fail = "failed";
        fail = get_encript(fail);
        return "<STARTSTART>" + fail + "<ENDEND>";
    elif (my_str != ""):
        separator_url = '<url>'
        cid = ''
        user_id = ''
        password = ''
        mac_get = ''
        depot_get = ''
        url_list = my_str.split(separator_url, my_str.count(separator_url))
        cid = url_list[0]
        user_type = url_list[1]
        user_id = url_list[2]
        password = url_list[3]
        mac_get = url_list[4]
#        depot_get=url_list[5]
#        table_name=url_list[4]
#        return depot_get
        date_download = date_fixed


#        return ("fixed"+str(date_fixed)+"dd"+str(date_download))
        user_type_check = str(user_type).upper()
        depot_mac = 0
#        ====================if user type HO===============
        if (user_type_check == 'HO'):
            com_valid_user = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).select()
#            return db._lastsql
            if com_valid_user:
    #            return 'Valid user'

                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.s_value

                flag_mac = '0'
    #  Set mac in db
                if depot_mac == '0':
                    flag_mac = 1
                    mac_update = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).update(s_value=mac_get)
                elif(depot_mac != '0'):
                    check_mac = db((db.sm_settings.cid == str(cid)) & (db.sm_settings.s_key == password) & (db.sm_settings.s_value == mac_get)).select()
                    if check_mac:
                        flag_mac = 2
                    else:
                        fail = "failed";
    #                    fail = get_encript(fail)
                        return "<STARTSTART>" + fail + "<ENDEND>"
                else:
                    fail = "failed";
                    return "<STARTSTART>" + fail + "<ENDEND>"
            else:
                fail = "failed";
                return "<STARTSTART>" + fail + "<ENDEND>"
#========================if user type depot===================                
        else:
            com_valid_user = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password)).select()
            if com_valid_user:
                depot_mac = 0
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.mac

                flag_mac = '0'
    #  Set mac in db
                if depot_mac == '0':
                    flag_mac = 1
                    mac_update = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id)).update(mac=mac_get)
                elif(depot_mac != '0'):
                    check_mac = db((db.sm_depot.cid == str(cid)) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password) & (db.sm_depot.mac == mac_get)).select()
                    if check_mac:
                        flag_mac = 2
                    else:
                        fail = "failed";
                        return "<STARTSTART>" + fail + "<ENDEND>"
                else:
                        fail = "failed";
                        return "<STARTSTART>" + fail + "<ENDEND>"


#        return depot_mac    
        if(depot_mac == mac_get):

            com_data_limit = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'LIMITBY')).select(db.sm_settings.s_value)
            if com_valid_user:
                limitby = 0
                limit = 0
                for com_data_limit in com_data_limit:
                    limit = com_data_limit.s_value


            limitby = (0, int(limit))

#                if(single_table[i]=='sm_order'):
                #  order==============   
            date_download = date_fixed - datetime.timedelta(minutes=2)
#            return date_download
            req_status = []
            req_status.append('Posted')
            req_status.append('Cancelled')
#            return user_type_check
            if user_type_check == 'HO':
#                return "afdsg"

#                 query_data=db((db.sm_requisition.cid==cid) & (db.sm_requisition.req_date<=date_download)  & (db.sm_requisition.ho_status=='0') & (db.sm_requisition.status.belongs(req_status))).select(db.sm_requisition.depot_id,db.sm_requisition.sl,db.sm_requisition.requisition_to,db.sm_requisition.req_date,db.sm_requisition.item_id,db.sm_requisition.item_name,db.sm_requisition.quantity,db.sm_requisition.dist_rate,db.sm_requisition.short_note,db.sm_requisition.note,db.sm_requisition.status,orderby=db.sm_requisition.req_date|db.sm_requisition.depot_id|db.sm_requisition.sl,limitby=limitby) 
                 query_data = db((db.sm_requisition.cid == cid) & (db.sm_requisition.updated_on <= date_download) & (db.sm_requisition.ho_status == '0') & (db.sm_requisition.status.belongs(req_status))).select(db.sm_requisition.depot_id, db.sm_requisition.sl, db.sm_requisition.requisition_to, db.sm_requisition.req_date, db.sm_requisition.item_id, db.sm_requisition.item_name, db.sm_requisition.quantity, db.sm_requisition.dist_rate, db.sm_requisition.short_note, db.sm_requisition.note, db.sm_requisition.status, orderby=db.sm_requisition.updated_on | db.sm_requisition.depot_id | db.sm_requisition.sl, limitby=limitby)


#                 query_data=db(q1 & q2)
#                return db._lastsql
            else:
#                 query_data=db((db.sm_requisition.cid==cid) & (db.sm_requisition.req_date<=date_download)  & (db.sm_requisition.depot_status=='0') & (db.sm_requisition.depot_id==user_id) & (db.sm_requisition.status.belongs(req_status))).select(db.sm_requisition.depot_id,db.sm_requisition.sl,db.sm_requisition.requisition_to,db.sm_requisition.req_date,db.sm_requisition.item_id,db.sm_requisition.item_name,db.sm_requisition.quantity,db.sm_requisition.dist_rate,db.sm_requisition.short_note,db.sm_requisition.note,db.sm_requisition.status,orderby=db.sm_requisition.req_date|db.sm_requisition.depot_id|db.sm_requisition.sl,limitby=limitby)
                 query_data = db((db.sm_requisition.cid == cid) & (db.sm_requisition.updated_on <= date_download) & (db.sm_requisition.depot_status == '0') & (db.sm_requisition.depot_id == user_id) & (db.sm_requisition.status.belongs(req_status))).select(db.sm_requisition.depot_id, db.sm_requisition.sl, db.sm_requisition.requisition_to, db.sm_requisition.req_date, db.sm_requisition.item_id, db.sm_requisition.item_name, db.sm_requisition.quantity, db.sm_requisition.dist_rate, db.sm_requisition.short_note, db.sm_requisition.note, db.sm_requisition.status, orderby=db.sm_requisition.updated_on | db.sm_requisition.depot_id | db.sm_requisition.sl, limitby=limitby)

            return_value = ''
#            return query_data      
#            return db._lastsql
            for row_query_data in query_data:
                return_value = str(return_value) + str(row_query_data.depot_id) + "<fd>" + str(row_query_data.sl) + "<fd>" + str(row_query_data.requisition_to) + "<fd>" + str(row_query_data.req_date) + "<fd>" + str(row_query_data.item_id) + "<fd>" + str(row_query_data.item_name) + "<fd>" + str(row_query_data.quantity) + "<fd>" + str(row_query_data.dist_rate) + "<fd>" + str(row_query_data.short_note) + "<fd>" + str(row_query_data.note) + "<fd>" + str(row_query_data.status) + "<fd><rd>"

#            return db._lastsql
            return "<STARTSTART>" + str(return_value) + "<ENDEND>"

        else :
            fail = "failed"

            return "<STARTSTART>" + fail + "<ENDEND>"


def update_requisition():
    my_str = request.args(0)

    my_str = get_decript(my_str)
#    return my_str
    if my_str == '':
        fail = "failed";
        fail = get_encript(fail);
        return "<STARTSTART>" + fail + "<ENDEND>";
    elif (my_str != ""):
        separator_url = '<url>'
        cid = ''
        user_id = ''

        password = ''
        mac_get = ''
        depot_get = ''
#        table_name_withSl=''
        url_list = my_str.split(separator_url, my_str.count(separator_url))

        cid = url_list[0]
        user_type = url_list[1]
        user_id = url_list[2]
        password = url_list[3]
        mac_get = url_list[4]
        update_string = url_list[5] #Get full depot_id and sl string

#        return sl


        depot_mac = 0
        user_type_check = str(user_type).upper()
#        ====================if user type HO===============

        if (user_type_check == 'HO'):
            com_valid_user = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).select()
            if com_valid_user:
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.s_value


        elif (user_type_check == 'DEPOT'):
            com_valid_user = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password)).select()
            if com_valid_user:
                depot_mac = 0
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.mac


        else:
            fail = "failed";
            return "<STARTSTART>" + fail + "<ENDEND>"





    if(depot_mac == mac_get):
        query = ''
        query2 = ''
        if user_type_check == 'HO':
            query = db.sm_order.cid == cid
        else:
           query = db.sm_order.cid == cid
           query &= db.sm_order.depot_id == user_id

        try:
            update_string_single = update_string.split('.', update_string.count('.')) #Split main data by.  
            total_update_string_single = update_string.count('.') #count total .
            i = 0
            while i < total_update_string_single + 1: #while lopp based oncount total
               update_id_sl = update_string_single[i].split(',', update_string_single[i].count(','))#split single strin by,
               if user_type_check == 'HO':
                   query = db((db.sm_requisition.cid == cid) & (db.sm_requisition.depot_id == update_id_sl[0]) & (db.sm_requisition.sl == update_id_sl[1])).update(ho_status='1')
                   query_head = db((db.sm_requisition_head.cid == cid) & (db.sm_requisition_head.depot_id == update_id_sl[0]) & (db.sm_requisition_head.sl == update_id_sl[1])).update(ho_status='1')

               else:
                   query = db((db.sm_requisition.cid == cid) & (db.sm_requisition.depot_id == update_id_sl[0]) & (db.sm_requisition.sl == update_id_sl[1])).update(depot_status='1')
                   query_head = db((db.sm_requisition_head.cid == cid) & (db.sm_requisition_head.depot_id == update_id_sl[0]) & (db.sm_requisition_head.sl == update_id_sl[1])).update(depot_status='1')

               i = i + 1 #increase i

            success = "success";
            return "<STARTSTART>" + success + "<ENDEND>"

        except:
            fail = "failed"
            return "<STARTSTART>" + fail + "<ENDEND>"




# ---------------------issue-----------------------    

def issue_data():
    my_str = request.args(0)

    my_str = get_decript(my_str)


    if my_str == '':
        fail = "failed";
        fail = get_encript(fail);
        return "<STARTSTART>" + fail + "<ENDEND>";

    elif (my_str != ""):
        separator_url = '<url>'
        cid = ''
        user_id = ''
        password = ''
        mac_get = ''
        depot_get = ''
        url_list = my_str.split(separator_url, my_str.count(separator_url))
        cid = url_list[0]
        user_type = url_list[1]
        user_id = url_list[2]
        password = url_list[3]
        mac_get = url_list[4]
#        depot_get=url_list[5]
#        table_name=url_list[4]
#        return depot_get
        date_download = date_fixed


#        return ("fixed"+str(date_fixed)+"dd"+str(date_download))
        user_type_check = str(user_type).upper()
        depot_mac = 0
#        ====================if user type HO===============

        if (user_type_check == 'HO'):
            com_valid_user = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).select()
            if com_valid_user:
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.s_value


        elif (user_type_check == 'DEPOT'):
            com_valid_user = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password)).select()
            if com_valid_user:
                depot_mac = 0
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.mac


        else:
            fail = "failed";
            return "<STARTSTART>" + fail + "<ENDEND>"


#        return depot_mac  

        if(depot_mac == mac_get):

            com_data_limit = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'LIMITBY')).select(db.sm_settings.s_value)
            if com_valid_user:
                limitby = 0
                limit = 0
                for com_data_limit in com_data_limit:
                    limit = com_data_limit.s_value


            limitby = (0, int(limit))

#                if(single_table[i]=='sm_order'):
                #  order==============   
            date_download = date_fixed - datetime.timedelta(minutes=2)
#            return date_download

            req_status = []
            req_status.append('Posted')
            req_status.append('Cancelled')

            if user_type_check == 'HO':

#                query_data=db((db.sm_issue.cid==cid) & (db.sm_issue.issue_date<=date_download)  & (db.sm_issue.ho_status=='0') & (db.sm_issue.status.belongs(req_status)) ).select(db.sm_issue.ALL,orderby=db.sm_issue.issue_date|db.sm_issue.depot_id|db.sm_issue.sl,limitby=limitby)
                query_data = db((db.sm_issue.cid == cid) & (db.sm_issue.updated_on <= date_download) & (db.sm_issue.ho_status == '0') & (db.sm_issue.status.belongs(req_status))).select(db.sm_issue.ALL, orderby=db.sm_issue.updated_on | db.sm_issue.depot_id | db.sm_issue.sl, limitby=limitby)

            else:
#                query_data=db((db.sm_issue.cid==cid) & (db.sm_issue.issue_date<=date_download)  & (db.sm_issue.depot_status=='0') & (db.sm_issue.depot_id==user_id)& (db.sm_issue.status.belongs(req_status))).select(db.sm_issue.ALL,orderby=db.sm_issue.issue_date|db.sm_issue.depot_id|db.sm_issue.sl,limitby=limitby)
                query_data = db((db.sm_issue.cid == cid) & (db.sm_issue.updated_on <= date_download) & (db.sm_issue.depot_status == '0') & (db.sm_issue.depot_id == user_id) & (db.sm_issue.status.belongs(req_status))).select(db.sm_issue.ALL, orderby=db.sm_issue.updated_on | db.sm_issue.depot_id | db.sm_issue.sl, limitby=limitby)

            return_value = ''
#            return db._lastsql
            for row_query_data in query_data:
                return_value = str(return_value) + str(row_query_data.depot_id) + "<fd>" + str(row_query_data.sl) + "<fd>" + str(row_query_data.issued_to) + "<fd>" + str(row_query_data.issue_date) + "<fd>" + str(row_query_data.status) + "<fd>" + str(row_query_data.total_discount) + "<fd>" + str(row_query_data.req_sl) + "<fd>" + str(row_query_data.item_id) + "<fd>" + str(row_query_data.item_name) + "<fd>" + str(row_query_data.quantity) + "<fd>" + str(row_query_data.bonus_qty) + "<fd>" + str(row_query_data.dist_rate) + "<fd>" + str(row_query_data.short_note) + "<fd>" + str(row_query_data.note) + "<fd><rd>"

#            return db._lastsql
            return "<STARTSTART>" + str(return_value) + "<ENDEND>"

        else :
            fail = "failed"

            return "<STARTSTART>" + fail + "<ENDEND>"

def update_issue():
    my_str = request.args(0)

    my_str = get_decript(my_str)
#    return my_str
    if my_str == '':
        fail = "failed";
        fail = get_encript(fail);
        return "<STARTSTART>" + fail + "<ENDEND>";
    elif (my_str != ""):
        separator_url = '<url>'
        cid = ''
        user_id = ''

        password = ''
        mac_get = ''
        depot_get = ''
#        table_name_withSl=''
        url_list = my_str.split(separator_url, my_str.count(separator_url))

        cid = url_list[0]
        user_type = url_list[1]
        user_id = url_list[2]
        password = url_list[3]
        mac_get = url_list[4]
        update_string = url_list[5] #Get full depot_id and sl string

#        return sl


        depot_mac = 0
        user_type_check = str(user_type).upper()
#        ====================if user type HO===============

        if (user_type_check == 'HO'):
            com_valid_user = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).select()
            if com_valid_user:
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.s_value


        elif (user_type_check == 'DEPOT'):
            com_valid_user = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password)).select()
            if com_valid_user:
                depot_mac = 0
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.mac


        else:
            fail = "failed";
            return "<STARTSTART>" + fail + "<ENDEND>"





    if(depot_mac == mac_get):
        query = ''
        query2 = ''
        if user_type_check == 'HO':
            query = db.sm_order.cid == cid
        else:
           query = db.sm_order.cid == cid
           query &= db.sm_order.depot_id == user_id

        try:
            update_string_single = update_string.split('.', update_string.count('.')) #Split main data by.  
            total_update_string_single = update_string.count('.') #count total .
            i = 0
            while i < total_update_string_single + 1: #while lopp based oncount total
               update_id_sl = update_string_single[i].split(',', update_string_single[i].count(','))#split single strin by,
               if user_type_check == 'HO':
                   query = db((db.sm_issue.cid == cid) & (db.sm_issue.depot_id == update_id_sl[0]) & (db.sm_issue.sl == update_id_sl[1])).update(ho_status='1')
                   query_head = db((db.sm_issue_head.cid == cid) & (db.sm_issue_head.depot_id == update_id_sl[0]) & (db.sm_issue_head.sl == update_id_sl[1])).update(ho_status='1')

               else:
                   query = db((db.sm_issue.cid == cid) & (db.sm_issue.depot_id == update_id_sl[0]) & (db.sm_issue.sl == update_id_sl[1])).update(depot_status='1')
                   query_head = db((db.sm_issue_head.cid == cid) & (db.sm_issue_head.depot_id == update_id_sl[0]) & (db.sm_issue_head.sl == update_id_sl[1])).update(depot_status='1')

               i = i + 1 #increase i

            success = "success";
            return "<STARTSTART>" + success + "<ENDEND>"

        except:
            fail = "failed"
            return "<STARTSTART>" + fail + "<ENDEND>"


 #-------------------------------------------receive----------------------


def receive_data():
    my_str = request.args(0)

    my_str = get_decript(my_str)

    if my_str == '':
        fail = "failed";
        fail = get_encript(fail);
        return "<STARTSTART>" + fail + "<ENDEND>";
    elif (my_str != ""):
        separator_url = '<url>'
        cid = ''
        user_id = ''
        password = ''
        mac_get = ''
        depot_get = ''
        url_list = my_str.split(separator_url, my_str.count(separator_url))
        cid = url_list[0]
        user_type = url_list[1]
        user_id = url_list[2]
        password = url_list[3]
        mac_get = url_list[4]
#        depot_get=url_list[5]
#        table_name=url_list[4]
#        return depot_get
        date_download = date_fixed


#        return ("fixed"+str(date_fixed)+"dd"+str(date_download))
        user_type_check = str(user_type).upper()
        depot_mac = 0



#        ====================if user type HO===============

        if (user_type_check == 'HO'):
            com_valid_user = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).select()
            if com_valid_user:
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.s_value


        elif (user_type_check == 'DEPOT'):
            com_valid_user = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password)).select()
            if com_valid_user:
                depot_mac = 0
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.mac


        else:
            fail = "failed";
            return "<STARTSTART>" + fail + "<ENDEND>"


#        return depot_mac    
        if(depot_mac == mac_get):

            com_data_limit = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'LIMITBY')).select(db.sm_settings.s_value)
            if com_valid_user:
                limitby = 0
                limit = 0
                for com_data_limit in com_data_limit:
                    limit = com_data_limit.s_value


            limitby = (0, int(limit))

#                if(single_table[i]=='sm_order'):
                #  order==============   
            date_download = date_fixed - datetime.timedelta(minutes=2)
#            return date_download

            req_status = []
            req_status.append('Posted')
            req_status.append('Cancelled')
            if user_type_check == 'HO':
#                return "afdsg"
#                query_data=db((db.sm_receive.cid==cid) & (db.sm_receive.receive_date<=date_download)  & (db.sm_receive.ho_status=='0') & (db.sm_receive.status.belongs(req_status))).select(db.sm_receive.ALL,orderby=db.sm_receive.receive_date|db.sm_receive.depot_id|db.sm_receive.sl,limitby=limitby)
                query_data = db((db.sm_receive.cid == cid) & (db.sm_receive.updated_on <= date_download) & (db.sm_receive.ho_status == '0') & (db.sm_receive.status.belongs(req_status))).select(db.sm_receive.ALL, orderby=db.sm_receive.updated_on | db.sm_receive.depot_id | db.sm_receive.sl, limitby=limitby)
            else:
#                query_data=db((db.sm_receive.cid==cid) & (db.sm_receive.receive_date<=date_download)  & (db.sm_receive.depot_status=='0') & (db.sm_receive.depot_id==user_id)& (db.sm_receive.status.belongs(req_status))).select(db.sm_receive.ALL,orderby=db.sm_receive.receive_date|db.sm_receive.depot_id|db.sm_receive.sl,limitby=limitby)
                query_data = db((db.sm_receive.cid == cid) & (db.sm_receive.updated_on <= date_download) & (db.sm_receive.depot_status == '0') & (db.sm_receive.depot_id == user_id) & (db.sm_receive.status.belongs(req_status))).select(db.sm_receive.ALL, orderby=db.sm_receive.updated_on | db.sm_receive.depot_id | db.sm_receive.sl, limitby=limitby)

            return_value = ''
#            return db._lastsql
            for row_query_data in query_data:
                return_value = str(return_value) + str(row_query_data.depot_id) + "<fd>" + str(row_query_data.sl) + "<fd>" + str(row_query_data.receive_from) + "<fd>" + str(row_query_data.receive_date) + "<fd>" + str(row_query_data.status) + "<fd>" + str(row_query_data.total_discount) + "<fd>" + str(row_query_data.ref_sl) + "<fd>" + str(row_query_data.item_id) + "<fd>" + str(row_query_data.item_name) + "<fd>" + str(row_query_data.quantity) + "<fd>" + str(row_query_data.bonus_qty) + "<fd>" + str(row_query_data.dist_rate) + "<fd>" + str(row_query_data.short_note) + "<fd>" + str(row_query_data.note) + "<fd><rd>"

#            return db._lastsql
            return "<STARTSTART>" + str(return_value) + "<ENDEND>"

        else :
            fail = "failed"

            return "<STARTSTART>" + fail + "<ENDEND>"

def update_receive():
    my_str = request.args(0)

    my_str = get_decript(my_str)
#    return my_str
    if my_str == '':
        fail = "failed";
        fail = get_encript(fail);
        return "<STARTSTART>" + fail + "<ENDEND>";
    elif (my_str != ""):
        separator_url = '<url>'
        cid = ''
        user_id = ''

        password = ''
        mac_get = ''
        depot_get = ''
#        table_name_withSl=''
        url_list = my_str.split(separator_url, my_str.count(separator_url))

        cid = url_list[0]
        user_type = url_list[1]
        user_id = url_list[2]
        password = url_list[3]
        mac_get = url_list[4]
        update_string = url_list[5] #Get full depot_id and sl string

#        return sl


        depot_mac = 0
        user_type_check = str(user_type).upper()
#        ====================if user type HO===============

        if (user_type_check == 'HO'):
            com_valid_user = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).select()
            if com_valid_user:
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.s_value


        elif (user_type_check == 'DEPOT'):
            com_valid_user = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password)).select()
            if com_valid_user:
                depot_mac = 0
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.mac


        else:
            fail = "failed";
            return "<STARTSTART>" + fail + "<ENDEND>"





    if(depot_mac == mac_get):
        query = ''
        query2 = ''
        if user_type_check == 'HO':
            query = db.sm_order.cid == cid
        else:
           query = db.sm_order.cid == cid
           query &= db.sm_order.depot_id == user_id

        try:
            update_string_single = update_string.split('.', update_string.count('.')) #Split main data by.  
            total_update_string_single = update_string.count('.') #count total .
            i = 0
            while i < total_update_string_single + 1: #while lopp based oncount total
               update_id_sl = update_string_single[i].split(',', update_string_single[i].count(','))#split single strin by,
               if user_type_check == 'HO':
                   query = db((db.sm_receive.cid == cid) & (db.sm_receive.depot_id == update_id_sl[0]) & (db.sm_receive.sl == update_id_sl[1])).update(ho_status='1')
                   query_head = db((db.sm_receive_head.cid == cid) & (db.sm_receive_head.depot_id == update_id_sl[0]) & (db.sm_receive_head.sl == update_id_sl[1])).update(ho_status='1')
               else:
                    query = db((db.sm_receive.cid == cid) & (db.sm_receive.depot_id == update_id_sl[0]) & (db.sm_receive.sl == update_id_sl[1])).update(depot_status='1')
                    query_head = db((db.sm_receive_head.cid == cid) & (db.sm_receive_head.depot_id == update_id_sl[0]) & (db.sm_receive_head.sl == update_id_sl[1])).update(depot_status='1')

               i = i + 1 #increase i

            success = "success";
            return "<STARTSTART>" + success + "<ENDEND>"

        except:
            fail = "failed"
            return "<STARTSTART>" + fail + "<ENDEND>"


#    --------------------------------damage----------------------------



def damage_data():
    my_str = request.args(0)

    my_str = get_decript(my_str)

    if my_str == '':
        fail = "failed";
        fail = get_encript(fail);
        return "<STARTSTART>" + fail + "<ENDEND>";
    elif (my_str != ""):
        separator_url = '<url>'
        cid = ''
        user_id = ''
        password = ''
        mac_get = ''
        depot_get = ''
        url_list = my_str.split(separator_url, my_str.count(separator_url))
        cid = url_list[0]
        user_type = url_list[1]
        user_id = url_list[2]
        password = url_list[3]
        mac_get = url_list[4]
        date_download = date_fixed


#        return ("fixed"+str(date_fixed)+"dd"+str(date_download))
        user_type_check = str(user_type).upper()
        depot_mac = 0


#        ====================if user type HO===============

        if (user_type_check == 'HO'):
            com_valid_user = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).select()
            if com_valid_user:
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.s_value


        elif (user_type_check == 'DEPOT'):
            com_valid_user = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password)).select()
            if com_valid_user:
                depot_mac = 0
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.mac


        else:
            fail = "failed";
            return "<STARTSTART>" + fail + "<ENDEND>"


#        return depot_mac    
        if(depot_mac == mac_get):

            com_data_limit = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'LIMITBY')).select(db.sm_settings.s_value)
            if com_valid_user:
                limitby = 0
                limit = 0
                for com_data_limit in com_data_limit:
                    limit = com_data_limit.s_value


            limitby = (0, int(limit))

#                if(single_table[i]=='sm_order'):
                #  order==============   
            date_download = date_fixed - datetime.timedelta(minutes=2)
#            return date_download

            req_status = []
            req_status.append('Posted')
            req_status.append('Cancelled')
            if user_type_check == 'HO':
#                return date_download
#                query_data=db((db.sm_damage.cid==cid) & (db.sm_damage.damage_date<=date_download)  & (db.sm_damage.ho_status=='0') & (db.sm_damage.status.belongs(req_status))).select(db.sm_damage.ALL,orderby=db.sm_damage.damage_date|db.sm_damage.depot_id|db.sm_damage.sl,limitby=limitby)
                query_data = db((db.sm_damage.cid == cid) & (db.sm_damage.updated_on <= date_download) & (db.sm_damage.ho_status == '0') & (db.sm_damage.status.belongs(req_status))).select(db.sm_damage.ALL, orderby=db.sm_damage.updated_on | db.sm_damage.depot_id | db.sm_damage.sl, limitby=limitby)
            else:
#                query_data=db((db.sm_damage.cid==cid) & (db.sm_damage.created_on<=date_download)  & (db.sm_damage.depot_status=='0')  & (db.sm_damage.depot_id==user_id) & (db.sm_damage.status.belongs(req_status))).select(db.sm_damage.ALL,orderby=db.sm_damage.damage_date|db.sm_damage.depot_id|db.sm_damage.sl,limitby=limitby)
                query_data = db((db.sm_damage.cid == cid) & (db.sm_damage.updated_on <= date_download) & (db.sm_damage.depot_status == '0') & (db.sm_damage.depot_id == user_id) & (db.sm_damage.status.belongs(req_status))).select(db.sm_damage.ALL, orderby=db.sm_damage.updated_on | db.sm_damage.depot_id | db.sm_damage.sl, limitby=limitby)

            return_value = ''
#            return db._lastsql
            for row_query_data in query_data:
                return_value = str(return_value) + str(row_query_data.depot_id) + "<fd>" + str(row_query_data.sl) + "<fd>" + str(row_query_data.damage_date) + "<fd>" + str(row_query_data.status) + "<fd>" + str(row_query_data.item_id) + "<fd>" + str(row_query_data.item_name) + "<fd>" + str(row_query_data.quantity) + "<fd>" + str(row_query_data.dist_rate) + "<fd>" + str(row_query_data.short_note) + "<fd>" + str(row_query_data.note) + "<fd><rd>"

#            return db._lastsql
            return "<STARTSTART>" + str(return_value) + "<ENDEND>"

        else :
            fail = "failed"

            return "<STARTSTART>" + fail + "<ENDEND>"

def update_damage():
    my_str = request.args(0)

    my_str = get_decript(my_str)
#    return my_str
    if my_str == '':
        fail = "failed";
        fail = get_encript(fail);
        return "<STARTSTART>" + fail + "<ENDEND>";
    elif (my_str != ""):
        separator_url = '<url>'
        cid = ''
        user_id = ''

        password = ''
        mac_get = ''
        depot_get = ''
#        table_name_withSl=''
        url_list = my_str.split(separator_url, my_str.count(separator_url))

        cid = url_list[0]
        user_type = url_list[1]
        user_id = url_list[2]
        password = url_list[3]
        mac_get = url_list[4]
        update_string = url_list[5] #Get full depot_id and sl string

#        return sl


        depot_mac = 0
        user_type_check = str(user_type).upper()
#        ====================if user type HO===============

        if (user_type_check == 'HO'):
            com_valid_user = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).select()
            if com_valid_user:
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.s_value


        elif (user_type_check == 'DEPOT'):
            com_valid_user = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password)).select()
            if com_valid_user:
                depot_mac = 0
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.mac


        else:
            fail = "failed";
            return "<STARTSTART>" + fail + "<ENDEND>"





    if(depot_mac == mac_get):
        query = ''
        query2 = ''
        if user_type_check == 'HO':
            query = db.sm_order.cid == cid
        else:
           query = db.sm_order.cid == cid
           query &= db.sm_order.depot_id == user_id

        try:
            update_string_single = update_string.split('.', update_string.count('.')) #Split main data by.  
            total_update_string_single = update_string.count('.') #count total .
            i = 0
            while i < total_update_string_single + 1: #while lopp based oncount total
               update_id_sl = update_string_single[i].split(',', update_string_single[i].count(','))#split single strin by,
               if user_type_check == 'HO':
                   query = db((db.sm_damage.cid == cid) & (db.sm_damage.depot_id == update_id_sl[0]) & (db.sm_damage.sl == update_id_sl[1])).update(ho_status='1')
                   query_head = db((db.sm_damage_head.cid == cid) & (db.sm_damage_head.depot_id == update_id_sl[0]) & (db.sm_damage_head.sl == update_id_sl[1])).update(ho_status='1')

               else:
                   query = db((db.sm_damage.cid == cid) & (db.sm_damage.depot_id == update_id_sl[0]) & (db.sm_damage.sl == update_id_sl[1])).update(depot_status='1')
                   query_head = db((db.sm_damage_head.cid == cid) & (db.sm_damage_head.depot_id == update_id_sl[0]) & (db.sm_damage_head.sl == update_id_sl[1])).update(depot_status='1')

               i = i + 1 #increase i

            success = "success";
            return "<STARTSTART>" + success + "<ENDEND>"

        except:
            fail = "failed"
            return "<STARTSTART>" + fail + "<ENDEND>"



#---------------------------order info-------------------

def order_data():
    my_str = request.args(0)

    my_str = get_decript(my_str)

    if my_str == '':
        fail = "failed";
        fail = get_encript(fail);
        return "<STARTSTART>" + fail + "<ENDEND>";
    elif (my_str != ""):
        separator_url = '<url>'
        cid = ''
        user_id = ''
        password = ''
        mac_get = ''
        depot_get = ''
        url_list = my_str.split(separator_url, my_str.count(separator_url))
        cid = url_list[0]
        user_type = url_list[1]
        user_id = url_list[2]
        password = url_list[3]
        mac_get = url_list[4]
        date_download = date_fixed


#        return ("fixed"+str(date_fixed)+"dd"+str(date_download))
        user_type_check = str(user_type).upper()
        depot_mac = 0
#        ====================if user type HO===============
        if (user_type_check == 'HO'):
            com_valid_user = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).select()
#            return db._lastsql
            if com_valid_user:
    #            return 'Valid user'

                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.s_value

                flag_mac = '0'
    #  Set mac in db
                if depot_mac == '0':
                    flag_mac = 1
                    mac_update = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).update(s_value=mac_get)
                elif(depot_mac != '0'):
                    check_mac = db((db.sm_settings.cid == str(cid)) & (db.sm_settings.s_key == password) & (db.sm_settings.s_value == mac_get)).select()
                    if check_mac:
                        flag_mac = 2
                    else:
                        fail = "failed";
    #                    fail = get_encript(fail)
                        return "<STARTSTART>" + fail + "<ENDEND>"
                else:
                    fail = "failed";
                    return "<STARTSTART>" + fail + "<ENDEND>"
            else:
                fail = "failed";
                return "<STARTSTART>" + fail + "<ENDEND>"
#========================if user type depot===================                
        else:
            com_valid_user = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password)).select()
            if com_valid_user:
                depot_mac = 0
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.mac

                flag_mac = '0'
    #  Set mac in db
                if depot_mac == '0':
                    flag_mac = 1
                    mac_update = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id)).update(mac=mac_get)
                elif(depot_mac != '0'):
                    check_mac = db((db.sm_depot.cid == str(cid)) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password) & (db.sm_depot.mac == mac_get)).select()
                    if check_mac:
                        flag_mac = 2
                    else:
                        fail = "failed";
                        return "<STARTSTART>" + fail + "<ENDEND>"
                else:
                        fail = "failed";
                        return "<STARTSTART>" + fail + "<ENDEND>"


#        return depot_mac    
        if(depot_mac == mac_get):

            com_data_limit = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'LIMITBY')).select(db.sm_settings.s_value)
            if com_valid_user:
                limitby = 0
                limit = 0
                for com_data_limit in com_data_limit:
                    limit = com_data_limit.s_value


            limitby = (0, int(limit))

#                if(single_table[i]=='sm_order'):
                #  order==============   
            date_download = date_fixed - datetime.timedelta(minutes=2)
#            return date_download

            req_status = []
            req_status.append('Submitted')
            req_status.append('Invoiced')
            req_status.append('Cancelled')
            if user_type_check == 'HO':
                query_data = db((db.sm_order.cid == cid) & (db.sm_order.order_datetime <= date_download) & (db.sm_order.ho_status == '0') & (db.sm_order.status.belongs(req_status))).select(db.sm_order.ALL, orderby=db.sm_order.order_datetime | db.sm_order.depot_id | db.sm_order.sl, limitby=limitby)
            else:
                query_data = db((db.sm_order.cid == cid) & (db.sm_order.order_datetime <= date_download) & (db.sm_order.depot_status == '0') & (db.sm_order.depot_id == user_id) & (db.sm_order.status.belongs(req_status))).select(db.sm_order.ALL, orderby=db.sm_order.order_datetime | db.sm_order.depot_id | db.sm_order.sl, limitby=limitby)

            return_value = ''
#            return query_data
            for row_query_data in query_data:
                return_value = str(return_value) + str(row_query_data.depot_id) + "<fd>" + str(row_query_data.depot_name) + "<fd>" + str(row_query_data.sl) + "<fd>" + str(row_query_data.client_id) + "<fd>" + str(row_query_data.client_name) + "<fd>" + str(row_query_data.rep_id) + "<fd>" + str(row_query_data.rep_name) + "<fd>" + str(row_query_data.order_date) + "<fd>" + str(row_query_data.delivery_date) + "<fd>" + str(row_query_data.payment_mode) + "<fd>" + str(row_query_data.area_id) + "<fd>" + str(row_query_data.area_name) + "<fd>" + str(row_query_data.status) + "<fd>" + str(row_query_data.item_id) + "<fd>" + str(row_query_data.item_name) + "<fd>" + str(row_query_data.category_id) + "<fd>" + str(row_query_data.quantity) + "<fd>" + str(row_query_data.price) + "<fd>" + str(row_query_data.order_media) + "<fd><rd>"

#            return db._lastsql
            return "<STARTSTART>" + str(return_value) + "<ENDEND>"

        else :
            fail = "failed"

            return "<STARTSTART>" + fail + "<ENDEND>"

def update_order():
    my_str = request.args(0)

    my_str = get_decript(my_str)
#    return my_str
    if my_str == '':
        fail = "failed";
        fail = get_encript(fail);
        return "<STARTSTART>" + fail + "<ENDEND>";
    elif (my_str != ""):
        separator_url = '<url>'
        cid = ''
        user_id = ''

        password = ''
        mac_get = ''
        depot_get = ''
#        table_name_withSl=''
        url_list = my_str.split(separator_url, my_str.count(separator_url))

        cid = url_list[0]
        user_type = url_list[1]
        user_id = url_list[2]
        password = url_list[3]
        mac_get = url_list[4]
        update_string = url_list[5] #Get full depot_id and sl string

#        return sl


        depot_mac = 0
        user_type_check = str(user_type).upper()
#        ====================if user type HO===============

        if (user_type_check == 'HO'):
            com_valid_user = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).select()
            if com_valid_user:
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.s_value


        elif (user_type_check == 'DEPOT'):
            com_valid_user = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password)).select()
            if com_valid_user:
                depot_mac = 0
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.mac


        else:
            fail = "failed";
            return "<STARTSTART>" + fail + "<ENDEND>"





    if(depot_mac == mac_get):
        query = ''
        query2 = ''
        if user_type_check == 'HO':
            query = db.sm_order.cid == cid
        else:
           query = db.sm_order.cid == cid
           query &= db.sm_order.depot_id == user_id

        try:
            update_string_single = update_string.split('.', update_string.count('.')) #Split main data by.  
            total_update_string_single = update_string.count('.') #count total .
            i = 0
            while i < total_update_string_single + 1: #while lopp based oncount total
               update_id_sl = update_string_single[i].split(',', update_string_single[i].count(','))#split single strin by,
               if user_type_check == 'HO':
                   query = db((db.sm_order.cid == cid) & (db.sm_order.depot_id == update_id_sl[0]) & (db.sm_order.sl == update_id_sl[1])).update(ho_status='1')
                   query_head = db((db.sm_order_head.cid == cid) & (db.sm_order_head.depot_id == update_id_sl[0]) & (db.sm_order_head.sl == update_id_sl[1])).update(ho_status='1')
               else:
                   query = db((db.sm_damage.cid == cid) & (db.sm_damage.depot_id == update_id_sl[0]) & (db.sm_damage.sl == update_id_sl[1])).update(depot_status='1')
                   query_head = db((db.sm_damage_head.cid == cid) & (db.sm_damage_head.depot_id == update_id_sl[0]) & (db.sm_damage_head.sl == update_id_sl[1])).update(depot_status='1')

               i = i + 1 #increase i

            success = "success";
            return "<STARTSTART>" + success + "<ENDEND>"

        except:
            fail = "failed"
            return "<STARTSTART>" + fail + "<ENDEND>"


def update_order_new():
    my_str = request.args(0)

    my_str = get_decript(my_str)
#    return my_str
    if my_str == '':
        fail = "failed";
        fail = get_encript(fail);
        return "<STARTSTART>" + fail + "<ENDEND>";
    elif (my_str != ""):
        separator_url = '<url>'
        cid = ''
        user_id = ''

        password = ''
        mac_get = ''
        depot_get = ''
#        table_name_withSl=''
        url_list = my_str.split(separator_url, my_str.count(separator_url))

        cid = url_list[0]
        user_type = url_list[1]
        user_id = url_list[2]
        password = url_list[3]
        mac_get = url_list[4]
        update_string = url_list[5] #Get full depot_id and sl string

#        return sl


        depot_mac = 0
        user_type_check = str(user_type).upper()
#        ====================if user type HO===============

        if (user_type_check == 'HO'):
            com_valid_user = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).select()
            if com_valid_user:
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.s_value


        elif (user_type_check == 'DEPOT'):
            com_valid_user = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password)).select()
            if com_valid_user:
                depot_mac = 0
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.mac


        else:
            fail = "failed";
            return "<STARTSTART>" + fail + "<ENDEND>"





    if(depot_mac == mac_get):
        query = ''
        query2 = ''
        if user_type_check == 'HO':
            query = db.sm_order.cid == cid
        else:
           query = db.sm_order.cid == cid
           query &= db.sm_order.depot_id == user_id

        try:
            update_string_single = update_string.split('.', update_string.count('.')) #Split main data by.  
            total_update_string_single = update_string.count('.') #count total .
            i = 0
            while i < total_update_string_single + 1: #while lopp based oncount total
               update_id_sl = update_string_single[i].split(',', update_string_single[i].count(','))#split single strin by,
               if user_type_check == 'HO':
                     query = db((db.sm_order.cid == cid) & (db.sm_order.depot_id == update_id_sl[0]) & (db.sm_order.sl == update_id_sl[1])).update(ho_status='1')
                     query_head = db((db.sm_order_head.cid == cid) & (db.sm_order_head.depot_id == update_id_sl[0]) & (db.sm_order_head.sl == update_id_sl[1])).update(ho_status='1')
               else:
                    query = db((db.sm_order.cid == cid) & (db.sm_order.depot_id == update_id_sl[0]) & (db.sm_order.sl == update_id_sl[1])).update(depot_status='1')
                    query_head = db((db.sm_order_head.cid == cid) & (db.sm_order_head.depot_id == update_id_sl[0]) & (db.sm_order_head.sl == update_id_sl[1])).update(depot_status='1')
               i = i + 1 #increase i

            success = "success";
            return "<STARTSTART>" + success + "<ENDEND>"

        except:
            fail = "failed"
            return "<STARTSTART>" + fail + "<ENDEND>"



#---------------------------------delivery-----------------------------

def delivery_data():
    my_str = request.args(0)

    my_str = get_decript(my_str)

    if my_str == '':
        fail = "failed";
        fail = get_encript(fail);
        return "<STARTSTART>" + fail + "<ENDEND>";
    elif (my_str != ""):
        separator_url = '<url>'
        cid = ''
        user_id = ''
        password = ''
        mac_get = ''
        depot_get = ''
        url_list = my_str.split(separator_url, my_str.count(separator_url))
        cid = url_list[0]
        user_type = url_list[1]
        user_id = url_list[2]
        password = url_list[3]
        mac_get = url_list[4]
        date_download = date_fixed


#        return ("fixed"+str(date_fixed)+"dd"+str(date_download))
        user_type_check = str(user_type).upper()
        depot_mac = 0
#        ====================if user type HO===============

        if (user_type_check == 'HO'):
            com_valid_user = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).select()
            if com_valid_user:
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.s_value


        elif (user_type_check == 'DEPOT'):
            com_valid_user = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password)).select()
            if com_valid_user:
                depot_mac = 0
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.mac


        else:
            fail = "failed";
            return "<STARTSTART>" + fail + "<ENDEND>"

#        return depot_mac    
        if(depot_mac == mac_get):

            com_data_limit = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'LIMITBY')).select(db.sm_settings.s_value)
            if com_valid_user:
                limitby = 0
                limit = 0
                for com_data_limit in com_data_limit:
                    limit = com_data_limit.s_value


            limitby = (0, int(limit))

#                if(single_table[i]=='sm_order'):
                #  order==============   
            date_download = date_fixed - datetime.timedelta(minutes=2)
#            return date_download

            req_status = []
            req_status.append('Invoiced')
#            req_status.append('Delivered')
#            req_status.append('Part Delivered')
#            req_status.append('Delivered On Demand')
#            req_status.append('Returned')
#            req_status.append('Blocked')
            req_status.append('Cancelled')

            if user_type_check == 'HO':
#                query_data=db((db.sm_invoice.cid==cid) & (db.sm_invoice.delivery_date<=date_download)  & (db.sm_invoice.ho_status=='0') & (db.sm_invoice.status.belongs(req_status))).select(db.sm_invoice.ALL,orderby=db.sm_invoice.delivery_date|db.sm_invoice.depot_id|db.sm_invoice.sl,limitby=limitby)
                query_data = db((db.sm_invoice.cid == cid) & (db.sm_invoice.updated_on <= date_download) & (db.sm_invoice.ho_status == '0') & (db.sm_invoice.status.belongs(req_status))).select(db.sm_invoice.ALL, orderby=db.sm_invoice.updated_on | db.sm_invoice.depot_id | db.sm_invoice.sl, limitby=limitby)
            else:
#                query_data=db((db.sm_invoice.cid==cid) & (db.sm_invoice.delivery_date<=date_download)  & (db.sm_invoice.depot_status=='0') & (db.sm_invoice.depot_id==user_id) & (db.sm_invoice.status.belongs(req_status))).select(db.sm_invoice.ALL,orderby=db.sm_invoice.delivery_date|db.sm_invoice.depot_id|db.sm_invoice.sl,limitby=limitby)
                query_data = db((db.sm_invoice.cid == cid) & (db.sm_invoice.updated_on <= date_download) & (db.sm_invoice.depot_status == '0') & (db.sm_invoice.depot_id == user_id) & (db.sm_invoice.status.belongs(req_status))).select(db.sm_invoice.ALL, orderby=db.sm_invoice.updated_on | db.sm_invoice.depot_id | db.sm_invoice.sl, limitby=limitby)

            return_value = ''
#            return query_data
            for row_query_data in query_data:
                return_value = str(return_value) + str(row_query_data.depot_id) + "<fd>" + str(row_query_data.depot_name) + "<fd>" + str(row_query_data.sl) + "<fd>" + str(row_query_data.order_sl) + "<fd>" + str(row_query_data.order_datetime) + "<fd>" + str(row_query_data.delivery_date) + "<fd>" + str(row_query_data.payment_mode) + "<fd>" + str(row_query_data.client_id) + "<fd>" + str(row_query_data.client_name) + "<fd>" + str(row_query_data.rep_id) + "<fd>" + str(row_query_data.rep_name) + "<fd>" + str(row_query_data.area_id) + "<fd>" + str(row_query_data.area_name) + "<fd>" + str(row_query_data.status) + "<fd>" + str(row_query_data.invoice_media) + "<fd>" + str(row_query_data.discount) + "<fd>" + str(row_query_data.item_id) + "<fd>" + str(row_query_data.item_name) + "<fd>" + str(row_query_data.category_id) + "<fd>" + str(row_query_data.quantity) + "<fd>" + str(row_query_data.bonus_qty) + "<fd>" + str(row_query_data.price) + "<fd>" + str(row_query_data.short_note) + "<fd>" + str(row_query_data.note) + "<fd>" + str(row_query_data.ym_date) + "<fd><rd>"

#            return db._lastsql
            return "<STARTSTART>" + str(return_value) + "<ENDEND>"

        else :
            fail = "failed"

            return "<STARTSTART>" + fail + "<ENDEND>"



def update_delivery_new():
    my_str = request.args(0)

    my_str = get_decript(my_str)
#    return my_str
    if my_str == '':
        fail = "failed";
        fail = get_encript(fail);
        return "<STARTSTART>" + fail + "<ENDEND>";
    elif (my_str != ""):
        separator_url = '<url>'
        cid = ''
        user_id = ''

        password = ''
        mac_get = ''
        depot_get = ''
#        table_name_withSl=''
        url_list = my_str.split(separator_url, my_str.count(separator_url))

        cid = url_list[0]
        user_type = url_list[1]
        user_id = url_list[2]
        password = url_list[3]
        mac_get = url_list[4]
        update_string = url_list[5] #Get full depot_id and sl string

#        return sl


        depot_mac = 0
        user_type_check = str(user_type).upper()
#        ====================if user type HO===============

        if (user_type_check == 'HO'):
            com_valid_user = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).select()
            if com_valid_user:
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.s_value


        elif (user_type_check == 'DEPOT'):
            com_valid_user = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password)).select()
            if com_valid_user:
                depot_mac = 0
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.mac


        else:
            fail = "failed";
            return "<STARTSTART>" + fail + "<ENDEND>"

    if(depot_mac == mac_get):
        query = ''
        query2 = ''
        if user_type_check == 'HO':
            query = db.sm_order.cid == cid
        else:
           query = db.sm_order.cid == cid
           query &= db.sm_order.depot_id == user_id

        try:
            update_string_single = update_string.split('.', update_string.count('.')) #Split main data by.  
            total_update_string_single = update_string.count('.') #count total .
            i = 0
            while i < total_update_string_single + 1: #while lopp based oncount total
               update_id_sl = update_string_single[i].split(',', update_string_single[i].count(','))#split single strin by,
               if user_type_check == 'HO':
                     query = db((db.sm_invoice.cid == cid) & (db.sm_invoice.depot_id == update_id_sl[0]) & (db.sm_invoice.sl == update_id_sl[1])).update(ho_status='1')
                     query_head = db((db.sm_invoice_head.cid == cid) & (db.sm_invoice_head.depot_id == update_id_sl[0]) & (db.sm_invoice_head.sl == update_id_sl[1])).update(ho_status='1')
               else:
                    query = db((db.sm_invoice.cid == cid) & (db.sm_invoice.depot_id == update_id_sl[0]) & (db.sm_invoice.sl == update_id_sl[1])).update(depot_status='1')
                    query_head = db((db.sm_invoice_head.cid == cid) & (db.sm_invoice_head.depot_id == update_id_sl[0]) & (db.sm_invoice_head.sl == update_id_sl[1])).update(depot_status='1')
               i = i + 1 #increase i

            success = "success";
            return "<STARTSTART>" + success + "<ENDEND>"

        except:
            fail = "failed"
            return "<STARTSTART>" + fail + "<ENDEND>"

#---------------------------------return------------------------

def return_data():
    my_str = request.args(0)

    my_str = get_decript(my_str)

    if my_str == '':
        fail = "failed";
        fail = get_encript(fail);
        return "<STARTSTART>" + fail + "<ENDEND>";
    elif (my_str != ""):
        separator_url = '<url>'
        cid = ''
        user_id = ''
        password = ''
        mac_get = ''
        depot_get = ''
        url_list = my_str.split(separator_url, my_str.count(separator_url))
        cid = url_list[0]
        user_type = url_list[1]
        user_id = url_list[2]
        password = url_list[3]
        mac_get = url_list[4]
        date_download = date_fixed


#        return ("fixed"+str(date_fixed)+"dd"+str(date_download))
        user_type_check = str(user_type).upper()
        depot_mac = 0
#        ====================if user type HO===============

        if (user_type_check == 'HO'):
            com_valid_user = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).select()
            if com_valid_user:
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.s_value


        elif (user_type_check == 'DEPOT'):
            com_valid_user = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password)).select()
            if com_valid_user:
                depot_mac = 0
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.mac


        else:
            fail = "failed";
            return "<STARTSTART>" + fail + "<ENDEND>"

#        return depot_mac    
        if(depot_mac == mac_get):

            com_data_limit = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'LIMITBY')).select(db.sm_settings.s_value)
            if com_valid_user:
                limitby = 0
                limit = 0
                for com_data_limit in com_data_limit:
                    limit = com_data_limit.s_value


            limitby = (0, int(limit))

#                if(single_table[i]=='sm_order'):
                #  order==============   
            date_download = date_fixed - datetime.timedelta(minutes=2)
#            return date_download

            req_status = []
            req_status.append('Returned')
            req_status.append('Cancelled')
            if user_type_check == 'HO':
#                query_data=db((db.sm_return.cid==cid) & (db.sm_return.return_date<=date_download)  & (db.sm_return.ho_status=='0') & (db.sm_return.status.belongs(req_status))).select(db.sm_return.ALL,orderby=db.sm_return.return_date|db.sm_return.depot_id|db.sm_return.sl,limitby=limitby)
                query_data = db((db.sm_return.cid == cid) & (db.sm_return.updated_on <= date_download) & (db.sm_return.ho_status == '0') & (db.sm_return.status.belongs(req_status))).select(db.sm_return.ALL, orderby=db.sm_return.updated_on | db.sm_return.depot_id | db.sm_return.sl, limitby=limitby)
            else:
#                query_data=db((db.sm_return.cid==cid) & (db.sm_return.return_date<=date_download)  & (db.sm_return.depot_status=='0') & (db.sm_return.depot_id==user_id) & (db.sm_return.status.belongs(req_status))).select(db.sm_return.ALL,orderby=db.sm_return.return_date|db.sm_return.depot_id|db.sm_return.sl,limitby=limitby)
                query_data = db((db.sm_return.cid == cid) & (db.sm_return.updated_on <= date_download) & (db.sm_return.depot_status == '0') & (db.sm_return.depot_id == user_id) & (db.sm_return.status.belongs(req_status))).select(db.sm_return.ALL, orderby=db.sm_return.updated_on | db.sm_return.depot_id | db.sm_return.sl, limitby=limitby)

            return_value = ''
#            return db._lastsql
            for row_query_data in query_data:
                return_value = str(return_value) + str(row_query_data.depot_id) + "<fd>" + str(row_query_data.sl) + "<fd>" + str(row_query_data.client_id) + "<fd>" + str(row_query_data.rep_id) + "<fd>" + str(row_query_data.return_date) + "<fd>" + str(row_query_data.order_sl) + "<fd>" + str(row_query_data.invoice_sl) + "<fd>" + str(row_query_data.area_id) + "<fd>" + str(row_query_data.status) + "<fd>" + str(row_query_data.order_media) + "<fd>" + str(row_query_data.discount) + "<fd>" + str(row_query_data.ym_date) + "<fd>" + str(row_query_data.item_id) + "<fd>" + str(row_query_data.item_name) + "<fd>" + str(row_query_data.category_id) + "<fd>" + str(row_query_data.quantity) + "<fd>" + str(row_query_data.bonus_qty) + "<fd>" + str(row_query_data.price) + "<fd>" + str(row_query_data.short_note) + "<fd>" + str(row_query_data.note) + "<fd><rd>"

#            return db._lastsql
            return "<STARTSTART>" + str(return_value) + "<ENDEND>"

        else :
            fail = "failed"

            return "<STARTSTART>" + fail + "<ENDEND>"

def update_return():
    my_str = request.args(0)

    my_str = get_decript(my_str)
#    return my_str
    if my_str == '':
        fail = "failed";
        fail = get_encript(fail);
        return "<STARTSTART>" + fail + "<ENDEND>";
    elif (my_str != ""):
        separator_url = '<url>'
        cid = ''
        user_id = ''

        password = ''
        mac_get = ''
        depot_get = ''
#        table_name_withSl=''
        url_list = my_str.split(separator_url, my_str.count(separator_url))

        cid = url_list[0]
        user_type = url_list[1]
        user_id = url_list[2]
        password = url_list[3]
        mac_get = url_list[4]
        update_string = url_list[5] #Get full depot_id and sl string

#        return sl


        depot_mac = 0
        user_type_check = str(user_type).upper()
#        ====================if user type HO===============

        if (user_type_check == 'HO'):
            com_valid_user = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).select()
            if com_valid_user:
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.s_value


        elif (user_type_check == 'DEPOT'):
            com_valid_user = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password)).select()
            if com_valid_user:
                depot_mac = 0
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.mac


        else:
            fail = "failed";
            return "<STARTSTART>" + fail + "<ENDEND>"





    if(depot_mac == mac_get):
        query = ''
        query2 = ''
        if user_type_check == 'HO':
            query = db.sm_order.cid == cid
        else:
           query = db.sm_order.cid == cid
           query &= db.sm_order.depot_id == user_id

        try:
            update_string_single = update_string.split('.', update_string.count('.')) #Split main data by.  
            total_update_string_single = update_string.count('.') #count total .
            i = 0
            while i < total_update_string_single + 1: #while lopp based oncount total
               update_id_sl = update_string_single[i].split(',', update_string_single[i].count(','))#split single strin by,
               if user_type_check == 'HO':
                   query = db((db.sm_return.cid == cid) & (db.sm_return.depot_id == update_id_sl[0]) & (db.sm_return.sl == update_id_sl[1])).update(ho_status='1')
                   query_head = db((db.sm_return_head.cid == cid) & (db.sm_return_head.depot_id == update_id_sl[0]) & (db.sm_return_head.sl == update_id_sl[1])).update(ho_status='1')

               else:
                   query = db((db.sm_return.cid == cid) & (db.sm_return.depot_id == update_id_sl[0]) & (db.sm_return.sl == update_id_sl[1])).update(depot_status='1')
                   query_head = db((db.sm_return_head.cid == cid) & (db.sm_return_head.depot_id == update_id_sl[0]) & (db.sm_return_head.sl == update_id_sl[1])).update(depot_status='1')


               i = i + 1 #increase i

            success = "success";
            return "<STARTSTART>" + success + "<ENDEND>"

        except:
            fail = "failed"
            return "<STARTSTART>" + fail + "<ENDEND>"






#----------------------Inbox--------------------------

def inbox_data():
    my_str = request.args(0)

    my_str = get_decript(my_str)

    if my_str == '':
        fail = "failed";
        fail = get_encript(fail);
        return "<STARTSTART>" + fail + "<ENDEND>";
    elif (my_str != ""):
        separator_url = '<url>'
        cid = ''
        user_id = ''
        password = ''
        mac_get = ''
        depot_get = ''
        url_list = my_str.split(separator_url, my_str.count(separator_url))
        cid = url_list[0]
        user_type = url_list[1]
        user_id = url_list[2]
        password = url_list[3]
        mac_get = url_list[4]
        date_download = date_fixed


#        return ("fixed"+str(date_fixed)+"dd"+str(date_download))
        user_type_check = str(user_type).upper()
        depot_mac = 0
#        ====================if user type HO===============

        if (user_type_check == 'HO'):
            com_valid_user = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).select()
            if com_valid_user:
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.s_value

        else:
            fail = "failed";
            return "<STARTSTART>" + fail + "<ENDEND>"

#        return depot_mac    
        if(depot_mac == mac_get):

            com_data_limit = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == 'LIMITBY')).select(db.sm_settings.s_value)
            if com_valid_user:
                limitby = 0
                limit = 0
                for com_data_limit in com_data_limit:
                    limit = com_data_limit.s_value


            limitby = (0, int(limit))

#                if(single_table[i]=='sm_order'):
                #  order==============   
            date_download = date_fixed - datetime.timedelta(minutes=2)
#            return date_download


            if user_type_check == 'HO':
                query_data = db((db.sm_inbox.cid == cid) & (db.sm_inbox.sms_date <= date_download) & (db.sm_inbox.ho_status == '0')).select(db.sm_inbox.ALL, orderby=db.sm_inbox.sms_date | db.sm_inbox.sl, limitby=limitby)

#            return db._lastsql        
            return_value = ''
#            return query_data
            for row_query_data in query_data:
                return_value = str(return_value) + str(row_query_data.sl) + "<fd>" + str(row_query_data.mobile_no) + "<fd>" + str(row_query_data.sms_date) + "<fd>" + str(row_query_data.sms) + "<fd>" + str(row_query_data.status) + "<fd>" + str(row_query_data.note) + "<fd>" + str(row_query_data.error_in_sms) + "<fd><rd>"
#            return db._lastsql
            return "<STARTSTART>" + str(return_value) + "<ENDEND>"

        else :
            fail = "failed"

            return "<STARTSTART>" + fail + "<ENDEND>"


def update_inbox():
    my_str = request.args(0)

    my_str = get_decript(my_str)
#    return my_str
    if my_str == '':
        fail = "failed";
        fail = get_encript(fail);
        return "<STARTSTART>" + fail + "<ENDEND>";
    elif (my_str != ""):
        separator_url = '<url>'
        cid = ''
        user_id = ''

        password = ''
        mac_get = ''
        depot_get = ''
#        table_name_withSl=''
        url_list = my_str.split(separator_url, my_str.count(separator_url))

        cid = url_list[0]
        user_type = url_list[1]
        user_id = url_list[2]
        password = url_list[3]
        mac_get = url_list[4]
        update_string = url_list[5] #Get full depot_id and sl string

#        return sl


        depot_mac = 0
        user_type_check = str(user_type).upper()
#        ====================if user type HO===============

        if (user_type_check == 'HO'):
            com_valid_user = db((db.sm_settings.cid == cid) & (db.sm_settings.s_key == password)).select()
            if com_valid_user:
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.s_value


        elif (user_type_check == 'DEPOT'):
            com_valid_user = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password)).select()
            if com_valid_user:
                depot_mac = 0
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.mac


        else:
            fail = "failed";
            return "<STARTSTART>" + fail + "<ENDEND>"





    if(depot_mac == mac_get):
        query = ''
        query2 = ''
        if user_type_check == 'HO':
            query = db.sm_order.cid == cid
        else:
           query = db.sm_order.cid == cid
           query &= db.sm_order.depot_id == user_id

        try:
#            return update_string
            update_string_single = update_string.split(',', update_string.count(',')) #Split main data by.  
            total_update_string_single = update_string.count(',') #count total .
            i = 0
#            sl_list="0"
            while i < total_update_string_single + 1: #while lopp based oncount total
#               update_id_sl=update_string_single[i].split(',',update_string_single[i].count(','))#split single strin by,
               if user_type_check == 'HO':
#                    sl_list=sl_list+","+update_string_single[i]
                   query = db((db.sm_inbox.cid == cid) & (db.sm_inbox.sl == update_string_single[i])).update(ho_status='1')



               i = i + 1 #increase i
#            return  sl_list   
            success = "success";
            return "<STARTSTART>" + success + "<ENDEND>"

        except:
            fail = "failed"
            return "<STARTSTART>" + fail + "<ENDEND>"





