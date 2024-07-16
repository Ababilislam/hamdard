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
    
    # seenStr = # seenUpdate = db((db.
    comRows = db((db.sm_settings.cid == session.cid) & (db. sm_settings.s_key == 'COM_NAME')).select(db.sm_settings.field1, limitby=(0, 1))
    if comRows:
        company_name=comRows[0].field1         
        session.company_name=company_name
        

    c_id = session.cid

    search_form =SQLFORM(db.sm_search_date)
    
    #block 1
    btn_company_track2=request.vars.btn_company_track2
    btn_company_track2_rm=request.vars.btn_company_track2_rm
    
    btn_institute_track2=request.vars.btn_institute_track2


    btn_corp_share_by_brand=request.vars.btn_corp_share_by_brand
    
    #block 2
    btn_physician_track2=request.vars.btn_physician_track2
    btn_physician_track2_d = request.vars.btn_physician_track2_d

    
    #block 3
    btn_pr_details=request.vars.btn_pr_details
    btn_pr_details_d=request.vars.btn_pr_details_d
    btn_pr_summary=request.vars.btn_pr_summary

    btn_generic_track2_by_physician = request.vars.btn_generic_track2_by_physician
    btn_generic_track2_by_competitions=request.vars.btn_generic_track2_by_competitions
    btn_company_track2_by_competitions = request.vars.btn_company_track2_by_competitions
    
    #block 4
    btn_sum_day_wise=request.vars.btn_sum_day_wise
    btn_sum_area_wise=request.vars.btn_sum_area_wise
    
    btn_sum_reg_wise=request.vars.btn_sum_reg_wise
    btn_sum_reg_wise_d=request.vars.btn_sum_reg_wise_d
    
    btn_sum_zone_wise=request.vars.btn_sum_zone_wise
    btn_sum_zone_wise_d=request.vars.btn_sum_zone_wise_d
    
    btn_sum_area_wise1=request.vars.btn_sum_area_wise1
    btn_sum_area_wise1_d=request.vars.btn_sum_area_wise1_d
    
    btn_sum_territory_wise=request.vars.btn_sum_territory_wise
    btn_sum_territory_wise_d=request.vars.btn_sum_territory_wise_d
    
    btn_sum_submit_by_wise=request.vars.btn_sum_submit_by_wise
    btn_sum_submit_by_wise_d=request.vars.btn_sum_submit_by_wise_d
    
    btn_sum_no_submission=request.vars.btn_sum_no_submission
    btn_sum_no_submission_d=request.vars.btn_sum_no_submission_d
    
    
    #block 5
    btn_orphan_med_list=request.vars.btn_orphan_med_list

    mpo_ranking=request.vars.mpo_ranking
    am_ranking=request.vars.am_ranking
    zm_ranking=request.vars.zm_ranking
    rsm_ranking=request.vars.rsm_ranking


    dr_mpo_ranking=request.vars.dr_mpo_ranking
    dr_am_ranking=request.vars.dr_am_ranking
    dr_zm_ranking=request.vars.dr_zm_ranking
    dr_rsm_ranking=request.vars.dr_rsm_ranking
    
    if btn_corp_share_by_brand or btn_institute_track2 or btn_company_track2_rm or btn_company_track2 :
        med_identical=request.vars.med_identical1
        med_division=request.vars.med_division1
        pr_region=request.vars.pr_region1
        pr_year1=request.vars.pr_year1
        pr_quarter1=request.vars.pr_quarter1
        pr_month1=request.vars.pr_month1
        pr_cycle1=request.vars.pr_cycle1
        
        pr_year2=request.vars.pr_year2
        pr_quarter2=request.vars.pr_quarter2
        pr_month2=request.vars.pr_month2
        pr_cycle2=request.vars.pr_cycle2
        
        
        pr_zone=request.vars.pr_zone1
        pr_area=request.vars.pr_area1
        pr_territory=request.vars.pr_territory1
        
                    
        if pr_year1=='' and pr_year2=='':
            response.flash="Select Region Year"
        else:
            if pr_region=='':
                response.flash="Select Region"
            else:
                if btn_company_track2:
                    redirect (URL('company_track2',vars=dict(identical=med_identical,med_division=med_division,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_year1=pr_year1,pr_quarter1=pr_quarter1,pr_month1=pr_month1,pr_cycle1=pr_cycle1,pr_year2=pr_year2,pr_quarter2=pr_quarter2,pr_month2=pr_month2,pr_cycle2=pr_cycle2)))
                elif btn_institute_track2:
                    redirect (URL('institute_track2',vars=dict(identical=med_identical,med_division=med_division,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_year1=pr_year1,pr_quarter1=pr_quarter1,pr_month1=pr_month1,pr_cycle1=pr_cycle1,pr_year2=pr_year2,pr_quarter2=pr_quarter2,pr_month2=pr_month2,pr_cycle2=pr_cycle2)))

            if btn_company_track2_rm:
                redirect (URL('company_track2_rm',vars=dict(identical=med_identical,med_division=med_division,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_year1=pr_year1,pr_quarter1=pr_quarter1,pr_month1=pr_month1,pr_cycle1=pr_cycle1,pr_year2=pr_year2,pr_quarter2=pr_quarter2,pr_month2=pr_month2,pr_cycle2=pr_cycle2)))

            if btn_corp_share_by_brand:
                redirect (URL('corp_share_by_brand',vars=dict(identical=med_identical,med_division=med_division,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_year1=pr_year1,pr_quarter1=pr_quarter1,pr_month1=pr_month1,pr_cycle1=pr_cycle1,pr_year2=pr_year2,pr_quarter2=pr_quarter2,pr_month2=pr_month2,pr_cycle2=pr_cycle2)))

            
    elif btn_physician_track2_d or btn_physician_track2:
        med_identical=request.vars.med_identical2
        med_division=request.vars.med_division2
        
        date_from=request.vars.from_dt
        date_to=request.vars.to_dt
        
        pr_region=request.vars.pr_region2
        pr_zone=request.vars.pr_zone2
        pr_area=request.vars.pr_area2
        pr_territory=request.vars.pr_territory2
        pr_doctor=request.vars.pr_doctor2
        pr_ff=request.vars.pr_ff2
        kol_doctor = request.vars.kol_doctor2
        
        if pr_region=='None':
            pr_region=''
        
        if pr_zone=='None':
            pr_zone=''
        
        if pr_area=='None':
            pr_area=''
        
        if pr_territory=='None':
            pr_territory=''
        
        if pr_doctor=='None':
            pr_doctor=''
        
        if pr_ff=='None':
            pr_ff=''


        
        
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
            if pr_doctor=='':                
                dateDiff=(to_dt2-from_dt2).days
                
                if dateDiff>31:
                    response.flash="Maximum 31 days allowed between Date Range"
                    dateFlag=False
                
                if pr_region=='':
                    response.flash="Select Region"
                
                
                
                        
        if dateFlag!=False:
            if btn_physician_track2:
                redirect (URL('physician_track2',vars=dict(identical=med_identical,med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,kol_doctor=kol_doctor,pr_ff=pr_ff)))

            if btn_physician_track2_d:
                redirect(URL('physician_track2_d',vars=dict(identical=med_identical, med_division=med_division, date_from=date_from,date_to=date_to, pr_region=pr_region, pr_zone=pr_zone, pr_area=pr_area,pr_territory=pr_territory, pr_doctor=pr_doctor,kol_doctor=kol_doctor,pr_ff=pr_ff)))

    elif btn_company_track2_by_competitions or btn_generic_track2_by_competitions or btn_generic_track2_by_physician or btn_pr_details or btn_pr_details_d or btn_pr_summary:
        med_division=request.vars.med_division3
        
        date_from=request.vars.from_dt_2
        date_to=request.vars.to_dt_2
        
        pr_region=request.vars.pr_region3
        pr_zone=request.vars.pr_zone3
        pr_area=request.vars.pr_area3
        pr_territory=request.vars.pr_territory3
        pr_doctor=request.vars.pr_doctor3
        pr_ff=request.vars.pr_ff3
        med_generic=request.vars.med_generic3
        
        if pr_region=='None':
            pr_region=''
        
        if pr_zone=='None':
            pr_zone=''
        
        if pr_area=='None':
            pr_area=''
        
        if pr_territory=='None':
            pr_territory=''
        
        if pr_doctor=='None':
            pr_doctor=''
        
        if pr_ff=='None':
            pr_ff=''
            
        if med_generic=='None':
            med_generic=''
        

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

            if dateDiff>31:
                response.flash="Maximum 31 days allowed between Date Range"
                dateFlag=False

        if dateFlag!=False:
            if btn_generic_track2_by_competitions or btn_company_track2_by_competitions:
                if pr_region == '':
                    response.flash = "Select Region"
                else:
                    if btn_generic_track2_by_competitions:
                        redirect(URL('generic_track2_by_competitions',vars=dict(med_division=med_division, date_from=date_from, date_to=date_to,pr_region=pr_region, pr_zone=pr_zone, pr_area=pr_area,pr_territory=pr_territory, pr_doctor=pr_doctor, pr_ff=pr_ff,med_generic=med_generic)))

                    elif btn_company_track2_by_competitions:
                        redirect(URL('company_track2_by_competitions',vars=dict(med_division=med_division, date_from=date_from, date_to=date_to,pr_region=pr_region, pr_zone=pr_zone, pr_area=pr_area,pr_territory=pr_territory, pr_doctor=pr_doctor, pr_ff=pr_ff,med_generic=med_generic)))

            elif btn_generic_track2_by_physician or btn_pr_summary or btn_pr_details or btn_pr_details_d:
                if med_generic=='':
                    response.flash='Required Generic'
                else:
                    if btn_pr_details:
                        redirect (URL('pr_details',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,med_generic=med_generic)))
                    elif btn_pr_details_d:
                        redirect (URL('pr_details_d',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,med_generic=med_generic)))
                    elif btn_pr_summary:
                        redirect(URL('pr_summary',vars=dict(med_division=med_division, date_from=date_from, date_to=date_to,pr_region=pr_region, pr_zone=pr_zone, pr_area=pr_area,pr_territory=pr_territory, pr_doctor=pr_doctor, pr_ff=pr_ff,med_generic=med_generic)))
                    elif btn_generic_track2_by_physician:
                        redirect(URL('generic_track2_by_physician',vars=dict(med_division=med_division, date_from=date_from, date_to=date_to,pr_region=pr_region, pr_zone=pr_zone, pr_area=pr_area,pr_territory=pr_territory, pr_doctor=pr_doctor, pr_ff=pr_ff,med_generic=med_generic)))



    elif btn_sum_reg_wise or btn_sum_reg_wise_d or btn_sum_zone_wise or btn_sum_zone_wise_d or btn_sum_area_wise1 or btn_sum_area_wise1_d or btn_sum_territory_wise or btn_sum_territory_wise_d or btn_sum_submit_by_wise or btn_sum_submit_by_wise_d or btn_sum_no_submission or btn_sum_no_submission_d or btn_sum_day_wise or btn_sum_area_wise  or mpo_ranking or am_ranking or zm_ranking or rsm_ranking or dr_mpo_ranking or dr_am_ranking or dr_zm_ranking or dr_rsm_ranking:
        med_division=request.vars.med_division4
        
        date_from=request.vars.from_dt_3
        date_to=request.vars.to_dt_3
        
        pr_region=request.vars.pr_region4
        pr_zone=request.vars.pr_zone4
        pr_area=request.vars.pr_area4
        pr_territory=request.vars.pr_territory4
        pr_brand=request.vars.pr_brand4
       
        pr_doctor=request.vars.pr_doctor4
        pr_doc=request.vars.pr_doctor3
        pr_ff=request.vars.pr_ff4
        
        
        if pr_region=='None':
            pr_region=''
        
        if pr_zone=='None':
            pr_zone=''
        
        if pr_area=='None':
            pr_area=''
        
        if pr_territory=='None':
            pr_territory=''
        
        if pr_brand=='None':
            pr_brand=''
        
        if pr_doctor=='None':
            pr_doctor=''
        
        if pr_ff=='None':
            pr_ff=''
        
        if pr_ff=='None':
            pr_ff=''


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

            if dateDiff>31:
                response.flash="Maximum 31 days allowed between Date Range"
                dateFlag=False

        if dateFlag!=False:
            if btn_sum_day_wise:
                redirect (URL('sum_day_wise',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)))
            elif btn_sum_area_wise:
                redirect (URL('sum_area_wise',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)))
                               
            elif btn_sum_reg_wise:
                redirect (URL('sum_reg_wise',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,pr_brand=pr_brand)))
            elif btn_sum_reg_wise_d:
                redirect (URL('sum_reg_wise_d',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,pr_brand=pr_brand)))
                        
            elif btn_sum_zone_wise:
                redirect (URL('sum_zone_wise',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,pr_brand=pr_brand)))
            elif btn_sum_zone_wise_d:
                redirect (URL('sum_zone_wise_d',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,pr_brand=pr_brand)))
                        
            elif btn_sum_area_wise1:
                redirect (URL('sum_area_wise1',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,pr_brand=pr_brand)))
            elif btn_sum_area_wise1_d:
                redirect (URL('sum_area_wise1_d',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,pr_brand=pr_brand)))
            
            elif btn_sum_territory_wise:
                redirect (URL('sum_territory_wise',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,pr_brand=pr_brand)))
            elif btn_sum_territory_wise_d:
                redirect (URL('sum_territory_wise_d',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,pr_brand=pr_brand)))
            
            elif btn_sum_submit_by_wise:
                redirect (URL('sum_submit_by_wise',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,pr_brand=pr_brand)))
            elif btn_sum_submit_by_wise_d:
                redirect (URL('sum_submit_by_wise_d',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,pr_brand=pr_brand)))
            
            elif btn_sum_no_submission:
                redirect (URL('no_submission_area',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,pr_brand=pr_brand)))
            elif btn_sum_no_submission_d:
                redirect (URL('no_submission_area_d',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,pr_brand=pr_brand)))
            
            if mpo_ranking:
                redirect (URL('sin_mpo_ranking',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doc=pr_doc,pr_ff=pr_ff,pr_brand=pr_brand)))
            if am_ranking:
                redirect (URL('sin_fm_ranking',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doc=pr_doc,pr_ff=pr_ff,pr_brand=pr_brand)))
            if zm_ranking:
                redirect (URL('sin_zm_ranking',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doc=pr_doc,pr_ff=pr_ff,pr_brand=pr_brand)))
            if rsm_ranking:
                redirect (URL('sin_rsm_ranking',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doc=pr_doc,pr_ff=pr_ff,pr_brand=pr_brand)))            

            if dr_mpo_ranking:
                redirect (URL('dr_sin_mpo_ranking',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doc=pr_doc,pr_ff=pr_ff,pr_brand=pr_brand)))
            if dr_am_ranking:
                redirect (URL('dr_sin_fm_ranking',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doc=pr_doc,pr_ff=pr_ff,pr_brand=pr_brand)))
            if dr_zm_ranking:
                redirect (URL('dr_sin_zm_ranking',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doc=pr_doc,pr_ff=pr_ff,pr_brand=pr_brand)))
            if dr_rsm_ranking:
                redirect (URL('dr_sin_rsm_ranking',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doc=pr_doc,pr_ff=pr_ff,pr_brand=pr_brand)))
                                                 
            if mpo_ranking:
                redirect (URL('sin_mpo_ranking',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doc=pr_doc,pr_ff=pr_ff,pr_brand=pr_brand)))
            if am_ranking:
                redirect (URL('sin_fm_ranking',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doc=pr_doc,pr_ff=pr_ff,pr_brand=pr_brand)))
            if zm_ranking:
                redirect (URL('sin_zm_ranking',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doc=pr_doc,pr_ff=pr_ff,pr_brand=pr_brand)))
            if rsm_ranking:
                redirect (URL('sin_rsm_ranking',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doc=pr_doc,pr_ff=pr_ff,pr_brand=pr_brand)))            

            if dr_mpo_ranking:
                redirect (URL('dr_sin_mpo_ranking',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doc=pr_doc,pr_ff=pr_ff,pr_brand=pr_brand)))
            if dr_am_ranking:
                redirect (URL('dr_sin_fm_ranking',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doc=pr_doc,pr_ff=pr_ff,pr_brand=pr_brand)))
            if dr_zm_ranking:
                redirect (URL('dr_sin_zm_ranking',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doc=pr_doc,pr_ff=pr_ff,pr_brand=pr_brand)))
            if dr_rsm_ranking:
                redirect (URL('dr_sin_rsm_ranking',vars=dict(med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doc=pr_doc,pr_ff=pr_ff,pr_brand=pr_brand)))
                                                   
    elif btn_orphan_med_list:
        date_from=request.vars.from_dt_4
        date_to=request.vars.to_dt_4
    
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
        
        if dateFlag!=False:
            if btn_orphan_med_list:
                redirect (URL('orphan_med_list',vars=dict(date_from=date_from,date_to=date_to)))



    # region
    regionRows = db((db.sm_level.cid == c_id) & (db.sm_level.is_leaf == '0') & (db.sm_level.depth == 0)).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
    # brand
    brandRows = db(db.seen_rx_brand.cid == c_id).select(db.seen_rx_brand.brand_name, orderby=db.seen_rx_brand.brand_name)
          
    return dict(regionRows=regionRows,brandRows=brandRows,search_form=search_form)


# block 5
def orphan_med_list():
    response.title='Orphan Medecine List'
    cid=session.cid
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    

    qset=db()
    qset=qset(db.sm_prescription_details.cid == cid)
    qset = qset(db.sm_prescription_details.submit_date >= date_from)
    qset = qset(db.sm_prescription_details.submit_date <= date_to)
    qset=qset(db.sm_prescription_details.medicine_id == 0)
    
        
    records=qset.select(db.sm_prescription_details.medicine_name,db.sm_prescription_details.submit_by_id,db.sm_prescription_details.submit_by_name, orderby=db.sm_prescription_details.medicine_name)
    
    
    return dict(records=records,date_from=date_from,date_to=date_to) 


# block 4

def no_submission_area_d():
    cid=session.cid    
    med_division=request.vars.med_division
    
    if med_division=='PHARMA':
        response.title='Details Pharma'
    elif med_division=='SINAVISION':
        response.title='Details Sinavision'
    else:
        response.title = 'No Submission Area'
        
    date_from=request.vars.date_from
    date_to=request.vars.date_to
        
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory    
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    pr_brand=request.vars.pr_brand
    
    if pr_region=='None':
        pr_region=''
    
    if pr_zone=='None':
        pr_zone=''
    
    if pr_area=='None':
        pr_area=''
    
    if pr_territory=='None':
        pr_territory=''
    
    if pr_doctor=='None':
        pr_doctor=''
    
    if pr_ff=='None':
        pr_ff=''
    
    
    condition=''
#    if pr_region != '':
#        condition += " and a.level0 ='" + pr_region + "'"
#    if pr_zone != '':
#        condition += " and a.level1 ='" + pr_zone + "'"
#    if pr_area != '':
#        condition += " and a.level2 ='" + pr_area + "'"
#    if pr_territory != '':
#        condition += " and a.level_id ='" + pr_territory + "'"

#    if pr_brand != '':
#        condition += " and b.medicine_id = '" + str(pr_brand) + "'"

#    if pr_doctor != '':
#        condition += " and b.doctor_id = '" + str(pr_doctor) + "'"
#    if med_generic != '':
#        condition += " and b.generic = '" + str(med_generic)+ "'"
    
    submitAreaList=[]
    sql1 = "(SELECT a.level3 as level3 FROM `sm_level` a,`sm_prescription_seen_head` b WHERE  b.cid='" + cid + "' and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id group by a.level0,a.level1,a.level2,a.level3)"
    submitAreaRecords = db.executesql(sql1, as_dict=True)
    for i in range(len(submitAreaRecords)):
        submitAreaRecordS=submitAreaRecords[i]
        submitAreaList.append(str(submitAreaRecordS['level3']).strip())
    
    submitAreaStr=''
    if len(submitAreaList)>0:
        submitAreaStr=str(submitAreaList).replace("['","'").replace("']","'")
    
    if submitAreaStr != '':
        condition += " and level_id not in ("+submitAreaStr+")"
        
    allAreaList=[]
    sql2 = "(SELECT level0,level0_name,level1,level1_name,level2,level2_name,level_id as level3,level_name as level3_name FROM `sm_level` WHERE  cid='" + cid + "' and depth=3 " + condition + " order by level0,level1,level2,level_id)"
    allAreaList = db.executesql(sql2, as_dict=True)
    
        
            
    myString = 'No Submission Area (Seen) \n'
    myString += 'Date Range:' + ',' + str(date_from) + ' To ' + str(date_to) + '\n\n'
    
    myString += 'SL,Region ID,Region Name,Zone ID,Zone Name,Area ID,Area Name,Territory ID,Territory Name' + '\n'
    
    sl=0
    
    for i in range(len(allAreaList)):
        allAreaListStr=allAreaList[i] 
        sl+=1
        
        level0=allAreaListStr['level0']
        level0_name=allAreaListStr['level0_name']
        level1=allAreaListStr['level1']
        level1_name=allAreaListStr['level1_name']
        level2=allAreaListStr['level2']
        level2_name=allAreaListStr['level2_name']
        level3=allAreaListStr['level3']
        level3_name=allAreaListStr['level3_name']
                
        myString += str(sl) + ',' + str(level0) + ',' + str(level0_name) + ',' + str(level1) + ',' + str(level1_name)+ ',' + str(level2) + ',' + str(level2_name)+ ',' + str(level3) + ',' + str(level3_name) + '\n'
    
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=prescription_seen_no_submission_area.csv'
    return str(myString)
    
def no_submission_area():
    cid=session.cid    
    med_division=request.vars.med_division
    
    if med_division=='PHARMA':
        response.title='Details Pharma'
    elif med_division=='SINAVISION':
        response.title='Details Sinavision'
    else:
        response.title = 'No Submission Area'
        
    date_from=request.vars.date_from
    date_to=request.vars.date_to
        
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory    
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    pr_brand=request.vars.pr_brand
    
    if pr_region=='None':
        pr_region=''
    
    if pr_zone=='None':
        pr_zone=''
    
    if pr_area=='None':
        pr_area=''
    
    if pr_territory=='None':
        pr_territory=''
    
    if pr_doctor=='None':
        pr_doctor=''
    
    if pr_ff=='None':
        pr_ff=''
    
    
    condition=''
#    if pr_region != '':
#        condition += " and a.level0 ='" + pr_region + "'"
#    if pr_zone != '':
#        condition += " and a.level1 ='" + pr_zone + "'"
#    if pr_area != '':
#        condition += " and a.level2 ='" + pr_area + "'"
#    if pr_territory != '':
#        condition += " and a.level_id ='" + pr_territory + "'"

#    if pr_brand != '':
#        condition += " and b.medicine_id = '" + str(pr_brand) + "'"

#    if pr_doctor != '':
#        condition += " and b.doctor_id = '" + str(pr_doctor) + "'"
#    if med_generic != '':
#        condition += " and b.generic = '" + str(med_generic)+ "'"
    
    submitAreaList=[]
    sql1 = "(SELECT a.level3 as level3 FROM `sm_level` a,`sm_prescription_seen_head` b WHERE  b.cid='" + cid + "' and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id group by a.level0,a.level1,a.level2,a.level3)"
    submitAreaRecords = db.executesql(sql1, as_dict=True)
    for i in range(len(submitAreaRecords)):
        submitAreaRecordS=submitAreaRecords[i]
        submitAreaList.append(str(submitAreaRecordS['level3']).strip())
    
    submitAreaStr=''
    if len(submitAreaList)>0:
        submitAreaStr=str(submitAreaList).replace("['","'").replace("']","'")
    
    if submitAreaStr != '':
        condition += " and level_id not in ("+submitAreaStr+")"
        
    allAreaList=[]
    sql2 = "(SELECT level0,level0_name,level1,level1_name,level2,level2_name,level_id as level3,level_name as level3_name FROM `sm_level` WHERE  cid='" + cid + "' and depth=3 " + condition + " order by level0,level1,level2,level_id)"
    allAreaList = db.executesql(sql2, as_dict=True)
    
        
    reg_name=''
    regionRows=db((db.sm_level.cid==cid)&(db.sm_level.level_id==pr_region)).select(db.sm_level.level_name,limitby=(0,1))
    if regionRows:
        reg_name=regionRows[0].level_name
    
    return dict(allAreaList=allAreaList,submitAreaList=submitAreaList,med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,reg_name=reg_name,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,pr_brand=pr_brand)

def sum_submit_by_wise_d():
    cid=session.cid    
    med_division=request.vars.med_division
    
    if med_division=='PHARMA':
        response.title='Details Pharma'
    elif med_division=='SINAVISION':
        response.title='Details Sinavision'
    else:
        response.title = 'Submitted By Wise'
        
    date_from=request.vars.date_from
    date_to=request.vars.date_to
        
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory    
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    pr_brand=request.vars.pr_brand
    
    if pr_region=='None':
        pr_region=''
    
    if pr_zone=='None':
        pr_zone=''
    
    if pr_area=='None':
        pr_area=''
    
    if pr_territory=='None':
        pr_territory=''
    
    if pr_brand=='None':
        pr_brand=''
    
    if pr_brand!='':
        pr_brand=str(pr_brand).replace("[","").replace(" ","").replace("]","")
    
    if pr_doctor=='None':
        pr_doctor=''
    
    if pr_ff=='None':
        pr_ff=''
    
    
    condition=''
    if pr_region != '':
        condition += " and a.level0 ='" + pr_region + "'"
    if pr_zone != '':
        condition += " and a.level1 ='" + pr_zone + "'"
    if pr_area != '':
        condition += " and a.level2 ='" + pr_area + "'"
    if pr_territory != '':
        condition += " and a.level_id ='" + pr_territory + "'"

    condition1=''
    if pr_brand != '':
        if len(str(pr_brand).split(','))>1:
            condition1 += " and b.medicine_id in (" + str(pr_brand) + ")"
        else:
            condition1 += " and b.medicine_id ='" + str(pr_brand) + "'"

#    if pr_doctor != '':
#        condition += " and b.doctor_id = '" + str(pr_doctor) + "'"
#    if med_generic != '':
#        condition += " and b.generic = '" + str(med_generic)+ "'"

    
    recordList=[]
    sql1 = "(SELECT a.level0 as level0,a.level0_name as level0_name,a.level1 as level1,a.level1_name as level1_name,a.level2 as level2,a.level2_name as level2_name,a.level3 as level3,a.level3_name as level3_name,b.submit_by_id as submit_by_id,b.submit_by_name as submit_by_name,count(b.sl) as totalRx,0 as brandPrecence FROM `sm_level` a,`sm_prescription_seen_head` b WHERE  b.cid='" + cid + "' and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0,a.level1,a.level2,a.level3 )"
    sql2 = "(SELECT a.level0 as level0,a.level0_name as level0_name,a.level1 as level1,a.level1_name as level1_name,a.level2 as level2,a.level2_name as level2_name,a.level3 as level3,a.level3_name as level3_name,b.submit_by_id as submit_by_id,b.submit_by_name as submit_by_name,0 as totalRx,count(distinct(b.sl)) as brandPrecence FROM `sm_level` a,`sm_prescription_seen_details` b WHERE  b.cid='" + cid + "' and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' " + str(condition1) + " and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0,a.level1,a.level2,a.level3)"
    
    records = "select level0,level0_name,level1,level1_name,level2,level2_name,level3,level3_name,submit_by_id,submit_by_name,sum(totalRx) as totalRx,sum(brandPrecence) as brandPrecence from (" + sql1 + " union all " + sql2 + ") p group by level0,level1,level2,level3 order by level0,level1,level2,level3,submit_by_id"
    recordList = db.executesql(records, as_dict=True)
      
    
    reg_name=''
    regionRows=db((db.sm_level.cid==cid)&(db.sm_level.level_id==pr_region)).select(db.sm_level.level_name,limitby=(0,1))
    if regionRows:
        reg_name=regionRows[0].level_name
    
    if pr_brand!='':
        pr_brand=str(pr_brand).replace("','","; ").replace("'","")
    else:
        pr_brand='ALL'
        
    myString = 'Prescription Summary Territory Wise (Seen) \n'
    myString += 'Date Range:' + ',' + str(date_from) + ' To ' + str(date_to) + '\n'
    myString += 'Zone:' + ',' + str(pr_region) + '\n'
    myString += 'Region:' + ',' + str(pr_zone) + '\n'
    myString += 'Area:' + ',' + str(pr_area) + '\n'
    myString += 'Territory:' + ',' + str(pr_territory) + '\n'
    myString += 'Brand:' + ',' + str(pr_brand) + '\n\n'

    
    myString += 'Region ID,Region Name,Zone ID,Zone Name,Area ID,Area Name,Territory ID,Territory Name,Submitted By ID,Submitted By Name,Total Rx,Brand Presence' + '\n'
    
    gTotal=0;gTotal1=0;
    
    for i in range(len(recordList)):
        recordListStr=recordList[i] 
        
        level0=recordListStr['level0']
        level0_name=recordListStr['level0_name']
        level1=recordListStr['level1']
        level1_name=recordListStr['level1_name']
        level2=recordListStr['level2']
        level2_name=recordListStr['level2_name']
        level3=recordListStr['level3']
        level3_name=recordListStr['level3_name']
        submit_by_id=recordListStr['submit_by_id']
        submit_by_name=recordListStr['submit_by_name']
        
        totalRx=recordListStr['totalRx']
        brandPrecence=recordListStr['brandPrecence']
        
        gTotal+=recordListStr['totalRx']
        gTotal1+=recordListStr['brandPrecence']
        
        myString += str(level0) + ',' + str(level0_name) + ',' + str(level1) + ',' + str(level1_name)+ ',' + str(level2) + ',' + str(level2_name)+ ',' + str(level3) + ',' + str(level3_name)+ ',' + str(submit_by_id) + ',' + str(submit_by_name)+ ',' + str(totalRx) + ',' + str(brandPrecence) + '\n'
    
    myString += 'Total,,,,,,,,,,' + str(gTotal) + ',' + str(gTotal1) + '\n'

    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=prescription_seen_submitted_by_wise.csv'
    return str(myString)
    
def sum_submit_by_wise():
    cid=session.cid    
    med_division=request.vars.med_division
    
    if med_division=='PHARMA':
        response.title='Details Pharma'
    elif med_division=='SINAVISION':
        response.title='Details Sinavision'
    else:
        response.title = 'Submitted By Wise'
        
    date_from=request.vars.date_from
    date_to=request.vars.date_to
        
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory    
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    pr_brand=request.vars.pr_brand
    
    if pr_region=='None':
        pr_region=''
    
    if pr_zone=='None':
        pr_zone=''
    
    if pr_area=='None':
        pr_area=''
    
    if pr_territory=='None':
        pr_territory=''
    
    if pr_brand=='None':
        pr_brand=''
    
    if pr_brand!='':
        pr_brand=str(pr_brand).replace("[","").replace(" ","").replace("]","")
    
    if pr_doctor=='None':
        pr_doctor=''
    
    if pr_ff=='None':
        pr_ff=''
    
    
    condition=''
    if pr_region != '':
        condition += " and a.level0 ='" + pr_region + "'"
    if pr_zone != '':
        condition += " and a.level1 ='" + pr_zone + "'"
    if pr_area != '':
        condition += " and a.level2 ='" + pr_area + "'"
    if pr_territory != '':
        condition += " and a.level_id ='" + pr_territory + "'"

    condition1=''
    if pr_brand != '':
        if len(str(pr_brand).split(','))>1:
            condition1 += " and b.medicine_id in (" + str(pr_brand) + ")"
        else:
            condition1 += " and b.medicine_id ='" + str(pr_brand) + "'"

#    if pr_doctor != '':
#        condition += " and b.doctor_id = '" + str(pr_doctor) + "'"
#    if med_generic != '':
#        condition += " and b.generic = '" + str(med_generic)+ "'"

    
    recordList=[]
    sql1 = "(SELECT a.level0 as level0,a.level0_name as level0_name,a.level1 as level1,a.level1_name as level1_name,a.level2 as level2,a.level2_name as level2_name,a.level3 as level3,a.level3_name as level3_name,b.submit_by_id as submit_by_id,b.submit_by_name as submit_by_name,count(b.sl) as totalRx,0 as brandPrecence FROM `sm_level` a,`sm_prescription_seen_head` b WHERE  b.cid='" + cid + "' and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0,a.level1,a.level2,a.level3 )"
    sql2 = "(SELECT a.level0 as level0,a.level0_name as level0_name,a.level1 as level1,a.level1_name as level1_name,a.level2 as level2,a.level2_name as level2_name,a.level3 as level3,a.level3_name as level3_name,b.submit_by_id as submit_by_id,b.submit_by_name as submit_by_name,0 as totalRx,count(distinct(b.sl)) as brandPrecence FROM `sm_level` a,`sm_prescription_seen_details` b WHERE  b.cid='" + cid + "' and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' " + str(condition1) + " and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0,a.level1,a.level2,a.level3)"
    
    records = "select level0,level0_name,level1,level1_name,level2,level2_name,level3,level3_name,submit_by_id,submit_by_name,sum(totalRx) as totalRx,sum(brandPrecence) as brandPrecence from (" + sql1 + " union all " + sql2 + ") p group by level0,level1,level2,level3 order by level0,level1,level2,level3,submit_by_id"
    recordList = db.executesql(records, as_dict=True)
      
    
    reg_name=''
    regionRows=db((db.sm_level.cid==cid)&(db.sm_level.level_id==pr_region)).select(db.sm_level.level_name,limitby=(0,1))
    if regionRows:
        reg_name=regionRows[0].level_name
    
    return dict(recordList=recordList,med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,reg_name=reg_name,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,pr_brand=pr_brand)

def sum_territory_wise_d():
    cid=session.cid    
    med_division=request.vars.med_division
    
    if med_division=='PHARMA':
        response.title='Details Pharma'
    elif med_division=='SINAVISION':
        response.title='Details Sinavision'
    else:
        response.title = 'Territory Wise'
        
    date_from=request.vars.date_from
    date_to=request.vars.date_to
        
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory    
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    pr_brand=request.vars.pr_brand
    
    if pr_region=='None':
        pr_region=''
    
    if pr_zone=='None':
        pr_zone=''
    
    if pr_area=='None':
        pr_area=''
    
    if pr_territory=='None':
        pr_territory=''
    
    if pr_brand=='None':
        pr_brand=''
    
    if pr_brand!='':
        pr_brand=str(pr_brand).replace("[","").replace(" ","").replace("]","")
    
    if pr_doctor=='None':
        pr_doctor=''
    
    if pr_ff=='None':
        pr_ff=''
    
    
    condition=''
    if pr_region != '':
        condition += " and a.level0 ='" + pr_region + "'"
    if pr_zone != '':
        condition += " and a.level1 ='" + pr_zone + "'"
    if pr_area != '':
        condition += " and a.level2 ='" + pr_area + "'"
    if pr_territory != '':
        condition += " and a.level_id ='" + pr_territory + "'"

    condition1=''
    if pr_brand != '':
        if len(str(pr_brand).split(','))>1:
            condition1 += " and b.medicine_id in (" + str(pr_brand) + ")"
        else:
            condition1 += " and b.medicine_id ='" + str(pr_brand) + "'"

#    if pr_doctor != '':
#        condition += " and b.doctor_id = '" + str(pr_doctor) + "'"
#    if med_generic != '':
#        condition += " and b.generic = '" + str(med_generic)+ "'"

    
    recordList=[]
    sql1 = "(SELECT a.level0 as level0,a.level0_name as level0_name,a.level1 as level1,a.level1_name as level1_name,a.level2 as level2,a.level2_name as level2_name,a.level3 as level3,a.level3_name as level3_name,count(b.sl) as totalRx,0 as brandPrecence FROM `sm_level` a,`sm_prescription_seen_head` b WHERE  b.cid='" + cid + "' and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0,a.level1,a.level2,a.level3 )"
    sql2 = "(SELECT a.level0 as level0,a.level0_name as level0_name,a.level1 as level1,a.level1_name as level1_name,a.level2 as level2,a.level2_name as level2_name,a.level3 as level3,a.level3_name as level3_name,0 as totalRx,count(distinct(b.sl)) as brandPrecence FROM `sm_level` a,`sm_prescription_seen_details` b WHERE  b.cid='" + cid + "' and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' " + str(condition1) + " and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0,a.level1,a.level2,a.level3)"
    
    records = "select level0,level0_name,level1,level1_name,level2,level2_name,level3,level3_name,sum(totalRx) as totalRx,sum(brandPrecence) as brandPrecence from (" + sql1 + " union all " + sql2 + ") p group by level0,level1,level2,level3 order by level0,level1,level2,level3"
    recordList = db.executesql(records, as_dict=True)
      
    
    reg_name=''
    regionRows=db((db.sm_level.cid==cid)&(db.sm_level.level_id==pr_region)).select(db.sm_level.level_name,limitby=(0,1))
    if regionRows:
        reg_name=regionRows[0].level_name
    
    if pr_brand!='':
        pr_brand=str(pr_brand).replace("','","; ").replace("'","")
    else:
        pr_brand='ALL'
        
    myString = 'Prescription Summary Territory Wise (Seen) \n'
    myString += 'Date Range:' + ',' + str(date_from) + ' To ' + str(date_to) + '\n'
    myString += 'Zone:' + ',' + str(pr_region) + '\n'
    myString += 'Region:' + ',' + str(pr_zone) + '\n'
    myString += 'Area:' + ',' + str(pr_area) + '\n'
    myString += 'Territory:' + ',' + str(pr_territory) + '\n'
    myString += 'Brand:' + ',' + str(pr_brand) + '\n\n'

    
    myString += 'Region ID,Region Name,Zone ID,Zone Name,Area ID,Area Name,Territory ID,Territory Name,Total Rx,Brand Presence' + '\n'
    
    gTotal=0;gTotal1=0;
    
    for i in range(len(recordList)):
        recordListStr=recordList[i] 
        
        level0=recordListStr['level0']
        level0_name=recordListStr['level0_name']
        level1=recordListStr['level1']
        level1_name=recordListStr['level1_name']
        level2=recordListStr['level2']
        level2_name=recordListStr['level2_name']
        level3=recordListStr['level3']
        level3_name=recordListStr['level3_name']
        
        totalRx=recordListStr['totalRx']
        brandPrecence=recordListStr['brandPrecence']
        
        gTotal+=recordListStr['totalRx']
        gTotal1+=recordListStr['brandPrecence']
        
        myString += str(level0) + ',' + str(level0_name) + ',' + str(level1) + ',' + str(level1_name)+ ',' + str(level2) + ',' + str(level2_name)+ ',' + str(level3) + ',' + str(level3_name)+ ',' + str(totalRx) + ',' + str(brandPrecence) + '\n'
    
    myString += 'Total,,,,,,,,' + str(gTotal) + ',' + str(gTotal1) + '\n'

    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=prescription_seen_territory_wise.csv'
    return str(myString)
    
def sum_territory_wise():
    cid=session.cid    
    med_division=request.vars.med_division
    
    if med_division=='PHARMA':
        response.title='Details Pharma'
    elif med_division=='SINAVISION':
        response.title='Details Sinavision'
    else:
        response.title = 'Territory Wise'
        
    date_from=request.vars.date_from
    date_to=request.vars.date_to
        
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory    
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    pr_brand=request.vars.pr_brand
    
    if pr_region=='None':
        pr_region=''
    
    if pr_zone=='None':
        pr_zone=''
    
    if pr_area=='None':
        pr_area=''
    
    if pr_territory=='None':
        pr_territory=''
    
    if pr_brand=='None':
        pr_brand=''
    
    if pr_brand!='':
        pr_brand=str(pr_brand).replace("[","").replace(" ","").replace("]","")
    
    if pr_doctor=='None':
        pr_doctor=''
    
    if pr_ff=='None':
        pr_ff=''
    
    
    condition=''
    if pr_region != '':
        condition += " and a.level0 ='" + pr_region + "'"
    if pr_zone != '':
        condition += " and a.level1 ='" + pr_zone + "'"
    if pr_area != '':
        condition += " and a.level2 ='" + pr_area + "'"
    if pr_territory != '':
        condition += " and a.level_id ='" + pr_territory + "'"

    condition1=''
    if pr_brand != '':
        if len(str(pr_brand).split(','))>1:
            condition1 += " and b.medicine_id in (" + str(pr_brand) + ")"
        else:
            condition1 += " and b.medicine_id ='" + str(pr_brand) + "'"

#    if pr_doctor != '':
#        condition += " and b.doctor_id = '" + str(pr_doctor) + "'"
#    if med_generic != '':
#        condition += " and b.generic = '" + str(med_generic)+ "'"

    
    recordList=[]
    sql1 = "(SELECT a.level0 as level0,a.level0_name as level0_name,a.level1 as level1,a.level1_name as level1_name,a.level2 as level2,a.level2_name as level2_name,a.level3 as level3,a.level3_name as level3_name,count(b.sl) as totalRx,0 as brandPrecence FROM `sm_level` a,`sm_prescription_seen_head` b WHERE  b.cid='" + cid + "' and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0,a.level1,a.level2,a.level3 )"
    sql2 = "(SELECT a.level0 as level0,a.level0_name as level0_name,a.level1 as level1,a.level1_name as level1_name,a.level2 as level2,a.level2_name as level2_name,a.level3 as level3,a.level3_name as level3_name,0 as totalRx,count(distinct(b.sl)) as brandPrecence FROM `sm_level` a,`sm_prescription_seen_details` b WHERE  b.cid='" + cid + "' and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' " + str(condition1) + " and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0,a.level1,a.level2,a.level3)"
    
    records = "select level0,level0_name,level1,level1_name,level2,level2_name,level3,level3_name,sum(totalRx) as totalRx,sum(brandPrecence) as brandPrecence from (" + sql1 + " union all " + sql2 + ") p group by level0,level1,level2,level3 order by level0,level1,level2,level3"
    recordList = db.executesql(records, as_dict=True)
      
    
    reg_name=''
    regionRows=db((db.sm_level.cid==cid)&(db.sm_level.level_id==pr_region)).select(db.sm_level.level_name,limitby=(0,1))
    if regionRows:
        reg_name=regionRows[0].level_name
    
    return dict(recordList=recordList,med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,reg_name=reg_name,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,pr_brand=pr_brand)

def sum_area_wise1_d():
    cid=session.cid    
    med_division=request.vars.med_division
    
    if med_division=='PHARMA':
        response.title='Details Pharma'
    elif med_division=='SINAVISION':
        response.title='Details Sinavision'
    else:
        response.title = 'Area Wise'
        
    date_from=request.vars.date_from
    date_to=request.vars.date_to
        
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory    
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    pr_brand=request.vars.pr_brand
    
    if pr_region=='None':
        pr_region=''
    
    if pr_zone=='None':
        pr_zone=''
    
    if pr_area=='None':
        pr_area=''
    
    if pr_territory=='None':
        pr_territory=''
    
    if pr_brand=='None':
        pr_brand=''
    
    if pr_brand!='':
        pr_brand=str(pr_brand).replace("[","").replace(" ","").replace("]","")
    
    if pr_doctor=='None':
        pr_doctor=''
    
    if pr_ff=='None':
        pr_ff=''
    
    
    condition=''
    if pr_region != '':
        condition += " and a.level0 ='" + pr_region + "'"
    if pr_zone != '':
        condition += " and a.level1 ='" + pr_zone + "'"
    if pr_area != '':
        condition += " and a.level2 ='" + pr_area + "'"
    if pr_territory != '':
        condition += " and a.level_id ='" + pr_territory + "'"

    condition1=''
    if pr_brand != '':
        if len(str(pr_brand).split(','))>1:
            condition1 += " and b.medicine_id in (" + str(pr_brand) + ")"
        else:
            condition1 += " and b.medicine_id ='" + str(pr_brand) + "'"

#    if pr_doctor != '':
#        condition += " and b.doctor_id = '" + str(pr_doctor) + "'"
#    if med_generic != '':
#        condition += " and b.generic = '" + str(med_generic)+ "'"

    
    recordList=[]
    sql1 = "(SELECT a.level0 as level0,a.level0_name as level0_name,a.level1 as level1,a.level1_name as level1_name,a.level2 as level2,a.level2_name as level2_name,count(b.sl) as totalRx,0 as brandPrecence FROM `sm_level` a,`sm_prescription_seen_head` b WHERE  b.cid='" + cid + "' and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0,a.level1,a.level2 )"
    sql2 = "(SELECT a.level0 as level0,a.level0_name as level0_name,a.level1 as level1,a.level1_name as level1_name,a.level2 as level2,a.level2_name as level2_name,0 as totalRx,count(distinct(b.sl)) as brandPrecence FROM `sm_level` a,`sm_prescription_seen_details` b WHERE  b.cid='" + cid + "' and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' " + str(condition1) + " and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0,a.level1,a.level2)"
    
    records = "select level0,level0_name,level1,level1_name,level2,level2_name,sum(totalRx) as totalRx,sum(brandPrecence) as brandPrecence from (" + sql1 + " union all " + sql2 + ") p group by level0,level1,level2 order by level0,level1,level2"
    recordList = db.executesql(records, as_dict=True)
      
    
    reg_name=''
    regionRows=db((db.sm_level.cid==cid)&(db.sm_level.level_id==pr_region)).select(db.sm_level.level_name,limitby=(0,1))
    if regionRows:
        reg_name=regionRows[0].level_name
    
    if pr_brand!='':
        pr_brand=str(pr_brand).replace("','","; ").replace("'","")
    else:
        pr_brand='ALL'
        
    myString = 'Prescription Summary Area Wise (Seen) \n'
    myString += 'Date Range:' + ',' + str(date_from) + ' To ' + str(date_to) + '\n'
    myString += 'Zone:' + ',' + str(pr_region) + '\n'
    myString += 'Region:' + ',' + str(pr_zone) + '\n'
    myString += 'Area:' + ',' + str(pr_area) + '\n'
    myString += 'Territory:' + ',' + str(pr_territory) + '\n'
    myString += 'Brand:' + ',' + str(pr_brand) + '\n\n'

    
    myString += 'Region ID,Region Name,Zone ID,Zone Name,Area ID,Area Name,Total Rx,Brand Presence' + '\n'
    
    gTotal=0;gTotal1=0;
    
    for i in range(len(recordList)):
        recordListStr=recordList[i] 
        
        level0=recordListStr['level0']
        level0_name=recordListStr['level0_name']
        level1=recordListStr['level1']
        level1_name=recordListStr['level1_name']
        level2=recordListStr['level2']
        level2_name=recordListStr['level2_name']
        totalRx=recordListStr['totalRx']
        brandPrecence=recordListStr['brandPrecence']
        
        gTotal+=recordListStr['totalRx']
        gTotal1+=recordListStr['brandPrecence']
        
        myString += str(level0) + ',' + str(level0_name) + ',' + str(level1) + ',' + str(level1_name)+ ',' + str(level2) + ',' + str(level2_name)+ ',' + str(totalRx) + ',' + str(brandPrecence) + '\n'
    
    myString += 'Total,,,,,,' + str(gTotal) + ',' + str(gTotal1) + '\n'

    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=prescription_seen_area_wise.csv'
    return str(myString)
    
def sum_area_wise1():
    cid=session.cid    
    med_division=request.vars.med_division
    
    if med_division=='PHARMA':
        response.title='Details Pharma'
    elif med_division=='SINAVISION':
        response.title='Details Sinavision'
    else:
        response.title = 'Area Wise'
        
    date_from=request.vars.date_from
    date_to=request.vars.date_to
        
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory    
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    pr_brand=request.vars.pr_brand
    
    if pr_region=='None':
        pr_region=''
    
    if pr_zone=='None':
        pr_zone=''
    
    if pr_area=='None':
        pr_area=''
    
    if pr_territory=='None':
        pr_territory=''
    
    if pr_brand=='None':
        pr_brand=''
    
    if pr_brand!='':
        pr_brand=str(pr_brand).replace("[","").replace(" ","").replace("]","")
    
    if pr_doctor=='None':
        pr_doctor=''
    
    if pr_ff=='None':
        pr_ff=''
    
    
    condition=''
    if pr_region != '':
        condition += " and a.level0 ='" + pr_region + "'"
    if pr_zone != '':
        condition += " and a.level1 ='" + pr_zone + "'"
    if pr_area != '':
        condition += " and a.level2 ='" + pr_area + "'"
    if pr_territory != '':
        condition += " and a.level_id ='" + pr_territory + "'"

    condition1=''
    if pr_brand != '':
        if len(str(pr_brand).split(','))>1:
            condition1 += " and b.medicine_id in (" + str(pr_brand) + ")"
        else:
            condition1 += " and b.medicine_id ='" + str(pr_brand) + "'"

#    if pr_doctor != '':
#        condition += " and b.doctor_id = '" + str(pr_doctor) + "'"
#    if med_generic != '':
#        condition += " and b.generic = '" + str(med_generic)+ "'"

    
    recordList=[]
    sql1 = "(SELECT a.level0 as level0,a.level0_name as level0_name,a.level1 as level1,a.level1_name as level1_name,a.level2 as level2,a.level2_name as level2_name,count(b.sl) as totalRx,0 as brandPrecence FROM `sm_level` a,`sm_prescription_seen_head` b WHERE  b.cid='" + cid + "' and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0,a.level1,a.level2 )"
    sql2 = "(SELECT a.level0 as level0,a.level0_name as level0_name,a.level1 as level1,a.level1_name as level1_name,a.level2 as level2,a.level2_name as level2_name,0 as totalRx,count(distinct(b.sl)) as brandPrecence FROM `sm_level` a,`sm_prescription_seen_details` b WHERE  b.cid='" + cid + "' and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' " + str(condition1) + " and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0,a.level1,a.level2)"
    
    records = "select level0,level0_name,level1,level1_name,level2,level2_name,sum(totalRx) as totalRx,sum(brandPrecence) as brandPrecence from (" + sql1 + " union all " + sql2 + ") p group by level0,level1,level2 order by level0,level1,level2"
    recordList = db.executesql(records, as_dict=True)
      
    
    reg_name=''
    regionRows=db((db.sm_level.cid==cid)&(db.sm_level.level_id==pr_region)).select(db.sm_level.level_name,limitby=(0,1))
    if regionRows:
        reg_name=regionRows[0].level_name
    
    return dict(recordList=recordList,med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,reg_name=reg_name,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,pr_brand=pr_brand)

def sum_zone_wise_d():
    cid=session.cid    
    med_division=request.vars.med_division
    
    if med_division=='PHARMA':
        response.title='Details Pharma'
    elif med_division=='SINAVISION':
        response.title='Details Sinavision'
    else:
        response.title = 'Zone Wise'
        
    date_from=request.vars.date_from
    date_to=request.vars.date_to
        
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory    
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    pr_brand=request.vars.pr_brand
    
    if pr_region=='None':
        pr_region=''
    
    if pr_zone=='None':
        pr_zone=''
    
    if pr_area=='None':
        pr_area=''
    
    if pr_territory=='None':
        pr_territory=''
    
    if pr_brand=='None':
        pr_brand=''
    
    if pr_brand!='':
        pr_brand=str(pr_brand).replace("[","").replace(" ","").replace("]","")
    
    if pr_doctor=='None':
        pr_doctor=''
    
    if pr_ff=='None':
        pr_ff=''
    
    
    condition=''
    if pr_region != '':
        condition += " and a.level0 ='" + pr_region + "'"
    if pr_zone != '':
        condition += " and a.level1 ='" + pr_zone + "'"
    if pr_area != '':
        condition += " and a.level2 ='" + pr_area + "'"
    if pr_territory != '':
        condition += " and a.level_id ='" + pr_territory + "'"

    condition1=''
    if pr_brand != '':
        if len(str(pr_brand).split(','))>1:
            condition1 += " and b.medicine_id in (" + str(pr_brand) + ")"
        else:
            condition1 += " and b.medicine_id ='" + str(pr_brand) + "'"

#    if pr_doctor != '':
#        condition += " and b.doctor_id = '" + str(pr_doctor) + "'"
#    if med_generic != '':
#        condition += " and b.generic = '" + str(med_generic)+ "'"

    
    recordList=[]
    sql1 = "(SELECT a.level0 as level0,a.level0_name as level0_name,a.level1 as level1,a.level1_name as level1_name,count(b.sl) as totalRx,0 as brandPrecence FROM `sm_level` a,`sm_prescription_seen_head` b WHERE  b.cid='" + cid + "' and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0,a.level1 )"
    sql2 = "(SELECT a.level0 as level0,a.level0_name as level0_name,a.level1 as level1,a.level1_name as level1_name,0 as totalRx,count(distinct(b.sl)) as brandPrecence FROM `sm_level` a,`sm_prescription_seen_details` b WHERE  b.cid='" + cid + "' and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' " + str(condition1) + " and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0,a.level1)"
    
    records = "select level0,level0_name,level1,level1_name,sum(totalRx) as totalRx,sum(brandPrecence) as brandPrecence from (" + sql1 + " union all " + sql2 + ") p group by level0,level1 order by level0,level1"
    recordList = db.executesql(records, as_dict=True)
      
    
    reg_name=''
    regionRows=db((db.sm_level.cid==cid)&(db.sm_level.level_id==pr_region)).select(db.sm_level.level_name,limitby=(0,1))
    if regionRows:
        reg_name=regionRows[0].level_name
    
    if pr_brand!='':
        pr_brand=str(pr_brand).replace("','","; ").replace("'","")
    else:
        pr_brand='ALL'
        
    myString = 'Prescription Summary Zone Wise (Seen) \n'
    myString += 'Date Range:' + ',' + str(date_from) + ' To ' + str(date_to) + '\n'
    myString += 'Zone:' + ',' + str(pr_region) + '\n'
    myString += 'Region:' + ',' + str(pr_zone) + '\n'
    myString += 'Area:' + ',' + str(pr_area) + '\n'
    myString += 'Territory:' + ',' + str(pr_territory) + '\n'
    myString += 'Brand:' + ',' + str(pr_brand) + '\n\n'

    
    myString += 'Region ID,Region Name,Zone ID,Zone Name,Total Rx,Brand Presence' + '\n'
    
    gTotal=0;gTotal1=0;
    
    for i in range(len(recordList)):
        recordListStr=recordList[i] 
        
        level0=recordListStr['level0']
        level0_name=recordListStr['level0_name']
        level1=recordListStr['level1']
        level1_name=recordListStr['level1_name']
        totalRx=recordListStr['totalRx']
        brandPrecence=recordListStr['brandPrecence']
        
        gTotal+=recordListStr['totalRx']
        gTotal1+=recordListStr['brandPrecence']
        
        myString += str(level0) + ',' + str(level0_name) + ',' + str(level1) + ',' + str(level1_name)+ ',' + str(totalRx) + ',' + str(brandPrecence) + '\n'
    
    myString += 'Total,,,,' + str(gTotal) + ',' + str(gTotal1) + '\n'

    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=prescription_seen_zone_wise.csv'
    return str(myString)
    
def sum_zone_wise():
    cid=session.cid    
    med_division=request.vars.med_division
    
    if med_division=='PHARMA':
        response.title='Details Pharma'
    elif med_division=='SINAVISION':
        response.title='Details Sinavision'
    else:
        response.title = 'Zone Wise'
        
    date_from=request.vars.date_from
    date_to=request.vars.date_to
        
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory    
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    pr_brand=request.vars.pr_brand
    
    if pr_region=='None':
        pr_region=''
    
    if pr_zone=='None':
        pr_zone=''
    
    if pr_area=='None':
        pr_area=''
    
    if pr_territory=='None':
        pr_territory=''
    
    if pr_brand=='None':
        pr_brand=''
    
    if pr_brand!='':
        pr_brand=str(pr_brand).replace("[","").replace(" ","").replace("]","")
    
    if pr_doctor=='None':
        pr_doctor=''
    
    if pr_ff=='None':
        pr_ff=''
    
    
    condition=''
    if pr_region != '':
        condition += " and a.level0 ='" + pr_region + "'"
    if pr_zone != '':
        condition += " and a.level1 ='" + pr_zone + "'"
    if pr_area != '':
        condition += " and a.level2 ='" + pr_area + "'"
    if pr_territory != '':
        condition += " and a.level_id ='" + pr_territory + "'"

    condition1=''
    if pr_brand != '':
        if len(str(pr_brand).split(','))>1:
            condition1 += " and b.medicine_id in (" + str(pr_brand) + ")"
        else:
            condition1 += " and b.medicine_id ='" + str(pr_brand) + "'"

#    if pr_doctor != '':
#        condition += " and b.doctor_id = '" + str(pr_doctor) + "'"
#    if med_generic != '':
#        condition += " and b.generic = '" + str(med_generic)+ "'"

    
    recordList=[]
    sql1 = "(SELECT a.level0 as level0,a.level0_name as level0_name,a.level1 as level1,a.level1_name as level1_name,count(b.sl) as totalRx,0 as brandPrecence FROM `sm_level` a,`sm_prescription_seen_head` b WHERE  b.cid='" + cid + "' and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0,a.level1 )"
    sql2 = "(SELECT a.level0 as level0,a.level0_name as level0_name,a.level1 as level1,a.level1_name as level1_name,0 as totalRx,count(distinct(b.sl)) as brandPrecence FROM `sm_level` a,`sm_prescription_seen_details` b WHERE  b.cid='" + cid + "' and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' " + str(condition1) + " and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0,a.level1)"
    
    records = "select level0,level0_name,level1,level1_name,sum(totalRx) as totalRx,sum(brandPrecence) as brandPrecence from (" + sql1 + " union all " + sql2 + ") p group by level0,level1 order by level0,level1"
    recordList = db.executesql(records, as_dict=True)
      
    
    reg_name=''
    regionRows=db((db.sm_level.cid==cid)&(db.sm_level.level_id==pr_region)).select(db.sm_level.level_name,limitby=(0,1))
    if regionRows:
        reg_name=regionRows[0].level_name
    
    return dict(recordList=recordList,med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,reg_name=reg_name,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,pr_brand=pr_brand)


def sum_reg_wise_d():
    cid=session.cid    
    med_division=request.vars.med_division
    
    if med_division=='PHARMA':
        response.title='Details Pharma'
    elif med_division=='SINAVISION':
        response.title='Details Sinavision'
    else:
        response.title = 'Region Wise'
        
    date_from=request.vars.date_from
    date_to=request.vars.date_to
        
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory    
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    pr_brand=request.vars.pr_brand
     
    if pr_region=='None':
        pr_region=''
    
    if pr_zone=='None':
        pr_zone=''
    
    if pr_area=='None':
        pr_area=''
    
    if pr_territory=='None':
        pr_territory=''
    
    if pr_brand=='None':
        pr_brand=''
    
    if pr_brand!='':
        pr_brand=str(pr_brand).replace("[","").replace(" ","").replace("]","")

       
    
    if pr_doctor=='None':
        pr_doctor=''
    
    if pr_ff=='None':
        pr_ff=''
    
    
    condition=''
    if pr_region != '':
        condition += " and a.level0 ='" + pr_region + "'"
    if pr_zone != '':
        condition += " and a.level1 ='" + pr_zone + "'"
    if pr_area != '':
        condition += " and a.level2 ='" + pr_area + "'"
    if pr_territory != '':
        condition += " and a.level_id ='" + pr_territory + "'"
    
    condition1=''
    if pr_brand != '':
        if len(str(pr_brand).split(','))>1:
            condition1 += " and b.medicine_id in (" + str(pr_brand) + ")"
        else:
            condition1 += " and b.medicine_id ='" + str(pr_brand) + "'"

#    if pr_doctor != '':
#        condition += " and b.doctor_id = '" + str(pr_doctor) + "'"
#    if med_generic != '':
#        condition += " and b.generic = '" + str(med_generic)+ "'"

    
    recordList=[]
    sql1 = "(SELECT a.level0 as level0,a.level0_name as level0_name,count(b.sl) as totalRx,0 as brandPrecence FROM `sm_level` a,`sm_prescription_seen_head` b WHERE  b.cid='" + cid + "' and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0 order by a.level0)"
    sql2 = "(SELECT a.level0 as level0,a.level0_name as level0_name,0 as totalRx,count(distinct(b.sl)) as brandPrecence FROM `sm_level` a,`sm_prescription_seen_details` b WHERE  b.cid='" + cid + "' and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' " + str(condition1) + " and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0 order by a.level0)"
    
    records = "select level0,level0_name,sum(totalRx) as totalRx,sum(brandPrecence) as brandPrecence from (" + sql1 + " union all " + sql2 + ") p group by level0 order by level0"
    recordList = db.executesql(records, as_dict=True)
      
    
    reg_name=''
    regionRows=db((db.sm_level.cid==cid)&(db.sm_level.level_id==pr_region)).select(db.sm_level.level_name,limitby=(0,1))
    if regionRows:
        reg_name=regionRows[0].level_name
    
    if pr_brand!='':
        pr_brand=str(pr_brand).replace("','","; ").replace("'","")
    else:
        pr_brand='ALL'
        
    myString = 'Prescription Summary Region Wise (Seen) \n'
    myString += 'Date Range:' + ',' + str(date_from) + ' To ' + str(date_to) + '\n'
    myString += 'Zone:' + ',' + str(pr_region) + '\n'
    myString += 'Region:' + ',' + str(pr_zone) + '\n'
    myString += 'Area:' + ',' + str(pr_area) + '\n'
    myString += 'Territory:' + ',' + str(pr_territory) + '\n'
    myString += 'Brand:' + ',' + str(pr_brand) + '\n\n'

    
    myString += 'Region ID,Region Name,Total Rx,Brand Presence' + '\n'
    
    gTotal=0;gTotal1=0;
    
    for i in range(len(recordList)):
        recordListStr=recordList[i] 
        
        level0=recordListStr['level0']
        level0_name=recordListStr['level0_name']
        totalRx=recordListStr['totalRx']
        brandPrecence=recordListStr['brandPrecence']
        
        gTotal+=recordListStr['totalRx']
        gTotal1+=recordListStr['brandPrecence']
        
        myString += str(level0) + ',' + str(level0_name)+ ',' + str(totalRx) + ',' + str(brandPrecence) + '\n'
    
    myString += 'Total,,' + str(gTotal) + ',' + str(gTotal1) + '\n'

    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=prescription_seen_region_wise.csv'
    return str(myString)
    
def sum_reg_wise():
    cid=session.cid    
    med_division=request.vars.med_division
    
    if med_division=='PHARMA':
        response.title='Details Pharma'
    elif med_division=='SINAVISION':
        response.title='Details Sinavision'
    else:
        response.title = 'Region Wise'
        
    date_from=request.vars.date_from
    date_to=request.vars.date_to
        
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory    
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    pr_brand=request.vars.pr_brand
     
    if pr_region=='None':
        pr_region=''
    
    if pr_zone=='None':
        pr_zone=''
    
    if pr_area=='None':
        pr_area=''
    
    if pr_territory=='None':
        pr_territory=''
    
    if pr_brand=='None':
        pr_brand=''
    
    if pr_brand!='':
        pr_brand=str(pr_brand).replace("[","").replace(" ","").replace("]","")

       
    
    if pr_doctor=='None':
        pr_doctor=''
    
    if pr_ff=='None':
        pr_ff=''
    
    
    condition=''
    if pr_region != '':
        condition += " and a.level0 ='" + pr_region + "'"
    if pr_zone != '':
        condition += " and a.level1 ='" + pr_zone + "'"
    if pr_area != '':
        condition += " and a.level2 ='" + pr_area + "'"
    if pr_territory != '':
        condition += " and a.level_id ='" + pr_territory + "'"
    
    condition1=''
    if pr_brand != '':
        if len(str(pr_brand).split(','))>1:
            condition1 += " and b.medicine_id in (" + str(pr_brand) + ")"
        else:
            condition1 += " and b.medicine_id ='" + str(pr_brand) + "'"

#    if pr_doctor != '':
#        condition += " and b.doctor_id = '" + str(pr_doctor) + "'"
#    if med_generic != '':
#        condition += " and b.generic = '" + str(med_generic)+ "'"

    
    recordList=[]
    sql1 = "(SELECT a.level0 as level0,a.level0_name as level0_name,count(b.sl) as totalRx,0 as brandPrecence FROM `sm_level` a,`sm_prescription_seen_head` b WHERE  b.cid='" + cid + "' and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0 order by a.level0)"
    sql2 = "(SELECT a.level0 as level0,a.level0_name as level0_name,0 as totalRx,count(distinct(b.sl)) as brandPrecence FROM `sm_level` a,`sm_prescription_seen_details` b WHERE  b.cid='" + cid + "' and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' " + str(condition1) + " and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0 order by a.level0)"
    
    records = "select level0,level0_name,sum(totalRx) as totalRx,sum(brandPrecence) as brandPrecence from (" + sql1 + " union all " + sql2 + ") p group by level0 order by level0"
    recordList = db.executesql(records, as_dict=True)
      
    
    reg_name=''
    regionRows=db((db.sm_level.cid==cid)&(db.sm_level.level_id==pr_region)).select(db.sm_level.level_name,limitby=(0,1))
    if regionRows:
        reg_name=regionRows[0].level_name
    
    return dict(recordList=recordList,med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,reg_name=reg_name,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,pr_brand=pr_brand)


def sum_area_wise():
    cid=session.cid    
    med_division=request.vars.med_division
    
    if med_division=='PHARMA':
        response.title='Details Pharma'
    elif med_division=='SINAVISION':
        response.title='Details Sinavision'
    else:
        response.title = 'Details ALL'
        
    date_from=request.vars.date_from
    date_to=request.vars.date_to
        
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    
    if pr_region=='None':
        pr_region=''
    
    if pr_zone=='None':
        pr_zone=''
    
    if pr_area=='None':
        pr_area=''
    
    if pr_territory=='None':
        pr_territory=''
    
    if pr_doctor=='None':
        pr_doctor=''
    
    if pr_ff=='None':
        pr_ff=''

    area_id_list=[]
    qset = db()
    qset = qset(db.sm_level.cid == cid)
    qset = qset(db.sm_level.depth == 3)

    if pr_region != '':
        qset = qset(db.sm_level.level0 == pr_region)
    if pr_zone != '':
        qset = qset(db.sm_level.level1 == pr_zone)
    if pr_area != '':
        qset = qset(db.sm_level.level2 == pr_area)
    if pr_territory != '':
        qset = qset(db.sm_level.level_id == pr_territory)

    levelRows = qset.select(db.sm_level.level_id,orderby=db.sm_level.level_id)

    for row in levelRows:
        area_id_list.append(row.level_id)

    qset1 = db()
    qset1 = qset1(db.sm_prescription_head.cid == cid)
    qset1 = qset1(db.sm_prescription_head.submit_date >= date_from)
    qset1 = qset1(db.sm_prescription_head.submit_date <= date_to)
    qset1 = qset1(db.sm_prescription_head.area_id.belongs(area_id_list))

    if pr_ff!='':
        qset1 = qset1(db.sm_prescription_head.submit_by_id == pr_ff)
    if pr_doctor!='':
        qset1 = qset1(db.sm_prescription_head.doctor_id == pr_doctor)

    # if med_division=='PHARMA':
    #     qset=qset((db.sm_prescription_head.update_med_count_flag >0)|(db.sm_prescription_head.update_med_count_flag_snv >0))
    # elif med_division=='SINAVISION':
    #     qset=qset(db.sm_prescription_head.update_med_count_flag_snv >0)

    records=qset1.select(db.sm_prescription_head.submit_by_id,db.sm_prescription_head.submit_by_name,db.sm_prescription_head.area_id,db.sm_prescription_head.area_name,db.sm_prescription_head.doctor_id,db.sm_prescription_head.doctor_name,db.sm_prescription_head.id.count(), orderby=db.sm_prescription_head.area_id|db.sm_prescription_head.submit_by_id|db.sm_prescription_head.doctor_id,groupby=db.sm_prescription_head.area_id|db.sm_prescription_head.submit_by_id|db.sm_prescription_head.doctor_id)


    reg_name=''
    regionRows=db((db.sm_level.cid==cid)&(db.sm_level.level_id==pr_region)).select(db.sm_level.level_name,limitby=(0,1))
    if regionRows:
        reg_name=regionRows[0].level_name
    
    return dict(records=records,med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,reg_name=reg_name,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)




def sum_day_wise():
    cid=session.cid    
    med_division=request.vars.med_division
    
    if med_division=='PHARMA':
        response.title='Details Pharma'
    elif med_division=='SINAVISION':
        response.title='Details Sinavision'
    else:
        response.title = 'Details ALL'
        
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    
        
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    
    if pr_region=='None':
        pr_region=''
    
    if pr_zone=='None':
        pr_zone=''
    
    if pr_area=='None':
        pr_area=''
    
    if pr_territory=='None':
        pr_territory=''
    
    if pr_doctor=='None':
        pr_doctor=''
    
    if pr_ff=='None':
        pr_ff=''

    area_id_list=[]
    qset = db()
    qset = qset(db.sm_level.cid == cid)
    qset = qset(db.sm_level.depth == 3)

    if pr_region != '':
        qset = qset(db.sm_level.level0 == pr_region)
    if pr_zone != '':
        qset = qset(db.sm_level.level1 == pr_zone)
    if pr_area != '':
        qset = qset(db.sm_level.level2 == pr_area)
    if pr_territory != '':
        qset = qset(db.sm_level.level_id == pr_territory)

    levelRows = qset.select(db.sm_level.level_id,orderby=db.sm_level.level_id)

    for row in levelRows:
        area_id_list.append(row.level_id)



    qset1=db()
    qset1=qset1(db.sm_prescription_head.cid == cid)
    qset1 = qset1(db.sm_prescription_head.submit_date >= date_from)
    qset1 = qset1(db.sm_prescription_head.submit_date <= date_to)

    if len(area_id_list)>0:
        qset1 = qset1(db.sm_prescription_head.area_id.belongs(area_id_list))

    if pr_ff!='':
        qset1=qset1(db.sm_prescription_head.submit_by_id == pr_ff)
    if pr_doctor!='':
        qset1=qset1(db.sm_prescription_head.doctor_id == pr_doctor)

    # if med_division=='PHARMA':
    #     qset=qset((db.sm_prescription_head.update_med_count_flag >0)|(db.sm_prescription_head.update_med_count_flag_snv >0))
    # elif med_division=='SINAVISION':
    #     qset=qset(db.sm_prescription_head.update_med_count_flag_snv >0)
    
        
    records=qset1.select(db.sm_prescription_head.submit_date,db.sm_prescription_head.id.count(), orderby=~db.sm_prescription_head.submit_date,groupby=db.sm_prescription_head.submit_date)

    reg_name=''
    regionRows=db((db.sm_level.cid==cid)&(db.sm_level.level_id==pr_region)).select(db.sm_level.level_name,limitby=(0,1))
    if regionRows:
        reg_name=regionRows[0].level_name
        
    return dict(records=records,med_division=med_division,date_from=date_from,date_to=date_to,pr_region=pr_region,reg_name=reg_name,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff)

# block 3
def pr_summary():
    cid=session.cid    
    med_division=request.vars.med_division
    
    if med_division=='PHARMA':
        response.title='Summary Pharma'
    elif med_division=='SINAVISION':
        response.title='Summary Sinavision'
        
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    
    if pr_region=='None':
        pr_region=''
    
    if pr_zone=='None':
        pr_zone=''
    
    if pr_area=='None':
        pr_area=''
    
    if pr_territory=='None':
        pr_territory=''
    
    if pr_doctor=='None':
        pr_doctor=''
    
    if pr_ff=='None':
        pr_ff=''
        
    if med_generic=='None':
        med_generic=''

    qset = db()
    qset = qset(db.sm_level.cid == cid)
    qset = qset(db.sm_level.depth == 3)
    qset = qset(db.sm_prescription_details.cid == cid)
    qset = qset(db.sm_prescription_details.update_flag == 2)
    qset = qset(db.sm_prescription_details.submit_date >= date_from)
    qset = qset(db.sm_prescription_details.submit_date <= date_to)
    qset = qset(db.sm_prescription_details.area_id == db.sm_level.level_id)

    if pr_region != '':
        qset = qset(db.sm_level.level0 == pr_region)
    if pr_zone != '':
        qset = qset(db.sm_level.level1 == pr_zone)
    if pr_area != '':
        qset = qset(db.sm_level.level2 == pr_area)
    if pr_territory != '':
        qset = qset(db.sm_level.level_id == pr_territory)

    if pr_ff != '':
        qset = qset(db.sm_prescription_details.submit_by_id == pr_ff)
    if pr_doctor != '':
        qset = qset(db.sm_prescription_details.doctor_id == pr_doctor)
    if med_generic != '':
        qset = qset(db.sm_prescription_details.generic == med_generic)

    if med_division == 'PHARMA':
        qset = qset(db.sm_prescription_details.dept != 'NMD')
    elif med_division == 'SINAVISION':
        qset = qset(db.sm_prescription_details.dept != 'SV')

    
    records=qset.select(db.sm_level.level_id,db.sm_level.level_name,db.sm_level.level2,db.sm_level.level2_name,db.sm_level.level1,db.sm_level.level0,db.sm_prescription_details.submit_date,db.sm_prescription_details.doctor_id,db.sm_prescription_details.doctor_name,db.sm_prescription_details.medicine_id,db.sm_prescription_details.medicine_name,db.sm_prescription_details.brand,db.sm_prescription_details.generic,db.sm_prescription_details.strength,db.sm_prescription_details.formation,db.sm_prescription_details.company,db.sm_prescription_details.id.count(),groupby=db.sm_prescription_details.doctor_id|db.sm_prescription_details.doctor_name|db.sm_prescription_details.area_id|db.sm_prescription_details.company|db.sm_prescription_details.brand,orderby=~db.sm_prescription_details.submit_date|db.sm_prescription_details.doctor_id|db.sm_prescription_details.doctor_name|db.sm_prescription_details.area_id|db.sm_prescription_details.company|db.sm_prescription_details.brand)

    doctor_id_list=[]
    for row in records:
        doctor_id=row[db.sm_prescription_details.doctor_id]

        if doctor_id=='0':continue
        if doctor_id not in doctor_id_list:
            doctor_id_list.append(doctor_id)

    doctorRows=db((db.sm_doctor.cid==cid)&(db.sm_doctor.doc_id.belongs(doctor_id_list))).select(db.sm_doctor.doc_id,db.sm_doctor.degree,db.sm_doctor.specialty)

    level3List = []
    for row in records:
        level3_id = row[db.sm_level.level_id]
        if level3_id not in level3List:
            level3List.append(level3_id)

    levelUserList = []
    for j in range(len(level3List)):
        level3_id = level3List[j]

        level3_rep = ''
        level3_rep_s = ''

        dicData={}
        if med_division == 'PHARMA':
            qset = db()
            qset = qset(db.sm_rep_area.area_id == level3_id)
            repRows = qset(db.sm_rep_area.rep_category == 'A').select(db.sm_rep_area.rep_name, orderby=db.sm_rep_area.rep_name)
            for rRow in repRows:
                if level3_rep == '':
                    level3_rep = str(rRow.rep_name)
                else:
                    level3_rep += ',' + str(rRow.rep_name)

            repRows1 = qset(db.sm_rep_area.rep_category == 'C').select(db.sm_rep_area.rep_name,orderby=db.sm_rep_area.rep_name)
            for rRow in repRows1:
                if level3_rep_s == '':
                    level3_rep_s = str(rRow.rep_name)
                else:
                    level3_rep_s += ',' + str(rRow.rep_name)

            levelRows = db((db.sm_level.cid == cid) & (db.sm_level.level_id == level3_id)).select(db.sm_level.level0,db.sm_level.level1,db.sm_level.level2,limitby=(0, 1))

            level0_sup = ''
            level1_sup = ''
            level2_sup = ''

            level0_sup_s = ''
            level1_sup_s = ''
            level2_sup_s = ''

            if levelRows:
                level0_id = str(levelRows[0].level0)
                level1_id = str(levelRows[0].level1)
                level2_id = str(levelRows[0].level2)

                supRow0 = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.level_id == level0_id) & (db.sm_supervisor_level.level_depth_no == 0)).select(db.sm_supervisor_level.sup_name,orderby=db.sm_supervisor_level.sup_name)
                for sRow0 in supRow0:
                    if level0_sup == '':
                        level0_sup = str(sRow0.sup_name)
                    else:
                        level0_sup += ',' + str(sRow0.sup_name)

                supRow1 = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.level_id == level1_id) & (db.sm_supervisor_level.level_depth_no == 1)).select(db.sm_supervisor_level.sup_name,orderby=db.sm_supervisor_level.sup_name)
                for sRow1 in supRow1:
                    if level1_sup == '':
                        level1_sup = str(sRow1.sup_name)
                    else:
                        level1_sup += ',' + str(sRow1.sup_name)

                supRow2 = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.level_id == level2_id) & (db.sm_supervisor_level.level_depth_no == 2)).select(db.sm_supervisor_level.sup_name,orderby=db.sm_supervisor_level.sup_name)
                for sRow in supRow2:
                    if level2_sup == '':
                        level2_sup = str(sRow.sup_name)
                    else:
                        level2_sup += ',' + str(sRow.sup_name)

                # Sinavision
                supRow0_s = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.level_id == level0_id) & (db.sm_supervisor_level.level_depth_no == 0)& (db.sm_rep.user_type == 'sup')&(db.sm_rep.note == 'SIN') & (db.sm_rep.status == 'ACTIVE')&(db.sm_rep.rep_id == db.sm_supervisor_level.sup_id)).select(db.sm_supervisor_level.sup_name,orderby=db.sm_supervisor_level.sup_name)
                for sRow0 in supRow0_s:
                    if level0_sup_s == '':
                        level0_sup_s = str(sRow0.sup_name)
                    else:
                        level0_sup_s += ',' + str(sRow0.sup_name)

                supRow1_s = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.level_id == level1_id) & (db.sm_supervisor_level.level_depth_no == 1) & (db.sm_rep.user_type == 'sup')&(db.sm_rep.note == 'SIN') & (db.sm_rep.status == 'ACTIVE') & (db.sm_rep.rep_id == db.sm_supervisor_level.sup_id)).select(db.sm_supervisor_level.sup_name, orderby=db.sm_supervisor_level.sup_name)
                for sRow1 in supRow1_s:
                    if level1_sup_s == '':
                        level1_sup_s = str(sRow1.sup_name)
                    else:
                        level1_sup_s += ',' + str(sRow1.sup_name)

                supRow2_s = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.level_id == level2_id) & (db.sm_supervisor_level.level_depth_no == 2) & (db.sm_rep.cid == cid)& (db.sm_rep.user_type == 'sup')&(db.sm_rep.note == 'SIN') & (db.sm_rep.status == 'ACTIVE') & (db.sm_rep.rep_id == db.sm_supervisor_level.sup_id)).select(db.sm_supervisor_level.sup_name, orderby=db.sm_supervisor_level.sup_name)

                for sRow2 in supRow2_s:
                    if level2_sup_s == '':
                        level2_sup_s = str(sRow2.sup_name)
                    else:
                        level2_sup_s += ',' + str(sRow2.sup_name)

            dicData = {'level3_id': level3_id, 'level3_rep': level3_rep,'level3_rep_s':level3_rep_s, 'level2_id': level2_id, 'level2_sup': level2_sup,'level2_sup_s':level2_sup_s,'level1_id': level1_id, 'level1_sup': level1_sup,'level1_sup_s':level1_sup_s, 'level0_id': level0_id, 'level0_sup': level0_sup,'level0_sup_s':level0_sup_s}

        elif med_division == 'SINAVISION':
            qset = db()
            qset = qset(db.sm_rep_area.area_id == level3_id)
            repRows1 = qset(db.sm_rep_area.rep_category == 'C').select(db.sm_rep_area.rep_name,orderby=db.sm_rep_area.rep_name)
            for rRow in repRows1:
                if level3_rep_s == '':
                    level3_rep_s = str(rRow.rep_name)
                else:
                    level3_rep_s += ',' + str(rRow.rep_name)

            levelRows = db((db.sm_level.cid == cid) & (db.sm_level.level_id == level3_id)).select(db.sm_level.level0,db.sm_level.level1,db.sm_level.level2,limitby=(0, 1))

            level0_sup_s = ''
            level1_sup_s = ''
            level2_sup_s = ''

            if levelRows:
                level0_id = str(levelRows[0].level0)
                level1_id = str(levelRows[0].level1)
                level2_id = str(levelRows[0].level2)

                # Sinavision
                level0_sup_s = ''
                level1_sup_s = ''
                level2_sup_s = ''
                supRow0_s = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.level_id == level0_id) & (db.sm_supervisor_level.level_depth_no == 0) & (db.sm_rep.user_type == 'sup') & (db.sm_rep.note == 'SIN') & (db.sm_rep.status == 'ACTIVE') & (db.sm_rep.rep_id == db.sm_supervisor_level.sup_id)).select(db.sm_supervisor_level.sup_name, orderby=db.sm_supervisor_level.sup_name)
                for sRow0 in supRow0_s:
                    if level0_sup_s == '':
                        level0_sup_s = str(sRow0.sup_name)
                    else:
                        level0_sup_s += ',' + str(sRow0.sup_name)

                supRow1_s = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.level_id == level1_id) & (db.sm_supervisor_level.level_depth_no == 1) & (db.sm_rep.user_type == 'sup') & (db.sm_rep.note == 'SIN') & (db.sm_rep.status == 'ACTIVE') & (db.sm_rep.rep_id == db.sm_supervisor_level.sup_id)).select(db.sm_supervisor_level.sup_name, orderby=db.sm_supervisor_level.sup_name)
                for sRow1 in supRow1_s:
                    if level1_sup_s == '':
                        level1_sup_s = str(sRow1.sup_name)
                    else:
                        level1_sup_s += ',' + str(sRow1.sup_name)

                supRow2_s = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.level_id == level2_id) & (db.sm_supervisor_level.level_depth_no == 2) & (db.sm_rep.cid == cid) & (db.sm_rep.user_type == 'sup') & (db.sm_rep.note == 'SIN') & (db.sm_rep.status == 'ACTIVE') & (db.sm_rep.rep_id == db.sm_supervisor_level.sup_id)).select(db.sm_supervisor_level.sup_name, orderby=db.sm_supervisor_level.sup_name)

                for sRow2 in supRow2_s:
                    if level2_sup_s == '':
                        level2_sup_s = str(sRow2.sup_name)
                    else:
                        level2_sup_s += ',' + str(sRow2.sup_name)

            dicData = {'level3_id': level3_id, 'level3_rep': level3_rep, 'level3_rep_s': level3_rep_s,'level2_id': level2_id, 'level2_sup': '', 'level2_sup_s': level2_sup_s,'level1_id': level1_id, 'level1_sup': '', 'level1_sup_s': level1_sup_s,'level0_id': level0_id, 'level0_sup': '', 'level0_sup_s': level0_sup_s}

        levelUserList.append(dicData)


    reg_name=''
    regionRows=db((db.sm_level.cid==cid)&(db.sm_level.level_id==pr_region)).select(db.sm_level.level_name,limitby=(0,1))
    if regionRows:
        reg_name=regionRows[0].level_name
      
    return dict(med_division=med_division,records=records,doctorRows=doctorRows,levelUserList=levelUserList,reg_name=reg_name,date_from=date_from,date_to=date_to,pr_region=pr_region,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,pr_ff=pr_ff,med_generic=med_generic)


def pr_details_d():
    cid=session.cid    
    med_division=request.vars.med_division
    
    if med_division=='PHARMA':
        response.title='Details Pharma'
    elif med_division=='SINAVISION':
        response.title='Details Sinavision'
        
    date_from=request.vars.date_from
    date_to=request.vars.date_to
        
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    
    if pr_region=='None':
        pr_region=''

    if pr_zone=='None':
        pr_zone=''

    if pr_area=='None':
        pr_area=''

    if pr_territory=='None':
        pr_territory=''

    if pr_doctor=='None':
        pr_doctor=''

    if pr_ff=='None':
        pr_ff=''

    if med_generic=='None':
        med_generic=''


    qset = db()
    qset = qset(db.sm_level.cid == cid)
    qset = qset(db.sm_level.depth == 3)
    qset = qset(db.sm_prescription_details.cid == cid)
    qset = qset(db.sm_prescription_details.update_flag == 2)
    qset = qset(db.sm_prescription_details.submit_date >= date_from)
    qset = qset(db.sm_prescription_details.submit_date <= date_to)
    qset = qset(db.sm_prescription_details.area_id == db.sm_level.level_id)

    if pr_region != '':
        qset = qset(db.sm_level.level0 == pr_region)
    if pr_zone != '':
        qset = qset(db.sm_level.level1 == pr_zone)
    if pr_area != '':
        qset = qset(db.sm_level.level2 == pr_area)
    if pr_territory != '':
        qset = qset(db.sm_level.level_id == pr_territory)

    if pr_ff != '':
        qset = qset(db.sm_prescription_details.submit_by_id == pr_ff)
    if pr_doctor != '':
        qset = qset(db.sm_prescription_details.doctor_id == pr_doctor)
    if med_generic != '':
        qset = qset(db.sm_prescription_details.generic == med_generic)

    if med_division == 'PHARMA':
        qset = qset(db.sm_prescription_details.dept != 'NMD')
    elif med_division == 'SINAVISION':
        qset = qset(db.sm_prescription_details.dept != 'SV')

    records = qset.select(db.sm_prescription_details.sl, db.sm_prescription_details.submit_date, db.sm_level.level1,
                          db.sm_level.level1_name, db.sm_level.level2, db.sm_prescription_details.submit_by_id,
                          db.sm_prescription_details.submit_by_name, db.sm_level.level_id, db.sm_level.level_name,
                          db.sm_prescription_details.doctor_id, db.sm_prescription_details.doctor_name,
                          db.sm_prescription_details.medicine_id, db.sm_prescription_details.medicine_name,
                          db.sm_prescription_details.brand, db.sm_prescription_details.generic,
                          db.sm_prescription_details.strength, db.sm_prescription_details.formation,
                          db.sm_prescription_details.company,
                          orderby=~db.sm_prescription_details.submit_date|db.sm_prescription_details.area_id | db.sm_prescription_details.submit_by_id | db.sm_prescription_details.doctor_id | ~db.sm_prescription_details.sl)

    if pr_region == '':
        pr_region = 'National'

    if pr_zone == '':
        pr_zone = 'ALL'

    if pr_area == 'None':
        pr_area = ''

    if pr_territory == 'None':
        pr_territory = ''

    if pr_doctor == 'None':
        pr_doctor = ''

    if pr_ff == 'None':
        pr_ff = ''

    if med_generic == 'None':
        med_generic = ''

    myString = 'Prescription Details ' + med_division + ' \n'
    myString += 'Date Range:' + ',' + str(date_from) + ' To ' + str(date_to) + '\n'
    myString += 'Zone:' + ',' + str(pr_region) + '\n'
    myString += 'Region:' + ',' + str(pr_zone) + '\n'
    myString += 'Area:' + ',' + str(pr_area) + '\n'
    myString += 'Territory:' + ',' + str(pr_territory) + '\n'
    myString += 'Field Force:' + ',' + str(pr_ff) + '\n'
    myString += 'Geniric:' + ',' + str(med_generic) + '\n'
    myString += 'Doctor:' + ',' + str(pr_doctor) + '\n'

    slNo = 0
    myString += 'SL,Date,Region,Territory id,Territory Name,Area Code,Submitted By id,Submitted By Name,Doctor Id,Doctor Name,pr.SL,Med. ID,Med. Name,Brand,Generic,Formation,Company' + '\n'

    for row in records:
        slNo += 1
        submit_date = row[db.sm_prescription_details.submit_date]
        reg_id = row[db.sm_level.level1]
        area_id = row[db.sm_level.level_id]
        area_name = row[db.sm_level.level_name]
        tl_id = row[db.sm_level.level2]
        submit_by_id = row[db.sm_prescription_details.submit_by_id]
        submit_by_name = row[db.sm_prescription_details.submit_by_name]
        doctor_id = row[db.sm_prescription_details.doctor_id]
        doctor_name = row[db.sm_prescription_details.doctor_name]
        sl = row[db.sm_prescription_details.sl]
        medicine_id = row[db.sm_prescription_details.medicine_id]
        medicine_name = row[db.sm_prescription_details.medicine_name]
        brand = row[db.sm_prescription_details.brand]
        generic = row[db.sm_prescription_details.generic]
        formation = row[db.sm_prescription_details.formation]
        company = row[db.sm_prescription_details.company]

        myString += str(slNo) + ',' + str(submit_date) + ',' + str(reg_id) + ',' + str(area_id) + ',' + str(
            area_name) + ',' + str(tl_id) + ',' + str(submit_by_id) + ',' + str(submit_by_name) + ',' + str(
            doctor_id) + ',' + str(doctor_name) + ',' + str(sl) + ',' + str(medicine_id) + ',' + str(
            medicine_name) + ',' + str(brand) + ',' + str(generic) + ',' + str(formation) + ',' + str(company) + '\n'

    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=prescription_details.csv'
    return str(myString)

def pr_details():
    cid=session.cid    
    med_division=request.vars.med_division
    
    if med_division=='PHARMA':
        response.title='Details Pharma'
    elif med_division=='SINAVISION':
        response.title='Details Sinavision'
        
    date_from=request.vars.date_from
    date_to=request.vars.date_to
    
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    
    if pr_region=='None':
        pr_region=''
    
    if pr_zone=='None':
        pr_zone=''
    
    if pr_area=='None':
        pr_area=''
    
    if pr_territory=='None':
        pr_territory=''
    
    if pr_doctor=='None':
        pr_doctor=''
    
    if pr_ff=='None':
        pr_ff=''
        
    if med_generic=='None':
        med_generic=''

    qset = db()
    qset = qset(db.sm_level.cid == cid)
    qset = qset(db.sm_level.depth == 3)
    qset = qset(db.sm_prescription_details.cid == cid)
    qset = qset(db.sm_prescription_details.update_flag == 2)
    qset = qset(db.sm_prescription_details.submit_date >= date_from)
    qset = qset(db.sm_prescription_details.submit_date <= date_to)
    qset = qset(db.sm_prescription_details.area_id == db.sm_level.level_id)

    if pr_region != '':
        qset = qset(db.sm_level.level0 == pr_region)
    if pr_zone != '':
        qset = qset(db.sm_level.level1 == pr_zone)
    if pr_area != '':
        qset = qset(db.sm_level.level2 == pr_area)
    if pr_territory != '':
        qset = qset(db.sm_level.level_id == pr_territory)

    if pr_ff!='':
        qset=qset(db.sm_prescription_details.submit_by_id == pr_ff)
    if pr_doctor!='':
        qset=qset(db.sm_prescription_details.doctor_id == pr_doctor)
    if med_generic!='':
        qset=qset(db.sm_prescription_details.generic == med_generic)
    
    if med_division=='PHARMA':
        qset=qset(db.sm_prescription_details.dept!='NMD')
    elif med_division=='SINAVISION':
        qset = qset(db.sm_prescription_details.dept != 'SV')
          
    records=qset.select(db.sm_prescription_details.sl,db.sm_prescription_details.submit_date,db.sm_level.level1,db.sm_level.level1_name,db.sm_level.level2,db.sm_prescription_details.submit_by_id,db.sm_prescription_details.submit_by_name,db.sm_level.level_id,db.sm_level.level_name,db.sm_prescription_details.doctor_id,db.sm_prescription_details.doctor_name,db.sm_prescription_details.medicine_id,db.sm_prescription_details.medicine_name,db.sm_prescription_details.brand,db.sm_prescription_details.generic,db.sm_prescription_details.strength,db.sm_prescription_details.formation,db.sm_prescription_details.company, orderby=~db.sm_prescription_details.submit_date|db.sm_prescription_details.area_id|db.sm_prescription_details.submit_by_id|db.sm_prescription_details.doctor_id|~db.sm_prescription_details.sl)

    reg_name=''
    regionRows=db((db.sm_level.cid==cid)&(db.sm_level.level_id==pr_region)).select(db.sm_level.level_name,limitby=(0,1))
    if regionRows:
        reg_name=regionRows[0].level_name
        
    return dict(records=records,med_division=med_division,pr_region=pr_region,reg_name=reg_name,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,date_from=date_from,date_to=date_to,pr_doctor=pr_doctor,pr_ff=pr_ff,med_generic=med_generic)

def company_track2_by_competitions():
    cid = session.cid
    med_division = request.vars.med_division

    if med_division == 'PHARMA':
        response.title = 'Company Track2 By Competition Pharma'
    elif med_division == 'SINAVISION':
        response.title = 'Company Track2 By Competition Sinavision'

    date_from = request.vars.date_from
    date_to = request.vars.date_to

    pr_region = request.vars.pr_region
    pr_zone = request.vars.pr_zone
    pr_area = request.vars.pr_area
    pr_territory = request.vars.pr_territory
    pr_doctor = request.vars.pr_doctor
    pr_ff = request.vars.pr_ff
    med_generic =request.vars.med_generic

    if pr_region == 'None':
        pr_region = ''

    if pr_zone == 'None':
        pr_zone = ''

    if pr_area == 'None':
        pr_area = ''

    if pr_territory == 'None':
        pr_territory = ''

    if pr_doctor == 'None':
        pr_doctor = ''

    if pr_ff == 'None':
        pr_ff = ''

    qset = db()
    qset = qset(db.sm_level.cid == cid)
    qset = qset(db.sm_level.depth == 3)
    if pr_region != '':
        qset = qset(db.sm_level.level0 == pr_region)
    if pr_zone != '':
        qset = qset(db.sm_level.level1 == pr_zone)
    if pr_area != '':
        qset = qset(db.sm_level.level2 == pr_area)
    if pr_territory != '':
        qset = qset(db.sm_level.level_id == pr_territory)


    level0_list = qset.select(db.sm_level.level0,db.sm_level.level0_name, groupby=db.sm_level.level0,orderby=db.sm_level.level0).as_list()
    level1_list = qset.select(db.sm_level.level0,db.sm_level.level0_name,db.sm_level.level1,db.sm_level.level1_name, groupby=db.sm_level.level0|db.sm_level.level1, orderby=db.sm_level.level0|db.sm_level.level1).as_list()
    level2_list = qset.select(db.sm_level.level0,db.sm_level.level0_name,db.sm_level.level1,db.sm_level.level1_name,db.sm_level.level2,db.sm_level.level2_name, groupby=db.sm_level.level0 | db.sm_level.level1 | db.sm_level.level2,orderby=db.sm_level.level0 | db.sm_level.level1| db.sm_level.level2).as_list()
    level3_list = qset.select(db.sm_level.level0,db.sm_level.level0_name, db.sm_level.level1,db.sm_level.level1_name, db.sm_level.level2,db.sm_level.level2_name,db.sm_level.level_id,db.sm_level.level_name,groupby=db.sm_level.level0 | db.sm_level.level1 | db.sm_level.level2|db.sm_level.level_id,orderby=db.sm_level.level0 | db.sm_level.level1 | db.sm_level.level2|db.sm_level.level_id).as_list()

    condition=''
    condition1 = ''
    if pr_region != '':
        condition += " and a.level0 ='" + pr_region + "'"
    if pr_zone != '':
        condition += " and a.level1 ='" + pr_zone + "'"
    if pr_area != '':
        condition += " and a.level2 ='" + pr_area + "'"
    if pr_territory != '':
        condition += " and a.level_id ='" + pr_territory + "'"

    if pr_ff != '':
        condition += " and b.submit_by_id = '" + str(pr_ff) + "'"
        condition1 += " and submit_by_id = '" + str(pr_ff) + "'"

    if pr_doctor != '':
        condition += " and b.doctor_id = '" + str(pr_doctor) + "'"
        condition1 += " and doctor_id = '" + str(pr_doctor) + "'"
    if med_generic != '':
        condition += " and b.generic = '" + str(med_generic)+ "'"
        condition1 += " and generic = '" + str(med_generic) + "'"

    if med_division=='PHARMA':
        sql0 = "(SELECT company,count(id) as rxSelfMed FROM `sm_prescription_details` WHERE  cid='" + cid + "' and update_flag =2 and submit_date>='" + date_from + "' and submit_date<='" + date_to + "' and dept !='NMD' and medicine_id!='0' " + condition1 + " group by company order by rxSelfMed desc)"
        sql1 = "(SELECT a.level0 as level0,b.company as company,count(b.id) as rxSelfMed FROM `sm_level` a,`sm_prescription_details` b WHERE  b.cid='" + cid + "' and b.update_flag =2 and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and b.dept !='NMD' and b.medicine_id!='0' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0,b.company order by a.level0,rxSelfMed desc)"
        sql2 = "(SELECT a.level0 as level0,a.level1 as level1,b.company as company,count(b.id) as rxSelfMed FROM `sm_level` a,`sm_prescription_details` b WHERE  b.cid='" + cid + "' and b.update_flag =2 and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and b.dept !='NMD' and b.medicine_id!='0' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0,a.level1,b.company order by a.level0,a.level1,rxSelfMed desc)"
        sql3 = "(SELECT a.level0 as level0,a.level1 as level1,a.level2 as level2,b.company as company,count(b.id) as rxSelfMed FROM `sm_level` a,`sm_prescription_details` b WHERE  b.cid='" + cid + "' and b.update_flag =2 and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and b.dept !='NMD' and b.medicine_id!='0' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0,a.level1,a.level2,b.company order by a.level0,a.level1,a.level2,rxSelfMed desc)"
        sql4 = "(SELECT a.level0 as level0,a.level1 as level1,a.level2 as level2,a.level_id as level3,b.company as company,count(b.id) as rxSelfMed FROM `sm_level` a,`sm_prescription_details` b WHERE  b.cid='" + cid + "' and b.update_flag =2 and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and b.dept !='NMD' and b.medicine_id!='0' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0,a.level1,a.level2,a.level_id,b.company order by a.level0,a.level1,a.level2,a.level_id,rxSelfMed desc)"
    elif med_division=='SINAVISION':
        sql0 = "(SELECT company,count(id) as rxSelfMed FROM `sm_prescription_details` WHERE  cid='" + cid + "' and update_flag =2 and submit_date>='" + date_from + "' and submit_date<='" + date_to + "' and dept ='SV' and medicine_id!='0' " + condition1 + " group by company order by rxSelfMed desc)"
        sql1 = "(SELECT a.level0 as level0,b.company as company,count(b.id) as rxSelfMed FROM `sm_level` a,`sm_prescription_details` b WHERE  b.cid='" + cid + "' and b.update_flag =2 and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and b.dept ='SV' and b.medicine_id!='0' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0,b.company order by a.level0,rxSelfMed desc)"
        sql2 = "(SELECT a.level0 as level0,a.level1 as level1,b.company as company,count(b.id) as rxSelfMed FROM `sm_level` a,`sm_prescription_details` b WHERE  b.cid='" + cid + "' and b.update_flag =2 and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and b.dept ='SV' and b.medicine_id!='0' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0,a.level1,b.company order by a.level0,a.level1,rxSelfMed desc)"
        sql3 = "(SELECT a.level0 as level0,a.level1 as level1,a.level2 as level2,b.company as company,count(b.id) as rxSelfMed FROM `sm_level` a,`sm_prescription_details` b WHERE  b.cid='" + cid + "' and b.update_flag =2 and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and b.dept ='SV' and b.medicine_id!='0' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0,a.level1,a.level2,b.company order by a.level0,a.level1,a.level2,rxSelfMed desc)"
        sql4 = "(SELECT a.level0 as level0,a.level1 as level1,a.level2 as level2,a.level_id as level3,b.company as company,count(b.id) as rxSelfMed FROM `sm_level` a,`sm_prescription_details` b WHERE  b.cid='" + cid + "' and b.update_flag =2 and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and b.dept ='SV' and b.medicine_id!='0' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by a.level0,a.level1,a.level2,a.level_id,b.company order by a.level0,a.level1,a.level2,a.level_id,rxSelfMed desc)"

    recordList0 = db.executesql(sql0, as_dict=True)
    recordList1 = db.executesql(sql1, as_dict=True)
    recordList2 = db.executesql(sql2, as_dict=True)
    recordList3 = db.executesql(sql3, as_dict=True)
    recordList4 = db.executesql(sql4, as_dict=True)

    #### N
    recordListN=[]
    dictData = {'level_type': 'National','level_id': '','level_name': '', 'rxTotalMed': '0', 'ibn': '0.00', 'rank': '0', '1st': '', '2nd': '','3rd': '', '4th': '', '5th': '', '6th': '', '7th': '', '8th': '', '9th': '', '10th': '', '11th': '','12th': '', '13th': ''}

    rxTotalMed=0
    for i in range(len(recordList0)):
        recordList0S=recordList0[i]
        rxTotalMed+=recordList0S['rxSelfMed']

    dictData1 = {'rxTotalMed': str(rxTotalMed)}
    dictData.update(dictData1)
    j=0
    for n in range(len(recordList0)):
        recordList0S = recordList0[n]
        company=recordList0S['company']
        rxSelfMed = recordList0S['rxSelfMed']
        share=round(float(rxSelfMed)/float(rxTotalMed)*100,2)
        comShare=str(company)+'-'+str(share)
        j+=1

        if j==1:
            if company=='IBN':
                dictData1={'ibn':str(share),'rank':str(j)}
                dictData.update(dictData1)

            dictData1={'1st':comShare}
            dictData.update(dictData1)

        elif j==2:
            if company=='IBN':
                dictData1={'ibn':str(share),'rank':str(j)}
                dictData.update(dictData1)

            dictData1={'2nd':comShare}
            dictData.update(dictData1)

        elif j==3:
            if company=='IBN':
                dictData1={'ibn':str(share),'rank':str(j)}
                dictData.update(dictData1)

            dictData1={'3rd':comShare}
            dictData.update(dictData1)

        elif j==4:
            if company=='IBN':
                dictData1={'ibn':str(share),'rank':str(j)}
                dictData.update(dictData1)

            dictData1={'4th':comShare}
            dictData.update(dictData1)


        elif j==5:
            if company=='IBN':
                dictData1={'ibn':str(share),'rank':str(j)}
                dictData.update(dictData1)

            dictData1={'5th':comShare}
            dictData.update(dictData1)

        elif j==6:
            if company=='IBN':
                dictData1={'ibn':str(share),'rank':str(j)}
                dictData.update(dictData1)

            dictData1={'6th':comShare}
            dictData.update(dictData1)

        elif j==7:
            if company=='IBN':
                dictData1={'ibn':str(share),'rank':str(j)}
                dictData.update(dictData1)

            dictData1={'7th':comShare}
            dictData.update(dictData1)
        elif j==8:
            if company=='IBN':
                dictData1={'ibn':str(share),'rank':str(j)}
                dictData.update(dictData1)

            dictData1={'8th':comShare}
            dictData.update(dictData1)
        elif j==9:
            if company=='IBN':
                dictData1={'ibn':str(share),'rank':str(j)}
                dictData.update(dictData1)

            dictData1={'9th':comShare}
            dictData.update(dictData1)
        elif j==10:
            if company=='IBN':
                dictData1={'ibn':str(share),'rank':str(j)}
                dictData.update(dictData1)

            dictData1={'10th':comShare}
            dictData.update(dictData1)
        elif j==11:
            if company=='IBN':
                dictData1={'ibn':str(share),'rank':str(j)}
                dictData.update(dictData1)

            dictData1={'11th':comShare}
            dictData.update(dictData1)
        elif j==12:
            if company=='IBN':
                dictData1={'ibn':str(share),'rank':str(j)}
                dictData.update(dictData1)

            dictData1={'12th':comShare}
            dictData.update(dictData1)
        elif j==13:
            if company=='IBN':
                dictData1={'ibn':str(share),'rank':str(j)}
                dictData.update(dictData1)

            dictData1={'13th':comShare}
            dictData.update(dictData1)
        else:
            continue

    recordListN.append(dictData)


    #### 0
    recordListL0=[]

    for k in range(len(level0_list)):
        level0_list_s=level0_list[k]
        level0=level0_list_s['level0']
        level0_name = level0_list_s['level0_name']

        dictData = {'level_type': 'GM', 'rxTotalMed': '0', 'level_id': '', 'level_name': '', 'ibn': '0.00', 'rank': '0','1st': '', '2nd': '', '3rd': '', '4th': '', '5th': '', '6th': '', '7th': '', '8th': '', '9th': '','10th': '', '11th': '', '12th': '', '13th': ''}

        dictData1 = {'level_id': str(level0),'level_name': str(level0_name)}
        dictData.update(dictData1)

        rxTotalMed=0
        for i in range(len(recordList1)):
            recordList1S=recordList1[i]
            rxTotalMed+=recordList1S['rxSelfMed']

        dictData1 = {'rxTotalMed': str(rxTotalMed)}
        dictData.update(dictData1)
        j=0
        for n in range(len(recordList1)):
            recordList1S = recordList1[n]
            company=recordList1S['company']
            rxSelfMed = recordList1S['rxSelfMed']

            share='0.00'
            if rxTotalMed > 0:
                share = round(float(rxSelfMed) / float(rxTotalMed) * 100, 2)
                comShare = str(company) + '-' + str(share)
            else:
                comShare = ''

            j+=1

            if j==1:
                if company=='IBN':
                    dictData1={'ibn':str(share),'rank':str(j)}
                    dictData.update(dictData1)

                dictData1={'1st':comShare}
                dictData.update(dictData1)

            elif j==2:
                if company=='IBN':
                    dictData1={'ibn':str(share),'rank':str(j)}
                    dictData.update(dictData1)

                dictData1={'2nd':comShare}
                dictData.update(dictData1)

            elif j==3:
                if company=='IBN':
                    dictData1={'ibn':str(share),'rank':str(j)}
                    dictData.update(dictData1)

                dictData1={'3rd':comShare}
                dictData.update(dictData1)

            elif j==4:
                if company=='IBN':
                    dictData1={'ibn':str(share),'rank':str(j)}
                    dictData.update(dictData1)

                dictData1={'4th':comShare}
                dictData.update(dictData1)


            elif j==5:
                if company=='IBN':
                    dictData1={'ibn':str(share),'rank':str(j)}
                    dictData.update(dictData1)

                dictData1={'5th':comShare}
                dictData.update(dictData1)

            elif j==6:
                if company=='IBN':
                    dictData1={'ibn':str(share),'rank':str(j)}
                    dictData.update(dictData1)

                dictData1={'6th':comShare}
                dictData.update(dictData1)

            elif j==7:
                if company=='IBN':
                    dictData1={'ibn':str(share),'rank':str(j)}
                    dictData.update(dictData1)

                dictData1={'7th':comShare}
                dictData.update(dictData1)
            elif j==8:
                if company=='IBN':
                    dictData1={'ibn':str(share),'rank':str(j)}
                    dictData.update(dictData1)

                dictData1={'8th':comShare}
                dictData.update(dictData1)
            elif j==9:
                if company=='IBN':
                    dictData1={'ibn':str(share),'rank':str(j)}
                    dictData.update(dictData1)

                dictData1={'9th':comShare}
                dictData.update(dictData1)
            elif j==10:
                if company=='IBN':
                    dictData1={'ibn':str(share),'rank':str(j)}
                    dictData.update(dictData1)

                dictData1={'10th':comShare}
                dictData.update(dictData1)
            elif j==11:
                if company=='IBN':
                    dictData1={'ibn':str(share),'rank':str(j)}
                    dictData.update(dictData1)

                dictData1={'11th':comShare}
                dictData.update(dictData1)
            elif j==12:
                if company=='IBN':
                    dictData1={'ibn':str(share),'rank':str(j)}
                    dictData.update(dictData1)

                dictData1={'12th':comShare}
                dictData.update(dictData1)
            elif j==13:
                if company=='IBN':
                    dictData1={'ibn':str(share),'rank':str(j)}
                    dictData.update(dictData1)

                dictData1={'13th':comShare}
                dictData.update(dictData1)
            else:
                continue

        recordListL0.append(dictData)


    # #### 1
    recordListL1=[]
    for k in range(len(level1_list)):
        level1_list_s=level1_list[k]
        level0=level1_list_s['level0']
        level0_name = level1_list_s['level0_name']
        level1 = level1_list_s['level1']
        level1_name = level1_list_s['level1_name']

        dictData = {'level_type': 'RM', 'rxTotalMed': '0','level0': str(level0), 'level_id': '', 'level_name': '', 'ibn': '0.00', 'rank': '0','1st': '', '2nd': '', '3rd': '', '4th': '', '5th': '', '6th': '', '7th': '', '8th': '', '9th': '','10th': '', '11th': '', '12th': '', '13th': ''}

        dictData1 = {'level_id': str(level1),'level_name': str(level1_name)}
        dictData.update(dictData1)

        rxTotalMed=0
        for i in range(len(recordList2)):
            recordList2S=recordList2[i]
            level01 = recordList2S['level0']
            level11 = recordList2S['level1']
            if level01==level0 and level11==level1:
                rxTotalMed+=recordList2S['rxSelfMed']

        dictData1 = {'rxTotalMed': str(rxTotalMed)}
        dictData.update(dictData1)

        rxSelfMed=0
        j=0
        for n in range(len(recordList2)):
            recordList2S = recordList2[n]
            level01 = recordList2S['level0']
            level11 = recordList2S['level1']
            company=recordList2S['company']
            rxSelfMed = recordList2S['rxSelfMed']

            share = '0.00'
            if level01 == level0 and level11 == level1:

                if rxTotalMed > 0:
                    share = round(float(rxSelfMed) / float(rxTotalMed) * 100, 2)
                    comShare = str(company) + '-' + str(share)
                else:
                    comShare = ''

                j+=1
                if j==1:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'1st':comShare}
                    dictData.update(dictData1)

                elif j==2:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'2nd':comShare}
                    dictData.update(dictData1)

                elif j==3:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'3rd':comShare}
                    dictData.update(dictData1)

                elif j==4:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'4th':comShare}
                    dictData.update(dictData1)


                elif j==5:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'5th':comShare}
                    dictData.update(dictData1)

                elif j==6:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'6th':comShare}
                    dictData.update(dictData1)

                elif j==7:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'7th':comShare}
                    dictData.update(dictData1)
                elif j==8:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'8th':comShare}
                    dictData.update(dictData1)
                elif j==9:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'9th':comShare}
                    dictData.update(dictData1)
                elif j==10:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'10th':comShare}
                    dictData.update(dictData1)
                elif j==11:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'11th':comShare}
                    dictData.update(dictData1)
                elif j==12:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'12th':comShare}
                    dictData.update(dictData1)
                elif j==13:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'13th':comShare}
                    dictData.update(dictData1)
                else:
                    continue

        recordListL1.append(dictData)

    #### 2
    recordListL2=[]
    for k in range(len(level2_list)):
        level2_list_s=level2_list[k]
        level0=level2_list_s['level0']
        level0_name = level2_list_s['level0_name']
        level1 = level2_list_s['level1']
        level1_name = level2_list_s['level1_name']
        level2 = level2_list_s['level2']
        level2_name = level2_list_s['level2_name']

        dictData = {'level_type': 'AM', 'rxTotalMed': '0','level0': str(level0),'level1': str(level1), 'level_id': '', 'level_name': '', 'ibn': '0.00', 'rank': '0','1st': '', '2nd': '', '3rd': '', '4th': '', '5th': '', '6th': '', '7th': '', '8th': '', '9th': '','10th': '', '11th': '', '12th': '', '13th': ''}

        dictData1 = {'level_id': str(level2),'level_name': str(level2_name)}
        dictData.update(dictData1)

        rxTotalMed=0
        for i in range(len(recordList3)):
            recordList3S=recordList3[i]
            level01 = recordList3S['level0']
            level11 = recordList3S['level1']
            level21 = recordList3S['level2']
            if level01==level0 and level11==level1 and level21==level2:
                rxTotalMed+=recordList3S['rxSelfMed']

        dictData1 = {'rxTotalMed': str(rxTotalMed)}
        dictData.update(dictData1)

        rxSelfMed=0
        j=0
        for n in range(len(recordList3)):
            recordList3S = recordList3[n]
            level01 = recordList3S['level0']
            level11 = recordList3S['level1']
            level21 = recordList3S['level2']
            company=recordList3S['company']
            rxSelfMed = recordList3S['rxSelfMed']

            share = '0.00'
            if level01 == level0 and level11 == level1 and level21 == level2:

                if rxTotalMed > 0:
                    share = round(float(rxSelfMed) / float(rxTotalMed) * 100, 2)
                    comShare = str(company) + '-' + str(share)
                else:
                    comShare = ''

                j+=1
                if j==1:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'1st':comShare}
                    dictData.update(dictData1)

                elif j==2:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'2nd':comShare}
                    dictData.update(dictData1)

                elif j==3:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'3rd':comShare}
                    dictData.update(dictData1)

                elif j==4:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'4th':comShare}
                    dictData.update(dictData1)


                elif j==5:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'5th':comShare}
                    dictData.update(dictData1)

                elif j==6:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'6th':comShare}
                    dictData.update(dictData1)

                elif j==7:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'7th':comShare}
                    dictData.update(dictData1)
                elif j==8:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'8th':comShare}
                    dictData.update(dictData1)
                elif j==9:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'9th':comShare}
                    dictData.update(dictData1)
                elif j==10:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'10th':comShare}
                    dictData.update(dictData1)
                elif j==11:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'11th':comShare}
                    dictData.update(dictData1)
                elif j==12:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'12th':comShare}
                    dictData.update(dictData1)
                elif j==13:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'13th':comShare}
                    dictData.update(dictData1)
                else:
                    continue

        recordListL2.append(dictData)


    #### 3
    recordListL3=[]
    for k in range(len(level3_list)):
        level3_list_s=level3_list[k]
        level0=level3_list_s['level0']
        level0_name = level3_list_s['level0_name']
        level1 = level3_list_s['level1']
        level1_name = level3_list_s['level1_name']
        level2 = level3_list_s['level2']
        level2_name = level3_list_s['level2_name']
        level3 = level3_list_s['level_id']
        level3_name = level3_list_s['level_name']

        dictData = {'level_type': 'TERR', 'rxTotalMed': '0','level0': str(level0),'level1': str(level1),'level2': str(level2), 'level_id': '', 'level_name': '', 'ibn': '0.00', 'rank': '0','1st': '', '2nd': '', '3rd': '', '4th': '', '5th': '', '6th': '', '7th': '', '8th': '', '9th': '','10th': '', '11th': '', '12th': '', '13th': ''}

        dictData1 = {'level_id': str(level3),'level_name': str(level3_name)}
        dictData.update(dictData1)

        rxTotalMed=0
        for i in range(len(recordList4)):
            recordList4S=recordList4[i]
            level01 = recordList4S['level0']
            level11 = recordList4S['level1']
            level21 = recordList4S['level2']
            level31 = recordList4S['level3']
            if level01==level0 and level11==level1 and level21==level2 and level31==level3:
                rxTotalMed+=recordList4S['rxSelfMed']

        dictData1 = {'rxTotalMed': str(rxTotalMed)}
        dictData.update(dictData1)

        rxSelfMed=0
        j=0
        for n in range(len(recordList4)):
            recordList4S = recordList4[n]
            level01 = recordList4S['level0']
            level11 = recordList4S['level1']
            level21 = recordList4S['level2']
            level31 = recordList4S['level3']
            company=recordList4S['company']
            rxSelfMed = recordList4S['rxSelfMed']

            share = 0.00
            if level01 == level0 and level11 == level1 and level21 == level2 and level31==level3:

                if rxTotalMed > 0:
                    share = round(float(rxSelfMed) / float(rxTotalMed) * 100, 2)
                    comShare = str(company) + '-' + str(share)
                else:
                    comShare = ''

                j+=1
                if j==1:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'1st':comShare}
                    dictData.update(dictData1)

                elif j==2:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'2nd':comShare}
                    dictData.update(dictData1)

                elif j==3:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'3rd':comShare}
                    dictData.update(dictData1)

                elif j==4:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'4th':comShare}
                    dictData.update(dictData1)


                elif j==5:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'5th':comShare}
                    dictData.update(dictData1)

                elif j==6:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'6th':comShare}
                    dictData.update(dictData1)

                elif j==7:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'7th':comShare}
                    dictData.update(dictData1)
                elif j==8:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'8th':comShare}
                    dictData.update(dictData1)
                elif j==9:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'9th':comShare}
                    dictData.update(dictData1)
                elif j==10:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'10th':comShare}
                    dictData.update(dictData1)
                elif j==11:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'11th':comShare}
                    dictData.update(dictData1)
                elif j==12:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'12th':comShare}
                    dictData.update(dictData1)
                elif j==13:
                    if company=='IBN':
                        dictData1={'ibn':str(share),'rank':str(j)}
                        dictData.update(dictData1)

                    dictData1={'13th':comShare}
                    dictData.update(dictData1)
                else:
                    continue

        recordListL3.append(dictData)

    reg_name = ''
    regionRows = db((db.sm_level.cid == cid) & (db.sm_level.level_id == pr_region)).select(db.sm_level.level_name,limitby=(0, 1))
    if regionRows:
        reg_name = regionRows[0].level_name

    return dict(med_division=med_division,recordListN=recordListN,recordListL0=recordListL0,recordListL1=recordListL1,recordListL2=recordListL2,recordListL3=recordListL3,date_from=date_from, date_to=date_to, pr_region=pr_region, reg_name=reg_name, pr_zone=pr_zone,pr_area=pr_area, pr_territory=pr_territory, pr_doctor=pr_doctor, med_generic=med_generic, pr_ff=pr_ff)


def generic_track2_by_competitions():
    cid = session.cid
    med_division = request.vars.med_division

    if med_division == 'PHARMA':
        response.title = 'Generic Track2 By Competition Pharma'
    elif med_division == 'SINAVISION':
        response.title = 'Generic Track2 By Competition Sinavision'

    date_from = request.vars.date_from
    date_to = request.vars.date_to

    pr_region = request.vars.pr_region
    pr_zone = request.vars.pr_zone
    pr_area = request.vars.pr_area
    pr_territory = request.vars.pr_territory
    pr_doctor = request.vars.pr_doctor
    pr_ff = request.vars.pr_ff
    med_generic =request.vars.med_generic

    if pr_region == 'None':
        pr_region = ''

    if pr_zone == 'None':
        pr_zone = ''

    if pr_area == 'None':
        pr_area = ''

    if pr_territory == 'None':
        pr_territory = ''

    if pr_doctor == 'None':
        pr_doctor = ''

    if pr_ff == 'None':
        pr_ff = ''

    condition = ''
    if pr_region != '':
        condition += " and a.level0 ='" + pr_region + "'"
    if pr_zone != '':
        condition += " and a.level1 ='" + pr_zone + "'"
    if pr_area != '':
        condition += " and a.level2 ='" + pr_area + "'"
    if pr_territory != '':
        condition += " and a.level_id ='" + pr_territory + "'"
    if pr_ff != '':
        condition += " and b.submit_by_id = '" + str(pr_ff) + "'"
    if pr_doctor != '':
        condition += " and b.doctor_id = '" + str(pr_doctor) + "'"
    if med_generic != '':
        condition += " and b.generic = '" + str(med_generic) + "'"




    recordListH0 = []
    recordListH1 = []

    recordList0=[]
    recordList1 = []

    sqlh1 = ''
    sqlh2 = ''

    sql1=''
    sql2=''


    if med_division == 'PHARMA':
        sqlh1 = "(SELECT b.generic as generic,count(b.id) as rxTotalMed FROM `sm_level` a, `sm_prescription_details` b WHERE b.cid='" + cid + "' and b.update_flag =2 and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and b.dept !='NMD' and b.medicine_id!='0' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by generic order by generic)"
        sqlh2 = "(SELECT b.generic as generic,b.company as company,count(b.id) as rxSelfMed FROM `sm_level` a, `sm_prescription_details` b WHERE b.cid='" + cid + "' and b.update_flag =2 and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and b.dept !='NMD' and b.medicine_id!='0' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by generic,company order by generic,rxSelfMed desc)"

        sql1 = "(SELECT b.generic as generic,b.formation as formation,b.strength as strength,count(b.id) as rxTotalMed FROM `sm_level` a, `sm_prescription_details` b WHERE b.cid='" + cid + "' and b.update_flag =2 and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and b.dept !='NMD' and b.medicine_id!='0' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by generic,formation,strength order by generic,formation,strength)"
        sql2 = "(SELECT b.generic as generic,b.formation as formation,b.strength as strength,b.company as company,count(b.id) as rxSelfMed FROM `sm_level` a, `sm_prescription_details` b WHERE b.cid='" + cid + "' and b.update_flag =2 and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and b.dept !='NMD' and b.medicine_id!='0' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by generic,formation,strength,company order by generic,formation,strength,rxSelfMed desc)"

    elif med_division == 'SINAVISION':
        sqlh1 = "(SELECT b.generic as generic,count(b.id) as rxTotalMed FROM `sm_level` a, `sm_prescription_details` b WHERE b.cid='" + cid + "' and b.update_flag =2 and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and b.dept ='SV' and b.medicine_id!='0' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by generic order by generic)"
        sqlh2 = "(SELECT b.generic as generic,b.company as company,count(b.id) as rxSelfMed FROM `sm_level` a, `sm_prescription_details` b WHERE b.cid='" + cid + "' and b.update_flag =2 and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and b.dept ='SV' and b.medicine_id!='0' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by generic,company order by generic,rxSelfMed desc)"

        sql1 = "(SELECT b.generic as generic,b.formation as formation,b.strength as strength,count(b.id) as rxTotalMed FROM `sm_level` a, `sm_prescription_details` b WHERE b.cid='" + cid + "' and b.update_flag =2 and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and b.dept ='SV' and b.medicine_id!='0' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by generic,formation,strength order by generic,formation,strength)"
        sql2 = "(SELECT b.generic as generic,b.formation as formation,b.strength as strength,b.company as company,count(b.id) as rxSelfMed FROM `sm_level` a, `sm_prescription_details` b WHERE b.cid='" + cid + "' and b.update_flag =2 and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and b.dept ='SV' and b.medicine_id!='0' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id  " + condition + " group by generic,formation,strength,company order by generic,formation,strength,rxSelfMed desc)"

    recordListH0 = db.executesql(sqlh1, as_dict=True)
    recordListH1 = db.executesql(sqlh2, as_dict=True)

    recordList0 = db.executesql(sql1, as_dict=True)
    recordList1 = db.executesql(sql2, as_dict=True)

    recordListH = []
    for i in range(len(recordListH0)):
        recordListH0S = recordListH0[i]
        generic = recordListH0S['generic']
        rxTotalMed = recordListH0S['rxTotalMed']

        dictData = {'generic': generic,'rxTotalMed': str(rxTotalMed),'ibn': '0.00', 'rank': '0', '1st': '', '2nd': '', '3rd': '', '4th': '', '5th': '', '6th': '', '7th': '', '8th': '', '9th': '', '10th': ''}

        j = 0
        for n in range(len(recordListH1)):
            recordListH1S = recordListH1[n]
            generic1 = recordListH1S['generic']
            company = recordListH1S['company']
            rxSelfMed = recordListH1S['rxSelfMed']

            share = 0.00
            if generic1 == generic:
                if rxTotalMed > 0:
                    share = round(float(rxSelfMed) / float(rxTotalMed) * 100, 2)
                    comShare = str(company) + '-' + str(share)
                else:
                    comShare = ''

                j += 1
                if j == 1:
                    if company == 'IBN':
                        dictData1 = {'ibn': str(share), 'rank': str(j)}
                        dictData.update(dictData1)

                    dictData1 = {'1st': comShare}
                    dictData.update(dictData1)

                elif j == 2:
                    if company == 'IBN':
                        dictData1 = {'ibn': str(share), 'rank': str(j)}
                        dictData.update(dictData1)

                    dictData1 = {'2nd': comShare}
                    dictData.update(dictData1)

                elif j == 3:
                    if company == 'IBN':
                        dictData1 = {'ibn': str(share), 'rank': str(j)}
                        dictData.update(dictData1)

                    dictData1 = {'3rd': comShare}
                    dictData.update(dictData1)

                elif j == 4:
                    if company == 'IBN':
                        dictData1 = {'ibn': str(share), 'rank': str(j)}
                        dictData.update(dictData1)

                    dictData1 = {'4th': comShare}
                    dictData.update(dictData1)


                elif j == 5:
                    if company == 'IBN':
                        dictData1 = {'ibn': str(share), 'rank': str(j)}
                        dictData.update(dictData1)

                    dictData1 = {'5th': comShare}
                    dictData.update(dictData1)

                elif j == 6:
                    if company == 'IBN':
                        dictData1 = {'ibn': str(share), 'rank': str(j)}
                        dictData.update(dictData1)

                    dictData1 = {'6th': comShare}
                    dictData.update(dictData1)

                elif j == 7:
                    if company == 'IBN':
                        dictData1 = {'ibn': str(share), 'rank': str(j)}
                        dictData.update(dictData1)

                    dictData1 = {'7th': comShare}
                    dictData.update(dictData1)
                elif j == 8:
                    if company == 'IBN':
                        dictData1 = {'ibn': str(share), 'rank': str(j)}
                        dictData.update(dictData1)

                    dictData1 = {'8th': comShare}
                    dictData.update(dictData1)
                elif j == 9:
                    if company == 'IBN':
                        dictData1 = {'ibn': str(share), 'rank': str(j)}
                        dictData.update(dictData1)

                    dictData1 = {'9th': comShare}
                    dictData.update(dictData1)
                elif j == 10:
                    if company == 'IBN':
                        dictData1 = {'ibn': str(share), 'rank': str(j)}
                        dictData.update(dictData1)

                    dictData1 = {'10th': comShare}
                    dictData.update(dictData1)
                else:
                    continue

        recordListH.append(dictData)


    recordList=[]
    for i in range(len(recordList0)):
        recordList0S=recordList0[i]
        generic=recordList0S['generic']
        formation = recordList0S['formation']
        strength = recordList0S['strength']
        rxTotalMed = recordList0S['rxTotalMed']

        dictData = {'generic':generic,'formation':formation,'strength':strength,'rxTotalMed':str(rxTotalMed),'ibn':'0.00','rank':'0', '1st': '', '2nd': '', '3rd': '', '4th': '', '5th': '', '6th': '', '7th': '', '8th': '', '9th': '', '10th': ''}

        j=0
        for n in range(len(recordList1)):
            recordList1S = recordList1[n]
            generic1 = recordList1S['generic']
            formation1 = recordList1S['formation']
            strength1 = recordList1S['strength']
            company = recordList1S['company']
            rxSelfMed=recordList1S['rxSelfMed']

            share = 0.00
            if generic1==generic and formation1==formation and strength1==strength:
                if rxTotalMed > 0:
                    share = round(float(rxSelfMed) / float(rxTotalMed) * 100, 2)
                    comShare = str(company) + '-' + str(share)
                else:
                    comShare = ''

                j += 1
                if j == 1:
                    if company == 'IBN':
                        dictData1 = {'ibn': str(share), 'rank': str(j)}
                        dictData.update(dictData1)

                    dictData1 = {'1st': comShare}
                    dictData.update(dictData1)

                elif j == 2:
                    if company == 'IBN':
                        dictData1 = {'ibn': str(share), 'rank': str(j)}
                        dictData.update(dictData1)

                    dictData1 = {'2nd': comShare}
                    dictData.update(dictData1)

                elif j == 3:
                    if company == 'IBN':
                        dictData1 = {'ibn': str(share), 'rank': str(j)}
                        dictData.update(dictData1)

                    dictData1 = {'3rd': comShare}
                    dictData.update(dictData1)

                elif j == 4:
                    if company == 'IBN':
                        dictData1 = {'ibn': str(share), 'rank': str(j)}
                        dictData.update(dictData1)

                    dictData1 = {'4th': comShare}
                    dictData.update(dictData1)


                elif j == 5:
                    if company == 'IBN':
                        dictData1 = {'ibn': str(share), 'rank': str(j)}
                        dictData.update(dictData1)

                    dictData1 = {'5th': comShare}
                    dictData.update(dictData1)

                elif j == 6:
                    if company == 'IBN':
                        dictData1 = {'ibn': str(share), 'rank': str(j)}
                        dictData.update(dictData1)

                    dictData1 = {'6th': comShare}
                    dictData.update(dictData1)

                elif j == 7:
                    if company == 'IBN':
                        dictData1 = {'ibn': str(share), 'rank': str(j)}
                        dictData.update(dictData1)

                    dictData1 = {'7th': comShare}
                    dictData.update(dictData1)
                elif j == 8:
                    if company == 'IBN':
                        dictData1 = {'ibn': str(share), 'rank': str(j)}
                        dictData.update(dictData1)

                    dictData1 = {'8th': comShare}
                    dictData.update(dictData1)
                elif j == 9:
                    if company == 'IBN':
                        dictData1 = {'ibn': str(share), 'rank': str(j)}
                        dictData.update(dictData1)

                    dictData1 = {'9th': comShare}
                    dictData.update(dictData1)
                elif j == 10:
                    if company == 'IBN':
                        dictData1 = {'ibn': str(share), 'rank': str(j)}
                        dictData.update(dictData1)

                    dictData1 = {'10th': comShare}
                    dictData.update(dictData1)
                else:
                    continue

        recordList.append(dictData)

    reg_name = ''
    regionRows = db((db.sm_level.cid == cid) & (db.sm_level.level_id == pr_region)).select(db.sm_level.level_name,limitby=(0, 1))
    if regionRows:
        reg_name = regionRows[0].level_name

    return dict(med_division=med_division,recordListH=recordListH,recordList=recordList,date_from=date_from, date_to=date_to, pr_region=pr_region, reg_name=reg_name, pr_zone=pr_zone,pr_area=pr_area, pr_territory=pr_territory, pr_doctor=pr_doctor, med_generic=med_generic, pr_ff=pr_ff)


def generic_track2_by_physician():
    cid = session.cid
    med_division = request.vars.med_division

    if med_division == 'PHARMA':
        response.title = 'Generic Track2 By Physician Pharma'
    elif med_division == 'SINAVISION':
        response.title = 'Generic Track2 By Physician Sinavision'

    date_from = request.vars.date_from
    date_to = request.vars.date_to

    pr_region = request.vars.pr_region
    pr_zone = request.vars.pr_zone
    pr_area = request.vars.pr_area
    pr_territory = request.vars.pr_territory
    pr_doctor = request.vars.pr_doctor
    pr_ff = request.vars.pr_ff
    med_generic =request.vars.med_generic

    if pr_region == 'None':
        pr_region = ''

    if pr_zone == 'None':
        pr_zone = ''

    if pr_area == 'None':
        pr_area = ''

    if pr_territory == 'None':
        pr_territory = ''

    if pr_doctor == 'None':
        pr_doctor = ''

    if pr_ff == 'None':
        pr_ff = ''

    condition = ''
    if pr_region != '':
        condition += " and a.level0 ='" + pr_region + "'"
    if pr_zone != '':
        condition += " and a.level1 ='" + pr_zone + "'"
    if pr_area != '':
        condition += " and a.level2 ='" + pr_area + "'"
    if pr_territory != '':
        condition += " and a.level_id ='" + pr_territory + "'"
    if pr_ff != '':
        condition += " and b.submit_by_id = '" + str(pr_ff) + "'"
    if pr_doctor != '':
        condition += " and b.doctor_id = '" + str(pr_doctor) + "'"
    if med_generic != '':
        condition += " and b.generic = '" + str(med_generic) + "'"

    sql11 = ''
    sql12 = ''
    recordList0 = []
    recordList1 = []
    if med_division == 'PHARMA':
        sql11 = "(SELECT b.area_id as area_id,b.doctor_id as doctor_id,count(b.id) as rxTotalMed FROM `sm_level` a,`sm_prescription_details` b WHERE b.cid='" + cid + "' and b.update_flag =2 and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and b.dept !='NMD' and b.medicine_id!='0' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id " + condition + " group by b.area_id,b.doctor_id order by b.area_id,b.doctor_id)"
        sql12 = "(SELECT b.area_id as area_id,b.doctor_id as doctor_id,b.company as company,b.brand as brand,count(b.id) as rxSelfMed FROM `sm_level` a,`sm_prescription_details` b WHERE b.cid='" + cid + "' and b.update_flag =2 and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and b.dept !='NMD' and b.medicine_id!='0' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id " + condition + " group by b.area_id,b.doctor_id,b.company,b.brand order by b.area_id,b.doctor_id,rxSelfMed desc)"
    elif med_division == 'SINAVISION':
        sql11 = "(SELECT b.area_id as area_id,b.doctor_id as doctor_id,count(b.id) as rxTotalMed FROM `sm_level` a,`sm_prescription_details` b WHERE b.cid='" + cid + "' and b.update_flag =2 and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and b.dept ='SV' and b.medicine_id!='0' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id " + condition + " group by b.area_id,b.doctor_id order by b.area_id,b.doctor_id)"
        sql12 = "(SELECT b.area_id as area_id,b.doctor_id as doctor_id,b.company as company,b.brand as brand,count(b.id) as rxSelfMed FROM `sm_level` a,`sm_prescription_details` b WHERE b.cid='" + cid + "' and b.update_flag =2 and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and b.dept ='SV' and b.medicine_id!='0' and a.cid=b.cid and a.depth=3 and a.level_id=b.area_id " + condition + " group by b.area_id,b.doctor_id,b.company,b.brand order by b.area_id,b.doctor_id,rxSelfMed desc)"

    recordList0 = db.executesql(sql11, as_dict=True)
    recordList1 = db.executesql(sql12, as_dict=True)


    doctor_id_list = []
    for i in range(len(recordList0)):
        recordsS = recordList0[i]
        doctor_id = str(recordsS['doctor_id'])

        if doctor_id not in doctor_id_list:
            doctor_id_list.append(doctor_id)


    doctorList = []
    if len(doctor_id_list) > 0:
        doctor_id_str = str(doctor_id_list).replace("['", "'").replace("']", "'")
        sql31 = "select b.area_id as area_id,a.doc_id as doc_id,a.doc_name as doc_name,a.degree as degree,a.specialty as specialty,a.des as des,b.address as address,b.district as district,b.thana as thana from sm_doctor a,sm_doctor_area b where a.cid='" + cid + "' and a.doc_id in (" + doctor_id_str + ") and a.cid=b.cid and a.doc_id=b.doc_id;"
        doctorList = db.executesql(sql31, as_dict=True)


    recordList=[]

    for i in range(len(recordList0)):
        recordList0S=recordList0[i]
        area_id = recordList0S['area_id']
        doc_id = recordList0S['doctor_id']
        rxTotalMed = recordList0S['rxTotalMed']

        dictData={'area_id':area_id,'doc_id':doc_id,'rxTotalMed':str(rxTotalMed),'ibn':'0.00','rank':'0','company':'','brand':'','rxSelfMed':'0','share':'','company1':'','brand1':'','rxSelfMed1':'0','share1':''}

        conpanyCount = 0
        rank = 0
        for j in range(len(recordList1)):
            recordList1S = recordList1[j]
            area_id1 = recordList1S['area_id']
            doc_id1 = recordList1S['doctor_id']
            company = recordList1S['company']
            brand = recordList1S['brand']
            rxSelfMed = recordList1S['rxSelfMed']
            share=round(float(rxSelfMed)/float(rxTotalMed)*100,2)

            if area_id1==area_id and doc_id1==doc_id:
                if conpanyCount==0:
                    dictData1 = { 'company': company,'brand': brand, 'rxSelfMed': str(rxSelfMed), 'share': str(share)}
                    dictData.update(dictData1)
                    conpanyCount += 1

                    if company == 'IBN':
                        dictData1 = {'ibn': str(share),'rank': str(conpanyCount)}
                        dictData.update(dictData1)

                elif conpanyCount==1:
                    dictData1 = { 'company1': company,'brand1': brand, 'rxSelfMed1': str(rxSelfMed), 'share1': str(share)}
                    dictData.update(dictData1)
                    conpanyCount += 1

                    if company == 'IBN':
                        dictData1 = {'ibn': str(share),'rank': str(conpanyCount)}
                        dictData.update(dictData1)
                else:
                    continue

        recordList.append(dictData)
    
    reg_name = ''
    regionRows = db((db.sm_level.cid == cid) & (db.sm_level.level_id == pr_region)).select(db.sm_level.level_name,limitby=(0, 1))
    if regionRows:
        reg_name = regionRows[0].level_name

    return dict(med_division=med_division,recordList=recordList,doctorList=doctorList,date_from=date_from, date_to=date_to, pr_region=pr_region, reg_name=reg_name, pr_zone=pr_zone,pr_area=pr_area, pr_territory=pr_territory, pr_doctor=pr_doctor, med_generic=med_generic, pr_ff=pr_ff)


#========== block 2
def physician_track2_d():
    cid = session.cid
    identical = request.vars.identical
    med_division = request.vars.med_division

    if med_division == 'PHARMA':
        response.title = 'Physician track2 Pharma'
    elif med_division == 'SINAVISION':
        response.title = 'Physician track2 Sinavision'

    date_from = request.vars.date_from
    date_to = request.vars.date_to

    pr_region = request.vars.pr_region
    pr_zone = request.vars.pr_zone
    pr_area = request.vars.pr_area
    pr_territory = request.vars.pr_territory
    pr_doctor = request.vars.pr_doctor
    kol_doctor = request.vars.kol_doctor
    pr_ff = request.vars.pr_ff

    if pr_region == 'None':
        pr_region = ''

    if pr_zone == 'None':
        pr_zone = ''

    if pr_area == 'None':
        pr_area = ''

    if pr_territory == 'None':
        pr_territory = ''

    if pr_doctor == 'None':
        pr_doctor = ''

    if pr_ff == 'None':
        pr_ff = ''

    condition = ''
    if pr_region != '':
        condition += " and a.level0 = '" + str(pr_region) + "'"
    if pr_zone != '':
        condition += " and a.level1 = '" + str(pr_zone) + "'"
    if pr_area != '':
        condition += " and a.level2 = '" + str(pr_area) + "'"
    if pr_territory != '':
        condition += " and a.level_id = '" + str(pr_territory) + "'"
    if pr_doctor != '':
        condition += " and b.doctor_id = '" + str(pr_doctor).split('|')[0] + "'"
    if kol_doctor != '0':
        condition += " and b.service_kol_dsc = " + str(kol_doctor)

    if int(identical) == 1:
        if med_division == 'PHARMA':
            condition += " and ( b.update_med_count_flag_i >0 or b.update_med_count_flag_i_snv >0) "
        elif med_division == 'SINAVISION':
            condition += " and b.update_med_count_flag_i_snv >0 "
    elif int(identical) == 0:
        if med_division == 'PHARMA':
            condition += " and ( b.update_med_count_flag >0 or b.update_med_count_flag_snv >0) "
        elif med_division == 'SINAVISION':
            condition += " and b.update_med_count_flag_snv >0 "

    sql1 = ''
    sql2 = ''
    if int(identical) == 1:
        if med_division == 'PHARMA':
            sql1 = "(SELECT a.level_id as area_id,b.doctor_id as doctor_id,b.doctor_name as doctor_name,b.doctor_speciality as doctor_speciality,b.doctor_chamber_address as doctor_chamber_address,b.service_kol_dsc as service_kol_dsc,b.sl as rxSelfCount, b.sl as rxTotalCount,(b.med_self+b.med_self_snv) as rxSelfMed, 0 as rxTotalMed FROM `sm_level` a,`sm_prescription_head` b WHERE a.cid='" + cid + "' and a.depth=3 and a.level_id=b.area_id and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and (b.med_self>0 or b.med_self_snv>0) " + condition + ")"
            sql2 = "(SELECT a.level_id as area_id,b.doctor_id as doctor_id,b.doctor_name as doctor_name,b.doctor_speciality as doctor_speciality,b.doctor_chamber_address as doctor_chamber_address,b.service_kol_dsc as service_kol_dsc,0 as rxSelfCount,sl as rxTotalCount,0 as rxSelfMed, (b.med_total_i+b.med_total_i_snv) as rxTotalMed FROM `sm_level` a,`sm_prescription_head` b WHERE a.cid='" + cid + "' and a.depth=3 and a.level_id=b.area_id and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' " + condition + ")"
        elif med_division == 'SINAVISION':
            sql1 = "(SELECT a.level_id as area_id,b.doctor_id as doctor_id,b.doctor_name as doctor_name,b.doctor_speciality as doctor_speciality,b.doctor_chamber_address as doctor_chamber_address,b.service_kol_dsc as service_kol_dsc,b.sl as rxSelfCount, b.sl as rxTotalCount,b.med_self_snv as rxSelfMed, 0 as rxTotalMed FROM sm_level a,`sm_prescription_head` b WHERE a.cid='" + cid + "' and a.depth=3 and a.level_id=b.area_id and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and b.med_self_snv>0 " + condition + ")"
            sql2 = "(SELECT a.level_id as area_id,b.doctor_id as doctor_id,b.doctor_name as doctor_name,b.doctor_speciality as doctor_speciality,b.doctor_chamber_address as doctor_chamber_address,b.service_kol_dsc as service_kol_dsc,0 as rxSelfCount,b.sl as rxTotalCount,0 as rxSelfMed, b.med_total_i_snv as rxTotalMed FROM sm_level a,`sm_prescription_head` b WHERE a.cid='" + cid + "' and a.depth=3 and a.level_id=b.area_id and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' " + condition + ")"

    elif int(identical) == 0:
        if med_division == 'PHARMA':
            sql1 = "(SELECT a.level_id as area_id,b.doctor_id as doctor_id,b.doctor_name as doctor_name,b.doctor_speciality as doctor_speciality,b.doctor_chamber_address as doctor_chamber_address,b.service_kol_dsc as service_kol_dsc,b.sl as rxSelfCount, b.sl as rxTotalCount,(b.med_self+b.med_self_snv) as rxSelfMed, 0 as rxTotalMed FROM sm_level a,`sm_prescription_head` b WHERE a.cid='" + cid + "' and a.depth=3 and a.level_id=b.area_id and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and (b.med_self>0 or b.med_self_snv>0) " + condition + ")"
            sql2 = "(SELECT a.level_id as area_id,b.doctor_id as doctor_id,b.doctor_name as doctor_name,b.doctor_speciality as doctor_speciality,b.doctor_chamber_address as doctor_chamber_address,b.service_kol_dsc as service_kol_dsc,0 as rxSelfCount,sl as rxTotalCount,0 as rxSelfMed, (b.med_total+b.med_total_snv) as rxTotalMed FROM `sm_level` a,`sm_prescription_head` b WHERE a.cid='" + cid + "' and a.depth=3 and a.level_id=b.area_id and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' " + condition + ")"
        elif med_division == 'SINAVISION':
            sql1 = "(SELECT a.level_id as area_id,b.doctor_id as doctor_id,b.doctor_name as doctor_name,b.doctor_speciality as doctor_speciality,b.doctor_chamber_address as doctor_chamber_address,b.service_kol_dsc as service_kol_dsc,b.sl as rxSelfCount, b.sl as rxTotalCount,b.med_self_snv as rxSelfMed, 0 as rxTotalMed FROM sm_level a,`sm_prescription_head` b WHERE a.cid='" + cid + "' and a.depth=3 and a.level_id=b.area_id and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' and b.med_self_snv>0 " + condition + ")"
            sql2 = "(SELECT a.level_id as area_id,b.doctor_id as doctor_id,b.doctor_name as doctor_name,b.doctor_speciality as doctor_speciality,b.doctor_chamber_address as doctor_chamber_address,b.service_kol_dsc as service_kol_dsc,0 as rxSelfCount,b.sl as rxTotalCount,0 as rxSelfMed, b.med_total_snv as rxTotalMed FROM sm_level a,`sm_prescription_head` b WHERE a.cid='" + cid + "' and a.depth=3 and a.level_id=b.area_id and b.submit_date>='" + date_from + "' and b.submit_date<='" + date_to + "' " + condition + ")"

    records = "select area_id,doctor_id,doctor_name,doctor_speciality,doctor_chamber_address,service_kol_dsc,count(distinct(rxSelfCount))-1 as rxSelfCount,count(distinct(rxTotalCount)) as rxTotalCount,sum(rxSelfMed) as rxSelfMed,sum(rxTotalMed) as rxTotalMed from (" + sql1 + " union all " + sql2 + ") p group by area_id,doctor_id;"

    recordList = db.executesql(records, as_dict=True)

    level3List = []
    for i in range(len(recordList)):
        recordListS = recordList[i]
        level3_id = recordListS['area_id']
        if level3_id not in level3List:
            level3List.append(level3_id)

    levelUserList = []
    for j in range(len(level3List)):
        level3_id = level3List[j]

        level3_rep = ''
        qset = db()
        qset = qset(db.sm_rep_area.area_id == level3_id)

        if med_division == 'PHARMA':
            qset = qset(db.sm_rep_area.rep_category == 'A')
        elif med_division == 'SINAVISION':
            qset = qset(db.sm_rep_area.rep_category == 'C')

        repRows = qset.select(db.sm_rep_area.rep_name, orderby=db.sm_rep_area.rep_name)
        for rRow in repRows:
            if level3_rep == '':
                level3_rep = str(rRow.rep_name)
            else:
                level3_rep += ',' + str(rRow.rep_name)

        levelRows = db((db.sm_level.cid == cid) & (db.sm_level.level_id == level3_id)).select(db.sm_level.level0,db.sm_level.level1,db.sm_level.level2,limitby=(0, 1))
        level0_sup = ''
        level1_sup = ''
        level2_sup = ''
        if levelRows:
            level0_id = str(levelRows[0].level0)
            level1_id = str(levelRows[0].level1)
            level2_id = str(levelRows[0].level2)

            supRow0 = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.level_id == level0_id) & (db.sm_supervisor_level.level_depth_no == 0)).select(db.sm_supervisor_level.sup_name,orderby=db.sm_supervisor_level.sup_name)
            for sRow0 in supRow0:
                if level0_sup == '':
                    level0_sup = str(sRow0.sup_name)
                else:
                    level0_sup += ',' + str(sRow0.sup_name)

            supRow1 = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.level_id == level1_id) & (db.sm_supervisor_level.level_depth_no == 1)).select(db.sm_supervisor_level.sup_name,orderby=db.sm_supervisor_level.sup_name)
            for sRow1 in supRow1:
                if level1_sup == '':
                    level1_sup = str(sRow1.sup_name)
                else:
                    level1_sup += ',' + str(sRow1.sup_name)

            supRow2 = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.level_id == level2_id) & (db.sm_supervisor_level.level_depth_no == 2)).select(db.sm_supervisor_level.sup_name,orderby=db.sm_supervisor_level.sup_name)
            for sRow in supRow2:
                if level2_sup == '':
                    level2_sup = str(sRow.sup_name)
                else:
                    level2_sup += ',' + str(sRow.sup_name)

        dicData = {'level3_id': level3_id, 'level3_rep': level3_rep, 'level2_id': level2_id, 'level2_sup': level2_sup,'level1_id': level1_id, 'level1_sup': level1_sup, 'level0_id': level0_id, 'level0_sup': level0_sup}
        levelUserList.append(dicData)

    reg_name = ''
    regionRows = db((db.sm_level.cid == cid) & (db.sm_level.level_id == pr_region)).select(db.sm_level.level_name,limitby=(0, 1))
    if regionRows:
        reg_name = regionRows[0].level_name

    if pr_region == '':
        pr_region = 'National'

    if pr_zone == '':
        pr_zone = 'ALL'

    if pr_area == 'None':
        pr_area = ''

    if pr_territory == 'None':
        pr_territory = ''

    if pr_doctor == 'None':
        pr_doctor = ''

    if pr_ff == 'None':
        pr_ff = ''



    if int(identical)==1:
        identical='Identical Products'
    else:
        identical='All Products'

    myString = 'Physician track2 ' + med_division + ' ' + str(identical) + ' \n'
    myString += 'Date Range:' + ',' + str(date_from) + ' To ' + str(date_to) + '\n'

    if reg_name != '':
        myString += 'Region:' + ',' + str(reg_name) + '\n'

    if pr_zone != '':
        myString += 'ZM:' + ',' + str(pr_zone) + '\n'

    if pr_area != '':
        myString += 'AM:' + ',' + str(pr_area) + '\n'

    if pr_ff!='':
        myString += 'Field Force:' + ',' + str(pr_ff) + '\n'

    if pr_doctor!='':
        myString += 'Doctor:' + ',' + str(pr_doctor) + '\n'

    if kol_doctor!='0':
        if kol_doctor=='1':
            kol_doctor='YES'
        elif kol_doctor=='2':
            kol_doctor = 'NO'

        myString += 'KOL:' + ',' + str(kol_doctor) + '\n'

    myString += '\n'

    slNo = 0
    myString += 'SL,MPO,Phy ID,Physician Name,Specialization,Chamber Address,KOL,Base,IPI,PER(%)' + '\n'

    for i in range(len(recordList)):
        recordListStr = recordList[i]
        slNo += 1
        area_id = recordListStr['area_id']
        doctor_id = recordListStr['doctor_id']
        doctor_name = str(recordListStr['doctor_name']).replace(',',' ')
        doctor_speciality = str(recordListStr['doctor_speciality']).replace(',',' ')
        doctor_chamber_address = str(recordListStr['doctor_chamber_address']).replace(',',' ')
        service_kol_dsc = recordListStr['service_kol_dsc']
        rxTotalMed = recordListStr['rxTotalMed']
        rxSelfMed = recordListStr['rxSelfMed']

        if doctor_chamber_address == 'None':
            doctor_chamber_address = ''


        if service_kol_dsc == 1:
            service_kol_dsc = 'YES'
        elif service_kol_dsc == 2:
            service_kol_dsc = 'NO'
        else:
            service_kol_dsc = ''

        selfMedPrPer = 0
        if int(recordListStr['rxTotalMed']) > 0:
            selfMedPrPer = round((float(recordListStr['rxSelfMed']) / float(recordListStr['rxTotalMed']) * 100), 3)
        else:
            selfMedPrPer = 0

        myString += str(slNo) + ',' + str(area_id) + ',' + str(doctor_id) + ',' + str(doctor_name)+ ',' + str(doctor_speciality)+ ',' + str(doctor_chamber_address)+ ',' + str(service_kol_dsc)+ ',' + str(rxTotalMed)+ ',' + str(rxSelfMed)+ ',' + str(selfMedPrPer) + '\n'

    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=physician_track2.csv'
    return str(myString)

def physician_track2():
    cid=session.cid
    identical=request.vars.identical
    med_division=request.vars.med_division
    
    if med_division=='PHARMA':
        response.title='Physician track2 Pharma'
    elif med_division=='SINAVISION':
        response.title='Physician track2 Sinavision'
        
    date_from=request.vars.date_from
    date_to=request.vars.date_to

    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    pr_doctor=request.vars.pr_doctor
    kol_doctor = request.vars.kol_doctor
    pr_ff=request.vars.pr_ff
    
    
    if pr_region=='None':
        pr_region=''
    
    if pr_zone=='None':
        pr_zone=''
    
    if pr_area=='None':
        pr_area=''
    
    if pr_territory=='None':
        pr_territory=''
    
    if pr_doctor=='None':
        pr_doctor=''
    
    if pr_ff=='None':
        pr_ff=''
    


    condition=''   
    if pr_region!='':
        condition+=" and a.level0 = '" + str(pr_region) + "'"
    if pr_zone!='':
        condition+=" and a.level1 = '" + str(pr_zone) + "'"
    if pr_area!='':
        condition+= " and a.level2 = '" + str(pr_area) + "'"
    if pr_territory!='':
        condition+=" and a.level_id = '" + str(pr_territory) + "'"
    if pr_doctor!='':
        condition+=" and b.doctor_id = '"+str(pr_doctor).split('|')[0]+"'"
    if kol_doctor!='0':
        condition += " and b.service_kol_dsc = " + str(kol_doctor)


    if int(identical)==1:
        if med_division=='PHARMA':
            condition+=" and ( b.update_med_count_flag_i >0 or b.update_med_count_flag_i_snv >0) "
        elif med_division=='SINAVISION':
            condition+=" and b.update_med_count_flag_i_snv >0 "
    elif int(identical)==0:
        if med_division=='PHARMA':
            condition+=" and ( b.update_med_count_flag >0 or b.update_med_count_flag_snv >0) "
        elif med_division=='SINAVISION':
            condition+=" and b.update_med_count_flag_snv >0 "


    sql1=''
    sql2=''
    if int(identical)==1:
        if med_division=='PHARMA':
            sql1="(SELECT a.level_id as area_id,b.doctor_id as doctor_id,b.doctor_name as doctor_name,b.doctor_speciality as doctor_speciality,b.doctor_chamber_address as doctor_chamber_address,b.service_kol_dsc as service_kol_dsc,b.sl as rxSelfCount, b.sl as rxTotalCount,(b.med_self+b.med_self_snv) as rxSelfMed, 0 as rxTotalMed FROM `sm_level` a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.level_id=b.area_id and b.submit_date>='"+date_from+"' and b.submit_date<='"+date_to+"' and (b.med_self>0 or b.med_self_snv>0) "+condition+")"
            sql2="(SELECT a.level_id as area_id,b.doctor_id as doctor_id,b.doctor_name as doctor_name,b.doctor_speciality as doctor_speciality,b.doctor_chamber_address as doctor_chamber_address,b.service_kol_dsc as service_kol_dsc,0 as rxSelfCount,sl as rxTotalCount,0 as rxSelfMed, (b.med_total_i+b.med_total_i_snv) as rxTotalMed FROM `sm_level` a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.level_id=b.area_id and b.submit_date>='"+date_from+"' and b.submit_date<='"+date_to+"' "+condition+")"
        elif med_division=='SINAVISION':
            sql1="(SELECT a.level_id as area_id,b.doctor_id as doctor_id,b.doctor_name as doctor_name,b.doctor_speciality as doctor_speciality,b.doctor_chamber_address as doctor_chamber_address,b.service_kol_dsc as service_kol_dsc,b.sl as rxSelfCount, b.sl as rxTotalCount,b.med_self_snv as rxSelfMed, 0 as rxTotalMed FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.level_id=b.area_id and b.submit_date>='"+date_from+"' and b.submit_date<='"+date_to+"' and b.med_self_snv>0 "+condition+")"
            sql2="(SELECT a.level_id as area_id,b.doctor_id as doctor_id,b.doctor_name as doctor_name,b.doctor_speciality as doctor_speciality,b.doctor_chamber_address as doctor_chamber_address,b.service_kol_dsc as service_kol_dsc,0 as rxSelfCount,b.sl as rxTotalCount,0 as rxSelfMed, b.med_total_i_snv as rxTotalMed FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.level_id=b.area_id and b.submit_date>='"+date_from+"' and b.submit_date<='"+date_to+"' "+condition+")"

    elif int(identical)==0:
        if med_division=='PHARMA':
            sql1="(SELECT a.level_id as area_id,b.doctor_id as doctor_id,b.doctor_name as doctor_name,b.doctor_speciality as doctor_speciality,b.doctor_chamber_address as doctor_chamber_address,b.service_kol_dsc as service_kol_dsc,b.sl as rxSelfCount, b.sl as rxTotalCount,(b.med_self+b.med_self_snv) as rxSelfMed, 0 as rxTotalMed FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.level_id=b.area_id and b.submit_date>='"+date_from+"' and b.submit_date<='"+date_to+"' and (b.med_self>0 or b.med_self_snv>0) "+condition+")"
            sql2="(SELECT a.level_id as area_id,b.doctor_id as doctor_id,b.doctor_name as doctor_name,b.doctor_speciality as doctor_speciality,b.doctor_chamber_address as doctor_chamber_address,b.service_kol_dsc as service_kol_dsc,0 as rxSelfCount,sl as rxTotalCount,0 as rxSelfMed, (b.med_total+b.med_total_snv) as rxTotalMed FROM `sm_level` a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.level_id=b.area_id and b.submit_date>='"+date_from+"' and b.submit_date<='"+date_to+"' "+condition+")"
        elif med_division=='SINAVISION':
            sql1="(SELECT a.level_id as area_id,b.doctor_id as doctor_id,b.doctor_name as doctor_name,b.doctor_speciality as doctor_speciality,b.doctor_chamber_address as doctor_chamber_address,b.service_kol_dsc as service_kol_dsc,b.sl as rxSelfCount, b.sl as rxTotalCount,b.med_self_snv as rxSelfMed, 0 as rxTotalMed FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.level_id=b.area_id and b.submit_date>='"+date_from+"' and b.submit_date<='"+date_to+"' and b.med_self_snv>0 "+condition+")"
            sql2="(SELECT a.level_id as area_id,b.doctor_id as doctor_id,b.doctor_name as doctor_name,b.doctor_speciality as doctor_speciality,b.doctor_chamber_address as doctor_chamber_address,b.service_kol_dsc as service_kol_dsc,0 as rxSelfCount,b.sl as rxTotalCount,0 as rxSelfMed, b.med_total_snv as rxTotalMed FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.level_id=b.area_id and b.submit_date>='"+date_from+"' and b.submit_date<='"+date_to+"' "+condition+")"

    records="select area_id,doctor_id,doctor_name,doctor_speciality,doctor_chamber_address,service_kol_dsc,count(distinct(rxSelfCount))-1 as rxSelfCount,count(distinct(rxTotalCount)) as rxTotalCount,sum(rxSelfMed) as rxSelfMed,sum(rxTotalMed) as rxTotalMed from ("+sql1+" union all "+sql2+") p group by area_id,doctor_id;"
    
    recordList=db.executesql(records,as_dict=True)
    
    level3List=[]
    for i in range(len(recordList)):
        recordListS=recordList[i]
        level3_id=recordListS['area_id'] 
        if level3_id not in level3List:
            level3List.append(level3_id)
    
    levelUserList=[]
    for j in range(len(level3List)):        
        level3_id=level3List[j]
        
        level3_rep=''
        qset=db()
        qset=qset(db.sm_rep_area.area_id == level3_id)
        
        if med_division=='PHARMA':
            qset=qset(db.sm_rep_area.rep_category == 'A')
        elif med_division=='SINAVISION':
            qset=qset(db.sm_rep_area.rep_category == 'C')
            
        repRows=qset.select(db.sm_rep_area.rep_name,orderby=db.sm_rep_area.rep_name)
        for rRow in repRows:
            if level3_rep=='':
                level3_rep=str(rRow.rep_name)
            else:
                level3_rep+=','+str(rRow.rep_name)
        
        levelRows=db((db.sm_level.cid == cid)&(db.sm_level.level_id == level3_id)).select(db.sm_level.level0,db.sm_level.level1,db.sm_level.level2,limitby=(0,1))
        level0_sup=''
        level1_sup=''
        level2_sup=''
        if levelRows:
            level0_id=str(levelRows[0].level0)
            level1_id=str(levelRows[0].level1)
            level2_id=str(levelRows[0].level2)
            
            supRow0=db((db.sm_supervisor_level.cid == cid)&(db.sm_supervisor_level.level_id == level0_id)&(db.sm_supervisor_level.level_depth_no == 0)).select(db.sm_supervisor_level.sup_name,orderby=db.sm_supervisor_level.sup_name)
            for sRow0 in supRow0:
                if level0_sup=='':
                    level0_sup=str(sRow0.sup_name)
                else:
                    level0_sup+=','+str(sRow0.sup_name)
            
            supRow1=db((db.sm_supervisor_level.cid == cid)&(db.sm_supervisor_level.level_id == level1_id)&(db.sm_supervisor_level.level_depth_no == 1)).select(db.sm_supervisor_level.sup_name,orderby=db.sm_supervisor_level.sup_name)
            for sRow1 in supRow1:
                if level1_sup=='':
                    level1_sup=str(sRow1.sup_name)
                else:
                    level1_sup+=','+str(sRow1.sup_name)
            
            supRow2=db((db.sm_supervisor_level.cid == cid)&(db.sm_supervisor_level.level_id == level2_id)&(db.sm_supervisor_level.level_depth_no == 2)).select(db.sm_supervisor_level.sup_name,orderby=db.sm_supervisor_level.sup_name)
            for sRow in supRow2:
                if level2_sup=='':
                    level2_sup=str(sRow.sup_name)
                else:
                    level2_sup+=','+str(sRow.sup_name)
                        
        dicData={'level3_id':level3_id,'level3_rep':level3_rep,'level2_id':level2_id,'level2_sup':level2_sup,'level1_id':level1_id,'level1_sup':level1_sup,'level0_id':level0_id,'level0_sup':level0_sup}
        levelUserList.append(dicData)
    
    reg_name=''
    regionRows=db((db.sm_level.cid==cid)&(db.sm_level.level_id==pr_region)).select(db.sm_level.level_name,limitby=(0,1))
    if regionRows:
        reg_name=regionRows[0].level_name
        
    return dict(identical=identical,med_division=med_division,levelUserList=levelUserList,recordList=recordList,date_from=date_from,date_to=date_to,pr_region=pr_region,reg_name=reg_name,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,pr_doctor=pr_doctor,kol_doctor=kol_doctor,pr_ff=pr_ff)


#========== report block 1

def corp_share_by_brand():
    cid=session.cid
    identical=request.vars.identical
    med_division=request.vars.med_division

    if med_division=='PHARMA':
        response.title='Corporate Share by Brand Pharma'
    elif med_division=='SINAVISION':
        response.title='Corporate Share by Brand Sinavision'


    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory


    if pr_region=='None':
        pr_region=''

    if pr_zone=='None':
        pr_zone=''

    if pr_area=='None':
        pr_area=''

    if pr_territory=='None':
        pr_territory=''


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
    regionRows=db((db.sm_level.cid==cid)&(db.sm_level.level_id==pr_region)).select(db.sm_level.level_name,limitby=(0,1))
    if regionRows:
        reg_name=regionRows[0].level_name


    # condition1=''
    # if pr_region!='':
    #     condition1+=" and level0 = '"+str(pr_region)+"'"
    # if pr_zone!='':
    #     condition1+=" and level1 = '"+str(pr_zone)+"'"
    # if pr_area!='':
    #     condition1+=" and level2 = '"+str(pr_area)+"'"
    # if pr_territory!='':
    #     condition1+=" and level_id = '"+str(pr_territory)+"'"



    # sql="select group_concat(level_id) as level_id_list from sm_level where cid='"+cid+"' and depth=3 "+condition1+" group by cid"
    # level_id_row=db.executesql(sql,as_dict=True)
    #
    # level_id=''
    # for i in range(len(level_id_row)):
    #     level_id_s=level_id_row[i]
    #     level_id=level_id_s['level_id_list']
    #
    # level_id_str=''
    # level_id_str="'"+level_id.replace(',',"','")+"'"

    if med_division=='SINAVISION':
        med_division='SV'

    condition2=''
    if int(identical)==1:
        condition2+=" and dept='"+med_division+"' and identical='"+identical+"'"
    else:
        condition2+=" and dept='"+med_division+"'"


    # if level_id_str!='':
    #     condition2+=" and area_id in ("+level_id_str+") "

    sql1=''
    sql2=''

    sql3=''
    sql4=''

    med_total1='0'
    med_total2='0'
    sql1="(SELECT count(id) as med_total1 FROM `sm_prescription_details` WHERE cid='"+cid+"' and submit_date>='"+date_from_1+"' and submit_date<='"+date_to_1+"' and update_flag=2 "+condition2+" group by cid)"
    recordList1=db.executesql(sql1,as_dict=True)
    for i in range(len(recordList1)):
        recordList1s=recordList1[i]
        med_total1=str(recordList1s['med_total1'])

    sql2="(SELECT count(id) as med_total2 FROM `sm_prescription_details` WHERE cid='"+cid+"' and submit_date>='"+date_from_2+"' and submit_date<='"+date_to_2+"' and update_flag=2 "+condition2+" group by cid)"
    recordList2=db.executesql(sql2,as_dict=True)
    for i in range(len(recordList2)):
        recordList2s=recordList2[i]
        med_total2=str(recordList2s['med_total2'])

    #return str(sql1)+'....'+str(sql2)
    #return str(med_total1)+'....'+str(med_total2)
    sql3="(SELECT company,1 as med_self1, 0 as med_self2 FROM `sm_prescription_details` WHERE cid='"+cid+"' and submit_date>='"+date_from_1+"' and submit_date<='"+date_to_1+"' and update_flag=2 "+condition2+")"
    sql4="(SELECT company,0 as med_self1,1 as med_self2 FROM `sm_prescription_details` WHERE cid='"+cid+"' and submit_date>='"+date_from_2+"' and submit_date<='"+date_to_2+"' and update_flag=2 "+condition2+")"

    records0="select company, sum(med_self1) as med_self1,"+med_total1+" as med_total1,round((sum(med_self1)/"+med_total1+")*100,2) as perP1, sum(med_self2) as med_self2, "+med_total2+" as med_total2,round((sum(med_self2)/"+med_total2+")*100,2) as perP2, round((((sum(med_self2)/"+med_total2+")*100)-((sum(med_self1)/"+med_total1+")*100))/((sum(med_self1)/"+med_total1+")*100)*100,2) as growth from ("+sql3+" union all "+sql4+") p group by company order by round((sum(med_self2)/"+med_total2+")*100,2) desc;"

    recordList0=db.executesql(records0,as_dict=True)


    return dict(identical=identical,med_division=med_division,pr_year1=pr_year1,pr_year2=pr_year2,pr_quarter1=pr_quarter1,pr_quarter2=pr_quarter2,pr_month1=pr_month1,pr_month2=pr_month2,pr_cycle1=pr_cycle1,pr_cycle2=pr_cycle2,recordList0=recordList0,pr_region=pr_region,reg_name=reg_name,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2)


def institute_track2():
    cid=session.cid
    identical=request.vars.identical
    med_division=request.vars.med_division

    if med_division=='PHARMA':
        response.title='Institute track2 Pharma'
    elif med_division=='SINAVISION':
        response.title='Institute track2 Sinavision'


    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory


    if pr_region=='None':
        pr_region=''

    if pr_zone=='None':
        pr_zone=''

    if pr_area=='None':
        pr_area=''

    if pr_territory=='None':
        pr_territory=''


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
    regionRows=db((db.sm_level.cid==cid)&(db.sm_level.level_id==pr_region)).select(db.sm_level.level_name,limitby=(0,1))
    if regionRows:
        reg_name=regionRows[0].level_name


    condition1=''
    if pr_region!='':
        condition1+=" and a.level0 = '"+str(pr_region)+"'"
    if pr_zone!='':
        condition1+=" and a.level1 = '"+str(pr_zone)+"'"
    if pr_area!='':
        condition1+=" and a.level2 = '"+str(pr_area)+"'"
    if pr_territory!='':
        condition1+=" and a.level3 = '"+str(pr_territory)+"'"

    if int(identical)==1:
        if med_division=='PHARMA':
            condition1+=" and ( b.update_med_count_flag_i >0 or b.update_med_count_flag_i_snv >0) "
        elif med_division=='SINAVISION':
            condition1+=" and b.update_med_count_flag_i_snv >0 "
    elif int(identical)==0:
        if med_division=='PHARMA':
            condition1+=" and ( b.update_med_count_flag >0 or b.update_med_count_flag_snv >0) "
        elif med_division=='SINAVISION':
            condition1+=" and b.update_med_count_flag_snv >0 "

    condition1+=" and b.doctor_category = 'INSTITUTE'"

    sql1=''
    sql2=''
    if int(identical)==1:
        if med_division=='PHARMA':
            sql1="(SELECT a.cid as cid,a.level0 as zone_id,a.level0_name as zone_name,a.level1 as reg_id,a.level1_name as reg_name,a.level2 as tl_id,a.level2_name as tl_name,a.level_id as area_id,a.level_name as area_name,b.doctor_inst as doctor_inst,'' as level0_sup_id,'' as level0_sup_name,'' as level1_sup_id,'' as level1_sup_name,'' as level2_sup_id,'' as level2_sup_name,'' as level3_sup_id,'' as level3_sup_name,b.sl as rxCount1,0 as rxCount2,(b.med_self+b.med_self_snv) as med_self1,(b.med_total_i+b.med_total_i_snv) as med_total1, 0 as med_self2, 0 as med_total2 FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.cid=b.cid and a.level_id=b.area_id and b.submit_date>='"+date_from_1+"' and b.submit_date<='"+date_to_1+"'"+condition1+")"
            sql2="(SELECT a.cid as cid,a.level0 as zone_id,a.level0_name as zone_name,a.level1 as reg_id,a.level1_name as reg_name,a.level2 as tl_id,a.level2_name as tl_name,a.level_id as area_id,a.level_name as area_name,b.doctor_inst as doctor_inst,'' as level0_sup_id,'' as level0_sup_name,'' as level1_sup_id,'' as level1_sup_name,'' as level2_sup_id,'' as level2_sup_name,'' as level3_sup_id,'' as level3_sup_name,0 as rxCount1,b.sl as rxCount2,0 as med_self1, 0 as med_total1,(b.med_self+b.med_self_snv) as med_self2,(b.med_total_i+b.med_total_i_snv) as total2 FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.cid=b.cid and a.level_id=b.area_id and b.submit_date>='"+date_from_2+"' and b.submit_date<='"+date_to_2+"'"+condition1+")"

        elif med_division=='SINAVISION':
            sql1="(SELECT a.cid as cid,a.level0 as zone_id,a.level0_name as zone_name,a.level1 as reg_id,a.level1_name as reg_name,a.level2 as tl_id,a.level2_name as tl_name,a.level_id as area_id,a.level_name as area_name,b.doctor_inst as doctor_inst,'' as level0_sup_id,'' as level0_sup_name,'' as level1_sup_id,'' as level1_sup_name,'' as level2_sup_id,'' as level2_sup_name,'' as level3_sup_id,'' as level3_sup_name,b.sl as rxCount1,0 as rxCount2, b.med_self_snv as med_self1,b.med_total_i_snv as med_total1, 0 as med_self2, 0 as med_total2 FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.level_id=b.area_id and  b.submit_date>='"+date_from_1+"' and b.submit_date<='"+date_to_1+"' "+condition1+")"
            sql2="(SELECT a.cid as cid,a.level0 as zone_id,a.level0_name as zone_name,a.level1 as reg_id,a.level1_name as reg_name,a.level2 as tl_id,a.level2_name as tl_name,a.level_id as area_id,a.level_name as area_name,b.doctor_inst as doctor_inst,'' as level0_sup_id,'' as level0_sup_name,'' as level1_sup_id,'' as level1_sup_name,'' as level2_sup_id,'' as level2_sup_name,'' as level3_sup_id,'' as level3_sup_name,0 as rxCount1,b.sl as rxCount2,0 as med_self1, 0 as med_total1,b.med_self_snv as med_self2,b.med_total_i_snv as total2 FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.level_id=b.area_id and b.submit_date>='"+date_from_2+"' and b.submit_date<='"+date_to_2+"' "+condition1+")"

    elif int(identical)==0:
        if med_division=='PHARMA':
            sql1="(SELECT a.cid as cid,a.level0 as zone_id,a.level0_name as zone_name,a.level1 as reg_id,a.level1_name as reg_name,a.level2 as tl_id,a.level2_name as tl_name,a.level_id as area_id,a.level_name as area_name,b.doctor_inst as doctor_inst,'' as level0_sup_id,'' as level0_sup_name,'' as level1_sup_id,'' as level1_sup_name,'' as level2_sup_id,'' as level2_sup_name,'' as level3_sup_id,'' as level3_sup_name,b.sl as rxCount1,0 as rxCount2,(b.med_self+b.med_self_snv) as med_self1,(b.med_total+b.med_total_snv) as med_total1, 0 as med_self2, 0 as med_total2 FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.cid=b.cid and a.level_id=b.area_id and b.submit_date>='"+date_from_1+"' and b.submit_date<='"+date_to_1+"'"+condition1+")"
            sql2="(SELECT a.cid as cid,a.level0 as zone_id,a.level0_name as zone_name,a.level1 as reg_id,a.level1_name as reg_name,a.level2 as tl_id,a.level2_name as tl_name,a.level_id as area_id,a.level_name as area_name,b.doctor_inst as doctor_inst,'' as level0_sup_id,'' as level0_sup_name,'' as level1_sup_id,'' as level1_sup_name,'' as level2_sup_id,'' as level2_sup_name,'' as level3_sup_id,'' as level3_sup_name,0 as rxCount1,b.sl as rxCount2,0 as med_self1, 0 as med_total1,(b.med_self+b.med_self_snv) as med_self2,(b.med_total+b.med_total_snv) as total2 FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.cid=b.cid and a.level_id=b.area_id and b.submit_date>='"+date_from_2+"' and b.submit_date<='"+date_to_2+"'"+condition1+")"

        elif med_division=='SINAVISION':
            sql1="(SELECT a.cid as cid,a.level0 as zone_id,a.level0_name as zone_name,a.level1 as reg_id,a.level1_name as reg_name,a.level2 as tl_id,a.level2_name as tl_name,a.level_id as area_id,a.level_name as area_name,b.doctor_inst as doctor_inst,'' as level0_sup_id,'' as level0_sup_name,'' as level1_sup_id,'' as level1_sup_name,'' as level2_sup_id,'' as level2_sup_name,'' as level3_sup_id,'' as level3_sup_name,b.sl as rxCount1,0 as rxCount2, b.med_self_snv as med_self1,b.med_total_snv as med_total1, 0 as med_self2, 0 as med_total2 FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.level_id=b.area_id and  b.submit_date>='"+date_from_1+"' and b.submit_date<='"+date_to_1+"' "+condition1+")"
            sql2="(SELECT a.cid as cid,a.level0 as zone_id,a.level0_name as zone_name,a.level1 as reg_id,a.level1_name as reg_name,a.level2 as tl_id,a.level2_name as tl_name,a.level_id as area_id,a.level_name as area_name,b.doctor_inst as doctor_inst,'' as level0_sup_id,'' as level0_sup_name,'' as level1_sup_id,'' as level1_sup_name,'' as level2_sup_id,'' as level2_sup_name,'' as level3_sup_id,'' as level3_sup_name,0 as rxCount1,b.sl as rxCount2,0 as med_self1, 0 as med_total1,b.med_self_snv as med_self2,b.med_total_snv as total2 FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.level_id=b.area_id and b.submit_date>='"+date_from_2+"' and b.submit_date<='"+date_to_2+"' "+condition1+")"

    records0="select cid,zone_id,zone_name,level0_sup_id,level0_sup_name,doctor_inst,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by cid,doctor_inst;"
    recordList0=db.executesql(records0,as_dict=True)

    records1="select zone_id,reg_id,reg_name,level1_sup_id,level1_sup_name,doctor_inst,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,doctor_inst;"
    recordList1=db.executesql(records1,as_dict=True)

    recordListH0 = []
    zone_id_list = []
    for i in range(len(recordList0)):
        recordList0s = recordList0[i]
        zone_id = recordList0s['zone_id']

        if zone_id not in zone_id_list:
            dict_data = {'zone_id': zone_id}
            recordListH0.append(dict_data)
            zone_id_list.append(zone_id)

    # recordListH0=[]
    # for i in range(len(recordList0)):
    #     recordList0s=recordList0[i]
    #     zone_id=recordList0s['zone_id']
    #
    #     if len(recordListH0)==0:
    #         dict_data={'zone_id':zone_id}
    #         recordListH0.append(dict_data)
    #     else:
    #         for k in range(len(recordListH0)):
    #             recordListH0s=recordListH0[k]
    #             zone_id_1=recordListH0s['zone_id']
    #             if zone_id_1!=zone_id:
    #                 dict_data={'zone_id':zone_id}
    #                 recordListH0.append(dict_data)


    # recordsH0="select zone_id,level0_sup_id,level0_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id order by zone_id;"
    # recordListH0=db.executesql(recordsH0,as_dict=True)

    recordListH1=[]
    recordListH1=recordListH0

    # recordListH1=[]
    # recordsH1="select zone_id,level0_sup_id,level0_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id order by zone_id;"
    # recordListH1=db.executesql(recordsH1,as_dict=True)


    recordList2=[]
    records2="select zone_id,reg_id,tl_id,tl_name,level2_sup_id,level2_sup_name,doctor_inst,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id order by zone_id,reg_id,tl_id,doctor_inst;"
    recordList2=db.executesql(records2,as_dict=True)

    recordListH2 = []
    reg_id_list = []
    for i in range(len(recordList2)):
        recordList2s = recordList2[i]
        zone_id = recordList2s['zone_id']
        reg_id = recordList2s['reg_id']

        if reg_id not in reg_id_list:
            dict_data = {'zone_id': zone_id, 'reg_id': reg_id}
            recordListH2.append(dict_data)
            reg_id_list.append(reg_id)

    # recordListH2=[]
    # for i in range(len(recordList2)):
    #     recordList2s=recordList2[i]
    #     zone_id=recordList2s['zone_id']
    #     reg_id=recordList2s['reg_id']
    #     tl_id=recordList2s['tl_id']
    #
    #     if len(recordListH2)==0:
    #         dict_data={'zone_id':zone_id,'reg_id':reg_id,'tl_id':tl_id}
    #         recordListH2.append(dict_data)
    #     else:
    #         for k in range(len(recordListH2)):
    #             recordListH2s=recordListH2[k]
    #             zone_id_1=recordListH2s['zone_id']
    #             reg_id_1=recordListH2s['reg_id']
    #             tl_id_1=recordListH2s['tl_id']
    #             if zone_id_1==zone_id and reg_id_1==reg_id and tl_id_1!=tl_id:
    #                 dict_data={'zone_id':zone_id,'reg_id':reg_id,'tl_id':tl_id}
    #                 recordListH2.append(dict_data)


    # recordsH2="select zone_id,reg_id,level0_sup_id,level0_sup_name,level1_sup_id,level1_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id;"
    # recordListH2=db.executesql(recordsH2,as_dict=True)

    recordList3=[]
    records3="select zone_id,reg_id,tl_id,area_id,area_name,level3_sup_id,level3_sup_name,doctor_inst,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id,area_id order by zone_id,reg_id,tl_id,area_id,doctor_inst;"
    recordList3=db.executesql(records3,as_dict=True)

    recordListH3 = []
    tl_id_list = []
    for i in range(len(recordList3)):
        recordList3s = recordList3[i]
        zone_id = recordList3s['zone_id']
        reg_id = recordList3s['reg_id']
        tl_id = recordList3s['tl_id']

        if tl_id not in tl_id_list:
            dict_data = {'zone_id': zone_id, 'reg_id': reg_id, 'tl_id': tl_id}
            recordListH3.append(dict_data)
            tl_id_list.append(tl_id)

    # recordListH3=[]
    # for i in range(len(recordList3)):
    #     recordList3s=recordList3[i]
    #     zone_id=recordList3s['zone_id']
    #     reg_id=recordList3s['reg_id']
    #     tl_id=recordList3s['tl_id']
    #     area_id=recordList3s['area_id']
    #
    #     if len(recordListH3)==0:
    #         dict_data={'zone_id':zone_id,'reg_id':reg_id,'tl_id':tl_id,'area_id':area_id}
    #         recordListH3.append(dict_data)
    #     else:
    #         for k in range(len(recordListH3)):
    #             recordListH3s=recordListH3[k]
    #             zone_id_1=recordListH3s['zone_id']
    #             reg_id_1=recordListH3s['reg_id']
    #             tl_id_1=recordListH3s['tl_id']
    #             area_id_1=recordListH3s['area_id']
    #             if zone_id_1==zone_id and reg_id_1==reg_id and tl_id_1==tl_id and area_id_1!=area_id:
    #                 dict_data={'zone_id':zone_id,'reg_id':reg_id,'tl_id':tl_id,'area_id':area_id}
    #                 recordListH3.append(dict_data)

    # recordListH3=[]
    # recordsH3="select zone_id,reg_id,tl_id,level2_sup_id,level2_sup_name,level1_sup_id,level1_sup_name,level0_sup_id,level0_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id order by zone_id,reg_id,tl_id;"
    # recordListH3=db.executesql(recordsH3,as_dict=True)

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
    if med_division=='PHARMA':
        supListH3="select area_id,rep_id,rep_name from sm_rep_area where cid='"+cid+"' and rep_category!='C' order by area_id;"
    elif med_division=='SINAVISION':
        supListH3="select area_id,rep_id,rep_name from sm_rep_area where cid='"+cid+"' and rep_category='C' order by area_id;"

    supListH3=db.executesql(supListH3,as_dict=True)

    return dict(identical=identical,med_division=med_division,supListH3=supListH3,supListH2=supListH2,supListH1=supListH1,supListH0=supListH0,pr_year1=pr_year1,pr_year2=pr_year2,pr_quarter1=pr_quarter1,pr_quarter2=pr_quarter2,pr_month1=pr_month1,pr_month2=pr_month2,pr_cycle1=pr_cycle1,pr_cycle2=pr_cycle2,recordListH3=recordListH3,recordList3=recordList3,recordListH2=recordListH2,recordList2=recordList2,recordListH1=recordListH1,recordList1=recordList1,recordListH0=recordListH0,recordList0=recordList0,pr_region=pr_region,reg_name=reg_name,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2)

def company_track2_rm():
    cid=session.cid
    identical=request.vars.identical
    med_division=request.vars.med_division
    
    if med_division=='PHARMA':
        response.title='Company track2 RM Pharma'
    elif med_division=='SINAVISION':
        response.title='Company track2 RM Sinavision'
        
     
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    
        
    if pr_region=='None':
        pr_region=''
    
    if pr_zone=='None':
        pr_zone=''
    
    if pr_area=='None':
        pr_area=''
    
    if pr_territory=='None':
        pr_territory=''
    
        
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
    regionRows=db((db.sm_level.cid==cid)&(db.sm_level.level_id==pr_region)).select(db.sm_level.level_name,limitby=(0,1))
    if regionRows:
        reg_name=regionRows[0].level_name
    

    condition1=''    
    if pr_region!='':
        condition1+=" and a.level0 = '"+str(pr_region)+"'"
    if pr_zone!='':
        condition1+=" and a.level1 = '"+str(pr_zone)+"'"
    if pr_area!='':
        condition1+=" and a.level2 = '"+str(pr_area)+"'"
    if pr_territory!='':
        condition1+=" and a.level3 = '"+str(pr_territory)+"'"

    if int(identical)==1:
        if med_division=='PHARMA':
            condition1+=" and ( b.update_med_count_flag_i >0 or b.update_med_count_flag_i_snv >0) "
        elif med_division=='SINAVISION':
            condition1+=" and b.update_med_count_flag_i_snv >0 "
    elif int(identical)==0:
        if med_division=='PHARMA':
            condition1+=" and ( b.update_med_count_flag >0 or b.update_med_count_flag_snv >0) "
        elif med_division=='SINAVISION':
            condition1+=" and b.update_med_count_flag_snv >0 "


    sql1=''
    sql2=''
    if int(identical)==1:
        if med_division=='PHARMA':
            sql1="(SELECT a.cid as cid,a.level0 as zone_id,a.level0_name as zone_name,a.level1 as reg_id,a.level1_name as reg_name,a.level2 as tl_id,a.level2_name as tl_name,a.level_id as area_id,a.level_name as area_name,'' as level0_sup_id,'' as level0_sup_name,'' as level1_sup_id,'' as level1_sup_name,'' as level2_sup_id,'' as level2_sup_name,'' as level3_sup_id,'' as level3_sup_name,b.sl as rxCount1,0 as rxCount2,(b.med_self+b.med_self_snv) as med_self1,(b.med_total_i+b.med_total_i_snv) as med_total1, 0 as med_self2, 0 as med_total2 FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.cid=b.cid and a.level_id=b.area_id and b.submit_date>='"+date_from_1+"' and b.submit_date<='"+date_to_1+"'"+condition1+")"
            sql2="(SELECT a.cid as cid,a.level0 as zone_id,a.level0_name as zone_name,a.level1 as reg_id,a.level1_name as reg_name,a.level2 as tl_id,a.level2_name as tl_name,a.level_id as area_id,a.level_name as area_name,'' as level0_sup_id,'' as level0_sup_name,'' as level1_sup_id,'' as level1_sup_name,'' as level2_sup_id,'' as level2_sup_name,'' as level3_sup_id,'' as level3_sup_name,0 as rxCount1,b.sl as rxCount2,0 as med_self1, 0 as med_total1,(b.med_self+b.med_self_snv) as med_self2,(b.med_total_i+b.med_total_i_snv) as total2 FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.cid=b.cid and a.level_id=b.area_id and b.submit_date>='"+date_from_2+"' and b.submit_date<='"+date_to_2+"'"+condition1+")"

        elif med_division=='SINAVISION':
            sql1="(SELECT a.cid as cid,a.level0 as zone_id,a.level0_name as zone_name,a.level1 as reg_id,a.level1_name as reg_name,a.level2 as tl_id,a.level2_name as tl_name,a.level_id as area_id,a.level_name as area_name,'' as level0_sup_id,'' as level0_sup_name,'' as level1_sup_id,'' as level1_sup_name,'' as level2_sup_id,'' as level2_sup_name,'' as level3_sup_id,'' as level3_sup_name,b.sl as rxCount1,0 as rxCount2, b.med_self_snv as med_self1,b.med_total_i_snv as med_total1, 0 as med_self2, 0 as med_total2 FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.level_id=b.area_id and  b.submit_date>='"+date_from_1+"' and b.submit_date<='"+date_to_1+"' "+condition1+")"
            sql2="(SELECT a.cid as cid,a.level0 as zone_id,a.level0_name as zone_name,a.level1 as reg_id,a.level1_name as reg_name,a.level2 as tl_id,a.level2_name as tl_name,a.level_id as area_id,a.level_name as area_name,'' as level0_sup_id,'' as level0_sup_name,'' as level1_sup_id,'' as level1_sup_name,'' as level2_sup_id,'' as level2_sup_name,'' as level3_sup_id,'' as level3_sup_name,0 as rxCount1,b.sl as rxCount2,0 as med_self1, 0 as med_total1,b.med_self_snv as med_self2,b.med_total_i_snv as total2 FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.level_id=b.area_id and b.submit_date>='"+date_from_2+"' and b.submit_date<='"+date_to_2+"' "+condition1+")"

    elif int(identical)==0:
        if med_division=='PHARMA':
            sql1="(SELECT a.cid as cid,a.level0 as zone_id,a.level0_name as zone_name,a.level1 as reg_id,a.level1_name as reg_name,a.level2 as tl_id,a.level2_name as tl_name,a.level_id as area_id,a.level_name as area_name,'' as level0_sup_id,'' as level0_sup_name,'' as level1_sup_id,'' as level1_sup_name,'' as level2_sup_id,'' as level2_sup_name,'' as level3_sup_id,'' as level3_sup_name,b.sl as rxCount1,0 as rxCount2,(b.med_self+b.med_self_snv) as med_self1,(b.med_total+b.med_total_snv) as med_total1, 0 as med_self2, 0 as med_total2 FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.cid=b.cid and a.level_id=b.area_id and b.submit_date>='"+date_from_1+"' and b.submit_date<='"+date_to_1+"'"+condition1+")"
            sql2="(SELECT a.cid as cid,a.level0 as zone_id,a.level0_name as zone_name,a.level1 as reg_id,a.level1_name as reg_name,a.level2 as tl_id,a.level2_name as tl_name,a.level_id as area_id,a.level_name as area_name,'' as level0_sup_id,'' as level0_sup_name,'' as level1_sup_id,'' as level1_sup_name,'' as level2_sup_id,'' as level2_sup_name,'' as level3_sup_id,'' as level3_sup_name,0 as rxCount1,b.sl as rxCount2,0 as med_self1, 0 as med_total1,(b.med_self+b.med_self_snv) as med_self2,(b.med_total+b.med_total_snv) as total2 FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.cid=b.cid and a.level_id=b.area_id and b.submit_date>='"+date_from_2+"' and b.submit_date<='"+date_to_2+"'"+condition1+")"

        elif med_division=='SINAVISION':
            sql1="(SELECT a.cid as cid,a.level0 as zone_id,a.level0_name as zone_name,a.level1 as reg_id,a.level1_name as reg_name,a.level2 as tl_id,a.level2_name as tl_name,a.level_id as area_id,a.level_name as area_name,'' as level0_sup_id,'' as level0_sup_name,'' as level1_sup_id,'' as level1_sup_name,'' as level2_sup_id,'' as level2_sup_name,'' as level3_sup_id,'' as level3_sup_name,b.sl as rxCount1,0 as rxCount2, b.med_self_snv as med_self1,b.med_total_snv as med_total1, 0 as med_self2, 0 as med_total2 FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.level_id=b.area_id and  b.submit_date>='"+date_from_1+"' and b.submit_date<='"+date_to_1+"' "+condition1+")"
            sql2="(SELECT a.cid as cid,a.level0 as zone_id,a.level0_name as zone_name,a.level1 as reg_id,a.level1_name as reg_name,a.level2 as tl_id,a.level2_name as tl_name,a.level_id as area_id,a.level_name as area_name,'' as level0_sup_id,'' as level0_sup_name,'' as level1_sup_id,'' as level1_sup_name,'' as level2_sup_id,'' as level2_sup_name,'' as level3_sup_id,'' as level3_sup_name,0 as rxCount1,b.sl as rxCount2,0 as med_self1, 0 as med_total1,b.med_self_snv as med_self2,b.med_total_snv as total2 FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.level_id=b.area_id and b.submit_date>='"+date_from_2+"' and b.submit_date<='"+date_to_2+"' "+condition1+")"


    records0="select cid,zone_id,zone_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by cid,zone_id;"
    recordList0=db.executesql(records0,as_dict=True)


    #sup list
    supListH0=[]
    supListH0="select level_id,sup_id as level0_sup_id,sup_name as level0_sup_name from sm_supervisor_level where cid='"+cid+"' and level_depth_no=0 order by level_id;"
    supListH0=db.executesql(supListH0,as_dict=True)
    
    return dict(identical=identical,med_division=med_division,supListH0=supListH0,pr_year1=pr_year1,pr_year2=pr_year2,pr_quarter1=pr_quarter1,pr_quarter2=pr_quarter2,pr_month1=pr_month1,pr_month2=pr_month2,pr_cycle1=pr_cycle1,pr_cycle2=pr_cycle2,recordList0=recordList0,pr_region=pr_region,reg_name=reg_name,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2)


def company_track2():
    cid=session.cid
    identical=request.vars.identical
    med_division=request.vars.med_division
    
    if med_division=='PHARMA':
        response.title='Company track2 Pharma'
    elif med_division=='SINAVISION':
        response.title='Company track2 Sinavision'
        
     
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory
    
        
    if pr_region=='None':
        pr_region=''
    
    if pr_zone=='None':
        pr_zone=''
    
    if pr_area=='None':
        pr_area=''
    
    if pr_territory=='None':
        pr_territory=''
    
        
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
    regionRows=db((db.sm_level.cid==cid)&(db.sm_level.level_id==pr_region)).select(db.sm_level.level_name,limitby=(0,1))
    if regionRows:
        reg_name=regionRows[0].level_name
    

    condition1=''    
    if pr_region!='':
        condition1+=" and a.level0 = '"+str(pr_region)+"'"
    if pr_zone!='':
        condition1+=" and a.level1 = '"+str(pr_zone)+"'"
    if pr_area!='':
        condition1+=" and a.level2 = '"+str(pr_area)+"'"
    if pr_territory!='':
        condition1+=" and a.level_id = '"+str(pr_territory)+"'"

    if int(identical)==1:
        if med_division=='PHARMA':
            condition1+=" and ( b.update_med_count_flag_i >0 or b.update_med_count_flag_i_snv >0) "
        elif med_division=='SINAVISION':
            condition1+=" and b.update_med_count_flag_i_snv >0 "
    elif int(identical)==0:
        if med_division=='PHARMA':
            condition1+=" and ( b.update_med_count_flag >0 or b.update_med_count_flag_snv >0) "
        elif med_division=='SINAVISION':
            condition1+=" and b.update_med_count_flag_snv >0 "


    sql1=''
    sql2=''
    if int(identical)==1:
        if med_division=='PHARMA':
            sql1="(SELECT a.cid as cid,a.level0 as zone_id,a.level0_name as zone_name,a.level1 as reg_id,a.level1_name as reg_name,a.level2 as tl_id,a.level2_name as tl_name,a.level_id as area_id,a.level_name as area_name,'' as level0_sup_id,'' as level0_sup_name,'' as level1_sup_id,'' as level1_sup_name,'' as level2_sup_id,'' as level2_sup_name,'' as level3_sup_id,'' as level3_sup_name,b.sl as rxCount1,0 as rxCount2,(b.med_self+b.med_self_snv) as med_self1,(b.med_total_i+b.med_total_i_snv) as med_total1, 0 as med_self2, 0 as med_total2 FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.cid=b.cid and a.level_id=b.area_id and b.submit_date>='"+date_from_1+"' and b.submit_date<='"+date_to_1+"'"+condition1+")"
            sql2="(SELECT a.cid as cid,a.level0 as zone_id,a.level0_name as zone_name,a.level1 as reg_id,a.level1_name as reg_name,a.level2 as tl_id,a.level2_name as tl_name,a.level_id as area_id,a.level_name as area_name,'' as level0_sup_id,'' as level0_sup_name,'' as level1_sup_id,'' as level1_sup_name,'' as level2_sup_id,'' as level2_sup_name,'' as level3_sup_id,'' as level3_sup_name,0 as rxCount1,b.sl as rxCount2,0 as med_self1, 0 as med_total1,(b.med_self+b.med_self_snv) as med_self2,(b.med_total_i+b.med_total_i_snv) as total2 FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.cid=b.cid and a.level_id=b.area_id and b.submit_date>='"+date_from_2+"' and b.submit_date<='"+date_to_2+"'"+condition1+")"

        elif med_division=='SINAVISION':
            sql1="(SELECT a.cid as cid,a.level0 as zone_id,a.level0_name as zone_name,a.level1 as reg_id,a.level1_name as reg_name,a.level2 as tl_id,a.level2_name as tl_name,a.level_id as area_id,a.level_name as area_name,'' as level0_sup_id,'' as level0_sup_name,'' as level1_sup_id,'' as level1_sup_name,'' as level2_sup_id,'' as level2_sup_name,'' as level3_sup_id,'' as level3_sup_name,b.sl as rxCount1,0 as rxCount2, b.med_self_snv as med_self1,b.med_total_i_snv as med_total1, 0 as med_self2, 0 as med_total2 FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.level_id=b.area_id and  b.submit_date>='"+date_from_1+"' and b.submit_date<='"+date_to_1+"' "+condition1+")"
            sql2="(SELECT a.cid as cid,a.level0 as zone_id,a.level0_name as zone_name,a.level1 as reg_id,a.level1_name as reg_name,a.level2 as tl_id,a.level2_name as tl_name,a.level_id as area_id,a.level_name as area_name,'' as level0_sup_id,'' as level0_sup_name,'' as level1_sup_id,'' as level1_sup_name,'' as level2_sup_id,'' as level2_sup_name,'' as level3_sup_id,'' as level3_sup_name,0 as rxCount1,b.sl as rxCount2,0 as med_self1, 0 as med_total1,b.med_self_snv as med_self2,b.med_total_i_snv as total2 FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.level_id=b.area_id and b.submit_date>='"+date_from_2+"' and b.submit_date<='"+date_to_2+"' "+condition1+")"

    elif int(identical)==0:
        if med_division=='PHARMA':
            sql1="(SELECT a.cid as cid,a.level0 as zone_id,a.level0_name as zone_name,a.level1 as reg_id,a.level1_name as reg_name,a.level2 as tl_id,a.level2_name as tl_name,a.level_id as area_id,a.level_name as area_name,'' as level0_sup_id,'' as level0_sup_name,'' as level1_sup_id,'' as level1_sup_name,'' as level2_sup_id,'' as level2_sup_name,'' as level3_sup_id,'' as level3_sup_name,b.sl as rxCount1,0 as rxCount2,(b.med_self+b.med_self_snv) as med_self1,(b.med_total+b.med_total_snv) as med_total1, 0 as med_self2, 0 as med_total2 FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.cid=b.cid and a.level_id=b.area_id and b.submit_date>='"+date_from_1+"' and b.submit_date<='"+date_to_1+"'"+condition1+")"
            sql2="(SELECT a.cid as cid,a.level0 as zone_id,a.level0_name as zone_name,a.level1 as reg_id,a.level1_name as reg_name,a.level2 as tl_id,a.level2_name as tl_name,a.level_id as area_id,a.level_name as area_name,'' as level0_sup_id,'' as level0_sup_name,'' as level1_sup_id,'' as level1_sup_name,'' as level2_sup_id,'' as level2_sup_name,'' as level3_sup_id,'' as level3_sup_name,0 as rxCount1,b.sl as rxCount2,0 as med_self1, 0 as med_total1,(b.med_self+b.med_self_snv) as med_self2,(b.med_total+b.med_total_snv) as total2 FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.cid=b.cid and a.level_id=b.area_id and b.submit_date>='"+date_from_2+"' and b.submit_date<='"+date_to_2+"'"+condition1+")"

        elif med_division=='SINAVISION':
            sql1="(SELECT a.cid as cid,a.level0 as zone_id,a.level0_name as zone_name,a.level1 as reg_id,a.level1_name as reg_name,a.level2 as tl_id,a.level2_name as tl_name,a.level_id as area_id,a.level_name as area_name,'' as level0_sup_id,'' as level0_sup_name,'' as level1_sup_id,'' as level1_sup_name,'' as level2_sup_id,'' as level2_sup_name,'' as level3_sup_id,'' as level3_sup_name,b.sl as rxCount1,0 as rxCount2, b.med_self_snv as med_self1,b.med_total_snv as med_total1, 0 as med_self2, 0 as med_total2 FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.level_id=b.area_id and  b.submit_date>='"+date_from_1+"' and b.submit_date<='"+date_to_1+"' "+condition1+")"
            sql2="(SELECT a.cid as cid,a.level0 as zone_id,a.level0_name as zone_name,a.level1 as reg_id,a.level1_name as reg_name,a.level2 as tl_id,a.level2_name as tl_name,a.level_id as area_id,a.level_name as area_name,'' as level0_sup_id,'' as level0_sup_name,'' as level1_sup_id,'' as level1_sup_name,'' as level2_sup_id,'' as level2_sup_name,'' as level3_sup_id,'' as level3_sup_name,0 as rxCount1,b.sl as rxCount2,0 as med_self1, 0 as med_total1,b.med_self_snv as med_self2,b.med_total_snv as total2 FROM sm_level a,`sm_prescription_head` b WHERE a.cid='"+cid+"' and a.depth=3 and a.level_id=b.area_id and b.submit_date>='"+date_from_2+"' and b.submit_date<='"+date_to_2+"' "+condition1+")"

    records0="select cid,zone_id,zone_name,level0_sup_id,level0_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by cid;"
    recordList0=db.executesql(records0,as_dict=True)

    records1="select zone_id,reg_id,reg_name,level1_sup_id,level1_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id;"
    recordList1=db.executesql(records1,as_dict=True)

    recordListH0=[]
    zone_id_list=[]
    for i in range(len(recordList0)):
        recordList0s=recordList0[i]
        zone_id=recordList0s['zone_id']

        if zone_id not in zone_id_list:
            dict_data = {'zone_id': zone_id}
            recordListH0.append(dict_data)
            zone_id_list.append(zone_id)


    # recordListH0=[]
    # recordsH0="select zone_id,level0_sup_id,level0_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id order by zone_id;"
    # recordListH0=db.executesql(recordsH0,as_dict=True)

    recordListH1=[]
    recordListH1=recordListH0

    # recordListH1=[]
    # recordsH1="select zone_id,level0_sup_id,level0_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id order by zone_id;"
    # recordListH1=db.executesql(recordsH1,as_dict=True)

    
    recordList2=[]
    records2="select zone_id,reg_id,tl_id,tl_name,level2_sup_id,level2_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id order by zone_id,reg_id,tl_id;"
    recordList2=db.executesql(records2,as_dict=True)

    recordListH2=[]
    reg_id_list=[]
    for i in range(len(recordList2)):
        recordList2s=recordList2[i]
        zone_id=recordList2s['zone_id']
        reg_id=recordList2s['reg_id']

        if reg_id not in reg_id_list:
            dict_data = {'zone_id': zone_id, 'reg_id': reg_id}
            recordListH2.append(dict_data)
            reg_id_list.append(reg_id)


    # recordListH2=[]
    # recordsH2="select zone_id,reg_id,level0_sup_id,level0_sup_name,level1_sup_id,level1_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id;"
    # recordListH2=db.executesql(recordsH2,as_dict=True)
    #return str(recordListH2)
    recordList3=[]
    records3="select zone_id,reg_id,tl_id,area_id,area_name,level3_sup_id,level3_sup_name,count(distinct(rxCount1))-1 as rxCount1,count(distinct(rxCount2))-1 as rxCount2, sum(med_self1) as med_self1, sum(med_total1) as med_total1,round((sum(med_self1)/sum(med_total1))*100,2) as perP1, sum(med_self2) as med_self2, sum(med_total2) as med_total2,round((sum(med_self2)/sum(med_total2))*100,2) as perP2, round((((sum(med_self2)/sum(med_total2))*100)-((sum(med_self1)/sum(med_total1))*100))/((sum(med_self1)/sum(med_total1))*100)*100,2) as growth from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id,area_id order by zone_id,reg_id,tl_id,area_id;"
    recordList3=db.executesql(records3,as_dict=True)

    recordListH3=[]
    tl_id_list=[]
    for i in range(len(recordList3)):
        recordList3s=recordList3[i]
        zone_id=recordList3s['zone_id']
        reg_id=recordList3s['reg_id']
        tl_id = recordList3s['tl_id']

        if tl_id not in tl_id_list:
            dict_data = {'zone_id': zone_id, 'reg_id': reg_id,'tl_id': tl_id}
            recordListH3.append(dict_data)
            tl_id_list.append(tl_id)



    # recordListH3=[]
    # recordsH3="select zone_id,reg_id,tl_id,level2_sup_id,level2_sup_name,level1_sup_id,level1_sup_name,level0_sup_id,level0_sup_name from ("+sql1+" union all "+sql2+") p group by zone_id,reg_id,tl_id order by zone_id,reg_id,tl_id;"
    # recordListH3=db.executesql(recordsH3,as_dict=True)
    
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
    if med_division=='PHARMA':
        supListH3="select area_id,rep_id,rep_name from sm_rep_area where cid='"+cid+"' and rep_category!='C' order by area_id;"
    elif med_division=='SINAVISION':
        supListH3="select area_id,rep_id,rep_name from sm_rep_area where cid='"+cid+"' and rep_category='C' order by area_id;"

    supListH3=db.executesql(supListH3,as_dict=True)
    
    return dict(identical=identical,med_division=med_division,supListH3=supListH3,supListH2=supListH2,supListH1=supListH1,supListH0=supListH0,pr_year1=pr_year1,pr_year2=pr_year2,pr_quarter1=pr_quarter1,pr_quarter2=pr_quarter2,pr_month1=pr_month1,pr_month2=pr_month2,pr_cycle1=pr_cycle1,pr_cycle2=pr_cycle2,recordListH3=recordListH3,recordList3=recordList3,recordListH2=recordListH2,recordList2=recordList2,recordListH1=recordListH1,recordList1=recordList1,recordListH0=recordListH0,recordList0=recordList0,pr_region=pr_region,reg_name=reg_name,pr_zone=pr_zone,pr_area=pr_area,pr_territory=pr_territory,date_from_1=date_from_1,date_to_1=date_to_1,date_from_2=date_from_2,date_to_2=date_to_2)

#============/ block 1


def sin_zm_ranking():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

    cid=session.cid
    date_from=request.vars.date_from
    date_to=request.vars.date_to        
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory        
    pr_doc=request.vars.pr_doc

    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    pr_brand=request.vars.pr_brand
     
    if pr_region=='None':
        pr_region=''
    
    if pr_zone=='None':
        pr_zone=''
    
    if pr_area=='None':
        pr_area=''
    
    if pr_territory=='None':
        pr_territory=''
    
    if pr_brand=='None':
        pr_brand=''
    
     
    if pr_doc=='None':
        pr_doc=''
    
    if pr_ff=='None':
        pr_ff=''

    if pr_brand!='':
        pr_brand=str(pr_brand).replace("[","").replace(" ","").replace("]","").replace("'","")
          
    brand_list=[]
    b_list=pr_brand.split(',')
    
    for i in range(len(b_list)):
        brand_list.append(b_list[i])

    # return pr_brand
    qset = db()
    qset = qset(db.sm_prescription_seen_head.cid == cid)
    qset = qset(db.sm_prescription_seen_head.submit_date >= date_from)
    qset = qset(db.sm_prescription_seen_head.submit_date <= date_to)


    


    doc_id=pr_doc
    doc_name=''
    
    zm_id=pr_zone
    zm_name=''

    rsm_id=pr_region
    rsm_name=''

    fm_id=pr_area
    fm_name=''

    tl_id=pr_territory
    tl_name=''
    
    if (doc_id!=''):
        qset = qset(db.sm_prescription_seen_head.doctor_id == doc_id)
    
    if (zm_id!=''):
        qset = qset(db.sm_prescription_seen_head.reg_id == zm_id)

    if (rsm_id!=''):
        qset = qset(db.sm_prescription_seen_head.zone_id == rsm_id)

    if (fm_id!=''):
        qset = qset(db.sm_prescription_seen_head.area_id == tl_id) 

    if (tl_id!=''):
        qset = qset(db.sm_prescription_seen_head.tl_id == fm_id) 
    if pr_brand!='':
        qset = qset(db.sm_prescription_seen_head.cid == db.sm_prescription_seen_details.cid)
        qset = qset(db.sm_prescription_seen_head.sl == db.sm_prescription_seen_details.sl) 
        qset = qset(db.sm_prescription_seen_details.medicine_id.belongs(brand_list)) 

    records = qset.select(db.sm_prescription_seen_head.ALL,db.sm_prescription_seen_head.id.count(), orderby= ~db.sm_prescription_seen_head.id.count(),groupby= db.sm_prescription_seen_head.zone_id, limitby=(0,100))
    
    
    return dict (records=records,date_from=date_from,date_to=date_to,zm_id=zm_id,zm_name=zm_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tl_id=tl_id,tl_name=tl_name,doc_id=doc_id,doc_name=doc_name,pr_brand=pr_brand)



def sin_rsm_ranking():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

    cid=session.cid
    date_from=request.vars.date_from
    date_to=request.vars.date_to
        
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory    
    pr_doc=request.vars.pr_doc
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    pr_brand=request.vars.pr_brand
     
    if pr_region=='None':
        pr_region=''
    
    if pr_zone=='None':
        pr_zone=''
    
    if pr_area=='None':
        pr_area=''
    
    if pr_territory=='None':
        pr_territory=''
    
    if pr_brand=='None':
        pr_brand=''
    
    if pr_brand!='':
        pr_brand=str(pr_brand).replace("[","").replace(" ","").replace("]","").replace("'","")
          
    brand_list=[]
    b_list=pr_brand.split(',')
    
    for i in range(len(b_list)):
        brand_list.append(b_list[i])
       
    
    if pr_doc=='None':
        pr_doc=''
    
    if pr_ff=='None':
        pr_ff=''
   

    
    qset = db()
    qset = qset(db.sm_prescription_seen_head.cid == cid)
    qset = qset(db.sm_prescription_seen_head.submit_date >= date_from)
    qset = qset(db.sm_prescription_seen_head.submit_date <= date_to)



    doc_id=pr_doc
    doc_name=''
    
    zm_id=pr_zone
    zm_name=''

    rsm_id=pr_region
    rsm_name=''

    fm_id=pr_area
    fm_name=''

    tl_id=pr_territory
    tl_name=''
    
    if (doc_id!=''):
        qset = qset(db.sm_prescription_seen_head.doctor_id == doc_id)
    
    if (zm_id!=''):
        qset = qset(db.sm_prescription_seen_head.reg_id == zm_id)

    if (rsm_id!=''):
        qset = qset(db.sm_prescription_seen_head.zone_id == rsm_id)

    if (fm_id!=''):
        qset = qset(db.sm_prescription_seen_head.area_id == tl_id) 

    if (tl_id!=''):
        qset = qset(db.sm_prescription_seen_head.tl_id == fm_id) 
            
    if pr_brand!='':
        qset = qset(db.sm_prescription_seen_head.cid == db.sm_prescription_seen_details.cid)
        qset = qset(db.sm_prescription_seen_head.sl == db.sm_prescription_seen_details.sl) 
        qset = qset(db.sm_prescription_seen_details.medicine_id.belongs(brand_list)) 

    records = qset.select(db.sm_prescription_seen_head.ALL,db.sm_prescription_seen_head.id.count(), orderby= ~db.sm_prescription_seen_head.id.count(),groupby= db.sm_prescription_seen_head.reg_id, limitby=(0,100))
    
    
    return dict (records=records,date_from=date_from,date_to=date_to,zm_id=zm_id,zm_name=zm_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tl_id=tl_id,tl_name=tl_name,doc_id=doc_id,doc_name=doc_name,pr_brand=pr_brand)



def sin_fm_ranking():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

    cid=session.cid
    date_from=request.vars.date_from
    date_to=request.vars.date_to
        
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory    
    pr_doc=request.vars.pr_doc
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    pr_brand=request.vars.pr_brand
     
    if pr_region=='None':
        pr_region=''
    
    if pr_zone=='None':
        pr_zone=''
    
    if pr_area=='None':
        pr_area=''
    
    if pr_territory=='None':
        pr_territory=''
    
    if pr_brand=='None':
        pr_brand=''
    
    if pr_brand!='':
        pr_brand=str(pr_brand).replace("[","").replace(" ","").replace("]","").replace("'","")
          
    brand_list=[]
    b_list=pr_brand.split(',')
    
    for i in range(len(b_list)):
        brand_list.append(b_list[i])
       
    
    if pr_doc=='None':
        pr_doc=''
    
    if pr_ff=='None':
        pr_ff=''

    
    qset = db()
    qset = qset(db.sm_prescription_seen_head.cid == cid)
    qset = qset(db.sm_prescription_seen_head.submit_date >= date_from)
    qset = qset(db.sm_prescription_seen_head.submit_date <= date_to)


   


    doc_id=pr_doc
    doc_name=''
    
    zm_id=pr_zone
    zm_name=''

    rsm_id=pr_region
    rsm_name=''

    fm_id=pr_area
    fm_name=''

    tl_id=pr_territory
    tl_name=''
    
    if (doc_id!=''):
        qset = qset(db.sm_prescription_seen_head.doctor_id == doc_id)
    
    if (zm_id!=''):
        qset = qset(db.sm_prescription_seen_head.reg_id == zm_id)

    if (rsm_id!=''):
        qset = qset(db.sm_prescription_seen_head.zone_id == rsm_id)

    if (fm_id!=''):
        qset = qset(db.sm_prescription_seen_head.area_id == tl_id) 

    if (tl_id!=''):
        qset = qset(db.sm_prescription_seen_head.tl_id == fm_id) 
    # return tl_id        
    if pr_brand!='':
        qset = qset(db.sm_prescription_seen_head.cid == db.sm_prescription_seen_details.cid)
        qset = qset(db.sm_prescription_seen_head.sl == db.sm_prescription_seen_details.sl) 
        qset = qset(db.sm_prescription_seen_details.medicine_id.belongs(brand_list)) 

    records = qset.select(db.sm_prescription_seen_head.ALL,db.sm_prescription_seen_head.id.count(), orderby= ~db.sm_prescription_seen_head.id.count(),groupby= db.sm_prescription_seen_head.tl_id, limitby=(0,100))

    
    return dict (records=records,date_from=date_from,date_to=date_to,zm_id=zm_id,zm_name=zm_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tl_id=tl_id,tl_name=tl_name,doc_id=doc_id,doc_name=doc_name,pr_brand=pr_brand)


def sin_mpo_ranking():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

    cid=session.cid
    date_from=request.vars.date_from
    date_to=request.vars.date_to
        
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory    
    pr_doc=request.vars.pr_doc
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    pr_brand=request.vars.pr_brand
     
    if pr_region=='None':
        pr_region=''
    
    if pr_zone=='None':
        pr_zone=''
    
    if pr_area=='None':
        pr_area=''
    
    if pr_territory=='None':
        pr_territory=''
    
    if pr_brand=='None':
        pr_brand=''
    
    if pr_brand!='':
        pr_brand=str(pr_brand).replace("[","").replace(" ","").replace("]","").replace("'","")
          
    brand_list=[]
    b_list=pr_brand.split(',')
    
    for i in range(len(b_list)):
        brand_list.append(b_list[i])


    if pr_doc=='None':
        pr_doc=''
    
    if pr_ff=='None':
        pr_ff=''
   
    
    
    qset = db()
    qset = qset(db.sm_prescription_seen_head.cid == cid)
    qset = qset(db.sm_prescription_seen_head.submit_date >= date_from)
    qset = qset(db.sm_prescription_seen_head.submit_date <= date_to)


    doc_id=pr_doc
    doc_name=''
    
    zm_id=pr_zone
    zm_name=''

    rsm_id=pr_region
    rsm_name=''

    fm_id=pr_area
    fm_name=''

    tl_id=pr_territory
    tl_name=''
    # return rsm_id
    if (doc_id!=''):
        qset = qset(db.sm_prescription_seen_head.doctor_id == doc_id)
    
    if (zm_id!=''):
        qset = qset(db.sm_prescription_seen_head.reg_id == zm_id)

    if (rsm_id!=''):
        qset = qset(db.sm_prescription_seen_head.zone_id == rsm_id)

    if (fm_id!=''):
        qset = qset(db.sm_prescription_seen_head.area_id == tl_id) 

    if (tl_id!=''):
        qset = qset(db.sm_prescription_seen_head.tl_id == fm_id) 
    if pr_brand!='':
        qset = qset(db.sm_prescription_seen_head.cid == db.sm_prescription_seen_details.cid)
        qset = qset(db.sm_prescription_seen_head.sl == db.sm_prescription_seen_details.sl) 
        qset = qset(db.sm_prescription_seen_details.medicine_id.belongs(brand_list)) 

    records = qset.select(db.sm_prescription_seen_head.ALL,db.sm_prescription_seen_head.id.count(), orderby= ~db.sm_prescription_seen_head.id.count(),groupby= db.sm_prescription_seen_head.area_id, limitby=(0,100))
    
    return dict (records=records,date_from=date_from,date_to=date_to,zm_id=zm_id,zm_name=zm_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tl_id=tl_id,tl_name=tl_name,doc_id=doc_id,doc_name=doc_name,pr_brand=pr_brand)


def dr_sin_zm_ranking():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

    cid=session.cid
    date_from=request.vars.date_from
    date_to=request.vars.date_to
        
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory    
    pr_doc=request.vars.pr_doc
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    pr_brand=request.vars.pr_brand
     
    if pr_region=='None':
        pr_region=''
    
    if pr_zone=='None':
        pr_zone=''
    
    if pr_area=='None':
        pr_area=''
    
    if pr_territory=='None':
        pr_territory=''
    
    if pr_brand=='None':
        pr_brand=''
    
    if pr_brand!='':
        pr_brand=str(pr_brand).replace("[","").replace(" ","").replace("]","").replace("'","")
          
    brand_list=[]
    b_list=pr_brand.split(',')
    
    for i in range(len(b_list)):
        brand_list.append(b_list[i])
       
    
    if pr_doc=='None':
        pr_doc=''
    
    if pr_ff=='None':
        pr_ff=''
   
    
    qset = db()
    qset = qset(db.sm_prescription_seen_head.cid == cid)
    qset = qset(db.sm_prescription_seen_head.submit_date >= date_from)
    qset = qset(db.sm_prescription_seen_head.submit_date <= date_to)
    

    doc_id=pr_doc
    doc_name=''
    
    zm_id=pr_zone
    zm_name=''

    rsm_id=pr_region
    rsm_name=''

    fm_id=pr_area
    fm_name=''

    tl_id=pr_territory
    tl_name=''
    
    if (doc_id!=''):
        qset = qset(db.sm_prescription_seen_head.doctor_id == doc_id)
    
    if (zm_id!=''):
        qset = qset(db.sm_prescription_seen_head.reg_id == zm_id)

    if (rsm_id!=''):
        qset = qset(db.sm_prescription_seen_head.zone_id == rsm_id)

    if (fm_id!=''):
        qset = qset(db.sm_prescription_seen_head.area_id == tl_id) 

    if (tl_id!=''):
        qset = qset(db.sm_prescription_seen_head.tl_id == fm_id) 
    
    if pr_brand!='':
        qset = qset(db.sm_prescription_seen_head.cid == db.sm_prescription_seen_details.cid)
        qset = qset(db.sm_prescription_seen_head.sl == db.sm_prescription_seen_details.sl) 
        qset = qset(db.sm_prescription_seen_details.medicine_id.belongs(brand_list)) 

    records = qset.select(db.sm_prescription_seen_head.ALL,db.sm_prescription_seen_head.id.count(), orderby= ~db.sm_prescription_seen_head.id.count(),groupby= db.sm_prescription_seen_head.zone_id|db.sm_prescription_seen_head.doctor_id, limitby=(0,100))
    
    return dict (records=records,date_from=date_from,date_to=date_to,zm_id=zm_id,zm_name=zm_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tl_id=tl_id,tl_name=tl_name,doc_id=doc_id,doc_name=doc_name,pr_brand=pr_brand)




def dr_sin_rsm_ranking():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

    cid=session.cid
    date_from=request.vars.date_from
    date_to=request.vars.date_to
        
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory    
    pr_doc=request.vars.pr_doc
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    pr_brand=request.vars.pr_brand
     
    if pr_region=='None':
        pr_region=''
    
    if pr_zone=='None':
        pr_zone=''
    
    if pr_area=='None':
        pr_area=''
    
    if pr_territory=='None':
        pr_territory=''
    
    if pr_brand=='None':
        pr_brand=''
    
    if pr_brand!='':
        pr_brand=str(pr_brand).replace("[","").replace(" ","").replace("]","").replace("'","")
          
    brand_list=[]
    b_list=pr_brand.split(',')
    
    for i in range(len(b_list)):
        brand_list.append(b_list[i])
       
    
    if pr_doc=='None':
        pr_doc=''
    
    if pr_ff=='None':
        pr_ff=''
   
    
    qset = db()
    qset = qset(db.sm_prescription_seen_head.cid == cid)
    qset = qset(db.sm_prescription_seen_head.submit_date >= date_from)
    qset = qset(db.sm_prescription_seen_head.submit_date <= date_to)
    


    doc_id=pr_doc
    doc_name=''
    
    zm_id=pr_zone
    zm_name=''

    rsm_id=pr_region
    rsm_name=''

    fm_id=pr_area
    fm_name=''

    tl_id=pr_territory
    tl_name=''
    
    if (doc_id!=''):
        qset = qset(db.sm_prescription_seen_head.doctor_id == doc_id)
    
    if (zm_id!=''):
        qset = qset(db.sm_prescription_seen_head.reg_id == zm_id)

    if (rsm_id!=''):
        qset = qset(db.sm_prescription_seen_head.zone_id == rsm_id)

    if (fm_id!=''):
        qset = qset(db.sm_prescription_seen_head.area_id == tl_id) 

    if (tl_id!=''):
        qset = qset(db.sm_prescription_seen_head.tl_id == fm_id) 
    if pr_brand!='':
        qset = qset(db.sm_prescription_seen_head.cid == db.sm_prescription_seen_details.cid)
        qset = qset(db.sm_prescription_seen_head.sl == db.sm_prescription_seen_details.sl) 
        qset = qset(db.sm_prescription_seen_details.medicine_id.belongs(brand_list)) 

    records = qset.select(db.sm_prescription_seen_head.ALL,db.sm_prescription_seen_head.id.count(), orderby= ~db.sm_prescription_seen_head.id.count(),groupby= db.sm_prescription_seen_head.reg_id|db.sm_prescription_seen_head.doctor_id, limitby=(0,100))
    
    return dict (records=records,date_from=date_from,date_to=date_to,zm_id=zm_id,zm_name=zm_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tl_id=tl_id,tl_name=tl_name,doc_id=doc_id,doc_name=doc_name,pr_brand=pr_brand)

def dr_sin_fm_ranking():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

    cid=session.cid
    date_from=request.vars.date_from
    date_to=request.vars.date_to
        
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory    
    
    pr_doc=request.vars.pr_doc
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    pr_brand=request.vars.pr_brand
     
    if pr_region=='None':
        pr_region=''
    
    if pr_zone=='None':
        pr_zone=''
    
    if pr_area=='None':
        pr_area=''
    
    if pr_territory=='None':
        pr_territory=''
    
    if pr_brand=='None':
        pr_brand=''
    
    if pr_brand!='':
        pr_brand=str(pr_brand).replace("[","").replace(" ","").replace("]","").replace("'","")
          
    brand_list=[]
    b_list=pr_brand.split(',')
    
    for i in range(len(b_list)):
        brand_list.append(b_list[i]) 
    
    if pr_doc=='None':
        pr_doc=''
    
    if pr_ff=='None':
        pr_ff=''
       
    qset = db()
    qset = qset(db.sm_prescription_seen_head.cid == cid)
    qset = qset(db.sm_prescription_seen_head.submit_date >= date_from)
    qset = qset(db.sm_prescription_seen_head.submit_date <= date_to)


    
    
    doc_id=pr_doc
    doc_name=''
    
    zm_id=pr_zone
    zm_name=''

    rsm_id=pr_region
    rsm_name=''

    fm_id=pr_area
    fm_name=''

    tl_id=pr_territory
    tl_name=''
    
    if (doc_id!=''):
        qset = qset(db.sm_prescription_seen_head.doctor_id == doc_id)
    
    if (zm_id!=''):
        qset = qset(db.sm_prescription_seen_head.reg_id == zm_id)

    if (rsm_id!=''):
        qset = qset(db.sm_prescription_seen_head.zone_id == rsm_id)

    if (fm_id!=''):
        qset = qset(db.sm_prescription_seen_head.area_id == tl_id) 

    if (tl_id!=''):
        qset = qset(db.sm_prescription_seen_head.tl_id == fm_id)   
    if pr_brand!='':
        qset = qset(db.sm_prescription_seen_head.cid == db.sm_prescription_seen_details.cid)
        qset = qset(db.sm_prescription_seen_head.sl == db.sm_prescription_seen_details.sl) 
        qset = qset(db.sm_prescription_seen_details.medicine_id.belongs(brand_list)) 

    records = qset.select(db.sm_prescription_seen_head.ALL,db.sm_prescription_seen_head.id.count(), orderby= ~db.sm_prescription_seen_head.id.count(),groupby= db.sm_prescription_seen_head.tl_id|db.sm_prescription_seen_head.doctor_id, limitby=(0,100))
    
    return dict (records=records,date_from=date_from,date_to=date_to,zm_id=zm_id,zm_name=zm_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tl_id=tl_id,tl_name=tl_name,doc_id=doc_id,doc_name=doc_name,pr_brand=pr_brand)




def dr_sin_mpo_ranking():
    task_id = 'rm_doctor_visit_manage'
    task_id_view = 'rm_doctor_visit_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if (access_permission == False) and (task_id_view == False):
        session.flash = 'Access is Denied !'
        redirect (URL(c='default', f='home'))

    cid=session.cid
    date_from=request.vars.date_from
    date_to=request.vars.date_to
        
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=cid=session.cid
    date_from=request.vars.date_from
    date_to=request.vars.date_to
        
    pr_region=request.vars.pr_region
    pr_zone=request.vars.pr_zone
    pr_area=request.vars.pr_area
    pr_territory=request.vars.pr_territory    
    pr_doc=request.vars.pr_doc
    pr_ff=request.vars.pr_ff
    med_generic=request.vars.med_generic
    pr_brand=request.vars.pr_brand
     
    if pr_region=='None':
        pr_region=''
    
    if pr_zone=='None':
        pr_zone=''
    
    if pr_area=='None':
        pr_area=''
    
    if pr_territory=='None':
        pr_territory=''
    
    if pr_brand=='None':
        pr_brand=''
    
    if pr_brand!='':
        pr_brand=str(pr_brand).replace("[","").replace(" ","").replace("]","").replace("'","")
          
    brand_list=[]
    b_list=pr_brand.split(',')
    
    for i in range(len(b_list)):
        brand_list.append(b_list[i])


    if pr_doc=='None':
        pr_doc=''
    
    if pr_ff=='None':
        pr_ff=''

    
    qset = db()
    qset = qset(db.sm_prescription_seen_head.cid == cid)
    qset = qset(db.sm_prescription_seen_head.submit_date >= date_from)
    qset = qset(db.sm_prescription_seen_head.submit_date <= date_to)




    doc_id=pr_doc
    doc_name=''

    zm_id=pr_zone
    zm_name=''

    rsm_id=pr_region
    rsm_name=''

    fm_id=pr_area
    fm_name=''

    tl_id=pr_territory
    tl_name=''
    
    if (doc_id!=''):
        qset = qset(db.sm_prescription_seen_head.doctor_id == doc_id)
    
    if (zm_id!=''):
        qset = qset(db.sm_prescription_seen_head.reg_id == zm_id)

    if (rsm_id!=''):
        qset = qset(db.sm_prescription_seen_head.zone_id == rsm_id)

    if (fm_id!=''):
        qset = qset(db.sm_prescription_seen_head.area_id == tl_id) 

    if (tl_id!=''):
        qset = qset(db.sm_prescription_seen_head.tl_id == fm_id) 
    if pr_brand!='':
        qset = qset(db.sm_prescription_seen_head.cid == db.sm_prescription_seen_details.cid)
        qset = qset(db.sm_prescription_seen_head.sl == db.sm_prescription_seen_details.sl) 
        qset = qset(db.sm_prescription_seen_details.medicine_id.belongs(brand_list)) 

    records = qset.select(db.sm_prescription_seen_head.ALL,db.sm_prescription_seen_head.id.count(), orderby= ~db.sm_prescription_seen_head.id.count(),groupby= db.sm_prescription_seen_head.area_id|db.sm_prescription_seen_head.doctor_id, limitby=(0,100))
    
    return dict (records=records,date_from=date_from,date_to=date_to,zm_id=zm_id,zm_name=zm_name,rsm_id=rsm_id,rsm_name=rsm_name,fm_id=fm_id,fm_name=fm_name,tl_id=tl_id,tl_name=tl_name,doc_id=doc_id,doc_name=doc_name,pr_brand=pr_brand)

