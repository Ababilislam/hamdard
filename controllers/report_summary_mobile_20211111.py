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
# http://127.0.0.1:8000/hamdard/report_summary_mobile/index?cid=HAMDARD&rep_id=ITZM&rep_pass=1234

# region
# http://127.0.0.1:8000/hamdard/report_summary_mobile/index?cid=HAMDARD&rep_id=ITRSM&rep_pass=1234

# area
# http://127.0.0.1:8000/hamdard/report_summary_mobile/index?cid=HAMDARD&rep_id=ITFM&rep_pass=1234

# tr
# http://127.0.0.1:8000/hamdard/report_summary_mobile/index?cid=HAMDARD&rep_id=IT03&rep_pass=1234


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
            redirect(URL(c='report_summary_mobile', f='target_vs_achievement_tr_summary'))

        else:
            checkSupRows = db((db.sm_supervisor_level.cid == c_id) & (db.sm_supervisor_level.sup_id == user_id)).select(db.sm_supervisor_level.level_depth_no)

            if checkSupRows:
                level_depth_no = checkSupRows[0].level_depth_no

                if level_depth_no == 0:
                    redirect(URL(c='report_summary_mobile', f='target_vs_achievement_zone_wise'))
                elif level_depth_no == 1:
                    redirect(URL(c='report_summary_mobile', f='target_vs_achievement_region_wise'))
                elif level_depth_no == 2:
                    redirect(URL(c='report_summary_mobile', f='target_vs_achievement_area_wise'))

    return dict()

def target_vs_achievement_zone_wise():
    c_id = session.cid
    user_id = session.user_id

    response.title = 'Target Vs Achievement '

    first_currentDate = datetime.datetime.strptime(str(current_date)[0:7] + '-01', '%Y-%m-%d')

    zone_list=[]
    checkSupRows = db((db.sm_supervisor_level.cid == c_id) & (db.sm_supervisor_level.sup_id == user_id) & (db.sm_supervisor_level.level_depth_no == 0)).select(db.sm_supervisor_level.level_id)

    if checkSupRows:
        level_id = checkSupRows[0].level_id
        zone_list.append(level_id)

    targetAchRows=''
    if len(zone_list)>0:
        qset=db()
        qset=qset(db.target_vs_achievement_route_item.cid == c_id)
        qset = qset(db.target_vs_achievement_route_item.first_date == first_currentDate)
        qset = qset(db.target_vs_achievement_route_item.zone_id.belongs(zone_list))
        # qset = qset(db.sm_level.cid == db.target_vs_achievement_route_item.cid)
        # qset = qset(db.sm_level.depth == 3)
        # qset = qset(db.sm_level.level_id == db.target_vs_achievement_route_item.territory_id)#,db.sm_level.level_name

        targetAchRows=qset.select(db.target_vs_achievement_route_item.zone_id,db.target_vs_achievement_route_item.item_id,db.target_vs_achievement_route_item.item_name,db.target_vs_achievement_route_item.target_qty.sum(),db.target_vs_achievement_route_item.achievement_qty.sum(),groupby=db.target_vs_achievement_route_item.zone_id|db.target_vs_achievement_route_item.item_id,orderby=~db.target_vs_achievement_route_item.achievement_qty)

    return dict(targetAchRows=targetAchRows)

def target_vs_achievement_region_wise():
    c_id = session.cid
    user_id = session.user_id

    response.title = 'Target Vs Achievement '

    first_currentDate = datetime.datetime.strptime(str(current_date)[0:7] + '-01', '%Y-%m-%d')

    region_list=[]
    checkSupRows = db((db.sm_supervisor_level.cid == c_id) & (db.sm_supervisor_level.sup_id == user_id) & (db.sm_supervisor_level.level_depth_no == 1)).select(db.sm_supervisor_level.level_id)

    if checkSupRows:
        level_id = checkSupRows[0].level_id
        region_list.append(level_id)

    targetAchRows=''
    if len(region_list)>0:
        qset=db()
        qset=qset(db.target_vs_achievement_route_item.cid == c_id)
        qset = qset(db.target_vs_achievement_route_item.first_date == first_currentDate)
        qset = qset(db.target_vs_achievement_route_item.region_id.belongs(region_list))
        # qset = qset(db.sm_level.cid == db.target_vs_achievement_route_item.cid)
        # qset = qset(db.sm_level.depth == 3)
        # qset = qset(db.sm_level.level_id == db.target_vs_achievement_route_item.territory_id)#,db.sm_level.level_name

        targetAchRows=qset.select(db.target_vs_achievement_route_item.region_id,db.target_vs_achievement_route_item.item_id,db.target_vs_achievement_route_item.item_name,db.target_vs_achievement_route_item.target_qty.sum(),db.target_vs_achievement_route_item.achievement_qty.sum(),groupby=db.target_vs_achievement_route_item.region_id|db.target_vs_achievement_route_item.item_id,orderby=~db.target_vs_achievement_route_item.achievement_qty)

    return dict(targetAchRows=targetAchRows)

def target_vs_achievement_area_wise():
    c_id = session.cid
    user_id = session.user_id

    response.title = 'Target Vs Achievement '

    first_currentDate = datetime.datetime.strptime(str(current_date)[0:7] + '-01', '%Y-%m-%d')

    area_list=[]
    checkSupRows = db((db.sm_supervisor_level.cid == c_id) & (db.sm_supervisor_level.sup_id == user_id) & (db.sm_supervisor_level.level_depth_no == 2)).select(db.sm_supervisor_level.level_id)

    if checkSupRows:
        level_id = checkSupRows[0].level_id
        area_list.append(level_id)

    targetAchRows=''
    if len(area_list)>0:
        qset=db()
        qset=qset(db.target_vs_achievement_route_item.cid == c_id)
        qset = qset(db.target_vs_achievement_route_item.first_date == first_currentDate)
        qset = qset(db.target_vs_achievement_route_item.area_id.belongs(area_list))
        # qset = qset(db.sm_level.cid == db.target_vs_achievement_route_item.cid)
        # qset = qset(db.sm_level.depth == 3)
        # qset = qset(db.sm_level.level_id == db.target_vs_achievement_route_item.territory_id)#,db.sm_level.level_name

        targetAchRows=qset.select(db.target_vs_achievement_route_item.area_id,db.target_vs_achievement_route_item.item_id,db.target_vs_achievement_route_item.item_name,db.target_vs_achievement_route_item.target_qty.sum(),db.target_vs_achievement_route_item.achievement_qty.sum(),groupby=db.target_vs_achievement_route_item.area_id|db.target_vs_achievement_route_item.item_id,orderby=~db.target_vs_achievement_route_item.achievement_qty)

    return dict(targetAchRows=targetAchRows)

def target_vs_achievement_tr_summary():
    c_id = session.cid
    user_id = session.user_id

    response.title = 'Target Vs Achievement '

    first_currentDate = datetime.datetime.strptime(str(current_date)[0:7] + '-01', '%Y-%m-%d')

    btn_submit=request.vars.btn_submit
    if btn_submit:
        tr_id=request.vars.tr_id
        redirect(URL(c='report_summary_mobile', f='target_vs_achievement_tr_details',vars=dict(tr_id=tr_id)))



    tr_list=[]
    repRows = db((db.sm_rep_area.cid == c_id) & (db.sm_rep_area.rep_id == user_id)).select(db.sm_rep_area.area_id)
    for row in repRows:
        area_id=row.area_id
        tr_list.append(area_id)

    targetAchRows=''
    if len(tr_list)>0:
        qset=db()
        qset=qset(db.target_vs_achievement_route_item.cid == c_id)
        qset = qset(db.target_vs_achievement_route_item.first_date == first_currentDate)
        qset = qset(db.target_vs_achievement_route_item.territory_id.belongs(tr_list))

        targetAchRows=qset.select(db.target_vs_achievement_route_item.territory_id,db.target_vs_achievement_route_item.territory_name,db.target_vs_achievement_route_item.price,db.target_vs_achievement_route_item.target_qty.sum(),db.target_vs_achievement_route_item.achievement_qty.sum(),groupby=~db.target_vs_achievement_route_item.territory_id,orderby=~db.target_vs_achievement_route_item.achievement_qty)


    return dict(targetAchRows=targetAchRows)

def target_vs_achievement_tr_details():
    c_id = session.cid
    user_id = session.user_id

    response.title = 'Target Vs Achievement '
    tr_id = request.vars.tr_id
    first_currentDate = datetime.datetime.strptime(str(current_date)[0:7] + '-01', '%Y-%m-%d')

    repRows=''
    targetAchRows=''
    repRows = db((db.sm_rep_area.cid == c_id) & (db.sm_rep_area.rep_id == user_id)& (db.sm_rep_area.area_id == tr_id)).select(db.sm_rep_area.area_id,db.sm_rep_area.area_name,limitby=(0,1))
    if repRows:
        area_id = repRows[0].area_id
        area_name = repRows[0].area_name

        qset = db()
        qset = qset(db.target_vs_achievement_route_item.cid == c_id)
        qset = qset(db.target_vs_achievement_route_item.first_date == first_currentDate)
        qset = qset(db.target_vs_achievement_route_item.territory_id==area_id)

        targetAchRows = qset.select(db.target_vs_achievement_route_item.territory_id,db.target_vs_achievement_route_item.category_id,db.target_vs_achievement_route_item.item_id,db.target_vs_achievement_route_item.item_name,db.target_vs_achievement_route_item.price,db.target_vs_achievement_route_item.target_qty,db.target_vs_achievement_route_item.achievement_qty, orderby=db.target_vs_achievement_route_item.category_id|~db.target_vs_achievement_route_item.achievement_qty)

    return dict(repRows=repRows,targetAchRows=targetAchRows)


