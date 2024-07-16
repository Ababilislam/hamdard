import urllib2
import calendar
import urllib
import time


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)

# zone
# http://127.0.0.1:8000/hamdard/report_summary_mobile/index?cid=HAMDARD&rep_id=5051&rep_pass=1906

# region
# http://127.0.0.1:8000/hamdard/report_summary_mobile/index?cid=HAMDARD&rep_id=948&rep_pass=2505

# area
# http://127.0.0.1:8000/hamdard/report_summary_mobile/index?cid=HAMDARD&rep_id=1596&rep_pass=1906

# tr
# http://127.0.0.1:8000/hamdard/report_summary_mobile/index?cid=HAMDARD&rep_id=3229&rep_pass=1906


def index():
    c_id = request.vars.cid
    rep_id = request.vars.rep_id
    rep_pass = request.vars.rep_pass

    # ---------------------- rep check
    userRecords = 'select cid,rep_id,name,user_type from sm_rep where cid="' + c_id + '" and rep_id="' + rep_id + '" and password="' + rep_pass + '" and status="ACTIVE" limit 0,1;'
    userRecords = db.executesql(userRecords, as_dict=True)

    if len(userRecords) == 0:
        session.flash = 'Invalid/Inactive Supervisor'
    else:
        for i in range(len(userRecords)):
            userRecordsS = userRecords[i]

            cid = userRecordsS['cid']
            user_id = str(userRecordsS['rep_id'])
            name = str(userRecordsS['name'])
            user_type = str(userRecordsS['user_type'])

            session.cid = c_id
            session.user_id = user_id
            session.user_type = user_type

    redirect(URL('report_home'))

    return dict()


def report_home():
    c_id=session.cid
    user_id=session.user_id
    user_type = session.user_type
    btn_submit=request.vars.btn_submit

    if btn_submit:
        if user_type=='rep':
            session.level_depth_no=3
            #redirect(URL(c='report_summary_mobile', f='target_vs_achievement_tr_summary'))

        else:
            checkSupRows = 'select level_depth_no from sm_supervisor_level where cid="' + c_id + '" and sup_id="' + user_id + '";'
            checkSupRows = db.executesql(checkSupRows, as_dict=True)

            #checkSupRows = db((db.sm_supervisor_level.cid == c_id) & (db.sm_supervisor_level.sup_id == user_id)).select(db.sm_supervisor_level.level_depth_no)

            if len(checkSupRows)>0:
                for i in range(len(checkSupRows)):
                    supRows=checkSupRows[i]
                    level_depth_no = supRows['level_depth_no']
                    session.level_depth_no = level_depth_no



        redirect(URL(c='report_summary_mobile', f='target_vs_achievement_item_summary'))

    return dict()

# get item summary

# zone wise item
# region wise item
# area wise item
# tr wise item


def target_vs_achievement_item_summary():
    c_id = session.cid
    user_id = session.user_id
    level_depth_no=session.level_depth_no

    response.title = 'Target Vs Achievement '

    first_currentDate = datetime.datetime.strptime(str(current_date)[0:7] + '-01', '%Y-%m-%d')

    btn_submit = request.vars.btn_submit

    if btn_submit:
        category_id = request.vars.category_id
        item_id = request.vars.item_id
        item_name=request.vars.item_name

        redirect(URL(c='report_summary_mobile', f='target_vs_achievement_item_summary_zone',vars=dict(category_id=category_id,item_id=item_id,item_name=item_name)))

        # if int(level_depth_no)==0:
        #     redirect(URL(c='report_summary_mobile', f='target_vs_achievement_item_summary_zone', vars=dict(category_id=category_id,item_id=item_id)))
        # elif int(level_depth_no)==1:
        #     zone_id=''
        #     levelRows = 'select level_id from sm_level where cid="' + c_id + '" and depth="' + str(level_depth_no) + '" limit 0,1;'
        #     levelRows = db.executesql(levelRows, as_dict=True)
        #     for lRow in range(len(levelRows)):
        #         levelRowsS=levelRows[lRow]
        #         zone_id=levelRowsS['level_id']
        #
        #         redirect(URL(c='report_summary_mobile', f='target_vs_achievement_item_summary_region', vars=dict(category_id=category_id,item_id=item_id,zone_id=zone_id)))
        # elif int(level_depth_no)==2:
        #     redirect(URL(c='report_summary_mobile', f='target_vs_achievement_item_summary_area', vars=dict(category_id=category_id,item_id=item_id)))
        # elif int(level_depth_no)==3:
        #     redirect(URL(c='report_summary_mobile', f='target_vs_achievement_item_summary_tr', vars=dict(category_id=category_id,item_id=item_id)))

    # item category
    itemCatRows = 'select cat_type_id from sm_category_type where cid="' + c_id + '" and type_name="ITEM_CATEGORY" ;'
    itemCatRows = db.executesql(itemCatRows, as_dict=True)

    # user level
    if level_depth_no==3:
        userLevelRows = 'select area_id as level_id from sm_rep_area where cid="' + c_id + '" and rep_id="' + user_id + '";'
        userLevelRows = db.executesql(userLevelRows, as_dict=True)
    else:
        userLevelRows = 'select level_id from sm_supervisor_level where cid="' + c_id + '" and sup_id="' + user_id + '" and level_depth_no="' + str(level_depth_no) + '";'
        userLevelRows = db.executesql(userLevelRows, as_dict=True)

    if len(userLevelRows)==0:
        response.flash='Assign Area'
    else:
        level_id_list=[]
        for uRow in range(len(userLevelRows)):
            userLevelRowsS=userLevelRows[uRow]

            level_id_list.append(str(userLevelRowsS['level_id']))

        level_id_str = str(level_id_list).replace("[","").replace("]","").replace("', '","','")


        condition_str=''

        if level_depth_no == 0:
            condition_str = ' and zone_id in ( '+level_id_str+') '
        elif level_depth_no == 1:
            condition_str = ' and region_id in ( '+level_id_str+') '
        elif level_depth_no == 2:
            condition_str = ' and area_id  in ( '+level_id_str+') '
        elif level_depth_no == 3:
            condition_str = ' and territory_id in ('+level_id_str+') '

        targetAchRows = 'select category_id,item_id,item_name,sum(target_qty) as target_qty,sum(achievement_qty) as achievement_qty from target_vs_achievement_route_item where cid="' + c_id + '" and first_date="' + str(first_currentDate)[:10] + '" ' + str(condition_str) + ' group by category_id,item_id order by category_id,item_name;'
        targetAchRows = db.executesql(targetAchRows, as_dict=True)


    return dict(itemCatRows=itemCatRows,targetAchRows=targetAchRows)


def target_vs_achievement_item_summary_zone():
    c_id = session.cid
    user_id = session.user_id
    level_depth_no=session.level_depth_no

    response.title = 'Target Vs Achievement Zone Wise'

    first_currentDate = datetime.datetime.strptime(str(current_date)[0:7] + '-01', '%Y-%m-%d')

    category_id = request.vars.category_id
    item_id = request.vars.item_id
    item_name = request.vars.item_name

    btn_submit_z = request.vars.btn_submit_z
    if btn_submit_z:
        zone_id = request.vars.zone_id
        zone_name = request.vars.zone_name
        redirect(URL(c='report_summary_mobile', f='target_vs_achievement_item_summary_region', vars=dict(category_id=category_id,item_id=item_id,item_name=item_name,zone_id=zone_id,zone_name=zone_name)))


    # user level
    if level_depth_no==3:
        userLevelRows = 'select area_id as level_id from sm_rep_area where cid="' + c_id + '" and rep_id="' + user_id + '";'
        userLevelRows = db.executesql(userLevelRows, as_dict=True)
    else:
        userLevelRows = 'select level_id from sm_supervisor_level where cid="' + c_id + '" and sup_id="' + user_id + '" and level_depth_no="' + str(level_depth_no) + '";'
        userLevelRows = db.executesql(userLevelRows, as_dict=True)

    if len(userLevelRows)==0:
        response.flash='Assign Area'
    else:
        level_id_list=[]
        for uRow in range(len(userLevelRows)):
            userLevelRowsS=userLevelRows[uRow]

            level_id_list.append(str(userLevelRowsS['level_id']))

        level_id_str = str(level_id_list).replace("[","").replace("]","").replace("', '","','")


        condition_str=''
        if level_depth_no == 0:
            condition_str = ' and zone_id in ( '+level_id_str+') '
        elif level_depth_no == 1:
            condition_str = ' and region_id in ( '+level_id_str+') '
        elif level_depth_no == 2:
            condition_str = ' and area_id  in ( '+level_id_str+') '
        elif level_depth_no == 3:
            condition_str = ' and territory_id in ('+level_id_str+') '

        condition_str += ' and category_id ="' + category_id + '" '
        condition_str += ' and item_id ="' + item_id + '" '

        targetAchRows = 'select zone_id,zone_name,item_id,item_name,sum(target_qty) as target_qty,sum(achievement_qty) as achievement_qty from target_vs_achievement_route_item where cid="' + c_id + '" and first_date="' + str(first_currentDate)[:10] + '" ' + str(condition_str) + ' group by category_id,zone_id,item_id order by category_id,zone_id,item_name;'
        targetAchRows = db.executesql(targetAchRows, as_dict=True)


    return dict(category_id=category_id,item_id=item_id,item_name=item_name,targetAchRows=targetAchRows)


def target_vs_achievement_item_summary_region():
    c_id = session.cid
    user_id = session.user_id
    level_depth_no=session.level_depth_no

    response.title = 'Target Vs Achievement Region Wise'

    first_currentDate = datetime.datetime.strptime(str(current_date)[0:7] + '-01', '%Y-%m-%d')

    category_id = request.vars.category_id
    item_id = request.vars.item_id
    item_name = request.vars.item_name
    zone_id = request.vars.zone_id
    zone_name = request.vars.zone_name

    btn_submit_r = request.vars.btn_submit_r
    if btn_submit_r:
        region_id = request.vars.region_id
        region_name = request.vars.region_name
        redirect(URL(c='report_summary_mobile', f='target_vs_achievement_item_summary_area', vars=dict(category_id=category_id,item_id=item_id,item_name=item_name,zone_id=zone_id,zone_name=zone_name,region_id=region_id,region_name=region_name)))


    # user level
    if level_depth_no==3:
        userLevelRows = 'select area_id as level_id from sm_rep_area where cid="' + c_id + '" and rep_id="' + user_id + '";'
        userLevelRows = db.executesql(userLevelRows, as_dict=True)
    else:
        userLevelRows = 'select level_id from sm_supervisor_level where cid="' + c_id + '" and sup_id="' + user_id + '" and level_depth_no="' + str(level_depth_no) + '";'
        userLevelRows = db.executesql(userLevelRows, as_dict=True)

    if len(userLevelRows)==0:
        response.flash='Assign Area'
    else:
        level_id_list=[]
        for uRow in range(len(userLevelRows)):
            userLevelRowsS=userLevelRows[uRow]

            level_id_list.append(str(userLevelRowsS['level_id']))

        level_id_str = str(level_id_list).replace("[","").replace("]","").replace("', '","','")


        condition_str=''
        if level_depth_no == 0:
            condition_str = ' and zone_id in ( '+level_id_str+') '
        elif level_depth_no == 1:
            condition_str = ' and region_id in ( '+level_id_str+') '
        elif level_depth_no == 2:
            condition_str = ' and area_id  in ( '+level_id_str+') '
        elif level_depth_no == 3:
            condition_str = ' and territory_id in ('+level_id_str+') '

        condition_str += ' and category_id ="' + category_id + '" '
        condition_str += ' and item_id ="' + item_id + '" '
        condition_str += ' and zone_id ="' + zone_id + '" '

        targetAchRows = 'select region_id,region_name,item_id,item_name,sum(target_qty) as target_qty,sum(achievement_qty) as achievement_qty from target_vs_achievement_route_item where cid="' + c_id + '" and first_date="' + str(first_currentDate)[:10] + '" ' + str(condition_str) + ' group by region_id,item_id order by region_id,item_name;'
        targetAchRows = db.executesql(targetAchRows, as_dict=True)


    return dict(category_id=category_id,item_id=item_id,item_name=item_name,zone_id=zone_id,zone_name=zone_name,targetAchRows=targetAchRows)


def target_vs_achievement_item_summary_area():
    c_id = session.cid
    user_id = session.user_id
    level_depth_no=session.level_depth_no

    response.title = 'Target Vs Achievement Area Wise'

    first_currentDate = datetime.datetime.strptime(str(current_date)[0:7] + '-01', '%Y-%m-%d')

    category_id = request.vars.category_id
    item_id = request.vars.item_id
    item_name = request.vars.item_name
    zone_id = request.vars.zone_id
    zone_name = request.vars.zone_name
    region_id = request.vars.region_id
    region_name = request.vars.region_name

    btn_submit_a = request.vars.btn_submit_a
    if btn_submit_a:
        area_id = request.vars.area_id
        area_name = request.vars.area_name
        redirect(URL(c='report_summary_mobile', f='target_vs_achievement_item_summary_tr', vars=dict(category_id=category_id,item_id=item_id,item_name=item_name,zone_id=zone_id,zone_name=zone_name,region_id=region_id,region_name=region_name,area_id=area_id,area_name=area_name)))


    # user level
    if level_depth_no==3:
        userLevelRows = 'select area_id as level_id from sm_rep_area where cid="' + c_id + '" and rep_id="' + user_id + '";'
        userLevelRows = db.executesql(userLevelRows, as_dict=True)
    else:
        userLevelRows = 'select level_id from sm_supervisor_level where cid="' + c_id + '" and sup_id="' + user_id + '" and level_depth_no="' + str(level_depth_no) + '";'
        userLevelRows = db.executesql(userLevelRows, as_dict=True)

    if len(userLevelRows)==0:
        response.flash='Assign Area'
    else:
        level_id_list=[]
        for uRow in range(len(userLevelRows)):
            userLevelRowsS=userLevelRows[uRow]

            level_id_list.append(str(userLevelRowsS['level_id']))

        level_id_str = str(level_id_list).replace("[","").replace("]","").replace("', '","','")


        condition_str=''
        if level_depth_no == 0:
            condition_str = ' and zone_id in ( '+level_id_str+') '
        elif level_depth_no == 1:
            condition_str = ' and region_id in ( '+level_id_str+') '
        elif level_depth_no == 2:
            condition_str = ' and area_id  in ( '+level_id_str+') '
        elif level_depth_no == 3:
            condition_str = ' and territory_id in ('+level_id_str+') '

        condition_str += ' and category_id ="' + category_id + '" '
        condition_str += ' and item_id ="' + item_id + '" '
        condition_str += ' and zone_id ="' + zone_id + '" '
        condition_str += ' and region_id ="' + region_id + '" '

        targetAchRows = 'select area_id,area_name,item_id,item_name,sum(target_qty) as target_qty,sum(achievement_qty) as achievement_qty from target_vs_achievement_route_item where cid="' + c_id + '" and first_date="' + str(first_currentDate)[:10] + '" ' + str(condition_str) + ' group by area_id,item_id order by area_id,item_name;'
        targetAchRows = db.executesql(targetAchRows, as_dict=True)


    return dict(category_id=category_id,item_id=item_id,item_name=item_name,zone_id=zone_id,zone_name=zone_name,region_id=region_id,region_name=region_name,targetAchRows=targetAchRows)


def target_vs_achievement_item_summary_tr():
    c_id = session.cid
    user_id = session.user_id
    level_depth_no=session.level_depth_no

    response.title = 'Target Vs Achievement Zone Wise'

    first_currentDate = datetime.datetime.strptime(str(current_date)[0:7] + '-01', '%Y-%m-%d')

    category_id = request.vars.category_id
    item_id = request.vars.item_id
    item_name = request.vars.item_name
    zone_id = request.vars.zone_id
    zone_name = request.vars.zone_name
    region_id = request.vars.region_id
    region_name = request.vars.region_name
    area_id = request.vars.area_id
    area_name = request.vars.area_name


    # user level
    if level_depth_no==3:
        userLevelRows = 'select area_id as level_id from sm_rep_area where cid="' + c_id + '" and rep_id="' + user_id + '";'
        userLevelRows = db.executesql(userLevelRows, as_dict=True)
    else:
        userLevelRows = 'select level_id from sm_supervisor_level where cid="' + c_id + '" and sup_id="' + user_id + '" and level_depth_no="' + str(level_depth_no) + '";'
        userLevelRows = db.executesql(userLevelRows, as_dict=True)

    if len(userLevelRows)==0:
        response.flash='Assign Area'
    else:
        level_id_list=[]
        for uRow in range(len(userLevelRows)):
            userLevelRowsS=userLevelRows[uRow]

            level_id_list.append(str(userLevelRowsS['level_id']))

        level_id_str = str(level_id_list).replace("[","").replace("]","").replace("', '","','")


        condition_str=''
        if level_depth_no == 0:
            condition_str = ' and zone_id in ( '+level_id_str+') '
        elif level_depth_no == 1:
            condition_str = ' and region_id in ( '+level_id_str+') '
        elif level_depth_no == 2:
            condition_str = ' and area_id  in ( '+level_id_str+') '
        elif level_depth_no == 3:
            condition_str = ' and territory_id in ('+level_id_str+') '

        condition_str += ' and category_id ="' + category_id + '" '
        condition_str += ' and item_id ="' + item_id + '" '
        condition_str += ' and zone_id ="' + zone_id + '" '
        condition_str += ' and region_id ="' + region_id + '" '
        condition_str += ' and area_id ="' + area_id + '" '

        targetAchRows = 'select territory_id,territory_name,item_id,item_name,sum(target_qty) as target_qty,sum(achievement_qty) as achievement_qty from target_vs_achievement_route_item where cid="' + c_id + '" and first_date="' + str(first_currentDate)[:10] + '" ' + str(condition_str) + ' group by territory_id,item_id order by territory_id,item_name;'
        targetAchRows = db.executesql(targetAchRows, as_dict=True)


    return dict(category_id=category_id,item_id=item_id,item_name=item_name,zone_id=zone_id,zone_name=zone_name,region_id=region_id,region_name=region_name,area_id=area_id,area_name=area_name,targetAchRows=targetAchRows)















# not use


# def target_vs_achievement_zone_summary():
#     c_id = session.cid
#     user_id = session.user_id
#
#     response.title = 'Target Vs Achievement '
#
#     first_currentDate = datetime.datetime.strptime(str(current_date)[0:7] + '-01', '%Y-%m-%d')
#
#     btn_submit = request.vars.btn_submit
#     if btn_submit:
#         item_id = request.vars.item_id
#         redirect(URL(c='report_summary_mobile', f='target_vs_achievement_zone_wise', vars=dict(item_id=item_id)))
#
#
#     itemCatRows=db((db.sm_category_type.cid == c_id) & (db.sm_category_type.type_name == 'ITEM_CATEGORY')).select(db.sm_category_type.cat_type_id)
#
#     zone_list=[]
#     checkSupRows = db((db.sm_supervisor_level.cid == c_id) & (db.sm_supervisor_level.sup_id == user_id) & (db.sm_supervisor_level.level_depth_no == 0)).select(db.sm_supervisor_level.level_id)
#
#     for row in checkSupRows:
#         level_id = row.level_id
#         zone_list.append(level_id)
#
#
#
#     targetAchRows=''
#     if len(zone_list)>0:
#         qset=db()
#         qset=qset(db.target_vs_achievement_route_item.cid == c_id)
#         qset = qset(db.target_vs_achievement_route_item.first_date == first_currentDate)
#         qset = qset(db.target_vs_achievement_route_item.zone_id.belongs(zone_list))
#         # qset = qset(db.sm_level.cid == db.target_vs_achievement_route_item.cid)
#         # qset = qset(db.sm_level.depth == 3)
#         # qset = qset(db.sm_level.level_id == db.target_vs_achievement_route_item.territory_id)#,db.sm_level.level_name
#
#         targetAchRows=qset.select(db.target_vs_achievement_route_item.category_id,db.target_vs_achievement_route_item.item_id,db.target_vs_achievement_route_item.item_name,db.target_vs_achievement_route_item.target_qty.sum(),db.target_vs_achievement_route_item.achievement_qty.sum(),groupby=db.target_vs_achievement_route_item.category_id|db.target_vs_achievement_route_item.item_name,orderby=db.target_vs_achievement_route_item.item_name)
#
#     return dict(itemCatRows=itemCatRows,targetAchRows=targetAchRows)
#
# def target_vs_achievement_zone_wise():
#     c_id = session.cid
#     user_id = session.user_id
#
#     response.title = 'Target Vs Achievement '
#
#     first_currentDate = datetime.datetime.strptime(str(current_date)[0:7] + '-01', '%Y-%m-%d')
#     item_id = request.vars.item_id
#
#     btn_submit = request.vars.btn_submit
#     if btn_submit:
#         zone_id = request.vars.zone_id
#         item_id = request.vars.item_id
#         redirect(URL(c='report_summary_mobile', f='target_vs_achievement_region_wise', vars=dict(zone_id=zone_id,item_id=item_id)))
#
#     zone_list=[]
#     checkSupRows = db((db.sm_supervisor_level.cid == c_id) & (db.sm_supervisor_level.sup_id == user_id) & (db.sm_supervisor_level.level_depth_no == session.level_depth_no)).select(db.sm_supervisor_level.level_id)
#
#     for row in checkSupRows:
#         level_id = row.level_id
#         zone_list.append(level_id)
#
#     level0Str = str(zone_list).replace("['", "").replace("']", "").replace("', '", ",")
#
#     targetAchRows=''
#     if len(zone_list)>0:
#         qset=db()
#         qset=qset(db.target_vs_achievement_route_item.cid == c_id)
#         qset = qset(db.target_vs_achievement_route_item.first_date == first_currentDate)
#         qset = qset(db.target_vs_achievement_route_item.zone_id.belongs(zone_list))
#         qset = qset(db.target_vs_achievement_route_item.item_id==item_id)
#         # qset = qset(db.sm_level.cid == db.target_vs_achievement_route_item.cid)
#         # qset = qset(db.sm_level.depth == 3)
#         # qset = qset(db.sm_level.level_id == db.target_vs_achievement_route_item.territory_id)#,db.sm_level.level_name
#
#         targetAchRows=qset.select(db.target_vs_achievement_route_item.zone_id,db.target_vs_achievement_route_item.item_id,db.target_vs_achievement_route_item.item_name,db.target_vs_achievement_route_item.target_qty.sum(),db.target_vs_achievement_route_item.achievement_qty.sum(),groupby=db.target_vs_achievement_route_item.zone_id|db.target_vs_achievement_route_item.item_id,orderby=db.target_vs_achievement_route_item.zone_id)
#
#     return dict(item_id=item_id,level0Str=level0Str,targetAchRows=targetAchRows)
#
# def target_vs_achievement_region_summary():
#     c_id = session.cid
#     user_id = session.user_id
#
#     response.title = 'Target Vs Achievement '
#
#     first_currentDate = datetime.datetime.strptime(str(current_date)[0:7] + '-01', '%Y-%m-%d')
#
#     btn_submit = request.vars.btn_submit
#     if btn_submit:
#         item_id = request.vars.item_id
#         redirect(URL(c='report_summary_mobile', f='target_vs_achievement_region_wise', vars=dict(item_id=item_id)))
#
#     region_list=[]
#     checkSupRows = db((db.sm_supervisor_level.cid == c_id) & (db.sm_supervisor_level.sup_id == user_id) & (db.sm_supervisor_level.level_depth_no == session.level_depth_no)).select(db.sm_supervisor_level.level_id)
#
#     for row in checkSupRows:
#         level_id = row.level_id
#         region_list.append(level_id)
#
#     targetAchRows=''
#     if len(region_list)>0:
#         qset=db()
#         qset=qset(db.target_vs_achievement_route_item.cid == c_id)
#         qset = qset(db.target_vs_achievement_route_item.first_date == first_currentDate)
#         qset = qset(db.target_vs_achievement_route_item.region_id.belongs(region_list))
#         # qset = qset(db.sm_level.cid == db.target_vs_achievement_route_item.cid)
#         # qset = qset(db.sm_level.depth == 3)
#         # qset = qset(db.sm_level.level_id == db.target_vs_achievement_route_item.territory_id)#,db.sm_level.level_name
#
#         targetAchRows=qset.select(db.target_vs_achievement_route_item.item_id,db.target_vs_achievement_route_item.item_name,db.target_vs_achievement_route_item.target_qty.sum(),db.target_vs_achievement_route_item.achievement_qty.sum(),groupby=db.target_vs_achievement_route_item.item_id,orderby=db.target_vs_achievement_route_item.item_id)
#
#     return dict(targetAchRows=targetAchRows)
#
# def target_vs_achievement_region_wise():
#     c_id = session.cid
#     user_id = session.user_id
#
#     response.title = 'Target Vs Achievement '
#
#     first_currentDate = datetime.datetime.strptime(str(current_date)[0:7] + '-01', '%Y-%m-%d')
#     item_id = request.vars.item_id
#     zone_id = request.vars.zone_id
#
#     region_list=[]
#     qset=db()
#     qset=qset(db.sm_supervisor_level.cid == c_id)
#     qset = qset(db.sm_supervisor_level.sup_id == user_id)
#
#     if zone_id!='':
#         qset = qset(db.sm_supervisor_level.level_id == zone_id)
#
#     qset = qset(db.sm_supervisor_level.level_depth_no == session.level_depth_no)
#
#     checkSupRows = qset.select(db.sm_supervisor_level.level_id)
#
#     for row in checkSupRows:
#         level_id = row.level_id
#         region_list.append(level_id)
#
#     level0Str = str(region_list).replace("['", "").replace("']", "").replace("', '", ",")
#
#     targetAchRows=''
#     if len(region_list)>0:
#         qset=db()
#         qset=qset(db.target_vs_achievement_route_item.cid == c_id)
#         qset = qset(db.target_vs_achievement_route_item.first_date == first_currentDate)
#         qset = qset(db.target_vs_achievement_route_item.region_id.belongs(region_list))
#         qset = qset(db.target_vs_achievement_route_item.item_id == item_id)
#         # qset = qset(db.sm_level.cid == db.target_vs_achievement_route_item.cid)
#         # qset = qset(db.sm_level.depth == 3)
#         # qset = qset(db.sm_level.level_id == db.target_vs_achievement_route_item.territory_id)#,db.sm_level.level_name
#
#         targetAchRows=qset.select(db.target_vs_achievement_route_item.region_id,db.target_vs_achievement_route_item.item_id,db.target_vs_achievement_route_item.item_name,db.target_vs_achievement_route_item.target_qty.sum(),db.target_vs_achievement_route_item.achievement_qty.sum(),groupby=db.target_vs_achievement_route_item.region_id|db.target_vs_achievement_route_item.item_id,orderby=db.target_vs_achievement_route_item.region_id)
#
#     return dict(item_id=item_id,zone_id=zone_id,level0Str=level0Str,targetAchRows=targetAchRows)
#
# def target_vs_achievement_area_summary():
#     c_id = session.cid
#     user_id = session.user_id
#
#     response.title = 'Target Vs Achievement '
#
#     first_currentDate = datetime.datetime.strptime(str(current_date)[0:7] + '-01', '%Y-%m-%d')
#
#     area_list=[]
#     checkSupRows = db((db.sm_supervisor_level.cid == c_id) & (db.sm_supervisor_level.sup_id == user_id) & (db.sm_supervisor_level.level_depth_no == session.level_depth_no)).select(db.sm_supervisor_level.level_id)
#
#     for row in checkSupRows:
#         level_id = row.level_id
#         area_list.append(level_id)
#
#     targetAchRows=''
#     if len(area_list)>0:
#         qset=db()
#         qset=qset(db.target_vs_achievement_route_item.cid == c_id)
#         qset = qset(db.target_vs_achievement_route_item.first_date == first_currentDate)
#         qset = qset(db.target_vs_achievement_route_item.area_id.belongs(area_list))
#         # qset = qset(db.sm_level.cid == db.target_vs_achievement_route_item.cid)
#         # qset = qset(db.sm_level.depth == 3)
#         # qset = qset(db.sm_level.level_id == db.target_vs_achievement_route_item.territory_id)#,db.sm_level.level_name
#
#         targetAchRows=qset.select(db.target_vs_achievement_route_item.item_id,db.target_vs_achievement_route_item.item_name,db.target_vs_achievement_route_item.target_qty.sum(),db.target_vs_achievement_route_item.achievement_qty.sum(),groupby=db.target_vs_achievement_route_item.item_id,orderby=db.target_vs_achievement_route_item.item_id)
#
#     return dict(targetAchRows=targetAchRows)
#
# def target_vs_achievement_area_wise():
#     c_id = session.cid
#     user_id = session.user_id
#
#     response.title = 'Target Vs Achievement '
#
#     first_currentDate = datetime.datetime.strptime(str(current_date)[0:7] + '-01', '%Y-%m-%d')
#     item_id = request.vars.item_id
#
#     area_list=[]
#     checkSupRows = db((db.sm_supervisor_level.cid == c_id) & (db.sm_supervisor_level.sup_id == user_id) & (db.sm_supervisor_level.level_depth_no == session.level_depth_no)).select(db.sm_supervisor_level.level_id)
#
#     for row in checkSupRows:
#         level_id = row.level_id
#         area_list.append(level_id)
#
#     targetAchRows=''
#     if len(area_list)>0:
#         qset=db()
#         qset=qset(db.target_vs_achievement_route_item.cid == c_id)
#         qset = qset(db.target_vs_achievement_route_item.first_date == first_currentDate)
#         qset = qset(db.target_vs_achievement_route_item.area_id.belongs(area_list))
#         qset = qset(db.target_vs_achievement_route_item.item_id == item_id)
#         # qset = qset(db.sm_level.cid == db.target_vs_achievement_route_item.cid)
#         # qset = qset(db.sm_level.depth == 3)
#         # qset = qset(db.sm_level.level_id == db.target_vs_achievement_route_item.territory_id)#,db.sm_level.level_name
#
#         targetAchRows=qset.select(db.target_vs_achievement_route_item.area_id,db.target_vs_achievement_route_item.item_id,db.target_vs_achievement_route_item.item_name,db.target_vs_achievement_route_item.target_qty.sum(),db.target_vs_achievement_route_item.achievement_qty.sum(),groupby=db.target_vs_achievement_route_item.area_id|db.target_vs_achievement_route_item.item_id,orderby=db.target_vs_achievement_route_item.area_id)
#
#     return dict(targetAchRows=targetAchRows)
#
# def target_vs_achievement_tr_summary():
#     c_id = session.cid
#     user_id = session.user_id
#
#     response.title = 'Target Vs Achievement '
#
#     first_currentDate = datetime.datetime.strptime(str(current_date)[0:7] + '-01', '%Y-%m-%d')
#
#     btn_submit=request.vars.btn_submit
#     if btn_submit:
#         tr_id=request.vars.tr_id
#         redirect(URL(c='report_summary_mobile', f='target_vs_achievement_tr_details',vars=dict(tr_id=tr_id)))
#
#
#
#     tr_list=[]
#     repRows = db((db.sm_rep_area.cid == c_id) & (db.sm_rep_area.rep_id == user_id)).select(db.sm_rep_area.area_id)
#     for row in repRows:
#         area_id=row.area_id
#         tr_list.append(area_id)
#
#     targetAchRows=''
#     if len(tr_list)>0:
#         qset=db()
#         qset=qset(db.target_vs_achievement_route_item.cid == c_id)
#         qset = qset(db.target_vs_achievement_route_item.first_date == first_currentDate)
#         qset = qset(db.target_vs_achievement_route_item.territory_id.belongs(tr_list))
#
#         targetAchRows=qset.select(db.target_vs_achievement_route_item.territory_id,(db.target_vs_achievement_route_item.price*db.target_vs_achievement_route_item.target_qty).sum(),(db.target_vs_achievement_route_item.price*db.target_vs_achievement_route_item.achievement_qty).sum(),groupby=db.target_vs_achievement_route_item.territory_id,orderby=db.target_vs_achievement_route_item.territory_id) #,db.target_vs_achievement_route_item.territory_name
#
#     return dict(targetAchRows=targetAchRows)
#
# def target_vs_achievement_tr_details():
#     c_id = session.cid
#     user_id = session.user_id
#
#     response.title = 'Target Vs Achievement '
#     tr_id = request.vars.tr_id
#     first_currentDate = datetime.datetime.strptime(str(current_date)[0:7] + '-01', '%Y-%m-%d')
#
#     repRows=''
#     targetAchRows=''
#     repRows = db((db.sm_rep_area.cid == c_id) & (db.sm_rep_area.rep_id == user_id)& (db.sm_rep_area.area_id == tr_id)).select(db.sm_rep_area.area_id,db.sm_rep_area.area_name,limitby=(0,1))
#     if repRows:
#         area_id = repRows[0].area_id
#         area_name = repRows[0].area_name
#
#         qset = db()
#         qset = qset(db.target_vs_achievement_route_item.cid == c_id)
#         qset = qset(db.target_vs_achievement_route_item.first_date == first_currentDate)
#         qset = qset(db.target_vs_achievement_route_item.territory_id==area_id)
#
#         targetAchRows = qset.select(db.target_vs_achievement_route_item.territory_id,db.target_vs_achievement_route_item.item_id,db.target_vs_achievement_route_item.item_name,db.target_vs_achievement_route_item.price,db.target_vs_achievement_route_item.target_qty,db.target_vs_achievement_route_item.achievement_qty, orderby=db.target_vs_achievement_route_item.territory_id|db.target_vs_achievement_route_item.item_id)
#
#     return dict(repRows=repRows,targetAchRows=targetAchRows)


