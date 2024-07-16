#area
# http://127.0.0.1:8000/hamdard_api/area/area_list?cid=HAMDARD&user_id=ITMSO&user_pass=1234

def index():
    return 'Welcome to mReporting.'

def area_list():
    cid = request.vars.cid
    user_id = request.vars.user_id
    password = request.vars.user_pass
    res_data=''

    if cid==None:
        cid=''
    if user_id==None:
        user_id=''
    if password==None:
        password=''

    if cid=='' or user_id=='' or password=='':
        res_data = {'status': 'Failed', 'ret_str': 'Required All'}
    else:
        userRecords = 'select rep_id,name,user_type from sm_rep where cid="' + cid + '" and rep_id="' + user_id + '" and password="' + password + '" and status="ACTIVE" limit 0,1;'
        userRecords = db.executesql(userRecords, as_dict=True)

        if len(userRecords) == 0:
            res_data = {'status': 'Failed', 'ret_str': 'Invalid/Inactive User'}
        else:
            for rRow in range(len(userRecords)):
                userRecordsStr = userRecords[rRow]
                user_type = str(userRecordsStr['user_type'])

                area_list = []
                level_id_list = []
                if user_type == 'rep':
                    userAreaRecords = 'select area_id,area_name from sm_rep_area where cid="' + cid + '" and rep_id="' + user_id + '";'
                    userAreaRecords = db.executesql(userAreaRecords, as_dict=True)
                    for i in range(len(userAreaRecords)):
                        userAreaRecordsStr = userAreaRecords[i]
                        area_id = str(userAreaRecordsStr['area_id'])
                        area_name = str(userAreaRecordsStr['area_name'])
                        dict_data1 = {'area_id': area_id, 'area_name': area_name}
                        area_list.append(dict_data1)
                else:
                    userLevelRecords = 'select sup_id,sup_name,level_id,level_depth_no from sm_supervisor_level where cid="' + cid + '" and sup_id="' + user_id + '" ;'
                    userLevelRecords = db.executesql(userLevelRecords, as_dict=True)
                    for i in range(len(userLevelRecords)):
                        userLevelRecordsStr = userLevelRecords[i]
                        level_id = str(userLevelRecordsStr['level_id'])
                        level_depth_no = str(userLevelRecordsStr['level_depth_no'])

                        level_id_list.append(level_id)

                    level_id_str = str(level_id_list).replace('[', '').replace(']', '')

                    condition = 'cid="' + cid + '" and is_leaf=1'
                    if int(level_depth_no) == 0:
                        if len(level_id_list) > 0:
                            condition += ' and level0 in (' + level_id_str + ') '
                    elif int(level_depth_no) == 1:
                        if len(level_id_list) > 0:
                            condition += ' and level1 in (' + level_id_str + ') '
                    elif int(level_depth_no) == 2:
                        if len(level_id_list) > 0:
                            condition += ' and level2 in (' + level_id_str + ') '

                    levelRecords = 'select level_id,level_name from sm_level where ' + condition + ' ;'
                    levelRecords = db.executesql(levelRecords, as_dict=True)
                    for j in range(len(levelRecords)):
                        levelRecordsStr = levelRecords[j]
                        area_id = str(levelRecordsStr['level_id'])
                        area_name = str(levelRecordsStr['level_name'])
                        dict_data1 = {'area_id': area_id, 'area_name': area_name}
                        area_list.append(dict_data1)

            res_data = {'status': 'Success', 'area_list': area_list}


    data=response.json(res_data)

    return data