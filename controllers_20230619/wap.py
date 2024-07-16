# wap login
import urllib2

def index():
    return "Success"
    response.title = 'Wap'
    return dict()

def check_user():
    cid = str(request.vars.cid).strip().upper()
    uid = str(request.vars.uid).strip().upper()
    password = str(request.vars.password).strip()
#    return password
    # if cid,userid,pass blank
    if (cid == '' or uid == '' or password == ''):
        session.flash = 'CID,User ID and Password required !'
        redirect(URL('index'))
    # Check valid company

    comp_check_row = db((db.sm_company_settings.cid == cid) & (db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.status, limitby=(0, 1))
    if comp_check_row:
        rep_check_row = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == uid) & (db.sm_rep.password == password) & (db.sm_rep.wap == 'Yes') & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.status, db.sm_rep.field1, db.sm_rep.note, limitby=(0, 1))
        if rep_check_row:
            session.wap_cid = cid
            session.wap_uid = uid
            for records_rep in rep_check_row:
                field1 = str(records_rep.field1).strip()  # Used to set area
                first_page = str(records_rep.note).strip()  # Used to set settings

#                return first_page
#            check rep set area in sm_rep

            if (field1 == ''):
                rep_route_row = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.rep_id == uid)).select(db.sm_rep_area.ALL, orderby=db.sm_rep_area.area_name, limitby=(0, 1))
                area_id = ''
                area_name = ''
                depot_id = ''
                for records in rep_route_row:
                    area_id = str(records.area_id).strip()
                    area_name = str(records.area_name).strip()
                    depot_id = str(records.depot_id).strip()
#                return area_id


#                 db((db.sm_rep.cid == session.wap_cid) & (db.sm_rep.rep_id == session.wap_uid)).update(field1=area_id)
                area_id_show = 'All'
                area_name_show = 'All'
                return str(area_id_show) + 'rdrd' + str(area_name_show) + 'rdrd' + str(depot_id) + 'rdrd' + str(first_page)
#                session.wap_area_id=area_id
#                session.wap_area_name=area_name
#                session.wap_depot_id=depot_id
            else:
                rep_route_row = db((db.sm_rep_area.cid == cid) & (db.sm_rep_area.rep_id == uid) & (db.sm_rep_area.area_id == field1)).select(db.sm_rep_area.ALL, orderby=db.sm_rep_area.area_name, limitby=(0, 1))
                for records in rep_route_row:
                    area_id = str(records.area_id).strip()
                    area_name = str(records.area_name).strip()
                    depot_id = str(records.depot_id).strip()


                return str(area_id) + 'rdrd' + str(area_name) + 'rdrd' + str(depot_id) + 'rdrd' + str(first_page)
#                session.wap_area_id=area_id
#                session.wap_area_name=area_name
#                session.wap_depot_id=depot_id

#            return first_page
            #            check rep set first page in sm_rep on note field
#            if ((first_page=='') | (first_page=='None')):
#                return 'noroute'
# #                redirect(URL(c='wap',f='menu'))
#            else:
#                return first_page
# #                session.wap_first_page=first_page
#                redirect(URL(c='wap',f=first_page))

            # return rep_check_row
#            redirect(URL(c='wap',f='menu'))
        else:
            return 'Failed'
#            redirect(URL('index'))
    else:
        return 'Failed'
#        redirect(URL('index'))




def menu():
    response.title = 'Menu'
    return dict()


def order():
    response.title = 'Order'
    session.submit_type = "order"
    redirect(URL('customer'))

def delivery():
    response.title = 'Delivery'
    session.submit_type = "delivery"
    redirect(URL('customer'))

def customer():
    response.title = 'Customer'

    wap_cid = str(request.vars.cid).strip().upper()
    wap_area_id = str(request.vars.area_id).strip().upper()
    wap_uid = str(request.vars.rep_id).strip().upper()
#    return wap_area_id


    if (wap_area_id == 'ALL'):
        rep_level_row = db((db.sm_rep.cid == wap_cid) & (db.sm_rep.rep_id == wap_uid)).select(db.sm_rep.depot_id, limitby=(0, 1))
#         return db._lastsql
        rep_depot = ''
        for records_level in rep_level_row:
            rep_depot = records_level.depot_id
        records = db((db.sm_client.cid == wap_cid) & (db.sm_client.depot_id == rep_depot)).select(db.sm_client.client_id, db.sm_client.name, orderby=db.sm_client.name)
    else:
        records = db((db.sm_client.cid == wap_cid) & (db.sm_client.area_id == wap_area_id)).select(db.sm_client.client_id, db.sm_client.name, orderby=db.sm_client.name)

    client_string = ''
    for records in records:
        client_id = str(records.client_id).strip()
        name = str(records.name).strip()
        client_string = client_string + client_id + ',' + name + 'fdfd'

#    return db._lastsql
    return client_string
#    return dict(records=records)


# def customer_set():
#
#
#     Radio_client = str(request.vars.Radio_client).strip().upper()
#
# #    return Radio_client
#     if (Radio_client == "NONE"):
#         redirect(URL('customer'))
#     session.wap_client_id = Radio_client
#
#
#     client_name_row = db((db.sm_client.cid == session.wap_cid) & (db.sm_client.client_id == session.wap_client_id)).select(db.sm_client.name, limitby=(0, 1))
#     client_name = ""
#     for records in client_name_row:
#         client_name = str(records.name).strip()
#
#     session.wap_client_name = client_name
#
#
#     redirect(URL('item'))
def item():
    response.title = 'Item'
    wap_cid = str(request.vars.cid).strip().upper()

    records = db((db.sm_item.cid == wap_cid)).select(db.sm_item.ALL, orderby=db.sm_item.name)
#     return db._lastsql
    item_string = ''
    for records in records:
        item_id = str(records.item_id).strip()
        name = str(records.name).strip()
        des = str(records.des).strip()
        category_id = str(records.category_id).strip()
        unit_type = str(records.unit_type).strip()
        manufacturer = str(records.manufacturer).strip()
        price = str(records.price).strip()
        dist_price = str(records.dist_price).strip()
        item_string = item_string + item_id + ',' + name + ',' + des + ',' + category_id + ',' + unit_type + ',' + manufacturer + ',' + price + ',' + dist_price + 'fdfd'

#    return db._lastsql
    session.item_string = item_string
    return item_string

#     return dict(records_item=records_item)




# def show_cart():
#     response.title = 'Cart'
# #   Item id list
#     item_id = str(request.vars.item_id)
#     item_id = item_id.replace("[", "")
#     item_id = item_id.replace("]", "")
#     item_id = item_id.replace("'", "")
#     item_id = item_id.replace(" ", "")
#     item_id_list = item_id.split(',')
#
# #   Item name list
#     item_name = str(request.vars.item_name)
#     item_name = item_name.replace("[", "")
#     item_name = item_name.replace("]", "")
#     item_name = item_name.replace("'", "")
#     item_name = item_name.replace(" ", "")
#     item_name_list = item_name.split(',')
# #    return item_id
# #   Item Qty
#     item_qty = str(request.vars.item_qty)
#     item_qty = item_qty.replace("[", "")
#     item_qty = item_qty.replace("]", "")
#     item_qty = item_qty.replace("'", "")
#     item_qty = item_qty.replace(" ", "")
#     qty_list = item_qty.split(',')
#
# #   Item Catagory
#     item_catagory = str(request.vars.category_id)
# #    return item_catagory
#     item_catagory = item_catagory.replace("[", "")
#     item_catagory = item_catagory.replace("]", "")
#     item_catagory = item_catagory.replace("'", "")
#     item_catagory = item_catagory.replace(" ", "")
#     catagory_list = item_catagory.split(',')
#
# #   Item Price
#     price = str(request.vars.price)
#     price = price.replace("[", "")
#     price = price.replace("]", "")
#     price = price.replace("'", "")
#     price = price.replace(" ", "")
#     price_list = price.split(',')
#
#
#     ins_list = []
#     for i in range(len(item_id_list)):
#         item_id_ins = str(item_id_list[i]).strip()
#         item_name_ins = str(item_name_list[i]).strip()
#         item_catagory_ins = str(catagory_list[i]).strip()
#         price_ins = str(price_list[i]).strip()
#         item_qty_ins = str(qty_list[i]).strip()
#
#
#
#         if (item_qty_ins != ""):
#             ins_dict = {'cid':session.wap_cid, 'item_id':item_id_ins, 'name':item_name_ins, 'category_id':item_catagory_ins, 'price':price_ins, 'qty':item_qty_ins}
#             ins_list.append(ins_dict)
# #    return ins_list
#
#     return dict(ins_list=ins_list)


def item_change():
    response.title = 'Item'
    wap_cid = str(request.vars.cid).strip().upper()
    wap_depot_id_get = str(request.vars.depot_id).strip().upper()
    wap_uid = str(request.vars.wap_uid).strip().upper()
    submit_type = str(request.vars.submit_type).strip()
    submit_string = str(request.vars.submit_string).strip()
    wap_client_id = str(request.vars.client_id).strip()
    wap_client_name = str(request.vars.client_name).strip()
#     return submit_type
    rep_level_row = db((db.sm_rep.cid == wap_cid) & (db.sm_rep.rep_id == wap_uid)).select(db.sm_rep.depot_id, limitby=(0, 1))
#         return db._lastsql
    wap_depot_id = ''
    for records_level in rep_level_row:
        wap_depot_id = records_level.depot_id

    submit_string = urllib2.unquote(submit_string)
    wap_client_name = urllib2.unquote(wap_client_name)
#     return wap_cid
    ins_list = []
    ins_dict = {}
    if (submit_type == 'delivery'):

        # Get sl from sm_depot
        query_sl = db((db.sm_depot.cid == wap_cid) & (db.sm_depot.depot_id == wap_depot_id)).select(db.sm_depot.id, db.sm_depot.del_sl, limitby=(0, 1))
        for row_sl in query_sl:
            sl = row_sl.del_sl
            sl = int(sl) + 1
            break
#            --- sl update in depot
        query_sl[0].update_record(del_sl=sl)


        order_date = str(date_fixed)[0:10]
        delivery_date = date_fixed
        ym_date = str(delivery_date)[0:7] + '-01'
        depot_name_check = db((db.sm_depot.cid == wap_cid) & (db.sm_depot.depot_id == wap_depot_id)).select(db.sm_depot.name)
        for depot_name_check in depot_name_check:
            depot_name = depot_name_check.name
            break
        rep_name_check = db((db.sm_rep.cid == wap_cid) & (db.sm_rep.rep_id == wap_uid)).select(db.sm_rep.name)
        for rep_name_check in rep_name_check:
            rep_name = rep_name_check.name
            break
        area_id_check = db((db.sm_client.cid == wap_cid) & (db.sm_client.client_id == wap_client_id)).select(db.sm_client.area_id)
        wap_area_id = ''
        for area_id_check in area_id_check:
            wap_area_id = area_id_check.area_id
            break
        area_name_check = db((db.sm_level.cid == wap_cid) & (db.sm_level.level_id == wap_area_id)).select(db.sm_level.level_name)
        wap_area_name = ''
        for area_name_check in area_name_check:
            wap_area_name = area_name_check.level_name
            break
        totalAmount = 0
        item_single = submit_string.split('rdrd', submit_string.count('rdrd'))
        item_total = submit_string.count('rdrd')
#         return submit_string
        x = 0
        while (x < item_total):
            item_info = item_single[x].split('fdfd', item_single[x].count('fdfd'))

            item_id_ins = item_info[0]
            item_name_ins = item_info[1]
            item_catagory_ins = item_info[2]
            price_ins = item_info[3]
            item_qty_ins = item_info[4]


            temp_amount = float(price_ins) * float(item_qty_ins)
            totalAmount = float(totalAmount) + float(temp_amount)

            ins_dict = {'cid':wap_cid, 'depot_id':wap_depot_id, 'depot_name':depot_name, 'sl':int(sl), 'client_id':wap_client_id, 'client_name':wap_client_name, 'rep_id':wap_uid, 'rep_name':rep_name, 'order_datetime':date_fixed, 'delivery_date':delivery_date, 'area_id':wap_area_id, 'area_name':wap_area_name, 'item_id':item_id_ins, 'item_name':item_name_ins, 'category_id':item_catagory_ins, 'price':price_ins, 'quantity':item_qty_ins, 'invoice_media':'WAP', 'status':'Invoiced', 'ym_date':ym_date}
#                          (cid=cid,              depot_id=depot_id,              depot_name=depot_name,  sl=int(sl), client_id=client_id,               client_name=client_name,             rep_id=rep_id,           rep_name=rep_name,   order_datetime=date_fixed,  delivery_date=delivery_date,  area_id=area_id,              area_name=area_name,              item_id=prodct_id,   item_name=name,           category_id=catagory,            price=price,     quantity=product_qty,invoice_media='SMS', status='Invoiced',  ym_date=ym_date)
            ins_list.append(ins_dict)
            x = x + 1
#         return len(ins_list)
        db.sm_invoice_head.insert(cid=wap_cid, depot_id=wap_depot_id, depot_name=depot_name, sl=int(sl), client_id=wap_client_id, client_name=wap_client_name, rep_id=wap_uid, rep_name=rep_name, order_datetime=date_fixed, delivery_date=delivery_date, area_id=wap_area_id, area_name=wap_area_name, invoice_media='WAP', status='Invoiced', ym_date=ym_date)

        if len(ins_list) > 0:
            # Bulk insert
            db.sm_invoice.bulk_insert(ins_list)

#            Update balance
            data_for_balance_update = str(session.wap_cid) + '<fdfd>DELIVERY<fdfd>' + str(sl) + '<fdfd>' + str(datetime_fixed) + '<fdfd>' + str(session.wap_depot_id) + '-' + str(sl) + '<fdfd>DPT-' + str(session.wap_depot_id) + '<fdfd>CLT-' + str(session.wap_client_id) + '<fdfd>' + str(totalAmount)
    #                return data_for_balance_update

            result_string = set_balance_transaction(data_for_balance_update)
#             return result_string
            return "Successrdrd" + str(sl)
        else:
            return "Failed"

#         redirect(URL(c='wap', f='result', args=[sl, session.submit_type]))



    if (submit_type == 'order'):
        # Get sl from sm_depot
        query_sl = db((db.sm_depot.cid == wap_cid) & (db.sm_depot.depot_id == wap_depot_id)).select(db.sm_depot.id, db.sm_depot.order_sl, limitby=(0, 1))
#         return db._lastsql
        for row_sl in query_sl:
            sl = row_sl.order_sl
            sl = int(sl) + 1
            break
#            --- sl update in depot
        query_sl[0].update_record(order_sl=sl)


        order_date = str(date_fixed)[0:10]
        delivery_date = date_fixed
        ym_date = str(delivery_date)[0:7] + '-01'


        depot_name_check = db((db.sm_depot.cid == wap_cid) & (db.sm_depot.depot_id == wap_depot_id)).select(db.sm_depot.name)
        for depot_name_check in depot_name_check:
            depot_name = depot_name_check.name
            break
        rep_name_check = db((db.sm_rep.cid == wap_cid) & (db.sm_rep.rep_id == wap_uid)).select(db.sm_rep.name)
        for rep_name_check in rep_name_check:
            rep_name = rep_name_check.name
            break
        area_id_check = db((db.sm_client.cid == wap_cid) & (db.sm_client.client_id == wap_client_id)).select(db.sm_client.area_id)
        wap_area_id = ''
        for area_id_check in area_id_check:
            wap_area_id = area_id_check.area_id
            break
        area_name_check = db((db.sm_level.cid == wap_cid) & (db.sm_level.level_id == wap_area_id)).select(db.sm_level.level_name)
        wap_area_name = ''
        for area_name_check in area_name_check:
            wap_area_name = area_name_check.level_name
            break
        totalAmount = 0
        item_single = submit_string.split('rdrd', submit_string.count('rdrd'))
        item_total = submit_string.count('rdrd')
#         return submit_string
        x = 0
        while (x < item_total):
            item_info = item_single[x].split('fdfd', item_single[x].count('fdfd'))

            item_id_ins = item_info[0]
            item_name_ins = item_info[1]
            item_catagory_ins = item_info[2]
            price_ins = item_info[3]
            item_qty_ins = item_info[4]


            temp_amount = float(price_ins) * float(item_qty_ins)
            totalAmount = float(totalAmount) + float(temp_amount)


            ins_dict = {'cid':wap_cid, 'depot_id':wap_depot_id, 'depot_name':depot_name, 'sl':int(sl), 'client_id':wap_client_id, 'client_name':wap_client_name, 'rep_id':wap_uid, 'rep_name':rep_name, 'order_date':str(date_fixed)[0:10], 'delivery_date':str(date_fixed)[0:10], 'area_id':wap_area_id, 'area_name':wap_area_name, 'item_id':item_id_ins, 'item_name':item_name_ins, 'category_id':item_catagory_ins, 'price':price_ins, 'quantity':item_qty_ins, 'order_media':'WAP', 'status':'Submitted', 'ym_date':ym_date}
#                         (cid=cid,               depot_id=depot_id,              depot_name=depot_name,  sl=int(sl),  client_id=client_id,              client_name=client_name,             rep_id=rep_id,            rep_name=rep_name,  order_date=order_date,                 delivery_date=delivery_date,          area_id=area_id,              area_name=area_name,              item_id=prodct_id,    item_name=name,           category_id=catagory,           price=price,      quantity=product_qty,   order_media='SMS',  status='Submitted',  ym_date=ym_date)
            ins_list.append(ins_dict)
            x = x + 1
        db.sm_order_head.insert(cid=wap_cid, depot_id=wap_depot_id, depot_name=depot_name, sl=int(sl), client_id=wap_client_id, client_name=wap_client_name, rep_id=wap_uid, rep_name=rep_name, order_date=str(date_fixed)[0:10], delivery_date=str(date_fixed)[0:10], area_id=wap_area_id, area_name=wap_area_name, order_media='WAP', status='Submitted', ym_date=ym_date)
#                db.sm_order_head.insert(cid=cid,           depot_id=depot_id,            depot_name=depot_name,sl=int(sl),client_id=client_id,             client_name=client_name,           rep_id=rep_id,         rep_name=rep_name, order_date=order_date,          delivery_date=delivery_date,        area_id=area_id,            area_name=area_name,            order_media='SMS',status='Submitted',ym_date=ym_date)
        if len(ins_list) > 0:
            # Bulk insert
            db.sm_order.bulk_insert(ins_list)
            return "Successrdrd" + str(sl)
        else:
            return "Failed"

#         redirect(URL(c='wap', f='result', args=[sl, session.submit_type]))


def result():
    response.title = 'Result'
    sl = request.args(0)
    submit_type = request.args(1)
    return dict(sl=sl, submit_type=submit_type)



def settings():
    response.title = 'Settings'
    wap_cid = str(request.vars.cid).strip().upper()
    wap_uid = str(request.vars.wap_uid).strip().upper()
    first_page = str(request.vars.first_page).strip()

#    return first_page
    if (first_page == "None"):
        pass
    else:
        db((db.sm_rep.cid == wap_cid) & (db.sm_rep.rep_id == wap_uid)).update(note=first_page)
#        return db._lastsql
        rep_row = db((db.sm_rep.cid == wap_cid) & (db.sm_rep.rep_id == wap_uid)).select(db.sm_rep.note, limitby=(0, 1))
        for records in rep_row:
            first_page = str(records.note).strip()
#         first_page = records.note
#         session.wap_first_page = first_page
        return 'first_page'



#     return dict()




def route():

    response.title = 'Route'
    Radio_route = str(request.vars.Radio_route).strip().upper()
    wap_cid = str(request.vars.cid).strip().upper()
    wap_uid = str(request.vars.wap_uid).strip().upper()

    area_id = ''
    area_name = ''
    depot_id = ''
    record_string = ''
#    return Radio_route
    if ((Radio_route == "NONE") or (Radio_route == "All")):
#         db((db.sm_rep.cid == wap_cid) & (db.sm_rep.rep_id == wap_uid)).update(field1='')
        rep_level_row = db((db.sm_rep.cid == wap_cid) & (db.sm_rep.rep_id == wap_uid)).select(db.sm_rep.depot_id, limitby=(0, 1))
        for records_level in rep_level_row:
            rep_depot = records_level.depot_id

        records = db((db.sm_level.cid == wap_cid) & (db.sm_level.depot_id == rep_depot) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)

        for record in records:
            area_id_record = record.level_id
            area_name_record = record.level_name
            record_string = record_string + area_id_record + ',' + area_name_record + 'fdfd'

        pass
    else:
        rep_route_row = db((db.sm_rep_area.cid == wap_cid) & (db.sm_rep_area.rep_id == wap_uid) & (db.sm_rep_area.area_id == Radio_route)).select(db.sm_rep_area.ALL, orderby=db.sm_rep_area.area_name, limitby=(0, 1))

        for records in rep_route_row:
            area_id = records.area_id
            area_name = records.area_name
            depot_id = records.depot_id
            record_string = record_string + area_id + ',' + area_name + 'fdfd'

#         db((db.sm_rep.cid == wap_cid) & (db.sm_rep.rep_id == wap_uid)).update(field1=area_id)
#        session.wap_area_id=area_id
#        session.wap_area_name=area_name
#        session.wap_depot_id=depot_id



#     records = ''
#     if((Radio_route == "NONE") or (Radio_route == "All")):
#         records = db((db.sm_rep_area.cid == wap_cid) & (db.sm_rep_area.rep_id == wap_uid) & (db.sm_rep_area.depot_id == depot_id)).select(db.sm_rep_area.area_id, db.sm_rep_area.area_name,
#         orderby=db.sm_rep_area.area_name)
#     else:

#     rep_level_row = db((db.sm_rep.cid == wap_cid) & (db.sm_rep.rep_id == wap_uid)).select(db.sm_rep.depot_id, limitby=(0, 1))
#     for records_level in rep_level_row:
#         rep_depot = records_level.depot_id
#
#     records = db((db.sm_level.cid == wap_cid) & (db.sm_level.depot_id == rep_depot) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
#     record_string = ''
#     for record in records:
#         area_id_record = record.level_id
#         area_name_record = record.level_name
#         record_string = record_string + area_id_record + ',' + area_name_record + 'fdfd'


#    return records
    return str(area_id) + 'rdrd' + str(area_name) + 'rdrd' + str(depot_id) + 'rdrd' + str(record_string)
#    return dict(records=records)


def logout():
    session.clear
    redirect(URL('index'))

#===========get pass



#======================
# http://127.0.0.1:8000/mf/sync_api/getPassword?cid=MFDEMO&mobile=8801719078552&msg=PASSWORD&httppass=Compaq510DuoDuo
def getPassword():
    import urllib2
    from random import randint
    returnStr = ''

    cid = str(request.vars.cid).strip().upper()
    mobileNo = request.vars.mobile
    keyword = str(request.vars.msg).strip().upper()
    httppass = str(request.vars.httppass).strip()
    
    if httppass != 'Compaq510DuoDuo':
        returnStr = 'Invalid request'
    else:
        if keyword != 'PASSWORD':
            returnStr = 'Invalid Keyword'
        else:
            repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.mobile_no == mobileNo) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.id, db.sm_rep.rep_id,db.sm_rep.user_type, limitby=(0, 1))
#            return db._lastsql
            if not repRow:
                returnStr = 'Invalid User'
            else:
                user_type=repRow[0].user_type
                fieldForceId = repRow[0].rep_id                
                randNumber = randint(1001, 9999)
                
                if user_type=='sup':
                    repRow[0].update_record(password=randNumber, syncCode='')
                else:
                    repRow[0].update_record(password=randNumber, syncCode='', field2=0)
                
                returnStr = 'User ID: ' + str(fieldForceId) + ', Password: ' + str(randNumber) + '  Download Link:  http://im-gp.com/d/bio '

    return returnStr


def set_latlong():
    lat = ''
    long = ''
    visited_id = ''
    visit_time=''
    visited_latlong=''
    id=int(request.args[0])
#    return id
    trackingRows = db((db.sm_tracking_table.cid == "BIOPHARMA") & (db.sm_tracking_table.call_type == "DCR") &  (db.sm_tracking_table.id > int(id)) & (db.sm_tracking_table.id < 793)).select(db.sm_tracking_table.ALL, orderby=db.sm_tracking_table.visit_time ,limitby=(0, 20))
#    return db._lastsql
    for trackingRows in trackingRows:
        id=trackingRows.id
        visited_id = trackingRows.visited_id
        visit_time=trackingRows.visit_time
        visited_latlong=trackingRows.visited_latlong
        
        lat=visited_latlong.split(',')[0]
        long=visited_latlong.split(',')[1]
        
        db((db.sm_doctor_visit.cid == "BIOPHARMA") & (db.sm_doctor_visit.doc_id == visited_id) & (db.sm_doctor_visit.visit_dtime == visit_time)).update(latitude=lat,longitude=long)
#        return db._lastsql
                    
    return id
