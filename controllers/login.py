#login_API
# http://127.0.0.1:8000/hamdard_api/login/check_user?cid=HAMDARD&user_id=ITMSO&user_pass=1234

def index():
    return 'Welcome to mReporting.'

def check_user():
    cid = request.vars.cid
    user_id = request.vars.user_id
    password = request.vars.user_pass

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
            res_data={'status': 'Failed', 'ret_str': 'Invalid/Inactive User'}
        else:
            user_name = ''
            area_page = False
            for rRow in range(len(userRecords)):
                userRecordsStr = userRecords[rRow]
                user_name = str(userRecordsStr['name'])
                user_type = str(userRecordsStr['user_type'])

                if user_type == 'sup':
                    userLevelRecords = 'select id from sm_supervisor_level where cid="' + cid + '" and sup_id="' + user_id + '" and (level_depth_no=0 or level_depth_no=1);'
                    userLevelRecords = db.executesql(userLevelRecords, as_dict=True)
                    if len(userLevelRecords) > 0:
                        area_page = True

            res_data = {'status': 'Success', 'user_id': user_id, 'user_name': user_name, 'area_page': area_page}

    data=response.json(res_data)

    return data