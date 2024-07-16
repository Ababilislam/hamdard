#index
#log_out
#check_super_admin
#home
#sys_web_settings
#update_sys_web_settings
#sys_comp_mobile
#update_sys_comp_mobile
#sys_mobile_settings
#update_sys_mobile_settings
#sys_depot_device_settings
#update_sys_depot_device_settings
#sys_super_settings
#update_sys_super_settings
#sys_company_settings
#update_sys_company_settings
#web_settings_batch_upload
#mobile_settings_batch_upload
#company_mobile_batch_upload
#sys_data_clean

import urllib2
#from google.tools import fetch

#============================Logout
def log_out():
    session.clear()
    if ((session.super_cid == None) or (session.uid == None)):
        redirect(URL(c='super',f='index'))
    else:
        redirect(URL(c='super',f='home'))
    
    return dict()

#=============================== Login
def index():
    session.clear()
    #----------
    response.title='Super-login'
    #----------
    return dict(message="Login-Super Admin")


#---------------------
def check_super_admin():    
    btn_login=request.vars.btn_login    
    if btn_login:
        c_id=request.vars.cid.strip().upper()
        user_id=request.vars.user_id.strip().upper()
        password=request.vars.password.strip()
        
        if not(c_id=='' or user_id==''or password==''):            
            #Submit to cpanel
            userText=str(c_id).strip()+'<url>'+str(user_id).strip()+'<url>'+str(password).strip()
            
            request_text=urllib2.quote(userText)
            #url = 'http://www.businesssolutionapps.appspot.com/cpanel/default/module_super_login?login_data='+request_text
            #url = 'http://127.0.0.1:8000/cpanel/default/module_super_login?login_data='+request_text
            url = 'http://e.businesssolutionapps.com/cpanel/default/module_super_login?login_data='+request_text
            
            try:
                result= fetch(url)
            except:
                session.flash='Connection Time out. Please try again after few minutes.'
                redirect(URL(c='super',f='index'))
            
            
            if (str(result).find('START')==(-1) or str(result).find('END')==(-1)):
                session.flash='Communication error'
            else:
                encResult=str(result)[5:-3]
            
                if encResult=='success':        
                    session.cid=c_id
                    session.super_id=user_id
                    
                    redirect(URL(c='super',f='home'))
                    
                else:
                    session.flash='Invalid Authorization'
        else:
            session.flash = 'All fields must be required !'
             
    redirect(URL(c='super',f='index'))
#    
#    #---------------------
#
#
##============================================= Check Super USER

#def check_super_admin():
#    c_id=request.vars.cid.strip().upper() #new
#    user_id=request.vars.user_id.strip().upper()
#    password=request.vars.password.strip()
#
##    rows=db((db.sm_settings.cid=='SUPER')&(db.sm_settings.s_key==user_id)&(db.sm_settings.s_value==password)).select(db.sm_settings.ALL)
#    
#    rows=False
#    if (user_id=='SUPER'and password=='SUPER123'):
#        rows=True
#    
#    if rows:
##        for row in rows:
#        s_key='SUPER123'#row.s_key
#        
#        session.cid=c_id    #new
#        session.super_id=s_key
#
#        redirect(URL(c='super',f='home'))
#            
#    else:
#        session.flash = 'Invalid user'
#        redirect(URL(c='super',f='index'))


        
def home():#Home page with links
    if (session.super_id==None or session.super_id==''):
        redirect(URL(c='super',f='index'))
    
    #----------
    response.title='Super-Home'
    
    #----------
    btn_web_settings=request.vars.btn_web_settings
    btn_comp_mobile=request.vars.btn_comp_mobile
    btn_mobile_settings=request.vars.btn_mobile_settings
    
    btn_depot_device_settings=request.vars.btn_depot_device_settings
    
    btn_super_settings=request.vars.btn_super_settings
    btn_company_settings=request.vars.btn_company_settings
    btn_level_settings=request.vars.btn_level_settings
    
    btn_data_clean=request.vars.btn_data_clean    
    btn_object_data_clean=request.vars.btn_object_data_clean
    
    btn_logout=request.vars.btn_logout
    
    #---------------------
    if btn_web_settings:
        redirect(URL(c='super',f='sys_web_settings'))                
    elif btn_comp_mobile:
        redirect(URL(c='super',f='sys_comp_mobile'))
    elif btn_mobile_settings:
        redirect(URL(c='super',f='sys_mobile_settings'))
    
    elif btn_depot_device_settings:
        redirect(URL(c='super',f='sys_depot_device_settings'))

    #-------------
    elif btn_super_settings:
        redirect(URL(c='super',f='sys_super_settings'))
    elif btn_company_settings:
        redirect(URL(c='super',f='sys_company_settings'))
    elif btn_level_settings:
        redirect(URL(c='super',f='sys_level_settings'))
    
    #-----------------
    elif btn_data_clean:
        redirect(URL(c='super',f='sys_data_clean'))
    
    #-----------------
    elif btn_object_data_clean:
        redirect(URL(c='super',f='sys_object_data_clean'))
        
    #-------------
    elif btn_logout:
        redirect(URL(c='super',f='log_out'))
    else:
        return dict()


#==============================================================WEB SETTNGS
def sys_web_settings():  
    if (session.super_id==None or session.super_id==''):
        redirect(URL(c='super',f='index'))
    
    #----------
    response.title='Web Settings'
    #----------
    
    form=crud.create(db.sm_web_settings)    
    
    #---------------
    btn_filter_web_sett=request.vars.btn_filter_web_sett
    btn_filter_all=request.vars.btn_filter_all

    cid_value=str(request.vars.cid_value).strip()
    
    reqPage=len(request.args)
    
    if btn_filter_web_sett:
        session.btn_filter_web_sett=btn_filter_web_sett
        session.cid_value=cid_value
        reqPage=0
        
    elif btn_filter_all:
        session.btn_filter_web_sett=None
        session.cid_value=None
        reqPage=0
    
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging 
    
    #Set query based on filter
    qset=db()
    if (session.btn_filter_web_sett):
        if (session.cid_value!=''):
            qset=qset(db.sm_web_settings.cid==session.cid_value)            
        #----------------   
        records=qset.select(db.sm_web_settings.ALL,orderby=db.sm_web_settings.cid,limitby=limitby)
    else:
        records=qset.select(db.sm_web_settings.ALL,orderby=db.sm_web_settings.cid,limitby=limitby)  

    #------------------


    return dict(form=form,records=records,page=page,items_per_page=items_per_page)

def update_sys_web_settings():     
    if (session.super_id==None or session.super_id==''):
        redirect(URL(c='super',f='index'))
    
    #----------
    response.title='Web Settings-Edit'
    #----------
    
    page=request.args(0)
    form=crud.update(db.sm_web_settings, request.args(1))    
    
    return dict(form=form,page=page)


#==============================================================COMPANY MOBILE
def validation_sysCompMobile(form):       
    cid=str(request.vars.cid).strip().upper()
    mobile_no=str(request.vars.mobile_no).strip()
    compMobRows=db((db.sm_comp_mobile.cid == cid)&(db.sm_comp_mobile.mobile_no == mobile_no)).select(db.sm_comp_mobile.mobile_no,limitby=(0,1))
    if compMobRows:
        form.errors.mobile_no='already exist'
        
def sys_comp_mobile():
    if (session.super_id==None or session.super_id==''):
        redirect(URL(c='super',f='index'))
    
    #----------
    response.title='Company Mobile'
    #----------
    
    form=crud.create(db.sm_comp_mobile)    
    
    if form.accepts(request.vars, session,onvalidation=validation_sysCompMobile):
        response.flash = 'Submitted Successfully'      
        
    #---------------
    btn_filter_comp_mob=request.vars.btn_filter_comp_mob
    btn_filter_all=request.vars.btn_filter_all

    cid_value=str(request.vars.cid_value).strip()
    
    reqPage=len(request.args)
    
    if btn_filter_comp_mob:
        session.btn_filter_comp_mob=btn_filter_comp_mob
        session.cid_value=cid_value
        
        reqPage=0
        
    elif btn_filter_all:
        session.btn_filter_comp_mob=None
        session.cid_value=None
        
        reqPage=0
    
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=200
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging 
    
    #Set query based on search type
    qset=db()
    if (session.btn_filter_comp_mob):
        if (session.cid_value!=''):
            qset=qset(db.sm_comp_mobile.cid==session.cid_value)            
        
        #----------------  

        records=qset.select(db.sm_comp_mobile.ALL,orderby=db.sm_comp_mobile.mobile_no,limitby=limitby)
    else:
        records=qset.select(db.sm_comp_mobile.ALL,orderby=db.sm_comp_mobile.mobile_no,limitby=limitby)  

    #------------------
    return dict(form=form,records=records,page=page,items_per_page=items_per_page)

def validation_updateSysCompMobile(form): 
    rowid=str(request.vars.id)
    cid=str(request.vars.cid).strip().upper()
    mobile_no=str(request.vars.mobile_no).strip()
    
    compMobRows=db((db.sm_comp_mobile.cid == cid)&(db.sm_comp_mobile.mobile_no == mobile_no)&(db.sm_comp_mobile.id != rowid)).select(db.sm_comp_mobile.mobile_no,limitby=(0,1))
    if compMobRows:
        form.errors.mobile_no='already exist'
    
def update_sys_comp_mobile():     
    if (session.super_id==None or session.super_id==''):
        redirect(URL(c='super',f='index'))
    
    #----------
    response.title='Company Mobile-Edit'
    #----------
    
    page=request.args(0)
    form=crud.update(db.sm_comp_mobile, request.args(1))    
    
    if form.accepts(request.vars, session,onvalidation=validation_updateSysCompMobile):
        session.flash = 'Updated Successfully'   
        redirect(URL(f='sys_comp_mobile'))
        
    return dict(form=form,page=page)



#==============================================================MOBILE SETTINGS
def sys_mobile_settings():  
    if (session.super_id==None or session.super_id==''):
        redirect(URL(c='super',f='index'))

    #----------
    response.title='Mobile Settings'
    #----------
    
    form=crud.create(db.sm_mobile_settings)    

    #---------------
    btn_filter_mob_stt=request.vars.btn_filter_mob_stt
    btn_filter_all=request.vars.btn_filter_all
    
    cid_value=str(request.vars.cid_value).strip()
    type_value=str(request.vars.type_value).strip()
    
    reqPage=len(request.args)
    
    if btn_filter_mob_stt:
        session.btn_filter_mob_stt=btn_filter_mob_stt
        session.cid_value=cid_value
        session.type_value=type_value
        
        reqPage=0
        
    elif btn_filter_all:
        session.btn_filter_mob_stt=None
        session.cid_value=None
        session.type_value=None
        
        reqPage=0

    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging 
    
    #Set query based on search type
    qset=db()
    if (session.btn_filter_mob_stt):
        if (session.cid_value!=''):
            qset=qset(db.sm_mobile_settings.cid==session.cid_value)            
        #----------------  
        if (session.type_value!=''):
            qset=qset(db.sm_mobile_settings.type==session.type_value)            
        #----------------
         
        records=qset.select(db.sm_mobile_settings.ALL,orderby=db.sm_mobile_settings.cid,limitby=limitby)
    else:
        records=qset.select(db.sm_mobile_settings.ALL,orderby=db.sm_mobile_settings.cid,limitby=limitby)  

    #------------------
    
    return dict(form=form,records=records,page=page,items_per_page=items_per_page)


def update_sys_mobile_settings():     
    if (session.super_id==None or session.super_id==''):
        redirect(URL(c='super',f='index'))
    
    #----------
    response.title='Mobile Settings-Edit'
    #----------
    
    page=request.args(0)
    form=crud.update(db.sm_mobile_settings, request.args(1))    
    
    return dict(form=form,page=page)


#==============================================================DEPOT DEVICE SETTINGS
def sys_depot_device_settings():  
    if (session.super_id==None or session.super_id==''):
        redirect(URL(c='super',f='index'))

    #----------
    response.title='Depot Device Settings'
    #----------
    
    form=crud.create(db.sm_depot)    

    #---------------
    btn_filter_depot_device=request.vars.btn_filter_depot_device
    btn_filter_all=request.vars.btn_filter_all
    
    cid_value=str(request.vars.cid_value).strip()
    depot_id_value=str(request.vars.depot_id_value).strip()
    
    reqPage=len(request.args)
    
    if btn_filter_depot_device:
        session.btn_filter_depot_device=btn_filter_depot_device
        session.cid_value=cid_value
        session.depot_id_value=depot_id_value
        
        reqPage=0
        
    elif btn_filter_all:
        session.btn_filter_depot_device=None
        session.cid_value=None
        session.depot_id_value=None
        
        reqPage=0

    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging 
    
    #Set query based on search type
    qset=db()
    if (session.btn_filter_depot_device):
        if (session.cid_value!=''):
            qset=qset(db.sm_depot.cid==session.cid_value)            
        #----------------  
        if (session.depot_id_value!=''):
            qset=qset(db.sm_depot.depot_id==session.depot_id_value)            
        #----------------
         
        records=qset.select(db.sm_depot.ALL,orderby=db.sm_depot.cid,limitby=limitby)
    else:
        records=qset.select(db.sm_depot.ALL,orderby=db.sm_depot.cid,limitby=limitby)  

    #------------------

    return dict(form=form,records=records,page=page,items_per_page=items_per_page)


def update_sys_depot_device_settings():     
    if (session.super_id==None or session.super_id==''):
        redirect(URL(c='super',f='index'))
    
    #----------
    response.title='Depot Device Settings-Edit'
    #----------
    
    page=request.args(0)
    form=crud.update(db.sm_depot, request.args(1))    
    
    return dict(form=form,page=page)


#========================================SUPER SETTINGS
def sys_super_settings():    
    if (session.super_id==None or session.super_id==''):
        redirect(URL(c='super',f='index'))
    
    #----------
    response.title='Super Settings'
    #----------
    
    form=crud.create(db.sm_settings)    
    
    #---------------
    btn_filter_sup_sett=request.vars.btn_filter_sup_sett
    btn_filter_all=request.vars.btn_filter_all

    cid_value=str(request.vars.cid_value).strip()
    
    reqPage=len(request.args)
    
    if btn_filter_sup_sett:
        session.btn_filter_sup_sett=btn_filter_sup_sett
        session.cid_value=cid_value
        reqPage=0
        
    elif btn_filter_all:
        session.btn_filter_sup_sett=None
        session.cid_value=None
        reqPage=0
    
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging 
    
    #Set query based on search type
    qset=db()
    if (session.btn_filter_sup_sett):
        if (session.cid_value!=''):
            qset=qset(db.sm_settings.cid==session.cid_value)            
        #----------------   
        records=qset.select(db.sm_settings.ALL,orderby=db.sm_settings.cid,limitby=limitby)
    else:
        records=qset.select(db.sm_settings.ALL,orderby=db.sm_settings.cid,limitby=limitby)  

    #------------------
        
    return dict(form=form,records=records,items_per_page=items_per_page,page=page)


def update_sys_super_settings():     
    if (session.super_id==None or session.super_id==''):
        redirect(URL(c='super',f='index'))
    
    #----------
    response.title='Super Settings-Edit'
    #----------
    page=request.args(0)
    form=crud.update(db.sm_settings, request.args(1))  
      
    return dict(form=form,page=page)


#==============================================================DEPOT DEVICE SETTINGS
def sys_company_settings():  
    if (session.super_id==None or session.super_id==''):
        redirect(URL(c='super',f='index'))

    #----------
    response.title='Company Settings'
    #----------
    
    form=crud.create(db.sm_company_settings)    

    #---------------
    btn_filter_comp_sett=request.vars.btn_filter_comp_sett
    btn_filter_all=request.vars.btn_filter_all
    
    cid_value=str(request.vars.cid_value).strip()
    
    reqPage=len(request.args)
    
    if btn_filter_comp_sett:
        session.btn_filter_comp_sett=btn_filter_comp_sett
        session.cid_value=cid_value
        
        reqPage=0
        
    elif btn_filter_all:
        session.btn_filter_comp_sett=None
        session.cid_value=None
        
        reqPage=0

    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging 
    
    #Set query based on search type
    qset=db()
    if (session.btn_filter_comp_sett):
        if (session.cid_value!=''):
            qset=qset(db.sm_company_settings.cid==session.cid_value)            
        #----------------
         
        records=qset.select(db.sm_company_settings.ALL,orderby=db.sm_company_settings.cid,limitby=limitby)
    else:
        records=qset.select(db.sm_company_settings.ALL,orderby=db.sm_company_settings.cid,limitby=limitby)  

    #------------------

    return dict(form=form,records=records,page=page,items_per_page=items_per_page)


def update_sys_company_settings():     
    if (session.super_id==None or session.super_id==''):
        redirect(URL(c='super',f='index'))
    
    #----------
    response.title='Company Settings-Edit'
    #----------
    
    page=request.args(0)
    form=crud.update(db.sm_company_settings, request.args(1))    
    
    return dict(form=form,page=page)


#========================================SUPER SETTINGS
def sys_level_settings():    
    if (session.super_id==None or session.super_id==''):
        redirect(URL(c='super',f='index'))
    
    #----------
    response.title='Level Settings'
    #----------
    
    form=crud.create(db.level_name_settings)    
    
    #---------------
    btn_filter_level_sett=request.vars.btn_filter_level_sett
    btn_filter_all=request.vars.btn_filter_all

    cid_value=str(request.vars.cid_value).strip()
    
    reqPage=len(request.args)
    
    if btn_filter_level_sett:
        session.btn_filter_level_sett=btn_filter_level_sett
        session.cid_value=cid_value
        reqPage=0
        
    elif btn_filter_all:
        session.btn_filter_level_sett=None
        session.cid_value=None
        reqPage=0
    
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging 
    
    #Set query based on search type
    qset=db()
    if (session.btn_filter_level_sett):
        if (session.cid_value!=''):
            qset=qset(db.level_name_settings.cid==session.cid_value)            
    
    #----------------
    records=qset.select(db.level_name_settings.ALL,orderby=db.level_name_settings.cid,limitby=limitby)
    
    #------------------
        
    return dict(form=form,records=records,items_per_page=items_per_page,page=page)


def update_sys_level_settings():     
    if (session.super_id==None or session.super_id==''):
        redirect(URL(c='super',f='index'))
    
    #----------
    response.title='level Settings-Edit'
    #----------
    page=request.args(0)
    form=crud.update(db.level_name_settings, request.args(1))  
    if form.accepts(request.vars, session):
        session.flash = 'Updated Successfully'   
        redirect(URL(f='sys_level_settings'))
    
    return dict(form=form,page=page)
    
    
#================================= Web settings batch upload
def web_settings_batch_upload():
    if (session.super_id==None or session.super_id==''):
        redirect(URL(c='super',f='index'))
    
    btn_upload=request.vars.btn_upload
    cid_value=str(request.vars.cid_value).strip().upper()
    
    count_inserted=0
    count_error=0
    error_str=''
    total_row=0
    if btn_upload=='Upload' and not(cid_value=='' or cid_value==None):        
          excel_data=str(request.vars.excel_data)
          inserted_count=0
          error_count=0
          error_list=[]
          row_list=excel_data.split( '\n')
          total_row=len(row_list)
          
          data_list_excel=[]
          data_list_exist=[]
          category_list_exist=[]
    
          area_list_excel=[]
          unit_list=[]
          
          ins_list=[]
          ins_dict={}
          #---------- rep area
          for i in range(total_row):
              if i>=30:
                  break
              else:
                  row_data=row_list[i]                    
                  coloum_list=row_data.split( '\t')
                  if len(coloum_list)==2:
                      data_list_excel.append(coloum_list[0])
    
          existRows=db((db.sm_web_settings.cid==cid_value)&(db.sm_web_settings.s_key.belongs(data_list_excel))).select(db.sm_web_settings.s_key,orderby=db.sm_web_settings.s_key)
          data_list_exist=existRows.as_list()
          
          #   --------------------    main loop 
          for i in range(total_row):
              if i>=30: 
                  break
              else:
                  row_data=row_list[i]
                  
              coloum_list=row_data.split( '\t')  
              if len(coloum_list)==2:
                  s_key=coloum_list[0]
                  s_value=coloum_list[1]
                  
                  try:
                      duplicate_key=False                                                  
                      for i in range(len(data_list_exist)):
                          myRowData=data_list_exist[i]                                
                          sKey=myRowData['s_key']
                          if (str(sKey).strip()==str(s_key).strip()):
                              duplicate_key=True                                 
                              break
                      
                      #-----------------                            
                      if duplicate_key==False:
                          if s_key!='':
                              ins_dict= {'cid':cid_value,'s_key':s_key,'s_value':s_value}
                              ins_list.append(ins_dict)                               
                              count_inserted+=1
                          else:
                              error_data=row_data+'(key needed!)\n'
                              error_str=error_str+error_data
                              count_error+=1
                              continue                            
                      else:
                          error_data=row_data+'(key already exist!)\n'
                          error_str=error_str+error_data
                          count_error+=1
                          continue                            
                  except:
                      error_data=row_data+'(error in process!)\n'
                      error_str=error_str+error_data
                      count_error+=1
                      continue
              else:
                  error_data=row_data+'(2 columns need in a row)\n'
                  error_str=error_str+error_data
                  count_error+=1
                  continue
          
          if error_str=='':
              error_str='No error'
          
          if len(ins_list) > 0:
              inCountList=db.sm_web_settings.bulk_insert(ins_list)             
    
          return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)        
    
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)

#================================= mobile settings batch upload
def mobile_settings_batch_upload():
    if (session.super_id==None or session.super_id==''):
        redirect(URL(c='super',f='index'))
        
        
    btn_upload=request.vars.btn_upload
    cid_value=str(request.vars.cid_value).strip().upper()
    
    count_inserted=0
    count_error=0
    error_str=''
    total_row=0
    if btn_upload=='Upload' and not(cid_value=='' or cid_value==None):        
          excel_data=str(request.vars.excel_data)
          inserted_count=0
          error_count=0
          error_list=[]
          row_list=excel_data.split( '\n')
          total_row=len(row_list)
          
          data_list_excel=[]
          data_list_exist=[]
          category_list_exist=[]
    
          area_list_excel=[]
          unit_list=[]
          
          ins_list=[]
          ins_dict={}
          #---------- rep area
          for i in range(total_row):
              if i>=30:
                  break
              else:
                  row_data=row_list[i]                    
                  coloum_list=row_data.split( '\t')
                  if len(coloum_list)==4:
                      data_list_excel.append(coloum_list[1])
    
          existRows=db((db.sm_mobile_settings.cid==cid_value)&(db.sm_mobile_settings.s_key.belongs(data_list_excel))).select(db.sm_mobile_settings.s_key,db.sm_mobile_settings.type,orderby=db.sm_mobile_settings.s_key)
          data_list_exist=existRows.as_list()
          
          #   --------------------    main loop 
          for i in range(total_row):
              if i>=30: 
                  break
              else:
                  row_data=row_list[i]
                  
              coloum_list=row_data.split( '\t')  
              if len(coloum_list)==4:
                  sl_value=coloum_list[0]
                  s_key=coloum_list[1]
                  s_value=coloum_list[2]
                  type_value=coloum_list[3]
                  
                  try:
                      duplicate_key=False                                                  
                      for i in range(len(data_list_exist)):
                          myRowData=data_list_exist[i]                                
                          sKey=myRowData['s_key']
                          type=myRowData['type']
                          if (str(sKey).strip()==str(s_key).strip() and str(type).strip()==str(type_value).strip()):
                              duplicate_key=True                                 
                              break
                      
                      #-----------------                            
                      if duplicate_key==False:
                          if sl_value!='' and s_key!='' and type_value!='':
                              ins_dict= {'cid':cid_value,'sl':sl_value,'s_key':s_key,'s_value':s_value,'type':type_value}
                              ins_list.append(ins_dict)                               
                              count_inserted+=1
                          else:
                              error_data=row_data+'(key needed!)\n'
                              error_str=error_str+error_data
                              count_error+=1
                              continue                            
                      else:
                          error_data=row_data+'(key already exist!)\n'
                          error_str=error_str+error_data
                          count_error+=1
                          continue                            
                  except:
                      error_data=row_data+'(error in process!)\n'
                      error_str=error_str+error_data
                      count_error+=1
                      continue
              else:
                  error_data=row_data+'(4 columns need in a row)\n'
                  error_str=error_str+error_data
                  count_error+=1
                  continue
          
          if error_str=='':
              error_str='No error'
          
          if len(ins_list) > 0:
              inCountList=db.sm_mobile_settings.bulk_insert(ins_list)             
    
          return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)        
    
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)


#================================= company mobile batch upload
def company_mobile_batch_upload():
    if (session.super_id==None or session.super_id==''):
        redirect(URL(c='super',f='index'))
        
        
    btn_upload=request.vars.btn_upload
    cid_value=str(request.vars.cid_value).strip().upper()
    
    count_inserted=0
    count_error=0
    error_str=''
    total_row=0
    if btn_upload=='Upload' and not(cid_value=='' or cid_value==None):        
          excel_data=str(request.vars.excel_data)
          inserted_count=0
          error_count=0
          error_list=[]
          row_list=excel_data.split( '\n')
          total_row=len(row_list)
          
          data_list_excel=[]
          data_list_exist=[]
          category_list_exist=[]
    
          area_list_excel=[]
          unit_list=[]
          
          ins_list=[]
          ins_dict={}
          #---------- rep area
          for i in range(total_row):
              if i>=30:
                  break
              else:
                  row_data=row_list[i]                    
                  coloum_list=row_data.split( '\t')
                  if len(coloum_list)==2:
                      data_list_excel.append(coloum_list[0])
    
          existRows=db((db.sm_comp_mobile.cid==cid_value)&(db.sm_comp_mobile.mobile_no.belongs(data_list_excel))).select(db.sm_comp_mobile.mobile_no)
          data_list_exist=existRows.as_list()
          
          #   --------------------    main loop 
          for i in range(total_row):
              if i>=30: 
                  break
              else:
                  row_data=row_list[i]
                  
              coloum_list=row_data.split( '\t')  
              if len(coloum_list)==2:
                  mobile_no=str(coloum_list[0]).strip()
                  user_type=str(coloum_list[1]).strip().lower()
                  
                  try:
                      duplicate_key=False                                                  
                      for i in range(len(data_list_exist)):
                          myRowData=data_list_exist[i]                                
                          mobileNo=myRowData['mobile_no']
                          if (str(mobileNo).strip()==str(mobile_no).strip()):
                              duplicate_key=True                                 
                              break
                      
                      #-----------------                            
                      if duplicate_key==False:
                          if mobile_no!='' and user_type!='':
                              ins_dict= {'cid':cid_value,'mobile_no':mobile_no,'user_type':user_type}
                              ins_list.append(ins_dict)                               
                              count_inserted+=1
                          else:
                              error_data=row_data+'(mobile no and user_type needed!)\n'
                              error_str=error_str+error_data
                              count_error+=1
                              continue                            
                      else:
                          error_data=row_data+'(mobile no already exist!)\n'
                          error_str=error_str+error_data
                          count_error+=1
                          continue                            
                  except:
                      error_data=row_data+'(error in process!)\n'
                      error_str=error_str+error_data
                      count_error+=1
                      continue
              else:
                  error_data=row_data+'(2 columns need in a row)\n'
                  error_str=error_str+error_data
                  count_error+=1
                  continue
          
          if error_str=='':
              error_str='No error'
          
          if len(ins_list) > 0:
              inCountList=db.sm_comp_mobile.bulk_insert(ins_list)             
    
          return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)        
    
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)

def sys_data_clean():#Used clean data of specific table
    if (session.super_id==None or session.super_id==''):
        redirect(URL(c='super',f='index'))

    #----------
    response.title='Table Data Clean'
    
    #----------    
    cid_value=str(request.vars.cid_value).strip().upper()
    table_name=str(request.vars.table_name).strip().lower()
    passwordValue=str(request.vars.password).strip()
    
    btn_set=request.vars.btn_set
    btn_reset=request.vars.btn_reset
    btn_clean=request.vars.btn_clean
    btn_update=request.vars.btn_update
    returnStr=''
    if btn_set:
        if (cid_value!='' and table_name!='' and passwordValue!=''):        
            session.cid_value=cid_value
            session.table_name=table_name
            session.passwordValue=passwordValue
            
            if (session.cid_value!=None and session.table_name!=None and session.passwordValue!=None):
                response.flash='settings done'
        else:
            response.flash='all values required'
        
    elif btn_reset:
        #Clear sessions
        session.cid_value=None
        session.table_name=None
        session.passwordValue=None
        if (session.cid_value==None and session.table_name==None and session.passwordValue==None):
            response.flash='reset successfully'
            
    elif btn_clean:
        cid_value=session.cid_value
        table_name=session.table_name
        password=session.passwordValue
        
        if not(cid_value=='' or cid_value==None or table_name=='' or table_name==None or password=='' or password==None):
            if password=='dsfi293kiswerds99':
                compRows=db(db.sm_company_settings.cid==cid_value).select(db.sm_company_settings.cid,limitby=(0,1))
                if compRows:
                    try:            
                        #Delete table data
                        records=db(db[table_name].cid==cid_value).select(db[table_name].id,limitby=(0, 500))
                        
                        if records:
                            count=0
                            for rec in records:
                                db(db[table_name].id==rec.id).delete()
                                count+=1
                            
                            response.flash='%s records cleaned successfully from %s,%s'%(count,table_name,cid_value)
                            
                        else:
                            response.flash='Data not available for %s'%(table_name)
                    except:
                        response.flash='Need valid Table Name settings'
                else:
                    response.flash='Need valid company settings'
            else:
                response.flash='Need valid password settings'
        else:
            response.flash='Need valid CID,Table Name and Password settings'
    
    elif btn_update:
        
        updateStr=str(request.vars.update_sql).strip()
        update_password=str(request.vars.update_password).strip()     
        if not(updateStr=='' or updateStr==None or update_password=='' or update_password==None):
            if update_password=='123123':
#                try:
                             
                resultDict=db.executesql(updateStr)
                
                if resultDict:                        
                    returnStr=str(resultDict)  
                    returnStr=returnStr.replace('), (', '\n') 
                    returnStr=returnStr.replace("u'", "'")
                    returnStr=returnStr.replace("[(", "") 
                    returnStr=returnStr.replace(")]", "")  
                    returnStr=returnStr.replace("'", "")     
                
                response.flash='Executed successfully'    
                    
#                except:
#                    response.flash='Error: Invalid SQL'                
            else:
                response.flash='Need valid password'
        else:
            response.flash='Need SQL and Password'
        
        return dict(returnStr=returnStr)
    
    
    #------------------sm_category
    return dict(returnStr=returnStr)




#==============================================================COMPANY MOBILE
def validation_sys_object_data_clean(form):       
    cid=str(request.vars.cid).strip().upper()
#    mobile_no=str(request.vars.mobile_no).strip()
#    compMobRows=db((db.sm_data_clean.cid == cid)&(db.sm_data_clean.mobile_no == mobile_no)).select(db.sm_data_clean.mobile_no,limitby=(0,1))
#    if compMobRows:
#        form.errors.mobile_no='already exist'
        
def sys_object_data_clean():
    if (session.super_id==None or session.super_id==''):
        redirect(URL(c='super',f='index'))
    
    #----------
    response.title='Object Data Clean'
    #----------
    
    form=crud.create(db.sm_data_clean)    
    
    if form.accepts(request.vars, session,onvalidation=validation_sys_object_data_clean):
        response.flash = 'Submitted Successfully'      
    
    #--------paging
    reqPage=len(request.args)
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=50
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging 
    
    #Set query based on search type
    qset=db()
    records=qset.select(db.sm_data_clean.ALL,orderby=db.sm_data_clean.object_name,limitby=limitby)  

    #------------------
    return dict(form=form,records=records,page=page,items_per_page=items_per_page)

def validation_sys_object_data_clean(form): 
    rowid=str(request.vars.id)
#    cid=str(request.vars.cid).strip().upper()
#    mobile_no=str(request.vars.mobile_no).strip()
#    
#    compMobRows=db((db.sm_data_clean.cid == cid)&(db.sm_data_clean.mobile_no == mobile_no)&(db.sm_data_clean.id != rowid)).select(db.sm_data_clean.mobile_no,limitby=(0,1))
#    if compMobRows:
#        form.errors.mobile_no='already exist'
    
def update_sys_object_data_clean():     
    if (session.super_id==None or session.super_id==''):
        redirect(URL(c='super',f='index'))
    
    #----------
    response.title='Object Data Clean-Edit'
    #----------
    
    page=request.args(0)
    form=crud.update(db.sm_data_clean, request.args(1))    
    
    if form.accepts(request.vars, session,onvalidation=validation_sys_object_data_clean):
        session.flash = 'Updated Successfully'   
        redirect(URL(f='sys_object_data_clean'))
        
    return dict(form=form,page=page)


