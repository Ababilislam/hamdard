# -*- coding: utf-8 -*-

#########################################################################

from gluon.tools import *
mail = Mail()                                  # mailer
auth = Auth(globals(),db)                      # authentication/authorization
crud = Crud(globals(),db)                      # for CRUD helpers using auth
service = Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc
plugins = PluginManager()

mail.settings.server = 'logging' or 'smtp.gmail.com:587'  # your SMTP server
mail.settings.sender = 'you@gmail.com'         # your email
mail.settings.login = 'username:password'      # your credentials or None

auth.settings.hmac_key = 'sha512:d6160708-08e3-4217-bd9e-e9a550109a8d'   # before define_tables()
#auth.define_tables()                           # creates all needed tables
auth.settings.mailer = mail                    # for user email verification
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL('default','user',args=['verify_email'])+'/%(key)s to verify your email'
auth.settings.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL('default','user',args=['reset_password'])+'/%(key)s to reset your password'

#########################################################################

crud.settings.auth = None                      # =auth to enforce authorization on crud

#########################################################################
# Common Variable
#mreporting_http_pass='abC321'
# ' " / \ < > ( ) [ ] { } , 

#======================date========================
import datetime
import os

datetime_fixed=str(date_fixed)[0:19]    # default datetime 2012-07-01 11:48:10
current_date=str(date_fixed)[0:10]   # default date 2012-07-01

first_currentDate = datetime.datetime.strptime(str(current_date)[0:7] + '-01', '%Y-%m-%d')

#================mrep_Database===================
#--------------------------- signature
signature=db.Table(db,'signature',
                Field('field1','string',default=''), 
                Field('field2','integer',default=0),
                Field('note','string',default=''),  
                Field('created_on','datetime',default=date_fixed),
                Field('created_by',default=session.user_id),
                Field('updated_on','datetime',update=date_fixed),
                Field('updated_by',update=session.user_id),
                )

#=====================item================
# ADJUSTMENT_TYPE, CLIENT_CATEGORY, CLIENT_SUB_CATEGORY, CREDIT_NOTE, DEPOT_CATEGORY, ISSUE_CAUSE, ITEM_CATEGORY, ITEM_UNIT, PAYMENT_ADJUSTMENT_TYPE, PAYMENT_MODE, PAYMENT_TYPE, RET_REASON, TRANSFER_TYPE
db.define_table('sm_category_type',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('type_name','string',requires=IS_NOT_EMPTY()), #Item,
                Field('cat_type_id','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='enter maximum 50 character')]),
                Field('cat_type_name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(100,error_message='enter maximum 100 character')]),
                signature,
                migrate=False
                )

db.define_table('sm_item',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('item_id','string',requires=[IS_NOT_EMPTY(),IS_ALPHANUMERIC(error_message=T('must be alphanumeric ( a-z, A-Z, 0-9 )!')),IS_LENGTH(20,error_message='enter maximum 20 character')]),
                Field('name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(100,error_message='enter maximum 100 character')]),
                Field('des','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(100,error_message='enter maximum 100 character')],default='-'),
                Field('category_id','string',requires=IS_NOT_EMPTY()),  #primary category
                Field('category_id_sp','string',default=''),            #special category
                Field('unit_type','string',requires=IS_NOT_EMPTY()),                
                Field('manufacturer','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='enter maximum 50 character')],default='-'),
                Field('item_carton','integer',default=0),
                
                Field('price','double',requires=[IS_NOT_EMPTY(),IS_FLOAT_IN_RANGE(0, 999999, dot=".",error_message='too small or too large!')]),
                Field('dist_price','double',requires=[IS_NOT_EMPTY(),IS_FLOAT_IN_RANGE(0, 999999, dot=".",error_message='too small or too large!')]),
                
                Field('vat_amt','double',requires=[IS_NOT_EMPTY(),IS_FLOAT_IN_RANGE(0, 999999, dot=".",error_message='too small or too large!')]),
                Field('total_amt','double',default=0),
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='ACTIVE'),
                signature,
                migrate=False
                )

# use to Change item which r change based on schedule by cron
db.define_table('sm_item_temp',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('item_id','string',requires=[IS_NOT_EMPTY(),IS_ALPHANUMERIC(error_message=T('must be alphanumeric ( a-z, A-Z, 0-9 )!')),IS_LENGTH(20,error_message='enter maximum 20 character')]),
                Field('name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(100,error_message='enter maximum 100 character')]),
                Field('des','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(100,error_message='enter maximum 100 character')],default='-'),
                Field('category_id','string',requires=IS_NOT_EMPTY()),  #primary category
                Field('category_id_sp','string',default=''),            #special category
                Field('unit_type','string',requires=IS_NOT_EMPTY()),
                Field('manufacturer','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='enter maximum 50 character')],default='-'),
                Field('item_carton','integer',default=0),
                
                Field('price','double',requires=[IS_NOT_EMPTY(),IS_FLOAT_IN_RANGE(0, 999999, dot=".",error_message='too small or too large!')]),
                Field('dist_price','double',requires=[IS_NOT_EMPTY(),IS_FLOAT_IN_RANGE(0, 999999, dot=".",error_message='too small or too large!')]),
                
                Field('vat_amt','double',requires=[IS_NOT_EMPTY(),IS_FLOAT_IN_RANGE(0, 999999, dot=".",error_message='too small or too large!')]),
                Field('total_amt','double',default=0),
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='ACTIVE'),
                Field('schedule_date','date',requires=IS_NOT_EMPTY()),
                Field('process_flag','integer',default=0),#0=pending,1=complete
                
                signature,
                migrate=False
                )


db.define_table('sm_item_process_schedule',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('schedule_date','date',requires=IS_NOT_EMPTY()),
                
                Field('process_flag','integer',default=0),#0=pending,2=running,1=complete
                Field('item_list_str','text',default=''),
                
                signature,
                migrate=False
                )

#=================level===================
db.define_table('sm_level',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('level_id','string',requires=[IS_NOT_EMPTY(),IS_ALPHANUMERIC(error_message=T('must be alphanumeric ( a-z, A-Z, 0-9 )!')),IS_LENGTH(20,error_message='Maximum 20 character')]),
                Field('level_name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='Maximum 50 character')]),
                Field('parent_level_id','string',default='0',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='Maximum 50 character')]),
                Field('parent_level_name','string',default=''),
                Field('is_leaf','string',requires=IS_NOT_EMPTY(),default='0'), #0 for group & 1 for final
                Field('area_id_list','string',default=''),
                Field('special_territory_code','string',default=''),
                Field('depot_id','string',default='-',requires=[IS_NOT_EMPTY(),IS_LENGTH(20,error_message='Maximum 20 character')]),
                
                Field('depth','integer',default=0),
                Field('level0','string',default=''),
                Field('level0_name','string',default=''),
                Field('level1','string',default=''),
                Field('level1_name','string',default=''),
                Field('level2','string',default=''),
                Field('level2_name','string',default=''),
                Field('level3','string',default=''),
                Field('level3_name','string',default=''),
                Field('level4','string',default=''),
                Field('level4_name','string',default=''),
                Field('level5','string',default=''),
                Field('level5_name','string',default=''),
                Field('level6','string',default=''),
                Field('level6_name','string',default=''),
                Field('level7','string',default=''),
                Field('level7_name','string',default=''),
                Field('level8','string',default=''),
                Field('level8_name','string',default=''),
                Field('territory_des','string',default=''),
                signature,
                migrate=False
                )

#=========================rep============
db.define_table('sm_rep',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('rep_id','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(20,error_message='Mmaximum 20 character')]),
                Field('name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='Maximum 50 character')]),
                Field('mobile_no','bigint',default=''),
                Field('password','password',requires=IS_LENGTH(minsize=3,maxsize=12)),
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='ACTIVE'),
                Field('sync_code','string',default=''),
                Field('sync_code_servey','string',default=''),
                Field('sync_count','integer',requires=IS_NOT_EMPTY(),default=0),
                Field('first_sync_date','datetime',default=''),
                Field('last_sync_date','datetime',default=''),
                Field('monthly_sms_count','integer',requires=IS_NOT_EMPTY(),default=0),
                Field('monthly_voucher_count','integer',requires=IS_NOT_EMPTY(),default=0),
                
                Field('java','string',requires=IS_IN_SET(('Yes','No')),default='No'),
                Field('wap','string',requires=IS_IN_SET(('Yes','No')),default='No'),
                Field('android','string',requires=IS_IN_SET(('Yes','No')),default='No'),
                Field('sms','string',requires=IS_IN_SET(('Yes','No')),default='Yes'),
                
                Field('user_type','string',default='rep'),
                Field('level_id','string',default=''),
                Field('depot_id','string',default=''),
                  
                # user click on "Sync" will get response lik "You sync request is in que Please try to sync after few minutes" o - > 1
                # if already submitted (flag = 1) - "Your request is already in que, please try to sync ... "
                # if last sync request is less that 10 minutes before .. your sync data is just processed please try to sync or wait atleast 10 minute to make another "Que to Sync" request
                
                Field('sync_req_time','datetime',default=''),#10 min gap in 2 sync
                Field('sync_flag','string',default='0'),
                Field('sync_data','string',default=''),
                signature,
                migrate=False
                )#field2 is used for depth

db.define_table('sm_rep_area',   
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('rep_id','string',requires=IS_NOT_EMPTY()),
                Field('rep_name','string',default=''),
                Field('rep_category','string',requires=IS_IN_SET(('A','B','C','Z'))),#MSO Category
                
                Field('area_id','string',requires=IS_NOT_EMPTY()),
                Field('area_name','string',default=''),                
                Field('depot_id','string',default=''),
                signature,
                migrate=False
                )

db.define_table('sm_supervisor_level',   
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('sup_id','string',requires=IS_NOT_EMPTY()),
                Field('sup_name','string',default=''),
                
                Field('level_id','string',requires=IS_NOT_EMPTY()),
                Field('level_name','string',default=''),
                Field('level_depth_no','integer',default=0),
                
                signature,
                migrate=False
                )

#--- team structure process
db.define_table('sm_area_team_process_schedule',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                
                Field('first_date','date',requires=IS_NOT_EMPTY()),
                Field('schedule_date','date',requires=IS_NOT_EMPTY()),                
                Field('status','string',default='0'),
                Field('notes','string',default=''),
                
                signature,
                migrate=False
                )#field2=Process to live flag, 0=draft,1=Completed,2=Pending..

#================= Area and Team temp structure
db.define_table('sm_area_team_temp',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),                
                Field('firstdate','date',default=first_currentDate),
                
                Field('zone_id','string',default=''),
                Field('zone_name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(100,error_message='Maximum 100 character')]),
                Field('region_id','string',default=''),
                Field('region_name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(100,error_message='Maximum 100 character')]),
                Field('area_id','string',default=''),
                Field('area_name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(100,error_message='Maximum 100 character')]),
                Field('territory_id','string',default=''),
                Field('territory_name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(100,error_message='Maximum 100 character')]),
                Field('territory_des','string',default=''),
                Field('special_territory_code','string',default=''),
                
                Field('zm_id','string',default=''),
                Field('zm_name','string',default=''),
                Field('zm_mobile_no','bigint',default=0),
                Field('rsm_id','string',default=''),
                Field('rsm_name','string',default=''),
                Field('rsm_mobile_no','bigint',default=0),
                Field('fm_id','string',default=''),
                Field('fm_name','string',default=''),
                Field('fm_mobile_no','bigint',default=0),
                Field('mso_id','string',requires=[IS_NOT_EMPTY(),IS_ALPHANUMERIC(error_message=T('must be alphanumeric ( a-z, A-Z, 0-9 )!')),IS_LENGTH(20,error_message='Maximum 20 character')]),
                Field('mso_name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='Maximum 50 character')]),
                Field('mso_mobile_no','bigint',default=0),
                Field('mso_category','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='Maximum 50 character')]),
                
                Field('zone_flag','integer',default=0), #0=Pending,1=Complete,2=Error
                Field('region_flag','integer',default=0), #0=Pending,1=Complete,2=Error
                Field('area_flag','integer',default=0), #0=Pending,1=Complete,2=Error
                Field('territory_flag','integer',default=0), #0=Pending,1=Complete,2=Error
                Field('first_part_flag','integer',default=0), #0=Pending,1=Complete
                
                Field('zm_flag','integer',default=0), #0=Pending,1=Complete,2=Error
                Field('rsm_flag','integer',default=0), #0=Pending,1=Complete,2=Error
                Field('fm_flag','integer',default=0), #0=Pending,1=Complete,2=Error
                Field('mso_flag','integer',default=0), #0=Pending,1=Complete,2=Error
                Field('second_part_flag','integer',default=0), #0=Pending,1=Complete
                
                Field('des','string',default=''),
                
                signature,
                migrate=False
                )

#================= Area and Team temp structure
db.define_table('sm_area_team_temp_backup',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),                
                Field('firstdate','date',default=first_currentDate),
                Field('currentdate','date',default=current_date),
                
                Field('zone_id','string',default=''),
                Field('zone_name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(100,error_message='Maximum 100 character')]),
                Field('region_id','string',default=''),
                Field('region_name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(100,error_message='Maximum 100 character')]),
                Field('area_id','string',default=''),
                Field('area_name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(100,error_message='Maximum 100 character')]),
                Field('territory_id','string',default=''),
                Field('territory_name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(100,error_message='Maximum 100 character')]),
                Field('territory_des','string',default=''),
                Field('special_territory_code','string',default=''),
                
                Field('zm_id','string',default=''),
                Field('zm_name','string',default=''),
                Field('zm_mobile_no','bigint',default=0),
                Field('rsm_id','string',default=''),
                Field('rsm_name','string',default=''),
                Field('rsm_mobile_no','bigint',default=0),
                Field('fm_id','string',default=''),
                Field('fm_name','string',default=''),
                Field('fm_mobile_no','bigint',default=0),
                Field('mso_id','string',requires=[IS_NOT_EMPTY(),IS_ALPHANUMERIC(error_message=T('must be alphanumeric ( a-z, A-Z, 0-9 )!')),IS_LENGTH(20,error_message='Maximum 20 character')]),
                Field('mso_name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='Maximum 50 character')]),
                Field('mso_mobile_no','bigint',default=0),
                Field('mso_category','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='Maximum 50 character')]),
                
                signature,
                migrate=False
                )


#========================= Delivery Man
db.define_table('sm_delivery_man',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('d_man_id','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(20,error_message='Mmaximum 20 character')]),
                Field('name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='Maximum 50 character')]),
                Field('mobile_no','bigint',default=''),
                Field('password','password',requires=IS_LENGTH(minsize=3,maxsize=12)),
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='ACTIVE'),
                Field('sync_code','string',default=''),
                Field('sync_count','integer',requires=IS_NOT_EMPTY(),default=0),
                Field('first_sync_date','datetime',default=''),
                Field('last_sync_date','datetime',default=''),
                Field('monthly_sms_count','integer',requires=IS_NOT_EMPTY(),default=0),
                Field('monthly_voucher_count','integer',requires=IS_NOT_EMPTY(),default=0),
                
                Field('java','string',requires=IS_IN_SET(('Yes','No')),default='No'),
                Field('wap','string',requires=IS_IN_SET(('Yes','No')),default='No'),
                Field('android','string',requires=IS_IN_SET(('Yes','No')),default='No'),
                Field('sms','string',requires=IS_IN_SET(('Yes','No')),default='Yes'),
                
                Field('depot_id','string',default=''),
                
                signature,
                migrate=False
                )

db.define_table('sm_client',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('client_id','string',default=''),
                Field('client_old_id','string',default=''),#ACCPAC ID
                
                Field('name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='enter maximum 50 character')]),
                Field('area_id','string',requires=IS_NOT_EMPTY()),
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='ACTIVE'),
                Field('op_balance','double',requires=IS_NOT_EMPTY(),default=0.0),#change type from integer
                Field('balance','double',requires=IS_NOT_EMPTY(),default=0.0),  #change type from integer
                Field('credit_limit','double',requires=IS_NOT_EMPTY(),default=0.0),#change type from integer
                Field('address','string',default=''),
                Field('latitude','string',default='0'),
                Field('longitude','string',default='0'),
                Field('depot_id','string',requires=IS_NOT_EMPTY()),
                Field('depot_name','string',default=''),
                Field('store_id','string',requires=IS_NOT_EMPTY()),
                Field('store_name','string',default=''),
                
                Field('depot_belt_name','string',default=''),#depot/brance belt
                Field('category_id','string',default=''),
                Field('category_name','string',default=''),
                Field('sub_category_id','string',default=''),
                Field('sub_category_name','string',default=''),
                Field('market_id','string',requires=IS_NOT_EMPTY()),
                Field('market_name','string','string',default=''),
                
                Field('owner_name','string',default=''),
                Field('nid','integer',default=''),
                Field('passport','string',default=''),
                Field('trade_license','string',default=''),#Yes/No
                Field('trade_license_no','string',default=''),
                Field('vat_registration','string',default=''),#Yes/No
                Field('vat_registration_no','string',default=''),
                Field('drug_registration_num','string','string',default=''),
                Field('doctor','string',requires=IS_EMPTY_OR(IS_IN_SET(('YES','NO')))),
                Field('contact_no1','integer',default=''),
                Field('contact_no2','integer',default=''),
                Field('dob','date'),
                Field('dom','date'),
                Field('kids_info','string',default=''),
                Field('hobby','string',default=''),
                
                Field('manager_name','string',default=''),
                Field('manager_contact_no','integer',default=''),
                
                Field('starting_year','integer',default=''),                
                Field('monthly_sales_capacity','integer',default=0),
                Field('monthly_sales','integer',default=0),
                Field('shop_owner_status','string',default=''),#Rented/Own
                
                Field('warehouse_capacity','integer',default=0),#number of bag Qty
                Field('shop_size','integer',default=0), #sft
                Field('shop_front_size','integer',default=0),                
                Field('photo','string',default=''),#'upload',autodelete=True,uploadfolder=os.path.join(request.folder,'static/client_pic')),
                Field('photo_str','string',default=''),
                
                Field('thana_id','integer'),#not used                
                Field('thana','string',requires=IS_NOT_EMPTY()),
                Field('district_id','string',requires=IS_NOT_EMPTY()),
                Field('district','string',default=''),
                
                signature,
                migrate=False      
                )


#=============================================
db.define_table('sm_client_user',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('client_id','string',requires=IS_NOT_EMPTY()),

                Field('user_id','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(20,error_message='enter maximum 20 character')]),
                Field('name','string',default=''),
                Field('mobile_no','string',default=''),
                Field('password','string',default='',requires=IS_LENGTH(minsize=3,maxsize=12)),
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='INACTIVE'),
               
                Field('sync_code','string',default=''),
                Field('sync_count','integer',requires=IS_NOT_EMPTY(),default=0),
                Field('first_sync_date','datetime',default=''),
                Field('last_sync_date','datetime',default=''),
                Field('monthly_sms_count','integer',requires=IS_NOT_EMPTY(),default=0),
                Field('monthly_voucher_count','integer',requires=IS_NOT_EMPTY(),default=0),
                
                Field('java','string',requires=IS_IN_SET(('Yes','No')),default='No'),
                Field('wap','string',requires=IS_IN_SET(('Yes','No')),default='No'),
                Field('android','string',requires=IS_IN_SET(('Yes','No')),default='No'),
                Field('sms','string',requires=IS_IN_SET(('Yes','No')),default='No'),                
                signature,
                migrate=False
        
                )                

#=================depot===================
db.define_table('sm_depot',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('depot_id','string',requires=[IS_NOT_EMPTY(),IS_ALPHANUMERIC(error_message=T('must be alphanumeric!')),IS_LENGTH(20,error_message='enter maximum 20 character')]),
                Field('name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='enter maximum 50 character')]),
                Field('short_name','string',default=''),
                Field('requisition_sl','integer',requires=IS_NOT_EMPTY(),default=0),
                Field('issue_sl','integer',requires=IS_NOT_EMPTY(),default=0),
                Field('receive_sl','integer',requires=IS_NOT_EMPTY(),default=0),
                Field('damage_sl','integer',requires=IS_NOT_EMPTY(),default=0),
                Field('order_sl','integer',requires=IS_NOT_EMPTY(),default=0),
                Field('del_sl','integer',requires=IS_NOT_EMPTY(),default=0),
                Field('return_sl','integer',requires=IS_NOT_EMPTY(),default=0),
                Field('client_payment_sl','integer',requires=IS_NOT_EMPTY(),default=0),
                Field('depot_payment_sl','integer',requires=IS_NOT_EMPTY(),default=0),
                Field('stock_in_sl','integer',requires=IS_NOT_EMPTY(),default=0),# used for payment to client sl
                Field('issue_balance','double',requires=IS_NOT_EMPTY(),default=0.0),# Not used
                Field('receive_balance','double',requires=IS_NOT_EMPTY(),default=0.0),# Not used
                Field('op_balance','double',requires=IS_NOT_EMPTY(),default=0.0),# Not used
                Field('balance','double',requires=IS_NOT_EMPTY(),default=0.0),# Not used
                Field('depot_category','string',default=''),#used for depot Type
                Field('reporting_level_id','string',default=''),#used for achievement report
                Field('reporting_level_name','string',default=''),
                
                Field('auto_del_cron_flag','integer',default=0),#used for auto delivery
                
                Field('dm_pass','string',default=''),
                Field('mac','string',default='0'),
                Field('hdd','string',default='0'),
                Field('status','string',default='INACTIVE'),                
                signature,
                migrate=False
                )

db.define_table('sm_depot_settings',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('depot_id','string',requires=IS_NOT_EMPTY()),
                Field('from_to_type','string',default='Receive'),#Receive (Requisition to and Receive from); Issue(Issue to)
                Field('depot_id_from_to','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='enter maximum 50 character')]),
                signature,
                migrate=False
                )

db.define_table('sm_depot_store',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('depot_id','string',requires=IS_NOT_EMPTY()),
                Field('store_id','string',requires=IS_NOT_EMPTY()),         
                Field('store_name','string',requires=IS_NOT_EMPTY()),
                Field('store_type','string',requires=IS_IN_SET(('SALES','OTHERS')),default='SALES'),#SALES,OTHERS
                signature,
                migrate=False
                )

db.define_table('sm_depot_market',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('depot_id','string',requires=IS_NOT_EMPTY()),
                Field('market_id','string',requires=IS_NOT_EMPTY()),         
                Field('market_name','string',requires=IS_NOT_EMPTY()),                
                signature,
                migrate=False
                )

db.define_table('sm_depot_belt',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('depot_id','string',requires=IS_NOT_EMPTY()),                
                Field('belt_name','string',requires=IS_NOT_EMPTY()),
                signature,
                migrate=False
                )

#=========================================================
#db.define_table('sm_depot_stock',#monthly
#                Field('cid','string',requires=IS_NOT_EMPTY()),
#                Field('depot_id','string',requires=IS_NOT_EMPTY()),
#                Field('ym_date','date',requires=IS_NOT_EMPTY(),default=current_date),
#                Field('item_id','string',requires=IS_NOT_EMPTY()),
#                Field('quantity','integer',requires=IS_NOT_EMPTY(),default=0),
#                Field('req_qty','integer',requires=IS_NOT_EMPTY(),default=0),
#                Field('iss_qty','integer',requires=IS_NOT_EMPTY(),default=0),
#                Field('rec_qty','integer',requires=IS_NOT_EMPTY(),default=0),
#                Field('dam_qty','integer',requires=IS_NOT_EMPTY(),default=0),
#                Field('ord_qty','integer',requires=IS_NOT_EMPTY(),default=0),
#                Field('del_qty','integer',requires=IS_NOT_EMPTY(),default=0),
#                Field('retn_qty','integer',requires=IS_NOT_EMPTY(),default=0),
#                Field('oth_plus_qty','integer',requires=IS_NOT_EMPTY(),default=0),
#                Field('oth_minus_qty','integer',requires=IS_NOT_EMPTY(),default=0),
#                Field('booked_for_delivery','integer',default=0),
#                signature,
#                migrate=False
#                )

#=========================================================
db.define_table('sm_depot_stock_balance',#current stock
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('depot_id','string',requires=IS_NOT_EMPTY()),
                Field('store_id','string',requires=IS_NOT_EMPTY()),#location id
                Field('store_name','string',requires=IS_NOT_EMPTY()),#location name
                Field('item_id','string',requires=IS_NOT_EMPTY()),
                Field('batch_id','string',default=''),
                Field('expiary_date', 'date'),
                
                Field('quantity','integer',requires=IS_NOT_EMPTY(),default=0),
                Field('block_qty','integer',default=0),
                migrate=False
                )

#================= sm amount transaction NB: depot issue/receive,delivery, return,depot payment,client payment
db.define_table('sm_transaction',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('txid','string',requires=IS_NOT_EMPTY()), # txtype+tx_account+sl
                Field('tx_date','datetime',requires=IS_NOT_EMPTY(),default=date_fixed),
                Field('tx_type','string',requires=IS_NOT_EMPTY()), #issue,receive,opening,delivery,return,depot payment,client payment
                Field('reference','string',default=''),
                Field('tx_account','string',requires=IS_NOT_EMPTY()),
                Field('opposite_account','string',requires=IS_NOT_EMPTY()),
                
                Field('tx_op_balance','double',requires=IS_NOT_EMPTY(),default=0.0),
                Field('tx_amount','double',requires=IS_NOT_EMPTY(),default=0.0),
                Field('tx_closing_balance','double',requires=IS_NOT_EMPTY(),default=0.0),
                
                Field('tx_des','string',default=''),
                Field('sales_type','string',default=''),#P for Primary, S for secondary
                Field('row_flag','string',default='0'),
                
                Field('depot_status','string',default='0'),
                Field('ho_status','string',default='0'),
                signature,
                migrate=False
                )

#========================stock requisition========================
db.define_table('sm_requisition_head', 
                Field('cid','string',requires=IS_NOT_EMPTY()), #from session
                Field('depot_id','string',requires=IS_NOT_EMPTY()), #from session
                Field('depot_name','string',default=''),
                Field('sl','integer',requires=IS_NOT_EMPTY()), # max + 1 for each depot
                Field('requisition_to','string',requires=IS_NOT_EMPTY()), # anothoer depot - selected from combo
                Field('depot_to_name','string',default=''),
                Field('req_date','date',requires=IS_NOT_EMPTY(),default=current_date),
                Field('status','string',default='Draft'),#draft/posted/cancelled
                Field('req_process_status','string',default='Requisition'),# Requisition, Issued

                Field('ym_date','date'),
                
                Field('depot_status','string',default='0'),
                Field('ho_status','string',default='0'),

                Field('flag_depot_stock','integer',default=0),
                Field('flag_data','string',default='0'),
                signature,
                migrate=False
                )

db.define_table('sm_requisition', 
                Field('cid','string',requires=IS_NOT_EMPTY()), #from session
                Field('depot_id','string',requires=IS_NOT_EMPTY()), #from session
                Field('depot_name','string',default=''),
                Field('sl','integer',requires=IS_NOT_EMPTY()), # max + 1 for each depot
                Field('requisition_to','string',requires=IS_NOT_EMPTY()), # anothoer depot - selected from combo
                Field('depot_to_name','string',default=''),
                Field('req_date','date',requires=IS_NOT_EMPTY(),default=current_date),
                Field('status','string',default='Draft'),#draft/posted/cancelled
                Field('req_process_status','string',default='Requisition'),# Requisition, Issued
                
                Field('item_id','string',requires=IS_NOT_EMPTY()),
                Field('item_name','string',requires=IS_NOT_EMPTY()),
                Field('quantity','integer',requires=[IS_NOT_EMPTY(),IS_INT_IN_RANGE(1, 999999)],default=0),
                Field('dist_rate','double',requires=IS_NOT_EMPTY(),default=0), #distributor rate 
                
                Field('short_note','string',default=''), 
                Field('ym_date','date'),
                
                Field('depot_status','string',default='0'),
                Field('ho_status','string',default='0'),

                Field('flag_depot_stock','integer',default=0),
                Field('flag_data','string',default='0'),              
                signature,
                migrate=False
                )

#========================stock issue========================
db.define_table('sm_issue_head',   # issue 
                Field('cid','string',requires=IS_NOT_EMPTY()), #from session
                Field('depot_id','string',requires=IS_NOT_EMPTY()), #from session
                Field('depot_name','string',default=''),                                
                Field('sl','integer',requires=IS_NOT_EMPTY()), # max + 1 for each depot
                Field('store_id','string',default=''),
                Field('store_name','string',default=''),
                
                Field('issued_to','string',requires=IS_NOT_EMPTY()), # anothoer depot - selected from combo
                Field('depot_to_name','string',default=''),
                Field('issue_date','date',requires=IS_NOT_EMPTY(),default=current_date),
                Field('status','string',default='Draft'),#draft/posted/cancelled
                Field('issue_process_status','string',default='Issued'),# Requisition, Issued, Received                
                Field('total_discount','double',requires=IS_NOT_EMPTY(),default=0), 
                Field('transaction_cause','string',default=''),
                
                Field('req_sl','integer',default=0),                
                Field('ym_date','date'),
                
                Field('depot_status','string',default='0'),
                Field('ho_status','string',default='0'),

                Field('flag_depot_stock','integer',default=0),
                Field('flag_depot_stock_balance','integer',default=0),  
                Field('flag_data','string',default='0'),
                signature,
                migrate=False
                )

db.define_table('sm_issue',   # issue
                Field('cid','string',requires=IS_NOT_EMPTY()), #from session
                Field('depot_id','string',requires=IS_NOT_EMPTY()), 
                Field('depot_name','string',default=''),
                Field('sl','integer',requires=IS_NOT_EMPTY()), # max + 1 for each depot
                Field('store_id','string',default=''),
                Field('store_name','string',default=''),
                
                Field('issued_to','string',requires=IS_NOT_EMPTY()), # anothoer depot - selected from combo
                Field('depot_to_name','string',default=''),
                Field('issue_date','date',requires=IS_NOT_EMPTY(),default=current_date),
                Field('status','string',default='Draft'),#draft/posted/cancelled
                Field('issue_process_status','string',default='Issued'),# Requisition, Issued, Received                
                Field('total_discount','double',requires=IS_NOT_EMPTY(),default=0),
                Field('transaction_cause','string',default=''),
                
                Field('req_sl','integer',default=0),
                Field('item_id','string',requires=IS_NOT_EMPTY()),
                Field('batch_id','string',default=''),
                
                Field('item_name','string',requires=IS_NOT_EMPTY()),
                Field('quantity','integer',requires=[IS_NOT_EMPTY(),IS_INT_IN_RANGE(1, 999999)],default=0),
                Field('bonus_qty','integer',requires=IS_INT_IN_RANGE(0, 999999),default=0),
                Field('dist_rate','double',requires=IS_NOT_EMPTY(),default=0),
                
                Field('item_unit','string',default=''),
                Field('item_carton','integer',default=0),
                Field('expiary_date', 'date'),
                
                Field('short_note','string',default=''),
                Field('ym_date','date'),
                
                Field('depot_status','string',default='0'),
                Field('ho_status','string',default='0'),

                Field('flag_depot_stock','integer',default=0),
                Field('flag_depot_stock_balance','integer',default=0),  
                Field('flag_data','string',default='0'),
                signature,
                migrate=False
                )

#========================stock Receive========================
db.define_table('sm_receive_head',
                Field('cid','string',requires=IS_NOT_EMPTY()),#PK
                Field('depot_id','string',requires=IS_NOT_EMPTY()),#PK
                Field('depot_name','string',default=''),
                Field('sl','integer',requires=IS_NOT_EMPTY()),#PK
                Field('store_id','string',default=''),
                Field('store_name','string',default=''),
                
                Field('receive_from','string',requires=IS_NOT_EMPTY()),
                Field('depot_from_name','string',default=''),
                Field('receive_date','date',requires=IS_NOT_EMPTY(),default=current_date),
                Field('status','string',default='Draft'),#draft/posted/cancelled
                Field('receive_process_status','string',default='Received'),# Requisition, Issued, Received
                Field('total_discount','double',requires=IS_NOT_EMPTY(),default=0),
                Field('transaction_cause','string',default=''),
                
                Field('ref_sl','integer',default=0),  
                Field('ym_date','date'),
                
                Field('depot_status','string',default='0'),
                Field('ho_status','string',default='0'),
                
                Field('flag_depot_stock','integer',default=0),
                Field('flag_depot_stock_balance','integer',default=0),  
                Field('flag_data','string',default='0'),                
                signature,
                migrate=False
                )

db.define_table('sm_receive',
                Field('cid','string',requires=IS_NOT_EMPTY()),#PK
                Field('depot_id','string',requires=IS_NOT_EMPTY()),#PK
                Field('depot_name','string',default=''),
                Field('sl','integer',requires=IS_NOT_EMPTY()),#PK
                Field('store_id','string',default=''),
                Field('store_name','string',default=''),
                
                Field('receive_from','string',requires=IS_NOT_EMPTY()),
                Field('depot_from_name','string',default=''),
                Field('receive_date','date',requires=IS_NOT_EMPTY(),default=current_date),
                Field('status','string',default='Draft'),#draft/posted/cancelled
                Field('receive_process_status','string',default='Received'),# Requisition, Issued, Received
                Field('total_discount','double',requires=IS_NOT_EMPTY(),default=0),
                Field('transaction_cause','string',default=''),
                
                Field('ref_sl','integer',default=0),                
                Field('item_id','string',requires=IS_NOT_EMPTY()),
                Field('batch_id','string',default=''),                
                Field('item_name','string',requires=IS_NOT_EMPTY()),
                Field('quantity','integer',requires=[IS_NOT_EMPTY(),IS_INT_IN_RANGE(1, 999999)],default=0),
                Field('bonus_qty','integer',requires=IS_INT_IN_RANGE(0, 999999),default=0),
                Field('dist_rate','double',requires=IS_NOT_EMPTY(),default=0),#Used as Tp Rate
                
                Field('item_unit','string',default=''),
                Field('item_carton','integer',default=0),
                Field('expiary_date', 'date'),
                
                Field('short_note','string',default=''),
                Field('ym_date','date'),
                Field('depot_status','string',default='0'),
                Field('ho_status','string',default='0'),
                
                Field('flag_depot_stock','integer',default=0),
                Field('flag_depot_stock_balance','integer',default=0),  
                Field('flag_data','string',default='0'),                
                signature,
                migrate=False
                )

#========================damage
db.define_table('sm_damage_head',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('depot_id','string',requires=IS_NOT_EMPTY()),
                Field('depot_name','string',default=''),
                Field('sl','integer',requires=IS_NOT_EMPTY(),default=0),
                
                Field('transfer_type','string',default=''),   #TRANSFER,ADJUSTMENT
                Field('type_sl','integer',requires=IS_NOT_EMPTY(),default=0),
                
                Field('store_id','string',default=''),      #From Store id
                Field('store_name','string',default=''),    #From Store name
                
                Field('store_id_to','string',default=''),      #To Store id
                Field('store_name_to','string',default=''),    #To Store name
                
                Field('damage_date','date',requires=IS_NOT_EMPTY(),default=current_date),
                Field('status','string',default='Draft'),       #draft/posted/cancelled    
                
                Field('adjustment_reference','string',default=''),           
                Field('adjustment_type','string',default=''),   #Positive,Negative
                
                Field('ym_date','date'),
                
                Field('depot_status','string',default='0'),
                Field('ho_status','string',default='0'),   
                
                Field('flag_depot_stock','integer',default=0),
                Field('flag_depot_stock_balance','integer',default=0),  
                Field('flag_data','string',default='0'),                         
                signature,
                migrate=False    
                )

db.define_table('sm_damage',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('depot_id','string',requires=IS_NOT_EMPTY()),
                Field('depot_name','string',default=''),
                Field('sl','integer',requires=IS_NOT_EMPTY(),default=0),
                
                Field('transfer_type','string',default=''),   #TRANSFER,ADJUSTMENT
                Field('type_sl','integer',requires=IS_NOT_EMPTY(),default=0),
                
                Field('store_id','string',default=''),
                Field('store_name','string',default=''),
                
                Field('store_id_to','string',default=''),      #To Store id
                Field('store_name_to','string',default=''),    #To Store name
                
                Field('damage_date','date',requires=IS_NOT_EMPTY(),default=current_date),
                Field('status','string',default='Draft'),       #draft/posted/cancelled   
                
                Field('adjustment_reference','string',default=''),             
                Field('adjustment_type','string',default=''),   #Positive,Negative
                
                Field('item_id','string',requires=IS_NOT_EMPTY()),
                Field('batch_id','string',default=''),                
                Field('item_name','string',requires=IS_NOT_EMPTY()),
                Field('quantity','integer',requires=[IS_NOT_EMPTY(),IS_INT_IN_RANGE(1, 999999)],default=0),
                Field('dist_rate','double',requires=IS_NOT_EMPTY(),default=0),
                
                Field('item_unit','string',default=''),
                Field('item_carton','integer',default=0),
                Field('expiary_date', 'date'),
                
                Field('short_note','string',default=''), 
                Field('ym_date','date'), 
                
                Field('depot_status','string',default='0'),
                Field('ho_status','string',default='0'),   
 
                Field('flag_depot_stock','integer',default=0),
                Field('flag_depot_stock_balance','integer',default=0),  
                Field('flag_data','string',default='0'),                         
                signature,
                migrate=False      
                )

#=======================order
db.define_table('sm_order_head',
                Field('cid','string',requires=IS_NOT_EMPTY()), 
                Field('depot_id','string',requires=IS_NOT_EMPTY()), 
                Field('depot_name','string',default=''),
                Field('sl','integer',requires=IS_NOT_EMPTY(),default=0),
                Field('store_id','string',default=''),
                Field('store_name','string',default=''),
                
                Field('client_id','string',default=''),
                Field('client_name','string',default=''),                
                Field('rep_id','string',default=''),
                Field('rep_name','string',default=''),
                
                Field('market_id','string',default=''),
                Field('market_name','string','string',default=''),
                
                Field('order_date','date',requires=IS_NOT_EMPTY(),default=current_date), #visit_date
                Field('order_datetime','datetime',default=date_fixed),   #submit_date
                
                Field('delivery_date','date',default=current_date),#extra
                Field('collection_date','date',default=current_date),
                Field('payment_mode','string',default='CASH',requires=IS_IN_SET(('CASH','CHEQUE','PAY ORDER','CREDIT'))), #extra #cash / Credit /Bank Draft/Pay order
                
                Field('area_id','string',default=''),#route_id
                Field('area_name','string',default=''),#route_name    
                Field('level0_id','string',default=''),
                Field('level0_name','string',default=''),
                Field('level1_id','string',default=''),
                Field('level1_name','string',default=''),
                Field('level2_id','string',default=''),
                Field('level2_name','string',default=''),
                Field('level3_id','string',default=''),
                Field('level3_name','string',default=''),
                
                Field('status','string',default='Submitted',), # Draft / Submitted / Invoiced / Cancelled  
                
                Field('invoice_ref','integer',default=0), #extra                
                #detail-----
                Field('order_media','string',default=''), #extra # SMS , APP, WAP, MANUAL 
                Field('device_user_agent','string',default=''),#extra
                Field('ip_ref','string',default=''),#extra
                
                Field('ym_date','date', default=first_currentDate),#first_date 
                
                Field('depot_status','string',default='0'),
                Field('ho_status','string',default='0'),#extra
                Field('flag_depot_stock','integer',default=0), #extra
                Field('flag_data','string',default='0'), #extra #used for invoice processing rules
                
                # New
                Field('visit_type', 'string', default=''),#Scheduled,Unscheduled   
                Field('user_type', 'string', default=''),#rep/sup
                Field('mobile_no', 'string', default=''),
                Field('client_cat','string',default=''),
                Field('start_time', 'datetime', default=datetime_fixed),
                Field('end_time', 'datetime', default=datetime_fixed),
                Field('lat_long', 'string', default='0'),
                Field('location_detail', 'string', default='-'),
                Field('last_location', 'string', default='0'),
                Field('visit_image', 'string', default=''),
                Field('promo_ref', 'integer',default=0),#0=No,1=Yes
                #field2 used for In Process Status
                signature,
                migrate=False
                )

db.define_table('sm_order',
                Field('cid','string',requires=IS_NOT_EMPTY()), #PK
                Field('vsl','integer',default=0),                
                Field('depot_id','string',requires=IS_NOT_EMPTY()), #PK
                Field('depot_name','string',default=''),
                Field('sl','integer',requires=IS_NOT_EMPTY(),default=0), #PK
                Field('store_id','string',default=''),
                Field('store_name','string',default=''),
                
                Field('client_id','string',default=''),#old
                Field('client_name','string',default=''),#old
                Field('rep_id','string',default=''),#old
                Field('rep_name','string',default=''),#old
                
                Field('market_id','string',default=''),
                Field('market_name','string','string',default=''),
                
                Field('order_date','date',requires=IS_NOT_EMPTY(),default=current_date),#old
                Field('order_datetime','datetime',default=date_fixed),#old
                Field('delivery_date','date'),#old
                Field('collection_date','date',default=current_date),
                Field('payment_mode','string',default='CASH',requires=IS_IN_SET(('CASH','CHEQUE','PAY ORDER','CREDIT'))),#old #cash / Credit /Bank Draft/Pay order
                
                Field('area_id','string',default=''),#old
                Field('area_name','string',default=''),#old
                Field('level0_id','string',default=''),
                Field('level0_name','string',default=''),
                Field('level1_id','string',default=''),
                Field('level1_name','string',default=''),
                Field('level2_id','string',default=''),
                Field('level2_name','string',default=''),
                Field('level3_id','string',default=''),
                Field('level3_name','string',default=''),
                
                Field('status','string',default='Draft',),#old # Draft / Submitted / Invoiced / Cancelled         
                Field('invoice_ref','integer',default=0), #old
                
                #detail-----
                Field('item_id','string',requires=IS_NOT_EMPTY()), #PK
                Field('item_name','string',default=''),
                Field('category_id','string',default=''),
                Field('category_id_sp','string',default=''),
                Field('quantity','integer',requires=[IS_NOT_EMPTY(),IS_INT_IN_RANGE(1, 999999)]),
                Field('price','double',default=0.0),
                Field('item_vat','double',default=0.0),                
                Field('item_unit','string',default=''),
                Field('item_carton','integer',default=0),
                
                Field('order_media','string',default=''),#old # SMS , APP, WAP, MANUAL 
                Field('device_user_agent','string',default=''),#old
                Field('ip_ref','string',default=''), #old
                Field('ym_date','date', default=first_currentDate),#old #first_date 
                
                Field('depot_status','string',default='0'),
                Field('ho_status','string',default='0'),
                
                Field('flag_depot_stock','integer',default=0), 
                Field('flag_data','string',default='0'), #used for invoice processing rules                
                signature,
                migrate=False
                )

#========================Invoice=================================
db.define_table('sm_invoice_head',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid), 
                Field('depot_id','string',requires=IS_NOT_EMPTY()),
                Field('depot_name','string',default=''), 
                Field('sl','integer',requires=IS_NOT_EMPTY(),default=0), 
                Field('store_id','string',default=''),
                Field('store_name','string',default=''),
                
                Field('order_sl','integer',default=0),
                Field('order_datetime','datetime'),
                
                Field('delivery_date','date',requires=IS_NOT_EMPTY(),default=current_date),
                Field('payment_mode','string',default=''), #'CASH','CREDIT'
                Field('credit_note','string',default=''),
                
                Field('client_id','string',default=''),
                Field('client_name','string',default=''),
                Field('rep_id','string',default=''),
                Field('rep_name','string',default=''),
                
                Field('market_id','string',default=''),
                Field('market_name','string','string',default=''),
                
                Field('d_man_id','string',default=''),
                Field('d_man_name','string',default=''),
                
                Field('area_id','string',default=''),
                Field('area_name','string',default=''),
                Field('level0_id','string',default=''),
                Field('level0_name','string',default=''),
                Field('level1_id','string',default=''),
                Field('level1_name','string',default=''),
                Field('level2_id','string',default=''),
                Field('level2_name','string',default=''),
                Field('level3_id','string',default=''),
                Field('level3_name','string',default=''),
                
                Field('cl_category_id','string',default=''),
                Field('cl_category_name','string',default=''),
                Field('cl_sub_category_id','string',default=''),
                Field('cl_sub_category_name','string',default=''),
                
                Field('special_rsm_code','string',default=''),
                Field('special_fm_code','string',default=''),
                Field('special_territory_code','string',default=''),
                
                Field('status','string',default='Submitted'), # Draft / Invoiced /  Delivered /Part Delivered/ Delivered On Demand / Returned / Blocked /Cancelled                            
                
                Field('invoice_media','string',default=''), # SMS , APP, WAP, MANUAL ,OPENING
                Field('device_user_agent','string',default=''),
                Field('ip_ref','string',default=''), 
                Field('shipment_no','string',default=''), #new
                
                Field('actual_total_tp','double',default=0),                
                Field('regular_disc_tp','double',default=0),
                Field('flat_disc_tp','double',default=0),
                Field('approved_disc_tp','double',default=0),
                Field('others_disc_tp','double',default=0),
                Field('no_disc_tp','double',default=0),
                
                Field('ret_actual_total_tp','double',default=0),    #New *
                Field('ret_regular_disc_tp','double',default=0),    #New *
                Field('ret_flat_disc_tp','double',default=0),       #New *
                Field('ret_approved_disc_tp','double',default=0),   #New *
                Field('ret_others_disc_tp','double',default=0),     #New *
                
                Field('total_amount','double',default=0),#with vat (itemAmt+vatAmt-discount)
                Field('discount','double',default=0), # regular discount
                Field('vat_total_amount','double',default=0),
                Field('collection_amount','double',default=0),#applied amount
                Field('discount_precent','double',default=0),    #discount_percent            
                Field('adjust_amount','double',default=0),#payment adjustment amount                
                
                Field('return_tp','double',default=0),
                Field('return_vat','double',default=0),
                Field('return_discount','double',default=0),  
                
                Field('sp_discount','double',default=0), # special discount for flat+approved+others           
                Field('sp_flat','double',default=0), # special discount for flat   
                Field('sp_approved','double',default=0), # special discount for approved   
                Field('sp_others','double',default=0), # special discount for others    
                
                Field('return_sp_discount','double',default=0), # special discount for flat, approved rate and others
                Field('ret_sp_flat','double',default=0),    #New *
                Field('ret_sp_approved','double',default=0),#New *
                Field('ret_sp_others','double',default=0),  #New *
                
                Field('return_count','integer',default=0),
                
                Field('previous_ost_amt','double',default=0),
                Field('client_limit_amt','double',default=0),#client credit limit amount from approved credit
                
                #detail-----                
                Field('ym_date','date'), 
                
                #---------- Invoice Date and month
                Field('invoice_date','date'),
                Field('invoice_ym_date','date'),
                
                Field('depot_status','string',default='0'),
                Field('ho_status','string',default='0'),
                
                Field('flag_depot_stock','integer',default=0),#not used
                Field('flag_depot_stock_balance','integer',default=0),  
                Field('flag_data','string',default='0'),
                Field('client_limit_over','integer',default=0),#0=under limit, 1=over limit 
                Field('empty_batch_flag','integer',default=0),#0=not empty batch id, 1=empty batch id 
                Field('acknowledge_flag','integer',default=0),#0=not acknowledge, 1=acknowledged
                Field('promo_ref', 'integer',default=0),    #0=No,1=Yes
                Field('inv_pending_flag', 'integer',default=0),    #0=No,1=Yes
                
                Field('rpt_trans_flag', 'integer',default=0),    #0=No,1=Yes, used for transaction table
                
                Field('posted_on','datetime'),
                Field('posted_by','string',default=''),
                
                signature,
                migrate=False
                )

db.define_table('sm_invoice',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid), 
                Field('depot_id','string',requires=IS_NOT_EMPTY()),
                Field('depot_name','string',default=''), 
                Field('sl','integer',requires=IS_NOT_EMPTY(),default=0), 
                Field('store_id','string',default=''),
                Field('store_name','string',default=''),
                
                Field('order_sl','integer',default=0),#old
                Field('order_datetime','datetime'),#old
                Field('delivery_date','date',requires=IS_NOT_EMPTY(),default=current_date),#old
                
                Field('payment_mode','string',default=''), #'CASH','CREDIT'
                Field('credit_note','string',default=''),
                
                Field('client_id','string',default=''),#old
                Field('client_name','string',default=''),#old
                Field('rep_id','string',default=''),#old
                Field('rep_name','string',default=''),#old
                
                Field('market_id','string',default=''),
                Field('market_name','string','string',default=''),
                
                Field('d_man_id','string',default=''),
                Field('d_man_name','string',default=''),
                
                Field('area_id','string',default=''),#old
                Field('area_name','string',default=''),#old
                Field('level0_id','string',default=''),
                Field('level0_name','string',default=''),
                Field('level1_id','string',default=''),
                Field('level1_name','string',default=''),
                Field('level2_id','string',default=''),
                Field('level2_name','string',default=''),
                Field('level3_id','string',default=''),
                Field('level3_name','string',default=''),
                
                Field('cl_category_id','string',default=''),
                Field('cl_category_name','string',default=''),
                Field('cl_sub_category_id','string',default=''),
                Field('cl_sub_category_name','string',default=''),
                
                Field('special_rsm_code','string',default=''),
                Field('special_fm_code','string',default=''),
                Field('special_territory_code','string',default=''),
                
                Field('invoice_media','string',default=''),#old # SMS , APP, WAP, MANUAL
                Field('device_user_agent','string',default=''),#old
                Field('ip_ref','string',default=''), #old
                Field('discount','double',default=0), # invoice (BD) regular discount
                Field('ym_date','date'), #old
                
                #---------- Invoice Date and month
                Field('invoice_date','date'),
                Field('invoice_ym_date','date'),
                
                #detail-----
                Field('item_id','string',default=''), #PK
                Field('item_name','string',default=''),
                Field('batch_id','string',default=''),                
                Field('category_id','string',default=''),
                Field('actual_tp','double',default=0),
                Field('actual_vat','double',default=0),
                Field('quantity','integer',requires=IS_INT_IN_RANGE(0, 999999),default=0),
                Field('bonus_qty','integer',requires=IS_INT_IN_RANGE(0, 999999),default=0),
                Field('price','double',default=0), #flat,special
                Field('item_vat','double',default=0),
                Field('item_unit','string',default=''),
                Field('item_carton','integer',default=0),
                
                Field('return_qty','integer',default=0),
                Field('return_bonus_qty','integer',default=0),
                Field('return_rate','double',default=0), #Unused
                
                Field('sp_discount_item','double',default=0),#Unused
                Field('return_sp_discount_item','double',default=0),#Unused
                
                Field('promotion_type','string',default=''), #new field *during process
                Field('bonus_applied_on_qty','integer',default=0), #new field *during process(item wise same qty,batch wise not different)
                Field('circular_no','string',default=''), #new field *during process
                
                Field('discount_type','string',default=''),     #new field
                Field('item_discount','double',default=0),      #new field
                Field('item_discount_percent','double',default=0),   #new field *                
                Field('discount_type_quantity','integer',default=0), #new field *
                Field('ret_discount_type_quantity','integer',default=0), #new *
                
                Field('short_note','string',default=''),
                Field('status','string',default='Submitted'),
                
                #---------- Invoice Date and month
                Field('depot_status','string',default='0'),
                Field('ho_status','string',default='0'),
                
                Field('flag_depot_stock','integer',default=0),#not used
                Field('flag_depot_stock_balance','integer',default=0),  
                Field('flag_data','string',default='0'),#not used
                
                Field('posted_on','datetime'),
                Field('posted_by','string',default=''),
                
                signature,
                migrate=False
                )

#========================return=================================
db.define_table('sm_return_head',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('depot_id','string',requires=IS_NOT_EMPTY()),#PK
                Field('depot_name','string',default=''),
                Field('sl','integer',requires=IS_NOT_EMPTY(),default=0),#PK
                Field('store_id','string',default=''),
                Field('store_name','string',default=''),
                
                Field('client_id','string',default=''),
                Field('client_name','string',default=''),
                Field('rep_id','string',default=''),
                Field('rep_name','string',default=''),
                
                Field('market_id','string',default=''),
                Field('market_name','string','string',default=''),                
                Field('d_man_id','string',default=''),
                Field('d_man_name','string',default=''),
                Field('shipment_no','string',default=''),
                Field('invoice_date','date'),
                Field('invoice_ym_date','date'),
                
                Field('return_date','date',requires=IS_NOT_EMPTY(),default=current_date),
                Field('ret_reason','string',default=''),#DAMAGED,EXPIRED,SHOP-CLOSED,EXCHANGED
                
                Field('order_sl','integer',default=0),
                Field('invoice_sl','integer',default=0),
                
                Field('area_id','string',default=''),
                Field('area_name','string',default=''),
                Field('level0_id','string',default=''),
                Field('level0_name','string',default=''),
                Field('level1_id','string',default=''),
                Field('level1_name','string',default=''),
                Field('level2_id','string',default=''),
                Field('level2_name','string',default=''),
                Field('level3_id','string',default=''),
                Field('level3_name','string',default=''),
                
                Field('cl_category_id','string',default=''),
                Field('cl_category_name','string',default=''),
                Field('cl_sub_category_id','string',default=''),
                Field('cl_sub_category_name','string',default=''),
                Field('special_territory_code','string',default=''),
                
                Field('status','string',default='Draft'), # Draft / Returned / Cancelled
                
                Field('order_media','string',default=''), # sms , app, wap, manual 
                Field('device_user_agent','string',default=''),
                Field('ip_ref','string',default=''), 
                
                Field('inv_actual_total_tp','double',default=0),
                Field('inv_regular_disc_tp','double',default=0),
                Field('inv_flat_disc_tp','double',default=0),
                Field('inv_approved_disc_tp','double',default=0),
                Field('inv_others_disc_tp','double',default=0),
                Field('inv_no_disc_tp','double',default=0),
                
                Field('ret_actual_total_tp','double',default=0),    #New *
                Field('ret_regular_disc_tp','double',default=0),    #New *
                Field('ret_flat_disc_tp','double',default=0),       #New *
                Field('ret_approved_disc_tp','double',default=0),   #New *
                Field('ret_others_disc_tp','double',default=0),     #New *
                
                Field('total_amount','double',default=0),# Return net (itemAmt+vatAmt-discount)                
                Field('vat_total_amount','double',default=0),
                Field('discount','double',default=0),   #Return regular discount
                
                #-----------------
                Field('inv_vat_total_amount','double',default=0),
                Field('inv_discount','double',default=0),
                Field('inv_discount_precent','double',default=0),    # invoice regular discount_percent *new
                Field('prev_return_discount','double',default=0),
                
                Field('sp_discount','double',default=0),    #return sp discount           
                Field('ret_sp_flat','double',default=0),    #New *
                Field('ret_sp_approved','double',default=0),#New *
                Field('ret_sp_others','double',default=0),  #New *
                
                Field('inv_sp_discount','double',default=0),
                Field('prev_return_sp_discount','double',default=0),
                
                Field('inv_sp_flat','double',default=0), # special discount for flat   *new
                Field('inv_sp_approved','double',default=0), # special discount for approved   *new
                Field('inv_sp_others','double',default=0), # special discount for others *new
                
                #--------------
                Field('ym_date','date'),
                
                Field('depot_status','string',default='0'),
                Field('ho_status','string',default='0'),
                
                Field('flag_depot_stock','integer',default=0),
                Field('flag_depot_stock_balance','integer',default=0),  
                Field('flag_data','string',default='0'),    
                
                Field('rpt_trans_flag', 'integer',default=0),    #0=No,1=Yes, used for transaction table
                
                Field('returned_on','datetime'),
                Field('returned_by','string',default=''),
                
                signature,
                migrate=False
                )

db.define_table('sm_return',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('depot_id','string',requires=IS_NOT_EMPTY()),#PK
                Field('depot_name','string',default=''),
                Field('sl','integer',requires=IS_NOT_EMPTY(),default=0),#PK
                Field('store_id','string',default=''),
                Field('store_name','string',default=''),
                
                Field('client_id','string',default=''),
                Field('client_name','string',default=''),
                Field('rep_id','string',default=''),
                Field('rep_name','string',default=''),
                
                Field('market_id','string',default=''),
                Field('market_name','string','string',default=''),                
                Field('d_man_id','string',default=''),
                Field('d_man_name','string',default=''),
                Field('shipment_no','string',default=''),
                Field('invoice_date','date'),
                Field('invoice_ym_date','date'),
                
                Field('return_date','date',requires=IS_NOT_EMPTY(),default=current_date),
                Field('ret_reason','string',default=''),#DAMAGED,EXPIRED,SHOP-CLOSED,EXCHANGED
                
                Field('order_sl','integer',default=0),
                Field('invoice_sl','integer',default=0),
                
                Field('area_id','string',default=''),
                Field('area_name','string',default=''),
                Field('level0_id','string',default=''),
                Field('level0_name','string',default=''),
                Field('level1_id','string',default=''),
                Field('level1_name','string',default=''),
                Field('level2_id','string',default=''),
                Field('level2_name','string',default=''),
                Field('level3_id','string',default=''),
                Field('level3_name','string',default=''),
                
                Field('cl_category_id','string',default=''),
                Field('cl_category_name','string',default=''),
                Field('cl_sub_category_id','string',default=''),
                Field('cl_sub_category_name','string',default=''),
                Field('special_territory_code','string',default=''),
                
                Field('status','string',default='Draft'), # Draft / Returned / Cancelled
                
                Field('order_media','string',default=''), # sms , app, wap, manual 
                Field('device_user_agent','string',default=''),
                Field('ip_ref','string',default=''), 
                Field('discount','double',default=0),
                
                Field('item_id','string',requires=IS_NOT_EMPTY()),                
                Field('item_name','string',requires=IS_NOT_EMPTY()),
                Field('batch_id','string',default=''),
                Field('category_id','string',default=''),
                Field('actual_tp','double',default=0),
                Field('actual_vat','double',default=0),
                Field('quantity','integer',requires=[IS_NOT_EMPTY(error_message='enter quantity'),IS_INT_IN_RANGE(1, 999999,error_message='enter valid quantity')]),
                Field('bonus_qty','integer',requires=IS_INT_IN_RANGE(0, 999999),default=0),
                Field('price','double',default=0),
                Field('item_vat','double',default=0),
                Field('item_unit','string',default=''),
                Field('item_carton','integer',default=0),
                
                Field('inv_promotion_type','string',default=''), #new
                Field('inv_bonus_applied_on_qty','integer',default=0), #new
                Field('inv_circular_no','string',default=''), #new
                
                Field('discount_type','string',default=''), #invoice discount type
                Field('item_discount','double',default=0),  #invoice item discount                
                Field('inv_item_discount_percent','double',default=0),   #new
                Field('inv_discount_type_quantity','integer',default=0), #new *
                
                Field('return_item_discount','double',default=0),   #adjustment new
                Field('ret_discount_type_quantity','integer',default=0), #new *
                
                Field('short_note','string',default=''),
                
                #-------------------
                Field('inv_quantity','integer',default=0),
                Field('inv_bonus_qty','integer',default=0),
                Field('inv_price','double',default=0),
                Field('inv_item_vat','double',default=0),
                
                Field('prev_return_qty','integer',default=0),
                Field('prev_return_bonus_qty','integer',default=0),
                
                Field('inv_discount','double',default=0),
                Field('prev_return_discount','double',default=0),
                Field('invdet_rowid','integer',default=0),#Invoice Details Row id used to update invoice details records
                #------------------
                
                Field('sp_discount_item','double',default=0),#item wise special discount
                Field('inv_sp_discount_item','double',default=0),#item wise special discount
                Field('prev_return_sp_discount_item','double',default=0),#item wise special discount return
                
                Field('ym_date','date'),
                
                Field('depot_status','string',default='0'),
                Field('ho_status','string',default='0'),
                
                Field('flag_depot_stock','integer',default=0),
                Field('flag_depot_stock_balance','integer',default=0),  
                Field('flag_data','string',default='0'),              
                
                Field('returned_on','datetime'),
                Field('returned_by','string',default=''),
                
                signature,
                migrate=False
                )

db.define_table('sm_return_cancel',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('depot_id','string',requires=IS_NOT_EMPTY()),#PK
                Field('depot_name','string',default=''),
                Field('sl','integer',requires=IS_NOT_EMPTY(),default=0),#PK
                Field('store_id','string',default=''),
                Field('store_name','string',default=''),
                
                Field('client_id','string',default=''),
                Field('client_name','string',default=''),
                Field('rep_id','string',default=''),
                Field('rep_name','string',default=''),
                
                Field('market_id','string',default=''),
                Field('market_name','string','string',default=''),                
                Field('d_man_id','string',default=''),
                Field('d_man_name','string',default=''),
                Field('shipment_no','string',default=''),
                Field('invoice_date','date'),
                Field('invoice_ym_date','date'),
                
                Field('return_date','date',requires=IS_NOT_EMPTY(),default=current_date),
                Field('ret_reason','string',default=''),#DAMAGED,EXPIRED,SHOP-CLOSED,EXCHANGED
                
                Field('order_sl','integer',default=0),
                Field('invoice_sl','integer',default=0),
                
                Field('area_id','string',default=''),
                Field('area_name','string',default=''),
                Field('level0_id','string',default=''),
                Field('level0_name','string',default=''),
                Field('level1_id','string',default=''),
                Field('level1_name','string',default=''),
                Field('level2_id','string',default=''),
                Field('level2_name','string',default=''),
                Field('level3_id','string',default=''),
                Field('level3_name','string',default=''),
                
                Field('cl_category_id','string',default=''),
                Field('cl_category_name','string',default=''),
                Field('cl_sub_category_id','string',default=''),
                Field('cl_sub_category_name','string',default=''),
                Field('special_territory_code','string',default=''),
                
                Field('status','string',default='Draft'), # Draft / Returned / Cancelled
                
                Field('order_media','string',default=''), # sms , app, wap, manual 
                Field('device_user_agent','string',default=''),
                Field('ip_ref','string',default=''), 
                Field('discount','double',default=0),
                
                Field('item_id','string',requires=IS_NOT_EMPTY()),                
                Field('item_name','string',requires=IS_NOT_EMPTY()),
                Field('batch_id','string',default=''),
                Field('category_id','string',default=''),
                Field('actual_tp','double',default=0),
                Field('actual_vat','double',default=0),
                Field('quantity','integer',requires=[IS_NOT_EMPTY(error_message='enter quantity'),IS_INT_IN_RANGE(1, 999999,error_message='enter valid quantity')]),
                Field('bonus_qty','integer',requires=IS_INT_IN_RANGE(0, 999999),default=0),
                Field('price','double',default=0),
                Field('item_vat','double',default=0),
                Field('item_unit','string',default=''),
                Field('item_carton','integer',default=0),
                
                Field('inv_promotion_type','string',default=''), #new
                Field('inv_bonus_applied_on_qty','integer',default=0), #new
                Field('inv_circular_no','string',default=''), #new
                
                Field('discount_type','string',default=''), #invoice discount type
                Field('item_discount','double',default=0),  #invoice item discount
                
                Field('inv_item_discount_percent','double',default=0),   #new           
                Field('inv_discount_type_quantity','integer',default=0), #new *
                
                Field('return_item_discount','double',default=0),   #adjustment new
                Field('ret_discount_type_quantity','integer',default=0), #new *
                
                Field('short_note','string',default=''),
                
                #-------------------
                Field('inv_quantity','integer',default=0),
                Field('inv_bonus_qty','integer',default=0),
                Field('inv_price','double',default=0),
                Field('inv_item_vat','double',default=0),
                
                Field('prev_return_qty','integer',default=0),
                Field('prev_return_bonus_qty','integer',default=0),
                
                Field('inv_discount','double',default=0),
                Field('prev_return_discount','double',default=0),
                Field('invdet_rowid','integer',default=0),#Invoice Details Row id used to update invoice details records
                #------------------
                
                Field('sp_discount_item','double',default=0),#item wise special discount
                Field('inv_sp_discount_item','double',default=0),#item wise special discount
                Field('prev_return_sp_discount_item','double',default=0),#item wise special discount return
                
                Field('ym_date','date'),
                
                Field('depot_status','string',default='0'),
                Field('ho_status','string',default='0'),
                
                Field('flag_depot_stock','integer',default=0),
                Field('flag_depot_stock_balance','integer',default=0),  
                Field('flag_data','string',default='0'),              
                
                Field('returned_on','datetime'),
                Field('returned_by','string',default=''),
                
                signature,
                migrate=False
                )

#======================== Payment collection
db.define_table('sm_payment_collection',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid), 
                Field('depot_id','string',requires=IS_NOT_EMPTY()),
                Field('depot_name','string',default=''), 
                Field('sl','integer',requires=IS_NOT_EMPTY(),default=0), #Invoice SL
                Field('head_rowid','integer',default=0),
                Field('store_id','string',default=''),
                Field('store_name','string',default=''),
                
                Field('order_sl','integer',default=0),
                Field('order_datetime','datetime'),
                
                Field('delivery_date','date',requires=IS_NOT_EMPTY(),default=current_date),
                Field('payment_mode','string',default=''), #Invoice term #Cash / Credit
                Field('credit_note','string',default=''),
                Field('payment_type','string',default=''), #'CASH','CHEQUE','PAY ORDER','CREDIT', DD/ Bank Draft
                
                Field('client_id','string',default=''),
                Field('client_name','string',default=''),
                Field('rep_id','string',default=''),
                Field('rep_name','string',default=''),
                Field('market_id','string',default=''),
                Field('market_name','string','string',default=''),
                
                Field('d_man_id','string',default=''),
                Field('d_man_name','string',default=''),
                
                Field('area_id','string',default=''),
                Field('area_name','string',default=''),
                
                Field('level0_id','string',default=''),
                Field('level0_name','string',default=''),
                Field('level1_id','string',default=''),
                Field('level1_name','string',default=''),
                Field('level2_id','string',default=''),
                Field('level2_name','string',default=''),
                Field('level3_id','string',default=''),
                Field('level3_name','string',default=''),
                
                Field('cl_category_id','string',default=''),
                Field('cl_category_name','string',default=''),
                Field('cl_sub_category_id','string',default=''),
                Field('cl_sub_category_name','string',default=''),
                Field('special_territory_code','string',default=''),
                
                #---------- Invoice Date and month
                Field('invoice_date','date'),
                Field('invoice_ym_date','date'),
                
                #detail-----    
                Field('collection_date','date',requires=IS_NOT_EMPTY(),default=current_date),#transaction date
                Field('ym_date','date'), #collection ym date
                
                Field('collection_batch','string',default=''),
                Field('collection_note','string',default=''),
                Field('shipment_no','string',default=''),
                Field('doc_number','string',default=''),#unused
                Field('receipt_description','string',default=''),
                
                Field('transaction_type','string',default=''),#Payment=MR,Adjustment(Positive,Negative)
                Field('transaction_cause','string',default=''),
                Field('collection_flag','integer',default=0),  #MR,Collection Error, Entry Error =1 ,otherwise (BAD DEBTS,VAT AIT Etc.)=0
                
                Field('total_inv_amount','double',default=0),
                Field('receivable_amount','double',default=0),# Receivable at the time of MR
                Field('collection_amount','double',default=0),# MR,Adjustment amount (transaction amount)
                
                Field('payment_collection_date','date',requires=IS_NOT_EMPTY(),default=current_date),#payment date
                Field('payment_ym_date','date'), #payment ym date
                
                Field('status','string',default='Draft'), # Posted
                
                Field('rpt_trans_flag', 'integer',default=0),    #0=No,1=Yes, used for transaction table
                
                signature,
                migrate=False
                )

#======================Payment from client========================
db.define_table('sm_client_payment',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('depot_id','string',requires=IS_NOT_EMPTY()),
                Field('sl','integer',requires=IS_NOT_EMPTY(),default=0),
                
                Field('rep_id','string',requires=IS_NOT_EMPTY()),
                Field('rep_name','string',default=''),
                Field('client_id','string',requires=IS_NOT_EMPTY()),  
                Field('client_name','string',default=''),
                Field('area_id','string',default=''),
                
                Field('paytype','string',requires=IS_NOT_EMPTY()), 
                Field('pay_date','datetime',default=date_fixed),
                
                Field('amount','double',default=0),   
                Field('narration','text',default=''),
                
                Field('depot_status','string',default='0'),
                Field('ho_status','string',default='0'),    
                signature,
                migrate=False
                )
db.sm_client_payment.paytype.requires=IS_IN_SET(('CASH','CHEQUE','PAY ORDER','CREDIT'))

#====================== Depot Payment ========================
db.define_table('sm_depot_payment',
                Field('cid','string',requires=IS_NOT_EMPTY()), #PK
                Field('sl','integer',requires=IS_NOT_EMPTY(),default=0),
                Field('from_depot','string',requires=IS_NOT_EMPTY()),
                Field('depot_from_name','string',default=''),
                Field('to_depot','string',requires=IS_NOT_EMPTY()),
                Field('depot_to_name','string',default=''),
                Field('pay_date','datetime',default=date_fixed),
                Field('issue_ref','integer',default=0),
                Field('receive_ref','integer',default=0),  
                Field('paytype','string',requires=IS_NOT_EMPTY()), 
                Field('amount','double',default=0),   
                Field('narration','text',default=''),
                
                Field('depot_status','string',default='0'),
                Field('ho_status','string',default='0'),           
                signature,
                migrate=False
                )
db.sm_depot_payment.paytype.requires=IS_IN_SET(('CASH','CHEQUE','PAY ORDER','CREDIT'))

#==================
db.define_table('sm_comp_mobile',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('mobile_no','bigint',requires=IS_NOT_EMPTY()),
                Field('user_type','string',default='rep'),
                migrate=False               
                )

#======================setting========================
db.define_table('sm_mobile_settings',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('sl','integer',requires=IS_NOT_EMPTY()),
                Field('s_key','string',requires=IS_NOT_EMPTY()),
                Field('s_value','string',default=''),
                Field('type','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(15,error_message='enter maximum 15 character')]),
                signature,
                migrate=False
                )

db.define_table('sm_mobile_settings_pharma',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('sl','integer',requires=IS_NOT_EMPTY()),
                Field('s_key','string',requires=IS_NOT_EMPTY()),
                Field('s_value','string',default=''),
                Field('type','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(15,error_message='enter maximum 15 character')]),
                signature,
                migrate=False
                )
#===================web setting-----------------
db.define_table('sm_web_settings',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('s_key','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(20,error_message='enter maximum 20 character')]),
                Field('s_value','integer',default=1),
                signature,
                migrate=False
                )
db.define_table('sm_settings_pharma',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('s_key','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(20,error_message='enter maximum 20 character')]),
                Field('s_value','string',default=''),
                signature,
                migrate=False
                )
#===================later-----------------
db.define_table('sm_settings',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('s_key','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(20,error_message='enter maximum 20 character')]),
                Field('s_value','string',default=''),
                signature,
                migrate=False
                )

db.define_table('sm_company_settings',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('http_pass','string',default=''),
                Field('subscription_model','string',default=''),
                Field('clean_Data','string',default=''),
                Field('keep_history','string',default=''),
                Field('subscription_date','date',requires=IS_NOT_EMPTY(),default=current_date),
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='ACTIVE'),
                Field('admin_mobile_no','string',default=''),
                Field('item_list','text',default=''),
                Field('item_list_mobile','text',default=''),
                
                Field('temp_item_list','text',default=''),
                
                signature,
                migrate=False
                )

#========================user========================================
db.define_table('sm_depot_user',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('user_id','string',requires=IS_NOT_EMPTY()),
                Field('depot_id','string',default=''),
                signature,
                migrate=False
                )


#===============================Download============================
db.define_table('sm_download_url',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('sl','integer',requires=IS_NOT_EMPTY()),
                Field('download_url','string',default=''),
                Field('update_url','string',default=''),
                Field('field1','string',default=''),
                Field('status','string',default='INACTIVE'),
                migrate=False
                )

db.define_table('sm_download_table',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('table_name','string',requires=IS_NOT_EMPTY()),
                Field('primary_key','string',default=''),
                Field('field_name','string',default=''),
                Field('insert_query','string',default=''),
                Field('delete_query','string',default=''),
                Field('update_query','string',default=''),
                migrate=False
                )

db.define_table('sm_search_date',
                Field('from_dt','date',default=first_currentDate),
                Field('to_dt','date',default=date_fixed),
                Field('from_date','datetime'),
                Field('to_date','datetime'),
                
                Field('from_dt_2','date',default=first_currentDate),
                Field('to_dt_2','date',default=date_fixed),
                Field('from_dt_3','date',default=first_currentDate),
                Field('to_dt_3','date',default=date_fixed),
                Field('from_dt_4','date',default=first_currentDate),
                Field('to_dt_4','date',default=date_fixed),
                Field('from_dt_5','date',default=first_currentDate),
                Field('to_dt_5','date',default=date_fixed),
                
                migrate=False
                )

#========================doctor====================
db.define_table('sm_doctor',
                Field('cid', 'string', requires=IS_NOT_EMPTY(), default=session.cid),
                Field('doc_id', 'string', requires=[IS_NOT_EMPTY(), IS_ALPHANUMERIC(error_message=T('must be alphanumeric(a-z,A-Z,0-9)!')), IS_LENGTH(20, error_message='enter maximum 20 character')]),
                Field('doc_name', 'string', requires=[IS_NOT_EMPTY(), IS_LENGTH(30, error_message='enter maximum 30 character')]),
                Field('specialty', 'string', requires=IS_LENGTH(30, error_message='enter maximum 30 character')),
                Field('degree', 'string', default='-'),
                Field('password', 'string', default='', requires=IS_LENGTH(minsize=3, maxsize=12)),
                Field('mobile', 'bigint', default=0, requires=IS_LENGTH(13, error_message='enter maximum 13 character')),
                Field('sync_code', 'integer', default=0),
                Field('des', 'text', requires=IS_LENGTH(100, error_message='enter maximum 100 character'), default=''),
                Field('status', 'string', requires=IS_IN_SET(('ACTIVE', 'INACTIVE')), default='ACTIVE'),
                Field('attached_institution', 'string', default=''),
                Field('designation', 'string', default=''),
                Field('dob', 'date'),
                Field('mar_day', 'date'),
                Field('doctors_category', 'string', default=''),
                
                signature,
                migrate=False
                )

#========================Doctor Gift
db.define_table('sm_doctor_gift',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),#PK
                Field('gift_id','string',requires=[IS_NOT_EMPTY(),IS_ALPHANUMERIC(error_message=T('must be alphanumeric(a-z,A-Z,0-9)!')),IS_LENGTH(20,error_message='enter maximum 20 character')]),
                Field('gift_name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='enter maximum 50 character')]),
                Field('des','string',requires=IS_LENGTH(100,error_message='enter maximum 100 character')),
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='ACTIVE'),
                signature,
                migrate=False
                )

#========================Doctor PPM
db.define_table('sm_doctor_ppm',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),#PK
                Field('gift_id','string',requires=[IS_NOT_EMPTY(),IS_ALPHANUMERIC(error_message=T('must be alphanumeric(a-z,A-Z,0-9)!')),IS_LENGTH(20,error_message='enter maximum 20 character')]),
                Field('gift_name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='enter maximum 50 character')]),
                Field('des','string',requires=IS_LENGTH(100,error_message='enter maximum 100 character')),
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='ACTIVE'),
                signature,
                migrate=False
                )

#========================doctor_area
db.define_table('sm_doctor_area',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('doc_id','string',requires=[IS_NOT_EMPTY(),IS_ALPHANUMERIC(error_message=T('must be alphanumeric(a-z,A-Z,0-9)!')),IS_LENGTH(20,error_message='enter maximum 20 character')]),
                Field('doc_name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='enter maximum 50 character')]),
                Field('area_id','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(20,error_message='enter maximum 20 character')]),
                Field('area_name','string',requires=IS_LENGTH(50,error_message='enter maximum 50 character'),default=''),
                Field('client_id','string',requires=IS_LENGTH(20,error_message='enter maximum 20 character'),default=''),
                Field('client_name','string',requires=IS_LENGTH(50,error_message='enter maximum 50 character'),default=''),
                Field('address','string',requires=IS_LENGTH(100,error_message='enter maximum 100 character'),default=''),
                Field('district', 'string', default=''),
                Field('thana', 'string', default=''),
                Field('depot_id','string',default=''),
                Field('latitude','integer',default=0),
                Field('longitude','integer',default=0),
                
                signature,
                migrate=False
                )#field2 used

#================================= Doctor visit plan
db.define_table('sm_doctor_visit_plan',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('rep_id', 'string', default=''),
                Field('rep_name', 'string', default=''),
                
                Field('first_date','date',default=date_fixed),
                Field('schedule_date','date',default=date_fixed),
                
                Field('doc_id', 'string', requires=IS_NOT_EMPTY()),                
                Field('doc_name', 'string', default=''),                
                Field('route_id', 'string', default=''),
                Field('route_name', 'string', default=''),                
                Field('depot_id', 'string', default=''),
                Field('depot_name', 'string', default=''),
                
                Field('level2_id', 'string', default=''),
                Field('level2_name', 'string', default=''),                
                Field('level1_id', 'string', default=''),
                Field('level1_name', 'string', default=''),
                Field('level0_id', 'string', default=''),
                Field('level0_name', 'string', default=''),
                
                Field('visited_flag', 'integer', default=0), #1=visited,0=Not visited ,#Mobile
                Field('visit_sl','integer',default=0),#Mobile
                Field('visit_date', 'date'),#Mobile
                Field('status', 'string', default='Submitted'),  #Submitted,Approved,Cancelled,Visited
                
                signature,
                migrate=False
                )

#========================doctor_visit
db.define_table('sm_doctor_visit',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('doc_id','string',requires=[IS_NOT_EMPTY(),IS_ALPHANUMERIC(error_message=T('must be alphanumeric(a-z,A-Z,0-9)!')),IS_LENGTH(20,error_message='enter maximum 20 character')]),
                Field('doc_name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='enter maximum 50 character')]),
                Field('rep_id','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(30,error_message='enter maximum 30 character')]),
                Field('rep_name','string',requires=IS_LENGTH(50,error_message='enter maximum 50 character'),default=''),
                Field('feedback','string',requires=IS_LENGTH(100,error_message='enter maximum 100 character'),default=''),
                Field('ho_status','string',requires=IS_LENGTH(50,error_message='enter maximum 50 character'),default=''),
                
                Field('route_id','string',requires=IS_LENGTH(20,error_message='enter maximum 20 character')),
                Field('route_name','string',default=''),
                
                Field('level0_id','string',default=''),
                Field('level0_name','string',default=''),
                Field('level1_id','string',default=''),
                Field('level1_name','string',default=''),
                Field('level2_id','string',default=''),
                Field('level2_name','string',default=''),
                Field('level3_id','string',default=''),
                Field('level3_name','string',default=''),
                
                Field('depot_id','string',default=''),
                
                Field('visit_dtime','datetime',default=date_fixed),
                Field('visit_date','date',default=date_fixed),
                Field('visit_firstdate','date',default=first_currentDate),
                Field('giftnsample','text',default=''),
                
                Field('latitude','string',default='0'),
                Field('longitude','string',default='0'),
                Field('location_detail','string',default='-'),
                Field('last_location', 'string', default='0'),
                signature,
                migrate=False
                )

#===========================doctor inbox
db.define_table('sm_doctor_inbox',
                Field('cid','string',requires=IS_NOT_EMPTY()), #PK
                Field('sl','integer',requires=IS_NOT_EMPTY()), #PK
                Field('mobile_no','string',default=''),
                Field('sms_date','datetime',default=date_fixed),
                Field('sms','string',requires=IS_NOT_EMPTY()), 
                Field('status','string',default='OK'),
                Field('error_in_sms','string',default=''),
                Field('ho_status','integer',default=0),
                signature,
                migrate=False
                )

#================================== Office
db.define_table('sm_notice',
                Field('cid','string',requires=IS_NOT_EMPTY()), #PK
                Field('sl','integer',requires=IS_NOT_EMPTY()), #PK
                Field('notice_date','datetime',default=date_fixed),
                Field('notice','string',default=''),                
                signature,
                migrate=False
                )

db.define_table('sm_attendance',
                Field('cid','string',requires=IS_NOT_EMPTY()), #PK
                Field('rep_id','string',requires=IS_NOT_EMPTY()), #PK
                Field('rep_name','string',requires=IS_NOT_EMPTY()),
                Field('attend_date','datetime',default=date_fixed),
                Field('in_time','datetime',default=date_fixed),#PK
                Field('out_time','datetime',default=date_fixed),
                Field('notice','string',default=''),                
                signature,
                migrate=False
                )

db.define_table('sm_paytype',
                Field('cid','string',requires=IS_NOT_EMPTY()), #PK
                Field('paytype','string',requires=IS_NOT_EMPTY()), #PK
                Field('detail','string',default=''),                
                signature,
                migrate=False
                )

#======================== Target
db.define_table('sm_target',
                Field('cid','string',requires=IS_NOT_EMPTY()), #PK
                Field('depot_id','string',requires=IS_NOT_EMPTY()), #PK
                Field('reporting_level_id','string',default=''),#unused
                Field('reporting_level_name','string',default=''),#unused
                Field('ym_date','date',requires=IS_NOT_EMPTY(),default=current_date),#PK
                Field('rep_id','string',requires=IS_NOT_EMPTY()),#PK
                Field('rep_name','string',default=''),
                
                Field('item_id','string',requires=IS_NOT_EMPTY()), #PK
                Field('item_name','string',default=''),
                
                Field('target_qty','integer',default=0),   
                Field('achievement_qty','integer',default=0),
                Field('target_amount','double',default=0),
                Field('achievement_amount','double',default=0),
                Field('ho_status','integer',default=0),
                Field('depot_status','integer',default=0),                
                signature,
                migrate=False
                )

#===========================INBOX============
db.define_table('sm_inbox',
                Field('cid','string',requires=IS_NOT_EMPTY()), #PK
                Field('sl','integer',requires=IS_NOT_EMPTY()), #PK
                Field('mobile_no','string',default=''),
                Field('sms_date','datetime',default=date_fixed),
                Field('sms','string',requires=IS_NOT_EMPTY()), 
                Field('status','string',default='OK'),
                Field('error_in_sms','string',default=''),
                Field('ho_status','integer',default=0),
                signature,
                migrate=False
                )
#field2 used for error submit, flag o for default and 1 for resubmit


#====================================
db.define_table('sm_tpcp_rules',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                                
                Field('campaign_ref','string',requires=IS_NOT_EMPTY()),
                Field('client_cat','string',requires=IS_NOT_EMPTY()),
                Field('from_date','date',requires=IS_NOT_EMPTY()),
                Field('to_date','date',requires=IS_NOT_EMPTY()),
                
                Field('for_any_item','string',requires=IS_NOT_EMPTY()),  # ANY/Item Code
                Field('from_amt_qty','integer',requires=IS_NOT_EMPTY(),default=0),
                Field('to_amt_qty','integer',requires=IS_NOT_EMPTY(),default=0),
                
                Field('bonus_type','string',requires=IS_IN_SET(('Item','DiscAmt','DiscPer'))),    #Item/DiscountAmt/DiscountPer
                
                Field('b_item_id1','string',default=''),
                Field('b_item_name1','string',default=''),
                Field('b_item_qty1','integer',default=0),
                
                Field('b_item_id2','string',default=''),
                Field('b_item_name2','string',default=''),
                Field('b_item_qty2','integer',default=0),
                
                Field('b_item_id3','string',default=''),
                Field('b_item_name3','string',default=''),
                Field('b_item_qty3','integer',default=0),
                
                Field('disc_amt_per','integer',default=0),
                
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='ACTIVE'),
                
                signature,
                migrate=False
                )

#==================================== 1. Approved Rate
db.define_table('sm_promo_approved_rate',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),                
                Field('client_id','string',requires=IS_NOT_EMPTY()),#customerID
                Field('client_name','string',default=''),
                
                Field('depot_id','string',default=''),
                Field('depot_name','string',default=''), 
                
                Field('from_date','date',requires=IS_NOT_EMPTY()),
                Field('to_date','date',requires=IS_NOT_EMPTY()),                
                Field('product_id','string',requires=IS_NOT_EMPTY()),
                Field('product_name','string',default=''),                
                Field('bonus_type','string',requires=IS_IN_SET(('Fixed','Percentage'))),                
                Field('fixed_percent_rate','double',default=0),                
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='ACTIVE'),
                
                signature,
                migrate=False
                )

#==================================== 2a. Product Bonus - head
db.define_table('sm_promo_product_bonus',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('from_date','date',requires=IS_NOT_EMPTY()),
                Field('to_date','date',requires=IS_NOT_EMPTY()),
                Field('min_qty','integer',default=0),
                Field('circular_number','string',default=''),
                Field('until_stock_last','string',requires=IS_IN_SET(('YES','NA')),default='NA'),
                Field('allowed_credit_inv','string',requires=IS_IN_SET(('YES','NO')),default='NO'),
                Field('regular_discount_apply','string',requires=IS_IN_SET(('YES','NO')),default='NO'),
                Field('status','string',requires=IS_IN_SET(('DRAFT','ACTIVE','INACTIVE')),default='DRAFT'),                
                signature,
                migrate=False
                )

#==================================== 2b. Product Bonus - product details
db.define_table('sm_promo_product_bonus_products',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('refrowid','integer',default=0),
                Field('circular_number','string',default=''),
                Field('from_date','date',requires=IS_NOT_EMPTY()),
                Field('to_date','date',requires=IS_NOT_EMPTY()),
                
                Field('product_id','string',requires=IS_NOT_EMPTY()),
                Field('product_name','string',default=''),
                Field('status','string',default=''),
                
                signature,
                migrate=False
                )

#==================================== 2c. Product Bonus - bonus details
db.define_table('sm_promo_product_bonus_bonuses',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('refrowid','integer',default=0),
                Field('circular_number','string',default=''),
                Field('from_date','date',requires=IS_NOT_EMPTY()),
                Field('to_date','date',requires=IS_NOT_EMPTY()), 
                
                Field('bonus_product_id','string',requires=IS_NOT_EMPTY()),
                Field('bonus_product_name','string',default=''),
                Field('bonus_qty','integer',default=0),
                Field('status','string',default=''),
                
                signature,
                migrate=False
                )

#==================================== 3. Special Rate
db.define_table('sm_promo_special_rate',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('from_date','date',requires=IS_NOT_EMPTY()),
                Field('to_date','date',requires=IS_NOT_EMPTY()),    
                Field('campaign_ref','string',requires=IS_NOT_EMPTY()),
                Field('product_id','string',requires=IS_NOT_EMPTY()),
                Field('product_name','string',default=''),    
                Field('mrp','double',default=0), #not used
                Field('tp','double',default=0),  #not used
                Field('vat','double',default=0), #not used
                Field('min_qty','integer',default=0),
                Field('special_rate_tp','double',default=0),  
                Field('special_rate_vat','double',default=0),  
                Field('allowed_credit_inv','string',requires=IS_IN_SET(('YES','NO')),default='NO'),
                Field('regular_discount_apply','string',requires=IS_IN_SET(('YES','NO')),default='NO'),
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='ACTIVE'),                
                signature,
                migrate=False
                )

#==================================== 4. Flat Rate
db.define_table('sm_promo_flat_rate',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('from_date','date',requires=IS_NOT_EMPTY()),
                Field('to_date','date',requires=IS_NOT_EMPTY()),    
                Field('campaign_ref','string',requires=IS_NOT_EMPTY()),
                Field('product_id','string',requires=IS_NOT_EMPTY()),
                Field('product_name','string',default=''),    
                Field('mrp','double',default=0),#not used
                Field('tp','double',default=0), #not used
                Field('vat','double',default=0),
                Field('min_qty','integer',default=0),
                Field('flat_rate','double',default=0),
                Field('allowed_credit_inv','string',requires=IS_IN_SET(('YES','NO')),default='NO'),
                Field('regular_discount_apply','string',requires=IS_IN_SET(('YES','NO')),default='NO'),
                Field('allow_bundle','string',requires=IS_IN_SET(('YES','NO')),default='NO'),
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='ACTIVE'),                
                signature,
                migrate=False
                )

#==================================== 5. Regular Discount
db.define_table('sm_promo_regular_discount',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('from_date','date',requires=IS_NOT_EMPTY()),
                Field('to_date','date',requires=IS_NOT_EMPTY()),    
                
                Field('min_amount','double',default=0),  
                Field('discount_precent','double',default=0),  
                Field('discount_amount','double',default=0),  #not used
                Field('circular_number','string',default=''),
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='ACTIVE'),                
                signature,
                migrate=False
                )
#==================================== 6. Declared Item
db.define_table('sm_promo_declared_item',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('approved_date','date',requires=IS_NOT_EMPTY()),
                Field('product_id','string',requires=IS_NOT_EMPTY()),
                Field('product_name','string',default=''),  
                
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='ACTIVE'),                
                signature,
                migrate=False
                )

#==================================== 1. Credit Policy (approved)
db.define_table('sm_cp_approved',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('approved_date','date',requires=IS_NOT_EMPTY()),
                Field('branch_id','string',default=''),
                Field('client_id','string',requires=IS_NOT_EMPTY()),
                Field('credit_amount','double',default=0),                
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='ACTIVE'),                
                signature,
                migrate=False
                )

#==================================== 2. Credit Policy (rsm)
db.define_table('sm_cp_rsm',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('approved_date','date',requires=IS_NOT_EMPTY()),
                Field('region_id','string',requires=IS_NOT_EMPTY()),
                Field('branch_id','string',requires=IS_NOT_EMPTY()),
                Field('credit_amount','double',default=0),
                
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='ACTIVE'),                
                signature,
                migrate=False
                )

#==================================== 3. Credit Policy (special)
db.define_table('sm_cp_special',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('approved_date','date',requires=IS_NOT_EMPTY()),
                Field('from_date','date',requires=IS_NOT_EMPTY()),
                Field('to_date','date',requires=IS_NOT_EMPTY()),
                Field('credit_type','string',requires=IS_NOT_EMPTY()),
                Field('region_id','string',requires=IS_NOT_EMPTY()),
                Field('branch_id','string',requires=IS_NOT_EMPTY()),
                Field('credit_amount','double',default=0),
                
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='ACTIVE'),                
                signature,
                migrate=False
                )

#====================================
db.define_table('sm_restricted_item',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                
                Field('item_id','string',requires=IS_NOT_EMPTY()),
                Field('item_name','string',default=''),
                Field('item_cat','string',default=''),
                Field('dist_price','double',default=0),
                Field('retail_price','double',default=0),
                Field('item_qty','integer',requires=IS_NOT_EMPTY(),default=0),       
                Field('auto_voucher','string',requires=IS_IN_SET(('YES','NO')),default='YES'),
                
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='ACTIVE'),
                
                signature,
                migrate=False
                )


#======================= Tp rules temp table (pk=cid+depotid+sl)
db.define_table('sm_tp_rules_temp_process',
                Field('cid','string',requires=IS_NOT_EMPTY()), 
                Field('depot_id','string',requires=IS_NOT_EMPTY()), 
                Field('depot_name','string',default=''),
                Field('sl','integer',default=0),
                Field('store_id','string',default=''),
                Field('store_name','string',default=''),
                
                Field('client_id','string',default=''),
                Field('client_name','string',default=''),
                Field('rep_id','string',default=''),
                Field('rep_name','string',default=''),   
                Field('market_id','string',default=''),
                Field('market_name','string','string',default=''),
                
                Field('order_date','date'), #visit_date
                Field('order_datetime','datetime'),   #submit_date       
                Field('delivery_date','date'),#extra
                Field('payment_mode','string',default='CASH'), #cash / Credit /Bank Draft/Pay order                
                Field('area_id','string',default=''),#route_id
                Field('area_name','string',default=''),#route_name 
                Field('order_media','string',default=''), #extra # SMS , APP, WAP, MANUAL                
                Field('ym_date','date'),#first_date     
                Field('client_cat','string',default=''),
                Field('note','string',default=''),
                
                #detail-----
                Field('item_id','string',requires=IS_NOT_EMPTY()),
                Field('item_name','string',default=''),
                Field('category_id','string',default=''),
                Field('quantity','integer',default=0),                
                Field('price','double',default=0.0),    #actual tp
                Field('item_vat','double',default=0.0), #actual vat
                Field('item_unit','string',default=''), 
                Field('item_carton','integer',default=0),
                
                Field('item_flag','integer',default=0), #used for invoice processing rules   
                Field('prio_flag','integer',default=0), #Priority rate
                Field('ar_flag','integer',default=0),   #approved rate
                Field('pb_flag','integer',default=0),   #product bonus
                Field('sr_flag','integer',default=0),   #special rate
                Field('fr_flag','integer',default=0),   #fixed rate
                Field('di_flag','integer',default=0),   #declared item
                Field('rd_flag','integer',default=0),   #regular discount
                
                migrate=False
                )

#======================= Tp rules temp table (pk=cid+depotid+sl)
db.define_table('sm_tp_rules_temp_process_manual',
                Field('cid','string',requires=IS_NOT_EMPTY()), 
                Field('depot_id','string',requires=IS_NOT_EMPTY()), 
                Field('depot_name','string',default=''),
                Field('sl','integer',default=0),
                Field('store_id','string',default=''),
                Field('store_name','string',default=''),
                
                Field('client_id','string',default=''),
                Field('client_name','string',default=''),
                Field('rep_id','string',default=''),
                Field('rep_name','string',default=''),
                Field('market_id','string',default=''),
                Field('market_name','string','string',default=''),
                
                Field('order_date','date'), #visit_date
                Field('order_datetime','datetime'),   #submit_date
                Field('delivery_date','date'),#extra
                Field('payment_mode','string',default='CASH'), #cash / Credit /Bank Draft/Pay order   
                Field('area_id','string',default=''),#route_id
                Field('area_name','string',default=''),#route_name
                Field('order_media','string',default=''), #extra # SMS , APP, WAP, MANUAL       
                Field('ym_date','date'),#first_date
                Field('client_cat','string',default=''),
                Field('note','string',default=''),
                
                #detail-----
                Field('item_id','string',requires=IS_NOT_EMPTY()),
                Field('item_name','string',default=''),
                Field('category_id','string',default=''),
                Field('actual_tp','double',default=0),
                Field('actual_vat','double',default=0),                
                Field('quantity','integer',default=0),                
                Field('price','double',default=0.0),
                Field('item_vat','double',default=0.0),
                
                Field('item_unit','string',default=''),
                Field('item_carton','integer',default=0),
                
                Field('item_flag','integer',default=0), #used for invoice processing rules    
                Field('prio_flag','integer',default=0), #Priority rate            
                Field('ar_flag','integer',default=0),   #approved rate
                Field('pb_flag','integer',default=0),   #product bonus
                Field('sr_flag','integer',default=0),   #special rate
                Field('fr_flag','integer',default=0),   #fixed rate
                Field('di_flag','integer',default=0),   #declared item
                Field('rd_flag','integer',default=0),   #regular discount
                
                migrate=False
                )
            
#======================= Tp rules temp table (pk=cid+depotid+sl)
db.define_table('sm_tp_rules_temp_return',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('depot_id','string',requires=IS_NOT_EMPTY()),
                Field('return_sl','integer',default=0),
                Field('invoice_sl','integer',default=0),
                Field('ret_rowid','integer',default=0),
                Field('store_id','string',default=''),
                Field('client_id','string',default=''),
                Field('order_date','date'),
                Field('delivery_date','date'),
                Field('payment_mode','string',default=''),
                Field('inv_discount','double',default=0.0),
                Field('prev_return_discount','double',default=0.0),
                Field('promo_ref','integer',default=0),
                Field('quantity','integer',default=0),
                
                #detail-----
                Field('item_id','string',default=''),
                Field('actual_tp','double',default=0),
                Field('actual_vat','double',default=0),
                
                Field('ret_price','double',default=0.0),
                Field('ret_item_vat','double',default=0.0),
                Field('inv_price','double',default=0.0),
                Field('inv_item_vat','double',default=0.0),
                
                Field('item_flag','integer',default=0), #used for invoice processing rules    
                Field('prio_flag','integer',default=0), #Priority rate            
                Field('ar_flag','integer',default=0),   #approved rate
                Field('pb_flag','integer',default=0),   #product bonus
                Field('sr_flag','integer',default=0),   #special rate
                Field('fr_flag','integer',default=0),   #fixed rate
                Field('di_flag','integer',default=0),   #declared item
                Field('rd_flag','integer',default=0),   #regular discount
                
                migrate=False
                )

#======================= Tp rules temp table (pk=cid+depotid+sl)
db.define_table('sm_tp_rules_temp_return_invoice',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('depot_id','string',requires=IS_NOT_EMPTY()),
                Field('return_sl','integer',default=0),
                Field('invoice_sl','integer',default=0),
                Field('ret_rowid','integer',default=0),                
                Field('discount','double',default=0.0),
                
                Field('item_id','string',default=''),
                Field('quantity','integer',default=0),
                Field('bonus_qty','integer',default=0),
                Field('price','double',default=0.0),
                Field('item_vat','double',default=0.0),                
                migrate=False
                )

#=================================
db.define_table('sm_merchandizing_item',
                Field('cid', 'string', requires=IS_NOT_EMPTY(), default=session.cid),
                Field('item_id', 'string', requires=IS_NOT_EMPTY()),
                Field('name', 'string', requires=IS_NOT_EMPTY()),
                Field('des', 'string', default=''),
                migrate=False
                )

#=================================
db.define_table('sm_visit_plan',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('rep_id', 'string', default=''),
                Field('rep_name', 'string', default=''),
                
                Field('first_date','date',default=date_fixed),
                Field('schedule_date','date',default=date_fixed),
                
                Field('client_id', 'string', requires=IS_NOT_EMPTY()),                
                Field('client_name', 'string', default=''),                
                Field('route_id', 'string', default=''),
                Field('route_name', 'string', default=''),                
                Field('depot_id', 'string', default=''),
                Field('depot_name', 'string', default=''),
                
                Field('level2_id', 'string', default=''),
                Field('level2_name', 'string', default=''),                
                Field('level1_id', 'string', default=''),
                Field('level1_name', 'string', default=''),
                Field('level0_id', 'string', default=''),
                Field('level0_name', 'string', default=''),
                
                Field('visited_flag', 'integer', default=0), #1=visited,0=Not visited ,#Mobile
                Field('visit_sl','integer',default=0),#Mobile
                Field('visit_date', 'date'),#Mobile
                Field('status', 'string', default='Submitted'),  #Submitted,Approved,Cancelled,Visited
                
                signature,
                migrate=False
                )

# ============ Visit table/ Order Head
db.define_table('visit_market_info',
                Field('cid', 'string', requires=IS_NOT_EMPTY(), default=session.cid),
                Field('SL', 'integer', requires=IS_NOT_EMPTY(), default=0),
                
                Field('brand_id', 'string', default=""),#not used
                Field('brand_name', 'string', default=""),
                
                Field('monthly_sales', 'integer',default=0),
                Field('stock', 'integer',default=0),
                Field('credit_amt', 'integer',default=0),
                Field('price', 'integer',default=0),
                Field('free_bag', 'integer',default=0),
                Field('retailer_commission', 'double',default=0),
                Field('trade_promotion', 'string', default=""),
                Field('remarks', 'string', default=""),
                
                #------ new
                Field('first_date', 'date', default=first_currentDate),
                Field('client_id', 'string', requires=IS_NOT_EMPTY()),
                Field('region_id', 'string',  default=""),
                Field('area_id', 'string',  default=""),
                Field('territory_id', 'string',  default=""),
                Field('market_id', 'string',  default=""),
                Field('monthly_last_flag','integer',default=1), #last=1,previous=0
                #-----
                
                migrate=False
                )

db.define_table('visit_merchandising',
                Field('cid', 'string', requires=IS_NOT_EMPTY(), default=session.cid),
                Field('SL', 'integer', requires=IS_NOT_EMPTY(), default=0), 
                
                Field('client_id', 'string', requires=IS_NOT_EMPTY()),
                Field('client_name', 'string', default=''),
                
                Field('m_item_id', 'string', requires=IS_NOT_EMPTY()),                
                Field('name', 'string', default=""),
                Field('qty', 'integer', default=0),
                
                Field('installation_date', 'date'),
                Field('new_flag', 'integer',default=0),#0,1 x
                Field('visible', 'string', default=""),#YES,NO
                Field('condition_value', 'string', default=""),#GOOD,BAD
                
                Field('dismantled', 'string', default=""),#YES/NO
                Field('last_flag','integer',default=0), #last=1,previous=0
                
                migrate=False
                )

db.define_table('trade_promotional_offer',
                Field('cid', 'string', requires=IS_NOT_EMPTY(), default=session.cid),
                Field('offer_name', 'string', requires=IS_NOT_EMPTY()),                
                Field('from_date', 'date',  requires=IS_NOT_EMPTY()),
                Field('to_date', 'date', requires=IS_NOT_EMPTY()),                
                Field('target_qty', 'integer', default=0),                
                Field('reward', 'string', default=''),
                Field('bonus_con', 'string', default=''),
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='ACTIVE'),
                
                migrate=False
                )

db.define_table('visit_client_offer',
                Field('cid', 'string', requires=IS_NOT_EMPTY(), default=session.cid),
                Field('vsl', 'integer', requires=IS_NOT_EMPTY()),
                
                Field('first_date', 'date', default=first_currentDate),
                Field('visit_date', 'date', default=date_fixed),
                
                Field('client_id', 'string', requires=IS_NOT_EMPTY()),
                Field('client_name', 'string', default=''),
                
                Field('offer_id', 'integer',requires=IS_NOT_EMPTY()),
                Field('offer_name', 'string', requires=IS_NOT_EMPTY()),
                
                Field('offer_from_date', 'date', requires=IS_NOT_EMPTY()),
                Field('offer_to_date', 'date', requires=IS_NOT_EMPTY()),                
                Field('last_flag','integer',default=0), #last=1,previous=0
                
                migrate=False
                )

db.define_table('target_vs_achievement',
                Field('cid', 'string', requires=IS_NOT_EMPTY(), default=session.cid),
                Field('first_date', 'date', default=first_currentDate),
                Field('target_date', 'date'),
                
                Field('client_id', 'string', requires=IS_NOT_EMPTY()),
                Field('client_name', 'string', default=''),
                Field('item_id', 'string', requires=IS_NOT_EMPTY()),
                Field('item_name', 'string', default=''),
                
                Field('region_id', 'string', default=''),
                Field('area_id', 'string', default=''),
                Field('territory_id', 'string', default=''),
                Field('market_id', 'string', default=''),                
                Field('depot_id', 'string', default=''),
                                
                Field('target_qty', 'integer', default=0),
                Field('achievement_qty', 'integer', default=0),
                
                migrate=False
                )

db.define_table('target_vs_achievement_field_force',
                Field('cid', 'string', requires=IS_NOT_EMPTY(), default=session.cid),
                Field('first_date', 'date', default=first_currentDate),                
                Field('target_year', 'integer', default=0),
                Field('target_month', 'integer', default=0),
                
                Field('rep_id', 'string', requires=IS_NOT_EMPTY()),
                Field('rep_name', 'string', default=''),
                
                Field('target_amount', 'double', default=0),
                Field('achievement_amount', 'double', default=0),
                
                migrate=False
                )

db.define_table('lifting_plan',
                Field('cid', 'string', requires=IS_NOT_EMPTY(), default=session.cid),
                Field('first_date', 'date', default=first_currentDate),
                Field('plan_date', 'date'),
                
                Field('distributor_id', 'string', requires=IS_NOT_EMPTY()),
                Field('distributor_name', 'string',  default=''),
                Field('super_depot_id', 'string', default=''),
                Field('super_depot_name', 'string', default=''),
                Field('mode', 'string', default=''),#Truck,Burge
                
                Field('t_1', 'integer', default=0),
                Field('a_1', 'integer', default=0),                
                Field('t_2', 'integer', default=0),
                Field('a_2', 'integer', default=0),
                Field('t_3', 'integer', default=0),
                Field('a_3', 'integer', default=0),
                Field('t_4', 'integer', default=0),
                Field('a_4', 'integer', default=0),
                Field('t_5', 'integer', default=0),
                Field('a_5', 'integer', default=0),
                Field('t_6', 'integer', default=0),
                Field('a_6', 'integer', default=0),
                Field('t_7', 'integer', default=0),
                Field('a_7', 'integer', default=0),
                Field('t_8', 'integer', default=0),
                Field('a_8', 'integer', default=0),
                Field('t_9', 'integer', default=0),
                Field('a_9', 'integer', default=0),
                Field('t_10', 'integer', default=0),
                Field('a_10', 'integer', default=0),
                Field('t_11', 'integer', default=0),
                Field('a_11', 'integer', default=0),
                Field('t_12', 'integer', default=0),
                Field('a_12', 'integer', default=0),
                Field('t_13', 'integer', default=0),
                Field('a_13', 'integer', default=0),
                Field('t_14', 'integer', default=0),
                Field('a_14', 'integer', default=0),
                Field('t_15', 'integer', default=0),
                Field('a_15', 'integer', default=0),
                Field('t_16', 'integer', default=0),
                Field('a_16', 'integer', default=0),
                Field('t_17', 'integer', default=0),
                Field('a_17', 'integer', default=0),
                Field('t_18', 'integer', default=0),
                Field('a_18', 'integer', default=0),
                Field('t_19', 'integer', default=0),
                Field('a_19', 'integer', default=0),
                Field('t_20', 'integer', default=0),
                Field('a_20', 'integer', default=0),
                Field('t_21', 'integer', default=0),
                Field('a_21', 'integer', default=0),
                Field('t_22', 'integer', default=0),
                Field('a_22', 'integer', default=0),
                Field('t_23', 'integer', default=0),
                Field('a_23', 'integer', default=0),
                Field('t_24', 'integer', default=0),
                Field('a_24', 'integer', default=0),
                Field('t_25', 'integer', default=0),
                Field('a_25', 'integer', default=0),
                Field('t_26', 'integer', default=0),
                Field('a_26', 'integer', default=0),
                Field('t_27', 'integer', default=0),
                Field('a_27', 'integer', default=0),
                Field('t_28', 'integer', default=0),
                Field('a_28', 'integer', default=0),
                Field('t_29', 'integer', default=0),
                Field('a_29', 'integer', default=0),
                Field('t_30', 'integer', default=0),
                Field('a_30', 'integer', default=0),
                Field('t_31', 'integer', default=0),
                Field('a_31', 'integer', default=0),
                migrate=False
                )

db.define_table('complain',
                Field('cid', 'string', requires=IS_NOT_EMPTY(), default=session.cid),
                Field('submit_firstdt', 'date', default=first_currentDate),
                Field('submit_date', 'date'),
                Field('submitted_by_id', 'string', default=''),
                Field('submitted_by_name', 'string', default=''),
                
                Field('complain_from', 'string', default=''),
                Field('ref', 'string', 'string', default=''),
                Field('complain_type', 'string', default=''),                
                Field('des', 'string', default=''),                
                Field('status', 'string', default='Submitted'),#Submitted, Replied
                
                #followup
                Field('reply_msg', 'string', default=''),
                Field('action', 'string', default='Pending'),#Resolved,Pending
                
                Field('followup_by', 'string', update=session.user_id),
                Field('followup_firstdt', 'date', update=first_currentDate),
                Field('followup_date', 'date', update=current_date),
                
                migrate=False
                )

db.define_table('task',
                Field('cid', 'string', requires=IS_NOT_EMPTY(), default=session.cid),                
                Field('first_date', 'date', default=first_currentDate),
                Field('submit_date', 'date', default=current_date),                
                Field('task_type', 'string', requires=IS_NOT_EMPTY()),  
                
                Field('spo_id', 'string', requires=IS_NOT_EMPTY()),
                Field('spo_name', 'string', default=''),
                
                Field('task', 'string', requires=IS_NOT_EMPTY()),  
                
                Field('task_datetime', 'datetime', requires=IS_NOT_EMPTY()),
                Field('task_date', 'date'),
                
                Field('complete_datetime', 'datetime'),
                Field('complete_date', 'date'),
                
                Field('status', 'string', default='Due'), #Due,Done
                
                migrate=False
                )

db.define_table('district',
                Field('cid', 'string', requires=IS_NOT_EMPTY(), default=session.cid),
                Field('district_id', 'string', requires=IS_NOT_EMPTY()),
                Field('name', 'string', requires=IS_NOT_EMPTY()),
                migrate=False
                )

db.define_table('district_thana',
                Field('cid', 'string', requires=IS_NOT_EMPTY(), default=session.cid),
                Field('name', 'string', requires=IS_NOT_EMPTY()),
                Field('district', 'string', requires=IS_NOT_EMPTY()),
                migrate=False
                )

db.define_table('doc_speciality',
                Field('cid', 'string', requires=IS_NOT_EMPTY(), default=session.cid),
                Field('specialty', 'string', default=''),
                migrate=False
                )

db.define_table('doc_catagory',
                Field('cid', 'string', requires=IS_NOT_EMPTY(), default=session.cid),
                Field('category', 'string', default=''),
                migrate=False
                )

db.define_table('level_name_settings',
                Field('cid', 'string', requires=IS_NOT_EMPTY(), default=session.cid),
                Field('depth', 'integer', requires=IS_NOT_EMPTY()),
                Field('name', 'string', default=''),
                Field('starting_code', 'string', default=''),
                migrate=False
                )

#================================= Temp Report Table
db.define_table('sm_temp_report_process',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('created_date','date',default=date_fixed),
                
                Field('month_1','date'),
                Field('month_2','date'),
                Field('process_key','string',default=''),#month_1+month_1
                
                Field('status_flag', 'integer', default=0),#1=month1,2=month2,3=completed
                Field('status', 'string',default=''),
                
                migrate=False
                )

db.define_table('sm_temp_report',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('created_date','date',default=date_fixed),
                
                Field('month_date','date'),#month_1 or month_2
                Field('process_key','string',default=''),#month_1+month_2
                
                Field('region_id', 'string', default=''),
                Field('region_name', 'string', default=''),                
                Field('tl_id', 'string', default=''),
                Field('tl_name', 'string', default=''),                
                Field('mpo_id', 'string', default=''),
                Field('mpo_name', 'string', default=''),
                
                Field('m1_amt', 'double', default=0),
                Field('m2_amt', 'double', default=0),
                
                Field('m1_order_count', 'integer', default=0),
                Field('m2_order_count', 'integer', default=0),
                
                migrate=False
                )

db.define_table('sm_market_day',
                Field('cid','string',requires=IS_NOT_EMPTY(), default=session.cid),                
                Field('area_id', 'string',requires=IS_NOT_EMPTY(), default=''), #market_id
                Field('area_name', 'string', default=''),                       #market_name
                Field('depot_id','string',default=''),
                Field('depot_name','string',default=''),
                
                Field('day_name', 'string',requires=IS_NOT_EMPTY(), default=''),
                
                migrate=False
                )

db.define_table('sm_tracking_table',
                Field('cid', 'string', requires=IS_NOT_EMPTY(), default=session.cid),
                Field('depot_id', 'string', default=''),
                Field('depot_name', 'string', default=''),
                Field('area_id', 'string', default=''),
                Field('area_name', 'string', default=''),
                Field('sl', 'string', default=''),
                Field('rep_id', 'string', default=''),
                Field('rep_name', 'string', default=''),
                Field('call_type', 'string', default=''),#SELL,DCR
                Field('visited_id', 'string', default=''),
                Field('visited_name', 'string', default=''),
                Field('visited_latlong', 'string', default='0,0'),
                Field('actual_latlong', 'string', default='0,0'),
                Field('visit_type', 'string', default=''),
                Field('visit_date', 'date'),
                Field('visit_time', 'string', default=''),
                Field('location_detail', 'string', default='-'),
                Field('last_location', 'string', default='0'),
                migrate=False
                )

#============== Login device
db.define_table('sm_login_device',
                Field('cid', 'string', requires=IS_NOT_EMPTY(), default=session.cid),
                Field('user_id', 'string', default='',requires=[IS_NOT_EMPTY(),IS_LENGTH(20,error_message='Mmaximum 20 character')]),
                Field('device_name', 'string', default='',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='Mmaximum 50 character')]),
                Field('user_agent', 'string', default=''),
                Field('sync_code', 'string', default=''),
                Field('request_ip', 'string', default=''),
                Field('status','string',requires=IS_IN_SET(('Submitted','Activated','Blocked')),default='Submitted'),
                
                Field('created_on','datetime',default=date_fixed),
                Field('updated_on','datetime',update=date_fixed),
                Field('updated_by',update=session.user_id),
                migrate=False
                )

#============== Login device
db.define_table('sm_login_log',
                Field('cid', 'string', requires=IS_NOT_EMPTY(), default=session.cid),
                Field('user_id', 'string', default='',requires=[IS_NOT_EMPTY(),IS_LENGTH(20,error_message='Mmaximum 20 character')]),
                Field('device_name', 'string', default='',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='Mmaximum 50 character')]),
                Field('user_agent', 'string', default=''),          
                Field('request_ip', 'string', default=''),
                Field('sync_code', 'string', default=''),
                
                Field('login_time','datetime',default=date_fixed),
                Field('logout_time','datetime'),
                
                migrate=False
                )

#============== Item Batch
db.define_table('sm_item_batch',
                Field('cid', 'string', requires=IS_NOT_EMPTY(), default=session.cid),
                Field('item_id','string', requires=IS_NOT_EMPTY()),
                Field('name','string',default=''),
                Field('batch_id','string', requires=IS_NOT_EMPTY()),
                Field('expiary_date', 'date', requires=IS_NOT_EMPTY()),
                signature,
                migrate=False
                )

#============== transaction dispute=========================

db.define_table('sm_transaction_dispute_head', 
                Field('cid','string',requires=IS_NOT_EMPTY()), #from session
                Field('depot_id','string',requires=IS_NOT_EMPTY()), #from session
                Field('depot_name','string',default=''),
                Field('sl','integer',requires=IS_NOT_EMPTY()), # max + 1 for each depot
                Field('store_id','string',default=''),
                Field('store_name','string',default=''),
                
                Field('dispute_date','date',requires=IS_NOT_EMPTY(),default=current_date),
                Field('issu_sl','integer',requires=IS_NOT_EMPTY(),default=0),
                Field('recieve_sl','integer',requires=IS_NOT_EMPTY(),default=0),                
                Field('status','string',default='Open'),# Open / Close     
                Field('dispute_type','string',default='Positive'),# Positive / Negetive
                
                Field('ym_date','date'),             
                Field('depot_status','string',default='0'),
                Field('ho_status','string',default='0'),            
                signature,
                migrate=False
                )

db.define_table('sm_transaction_dispute',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('depot_id','string',requires=IS_NOT_EMPTY()),#PK
                Field('depot_name','string',default=''),
                Field('sl','integer',requires=IS_NOT_EMPTY(),default=0),#PK
                Field('store_id','string',default=''),
                Field('store_name','string',default=''),
                
                Field('issu_sl','integer',requires=IS_NOT_EMPTY(),default=0),
                Field('recieve_sl','integer',requires=IS_NOT_EMPTY(),default=0),
                
                Field('status','string',default='Open'), # Open / Close 
                Field('dispute_type','string',default='Positive'),# Positive / Negetive       
                
                Field('item_id','string',requires=IS_NOT_EMPTY()),
                Field('item_name','string',requires=IS_NOT_EMPTY()),
                Field('batch_id','string',default=''),
                
                Field('issued_quantity','integer',requires=[IS_NOT_EMPTY(error_message='enter quantity'),IS_INT_IN_RANGE(1, 999999,error_message='enter valid quantity')]),
                Field('recieved_quantity','integer',requires=[IS_NOT_EMPTY(error_message='enter quantity'),IS_INT_IN_RANGE(1, 999999,error_message='enter valid quantity')]),               
                Field('issued_bonus_qty','integer',requires=[IS_NOT_EMPTY(error_message='enter quantity'),IS_INT_IN_RANGE(1, 999999,error_message='enter valid quantity')]),
                Field('recieved_bonus_qty','integer',requires=[IS_NOT_EMPTY(error_message='enter quantity'),IS_INT_IN_RANGE(1, 999999,error_message='enter valid quantity')]),
                
                Field('quantity','integer',requires=[IS_NOT_EMPTY(error_message='enter quantity'),IS_INT_IN_RANGE(1, 999999,error_message='enter valid quantity')]),                
                Field('bonus_qty','integer',default=0),
                
                Field('price','double',default=0),
                
                Field('item_unit','string',default=''),
                Field('item_carton','integer',default=0),
                Field('expiary_date', 'date'),
                
                Field('dispute_date','date',requires=IS_NOT_EMPTY(),default=current_date),
                Field('ym_date','date'),
                
                Field('depot_status','string',default='0'),
                Field('ho_status','string',default='0'),
                
                Field('flag_depot_stock','integer',default=0),
                Field('flag_depot_stock_balance','integer',default=0),  
                Field('flag_data','string',default='0'),                
                signature,
                migrate=False
                )


db.define_table('sm_prescription_head',
                Field('cid', 'string', requires=IS_NOT_EMPTY(), default=session.cid),
                Field('sl', 'integer', requires=IS_NOT_EMPTY(), default=0),
                Field('submit_date', 'date', requires=IS_NOT_EMPTY()),
                Field('first_date', 'date', requires=IS_NOT_EMPTY()),
                Field('submit_by_id', 'string', requires=IS_NOT_EMPTY()),
                Field('submit_by_name', 'string', requires=IS_NOT_EMPTY()),
                Field('user_type', 'string', requires=IS_NOT_EMPTY()),
                
                Field('doctor_id', 'string', requires=IS_NOT_EMPTY()),
                Field('doctor_name', 'string', requires=IS_NOT_EMPTY()),
                
                Field('image_name', 'string', default=''),
                Field('image_path', 'string', default=''),
                Field('lat_long','string',default='0'),
                
                
                Field('area_id', 'string', default=''),
                Field('area_name', 'string', default=''),
                Field('tl_id', 'string', default=''),
                Field('tl_name', 'string', default=''),
                Field('reg_id', 'string', default=''),
                Field('reg_name', 'string', default=''),
                
                signature,
                migrate=False
                )
db.define_table('sm_prescription_details',
                Field('cid', 'string', requires=IS_NOT_EMPTY(), default=session.cid),
                Field('sl', 'integer', default=0),      
                Field('medicine_id', 'string', default=''),              
                Field('medicine_name', 'string', default=''),    
                Field('med_type', 'string', default=''),
           
                migrate=False
                )



# -------------------------Doctor Visit Tables-------------------
db.define_table('sm_doc_visit_prop',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('rep_id', 'string', default=''),
                Field('rep_name', 'string', default=''),
                
                Field('first_date','date',default=date_fixed),
                Field('schedule_date','date',default=date_fixed),
                
                Field('doc_id', 'string', requires=IS_NOT_EMPTY()),                
                Field('doc_name', 'string', default=''),                
                Field('route_id', 'string', default=''),
                Field('route_name', 'string', default=''),                
                Field('depot_id', 'string', default=''),
                Field('depot_name', 'string', default=''),
                
                Field('level2_id', 'string', default=''),
                Field('level2_name', 'string', default=''),                
                Field('level1_id', 'string', default=''),
                Field('level1_name', 'string', default=''),
                Field('level0_id', 'string', default=''),
                Field('level0_name', 'string', default=''),
                
                Field('visited_flag', 'integer', default=0), #1=visited,0=Not visited ,#Mobile
                Field('visit_sl','integer',default=0),#Mobile
                Field('visit_date', 'date'),#Mobile
                Field('status', 'string', default='Submitted'), 
                
                Field('item_id', 'string', default=''),              
                Field('item_name', 'string', default=''),    
                Field('item_cat', 'string', default=''),
                Field('item_brand', 'string', default=''),
           
                migrate=False
                )
db.define_table('sm_doc_visit_sample',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('rep_id', 'string', default=''),
                Field('rep_name', 'string', default=''),
                
                Field('first_date','date',default=date_fixed),
                Field('schedule_date','date',default=date_fixed),
                
                Field('doc_id', 'string', requires=IS_NOT_EMPTY()),                
                Field('doc_name', 'string', default=''),                
                Field('route_id', 'string', default=''),
                Field('route_name', 'string', default=''), 
                Field('trDesc', 'string', default=''),               
                Field('depot_id', 'string', default=''),
                Field('depot_name', 'string', default=''),
                
                Field('level2_id', 'string', default=''),
                Field('level2_name', 'string', default=''),                
                Field('level1_id', 'string', default=''),
                Field('level1_name', 'string', default=''),
                Field('level0_id', 'string', default=''),
                Field('level0_name', 'string', default=''),
                
                Field('visited_flag', 'integer', default=0), #1=visited,0=Not visited ,#Mobile
                Field('visit_sl','integer',default=0),#Mobile
                Field('visit_date', 'date'),#Mobile
                Field('status', 'string', default='Submitted'),
                      
                Field('item_id', 'string', default=''),              
                Field('item_name', 'string', default=''),    
                Field('item_cat', 'string', default=''),
                Field('item_brand', 'string', default=''),
                Field('qty', 'string', default=''),
           
                migrate=False
                )
db.define_table('sm_doc_visit_gift',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('rep_id', 'string', default=''),
                Field('rep_name', 'string', default=''),
                
                Field('first_date','date',default=date_fixed),
                Field('schedule_date','date',default=date_fixed),
                
                Field('doc_id', 'string', requires=IS_NOT_EMPTY()),                
                Field('doc_name', 'string', default=''),                
                Field('route_id', 'string', default=''),
                Field('route_name', 'string', default=''),                
                Field('depot_id', 'string', default=''),
                Field('depot_name', 'string', default=''),
                
                Field('level2_id', 'string', default=''),
                Field('level2_name', 'string', default=''),                
                Field('level1_id', 'string', default=''),
                Field('level1_name', 'string', default=''),
                Field('level0_id', 'string', default=''),
                Field('level0_name', 'string', default=''),
                
                Field('visited_flag', 'integer', default=0), #1=visited,0=Not visited ,#Mobile
                Field('visit_sl','integer',default=0),#Mobile
                Field('visit_date', 'date'),#Mobile
                Field('status', 'string', default='Submitted'),   
                  
                Field('item_id', 'string', default=''),              
                Field('item_name', 'string', default=''),
                
                migrate=False
                )
db.define_table('sm_doc_visit_ppm',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('rep_id', 'string', default=''),
                Field('rep_name', 'string', default=''),
                
                Field('first_date','date',default=date_fixed),
                Field('schedule_date','date',default=date_fixed),
                
                Field('doc_id', 'string', requires=IS_NOT_EMPTY()),                
                Field('doc_name', 'string', default=''),                
                Field('route_id', 'string', default=''),
                Field('route_name', 'string', default=''),                
                Field('depot_id', 'string', default=''),
                Field('depot_name', 'string', default=''),
                
                Field('level2_id', 'string', default=''),
                Field('level2_name', 'string', default=''),                
                Field('level1_id', 'string', default=''),
                Field('level1_name', 'string', default=''),
                Field('level0_id', 'string', default=''),
                Field('level0_name', 'string', default=''),
                
                Field('visited_flag', 'integer', default=0), #1=visited,0=Not visited ,#Mobile
                Field('visit_sl','integer',default=0),#Mobile
                Field('visit_date', 'date'),#Mobile
                Field('status', 'string', default='Submitted'),   
                  
                Field('item_id', 'string', default=''),              
                Field('item_name', 'string', default=''),
           
                migrate=False
                )

#======================== As of date report table
db.define_table('sm_report_as_of_date',
                Field('cid','string',default=''),#***
                Field('depot_id','string',default=''),#***
                Field('depot_name','string',default=''), 
                Field('sl','integer',default=0), 
                Field('store_id','string',default=''),
                Field('store_name','string',default=''),
                
                #Date
                Field('report_date','date'),#***                
                Field('process_date','datetime'),                
                #----------
                Field('invoice_date','date'),
                
                Field('order_sl','integer',default=0),
                Field('order_datetime','datetime'),
                
                Field('delivery_date','date','date'),
                Field('payment_mode','string',default=''), #'CASH','CREDIT'
                Field('credit_note','string',default=''),
                
                Field('client_id','string',default=''),
                Field('client_name','string',default=''),                
                Field('cl_category_id','string',default=''),
                Field('cl_category_name','string',default=''),
                Field('cl_sub_category_id','string',default=''),
                Field('cl_sub_category_name','string',default=''),
                Field('client_limit_amt','double',default=0),#client credit limit amount from approved credit
                
                Field('rep_id','string',default=''),
                Field('rep_name','string',default=''),                
                Field('market_id','string',default=''),
                Field('market_name','string','string',default=''),                
                Field('d_man_id','string',default=''),
                Field('d_man_name','string',default=''),
                
                Field('level0_id','string',default=''),#zone
                Field('level0_name','string',default=''),
                Field('level1_id','string',default=''),#region
                Field('level1_name','string',default=''),
                Field('level2_id','string',default=''),#area
                Field('level2_name','string',default=''),
                
                Field('area_id','string',default=''),#territory
                Field('area_name','string',default=''),
                
                Field('shipment_no','string',default=''), #new
                
                Field('actual_total_tp','double',default=0),
                Field('vat_total_amount','double',default=0),
                Field('discount','double',default=0), # regular discount
                Field('sp_discount','double',default=0), # special discount for flat+approved+others 
                Field('total_amount','double',default=0),#with vat (itemAmt+vatAmt-discount)
                
                Field('ret_actual_total_tp','double',default=0),    #New *
                Field('return_tp','double',default=0),
                Field('return_vat','double',default=0),
                Field('return_discount','double',default=0), 
                Field('return_sp_discount','double',default=0), # special discount for flat, approved rate and others
                
                Field('collection_amount','double',default=0),#applied amount                         
                Field('adjust_amount','double',default=0),#payment adjustment amount                
                
                Field('note','string',default=''),
                
                migrate=False
                )


#======================== Invoice, Return and Payment Collection Transaction
db.define_table('sm_rpt_transaction',
                Field('cid','string',default=''),#***
                Field('depot_id','string',default=''),#***
                Field('depot_name','string',default=''),
                Field('store_id','string',default=''),
                Field('store_name','string',default=''),
                
                Field('inv_rowid','integer',default=0), 
                Field('inv_sl','integer',default=0),
                Field('invoice_date','date'),
                
                #Date
                Field('transaction_type','string',default=''),#INV,RET,RETC,PAYCOLL,PAYADJP(Positive),PAYADJN(Negative)
                Field('transaction_date','date'),#***
                Field('transaction_ref','integer',default=0), #Invoice Sl,Return sl, Payment rowid(MRNo)
                Field('transaction_ref_date','date'),#Invoice date,Return date, Payment date
                
                Field('trans_net_amt','double',default=0),
                Field('tp_amt','double',default=0),
                Field('vat_amt','double',default=0),
                Field('disc_amt','double',default=0),
                Field('spdisc_amt','double',default=0),
                
                Field('adjust_amount','double',default=0),#payment adjustment amount   
                
                Field('delivery_date','date','date'),
                Field('payment_mode','string',default=''), #'CASH','CREDIT'
                Field('credit_note','string',default=''),
                
                Field('client_id','string',default=''),
                Field('client_name','string',default=''),                
                Field('cl_category_id','string',default=''),
                Field('cl_category_name','string',default=''),
                Field('cl_sub_category_id','string',default=''),
                Field('cl_sub_category_name','string',default=''),
                Field('client_limit_amt','double',default=0),#client credit limit amount from approved credit
                
                Field('rep_id','string',default=''),
                Field('rep_name','string',default=''),                
                Field('market_id','string',default=''),
                Field('market_name','string','string',default=''),                
                Field('d_man_id','string',default=''),
                Field('d_man_name','string',default=''),
                
                Field('level0_id','string',default=''),#zone
                Field('level0_name','string',default=''),
                Field('level1_id','string',default=''),#region
                Field('level1_name','string',default=''),
                Field('level2_id','string',default=''),#area
                Field('level2_name','string',default=''),
                
                Field('area_id','string',default=''),#territory
                Field('area_name','string',default=''),                
                Field('shipment_no','string',default=''), #new
                
                Field('note','string',default=''),
                
                Field('created_on','datetime',default=date_fixed),
                Field('created_by',default=session.user_id),
                
                migrate=False
                )

db.define_table('sm_doctor_sample',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('item_id','string',requires=[IS_NOT_EMPTY(),IS_ALPHANUMERIC(error_message=T('must be alphanumeric ( a-z, A-Z, 0-9 )!')),IS_LENGTH(20,error_message='enter maximum 20 character')]),
                Field('name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(100,error_message='enter maximum 100 character')]),
                Field('des','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(100,error_message='enter maximum 100 character')],default='-'),
                Field('unit_type','string',requires=IS_NOT_EMPTY()),                
                Field('manufacturer','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='enter maximum 50 character')],default='-'),
                Field('pack_size','string',requires=IS_NOT_EMPTY()),
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='ACTIVE'),
                signature,
                migrate=False
                )

db.define_table('sm_item_prescription',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('item_id','string',requires=[IS_NOT_EMPTY(),IS_ALPHANUMERIC(error_message=T('must be alphanumeric ( a-z, A-Z, 0-9 )!')),IS_LENGTH(20,error_message='enter maximum 20 character')]),
                Field('name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(100,error_message='enter maximum 100 character')]),
                Field('des','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(100,error_message='enter maximum 100 character')],default='-'),
                Field('category_id','string',requires=IS_NOT_EMPTY()),  #primary category
                Field('category_id_sp','string',default=''),            #special category
                Field('unit_type','string',requires=IS_NOT_EMPTY()),                
                Field('manufacturer','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='enter maximum 50 character')],default='-'),
                Field('item_carton','integer',default=0),
                Field('item_identity','string',default=''),#self/others
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='ACTIVE'),
                signature,
                migrate=False
                )


#=================================== level backup previous month befor ff and area process ===================
db.define_table('temp_sm_level',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('level_id','string',requires=[IS_NOT_EMPTY(),IS_ALPHANUMERIC(error_message=T('must be alphanumeric ( a-z, A-Z, 0-9 )!')),IS_LENGTH(20,error_message='Maximum 20 character')]),
                Field('level_name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='Maximum 50 character')]),
                Field('parent_level_id','string',default='0',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='Maximum 50 character')]),
                Field('parent_level_name','string',default=''),
                Field('is_leaf','string',requires=IS_NOT_EMPTY(),default='0'), #0 for group & 1 for final
                Field('area_id_list','string',default=''),
                Field('special_territory_code','string',default=''),
                Field('depot_id','string',default='-',requires=[IS_NOT_EMPTY(),IS_LENGTH(20,error_message='Maximum 20 character')]),
                
                Field('depth','integer',default=0),
                Field('level0','string',default=''),
                Field('level0_name','string',default=''),
                Field('level1','string',default=''),
                Field('level1_name','string',default=''),
                Field('level2','string',default=''),
                Field('level2_name','string',default=''),
                Field('level3','string',default=''),
                Field('level3_name','string',default=''),
                Field('level4','string',default=''),
                Field('level4_name','string',default=''),
                Field('level5','string',default=''),
                Field('level5_name','string',default=''),
                Field('level6','string',default=''),
                Field('level6_name','string',default=''),
                Field('level7','string',default=''),
                Field('level7_name','string',default=''),
                Field('level8','string',default=''),
                Field('level8_name','string',default=''),
                Field('territory_des','string',default=''),
                signature,
                migrate=False
                )

#========================= rep+supervisor backup ============
db.define_table('temp_sm_rep',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('rep_id','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(20,error_message='Mmaximum 20 character')]),
                Field('name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='Maximum 50 character')]),
                Field('mobile_no','bigint',default=''),
                Field('password','password',requires=IS_LENGTH(minsize=3,maxsize=12)),
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='ACTIVE'),
                Field('sync_code','string',default=''),
                Field('sync_code_servey','string',default=''),
                Field('sync_count','integer',requires=IS_NOT_EMPTY(),default=0),
                Field('first_sync_date','datetime',default=''),
                Field('last_sync_date','datetime',default=''),
                Field('monthly_sms_count','integer',requires=IS_NOT_EMPTY(),default=0),
                Field('monthly_voucher_count','integer',requires=IS_NOT_EMPTY(),default=0),
                
                Field('java','string',requires=IS_IN_SET(('Yes','No')),default='No'),
                Field('wap','string',requires=IS_IN_SET(('Yes','No')),default='No'),
                Field('android','string',requires=IS_IN_SET(('Yes','No')),default='No'),
                Field('sms','string',requires=IS_IN_SET(('Yes','No')),default='Yes'),
                
                Field('user_type','string',default='rep'),
                Field('level_id','string',default=''),
                Field('depot_id','string',default=''),
                
                # user click on "Sync" will get response lik "You sync request is in que Please try to sync after few minutes" o - > 1
                # if already submitted (flag = 1) - "Your request is already in que, please try to sync ... "
                # if last sync request is less that 10 minutes before .. your sync data is just processed please try to sync or wait atleast 10 minute to make another "Que to Sync" request
                
                Field('sync_req_time','datetime',default=''),#10 min gap in 2 sync
                Field('sync_flag','string',default='0'),
                Field('sync_data','string',default=''),
                signature,
                migrate=False
                )#field2 is used for depth

db.define_table('temp_sm_rep_area',   
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('rep_id','string',requires=IS_NOT_EMPTY()),
                Field('rep_name','string',default=''),
                Field('rep_category','string',requires=IS_IN_SET(('A','B','C','Z'))),#MSO Category
                
                Field('area_id','string',requires=IS_NOT_EMPTY()),
                Field('area_name','string',default=''),                
                Field('depot_id','string',default=''),
                signature,
                migrate=False
                )

db.define_table('temp_sm_supervisor_level',   
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('sup_id','string',requires=IS_NOT_EMPTY()),
                Field('sup_name','string',default=''),
                
                Field('level_id','string',requires=IS_NOT_EMPTY()),
                Field('level_name','string',default=''),
                Field('level_depth_no','integer',default=0),
                
                signature,
                migrate=False
                )

#======================== backup table
db.define_table('backup_sm_level',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('level_id','string',requires=[IS_NOT_EMPTY(),IS_ALPHANUMERIC(error_message=T('must be alphanumeric ( a-z, A-Z, 0-9 )!')),IS_LENGTH(20,error_message='Maximum 20 character')]),
                Field('level_name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='Maximum 50 character')]),
                Field('parent_level_id','string',default='0',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='Maximum 50 character')]),
                Field('parent_level_name','string',default=''),
                Field('is_leaf','string',requires=IS_NOT_EMPTY(),default='0'), #0 for group & 1 for final
                Field('area_id_list','string',default=''),
                Field('special_territory_code','string',default=''),
                Field('depot_id','string',default='-',requires=[IS_NOT_EMPTY(),IS_LENGTH(20,error_message='Maximum 20 character')]),
                
                Field('depth','integer',default=0),
                Field('level0','string',default=''),
                Field('level0_name','string',default=''),
                Field('level1','string',default=''),
                Field('level1_name','string',default=''),
                Field('level2','string',default=''),
                Field('level2_name','string',default=''),
                Field('level3','string',default=''),
                Field('level3_name','string',default=''),
                Field('level4','string',default=''),
                Field('level4_name','string',default=''),
                Field('level5','string',default=''),
                Field('level5_name','string',default=''),
                Field('level6','string',default=''),
                Field('level6_name','string',default=''),
                Field('level7','string',default=''),
                Field('level7_name','string',default=''),
                Field('level8','string',default=''),
                Field('level8_name','string',default=''),
                Field('territory_des','string',default=''),
                signature,
                migrate=False
                )

#========================= rep+supervisor backup ============
db.define_table('backup_sm_rep',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('rep_id','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(20,error_message='Mmaximum 20 character')]),
                Field('name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='Maximum 50 character')]),
                Field('mobile_no','bigint',default=''),
                Field('password','password',requires=IS_LENGTH(minsize=3,maxsize=12)),
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='ACTIVE'),
                Field('sync_code','string',default=''),
                Field('sync_code_servey','string',default=''),
                Field('sync_count','integer',requires=IS_NOT_EMPTY(),default=0),
                Field('first_sync_date','datetime',default=''),
                Field('last_sync_date','datetime',default=''),
                Field('monthly_sms_count','integer',requires=IS_NOT_EMPTY(),default=0),
                Field('monthly_voucher_count','integer',requires=IS_NOT_EMPTY(),default=0),
                
                Field('java','string',requires=IS_IN_SET(('Yes','No')),default='No'),
                Field('wap','string',requires=IS_IN_SET(('Yes','No')),default='No'),
                Field('android','string',requires=IS_IN_SET(('Yes','No')),default='No'),
                Field('sms','string',requires=IS_IN_SET(('Yes','No')),default='Yes'),
                
                Field('user_type','string',default='rep'),
                Field('level_id','string',default=''),
                Field('depot_id','string',default=''),
                
                # user click on "Sync" will get response lik "You sync request is in que Please try to sync after few minutes" o - > 1
                # if already submitted (flag = 1) - "Your request is already in que, please try to sync ... "
                # if last sync request is less that 10 minutes before .. your sync data is just processed please try to sync or wait atleast 10 minute to make another "Que to Sync" request
                
                Field('sync_req_time','datetime',default=''),#10 min gap in 2 sync
                Field('sync_flag','string',default='0'),
                Field('sync_data','string',default=''),
                signature,
                migrate=False
                )#field2 is used for depth
                
db.define_table('backup_sm_rep_area',   
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('rep_id','string',requires=IS_NOT_EMPTY()),
                Field('rep_name','string',default=''),
                Field('rep_category','string',requires=IS_IN_SET(('A','B','C','Z'))),#MSO Category
                
                Field('area_id','string',requires=IS_NOT_EMPTY()),
                Field('area_name','string',default=''),                
                Field('depot_id','string',default=''),
                signature,
                migrate=False
                )

db.define_table('backup_sm_supervisor_level',   
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('sup_id','string',requires=IS_NOT_EMPTY()),
                Field('sup_name','string',default=''),
                
                Field('level_id','string',requires=IS_NOT_EMPTY()),
                Field('level_name','string',default=''),
                Field('level_depth_no','integer',default=0),
                
                signature,
                migrate=False
                )

