import urllib2;

# http://127.0.0.1:8000/hamdard/url_sample_gift_ppm/home?cid=hamdard&rep_id=5172&password=1234 

def sample_gift_ppm():    
        redirect(URL(c='url_sample_gift_ppm',f='home')) 


 
def home():   
    cid = str(request.vars.cid).strip().upper()
    rep_id=str(request.vars.rep_id).strip().upper() 
    password=str(request.vars.rep_pass).strip()
    session.cid=cid

     
    checkRep=  db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id)  & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.password,limitby=(0, 1))
    
    if not checkRep:
        response.flash='Invalid User'
        return dict(cid=cid,rep_id=rep_id,password=password)

    else:  
        return dict(cid=cid,rep_id=rep_id,password=password)



 
def get_sample():  
    cid = str(request.vars.cid).strip().upper()
    rep_id=str(request.vars.rep_id).strip().upper() 
    password=str(request.vars.rep_pass).strip()
    items_per_page=0

    btn_filter_sample = request.vars.btn_filter_sample
    btn_all_sample = request.vars.btn_all_sample 
    reqPage = len(request.args)
    if btn_filter_sample:
        session.btn_filter_sample = btn_filter_sample 
        session.sampleId = str(request.vars.sampleId).strip().upper()
        reqPage = 0
    elif btn_all_sample:
        session.btn_filter_sample = None 
        session.sampleId = None
        reqPage = 0

    #--------paging
    if reqPage:
        page = int(request.args[0])
    else:
        page = 0
    # items_per_page = session.items_per_page
    # limitby = (page * items_per_page, (page + 1) * items_per_page + 1)

    checkRep=  db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id)  & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.password,limitby=(0, 1))
    get_sampleStr=''
    if not checkRep:
        response.flash='Invalid User'
        return dict(cid=cid,rep_id=rep_id,password=password,get_sampleStr=get_sampleStr,items_per_page=items_per_page,page=page)
    else: 
        
        qset=db()
        qset=qset(db.sm_doctor_sample.cid==cid)
        qset=qset(db.sm_doctor_sample.status=='ACTIVE')


        
        if (session.btn_filter_sample):
            searchValue=str(session.sampleId).split('|')[0]        
            qset=qset(db.sm_doctor_sample.item_id==searchValue.upper())
        
        get_sampleStr=qset.select(db.sm_doctor_sample.item_id,db.sm_doctor_sample.name,groupby=db.sm_doctor_sample.item_id,orderby=db.sm_doctor_sample.name)
        # return get_sampleStr
        
    return dict(cid=cid,rep_id=rep_id,password=password,get_sampleStr=get_sampleStr,items_per_page=items_per_page,page=page)



 
def get_gift():  
    cid = str(request.vars.cid).strip().upper()
    rep_id=str(request.vars.rep_id).strip().upper() 
    password=str(request.vars.rep_pass).strip()
    items_per_page=0

    btn_filter_gift = request.vars.btn_filter
    btn_all = request.vars.btn_filter_all
    reqPage = len(request.args)
    if btn_filter_gift:
        session.btn_filter_gift = btn_filter_gift
        session.searchType_gift = str(request.vars.search_type).strip()
        session.searchValue_gift = str(request.vars.search_value).strip().upper()
        reqPage = 0
    elif btn_all:
        session.btn_filter_gift = None
        session.searchType_gift = None
        session.searchValue_gift = None
        reqPage = 0

    #--------paging
    if reqPage:
        page = int(request.args[0])
    else:
        page = 0
    # items_per_page = session.items_per_page
    # limitby = (page * items_per_page, (page + 1) * items_per_page + 1)

    checkRep=  db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id)  & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.password,limitby=(0, 1))
    get_giftStr=''
    if not checkRep:
        response.flash='Invalid User'
        return dict(cid=cid,rep_id=rep_id,password=password,get_giftStr=get_giftStr,items_per_page=items_per_page,page=page)
    else: 
     
        qset=db()
        qset=qset(db.sm_doctor_gift.cid==cid)
        qset=qset(db.sm_doctor_gift.status=='ACTIVE')


        
        if (session.btn_filter_sample):
            searchValue=str(session.sampleId).split('|')[0]        
            qset=qset(db.sm_doctor_gift.gift_id==searchValue.upper())

        get_giftStr=db((db.sm_doctor_gift.cid==cid) & (db.sm_doctor_gift.status=='ACTIVE')).select(db.sm_doctor_gift.gift_id,db.sm_doctor_gift.gift_name,orderby=db.sm_doctor_gift.gift_name)
        # return get_giftStr
        
    return dict(cid=cid,rep_id=rep_id,password=password,get_giftStr=get_giftStr,items_per_page=items_per_page,page=page)



 
def get_ppm():  
    cid = str(request.vars.cid).strip().upper()
    rep_id=str(request.vars.rep_id).strip().upper() 
    password=str(request.vars.rep_pass).strip()
    items_per_page=0

    btn_filter_ppm = request.vars.btn_filter
    btn_all = request.vars.btn_filter_all
    reqPage = len(request.args)
    if btn_filter_ppm:
        session.btn_filter_ppm = btn_filter_ppm
        session.searchType_ppm = str(request.vars.search_type).strip()
        session.searchValue_ppm = str(request.vars.search_value).strip().upper()
        reqPage = 0
    elif btn_all:
        session.btn_filter_ppm = None
        session.searchType_ppm = None
        session.searchValue_ppm = None
        reqPage = 0

    #--------paging
    if reqPage:
        page = int(request.args[0])
    else:
        page = 0
    # items_per_page = session.items_per_page
    # limitby = (page * items_per_page, (page + 1) * items_per_page + 1)

    checkRep=  db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id)  & (db.sm_rep.password == password) & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.password,limitby=(0, 1))
    get_ppmStr=''
    if not checkRep:
        response.flash='Invalid User'
        return dict(cid=cid,rep_id=rep_id,password=password,get_ppmStr=get_ppmStr,items_per_page=items_per_page,page=page)
    else: 
        
        qset=db()
        qset=qset(db.sm_doctor_ppm.cid==cid)
        qset=qset(db.sm_doctor_ppm.status=='ACTIVE')


        
        if (session.btn_filter_sample):
            searchValue=str(session.sampleId).split('|')[0]        
            qset=qset(db.sm_doctor_ppm.gift_id==searchValue.upper())
        get_ppmStr=db((db.sm_doctor_ppm.cid==cid) & (db.sm_doctor_ppm.status=='ACTIVE')).select(db.sm_doctor_ppm.gift_id,db.sm_doctor_ppm.gift_name,orderby=db.sm_doctor_ppm.gift_name)
        # return get_ppmStr
        
    return dict(cid=cid,rep_id=rep_id,password=password,get_ppmStr=get_ppmStr,items_per_page=items_per_page,page=page)





def search_sample():
    lvlStr = ''
    cid = session.cid

    rows = db((db.sm_doctor_sample.cid == cid)).select(db.sm_doctor_sample.item_id, db.sm_doctor_sample.name, groupby=db.sm_doctor_sample.item_id ,orderby=db.sm_doctor_sample.name)
    for row in rows:
        item_id = str(row.item_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')
        
        if lvlStr == '':
            lvlStr = item_id + '|' + name 
        else:
            lvlStr += ',' + item_id + '|' +  name 
            
    return lvlStr


def search_gift():
    lvlStr = ''
    cid = session.cid

    rows = db((db.sm_doctor_gift.cid == cid)).select(db.sm_doctor_gift.gift_id, db.sm_doctor_gift.gift_name, groupby=db.sm_doctor_gift.gift_id ,orderby=db.sm_doctor_gift.gift_name)
    for row in rows:
        gift_id = str(row.gift_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')
        
        if lvlStr == '':
            lvlStr = gift_id + '|' + name 
        else:
            lvlStr += ',' + gift_id + '|' +  name 
            
    return lvlStr


def search_ppm():
    lvlStr = ''
    cid = session.cid

    rows = db((db.sm_doctor_ppm.cid == cid)).select(db.sm_doctor_ppm.gift_id, db.sm_doctor_ppm.gift_name, groupby=db.sm_doctor_ppm.gift_id ,orderby=db.sm_doctor_ppm.gift_name)
    for row in rows:
        gift_id = str(row.gift_id)
        name = str(row.name).replace('|', ' ').replace(',', ' ')
        
        if lvlStr == '':
            lvlStr = gift_id + '|' + name 
        else:
            lvlStr += ',' + gift_id + '|' +  name 
            
    return lvlStr



 