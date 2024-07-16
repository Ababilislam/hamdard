



def money_indent_level_show():

    cid=session.cid
       
    response.title='Money Indent Level Show'

    page=request.args(0)
    record=request.args(1)
    # return record

    # record= db.pms_money_indent(request.args(1))

    

    ref_show=''
    pm_date_show=''
    acc_sl_show=''
    t_id_show=''
    t_name_show=''
    dept_show=''
    brand_id_show=''
    pms_purpose_show=''
    p_amount_show=''
    trnsfr_acc_show=''
    trnsfr_bank_show=''
    activity_from_show=''
    activity_to_show=''
    expected_adjustment_date_show=''
    raised_by=''
    record_row=db((db.pms_money_indent.cid==cid)  & (db.pms_money_indent.ref==record)).select(db.pms_money_indent.p_amount.sum(),db.pms_money_indent.ALL,orderby=db.pms_money_indent.id,groupby=db.pms_money_indent.ref)
     
    
    for record_row in record_row:  
        raised_by=record_row.pms_money_indent.raisedby
        ref_show=record_row.pms_money_indent.ref

        pm_date_show=record_row.pms_money_indent.pm_date
        acc_sl_show=record_row.pms_money_indent.acc_sl
        t_id_show=record_row.pms_money_indent.t_id
        t_name_show=record_row.pms_money_indent.t_name
        dept_show=record_row.pms_money_indent.dept
        brand_id_show=record_row.pms_money_indent.brand_id

        pms_purpose_show=str(record_row.pms_money_indent.pms_purpose).strip() 
        p_amount_show=record_row[db.pms_money_indent.p_amount.sum()] 
        trnsfr_acc_show=record_row.pms_money_indent.trnsfr_acc
        trnsfr_bank_show=record_row.pms_money_indent.trnsfr_bank

        activity_from_show=str(record_row.pms_money_indent.activity_from)#.split('-')[1]+'/'+str(record_row.pms_money_indent.activity_from).split('-')[2]+'/'+str(record_row.pms_money_indent.activity_from).split('-').pms_money_indent
        activity_to_show=record_row.pms_money_indent.activity_to

        expected_adjustment_date_show=record_row.pms_money_indent.expected_adjustment_date
        
        # ==================
        sub_cid=str(request.vars.sub_cid).strip()   
        pm_year=str(current_date).strip().split('-')[0]
        p_month=str(current_date).strip().split('-')[1] 
        pms_purpose=str(request.vars.pms_purpose).strip().replace('[','').replace(']','').replace("'","").replace(",","")
        pms_desc=str(request.vars.pms_description).strip()
        # return pms_desc
        p_amount=str(request.vars.p_amount).strip()
        
        ref=str(request.vars.ref).strip()
        trnsfr_instruction=str(request.vars.trnsfr_instruction).strip() 
        pm_date=str(current_date).strip()
        
        trnsfr_acc=str(request.vars.trnsfr_acc).strip()
        # acc_sl=str(request.vars.acc_sl).strip()
        trnsfr_bank=str(request.vars.trnsfr_bank).strip()
        activity_from=str(request.vars.activity_from).strip()
        brand_id=str(request.vars.brand_id).strip()
        activity_to=str(request.vars.activity_to).strip()
        dept=str(request.vars.dept).strip()
        expected_adjustment_date=str(request.vars.expected_adjustment_date).strip()
        t_id=''
        t_name=''
        t_dept=''
        tm_id_name=str(request.vars.tm_id_name).strip()
        if ((tm_id_name!=None) and (tm_id_name!='')  and (tm_id_name!='None')):
            try:
                t_id=tm_id_name.split('|')[0]
                t_name=tm_id_name.split('|')[1]
            except:
                t_id=''
                t_name=''
            try:
                t_dept=tm_id_name.split('|')[2]
            except:
                t_dept=''
        
        # ======
        # ===========
        # return ref_show
       

        
    btn_approve=request.vars.btn_approve
    btn_cancel=request.vars.btn_cancel
    btn_disbursed=request.vars.btn_disbursed
    # return btn_disbursed
    status=request.vars.status
    
    if btn_approve =='Confirm':
        # return '1'
        db((db.pms_money_indent.ref == record)).update(pm_year=pm_year,p_month=p_month,pms_purpose=pms_purpose,pm_date=pm_date,trnsfr_acc=trnsfr_acc,trnsfr_bank=trnsfr_bank,t_id=t_id,activity_from=activity_from,t_name=t_name,activity_to=activity_to,expected_adjustment_date=expected_adjustment_date,confirm_cancel_by=session.user_id,confirm_cancel_time=datetime_fixed,status='Approved')
        db((db.pms_money_indent_head.ref == record)).update(pm_year=pm_year,p_month=p_month,pms_purpose=pms_purpose,pm_date=pm_date,trnsfr_acc=trnsfr_acc,trnsfr_bank=trnsfr_bank,t_id=t_id,activity_from=activity_from,t_name=t_name,activity_to=activity_to,expected_adjustment_date=expected_adjustment_date,confirm_cancel_by=session.user_id,confirm_cancel_time=datetime_fixed,status='Approved')
        session.flash = 'Confirmed Successfully'
        confirm_status=db((db.pms_money_indent_head.cid==cid) & (db.pms_money_indent_head.ref==record)).select(db.pms_money_indent_head.status,orderby=db.pms_money_indent_head.id,groupby=db.pms_money_indent_head.ref)
        
        if confirm_status:  
            status=confirm_status[0].status
          

        redirect (URL(c='money_indent_level_show',f='money_indent_level_show',args=[page,record],vars=dict(status=status))) 
    if btn_cancel =='Cancel':
         
        db((db.pms_money_indent.ref == record)).update(status='Canceled')
        db((db.pms_money_indent_head.ref == record)).update(status='Canceled')
        session.flash = 'Canceled Successfully'
        confirm_status=db((db.pms_money_indent_head.cid==cid) & (db.pms_money_indent_head.ref==record)).select(db.pms_money_indent_head.status,orderby=db.pms_money_indent_head.id,groupby=db.pms_money_indent_head.ref)
        
        if confirm_status:  
            status=confirm_status[0].status
        redirect (URL(c='money_indent_level_show',f='money_indent_level_show',args=[page,record],vars=dict(status=status))) 
    if btn_disbursed =='Confirm Payment':
        # return 'jh'
        db((db.pms_money_indent.ref == record)).update(status='Disbursed')
        db((db.pms_money_indent_head.ref == record)).update(status='Disbursed')
        session.flash = 'Disbursed Successfully'
        confirm_status=db((db.pms_money_indent_head.cid==cid) & (db.pms_money_indent_head.ref==record)).select(db.pms_money_indent_head.status,orderby=db.pms_money_indent_head.id,groupby=db.pms_money_indent_head.ref)
        
        if confirm_status:  
            status=confirm_status[0].status
        # return status
        redirect (URL(c='money_indent_level_show',f='money_indent_level_show',args=[page,record],vars=dict(status=status))) 
    
    emp_id='-'
    emp_name='-'
    emp_designation='-'
    emp_dept='-'
    emp_r_acc='-'
    emp_info=db((db.pms_employee.cid==cid) & (db.pms_employee.emp_id==raised_by)).select(db.pms_employee.ALL,orderby=db.pms_employee.id,limitby=(0,1))
    # return c_id
    if emp_info: 
        emp_id=emp_info[0].emp_id
        emp_name=emp_info[0].emp_name
        emp_designation=emp_info[0].emp_designation
        emp_dept=emp_info[0].dept 
        emp_r_acc=emp_info[0].bank_acc_no 

        pass


    return dict(page=page,status=status,record=record,emp_id=emp_id,emp_name=emp_name,emp_designation=emp_designation,emp_dept=emp_dept,ref_show=ref_show,pm_date_show=pm_date_show,acc_sl_show=acc_sl_show,t_id_show=t_id_show,t_name_show=t_name_show,dept_show=dept_show,brand_id_show=brand_id_show,pms_purpose_show=pms_purpose_show,p_amount_show=p_amount_show,trnsfr_acc_show=trnsfr_acc_show,trnsfr_bank_show=trnsfr_bank_show,activity_from_show=activity_from_show,activity_to_show=activity_to_show,expected_adjustment_date_show=expected_adjustment_date_show,emp_r_acc=emp_r_acc)




def money_indent_adjust():
    cid=session.cid
    response.title='Money Indent Level Show'
    page=request.args(0)
    record=request.args(1)
    # return record
    raised_by=''



    record_row=db((db.pms_money_indent.cid==cid)  & (db.pms_money_indent.ref==record)).select(db.pms_money_indent.ALL,orderby=db.pms_money_indent.id,limitby=(0,1))
    
    if record_row:
        raised_by=record_row[0].raisedby
        sub_cid_show=record_row[0].sub_cid
        pm_year_show=record_row[0].pm_year
        p_month_show=record_row[0].p_month
        ref_show=record_row[0].ref

        pm_date_show=record_row[0].pm_date
        acc_sl_show=record_row[0].acc_sl
        t_id_show=record_row[0].t_id
        t_name_show=record_row[0].t_name
        dept_show=record_row[0].dept
        brand_id_show=record_row[0].brand_id

        pms_purpose_show=str(record_row[0].pms_purpose).strip()
        pms_desc_show=record_row[0].pms_desc
        p_amount_show=record_row[0].p_amount
        trnsfr_instruction_show=record_row[0].trnsfr_instruction
        trnsfr_acc_show=record_row[0].trnsfr_acc
        trnsfr_bank_show=record_row[0].trnsfr_bank

        activity_from_show=str(record_row[0].activity_from)#.split('-')[1]+'/'+str(record_row[0].activity_from).split('-')[2]+'/'+str(record_row[0].activity_from).split('-')[0]
        activity_to_show=record_row[0].activity_to

        expected_adjustment_date_show=record_row[0].expected_adjustment_date

        bill_rec_date_show=record_row[0].bill_rec_date
        bill_rec_amt_show=record_row[0].bill_rec_amt
        refund_paid_show=record_row[0].refund_paid
        narration_show=record_row[0].narration
        meeting_tour_place_show=record_row[0].meeting_tour_place
        date_from_show=record_row[0].date_from
        date_to_show=record_row[0].date_to
        no_of_meeting_show=record_row[0].no_of_meeting
        participants_show=record_row[0].participants
        
        



        btn_adjust          =request.vars.btn_adjust
       
        bill_rec_date       =request.vars.bill_rec_date
        bill_rec_amt        =request.vars.bill_rec_amt
        refund_paid         =request.vars.refund_paid
        narration           =request.vars.narration
        meeting_tour_place  =request.vars.meeting_tour_place
        date_from           =request.vars.date_from
        date_to             =request.vars.date_from
        no_of_meeting       =request.vars.no_of_meeting
        participants        =request.vars.participants


        cycle_meeting=request.vars.cycle_meeting
        # return  cycle_meeting
        regional_meeting=request.vars.regional_meeting
        clinical_meeting=request.vars.clinical_meeting
        tour_expense_bill=request.vars.tour_expense_bill
        brand_promotion=request.vars.brand_promotion
        birthday_gift=request.vars.birthday_gift

        eskayef_attended_person=request.vars.eskayef_attended_person
        id_no=request.vars.id_no
        meeting_date=request.vars.meeting_date
        # return id_no 
        region=request.vars.region
        location_address=request.vars.location_address
        place_of_tour=request.vars.place_of_tour
        tour_period_and_objective=request.vars.tour_period_and_objective
        no_of_perticipents=request.vars.no_of_perticipents
        meeting_expense_or_other_expense=request.vars.meeting_expense_or_other_expense
 
        if (meeting_date=='None' or meeting_date==None or meeting_date==''):
            meeting_date=current_date
        # return meeting_date
        if (meeting_expense_or_other_expense=='None' or  meeting_expense_or_other_expense==None):
            meeting_expense_or_other_expense=0
        if (cycle_meeting=='None' or cycle_meeting==None):
            cycle_meeting=0
        if (regional_meeting=='None' or regional_meeting==None):
            regional_meeting=0
        if (clinical_meeting=='None' or clinical_meeting==None):
            clinical_meeting=0
        if (tour_expense_bill=='None' or tour_expense_bill==None):
            tour_expense_bill=0
        if (brand_promotion=='None' or brand_promotion==None):
            brand_promotion=0
        if (birthday_gift=='None' or birthday_gift==None):
            birthday_gift=0
        # return birthday_gift
 
        hall_rent_sl=request.vars.hall_rent_sl
        hall_rent_amount= request.vars.hall_rent_amount
        morning_refreshment_sl=request.vars.morning_refreshment_sl
        morning_refreshment_amount= request.vars.morning_refreshment_amount
        evening_refreshment_sl=request.vars.evening_refreshment_sl
        evening_refreshment_amount= request.vars.evening_refreshment_amount
        lunch_dinner_with_pre_pcb_sl=request.vars.lunch_dinner_with_pre_pcb_sl
        lunch_dinner_with_pre_pcb_amount= request.vars.lunch_dinner_with_pre_pcb_amount
        stationer_gift_sl=request.vars.stationer_gift_sl
        stationer_gift_amount= request.vars.stationer_gift_amount
        tips_and_others_sl=request.vars.tips_and_others_sl
        tips_and_others_amount= request.vars.tips_and_others_amount
        
        transport_fare_fuel_sl=request.vars.transport_fare_fuel_sl
        transport_fare_fuel_amount=request.vars.transport_fare_fuel_amount
        self_boarding_sl=request.vars.self_boarding_sl
        self_boarding_amount=request.vars.self_boarding_amount
        food_expense_sl=request.vars.food_expense_sl
        food_expense_amount=request.vars.food_expense_amount
        driver_expense_sl=request.vars.driver_expense_sl
        driver_expense_amount=request.vars.driver_expense_amount
        tips_telephone_and_others_sl=request.vars.tips_telephone_and_others_sl
        tips_telephone_and_others_amount=request.vars.tips_telephone_and_others_amount
        tour_allowance_sl=request.vars.tour_allowance_sl
        tour_allowance_amount=request.vars.tour_allowance_amount

        
        if btn_adjust =='Adjust Bill':
            updaterow=db((db.pms_money_indent_head.ref == record)).update(cycle_meeting=cycle_meeting,regional_meeting=regional_meeting,clinical_meeting=clinical_meeting,tour_expense_bill=tour_expense_bill,brand_promotion=brand_promotion,birthday_gift=birthday_gift,eskayef_attended_person=eskayef_attended_person,narration=id_no,meeting_date=meeting_date,region=region,location_address=location_address,place_of_tour=place_of_tour,tour_period_and_objective=tour_period_and_objective,no_of_perticipents=no_of_perticipents,meeting_expense_or_other_expense=meeting_expense_or_other_expense,hall_rent_sl=hall_rent_sl,morning_refreshment_sl=morning_refreshment_sl,evening_refreshment_sl=evening_refreshment_sl,lunch_dinner_with_pre_pcb_sl=lunch_dinner_with_pre_pcb_sl,stationer_gift_sl=stationer_gift_sl,tips_and_others_sl=tips_and_others_sl,hall_rent_amount=hall_rent_amount,morning_refreshment_amount=morning_refreshment_amount,evening_refreshment_amount=evening_refreshment_amount,lunch_dinner_with_pre_pcb_amount=lunch_dinner_with_pre_pcb_amount,stationer_gift_amount=stationer_gift_amount,tips_and_others_amount=tips_and_others_amount,transport_fare_fuel_sl=transport_fare_fuel_sl,self_boarding_sl=self_boarding_sl,food_expense_sl=food_expense_sl,driver_expense_sl=driver_expense_sl,tips_telephone_and_others_sl=tips_telephone_and_others_sl,tour_allowance_sl=tour_allowance_sl,transport_fare_fuel_amount=transport_fare_fuel_amount,self_boarding_amount=self_boarding_amount,food_expense_amount=food_expense_amount,driver_expense_amount=driver_expense_amount,tips_telephone_and_others_amount=tips_telephone_and_others_amount,tour_allowance_amount=tour_allowance_amount,adjustby=session.user_id,adjust_time=datetime_fixed,status='Bill Adjusted')
            if updaterow: 
                db((db.pms_money_indent.ref == record)).update(status='Bill Adjusted')
            pass
            session.flash = 'Adjusted Successfully'
            redirect (URL(c='money_indent_level_show',f='money_indent_adjust',args=[page,record]))
    emp_id='-'
    emp_name='-'
    emp_designation='-'
    emp_dept='-'
    emp_r_acc='-'
    emp_info=db((db.pms_employee.cid==cid) & (db.pms_employee.emp_id==raised_by)).select(db.pms_employee.ALL,orderby=db.pms_employee.id,limitby=(0,1))
    # return c_id
    if emp_info: 
        emp_id=emp_info[0].emp_id
        emp_name=emp_info[0].emp_name
        emp_designation=emp_info[0].emp_designation
        emp_dept=emp_info[0].dept 
        emp_r_acc=emp_info[0].bank_acc_no 

        pass    

    return dict(page=page,record=record,sub_cid_show=sub_cid_show,ref_show=ref_show,pm_date_show=pm_date_show,acc_sl_show=acc_sl_show,t_id_show=t_id_show,t_name_show=t_name_show,dept_show=dept_show,brand_id_show=brand_id_show,pms_purpose_show=pms_purpose_show,p_amount_show=p_amount_show,trnsfr_instruction_show=trnsfr_instruction_show,trnsfr_acc_show=trnsfr_acc_show,trnsfr_bank_show=trnsfr_bank_show,activity_from_show=activity_from_show,activity_to_show=activity_to_show,expected_adjustment_date_show=expected_adjustment_date_show,pms_desc_show=pms_desc_show,bill_rec_date_show=bill_rec_date_show,bill_rec_amt_show=bill_rec_amt_show,refund_paid_show=refund_paid_show,narration_show=narration_show,meeting_tour_place_show=meeting_tour_place_show,date_from_show=date_from_show,date_to_show=date_to_show,no_of_meeting_show=no_of_meeting_show,participants_show=participants_show,raised_by=raised_by,emp_id=emp_id,emp_name=emp_name,emp_designation=emp_designation,emp_dept=emp_dept,emp_r_acc=emp_r_acc)






