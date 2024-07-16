from random import randint



def get_zone():
    retStr=''
    c_id = session.cid
    region=str(request.vars.region)
    
    records=db((db.sm_level.cid == c_id)&(db.sm_level.level0 == region)&(db.sm_level.depth == 1)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
    for row in records:
        level_id=str(row.level_id)
        level_name=str(row.level_name)
        
        if retStr=='':
            retStr=level_id+'<fd>'+level_name
        else:
            retStr+='<rd>'+level_id+'<fd>'+level_name
        
    
    return retStr

def get_area():
    retStr=''
    c_id = session.cid
    region=str(request.vars.region)
    zone=str(request.vars.zone)
    
    records=db((db.sm_level.cid == c_id)&(db.sm_level.level0 == region)&(db.sm_level.level1 == zone)&(db.sm_level.depth == 2)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
    for row in records:
        level_id=str(row.level_id)
        level_name=str(row.level_name)
        
        if retStr=='':
            retStr=level_id+'<fd>'+level_name
        else:
            retStr+='<rd>'+level_id+'<fd>'+level_name
        
    
    return retStr


def get_territory():
    retStr=''
    c_id = session.cid
    region=str(request.vars.region)
    zone=str(request.vars.zone)
    area=str(request.vars.area)
    
    records=db((db.sm_level.cid == c_id)&(db.sm_level.level0 == region)&(db.sm_level.level1 == zone)&(db.sm_level.level2 == area)&(db.sm_level.depth == 3)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
    #return db._lastsql
    for row in records:
        level_id=str(row.level_id)
        level_name=str(row.level_name)
        
        if retStr=='':
            retStr=level_id+'<fd>'+level_name
        else:
            retStr+='<rd>'+level_id+'<fd>'+level_name
        
    
    return retStr




#---------------------------- ADD
def index():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

    response.title = 'Prescription Report'
    

    comRows = db((db.sm_settings.cid == session.cid) & (db. sm_settings.s_key == 'COM_NAME')).select(db.sm_settings.field1, limitby=(0, 1))
    if comRows:
        company_name=comRows[0].field1         
        session.company_name=company_name
        

    c_id = session.cid

    search_form =SQLFORM(db.sm_search_date)
    
    btn_sum_day_wise=request.vars.btn_sum_day_wise
    btn_area_wise=request.vars.btn_area_wise
    btn_pr_details=request.vars.btn_pr_details
    btn_pr_details_d=request.vars.btn_pr_details_d
    btn_pr_summary=request.vars.btn_pr_summary
    btn_pr_summary_d=request.vars.btn_pr_summary_d
    
    btn_orphan_med_list=request.vars.btn_orphan_med_list
    btn_orphan_med_list_d=request.vars.btn_orphan_med_list_d
    
    btn_company_track_rm=request.vars.btn_company_track_rm
    btn_company_track_rm_d=request.vars.btn_company_track_rm_d
    
    btn_company_track_zm=request.vars.btn_company_track_zm
    btn_company_track_zm_d=request.vars.btn_company_track_zm_d
    
    btn_company_track_am=request.vars.btn_company_track_am
    btn_company_track_am_d=request.vars.btn_company_track_am_d
    
    btn_company_track_mpo=request.vars.btn_company_track_mpo
    btn_company_track_mpo_d=request.vars.btn_company_track_mpo_d
    
    btn_company_track1=request.vars.btn_company_track1
    btn_company_track_d1=request.vars.btn_company_track_d1
    
    btn_company_track2=request.vars.btn_company_track2
    btn_company_track_d2=request.vars.btn_company_track_d2
    
    btn_company_track=request.vars.btn_company_track
    btn_company_track_d=request.vars.btn_company_track_d    
    
    btn_physician_track=request.vars.btn_physician_track
    btn_physician_track_d=request.vars.btn_physician_track_d
    
    btn_institute_track_mpo=request.vars.btn_institute_track_mpo
    btn_institute_track_mpo_d=request.vars.btn_institute_track_mpo_d
    
    btn_institute_track_am=request.vars.btn_institute_track_am
    btn_institute_track_am_d=request.vars.btn_institute_track_am_d
    
    btn_institute_track_zm=request.vars.btn_institute_track_zm
    btn_institute_track_zm_d=request.vars.btn_institute_track_zm_d
    
    btn_institute_track_rm=request.vars.btn_institute_track_rm
    btn_institute_track_rm_d=request.vars.btn_institute_track_rm_d
    
#    btn_chart_generic=request.vars.btn_chart_generic
    
    
    if btn_institute_track_rm or btn_institute_track_zm or btn_institute_track_am or btn_institute_track_mpo_d or btn_institute_track_mpo or btn_physician_track_d or btn_physician_track or btn_company_track or btn_company_track_d or btn_company_track_rm or btn_company_track_zm or btn_company_track_am or btn_company_track_mpo or btn_company_track_mpo_d or btn_company_track_am_d or btn_company_track_zm_d or btn_company_track_rm_d or btn_orphan_med_list_d or btn_orphan_med_list or btn_pr_summary or btn_pr_summary_d or btn_pr_details_d or btn_pr_details or btn_area_wise or btn_sum_day_wise:
        
        pr_region=request.vars.pr_region
        pr_zone=request.vars.pr_zone
        pr_area=request.vars.pr_area
        pr_territory=request.vars.pr_territory
        pr_doctor=request.vars.pr_doctor
        pr_ff=request.vars.pr_ff
        med_generic=request.vars.med_generic
        
        if pr_zone==None:
            pr_zone=''
        
        if pr_area==None:
            pr_area=''
        
        if pr_territory==None:
            pr_territory=''
        
        #return pr_territory        
        pr_doctor_str=str(request.vars.pr_doctor).split('|')
        if len(pr_doctor_str)>0:
            pr_doctor=pr_doctor_str[0]
        
        pr_ff_str=str(request.vars.pr_ff).split('|')
        if len(pr_ff_str)>0:
            pr_ff=pr_ff_str[0]
        
         
        #=========== date 0
        date_from=request.vars.from_dt_3
        date_to=request.vars.to_dt_3
    
        dateFlag=True        
        try:
          from_dt2=datetime.datetime.strptime(str(date_from),'%Y-%m-%d')
          to_dt2=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 

          if from_dt2>to_dt2:
             dateFlag=False
        except:
            dateFlag=False
        
        
        if dateFlag==False:
            response.flash="Invalid Date Range"
        else:            
            dateDiff=(to_dt2-from_dt2).days
            
            if dateDiff>90:
                response.flash="Maximum 90 days allowed between Date Range"
                dateFlag=False
        
        
        #=========== date 1
        date_from_1=request.vars.from_dt_4
        date_to_1=request.vars.to_dt_4
                
        dateFlag1=True
        try:
          from_dt4=datetime.datetime.strptime(str(date_from_1),'%Y-%m-%d')
          to_dt4=datetime.datetime.strptime(str(date_to_1),'%Y-%m-%d') 

          if from_dt4>to_dt4:
             dateFlag1=False
        except:
            dateFlag1=False
        
        if dateFlag1==False:
            response.flash="Invalid Date Range (1st)"
                        
        
        #=========== date 2
        date_from_2=request.vars.from_dt_5
        date_to_2=request.vars.to_dt_5
        
        dateFlag2=True
        try:
          from_dt5=datetime.datetime.strptime(str(date_from_2),'%Y-%m-%d')
          to_dt5=datetime.datetime.strptime(str(date_to_2),'%Y-%m-%d') 

          if from_dt5>to_dt5:
             dateFlag2=False
        except:
            dateFlag2=False
    
        
        if dateFlag2==False:
            response.flash="Invalid Date Range (2nd)"
       
        
        if dateFlag!=False:
            if btn_pr_summary:
                redirect (URL('pr_summary',vars=dict(date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,med_generic=med_generic)))
            
            if btn_pr_summary_d:
                redirect (URL('pr_summary_d',vars=dict(date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,med_generic=med_generic)))
            
            if btn_pr_details_d:
                redirect (URL('pr_details_d',vars=dict(date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,med_generic=med_generic))) 
            if btn_pr_details:
                redirect (URL('pr_details',vars=dict(date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,med_generic=med_generic))) 
            if btn_area_wise:
                redirect (URL('count_area_wise',vars=dict(date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,med_generic=med_generic)))        
            if btn_sum_day_wise:
                redirect (URL('count_day_wise',vars=dict(date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,med_generic=med_generic)))
            if btn_orphan_med_list:
                redirect (URL('orphan_med_list',vars=dict(date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,med_generic=med_generic)))
            if btn_orphan_med_list_d:
                redirect (URL('orphan_med_list_d',vars=dict(date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,med_generic=med_generic)))
            
            if btn_physician_track or btn_physician_track_d:
                if pr_region=='':
                    response.flash="Select Region"
                else:
                    if btn_physician_track:
                        redirect (URL('physician_track',vars=dict(date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)))
                    if btn_physician_track_d:
                        redirect (URL('physician_track_d',vars=dict(date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)))
                
#            if btn_chart_generic:
#                med_generic=request.vars.med_generic
#                if med_generic=='':
#                    response.flash='Required Generic'
#                else:
#                    redirect (URL('chart_generic',vars=dict(date_from=date_from,date_to=date_to,generic=med_generic)))
        
        
        if dateFlag1!=False and dateFlag2!=False:            
            if btn_institute_track_rm or btn_institute_track_zm or btn_institute_track_am or btn_institute_track_mpo_d or btn_institute_track_mpo or btn_company_track_zm or btn_company_track_zm_d or btn_company_track_am or btn_company_track_am or btn_company_track_am_d or btn_company_track_mpo or btn_company_track_mpo_d or btn_company_track or btn_company_track_d:
                if pr_region=='':
                    response.flash="Select Region"
                else:                    
                    if btn_company_track_d:
                        redirect (URL('company_track_d',vars=dict(date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)))            
                    if btn_company_track:                
                        redirect (URL('company_track',vars=dict(date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)))
              
                    if btn_company_track_mpo_d:
                        redirect (URL('company_track_mpo_d',vars=dict(date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)))            
                    if btn_company_track_mpo:                
                        redirect (URL('company_track_mpo',vars=dict(date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)))
              
                    if btn_company_track_am_d:                
                        redirect (URL('company_track_am_d',vars=dict(date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_doctor=pr_doctor,pr_ff=pr_ff)))
                    if btn_company_track_am:
                        redirect (URL('company_track_am',vars=dict(date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)))
               
                    if btn_company_track_zm_d:                
                        redirect (URL('company_track_zm_d',vars=dict(date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2,pr_region=pr_region,pr_zone=pr_zone,pr_doctor=pr_doctor,pr_ff=pr_ff)))
                    if btn_company_track_zm:
                        redirect (URL('company_track_zm',vars=dict(date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)))
                    
                    if btn_institute_track_mpo_d:                
                        redirect (URL('institute_track_mpo_d',vars=dict(date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2,pr_region=pr_region,pr_zone=pr_zone,pr_doctor=pr_doctor,pr_ff=pr_ff)))
                    if btn_institute_track_mpo:
                        redirect (URL('institute_track_mpo',vars=dict(date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)))
                    
                    if btn_institute_track_am:
                        redirect (URL('institute_track_am',vars=dict(date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)))
                    
                    if btn_institute_track_zm:
                        redirect (URL('institute_track_zm',vars=dict(date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)))
                    
                    if btn_institute_track_rm:
                        redirect (URL('institute_track_rm',vars=dict(date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)))
                    
                    
             
            if btn_company_track_rm_d:
                redirect (URL('company_track_rm_d',vars=dict(date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2,pr_region=pr_region,pr_doctor=pr_doctor,pr_ff=pr_ff)))
            if btn_company_track_rm:
                redirect (URL('company_track_rm',vars=dict(date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)))
        
    elif btn_company_track2 or btn_company_track1 or btn_company_track_d1:
        pr_region1=request.vars.pr_region1
        
        if pr_region1=='':
            response.flash="Select Region"
        else:            
            pr_year1=request.vars.pr_year1
            pr_quarter1=request.vars.pr_quarter1
            pr_month1=request.vars.pr_month1
            pr_cycle1=request.vars.pr_cycle1
            
            pr_year2=request.vars.pr_year2
            pr_quarter2=request.vars.pr_quarter2
            pr_month2=request.vars.pr_month2
            pr_cycle2=request.vars.pr_cycle2
            
            
            pr_zone1=request.vars.pr_zone1
            pr_area1=request.vars.pr_area1
            pr_territory1=request.vars.pr_territory1
            pr_doctor1=request.vars.pr_doctor1
            pr_ff1=request.vars.pr_ff1
            
            if pr_year1=='' and pr_year2=='':
                response.flash="Select Region Year"
            else:                        
                if btn_company_track_d1:
                    redirect (URL('company_track_d1',vars=dict(pr_region1=pr_region1,pr_zone1=pr_zone1,pr_area1=pr_area1,pr_territory1=pr_territory1,pr_doctor1=pr_doctor1,pr_ff1=pr_ff1,pr_year1=pr_year1,pr_quarter1=pr_quarter1,pr_month1=pr_month1,pr_cycle1=pr_cycle1,pr_year2=pr_year2,pr_quarter2=pr_quarter2,pr_month2=pr_month2,pr_cycle2=pr_cycle2)))            
                if btn_company_track1:                
                    redirect (URL('company_track1',vars=dict(pr_region1=pr_region1,pr_zone1=pr_zone1,pr_area1=pr_area1,pr_territory1=pr_territory1,pr_doctor1=pr_doctor1,pr_ff1=pr_ff1,pr_year1=pr_year1,pr_quarter1=pr_quarter1,pr_month1=pr_month1,pr_cycle1=pr_cycle1,pr_year2=pr_year2,pr_quarter2=pr_quarter2,pr_month2=pr_month2,pr_cycle2=pr_cycle2)))
                if btn_company_track2:                
                    redirect (URL('company_track2',vars=dict(pr_region1=pr_region1,pr_zone1=pr_zone1,pr_area1=pr_area1,pr_territory1=pr_territory1,pr_doctor1=pr_doctor1,pr_ff1=pr_ff1,pr_year1=pr_year1,pr_quarter1=pr_quarter1,pr_month1=pr_month1,pr_cycle1=pr_cycle1,pr_year2=pr_year2,pr_quarter2=pr_quarter2,pr_month2=pr_month2,pr_cycle2=pr_cycle2)))
                                     
            
         
    # region
    regionRows = db((db.sm_level.cid == c_id) & (db.sm_level.is_leaf == '0') & (db.sm_level.depth == 0)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
        
    return dict(regionRows=regionRows,search_form=search_form)

def company_track2():
    
    response.title='Company track2'
    
    cid=session.cid
    date_from_1=''#request.vars.date_from_1
    date_to_1=''#request.vars.date_to_1   
    
#    date_to_m_1=datetime.datetime.strptime(str(date_to_1),'%Y-%m-%d') 
#    date_to_m_1=date_to_m_1 + datetime.timedelta(days = 1)
    
    date_from_2=''#request.vars.date_from_2
    date_to_2=''#request.vars.date_to_2
    
#    date_to_m_2=datetime.datetime.strptime(str(date_to_2),'%Y-%m-%d') 
#    date_to_m_2=date_to_m_2 + datetime.timedelta(days = 1)
    
    pr_region1=request.vars.pr_region1
    pr_zone1=request.vars.pr_zone1
    pr_area1=request.vars.pr_area1
    pr_territory1=request.vars.pr_territory1
    pr_doctor1=request.vars.pr_doctor1
    pr_ff1=request.vars.pr_ff1
    
    
    if pr_region1=='None':
        pr_region1=''
    
    if pr_zone1=='None':
        pr_zone1=''
    
    if pr_area1=='None':
        pr_area1=''
    
    if pr_territory1=='None':
        pr_territory1=''
    
    if pr_doctor1=='None':
        pr_doctor1=''
    
    if pr_ff1=='None':
        pr_ff1=''
        
    
    pr_year1=request.vars.pr_year1
    pr_quarter1=request.vars.pr_quarter1
    pr_month1=request.vars.pr_month1
    pr_cycle1=request.vars.pr_cycle1
    
    pr_year2=request.vars.pr_year2
    pr_quarter2=request.vars.pr_quarter2
    pr_month2=request.vars.pr_month2
    pr_cycle2=request.vars.pr_cycle2
    
    if pr_year1=='None':
        pr_year1=''
    
    if pr_year2=='None':
        pr_year2=''
    
    if pr_quarter1=='None':
        pr_quarter1=''
    
    if pr_month1=='None':
        pr_month1=''
    
    if pr_cycle1=='None':
        pr_cycle1=''
    
    
    if pr_quarter2=='None':
        pr_quarter2=''
    
    if pr_month2=='None':
        pr_month2=''
    
    if pr_cycle2=='None':
        pr_cycle2=''
    
    stMonth1='00'
    endMonth1='00'
    
    stDay1='00'
    endDay1='00'
    
    stMonth2='00'
    endMonth2='00'
    
    stDay2='00'
    endDay2='00'
        
    if pr_year1!='' and pr_year2!='':
        stMonth1='01'
        endMonth1='12'
        
        stDay1='01'
        endDay1='31'
        
        stMonth2='01'
        endMonth2='12'
        
        stDay2='01'
        endDay2='31'
            

    if pr_year1!='' and pr_year2!='' and pr_quarter1!='' and pr_quarter2!='':
        if pr_quarter1=='1':            
            stMonth1='01'
            endMonth1='03'
            
            stDay1='01'
            endDay1='31'
            
        elif pr_quarter1=='2':
            stMonth1='04'
            endMonth1='06'
            
            stDay1='01'
            endDay1='30'            
            
        elif pr_quarter1=='3':
            stMonth1='07'
            endMonth1='09'
            
            stDay1='01'
            endDay1='31'
            
        elif pr_quarter1=='4':
            stMonth1='10'
            endMonth1='12'
            
            stDay1='01'
            endDay1='31'
                    
        if pr_quarter2=='1':
            stMonth2='01'
            endMonth2='03'
            
            stDay2='01'
            endDay2='31'
                        
        elif pr_quarter2=='2':
            stMonth2='04'
            endMonth2='06'
            
            stDay2='01'
            endDay2='31'
                        
        elif pr_quarter2=='3':
            stMonth2='07'
            endMonth2='09'
            
            stDay2='01'
            endDay2='31'
            
        elif pr_quarter2=='4':
            stMonth2='10'
            endMonth2='12'
            
            stDay2='01'
            endDay2='31'
            
    
    if pr_year1!='' and pr_year2!='' and pr_quarter1!='' and pr_quarter2!='' and pr_month1!='' and pr_month2!='':
            
            stMonth1=pr_month1
            endMonth1=pr_month1
            stDay1='01'
            endDay1='31'
            
            stMonth2=pr_month2
            endMonth2=pr_month2
            stDay2='01'
            endDay2='31'
            
            
    if pr_year1!='' and pr_year2!='' and pr_quarter1!='' and pr_quarter2!='' and pr_month1!='' and pr_month2!='' and pr_cycle1!='' and pr_cycle2!='':
        
        stMonth1=pr_month1
        endMonth1=pr_month1
            
        if pr_cycle1=='1':
            stDay1='01'
            endDay1='07'
        elif pr_cycle1=='2':
            stDay1='08'
            endDay1='15'
        elif pr_cycle1=='3':
            stDay1='16'
            endDay1='21'
        elif pr_cycle1=='4':
            stDay1='22'
            endDay1='31'
        
        stMonth2=pr_month2
        endMonth2=pr_month2
            
        if pr_cycle2=='1':
            stDay2='01'
            endDay2='07'
        elif pr_cycle2=='2':
            stDay2='08'
            endDay2='15'
        elif pr_cycle2=='3':
            stDay2='16'
            endDay2='21'
        elif pr_cycle2=='4':
            stDay2='22'
            endDay2='31'
            
        
    date_from_1=pr_year1+'-'+stMonth1+'-'+stDay1
    date_to_1=pr_year1+'-'+endMonth1+'-'+endDay1
    
    date_from_2=pr_year2+'-'+stMonth2+'-'+stDay2
    date_to_2=pr_year2+'-'+endMonth2+'-'+endDay2
    
            
    #return str(date_from_1)+','+str(date_to_1)+'.......'+str(date_from_2)+','+str(date_to_2)    
    
    reg_name=''
    regionRows=db((db.sm_level.cid==cid)&(db.sm_level.level_id==pr_region1)).select(db.sm_level.level_name,limitby=(0,1))
    if regionRows:
        reg_name=regionRows[0].level_name
        
    
    condition1=''
    if pr_region1!='':
        condition1+=condition1+" and a.level0 = '"+str(pr_region1)+"'"
    if pr_zone1!='':
        condition1+=condition1+" and a.level1 = '"+str(pr_zone1)+"'"
    if pr_area1!='':
        condition1+=condition1+" and a.level2 = '"+str(pr_area1)+"'"
    if pr_territory1!='':
        condition1+=condition1+" and a.level3 = '"+str(pr_territory1)+"'"
    if pr_doctor1!='':
        condition1+=condition1+" and b.doctor_id = '"+str(pr_doctor1)+"'"
    if pr_ff1!='':
        condition1+=condition1+" and b.submit_by_id = '"+str(pr_ff1)+"'"

    
#    if pr_year1!='' and pr_year2!='':
#        date_to_1=datetime.datetime.strptime(str(date_to_1),'%Y-%m-%d')
#        dateTo_1=date_to_1 + datetime.timedelta(days = 1)        
#        
#        sql1="(SELECT zone_id,zone_name,reg_id,reg_name,tl_id,tl_name,area_id,area_name,level0_sup_id,level0_sup_name,level1_sup_id,level1_sup_name,level2_sup_id,level2_sup_name,level3_sup_id,level3_sup_name,sl as rxCount1,0 as rxCount2, med_self as med_self1,med_total as med_total1, 0 as med_self2, 0 as med_total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and first_date>='"+date_from_1+"' and first_date<'"+str(dateTo_1)[:10]+"' "+condition+")"
#    
#        sql2="(SELECT zone_id,zone_name,reg_id,reg_name,tl_id,tl_name,area_id,area_name,level0_sup_id,level0_sup_name,level1_sup_id,level1_sup_name,level2_sup_id,level2_sup_name,level3_sup_id,level3_sup_name,0 as rxCount1,sl as rxCount2,0 as med_self1, 0 as med_total1,med_self as med_self2,med_total as total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and first_date>='"+date_from_2+"' and submit_date<'"+current_date+"' "+condition+")"
    
    
    #if pr_cycle1!='' and pr_cycle2!='':
    sql1="(SELECT a.cid as cid,a.level0 as zone_id,a.level0_name as zone_name,a.level1 as reg_id,a.level1_name as reg_name,a.level2 as tl_id,a.level2_name as tl_name,a.level3 as area_id,a.level3_name as area_name,'' as level0_sup_id,'' as level0_sup_name,'' as level1_sup_id,'' as level1_sup_name,'' as level2_sup_id,'' as level2_sup_name,'' as level3_sup_id,'' as level3_sup_name,b.sl as rxCount1,0 as rxCount2, b.med_self as med_self1,b.med_total as med_total1, 0 as med_self2, 0 as med_total2 FROM sm_level a,`sm_prescription_head` b WHERE a.cid=b.cid and a.level3=b.area_id and b.cid='"+cid+"' and b.submit_date>='"+date_from_1+"' and b.submit_date<='"+date_to_1+"'"+condition1+")"
    
    sql2="(SELECT a.cid as cid,a.level0 as zone_id,a.level0_name as zone_name,a.level1 as reg_id,a.level1_name as reg_name,a.level2 as tl_id,a.level2_name as tl_name,a.level3 as area_id,a.level3_name as area_name,'' as level0_sup_id,'' as level0_sup_name,'' as level1_sup_id,'' as level1_sup_name,'' as level2_sup_id,'' as level2_sup_name,'' as level3_sup_id,'' as level3_sup_name,0 as rxCount1,b.sl as rxCount2,0 as med_self1, 0 as med_total1,b.med_self as med_self2,b.med_total as total2 FROM sm_level a,`sm_prescription_head` b WHERE a.cid=b.cid and a.level3=b.area_id and  b.cid='"+cid+"' and b.submit_date>='"+date_from_2+"' and b.submit_date<='"+date_to_2+"' and b.submit_date<'"+current_date+"' "+condition1+")"
    
    records0="select cid,zone_id,zone_name,level0_sup_id,level0_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by cid;"
    
    recordList0=db.executesql(records0,as_dict=True)
          
    records1="select zone_id,reg_id,reg_name,level1_sup_id,level1_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id;"
    recordList1=db.executesql(records1,as_dict=True)

    recordListH0=[]
    recordsH0="select zone_id,level0_sup_id,level0_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id order by zone_id;"
    recordListH0=db.executesql(recordsH0,as_dict=True)

    recordListH1=[]
    recordsH1="select zone_id,level0_sup_id,level0_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id order by zone_id;"
    recordListH1=db.executesql(recordsH1,as_dict=True)

    
    recordList2=[]
    records2="select zone_id,reg_id,tl_id,tl_name,level2_sup_id,level2_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id order by zone_id,reg_id,tl_id;"
    recordList2=db.executesql(records2,as_dict=True)
    
    recordListH2=[]
    recordsH2="select zone_id,reg_id,level0_sup_id,level0_sup_name,level1_sup_id,level1_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id;"
    recordListH2=db.executesql(recordsH2,as_dict=True)

    recordList3=[]
    records3="select zone_id,reg_id,tl_id,area_id,area_name,level3_sup_id,level3_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id,area_id order by zone_id,reg_id,tl_id,area_id;"
    recordList3=db.executesql(records3,as_dict=True)
    
    recordListH3=[]
    recordsH3="select zone_id,reg_id,tl_id,level2_sup_id,level2_sup_name,level1_sup_id,level1_sup_name,level0_sup_id,level0_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id order by zone_id,reg_id,tl_id;"
    recordListH3=db.executesql(recordsH3,as_dict=True)
    
    #sup list
    supListH0=[]
    supListH0="select level_id,sup_id as level0_sup_id,sup_name as level0_sup_name from sm_supervisor_level where cid='"+cid+"' and level_depth_no=0 order by level_id;"
    supListH0=db.executesql(supListH0,as_dict=True)
    
    supListH1=[]
    supListH1="select level_id,sup_id as level1_sup_id,sup_name as level1_sup_name from sm_supervisor_level where cid='"+cid+"' and level_depth_no=1 order by level_id;"
    supListH1=db.executesql(supListH1,as_dict=True)
    
    supListH2=[]
    supListH2="select level_id,sup_id as level2_sup_id,sup_name as level2_sup_name from sm_supervisor_level where cid='"+cid+"' and level_depth_no=2 order by level_id;"
    supListH2=db.executesql(supListH2,as_dict=True)
    
    supListH3=[]
    supListH3="select area_id,rep_id,rep_name from sm_rep_area where cid='"+cid+"' order by area_id;"
    supListH3=db.executesql(supListH3,as_dict=True)
    
    return dict(supListH3=supListH3,supListH2=supListH2,supListH1=supListH1,supListH0=supListH0,pr_year1=pr_year1,pr_year2=pr_year2,pr_quarter1=pr_quarter1,pr_quarter2=pr_quarter2,pr_month1=pr_month1,pr_month2=pr_month2,pr_cycle1=pr_cycle1,pr_cycle2=pr_cycle2,recordListH3=recordListH3,recordList3=recordList3,recordListH2=recordListH2,recordList2=recordList2,recordListH1=recordListH1,recordList1=recordList1,recordListH0=recordListH0,recordList0=recordList0,pr_region=pr_region1,reg_name=reg_name,pr_zone=pr_zone1,pr_area=pr_area1,pr_territory=pr_territory1,pr_doctor=pr_doctor1,pr_ff=pr_ff1,date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2)



def company_track1():
    
    response.title='Company track'
    
    cid=session.cid
    date_from_1=''#request.vars.date_from_1
    date_to_1=''#request.vars.date_to_1   
    
#    date_to_m_1=datetime.datetime.strptime(str(date_to_1),'%Y-%m-%d') 
#    date_to_m_1=date_to_m_1 + datetime.timedelta(days = 1)
    
    date_from_2=''#request.vars.date_from_2
    date_to_2=''#request.vars.date_to_2
    
#    date_to_m_2=datetime.datetime.strptime(str(date_to_2),'%Y-%m-%d') 
#    date_to_m_2=date_to_m_2 + datetime.timedelta(days = 1)
    
    pr_region1=request.vars.pr_region1
    pr_zone1=request.vars.pr_zone1
    pr_area1=request.vars.pr_area1
    pr_territory1=request.vars.pr_territory1
    pr_doctor1=request.vars.pr_doctor1
    pr_ff1=request.vars.pr_ff1
    
    
    if pr_region1=='None':
        pr_region1=''
    
    if pr_zone1=='None':
        pr_zone1=''
    
    if pr_area1=='None':
        pr_area1=''
    
    if pr_territory1=='None':
        pr_territory1=''
    
    if pr_doctor1=='None':
        pr_doctor1=''
    
    if pr_ff1=='None':
        pr_ff1=''
        
    
    pr_year1=request.vars.pr_year1
    pr_quarter1=request.vars.pr_quarter1
    pr_month1=request.vars.pr_month1
    pr_cycle1=request.vars.pr_cycle1
    
    pr_year2=request.vars.pr_year2
    pr_quarter2=request.vars.pr_quarter2
    pr_month2=request.vars.pr_month2
    pr_cycle2=request.vars.pr_cycle2
    
    if pr_year1=='None':
        pr_year1=''
    
    if pr_year2=='None':
        pr_year2=''
    
    if pr_quarter1=='None':
        pr_quarter1=''
    
    if pr_month1=='None':
        pr_month1=''
    
    if pr_cycle1=='None':
        pr_cycle1=''
    
    
    if pr_quarter2=='None':
        pr_quarter2=''
    
    if pr_month2=='None':
        pr_month2=''
    
    if pr_cycle2=='None':
        pr_cycle2=''
    
    stMonth1='00'
    endMonth1='00'
    
    stDay1='00'
    endDay1='00'
    
    stMonth2='00'
    endMonth2='00'
    
    stDay2='00'
    endDay2='00'
        
    if pr_year1!='' and pr_year2!='':
        stMonth1='01'
        endMonth1='12'
        
        stDay1='01'
        endDay1='31'
        
        stMonth2='01'
        endMonth2='12'
        
        stDay2='01'
        endDay2='31'
            

    if pr_year1!='' and pr_year2!='' and pr_quarter1!='' and pr_quarter2!='':
        if pr_quarter1=='1':            
            stMonth1='01'
            endMonth1='03'
            
            stDay1='01'
            endDay1='31'
            
        elif pr_quarter1=='2':
            stMonth1='04'
            endMonth1='06'
            
            stDay1='01'
            endDay1='30'            
            
        elif pr_quarter1=='3':
            stMonth1='07'
            endMonth1='09'
            
            stDay1='01'
            endDay1='31'
            
        elif pr_quarter1=='4':
            stMonth1='10'
            endMonth1='12'
            
            stDay1='01'
            endDay1='31'
                    
        if pr_quarter2=='1':
            stMonth2='01'
            endMonth2='03'
            
            stDay2='01'
            endDay2='31'
                        
        elif pr_quarter2=='2':
            stMonth2='04'
            endMonth2='06'
            
            stDay2='01'
            endDay2='31'
                        
        elif pr_quarter2=='3':
            stMonth2='07'
            endMonth2='09'
            
            stDay2='01'
            endDay2='31'
            
        elif pr_quarter2=='4':
            stMonth2='10'
            endMonth2='12'
            
            stDay2='01'
            endDay2='31'
            
    
    if pr_year1!='' and pr_year2!='' and pr_quarter1!='' and pr_quarter2!='' and pr_month1!='' and pr_month2!='':
            
            stMonth1=pr_month1
            endMonth1=pr_month1
            stDay1='01'
            endDay1='31'
            
            stMonth2=pr_month2
            endMonth2=pr_month2
            stDay2='01'
            endDay2='31'
            
            
    if pr_year1!='' and pr_year2!='' and pr_quarter1!='' and pr_quarter2!='' and pr_month1!='' and pr_month2!='' and pr_cycle1!='' and pr_cycle2!='':
        
        stMonth1=pr_month1
        endMonth1=pr_month1
            
        if pr_cycle1=='1':
            stDay1='01'
            endDay1='07'
        elif pr_cycle1=='2':
            stDay1='08'
            endDay1='15'
        elif pr_cycle1=='3':
            stDay1='16'
            endDay1='21'
        elif pr_cycle1=='4':
            stDay1='22'
            endDay1='31'
        
        stMonth2=pr_month2
        endMonth2=pr_month2
            
        if pr_cycle2=='1':
            stDay2='01'
            endDay2='07'
        elif pr_cycle2=='2':
            stDay2='08'
            endDay2='15'
        elif pr_cycle2=='3':
            stDay2='16'
            endDay2='21'
        elif pr_cycle2=='4':
            stDay2='22'
            endDay2='31'
            
        
    date_from_1=pr_year1+'-'+stMonth1+'-'+stDay1
    date_to_1=pr_year1+'-'+endMonth1+'-'+endDay1
    
    date_from_2=pr_year2+'-'+stMonth2+'-'+stDay2
    date_to_2=pr_year2+'-'+endMonth2+'-'+endDay2
    
            
    #return str(date_from_1)+','+str(date_to_1)+'.......'+str(date_from_2)+','+str(date_to_2)    
    
    reg_name=''
    regionRows=db((db.sm_level.cid==cid)&(db.sm_level.level_id==pr_region1)).select(db.sm_level.level_name,limitby=(0,1))
    if regionRows:
        reg_name=regionRows[0].level_name
        
    
    
    
    condition1=''
    if pr_region1!='':
        condition1+=condition1+" and zone_id = '"+str(pr_region1)+"'"
    if pr_zone1!='':
        condition1+=condition1+" and reg_id = '"+str(pr_zone1)+"'"
    if pr_area1!='':
        condition1+=condition1+" and tl_id = '"+str(pr_area1)+"'"
    if pr_territory1!='':
        condition1+=condition1+" and area_id = '"+str(pr_territory1)+"'"
    if pr_doctor1!='':
        condition1+=condition1+" and doctor_id = '"+str(pr_doctor1)+"'"
    if pr_ff1!='':
        condition1+=condition1+" and submit_by_id = '"+str(pr_ff1)+"'"

    
#    if pr_year1!='' and pr_year2!='':
#        date_to_1=datetime.datetime.strptime(str(date_to_1),'%Y-%m-%d')
#        dateTo_1=date_to_1 + datetime.timedelta(days = 1)        
#        
#        sql1="(SELECT zone_id,zone_name,reg_id,reg_name,tl_id,tl_name,area_id,area_name,level0_sup_id,level0_sup_name,level1_sup_id,level1_sup_name,level2_sup_id,level2_sup_name,level3_sup_id,level3_sup_name,sl as rxCount1,0 as rxCount2, med_self as med_self1,med_total as med_total1, 0 as med_self2, 0 as med_total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and first_date>='"+date_from_1+"' and first_date<'"+str(dateTo_1)[:10]+"' "+condition+")"
#    
#        sql2="(SELECT zone_id,zone_name,reg_id,reg_name,tl_id,tl_name,area_id,area_name,level0_sup_id,level0_sup_name,level1_sup_id,level1_sup_name,level2_sup_id,level2_sup_name,level3_sup_id,level3_sup_name,0 as rxCount1,sl as rxCount2,0 as med_self1, 0 as med_total1,med_self as med_self2,med_total as total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and first_date>='"+date_from_2+"' and submit_date<'"+current_date+"' "+condition+")"
    
    
    #if pr_cycle1!='' and pr_cycle2!='':
    sql1="(SELECT cid,zone_id,zone_name,reg_id,reg_name,tl_id,tl_name,area_id,area_name,level0_sup_id,level0_sup_name,level1_sup_id,level1_sup_name,level2_sup_id,level2_sup_name,level3_sup_id,level3_sup_name,sl as rxCount1,0 as rxCount2, med_self as med_self1,med_total as med_total1, 0 as med_self2, 0 as med_total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_1+"' and submit_date<='"+date_to_1+"'"+condition1+")"
    
    sql2="(SELECT cid,zone_id,zone_name,reg_id,reg_name,tl_id,tl_name,area_id,area_name,level0_sup_id,level0_sup_name,level1_sup_id,level1_sup_name,level2_sup_id,level2_sup_name,level3_sup_id,level3_sup_name,0 as rxCount1,sl as rxCount2,0 as med_self1, 0 as med_total1,med_self as med_self2,med_total as total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_2+"' and submit_date<='"+date_to_2+"' and submit_date<'"+current_date+"' "+condition1+")"
    
    records0="select cid,zone_id,zone_name,level0_sup_id,level0_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by cid;"
    
    recordList0=db.executesql(records0,as_dict=True)
          
    records1="select zone_id,reg_id,reg_name,level1_sup_id,level1_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id;"
    recordList1=db.executesql(records1,as_dict=True)

    recordListH0=[]
    recordsH0="select zone_id,level0_sup_id,level0_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id order by zone_id;"
    recordListH0=db.executesql(recordsH0,as_dict=True)

    recordListH1=[]
    recordsH1="select zone_id,level0_sup_id,level0_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id order by zone_id;"
    recordListH1=db.executesql(recordsH1,as_dict=True)

    
    recordList2=[]
    records2="select zone_id,reg_id,tl_id,tl_name,level2_sup_id,level2_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id order by zone_id,reg_id,tl_id;"
    recordList2=db.executesql(records2,as_dict=True)
    
    recordListH2=[]
    recordsH2="select zone_id,reg_id,level0_sup_id,level0_sup_name,level1_sup_id,level1_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id;"
    recordListH2=db.executesql(recordsH2,as_dict=True)

    recordList3=[]
    records3="select zone_id,reg_id,tl_id,area_id,area_name,level3_sup_id,level3_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id,area_id order by zone_id,reg_id,tl_id,area_id;"
    recordList3=db.executesql(records3,as_dict=True)
    
    recordListH3=[]
    recordsH3="select zone_id,reg_id,tl_id,level2_sup_id,level2_sup_name,level1_sup_id,level1_sup_name,level0_sup_id,level0_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id order by zone_id,reg_id,tl_id;"
    recordListH3=db.executesql(recordsH3,as_dict=True)
    
       
    
    return dict(pr_year1=pr_year1,pr_year2=pr_year2,pr_quarter1=pr_quarter1,pr_quarter2=pr_quarter2,pr_month1=pr_month1,pr_month2=pr_month2,pr_cycle1=pr_cycle1,pr_cycle2=pr_cycle2,recordListH3=recordListH3,recordList3=recordList3,recordListH2=recordListH2,recordList2=recordList2,recordListH1=recordListH1,recordList1=recordList1,recordListH0=recordListH0,recordList0=recordList0,pr_region=pr_region1,reg_name=reg_name,pr_zone=pr_zone1,pr_area=pr_area1,pr_territory=pr_territory1,pr_doctor=pr_doctor1,pr_ff=pr_ff1,date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2)



def institute_track_rm():
    cid=session.cid
    date_from_1=request.vars.date_from_1
    date_to_1=request.vars.date_to_1   
    
    date_to_m_1=datetime.datetime.strptime(str(date_to_1),'%Y-%m-%d') 
    date_to_m_1=date_to_m_1 + datetime.timedelta(days = 1)
    
    date_from_2=request.vars.date_from_2
    date_to_2=request.vars.date_to_2
    
    date_to_m_2=datetime.datetime.strptime(str(date_to_2),'%Y-%m-%d') 
    date_to_m_2=date_to_m_2 + datetime.timedelta(days = 1)
    
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    
    
    
    condition=''
    condition+=condition+" and doctor_category = '"+str('INSTITUTE')+"'"
    
    if pr_region!='':
        condition+=condition+" and zone_id = '"+str(pr_region)+"'"
    if pr_doctor!='':
        condition+=condition+" and doctor_id = '"+str(pr_doctor)+"'"
    if pr_ff!='':
        condition+=condition+" and submit_by_id = '"+str(pr_ff)+"'"

    
    
    sql1="(SELECT zone_id,zone_name,doctor_inst,doctor_chamber_address,level0_sup_id,level0_sup_name,sl as rxCount1,0 as rxCount2, med_self as med_self1,med_total as med_total1, 0 as med_self2, 0 as med_total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_1+"' and submit_date<='"+date_to_1+"'"+condition+")"
    sql2="(SELECT zone_id,zone_name,doctor_inst,doctor_chamber_address,level0_sup_id,level0_sup_name,0 as rxCount1,sl as rxCount2,0 as med_self1, 0 as med_total1,med_self as med_self2,med_total as total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_2+"' and submit_date<='"+date_to_2+"'"+condition+")"
    records="select zone_id,zone_name,doctor_inst,doctor_chamber_address,level0_sup_id,level0_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,doctor_inst;"
    recordList=db.executesql(records,as_dict=True)
  
    return dict(recordList=recordList,date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)

def institute_track_zm():
    cid=session.cid
    date_from_1=request.vars.date_from_1
    date_to_1=request.vars.date_to_1   
    
    date_to_m_1=datetime.datetime.strptime(str(date_to_1),'%Y-%m-%d') 
    date_to_m_1=date_to_m_1 + datetime.timedelta(days = 1)
    
    date_from_2=request.vars.date_from_2
    date_to_2=request.vars.date_to_2
    
    date_to_m_2=datetime.datetime.strptime(str(date_to_2),'%Y-%m-%d') 
    date_to_m_2=date_to_m_2 + datetime.timedelta(days = 1)
    
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    
    
    
    condition=''
    condition+=condition+" and doctor_category = '"+str('INSTITUTE')+"'"
    
    if pr_region!='':
        condition+=condition+" and zone_id = '"+str(pr_region)+"'"
    if pr_zone!='':
        condition+=condition+" and reg_id = '"+str(pr_zone)+"'"
    if pr_doctor!='':
        condition+=condition+" and doctor_id = '"+str(pr_doctor)+"'"
    if pr_ff!='':
        condition+=condition+" and submit_by_id = '"+str(pr_ff)+"'"

    
    
    sql1="(SELECT zone_id,reg_id,reg_name,doctor_inst,doctor_chamber_address,level1_sup_id,level1_sup_name,sl as rxCount1,0 as rxCount2, med_self as med_self1,med_total as med_total1, 0 as med_self2, 0 as med_total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_1+"' and submit_date<='"+date_to_1+"'"+condition+")"
    sql2="(SELECT zone_id,reg_id,reg_name,doctor_inst,doctor_chamber_address,level1_sup_id,level1_sup_name,0 as rxCount1,sl as rxCount2,0 as med_self1, 0 as med_total1,med_self as med_self2,med_total as total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_2+"' and submit_date<='"+date_to_2+"'"+condition+")"
    records="select zone_id,reg_id,reg_name,doctor_inst,doctor_chamber_address,level1_sup_id,level1_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,doctor_inst;"
    recordList=db.executesql(records,as_dict=True)
  
    return dict(recordList=recordList,date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)

def institute_track_am():
    cid=session.cid
    date_from_1=request.vars.date_from_1
    date_to_1=request.vars.date_to_1   
    
    date_to_m_1=datetime.datetime.strptime(str(date_to_1),'%Y-%m-%d') 
    date_to_m_1=date_to_m_1 + datetime.timedelta(days = 1)
    
    date_from_2=request.vars.date_from_2
    date_to_2=request.vars.date_to_2
    
    date_to_m_2=datetime.datetime.strptime(str(date_to_2),'%Y-%m-%d') 
    date_to_m_2=date_to_m_2 + datetime.timedelta(days = 1)
    
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    
    
    
    condition=''
    condition+=condition+" and doctor_category = '"+str('INSTITUTE')+"'"
    
    if pr_region!='':
        condition+=condition+" and zone_id = '"+str(pr_region)+"'"
    if pr_zone!='':
        condition+=condition+" and reg_id = '"+str(pr_zone)+"'"
    if pr_area!='':
        condition+=condition+" and tl_id = '"+str(pr_area)+"'"
    if pr_doctor!='':
        condition+=condition+" and doctor_id = '"+str(pr_doctor)+"'"
    if pr_ff!='':
        condition+=condition+" and submit_by_id = '"+str(pr_ff)+"'"

    
    
    sql1="(SELECT zone_id,reg_id,tl_id,tl_name,doctor_inst,doctor_chamber_address,level2_sup_id,level2_sup_name,sl as rxCount1,0 as rxCount2, med_self as med_self1,med_total as med_total1, 0 as med_self2, 0 as med_total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_1+"' and submit_date<='"+date_to_1+"'"+condition+")"
    sql2="(SELECT zone_id,reg_id,tl_id,tl_name,doctor_inst,doctor_chamber_address,level2_sup_id,level2_sup_name,0 as rxCount1,sl as rxCount2,0 as med_self1, 0 as med_total1,med_self as med_self2,med_total as total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_2+"' and submit_date<='"+date_to_2+"'"+condition+")"
    records="select zone_id,reg_id,tl_id,tl_name,doctor_inst,doctor_chamber_address,level2_sup_id,level2_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id,doctor_inst;"
    recordList=db.executesql(records,as_dict=True)
  
    return dict(recordList=recordList,date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)


def institute_track_mpo():
    cid=session.cid
    date_from_1=request.vars.date_from_1
    date_to_1=request.vars.date_to_1   
    
    date_to_m_1=datetime.datetime.strptime(str(date_to_1),'%Y-%m-%d') 
    date_to_m_1=date_to_m_1 + datetime.timedelta(days = 1)
    
    date_from_2=request.vars.date_from_2
    date_to_2=request.vars.date_to_2
    
    date_to_m_2=datetime.datetime.strptime(str(date_to_2),'%Y-%m-%d') 
    date_to_m_2=date_to_m_2 + datetime.timedelta(days = 1)
    
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    
    
    
    condition=''
    condition+=condition+" and doctor_category = '"+str('INSTITUTE')+"'"
    
    if pr_region!='':
        condition+=condition+" and zone_id = '"+str(pr_region)+"'"
    if pr_zone!='':
        condition+=condition+" and reg_id = '"+str(pr_zone)+"'"
    if pr_area!='':
        condition+=condition+" and tl_id = '"+str(pr_area)+"'"
    if pr_territory!='':
        condition+=condition+" and area_id = '"+str(pr_territory)+"'"
    if pr_doctor!='':
        condition+=condition+" and doctor_id = '"+str(pr_doctor)+"'"
    if pr_ff!='':
        condition+=condition+" and submit_by_id = '"+str(pr_ff)+"'"

    
    
    sql1="(SELECT zone_id,reg_id,tl_id,area_id,area_name,doctor_inst,doctor_chamber_address,level3_sup_id,level3_sup_name,sl as rxCount1,0 as rxCount2, med_self as med_self1,med_total as med_total1, 0 as med_self2, 0 as med_total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_1+"' and submit_date<='"+date_to_1+"'"+condition+")"
    sql2="(SELECT zone_id,reg_id,tl_id,area_id,area_name,doctor_inst,doctor_chamber_address,level3_sup_id,level3_sup_name,0 as rxCount1,sl as rxCount2,0 as med_self1, 0 as med_total1,med_self as med_self2,med_total as total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_2+"' and submit_date<='"+date_to_2+"'"+condition+")"
    records="select zone_id,reg_id,tl_id,area_id,area_name,doctor_inst,doctor_chamber_address,level3_sup_id,level3_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id,area_id,doctor_inst;"
    recordList=db.executesql(records,as_dict=True)
  
    return dict(recordList=recordList,date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)

def institute_track_mpo_d():
    cid=session.cid
    date_from_1=request.vars.date_from_1
    date_to_1=request.vars.date_to_1   
    
    date_to_m_1=datetime.datetime.strptime(str(date_to_1),'%Y-%m-%d') 
    date_to_m_1=date_to_m_1 + datetime.timedelta(days = 1)
    
    date_from_2=request.vars.date_from_2
    date_to_2=request.vars.date_to_2
    
    date_to_m_2=datetime.datetime.strptime(str(date_to_2),'%Y-%m-%d') 
    date_to_m_2=date_to_m_2 + datetime.timedelta(days = 1)
    
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    
    if pr_area==None:
        pr_area=''
    
    if pr_territory==None:
        pr_territory=''
    
    
    condition=''
    condition+=condition+" and doctor_category = '"+str('INSTITUTE')+"'"
    
    if pr_region!='':
        condition+=condition+" and zone_id = '"+str(pr_region)+"'"
    if pr_zone!='':
        condition+=condition+" and reg_id = '"+str(pr_zone)+"'"
    if pr_area!='':
        condition+=condition+" and tl_id = '"+str(pr_area)+"'"
    if pr_territory!='':
        condition+=condition+" and area_id = '"+str(pr_territory)+"'"
    if pr_doctor!='':
        condition+=condition+" and doctor_id = '"+str(pr_doctor)+"'"
    if pr_ff!='':
        condition+=condition+" and submit_by_id = '"+str(pr_ff)+"'"
    
    
    
    
    sql1="(SELECT zone_id,reg_id,tl_id,area_id,area_name,doctor_inst,doctor_chamber_address,level3_sup_id,level3_sup_name,sl as rxCount1,0 as rxCount2, med_self as med_self1,med_total as med_total1, 0 as med_self2, 0 as med_total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_1+"' and submit_date<='"+date_to_1+"'"+condition+")"
    sql2="(SELECT zone_id,reg_id,tl_id,area_id,area_name,doctor_inst,doctor_chamber_address,level3_sup_id,level3_sup_name,0 as rxCount1,sl as rxCount2,0 as med_self1, 0 as med_total1,med_self as med_self2,med_total as total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_2+"' and submit_date<='"+date_to_2+"'"+condition+")"
    records="select zone_id,reg_id,tl_id,area_id,area_name,doctor_inst,doctor_chamber_address,level3_sup_id,level3_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id,area_id,doctor_inst;"
    recordList=db.executesql(records,as_dict=True)
    
    myString='Institute Track MPO \n'     
    myString+='Period 1:'+','+str(date_from_1)+' To '+str(date_to_1)+'\n'            
    myString+='Period 2:'+','+str(date_from_2)+' To '+str(date_to_2)+'\n'
    myString+='RM :'+','+str(pr_region)+'\n'   #+' | '+str(pr_region) 
    myString+='ZM :'+','+str(pr_zone)+'\n'
    myString+='AM :'+','+str(pr_area)+'\n'
    myString+='MPO :'+','+str(pr_territory)+'\n\n\n'        
    
    
    myString+='Region,Zone,Area,MPO,MPO TM,INST Name,P1_RX QTY,P1 Own Med,P1 Other Med,P1 Share,P2_RX QTY,P2 Own Med,P2 Other Med,P2 Share,Growth'+'\n'

    for i in range(len(recordList)):
        recordListStr=recordList[i]
        
        zone_id=recordListStr['zone_id']
        reg_id=recordListStr['reg_id']
        tl_id=recordListStr['tl_id']
        area_id=recordListStr['area_id']
        area_name=recordListStr['area_name']
        doctor_inst=recordListStr['doctor_inst']
        rxCount1=recordListStr['rxCount1']
        med_self1=recordListStr['med_self1']
        med_total1=recordListStr['med_total1']
        perP1=recordListStr['perP1']
        rxCount2=recordListStr['rxCount2']
        med_self2=recordListStr['med_self2']
        med_total2=recordListStr['med_total2']
        perP2=recordListStr['perP2']
        growth=recordListStr['growth']
        
        otherMed1=med_total1-med_self1
        otherMed2=med_total2-med_self2
        
        if perP1==None:
            perP1=''
        
        if perP2==None:
            perP2=''
        
        if growth==None:
            growth=''
             
        myString+=str(zone_id)+','+str(reg_id)+','+str(tl_id)+','+str(area_id)+','+str(area_name)+','+str(doctor_inst)+','+\
        str(rxCount1)+','+str(med_self1)+','+str(otherMed1)+','+str(perP1)+','+str(rxCount2)+','+str(med_self2)+','+\
        str(otherMed2)+','+str(perP2)+','+str(growth)+'\n'
        
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=institute_track_mpo.csv'   
    return str(myString)

def physician_track_d():
    cid=session.cid
    date_from=request.vars.date_from
    date_to=request.vars.date_to

    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    
    
    condition=''
    if pr_region!='':
        condition+=condition+" and zone_id = '"+str(pr_region)+"'"
    if pr_zone!='':
        condition+=condition+" and reg_id = '"+str(pr_zone)+"'"
    if pr_area!='':
        condition+=condition+" and reg_id = '"+str(pr_area)+"'"
    if pr_territory!='':
        condition+=condition+" and area_id = '"+str(pr_territory)+"'"
    if pr_doctor!='':
        condition+=condition+" and doctor_id = '"+str(pr_doctor)+"'"

    
    
    sql1="(SELECT zone_id,reg_id,tl_id,area_id,doctor_id,doctor_name,doctor_speciality,doctor_chamber_address,sl as rxSelfCount, sl as rxTotalCount,med_self as rxSelfMed, 0 as rxTotalMed,level3_sup_id,level3_sup_name,level2_sup_id,level2_sup_name,level1_sup_id,level1_sup_name,level0_sup_id,level0_sup_name FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from+"' and submit_date<='"+date_to+"' and med_self>0 "+condition+")"
    sql2="(SELECT zone_id,reg_id,tl_id,area_id,doctor_id,doctor_name,doctor_speciality,doctor_chamber_address,0 as rxSelfCount,sl as rxTotalCount,0 as rxSelfMed, med_total as rxTotalMed,level3_sup_id,level3_sup_name,level2_sup_id,level2_sup_name,level1_sup_id,level1_sup_name,level0_sup_id,level0_sup_name FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from+"' and submit_date<='"+date_to+"'"+condition+")"
    records="select zone_id,reg_id,tl_id,area_id,doctor_id,doctor_name,doctor_speciality,doctor_chamber_address,count(distinct(rxSelfCount))-1 as rxSelfCount,count(distinct(rxTotalCount)) as rxTotalCount,sum(rxSelfMed) as rxSelfMed,sum(rxTotalMed) as rxTotalMed,level3_sup_id,level3_sup_name,level2_sup_id,level2_sup_name,level1_sup_id,level1_sup_name,level0_sup_id,level0_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id,area_id,doctor_id;"

    recordList=db.executesql(records,as_dict=True)
    
    recordsH="select zone_id,reg_id,tl_id,area_id,level3_sup_id,level3_sup_name,level2_sup_id,level2_sup_name,level1_sup_id,level1_sup_name,level0_sup_id,level0_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id,area_id;"
    recordListH=db.executesql(recordsH,as_dict=True)
    
    myString='Physician Track \n'     
    myString+='Period:'+','+str(date_from)+' To '+str(date_to)+'\n' 
    myString+='RM :'+','+str(pr_region)+'\n' 
    myString+='ZM :'+','+str(pr_zone)+'\n'
    myString+='AM :'+','+str(pr_area)+'\n'
    myString+='MPO :'+','+str(pr_territory)+'\n\n\n'        
    
    
    
#    for j in range(len(recordListH)):
#        recordListStrH=recordListH[j]
#        
#        myString+=recordListStrH['area_id']+' : '+str(recordListStrH['level3_sup_name']).replace(',',';')+' '+recordListStrH['tl_id']+' : '+str(recordListStrH['level2_sup_name']).replace(',',';')+' '+recordListStrH['reg_id']+' : '+str(recordListStrH['level1_sup_name']).replace(',',';')+' '+recordListStrH['zone_id']+' : '+str(recordListStrH['level0_sup_name']).replace(',',';')+'\n'
    
    myString+='MPO,Phy ID,Physician Name,Specialization,Chamber Address,Base,IPI,PER(%)'+'\n'

    for i in range(len(recordList)):
        recordListStr=recordList[i]
        
        #if recordListStrH['area_id']==recordListStr['area_id']:             
        area_id=recordListStr['area_id']
        doctor_id=recordListStr['doctor_id']
        doctor_name=str(recordListStr['doctor_name']).replace(',', ' ')
        doctor_speciality=str(recordListStr['doctor_speciality']).replace(',', ' ')
        doctor_chamber_address=recordListStr['doctor_chamber_address'].replace(',',' ')
        #rxSelfCount=recordListStr['rxSelfCount']
        
#                if int(rxTotalCount)>0:        
#                    selfPrPer=round((float(rxSelfCount)/float(rxTotalCount)*100),3)
#                else:
#                    selfPrPer=0
        
        rxTotalMed=recordListStr['rxTotalMed']
        rxSelfMed=recordListStr['rxSelfMed'] 
        
        if int(rxTotalMed)>0:       
            selfMedPrPer=round((float(rxSelfMed)/float(rxTotalMed)*100),3)
        else:
            selfMedPrPer=0
        
        
        try:
            doctor_name=str(doctor_name)
        except:
            doctor_name='11'
        
        try:
            doctor_speciality=str(doctor_speciality)
        except:
            doctor_speciality='22'
        
        try:
            doctor_chamber_address=str(doctor_chamber_address)
        except:
            doctor_chamber_address='33'
        
                     
        myString+=str(area_id)+','+str(doctor_id)+','+str(doctor_name)+','+str(doctor_speciality)\
        +','+str(doctor_chamber_address)+','+str(rxTotalMed)+','+str(rxSelfMed)+','+str(selfMedPrPer)+'\n'
        
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=physician_track.csv'   
    return str(myString)


def physician_track():
    cid=session.cid
    date_from=request.vars.date_from
    date_to=request.vars.date_to

    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    
    
    condition=''
    if pr_region!='':
        condition+=condition+" and zone_id = '"+str(pr_region)+"'"
    if pr_zone!='':
        condition+=condition+" and reg_id = '"+str(pr_zone)+"'"
    if pr_area!='':
        condition+=condition+" and reg_id = '"+str(pr_area)+"'"
    if pr_territory!='':
        condition+=condition+" and area_id = '"+str(pr_territory)+"'"
    if pr_doctor!='':
        condition+=condition+" and doctor_id = '"+str(pr_doctor)+"'"

    
    
    sql1="(SELECT zone_id,reg_id,tl_id,area_id,doctor_id,doctor_name,doctor_speciality,doctor_chamber_address,sl as rxSelfCount, sl as rxTotalCount,med_self as rxSelfMed, 0 as rxTotalMed,level3_sup_id,level3_sup_name,level2_sup_id,level2_sup_name,level1_sup_id,level1_sup_name,level0_sup_id,level0_sup_name FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from+"' and submit_date<='"+date_to+"' and med_self>0 "+condition+")"
    sql2="(SELECT zone_id,reg_id,tl_id,area_id,doctor_id,doctor_name,doctor_speciality,doctor_chamber_address,0 as rxSelfCount,sl as rxTotalCount,0 as rxSelfMed, med_total as rxTotalMed,level3_sup_id,level3_sup_name,level2_sup_id,level2_sup_name,level1_sup_id,level1_sup_name,level0_sup_id,level0_sup_name FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from+"' and submit_date<='"+date_to+"'"+condition+")"
    records="select zone_id,reg_id,tl_id,area_id,doctor_id,doctor_name,doctor_speciality,doctor_chamber_address,count(distinct(rxSelfCount))-1 as rxSelfCount,count(distinct(rxTotalCount)) as rxTotalCount,sum(rxSelfMed) as rxSelfMed,sum(rxTotalMed) as rxTotalMed,level3_sup_id,level3_sup_name,level2_sup_id,level2_sup_name,level1_sup_id,level1_sup_name,level0_sup_id,level0_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id,area_id,doctor_id;"

    recordList=db.executesql(records,as_dict=True)
    
    recordsH="select zone_id,reg_id,tl_id,area_id,level3_sup_id,level3_sup_name,level2_sup_id,level2_sup_name,level1_sup_id,level1_sup_name,level0_sup_id,level0_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id,area_id;"
    recordListH=db.executesql(recordsH,as_dict=True)
    
    return dict(recordListH=recordListH,recordList=recordList,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)

#

def company_track_d1():
    cid=session.cid
    date_from_1=request.vars.date_from_1
    date_to_1=request.vars.date_to_1   
    
    date_to_m_1=datetime.datetime.strptime(str(date_to_1),'%Y-%m-%d') 
    date_to_m_1=date_to_m_1 + datetime.timedelta(days = 1)
    
    date_from_2=request.vars.date_from_2
    date_to_2=request.vars.date_to_2
    
    date_to_m_2=datetime.datetime.strptime(str(date_to_2),'%Y-%m-%d') 
    date_to_m_2=date_to_m_2 + datetime.timedelta(days = 1)
    
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    
    
    pr_year1=request.vars.pr_year1
    pr_quarter1=request.vars.pr_quarter1
    pr_month1=request.vars.pr_month1
    pr_cycle1=request.vars.pr_cycle1
    
    pr_year2=request.vars.pr_year2
    pr_quarter2=request.vars.pr_quarter2
    pr_month2=request.vars.pr_month2
    pr_cycle2=request.vars.pr_cycle2

    if pr_year1=='None':
        pr_year1=''
    
    if pr_year2=='None':
        pr_year2=''
    
    if pr_quarter1=='None':
        pr_quarter1=''
    
    if pr_month1=='None':
        pr_month1=''
    
    if pr_cycle1=='None':
        pr_cycle1=''
    
    
    if pr_quarter2=='None':
        pr_quarter2=''
    
    if pr_month2=='None':
        pr_month2=''
    
    if pr_cycle2=='None':
        pr_cycle2=''    
    
    stMonth1='00'
    endMonth1='00'
    
    stDay1='00'
    endDay1='00'
    
    stMonth2='00'
    endMonth2='00'
    
    stDay2='00'
    endDay2='00'
        
    if pr_year1!='' and pr_year2!='':
        stMonth1='01'
        endMonth1='12'
        
        stDay1='01'
        endDay1='31'
        
        stMonth2='01'
        endMonth2='12'
        
        stDay2='01'
        endDay2='31'
            

    if pr_year1!='' and pr_year2!='' and pr_quarter1!='' and pr_quarter2!='':
        if pr_quarter1=='1':            
            stMonth1='01'
            endMonth1='03'
            
            stDay1='01'
            endDay1='31'
            
        elif pr_quarter1=='2':
            stMonth1='04'
            endMonth1='06'
            
            stDay1='01'
            endDay1='30'            
            
        elif pr_quarter1=='3':
            stMonth1='07'
            endMonth1='09'
            
            stDay1='01'
            endDay1='31'
            
        elif pr_quarter1=='4':
            stMonth1='10'
            endMonth1='12'
            
            stDay1='01'
            endDay1='31'
                    
        if pr_quarter2=='1':
            stMonth2='01'
            endMonth2='03'
            
            stDay2='01'
            endDay2='31'
                        
        elif pr_quarter2=='2':
            stMonth2='04'
            endMonth2='06'
            
            stDay2='01'
            endDay2='31'
                        
        elif pr_quarter2=='3':
            stMonth2='07'
            endMonth2='09'
            
            stDay2='01'
            endDay2='31'
            
        elif pr_quarter2=='4':
            stMonth2='10'
            endMonth2='12'
            
            stDay2='01'
            endDay2='31'
            
    
    if pr_year1!='' and pr_year2!='' and pr_quarter1!='' and pr_quarter2!='' and pr_month1!='' and pr_month2!='':
            
            stMonth1=pr_month1
            endMonth1=pr_month1
            stDay1='01'
            endDay1='31'
            
            stMonth2=pr_month2
            endMonth2=pr_month2
            stDay2='01'
            endDay2='31'
            
            
    if pr_year1!='' and pr_year2!='' and pr_quarter1!='' and pr_quarter2!='' and pr_month1!='' and pr_month2!='' and pr_cycle1!='' and pr_cycle2!='':
        
        stMonth1=pr_month1
        endMonth1=pr_month1
            
        if pr_cycle1=='1':
            stDay1='01'
            endDay1='07'
        elif pr_cycle1=='2':
            stDay1='08'
            endDay1='15'
        elif pr_cycle1=='3':
            stDay1='16'
            endDay1='21'
        elif pr_cycle1=='4':
            stDay1='22'
            endDay1='31'
        
        stMonth2=pr_month2
        endMonth2=pr_month2
            
        if pr_cycle2=='1':
            stDay2='01'
            endDay2='07'
        elif pr_cycle2=='2':
            stDay2='08'
            endDay2='15'
        elif pr_cycle2=='3':
            stDay2='16'
            endDay2='21'
        elif pr_cycle2=='4':
            stDay2='22'
            endDay2='31'
            
        
    date_from_1=pr_year1+'-'+stMonth1+'-'+stDay1
    date_to_1=pr_year1+'-'+endMonth1+'-'+endDay1
    
    date_from_2=pr_year2+'-'+stMonth2+'-'+stDay2
    date_to_2=pr_year2+'-'+endMonth2+'-'+endDay2
        
    #return str(date_from_1)+','+str(date_to_1)+'.......'+str(date_from_2)+','+str(date_to_2)    
    
    
    condition=''
    if pr_region!='':
        condition+=condition+" and zone_id = '"+str(pr_region)+"'"
    if pr_zone!='':
        condition+=condition+" and reg_id = '"+str(pr_zone)+"'"
    if pr_area!='':
        condition+=condition+" and tl_id = '"+str(pr_area)+"'"
    if pr_territory!='':
        condition+=condition+" and area_id = '"+str(pr_territory)+"'"
    if pr_doctor!='':
        condition+=condition+" and doctor_id = '"+str(pr_doctor)+"'"
    if pr_ff!='':
        condition+=condition+" and submit_by_id = '"+str(pr_ff)+"'"

    
    
    sql1="(SELECT cid,zone_id,zone_name,reg_id,reg_name,tl_id,tl_name,area_id,area_name,level0_sup_id,level0_sup_name,level1_sup_id,level1_sup_name,level2_sup_id,level2_sup_name,level3_sup_id,level3_sup_name,sl as rxCount1,0 as rxCount2, med_self as med_self1,med_total as med_total1, 0 as med_self2, 0 as med_total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_1+"' and submit_date<='"+date_to_1+"'"+condition+")"
    
    sql2="(SELECT cid,zone_id,zone_name,reg_id,reg_name,tl_id,tl_name,area_id,area_name,level0_sup_id,level0_sup_name,level1_sup_id,level1_sup_name,level2_sup_id,level2_sup_name,level3_sup_id,level3_sup_name,0 as rxCount1,sl as rxCount2,0 as med_self1, 0 as med_total1,med_self as med_self2,med_total as total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_2+"' and submit_date<='"+date_to_2+"' and submit_date<'"+current_date+"' "+condition+")"
    
    records0="select cid,zone_id,zone_name,level0_sup_id,level0_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by cid;"
    recordList0=db.executesql(records0,as_dict=True)
          
    records1="select zone_id,reg_id,reg_name,level1_sup_id,level1_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id;"
    recordList1=db.executesql(records1,as_dict=True)

    recordListH0=[]
    recordsH0="select zone_id,level0_sup_id,level0_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id order by zone_id;"
    recordListH0=db.executesql(recordsH0,as_dict=True)
    
    recordsH1="select zone_id,level0_sup_id,level0_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id order by zone_id;"
    recordListH1=db.executesql(recordsH1,as_dict=True)

    
    records2="select zone_id,reg_id,tl_id,tl_name,level2_sup_id,level2_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id order by zone_id,reg_id,tl_id;"
    recordList2=db.executesql(records2,as_dict=True)
    
    recordsH2="select zone_id,reg_id,level0_sup_id,level0_sup_name,level1_sup_id,level1_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id;"
    recordListH2=db.executesql(recordsH2,as_dict=True)

  
    records3="select zone_id,reg_id,tl_id,area_id,area_name,level3_sup_id,level3_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id,area_id order by zone_id,reg_id,tl_id,area_id;"
    recordList3=db.executesql(records3,as_dict=True)
    
    recordsH3="select zone_id,reg_id,tl_id,level2_sup_id,level2_sup_name,level1_sup_id,level1_sup_name,level0_sup_id,level0_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id order by zone_id,reg_id,tl_id;"
    recordListH3=db.executesql(recordsH3,as_dict=True)
    
    myString='Company Track \n'     
    #myString+='Previous:'+','+str(date_from_1)+' to '+str(date_to_1)+'\n' 
    #myString+='Current:'+','+str(date_from_2)+' to '+str(date_to_2)+'\n' 
    myString+='RM :'+','+str(pr_region)+'\n' 
    myString+='ZM :'+','+str(pr_zone)+'\n'
    myString+='AM :'+','+str(pr_area)+'\n'
    myString+='MPO :'+','+str(pr_territory)+'\n\n\n'        
    
    
    filter1=''
    filter2=''
    
    if pr_year1!='':
        filter1=str(pr_year1)
    
    if pr_year2!='':
        filter2=str(pr_year2)
    
    if pr_quarter1!='':
        filter1='Q'+str(pr_quarter1)+' '+str(pr_year1)
    
    if pr_quarter2!='':
        filter2='Q'+str(pr_quarter2)+' '+str(pr_year2)
     
        
    if pr_month1!='':
        filter1='Q'+str(pr_quarter1)+' '+datetime.datetime.strptime(str(date_from_1),'%Y-%m-%d').strftime('%b-%y')
    
    if pr_month2!='':
        filter2='Q'+str(pr_quarter2)+' '+datetime.datetime.strptime(str(date_from_2),'%Y-%m-%d').strftime('%b-%y')
    
    
    if pr_cycle1!='':
        filter1='C'+pr_cycle1+' '+str(datetime.datetime.strptime(str(date_from_1),'%Y-%m-%d').strftime('%b-%y'))
    
    if pr_cycle2!='':
        filter2='C'+pr_cycle1+' '+str(datetime.datetime.strptime(str(date_from_2),'%Y-%m-%d').strftime('%b-%y'))
        

    # rm
    for j in range(len(recordListH0)):
        recordListStrH0=recordListH0[j]
        
        myString+=recordListStrH0['zone_id']+':'+recordListStrH0['level0_sup_name']+'\n'
              
    
        myString+='RM,RM TM,RM Name,Base '+filter1+',IPI '+filter1+',PER(%) '+filter1+',Base '+filter2+',IPI '+filter2+',PER(%) '+filter2+',Growth(%)'+'\n'
    
        for i in range(len(recordList0)):
            recordListStr0=recordList0[i] 
               
            reg_id=recordListStr0['zone_id']
            reg_name=recordListStr0['zone_name']
            level1_sup_name=recordListStr0['level0_sup_name'].replace(',',' ')
            med_total1=recordListStr0['med_total1']
            ipi_med=recordListStr0['med_self1']
            perP1=recordListStr0['perP1']
            med_total2=recordListStr0['med_total2']
            ipi_med2=recordListStr0['med_self2']
            perP2=recordListStr0['perP2']
            growth=recordListStr0['growth']
            
            try:
                level1_sup_name=str(level1_sup_name)
            except:
                level1_sup_name='11'
            
            if perP1==None:
                perP1=''
            
            if perP2==None:
                perP2=''
            
            if growth==None:
                growth=''
            
                         
            myString+=str(reg_id)+','+str(reg_name)+','+str(level1_sup_name)+','+str(med_total1)+','+str(ipi_med)+','+str(perP1)+','+\
            str(med_total2)+','+str(ipi_med2)+','+str(perP2)+','+str(growth)+'\n'
        
    myString+='\n\n'    
    # zm
    for j in range(len(recordListH1)):
        recordListStrH1=recordListH1[j]
        
        myString+=recordListStrH1['zone_id']+':'+recordListStrH1['level0_sup_name']+'\n'
              
    
        myString+='ZM,ZM TM,ZM Name,Base '+filter1+',IPI '+filter1+',PER(%) '+filter1+',Base '+filter2+',IPI '+filter2+',PER(%) '+filter2+',Growth(%)'+'\n'
    
        for i in range(len(recordList1)):
            recordListStr1=recordList1[i]        
            if recordListStrH1['zone_id']==recordListStr1['zone_id']:       
                reg_id=recordListStr1['reg_id']
                reg_name=recordListStr1['reg_name']
                level1_sup_name=recordListStr1['level1_sup_name'].replace(',',' ')
                med_total1=recordListStr1['med_total1']
                ipi_med=recordListStr1['med_self1']
                perP1=recordListStr1['perP1']
                med_total2=recordListStr1['med_total2']
                ipi_med2=recordListStr1['med_self2']
                perP2=recordListStr1['perP2']
                growth=recordListStr1['growth']
                
                try:
                    level1_sup_name=str(level1_sup_name)
                except:
                    level1_sup_name='11'
                
                if perP1==None:
                    perP1=''
                
                if perP2==None:
                    perP2=''
                
                if growth==None:
                    growth=''
                
                             
                myString+=str(reg_id)+','+str(reg_name)+','+str(level1_sup_name)+','+str(med_total1)+','+str(ipi_med)+','+str(perP1)+','+\
                str(med_total2)+','+str(ipi_med2)+','+str(perP2)+','+str(growth)+'\n'
        
    myString+='\n\n'
    
    # am
    for j in range(len(recordListH2)):
        recordListStrH2=recordListH2[j]
        
        myString+=recordListStrH2['reg_id']+':'+recordListStrH2['level1_sup_name']+'    ,    '+recordListStrH2['zone_id']+':'+recordListStrH2['level0_sup_name']+'\n'
              
    
        myString+='AM,AM TM,AM Name,Base '+filter1+',IPI '+filter1+',PER(%) '+filter1+',Base '+filter2+',IPI '+filter2+',PER(%) '+filter2+',Growth(%)'+'\n'
    
        for i in range(len(recordList2)):
            recordListStr2=recordList2[i]        
            if recordListStrH2['zone_id']==recordListStr2['zone_id'] and recordListStrH2['reg_id']==recordListStr2['reg_id']:       
                tl_id=recordListStr2['tl_id']
                tl_name=recordListStr2['tl_name']
                level2_sup_name=recordListStr2['level2_sup_name'].replace(',',' ')
                med_total1=recordListStr2['med_total1']
                ipi_med=recordListStr2['med_self1']
                perP1=recordListStr2['perP1']
                med_total2=recordListStr2['med_total2']
                ipi_med2=recordListStr2['med_self2']
                perP2=recordListStr2['perP2']
                growth=recordListStr2['growth']
                
                try:
                    level2_sup_name=str(level2_sup_name)
                except:
                    level2_sup_name='11'
                
                if perP1==None:
                    perP1=''
                
                if perP2==None:
                    perP2=''
                
                if growth==None:
                    growth=''
                
                             
                myString+=str(tl_id)+','+str(tl_name)+','+str(level2_sup_name)+','+str(med_total1)+','+str(ipi_med)+','+str(perP1)+','+\
                str(med_total2)+','+str(ipi_med2)+','+str(perP2)+','+str(growth)+'\n'
    
    myString+='\n\n'    
    # mpo
    for j in range(len(recordListH3)):
        recordListStrH3=recordListH3[j]
        
        myString+=recordListStrH3['tl_id']+':'+recordListStrH3['level2_sup_name']+'    ,    '+recordListStrH3['reg_id']+':'+recordListStrH3['level1_sup_name']+'    ,    '+recordListStrH3['zone_id']+':'+recordListStrH3['level0_sup_name']+'\n'
              
    
        myString+='MPO,MPO TM,MPO Name,Base '+filter1+',IPI '+filter1+',PER(%) '+filter1+',Base '+filter2+',IPI '+filter2+',PER(%) '+filter2+',Growth(%)'+'\n'
    
        for i in range(len(recordList3)):
            recordListStr3=recordList3[i]        
            if recordListStrH3['zone_id']==recordListStr3['zone_id'] and recordListStrH3['reg_id']==recordListStr3['reg_id'] and recordListStrH3['tl_id']==recordListStr3['tl_id']:       
                area_id=recordListStr3['area_id']
                area_name=recordListStr3['area_name']
                level3_sup_name=recordListStr3['level3_sup_name'].replace(',',' ')
                med_total1=recordListStr3['med_total1']
                ipi_med=recordListStr3['med_self1']
                perP1=recordListStr3['perP1']
                med_total2=recordListStr3['med_total2']
                ipi_med2=recordListStr3['med_self2']
                perP2=recordListStr3['perP2']
                growth=recordListStr3['growth']
                
                try:
                    level3_sup_name=str(level3_sup_name)
                except:
                    level3_sup_name='11'
                
                if perP1==None:
                    perP1=''
                
                if perP2==None:
                    perP2=''
                
                if growth==None:
                    growth=''
                
                             
                myString+=str(area_id)+','+str(area_name)+','+str(level3_sup_name)+','+str(med_total1)+','+str(ipi_med)+','+str(perP1)+','+\
                str(med_total2)+','+str(ipi_med2)+','+str(perP2)+','+str(growth)+'\n'
    
    
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=Company_track.csv'   
    return str(myString)



def company_track():
    cid=session.cid
    date_from_1=request.vars.date_from_1
    date_to_1=request.vars.date_to_1   
    
    date_to_m_1=datetime.datetime.strptime(str(date_to_1),'%Y-%m-%d') 
    date_to_m_1=date_to_m_1 + datetime.timedelta(days = 1)
    
    date_from_2=request.vars.date_from_2
    date_to_2=request.vars.date_to_2
    
    date_to_m_2=datetime.datetime.strptime(str(date_to_2),'%Y-%m-%d') 
    date_to_m_2=date_to_m_2 + datetime.timedelta(days = 1)
    
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    
    
    
    condition=''
    if pr_region!='':
        condition+=condition+" and zone_id = '"+str(pr_region)+"'"
    if pr_zone!='':
        condition+=condition+" and reg_id = '"+str(pr_zone)+"'"
    if pr_area!='':
        condition+=condition+" and tl_id = '"+str(pr_area)+"'"
    if pr_territory!='':
        condition+=condition+" and area_id = '"+str(pr_territory)+"'"
    if pr_doctor!='':
        condition+=condition+" and doctor_id = '"+str(pr_doctor)+"'"
    if pr_ff!='':
        condition+=condition+" and submit_by_id = '"+str(pr_ff)+"'"

    
    
    sql1="(SELECT zone_id,zone_name,reg_id,reg_name,tl_id,tl_name,area_id,area_name,level0_sup_id,level0_sup_name,level1_sup_id,level1_sup_name,level2_sup_id,level2_sup_name,level3_sup_id,level3_sup_name,sl as rxCount1,0 as rxCount2, med_self as med_self1,med_total as med_total1, 0 as med_self2, 0 as med_total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_1+"' and submit_date<='"+date_to_1+"'"+condition+")"
    sql2="(SELECT zone_id,zone_name,reg_id,reg_name,tl_id,tl_name,area_id,area_name,level0_sup_id,level0_sup_name,level1_sup_id,level1_sup_name,level2_sup_id,level2_sup_name,level3_sup_id,level3_sup_name,0 as rxCount1,sl as rxCount2,0 as med_self1, 0 as med_total1,med_self as med_self2,med_total as total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_2+"' and submit_date<='"+date_to_2+"'"+condition+")"

    records1="select zone_id,reg_id,reg_name,level1_sup_id,level1_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id;"
    recordList1=db.executesql(records1,as_dict=True)
    
    recordsH1="select zone_id,level0_sup_id,level0_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id order by zone_id;"
    recordListH1=db.executesql(recordsH1,as_dict=True)

    
    records2="select zone_id,reg_id,tl_id,tl_name,level2_sup_id,level2_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id order by zone_id,reg_id,tl_id;"
    recordList2=db.executesql(records2,as_dict=True)
    
    recordsH2="select zone_id,reg_id,level0_sup_id,level0_sup_name,level1_sup_id,level1_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id;"
    recordListH2=db.executesql(recordsH2,as_dict=True)

  
    records3="select zone_id,reg_id,tl_id,area_id,area_name,level3_sup_id,level3_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id,area_id order by zone_id,reg_id,tl_id,area_id;"
    recordList3=db.executesql(records3,as_dict=True)
    
    recordsH3="select zone_id,reg_id,tl_id,level2_sup_id,level2_sup_name,level1_sup_id,level1_sup_name,level0_sup_id,level0_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id order by zone_id,reg_id,tl_id;"
    recordListH3=db.executesql(recordsH3,as_dict=True)
    
    
    
   
    
    return dict(recordListH3=recordListH3,recordList3=recordList3,recordListH2=recordListH2,recordList2=recordList2,recordListH1=recordListH1,recordList1=recordList1,date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)


def company_track_d():
    cid=session.cid
    date_from_1=request.vars.date_from_1
    date_to_1=request.vars.date_to_1   
    
    date_to_m_1=datetime.datetime.strptime(str(date_to_1),'%Y-%m-%d') 
    date_to_m_1=date_to_m_1 + datetime.timedelta(days = 1)
    
    date_from_2=request.vars.date_from_2
    date_to_2=request.vars.date_to_2
    
    date_to_m_2=datetime.datetime.strptime(str(date_to_2),'%Y-%m-%d') 
    date_to_m_2=date_to_m_2 + datetime.timedelta(days = 1)
    
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    
    
    condition=''
    if pr_region!='':
        condition+=condition+" and zone_id = '"+str(pr_region)+"'"
    if pr_zone!='':
        condition+=condition+" and reg_id = '"+str(pr_zone)+"'"
    if pr_area!='':
        condition+=condition+" and tl_id = '"+str(pr_area)+"'"
    if pr_territory!='':
        condition+=condition+" and area_id = '"+str(pr_territory)+"'"
    if pr_doctor!='':
        condition+=condition+" and doctor_id = '"+str(pr_doctor)+"'"
    if pr_ff!='':
        condition+=condition+" and submit_by_id = '"+str(pr_ff)+"'"

    
    
    sql1="(SELECT zone_id,zone_name,reg_id,reg_name,tl_id,tl_name,area_id,area_name,level0_sup_id,level0_sup_name,level1_sup_id,level1_sup_name,level2_sup_id,level2_sup_name,level3_sup_id,level3_sup_name,sl as rxCount1,0 as rxCount2, med_self as med_self1,med_total as med_total1, 0 as med_self2, 0 as med_total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_1+"' and submit_date<='"+date_to_1+"'"+condition+")"
    sql2="(SELECT zone_id,zone_name,reg_id,reg_name,tl_id,tl_name,area_id,area_name,level0_sup_id,level0_sup_name,level1_sup_id,level1_sup_name,level2_sup_id,level2_sup_name,level3_sup_id,level3_sup_name,0 as rxCount1,sl as rxCount2,0 as med_self1, 0 as med_total1,med_self as med_self2,med_total as total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_2+"' and submit_date<='"+date_to_2+"'"+condition+")"

    records1="select zone_id,reg_id,reg_name,level1_sup_id,level1_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id;"
    recordList1=db.executesql(records1,as_dict=True)
    
    recordsH1="select zone_id,level0_sup_id,level0_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id order by zone_id;"
    recordListH1=db.executesql(recordsH1,as_dict=True)

    
    records2="select zone_id,reg_id,tl_id,tl_name,level2_sup_id,level2_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id order by zone_id,reg_id,tl_id;"
    recordList2=db.executesql(records2,as_dict=True)
    
    recordsH2="select zone_id,reg_id,level0_sup_id,level0_sup_name,level1_sup_id,level1_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id;"
    recordListH2=db.executesql(recordsH2,as_dict=True)

  
    records3="select zone_id,reg_id,tl_id,area_id,area_name,level3_sup_id,level3_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id,area_id order by zone_id,reg_id,tl_id,area_id;"
    recordList3=db.executesql(records3,as_dict=True)
    
    recordsH3="select zone_id,reg_id,tl_id,level2_sup_id,level2_sup_name,level1_sup_id,level1_sup_name,level0_sup_id,level0_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id order by zone_id,reg_id,tl_id;"
    recordListH3=db.executesql(recordsH3,as_dict=True)
    
    myString='Company Track \n'     
    myString+='Previous:'+','+str(date_from_1)+' to '+str(date_to_1)+'\n' 
    myString+='Current:'+','+str(date_from_2)+' to '+str(date_to_2)+'\n' 
    myString+='RM :'+','+str(pr_region)+'\n' 
    myString+='ZM :'+','+str(pr_zone)+'\n'
    myString+='AM :'+','+str(pr_area)+'\n'
    myString+='MPO :'+','+str(pr_territory)+'\n\n\n'        
    
    # rm
    for j in range(len(recordListH1)):
        recordListStrH1=recordListH1[j]
        
        myString+=recordListStrH1['zone_id']+':'+recordListStrH1['level0_sup_name']+'\n'
              
    
        myString+='RM,RM TM,RM Name,Previous Base,Previous IPI,Previous PER(%),Current Base,Current IPI,Current PER(%),Growth(%)'+'\n'
    
        for i in range(len(recordList1)):
            recordListStr1=recordList1[i]        
            if recordListStrH1['zone_id']==recordListStr1['zone_id']:       
                reg_id=recordListStr1['reg_id']
                reg_name=recordListStr1['reg_name']
                level1_sup_name=recordListStr1['level1_sup_name']
                med_total1=recordListStr1['med_total1']
                ipi_med=recordListStr1['med_self1']
                perP1=recordListStr1['perP1']
                med_total2=recordListStr1['med_total2']
                ipi_med2=recordListStr1['med_self2']
                perP2=recordListStr1['perP2']
                growth=recordListStr1['growth']
                
                try:
                    level1_sup_name=str(level1_sup_name)
                except:
                    level1_sup_name='11'
                
                if perP1==None:
                    perP1=''
                
                if perP2==None:
                    perP2=''
                
                if growth==None:
                    growth=''
                
                             
                myString+=str(reg_id)+','+str(reg_name)+','+str(level1_sup_name)+','+str(med_total1)+','+str(ipi_med)+','+str(perP1)+','+\
                str(med_total1)+','+str(ipi_med2)+','+str(perP2)+','+str(growth)+'\n'
        
    myString+='\n\n'
    
    # am
    for j in range(len(recordListH2)):
        recordListStrH2=recordListH2[j]
        
        myString+=recordListStrH2['reg_id']+':'+recordListStrH2['level1_sup_name']+'    ,    '+recordListStrH2['zone_id']+':'+recordListStrH2['level0_sup_name']+'\n'
              
    
        myString+='AM,AM TM,AM Name,Previous Base,Previous IPI,Previous PER(%),Current Base,Current IPI,Current PER(%),Growth(%)'+'\n'
    
        for i in range(len(recordList2)):
            recordListStr2=recordList2[i]        
            if recordListStrH2['zone_id']==recordListStr2['zone_id'] and recordListStrH2['reg_id']==recordListStr2['reg_id']:       
                tl_id=recordListStr2['tl_id']
                tl_name=recordListStr2['tl_name']
                level2_sup_name=recordListStr2['level2_sup_name']
                med_total1=recordListStr2['med_total1']
                ipi_med=recordListStr2['med_self1']
                perP1=recordListStr2['perP1']
                med_total2=recordListStr2['med_total2']
                ipi_med2=recordListStr2['med_self2']
                perP2=recordListStr2['perP2']
                growth=recordListStr2['growth']
                
                try:
                    level2_sup_name=str(level2_sup_name)
                except:
                    level2_sup_name='11'
                
                if perP1==None:
                    perP1=''
                
                if perP2==None:
                    perP2=''
                
                if growth==None:
                    growth=''
                
                             
                myString+=str(tl_id)+','+str(tl_name)+','+str(level2_sup_name)+','+str(med_total1)+','+str(ipi_med)+','+str(perP1)+','+\
                str(med_total2)+','+str(ipi_med2)+','+str(perP2)+','+str(growth)+'\n'
    
    myString+='\n\n'    
    # mpo
    for j in range(len(recordListH3)):
        recordListStrH3=recordListH3[j]
        
        myString+=recordListStrH3['tl_id']+':'+recordListStrH3['level2_sup_name']+'    ,    '+recordListStrH3['reg_id']+':'+recordListStrH3['level1_sup_name']+'    ,    '+recordListStrH3['zone_id']+':'+recordListStrH3['level0_sup_name']+'\n'
              
    
        myString+='MPO,MPO TM,MPO Name,Previous Base,Previous IPI,Previous PER(%),Current Base,Current IPI,Current PER(%),Growth(%)'+'\n'
    
        for i in range(len(recordList3)):
            recordListStr3=recordList3[i]        
            if recordListStrH3['zone_id']==recordListStr3['zone_id'] and recordListStrH3['reg_id']==recordListStr3['reg_id'] and recordListStrH3['tl_id']==recordListStr3['tl_id']:       
                area_id=recordListStr3['area_id']
                area_name=recordListStr3['area_name']
                level3_sup_name=recordListStr3['level3_sup_name']
                med_total1=recordListStr3['med_total1']
                ipi_med=recordListStr3['med_self1']
                perP1=recordListStr3['perP1']
                med_total2=recordListStr3['med_total2']
                ipi_med2=recordListStr3['med_self2']
                perP2=recordListStr3['perP2']
                growth=recordListStr3['growth']
                
                try:
                    level3_sup_name=str(level3_sup_name)
                except:
                    level3_sup_name='11'
                
                if perP1==None:
                    perP1=''
                
                if perP2==None:
                    perP2=''
                
                if growth==None:
                    growth=''
                
                             
                myString+=str(area_id)+','+str(area_name)+','+str(level3_sup_name)+','+str(med_total1)+','+str(ipi_med)+','+str(perP1)+','+\
                str(med_total2)+','+str(ipi_med2)+','+str(perP2)+','+str(growth)+'\n'
    
    
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=Company_track.csv'   
    return str(myString)

def company_track_rm():
    cid=session.cid
    date_from_1=request.vars.date_from_1
    date_to_1=request.vars.date_to_1   
    
    date_to_m_1=datetime.datetime.strptime(str(date_to_1),'%Y-%m-%d') 
    date_to_m_1=date_to_m_1 + datetime.timedelta(days = 1)
    
    date_from_2=request.vars.date_from_2
    date_to_2=request.vars.date_to_2
    
    date_to_m_2=datetime.datetime.strptime(str(date_to_2),'%Y-%m-%d') 
    date_to_m_2=date_to_m_2 + datetime.timedelta(days = 1)
    
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    
    
    
    condition=''
    if pr_region!='':
        condition+=condition+" and zone_id = '"+str(pr_region)+"'"
    if pr_doctor!='':
        condition+=condition+" and doctor_id = '"+str(pr_doctor)+"'"
    if pr_ff!='':
        condition+=condition+" and submit_by_id = '"+str(pr_ff)+"'"

    
    
    sql1="(SELECT zone_id,zone_name,level0_sup_id,level0_sup_name,sl as rxCount1,0 as rxCount2, med_self as med_self1,med_total as med_total1, 0 as med_self2, 0 as med_total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_1+"' and submit_date<='"+date_to_1+"'"+condition+")"
    sql2="(SELECT zone_id,zone_name,level0_sup_id,level0_sup_name,0 as rxCount1,sl as rxCount2,0 as med_self1, 0 as med_total1,med_self as med_self2,med_total as total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_2+"' and submit_date<='"+date_to_2+"'"+condition+")"
    records="select zone_id,zone_name,level0_sup_id,level0_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id;"
    recordList=db.executesql(records,as_dict=True)
  
    return dict(recordList=recordList,date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)

def company_track_zm():
    cid=session.cid
    date_from_1=request.vars.date_from_1
    date_to_1=request.vars.date_to_1   
    
    date_to_m_1=datetime.datetime.strptime(str(date_to_1),'%Y-%m-%d') 
    date_to_m_1=date_to_m_1 + datetime.timedelta(days = 1)
    
    date_from_2=request.vars.date_from_2
    date_to_2=request.vars.date_to_2
    
    date_to_m_2=datetime.datetime.strptime(str(date_to_2),'%Y-%m-%d') 
    date_to_m_2=date_to_m_2 + datetime.timedelta(days = 1)
    
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    
    
    
    condition=''
    if pr_region!='':
        condition+=condition+" and zone_id = '"+str(pr_region)+"'"
    if pr_zone!='':
        condition+=condition+" and reg_id = '"+str(pr_zone)+"'"
    if pr_doctor!='':
        condition+=condition+" and doctor_id = '"+str(pr_doctor)+"'"
    if pr_ff!='':
        condition+=condition+" and submit_by_id = '"+str(pr_ff)+"'"

    
    
    sql1="(SELECT zone_id,reg_id,reg_name,level1_sup_id,level1_sup_name,sl as rxCount1,0 as rxCount2, med_self as med_self1,med_total as med_total1, 0 as med_self2, 0 as med_total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_1+"' and submit_date<='"+date_to_1+"'"+condition+")"
    sql2="(SELECT zone_id,reg_id,reg_name,level1_sup_id,level1_sup_name,0 as rxCount1,sl as rxCount2,0 as med_self1, 0 as med_total1,med_self as med_self2,med_total as total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_2+"' and submit_date<='"+date_to_2+"'"+condition+")"
    records="select zone_id,reg_id,reg_name,level1_sup_id,level1_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id;"
    recordList=db.executesql(records,as_dict=True)
  
    return dict(recordList=recordList,date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)

def company_track_am():
    cid=session.cid
    date_from_1=request.vars.date_from_1
    date_to_1=request.vars.date_to_1   
    
    date_to_m_1=datetime.datetime.strptime(str(date_to_1),'%Y-%m-%d') 
    date_to_m_1=date_to_m_1 + datetime.timedelta(days = 1)
    
    date_from_2=request.vars.date_from_2
    date_to_2=request.vars.date_to_2
    
    date_to_m_2=datetime.datetime.strptime(str(date_to_2),'%Y-%m-%d') 
    date_to_m_2=date_to_m_2 + datetime.timedelta(days = 1)
    
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    
    
    
    condition=''
    if pr_region!='':
        condition+=condition+" and zone_id = '"+str(pr_region)+"'"
    if pr_zone!='':
        condition+=condition+" and reg_id = '"+str(pr_zone)+"'"
    if pr_area!='':
        condition+=condition+" and tl_id = '"+str(pr_area)+"'"
    if pr_doctor!='':
        condition+=condition+" and doctor_id = '"+str(pr_doctor)+"'"
    if pr_ff!='':
        condition+=condition+" and submit_by_id = '"+str(pr_ff)+"'"

    
    
    sql1="(SELECT zone_id,reg_id,tl_id,tl_name,level2_sup_id,level2_sup_name,sl as rxCount1,0 as rxCount2, med_self as med_self1,med_total as med_total1, 0 as med_self2, 0 as med_total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_1+"' and submit_date<='"+date_to_1+"'"+condition+")"
    sql2="(SELECT zone_id,reg_id,tl_id,tl_name,level2_sup_id,level2_sup_name,0 as rxCount1,sl as rxCount2,0 as med_self1, 0 as med_total1,med_self as med_self2,med_total as total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_2+"' and submit_date<='"+date_to_2+"'"+condition+")"
    records="select zone_id,reg_id,tl_id,tl_name,level2_sup_id,level2_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id;"
    recordList=db.executesql(records,as_dict=True)
  
    return dict(recordList=recordList,date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)


def company_track_mpo():
    cid=session.cid
    date_from_1=request.vars.date_from_1
    date_to_1=request.vars.date_to_1   
    
    date_to_m_1=datetime.datetime.strptime(str(date_to_1),'%Y-%m-%d') 
    date_to_m_1=date_to_m_1 + datetime.timedelta(days = 1)
    
    date_from_2=request.vars.date_from_2
    date_to_2=request.vars.date_to_2
    
    date_to_m_2=datetime.datetime.strptime(str(date_to_2),'%Y-%m-%d') 
    date_to_m_2=date_to_m_2 + datetime.timedelta(days = 1)
    
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    
    
    
    condition=''
    if pr_region!='':
        condition+=condition+" and zone_id = '"+str(pr_region)+"'"
    if pr_zone!='':
        condition+=condition+" and reg_id = '"+str(pr_zone)+"'"
    if pr_area!='':
        condition+=condition+" and tl_id = '"+str(pr_area)+"'"
    if pr_territory!='':
        condition+=condition+" and area_id = '"+str(pr_territory)+"'"
    if pr_doctor!='':
        condition+=condition+" and doctor_id = '"+str(pr_doctor)+"'"
    if pr_ff!='':
        condition+=condition+" and submit_by_id = '"+str(pr_ff)+"'"

    
    
    sql1="(SELECT zone_id,reg_id,tl_id,area_id,area_name,level3_sup_id,level3_sup_name,sl as rxCount1,0 as rxCount2, med_self as med_self1,med_total as med_total1, 0 as med_self2, 0 as med_total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_1+"' and submit_date<='"+date_to_1+"'"+condition+")"
    sql2="(SELECT zone_id,reg_id,tl_id,area_id,area_name,level3_sup_id,level3_sup_name,0 as rxCount1,sl as rxCount2,0 as med_self1, 0 as med_total1,med_self as med_self2,med_total as total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_2+"' and submit_date<='"+date_to_2+"'"+condition+")"
    records="select zone_id,reg_id,tl_id,area_id,area_name,level3_sup_id,level3_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id,area_id;"
    recordList=db.executesql(records,as_dict=True)
  
    return dict(recordList=recordList,date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)


def company_track_mpo_d():
    cid=session.cid
    date_from_1=request.vars.date_from_1
    date_to_1=request.vars.date_to_1   
    
    date_to_m_1=datetime.datetime.strptime(str(date_to_1),'%Y-%m-%d') 
    date_to_m_1=date_to_m_1 + datetime.timedelta(days = 1)
    
    date_from_2=request.vars.date_from_2
    date_to_2=request.vars.date_to_2
    
    date_to_m_2=datetime.datetime.strptime(str(date_to_2),'%Y-%m-%d') 
    date_to_m_2=date_to_m_2 + datetime.timedelta(days = 1)
    
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff

    condition=''
    if pr_region!='':
        condition+=condition+" and zone_id = '"+str(pr_region)+"'"
    if pr_zone!='':
        condition+=condition+" and reg_id = '"+str(pr_zone)+"'"
    if pr_area!='':
        condition+=condition+" and reg_id = '"+str(pr_area)+"'"
    if pr_territory!='':
        condition+=condition+" and area_id = '"+str(pr_territory)+"'"
    if pr_doctor!='':
        condition+=condition+" and doctor_id = '"+str(pr_doctor)+"'"
    if pr_ff!='':
        condition+=condition+" and submit_by_id = '"+str(pr_ff)+"'"

    
    
    sql1="(SELECT zone_id,reg_id,tl_id,area_id,area_name,level3_sup_id,level3_sup_name,sl as rxCount1,0 as rxCount2, med_self as med_self1,med_total as med_total1, 0 as med_self2, 0 as med_total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_1+"' and submit_date<='"+date_to_1+"'"+condition+")"
    sql2="(SELECT zone_id,reg_id,tl_id,area_id,area_name,level3_sup_id,level3_sup_name,0 as rxCount1,sl as rxCount2,0 as med_self1, 0 as med_total1,med_self as med_self2,med_total as total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_2+"' and submit_date<='"+date_to_2+"'"+condition+")"
    records="select zone_id,reg_id,tl_id,area_id,area_name,level3_sup_id,level3_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id,area_id;"
    recordList=db.executesql(records,as_dict=True)
    
    myString='Company Track MPO \n'     
    myString+='Previous:'+','+str(date_from_1)+' To '+str(date_to_1)+'\n'            
    myString+='Current:'+','+str(date_from_2)+' To '+str(date_to_2)+'\n'
    myString+='RM :'+','+str(pr_region)+'\n'   #+' | '+str(pr_region) 
    myString+='ZM :'+','+str(pr_zone)+'\n'
    myString+='AM :'+','+str(pr_area)+'\n'
    myString+='MPO :'+','+str(pr_territory)+'\n\n\n'        
    
    
    myString+='Region,Zone,Area,MPO,MPO TM,MPO Name,Previous Base,Previous Self Med,Previous Per(%),Current Base,Current Self Med,Current Per(%),Growth'+'\n'

    for i in range(len(recordList)):
        recordListStr=recordList[i]
        
        zone_id=recordListStr['zone_id']
        reg_id=recordListStr['reg_id']
        tl_id=recordListStr['tl_id']
        area_id=recordListStr['area_id']
        area_name=recordListStr['area_name']
        level3_sup_name=recordListStr['level3_sup_name']
        rxCount1=recordListStr['rxCount1']
        med_self1=recordListStr['med_self1']
        med_total1=recordListStr['med_total1']
        perP1=recordListStr['perP1']
        rxCount2=recordListStr['rxCount2']
        med_self2=recordListStr['med_self2']
        med_total2=recordListStr['med_total2']
        perP2=recordListStr['perP2']
        growth=recordListStr['growth']
        
#        otherMed1=med_total1-med_self1
#        otherMed2=med_total2-med_self2
        
        if perP1==None:
            perP1=''
        
        if perP2==None:
            perP2=''
        
        if growth==None:
            growth=''
             
        myString+=str(zone_id)+','+str(reg_id)+','+str(tl_id)+','+str(area_id)+','+str(area_name)+','+str(level3_sup_name)+','+\
        str(med_total1)+','+str(med_self1)+','+str(perP1)+','+str(med_total2)+','+\
        str(med_self2)+','+str(perP2)+','+str(growth)+'\n'
        
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=company_track_mpo.csv'   
    return str(myString)


def company_track_am_d():
    cid=session.cid
    date_from_1=request.vars.date_from_1
    date_to_1=request.vars.date_to_1   
    
    date_to_m_1=datetime.datetime.strptime(str(date_to_1),'%Y-%m-%d') 
    date_to_m_1=date_to_m_1 + datetime.timedelta(days = 1)
    
    date_from_2=request.vars.date_from_2
    date_to_2=request.vars.date_to_2
    
    date_to_m_2=datetime.datetime.strptime(str(date_to_2),'%Y-%m-%d') 
    date_to_m_2=date_to_m_2 + datetime.timedelta(days = 1)
    
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
#    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff

    condition=''
    if pr_region!='':
        condition+=condition+" and zone_id = '"+str(pr_region)+"'"
    if pr_zone!='':
        condition+=condition+" and reg_id = '"+str(pr_zone)+"'"
    if pr_area!='':
        condition+=condition+" and reg_id = '"+str(pr_area)+"'"
    if pr_doctor!='':
        condition+=condition+" and doctor_id = '"+str(pr_doctor)+"'"
    if pr_ff!='':
        condition+=condition+" and submit_by_id = '"+str(pr_ff)+"'"

    
    
    sql1="(SELECT zone_id,reg_id,tl_id,level2_sup_name,sl as rxCount, med_self as med_self1,med_total as med_total1, 0 as med_self2, 0 as med_total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_1+"' and submit_date<='"+date_to_1+"'"+condition+")"
    sql2="(SELECT zone_id,reg_id,tl_id,level2_sup_name,sl as rxCount,0 as med_self1, 0 as med_total1,med_self as med_self2,med_total as total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_2+"' and submit_date<='"+date_to_2+"'"+condition+")"
    records="select zone_id,reg_id,tl_id,level2_sup_name,count(distinct(rxCount)) as rxCount, sum(med_self1) as med_self1, sum(med_total1) as med_total1,(sum(med_self1)/sum(med_total1))*100 as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,(sum(med_self2)/sum(med_total2))*100 as perP2, (((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100 as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id;"
    recordList=db.executesql(records,as_dict=True)
    
    myString='Company Track AM \n'     
    myString+='Previous:'+','+str(date_from_1)+' To '+str(date_to_1)+'\n'            
    myString+='Current:'+','+str(date_from_2)+' To '+str(date_to_2)+'\n'
    myString+='RM :'+','+str(pr_region)+'\n'   #+' | '+str(pr_region) 
    myString+='ZM :'+','+str(pr_zone)+'\n'
    myString+='AM :'+','+str(pr_area)+'\n\n\n'        
    
    
    myString+='Region,Zone,Area,AM Name,Previous Base,Previous Self Med,Previous Per(%),Current Base,Current Self Med,Current Per(%),Growth'+'\n'

    for i in range(len(recordList)):
        recordListStr=recordList[i]
        
        zone_id=recordListStr['zone_id']
        reg_id=recordListStr['reg_id']
        tl_id=recordListStr['tl_id']
        level2_sup_name=recordListStr['level2_sup_name']
        
        med_self1=recordListStr['med_self1']
        med_total1=recordListStr['med_total1']
        perP1=recordListStr['perP1']        
        med_self2=recordListStr['med_self2']
        med_total2=recordListStr['med_total2']
        perP2=recordListStr['perP2']
        growth=recordListStr['growth']
        
        if perP1==None:
            perP1=''
        
        if perP2==None:
            perP2=''
        
        if growth==None:
            growth=''
             
        myString+=str(zone_id)+','+str(reg_id)+','+str(tl_id)+','+str(level2_sup_name)+','+str(med_total1)+','+str(med_self1)+','+str(perP1)+','+str(med_total2)+','+str(med_self2)+','+str(perP2)+','+str(growth)+'\n'
        
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=company_track_am.csv'   
    return str(myString)

def company_track_zm_d():
    cid=session.cid
    date_from_1=request.vars.date_from_1
    date_to_1=request.vars.date_to_1   
    
    date_to_m_1=datetime.datetime.strptime(str(date_to_1),'%Y-%m-%d') 
    date_to_m_1=date_to_m_1 + datetime.timedelta(days = 1)
    
    date_from_2=request.vars.date_from_2
    date_to_2=request.vars.date_to_2
    
    date_to_m_2=datetime.datetime.strptime(str(date_to_2),'%Y-%m-%d') 
    date_to_m_2=date_to_m_2 + datetime.timedelta(days = 1)
    
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    
    condition=''
    if pr_region!='':
        condition+=condition+" and zone_id = '"+str(pr_region)+"'"
    if pr_zone!='':
        condition+=condition+" and reg_id = '"+str(pr_zone)+"'"
    if pr_doctor!='':
        condition+=condition+" and doctor_id = '"+str(pr_doctor)+"'"
    if pr_ff!='':
        condition+=condition+" and submit_by_id = '"+str(pr_ff)+"'"

    
    
    sql1="(SELECT zone_id,reg_id,level1_sup_name,sl as rxCount, med_self as med_self1,med_total as med_total1, 0 as med_self2, 0 as med_total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_1+"' and submit_date<='"+date_to_1+"'"+condition+"  )"
    sql2="(SELECT zone_id,reg_id,level1_sup_name,sl as rxCount,0 as med_self1, 0 as med_total1,med_self as med_self2,med_total as total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_2+"' and submit_date<='"+date_to_2+"'"+condition+" )"
    records="select zone_id,reg_id,level1_sup_name,count(distinct(rxCount)) as rxCount, sum(med_self1) as med_self1, sum(med_total1) as med_total1,(sum(med_self1)/sum(med_total1))*100 as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,(sum(med_self2)/sum(med_total2))*100 as perP2,(((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100 as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id;"
    recordList=db.executesql(records,as_dict=True)
    
    myString='Company Track ZM \n'     
    myString+='Previous:'+','+str(date_from_1)+' To '+str(date_to_1)+'\n'            
    myString+='Current:'+','+str(date_from_2)+' To '+str(date_to_2)+'\n'
    myString+='RM :'+','+str(pr_region)+'\n'   #+' | '+str(pr_region) 
    myString+='ZM :'+','+str(pr_zone)+'\n\n\n'        
    
    
    myString+='Region,Zone,ZM Name,Previous Base,Previous Self Med,Previous Per(%),Current Base,Current Self Med,Current Per(%),Growth'+'\n'

    for i in range(len(recordList)):
        recordListStr=recordList[i]
        
        zone_id=recordListStr['zone_id']
        reg_id=recordListStr['reg_id']
        level1_sup_name=recordListStr['level1_sup_name']
        
        med_self1=recordListStr['med_self1']
        med_total1=recordListStr['med_total1']
        perP1=recordListStr['perP1']        
        med_self2=recordListStr['med_self2']
        med_total2=recordListStr['med_total2']
        perP2=recordListStr['perP2']
        growth=recordListStr['growth']
        
        if perP1==None:
            perP1=''
        
        if perP2==None:
            perP2=''
        
        if growth==None:
            growth=''
             
        myString+=str(zone_id)+','+str(reg_id)+','+str(level1_sup_name)+','+str(med_total1)+','+str(med_self1)+','+str(perP1)+','+str(med_total2)+','+str(med_self2)+','+str(perP2)+','+str(growth)+'\n'
        
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=company_track_zm.csv'   
    return str(myString)

def company_track_rm_d():
    cid=session.cid
    date_from_1=request.vars.date_from_1
    date_to_1=request.vars.date_to_1   
    
    date_to_m_1=datetime.datetime.strptime(str(date_to_1),'%Y-%m-%d') 
    date_to_m_1=date_to_m_1 + datetime.timedelta(days = 1)
    
    date_from_2=request.vars.date_from_2
    date_to_2=request.vars.date_to_2
    
    date_to_m_2=datetime.datetime.strptime(str(date_to_2),'%Y-%m-%d') 
    date_to_m_2=date_to_m_2 + datetime.timedelta(days = 1)
    
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    
    condition=''
    if pr_region!='':
        condition+=condition+" and zone_id = '"+str(pr_region)+"'"
    if pr_doctor!='':
        condition+=condition+" and doctor_id = '"+str(pr_doctor)+"'"
    if pr_ff!='':
        condition+=condition+" and submit_by_id = '"+str(pr_ff)+"'"

    
    
    sql1="(SELECT zone_id,level0_sup_name,sl as rxCount, med_self as med_self1,med_total as med_total1, 0 as med_self2, 0 as med_total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_1+"' and submit_date<='"+date_to_1+"'"+condition+"  )"
    sql2="(SELECT zone_id,level0_sup_name,sl as rxCount,0 as med_self1, 0 as med_total1,med_self as med_self2,med_total as total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_2+"' and submit_date<='"+date_to_2+"'"+condition+" )"
    records="select zone_id,level0_sup_name,count(distinct(rxCount)) as rxCount, sum(med_self1) as med_self1, sum(med_total1) as med_total1,(sum(med_self1)/sum(med_total1))*100 as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,(sum(med_self2)/sum(med_total2))*100 as perP2,(((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100 as growth from ("+sql1+" union all "+sql2+") p group by zone_id;"
    recordList=db.executesql(records,as_dict=True)
    
    myString='Company Track RM \n'     
    myString+='Previous:'+','+str(date_from_1)+' To '+str(date_to_1)+'\n'            
    myString+='Current:'+','+str(date_from_2)+' To '+str(date_to_2)+'\n'
    myString+='RM :'+','+str(pr_region)+'\n\n\n'   #+' | '+str(pr_region)         
    
    
    myString+='Region,RM Name,Previous Base,Previous Self Med,Previous Per(%),Current Base,Current Self Med,Current Per(%),Growth'+'\n'

    for i in range(len(recordList)):
        recordListStr=recordList[i]
        
        zone_id=recordListStr['zone_id']
        level0_sup_name=recordListStr['level0_sup_name']
        
        med_self1=recordListStr['med_self1']
        med_total1=recordListStr['med_total1']
        perP1=recordListStr['perP1']        
        med_self2=recordListStr['med_self2']
        med_total2=recordListStr['med_total2']
        perP2=recordListStr['perP2']
        growth=recordListStr['growth']
        
        if perP1==None:
            perP1=''
        
        if perP2==None:
            perP2=''
        
        if growth==None:
            growth=''
             
        myString+=str(zone_id)+','+str(level0_sup_name)+','+str(med_total1)+','+str(med_self1)+','+str(perP1)+','+str(med_total2)+','+str(med_self2)+','+str(perP2)+','+str(growth)+'\n'
        
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=company_track_rm.csv'   
    return str(myString)





def institute_track_am_d():
    cid=session.cid
    date_from_1=request.vars.date_from_1
    date_to_1=request.vars.date_to_1   
    
    date_to_m_1=datetime.datetime.strptime(str(date_to_1),'%Y-%m-%d') 
    date_to_m_1=date_to_m_1 + datetime.timedelta(days = 1)
    
    date_from_2=request.vars.date_from_2
    date_to_2=request.vars.date_to_2
    
    date_to_m_2=datetime.datetime.strptime(str(date_to_2),'%Y-%m-%d') 
    date_to_m_2=date_to_m_2 + datetime.timedelta(days = 1)
    
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
#    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff

    condition=''
    if pr_region!='':
        condition+=condition+" and zone_id = '"+str(pr_region)+"'"
    if pr_zone!='':
        condition+=condition+" and reg_id = '"+str(pr_zone)+"'"
    if pr_area!='':
        condition+=condition+" and reg_id = '"+str(pr_area)+"'"
    if pr_doctor!='':
        condition+=condition+" and doctor_id = '"+str(pr_doctor)+"'"
    if pr_ff!='':
        condition+=condition+" and submit_by_id = '"+str(pr_ff)+"'"

    
    
    sql1="(SELECT zone_id,reg_id,tl_id,level2_sup_name,sl as rxCount, med_self as med_self1,med_total as med_total1, 0 as med_self2, 0 as med_total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_1+"' and submit_date<='"+date_to_1+"'"+condition+")"
    sql2="(SELECT zone_id,reg_id,tl_id,level2_sup_name,sl as rxCount,0 as med_self1, 0 as med_total1,med_self as med_self2,med_total as total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_2+"' and submit_date<='"+date_to_2+"'"+condition+")"
    records="select zone_id,reg_id,tl_id,level2_sup_name,count(distinct(rxCount)) as rxCount, sum(med_self1) as med_self1, sum(med_total1) as med_total1,(sum(med_self1)/sum(med_total1))*100 as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,(sum(med_self2)/sum(med_total2))*100 as perP2, (((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100 as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id;"
    recordList=db.executesql(records,as_dict=True)
    
    myString='Company Track ZM \n'     
    myString+='Previous:'+','+str(date_from_1)+' To '+str(date_to_1)+'\n'            
    myString+='Current:'+','+str(date_from_2)+' To '+str(date_to_2)+'\n'
    myString+='RM :'+','+str(pr_region)+'\n'   #+' | '+str(pr_region) 
    myString+='ZM :'+','+str(pr_zone)+'\n'
    myString+='AM :'+','+str(pr_area)+'\n\n\n'        
    
    
    myString+='Region,Zone,Area,AM Name,Rx-Qty,Date Range 1st('+str(date_from_1)+' To '+str(date_to_1)+'),Date Range 2nd ('+str(date_from_2)+' To '+str(date_to_2)+'),Growth'+'\n'

    for i in range(len(recordList)):
        recordListStr=recordList[i]
        
        zone_id=recordListStr['zone_id']
        reg_id=recordListStr['reg_id']
        tl_id=recordListStr['tl_id']
        level2_sup_name=recordListStr['level2_sup_name']
        rxCount=recordListStr['rxCount']
        perP1=recordListStr['perP1']
        perP2=recordListStr['perP2']
        growth=recordListStr['growth']
        
        if perP1==None:
            perP1=''
        
        if perP2==None:
            perP2=''
        
        if growth==None:
            growth=''
             
        myString+=str(zone_id)+','+str(reg_id)+','+str(tl_id)+','+str(level2_sup_name)+','+str(rxCount)+','+str(perP1)+','+str(perP2)+','+str(growth)+'\n'
        
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=institute_track_am.csv'   
    return str(myString)

def institute_track_zm_d():
    cid=session.cid
    date_from_1=request.vars.date_from_1
    date_to_1=request.vars.date_to_1   
    
    date_to_m_1=datetime.datetime.strptime(str(date_to_1),'%Y-%m-%d') 
    date_to_m_1=date_to_m_1 + datetime.timedelta(days = 1)
    
    date_from_2=request.vars.date_from_2
    date_to_2=request.vars.date_to_2
    
    date_to_m_2=datetime.datetime.strptime(str(date_to_2),'%Y-%m-%d') 
    date_to_m_2=date_to_m_2 + datetime.timedelta(days = 1)
    
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    
    condition=''
    if pr_region!='':
        condition+=condition+" and zone_id = '"+str(pr_region)+"'"
    if pr_zone!='':
        condition+=condition+" and reg_id = '"+str(pr_zone)+"'"
    if pr_doctor!='':
        condition+=condition+" and doctor_id = '"+str(pr_doctor)+"'"
    if pr_ff!='':
        condition+=condition+" and submit_by_id = '"+str(pr_ff)+"'"

    
    
    sql1="(SELECT zone_id,reg_id,level1_sup_name,sl as rxCount, med_self as med_self1,med_total as med_total1, 0 as med_self2, 0 as med_total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_1+"' and submit_date<='"+date_to_1+"'"+condition+"  )"
    sql2="(SELECT zone_id,reg_id,level1_sup_name,sl as rxCount,0 as med_self1, 0 as med_total1,med_self as med_self2,med_total as total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_2+"' and submit_date<='"+date_to_2+"'"+condition+" )"
    records="select zone_id,reg_id,level1_sup_name,count(distinct(rxCount)) as rxCount, sum(med_self1) as med_self1, sum(med_total1) as med_total1,(sum(med_self1)/sum(med_total1))*100 as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,(sum(med_self2)/sum(med_total2))*100 as perP2,(((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100 as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id;"
    recordList=db.executesql(records,as_dict=True)
    
    myString='Company Track ZM \n'     
    myString+='Previous:'+','+str(date_from_1)+' To '+str(date_to_1)+'\n'            
    myString+='Current:'+','+str(date_from_2)+' To '+str(date_to_2)+'\n'
    myString+='RM :'+','+str(pr_region)+'\n'   #+' | '+str(pr_region) 
    myString+='ZM :'+','+str(pr_zone)+'\n\n\n'        
    
    
    myString+='Region,Zone,ZM Name,Rx-Qty,Date Range 1st('+str(date_from_1)+' To '+str(date_to_1)+'),Date Range 2nd ('+str(date_from_2)+' To '+str(date_to_2)+'),Growth'+'\n'

    for i in range(len(recordList)):
        recordListStr=recordList[i]
        
        zone_id=recordListStr['zone_id']
        reg_id=recordListStr['reg_id']
        level1_sup_name=recordListStr['level1_sup_name']
        rxCount=recordListStr['rxCount']
        perP1=recordListStr['perP1']
        perP2=recordListStr['perP2']
        growth=recordListStr['growth']
        
        if perP1==None:
            perP1=''
        
        if perP2==None:
            perP2=''
        
        if growth==None:
            growth=''
             
        myString+=str(zone_id)+','+str(reg_id)+','+str(level1_sup_name)+','+str(rxCount)+','+str(perP1)+','+str(perP2)+','+str(growth)+'\n'
        
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=institute_track_zm.csv'   
    return str(myString)

def institute_track_rm_d():
    cid=session.cid
    date_from_1=request.vars.date_from_1
    date_to_1=request.vars.date_to_1   
    
    date_to_m_1=datetime.datetime.strptime(str(date_to_1),'%Y-%m-%d') 
    date_to_m_1=date_to_m_1 + datetime.timedelta(days = 1)
    
    date_from_2=request.vars.date_from_2
    date_to_2=request.vars.date_to_2
    
    date_to_m_2=datetime.datetime.strptime(str(date_to_2),'%Y-%m-%d') 
    date_to_m_2=date_to_m_2 + datetime.timedelta(days = 1)
    
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    
    condition=''
    if pr_region!='':
        condition+=condition+" and zone_id = '"+str(pr_region)+"'"
    if pr_doctor!='':
        condition+=condition+" and doctor_id = '"+str(pr_doctor)+"'"
    if pr_ff!='':
        condition+=condition+" and submit_by_id = '"+str(pr_ff)+"'"

    
    
    sql1="(SELECT zone_id,level0_sup_name,sl as rxCount, med_self as med_self1,med_total as med_total1, 0 as med_self2, 0 as med_total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_1+"' and submit_date<='"+date_to_1+"'"+condition+"  )"
    sql2="(SELECT zone_id,level0_sup_name,sl as rxCount,0 as med_self1, 0 as med_total1,med_self as med_self2,med_total as total2 FROM `sm_prescription_head` WHERE cid='"+cid+"' and submit_date>='"+date_from_2+"' and submit_date<='"+date_to_2+"'"+condition+" )"
    records="select zone_id,level0_sup_name,count(distinct(rxCount)) as rxCount, sum(med_self1) as med_self1, sum(med_total1) as med_total1,(sum(med_self1)/sum(med_total1))*100 as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,(sum(med_self2)/sum(med_total2))*100 as perP2,(((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100 as growth from ("+sql1+" union all "+sql2+") p group by zone_id;"
    recordList=db.executesql(records,as_dict=True)
    
    myString='Company Track RM \n'     
    myString+='Previous:'+','+str(date_from_1)+' To '+str(date_to_1)+'\n'            
    myString+='Current:'+','+str(date_from_2)+' To '+str(date_to_2)+'\n'
    myString+='RM :'+','+str(pr_region)+'\n\n\n'   #+' | '+str(pr_region)         
    
    
    myString+='Region,RM Name,Rx-Qty,Date Range 1st('+str(date_from_1)+' To '+str(date_to_1)+'),Date Range 2nd ('+str(date_from_2)+' To '+str(date_to_2)+'),Growth'+'\n'

    for i in range(len(recordList)):
        recordListStr=recordList[i]
        
        zone_id=recordListStr['zone_id']
        level0_sup_name=recordListStr['level0_sup_name']
        rxCount=recordListStr['rxCount']
        perP1=recordListStr['perP1']
        perP2=recordListStr['perP2']
        growth=recordListStr['growth']
        
        if perP1==None:
            perP1=''
        
        if perP2==None:
            perP2=''
        
        if growth==None:
            growth=''
             
        myString+=str(zone_id)+','+str(level0_sup_name)+','+str(rxCount)+','+str(perP1)+','+str(perP2)+','+str(growth)+'\n'
        
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=institute_track_rm.csv'   
    return str(myString)
    


#def chart_generic():
#    response.title = 'Chart'
#
#    c_id = session.cid
#
#    date_from = str(request.vars.date_from).strip()
#    date_to = str(request.vars.date_to).strip()
#    
#    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
#    date_to_m=date_to_m + datetime.timedelta(days = 1)
#    
#    med_generic=str(request.vars.generic).strip()
#
#    qset=db()
#    qset=qset(db.sm_prescription_details.cid == c_id)
#    qset = qset(db.sm_prescription_details.submit_date >= date_from)
#    qset = qset(db.sm_prescription_details.submit_date < date_to_m)
#    qset=qset(db.sm_prescription_details.generic == med_generic)
#    
#    records=qset.select(db.sm_prescription_details.company,db.sm_prescription_details.id.count(),groupby=db.sm_prescription_details.company,orderby=~db.sm_prescription_details.id.count())
#    
#    generic_data_list=[]
#    
#    for row in records:
#        medCompany=row[db.sm_prescription_details.company]
#        medCount=row[db.sm_prescription_details.id.count()]
#        
#        dictData = {'Company':medCompany, 'Count':int(medCount)}
#        generic_data_list.append(dictData)
#
#
#    return dict(generic_data_list=generic_data_list, date_from=date_from, date_to=date_to, generic=med_generic)

def orphan_med_list_d():
    cid=session.cid
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)
    
        
    qset=db()
    qset=qset(db.sm_prescription_details.cid == cid)
    qset = qset(db.sm_prescription_details.submit_date >= date_from)
    qset = qset(db.sm_prescription_details.submit_date < date_to_m)
    qset=qset(db.sm_prescription_details.medicine_id == 0)
    
        
    records=qset.select(db.sm_prescription_details.medicine_name,db.sm_prescription_details.submit_by_id,db.sm_prescription_details.submit_by_name, orderby=db.sm_prescription_details.medicine_name)
    
   
    myString='Orphan Medicine Details \n'     
    myString+='Date Range:'+','+str(date_from)+' To '+str(date_to)+'\n\n\n'            
    
    slNo=0
    myString+='SL,Medicine Name,Submitted By ID,Submitted By Name'+'\n'

    for row in records:
        slNo+=1
        medicine_name=row.medicine_name       
        submit_by_id=row.submit_by_id
        submit_by_name=row.submit_by_name
             
        myString+=str(slNo)+','+str(medicine_name)+','+str(submit_by_id)+','+str(submit_by_name)+'\n'
        
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=orphan_medicine_list.csv'   
    return str(myString)

def orphan_med_list():
    cid=session.cid
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)
    
        
    qset=db()
    qset=qset(db.sm_prescription_details.cid == cid)
    qset = qset(db.sm_prescription_details.submit_date >= date_from)
    qset = qset(db.sm_prescription_details.submit_date < date_to_m)
    qset=qset(db.sm_prescription_details.medicine_id == 0)
    
        
    records=qset.select(db.sm_prescription_details.medicine_name,db.sm_prescription_details.submit_by_id,db.sm_prescription_details.submit_by_name, orderby=db.sm_prescription_details.medicine_name)
    
    
    return dict(records=records,date_from=date_from,date_to=date_to) 

def pr_summary_d():
    cid=session.cid
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)
    
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
        
    qset=db()
    qset=qset(db.sm_prescription_head.cid == cid)
    qset = qset(db.sm_prescription_head.submit_date >= date_from)
    qset = qset(db.sm_prescription_head.submit_date < date_to_m)  
    
    qset=qset(db.sm_prescription_details.cid == cid)
    qset=qset(db.sm_prescription_head.sl == db.sm_prescription_details.sl) 
    
    if pr_region!='':
        qset=qset(db.sm_prescription_head.zone_id == pr_region)
    if pr_zone!='':
        qset=qset(db.sm_prescription_head.reg_id == pr_zone)
    if pr_area!='':
        qset=qset(db.sm_prescription_head.tl_id == pr_area)
    if pr_territory!='':
        qset=qset(db.sm_prescription_head.area_id == pr_territory)
    if pr_ff!='':
        qset=qset(db.sm_prescription_head.submit_by_id == pr_ff)
    if med_generic!='':
        qset=qset(db.sm_prescription_details.generic == med_generic)
    if pr_doctor!='':
        qset=qset(db.sm_prescription_head.doctor_id == pr_doctor)   
              
           
    records=qset.select(db.sm_prescription_head.ALL,db.sm_prescription_details.medicine_id,db.sm_prescription_details.medicine_name,db.sm_prescription_details.brand,db.sm_prescription_details.generic,db.sm_prescription_details.strength,db.sm_prescription_details.formation,db.sm_prescription_details.company,db.sm_prescription_details.id.count(),groupby=db.sm_prescription_head.doctor_id|db.sm_prescription_head.doctor_name|db.sm_prescription_head.area_id|db.sm_prescription_details.company|db.sm_prescription_details.brand,orderby=db.sm_prescription_head.doctor_id|db.sm_prescription_head.doctor_name|db.sm_prescription_head.area_id|db.sm_prescription_details.company|db.sm_prescription_details.brand)
    
        
    if pr_region=='':
        pr_region='National'
    if pr_zone=='':
        pr_zone='ALL'
    if pr_area=='':
        pr_area='ALL'
    if pr_territory=='':
        pr_territory='ALL'
    if pr_ff=='':
        pr_ff='ALL'
    if med_generic=='':
        med_generic='ALL'
    if pr_doctor=='':
        pr_doctor='ALL'       
   
       
    myString='Prescription Summary \n'     
    myString+='Date Range:'+','+str(date_from)+' To '+str(date_to)+'\n'
    myString+='Zone:'+','+str(pr_region)+'\n'
    myString+='Region:'+','+str(pr_zone)+'\n'
    myString+='Area:'+','+str(pr_area)+'\n'
    myString+='Territory:'+','+str(pr_territory)+'\n'
    myString+='Field Force:'+','+str(pr_ff)+'\n'
    myString+='Geniric:'+','+str(med_generic)+'\n'
    myString+='Doctor:'+','+str(pr_doctor)+'\n'
    
    slNo=0
    myString+='Sl,Date,PHY_ID,PHY_NM,PHY_DEGREE,PHY_SPECIALTY,COMPANY NAME,UNIT_PRC,GENERIC,BRAND,Rx_QT,\
    MPO,AM,RM,REGION,MPO_TM,AM_TM,MPO_NAME,AM_NAME,CHAMBER_ADDRESS,MPO_NAME_S,AM_NAME_S,TL_NAME_S'+'\n'        #,Value,DSTMR,SM,,INSTCD,DIAGNAME,CH_DIST,CH_THA
    
    myString1=''
    for row in records:         
        slNo+=1                       
        submit_date=row[db.sm_prescription_head.submit_date]
        doctor_id=str(row[db.sm_prescription_head.doctor_id]).replace(',',' ')
        doctor_name=str(row[db.sm_prescription_head.doctor_name]).replace(',',' ')
        doctor_degree=str(row[db.sm_prescription_head.doctor_degree]).replace(',',' ')
        doctor_speciality=str(row[db.sm_prescription_head.doctor_speciality]).replace(',',' ')
        company=str(row[db.sm_prescription_details.company]).replace(',',' ')
        unit_prc='0'
        generic=str(row[db.sm_prescription_details.generic]).replace(',',' ')
        brand=str(row[db.sm_prescription_details.brand]).replace(',',' ')
        rxQt=str(row[db.sm_prescription_details.id.count()]).replace(',',' ')
        #rxValue='0'
        #dstmr=''
        area_id=str(row[db.sm_prescription_head.area_id]).replace(',',' ') 
        am=str(row[db.sm_prescription_head.tl_id]).replace(',',' ')
        rm=str(row[db.sm_prescription_head.reg_id]).replace(',',' ')
        reg_id=str(row[db.sm_prescription_head.zone_id]).replace(',',' ')
        #sm=''
        mpo_tm=str(row[db.sm_prescription_head.area_name]).replace(',',' ')
        am_tm=str(row[db.sm_prescription_head.tl_name]).replace(',',' ')
        mpo_name=str(row[db.sm_prescription_head.level3_sup_name]).replace(',',' ')
        am_name=str(row[db.sm_prescription_head.level2_sup_name]).replace(',',' ')
        level3_sup_name_s=str(row[db.sm_prescription_head.level3_sup_name_s]).replace(',',' ')
        level2_sup_name_s=str(row[db.sm_prescription_head.level2_sup_name_s]).replace(',',' ')
        level1_sup_name_s=str(row[db.sm_prescription_head.level1_sup_name_s]).replace(',',' ')
        chamber_address=str(row[db.sm_prescription_head.doctor_chamber_address]).replace(',',' ')
        ch_dist=''#str(row[db.sm_prescription_head.district]).replace(',',' ')
        ch_thana=''#str(row[db.sm_prescription_head.thana]).replace(',',' ')
        #insted=''
        
#        medicine_id=row[db.sm_prescription_details.medicine_id]
#        if medicine_id=='0':                         
#            myString+=str(slNo)+','+str(submit_date)+','+str(doctor_id)+','+str(doctor_name)+','+str(doctor_degree)+','+\
#            str(doctor_speciality)+','+str(company)+','+str(unit_prc)+','+str(generic)+','+str(brand)+','+str(rxQt)+','+\
#            str(rxValue)+','+str(submit_by_id)+','+str(am)+','+str(rm)+','+str(reg_id)+','+str(mpo_tm)+','+\
#            str(am_tm)+','+str(submit_by_name)+','+str(am_name)+','+str(chamber_address)+','+str(ch_dist)+','+str(ch_thana)+'\n'
#        else:

        myString1+=str(slNo)+','+str(submit_date)+','+str(doctor_id)+','+str(doctor_name)+','+str(doctor_degree)+','+\
        str(doctor_speciality)+','+str(company)+','+str(unit_prc)+','+str(generic)+','+str(brand)+','+str(rxQt)+','+\
        str(area_id)+','+str(am)+','+str(rm)+','+str(reg_id)+','+str(mpo_tm)+','+\
        str(am_tm)+','+str(mpo_name)+','+str(am_name)+','+str(chamber_address)+','+str(level3_sup_name_s)+','+str(level2_sup_name_s)+','+str(level1_sup_name_s)+'\n'
            
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=prescription_summary.csv'   
    return str(myString+myString1)

def pr_summary():
    cid=session.cid
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)
    
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
        
    qset=db()
    qset=qset(db.sm_prescription_head.cid == cid)
    qset = qset(db.sm_prescription_head.submit_date >= date_from)
    qset = qset(db.sm_prescription_head.submit_date < date_to_m)  
    
    qset=qset(db.sm_prescription_details.cid == cid)
    qset=qset(db.sm_prescription_head.sl == db.sm_prescription_details.sl) 
    
    if pr_region!='':
        qset=qset(db.sm_prescription_head.zone_id == pr_region)
    if pr_zone!='':
        qset=qset(db.sm_prescription_head.reg_id == pr_zone)
    if pr_area!='':
        qset=qset(db.sm_prescription_head.tl_id == pr_area)
    if pr_territory!='':
        qset=qset(db.sm_prescription_head.area_id == pr_territory)
    if pr_ff!='':
        qset=qset(db.sm_prescription_head.submit_by_id == pr_ff)
    if med_generic!='':
        qset=qset(db.sm_prescription_details.generic == med_generic)
    if pr_doctor!='':
        qset=qset(db.sm_prescription_head.doctor_id == pr_doctor)   
           
    records=qset.select(db.sm_prescription_head.ALL,db.sm_prescription_details.medicine_id,db.sm_prescription_details.medicine_name,db.sm_prescription_details.brand,db.sm_prescription_details.generic,db.sm_prescription_details.strength,db.sm_prescription_details.formation,db.sm_prescription_details.company,db.sm_prescription_details.id.count(),groupby=db.sm_prescription_head.doctor_id|db.sm_prescription_head.doctor_name|db.sm_prescription_head.area_id|db.sm_prescription_details.company|db.sm_prescription_details.brand,orderby=db.sm_prescription_head.doctor_id|db.sm_prescription_head.doctor_name|db.sm_prescription_head.area_id|db.sm_prescription_details.company|db.sm_prescription_details.brand)
    
        
    if pr_region=='':
        pr_region='National'
    if pr_zone=='':
        pr_zone='ALL'
    if pr_area=='':
        pr_area='ALL'
    if pr_territory=='':
        pr_territory='ALL'
    if pr_ff=='':
        pr_ff='ALL'
    if med_generic=='':
        med_generic='ALL'
    if pr_doctor=='':
        pr_doctor='ALL'       
   
    return dict(records=records,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)


def pr_details_d():
    cid=session.cid
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)
    
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
        
    qset=db()
    qset=qset(db.sm_prescription_head.cid == cid)
    qset = qset(db.sm_prescription_head.submit_date >= date_from)
    qset = qset(db.sm_prescription_head.submit_date < date_to_m)  
    
    qset=qset(db.sm_prescription_details.cid == cid)
    qset=qset(db.sm_prescription_head.sl == db.sm_prescription_details.sl) 
    
    if pr_region!='':
        qset=qset(db.sm_prescription_head.zone_id == pr_region)
    if pr_zone!='':
        qset=qset(db.sm_prescription_head.reg_id == pr_zone)
    if pr_area!='':
        qset=qset(db.sm_prescription_head.tl_id == pr_area)
    if pr_territory!='':
        qset=qset(db.sm_prescription_head.area_id == pr_territory)
    if pr_ff!='':
        qset=qset(db.sm_prescription_head.submit_by_id == pr_ff)
    if med_generic!='':
        qset=qset(db.sm_prescription_details.generic == med_generic)   
    if pr_doctor!='':
        qset=qset(db.sm_prescription_head.doctor_id == pr_doctor)
       
           
    records=qset.select(db.sm_prescription_head.sl,db.sm_prescription_head.submit_date,db.sm_prescription_head.reg_id,db.sm_prescription_head.tl_id,db.sm_prescription_head.submit_by_id,db.sm_prescription_head.submit_by_name,db.sm_prescription_head.area_id,db.sm_prescription_head.area_name,db.sm_prescription_head.doctor_id,db.sm_prescription_head.doctor_name,db.sm_prescription_details.medicine_id,db.sm_prescription_details.medicine_name,db.sm_prescription_details.brand,db.sm_prescription_details.generic,db.sm_prescription_details.strength,db.sm_prescription_details.formation,db.sm_prescription_details.company, orderby=db.sm_prescription_head.area_id|db.sm_prescription_head.submit_by_id|db.sm_prescription_head.doctor_id|~db.sm_prescription_head.sl)
    
    if pr_region=='':
        pr_region='National'
    if pr_zone=='':
        pr_zone='ALL'
    if pr_area=='':
        pr_area='ALL'
    if pr_territory=='':
        pr_territory='ALL'
    if pr_ff=='':
        pr_ff='ALL'
    if med_generic=='':
        med_generic='ALL'
    if pr_doctor=='':
        pr_doctor='ALL'
       
    myString='Prescription Details \n'     
    myString+='Date Range:'+','+str(date_from)+' To '+str(date_to)+'\n'
    myString+='Zone:'+','+str(pr_region)+'\n'
    myString+='Region:'+','+str(pr_zone)+'\n'
    myString+='Area:'+','+str(pr_area)+'\n'
    myString+='Territory:'+','+str(pr_territory)+'\n'
    myString+='Field Force:'+','+str(pr_ff)+'\n'
    myString+='Geniric:'+','+str(med_generic)+'\n'
    myString+='Doctor:'+','+str(pr_doctor)+'\n'            
    
    slNo=0
    myString+='SL,Date,Region,Territory id,Territory Name,Area Code,Submitted By id,Submitted By Name,Doctor Id,Doctor Name,pr.SL,Med. ID,Med. Name,Brand,Generic,Formation,Company'+'\n'

    for row in records:
        slNo+=1        
        submit_date=row[db.sm_prescription_head.submit_date]
        reg_id=row[db.sm_prescription_head.reg_id]
        area_id=row[db.sm_prescription_head.area_id]
        area_name=row[db.sm_prescription_head.area_name]
        tl_id=row[db.sm_prescription_head.tl_id]
        submit_by_id=row[db.sm_prescription_head.submit_by_id]
        submit_by_name=row[db.sm_prescription_head.submit_by_name]
        doctor_id=row[db.sm_prescription_head.doctor_id]
        doctor_name=row[db.sm_prescription_head.doctor_name]
        sl=row[db.sm_prescription_head.sl]
        medicine_id=row[db.sm_prescription_details.medicine_id]
        medicine_name=row[db.sm_prescription_details.medicine_name]
        brand=row[db.sm_prescription_details.brand]
        generic=row[db.sm_prescription_details.generic]
        formation=row[db.sm_prescription_details.formation]
        company=row[db.sm_prescription_details.company]
                
              
        myString+=str(slNo)+','+str(submit_date)+','+str(reg_id)+','+str(area_id)+','+str(area_name)+','+str(tl_id)+','+str(submit_by_id)+','+str(submit_by_name)+','+str(doctor_id)+','+str(doctor_name)+','+str(sl)+','+str(medicine_id)+','+str(medicine_name)+','+str(brand)+','+str(generic)+','+str(formation)+','+str(company)+'\n'
        
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=prescription_details.csv'   
    return str(myString)
    
    
def pr_details():
    cid=session.cid
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)
    
        
    qset=db()
    qset=qset(db.sm_prescription_head.cid == cid)
    qset = qset(db.sm_prescription_head.submit_date >= date_from)
    qset = qset(db.sm_prescription_head.submit_date < date_to_m)  
    
    qset=qset(db.sm_prescription_details.cid == cid)
    qset=qset(db.sm_prescription_head.sl == db.sm_prescription_details.sl)
      
        
    records=qset.select(db.sm_prescription_head.sl,db.sm_prescription_head.submit_date,db.sm_prescription_head.reg_id,db.sm_prescription_head.tl_id,db.sm_prescription_head.submit_by_id,db.sm_prescription_head.submit_by_name,db.sm_prescription_head.area_id,db.sm_prescription_head.area_name,db.sm_prescription_head.doctor_id,db.sm_prescription_head.doctor_name,db.sm_prescription_details.medicine_id,db.sm_prescription_details.medicine_name,db.sm_prescription_details.brand,db.sm_prescription_details.generic,db.sm_prescription_details.strength,db.sm_prescription_details.formation,db.sm_prescription_details.company, orderby=db.sm_prescription_head.area_id|db.sm_prescription_head.submit_by_id|db.sm_prescription_head.doctor_id|~db.sm_prescription_head.sl)
    
    
    return dict(records=records,date_from=date_from,date_to=date_to)


def count_area_wise():
    cid=session.cid
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)
    
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    
        
    qset=db()
    qset=qset(db.sm_prescription_head.cid == cid)
    qset = qset(db.sm_prescription_head.submit_date >= date_from)
    qset = qset(db.sm_prescription_head.submit_date < date_to_m) 
    
    if pr_region!='':
        qset=qset(db.sm_prescription_head.zone_id == pr_region)
    if pr_zone!='':
        qset=qset(db.sm_prescription_head.reg_id == pr_zone)
    if pr_area!='':
        qset=qset(db.sm_prescription_head.tl_id == pr_area)
    if pr_territory!='':
        qset=qset(db.sm_prescription_head.area_id == pr_territory)
    if pr_ff!='':
        qset=qset(db.sm_prescription_head.submit_by_id == pr_ff)
    if pr_doctor!='':
        qset=qset(db.sm_prescription_head.doctor_id == pr_doctor)
   
        
    records=qset.select(db.sm_prescription_head.submit_by_id,db.sm_prescription_head.submit_by_name,db.sm_prescription_head.area_id,db.sm_prescription_head.area_name,db.sm_prescription_head.doctor_id,db.sm_prescription_head.doctor_name,db.sm_prescription_head.id.count(), orderby=db.sm_prescription_head.area_id|db.sm_prescription_head.submit_by_id|db.sm_prescription_head.doctor_id,groupby=db.sm_prescription_head.area_id|db.sm_prescription_head.submit_by_id|db.sm_prescription_head.doctor_id)
    
    
    return dict(records=records,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)

def count_day_wise():
    cid=session.cid
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    
    date_to_m=datetime.datetime.strptime(str(date_to),'%Y-%m-%d') 
    date_to_m=date_to_m + datetime.timedelta(days = 1)
    
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    
        
    qset=db()
    qset=qset(db.sm_prescription_head.cid == cid)
    qset = qset(db.sm_prescription_head.submit_date >= date_from)
    qset = qset(db.sm_prescription_head.submit_date < date_to_m)
    
    if pr_region!='':
        qset=qset(db.sm_prescription_head.zone_id == pr_region)
    if pr_zone!='':
        qset=qset(db.sm_prescription_head.reg_id == pr_zone)
    if pr_area!='':
        qset=qset(db.sm_prescription_head.tl_id == pr_area)
    if pr_territory!='':
        qset=qset(db.sm_prescription_head.area_id == pr_territory)
    if pr_ff!='':
        qset=qset(db.sm_prescription_head.submit_by_id == pr_ff)
    if pr_doctor!='':
        qset=qset(db.sm_prescription_head.doctor_id == pr_doctor)


        
    records=qset.select(db.sm_prescription_head.submit_date,db.sm_prescription_head.id.count(), orderby=~db.sm_prescription_head.submit_date,groupby=db.sm_prescription_head.submit_date)
    
    return dict(records=records,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)




