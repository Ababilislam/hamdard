from random import randint
import urllib2
import calendar

def upload_item():
    cid = 'BIOPHARMA'
#    my_str = request.vars(0)
    my_str = request.vars.str
#    return my_str
#    decode utf8
    import urllib2
    my_str = urllib2.unquote(my_str.decode("utf8"))
#    return my_str
    
#    my_str = get_decript(my_str)


    if my_str == '':
        fail = "failed";
        fail = get_encript(fail);
        return "<START>" + fail + "<END>";
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
        upload_data = url_list[5]


#         return upload_data
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
                        return "<START>" + fail + "<END>"
                else:
                    fail = "failed";
                    return "<START>" + fail + "<END>"
            else:
                fail = "failed";
                return "<START>" + fail + "<END>"
#========================if user type depot===================
        else:
            com_valid_user = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password)).select()
            if com_valid_user:
                depot_mac = 0
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.field1

                flag_mac = '0'
    #  Set mac in db
                if depot_mac == '0':
                    flag_mac = 1
                    mac_update = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id)).update(field1=mac_get)
                elif(depot_mac != '0'):
                    check_mac = db((db.sm_depot.cid == str(cid)) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password) & (db.sm_depot.field1 == mac_get)).select(db.sm_depot.field1)
#                    return db._lastsql
                    if check_mac:
                        flag_mac = 2
                    else:
                        fail = "failed";
                        return "<START>" + fail + "<END>"
                else:
                        fail = "failed";
                        return "<START>" + fail + "<END>"


#         return depot_mac
        depot_mac = mac_get
        if(depot_mac == mac_get):

            separator_row = '<fd><rd>'
            separator_field = '<fd>'
            ProductID = '';
            ProductName = '';
            UnitPrice = 0;
            Unit = '';
            row_list = upload_data.split(separator_row, upload_data.count(separator_row))


            total_row = upload_data.count(separator_row)
            i = 0
            result = "Success"

            while i < total_row  :
                single_row = row_list[i]
#                 return single_row
                field_list = single_row.split(separator_field, single_row.count(separator_field))
                ProductID = field_list[0]
                ProductName = field_list[1]
                UnitPrice = field_list[2]
                Unit = field_list[3]
                Vat = field_list[4]
#                 return ProductID

                i = i + 1
                try:
        #                 Delete
                    db((db.sm_item.cid == cid) & (db.sm_item.item_id == ProductID)).delete()
        #                 Insert
                    price=float(UnitPrice)+(float(UnitPrice)*(float(Vat)/100))
                    price_insert = round(price, 2)
                    db.sm_item.insert(cid=cid, item_id=str(ProductID).strip().upper(), name=str(ProductName).strip().upper(), category_id='DEFAULT', price=float(price_insert), dist_price=float(price_insert), unit_type=Unit)
    #                 db.sm_item.insert(cid=cid, item_id=str(ProductID).strip().upper(), name=str(ProductName).strip().upper(), category_id='DEFAULT', price=float(UnitPrice), unit_type=Unit)
                except:
                    result = "Error: ProductID: "+str(item_id)




            return "<START>" + result + "<END>"


def upload_client():
    cid = 'BIOPHARMA'
#    my_str = request.args(0)

#    my_str = get_decript(my_str)
    
    my_str = request.vars.str
    import urllib2
    my_str = urllib2.unquote(my_str.decode("utf8"))
    
    if my_str == '':
        fail = "failed";
        fail = get_encript(fail);
        return "<START>" + fail + "<END>";
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
        upload_data = url_list[5]


#        return upload_data
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
                        return "<START>" + fail + "<END>"
                else:
                    fail = "failed";
                    return "<START>" + fail + "<END>"
            else:
                fail = "failed";
                return "<START>" + fail + "<END>"
#========================if user type depot===================
        else:
            com_valid_user = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password)).select()
            if com_valid_user:
                depot_mac = 0
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.field1

                flag_mac = '0'
    #  Set mac in db
                if depot_mac == '0':
                    flag_mac = 1
                    mac_update = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id)).update(field1=mac_get)
                elif(depot_mac != '0'):
                    check_mac = db((db.sm_depot.cid == str(cid)) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password) & (db.sm_depot.field1 == mac_get)).select(db.sm_depot.field1)
#                    return db._lastsql
                    if check_mac:
                        flag_mac = 2
                    else:
                        fail = "failed";
                        return "<START>" + fail + "<END>"
                else:
                        fail = "failed";
                        return "<START>" + fail + "<END>"


#         return depot_mac
        depot_mac = mac_get
        if(depot_mac == mac_get):

            separator_row = '<fd><rd>'
            separator_field = '<fd>'
            ProductID = '';
            ProductName = '';
            UnitPrice = 0;
            Unit = '';
            row_list = upload_data.split(separator_row, upload_data.count(separator_row))


            total_row = upload_data.count(separator_row)
            i = 0
            result = "Success"

            while i < total_row  :
                single_row = row_list[i]
#                 return single_row
                field_list = single_row.split(separator_field, single_row.count(separator_field))

                CustId = field_list[0]
                Name = field_list[1]
                WorkingArea = field_list[2]
                SalesCenter = field_list[3]
                PartyCategory = field_list[4]
                status = field_list[5]
#                 return ProductID

                i = i + 1
                try:
        #                 Delete
                    db((db.sm_client.cid == cid) & (db.sm_client.client_id == CustId)).delete()
        #                 Insert
                    db.sm_client.insert(cid=cid, client_id=str(CustId).strip().upper(), name=str(Name).strip().upper(), area_id=str(WorkingArea).strip().upper(), category_id=str(PartyCategory).strip().upper(), depot_id=str(user_id).strip().upper(),status='ACTIVE')
        #                 db.sm_item.insert(cid=cid, item_id=str(ProductID).strip().upper(), name=str(ProductName).strip().upper(), category_id='DEFAULT', price=float(UnitPrice), unit_type=Unit)
                except:
                    result = "Error: CustId: "+str(CustId)




            return "<START>" + result + "<END>"


def upload_area_n_reparea():
    cid = 'BIOPHARMA'
#    my_str = request.args(0)

#    my_str = get_decript(my_str)

    my_str = request.vars.str
    import urllib2
    my_str = urllib2.unquote(my_str.decode("utf8"))
    
    
    if my_str == '':
        fail = "failed";
        fail = get_encript(fail);
        return "<START>" + fail + "<END>";
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
        upload_data = url_list[5]


#        return upload_data
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
                        return "<START>" + fail + "<END>"
                else:
                    fail = "failed";
                    return "<START>" + fail + "<END>"
            else:
                fail = "failed";
                return "<START>" + fail + "<END>"
#========================if user type depot===================
        else:
            com_valid_user = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password)).select()
            if com_valid_user:
                depot_mac = 0
                for row_valid_user in com_valid_user:
                    depot_mac = row_valid_user.field1

                flag_mac = '0'
    #  Set mac in db
                if depot_mac == '0':
                    flag_mac = 1
                    mac_update = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id)).update(field1=mac_get)
                elif(depot_mac != '0'):
                    check_mac = db((db.sm_depot.cid == str(cid)) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password) & (db.sm_depot.field1 == mac_get)).select(db.sm_depot.field1)
#                    return db._lastsql
                    if check_mac:
                        flag_mac = 2
                    else:
                        fail = "failed";
                        return "<START>" + fail + "<END>"
                else:
                        fail = "failed";
                        return "<START>" + fail + "<END>"


#         return depot_mac
        depot_mac = mac_get
        if(depot_mac == mac_get):

            separator_row = '<fd><rd>'
            separator_field = '<fd>'
            ProductID = '';
            ProductName = '';
            UnitPrice = 0;
            Unit = '';
            row_list = upload_data.split(separator_row, upload_data.count(separator_row))


            total_row = upload_data.count(separator_row)
            i = 0
            result = "Success"

            while i < total_row  :
                single_row = row_list[i]
#                 return single_row
                field_list = single_row.split(separator_field, single_row.count(separator_field))

                PNO = field_list[0]
                TerritoryCode = field_list[1]
                TerritoryName = field_list[2]
                MPOCode = field_list[3]
                MPOName = field_list[4]
                
                
                


                i = i + 1
                try: 
        #                 Delete
                    db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.rep_id == MPOCode)).delete()
                    db((db.sm_level.cid == cid) & (db.sm_level.level_id == TerritoryCode)).delete()
                    
        #                 Insert
                    db.sm_rep_area.insert(cid=cid, rep_id=str(MPOCode).strip().upper(), rep_name=str(MPOName).strip().upper(), area_id=str(TerritoryCode).strip().upper(), area_name=str(TerritoryName).strip().upper(), depot_id=str(PNO).strip().upper())
                    
                    db.sm_level.insert(cid=cid, level_id=str(TerritoryCode).strip().upper(), level_name=str(TerritoryName).strip().upper(), parent_level_id=str(PNO).strip().upper(), level0=str(PNO).strip().upper(), level1=str(TerritoryCode).strip().upper(), depth=1, is_leaf=1, depot_id=str(PNO).strip().upper())
        #                 db.sm_item.insert(cid=cid, item_id=str(ProductID).strip().upper(), name=str(ProductName).strip().upper(), category_id='DEFAULT', price=float(UnitPrice), unit_type=Unit)
                except:
                    result = "Error: TerritoryCode: "+str(TerritoryCode)




            return "<START>" + result + "<END>"


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
                    depot_mac = row_valid_user.field1

                flag_mac = '0'
    #  Set mac in db
#                return depot_mac
                if depot_mac == '0':
                    flag_mac = 1
                    mac_update = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == user_id)).update(field1=mac_get)
                    return db._lastsql
                elif(depot_mac != '0'):
                    check_mac = db((db.sm_depot.cid == str(cid)) & (db.sm_depot.depot_id == user_id) & (db.sm_depot.dm_pass == password) & (db.sm_depot.field1 == mac_get)).select(db.sm_depot.field1)
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
            return "<STARTSTART>" + "Success" + "<ENDEND>"            
        else :
            return "<STARTSTART>" + "failed" + "<ENDEND>"



def upload_path():
    return '<start>http://e2.businesssolutionapps.com/mrepbiopharma/<end>';
#    return '<start>http://127.0.0.1:8000/mrepbiopharma/<end>';
#    



