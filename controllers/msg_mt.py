

# http://127.0.0.1:8000/dwokapia/syncmobile/submitData?from=8801719078552&message=warranty 12345678912345&message_id=111222542154&sent_to=8801713454218&secret=abc321&sent_timestamp=2014-05-15 17:07:10
#http://e.businesssolutionapps.com/dwokapia/syncmobile/submitData

# http://w05.yeapps.com/inbox/msg_mt/msg_mt?user_id=marico101&secret=testlkjjiljdsfill123hls&sent_to=8801711274122&email=nadira.nuri@gmail.com&msg=sms
# sender_mobileno= &email= &sent_to= &msg= &secret=asdfioo234234klmkn2
# import urllib.parse
import datetime

import urllib.request
from random import randint


def send_otp():
    import urllib.parse
    import urllib
    from datetime import date
    from datetime import datetime, timedelta
    randNumber = randint(1001, 9999)
    # return randNumber
    cid=str(request.vars['cid']).strip().upper()
    rep_id=str(request.vars['rep_id']).strip().upper()
    msg_send=str(randNumber)
    msg_send_show='YourPassword:'+str(randNumber)
    # return msg_send_show
    checkRows=db((db.sm_rep.cid==cid) & (db.sm_rep.rep_id==rep_id) & (db.sm_rep.status=='ACTIVE') ).select(db.sm_rep.mobile_no,db.sm_rep.user_type,limitby=(0,1))
    if checkRows:
        to_mobile=checkRows[0].mobile_no
        user_type=checkRows[0].user_type
    else:
        to_mobile='0'

    if str(to_mobile)!='0':
        # return 'http://portal.metrotel.com.bd/smsapi?api_key=R20000995f4d2930168889.87462470&type=unicode&contacts='+str(to_mobile)+'&senderid=8809612992200&msg='+str(msg_send_show)+'&unicode=1'
        updateRows=db((db.sm_rep.cid==cid) & (db.sm_rep.rep_id==rep_id) & (db.sm_rep.status=='ACTIVE') ).update(password=msg_send)
        # response = urllib2.urlopen('http://portal.metrotel.com.bd/smsapi?api_key=R20000995f4d2930168889.87462470&type=unicode&contacts='+str(to_mobile)+'&senderid=8809612992200&msg='+str(msg_send_show)+'&unicode=1')
        # url='http://portal.metrotel.com.bd/smsapi?api_key=R20000995f4d2930168889.87462470&type=unicode&contacts='+str(to_mobile)+'&senderid=8809612992200&msg='+str(msg_send_show)+'&unicode=1'
        # return url
        # response = fetch(url)
        # return_sms='2323'

        # url = 'http://portal.metrotel.com.bd/smsapi?api_key=R20000995f4d2930168889.87462470&type=unicode&contacts='+str(to_mobile)+'&senderid=8809612992200&msg='+str(msg_send_show)+'&unicode=1'
        
        s_key = "b71bcbcb93c36732125d46e9ab873ec110457fef"
        url = f"https://api.rtcom.xyz/onetomany?acode=30000077&api_key={s_key}&senderid=8809617612719&type=text&msg={msg_send_show}&contacts={to_mobile}&transactionType=T&contentID="
            
       
        # with urllib.request.urlopen(msg_send_url) as msg_response:
        #     result = msg_response.read()
        #     return result


        # url = 'http://portal.metrotel.com.bd/smsapi?api_key=R20000995f4d2930168889.87462470&type=unicode&contacts='+str(to_mobile)+'&senderid=8809612992200&msg='+str(return_sms)+'&unicode=1'

        # response=urllib.request.urlopen(url)

        response = fetch(url)
   
    retStr='{"payload":{"success":"true","error":"null"}}'

    session.flash = 'OTP Sent'
    if user_type=='rep':
        redirect(URL(c='representative', f='rep'))
    if user_type=='sup':
        redirect(URL(c='representative', f='supervisor_create'))
   
    # return retStr


