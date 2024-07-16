
#mpo
#http://127.0.0.1:8000/hamdard/score_card_mobile/index?cid=Hamdard&rep_id=it03&rep_pass=1234


def index():
    c_id = request.vars.cid
    rep_id = request.vars.rep_id
    rep_pass = request.vars.rep_pass

    # ---------------------- rep check
    userRecords='select cid,rep_id,name,user_type from sm_rep where cid="'+c_id+'" and rep_id="'+rep_id+'" and password="'+rep_pass+'" and status="ACTIVE" limit 0,1;'
    userRecords=db.executesql(userRecords,as_dict=True)
    
    if len(userRecords)==0:
        response.flash = 'Invalid/Inactive Supervisor'
    else:
        for i in range(len(userRecords)):
            userRecordsS=userRecords[i]
            
            cid=userRecordsS['cid'] 
            rep_id = str(userRecordsS['rep_id'])
            name = str(userRecordsS['name'])
            user_type = str(userRecordsS['user_type'])

            level3_id_str=''
            level_depth_no=''
            level_id=''
            if user_type == 'rep':
                userRecords = 'select area_id from sm_rep_area where cid="' + c_id + '" and rep_id="' + rep_id + '";'
                userRecords = db.executesql(userRecords, as_dict=True)

                if len(userRecords) == 0:
                    response.flash = 'Invalid Territory'
                else:
                    level3_id_list=[]
                    for i in range(len(userRecords)):
                        userRecordsS = userRecords[i]

                        area_id = str(userRecordsS['area_id'])
                        level3_id_list.append(area_id)

                    if len(level3_id_list) > 0:
                        level3_id_str = str(level3_id_list).replace('[', '').replace(']', '')


            else:
                userRecords = 'select level_depth_no,level_id from sm_supervisor_level where cid="' + c_id + '" and sup_id="' + rep_id + '" limit 0,1;'
                userRecords = db.executesql(userRecords, as_dict=True)

                if len(userRecords) == 0:
                    response.flash = 'Invalid Level'
                else:
                    for i in range(len(userRecords)):
                        userRecordsS = userRecords[i]

                        level_depth_no = userRecordsS['level_depth_no']
                        level_id = str(userRecordsS['level_id'])




            session.cid = c_id
            session.user_id = rep_id
            session.user_type = user_type
            session.level3_id_str = level3_id_str
            session.level_depth_no = level_depth_no
            session.level_id = level_id

            redirect(URL('home', vars=dict()))

    return dict()

def home():
    c_id = session.cid
    rep_id=str(session.user_id)

    btn_report = request.vars.btn_report

    if btn_report:
        from_date = request.vars.from_date
        to_date = request.vars.to_date
        session.from_date = from_date
        session.to_date = to_date

        # dateFlag = True
        # try:
        #     from_dt2 = datetime.datetime.strptime(str(from_date), '%Y-%m-%d')
        #     to_dt2 = datetime.datetime.strptime(str(to_date), '%Y-%m-%d')
        #     if from_date > to_dt2:
        #         dateFlag = False
        # except:
        #     dateFlag = False
        #
        # if dateFlag == False:
        #     response.flash = "Invalid Date Range"
        # else:
        #     dateDiff = (to_dt2 - from_dt2).days
        #     if dateDiff > 1:
        #         response.flash = "Single days allowed between Date Range"
        #     else:
        #         session.from_date = from_date
        #         session.to_date = to_date



    records = ''
    condition=' cid="' + c_id + '"'

    if session.from_date!=None and session.to_date!=None:
        condition += ' and submit_date>="' + session.from_date + '" and  submit_date<="' + session.to_date + '" '

    if session.user_type == 'rep':
        if session.level3_id_str!='':
            condition += ' and level3_id in (' + session.level3_id_str + ') '
    else:
        if session.level_depth_no == 0:
            condition += ' and level0_id="' + session.level_id + '" '
        elif session.level_depth_no == 1:
            condition += ' and level1_id="' + session.level_id + '" '
        elif session.level_depth_no == 2:
            condition += ' and level2_id="' + session.level_id + '" '




    records = 'select level0_id,level1_id,level2_id,level3_id,rep_id,rep_name,sum(ach) as ach,sum(pd_knowledge) as pd_knowledge,sum(rx_pres_share) as rx_pres_share,sum(pcpm) as pcpm,sum(four_p) as four_p,sum(reject_count) as reject_count,sum(facetime) as facetime,sum(walk_step_act_score) as walk_step_act_score,sum(overall_rate) as overall_rate from sm_score_card_details where ' + condition + ' group by level0_id,level1_id,level2_id,level3_id,rep_id;'
    records = db.executesql(records, as_dict=True)

    level_area_list=[]

    return dict(level_area_list=level_area_list,records=records)


def rep_details():
    c_id = session.cid
    rep_id=str(request.vars.rep_id)


    records = ''
    condition=' cid="' + c_id + '"'
    condition += ' and rep_id="' + rep_id + '" '

    if session.from_date!=None and session.to_date!=None:
        condition += ' and submit_date>="' + session.from_date + '" and  submit_date<="' + session.to_date + '" '


    records = 'select level0_id,level1_id,level2_id,level3_id,rep_id,rep_name,sum(ach) as ach,sum(pd_knowledge) as pd_knowledge,sum(rx_pres_share) as rx_pres_share,sum(pcpm) as pcpm,sum(four_p) as four_p,sum(reject_count) as reject_count,sum(facetime) as facetime,sum(walk_step_act_score) as walk_step_act_score,sum(overall_rate) as overall_rate from sm_score_card_details where ' + condition + ' group by level0_id,level1_id,level2_id,level3_id,rep_id;'
    records = db.executesql(records, as_dict=True)



    return dict(records=records)

