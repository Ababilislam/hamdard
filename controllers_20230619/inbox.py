

def inbox():
    #Check access permission
    task_id='rm_inbox_manage'
    task_id_view='rm_inbox_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (task_id_view==False):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))   
    
    response.title='Inbox'
    #---------------
    c_id=session.cid
    
    #======================
    #------------------------
    btn_filter_inbox=request.vars.btn_filter
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    if btn_filter_inbox:
        session.btn_filter_inbox=btn_filter_inbox
        session.search_type_inbox=request.vars.search_type
        session.search_value_inbox=str(request.vars.search_value).strip()
        
        if (session.search_type_inbox=='Date'):
            try:
                inboxFromDt=datetime.datetime.strptime(str(session.search_value_inbox)[0:10],'%Y-%m-%d')
                inboxToDt=inboxFromDt+datetime.timedelta(days=1)
                
                session.inboxFromDt=inboxFromDt
                session.inboxToDt=inboxToDt
            except:
                session.inboxFromDt=''
                session.inboxToDt=''
            
        reqPage=0
        
    elif btn_all:
        session.btn_filter_inbox=None
        session.search_type_inbox=None
        session.search_value_inbox=None
        session.inboxFromDt=None
        session.inboxToDt=None
        
        reqPage=0
    
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging    

    # Set text for filter
    
    qset=db()
    qset=qset(db.sm_inbox.cid==c_id)
    
    if (session.btn_filter_inbox):
        if (session.search_type_inbox=='MobileNo'):
            qset=qset(db.sm_inbox.mobile_no==session.search_value_inbox)
            
        elif (session.search_type_inbox=='Status'):
            qset=qset(db.sm_inbox.status==str(session.search_value_inbox).strip().upper())
        
        elif (session.search_type_inbox=='Date'):
            qset=qset((db.sm_inbox.sms_date>=session.inboxFromDt)&(db.sm_inbox.sms_date<session.inboxToDt))
        
        
    records=qset.select(db.sm_inbox.ALL,orderby=~db.sm_inbox.sl,limitby=limitby)
    
    
    #---------------- filter end
    return dict(records=records,page=page,items_per_page=items_per_page,access_permission=access_permission)
    
    #---------------end
    
def error_process():
    import urllib
    
    task_id='rm_inbox_manage'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied !'
        redirect (URL('inbox','inbox'))
    
    if session.error_process_flag!='YES':
        session.flash='Access is Denied'
        redirect (URL('inbox','inbox'))
    
    response.title='Error Process'
    
    #======================
    c_id=session.cid
    
    page=int(request.args[0])
    rowId=int(request.args[1])
    
    smspath=''
    settRow=db((db.sm_settings.cid==c_id)&(db.sm_settings.s_key=='SMS_PATH')).select(db.sm_settings.s_value,limitby=(0,1))
    if not settRow:
        session.flash='Settings needed for error sms'
        redirect (URL('inbox','inbox'))
    else:
        smspath=str(settRow[0].s_value)
    
    #-------
    hostName=request.env.http_host
    appName=request.application
    baseUrl='http://'+str(hostName)+'/'+str(appName)+'/'+smspath
    #-----
    
    btn_resubmit=request.vars.btn_resubmit
    if btn_resubmit:
        smsMobile=request.vars.smsMobile
        smsText=request.vars.smsText
        
        urlPath=str(baseUrl) + '&mob='+str(smsMobile)+'&cid='+str(c_id)+'&msg=.'+str(smsText)
        
        #return urlPath
        
        urlRes = urllib.urlopen(urlPath).read()
        
        if urlRes!='':
            updateRes=db((db.sm_inbox.cid==c_id)  & (db.sm_inbox.id==rowId)  & (db.sm_inbox.status=='ERROR')).update(field2=1)
            
            session.flash=urlRes[5:]
            redirect (URL('inbox','inbox'))
        
#        if urlRes!='':
#            retRes=str(urlRes)[5:]
    
    #field2 is used for already processed or not
    records=db((db.sm_inbox.cid==c_id)  & (db.sm_inbox.id==rowId)  & (db.sm_inbox.status=='ERROR') & (db.sm_inbox.field2==0)).select(db.sm_inbox.ALL,limitby=(0,1))
    
    return dict(records=records,page=page,rowId=rowId)
    #---------------


def test():    
    return 'request.url:'+str(request.url)+'; request.env.http_host:'+str(request.env.http_host)+'; request.env.server_name:'+str(request.env.server_name)
    
#    request.url    
#    request.env.path_info
    
#    return request.env.http_host
    
    #request.env.remote_addr    
    #request.env.http_referer
    #request.env.server_name
    #request.env.server_port
