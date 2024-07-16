#login_API
# cid=HAMDARD&user_id=ITMSO&user_pass=1234&client_id=&delivery_date=2022-06-22&delivery_time=MORNING&pay_mode=CASH&item_list=1002|5||1003|6
# http://127.0.0.1:8000/hamdard_api/order_submit/submit_data
def index():
    return 'Welcome to mReporting.'

def submit_data():
    if request.env.request_method != 'POST': raise HTTP(403)

    cid = request.vars.cid
    user_id = request.vars.user_id
    password = request.vars.user_pass
    client_id = request.vars.client_id
    delivery_date = request.vars.delivery_date
    delivery_time = request.vars.delivery_time
    pay_mode = request.vars.pay_mode
    item_list = request.vars.item_list

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
            submitStr=str(cid)+','+str(user_id)+','+str(client_id)+','+str(delivery_date)+','+str(delivery_time)+','+str(pay_mode)+','+str(item_list)
            res_data = {'status': 'Success','submitStr':submitStr}

    data=response.json(res_data)

    return data