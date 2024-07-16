import calendar

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)
def deduct_months(sourcedate, months):
    month = sourcedate.month - 1 - months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def analysis():
    task_id='rm_analysis_view'
    access_permission=check_role(task_id)
    if (access_permission==False ):
        session.flash='Access is Denied'
        redirect (URL('default','home'))
    
    response.title='Analysis'
    
    c_id=session.cid
    
    #-----
    
    search_form =SQLFORM(db.sm_search_date)

    btn_dashboard=request.vars.btn_dashboard
    
    btn_sr_wise_visit = request.vars.btn_sr_wise_visit
    btn_sr_wise_visit_d = request.vars.btn_sr_wise_visit_d
    
    btn_sr_wise_sales = request.vars.btn_sr_wise_sales
    btn_sr_wise_sales_d = request.vars.btn_sr_wise_sales_d
    
    btn_sr_attendance = request.vars.btn_sr_attendance
    btn_inactive_user = request.vars.btn_inactive_user
    btn_zero_sales_outlet = request.vars.btn_zero_sales_outlet
    btn_missed_outlet = request.vars.btn_missed_outlet
    
    btn_customer_order = request.vars.btn_customer_order
    btn_customer_order_d = request.vars.btn_customer_order_d
    
    btn_customer_sales = request.vars.btn_customer_sales
    btn_customer_sales_d = request.vars.btn_customer_sales_d
    
    btn_daily_sales_item_wise = request.vars.btn_daily_sales_item_wise
    btn_coverage = request.vars.btn_coverage
    btn_productivity = request.vars.btn_productivity
    
    btn_new_client = request.vars.btn_new_client
    btn_new_client_d = request.vars.btn_new_client_d
    
    btn_new_client_summary = request.vars.btn_new_client_summary
    btn_new_client_summary_d = request.vars.btn_new_client_summary_d

    btn_target_vs_ach=request.vars.btn_target_vs_ach
    btn_target_vs_ach_d = request.vars.btn_target_vs_ach_d

    btn_target_vs_ach_route_item=request.vars.btn_target_vs_ach_route_item
    btn_target_vs_ach_route_item_d = request.vars.btn_target_vs_ach_route_item_d


    #--------------------------------------Reports
    btn_visit_list=request.vars.btn_visit_list    
    btn_schedule_and_completed_visit=request.vars.btn_schedule_and_completed_visit
    btn_client_updated=request.vars.btn_client_updated
    
    btn_order_details_itemwise=request.vars.btn_order_details_itemwise
    btn_order_details_repwise=request.vars.btn_order_details_repwise
    btn_order_details_depotwise=request.vars.btn_order_details_depotwise
    visit_list_summary=request.vars.visit_list_summary
    
    btn_market_research_level0=request.vars.btn_market_research_level0
    btn_market_research_level1=request.vars.btn_market_research_level1
    btn_market_research_rep=request.vars.btn_market_research_rep
    
    btn_sales_summary_itemwise=request.vars.btn_sales_summary_itemwise
    btn_sales_summary_repwise=request.vars.btn_sales_summary_repwise
    btn_sales_summary_depotwise=request.vars.btn_sales_summary_depotwise
    btn_sales_details_download=request.vars.btn_sales_details_download
    btn_visit_count=request.vars.btn_visit_count
    btn_doctor_visit_summary=request.vars.btn_doctor_visit_summary    
    btn_doctor_visit=request.vars.btn_doctor_visit
    
    btn_doctor_visit_individual=request.vars.btn_doctor_visit_individual
    
    btn_market_research_level0_pres=request.vars.btn_market_research_level0_pres
    btn_market_research_level1_pres=request.vars.btn_market_research_level1_pres
    btn_market_research_rep_pres=request.vars.btn_market_research_rep_pres
    
    btn_pres_survey_summary=request.vars.btn_pres_survey_summary
    btn_pres_survey_visit=request.vars.btn_pres_survey_visit
    
    #----------- Others
    btn_monthly_visit_count=request.vars.btn_monthly_visit_count
    btn_target_vs_achievement=request.vars.btn_target_vs_achievement
    btn_retailer_distribution=request.vars.btn_retailer_distribution    
    btn_spo_distribution=request.vars.btn_spo_distribution 
    
    if (btn_new_client_summary_d or btn_new_client_summary or btn_new_client_d or btn_new_client or btn_productivity or btn_coverage or btn_daily_sales_item_wise or btn_customer_sales or btn_customer_sales_d or btn_customer_order or btn_customer_order_d or btn_zero_sales_outlet or btn_missed_outlet or btn_inactive_user or btn_sr_attendance or btn_sr_wise_sales or btn_sr_wise_sales_d or btn_sr_wise_visit or btn_sr_wise_visit_d or btn_dashboard or btn_market_research_level0_pres or btn_market_research_level1_pres or btn_market_research_rep_pres or btn_pres_survey_visit or btn_visit_list or btn_visit_count or btn_market_research_level0 or btn_market_research_level1 or btn_market_research_rep or btn_doctor_visit_summary or btn_schedule_and_completed_visit or btn_client_updated or visit_list_summary or btn_order_details_itemwise or btn_order_details_repwise or btn_order_details_depotwise or btn_sales_summary_itemwise or btn_sales_summary_repwise or btn_sales_summary_depotwise or btn_sales_details_download or btn_doctor_visit or btn_pres_survey_summary or btn_pres_survey_visit or btn_doctor_visit_individual):
        from_dt=request.vars.from_dt
        to_dt=request.vars.to_dt
        regionValue=str(request.vars.regionValue).strip()
        areaValue=str(request.vars.areaValue).split('|')[0]
        territoryValue=str(request.vars.territoryValue).split('|')[0]
        marketValue=str(request.vars.marketValue).split('|')[0]
        repCM=str(request.vars.repCM).split('|')[0]
        
        dateFlag=True
        try:
            from_dt2=datetime.datetime.strptime(str(from_dt),'%Y-%m-%d')
            to_dt2=datetime.datetime.strptime(str(to_dt),'%Y-%m-%d')            
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
            else:
                if btn_dashboard:
                    redirect(URL('dashboard',vars=dict(fromDate=from_dt, toDate=to_dt, regionValue=regionValue, areaValue=areaValue,territoryValue=territoryValue, marketValue=marketValue, repCM=repCM)))
                elif btn_sr_wise_visit:
                    redirect(URL('sr_wise_visit',vars=dict(fromDate=from_dt, toDate=to_dt, regionValue=regionValue, areaValue=areaValue,territoryValue=territoryValue, marketValue=marketValue, repCM=repCM)))
                elif btn_sr_wise_visit_d:
                    redirect(URL('sr_wise_visit_d',vars=dict(fromDate=from_dt, toDate=to_dt, regionValue=regionValue, areaValue=areaValue,territoryValue=territoryValue, marketValue=marketValue, repCM=repCM)))
                
                elif btn_sr_wise_sales:
                    redirect(URL('sr_wise_sales',vars=dict(fromDate=from_dt, toDate=to_dt, regionValue=regionValue, areaValue=areaValue,territoryValue=territoryValue, marketValue=marketValue, repCM=repCM)))
                elif btn_sr_wise_sales_d:
                    redirect(URL('sr_wise_sales_d',vars=dict(fromDate=from_dt, toDate=to_dt, regionValue=regionValue, areaValue=areaValue,territoryValue=territoryValue, marketValue=marketValue, repCM=repCM)))
                                
                elif btn_sr_attendance:
                    redirect(URL('sr_attendance',vars=dict(fromDate=from_dt, toDate=to_dt, regionValue=regionValue, areaValue=areaValue,territoryValue=territoryValue, marketValue=marketValue, repCM=repCM)))
                elif btn_inactive_user:
                    redirect(URL('inactive_user',vars=dict(fromDate=from_dt, toDate=to_dt, regionValue=regionValue, areaValue=areaValue,territoryValue=territoryValue, marketValue=marketValue, repCM=repCM)))
                elif btn_zero_sales_outlet:
                    redirect(URL('zero_sales_outlet',vars=dict(fromDate=from_dt, toDate=to_dt, regionValue=regionValue, areaValue=areaValue,territoryValue=territoryValue, marketValue=marketValue, repCM=repCM)))
                elif btn_missed_outlet:
                    redirect(URL('missed_outlet',vars=dict(fromDate=from_dt, toDate=to_dt, regionValue=regionValue, areaValue=areaValue,territoryValue=territoryValue, marketValue=marketValue, repCM=repCM)))
                
                elif btn_customer_order:
                    redirect(URL('customer_order',vars=dict(fromDate=from_dt, toDate=to_dt, regionValue=regionValue, areaValue=areaValue,territoryValue=territoryValue, marketValue=marketValue, repCM=repCM)))
                elif btn_customer_order_d:
                    redirect(URL('customer_order_d',vars=dict(fromDate=from_dt, toDate=to_dt, regionValue=regionValue, areaValue=areaValue,territoryValue=territoryValue, marketValue=marketValue, repCM=repCM)))
                
                elif btn_customer_sales:
                    redirect(URL('customer_sales',vars=dict(fromDate=from_dt, toDate=to_dt, regionValue=regionValue, areaValue=areaValue,territoryValue=territoryValue, marketValue=marketValue, repCM=repCM)))
                elif btn_customer_sales_d:
                    redirect(URL('customer_sales_d',vars=dict(fromDate=from_dt, toDate=to_dt, regionValue=regionValue, areaValue=areaValue,territoryValue=territoryValue, marketValue=marketValue, repCM=repCM)))
                                
                elif btn_daily_sales_item_wise:
                    if dateDiff > 1:
                        response.flash = "Single day allowed between Date Range"
                    else:
                        redirect(URL('daily_sales_item_wise',vars=dict(fromDate=from_dt, toDate=to_dt, regionValue=regionValue, areaValue=areaValue,territoryValue=territoryValue, marketValue=marketValue, repCM=repCM)))
                elif btn_coverage:
                    redirect(URL('coverage',vars=dict(fromDate=from_dt, toDate=to_dt, regionValue=regionValue, areaValue=areaValue,territoryValue=territoryValue, marketValue=marketValue, repCM=repCM)))
                elif btn_productivity:
                    redirect(URL('productivity',vars=dict(fromDate=from_dt, toDate=to_dt, regionValue=regionValue, areaValue=areaValue,territoryValue=territoryValue, marketValue=marketValue, repCM=repCM)))
                
                elif btn_new_client:
                    redirect(URL('new_client',vars=dict(fromDate=from_dt, toDate=to_dt, regionValue=regionValue, areaValue=areaValue,territoryValue=territoryValue, marketValue=marketValue, repCM=repCM)))
                elif btn_new_client_d:
                    redirect(URL('new_client_d',vars=dict(fromDate=from_dt, toDate=to_dt, regionValue=regionValue, areaValue=areaValue,territoryValue=territoryValue, marketValue=marketValue, repCM=repCM)))
                
                elif btn_new_client_summary:
                    redirect(URL('new_client_summary',vars=dict(fromDate=from_dt, toDate=to_dt, regionValue=regionValue, areaValue=areaValue,territoryValue=territoryValue, marketValue=marketValue, repCM=repCM)))
                elif btn_new_client_summary_d:
                    redirect(URL('new_client_summary_d',vars=dict(fromDate=from_dt, toDate=to_dt, regionValue=regionValue, areaValue=areaValue,territoryValue=territoryValue, marketValue=marketValue, repCM=repCM)))



                elif btn_visit_list:
                    redirect (URL('visitList',vars=dict(fromDate=from_dt,toDate=to_dt,regionValue=regionValue,areaValue=areaValue,territoryValue=territoryValue,marketValue=marketValue,repCM=repCM))) 
                
                elif btn_visit_count:
                    redirect (URL('visit_summary',vars=dict(fromDate=from_dt,toDate=to_dt,regionValue=regionValue,areaValue=areaValue,territoryValue=territoryValue,marketValue=marketValue,repCM=repCM)))
                
                elif btn_schedule_and_completed_visit:
                    redirect (URL('schedule_and_completed_visit',vars=dict(fromDate=from_dt,toDate=to_dt,regionValue=regionValue,areaValue=areaValue,territoryValue=territoryValue,marketValue=marketValue,repCM=repCM)))
                
                elif btn_client_updated:
                    redirect (URL('clientUpdatedList',vars=dict(fromDate=from_dt,toDate=to_dt,regionValue=regionValue,areaValue=areaValue,territoryValue=territoryValue,marketValue=marketValue,repCM=repCM)))
                
                elif visit_list_summary:
                    redirect (URL('visit_list_summary',vars=dict(fromDate=from_dt,toDate=to_dt,regionValue=regionValue,areaValue=areaValue,territoryValue=territoryValue,marketValue=marketValue,repCM=repCM))) 
                
                elif btn_order_details_itemwise:
                    redirect (URL('order_details_itemwise',vars=dict(fromDate=from_dt,toDate=to_dt,regionValue=regionValue,areaValue=areaValue,territoryValue=territoryValue,marketValue=marketValue,repCM=repCM))) 
                
                elif btn_order_details_repwise:
                    redirect (URL('order_details_repwise',vars=dict(fromDate=from_dt,toDate=to_dt,regionValue=regionValue,areaValue=areaValue,territoryValue=territoryValue,marketValue=marketValue,repCM=repCM))) 
                
                elif btn_order_details_depotwise:
                    redirect (URL('order_details_depotwise',vars=dict(fromDate=from_dt,toDate=to_dt,regionValue=regionValue,areaValue=areaValue,territoryValue=territoryValue,marketValue=marketValue,repCM=repCM))) 
                
                elif btn_sales_summary_itemwise:
                    redirect (URL('sales_summary_itemwise',vars=dict(fromDate=from_dt,toDate=to_dt,regionValue=regionValue,areaValue=areaValue,territoryValue=territoryValue,marketValue=marketValue,repCM=repCM))) 
                
                elif btn_sales_summary_repwise:
                    redirect (URL('sales_summary_repwise',vars=dict(fromDate=from_dt,toDate=to_dt,regionValue=regionValue,areaValue=areaValue,territoryValue=territoryValue,marketValue=marketValue,repCM=repCM))) 
                
                elif btn_sales_summary_depotwise:
                    redirect (URL('sales_summary_depotwise',vars=dict(fromDate=from_dt,toDate=to_dt,regionValue=regionValue,areaValue=areaValue,territoryValue=territoryValue,marketValue=marketValue,repCM=repCM))) 
                
                elif btn_sales_details_download:
                    redirect (URL('sales_details_download',vars=dict(fromDate=from_dt,toDate=to_dt,regionValue=regionValue,areaValue=areaValue,territoryValue=territoryValue,marketValue=marketValue,repCM=repCM))) 
                
                elif btn_market_research_level0:
                    redirect (URL('market_research_level0',vars=dict(fromDate=from_dt,toDate=to_dt,regionValue=regionValue,areaValue=areaValue))) 
                
                elif btn_market_research_level1:
                    redirect (URL('market_research_level1',vars=dict(fromDate=from_dt,toDate=to_dt,regionValue=regionValue,areaValue=areaValue))) 
                    
                elif btn_market_research_rep:
                    redirect (URL('market_research_rep',vars=dict(fromDate=from_dt,toDate=to_dt,regionValue=regionValue,areaValue=areaValue))) 
                
                elif btn_doctor_visit_summary:
                    redirect (URL('doctor_visit_summary_level0',vars=dict(fromDate=from_dt,toDate=to_dt,regionValue=regionValue,areaValue=areaValue,territoryValue=territoryValue,marketValue=marketValue,repCM=repCM))) 
                
                elif btn_doctor_visit:
                    redirect (URL('doctor_visit_list',vars=dict(fromDate=from_dt,toDate=to_dt,regionValue=regionValue,areaValue=areaValue,repCM=repCM))) 
                
                elif btn_doctor_visit_individual:
                    redirect (URL('doctor_survey_summary_mpo',vars=dict(fromDate=from_dt,toDate=to_dt,regionValue=regionValue,areaValue=areaValue,repCM=repCM))) 
                
                
                elif btn_market_research_level0_pres:
                    redirect (URL('pres_survey_summary_reg',vars=dict(fromDate=from_dt,toDate=to_dt,regionValue=regionValue,areaValue=areaValue,territoryValue=territoryValue,marketValue=marketValue,repCM=repCM))) 
                
                elif btn_market_research_level1_pres:
                    redirect (URL('pres_survey_summary_tl',vars=dict(fromDate=from_dt,toDate=to_dt,regionValue=regionValue,areaValue=areaValue))) 
                    
                elif btn_market_research_rep_pres:
                    redirect (URL('pres_survey_summary_mpo',vars=dict(fromDate=from_dt,toDate=to_dt,regionValue=regionValue,areaValue=areaValue,territoryValue=territoryValue,marketValue=marketValue,repCM=repCM)))  
                
                
                elif btn_pres_survey_summary:
                    redirect (URL('pres_survey_summary_level0',vars=dict(fromDate=from_dt,toDate=to_dt,regionValue=regionValue,areaValue=areaValue,territoryValue=territoryValue,marketValue=marketValue,repCM=repCM))) 
                
                elif btn_pres_survey_visit:
                    redirect (URL('pres_survey_visit_list',vars=dict(fromDate=from_dt,toDate=to_dt,regionValue=regionValue,areaValue=areaValue,territoryValue=territoryValue,marketValue=marketValue,repCM=repCM))) 
                elif btn_pres_survey_visit:
                    redirect (URL('pres_survey_visit_list',vars=dict(fromDate=from_dt,toDate=to_dt,regionValue=regionValue,areaValue=areaValue,territoryValue=territoryValue,marketValue=marketValue,repCM=repCM)))

    elif btn_target_vs_ach_d or btn_target_vs_ach or btn_target_vs_ach_route_item or btn_target_vs_ach_route_item_d:
        rpt_year = request.vars.rpt_year
        rpt_month = request.vars.rpt_month

        if rpt_year == '' or rpt_month == '':
            response.flash = "Required Valid Year and Month"
        else:
            rpt_ach_date_from = request.vars.rpt_ach_date_from
            rpt_ach_date_to = request.vars.rpt_ach_date_to


            if btn_target_vs_ach:
                redirect(URL('target_vs_ach', vars=dict(rpt_year=rpt_year, rpt_month=rpt_month,rpt_ach_date_from=rpt_ach_date_from,rpt_ach_date_to=rpt_ach_date_to)))
            elif btn_target_vs_ach_d:
                redirect(URL('target_vs_ach_d', vars=dict(rpt_year=rpt_year, rpt_month=rpt_month,rpt_ach_date_from=rpt_ach_date_from,rpt_ach_date_to=rpt_ach_date_to)))
            elif btn_target_vs_ach_route_item:
                redirect(URL('target_vs_ach_route_item', vars=dict(rpt_year=rpt_year, rpt_month=rpt_month,rpt_ach_date_from=rpt_ach_date_from,rpt_ach_date_to=rpt_ach_date_to)))
            elif btn_target_vs_ach_route_item_d:
                redirect(URL('target_vs_ach_route_item_d', vars=dict(rpt_year=rpt_year, rpt_month=rpt_month,rpt_ach_date_from=rpt_ach_date_from,rpt_ach_date_to=rpt_ach_date_to)))
                
    elif (btn_monthly_visit_count or btn_target_vs_achievement or btn_retailer_distribution or btn_spo_distribution):
        year=request.vars.yearValue2
        monthValue2=request.vars.monthValue2
        regionValue=request.vars.regionValue2
        
        if btn_retailer_distribution:
            redirect (URL('retailer_distribution_region',vars=dict(regionValue=regionValue))) 
        
        elif btn_spo_distribution:
            redirect (URL('spo_distribution_region',vars=dict(regionValue=regionValue))) 
             
        else:
            if (year=='' or monthValue2==''):
                response.flash="Invalid Year-Month"
            else:
                monthNo=''
                monthName=''
                month=monthValue2.split('-')
                if len(month)!=2:
                    response.flash="Invalid Month"
                else:
                    monthNo=month[0]
                    monthName=month[1]
                    
                    if btn_monthly_visit_count:
                        redirect (URL('monthlyVisitSummary',vars=dict(year=year,monthNo=monthNo,monthName=monthName,regionValue=regionValue)))
                    
                    elif btn_target_vs_achievement:
                        redirect (URL('target_vs_achievement_region_wise',vars=dict(year=year,monthNo=monthNo,monthName=monthName,regionValue=regionValue)))
                    
    #-------------------
    if session.user_type=='Supervisor':
        level = 'level' + str(session.depthNo)
        levelId=session.level_id
        
        level0=''
        levelRows = db((db.sm_level.cid==session.cid) & (db.sm_level[level] == levelId)).select(db.sm_level.level0,groupby=db.sm_level.level0)
        if levelRows:
            level0=levelRows[0].level0
        
        regionRows = db((db.sm_level.cid==session.cid)&(db.sm_level.depth==0) & (db.sm_level.level_id == level0)).select(db.sm_level.level_id,db.sm_level.level_name,orderby=db.sm_level.level_id)
        
    else:
        regionRows=db((db.sm_level.cid==c_id)&(db.sm_level.depth==0)).select(db.sm_level.level_id,db.sm_level.level_name,orderby=db.sm_level.level_id)
    
    
    #------------
    toDay=current_date
    
    #------
    currentMonth=first_currentDate
    
    #--------------------
    firstDate=str(first_currentDate)[0:10]
    
    #------------------------------
    regionWiseVisitList=[]
    records=''    
    monthName= date_fixed.strftime('%B,%Y')
    
    #--------- Process tabulation sheet
    processRow=db(db.sm_temp_report_process.cid==c_id).select(db.sm_temp_report_process.ALL,limitby=(0,1))
    
    
    return dict(processRow=processRow,search_form=search_form,monthName=monthName,regionWiseVisitList=regionWiseVisitList,regionRows=regionRows)


def target_vs_ach_route_item_d():
    c_id = session.cid

    response.title = 'Target Vs Achievement Route Item'

    rpt_year = request.vars.rpt_year
    rpt_month = request.vars.rpt_month
    rpt_ach_date_from = request.vars.rpt_ach_date_from
    rpt_ach_date_to = request.vars.rpt_ach_date_to

    monthArr = str(rpt_month).split('-')
    if len(monthArr) == 2:
        monthNo = monthArr[0]
        monthName = monthArr[1]
    else:
        monthNo = ''
        monthName = ''

    monthFirstDate = str(rpt_year) + '-' + str(monthNo) + '-01'


    try:
        if int(rpt_ach_date_from)<10:
            rpt_ach_date_from='0'+str(rpt_ach_date_from)

        achDateFrom = str(rpt_year) + '-' + str(monthNo) + '-' + str(rpt_ach_date_from)

        if int(rpt_ach_date_to)<10:
            rpt_ach_date_to='0'+str(rpt_ach_date_to)

        achDateTo = str(rpt_year) + '-' + str(monthNo) + '-' + str(rpt_ach_date_to)

    except:
        achDateFrom = ''
        achDateTo = ''

    monthFlag = True
    try:
        monthFirstDate = datetime.datetime.strptime(str(monthFirstDate), '%Y-%m-%d')
    except:
        monthFlag = False

    # --------------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # ---------------end paging

    if monthFlag == False:
        response.flash = 'Required valid Year and Month'
    else:
        condition2=''
        if achDateFrom!='' and achDateTo!='':
            condition2= " AND invoice_date>='"+str(achDateFrom)+"' AND invoice_date<='"+str(achDateTo)+"' "
        else:
            condition2 = " AND invoice_ym_date = '" + str(monthFirstDate)[:10] + "' "

        sql1 = "SELECT a.level0 as level0,a.level0_name as level0_name,a.level1 as level1,a.level1_name as level1_name,a.level2 as level2,a.level2_name as level2_name,a.level3 as level3,a.level3_name as level3_name,b.item_id as item_id,b.item_name as item_name,sum(b.target_qty*b.price) as target_amt,0 as ach_amt,sum(b.target_qty) as target_qty,0 as ach_qty,'' as last_inv_date FROM sm_level a,target_vs_achievement_route_item b WHERE a.cid = '" + c_id + "' AND a.cid=b.cid AND a.depth=3 AND a.level_id=b.territory_id AND b.first_date = '" + str(
            monthFirstDate)[:10] + "' GROUP BY a.level0,a.level1,a.level2,a.level3,b.item_id"
        sql2 = "SELECT level0_id as level0,level0_name as level0_name,level1_id as level1,level1_name as level1_name,level2_id as level2,level2_name as level2_name,level3_id as level3,level3_name as level3_name,item_id as item_id,item_name as item_name,0 as target_amt,sum(actual_tp*(quantity-return_qty)) as ach_amt,0 as target_qty,sum(quantity-return_qty) as ach_qty,invoice_date as last_inv_date FROM sm_invoice WHERE cid = '" + c_id + "' AND status='Invoiced'  "+condition2+" GROUP BY level0_id,level1_id,level2_id,level3_id,item_id"

        records = "SELECT level0,level0_name,level1,level1_name,level2,level2_name,level3,level3_name,item_id,item_name,sum(target_amt) as target_amt,sum(ach_amt) as ach_amt,sum(target_qty) as target_qty,sum(ach_qty) as ach_qty,max(last_inv_date) as last_inv_date FROM (" + sql1 + " union all " + sql2 + ") p GROUP BY level0,level1,level2,level3,item_id;"
        records = db.executesql(records, as_dict=True)

        # total_target_amt = 0
        # total_ach_amt = 0
        # for i in range(len(records)):
        #     recordsStr = records[i]
        #     total_target_amt += recordsStr['target_amt']
        #     total_ach_amt += recordsStr['ach_amt']
        #
        # ach_per = 0
        # if total_target_amt > 0:
        #     ach_per = (total_ach_amt / total_target_amt) * 100

        # chart
        tar_ach_list = []
        # tar_ach_list_head = ['Route','Target Amount', 'Achievement Amount']
        # tar_ach_list.append(tar_ach_list_head)
        # for i in range(len(records)):
        #     recordsStr=records[i]
        #     level3 = str(recordsStr['level3'])
        #     target_amt = recordsStr['target_amt']
        #     ach_amt = recordsStr['ach_amt']
        #
        #
        #     rec_list = [level3, target_amt,ach_amt]
        #     tar_ach_list.append(rec_list)

        myString = 'Target Vs Achievement Route Item ' + '\n'
        myString += 'Year-Month,' + rpt_year+'-'+monthName+ '\n'

        if achDateFrom!='' and achDateTo!='':
            myString += 'Achievement Date,' + str(achDateFrom) +' To '+str(achDateTo)+ '\n'

        myString += '\n'


        myString += 'SL,Division Id,Division Name,Zone Id, Zone Name,Area Id, Area Name,Market Id, Market Name,Item Id,Item Name,Amount Target,Amount Achieved,Volume Target,Volume Achieved,Last Invoice Date\n'
        sl = 0
        total = 0
        for i in range(len(records)):
            recStr = records[i]
            sl += 1

            level0 = recStr['level0']
            level0_name = recStr['level0_name']
            level1 = recStr['level1']
            level1_name = recStr['level1_name']
            level2 = recStr['level2']
            level2_name = recStr['level2_name']
            level3 = recStr['level3']
            level3_name = recStr['level3_name']

            item_id = recStr['item_id']
            item_name = recStr['item_name']

            target_amt = recStr['target_amt']
            ach_amt = recStr['ach_amt']

            target_qty = recStr['target_qty']
            ach_qty = recStr['ach_qty']
            last_inv_date=recStr['last_inv_date']


            myString += str(sl) + ',' + str(level0) + ',' + str(level0_name) + ',' + str(level1) + ',' + str(
                level1_name) + ',' + str(level2) + ',' + str(level2_name) + ',' + str(level3) + ',' + str(
                level3_name) + ',' + str(item_id)+ ',' + str(item_name)+ ',' + str(target_amt)+ ',' + str(ach_amt)+ ',' + str(target_qty)+ ',' + str(ach_qty)+ ',' + str(last_inv_date) + '\n'




        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=download_target_vs_ach_route_item.csv'
        return str(myString)





def target_vs_ach_route_item():
    c_id = session.cid

    response.title = 'Target Vs Achievement Route Item'

    rpt_year = request.vars.rpt_year
    rpt_month = request.vars.rpt_month
    rpt_ach_date_from = request.vars.rpt_ach_date_from
    rpt_ach_date_to = request.vars.rpt_ach_date_to

    monthArr = str(rpt_month).split('-')
    if len(monthArr) == 2:
        monthNo = monthArr[0]
        monthName = monthArr[1]
    else:
        monthNo = ''
        monthName = ''

    monthFirstDate = str(rpt_year) + '-' + str(monthNo) + '-01'

    monthFlag = True
    try:
        monthFirstDate = datetime.datetime.strptime(str(monthFirstDate), '%Y-%m-%d')
    except:
        monthFlag = False

    try:
        if int(rpt_ach_date_from)<10:
            rpt_ach_date_from='0'+str(rpt_ach_date_from)

        achDateFrom = str(rpt_year) + '-' + str(monthNo) + '-' + str(rpt_ach_date_from)

        if int(rpt_ach_date_to)<10:
            rpt_ach_date_to='0'+str(rpt_ach_date_to)

        achDateTo = str(rpt_year) + '-' + str(monthNo) + '-' + str(rpt_ach_date_to)

    except:
        achDateFrom = ''
        achDateTo = ''

    # --------------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # ---------------end paging

    if monthFlag==False:
        response.flash='Required valid Year and Month'
    else:
        condition2 = ''
        if achDateFrom != '' and achDateTo != '':
            condition2 = " AND invoice_date>='" + str(achDateFrom) + "' AND invoice_date<='" + str(achDateTo) + "' "
        else:
            condition2 = " AND invoice_ym_date = '" + str(monthFirstDate)[:10] + "' "

        sql1 = "SELECT a.level0 as level0,a.level0_name as level0_name,a.level1 as level1,a.level1_name as level1_name,a.level2 as level2,a.level2_name as level2_name,a.level3 as level3,a.level3_name as level3_name,b.item_id as item_id,b.item_name as item_name,sum(b.target_qty*b.price) as target_amt,0 as ach_amt,sum(b.target_qty) as target_qty,0 as ach_qty FROM sm_level a,target_vs_achievement_route_item b WHERE a.cid = '" + c_id + "' AND a.cid=b.cid AND a.depth=3 AND a.level_id=b.territory_id AND b.first_date = '" + str(monthFirstDate)[:10]+"' GROUP BY a.level0,a.level1,a.level2,a.level3,b.item_id"
        sql2 = "SELECT level0_id as level0,level0_name as level0_name,level1_id as level1,level1_name as level1_name,level2_id as level2,level2_name as level2_name,level3_id as level3,level3_name as level3_name,item_id as item_id,item_name as item_name,0 as target_amt,sum(actual_tp*(quantity-return_qty)) as ach_amt,0 as target_qty,sum(quantity-return_qty) as ach_qty FROM sm_invoice WHERE cid = '" + c_id + "' AND status='Invoiced' "+condition2+" GROUP BY level0_id,level1_id,level2_id,level3_id,item_id"
        records = "SELECT level0,level0_name,level1,level1_name,level2,level2_name,level3,level3_name,item_id,item_name,sum(target_amt) as target_amt,sum(ach_amt) as ach_amt,sum(target_qty) as target_qty,sum(ach_qty) as ach_qty FROM ("+sql1+" union all "+sql2+") p GROUP BY level0,level1,level2,level3,item_id;" #

        records = db.executesql(records, as_dict=True)

        total_target_amt=0
        total_ach_amt=0
        for i in range(len(records)):
            recordsStr=records[i]
            total_target_amt+=recordsStr['target_amt']
            total_ach_amt += recordsStr['ach_amt']

        ach_per=0
        if total_target_amt>0:
            ach_per=(total_ach_amt/total_target_amt)*100

        # chart
        tar_ach_list = []
        # tar_ach_list_head = ['Route','Target Amount', 'Achievement Amount']
        # tar_ach_list.append(tar_ach_list_head)
        # for i in range(len(records)):
        #     recordsStr=records[i]
        #     level3 = str(recordsStr['level3'])
        #     target_amt = recordsStr['target_amt']
        #     ach_amt = recordsStr['ach_amt']
        #
        #
        #     rec_list = [level3, target_amt,ach_amt]
        #     tar_ach_list.append(rec_list)

    return dict(records=records,total_target_amt=total_target_amt,total_ach_amt=total_ach_amt,ach_per=ach_per,tar_ach_list=tar_ach_list,monthFirstDate=monthFirstDate,achDateFrom=achDateFrom,achDateTo=achDateTo,page=page, items_per_page=items_per_page)

def target_vs_ach_d():
    c_id = session.cid

    response.title = 'Target Vs Achievement'

    rpt_year = request.vars.rpt_year
    rpt_month = request.vars.rpt_month
    rpt_ach_date_from = request.vars.rpt_ach_date_from
    rpt_ach_date_to = request.vars.rpt_ach_date_to

    monthArr = str(rpt_month).split('-')
    if len(monthArr) == 2:
        monthNo = monthArr[0]
        monthName = monthArr[1]
    else:
        monthNo = ''
        monthName = ''

    monthFirstDate = str(rpt_year) + '-' + str(monthNo) + '-01'

    monthFlag = True
    try:
        monthFirstDate = datetime.datetime.strptime(str(monthFirstDate), '%Y-%m-%d')
    except:
        monthFlag = False

    try:
        if int(rpt_ach_date_from)<10:
            rpt_ach_date_from='0'+str(rpt_ach_date_from)

        achDateFrom = str(rpt_year) + '-' + str(monthNo) + '-' + str(rpt_ach_date_from)

        if int(rpt_ach_date_to)<10:
            rpt_ach_date_to='0'+str(rpt_ach_date_to)

        achDateTo = str(rpt_year) + '-' + str(monthNo) + '-' + str(rpt_ach_date_to)

    except:
        achDateFrom = ''
        achDateTo = ''

    # --------------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # ---------------end paging

    if monthFlag==False:
        response.flash='Required valid Year and Month'
    else:
        condition2 = ''
        if achDateFrom != '' and achDateTo != '':
            condition2 = " AND invoice_date>='" + str(achDateFrom) + "' AND invoice_date<='" + str(achDateTo) + "' "
        else:
            condition2 = " AND invoice_ym_date = '" + str(monthFirstDate)[:10] + "' "

        sql1 = "SELECT a.level0 as level0,a.level0_name as level0_name,a.level1 as level1,a.level1_name as level1_name,a.level2 as level2,a.level2_name as level2_name,a.level3 as level3,a.level3_name as level3_name,sum(b.target_qty*b.price) target_amt,0 as ach_amt,sum(b.target_qty) as target_qty,0 as ach_qty FROM sm_level a,target_vs_achievement_route_item b WHERE a.cid = '" + c_id + "' AND a.cid=b.cid AND a.depth=3 AND a.level_id=b.territory_id AND b.first_date = '" + str(monthFirstDate)[:10]+"' GROUP BY a.level0,a.level1,a.level2,a.level3"
        sql2 = "SELECT level0_id as level0,level0_name as level0_name,level1_id as level1,level1_name as level1_name,level2_id as level2,level2_name as level2_name,level3_id as level3,level3_name as level3_name,0 target_amt,sum(actual_tp*(quantity+bonus_qty-return_qty-return_bonus_qty)) as ach_amt,0 as target_qty,sum(quantity+bonus_qty-return_qty-return_bonus_qty) as ach_qty FROM sm_invoice WHERE cid = '" + c_id + "' AND status='Invoiced' "+condition2+" GROUP BY level0_id,level1_id,level2_id,level3_id"
        records = "SELECT level0,level0_name,level1,level1_name,level2,level2_name,level3,level3_name,sum(target_amt) as target_amt,sum(ach_amt) as ach_amt,sum(target_qty) as target_qty,sum(ach_qty) as ach_qty FROM ("+sql1+" union all "+sql2+") p GROUP BY level0,level1,level2,level3;"
        records = db.executesql(records, as_dict=True)

        total_target_amt=0
        total_ach_amt=0
        for i in range(len(records)):
            recordsStr=records[i]
            total_target_amt+=recordsStr['target_amt']
            total_ach_amt += recordsStr['ach_amt']

        ach_per=0
        if total_target_amt>0:
            ach_per=(total_ach_amt/total_target_amt)*100

        # chart
        tar_ach_list = []
        # tar_ach_list_head = ['Route','Target Amount', 'Achievement Amount']
        # tar_ach_list.append(tar_ach_list_head)
        # for i in range(len(records)):
        #     recordsStr=records[i]
        #     level3 = str(recordsStr['level3'])
        #     target_amt = recordsStr['target_amt']
        #     ach_amt = recordsStr['ach_amt']
        #
        #
        #     rec_list = [level3, target_amt,ach_amt]
        #     tar_ach_list.append(rec_list)

        myString = 'Target Vs Achievement Route Item ' + '\n'
        myString += 'Year-Month,' + rpt_year + '-' + monthName + '\n'

        if achDateFrom != '' and achDateTo != '':
            myString += 'Achievement Date,' + str(achDateFrom) + ' To ' + str(achDateTo) + '\n'

        myString += '\n'

        myString += 'SL,Division Id,Division Name,Zone Id, Zone Name,Area Id, Area Name,Market Id, Market Name,Amount Target,Amount Achieved,Volume Target,Volume Achieved\n'
        sl = 0
        total = 0
        for i in range(len(records)):
            recStr = records[i]
            sl += 1

            level0 = recStr['level0']
            level0_name = recStr['level0_name']
            level1 = recStr['level1']
            level1_name = recStr['level1_name']
            level2 = recStr['level2']
            level2_name = recStr['level2_name']
            level3 = recStr['level3']
            level3_name = recStr['level3_name']


            target_amt = recStr['target_amt']
            ach_amt = recStr['ach_amt']

            target_qty = recStr['target_qty']
            ach_qty = recStr['ach_qty']

            myString += str(sl) + ',' + str(level0) + ',' + str(level0_name) + ',' + str(level1) + ',' + str(
                level1_name) + ',' + str(level2) + ',' + str(level2_name) + ',' + str(level3) + ',' + str(
                level3_name) + ',' + str(target_amt) + ',' + str(
                ach_amt) + ',' + str(target_qty) + ',' + str(ach_qty) + '\n'

        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=download_target_vs_ach.csv'
        return str(myString)

    #return dict(records=records,total_target_amt=total_target_amt,total_ach_amt=total_ach_amt,ach_per=ach_per,tar_ach_list=tar_ach_list,monthFirstDate=monthFirstDate,page=page, items_per_page=items_per_page)


def target_vs_ach():
    c_id = session.cid

    response.title = 'Target Vs Achievement'

    rpt_year = request.vars.rpt_year
    rpt_month = request.vars.rpt_month
    rpt_ach_date_from = request.vars.rpt_ach_date_from
    rpt_ach_date_to = request.vars.rpt_ach_date_to

    monthArr = str(rpt_month).split('-')
    if len(monthArr) == 2:
        monthNo = monthArr[0]
        monthName = monthArr[1]
    else:
        monthNo = ''
        monthName = ''

    monthFirstDate = str(rpt_year) + '-' + str(monthNo) + '-01'

    monthFlag = True
    try:
        monthFirstDate = datetime.datetime.strptime(str(monthFirstDate), '%Y-%m-%d')
    except:
        monthFlag = False

    try:
        if int(rpt_ach_date_from)<10:
            rpt_ach_date_from='0'+str(rpt_ach_date_from)

        achDateFrom = str(rpt_year) + '-' + str(monthNo) + '-' + str(rpt_ach_date_from)

        if int(rpt_ach_date_to)<10:
            rpt_ach_date_to='0'+str(rpt_ach_date_to)

        achDateTo = str(rpt_year) + '-' + str(monthNo) + '-' + str(rpt_ach_date_to)

    except:
        achDateFrom = ''
        achDateTo = ''

    # --------------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # ---------------end paging

    if monthFlag==False:
        response.flash='Required valid Year and Month'
    else:
        condition2 = ''
        if achDateFrom != '' and achDateTo != '':
            condition2 = " AND invoice_date>='" + str(achDateFrom) + "' AND invoice_date<='" + str(achDateTo) + "' "
        else:
            condition2 = " AND invoice_ym_date = '" + str(monthFirstDate)[:10] + "' "

        sql1 = "SELECT a.level0 as level0,a.level0_name as level0_name,a.level1 as level1,a.level1_name as level1_name,a.level2 as level2,a.level2_name as level2_name,a.level3 as level3,a.level3_name as level3_name,sum(b.target_qty*b.price) target_amt,0 as ach_amt,sum(b.target_qty) as target_qty,0 as ach_qty FROM sm_level a,target_vs_achievement_route_item b WHERE a.cid = '" + c_id + "' AND a.cid=b.cid AND a.depth=3 AND a.level_id=b.territory_id AND b.first_date = '" + str(monthFirstDate)[:10]+"' GROUP BY a.level0,a.level1,a.level2,a.level3"
        sql2 = "SELECT level0_id as level0,level0_name as level0_name,level1_id as level1,level1_name as level1_name,level2_id as level2,level2_name as level2_name,level3_id as level3,level3_name as level3_name,0 target_amt,sum(actual_tp*(quantity+bonus_qty-return_qty-return_bonus_qty)) as ach_amt,0 as target_qty,sum(quantity+bonus_qty-return_qty-return_bonus_qty) as ach_qty FROM sm_invoice WHERE cid = '" + c_id + "' AND status='Invoiced' "+condition2+" GROUP BY level0_id,level1_id,level2_id,level3_id"
        records = "SELECT level0,level0_name,level1,level1_name,level2,level2_name,level3,level3_name,sum(target_amt) as target_amt,sum(ach_amt) as ach_amt,sum(target_qty) as target_qty,sum(ach_qty) as ach_qty FROM ("+sql1+" union all "+sql2+") p GROUP BY level0,level1,level2,level3;"
        records = db.executesql(records, as_dict=True)

        total_target_amt=0
        total_ach_amt=0
        for i in range(len(records)):
            recordsStr=records[i]
            total_target_amt+=recordsStr['target_amt']
            total_ach_amt += recordsStr['ach_amt']

        ach_per=0
        if total_target_amt>0:
            ach_per=(total_ach_amt/total_target_amt)*100

        # chart
        tar_ach_list = []
        tar_ach_list_head = ['Route','Target Amount', 'Achievement Amount']
        tar_ach_list.append(tar_ach_list_head)
        for i in range(len(records)):
            recordsStr=records[i]
            level3 = str(recordsStr['level3'])
            target_amt = recordsStr['target_amt']
            ach_amt = recordsStr['ach_amt']


            rec_list = [level3, target_amt,ach_amt]
            tar_ach_list.append(rec_list)

    return dict(records=records,total_target_amt=total_target_amt,total_ach_amt=total_ach_amt,ach_per=ach_per,tar_ach_list=tar_ach_list,monthFirstDate=monthFirstDate,achDateFrom=achDateFrom,achDateTo=achDateTo,page=page, items_per_page=items_per_page)

def new_client_summary_d():
    c_id = session.cid

    response.title = 'New Client Summary'

    fromDate = request.vars.fromDate
    toDate = request.vars.toDate

    regionValue = str(request.vars.regionValue).strip()
    areaValue = str(request.vars.areaValue).strip()
    territoryValue = str(request.vars.territoryValue).strip()
    marketValue = str(request.vars.marketValue).strip()
    repCM = str(request.vars.repCM).strip()

    if regionValue == 'None':
        regionValue = ''
    if areaValue == 'None':
        areaValue = ''
    if territoryValue == 'None':
        territoryValue = ''
    if marketValue == 'None':
        marketValue = ''
    if repCM == 'None':
        repCM = ''

    regionValueShow = regionValue

    areaValueShow = areaValue

    territoryValueShow = territoryValue

    marketValueShow = marketValue

    startDt = datetime.datetime.strptime(str(fromDate), '%Y-%m-%d')
    endDt = datetime.datetime.strptime(str(toDate), '%Y-%m-%d')
    nextDate = endDt + datetime.timedelta(days=1)

    # --------------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # ---------------end paging

    condition = ''
    if regionValue != '':
        condition += " AND a.level0 = '" + regionValue + "'"
    if areaValue != '':
        condition += " AND a.level1 = '" + areaValue + "'"

    # if repCM != '':
    #     condition += " AND rep_id = '" + repCM + "'"

    records = "SELECT a.level0 as level0,a.level0_name as level0_name,a.level1 as level1,a.level1_name as level1_name,a.level2 as level2,a.level2_name as level2_name,a.level3 as level3,a.level3_name as level3_name,count(b.id) as no_of_client FROM sm_level a,sm_client b WHERE a.cid = '" + c_id + "' AND a.cid=b.cid AND a.depth=3 AND a.level_id=b.area_id AND b.created_on >= '" + str(fromDate)+ "' AND b.created_on <= '" + str(nextDate)+ "' " + condition + " group by a.level0,a.level1,a.level2,a.level3 order by a.level0,a.level1,a.level2,a.level3"
    records = db.executesql(records, as_dict=True)

    total_client=0
    for i in range(len(records)):
        recordsStr=records[i]
        total_client+=recordsStr['no_of_client']

    if regionValue=='':
        regionValueShow='All'
    else:
        regionValueShow=regionValueShow
    
    if areaValue=='':
        areaValueShow='All'
    else:
        areaValueShow=areaValueShow
    
    fromDate=str(datetime.datetime.strptime(fromDate,'%Y-%m-%d').strftime('%d-%m-%Y '))
    toDate=str(datetime.datetime.strptime(toDate,'%Y-%m-%d').strftime('%d-%m-%Y '))
        
    myString='New Client Summary'+'\n'
    myString+='Date From,'+fromDate+'\n'
    myString+='Date To,'+toDate+'\n'
    myString+=session.level0Name+','+regionValueShow.replace(',', ';')+'\n'
    myString+=session.level1Name+','+areaValueShow.replace(',', ';')+'\n'
    myString+='Visit By,'+repCM+'\n\n'
    
    myString+='Sl,Zone Id,Zone Name,Region Id,Region Name,Area Id,Area Name,Route Id,Route Name,Count\n'
    sl=0
    total=0
    for i in range(len(records)):
        recStr=records[i]
        sl+=1
        
        level0=recStr['level0']
        level0_name=recStr['level0_name']
        level1=recStr['level1']
        level1_name=recStr['level1_name']
        level2=recStr['level2']
        level2_name=recStr['level2_name']
        level3=recStr['level3']
        level3_name=recStr['level3_name']
        
        no_of_client=recStr['no_of_client']
        
        total+=no_of_client
                        
        myString+=str(sl)+','+str(level0)+','+str(level0_name)+','+str(level1)+','+str(level1_name)+','+str(level2)+','+str(level2_name)+','+str(level3)+','+str(level3_name)+','+str(no_of_client)+'\n'
    
    myString+='Total,,,,,,,,,'+str(total)
    
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_new_client_summary.csv'   
    return str(myString)

def new_client_summary():
    c_id = session.cid

    response.title = 'New Client Summary'

    fromDate = request.vars.fromDate
    toDate = request.vars.toDate

    regionValue = str(request.vars.regionValue).strip()
    areaValue = str(request.vars.areaValue).strip()
    territoryValue = str(request.vars.territoryValue).strip()
    marketValue = str(request.vars.marketValue).strip()
    repCM = str(request.vars.repCM).strip()

    if regionValue == 'None':
        regionValue = ''
    if areaValue == 'None':
        areaValue = ''
    if territoryValue == 'None':
        territoryValue = ''
    if marketValue == 'None':
        marketValue = ''
    if repCM == 'None':
        repCM = ''

    regionValueShow = regionValue

    areaValueShow = areaValue

    territoryValueShow = territoryValue

    marketValueShow = marketValue

    startDt = datetime.datetime.strptime(str(fromDate), '%Y-%m-%d')
    endDt = datetime.datetime.strptime(str(toDate), '%Y-%m-%d')
    nextDate = endDt + datetime.timedelta(days=1)

    # --------------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # ---------------end paging

    condition = ''
    if regionValue != '':
        condition += " AND a.level0 = '" + regionValue + "'"
    if areaValue != '':
        condition += " AND a.level1 = '" + areaValue + "'"

    # if repCM != '':
    #     condition += " AND rep_id = '" + repCM + "'"

    records = "SELECT a.level0 as level0,a.level0_name as level0_name,a.level1 as level1,a.level1_name as level1_name,a.level2 as level2,a.level2_name as level2_name,a.level3 as level3,a.level3_name as level3_name,count(b.id) as no_of_client FROM sm_level a,sm_client b WHERE a.cid = '" + c_id + "' AND a.cid=b.cid AND a.depth=3 AND a.level_id=b.area_id AND b.created_on >= '" + str(fromDate)+ "' AND b.created_on <= '" + str(nextDate)+ "' " + condition + " group by a.level0,a.level1,a.level2,a.level3 order by a.level0,a.level1,a.level2,a.level3"
    records = db.executesql(records, as_dict=True)

    total_client=0
    for i in range(len(records)):
        recordsStr=records[i]
        total_client+=recordsStr['no_of_client']



    return dict(records=records,total_client=total_client, fromDate=fromDate, toDate=toDate, regionValue=regionValue,regionValueShow=regionValueShow, areaValue=areaValue, territoryValue=territoryValue,areaValueShow=areaValueShow, territoryValueShow=territoryValueShow, marketValue=marketValue,marketValueShow=marketValueShow, repCM=repCM, page=page, items_per_page=items_per_page)

def new_client_d():
    c_id = session.cid

    response.title = 'New Client Addition'

    fromDate = request.vars.fromDate
    toDate = request.vars.toDate

    regionValue = str(request.vars.regionValue).strip()
    areaValue = str(request.vars.areaValue).strip()
    territoryValue = str(request.vars.territoryValue).strip()
    marketValue = str(request.vars.marketValue).strip()
    repCM = str(request.vars.repCM).strip()

    if regionValue == 'None':
        regionValue = ''
    if areaValue == 'None':
        areaValue = ''
    if territoryValue == 'None':
        territoryValue = ''
    if marketValue == 'None':
        marketValue = ''
    if repCM == 'None':
        repCM = ''

    regionValueShow = regionValue

    areaValueShow = areaValue

    territoryValueShow = territoryValue

    marketValueShow = marketValue

    startDt = datetime.datetime.strptime(str(fromDate), '%Y-%m-%d')
    endDt = datetime.datetime.strptime(str(toDate), '%Y-%m-%d')
    nextDate = endDt + datetime.timedelta(days=1)


    # --------------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # ---------------end paging

    condition = ''
    if regionValue != '':
        condition += " AND a.level0 = '" + regionValue + "'"
    if areaValue != '':
        condition += " AND a.level1 = '" + areaValue + "'"

    # if repCM != '':
    #     condition += " AND rep_id = '" + repCM + "'"

    records = "SELECT a.level0 as level0,a.level0_name as level0_name,a.level1 as level1,a.level1_name as level1_name,a.level2 as level2,a.level2_name as level2_name,a.level3 as level3,a.level3_name as level3_name,b.client_id,b.name,b.status,b.address,b.category_id,b.category_name,b.sub_category_id,b.sub_category_name FROM sm_level a,sm_client b WHERE a.cid = '" + c_id + "' AND a.cid=b.cid AND a.depth=3 AND a.level_id=b.area_id AND b.created_on >= '" + str(fromDate)+ "' AND b.created_on <= '" + str(nextDate)+ "' " + condition + " order by a.level0,a.level1,a.level2,a.level3,b.client_id"
    records = db.executesql(records, as_dict=True)
    
    
    if regionValue=='':
        regionValueShow='All'
    else:
        regionValueShow=regionValueShow
    
    if areaValue=='':
        areaValueShow='All'
    else:
        areaValueShow=areaValueShow
    
    fromDate=str(datetime.datetime.strptime(fromDate,'%Y-%m-%d').strftime('%d-%m-%Y '))
    toDate=str(datetime.datetime.strptime(toDate,'%Y-%m-%d').strftime('%d-%m-%Y '))
        
    myString='New Client'+'\n'
    myString+='Date From,'+fromDate+'\n'
    myString+='Date To,'+toDate+'\n'
    myString+=session.level0Name+','+regionValueShow.replace(',', ';')+'\n'
    myString+=session.level1Name+','+areaValueShow.replace(',', ';')+'\n'
    myString+='Visit By,'+repCM+'\n\n'
    
    myString+='Sl,Zone Id,Zone Name,Region Id,Region Name,Area Id,Area Name,Route Id,Route Name,Client Id,Client Name,Class,Sub Class,Address\n'
    sl=0
    for i in range(len(records)):
        recStr=records[i]
        sl+=1
        
        level0=recStr['level0']
        level0_name=recStr['level0_name']
        level1=recStr['level1']
        level1_name=recStr['level1_name']
        level2=recStr['level2']
        level2_name=recStr['level2_name']
        level3=recStr['level3']
        level3_name=recStr['level3_name']
        
        client_id=recStr['client_id']
        name=recStr['name'].replace(',', ' ')
        category_id=recStr['category_id']
        sub_category_id=recStr['sub_category_id']
        address=recStr['address'].replace(',', ' ')
                        
        myString+=str(sl)+','+str(level0)+','+str(level0_name)+','+str(level1)+','+str(level1_name)+','+str(level2)+','+str(level2_name)+','+str(level3)+','+str(level3_name)+','+str(client_id)+','+str(name)+','+str(category_id)+','+str(sub_category_id)+','+str(address)+'\n'
        
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_new_client_list.csv'   
    return str(myString)


def new_client():
    c_id = session.cid

    response.title = 'New Client Addition'

    fromDate = request.vars.fromDate
    toDate = request.vars.toDate

    regionValue = str(request.vars.regionValue).strip()
    areaValue = str(request.vars.areaValue).strip()
    territoryValue = str(request.vars.territoryValue).strip()
    marketValue = str(request.vars.marketValue).strip()
    repCM = str(request.vars.repCM).strip()

    if regionValue == 'None':
        regionValue = ''
    if areaValue == 'None':
        areaValue = ''
    if territoryValue == 'None':
        territoryValue = ''
    if marketValue == 'None':
        marketValue = ''
    if repCM == 'None':
        repCM = ''

    regionValueShow = regionValue

    areaValueShow = areaValue

    territoryValueShow = territoryValue

    marketValueShow = marketValue

    startDt = datetime.datetime.strptime(str(fromDate), '%Y-%m-%d')
    endDt = datetime.datetime.strptime(str(toDate), '%Y-%m-%d')
    nextDate = endDt + datetime.timedelta(days=1)


    # --------------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # ---------------end paging

    condition = ''
    if regionValue != '':
        condition += " AND a.level0 = '" + regionValue + "'"
    if areaValue != '':
        condition += " AND a.level1 = '" + areaValue + "'"

    # if repCM != '':
    #     condition += " AND rep_id = '" + repCM + "'"

    records = "SELECT a.level0 as level0,a.level0_name as level0_name,a.level1 as level1,a.level1_name as level1_name,a.level2 as level2,a.level2_name as level2_name,a.level3 as level3,a.level3_name as level3_name,b.client_id,b.name,b.status,b.address,b.category_id,b.category_name,b.sub_category_id,b.sub_category_name FROM sm_level a,sm_client b WHERE a.cid = '" + c_id + "' AND a.cid=b.cid AND a.depth=3 AND a.level_id=b.area_id AND b.created_on >= '" + str(fromDate)+ "' AND b.created_on <= '" + str(nextDate)+ "' " + condition + " order by a.level0,a.level1,a.level2,a.level3,b.client_id"
    records = db.executesql(records, as_dict=True)



    return dict(records=records, fromDate=fromDate, toDate=toDate, regionValue=regionValue,regionValueShow=regionValueShow, areaValue=areaValue, territoryValue=territoryValue,areaValueShow=areaValueShow, territoryValueShow=territoryValueShow, marketValue=marketValue,marketValueShow=marketValueShow, repCM=repCM, page=page, items_per_page=items_per_page)

def productivity():
    c_id = session.cid

    response.title = 'Productivity'

    fromDate = request.vars.fromDate
    toDate = request.vars.toDate

    regionValue = str(request.vars.regionValue).strip()
    areaValue = str(request.vars.areaValue).strip()
    territoryValue = str(request.vars.territoryValue).strip()
    marketValue = str(request.vars.marketValue).strip()
    repCM = str(request.vars.repCM).strip()

    if regionValue == 'None':
        regionValue = ''
    if areaValue == 'None':
        areaValue = ''
    if territoryValue == 'None':
        territoryValue = ''
    if marketValue == 'None':
        marketValue = ''
    if repCM == 'None':
        repCM = ''

    regionValueShow = regionValue

    areaValueShow = areaValue

    territoryValueShow = territoryValue

    marketValueShow = marketValue

    startDt = datetime.datetime.strptime(str(fromDate), '%Y-%m-%d')
    endDt = datetime.datetime.strptime(str(toDate), '%Y-%m-%d')

    # --------------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # ---------------end paging

    condition = ''
    if regionValue != '':
        condition += " AND a.level0 = '" + regionValue + "'"
    if areaValue != '':
        condition += " AND a.level1 = '" + areaValue + "'"

    # if repCM != '':
    #     condition += " AND rep_id = '" + repCM + "'"

    repRrecords = "SELECT a.level0 as level0,a.level0_name as level0_name,a.level1 as level1,a.level1_name as level1_name,a.level2 as level2,a.level2_name as level2_name,a.level3 as level3,a.level3_name as level3_name,b.rep_id as rep_id,b.rep_name as rep_name,GROUP_CONCAT(level3) as level3_list FROM sm_level a,sm_rep_area b WHERE a.cid = '" + c_id + "' AND a.cid=b.cid AND a.depth=3 AND a.level_id=b.area_id " + condition + " GROUP BY a.level0,a.level1,a.level2;"
    repRrecords = db.executesql(repRrecords, as_dict=True)

    records = []
    total_scheduled_client = 0
    total_actual_client_call = 0
    total_coverage_per = 0
    for i in range(len(repRrecords)):
        repRrecordsStr = repRrecords[i]
        level0 = repRrecordsStr['level0']
        level0_name = repRrecordsStr['level0_name']
        level1 = repRrecordsStr['level1']
        level1_name = repRrecordsStr['level1_name']
        level2 = repRrecordsStr['level2']
        level2_name = repRrecordsStr['level2_name']
        rep_id = repRrecordsStr['rep_id']
        rep_name = repRrecordsStr['rep_name']
        level3_list = "'" + str(repRrecordsStr['level3_list']).replace(',', "','") + "'"

        # area client
        clientRecords = "SELECT count(id) as schesuled_client  FROM sm_client WHERE cid = '" + c_id + "' AND area_id in (" + level3_list + ") GROUP BY cid;"
        clientRecords = db.executesql(clientRecords, as_dict=True)
        schesuled_client = 0
        for i in range(len(clientRecords)):
            clientRecordsStr = clientRecords[i]
            schesuled_client = clientRecordsStr['schesuled_client']
            total_scheduled_client += int(schesuled_client)

        # planned visit records
        orderRecords = "SELECT count(distinct(client_id)) as actual_client_call_scheduled  FROM sm_order_head WHERE cid = '" + c_id + "' AND order_date >= '" + str(
            startDt) + "' AND order_date <= '" + str(
            endDt) + "' AND rep_id = '" + rep_id + "' AND status='Invoiced' AND visit_type='Scheduled' AND area_id in (" + level3_list + ") GROUP BY cid;"
        orderRecords = db.executesql(orderRecords, as_dict=True)

        actual_client_call_scheduled = 0
        for i in range(len(orderRecords)):
            orderRecordsStr = orderRecords[i]
            actual_client_call_scheduled = orderRecordsStr['actual_client_call_scheduled']
            total_actual_client_call += int(actual_client_call_scheduled)

        # unplanned visit records
        orderRecords1 = "SELECT count(distinct(client_id)) as actual_client_call_unscheduled  FROM sm_order_head WHERE cid = '" + c_id + "' AND order_date >= '" + str(
            startDt) + "' AND order_date <= '" + str(
            endDt) + "' AND rep_id = '" + rep_id + "' AND status='Invoiced' AND visit_type='unscheduled' AND area_id in (" + level3_list + ") GROUP BY cid;"
        orderRecords1 = db.executesql(orderRecords1, as_dict=True)

        actual_client_call_unscheduled = 0
        for i in range(len(orderRecords1)):
            orderRecordsStr1 = orderRecords1[i]
            actual_client_call_unscheduled = orderRecordsStr1['actual_client_call_unscheduled']
            total_actual_client_call += int(actual_client_call_unscheduled)

        # coverage %
        coverage_per = 0
        if schesuled_client > 0:
            coverage_per = float(actual_client_call_scheduled / schesuled_client * 100)

        dictData = {'level0': level0, 'level0_name': level0_name, 'level1': level1, 'level1_name': level1_name,
                    'level2': level2, 'level2_name': level2_name, 'rep_id': rep_id, 'rep_id': rep_id, 'rep_id': rep_id,
                    'rep_name': rep_name, 'schesuled_client': str(schesuled_client),
                    'actual_client_call_scheduled': str(actual_client_call_scheduled),
                    'actual_client_call_unscheduled': str(actual_client_call_unscheduled),
                    'coverage_per': str(coverage_per)}
        records.append(dictData)

    if total_scheduled_client > 0:
        total_coverage_per = float(total_actual_client_call / total_scheduled_client * 100)

    return dict(records=records, total_scheduled_client=total_scheduled_client,
                actual_client_call_scheduled=actual_client_call_scheduled,
                actual_client_call_unscheduled=actual_client_call_unscheduled, total_coverage_per=total_coverage_per,
                fromDate=fromDate, toDate=toDate, regionValue=regionValue, regionValueShow=regionValueShow,
                areaValue=areaValue, territoryValue=territoryValue, areaValueShow=areaValueShow,
                territoryValueShow=territoryValueShow, marketValue=marketValue, marketValueShow=marketValueShow,
                repCM=repCM, page=page, items_per_page=items_per_page)


def coverage():
    c_id = session.cid

    response.title = 'Coverage'

    fromDate = request.vars.fromDate
    toDate = request.vars.toDate

    regionValue = str(request.vars.regionValue).strip()
    areaValue = str(request.vars.areaValue).strip()
    territoryValue = str(request.vars.territoryValue).strip()
    marketValue = str(request.vars.marketValue).strip()
    repCM = str(request.vars.repCM).strip()

    if regionValue == 'None':
        regionValue = ''
    if areaValue == 'None':
        areaValue = ''
    if territoryValue == 'None':
        territoryValue = ''
    if marketValue == 'None':
        marketValue = ''
    if repCM == 'None':
        repCM = ''

    regionValueShow = regionValue

    areaValueShow = areaValue

    territoryValueShow = territoryValue

    marketValueShow = marketValue

    startDt = datetime.datetime.strptime(str(fromDate), '%Y-%m-%d')
    endDt = datetime.datetime.strptime(str(toDate), '%Y-%m-%d')

    # --------------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # ---------------end paging


    condition = ''
    if regionValue != '':
        condition += " AND a.level0 = '" + regionValue + "'"
    if areaValue != '':
        condition += " AND a.level1 = '" + areaValue + "'"

    # if repCM != '':
    #     condition += " AND rep_id = '" + repCM + "'"


    repRrecords = "SELECT a.level0 as level0,a.level0_name as level0_name,a.level1 as level1,a.level1_name as level1_name,a.level2 as level2,a.level2_name as level2_name,a.level3 as level3,a.level3_name as level3_name,b.rep_id as rep_id,b.rep_name as rep_name,GROUP_CONCAT(level3) as level3_list FROM sm_level a,sm_rep_area b WHERE a.cid = '" + c_id + "' AND a.cid=b.cid AND a.depth=3 AND a.level_id=b.area_id " + condition + " GROUP BY a.level0,a.level1,a.level2;"
    repRrecords = db.executesql(repRrecords, as_dict=True)

    records=[]
    total_scheduled_client=0
    total_actual_client_call=0
    total_coverage_per=0
    for i in range(len(repRrecords)):
        repRrecordsStr=repRrecords[i]
        level0 = repRrecordsStr['level0']
        level0_name = repRrecordsStr['level0_name']
        level1 = repRrecordsStr['level1']
        level1_name = repRrecordsStr['level1_name']
        level2 = repRrecordsStr['level2']
        level2_name = repRrecordsStr['level2_name']
        level3 = repRrecordsStr['level3']
        level3_name = repRrecordsStr['level3_name']
        rep_id=repRrecordsStr['rep_id']
        rep_name = repRrecordsStr['rep_name']
        level3_list = "'"+str(repRrecordsStr['level3_list']).replace(',',"','")+"'"

        # area client
        clientRecords = "SELECT count(id) as schesuled_client  FROM sm_client WHERE cid = '" + c_id + "' AND area_id in ("+level3_list+") GROUP BY cid;"
        clientRecords = db.executesql(clientRecords, as_dict=True)

        schesuled_client=0
        for i in range(len(clientRecords)):
            clientRecordsStr = clientRecords[i]
            schesuled_client = clientRecordsStr['schesuled_client']
            total_scheduled_client+=int(schesuled_client)

        #planned visit records
        orderRecords = "SELECT count(distinct(client_id)) as actual_client_call_scheduled  FROM sm_order_head WHERE cid = '" + c_id + "' AND order_date >= '" + str(startDt) + "' AND order_date <= '" + str(endDt) + "' AND rep_id = '" + rep_id + "' AND status='Invoiced' AND visit_type='Scheduled' AND area_id in (" + level3_list + ") GROUP BY cid;"
        orderRecords = db.executesql(orderRecords, as_dict=True)

        actual_client_call_scheduled = 0
        for i in range(len(orderRecords)):
            orderRecordsStr = orderRecords[i]
            actual_client_call_scheduled = orderRecordsStr['actual_client_call_scheduled']
            total_actual_client_call+=int(actual_client_call_scheduled)

        # unplanned visit records
        orderRecords1 = "SELECT count(distinct(client_id)) as actual_client_call_unscheduled  FROM sm_order_head WHERE cid = '" + c_id + "' AND order_date >= '" + str(startDt) + "' AND order_date <= '" + str(endDt) + "' AND rep_id = '" + rep_id + "' AND status='Invoiced' AND visit_type='unscheduled' AND area_id in (" + level3_list + ") GROUP BY cid;"
        orderRecords1 = db.executesql(orderRecords1, as_dict=True)

        actual_client_call_unscheduled = 0
        for i in range(len(orderRecords1)):
            orderRecordsStr1 = orderRecords1[i]
            actual_client_call_unscheduled = orderRecordsStr1['actual_client_call_unscheduled']
            total_actual_client_call += int(actual_client_call_unscheduled)

        # coverage %
        coverage_per=0
        if schesuled_client>0:
            coverage_per=float(actual_client_call_scheduled/schesuled_client*100)


        dictData={'level0':level0,'level0_name':level0_name,'level1':level1,'level1_name':level1_name,'level2':level2,'level2_name':level2_name,'level3':level3,'level3_name':level3_name,'rep_id':rep_id,'rep_id':rep_id,'rep_id':rep_id,'rep_name':rep_name,'schesuled_client':str(schesuled_client),'actual_client_call_scheduled':str(actual_client_call_scheduled),'actual_client_call_unscheduled':str(actual_client_call_unscheduled),'coverage_per':str(coverage_per)}
        records.append(dictData)

    if total_scheduled_client>0:
        total_coverage_per=float(total_actual_client_call/total_scheduled_client*100)

    return dict(records=records,total_scheduled_client=total_scheduled_client,actual_client_call_scheduled=actual_client_call_scheduled,actual_client_call_unscheduled=actual_client_call_unscheduled,total_coverage_per=total_coverage_per, fromDate=fromDate, toDate=toDate, regionValue=regionValue,regionValueShow=regionValueShow, areaValue=areaValue, territoryValue=territoryValue,areaValueShow=areaValueShow, territoryValueShow=territoryValueShow, marketValue=marketValue,marketValueShow=marketValueShow, repCM=repCM, page=page, items_per_page=items_per_page)

def daily_sales_item_wise():
    c_id = session.cid

    response.title = 'Daily Sales Item Wise '

    fromDate = request.vars.fromDate
    toDate = request.vars.toDate

    regionValue = str(request.vars.regionValue).strip()
    areaValue = str(request.vars.areaValue).strip()
    territoryValue = str(request.vars.territoryValue).strip()
    marketValue = str(request.vars.marketValue).strip()
    repCM = str(request.vars.repCM).strip()

    if regionValue == 'None':
        regionValue = ''
    if areaValue == 'None':
        areaValue = ''
    if territoryValue == 'None':
        territoryValue = ''
    if marketValue == 'None':
        marketValue = ''
    if repCM == 'None':
        repCM = ''

    regionValueShow = regionValue

    areaValueShow = areaValue

    territoryValueShow = territoryValue

    marketValueShow = marketValue

    startDt = datetime.datetime.strptime(str(fromDate), '%Y-%m-%d')
    endDt = datetime.datetime.strptime(str(toDate), '%Y-%m-%d')

    # --------------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # ---------------end paging

    condition = ''
    if regionValue != '':
        condition += " AND level0_id = '" + regionValue + "'"
    if areaValue != '':
        condition += " AND level1_id = '" + areaValue + "'"

    if repCM != '':
        condition += " AND rep_id = '" + repCM + "'"

    records = "SELECT depot_id,depot_name,client_id,client_name,cl_category_id,cl_category_name,cl_sub_category_id,cl_sub_category_name,rep_id,rep_name,GROUP_CONCAT(distinct(sl)) as inv_sl,sum(quantity * price) as invAmount,item_id,item_name FROM sm_invoice WHERE cid = '" + c_id + "' AND invoice_date >= '" + str(startDt) + "' AND invoice_date <= '" + str(endDt) + "' AND status= 'Invoiced' "+condition+" GROUP BY depot_id,client_id,rep_id,item_id;"
    records = db.executesql(records, as_dict=True)

    total_sales=0
    #cash sum
    recordsCashSum = "SELECT sum(quantity * price) as invAmount FROM sm_invoice WHERE cid = '" + c_id + "' AND invoice_date >= '" + str(startDt) + "' AND invoice_date <= '" + str(endDt) + "' AND status='Invoiced' AND payment_mode='CASH' "+condition+" GROUP BY cid;"
    recordsCashSum = db.executesql(recordsCashSum, as_dict=True)
    total_cash_sales=0
    for i in range(len(recordsCashSum)):
        recordsCashSumStr = recordsCashSum[i]
        invAmount = recordsCashSumStr['invAmount']
        total_cash_sales=invAmount
        total_sales+=total_cash_sales

    # Credit sum
    recordsCreditSum = "SELECT sum(quantity * price) as invAmount FROM sm_invoice WHERE cid = '" + c_id + "' AND invoice_date >= '" + str(startDt) + "' AND invoice_date <= '" + str(endDt) + "' AND status='Invoiced' AND payment_mode='CREDIT' " + condition + " GROUP BY cid;"
    recordsCreditSum = db.executesql(recordsCreditSum, as_dict=True)
    total_credit_sales = 0
    for i in range(len(recordsCreditSum)):
        recordsCreditSumStr = recordsCashSum[i]
        invAmount = recordsCreditSumStr['invAmount']
        total_credit_sales = invAmount
        total_sales += total_credit_sales



    return dict(records=records,total_cash_sales=total_cash_sales,total_credit_sales=total_credit_sales,total_sales=total_sales, fromDate=fromDate, toDate=toDate, regionValue=regionValue,regionValueShow=regionValueShow, areaValue=areaValue, territoryValue=territoryValue,areaValueShow=areaValueShow, territoryValueShow=territoryValueShow, marketValue=marketValue,marketValueShow=marketValueShow, repCM=repCM, page=page, items_per_page=items_per_page)

def customer_sales_d():
    c_id = session.cid

    response.title = 'Customer Sales '

    fromDate = request.vars.fromDate
    toDate = request.vars.toDate

    regionValue = str(request.vars.regionValue).strip()
    areaValue = str(request.vars.areaValue).strip()
    territoryValue = str(request.vars.territoryValue).strip()
    marketValue = str(request.vars.marketValue).strip()
    repCM = str(request.vars.repCM).strip()

    if regionValue == 'None':
        regionValue = ''
    if areaValue == 'None':
        areaValue = ''
    if territoryValue == 'None':
        territoryValue = ''
    if marketValue == 'None':
        marketValue = ''
    if repCM == 'None':
        repCM = ''

    regionValueShow = regionValue

    areaValueShow = areaValue

    territoryValueShow = territoryValue

    marketValueShow = marketValue

    startDt = datetime.datetime.strptime(str(fromDate), '%Y-%m-%d')
    endDt = datetime.datetime.strptime(str(toDate), '%Y-%m-%d')

    # --------------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # ---------------end paging

    condition = ''
    if regionValue != '':
        condition += " AND level0_id = '" + regionValue + "'"
    if areaValue != '':
        condition += " AND level1_id = '" + areaValue + "'"

    if repCM != '':
        condition += " AND rep_id = '" + repCM + "'"

    records = "SELECT level0_id,level0_name,level1_id,level1_name,level2_id,level2_name,level3_id,level3_name,client_id,client_name,sum(quantity) as invQty,sum(quantity * price) as invAmount,count(distinct(sl)) as invCount  FROM sm_invoice WHERE cid = '" + c_id + "' AND invoice_date >= '" + str(startDt) + "' AND invoice_date <= '" + str(endDt) + "'"+condition+" GROUP BY level0_id,level1_id,level2_id,level3_id,client_id;"
    records = db.executesql(records, as_dict=True)

        
    fromDate=str(datetime.datetime.strptime(fromDate,'%Y-%m-%d').strftime('%d-%m-%Y '))
    toDate=str(datetime.datetime.strptime(toDate,'%Y-%m-%d').strftime('%d-%m-%Y '))
        
    myString='Customer Wise Order Summary'+'\n'
    myString+='Date From,'+fromDate+'\n'
    myString+='Date To,'+toDate+'\n'
    myString+=session.level0Name+','+regionValueShow.replace(',', ';')+'\n'
    myString+=session.level1Name+','+areaValueShow.replace(',', ';')+'\n'
    myString+='Visit By,'+repCM+'\n\n'
    
    myString+='Zone Id,Zone Name,Region Id,Region Name,Area Id,Area Name,Route Id,Route Name,Client Id,Client Name,Invoice Count,Invoice Quantity,Invoice Amount\n'
    sl=0
    totalInvCount=0
    totalInvQty=0
    total=0
    for i in range(len(records)):
        recStr=records[i]
        sl+=1
        
        level0=recStr['level0_id']
        level0_name=recStr['level0_name']
        level1=recStr['level1_id']
        level1_name=recStr['level1_name']
        level2=recStr['level2_id']
        level2_name=recStr['level2_name']
        level3=recStr['level3_id']
        level3_name=recStr['level3_name']
        client_id=recStr['client_id']
        client_name=recStr['client_name']
        
        
        invCount=recStr['invCount']
        invQty=recStr['invQty']
        invAmount=recStr['invAmount']
        
        totalInvCount+=invCount
        totalInvQty+=invQty
        total+=invAmount
                        
        myString+=str(level0)+','+str(level0_name)+','+str(level1)+','+str(level1_name)+','+str(level2)+','+str(level2_name)+','+str(level3)+','+str(level3_name)+','+str(client_id)+','+str(client_name)+','+str(invCount)+','+str(invQty)+','+str(invAmount)+'\n'
    
    myString+='Total,,,,,,,,,,'+str(totalInvCount)+','+str(totalInvQty)+','+str(total)
    
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_customer_sales.csv'   
    return str(myString)
    
def customer_sales():
    c_id = session.cid

    response.title = 'Customer Sales '

    fromDate = request.vars.fromDate
    toDate = request.vars.toDate

    regionValue = str(request.vars.regionValue).strip()
    areaValue = str(request.vars.areaValue).strip()
    territoryValue = str(request.vars.territoryValue).strip()
    marketValue = str(request.vars.marketValue).strip()
    repCM = str(request.vars.repCM).strip()

    if regionValue == 'None':
        regionValue = ''
    if areaValue == 'None':
        areaValue = ''
    if territoryValue == 'None':
        territoryValue = ''
    if marketValue == 'None':
        marketValue = ''
    if repCM == 'None':
        repCM = ''

    regionValueShow = regionValue

    areaValueShow = areaValue

    territoryValueShow = territoryValue

    marketValueShow = marketValue

    startDt = datetime.datetime.strptime(str(fromDate), '%Y-%m-%d')
    endDt = datetime.datetime.strptime(str(toDate), '%Y-%m-%d')

    # --------------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # ---------------end paging

    condition = ''
    if regionValue != '':
        condition += " AND level0_id = '" + regionValue + "'"
    if areaValue != '':
        condition += " AND level1_id = '" + areaValue + "'"

    if repCM != '':
        condition += " AND rep_id = '" + repCM + "'"

    records = "SELECT level0_id,level0_name,level1_id,level1_name,level2_id,level2_name,level3_id,level3_name,client_id,client_name,sum(quantity) as invQty,sum(quantity * price) as invAmount,count(distinct(sl)) as invCount  FROM sm_invoice WHERE cid = '" + c_id + "' AND invoice_date >= '" + str(startDt) + "' AND invoice_date <= '" + str(endDt) + "'"+condition+" GROUP BY level0_id,level1_id,level2_id,level3_id,client_id;"
    records = db.executesql(records, as_dict=True)

    recordsSum = "SELECT sum(quantity) as invQty,sum(quantity * price) as invAmount,count(distinct(sl)) as invCount  FROM sm_invoice WHERE cid = '" + c_id + "' AND invoice_date >= '" + str(startDt) + "' AND invoice_date <= '" + str(endDt) + "'"+condition+" GROUP BY cid;"
    recordsSum = db.executesql(recordsSum, as_dict=True)



    return dict(records=records,recordsSum=recordsSum, fromDate=fromDate, toDate=toDate, regionValue=regionValue,regionValueShow=regionValueShow, areaValue=areaValue, territoryValue=territoryValue,areaValueShow=areaValueShow, territoryValueShow=territoryValueShow, marketValue=marketValue,marketValueShow=marketValueShow, repCM=repCM, page=page, items_per_page=items_per_page)

def customer_order_d():
    c_id = session.cid

    response.title = 'Customer Order '

    fromDate = request.vars.fromDate
    toDate = request.vars.toDate

    regionValue = str(request.vars.regionValue).strip()
    areaValue = str(request.vars.areaValue).strip()
    territoryValue = str(request.vars.territoryValue).strip()
    marketValue = str(request.vars.marketValue).strip()
    repCM = str(request.vars.repCM).strip()

    if regionValue == 'None':
        regionValue = ''
    if areaValue == 'None':
        areaValue = ''
    if territoryValue == 'None':
        territoryValue = ''
    if marketValue == 'None':
        marketValue = ''
    if repCM == 'None':
        repCM = ''

    regionValueShow = regionValue

    areaValueShow = areaValue

    territoryValueShow = territoryValue

    marketValueShow = marketValue

    startDt = datetime.datetime.strptime(str(fromDate), '%Y-%m-%d')
    endDt = datetime.datetime.strptime(str(toDate), '%Y-%m-%d')

    # --------------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # ---------------end paging

    condition = ''
    if regionValue != '':
        condition += " AND level0_id = '" + regionValue + "'"
    if areaValue != '':
        condition += " AND level1_id = '" + areaValue + "'"

    if repCM != '':
        condition += " AND rep_id = '" + repCM + "'"

    records = "SELECT level0_id,level0_name,level1_id,level1_name,level2_id,level2_name,level3_id,level3_name,client_id,client_name,sum(quantity) as orderQty,sum(quantity * price) as orderAmount,count(distinct(sl)) as orderCount  FROM sm_order WHERE cid = '" + c_id + "' AND order_date >= '" + str(startDt) + "' AND order_date <= '" + str(endDt) + "'"+condition+" GROUP BY level0_id,level1_id,level2_id,level3_id,client_id;"
    records = db.executesql(records, as_dict=True)

        
    fromDate=str(datetime.datetime.strptime(fromDate,'%Y-%m-%d').strftime('%d-%m-%Y '))
    toDate=str(datetime.datetime.strptime(toDate,'%Y-%m-%d').strftime('%d-%m-%Y '))
        
    myString='Customer Wise Order Summary'+'\n'
    myString+='Date From,'+fromDate+'\n'
    myString+='Date To,'+toDate+'\n'
    myString+=session.level0Name+','+regionValueShow.replace(',', ';')+'\n'
    myString+=session.level1Name+','+areaValueShow.replace(',', ';')+'\n'
    myString+='Visit By,'+repCM+'\n\n'
    
    myString+='Zone Id,Zone Name,Region Id,Region Name,Area Id,Area Name,Route Id,Route Name,Client Id,Client Name,Order Count,Order Quantity,Order Amount\n'
    sl=0
    totalOrderCount=0
    totalOrderQty=0
    total=0
    for i in range(len(records)):
        recStr=records[i]
        sl+=1
        
        level0=recStr['level0_id']
        level0_name=recStr['level0_name']
        level1=recStr['level1_id']
        level1_name=recStr['level1_name']
        level2=recStr['level2_id']
        level2_name=recStr['level2_name']
        level3=recStr['level3_id']
        level3_name=recStr['level3_name']
        client_id=recStr['client_id']
        client_name=recStr['client_name']
        
        
        orderCount=recStr['orderCount']
        orderQty=recStr['orderQty']
        orderAmount=recStr['orderAmount']
        
        totalOrderCount+=orderCount
        totalOrderQty+=orderQty
        total+=orderAmount
                        
        myString+=str(level0)+','+str(level0_name)+','+str(level1)+','+str(level1_name)+','+str(level2)+','+str(level2_name)+','+str(level3)+','+str(level3_name)+','+str(client_id)+','+str(client_name)+','+str(orderCount)+','+str(orderQty)+','+str(orderAmount)+'\n'
    
    myString+='Total,,,,,,,,,,'+str(totalOrderCount)+','+str(totalOrderQty)+','+str(total)
    
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_customer_order.csv'   
    return str(myString)

def customer_order():
    c_id = session.cid

    response.title = 'Customer Order '

    fromDate = request.vars.fromDate
    toDate = request.vars.toDate

    regionValue = str(request.vars.regionValue).strip()
    areaValue = str(request.vars.areaValue).strip()
    territoryValue = str(request.vars.territoryValue).strip()
    marketValue = str(request.vars.marketValue).strip()
    repCM = str(request.vars.repCM).strip()

    if regionValue == 'None':
        regionValue = ''
    if areaValue == 'None':
        areaValue = ''
    if territoryValue == 'None':
        territoryValue = ''
    if marketValue == 'None':
        marketValue = ''
    if repCM == 'None':
        repCM = ''

    regionValueShow = regionValue

    areaValueShow = areaValue

    territoryValueShow = territoryValue

    marketValueShow = marketValue

    startDt = datetime.datetime.strptime(str(fromDate), '%Y-%m-%d')
    endDt = datetime.datetime.strptime(str(toDate), '%Y-%m-%d')

    # --------------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # ---------------end paging

    condition = ''
    if regionValue != '':
        condition += " AND level0_id = '" + regionValue + "'"
    if areaValue != '':
        condition += " AND level1_id = '" + areaValue + "'"

    if repCM != '':
        condition += " AND rep_id = '" + repCM + "'"

    records = "SELECT level0_id,level0_name,level1_id,level1_name,level2_id,level2_name,level3_id,level3_name,client_id,client_name,sum(quantity) as orderQty,sum(quantity * price) as orderAmount,count(distinct(sl)) as orderCount  FROM sm_order WHERE cid = '" + c_id + "' AND order_date >= '" + str(startDt) + "' AND order_date <= '" + str(endDt) + "'"+condition+" GROUP BY level0_id,level1_id,level2_id,level3_id,client_id;"
    records = db.executesql(records, as_dict=True)

    recordsSum = "SELECT sum(quantity) as orderQty,sum(quantity * price) as orderAmount,count(distinct(sl)) as orderCount  FROM sm_order WHERE cid = '" + c_id + "' AND order_date >= '" + str(startDt) + "' AND order_date <= '" + str(endDt) + "'"+condition+" GROUP BY cid;"
    recordsSum = db.executesql(recordsSum, as_dict=True)



    return dict(records=records,recordsSum=recordsSum, fromDate=fromDate, toDate=toDate, regionValue=regionValue,regionValueShow=regionValueShow, areaValue=areaValue, territoryValue=territoryValue,areaValueShow=areaValueShow, territoryValueShow=territoryValueShow, marketValue=marketValue,marketValueShow=marketValueShow, repCM=repCM, page=page, items_per_page=items_per_page)

def missed_outlet():
    c_id = session.cid

    response.title = 'Missed Outlet'

    fromDate = request.vars.fromDate
    toDate = request.vars.toDate

    regionValue = str(request.vars.regionValue).strip()
    areaValue = str(request.vars.areaValue).strip()
    territoryValue = str(request.vars.territoryValue).strip()
    marketValue = str(request.vars.marketValue).strip()
    repCM = str(request.vars.repCM).strip()

    if regionValue == 'None':
        regionValue = ''
    if areaValue == 'None':
        areaValue = ''
    if territoryValue == 'None':
        territoryValue = ''
    if marketValue == 'None':
        marketValue = ''
    if repCM == 'None':
        repCM = ''

    regionValueShow = regionValue

    areaValueShow = areaValue

    territoryValueShow = territoryValue

    marketValueShow = marketValue

    startDt = datetime.datetime.strptime(str(fromDate), '%Y-%m-%d')
    endDt = datetime.datetime.strptime(str(toDate), '%Y-%m-%d')

    # --------------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # ---------------end paging

    # all Client id
    allClientIdList = []
    qset1 = db()
    qset1 = qset1(db.sm_level.cid == c_id)
    qset1 = qset1(db.sm_level.depth == 3)
    if regionValue != '':
        qset1 = qset1(db.sm_level.level0 == regionValue)
    if areaValue != '':
        qset1 = qset1(db.sm_level.level1 == areaValue)
    qset1 = qset1(db.sm_client.cid == c_id)
    qset1 = qset1(db.sm_client.status == 'ACTIVE')
    qset1 = qset1(db.sm_client.area_id == db.sm_level.level_id)
    clRows = qset1.select(db.sm_client.client_id, groupby=db.sm_client.client_id)

    no_of_client=0
    for row in clRows:
        client_id = row.client_id
        allClientIdList.append(client_id)
        no_of_client+=1

    # ord Client id
    ordClientIdList = []
    qset = db()
    qset = qset(db.sm_order_head.cid == c_id)
    qset = qset((db.sm_order_head.order_date >= startDt) & (db.sm_order_head.order_date <= endDt))
    if regionValue != '':
        qset = qset(db.sm_order_head.level0_id == regionValue)
    if areaValue != '':
        qset = qset(db.sm_order_head.level1_id == areaValue)
    if repCM != '':
        qset = qset(db.sm_order_head.rep_id == repCM)
    ordRows = qset.select(db.sm_order_head.client_id, groupby=db.sm_order_head.client_id)

    no_of_client_order=0
    for row in ordRows:
        client_id = row.client_id
        ordClientIdList.append(client_id)
        no_of_client_order+=1

    newClientIdList = []
    no_of_client_missed=0
    for i in range(len(allClientIdList)):
        client_id = allClientIdList[i]

        if client_id not in ordClientIdList:
            newClientIdList.append(client_id)
            no_of_client_missed+=1


    records=[]
    clRows = db((db.sm_client.cid == c_id) & (db.sm_client.client_id.belongs(newClientIdList))).select(db.sm_client.client_id,db.sm_client.name,db.sm_client.area_id,db.sm_client.depot_id,db.sm_client.depot_name)
    for row in clRows:
        client_id = row.client_id
        name = str(row.name)
        area_id = str(row.area_id)
        depot_id = str(row.depot_id)
        depot_name = str(row.depot_name)


        levelRows=db((db.sm_level.cid == c_id) & (db.sm_level.level_id == area_id)& (db.sm_level.depth == 3)).select(db.sm_level.level0,db.sm_level.level0_name,db.sm_level.level1,db.sm_level.level1_name,db.sm_level.level2,db.sm_level.level2_name,db.sm_level.level3,db.sm_level.level3_name,limitby=(0,1))

        if levelRows:
            level0=levelRows[0].level0
            level0_name = levelRows[0].level0_name
            level1 = levelRows[0].level1
            level1_name = levelRows[0].level1_name
            level2 = levelRows[0].level2
            level2_name = levelRows[0].level2_name
            level3 = levelRows[0].level3
            level3_name = levelRows[0].level3_name


        dictData = {'level0': level0,'level0_name': level0_name,'level1': level1,'level1_name': level1_name,'level2': level2,'level2_name': level2_name,'level3': level3,'level3_name': level3_name,'client_id': client_id, 'name': name, 'area_id': area_id,'depot_id':depot_id,'depot_name':depot_name}
        records.append(dictData)


    return dict(records=records,no_of_client=no_of_client,no_of_client_order=no_of_client_order,no_of_client_missed=no_of_client_missed, fromDate=fromDate, toDate=toDate, regionValue=regionValue,regionValueShow=regionValueShow, areaValue=areaValue, territoryValue=territoryValue,areaValueShow=areaValueShow, territoryValueShow=territoryValueShow, marketValue=marketValue,marketValueShow=marketValueShow, repCM=repCM, page=page, items_per_page=items_per_page)


def zero_sales_outlet():
    c_id = session.cid

    response.title = 'Zero Sales Outlet'

    fromDate = request.vars.fromDate
    toDate = request.vars.toDate

    regionValue = str(request.vars.regionValue).strip()
    areaValue = str(request.vars.areaValue).strip()
    territoryValue = str(request.vars.territoryValue).strip()
    marketValue = str(request.vars.marketValue).strip()
    repCM = str(request.vars.repCM).strip()

    if regionValue == 'None':
        regionValue = ''
    if areaValue == 'None':
        areaValue = ''
    if territoryValue == 'None':
        territoryValue = ''
    if marketValue == 'None':
        marketValue = ''
    if repCM == 'None':
        repCM = ''

    regionValueShow = regionValue

    areaValueShow = areaValue

    territoryValueShow = territoryValue

    marketValueShow = marketValue

    startDt = datetime.datetime.strptime(str(fromDate), '%Y-%m-%d')
    endDt = datetime.datetime.strptime(str(toDate), '%Y-%m-%d')

    # --------------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # ---------------end paging

    # ord Client id
    ordClientIdList = []
    qset = db()
    qset = qset(db.sm_order_head.cid == c_id)
    qset = qset((db.sm_order_head.order_date >= startDt) & (db.sm_order_head.order_date <= endDt))

    if regionValue != '':
        qset = qset(db.sm_order_head.level0_id == regionValue)
    if areaValue != '':
        qset = qset(db.sm_order_head.level1_id == areaValue)

    if repCM != '':
        qset = qset(db.sm_order_head.rep_id == repCM)

    ordRows = qset.select(db.sm_order_head.client_id, groupby=db.sm_order_head.client_id)

    for row in ordRows:
        client_id = row.client_id
        ordClientIdList.append(client_id)

    # invoice Client id
    invClientIdList=[]
    qset1=db()
    qset1=qset1(db.sm_invoice_head.cid == c_id)
    qset1 = qset1((db.sm_invoice_head.invoice_date >= startDt) & (db.sm_invoice_head.invoice_date <= endDt))
    qset1 = qset1(db.sm_invoice_head.status == 'Invoiced')

    if regionValue != '':
        qset1 = qset1(db.sm_invoice_head.level0_id == regionValue)
    if areaValue != '':
        qset1 = qset1(db.sm_invoice_head.level1_id == areaValue)

    if repCM != '':
        qset1 = qset1(db.sm_invoice_head.rep_id == repCM)

    invRows = qset1.select(db.sm_invoice_head.client_id,groupby=db.sm_invoice_head.client_id)

    for row in invRows:
        client_id=row.client_id
        invClientIdList.append(client_id)

    newClientIdList=[]
    for i in range(len(ordClientIdList)):
        client_id=ordClientIdList[i]

        if client_id not in invClientIdList:
            newClientIdList.append(client_id)


    records=[]
    clRows = db((db.sm_client.cid == c_id) & (db.sm_client.client_id.belongs(newClientIdList)) & (db.sm_client.status == 'ACTIVE')).select(db.sm_client.client_id,db.sm_client.name,db.sm_client.area_id,db.sm_client.address,db.sm_client.depot_id,db.sm_client.depot_name,db.sm_client.thana,db.sm_client.district)
    for row in clRows:
        client_id = row.client_id
        name = str(row.name)
        area_id = str(row.area_id)
        address = str(row.address)
        depot_id = str(row.depot_id)
        depot_name = str(row.depot_name)
        thana = str(row.thana)
        district = str(row.district)


        levelRows=db((db.sm_level.cid == c_id) & (db.sm_level.level_id == area_id)& (db.sm_level.depth == 3)).select(db.sm_level.level0,db.sm_level.level0_name,db.sm_level.level1,db.sm_level.level1_name,db.sm_level.level2,db.sm_level.level2_name,db.sm_level.level3,db.sm_level.level3_name,limitby=(0,1))

        if levelRows:
            level0=levelRows[0].level0
            level0_name = levelRows[0].level0_name
            level1 = levelRows[0].level1
            level1_name = levelRows[0].level1_name
            level2 = levelRows[0].level2
            level2_name = levelRows[0].level2_name
            level3 = levelRows[0].level3
            level3_name = levelRows[0].level3_name


        dictData = {'level0': level0,'level0_name': level0_name,'level1': level1,'level1_name': level1_name,'level2': level2,'level2_name': level2_name,'level3': level3,'level3_name': level3_name,'client_id': client_id, 'name': name, 'area_id': area_id,'depot_id':depot_id,'depot_name':depot_name}
        records.append(dictData)

    return dict(records=records, fromDate=fromDate, toDate=toDate, regionValue=regionValue,regionValueShow=regionValueShow, areaValue=areaValue, territoryValue=territoryValue,areaValueShow=areaValueShow, territoryValueShow=territoryValueShow, marketValue=marketValue,marketValueShow=marketValueShow, repCM=repCM, page=page, items_per_page=items_per_page)

def inactive_user():
    c_id = session.cid

    response.title = 'Inactive user day wise'

    fromDate = request.vars.fromDate
    toDate = request.vars.toDate

    regionValue = str(request.vars.regionValue).strip()
    areaValue = str(request.vars.areaValue).strip()
    territoryValue = str(request.vars.territoryValue).strip()
    marketValue = str(request.vars.marketValue).strip()
    repCM = str(request.vars.repCM).strip()

    if regionValue == 'None':
        regionValue = ''
    if areaValue == 'None':
        areaValue = ''
    if territoryValue == 'None':
        territoryValue = ''
    if marketValue == 'None':
        marketValue = ''
    if repCM == 'None':
        repCM = ''

    regionValueShow = regionValue

    areaValueShow = areaValue

    territoryValueShow = territoryValue

    marketValueShow = marketValue

    startDt = datetime.datetime.strptime(str(fromDate), '%Y-%m-%d')
    endDt = datetime.datetime.strptime(str(toDate), '%Y-%m-%d')

    # --------------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # ---------------end paging
    condition = ''
    condition += " AND b.cid = '" + c_id + "'"
    condition += " AND b.depth = 3"
    if regionValue != '':
        condition += " AND b.level0 = '" + regionValue + "'"
    if areaValue != '':
        condition += " AND b.level1 = '" + areaValue + "'"

    if repCM != '':
        condition += " AND a.rep_id = '" + repCM + "'"

    trackRecords = "SELECT b.level0 as level0,b.level1 as level1,b.level2 as level2,a.rep_id as rep_id FROM sm_tracking_table a,sm_level b WHERE a.cid = '" + c_id + "' AND a.visit_date >= '" + str(startDt) + "' AND a.visit_date <= '" + str(endDt) + "' AND a.cid = b.cid AND b.depth=3 AND a.area_id=b.level_id " + condition + " GROUP BY b.level0,b.level1,b.level2,a.rep_id;"
    trackRecords = db.executesql(trackRecords, as_dict=True)


    repRecords = "SELECT b.level0 as level0,b.level0_name as level0_name,b.level1 as level1,b.level1_name as level1_name,b.level2 as level2,b.level2_name as level2_name,a.rep_id as rep_id,a.rep_name as rep_name  FROM sm_rep_area a,sm_level b WHERE a.cid = '" + c_id + "' AND a.cid = b.cid AND b.depth=3 AND a.area_id=b.level_id " + condition + "  GROUP BY b.level0,b.level1,b.level2 order BY b.level0,b.level1,b.level2,a.rep_id;"
    repRecords = db.executesql(repRecords, as_dict=True)

    records = []
    for i in range(len(repRecords)):
        repRecordStr = repRecords[i]
        level0 = str(repRecordStr['level0'])
        level0_name = str(repRecordStr['level0_name'])
        level1 = str(repRecordStr['level1'])
        level1_name = str(repRecordStr['level1_name'])
        level2 = str(repRecordStr['level2'])
        level2_name = str(repRecordStr['level2_name'])

        rep_id = str(repRecordStr['rep_id'])
        rep_name = str(repRecordStr['rep_name'])

        attendance_flag=0
        for j in range(len(trackRecords)):
            trackRecordStr = trackRecords[j]
            level01 = str(repRecordStr['level0'])
            level11 = str(repRecordStr['level1'])
            level21 = str(repRecordStr['level2'])
            rep_id1 = trackRecordStr['rep_id']

            if level01==level0 and level11==level1 and level21==level2 and rep_id1 == rep_id:
                attendance_flag=1
                break

        if int(attendance_flag)==0:
            dictData = {'level0': level0,'level0_name': level0_name,'level1': level1,'level1_name': level1_name,'level2': level2,'level2_name': level2_name,'rep_id': rep_id, 'rep_name': rep_name}
            records.append(dictData)

    return dict(records=records, fromDate=fromDate, toDate=toDate, regionValue=regionValue,
                regionValueShow=regionValueShow, areaValue=areaValue, territoryValue=territoryValue,
                areaValueShow=areaValueShow, territoryValueShow=territoryValueShow, marketValue=marketValue,
                marketValueShow=marketValueShow, repCM=repCM, page=page, items_per_page=items_per_page)

def sr_attendance():
    c_id = session.cid

    response.title = 'SR Wise Attendance'

    fromDate = request.vars.fromDate
    toDate = request.vars.toDate

    regionValue = str(request.vars.regionValue).strip()
    areaValue = str(request.vars.areaValue).strip()
    territoryValue = str(request.vars.territoryValue).strip()
    marketValue = str(request.vars.marketValue).strip()
    repCM = str(request.vars.repCM).strip()

    if regionValue == 'None':
        regionValue = ''
    if areaValue == 'None':
        areaValue = ''
    if territoryValue == 'None':
        territoryValue = ''
    if marketValue == 'None':
        marketValue = ''
    if repCM == 'None':
        repCM = ''

    regionValueShow = regionValue

    areaValueShow = areaValue

    territoryValueShow = territoryValue

    marketValueShow = marketValue

    startDt = datetime.datetime.strptime(str(fromDate), '%Y-%m-%d')
    endDt = datetime.datetime.strptime(str(toDate), '%Y-%m-%d')

    # --------------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # ---------------end paging
    condition=''
    condition+= " AND b.cid = '"+c_id+"'"
    condition += " AND b.depth = 3"
    if regionValue!='':
        condition+= " AND b.level0 = '"+regionValue+"'"
    if areaValue!='':
        condition+= " AND b.level1 = '"+areaValue+"'"

    if repCM!='':
        condition += " AND a.rep_id = '" + repCM + "'"

    records = "SELECT b.level0 as level0,b.level0_name as level0_name,b.level1 as level1,b.level1_name as level1_name,b.level2 as level2,b.level2_name as level2_name,a.rep_id as rep_id,a.rep_name as rep_name,count(distinct(a.visit_date)) as no_of_visit_day FROM sm_tracking_table a,sm_level b WHERE a.cid = '" + c_id + "' AND a.visit_date >= '" + str(startDt) + "' AND a.visit_date <= '" + str(endDt) + "' AND a.cid = b.cid AND b.depth=3 AND a.area_id=b.level_id "+condition+" GROUP BY b.level0,b.level1,b.level2,a.rep_id;"
    records = db.executesql(records, as_dict=True)

    return dict(records=records, fromDate=fromDate, toDate=toDate, regionValue=regionValue,
                regionValueShow=regionValueShow, areaValue=areaValue, territoryValue=territoryValue,
                areaValueShow=areaValueShow, territoryValueShow=territoryValueShow, marketValue=marketValue,
                marketValueShow=marketValueShow, repCM=repCM, page=page, items_per_page=items_per_page)

def sr_wise_sales_d():
    c_id = session.cid

    response.title = 'SR Wise Sales '

    fromDate = request.vars.fromDate
    toDate = request.vars.toDate

    regionValue = str(request.vars.regionValue).strip()
    areaValue = str(request.vars.areaValue).strip()
    territoryValue = str(request.vars.territoryValue).strip()
    marketValue = str(request.vars.marketValue).strip()
    repCM = str(request.vars.repCM).strip()

    if regionValue == 'None':
        regionValue = ''
    if areaValue == 'None':
        areaValue = ''
    if territoryValue == 'None':
        territoryValue = ''
    if marketValue == 'None':
        marketValue = ''
    if repCM == 'None':
        repCM = ''

    regionValueShow = regionValue

    areaValueShow = areaValue

    territoryValueShow = territoryValue

    marketValueShow = marketValue

    startDt = datetime.datetime.strptime(str(fromDate), '%Y-%m-%d')
    endDt = datetime.datetime.strptime(str(toDate), '%Y-%m-%d')

    # --------------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # ---------------end paging

    condition = ''
    if regionValue != '':
        condition += " AND level0_id = '" + regionValue + "'"
    if areaValue != '':
        condition += " AND level1_id = '" + areaValue + "'"

    if repCM != '':
        condition += " AND rep_id = '" + repCM + "'"

    records = "SELECT level0_id,level0_name,level1_id,level1_name,level2_id,level2_name,rep_id,rep_name,sum(quantity) as invQty,sum(quantity * price) as invAmount,count(distinct(sl)) as invCount  FROM sm_invoice WHERE cid = '" + c_id + "' AND invoice_date >= '" + str(startDt) + "' AND invoice_date <= '" + str(endDt) + "'"+condition+" GROUP BY level0_id,level1_id,level2_id,rep_id;"
    records = db.executesql(records, as_dict=True)

        
    fromDate=str(datetime.datetime.strptime(fromDate,'%Y-%m-%d').strftime('%d-%m-%Y '))
    toDate=str(datetime.datetime.strptime(toDate,'%Y-%m-%d').strftime('%d-%m-%Y '))
        
    myString='SR Wise Sales Summary'+'\n'
    myString+='Date From,'+fromDate+'\n'
    myString+='Date To,'+toDate+'\n'
    myString+=session.level0Name+','+regionValueShow.replace(',', ';')+'\n'
    myString+=session.level1Name+','+areaValueShow.replace(',', ';')+'\n'
    myString+='Visit By,'+repCM+'\n\n'
    
    myString+='Zone Id,Zone Name,Region Id,Region Name,Area Id,Area Name,SR Id,SR Name,Invoice Amount\n'
    sl=0
    total=0
    for i in range(len(records)):
        recStr=records[i]
        sl+=1
        
        level0=recStr['level0_id']
        level0_name=recStr['level0_name']
        level1=recStr['level1_id']
        level1_name=recStr['level1_name']
        level2=recStr['level2_id']
        level2_name=recStr['level2_name']
        rep_id=recStr['rep_id']
        rep_name=recStr['rep_name']
        
        invAmount=recStr['invAmount']
        
        total+=invAmount
                        
        myString+=str(level0)+','+str(level0_name)+','+str(level1)+','+str(level1_name)+','+str(level2)+','+str(level2_name)+','+str(rep_id)+','+str(rep_name)+','+str(invAmount)+'\n'
    
    myString+='Total,,,,,,,,'+str(total)
    
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_sr_wise_sales.csv'   
    return str(myString)
    
def sr_wise_sales():
    c_id = session.cid

    response.title = 'SR Wise Sales '

    fromDate = request.vars.fromDate
    toDate = request.vars.toDate

    regionValue = str(request.vars.regionValue).strip()
    areaValue = str(request.vars.areaValue).strip()
    territoryValue = str(request.vars.territoryValue).strip()
    marketValue = str(request.vars.marketValue).strip()
    repCM = str(request.vars.repCM).strip()

    if regionValue == 'None':
        regionValue = ''
    if areaValue == 'None':
        areaValue = ''
    if territoryValue == 'None':
        territoryValue = ''
    if marketValue == 'None':
        marketValue = ''
    if repCM == 'None':
        repCM = ''

    regionValueShow = regionValue

    areaValueShow = areaValue

    territoryValueShow = territoryValue

    marketValueShow = marketValue

    startDt = datetime.datetime.strptime(str(fromDate), '%Y-%m-%d')
    endDt = datetime.datetime.strptime(str(toDate), '%Y-%m-%d')

    # --------------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # ---------------end paging

    condition = ''
    if regionValue != '':
        condition += " AND level0_id = '" + regionValue + "'"
    if areaValue != '':
        condition += " AND level1_id = '" + areaValue + "'"

    if repCM != '':
        condition += " AND rep_id = '" + repCM + "'"

    records = "SELECT level0_id,level0_name,level1_id,level1_name,level2_id,level2_name,rep_id,rep_name,sum(quantity) as orderQty,sum(quantity * price) as orderAmount,count(distinct(sl)) as orderCount  FROM sm_invoice WHERE cid = '" + c_id + "' AND invoice_date >= '" + str(startDt) + "' AND invoice_date <= '" + str(endDt) + "'"+condition+" GROUP BY level0_id,level1_id,level2_id,rep_id;"
    records = db.executesql(records, as_dict=True)

    recordsSum=[]
    recordsSum = "SELECT sum(quantity) as invQty,sum(quantity * price) as invAmount,count(distinct(sl)) as invCount  FROM sm_invoice WHERE cid = '" + c_id + "' AND invoice_date >= '" + str(startDt) + "' AND invoice_date <= '" + str(endDt) + "'"+condition+" GROUP BY cid;"
    recordsSum = db.executesql(recordsSum, as_dict=True)
    
    
    sr_wise_sales_list = []
    sr_wise_sales_list_head = ['SR', 'Sales']
    sr_wise_sales_list.append(sr_wise_sales_list_head)
    for i in range(len(records)):
        recordsStr = records[i]
        rep_id = str(recordsStr['rep_id'])
        rep_name = str(recordsStr['rep_name'])
        orderAmount = recordsStr['orderAmount']

        rep=rep_name+' ('+rep_id+') '

        sales_list = [rep, orderAmount]
        sr_wise_sales_list.append(sales_list)


    return dict(records=records,recordsSum=recordsSum,sr_wise_sales_list=sr_wise_sales_list, fromDate=fromDate, toDate=toDate, regionValue=regionValue,regionValueShow=regionValueShow, areaValue=areaValue, territoryValue=territoryValue,areaValueShow=areaValueShow, territoryValueShow=territoryValueShow, marketValue=marketValue,marketValueShow=marketValueShow, repCM=repCM, page=page, items_per_page=items_per_page)

def sr_wise_visit_d():
    c_id = session.cid

    response.title = 'SR Wise Order '

    fromDate = request.vars.fromDate
    toDate = request.vars.toDate

    regionValue = str(request.vars.regionValue).strip()
    areaValue = str(request.vars.areaValue).strip()
    territoryValue = str(request.vars.territoryValue).strip()
    marketValue = str(request.vars.marketValue).strip()
    repCM = str(request.vars.repCM).strip()

    if regionValue == 'None':
        regionValue = ''
    if areaValue == 'None':
        areaValue = ''
    if territoryValue == 'None':
        territoryValue = ''
    if marketValue == 'None':
        marketValue = ''
    if repCM == 'None':
        repCM = ''

    regionValueShow = regionValue

    areaValueShow = areaValue

    territoryValueShow = territoryValue

    marketValueShow = marketValue

    startDt = datetime.datetime.strptime(str(fromDate), '%Y-%m-%d')
    endDt = datetime.datetime.strptime(str(toDate), '%Y-%m-%d')

    # --------------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # ---------------end paging

    condition = ''
    if regionValue != '':
        condition += " AND level0_id = '" + regionValue + "'"
    if areaValue != '':
        condition += " AND level1_id = '" + areaValue + "'"

    if repCM != '':
        condition += " AND rep_id = '" + repCM + "'"

    records = "SELECT level0_id,level0_name,level1_id,level1_name,level2_id,level2_name,rep_id,rep_name,depot_id,depot_name,sum(quantity) as orderQty,sum(quantity * price) as orderAmount,count(distinct(sl)) as orderCount  FROM sm_order WHERE cid = '" + c_id + "' AND order_date >= '" + str(startDt) + "' AND order_date <= '" + str(endDt) + "'"+condition+" GROUP BY level0_id,level1_id,level2_id,rep_id;"
    records = db.executesql(records, as_dict=True)

    #recordsSum=[]
    #recordsSum = "SELECT sum(quantity) as orderQty,sum(quantity * price) as orderAmount,count(distinct(sl)) as orderCount  FROM sm_order WHERE cid = '" + c_id + "' AND order_date >= '" + str(startDt) + "' AND order_date <= '" + str(endDt) + "'"+condition+" GROUP BY cid;"
    #recordsSum = db.executesql(recordsSum, as_dict=True)

        
    fromDate=str(datetime.datetime.strptime(fromDate,'%Y-%m-%d').strftime('%d-%m-%Y '))
    toDate=str(datetime.datetime.strptime(toDate,'%Y-%m-%d').strftime('%d-%m-%Y '))
        
    myString='SR Wise Order Summary'+'\n'
    myString+='Date From,'+fromDate+'\n'
    myString+='Date To,'+toDate+'\n'
    myString+=session.level0Name+','+regionValueShow.replace(',', ';')+'\n'
    myString+=session.level1Name+','+areaValueShow.replace(',', ';')+'\n'
    myString+='Visit By,'+repCM+'\n\n'
    
    myString+='Zone Id,Zone Name,Region Id,Region Name,Area Id,Area Name,SR Id,SR Name,Depot Id, Depot Name,Order Amount\n'
    sl=0
    total=0
    for i in range(len(records)):
        recStr=records[i]
        sl+=1
        
        level0=recStr['level0_id']
        level0_name=recStr['level0_name']
        level1=recStr['level1_id']
        level1_name=recStr['level1_name']
        level2=recStr['level2_id']
        level2_name=recStr['level2_name']
        rep_id=recStr['rep_id']
        rep_name=recStr['rep_name']
        depot_id=recStr['depot_id']
        depot_name=recStr['depot_name']
        
        orderAmount=recStr['orderAmount']
        
        total+=orderAmount
                        
        myString+=str(level0)+','+str(level0_name)+','+str(level1)+','+str(level1_name)+','+str(level2)+','+str(level2_name)+','+str(rep_id)+','+str(rep_name)+','+str(depot_id)+','+str(depot_name)+','+str(orderAmount)+'\n'
    
    myString+='Total,,,,,,,,,,'+str(total)
    
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_sr_wise_visit.csv'   
    return str(myString)
    
def sr_wise_visit():
    c_id = session.cid

    response.title = 'SR Wise Order '

    fromDate = request.vars.fromDate
    toDate = request.vars.toDate

    regionValue = str(request.vars.regionValue).strip()
    areaValue = str(request.vars.areaValue).strip()
    territoryValue = str(request.vars.territoryValue).strip()
    marketValue = str(request.vars.marketValue).strip()
    repCM = str(request.vars.repCM).strip()

    if regionValue == 'None':
        regionValue = ''
    if areaValue == 'None':
        areaValue = ''
    if territoryValue == 'None':
        territoryValue = ''
    if marketValue == 'None':
        marketValue = ''
    if repCM == 'None':
        repCM = ''

    regionValueShow = regionValue

    areaValueShow = areaValue

    territoryValueShow = territoryValue

    marketValueShow = marketValue

    startDt = datetime.datetime.strptime(str(fromDate), '%Y-%m-%d')
    endDt = datetime.datetime.strptime(str(toDate), '%Y-%m-%d')

    # --------------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # ---------------end paging

    condition = ''
    if regionValue != '':
        condition += " AND level0_id = '" + regionValue + "'"
    if areaValue != '':
        condition += " AND level1_id = '" + areaValue + "'"

    if repCM != '':
        condition += " AND rep_id = '" + repCM + "'"

    records = "SELECT level0_id,level0_name,level1_id,level1_name,level2_id,level2_name,rep_id,rep_name,depot_id,depot_name,sum(quantity) as orderQty,sum(quantity * price) as orderAmount,count(distinct(sl)) as orderCount  FROM sm_order WHERE cid = '" + c_id + "' AND order_date >= '" + str(startDt) + "' AND order_date <= '" + str(endDt) + "'"+condition+" GROUP BY level0_id,level1_id,level2_id,rep_id;"
    records = db.executesql(records, as_dict=True)

    recordsSum=[]
    recordsSum = "SELECT sum(quantity) as orderQty,sum(quantity * price) as orderAmount,count(distinct(sl)) as orderCount  FROM sm_order WHERE cid = '" + c_id + "' AND order_date >= '" + str(startDt) + "' AND order_date <= '" + str(endDt) + "'"+condition+" GROUP BY cid;"
    recordsSum = db.executesql(recordsSum, as_dict=True)

    sr_wise_visit_list = []
    sr_wise_visit_list_head = ['SR', 'Order']
    sr_wise_visit_list.append(sr_wise_visit_list_head)
    for i in range(len(records)):
        recordsStr = records[i]
        rep_id = str(recordsStr['rep_id'])
        rep_name = str(recordsStr['rep_name'])
        orderAmount = recordsStr['orderAmount']

        rep = rep_name + ' (' + rep_id + ') '

        visit_list = [rep, orderAmount]
        sr_wise_visit_list.append(visit_list)


    return dict(records=records,recordsSum=recordsSum,sr_wise_visit_list=sr_wise_visit_list, fromDate=fromDate, toDate=toDate, regionValue=regionValue,regionValueShow=regionValueShow, areaValue=areaValue, territoryValue=territoryValue,areaValueShow=areaValueShow, territoryValueShow=territoryValueShow, marketValue=marketValue,marketValueShow=marketValueShow, repCM=repCM, page=page, items_per_page=items_per_page)


def dashboard():
    c_id = session.cid

    response.title = 'Dashboard'

    fromDate = request.vars.fromDate
    toDate = request.vars.toDate

    regionValue = str(request.vars.regionValue).strip()
    areaValue = str(request.vars.areaValue).strip()
    territoryValue = str(request.vars.territoryValue).strip()
    marketValue = str(request.vars.marketValue).strip()
    repCM = str(request.vars.repCM).strip()

    if regionValue == 'None':
        regionValue = ''
    if areaValue == 'None':
        areaValue = ''
    if territoryValue == 'None':
        territoryValue = ''
    if marketValue == 'None':
        marketValue = ''
    if repCM == 'None':
        repCM = ''

    regionValueShow = regionValue

    areaValueShow = areaValue

    territoryValueShow = territoryValue

    marketValueShow = marketValue

    startDt = datetime.datetime.strptime(str(fromDate), '%Y-%m-%d')
    endDt = datetime.datetime.strptime(str(toDate), '%Y-%m-%d')
    nextDate = endDt + datetime.timedelta(days=1)

    # --------------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # ---------------end paging

    condition = ''
    if regionValue != '':
        condition += " AND level0_id = '" + regionValue + "'"
    if areaValue != '':
        condition += " AND level1_id = '" + areaValue + "'"

    # if repCM != '':
    #     condition += " AND rep_id = '" + repCM + "'"

    condition1 = ''
    if regionValue != '':
        condition1 += " AND a.level0 = '" + regionValue + "'"
    if areaValue != '':
        condition1 += " AND a.level1 = '" + areaValue + "'"


    # total sales
    salesRecords = "SELECT sum(total_amount) as total_amount  FROM sm_invoice_head WHERE cid = '" + c_id + "' and invoice_date >= '" + fromDate + "' and invoice_date <= '" + toDate + "' and status='Invoiced' " + condition + " GROUP BY cid;"
    salesRecords = db.executesql(salesRecords, as_dict=True)

    total_sales = 0
    for i in range(len(salesRecords)):
        salesRecordsStr = salesRecords[i]
        total_sales = salesRecordsStr['total_amount']

    # day wise sales last 7 days
    preDate = endDt - datetime.timedelta(days=6)
    salesRecords1 = "SELECT invoice_date,sum(total_amount) as sales_amount  FROM sm_invoice_head WHERE cid = '" + c_id + "' and invoice_date >= '" + str(preDate)[:10] + "' and invoice_date <= '" + toDate + "' and status='Invoiced' " + condition + " GROUP BY cid,invoice_date;"
    salesRecords1= db.executesql(salesRecords1, as_dict=True)

    seven_day_list=[]
    seven_day_list.append(str(preDate)[:10])
    for i in range(1,7):
        nDate = str(preDate + datetime.timedelta(days=i))[:10]
        seven_day_list.append(nDate)

    seven_day_sales_list=[]
    seven_day_sales_list_head=['Days','Sales']
    seven_day_sales_list.append(seven_day_sales_list_head)
    for i in range(len(seven_day_list)):
        invoice_date=seven_day_list[i]
        invoice_day=str(datetime.datetime.strptime(str(invoice_date), '%Y-%m-%d').strftime("%a"))

        invoice_date_sales=0
        for j in range(len(salesRecords1)):
            salesRecordsStr1 = salesRecords1[j]
            invoice_date1 = str(salesRecordsStr1['invoice_date'])
            if invoice_date==invoice_date1:
                invoice_date_sales=salesRecordsStr1['sales_amount']
                break

        sales_list=[invoice_day,invoice_date_sales]
        seven_day_sales_list.append(sales_list)

    # scheduled outlet
    total_scheduled_client = 0
    clientRecords = "SELECT count(b.id) as schesuled_client  FROM sm_level a,sm_client b WHERE a.cid = '" + c_id + "' AND a.cid=b.cid and a.depth=3 AND a.level_id=b.area_id " + condition1 + "  GROUP BY a.cid;"
    clientRecords = db.executesql(clientRecords, as_dict=True)
    for i in range(len(clientRecords)):
        clientRecordsStr = clientRecords[i]
        total_scheduled_client = clientRecordsStr['schesuled_client']

    # zero sales  scheduled outlet
    zero_sales_scheduled_client = 0
    orderRecords = "SELECT count(distinct(client_id)) as zero_sales_scheduled_client  FROM sm_order_head WHERE cid = '" + c_id + "' AND order_date >= '" + str(fromDate) + "' AND order_date <= '" + str(toDate) + "' AND status='Submitted' AND visit_type='Scheduled' " + condition + " GROUP BY cid;"
    orderRecords = db.executesql(orderRecords, as_dict=True)

    for i in range(len(orderRecords)):
        orderRecordsStr = orderRecords[i]
        zero_sales_scheduled_client = orderRecordsStr['zero_sales_scheduled_client']


    # zero sales  unscheduled outlet
    zero_sales_unscheduled_client = 0
    orderRecords1 = "SELECT count(distinct(client_id)) as zero_sales_unscheduled_client  FROM sm_order_head WHERE cid = '" + c_id + "' AND order_date >= '" + str(fromDate) + "' AND order_date <= '" + str(toDate) + "' AND status='Submitted' AND visit_type='unscheduled' " + condition + " GROUP BY cid;"
    orderRecords1 = db.executesql(orderRecords1, as_dict=True)
    for i in range(len(orderRecords1)):
        orderRecordsStr1 = orderRecords1[i]
        zero_sales_unscheduled_client = orderRecordsStr1['zero_sales_unscheduled_client']

    # sales unique outlet
    sales_unique_outlet = 0
    invRecords = "SELECT count(distinct(client_id)) as sales_unique_outlet  FROM sm_invoice_head WHERE cid = '" + c_id + "' AND invoice_date >= '" + str(fromDate) + "' AND invoice_date <= '" + str(toDate) + "' AND status='Invoiced' " + condition + " GROUP BY cid;"
    invRecords = db.executesql(invRecords, as_dict=True)

    for i in range(len(invRecords)):
        invRecordsStr = invRecords[i]
        sales_unique_outlet = invRecordsStr['sales_unique_outlet']

    # new client
    total_new_client=0
    clientRecords1 = "SELECT count(b.id) as new_client  FROM sm_level a,sm_client b WHERE a.cid = '" + c_id + "' AND b.created_on >= '" + str(startDt) + "' AND b.created_on < '" + str(nextDate) + "' AND a.cid=b.cid and a.depth=3 AND a.level_id=b.area_id " + condition1 + "  GROUP BY a.cid;"
    clientRecords1 = db.executesql(clientRecords1, as_dict=True)

    for i in range(len(clientRecords1)):
        clientRecordsStr1 = clientRecords1[i]
        total_new_client = clientRecordsStr1['new_client']


    return dict(total_sales=total_sales,seven_day_sales_list=seven_day_sales_list,total_scheduled_client=total_scheduled_client,zero_sales_scheduled_client=zero_sales_scheduled_client,zero_sales_unscheduled_client=zero_sales_unscheduled_client,sales_unique_outlet=sales_unique_outlet,total_new_client=total_new_client,
                fromDate=fromDate, toDate=toDate,
                regionValue=regionValue, regionValueShow=regionValueShow, areaValue=areaValue,
                territoryValue=territoryValue, areaValueShow=areaValueShow, territoryValueShow=territoryValueShow,
                marketValue=marketValue, marketValueShow=marketValueShow, repCM=repCM, page=page,
                items_per_page=items_per_page)



#============================================
def visitList():
    c_id=session.cid
    
    response.title='Visit List'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    areaValue=str(request.vars.areaValue).strip()
    territoryValue=str(request.vars.territoryValue).strip()
    marketValue=str(request.vars.marketValue).strip()    
    repCM=str(request.vars.repCM).strip()
    
    if regionValue=='None':
        regionValue=''
    if areaValue=='None':
        areaValue=''
    if territoryValue=='None':
        territoryValue=''
    if marketValue=='None':
        marketValue=''
    if repCM=='None':
        repCM=''
    
    
    regionValueShow=regionValue
    
    areaValueShow=areaValue
    
    territoryValueShow=territoryValue
    
    marketValueShow=marketValue
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    qset=db()
    qset=qset(db.sm_order_head.cid==c_id)
    qset=qset((db.sm_order_head.order_date>=startDt)&(db.sm_order_head.order_date<=endDt))
    
    
    market_List=[]
    if (regionValue!='' or areaValue!='' or territoryValue!='' or marketValue!=''):
        levelQset=db()
        levelQset=levelQset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
        
        if regionValue!='':
            levelQset=levelQset(db.sm_level.level0==regionValue)
        if areaValue!='':
            levelQset=levelQset(db.sm_level.level1==areaValue)
           
        if territoryValue!='':
            levelQset=levelQset(db.sm_level.level2==territoryValue)
            
        if marketValue!='':
            levelQset=levelQset(db.sm_level.level3==marketValue)
        
        rows = levelQset.select(db.sm_level.level_id, orderby=db.sm_level.level_id)
        for row in rows:
            level_id = str(row.level_id)
            market_List.append(level_id)
    
    if len(market_List)>0:
        qset=qset(db.sm_order_head.area_id.belongs(market_List))       
        
    if repCM!='':
        qset=qset(db.sm_order_head.rep_id==repCM)
    
    records=qset.select(db.sm_order_head.ALL,orderby=~db.sm_order_head.id,limitby=limitby)
    
    return dict(records=records,fromDate=fromDate,toDate=toDate,regionValue=regionValue,regionValueShow=regionValueShow,areaValue=areaValue,territoryValue=territoryValue,areaValueShow=areaValueShow,territoryValueShow=territoryValueShow,marketValue=marketValue,marketValueShow=marketValueShow,repCM=repCM,page=page,items_per_page=items_per_page)
def downloadVisitList():
    c_id=session.cid
    
    response.title='Download Visit List'
        
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    areaValue=str(request.vars.areaValue).strip()
    territoryValue=str(request.vars.territoryValue).strip()
    marketValue=str(request.vars.marketValue).strip()    
    repCM=str(request.vars.repCM).strip()
    
    if regionValue=='None':
        regionValue=''
    if areaValue=='None':
        areaValue=''
    if territoryValue=='None':
        territoryValue=''
    if marketValue=='None':
        marketValue=''
    if repCM=='None':
        repCM=''
    
    regionValueShow=regionValue    
    areaValueShow=areaValue    
    territoryValueShow=territoryValue    
    marketValueShow=marketValue
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------
    qset=db()
    qset=qset(db.sm_order_head.cid==c_id)
    qset=qset((db.sm_order_head.order_date>=startDt)&(db.sm_order_head.order_date<=endDt))
    
    market_List=[]
    if (regionValue!='' or areaValue!='' or territoryValue!='' or marketValue!=''):
        levelQset=db()
        levelQset=levelQset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
        
        if regionValue!='':
            levelQset=levelQset(db.sm_level.level0==regionValue)
        if areaValue!='':
            levelQset=levelQset(db.sm_level.level1==areaValue)
        if territoryValue!='':
            levelQset=levelQset(db.sm_level.level2==territoryValue)
        if marketValue!='':
            levelQset=levelQset(db.sm_level.level3==marketValue)
        
        rows = levelQset.select(db.sm_level.level_id, orderby=db.sm_level.level_id)
        for row in rows:
            level_id = str(row.level_id)
            market_List.append(level_id)
    
    
    if len(market_List)>0:
        qset=qset(db.sm_order_head.area_id.belongs(market_List))       
    
    if repCM!='':
        qset=qset(db.sm_order_head.rep_id==repCM)
    
    records=qset.select(db.sm_order_head.ALL,orderby=~db.sm_order_head.id)
    
    
    #REmove , from record.Cause , means new column in excel
    myString='Date From,'+fromDate+'\n'
    myString+='Date To,'+toDate+'\n'
    myString+=session.level0Name+','+regionValueShow.replace(',', ';')+'\n'
    myString+=session.level1Name+','+areaValueShow.replace(',', ';')+'\n'
    myString+='Visit By,'+repCM+'\n\n'
    
    myString+='VSL,Visit Date,Depot ID, Depot Name,VisitBy ID,VisitBy Name,VisitBy Mobile,Client ID,Client Name\n'
    for rec in records:
        rowid=rec.id
        order_date=rec.order_date
        depot_id=rec.depot_id
        depot_name=str(rec.depot_name).replace(',', ' ')
        rep_id=rec.rep_id        
        rep_name=str(rec.rep_name).replace(',', ' ')
        mobile_no=rec.mobile_no
        
        client_id=rec.client_id
        client_name=str(rec.client_name).replace(',', ' ')        
        #visit_type=rec.visit_type
        
        myString+=str(rowid)+','+str(order_date)+','+str(depot_id)+','+depot_name+','+str(rep_id)+','+rep_name+','+str(mobile_no)+','+str(client_id)+','+str(client_name)+'\n'
        
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_visit_list.csv'   
    return str(myString)

def visit_summary():
    c_id=session.cid
    
    response.title='Visit Summary'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    areaValue=str(request.vars.areaValue).strip()
    territoryValue=str(request.vars.territoryValue).strip()
    marketValue=str(request.vars.marketValue).strip()    
    repCM=str(request.vars.repCM).strip()    
    
    if regionValue=='None':
        regionValue=''
    if areaValue=='None':
        areaValue=''
    if territoryValue=='None':
        territoryValue=''
    if marketValue=='None':
        marketValue=''
    if repCM=='None':
        repCM=''
    
    regionValueShow=regionValue    
    areaValueShow=areaValue    
    territoryValueShow=territoryValue    
    marketValueShow=marketValue
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
        
    qset=db()
    qset=qset(db.sm_order_head.cid==c_id)
    qset=qset((db.sm_order_head.order_date>=startDt)&(db.sm_order_head.order_date<=endDt))
    qset=qset(db.sm_order_head.visit_type=='Unscheduled')
    
    areaList=[]
    if (regionValue!='' or areaValue!='' or territoryValue!='' or marketValue!=''):
        levelQset=db()
        levelQset=levelQset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
        
        if regionValue!='':
            levelQset=levelQset(db.sm_level.level0==regionValue)
        if areaValue!='':
            levelQset=levelQset(db.sm_level.level1==areaValue)
        if territoryValue!='':
            levelQset=levelQset(db.sm_level.level2==territoryValue)
        if marketValue!='':
            levelQset=levelQset(db.sm_level.level3==marketValue)
        
        rows = levelQset.select(db.sm_level.level_id, orderby=db.sm_level.level_id)
        for row in rows:
            level_id = str(row.level_id)
            areaList.append(level_id)
    
    
    if len(areaList)>0:
        qset=qset(db.sm_order_head.area_id.belongs(areaList))       
    
    
    if repCM!='':
        qset=qset(db.sm_order_head.rep_id==repCM)
    
    #---------
    unscheduleCount=qset.count()
    
    recordList=[]
    #recordList.append({'Type':'Scheduled Visit','Count':int(scheduleCount)})
    recordList.append({'Type':'Unscheduled Visit','Count':int(unscheduleCount)})
    #recordList.append({'Type':'Scheduled Visit Due','Count':int(scheduledVisitPendingCount)})
    
    return dict(recordList=recordList,unscheduleCount=unscheduleCount,fromDate=fromDate,toDate=toDate,regionValue=regionValue,regionValueShow=regionValueShow,areaValue=areaValue,territoryValue=territoryValue,areaValueShow=areaValueShow,territoryValueShow=territoryValueShow,marketValue=marketValue,marketValueShow=marketValueShow,repCM=repCM,page=page,items_per_page=items_per_page)

def visit_list_summary():
    c_id=session.cid
    response.title='Visit Summary'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    areaValue=str(request.vars.areaValue).strip()
    territoryValue=str(request.vars.territoryValue).strip()
    marketValue=str(request.vars.marketValue).strip()    
    repCM=str(request.vars.repCM).strip()
    
    if regionValue=='None':
        regionValue=''
    if areaValue=='None':
        areaValue=''
    if territoryValue=='None':
        territoryValue=''
    if marketValue=='None':
        marketValue=''
    if repCM=='None':
        repCM=''
    
    regionValueShow=regionValue    
    areaValueShow=areaValue    
    territoryValueShow=territoryValue    
    marketValueShow=marketValue
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #----------paging
    
    #----------end paging
    market_List=[]
    if (regionValue!='' or areaValue!='' or territoryValue!='' or marketValue!=''):
        levelQset=db()
        levelQset=levelQset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
        
        if regionValue!='':
            levelQset=levelQset(db.sm_level.level0==regionValue)
        if areaValue!='':
            levelQset=levelQset(db.sm_level.level1==areaValue)
        if territoryValue!='':
            levelQset=levelQset(db.sm_level.level2==territoryValue)
        if marketValue!='':
            levelQset=levelQset(db.sm_level.level3==marketValue)
        
        rows = levelQset.select(db.sm_level.level_id, orderby=db.sm_level.level_id)
        for row in rows:
            level_id = str(row.level_id)
            market_List.append(level_id)
    
    
    qset=db()
    qset=qset(db.sm_order_head.cid==c_id)
    qset=qset((db.sm_order_head.order_date>=startDt)&(db.sm_order_head.order_date<=endDt))
    qset=qset(db.sm_order_head.status=='Submitted')
    if len(market_List)>0:
        qset=qset(db.sm_order_head.area_id.belongs(market_List))
    if repCM!='':
        qset=qset(db.sm_order_head.rep_id==repCM)
    
    records=qset.select(db.sm_order_head.rep_id,db.sm_order_head.rep_name,db.sm_order_head.id.count(),orderby=db.sm_order_head.rep_name,groupby=db.sm_order_head.rep_id)
    
    qset=qset(db.sm_order.cid==c_id)
    qset=qset((db.sm_order.order_date>=startDt)&(db.sm_order.order_date<=endDt))    
    qset=qset((db.sm_order_head.depot_id==db.sm_order.depot_id)&(db.sm_order_head.sl==db.sm_order.sl))
    
    visitSummaryList=[]
    for rec in records:
        repName=rec.sm_order_head.rep_name
        repID=rec.sm_order_head.rep_id
        visitCount=rec[db.sm_order_head.id.count()]
        
        #-----------
        qsetF=qset(db.sm_order.rep_id==repID)        
        ordRecords=qsetF.select(db.sm_order.vsl,groupby=db.sm_order.vsl)
        ordCount=len(ordRecords)
        
        #-----------
        qsetAmt=qset(db.sm_order.rep_id==repID)        
        ordAmtRecords=qsetAmt.select(db.sm_order.quantity,db.sm_order.price)
        repTotal=0
            
        for ordAmt in ordAmtRecords:
            quantity=int(ordAmt.quantity)
            price=round(ordAmt.price,2)
            
            itemTotal=round(quantity*price,2)
            
            repTotal+=itemTotal
            
        dictData={'RepName':repName,'RepID':repID,'VisitCount':visitCount,'OrderCount':ordCount,'OrderAmount':repTotal}
        visitSummaryList.append(dictData)
        
        
    #-------------------------
    return dict(records=records,visitSummaryList=visitSummaryList,fromDate=fromDate,toDate=toDate,regionValue=regionValue,regionValueShow=regionValueShow,areaValue=areaValue,territoryValue=territoryValue,areaValueShow=areaValueShow,territoryValueShow=territoryValueShow,marketValue=marketValue,marketValueShow=marketValueShow,repCM=repCM)
def visit_list_summary_download():
    c_id=session.cid
    response.title='Visit Summary Download'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    areaValue=str(request.vars.areaValue).strip()
    territoryValue=str(request.vars.territoryValue).strip()
    marketValue=str(request.vars.marketValue).strip()    
    repCM=str(request.vars.repCM).strip()
    
    if regionValue=='None':
        regionValue=''
    if areaValue=='None':
        areaValue=''
    if territoryValue=='None':
        territoryValue=''
    if marketValue=='None':
        marketValue=''
    if repCM=='None':
        repCM=''
    
    regionValueShow=regionValue    
    areaValueShow=areaValue    
    territoryValueShow=territoryValue    
    marketValueShow=marketValue
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #----------paging
    
    #----------end paging
    market_List=[]
    if (regionValue!='' or areaValue!='' or territoryValue!='' or marketValue!=''):
        levelQset=db()
        levelQset=levelQset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
        
        if regionValue!='':
            levelQset=levelQset(db.sm_level.level0==regionValue)
        if areaValue!='':
            levelQset=levelQset(db.sm_level.level1==areaValue)
        if territoryValue!='':
            levelQset=levelQset(db.sm_level.level2==territoryValue)
        if marketValue!='':
            levelQset=levelQset(db.sm_level.level3==marketValue)
        
        rows = levelQset.select(db.sm_level.level_id, orderby=db.sm_level.level_id)
        for row in rows:
            level_id = str(row.level_id)
            market_List.append(level_id)
    
    
    qset=db()
    qset=qset(db.sm_order_head.cid==c_id)
    qset=qset((db.sm_order_head.order_date>=startDt)&(db.sm_order_head.order_date<=endDt))
    qset=qset(db.sm_order_head.status=='Submitted')
    if len(market_List)>0:
        qset=qset(db.sm_order_head.area_id.belongs(market_List))
    if repCM!='':
        qset=qset(db.sm_order_head.rep_id==repCM)
    
    records=qset.select(db.sm_order_head.rep_id,db.sm_order_head.rep_name,db.sm_order_head.id.count(),orderby=db.sm_order_head.rep_name,groupby=db.sm_order_head.rep_id)
    
    qset=qset(db.sm_order.cid==c_id)
    qset=qset((db.sm_order.order_date>=startDt)&(db.sm_order.order_date<=endDt))    
    qset=qset((db.sm_order_head.depot_id==db.sm_order.depot_id)&(db.sm_order_head.sl==db.sm_order.sl))
    
    visitSummaryList=[]
    for rec in records:
        repName=rec.sm_order_head.rep_name
        repID=rec.sm_order_head.rep_id
        visitCount=rec[db.sm_order_head.id.count()]
        
        #-----------
        qsetF=qset(db.sm_order.rep_id==repID)        
        ordRecords=qsetF.select(db.sm_order.vsl,groupby=db.sm_order.vsl)
        ordCount=len(ordRecords)
        
        #-----------
        qsetAmt=qset(db.sm_order.rep_id==repID)        
        ordAmtRecords=qsetAmt.select(db.sm_order.quantity,db.sm_order.price)
        
        repTotal=0
        
        for ordAmt in ordAmtRecords:
            quantity=int(ordAmt.quantity)
            price=round(ordAmt.price,2)
            
            itemTotal=round(quantity*price,2)
            
            repTotal+=itemTotal
            
        dictData={'RepName':repName,'RepID':repID,'VisitCount':visitCount,'OrderCount':ordCount,'OrderAmount':repTotal}
        visitSummaryList.append(dictData)
    
    #======    
    myString='Date From,'+fromDate+'\n'
    myString+='Date To,'+toDate+'\n'
    myString+=session.level0Name+','+regionValueShow.replace(',', ';')+'\n'
    myString+=session.level1Name+','+areaValueShow.replace(',', ';')+'\n'
    myString+='Visit By,'+repCM+'\n\n'
    
    
    myString+='Rep/SupervisorName,SPO/SupervisorID,Visit Count,Order Count,Order Amount\n'
    grandTotal=0
    for i in range(len(visitSummaryList)):
        dictData=visitSummaryList[i]
        
        RepName=str(dictData['RepName']).replace(',', ' ')
        RepID=str(dictData['RepID'])
        VisitCount=str(dictData['VisitCount'])
        OrderCount=str(dictData['OrderCount'])
        OrderAmount=dictData['OrderAmount']
                
        grandTotal+=OrderAmount
        
        myString+=RepName+','+RepID+','+VisitCount+','+OrderCount+','+str(OrderAmount)+'\n'
    
    myString+='Total,,,,'+str(grandTotal)+'\n'
    
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_visit_list_summary.csv'   
    return str(myString)

def schedule_and_completed_visit():
    c_id=session.cid
    
    response.title='Schedule And Completed Visit'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    areaValue=str(request.vars.areaValue).strip()
    territoryValue=str(request.vars.territoryValue).strip()
    marketValue=str(request.vars.marketValue).strip()    
    repCM=str(request.vars.repCM).strip()
    
    if regionValue=='None':
        regionValue=''
    if areaValue=='None':
        areaValue=''
    if territoryValue=='None':
        territoryValue=''
    if marketValue=='None':
        marketValue=''
    if repCM=='None':
        repCM=''
    
    regionValueShow=regionValue    
    areaValueShow=areaValue    
    territoryValueShow=territoryValue    
    marketValueShow=marketValue
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_visit_plan.cid==c_id)
    qset=qset((db.sm_visit_plan.schedule_date>=startDt)&(db.sm_visit_plan.schedule_date<=endDt))
    qset=qset((db.sm_visit_plan.status=='Approved')|(db.sm_visit_plan.status=='Visited'))
    
    if regionValue!='':
        qset=qset(db.sm_visit_plan.level0_id==regionValue)
    if areaValue!='':
        qset=qset(db.sm_visit_plan.level1_id==areaValue)
    if territoryValue!='':
        qset=qset(db.sm_visit_plan.level2_id==territoryValue)
    if marketValue!='':
        qset=qset(db.sm_visit_plan.route_id==marketValue)
    
    
    recordList=[]
    records=qset.select(db.sm_visit_plan.level0_id,db.sm_visit_plan.level0_name,db.sm_visit_plan.id.count(),db.sm_visit_plan.visited_flag.sum(),orderby=db.sm_visit_plan.level0_id,groupby=db.sm_visit_plan.level0_id,limitby=limitby)
    for rec in records:
        level0_id=str(rec.sm_visit_plan.level0_id)
        level0_name=str(rec.sm_visit_plan.level0_name)
        visitScheduled=int(rec[db.sm_visit_plan.id.count()])
        visited=int(rec[db.sm_visit_plan.visited_flag.sum()])
        
        regionNameId=level0_name+'-'+level0_id
        
        recordList.append({'Region':regionNameId,'VisitScheduled':visitScheduled,'VisitMade':visited})
    
    return dict(recordList=recordList,records=records,fromDate=fromDate,toDate=toDate,regionValue=regionValue,regionValueShow=regionValueShow,areaValue=areaValue,territoryValue=territoryValue,areaValueShow=areaValueShow,territoryValueShow=territoryValueShow,marketValue=marketValue,marketValueShow=marketValueShow,repCM=repCM,page=page,items_per_page=items_per_page)

def clientUpdatedList():
    c_id=session.cid
    
    response.title='Profile Updated List'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    areaValue=str(request.vars.areaValue).strip()
    territoryValue=str(request.vars.territoryValue).strip()
    marketValue=str(request.vars.marketValue).strip()    
    repCM=str(request.vars.repCM).strip()
    
    if regionValue=='None':
        regionValue=''
    if areaValue=='None':
        areaValue=''
    if territoryValue=='None':
        territoryValue=''
    if marketValue=='None':
        marketValue=''
    if repCM=='None':
        repCM=''
    
    regionValueShow=regionValue    
    areaValueShow=areaValue    
    territoryValueShow=territoryValue    
    marketValueShow=marketValue
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    nextDate=endDt+datetime.timedelta(days=1)
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    qset=db()
    qset=qset(db.sm_client.cid==c_id)
    qset=qset((db.sm_client.updated_on >= startDt)&(db.sm_client.updated_on < nextDate))
    qset=qset(db.sm_client.photo_str=='abc')
    
    market_List=[]
    if (regionValue!='' or areaValue!='' or territoryValue!='' or marketValue!=''):
        levelQset=db()
        levelQset=levelQset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
        
        if regionValue!='':
            levelQset=levelQset(db.sm_level.level0==regionValue)
        if areaValue!='':
            levelQset=levelQset(db.sm_level.level1==areaValue)
        if territoryValue!='':
            levelQset=levelQset(db.sm_level.level2==territoryValue)
        if marketValue!='':
            levelQset=levelQset(db.sm_level.level3==marketValue)
        
        rows = levelQset.select(db.sm_level.level_id, orderby=db.sm_level.level_id)
        for row in rows:
            level_id = str(row.level_id)
            market_List.append(level_id)
    
    if len(market_List)>0:
        qset=qset(db.sm_client.area_id.belongs(market_List))       
        
    
    if repCM!='':
        qset=qset(db.sm_client.updated_by==repCM)
    
    records=qset.select(db.sm_client.ALL,orderby=~db.sm_client.id,limitby=limitby)
    
    totalRecords=qset.count()
    
    return dict(records=records,totalRecords=totalRecords,fromDate=fromDate,toDate=toDate,regionValue=regionValue,regionValueShow=regionValueShow,areaValue=areaValue,territoryValue=territoryValue,areaValueShow=areaValueShow,territoryValueShow=territoryValueShow,marketValue=marketValue,marketValueShow=marketValueShow,repCM=repCM,page=page,items_per_page=items_per_page)
def downloadClientUpdatedList():
    c_id=session.cid
    
    response.title='Download Client Updated List'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    areaValue=str(request.vars.areaValue).strip()
    territoryValue=str(request.vars.territoryValue).strip()
    marketValue=str(request.vars.marketValue).strip()    
    repCM=str(request.vars.repCM).strip()
    
    if regionValue=='None':
        regionValue=''
    if areaValue=='None':
        areaValue=''
    if territoryValue=='None':
        territoryValue=''
    if marketValue=='None':
        marketValue=''
    if repCM=='None':
        repCM=''
    
    regionValueShow=regionValue    
    areaValueShow=areaValue    
    territoryValueShow=territoryValue    
    marketValueShow=marketValue
    
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    nextDate=endDt+datetime.timedelta(days=1)
    
    #--------------
    qset=db()
    qset=qset(db.sm_client.cid==c_id)
    qset=qset((db.sm_client.updated_on >= startDt)&(db.sm_client.updated_on < nextDate))
    
    market_List=[]
    if (regionValue!='' or areaValue!='' or territoryValue!='' or marketValue!=''):
        levelQset=db()
        levelQset=levelQset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
        
        if regionValue!='':
            levelQset=levelQset(db.sm_level.level0==regionValue)
        if areaValue!='':
            levelQset=levelQset(db.sm_level.level1==areaValue)
        if territoryValue!='':
            levelQset=levelQset(db.sm_level.level2==territoryValue)
        if marketValue!='':
            levelQset=levelQset(db.sm_level.level3==marketValue)
        
        rows = levelQset.select(db.sm_level.level_id, orderby=db.sm_level.level_id)
        for row in rows:
            level_id = str(row.level_id)
            market_List.append(level_id)
    
    if len(market_List)>0:
        qset=qset(db.sm_client.area_id.belongs(market_List))       
        
    
    if repCM!='':
        qset=qset(db.sm_client.updated_by==repCM)
    
    records=qset.select(db.sm_client.ALL,orderby=~db.sm_client.id)
    
    #REmove , from record.Cause , means new column in excel
    myString='Date From,'+fromDate+'\n'
    myString+='Date To,'+toDate+'\n'
    myString+='Region,'+regionValueShow.replace(',', ';')+'\n'
    myString+='Zone,'+zoneValueShow.replace(',', ';')+'\n'
    myString+='Visit By,'+repCM+'\n\n'
    
    myString+='Visit Date,VisitBy ID,VisitBy Name,VisitBy Mobile,Client ID,Client Name,Visit Type,Remarks,Region,Zone\n'
    for rec in records:
        rowid=rec.id
        submission_date=rec.submission_date
        visit_date=rec.visit_date
        user_type=rec.user_type
        rep_id=rec.rep_id
        rep_name=str(rec.rep_name).replace(',', ' ')
        rep_mobile=rec.rep_mobile
        client_id=rec.client_id
        client_name=str(rec.client_name).replace(',', ' ')
        
        route_id=str(rec.route_id).replace(',', ' ')
        unit_id=str(rec.unit_id).replace(',', ' ')
        visit_type=rec.visit_type
        remarks=str(rec.remarks).replace(',', ' ')
        myString+=str(visit_date)+','+str(rep_id)+','+str(rep_name)+','+str(rep_mobile)+','+str(client_id)+','+str(client_name)+','+str(visit_type)+','+str(remarks)+','+str(unit_id)+','+str(route_id)+'\n'
        
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_client_visit.csv'   
    return str(myString)
    
    
    return dict(records=records,monthlyVisitList=monthlyVisitList,year=year,monthNo=monthNo,monthName=monthName,regionValueShow=regionValueShow,zoneValueShow=zoneValueShow,page=page,items_per_page=items_per_page)
    


#======================
def monthlyVisitSummary():
    c_id=session.cid
    
    response.title='Monthly Visit Summary'
    
    year=str(request.vars.year).strip()
    monthNo=str(request.vars.monthNo).strip()
    monthName=str(request.vars.monthName).strip()
    firstDate=year+'-'+monthNo+'-01'
    
    regionValue=str(request.vars.regionValue).strip()
    
    regionValue=regionValue.replace('["','').replace("['","").replace("']","").replace('"]','').replace("',",",").replace(",'",",").replace(", '",",").replace('",',',').replace(', "',',')
    regionValueShow=regionValue.replace(",",", ")
    regionValueList=[]
    if regionValue=='None':
        regionValue=''
        regionValueShow=''
    regionValueList=regionValue.split(',')
    
    #--------------    
    qset=db()
    qset=qset(db.sm_level.cid==c_id)
    qset=qset(db.sm_level.is_leaf == '1')
    
    areaList=[]
    if regionValue!='':
        if len(regionValueList)>0:
             qset=qset(db.sm_level.level0.belongs(regionValueList))
            
    levelRows = qset.select(db.sm_level.level_id, orderby=db.sm_level.level_id)
    
    for levelRow in levelRows:
        level_id = str(levelRow.level_id).strip()
        areaList.append(level_id)
    
    
    #---------
    scheduleCount=db((db.sm_order_head.cid==c_id)&(db.sm_order_head.ym_date==firstDate)&(db.sm_order_head.visit_type=='Scheduled')&(db.sm_order_head.area_id.belongs(areaList))).count()
    unscheduleCount=db((db.sm_order_head.cid==c_id)&(db.sm_order_head.ym_date==firstDate)&(db.sm_order_head.visit_type=='Unscheduled')&(db.sm_order_head.area_id.belongs(areaList))).count()
    scheduledVisitPendingCount=db((db.sm_visit_plan.cid==c_id)&(db.sm_visit_plan.first_date==firstDate)&(db.sm_visit_plan.status=='Approved')&(db.sm_visit_plan.route_id.belongs(areaList))).count()
    
    recordList=[]
    #recordList.append({'Type':'Scheduled Visit','Count':int(scheduleCount)})
    recordList.append({'Type':'Unscheduled Visit','Count':int(unscheduleCount)})
    #recordList.append({'Type':'Scheduled Visit Due','Count':int(scheduledVisitPendingCount)})
    
    return dict(scheduleCount=scheduleCount,unscheduleCount=unscheduleCount,scheduledVisitPendingCount=scheduledVisitPendingCount,recordList=recordList,regionValue=regionValue,regionValueShow=regionValueShow,year=year,monthName=monthName)

def target_vs_achievement_region_wise():
    c_id=session.cid
    
    response.title='Target VS Achievement -RegionWise'
    
    year=str(request.vars.year).strip()
    monthNo=str(request.vars.monthNo).strip()
    monthName=str(request.vars.monthName).strip()
    firstDate=year+'-'+monthNo+'-01'
    
    regionValue=str(request.vars.regionValue).strip()    
    regionValue=regionValue.replace('["','').replace("['","").replace("']","").replace('"]','').replace("',",",").replace(",'",",").replace(", '",",").replace('",',',').replace(', "',',')
    regionValueShow=regionValue.replace(",",", ")
    regionValueList=[]
    if regionValue=='None':
        regionValue=''
        regionValueShow=''
    regionValueList=regionValue.split(',')
    
    #--------------
    
    qset=db()
    qset=qset(db.target_vs_achievement.cid == c_id)
    qset=qset(db.target_vs_achievement.first_date == firstDate)
    
    if regionValue!='':
        qset=qset(db.target_vs_achievement.region_id.belongs(regionValueList))
    
    #------------
    regionRecordShowList=[]
    regionRecordList=[]
    regionWiseTARows = qset.select(db.target_vs_achievement.region_id, db.target_vs_achievement.target_qty.sum(), db.target_vs_achievement.achievement_qty.sum(), orderby=db.target_vs_achievement.region_id, groupby=db.target_vs_achievement.region_id)
    for regRow in regionWiseTARows:
        region_id = regRow.target_vs_achievement.region_id
        target_qty = regRow[db.target_vs_achievement.target_qty.sum()]
        achievement_qty = regRow[db.target_vs_achievement.achievement_qty.sum()]
        
        region_name = ''
        levelRow = db((db.sm_level.cid == c_id) & (db.sm_level.level_id == region_id) & (db.sm_level.is_leaf == '0')).select(db.sm_level.level_name, limitby=(0, 1))
        if levelRow:
            region_name = levelRow[0].level_name
            
        rsm_name = ''
        supRow = db((db.sm_rep.cid == c_id) & (db.sm_rep.level_id == region_id)).select(db.sm_rep.name, limitby=(0, 1))
        if supRow:
            rsm_name = supRow[0].name

        regionRecordShowList.append({'RegionId':region_id,'RegionName':region_name, 'Supervisor':rsm_name, 'Target':target_qty, 'Achievement':achievement_qty})
        regionRecordList.append({'Region':region_name, 'Target':target_qty, 'Achievement':achievement_qty})
    
    
    return dict(regionRecordList=regionRecordList,regionRecordShowList=regionRecordShowList,regionValue=regionValue,regionValueShow=regionValueShow,year=year,monthNo=monthNo,monthName=monthName)
def target_vs_achievement_area_wise():
    c_id=session.cid
    
    response.title='Target VS Achievement -AreaWise'
    
    year=str(request.vars.year).strip()
    monthNo=str(request.vars.monthNo).strip()
    monthName=str(request.vars.monthName).strip()
    firstDate=year+'-'+monthNo+'-01'
    
    regionId=str(request.vars.regionId).strip()
    regionName=str(request.vars.regionName).strip()
    
    #--------------
    
    qset=db()
    qset=qset(db.target_vs_achievement.cid == c_id)
    qset=qset(db.target_vs_achievement.first_date == firstDate)
    qset=qset(db.target_vs_achievement.region_id== regionId)
    
    #------------
    recordShowList=[]
    recordList=[]
    taRows = qset.select(db.target_vs_achievement.area_id, db.target_vs_achievement.target_qty.sum(), db.target_vs_achievement.achievement_qty.sum(), orderby=db.target_vs_achievement.area_id, groupby=db.target_vs_achievement.area_id)
    for taRow in taRows:
        area_id = taRow.target_vs_achievement.area_id
        target_qty = taRow[db.target_vs_achievement.target_qty.sum()]
        achievement_qty = taRow[db.target_vs_achievement.achievement_qty.sum()]
        
        area_name = ''
        levelRow = db((db.sm_level.cid == c_id) & (db.sm_level.level_id == area_id) & (db.sm_level.is_leaf == '0')).select(db.sm_level.level_name, limitby=(0, 1))
        if levelRow:
            area_name = levelRow[0].level_name
            
        sup_name = ''
        supRow = db((db.sm_rep.cid == c_id) & (db.sm_rep.level_id == area_id)).select(db.sm_rep.name, limitby=(0, 1))
        if supRow:
            sup_name = supRow[0].name

        recordShowList.append({'AreaId':area_id,'AreaName':area_name, 'Supervisor':sup_name, 'Target':target_qty, 'Achievement':achievement_qty})
        recordList.append({'Area':area_name, 'Target':target_qty, 'Achievement':achievement_qty})
        
    return dict(recordList=recordList,recordShowList=recordShowList,regionId=regionId,regionName=regionName,year=year,monthNo=monthNo,monthName=monthName)
def target_vs_achievement_territory_wise():
    c_id=session.cid
    
    response.title='Target VS Achievement -TerritoryWise'
    
    year=str(request.vars.year).strip()
    monthNo=str(request.vars.monthNo).strip()
    monthName=str(request.vars.monthName).strip()
    firstDate=year+'-'+monthNo+'-01'
    
    regionId=str(request.vars.regionId).strip()
    regionName=str(request.vars.regionName).strip()
    
    areaId=str(request.vars.areaId).strip()
    areaName=str(request.vars.areaName).strip()
    
    #--------------
    
    qset=db()
    qset=qset(db.target_vs_achievement.cid == c_id)
    qset=qset(db.target_vs_achievement.first_date == firstDate)
    qset=qset(db.target_vs_achievement.region_id== regionId)
    qset=qset(db.target_vs_achievement.area_id== areaId)
    
    #------------
    recordShowList=[]
    recordList=[]
    taRows = qset.select(db.target_vs_achievement.territory_id, db.target_vs_achievement.target_qty.sum(), db.target_vs_achievement.achievement_qty.sum(), orderby=db.target_vs_achievement.territory_id, groupby=db.target_vs_achievement.territory_id)
    for taRow in taRows:
        territory_id = taRow.target_vs_achievement.territory_id
        target_qty = taRow[db.target_vs_achievement.target_qty.sum()]
        achievement_qty = taRow[db.target_vs_achievement.achievement_qty.sum()]
        
        territory_name = ''
        levelRow = db((db.sm_level.cid == c_id) & (db.sm_level.level_id == territory_id) & (db.sm_level.is_leaf == '0')).select(db.sm_level.level_name, limitby=(0, 1))
        if levelRow:
            territory_name = levelRow[0].level_name
            
        sup_name = ''
        supRow = db((db.sm_rep.cid == c_id) & (db.sm_rep.level_id == territory_id)).select(db.sm_rep.name, limitby=(0, 1))
        if supRow:
            sup_name = supRow[0].name

        recordShowList.append({'TerritoryId':territory_id,'TerritoryName':territory_name, 'Supervisor':sup_name, 'Target':target_qty, 'Achievement':achievement_qty})
        recordList.append({'Territory':territory_name, 'Target':target_qty, 'Achievement':achievement_qty})
        
    return dict(recordList=recordList,recordShowList=recordShowList,regionId=regionId,regionName=regionName,areaId=areaId,areaName=areaName,year=year,monthNo=monthNo,monthName=monthName)
def target_vs_achievement_market_wise():
    c_id=session.cid
    
    response.title='Target VS Achievement -MarketWise'
    
    year=str(request.vars.year).strip()
    monthNo=str(request.vars.monthNo).strip()
    monthName=str(request.vars.monthName).strip()
    firstDate=year+'-'+monthNo+'-01'
    
    regionId=str(request.vars.regionId).strip()
    regionName=str(request.vars.regionName).strip()
    
    areaId=str(request.vars.areaId).strip()
    areaName=str(request.vars.areaName).strip()
    
    territoryId=str(request.vars.territoryId).strip()
    territoryName=str(request.vars.territoryName).strip()
    
    #--------------
    
    qset=db()
    qset=qset(db.target_vs_achievement.cid == c_id)
    qset=qset(db.target_vs_achievement.first_date == firstDate)
    qset=qset(db.target_vs_achievement.region_id== regionId)
    qset=qset(db.target_vs_achievement.area_id== areaId)
    qset=qset(db.target_vs_achievement.territory_id== territoryId)
    #------------
    recordShowList=[]
    recordList=[]
    taRows = qset.select(db.target_vs_achievement.market_id, db.target_vs_achievement.target_qty.sum(), db.target_vs_achievement.achievement_qty.sum(), orderby=db.target_vs_achievement.market_id, groupby=db.target_vs_achievement.market_id)
    for taRow in taRows:
        market_id = taRow.target_vs_achievement.market_id
        target_qty = taRow[db.target_vs_achievement.target_qty.sum()]
        achievement_qty = taRow[db.target_vs_achievement.achievement_qty.sum()]
        
        market_name = ''
        levelRow = db((db.sm_level.cid == c_id) & (db.sm_level.level_id == market_id) & (db.sm_level.is_leaf == '1')).select(db.sm_level.level_name, limitby=(0, 1))
        if levelRow:
            market_name = levelRow[0].level_name
            
        sup_name = ''
        supRows = db((db.sm_rep_area.cid == c_id) & (db.sm_rep_area.area_id == market_id)).select(db.sm_rep_area.rep_id,db.sm_rep_area.rep_name,orderby=db.sm_rep_area.rep_name)
        for supRow in supRows:
            rep_id = str(supRow.rep_id)
            rep_name = str(supRow.rep_name)
            if sup_name=='':
                sup_name=rep_id+'-'+rep_name
            else:
                sup_name+=','+rep_id+'-'+rep_name
                
            
        recordShowList.append({'MarketId':market_id,'MarketName':market_name, 'Supervisor':sup_name, 'Target':target_qty, 'Achievement':achievement_qty})
        recordList.append({'Market':market_name, 'Target':target_qty, 'Achievement':achievement_qty})
        
    return dict(recordList=recordList,recordShowList=recordShowList,regionId=regionId,regionName=regionName,areaId=areaId,areaName=areaName,territoryId=territoryId,territoryName=territoryName,year=year,monthNo=monthNo,monthName=monthName)
def target_vs_achievement_retailer_wise():
    c_id=session.cid
    
    response.title='Target VS Achievement -RetailerWise'
    
    year=str(request.vars.year).strip()
    monthNo=str(request.vars.monthNo).strip()
    monthName=str(request.vars.monthName).strip()
    firstDate=year+'-'+monthNo+'-01'
    
    regionId=str(request.vars.regionId).strip()
    regionName=str(request.vars.regionName).strip()
    
    areaId=str(request.vars.areaId).strip()
    areaName=str(request.vars.areaName).strip()
    
    territoryId=str(request.vars.territoryId).strip()
    territoryName=str(request.vars.territoryName).strip()
    
    marketId=str(request.vars.marketId).strip()
    marketName=str(request.vars.marketName).strip()
    
    #--------------    
    qset=db()
    qset=qset(db.target_vs_achievement.cid == c_id)
    qset=qset(db.target_vs_achievement.first_date == firstDate)
    qset=qset(db.target_vs_achievement.region_id== regionId)
    qset=qset(db.target_vs_achievement.area_id== areaId)
    qset=qset(db.target_vs_achievement.territory_id== territoryId)
    qset=qset(db.target_vs_achievement.market_id== marketId)
    
    #------------
    recordShowList=[]
    recordList=[]
    taRows = qset.select(db.target_vs_achievement.client_id,db.target_vs_achievement.client_name, db.target_vs_achievement.target_qty.sum(), db.target_vs_achievement.achievement_qty.sum(), orderby=db.target_vs_achievement.client_name, groupby=db.target_vs_achievement.client_id)
    for taRow in taRows:
        client_id = taRow.target_vs_achievement.client_id
        client_name = taRow.target_vs_achievement.client_name
        target_qty = taRow[db.target_vs_achievement.target_qty.sum()]
        achievement_qty = taRow[db.target_vs_achievement.achievement_qty.sum()]
        
        recordShowList.append({'ClientId':client_id,'ClientName':client_name, 'Target':target_qty, 'Achievement':achievement_qty})
        recordList.append({'Client':client_name, 'Target':target_qty, 'Achievement':achievement_qty})
        
    return dict(recordList=recordList,recordShowList=recordShowList,regionId=regionId,regionName=regionName,areaId=areaId,areaName=areaName,territoryId=territoryId,territoryName=territoryName,marketId=marketId,marketName=marketName,year=year,monthNo=monthNo,monthName=monthName)


def retailer_distribution_region():
    c_id=session.cid
    
    response.title='Retailer Distribution- '+session.level0Name+' wise'
    
    regionValue=str(request.vars.regionValue).strip()
    
    
    regionValue=regionValue.replace('["','').replace("['","").replace("']","").replace('"]','').replace("',",",").replace(",'",",").replace(", '",",").replace('",',',').replace(', "',',')
    regionValueShow=regionValue.replace(",",", ")
    regionValueList=[]
    if regionValue=='None':
        regionValue=''
        regionValueShow=''
    regionValueList=regionValue.split(',')
    
    #--------------
    
    qset=db()
    qset=qset(db.sm_client.cid==c_id)
    qset=qset(db.sm_client.status=='ACTIVE')
    qset=qset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
    
    if regionValue!='':
        qset=qset(db.sm_level.level0.belongs(regionValueList))
    
    #------------
    qset=qset(db.sm_client.area_id==db.sm_level.level_id)
    
    records = qset.select(db.sm_level.level0, db.sm_client.client_id.count(), orderby=db.sm_level.level0, groupby=db.sm_level.level0)
    
    regionRecordShowList=[]
    regionRecordList=[]
    for rec in records:
        region_id = rec.sm_level.level0
        number_ofRet = int(rec[db.sm_client.client_id.count()])
        
        region_name = ''
        levelRow = db((db.sm_level.cid == c_id) & (db.sm_level.level_id == region_id)).select(db.sm_level.level_name, limitby=(0, 1))
        if levelRow:
            region_name = levelRow[0].level_name
        
        
        regionRecordShowList.append({'RegionId':region_id,'RegionName':region_name, 'NumberOfRet':number_ofRet})
        regionRecordList.append({'Region':region_name, 'NumberOfRet':number_ofRet})
    
    
    return dict(regionRecordList=regionRecordList,regionRecordShowList=regionRecordShowList,regionValue=regionValue,regionValueShow=regionValueShow)
def retailer_distribution_area_wise():
    c_id=session.cid
    
    response.title='Retailer Distribution- '+session.level1Name+' Wise'
    
    regionId=str(request.vars.regionId).strip()
    regionName=str(request.vars.regionName).strip()
    
    #--------------
    
    qset=db()
    qset=qset(db.sm_client.cid==c_id)
    qset=qset(db.sm_client.status=='ACTIVE')
    qset=qset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
    qset=qset(db.sm_level.level0==regionId)    
    #------------
    qset=qset(db.sm_client.area_id==db.sm_level.level_id)
    
    records = qset.select(db.sm_level.level1, db.sm_client.client_id.count(), orderby=db.sm_level.level1, groupby=db.sm_level.level1)
    
    recordShowList=[]
    recordList=[]
    for rec in records:
        area_id = rec.sm_level.level1
        number_ofRet = int(rec[db.sm_client.client_id.count()])
        
        level_name = ''
        levelRow = db((db.sm_level.cid == c_id) & (db.sm_level.level_id == area_id)).select(db.sm_level.level_name, limitby=(0, 1))
        if levelRow:
            level_name = levelRow[0].level_name
        
        recordShowList.append({'AreaId':area_id,'AreaName':level_name, 'NumberOfRet':number_ofRet})
        recordList.append({'Area':level_name, 'NumberOfRet':number_ofRet})
        
    return dict(recordList=recordList,recordShowList=recordShowList,regionId=regionId,regionName=regionName)
def retailer_distribution_territory_wise():
    c_id=session.cid
    
    response.title='Retailer Distribution -'+session.level2Name+' Wise'
    
    regionId=str(request.vars.regionId).strip()
    regionName=str(request.vars.regionName).strip()
    
    areaId=str(request.vars.areaId).strip()
    areaName=str(request.vars.areaName).strip()
    
    #--------------
    
    qset=db()
    qset=qset(db.sm_client.cid==c_id)
    qset=qset(db.sm_client.status=='ACTIVE')
    qset=qset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
    qset=qset(db.sm_level.level0==regionId)
    qset=qset(db.sm_level.level1==areaId)
    
    #------------
    qset=qset(db.sm_client.area_id==db.sm_level.level_id)
    
    records = qset.select(db.sm_level.level2, db.sm_client.client_id.count(), orderby=db.sm_level.level2, groupby=db.sm_level.level2)
    
    recordShowList=[]
    recordList=[]
    for rec in records:
        territory_id = rec.sm_level.level2
        number_ofRet = int(rec[db.sm_client.client_id.count()])
        
        level_name = ''
        levelRow = db((db.sm_level.cid == c_id) & (db.sm_level.level_id == territory_id)).select(db.sm_level.level_name, limitby=(0, 1))
        if levelRow:
            level_name = levelRow[0].level_name
        
        recordShowList.append({'TerritoryId':territory_id,'TerritoryName':level_name, 'NumberOfRet':number_ofRet})
        recordList.append({'Territory':level_name, 'NumberOfRet':number_ofRet})
        
    return dict(recordList=recordList,recordShowList=recordShowList,regionId=regionId,regionName=regionName,areaId=areaId,areaName=areaName)
def retailer_distribution_market_wise():
    c_id=session.cid
    
    response.title='Retailer Distribution -'+session.level3Name+' Wise'
    
    regionId=str(request.vars.regionId).strip()
    regionName=str(request.vars.regionName).strip()
    
    areaId=str(request.vars.areaId).strip()
    areaName=str(request.vars.areaName).strip()
    
    territoryId=str(request.vars.territoryId).strip()
    territoryName=str(request.vars.territoryName).strip()
    
    #--------------
    
    qset=db()
    qset=qset(db.sm_client.cid==c_id)
    qset=qset(db.sm_client.status=='ACTIVE')
    qset=qset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
    qset=qset(db.sm_level.level0==regionId)
    qset=qset(db.sm_level.level1==areaId)
    qset=qset(db.sm_level.level2==territoryId)
    
    #------------
    qset=qset(db.sm_client.area_id==db.sm_level.level_id)
    
    records = qset.select(db.sm_level.level3,db.sm_level.level_name, db.sm_client.client_id.count(), orderby=db.sm_level.level3, groupby=db.sm_level.level3)
    
    recordShowList=[]
    recordList=[]
    for rec in records:
        market_id = rec.sm_level.level3
        level_name = rec.sm_level.level_name        
        number_ofRet = int(rec[db.sm_client.client_id.count()])
        
        recordShowList.append({'MarketId':market_id,'MarketName':level_name, 'NumberOfRet':number_ofRet})
        recordList.append({'Market':level_name, 'NumberOfRet':number_ofRet})
        
    return dict(recordList=recordList,recordShowList=recordShowList,regionId=regionId,regionName=regionName,areaId=areaId,areaName=areaName,territoryId=territoryId,territoryName=territoryName)

#def target_vs_achievement_retailer_wise():
#    c_id=session.cid
#    
#    response.title='Target VS Achievement -RetailerWise'
#    
#    year=str(request.vars.year).strip()
#    monthNo=str(request.vars.monthNo).strip()
#    monthName=str(request.vars.monthName).strip()
#    firstDate=year+'-'+monthNo+'-01'
#    
#    regionId=str(request.vars.regionId).strip()
#    regionName=str(request.vars.regionName).strip()
#    
#    areaId=str(request.vars.areaId).strip()
#    areaName=str(request.vars.areaName).strip()
#    
#    territoryId=str(request.vars.territoryId).strip()
#    territoryName=str(request.vars.territoryName).strip()
#    
#    marketId=str(request.vars.marketId).strip()
#    marketName=str(request.vars.marketName).strip()
#    
#    #--------------
#    
#    qset=db()
#    qset=qset(db.target_vs_achievement.cid == c_id)
#    qset=qset(db.target_vs_achievement.first_date == firstDate)
#    qset=qset(db.target_vs_achievement.region_id== regionId)
#    qset=qset(db.target_vs_achievement.area_id== areaId)
#    qset=qset(db.target_vs_achievement.territory_id== territoryId)
#    qset=qset(db.target_vs_achievement.market_id== marketId)
#    
#    #------------
#    recordShowList=[]
#    recordList=[]
#    taRows = qset.select(db.target_vs_achievement.client_id,db.target_vs_achievement.client_name, db.target_vs_achievement.target_qty.sum(), db.target_vs_achievement.achievement_qty.sum(), orderby=db.target_vs_achievement.client_name, groupby=db.target_vs_achievement.client_id)
#    for taRow in taRows:
#        client_id = taRow.target_vs_achievement.client_id
#        client_name = taRow.target_vs_achievement.client_name
#        target_qty = taRow[db.target_vs_achievement.target_qty.sum()]
#        achievement_qty = taRow[db.target_vs_achievement.achievement_qty.sum()]
#        
#        recordShowList.append({'ClientId':client_id,'ClientName':client_name, 'Target':target_qty, 'Achievement':achievement_qty})
#        recordList.append({'Client':client_name, 'Target':target_qty, 'Achievement':achievement_qty})
#        
#    return dict(recordList=recordList,recordShowList=recordShowList,regionId=regionId,regionName=regionName,areaId=areaId,areaName=areaName,territoryId=territoryId,territoryName=territoryName,marketId=marketId,marketName=marketName,year=year,monthNo=monthNo,monthName=monthName)


#def monthlyOrderSummary():
#    c_id=session.cid
#    
#    response.title='Monthly Order Summary'
#    
#    year=str(request.vars.year).strip()
#    monthNo=str(request.vars.monthNo).strip()
#    monthName=str(request.vars.monthName).strip()
#    firstDate=year+'-'+monthNo+'-01'
#    
#    regionValue=str(request.vars.regionValue).strip()
#    zoneValue=str(request.vars.zoneValue).strip()
#    
#    
#    regionValue=regionValue.replace('["','').replace("['","").replace("']","").replace('"]','').replace("',",",").replace(",'",",").replace(", '",",").replace('",',',').replace(', "',',')
#    regionValueShow=regionValue.replace(",",", ")
#    regionValueList=[]
#    if regionValue=='None':
#        regionValue=''
#        regionValueShow=''
#    regionValueList=regionValue.split(',')
#    
#    zoneValue=zoneValue.replace('["','').replace("['","").replace("']","").replace('"]','').replace("',",",").replace(",'",",").replace(", '",",").replace('",',',').replace(', "',',')
#    zoneValueShow=zoneValue.replace(",",", ")
#    zoneValueList=[]
#    if zoneValue=='None':
#        zoneValue=''
#        zoneValueShow=''
#    zoneValueList=zoneValue.split(',')
#    
#    
#    #--------------
#    
#    qset=db()
#    qset=qset(db.sm_level.cid==c_id)
#    qset=qset(db.sm_level.is_leaf == '1')
#    
#    areaList=[]
#    if regionValue!='':
#        if len(regionValueList)>0:
#             qset=qset(db.sm_level.level0.belongs(regionValueList))
#            
#    levelRows = qset.select(db.sm_level.level_id, orderby=db.sm_level.level_id)
#    
#    for levelRow in levelRows:
#        level_id = str(levelRow.level_id).strip()
#        areaList.append(level_id)
#    
#    
#    #---------
#    records=db((db.sm_order.cid==cid)&(db.sm_order.ym_date==firstDate)&(db.sm_order.area_id.belongs(areaList))).select(db.sm_order.item_id,db.sm_order.item_name,db.sm_order.quantity.sum(),orderby=db.sm_order.item_name,groupby=db.sm_order.item_id)
#    
#    
#    return dict(records=records,regionValue=regionValue,regionValueShow=regionValueShow,zoneValue=zoneValue,zoneValueShow=zoneValueShow,year=year,monthName=monthName)

def spo_distribution_region():
    c_id=session.cid
    
    response.title='Rep Distribution- '+session.level0Name+' wise'
    
    regionValue=str(request.vars.regionValue).strip()
    
    regionValue=regionValue.replace('["','').replace("['","").replace("']","").replace('"]','').replace("',",",").replace(",'",",").replace(", '",",").replace('",',',').replace(', "',',')
    regionValueShow=regionValue.replace(",",", ")
    regionValueList=[]
    if regionValue=='None':
        regionValue=''
        regionValueShow=''
    regionValueList=regionValue.split(',')
    
    #--------------
    qset1=db()
    qset1=qset1((db.sm_level.cid == c_id)&(db.sm_level.depth == 0))
    if regionValue!='':
        qset1=qset1(db.sm_level.level_id.belongs(regionValueList))
    
    levelRows=qset1.select(db.sm_level.level_id,db.sm_level.level_name, orderby=db.sm_level.level_id)
    
    regionRecordShowList=[]
    regionRecordList=[]
    for levelRow in levelRows:
        region_id = levelRow.level_id
        region_name = levelRow.level_name
        
        qset=db()
        qset=qset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
        qset=qset(db.sm_level.level0 == region_id)
        qset=qset(db.sm_rep_area.cid==c_id)
        qset=qset(db.sm_rep_area.area_id==db.sm_level.level_id)
        
        #------------
        records = qset.select(db.sm_rep_area.rep_id, groupby=db.sm_rep_area.rep_id)        
        number_ofSpo=len(records)
        
        regionRecordShowList.append({'RegionId':region_id,'RegionName':region_name, 'NumberOfSPO':number_ofSpo})
        regionRecordList.append({'Region':region_name, 'NumberOfSPO':number_ofSpo})
    
    
    return dict(regionRecordList=regionRecordList,regionRecordShowList=regionRecordShowList,regionValue=regionValue,regionValueShow=regionValueShow)

def spo_distribution_area():
    c_id=session.cid
    
    response.title='Rep Distribution- '+session.level1Name+' Wise'
    
    regionId=str(request.vars.regionId).strip()
    regionName=str(request.vars.regionName).strip()
    
    #--------------
    qset1=db()
    qset1=qset1((db.sm_level.cid == c_id)&(db.sm_level.depth == 1))
    qset1=qset1(db.sm_level.level0 == regionId)
    
    levelRows=qset1.select(db.sm_level.level_id,db.sm_level.level_name, orderby=db.sm_level.level_id)
    
    
    recordShowList=[]
    recordList=[]
    for levelRow in levelRows:
        area_id = levelRow.level_id
        level_name = levelRow.level_name
        
        #--------
        qset=db()
        qset=qset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
        qset=qset(db.sm_level.level0 == regionId)
        qset=qset(db.sm_level.level1 == area_id)
        qset=qset(db.sm_rep_area.cid==c_id)
        qset=qset(db.sm_rep_area.area_id==db.sm_level.level_id)
        
        #------------
        records = qset.select(db.sm_rep_area.rep_id, groupby=db.sm_rep_area.rep_id)        
        number_ofSpo=len(records)
        
        recordShowList.append({'AreaId':area_id,'AreaName':level_name, 'NumberOfSPO':number_ofSpo})
        recordList.append({'Area':level_name, 'NumberOfSPO':number_ofSpo})
    
    return dict(recordList=recordList,recordShowList=recordShowList,regionId=regionId,regionName=regionName)
def spo_distribution_territory():
    c_id=session.cid
    
    response.title='Rep Distribution -'+session.level2Name+' Wise'
    
    regionId=str(request.vars.regionId).strip()
    regionName=str(request.vars.regionName).strip()
    
    areaId=str(request.vars.areaId).strip()
    areaName=str(request.vars.areaName).strip()
    
    #--------------
    qset1=db()
    qset1=qset1((db.sm_level.cid == c_id)&(db.sm_level.depth == 2))
    qset1=qset1(db.sm_level.level0 == regionId)
    qset1=qset1(db.sm_level.level1 == areaId)
    
    levelRows=qset1.select(db.sm_level.level_id,db.sm_level.level_name, orderby=db.sm_level.level_id)
    
    recordShowList=[]
    recordList=[]
    
    for levelRow in levelRows:
        territory_id = levelRow.level_id
        level_name = levelRow.level_name
        
        #--------
        qset=db()
        qset=qset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
        qset=qset(db.sm_level.level0 == regionId)
        qset=qset(db.sm_level.level1 == areaId)
        qset=qset(db.sm_level.level2 == territory_id)
        qset=qset(db.sm_rep_area.cid==c_id)
        qset=qset(db.sm_rep_area.area_id==db.sm_level.level_id)
        
        #------------
        number_ofSpo=0
        records = qset.select(db.sm_level.level2,db.sm_rep_area.rep_id,groupby=db.sm_rep_area.rep_id)
        number_ofSpo=len(records)
        
        recordShowList.append({'TerritoryId':territory_id,'TerritoryName':level_name, 'NumberOfSPO':number_ofSpo})
    
    return dict(recordList=recordList,recordShowList=recordShowList,regionId=regionId,regionName=regionName,areaId=areaId,areaName=areaName)


#================================== summary

def sales_summary_itemwise():
    c_id=session.cid
    response.title='Sales Summary - Item wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    areaValue=str(request.vars.areaValue).strip()
    territoryValue=str(request.vars.territoryValue).strip()
    marketValue=str(request.vars.marketValue).strip()    
    repCM=str(request.vars.repCM).strip()
    
    if regionValue=='None':
        regionValue=''
    if areaValue=='None':
        areaValue=''
    if territoryValue=='None':
        territoryValue=''
    if marketValue=='None':
        marketValue=''
    if repCM=='None':
        repCM=''
    
    regionValueShow=regionValue    
    areaValueShow=areaValue    
    territoryValueShow=territoryValue    
    marketValueShow=marketValue
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #----------paging
    
    #----------end paging
    market_List=[]
    if (regionValue!='' or areaValue!='' or territoryValue!='' or marketValue!=''):
        levelQset=db()
        levelQset=levelQset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
        
        if regionValue!='':
            levelQset=levelQset(db.sm_level.level0==regionValue)
        if areaValue!='':
            levelQset=levelQset(db.sm_level.level1==areaValue)
        if territoryValue!='':
            levelQset=levelQset(db.sm_level.level2==territoryValue)
        if marketValue!='':
            levelQset=levelQset(db.sm_level.level3==marketValue)
        
        rows = levelQset.select(db.sm_level.level_id, orderby=db.sm_level.level_id)
        for row in rows:
            level_id = str(row.level_id)
            market_List.append(level_id)
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset((db.sm_invoice_head.delivery_date>=startDt)&(db.sm_invoice_head.delivery_date<=endDt))
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.note!='Returned')
    if len(market_List)>0:
        qset=qset(db.sm_invoice_head.area_id.belongs(market_List))
    if repCM!='':
        qset=qset(db.sm_invoice_head.rep_id==repCM)
    
    qset=qset(db.sm_invoice.cid==c_id)
    qset=qset((db.sm_invoice.delivery_date>=startDt)&(db.sm_invoice.delivery_date<=endDt))    
    qset=qset((db.sm_invoice_head.depot_id==db.sm_invoice.depot_id)&(db.sm_invoice_head.sl==db.sm_invoice.sl))
    
    records=qset.select(db.sm_invoice.category_id,db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.quantity.sum(),orderby=db.sm_invoice.category_id|db.sm_invoice.item_name,groupby=db.sm_invoice.category_id|db.sm_invoice.item_id)
    
    #-------------------------
    return dict(records=records,fromDate=fromDate,toDate=toDate,regionValue=regionValue,regionValueShow=regionValueShow,areaValue=areaValue,territoryValue=territoryValue,areaValueShow=areaValueShow,territoryValueShow=territoryValueShow,marketValue=marketValue,marketValueShow=marketValueShow,repCM=repCM)
def sales_summary_itemwise_download():
    c_id=session.cid
    response.title='Sales Summary - Item wise Download'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    areaValue=str(request.vars.areaValue).strip()
    territoryValue=str(request.vars.territoryValue).strip()
    marketValue=str(request.vars.marketValue).strip()    
    repCM=str(request.vars.repCM).strip()
    
    if regionValue=='None':
        regionValue=''
    if areaValue=='None':
        areaValue=''
    if territoryValue=='None':
        territoryValue=''
    if marketValue=='None':
        marketValue=''
    if repCM=='None':
        repCM=''
    
    regionValueShow=regionValue    
    areaValueShow=areaValue    
    territoryValueShow=territoryValue    
    marketValueShow=marketValue
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #----------
    market_List=[]
    if (regionValue!='' or areaValue!='' or territoryValue!='' or marketValue!=''):
        levelQset=db()
        levelQset=levelQset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
        
        if regionValue!='':
            levelQset=levelQset(db.sm_level.level0==regionValue)
        if areaValue!='':
            levelQset=levelQset(db.sm_level.level1==areaValue)
        if territoryValue!='':
            levelQset=levelQset(db.sm_level.level2==territoryValue)
        if marketValue!='':
            levelQset=levelQset(db.sm_level.level3==marketValue)
        
        rows = levelQset.select(db.sm_level.level_id, orderby=db.sm_level.level_id)
        for row in rows:
            level_id = str(row.level_id)
            market_List.append(level_id)
    
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset((db.sm_invoice_head.delivery_date>=startDt)&(db.sm_invoice_head.delivery_date<=endDt))
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.note!='Returned')
    if len(market_List)>0:
        qset=qset(db.sm_invoice_head.area_id.belongs(market_List))
    if repCM!='':
        qset=qset(db.sm_invoice_head.rep_id==repCM)
    
    qset=qset(db.sm_invoice.cid==c_id)
    qset=qset((db.sm_invoice.delivery_date>=startDt)&(db.sm_invoice.delivery_date<=endDt))    
    qset=qset((db.sm_invoice_head.depot_id==db.sm_invoice.depot_id)&(db.sm_invoice_head.sl==db.sm_invoice.sl))
    
    records=qset.select(db.sm_invoice.category_id,db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.quantity.sum(),orderby=db.sm_invoice.category_id|db.sm_invoice.item_name,groupby=db.sm_invoice.category_id|db.sm_invoice.item_id)
    
    #======    
    myString='Date From,'+fromDate+'\n'
    myString+='Date To,'+toDate+'\n'
    myString+=session.level0Name+','+regionValueShow.replace(',', ';')+'\n'
    myString+=session.level1Name+','+areaValueShow.replace(',', ';')+'\n'
    
    myString+='Visit By,'+repCM+'\n\n'
    
    myString+='Category,ItemName,ItemID,Qty\n'
    for rec in records:
        category_id=str(rec.sm_invoice.category_id)
        item_id=str(rec.sm_invoice.item_id)
        item_name=str(rec.sm_invoice.item_name).replace(',', ' ')
        quantity=str(rec[db.sm_invoice.quantity.sum()])
        
        myString+=category_id+','+item_name+','+item_id+','+quantity+'\n'
        
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_sales_summary_itemwise.csv'   
    return str(myString)
    
    
#================================== summary

def sales_summary_repwise():
    c_id=session.cid
    response.title='Sales Summary - Rep/Sup wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    areaValue=str(request.vars.areaValue).strip()
    territoryValue=str(request.vars.territoryValue).strip()
    marketValue=str(request.vars.marketValue).strip()    
    repCM=str(request.vars.repCM).strip()
    
    if regionValue=='None':
        regionValue=''
    if areaValue=='None':
        areaValue=''
    if territoryValue=='None':
        territoryValue=''
    if marketValue=='None':
        marketValue=''
    if repCM=='None':
        repCM=''
    
    regionValueShow=regionValue    
    areaValueShow=areaValue    
    territoryValueShow=territoryValue    
    marketValueShow=marketValue
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #----------paging
    
    #----------end paging
    market_List=[]
    if (regionValue!='' or areaValue!='' or territoryValue!='' or marketValue!=''):
        levelQset=db()
        levelQset=levelQset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
        
        if regionValue!='':
            levelQset=levelQset(db.sm_level.level0==regionValue)
        if areaValue!='':
            levelQset=levelQset(db.sm_level.level1==areaValue)
        if territoryValue!='':
            levelQset=levelQset(db.sm_level.level2==territoryValue)
        if marketValue!='':
            levelQset=levelQset(db.sm_level.level3==marketValue)
        
        rows = levelQset.select(db.sm_level.level_id, orderby=db.sm_level.level_id)
        for row in rows:
            level_id = str(row.level_id)
            market_List.append(level_id)
    
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset((db.sm_invoice_head.delivery_date>=startDt)&(db.sm_invoice_head.delivery_date<=endDt))
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.note!='Returned')
    if len(market_List)>0:
        qset=qset(db.sm_invoice_head.area_id.belongs(market_List))
    if repCM!='':
        qset=qset(db.sm_invoice_head.rep_id==repCM)
    
    qset=qset(db.sm_invoice.cid==c_id)
    qset=qset((db.sm_invoice.delivery_date>=startDt)&(db.sm_invoice.delivery_date<=endDt))    
    qset=qset((db.sm_invoice_head.depot_id==db.sm_invoice.depot_id)&(db.sm_invoice_head.sl==db.sm_invoice.sl))
    
    records=qset.select(db.sm_invoice.rep_id,db.sm_invoice.rep_name,db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.quantity.sum(),orderby=db.sm_invoice.rep_name|db.sm_invoice.item_name,groupby=db.sm_invoice.rep_id|db.sm_invoice.item_id)
    
    #-------------------------
    return dict(records=records,fromDate=fromDate,toDate=toDate,regionValue=regionValue,regionValueShow=regionValueShow,areaValue=areaValue,territoryValue=territoryValue,areaValueShow=areaValueShow,territoryValueShow=territoryValueShow,marketValue=marketValue,marketValueShow=marketValueShow,repCM=repCM)
def sales_summary_repwise_download():
    c_id=session.cid
    response.title='Sales Summary - Rep/Sup wise Download'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    areaValue=str(request.vars.areaValue).strip()
    territoryValue=str(request.vars.territoryValue).strip()
    marketValue=str(request.vars.marketValue).strip()    
    repCM=str(request.vars.repCM).strip()
    
    if regionValue=='None':
        regionValue=''
    if areaValue=='None':
        areaValue=''
    if territoryValue=='None':
        territoryValue=''
    if marketValue=='None':
        marketValue=''
    if repCM=='None':
        repCM=''
    
    regionValueShow=regionValue    
    areaValueShow=areaValue    
    territoryValueShow=territoryValue    
    marketValueShow=marketValue
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #----------
    market_List=[]
    if (regionValue!='' or areaValue!='' or territoryValue!='' or marketValue!=''):
        levelQset=db()
        levelQset=levelQset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
        
        if regionValue!='':
            levelQset=levelQset(db.sm_level.level0==regionValue)
        if areaValue!='':
            levelQset=levelQset(db.sm_level.level1==areaValue)
        if territoryValue!='':
            levelQset=levelQset(db.sm_level.level2==territoryValue)
        if marketValue!='':
            levelQset=levelQset(db.sm_level.level3==marketValue)
        
        rows = levelQset.select(db.sm_level.level_id, orderby=db.sm_level.level_id)
        for row in rows:
            level_id = str(row.level_id)
            market_List.append(level_id)
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset((db.sm_invoice_head.delivery_date>=startDt)&(db.sm_invoice_head.delivery_date<=endDt))
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.note!='Returned')
    if len(market_List)>0:
        qset=qset(db.sm_invoice_head.area_id.belongs(market_List))
    if repCM!='':
        qset=qset(db.sm_invoice_head.rep_id==repCM)
    
    qset=qset(db.sm_invoice.cid==c_id)
    qset=qset((db.sm_invoice.delivery_date>=startDt)&(db.sm_invoice.delivery_date<=endDt))    
    qset=qset((db.sm_invoice_head.depot_id==db.sm_invoice.depot_id)&(db.sm_invoice_head.sl==db.sm_invoice.sl))
    
    records=qset.select(db.sm_invoice.rep_id,db.sm_invoice.rep_name,db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.quantity.sum(),orderby=db.sm_invoice.rep_name|db.sm_invoice.item_name,groupby=db.sm_invoice.rep_id|db.sm_invoice.item_id)
    
    
    #======    
    myString='Date From,'+fromDate+'\n'
    myString+='Date To,'+toDate+'\n'
    myString+=session.level0Name+','+regionValueShow.replace(',', ';')+'\n'
    myString+=session.level1Name+','+areaValueShow.replace(',', ';')+'\n'
    myString+='Visit By,'+repCM+'\n\n'
    
    
    myString+='Rep/SupervisorName,SPO/SupervisorID,ItemName,ItemID,Qty\n'
    for rec in records:
        rep_id=str(rec.sm_invoice.rep_id)
        rep_name=str(rec.sm_invoice.rep_name).replace(',', ' ')
        item_id=str(rec.sm_invoice.item_id)
        item_name=str(rec.sm_invoice.item_name).replace(',', ' ')
        quantity=str(rec[db.sm_invoice.quantity.sum()])
        
        myString+=rep_name+','+rep_id+','+item_name+','+item_id+','+quantity+'\n'
        
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_sales_summary_rep_supwise.csv'   
    return str(myString)
    
    
#================================== summary

def sales_summary_depotwise():
    c_id=session.cid
    response.title='Sales Summary - Distributor wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    areaValue=str(request.vars.areaValue).strip()
    territoryValue=str(request.vars.territoryValue).strip()
    marketValue=str(request.vars.marketValue).strip()    
    repCM=str(request.vars.repCM).strip()
    
    if regionValue=='None':
        regionValue=''
    if areaValue=='None':
        areaValue=''
    if territoryValue=='None':
        territoryValue=''
    if marketValue=='None':
        marketValue=''
    if repCM=='None':
        repCM=''
    
    regionValueShow=regionValue    
    areaValueShow=areaValue    
    territoryValueShow=territoryValue    
    marketValueShow=marketValue
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #----------paging
    
    #----------end paging
    market_List=[]
    if (regionValue!='' or areaValue!='' or territoryValue!='' or marketValue!=''):
        levelQset=db()
        levelQset=levelQset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
        
        if regionValue!='':
            levelQset=levelQset(db.sm_level.level0==regionValue)
        if areaValue!='':
            levelQset=levelQset(db.sm_level.level1==areaValue)
        if territoryValue!='':
            levelQset=levelQset(db.sm_level.level2==territoryValue)
        if marketValue!='':
            levelQset=levelQset(db.sm_level.level3==marketValue)
        
        rows = levelQset.select(db.sm_level.level_id, orderby=db.sm_level.level_id)
        for row in rows:
            level_id = str(row.level_id)
            market_List.append(level_id)
    
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset((db.sm_invoice_head.delivery_date>=startDt)&(db.sm_invoice_head.delivery_date<=endDt))
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.note!='Returned')
    if len(market_List)>0:
        qset=qset(db.sm_invoice_head.area_id.belongs(market_List))
    if repCM!='':
        qset=qset(db.sm_invoice_head.rep_id==repCM)
    
    qset=qset(db.sm_invoice.cid==c_id)
    qset=qset((db.sm_invoice.delivery_date>=startDt)&(db.sm_invoice.delivery_date<=endDt))    
    qset=qset((db.sm_invoice_head.depot_id==db.sm_invoice.depot_id)&(db.sm_invoice_head.sl==db.sm_invoice.sl))
    
    records=qset.select(db.sm_invoice.depot_id,db.sm_invoice.depot_name,db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.quantity.sum(),orderby=db.sm_invoice.depot_name|db.sm_invoice.item_name,groupby=db.sm_invoice.depot_id|db.sm_invoice.item_id)
    
    #-------------------------
    return dict(records=records,fromDate=fromDate,toDate=toDate,regionValue=regionValue,regionValueShow=regionValueShow,areaValue=areaValue,territoryValue=territoryValue,areaValueShow=areaValueShow,territoryValueShow=territoryValueShow,marketValue=marketValue,marketValueShow=marketValueShow,repCM=repCM)
def sales_summary_depotwise_download():
    c_id=session.cid
    response.title='Sales Summary - Depot wise Download'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    areaValue=str(request.vars.areaValue).strip()
    territoryValue=str(request.vars.territoryValue).strip()
    marketValue=str(request.vars.marketValue).strip()    
    repCM=str(request.vars.repCM).strip()
    
    if regionValue=='None':
        regionValue=''
    if areaValue=='None':
        areaValue=''
    if territoryValue=='None':
        territoryValue=''
    if marketValue=='None':
        marketValue=''
    if repCM=='None':
        repCM=''
    
    regionValueShow=regionValue    
    areaValueShow=areaValue    
    territoryValueShow=territoryValue    
    marketValueShow=marketValue
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #----------
    market_List=[]
    if (regionValue!='' or areaValue!='' or territoryValue!='' or marketValue!=''):
        levelQset=db()
        levelQset=levelQset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
        
        if regionValue!='':
            levelQset=levelQset(db.sm_level.level0==regionValue)
        if areaValue!='':
            levelQset=levelQset(db.sm_level.level1==areaValue)
        if territoryValue!='':
            levelQset=levelQset(db.sm_level.level2==territoryValue)
        if marketValue!='':
            levelQset=levelQset(db.sm_level.level3==marketValue)
        
        rows = levelQset.select(db.sm_level.level_id, orderby=db.sm_level.level_id)
        for row in rows:
            level_id = str(row.level_id)
            market_List.append(level_id)
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset((db.sm_invoice_head.delivery_date>=startDt)&(db.sm_invoice_head.delivery_date<=endDt))
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.note!='Returned')
    if len(market_List)>0:
        qset=qset(db.sm_invoice_head.area_id.belongs(market_List))
    if repCM!='':
        qset=qset(db.sm_invoice_head.rep_id==repCM)
    
    qset=qset(db.sm_invoice.cid==c_id)
    qset=qset((db.sm_invoice.delivery_date>=startDt)&(db.sm_invoice.delivery_date<=endDt))    
    qset=qset((db.sm_invoice_head.depot_id==db.sm_invoice.depot_id)&(db.sm_invoice_head.sl==db.sm_invoice.sl))
    
    records=qset.select(db.sm_invoice.depot_id,db.sm_invoice.depot_name,db.sm_invoice.item_id,db.sm_invoice.item_name,db.sm_invoice.quantity.sum(),orderby=db.sm_invoice.depot_name|db.sm_invoice.item_name,groupby=db.sm_invoice.depot_id|db.sm_invoice.item_id)
    
    #======    
    myString='Date From,'+fromDate+'\n'
    myString+='Date To,'+toDate+'\n'
    myString+=session.level0Name+','+regionValueShow.replace(',', ';')+'\n'
    myString+=session.level1Name+','+areaValueShow.replace(',', ';')+'\n'
    myString+='Visit By,'+repCM+'\n\n'
    
    myString+='DepotName,DepotID,ItemName,ItemID,Qty\n'
    for rec in records:
        depot_id=str(rec.sm_invoice.depot_id)
        depot_name=str(rec.sm_invoice.depot_name).replace(',', ' ')
        item_id=str(rec.sm_invoice.item_id)
        item_name=str(rec.sm_invoice.item_name).replace(',', ' ')
        quantity=str(rec[db.sm_invoice.quantity.sum()])
        
        myString+=depot_name+','+depot_id+','+item_name+','+item_id+','+quantity+'\n'
        
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_sales_summary_distributor.csv'   
    return str(myString)
    
    
#================================== 
def sales_details_download():
    c_id=session.cid
    response.title='Sales Details - Download'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    areaValue=str(request.vars.areaValue).strip()
    territoryValue=str(request.vars.territoryValue).strip()
    marketValue=str(request.vars.marketValue).strip()    
    repCM=str(request.vars.repCM).strip()
    
    if regionValue=='None':
        regionValue=''
    if areaValue=='None':
        areaValue=''
    if territoryValue=='None':
        territoryValue=''
    if marketValue=='None':
        marketValue=''
    if repCM=='None':
        repCM=''
    
    regionValueShow=regionValue    
    areaValueShow=areaValue    
    territoryValueShow=territoryValue    
    marketValueShow=marketValue
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #----------paging
    
    #----------end paging
    market_List=[]
    if (regionValue!='' or areaValue!='' or territoryValue!='' or marketValue!=''):
        levelQset=db()
        levelQset=levelQset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
        
        if regionValue!='':
            levelQset=levelQset(db.sm_level.level0==regionValue)
        if areaValue!='':
            levelQset=levelQset(db.sm_level.level1==areaValue)
        if territoryValue!='':
            levelQset=levelQset(db.sm_level.level2==territoryValue)
        if marketValue!='':
            levelQset=levelQset(db.sm_level.level3==marketValue)
        
        rows = levelQset.select(db.sm_level.level_id, orderby=db.sm_level.level_id)
        for row in rows:
            level_id = str(row.level_id)
            market_List.append(level_id)
    
    
    qset=db()
    qset=qset(db.sm_invoice_head.cid==c_id)
    qset=qset((db.sm_invoice_head.delivery_date>=startDt)&(db.sm_invoice_head.delivery_date<=endDt))
    qset=qset(db.sm_invoice_head.status=='Invoiced')
    qset=qset(db.sm_invoice_head.note!='Returned')
    if len(market_List)>0:
        qset=qset(db.sm_invoice_head.area_id.belongs(market_List))
    if repCM!='':
        qset=qset(db.sm_invoice_head.rep_id==repCM)
    
    qset=qset(db.sm_invoice.cid==c_id)
    qset=qset((db.sm_invoice.delivery_date>=startDt)&(db.sm_invoice.delivery_date<=endDt))    
    qset=qset((db.sm_invoice_head.depot_id==db.sm_invoice.depot_id)&(db.sm_invoice_head.sl==db.sm_invoice.sl))
    
    records=qset.select(db.sm_invoice.ALL,orderby=db.sm_invoice.depot_id|db.sm_invoice.sl)
    
    
    #======    
    myString='Date From,'+fromDate+'\n'
    myString+='Date To,'+toDate+'\n'
    myString+='Zone,'+regionValueShow.replace(',', ';')+'\n'
    myString+='Region,'+areaValueShow.replace(',', ';')+'\n'
    myString+='Area,'+territoryValueShow.replace(',', ';')+'\n'
    myString+='Territory/Market,'+marketValueShow.replace(',', ';')+'\n'
    myString+='Visit By,'+repCM+'\n\n'
    
    
    myString+='DistributorID,DistributiorName,SL,DeliveryDate,Client/RetailerID,Client/RetailerName,SPO/SupID,SPO/SupName,Territory/MarketID,Territory/MarketName,ItemID,ItemName,Category,Qty,Price\n'
    for rec in records:
        depot_id=str(rec.depot_id)
        depot_name=str(rec.depot_name).replace(',', ' ')
        sl=str(rec.sl)
        delivery_date=str(rec.delivery_date)
        
        client_id=str(rec.client_id)
        client_name=str(rec.client_name).replace(',', ' ')   
           
        rep_id=str(rec.rep_id)
        rep_name=str(rec.rep_name).replace(',', ' ')
        
        area_id=str(rec.area_id)
        area_name=str(rec.area_name).replace(',', ' ')
        
        item_id=str(rec.item_id)
        item_name=str(rec.item_name).replace(',', ' ')
        category_id=str(rec.category_id)
        quantity=str(rec.quantity)
        price=str(rec.price)
                
        myString+=depot_id+','+depot_name+','+sl+','+delivery_date+','+client_id+','+client_name+','+rep_id+','+rep_name+','+area_id+','+area_name+','+item_id+','+item_name+','+category_id+','+quantity+','+price+'\n'
        
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_sales_details.csv'   
    return str(myString)

    
#====================
def order_details_itemwise():
    c_id=session.cid
    response.title='Order Details - Item wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    areaValue=str(request.vars.areaValue).strip()
    territoryValue=str(request.vars.territoryValue).strip()
    marketValue=str(request.vars.marketValue).strip()    
    repCM=str(request.vars.repCM).strip()
    
    if regionValue=='None':
        regionValue=''
    if areaValue=='None':
        areaValue=''
    if territoryValue=='None':
        territoryValue=''
    if marketValue=='None':
        marketValue=''
    if repCM=='None':
        repCM=''
        
    regionValueShow=regionValue    
    areaValueShow=areaValue    
    territoryValueShow=territoryValue    
    marketValueShow=marketValue
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #----------paging
    
    #----------end paging
    market_List=[]
    if (regionValue!='' or areaValue!='' or territoryValue!='' or marketValue!=''):
        levelQset=db()
        levelQset=levelQset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
        
        if regionValue!='':
            levelQset=levelQset(db.sm_level.level0==regionValue)
        if areaValue!='':
            levelQset=levelQset(db.sm_level.level1==areaValue)
        if territoryValue!='':
            levelQset=levelQset(db.sm_level.level2==territoryValue)
        if marketValue!='':
            levelQset=levelQset(db.sm_level.level3==marketValue)
        
        rows = levelQset.select(db.sm_level.level_id, orderby=db.sm_level.level_id)
        for row in rows:
            level_id = str(row.level_id)
            market_List.append(level_id)
    
    qset=db()
    qset=qset(db.sm_order_head.cid==c_id)
    qset=qset((db.sm_order_head.order_date>=startDt)&(db.sm_order_head.order_date<=endDt))
    qset=qset(db.sm_order_head.status=='Submitted')
    if len(market_List)>0:
        qset=qset(db.sm_order_head.area_id.belongs(market_List))
    if repCM!='':
        qset=qset(db.sm_order_head.rep_id==repCM)
    
    qset=qset(db.sm_order.cid==c_id)
    qset=qset((db.sm_order.order_date>=startDt)&(db.sm_order.order_date<=endDt))    
    qset=qset((db.sm_order_head.depot_id==db.sm_order.depot_id)&(db.sm_order_head.sl==db.sm_order.sl))
    
    records=qset.select(db.sm_order.category_id,db.sm_order.item_id,db.sm_order.item_name,db.sm_order.quantity.sum(),db.sm_order.price,orderby=db.sm_order.category_id|db.sm_order.item_name,groupby=db.sm_order.category_id|db.sm_order.item_id|db.sm_order.price)
    
    #-------------------------
    return dict(records=records,fromDate=fromDate,toDate=toDate,regionValue=regionValue,regionValueShow=regionValueShow,areaValue=areaValue,territoryValue=territoryValue,areaValueShow=areaValueShow,territoryValueShow=territoryValueShow,marketValue=marketValue,marketValueShow=marketValueShow,repCM=repCM)
def order_details_itemwise_download():
    c_id=session.cid
    response.title='Order Details - Item wise Download'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    areaValue=str(request.vars.areaValue).strip()
    territoryValue=str(request.vars.territoryValue).strip()
    marketValue=str(request.vars.marketValue).strip()    
    repCM=str(request.vars.repCM).strip()
    
    if regionValue=='None':
        regionValue=''
    if areaValue=='None':
        areaValue=''
    if territoryValue=='None':
        territoryValue=''
    if marketValue=='None':
        marketValue=''
    if repCM=='None':
        repCM=''
        
    regionValueShow=regionValue    
    areaValueShow=areaValue    
    territoryValueShow=territoryValue    
    marketValueShow=marketValue
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #----------
    market_List=[]
    if (regionValue!='' or areaValue!='' or territoryValue!='' or marketValue!=''):
        levelQset=db()
        levelQset=levelQset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
        
        if regionValue!='':
            levelQset=levelQset(db.sm_level.level0==regionValue)
        if areaValue!='':
            levelQset=levelQset(db.sm_level.level1==areaValue)
        if territoryValue!='':
            levelQset=levelQset(db.sm_level.level2==territoryValue)
        if marketValue!='':
            levelQset=levelQset(db.sm_level.level3==marketValue)
        
        rows = levelQset.select(db.sm_level.level_id, orderby=db.sm_level.level_id)
        for row in rows:
            level_id = str(row.level_id)
            market_List.append(level_id)
    
    
    qset=db()
    qset=qset(db.sm_order_head.cid==c_id)
    qset=qset((db.sm_order_head.order_date>=startDt)&(db.sm_order_head.order_date<=endDt))
    qset=qset(db.sm_order_head.status=='Submitted')
    if len(market_List)>0:
        qset=qset(db.sm_order_head.area_id.belongs(market_List))
    if repCM!='':
        qset=qset(db.sm_order_head.rep_id==repCM)
    
    qset=qset(db.sm_order.cid==c_id)
    qset=qset((db.sm_order.order_date>=startDt)&(db.sm_order.order_date<=endDt))    
    qset=qset((db.sm_order_head.depot_id==db.sm_order.depot_id)&(db.sm_order_head.sl==db.sm_order.sl))
    
    records=qset.select(db.sm_order.category_id,db.sm_order.item_id,db.sm_order.item_name,db.sm_order.quantity.sum(),db.sm_order.price,orderby=db.sm_order.category_id|db.sm_order.item_name,groupby=db.sm_order.category_id|db.sm_order.item_id|db.sm_order.price)
    
    #======    
    myString='Date From,'+fromDate+'\n'
    myString+='Date To,'+toDate+'\n'
    myString+=session.level0Name+','+regionValueShow.replace(',', ';')+'\n'
    myString+=session.level1Name+','+areaValueShow.replace(',', ';')+'\n'
    
    myString+='Visit By,'+repCM+'\n\n'
    
    myString+='Category,ItemName,ItemID,Qty,Rate,Item Total\n'
    grandTotal=0
    for rec in records:
        category_id=str(rec.sm_order.category_id)
        
        if category_id=='':
            continue
        
        item_id=str(rec.sm_order.item_id)
        item_name=str(rec.sm_order.item_name).replace(',', ' ')
        quantity=rec[db.sm_order.quantity.sum()]
        rate=round(rec.sm_order.price,2)
        
        itemTotal=round(int(quantity)* rate,2)
        
        grandTotal+=itemTotal
        
        myString+=category_id+','+item_name+','+item_id+','+str(quantity)+','+str(rate)+','+str(itemTotal)+'\n'
    
    myString+='Total,,,,,'+str(grandTotal)+'\n'
    
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_order_details_itemwise.csv'   
    return str(myString)
    
    
#================================== 

def order_details_repwise():
    c_id=session.cid
    response.title='Order Details - Rep/Sup wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    areaValue=str(request.vars.areaValue).strip()
    territoryValue=str(request.vars.territoryValue).strip()
    marketValue=str(request.vars.marketValue).strip()    
    repCM=str(request.vars.repCM).strip()
    
    if regionValue=='None':
        regionValue=''
    if areaValue=='None':
        areaValue=''
    if territoryValue=='None':
        territoryValue=''
    if marketValue=='None':
        marketValue=''
    if repCM=='None':
        repCM=''
    
    regionValueShow=regionValue    
    areaValueShow=areaValue    
    territoryValueShow=territoryValue    
    marketValueShow=marketValue
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #----------paging
    
    #----------end paging
    market_List=[]
    if (regionValue!='' or areaValue!='' or territoryValue!='' or marketValue!=''):
        levelQset=db()
        levelQset=levelQset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
        
        if regionValue!='' :
            levelQset=levelQset(db.sm_level.level0==regionValue)            
        if areaValue!='':
            levelQset=levelQset(db.sm_level.level1==areaValue)            
        if territoryValue!='':
            levelQset=levelQset(db.sm_level.level2==territoryValue)
            
        if marketValue!='':
            levelQset=levelQset(db.sm_level.level3==marketValue)
        
        rows = levelQset.select(db.sm_level.level_id, orderby=db.sm_level.level_id)
        for row in rows:
            level_id = str(row.level_id)
            market_List.append(level_id)
            
            
    qset=db()
    qset=qset(db.sm_order_head.cid==c_id)
    qset=qset((db.sm_order_head.order_date>=startDt)&(db.sm_order_head.order_date<=endDt))
    qset=qset(db.sm_order_head.status=='Submitted')
    if len(market_List)>0:
        qset=qset(db.sm_order_head.area_id.belongs(market_List))
    if repCM!='':
        qset=qset(db.sm_order_head.rep_id==repCM)
    
    qset=qset(db.sm_order.cid==c_id)
    qset=qset((db.sm_order.order_date>=startDt)&(db.sm_order.order_date<=endDt))    
    qset=qset((db.sm_order_head.depot_id==db.sm_order.depot_id)&(db.sm_order_head.sl==db.sm_order.sl))
    
    records=qset.select(db.sm_order.rep_id,db.sm_order.rep_name,db.sm_order.item_id,db.sm_order.item_name,db.sm_order.quantity.sum(),db.sm_order.price,orderby=db.sm_order.rep_name|db.sm_order.item_name,groupby=db.sm_order.rep_id|db.sm_order.item_id|db.sm_order.price)
    
    #-------------------------
    return dict(records=records,fromDate=fromDate,toDate=toDate,regionValue=regionValue,regionValueShow=regionValueShow,areaValue=areaValue,territoryValue=territoryValue,areaValueShow=areaValueShow,territoryValueShow=territoryValueShow,marketValue=marketValue,marketValueShow=marketValueShow,repCM=repCM)
def order_details_repwise_download():
    c_id=session.cid
    response.title='Order Details - Rep/Sup wise Download'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    areaValue=str(request.vars.areaValue).strip()
    territoryValue=str(request.vars.territoryValue).strip()
    marketValue=str(request.vars.marketValue).strip()    
    repCM=str(request.vars.repCM).strip()
    
    if regionValue=='None':
        regionValue=''
    if areaValue=='None':
        areaValue=''
    if territoryValue=='None':
        territoryValue=''
    if marketValue=='None':
        marketValue=''
    if repCM=='None':
        repCM=''
        
    regionValueShow=regionValue    
    areaValueShow=areaValue    
    territoryValueShow=territoryValue    
    marketValueShow=marketValue
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #----------
    market_List=[]
    if (regionValue!='' or areaValue!='' or territoryValue!='' or marketValue!=''):
        levelQset=db()
        levelQset=levelQset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
        
        if regionValue!='':
            levelQset=levelQset(db.sm_level.level0==regionValue)
        if areaValue!='':
            levelQset=levelQset(db.sm_level.level1==areaValue)
        if territoryValue!='':
            levelQset=levelQset(db.sm_level.level2==territoryValue)
        if marketValue!='':
            levelQset=levelQset(db.sm_level.level3==marketValue)
        
        rows = levelQset.select(db.sm_level.level_id, orderby=db.sm_level.level_id)
        for row in rows:
            level_id = str(row.level_id)
            market_List.append(level_id)
    
    qset=db()
    qset=qset(db.sm_order_head.cid==c_id)
    qset=qset((db.sm_order_head.order_date>=startDt)&(db.sm_order_head.order_date<=endDt))
    qset=qset(db.sm_order_head.status=='Submitted')
    if len(market_List)>0:
        qset=qset(db.sm_order_head.area_id.belongs(market_List))
    if repCM!='':
        qset=qset(db.sm_order_head.rep_id==repCM)
    
    qset=qset(db.sm_order.cid==c_id)
    qset=qset((db.sm_order.order_date>=startDt)&(db.sm_order.order_date<=endDt))    
    qset=qset((db.sm_order_head.depot_id==db.sm_order.depot_id)&(db.sm_order_head.sl==db.sm_order.sl))
    
    records=qset.select(db.sm_order.rep_id,db.sm_order.rep_name,db.sm_order.item_id,db.sm_order.item_name,db.sm_order.quantity.sum(),db.sm_order.price,orderby=db.sm_order.rep_name|db.sm_order.item_name,groupby=db.sm_order.rep_id|db.sm_order.item_id|db.sm_order.price)
    
    #======    
    myString='Date From,'+fromDate+'\n'
    myString+='Date To,'+toDate+'\n'
    myString+=session.level0Name+','+regionValueShow.replace(',', ';')+'\n'
    myString+=session.level1Name+','+areaValueShow.replace(',', ';')+'\n'
    myString+='Visit By,'+repCM+'\n\n'
    
    
    myString+='Rep/SupervisorName,SPO/SupervisorID,ItemName,ItemID,Qty,Rate,Item Total\n'
    grandTotal=0
    for rec in records:
        rep_id=str(rec.sm_order.rep_id)
        rep_name=str(rec.sm_order.rep_name).replace(',', ' ')
        item_id=str(rec.sm_order.item_id)
        item_name=str(rec.sm_order.item_name).replace(',', ' ')
        
        quantity=rec[db.sm_order.quantity.sum()]
        rate=round(rec.sm_order.price,2)
        
        itemTotal=round(int(quantity)* rate,2)
        
        grandTotal+=itemTotal
        
        myString+=rep_name+','+rep_id+','+item_name+','+item_id+','+str(quantity)+','+str(rate)+','+str(itemTotal)+'\n'
    
    myString+='Total,,,,,,'+str(grandTotal)+'\n'
    
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_order_details_rep_supwise.csv'   
    return str(myString)
    
    
#================================== summary

def order_details_depotwise():
    c_id=session.cid
    response.title='Order Details - Distributor wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    areaValue=str(request.vars.areaValue).strip()
    territoryValue=str(request.vars.territoryValue).strip()
    marketValue=str(request.vars.marketValue).strip()    
    repCM=str(request.vars.repCM).strip()
    
    if regionValue=='None':
        regionValue=''
    if areaValue=='None':
        areaValue=''
    if territoryValue=='None':
        territoryValue=''
    if marketValue=='None':
        marketValue=''
    if repCM=='None':
        repCM=''
        
    regionValueShow=regionValue    
    areaValueShow=areaValue    
    territoryValueShow=territoryValue    
    marketValueShow=marketValue
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #----------paging
    
    #----------end paging
    market_List=[]
    if (regionValue!='' or areaValue!='' or territoryValue!='' or marketValue!=''):
        levelQset=db()
        levelQset=levelQset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
        
        if regionValue!='':
            levelQset=levelQset(db.sm_level.level0==regionValue)
        if areaValue!='':
            levelQset=levelQset(db.sm_level.level1==areaValue)
        if territoryValue!='':
            levelQset=levelQset(db.sm_level.level2==territoryValue)
        if marketValue!='':
            levelQset=levelQset(db.sm_level.level3==marketValue)
        
        rows = levelQset.select(db.sm_level.level_id, orderby=db.sm_level.level_id)
        for row in rows:
            level_id = str(row.level_id)
            market_List.append(level_id)
    
    
    qset=db()
    qset=qset(db.sm_order_head.cid==c_id)
    qset=qset((db.sm_order_head.order_date>=startDt)&(db.sm_order_head.order_date<=endDt))
    qset=qset(db.sm_order_head.status=='Submitted')
    if len(market_List)>0:
        qset=qset(db.sm_order_head.area_id.belongs(market_List))
    if repCM!='':
        qset=qset(db.sm_order_head.rep_id==repCM)
    
    qset=qset(db.sm_order.cid==c_id)
    qset=qset((db.sm_order.order_date>=startDt)&(db.sm_order.order_date<=endDt))    
    qset=qset((db.sm_order_head.depot_id==db.sm_order.depot_id)&(db.sm_order_head.sl==db.sm_order.sl))
    
    records=qset.select(db.sm_order.depot_id,db.sm_order.depot_name,db.sm_order.item_id,db.sm_order.item_name,db.sm_order.quantity.sum(),db.sm_order.price,orderby=db.sm_order.depot_name|db.sm_order.item_name,groupby=db.sm_order.depot_id|db.sm_order.item_id|db.sm_order.price)
    
    #-------------------------
    return dict(records=records,fromDate=fromDate,toDate=toDate,regionValue=regionValue,regionValueShow=regionValueShow,areaValue=areaValue,territoryValue=territoryValue,areaValueShow=areaValueShow,territoryValueShow=territoryValueShow,marketValue=marketValue,marketValueShow=marketValueShow,repCM=repCM)

def order_details_depotwise_download():
    c_id=session.cid
    response.title='Order Details - Depot wise Download'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    areaValue=str(request.vars.areaValue).strip()
    territoryValue=str(request.vars.territoryValue).strip()
    marketValue=str(request.vars.marketValue).strip()    
    repCM=str(request.vars.repCM).strip()
    
    if regionValue=='None':
        regionValue=''
    if areaValue=='None':
        areaValue=''
    if territoryValue=='None':
        territoryValue=''
    if marketValue=='None':
        marketValue=''
    if repCM=='None':
        repCM=''
        
    regionValueShow=regionValue    
    areaValueShow=areaValue    
    territoryValueShow=territoryValue    
    marketValueShow=marketValue
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #----------
    market_List=[]
    if (regionValue!='' or areaValue!='' or territoryValue!='' or marketValue!=''):
        levelQset=db()
        levelQset=levelQset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
        
        if regionValue!='':
            levelQset=levelQset(db.sm_level.level0==regionValue)
        if areaValue!='':
            levelQset=levelQset(db.sm_level.level1==areaValue)
        if territoryValue!='':
            levelQset=levelQset(db.sm_level.level2==territoryValue)
        if marketValue!='':
            levelQset=levelQset(db.sm_level.level3==marketValue)
        
        rows = levelQset.select(db.sm_level.level_id, orderby=db.sm_level.level_id)
        for row in rows:
            level_id = str(row.level_id)
            market_List.append(level_id)
    
    
    qset=db()
    qset=qset(db.sm_order_head.cid==c_id)
    qset=qset((db.sm_order_head.order_date>=startDt)&(db.sm_order_head.order_date<=endDt))
    qset=qset(db.sm_order_head.status=='Submitted')
    if len(market_List)>0:
        qset=qset(db.sm_order_head.area_id.belongs(market_List))
    if repCM!='':
        qset=qset(db.sm_order_head.rep_id==repCM)
    
    qset=qset(db.sm_order.cid==c_id)
    qset=qset((db.sm_order.order_date>=startDt)&(db.sm_order.order_date<=endDt))    
    qset=qset((db.sm_order_head.depot_id==db.sm_order.depot_id)&(db.sm_order_head.sl==db.sm_order.sl))
    
    records=qset.select(db.sm_order.depot_id,db.sm_order.depot_name,db.sm_order.item_id,db.sm_order.item_name,db.sm_order.quantity.sum(),db.sm_order.price,orderby=db.sm_order.depot_name|db.sm_order.item_name,groupby=db.sm_order.depot_id|db.sm_order.item_id|db.sm_order.price)
    
    #======    
    myString='Date From,'+fromDate+'\n'
    myString+='Date To,'+toDate+'\n'
    myString+=session.level0Name+','+regionValueShow.replace(',', ';')+'\n'
    myString+=session.level1Name+','+areaValueShow.replace(',', ';')+'\n'
    myString+='Visit By,'+repCM+'\n\n'
    
    myString+='DepotName,DepotID,ItemName,ItemID,Qty,Rate,Item Total\n'
    grandTotal=0
    for rec in records:
        depot_id=str(rec.sm_order.depot_id)
        depot_name=str(rec.sm_order.depot_name).replace(',', ' ')
        item_id=str(rec.sm_order.item_id)
        item_name=str(rec.sm_order.item_name).replace(',', ' ')
                
        quantity=rec[db.sm_order.quantity.sum()]
        rate=round(rec.sm_order.price,2)
        
        itemTotal=round(int(quantity)* rate,2)
        
        grandTotal+=itemTotal
        
        myString+=depot_name+','+depot_id+','+item_name+','+item_id+','+str(quantity)+','+str(rate)+','+str(itemTotal)+'\n'
    
    myString+='Total,,,,,,'+str(grandTotal)+'\n'
    
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_order_details_distributor.csv'   
    return str(myString)
    
#================

def doctor_visit_summary_level0():
    c_id=session.cid
    
    response.title='Doctor Visit Summary- '+session.level0Name+' wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    
    if regionValue=='None':
        regionValue=''
    
    
    regionValueShow=regionValue    
    repCM=str(request.vars.repCM).strip()   
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------
    qset1=db()
    qset1=qset1((db.sm_level.cid == c_id)&(db.sm_level.depth == 0))
    if regionValue!='':
        qset1=qset1(db.sm_level.level_id==regionValue)
    
    levelRows=qset1.select(db.sm_level.level_id,db.sm_level.level_name, orderby=db.sm_level.level_id)
    
    regionRecordShowList=[]
    regionRecordList=[]
    for levelRow in levelRows:
        region_id = levelRow.level_id
        region_name = levelRow.level_name
        
        qset=db()
        qset=qset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
        qset=qset(db.sm_level.level0 == region_id)
        
        qset=qset(db.sm_doctor_visit.cid==c_id)
        qset=qset((db.sm_doctor_visit.visit_date>=startDt)&(db.sm_doctor_visit.visit_date<=endDt))
        qset=qset(db.sm_doctor_visit.route_id==db.sm_level.level_id)
        
        if repCM!='':
            qset=qset(db.sm_doctor_visit.rep_id==repCM)
            
        #------------
        scheduledCount=0
        visitCount=0
        vRecords = qset.select(db.sm_doctor_visit.id.count(), groupby=db.sm_doctor_visit.cid)        
        if vRecords:
            visitCount=vRecords[0][db.sm_doctor_visit.id.count()]
        
        regionRecordShowList.append({'Level0Id':region_id,'Level0Name':region_name, 'Scheduled':scheduledCount, 'Visited':visitCount})
        regionRecordList.append({'Level0':region_name, 'Scheduled':int(scheduledCount), 'Visited':int(visitCount)})
    
    return dict(regionRecordList=regionRecordList,regionRecordShowList=regionRecordShowList,regionValue=regionValue,regionValueShow=regionValueShow,fromDate=fromDate,toDate=toDate,repCM=repCM)


def doctor_visit_summary_level1():
    c_id=session.cid
    
    response.title='Doctor Visit Summary- '+session.level1Name+' Wise'
    
        
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    regionId=str(request.vars.regionId).strip()
    regionName=str(request.vars.regionName).strip()
    repCM=str(request.vars.repCM).strip()
    
    #--------------
    qset1=db()
    qset1=qset1((db.sm_level.cid == c_id)&(db.sm_level.depth == 1))
    qset1=qset1(db.sm_level.level0 == regionId)
    
    levelRows=qset1.select(db.sm_level.level_id,db.sm_level.level_name, orderby=db.sm_level.level_id)
    
    
    recordShowList=[]
    recordList=[]
    for levelRow in levelRows:
        area_id = levelRow.level_id
        level_name = levelRow.level_name
        
        #--------
                
        qset=db()
        qset=qset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
        qset=qset(db.sm_level.level0 == regionId)
        qset=qset(db.sm_level.level1 == area_id)
        
        qset=qset(db.sm_doctor_visit.cid==c_id)
        qset=qset((db.sm_doctor_visit.visit_date>=startDt)&(db.sm_doctor_visit.visit_date<=endDt))
        qset=qset(db.sm_doctor_visit.route_id==db.sm_level.level_id)
        if repCM!='':
            qset=qset(db.sm_doctor_visit.rep_id==repCM)
            
        #------------
        scheduledCount=0
        visitCount=0
        vRecords = qset.select(db.sm_doctor_visit.id.count(), groupby=db.sm_doctor_visit.cid)        
        if vRecords:
            visitCount=vRecords[0][db.sm_doctor_visit.id.count()]
        
        recordShowList.append({'Level1Id':area_id,'Level1Name':level_name, 'Scheduled':scheduledCount, 'Visited':visitCount})
        recordList.append({'Level1':level_name, 'Scheduled':int(scheduledCount), 'Visited':int(visitCount)})
        
    return dict(recordList=recordList,recordShowList=recordShowList,regionId=regionId,regionName=regionName,repCM=repCM,fromDate=fromDate,toDate=toDate)
def doctor_visit_summary_level2():
    c_id=session.cid
    
    response.title='Doctor Visit Summary- '+session.level2Name+' Wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
        
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    regionId=str(request.vars.regionId).strip()
    regionName=str(request.vars.regionName).strip()
    repCM=str(request.vars.repCM).strip()
    
    areaId=str(request.vars.areaId).strip()
    areaName=str(request.vars.areaName).strip()
    
    #--------------
    qset1=db()
    qset1=qset1((db.sm_level.cid == c_id)&(db.sm_level.depth == 2))
    qset1=qset1(db.sm_level.level0 == regionId)
    qset1=qset1(db.sm_level.level1 == areaId)
    
    levelRows=qset1.select(db.sm_level.level_id,db.sm_level.level_name, orderby=db.sm_level.level_id)
    
    recordShowList=[]
    recordList=[]
    for levelRow in levelRows:
        territory_id = levelRow.level_id
        level_name = levelRow.level_name
        
        #--------
        qset=db()
        qset=qset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
        qset=qset(db.sm_level.level0 == regionId)
        qset=qset(db.sm_level.level1 == areaId)
        qset=qset(db.sm_level.level2 == territory_id)
        
        qset=qset(db.sm_doctor_visit.cid==c_id)
        qset=qset((db.sm_doctor_visit.visit_date>=startDt)&(db.sm_doctor_visit.visit_date<=endDt))
        qset=qset(db.sm_doctor_visit.route_id==db.sm_level.level_id)
        if repCM!='':
            qset=qset(db.sm_doctor_visit.rep_id==repCM)
            
        #------------
        scheduledCount=0
        visitCount=0
        vRecords = qset.select(db.sm_doctor_visit.id.count(), groupby=db.sm_doctor_visit.cid)        
        if vRecords:
            visitCount=vRecords[0][db.sm_doctor_visit.id.count()]
        
        recordShowList.append({'Level2Id':territory_id,'Level2Name':level_name, 'Scheduled':scheduledCount, 'Visited':visitCount})
        recordList.append({'Level2':level_name, 'Scheduled':int(scheduledCount), 'Visited':int(visitCount)})
        
    return dict(recordList=recordList,recordShowList=recordShowList,regionId=regionId,regionName=regionName,areaId=areaId,areaName=areaName,repCM=repCM,fromDate=fromDate,toDate=toDate)

def doctor_survey_summary_mpo():
    c_id=session.cid
    
    response.title='Doctor Visit Count (Individual)'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    
    if regionValue=='None':
        regionValue=''
    
    tlValue=str(request.vars.areaValue).strip()
    regionValueShow=regionValue    
    repCM=str(request.vars.repCM).strip()   
#     return repCM
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
   
    #------------------

    presRecordShowList=[]    
    
    qset=db()    
    qset=qset(db.sm_doctor_visit.cid==c_id)
    qset=qset((db.sm_doctor_visit.visit_date>=startDt)&(db.sm_doctor_visit.visit_date<=endDt))
    qset=qset(db.sm_level.cid==c_id)
    qset=qset(db.sm_doctor_visit.route_id==db.sm_level.level_id)
    
    
    if (regionValueShow!='ALL') & (regionValueShow!=''):
        qset=qset(db.sm_level.level0==regionValueShow)
    if (tlValue!='ALL') & (tlValue!=''):
        qset=qset(db.sm_level.level1==tlValue)
        
    #------------    
    prescriptCount=0

    pRecords = qset.select(db.sm_doctor_visit.rep_id,db.sm_doctor_visit.rep_name,db.sm_doctor_visit.id.count(),db.sm_level.level_id,db.sm_level.level_name,db.sm_level.level0,db.sm_level.level0_name,db.sm_level.level1,db.sm_level.level1_name, groupby=db.sm_doctor_visit.rep_id|db.sm_doctor_visit.route_id,orderby=db.sm_doctor_visit.route_id|db.sm_doctor_visit.rep_id)
#     return pRecords
    myString='Doctor Visit Count (Individual)\n\n\n'
    myString+='Date From,'+fromDate+'\n'
    myString+='Date To,'+toDate+'\n'
    myString+='Region,'+regionValueShow+'\n'
    myString+='TL,'+tlValue+'\n\n'
    
    myString+='RegionID,RegionName,TLID,TLName,TerritoryID,TerritoryName,SubmittedbyID,SubmittedbyName,Qty\n'
    for pRow in pRecords:
        reg_id=pRow.sm_level.level0
        reg_name=pRow.sm_level.level0_name
        tl_id=pRow.sm_level.level1
        tl_name=pRow.sm_level.level1_name
        area_id=pRow.sm_level.level_id
        area_name=pRow.sm_level.level_name
        
        submit_by_id=pRow.sm_doctor_visit.rep_id
        submit_by_name=pRow.sm_doctor_visit.rep_name
        visitCount=pRow[db.sm_doctor_visit.id.count()]
    
        myString=myString+str(reg_id)+','+str(reg_name)+','+str(tl_id)+','+str(tl_name)+','+str(area_id)+','+str(area_name)+','+str(submit_by_id)+','+str(submit_by_name)+','+str(visitCount)+'\n'
#     myString+='\n\n,,,,,,,Total,'+str(total)+'\n'    
    #Save as csv
    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=DoctorVisitCountndividual.csv'   
    return str(myString)
    return dict(presRecordShowList=presRecordShowList,fromDate=fromDate,toDate=toDate,regionValueShow=regionValueShow,tlValue=tlValue,page=page,items_per_page=items_per_page)


#================ prescription  


def pres_survey_summary_mpo():
    c_id=session.cid
    
    response.title='Prescription Survey Summary- '+session.level0Name+' wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    
    if regionValue=='None':
        regionValue=''
    
    tlValue=str(request.vars.areaValue).strip()
    regionValueShow=regionValue    
    repCM=str(request.vars.repCM).strip()   
#     return repCM
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    
    #------------------

    presRecordShowList=[]    
    
    qset=db()    
    qset=qset(db.sm_prescription_head.cid==c_id)
    qset=qset((db.sm_prescription_head.submit_date>=startDt)&(db.sm_prescription_head.submit_date<=endDt))

    if regionValueShow!='':
        qset=qset(db.sm_prescription_head.reg_id==regionValueShow)
    if tlValue!='':
        qset=qset(db.sm_prescription_head.tl_id==tlValue)
        
    #------------    
    prescriptCount=0
    pRecords = qset.select(db.sm_prescription_head.ALL,db.sm_prescription_head.id.count(), groupby=db.sm_prescription_head.submit_by_id|db.sm_prescription_head.area_id|db.sm_prescription_head.tl_id |db.sm_prescription_head.reg_id,orderby=db.sm_prescription_head.reg_id|db.sm_prescription_head.tl_id |db.sm_prescription_head.area_id|db.sm_prescription_head.submit_by_id)
#     pRecords = qset.select(db.sm_prescription_head.ALL,db.sm_prescription_head.id.count(), groupby=db.sm_prescription_head.area_id|db.sm_prescription_head.tl_id |db.sm_prescription_head.reg_id,orderby=db.sm_prescription_head.reg_id|db.sm_prescription_head.tl_id |db.sm_prescription_head.area_id|db.sm_prescription_head.submit_by_id,limitby=limitby)        
#     return pRecords  
    for pRow in pRecords:
        reg_id=pRow.sm_prescription_head.reg_id
        reg_name=pRow.sm_prescription_head.reg_name
        tl_id=pRow.sm_prescription_head.tl_id
        tl_name=pRow.sm_prescription_head.tl_name
        area_id=pRow.sm_prescription_head.area_id
        area_name=pRow.sm_prescription_head.area_name
        submit_by_id=pRow.sm_prescription_head.submit_by_id
        submit_by_name=pRow.sm_prescription_head.submit_by_name
        prescriptCount=pRow[db.sm_prescription_head.id.count()]
#         return reg_id
        presRecordShowList.append({'reg_id':reg_id,'reg_name':reg_name,'tl_id':tl_id,'tl_name':tl_name,'area_id':area_id,'area_name':area_name,'SubmitedByID':submit_by_id,'SubmitedByName':submit_by_name, 'Prescription':prescriptCount})

    
    return dict(presRecordShowList=presRecordShowList,fromDate=fromDate,toDate=toDate,regionValueShow=regionValueShow,tlValue=tlValue,page=page,items_per_page=items_per_page)




def pres_survey_summary_tl():
    c_id=session.cid
    
    response.title='Prescription Survey Summary- '+session.level0Name+' wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    tlValue=str(request.vars.areaValue).strip()
    if regionValue=='None':
        regionValue=''
    
    
    regionValueShow=regionValue    
    repCM=str(request.vars.repCM).strip()   
#     return repCM
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    
    #------------------

    presRecordShowList=[]    
    
    qset=db()    
    qset=qset(db.sm_prescription_head.cid==c_id)
    qset=qset((db.sm_prescription_head.submit_date>=startDt)&(db.sm_prescription_head.submit_date<=endDt))

    if regionValueShow!='':
        qset=qset(db.sm_prescription_head.reg_id==regionValueShow)
    if tlValue!='':
        qset=qset(db.sm_prescription_head.tl_id==tlValue)
        
    #------------    
    prescriptCount=0
    pRecords = qset.select(db.sm_prescription_head.reg_id,db.sm_prescription_head.reg_name,db.sm_prescription_head.tl_id,db.sm_prescription_head.tl_name,db.sm_prescription_head.id.count(),orderby=db.sm_prescription_head.reg_id|db.sm_prescription_head.tl_id, groupby=db.sm_prescription_head.reg_id|db.sm_prescription_head.tl_id)        
#     return pRecords 
    for pRow in pRecords:
        reg_id=pRow.sm_prescription_head.reg_id
#         return reg_id
        reg_name=pRow.sm_prescription_head.reg_name
        tl_id=pRow.sm_prescription_head.tl_id
        tl_name=pRow.sm_prescription_head.tl_name
#         return pRow.sm_prescription_head.reg_id
        prescriptCount=pRow[db.sm_prescription_head.id.count()]
#         return tl_id
        presRecordShowList.append({'reg_id':reg_id,'reg_name':reg_name,'tl_id':tl_id,'tl_name':tl_name, 'Prescription':prescriptCount})

    
    return dict(presRecordShowList=presRecordShowList,fromDate=fromDate,toDate=toDate,regionValueShow=regionValueShow,tlValue=tlValue,page=page,items_per_page=items_per_page)


def pres_survey_summary_reg():
    c_id=session.cid
    
    response.title='Prescription Survey Summary- '+session.level0Name+' wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    
    if regionValue=='None':
        regionValue=''
    
    
    regionValueShow=regionValue    
    repCM=str(request.vars.repCM).strip()   
#     return repCM
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    
    #------------------

    presRecordShowList=[]    
    
    qset=db()    
    qset=qset(db.sm_prescription_head.cid==c_id)
    qset=qset((db.sm_prescription_head.submit_date>=startDt)&(db.sm_prescription_head.submit_date<=endDt))

    if regionValueShow!='':
        qset=qset(db.sm_prescription_head.reg_id==regionValueShow)
     
      
    #------------    
    prescriptCount=0
    pRecords = qset.select(db.sm_prescription_head.reg_id,db.sm_prescription_head.reg_name,db.sm_prescription_head.id.count(),orderby=db.sm_prescription_head.reg_id, groupby=db.sm_prescription_head.reg_id)        
         
    for pRow in pRecords:
        reg_id=pRow.sm_prescription_head.reg_id
        reg_name=pRow.sm_prescription_head.reg_name
        prescriptCount=pRow[db.sm_prescription_head.id.count()]
    
        presRecordShowList.append({'reg_id':reg_id,'reg_name':reg_name, 'Prescription':prescriptCount})

    
    return dict(presRecordShowList=presRecordShowList,fromDate=fromDate,toDate=toDate,regionValueShow=regionValueShow,page=page,items_per_page=items_per_page)

def pres_survey_summary_level0():
    c_id=session.cid
    
    response.title='Prescription Survey Summary- '+session.level0Name+' wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    
    if regionValue=='None':
        regionValue=''
    
    
    regionValueShow=regionValue    
    repCM=str(request.vars.repCM).strip()   
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    
    #------------------

    presRecordShowList=[]    
    
    qset=db()    
    qset=qset(db.sm_prescription_head.cid==c_id)
    qset=qset((db.sm_prescription_head.submit_date>=startDt)&(db.sm_prescription_head.submit_date<=endDt))

    if repCM!='':
        qset=qset(db.sm_prescription_head.submit_by_id==repCM)
        
    #------------    
    prescriptCount=0
    pRecords = qset.select(db.sm_prescription_head.submit_by_id,db.sm_prescription_head.submit_by_name,db.sm_prescription_head.id.count(), groupby=db.sm_prescription_head.submit_by_id,limitby=limitby)        
            
    for pRow in pRecords:
        submited_by_id=pRow.sm_prescription_head.submit_by_id
        submit_by_name=pRow.sm_prescription_head.submit_by_name
        prescriptCount=pRow[db.sm_prescription_head.id.count()]
    
        presRecordShowList.append({'SubmitedByID':submited_by_id,'SubmitedByName':submit_by_name, 'Prescription':prescriptCount})

    
    return dict(presRecordShowList=presRecordShowList,fromDate=fromDate,toDate=toDate,repCM=repCM,page=page,items_per_page=items_per_page)



def prescription_survey_summary_download():
    c_id=session.cid
    response.title='Prescription Details - Download'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate    

    repCM=str(request.vars.repCM).strip()   
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    regionValue=str(request.vars.regionValue).strip()   
    tlValue=str(request.vars.areaValue).strip()
    
    if (regionValue=='None') | (regionValue==''):
        regionValue='ALL'
    if (tlValue=='None') | (tlValue==''):
        tlValue='ALL'
    
    
    regionValueShow=regionValue  
    #------------------

    #------------    
    prescriptCount=0
    myString='Prescription Summary Territory Wise\n\n'
    myString+='Date From,'+fromDate+'\n'
    myString+='Date To,'+toDate+'\n'
    myString+='Region,'+regionValueShow+'\n'
    myString+='TL,'+tlValue+'\n\n'
        
    myString+='RegionID,RegionName,TLID,TLName,TerritoryID,TerritoryName,SubmittedbyID,SubmittedbyName,Qty\n'
    
    qset=db()    
    qset=qset(db.sm_prescription_head.cid==c_id)
    qset=qset((db.sm_prescription_head.submit_date>=startDt)&(db.sm_prescription_head.submit_date<=endDt))

    if (regionValueShow!='ALL') & (regionValueShow!=''):
        qset=qset(db.sm_prescription_head.reg_id==regionValueShow)
    if (tlValue!='ALL') & (tlValue!=''):
        qset=qset(db.sm_prescription_head.tl_id==tlValue)
        
    #------------    
    
    pRecords = qset.select(db.sm_prescription_head.ALL,db.sm_prescription_head.id.count(), groupby=db.sm_prescription_head.submit_by_id|db.sm_prescription_head.area_id|db.sm_prescription_head.tl_id |db.sm_prescription_head.reg_id,orderby=db.sm_prescription_head.reg_id|db.sm_prescription_head.tl_id |db.sm_prescription_head.area_id|db.sm_prescription_head.submit_by_id)
        
#     return pRecords
    total=0
    for pRow in pRecords:
        reg_id=pRow.sm_prescription_head.reg_id
        reg_name=pRow.sm_prescription_head.reg_name
        tl_id=pRow.sm_prescription_head.tl_id
        tl_name=pRow.sm_prescription_head.tl_name
        area_id=pRow.sm_prescription_head.area_id
        area_name=pRow.sm_prescription_head.area_name
        submit_by_id=pRow.sm_prescription_head.submit_by_id
        submit_by_name=pRow.sm_prescription_head.submit_by_name
        prescriptCount=pRow[db.sm_prescription_head.id.count()]
        total=total+int(prescriptCount)
 
                
        myString+=str(reg_id)+','+str(reg_name)+','+str(tl_id)+','+str(tl_name)+','+str(area_id)+','+str(area_name)+','+str(submit_by_id)+','+str(submit_by_name)+','+str(prescriptCount)+'\n'
#     myString+='\n\n,,,,,,,Total,'+str(total)+'\n'    
    #Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_prescription.csv'   
    return str(myString)




def pres_survey_visit_list():
    c_id=session.cid
    
    response.title='Prescription List'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    areaValue=str(request.vars.areaValue).strip()
    territoryValue=str(request.vars.territoryValue).strip()
    marketValue=str(request.vars.marketValue).strip()    
    repCM=str(request.vars.repCM).strip()
    
    if regionValue=='None':
        regionValue=''
    if areaValue=='None':
        areaValue=''
    if territoryValue=='None':
        territoryValue=''
    if marketValue=='None':
        marketValue=''
    if repCM=='None':
        repCM=''
        
    regionValueShow=regionValue    
    areaValueShow=areaValue    
    territoryValueShow=territoryValue    
    marketValueShow=marketValue
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_prescription_head.cid==c_id)
    qset=qset((db.sm_prescription_head.submit_date>=startDt)&(db.sm_prescription_head.submit_date<=endDt))
    
    
    if repCM!='':
        qset=qset(db.sm_prescription_head.submit_by_id==repCM)
    

    records=qset.select(db.sm_prescription_head.ALL,orderby=~db.sm_prescription_head.submit_date,limitby=limitby)
    
    return dict(records=records,fromDate=fromDate,toDate=toDate,repCM=repCM,page=page,items_per_page=items_per_page)

    


#================

def market_research_level0():
    c_id=session.cid
    
    response.title='Order Summary - '+session.level0Name+' wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    areaValue=str(request.vars.areaValue).strip()
    
    if regionValue=='None':
        regionValue=''
    if areaValue=='None':
        areaValue=''
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')  
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------   
    dateRecordsDictList=[]
    
#    qset1=db()
#    qset1=qset1((db.sm_level.cid == c_id)&(db.sm_level.depth == 0))
#    if regionValue!='':
#        qset1=qset1(db.sm_level.level_id==regionValue)
#    
#    levelRows=qset1.select(db.sm_level.level_id,db.sm_level.level_name, orderby=db.sm_level.level_id)
#    
#    
#    for levelRow in levelRows:
#        region_id = levelRow.level_id
#        region_name = levelRow.level_name
        
#        qset=db()
#        qset=qset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
#        qset=qset(db.sm_level.level0 == region_id)
#        
#        qset=qset(db.sm_order.cid==c_id)
#        qset=qset((db.sm_order.order_date>=startDt)&(db.sm_order.order_date<=endDt))
#        qset=qset(db.sm_order.area_id==db.sm_level.level_id)
#        
#        records=qset.select(db.sm_order.item_id,db.sm_order.quantity.sum(),db.sm_order.price,groupby=db.sm_order.item_id|db.sm_order.price) And L.level0='"+str(region_id)+"'
    
    conditoionStr=''
    if regionValue!='':
        conditoionStr="L.level0='"+regionValue+"'"
        
    if areaValue!='':                
        if conditoionStr=='':
            conditoionStr="L.level1='"+areaValue+"'"
        else: 
            conditoionStr+=" And L.level1='"+areaValue+"'"
    
    if conditoionStr=='':
        dateRecords="SELECT L.level0 as level0,sum(O.quantity*O.price) as orderTotal FROM sm_order O,sm_level L WHERE L.cid='"+c_id+"' And L.is_leaf='1'  And O.cid='"+c_id+"' And (O.order_date>='"+str(startDt)+"' And O.order_date<='"+str(endDt)+"') And (O.area_id=L.level_id)  Group by L.level0 order by L.level0"
    else:
        dateRecords="SELECT L.level0 as level0,sum(O.quantity*O.price) as orderTotal FROM sm_order O,sm_level L WHERE L.cid='"+c_id+"' And L.is_leaf='1' And "+conditoionStr+"  And O.cid='"+c_id+"' And (O.order_date>='"+str(startDt)+"' And O.order_date<='"+str(endDt)+"') And (O.area_id=L.level_id)  Group by L.level0 order by L.level0"
    
    dateRecordsDictList=db.executesql(dateRecords,as_dict = True)                    
    
    return dict(dateRecordsDictList=dateRecordsDictList,regionValue=regionValue,areaValue=areaValue,fromDate=fromDate,toDate=toDate)
def market_research_level1():
    c_id=session.cid
    
    response.title='Order Summary - '+session.level1Name+' wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    areaValue=str(request.vars.areaValue).strip()
    
    if regionValue=='None':
        regionValue=''
    if areaValue=='None':
        areaValue=''
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')  
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------
    dateRecordsDictList=[]
    
    conditoionStr=''
    if regionValue!='':
        conditoionStr="L.level0='"+regionValue+"'"
        
    if areaValue!='':                
        if conditoionStr=='':
            conditoionStr="L.level1='"+areaValue+"'"
        else: 
            conditoionStr+=" And L.level1='"+areaValue+"'"
    
    if conditoionStr=='':
        dateRecords="SELECT L.level0 as level0,L.level1 as level1,sum(O.quantity*O.price) as orderTotal FROM sm_order O,sm_level L WHERE L.cid='"+c_id+"' And L.is_leaf='1'  And O.cid='"+c_id+"' And (O.order_date>='"+str(startDt)+"' And O.order_date<='"+str(endDt)+"') And (O.area_id=L.level_id) Group by L.level0,L.level1 order by L.level0,L.level1"
    else:
        dateRecords="SELECT L.level0 as level0,L.level1 as level1,sum(O.quantity*O.price) as orderTotal FROM sm_order O,sm_level L WHERE L.cid='"+c_id+"' And L.is_leaf='1' And "+conditoionStr+"  And O.cid='"+c_id+"' And (O.order_date>='"+str(startDt)+"' And O.order_date<='"+str(endDt)+"') And (O.area_id=L.level_id) Group by L.level0,L.level1 order by L.level0,L.level1"
        
    dateRecordsDictList=db.executesql(dateRecords,as_dict = True)                    
    
    return dict(dateRecordsDictList=dateRecordsDictList,regionValue=regionValue,areaValue=areaValue,fromDate=fromDate,toDate=toDate)
def market_research_rep():
    c_id=session.cid
    
    response.title='Order Summary - SR wise'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    areaValue=str(request.vars.areaValue).strip()
    
    if regionValue=='None':
        regionValue=''
    if areaValue=='None':
        areaValue=''
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d').strftime('%Y-%m-%d')  
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d').strftime('%Y-%m-%d')
    
    #--------------
    dateRecordsDictList=[]
    
    conditoionStr=''
    if regionValue!='':
        conditoionStr="L.level0='"+regionValue+"'"
        
    if areaValue!='':                
        if conditoionStr=='':
            conditoionStr="L.level1='"+areaValue+"'"
        else: 
            conditoionStr+=" And L.level1='"+areaValue+"'"
    
    if conditoionStr=='':
        dateRecords="SELECT L.level0 as level0,L.level1 as level1, O.rep_id as repId,O.rep_name as repName, sum(O.quantity*O.price) as orderTotal FROM sm_order O,sm_level L WHERE L.cid='"+c_id+"' And L.is_leaf='1'  And O.cid='"+c_id+"' And (O.order_date>='"+str(startDt)+"' And O.order_date<='"+str(endDt)+"') And (O.area_id=L.level_id) Group by L.level0,L.level1,O.rep_id order by L.level0,L.level1,O.rep_id"
    else:
        dateRecords="SELECT L.level0 as level0,L.level1 as level1, O.rep_id as repId,O.rep_name as repName, sum(O.quantity*O.price) as orderTotal FROM sm_order O,sm_level L WHERE L.cid='"+c_id+"' And L.is_leaf='1' And "+conditoionStr+"  And O.cid='"+c_id+"' And (O.order_date>='"+str(startDt)+"' And O.order_date<='"+str(endDt)+"') And (O.area_id=L.level_id) Group by L.level0,L.level1,O.rep_id order by L.level0,L.level1,O.rep_id"
        
    dateRecordsDictList=db.executesql(dateRecords,as_dict = True)                    
    
    return dict(dateRecordsDictList=dateRecordsDictList,regionValue=regionValue,areaValue=areaValue,fromDate=fromDate,toDate=toDate)
    
    
def doctor_visit_list():
    c_id=session.cid
    
    response.title='Doctor Visit List'
    
    fromDate=request.vars.fromDate
    toDate=request.vars.toDate
    
    regionValue=str(request.vars.regionValue).strip()
    areaValue=str(request.vars.areaValue).strip()
    territoryValue=str(request.vars.territoryValue).strip()
    marketValue=str(request.vars.marketValue).strip()    
    repCM=str(request.vars.repCM).strip()
    
    if regionValue=='None':
        regionValue=''
    if areaValue=='None':
        areaValue=''
    if territoryValue=='None':
        territoryValue=''
    if marketValue=='None':
        marketValue=''
    if repCM=='None':
        repCM=''
        
    regionValueShow=regionValue    
    areaValueShow=areaValue    
    territoryValueShow=territoryValue    
    marketValueShow=marketValue
    
    startDt=datetime.datetime.strptime(str(fromDate),'%Y-%m-%d')    
    endDt=datetime.datetime.strptime(str(toDate),'%Y-%m-%d')
    
    #--------------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=20   
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #---------------end paging
    
    qset=db()
    qset=qset(db.sm_doctor_visit.cid==c_id)
    qset=qset((db.sm_doctor_visit.visit_date>=startDt)&(db.sm_doctor_visit.visit_date<=endDt))
    qset=qset((db.sm_level.cid == c_id)&(db.sm_level.is_leaf == '1'))
    
    if (regionValue!='' or areaValue!='' or territoryValue!='' or marketValue!=''):        
        if regionValue!='':
            qset=qset(db.sm_level.level0==regionValue)
        if areaValue!='':
            qset=qset(db.sm_level.level1==areaValue)
           
        if territoryValue!='':
            qset=qset(db.sm_level.level2==territoryValue)
            
        if marketValue!='':
            qset=qset(db.sm_level.level3==marketValue)
    
    if repCM!='':
        qset=qset(db.sm_doctor_visit.rep_id==repCM)
    
    qset=qset(db.sm_doctor_visit.route_id == db.sm_level.level_id)
    
    records=qset.select(db.sm_doctor_visit.ALL,orderby=~db.sm_doctor_visit.id,limitby=limitby)
    
    return dict(records=records,fromDate=fromDate,toDate=toDate,regionValue=regionValue,regionValueShow=regionValueShow,areaValue=areaValue,territoryValue=territoryValue,areaValueShow=areaValueShow,territoryValueShow=territoryValueShow,marketValue=marketValue,marketValueShow=marketValueShow,repCM=repCM,page=page,items_per_page=items_per_page)


def dashboard_today():
    c_id = session.cid

    response.title = 'Dashboard current Date'

    fromDate = current_date
    toDate = current_date

    regionValue = str(request.vars.regionValue).strip()
    areaValue = str(request.vars.areaValue).strip()
    territoryValue = str(request.vars.territoryValue).strip()
    marketValue = str(request.vars.marketValue).strip()
    repCM = str(request.vars.repCM).strip()

    if regionValue == 'None':
        regionValue = ''
    if areaValue == 'None':
        areaValue = ''
    if territoryValue == 'None':
        territoryValue = ''
    if marketValue == 'None':
        marketValue = ''
    if repCM == 'None':
        repCM = ''

    regionValueShow = regionValue

    areaValueShow = areaValue

    territoryValueShow = territoryValue

    marketValueShow = marketValue

    startDt = datetime.datetime.strptime(str(fromDate), '%Y-%m-%d')
    endDt = datetime.datetime.strptime(str(toDate), '%Y-%m-%d')
    nextDate = endDt + datetime.timedelta(days=1)

    # --------------paging
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 20
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # ---------------end paging

    condition = ''
    if regionValue != '':
        condition += " AND level0_id = '" + regionValue + "'"
    if areaValue != '':
        condition += " AND level1_id = '" + areaValue + "'"

    # if repCM != '':
    #     condition += " AND rep_id = '" + repCM + "'"

    condition1 = ''
    if regionValue != '':
        condition1 += " AND a.level0 = '" + regionValue + "'"
    if areaValue != '':
        condition1 += " AND a.level1 = '" + areaValue + "'"


    # total sales
    salesRecords = "SELECT sum(total_amount) as total_amount  FROM sm_invoice_head WHERE cid = '" + c_id + "' and invoice_date >= '" + fromDate + "' and invoice_date <= '" + toDate + "' and status='Invoiced' " + condition + " GROUP BY cid;"
    salesRecords = db.executesql(salesRecords, as_dict=True)

    total_sales = 0
    for i in range(len(salesRecords)):
        salesRecordsStr = salesRecords[i]
        total_sales = salesRecordsStr['total_amount']

    # day wise sales last 7 days
    preDate = endDt - datetime.timedelta(days=6)
    salesRecords1 = "SELECT invoice_date,sum(total_amount) as sales_amount  FROM sm_invoice_head WHERE cid = '" + c_id + "' and invoice_date >= '" + str(preDate)[:10] + "' and invoice_date <= '" + toDate + "' and status='Invoiced' " + condition + " GROUP BY cid,invoice_date;"
    salesRecords1= db.executesql(salesRecords1, as_dict=True)

    seven_day_list=[]
    seven_day_list.append(str(preDate)[:10])
    for i in range(1,7):
        nDate = str(preDate + datetime.timedelta(days=i))[:10]
        seven_day_list.append(nDate)

    seven_day_sales_list=[]
    seven_day_sales_list_head=['Days','Sales']
    seven_day_sales_list.append(seven_day_sales_list_head)
    for i in range(len(seven_day_list)):
        invoice_date=seven_day_list[i]
        invoice_day=str(datetime.datetime.strptime(str(invoice_date), '%Y-%m-%d').strftime("%a"))

        invoice_date_sales=0
        for j in range(len(salesRecords1)):
            salesRecordsStr1 = salesRecords1[j]
            invoice_date1 = str(salesRecordsStr1['invoice_date'])
            if invoice_date==invoice_date1:
                invoice_date_sales=salesRecordsStr1['sales_amount']
                break

        sales_list=[invoice_day,invoice_date_sales]
        seven_day_sales_list.append(sales_list)

    # scheduled outlet
    total_scheduled_client = 0
    clientRecords = "SELECT count(b.id) as schesuled_client  FROM sm_level a,sm_client b WHERE a.cid = '" + c_id + "' AND a.cid=b.cid and a.depth=3 AND a.level_id=b.area_id " + condition1 + "  GROUP BY a.cid;"
    clientRecords = db.executesql(clientRecords, as_dict=True)
    for i in range(len(clientRecords)):
        clientRecordsStr = clientRecords[i]
        total_scheduled_client = clientRecordsStr['schesuled_client']

    # zero sales  scheduled outlet
    zero_sales_scheduled_client = 0
    orderRecords = "SELECT count(distinct(client_id)) as zero_sales_scheduled_client  FROM sm_order_head WHERE cid = '" + c_id + "' AND order_date >= '" + str(fromDate) + "' AND order_date <= '" + str(toDate) + "' AND status='Submitted' AND visit_type='Scheduled' " + condition + " GROUP BY cid;"
    orderRecords = db.executesql(orderRecords, as_dict=True)

    for i in range(len(orderRecords)):
        orderRecordsStr = orderRecords[i]
        zero_sales_scheduled_client = orderRecordsStr['zero_sales_scheduled_client']


    # zero sales  unscheduled outlet
    zero_sales_unscheduled_client = 0
    orderRecords1 = "SELECT count(distinct(client_id)) as zero_sales_unscheduled_client  FROM sm_order_head WHERE cid = '" + c_id + "' AND order_date >= '" + str(fromDate) + "' AND order_date <= '" + str(toDate) + "' AND status='Submitted' AND visit_type='unscheduled' " + condition + " GROUP BY cid;"
    orderRecords1 = db.executesql(orderRecords1, as_dict=True)
    for i in range(len(orderRecords1)):
        orderRecordsStr1 = orderRecords1[i]
        zero_sales_unscheduled_client = orderRecordsStr1['zero_sales_unscheduled_client']

    # sales unique outlet
    sales_unique_outlet = 0
    invRecords = "SELECT count(distinct(client_id)) as sales_unique_outlet  FROM sm_invoice_head WHERE cid = '" + c_id + "' AND invoice_date >= '" + str(fromDate) + "' AND invoice_date <= '" + str(toDate) + "' AND status='Invoiced' " + condition + " GROUP BY cid;"
    invRecords = db.executesql(invRecords, as_dict=True)

    for i in range(len(invRecords)):
        invRecordsStr = invRecords[i]
        sales_unique_outlet = invRecordsStr['sales_unique_outlet']

    # new client
    total_new_client=0
    clientRecords1 = "SELECT count(b.id) as new_client  FROM sm_level a,sm_client b WHERE a.cid = '" + c_id + "' AND b.created_on >= '" + str(startDt) + "' AND b.created_on < '" + str(nextDate) + "' AND a.cid=b.cid and a.depth=3 AND a.level_id=b.area_id " + condition1 + "  GROUP BY a.cid;"
    clientRecords1 = db.executesql(clientRecords1, as_dict=True)

    for i in range(len(clientRecords1)):
        clientRecordsStr1 = clientRecords1[i]
        total_new_client = clientRecordsStr1['new_client']


    return dict(total_sales=total_sales,seven_day_sales_list=seven_day_sales_list,total_scheduled_client=total_scheduled_client,zero_sales_scheduled_client=zero_sales_scheduled_client,zero_sales_unscheduled_client=zero_sales_unscheduled_client,sales_unique_outlet=sales_unique_outlet,total_new_client=total_new_client,
                fromDate=fromDate, toDate=toDate,
                regionValue=regionValue, regionValueShow=regionValueShow, areaValue=areaValue,
                territoryValue=territoryValue, areaValueShow=areaValueShow, territoryValueShow=territoryValueShow,
                marketValue=marketValue, marketValueShow=marketValueShow, repCM=repCM, page=page,
                items_per_page=items_per_page)



def dashboard_new():
    c_id = session.cid

    response.title = 'Dashboard new'

    fromDate = str(first_currentDate)[:10]
    toDate = current_date

    next_month_first_date=add_months(first_currentDate, 1)


    startDt = datetime.datetime.strptime(str(fromDate), '%Y-%m-%d')
    endDt = datetime.datetime.strptime(str(toDate), '%Y-%m-%d')
    nextDate = endDt + datetime.timedelta(days=1)


    # total sales
    salesRecords = "SELECT sum(total_amount) as total_amount  FROM sm_invoice_head WHERE cid = '" + c_id + "' and invoice_date >= '" + fromDate + "' and invoice_date <= '" + toDate + "' and status='Invoiced' GROUP BY cid;"
    salesRecords = db.executesql(salesRecords, as_dict=True)

    total_sales = 0
    for i in range(len(salesRecords)):
        salesRecordsStr = salesRecords[i]
        total_sales = salesRecordsStr['total_amount']

    # day wise sales last 7 days
    preDate = endDt - datetime.timedelta(days=6)
    salesRecords1 = "SELECT invoice_date,sum(total_amount) as sales_amount  FROM sm_invoice_head WHERE cid = '" + c_id + "' and invoice_date >= '" + str(preDate)[:10] + "' and invoice_date <= '" + toDate + "' and status='Invoiced' GROUP BY cid,invoice_date;"
    salesRecords1= db.executesql(salesRecords1, as_dict=True)

    seven_day_list=[]
    seven_day_list.append(str(preDate)[:10])
    for i in range(1,7):
        nDate = str(preDate + datetime.timedelta(days=i))[:10]
        seven_day_list.append(nDate)

    seven_day_sales_list=[]
    seven_day_sales_list_head=['Days','Sales']
    seven_day_sales_list.append(seven_day_sales_list_head)
    for i in range(len(seven_day_list)):
        invoice_date=seven_day_list[i]
        invoice_day=str(datetime.datetime.strptime(str(invoice_date), '%Y-%m-%d').strftime("%a"))

        invoice_date_sales=0
        for j in range(len(salesRecords1)):
            salesRecordsStr1 = salesRecords1[j]
            invoice_date1 = str(salesRecordsStr1['invoice_date'])
            if invoice_date==invoice_date1:
                invoice_date_sales=salesRecordsStr1['sales_amount']
                break

        sales_list=[invoice_day,invoice_date_sales]
        seven_day_sales_list.append(sales_list)

    # region wise sales
    regionRows = "SELECT level_id  FROM sm_level WHERE cid = '" + c_id + "' and depth=1 ;"
    regionRows = db.executesql(regionRows, as_dict=True)

    # region wise sales last 7 days
    preDate = endDt - datetime.timedelta(days=6)
    salesRecords2 = "SELECT level1_id,sum(total_amount) as sales_amount  FROM sm_invoice_head WHERE cid = '" + c_id + "' and invoice_date >= '" + str(preDate)[:10] + "' and invoice_date <= '" + toDate + "' and status='Invoiced' GROUP BY cid,level0_id;"
    salesRecords2 = db.executesql(salesRecords2, as_dict=True)


    seven_day_sales_list_region_wise=[]
    seven_day_sales_list_region_wise_head=['Region','Sales']
    seven_day_sales_list_region_wise.append(seven_day_sales_list_region_wise_head)
    for i in range(len(regionRows)):
        regionRowsStr=regionRows[i]
        region_id=str(regionRowsStr['level_id'])

        region_sales=0
        for j in range(len(salesRecords2)):
            salesRecordsStr2 = salesRecords2[j]
            region_id1 = str(salesRecordsStr2['level1_id'])
            if region_id==region_id1:
                region_sales=salesRecordsStr2['sales_amount']
                break

        sales_list=[region_id,region_sales]
        seven_day_sales_list_region_wise.append(sales_list)

    # target
    total_target_amt=0
    targetSql = "SELECT sum(target_qty*price) target_amt FROM target_vs_achievement_route_item WHERE cid = '" + c_id + "' AND first_date = '" + str(first_currentDate)[:10] + "' GROUP BY cid"
    targetRows = db.executesql(targetSql, as_dict=True)
    for i in range(len(targetRows)):
        targetRowsStr=targetRows[i]
        total_target_amt=targetRowsStr['target_amt']

    total_no_of_day_this_month = (datetime.datetime.strptime(str(next_month_first_date), '%Y-%m-%d') - startDt).days
    no_of_day_this_month = str(current_date)[-2:]

    this_day_target=float(total_target_amt/total_no_of_day_this_month)*int(no_of_day_this_month)

    # achievement
    total_achivement_amt=0
    achievementSql = "SELECT sum(total_amount) as ach_amt  FROM sm_invoice_head WHERE cid = '" + c_id + "' and invoice_date >= '" + fromDate + "' and invoice_date <= '" + toDate + "' and status='Invoiced' GROUP BY cid;"
    achievementRows = db.executesql(achievementSql, as_dict=True)
    for i in range(len(achievementRows)):
        achievementRowsStr = achievementRows[i]
        total_achivement_amt = achievementRowsStr['ach_amt']

    shortfall = this_day_target-total_achivement_amt


    achieve_percent=0
    if total_target_amt>0:
        achieve_percent=round((total_achivement_amt/total_target_amt*100),2)

    # projected
    daily_achive=total_achivement_amt/int(no_of_day_this_month)
    day_left_this_month=int(total_no_of_day_this_month)-int(no_of_day_this_month)

    projected = float(daily_achive) * int(day_left_this_month)

    return dict(projected=projected,achieve_percent=achieve_percent,shortfall=shortfall,total_target_amt=total_target_amt,total_achivement_amt=total_achivement_amt,total_sales=total_sales,seven_day_sales_list=seven_day_sales_list,seven_day_sales_list_region_wise=seven_day_sales_list_region_wise)