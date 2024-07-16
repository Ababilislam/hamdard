#http://w04.yeapps.com/skf/ppm_mark_mobile/index?cid=SKF&rep_id=TRRSM&rep_pass=3671

#rsm
#http://127.0.0.1:8000/skf_w04/ppm_mark_mobile/index?cid=SKF&rep_id=TRRSM&rep_pass=3671

#nsm
#http://127.0.0.1:8000/skf_w04/ppm_mark_mobile/index?cid=SKF&rep_id=TRNSM&rep_pass=7650

#rsm
#http://127.0.0.1:8000/hamdard/report_seen_rx_mobile/index?cid=HAMDARD&rep_id=itmso&rep_pass=1234

def index():
    c_id = request.vars.cid
    rep_id = request.vars.rep_id
    rep_pass = request.vars.rep_pass

    # ---------------------- rep check
    userRecords = db((db.sm_rep.cid == c_id) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == rep_pass) & (
                db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.id, db.sm_rep.name, db.sm_rep.user_type, limitby=(0, 1))

    if not userRecords:
        response.flash = 'Invalid/Inactive Supervisor'
    else:
        name = userRecords[0].name
        user_type = userRecords[0].user_type

        session.cid = c_id
        session.rep_id = rep_id
        session.user_id = rep_id
        session.user_type = user_type

        level_area_list = []

        if user_type=='rep':
            repAreaRows = db((db.sm_rep_area.cid == c_id) & (db.sm_rep_area.rep_id == rep_id)).select(db.sm_rep_area.area_id,db.sm_rep_area.area_name,orderby=db.sm_rep_area.area_id)

            if not repAreaRows:
                response.flash = 'Rep Territory Not Available'
            else:
                for rRow in repAreaRows:
                    area_id=rRow.area_id
                    area_name = rRow.area_name

                    dictData = {'area_id': area_id, 'area_name': area_name}
                    level_area_list.append(dictData)

        else:
            supLevelRows=db((db.sm_supervisor_level.cid==c_id) & (db.sm_supervisor_level.sup_id==rep_id)).select(db.sm_supervisor_level.level_depth_no,db.sm_supervisor_level.level_id)

            if not supLevelRows:
                response.flash = 'Supervisor Level Not Available'
            else:
                sup_level_id_list=[]
                level_depth_no=0
                for sRow in supLevelRows:
                    level_depth_no=sRow.level_depth_no
                    level_id=sRow.level_id
                    sup_level_id_list.append(level_id)

                if level_depth_no==0:
                    level3Rows = db((db.sm_level.cid == c_id) & (db.sm_level.level0.belongs(sup_level_id_list)) & (db.sm_level.depth == 3)).select(db.sm_level.level_id,db.sm_level.level_name, orderby=db.sm_level.level_id,groupby=db.sm_level.level_id)

                    for dRow1 in level3Rows:
                        level_id = dRow1.level_id
                        level_name = dRow1.level_name

                        dictData = {'area_id': level_id, 'area_name': level_name}
                        level_area_list.append(dictData)

                if level_depth_no == 1:
                    level3Rows = db((db.sm_level.cid == c_id) & (db.sm_level.level1.belongs(sup_level_id_list)) & (db.sm_level.depth == 3)).select(db.sm_level.level_id, db.sm_level.level_name,orderby=db.sm_level.level_id,groupby=db.sm_level.level_id)

                    for dRow1 in level3Rows:
                        level_id = dRow1.level_id
                        level_name = dRow1.level_name

                        dictData = {'area_id': level_id, 'area_name': level_name}
                        level_area_list.append(dictData)

                elif level_depth_no==2:
                    level3Rows = db((db.sm_level.cid == c_id) & (db.sm_level.level2.belongs(sup_level_id_list)) & (db.sm_level.depth == 3)).select(db.sm_level.level_id,db.sm_level.level_name, orderby=db.sm_level.level_id,groupby=db.sm_level.level_id)

                    for dRow1 in level3Rows:
                        level_id = dRow1.level_id
                        level_name = dRow1.level_name

                        dictData = {'area_id': level_id, 'area_name': level_name}
                        level_area_list.append(dictData)

        session.level_area_list=level_area_list

        level_area_id_list = []
        for i in range(len(level_area_list)):
            level_area_str = level_area_list[i]
            level_area_id_list.append(level_area_str['area_id'])

        session.level_area_id_list = level_area_id_list

        redirect(URL(c='report_seen_rx_mobile', f='home'))

    return dict()


def home():
    if session.cid=='' or session.cid==None:
        redirect(URL(c='report_seen_rx_mobile',f='index'))

    session.from_date =str(first_currentDate)[:10]
    session.to_date = current_date
    level_area_list = session.level_area_list




    btn_report=request.vars.btn_report

    if btn_report:
        from_date = request.vars.from_date
        to_date = request.vars.to_date
        sch_area = request.vars.sch_area

        session.from_date=from_date
        session.to_date=to_date
        session.sch_area = sch_area

    qset=db()
    qset=qset(db.sm_prescription_seen_details.cid == session.cid)

    if session.user_type=='rep':
        qset = qset(db.sm_prescription_seen_details.submit_by_id == session.rep_id)


    if session.from_date!='' and session.to_date!='':
        qset = qset((db.sm_prescription_seen_details.submit_date >= session.from_date)&(db.sm_prescription_seen_details.submit_date <= session.to_date))

    if session.sch_area!='' and session.sch_area!=None:
        qset = qset(db.sm_prescription_seen_details.area_id==session.sch_area)
    else:
        qset = qset(db.sm_prescription_seen_details.area_id.belongs(session.level_area_id_list))


    records=qset.select(db.sm_prescription_seen_details.submit_by_id,db.sm_prescription_seen_details.submit_by_name,db.sm_prescription_seen_details.area_id,db.sm_prescription_seen_details.medicine_name,db.sm_prescription_seen_details.id.count(),groupby=db.sm_prescription_seen_details.area_id|db.sm_prescription_seen_details.submit_by_id|db.sm_prescription_seen_details.medicine_name,orderby=db.sm_prescription_seen_details.area_id|db.sm_prescription_seen_details.submit_by_id|db.sm_prescription_seen_details.medicine_name)

    # rx count
    qsetH = db()
    qsetH = qsetH(db.sm_prescription_seen_head.cid == session.cid)

    if session.user_type=='rep':
        qsetH = qsetH(db.sm_prescription_seen_head.submit_by_id == session.rep_id)

    if session.from_date!='' and session.to_date!='':
        qsetH = qsetH((db.sm_prescription_seen_head.submit_date >= session.from_date) & (
                    db.sm_prescription_seen_head.submit_date <= session.to_date))

    if session.sch_area!='' and session.sch_area!=None:
        qsetH = qsetH(db.sm_prescription_seen_head.area_id == session.sch_area)
    else:
        qsetH = qsetH(db.sm_prescription_seen_head.area_id.belongs(session.level_area_id_list))

    recordsH=qsetH.count()
    
    return dict(records=records,recordsH=recordsH,level_area_list=level_area_list)







# def index_x():
#
#     c_id=request.vars.cid
#     rep_id=request.vars.rep_id
#     rep_pass=request.vars.rep_pass
#
#     #---------------------- rep check
#     userRecords=db((db.sm_rep.cid==c_id) & (db.sm_rep.rep_id==rep_id)& (db.sm_rep.password==rep_pass)& (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.id,db.sm_rep.name,db.sm_rep.user_type,limitby=(0,1))
#
#     if not userRecords:
#         response.flash = 'Invalid/Inactive Supervisor'
#     else:
#         name=userRecords[0].name
#         user_type=userRecords[0].user_type
#
#         session.cid=c_id
#         session.rep_id=rep_id
#         session.user_id=rep_id
#
#
#         level_area_list = []
#
#         supLevelRows=db((db.sm_supervisor_level.cid==c_id) & (db.sm_supervisor_level.sup_id==rep_id)).select(db.sm_supervisor_level.level_depth_no,db.sm_supervisor_level.level_id)
#
#         if not supLevelRows:
#             response.flash = 'Supervisor Level Not Available'
#         else:
#             sup_level_id_list=[]
#             level_depth_no=0
#             for sRow in supLevelRows:
#                 level_depth_no=sRow.level_depth_no
#                 level_id=sRow.level_id
#                 sup_level_id_list.append(level_id)
#
#             if level_depth_no==0:
#                 level3Rows = db((db.sm_level.cid == c_id) & (db.sm_level.level0.belongs(sup_level_id_list)) & (db.sm_level.depth == 3)).select(db.sm_level.level_id,db.sm_level.level_name, orderby=db.sm_level.level_id,groupby=db.sm_level.level_id)
#
#                 for dRow1 in level3Rows:
#                     level_id = dRow1.level_id
#                     level_name = dRow1.level_name
#
#                     dictData = {'area_id': level_id, 'area_name': level_name}
#                     level_area_list.append(dictData)
#
#             if level_depth_no == 1:
#                 level3Rows = db((db.sm_level.cid == c_id) & (db.sm_level.level1.belongs(sup_level_id_list)) & (db.sm_level.depth == 3)).select(db.sm_level.level_id, db.sm_level.level_name,orderby=db.sm_level.level_id,groupby=db.sm_level.level_id)
#
#                 for dRow1 in level3Rows:
#                     level_id = dRow1.level_id
#                     level_name = dRow1.level_name
#
#                     dictData = {'area_id': level_id, 'area_name': level_name}
#                     level_area_list.append(dictData)
#
#             elif level_depth_no==2:
#                 level3Rows = db((db.sm_level.cid == c_id) & (db.sm_level.level2.belongs(sup_level_id_list)) & (db.sm_level.depth == 3)).select(db.sm_level.level_id,db.sm_level.level_name, orderby=db.sm_level.level_id,groupby=db.sm_level.level_id)
#
#                 for dRow1 in level3Rows:
#                     level_id = dRow1.level_id
#                     level_name = dRow1.level_name
#
#                     dictData = {'area_id': level_id, 'area_name': level_name}
#                     level_area_list.append(dictData)
#
#             session.level_area_list=level_area_list
#
#             redirect(URL(c='ppm_mark_mobile',f='home'))
#
#     return dict()
#
#
#
#
#
#
# def rep_list():
#     if session.cid=='' or session.cid==None:
#         redirect(URL(c='ppm_mark_mobile',f='index'))
#
#
#     repRows=db((db.sm_rep_area.cid == session.cid) & (db.sm_rep_area.area_id==session.area_id)).select(db.sm_rep_area.rep_id,db.sm_rep_area.rep_name,db.sm_rep_area.rep_category,orderby=db.sm_rep_area.rep_name)
#     repListStr=''
#     for row in repRows:
#         rep_name=row.rep_name
#         rep_id = row.rep_id
#
#         if repListStr=='':
#             repListStr=rep_name+'|'+rep_id
#         else:
#             repListStr +='<rd>'+rep_name + '|' + rep_id
#
#     return repListStr
#
#
# def rep():
#     if session.cid=='' or session.cid==None:
#         redirect(URL(c='ppm_mark_mobile',f='index'))
#
#
#
#     return dict()
#
#
# def ppm_list():
#     if session.cid=='' or session.cid==None:
#         redirect(URL(c='ppm_mark_mobile',f='index'))
#
#     ppmRows=db((db.sm_doctor_ppm.cid == session.cid)& (db.sm_doctor_ppm.status =='ACTIVE')).select(db.sm_doctor_ppm.gift_id,db.sm_doctor_ppm.gift_name,db.sm_doctor_ppm.item_brand,db.sm_doctor_ppm.item_price,orderby=db.sm_doctor_ppm.gift_name)
#
#     ppmListStr = ''
#     for row in ppmRows:
#         gift_id = str(row.gift_id)
#         gift_name = str(row.gift_name)
#         item_brand = str(row.item_brand)
#         item_price = str(row.item_price)
#
#         if ppmListStr == '':
#             ppmListStr = gift_name + '|' +gift_id+ '|' + item_brand+ '|' + item_price
#         else:
#             ppmListStr += '<rd>' + gift_name + '|' +gift_id+ '|' + item_brand+ '|' + item_price
#
#     return ppmListStr
#
#
# def ppm():
#     if session.cid=='' or session.cid==None:
#         redirect(URL(c='ppm_mark_mobile',f='index'))
#
#     rep_id = request.vars.repId
#     rep_name = request.vars.repName
#
#
#     return dict(rep_id=rep_id,rep_name=rep_name)
#
# def ppm_submit():
#     if session.cid=='' or session.cid==None:
#         redirect(URL(c='ppm_mark_mobile',f='index'))
#
#     rep_id = request.vars.repId
#
#     submitItem=request.vars.submitItem
#
#     emp_id=''
#     emp_name = ''
#     level_id = ''
#     level_name = ''
#
#     supLevelRows = db((db.sm_supervisor_level.cid == session.cid) & (db.sm_supervisor_level.sup_id == session.rep_id)).select(db.sm_supervisor_level.sup_id,db.sm_supervisor_level.sup_name,db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_name,limitby=(0,1))
#
#     if supLevelRows:
#         emp_id = supLevelRows[0].sup_id
#         emp_name = supLevelRows[0].sup_name
#         level_id = supLevelRows[0].level_id
#         level_name = supLevelRows[0].level_name
#
#         repAreaRows = db((db.sm_rep_area.cid == session.cid)&(db.sm_rep_area.area_id == session.area_id) & (db.sm_rep_area.rep_id == rep_id) ).select(db.sm_rep_area.rep_id, db.sm_rep_area.rep_name,db.sm_rep_area.area_id, db.sm_rep_area.area_name,limitby=(0, 1))
#         sqlInsert=''
#         rep_name=''
#         if repAreaRows:
#             rep_id = repAreaRows[0].rep_id
#             rep_name = repAreaRows[0].rep_name
#             rep_area_id = repAreaRows[0].area_id
#
#             item_arr = submitItem.split('||')
#             sqlInsert=''
#             for i in range(len(item_arr)):
#                 itemStr=item_arr[i].split('|')
#                 item_id=itemStr[0]
#                 item_value = itemStr[1]
#
#                 try:
#                     item_value=int(item_value)
#                     if item_value<0 or item_value>10:
#                         item_value=0
#                 except:
#                     item_value=0
#
#                 if item_value==0:continue
#
#                 ppmRows = db((db.sm_doctor_ppm.cid == session.cid)&(db.sm_doctor_ppm.gift_id == item_id)).select(db.sm_doctor_ppm.gift_id,db.sm_doctor_ppm.gift_name,db.sm_doctor_ppm.item_brand,db.sm_doctor_ppm.item_price,limitby=(0,1))
#
#                 if ppmRows:
#                     gift_id=ppmRows[0].gift_id
#                     gift_name = ppmRows[0].gift_name
#                     item_brand = ppmRows[0].item_brand
#                     item_price = ppmRows[0].item_price
#
#                     sqlInsert = db.sm_ppm_mark_details.insert(emp_id=emp_id,emp_name=emp_name,level_id=level_id,level_name=level_name,rep_id=rep_id,rep_name=rep_name,rep_area=rep_area_id,ppm_id=gift_id,ppm_name=gift_name,item_brand=item_brand,item_price=item_price,item_value=item_value)
#
#         if sqlInsert:
#             session.flash='Submitted Successfullly ('+rep_name+'|'+rep_id+')'
#             redirect(URL(c='ppm_mark_mobile', f='rep'))
#
#
#     return dict(rep_id=rep_id,rep_name=rep_name)
#
#
# def ppm_history():
#     if session.cid=='' or session.cid==None:
#         redirect(URL(c='ppm_mark_mobile',f='index'))
#
#     rep_id = request.vars.repId
#     rep_name = request.vars.repName
#
#     records=db((db.sm_ppm_mark_details.cid == session.cid)&(db.sm_ppm_mark_details.emp_id == session.rep_id)&(db.sm_ppm_mark_details.rep_id == rep_id)).select(db.sm_ppm_mark_details.submit_date,db.sm_ppm_mark_details.ppm_id,db.sm_ppm_mark_details.ppm_name,db.sm_ppm_mark_details.item_brand,db.sm_ppm_mark_details.item_price,db.sm_ppm_mark_details.item_value,orderby=~db.sm_ppm_mark_details.id,limitby=(0,30))
#
#     return dict(records=records,rep_id=rep_id,rep_name=rep_name)





