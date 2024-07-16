
from random import randint

#---------------------------- ADD VALIDATION
def invoice_rules_validation(form):
    c_id=session.cid
    
    campaign_ref=str(form.vars.campaign_ref).strip().upper()    
    client_cat=form.vars.client_cat
    
    from_date=form.vars.from_date
    to_date=form.vars.to_date
    
    for_any_item=str(form.vars.for_any_item).strip().upper()
    from_amt_qty=form.vars.from_amt_qty
    to_amt_qty=form.vars.to_amt_qty
    
    bonus_type=form.vars.bonus_type
    
    b_item_id1=str(form.vars.b_item_id1).strip().upper()
    b_item_id2=str(form.vars.b_item_id2).strip().upper()
    b_item_id3=str(form.vars.b_item_id3).strip().upper()
    
    b_item_qty1=form.vars.b_item_qty1
    b_item_qty2=form.vars.b_item_qty2
    b_item_qty3=form.vars.b_item_qty3
    
    disc_amt_per=form.vars.disc_amt_per
    
    if from_amt_qty=='' or from_amt_qty==None:
        from_amt_qty=0
    if to_amt_qty=='' or to_amt_qty==None:
        to_amt_qty=0
    if b_item_qty1=='' or b_item_qty1==None:
        b_item_qty1=0
    if b_item_qty2=='' or b_item_qty2==None:
        b_item_qty2=0
    if b_item_qty3=='' or b_item_qty3==None:
        b_item_qty3=0
    if disc_amt_per=='' or disc_amt_per==None:
        disc_amt_per=0
    
    
    dateFlag=True
    try:
        fromDt=datetime.datetime.strptime(str(from_date),"%Y-%m-%d" )
        toDt=datetime.datetime.strptime(str(to_date),"%Y-%m-%d" )                        
        if (fromDt > toDt):
            dateFlag=False            
            response.flash='To date need greater than From date'
    except:
        dateFlag=False
        response.flash='Required valid date'
    
    if dateFlag==False:
        form.errors.campaign_ref=''
    else:
        forItemFlag=True
        if for_any_item!='ANY':
            itemRows=db((db.sm_item.cid==c_id) & (db.sm_item.item_id==for_any_item)).select(db.sm_item.item_id,limitby=(0,1))
            if not itemRows:
                form.errors.for_any_item='invalid item'
                forItemFlag=False
        
        if forItemFlag==True:
            if int(from_amt_qty)<=0:
                forItemFlag=False
                form.errors.from_amt_qty='limit from need greater than 0'
                
            elif int(from_amt_qty)>int (to_amt_qty):
                forItemFlag=False
                form.errors.to_amt_qty='limit to need greater than limit from'
                
        
        if forItemFlag==False:
            pass
        else:
            bonusFlag=True
            if bonus_type=='Item':
                disc_amt_per=0
                
                if b_item_id1=='':
                    form.errors.b_item_id1='enter a value'
                    bonusFlag=False
                else:
                    itemRows=db((db.sm_item.cid==c_id) & (db.sm_item.item_id==b_item_id1)).select(db.sm_item.name,limitby=(0,1))
                    if not itemRows:
                        form.errors.b_item_id1='invalid item'
                        bonusFlag=False
                    else:
                        form.vars.b_item_name1=itemRows[0].name
                        
                        if int(b_item_qty1)<=0:
                            bonusFlag=False
                            form.errors.b_item_qty1='need greater than 0'
                        else:
                            if b_item_id2=='':
                                b_item_qty2=0     
                                b_item_id3=''                                
                                b_item_qty3=0
                            else:
                                itemRows2=db((db.sm_item.cid==c_id) & (db.sm_item.item_id==b_item_id2)).select(db.sm_item.name,limitby=(0,1))
                                if not itemRows2:
                                    form.errors.b_item_id2='invalid item'
                                    bonusFlag=False
                                else:
                                    form.vars.b_item_name2=itemRows2[0].name
                                    
                                    if int(b_item_qty2)<=0:
                                        bonusFlag=False
                                        form.errors.b_item_qty2='need greater than 0'
                                    else:
                                        if b_item_id3=='':                              
                                            b_item_qty3=0
                                        else:
                                            itemRows3=db((db.sm_item.cid==c_id) & (db.sm_item.item_id==b_item_id3)).select(db.sm_item.name,limitby=(0,1))
                                            if not itemRows3:
                                                form.errors.b_item_id3='invalid item'
                                                bonusFlag=False
                                            else:
                                                form.vars.b_item_name3=itemRows3[0].name
                                                
                                                if int(b_item_qty3)<=0:
                                                    bonusFlag=False
                                                    form.errors.b_item_qty3='need greater than 0'
            
            elif bonus_type=='DiscAmt' or bonus_type=='DiscPer':
                b_item_id1=''
                b_item_id2=''
                b_item_id3=''                
                b_item_qty1=0
                b_item_qty2=0
                b_item_qty3=0
                
                if int(disc_amt_per)<=0:
                    bonusFlag=False
                    form.errors.disc_amt_per='need greater than 0'
                    
            #---------------------
            if bonusFlag==False:
                pass
            else:
                #------- check duplicate
                existRows=db((db.sm_tpcp_rules.cid==c_id) & (db.sm_tpcp_rules.client_cat==client_cat) & (db.sm_tpcp_rules.from_date==from_date) & (db.sm_tpcp_rules.to_date==to_date) & (db.sm_tpcp_rules.for_any_item==for_any_item) & (db.sm_tpcp_rules.from_amt_qty==from_amt_qty)).select(db.sm_tpcp_rules.campaign_ref,limitby=(0,1))
                if existRows:
                    form.errors.campaign_ref=''
                    response.flash='already exist'
                else:
                    form.vars.campaign_ref=campaign_ref
                    form.vars.for_any_item=for_any_item
                    
                    form.vars.b_item_id1=b_item_id1
                    form.vars.b_item_id2=b_item_id2
                    form.vars.b_item_id3=b_item_id3
                    
                    form.vars.b_item_qty1=b_item_qty1
                    form.vars.b_item_qty2=b_item_qty2
                    form.vars.b_item_qty3=b_item_qty3
                    
                    form.vars.disc_amt_per=disc_amt_per

#---------------------------- ADD
def invoice_rules_add():
    c_id=session.cid
    if (session.user_type!='Admin'):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))    
    elif session.utility_settings!=1:
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
    
    response.title='Invoice Rules'
    
    #   ---------------------
    #db.sm_tpcp_rules.client_cat.requires=IS_IN_DB(db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')),db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id)
    db.sm_tpcp_rules.bonus_type.requires=IS_IN_SET(('Item','DiscAmt','DiscPer'))
    
    form =SQLFORM(db.sm_tpcp_rules,
                  fields=['campaign_ref','client_cat','from_date','to_date','for_any_item','from_amt_qty','to_amt_qty','bonus_type','b_item_id1','b_item_id2','b_item_id3','b_item_qty1','b_item_qty2','b_item_qty3','disc_amt_per','status'],
                  submit_button='Save'
                  )
    
    form.vars.cid=c_id
    form.vars.from_amt_qty=''
    form.vars.to_amt_qty=''
    form.vars.b_item_qty1=''  
    form.vars.b_item_qty2=''  
    form.vars.b_item_qty3=''  
    form.vars.disc_amt_per='' 
    if form.accepts(request.vars,session,onvalidation=invoice_rules_validation):
       response.flash = 'Submitted Successfully'
       
    #  ---------------filter-------
    btn_filter=request.vars.btn_filter
    btn_all=request.vars.btn_all
    reqPage=len(request.args)    
    if btn_filter:
        session.btn_filter_tpcp=btn_filter
        session.searchType_tpcp=str(request.vars.searchType).strip()
        session.searchValue_tpcp=str(request.vars.searchValue).strip().upper()
        reqPage=0
    elif btn_all:
        session.btn_filter_tpcp=None
        session.searchType_tpcp=None
        session.searchValue_tpcp=None
        reqPage=0
        
    #--------paging
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging   
    
    qset=db()
    qset=qset(db.sm_tpcp_rules.cid==c_id)
    if ((session.btn_filter_tpcp) and (session.searchType_tpcp=='Reference')):
        qset=qset(db.sm_tpcp_rules.campaign_ref==session.searchValue_tpcp)  
        
    elif ((session.btn_filter_tpcp) and (session.searchType_tpcp=='Category')):
        qset=qset(db.sm_tpcp_rules.client_cat==session.searchValue_tpcp)        
        
    elif ((session.btn_filter_tpcp) and (session.searchType_tpcp=='Status')):
        qset=qset(db.sm_tpcp_rules.status==session.searchValue_tpcp)      
        
    records=qset.select(db.sm_tpcp_rules.ALL,orderby=~db.sm_tpcp_rules.id,limitby=limitby)
    
    #------------------
    categoryRecords=db((db.sm_category_type.cid == c_id)&(db.sm_category_type.type_name=='CLIENT_CATEGORY')).select(db.sm_category_type.cat_type_id,orderby=db.sm_category_type.cat_type_id)
    
    return dict(form=form,records=records,categoryRecords=categoryRecords,page=page,items_per_page=items_per_page)


#---------------------------- EDIT VALIDATION

#---------------------------- EDIT
def invoice_rules_edit():
    c_id=session.cid
    if (session.user_type!='Admin'):
        session.flash='Access is Denied !'
        redirect (URL('default','home'))    
    elif session.utility_settings!=1:
        session.flash='Access is Denied !'
        redirect (URL('default','home'))
        
    #   --------------------- 
    response.title='Invoice Rules-Edit'
    
    page=request.args(0)
    rowID=request.args(1)
    
    record= db.sm_tpcp_rules(rowID) or redirect(URL('invoice_rules_add'))   
        
    form =SQLFORM(db.sm_tpcp_rules,
                  record=record,
                  deletable=True,
                  fields=['status'],
                  submit_button='Update'
                  )
    
    if form.accepts(request.vars, session):
        session.flash = 'Updated Successfully'
        redirect(URL('invoice_rules_add',args=[page]))
    
    records=db((db.sm_tpcp_rules.cid==c_id)&(db.sm_tpcp_rules.id==rowID)).select(db.sm_tpcp_rules.ALL,limitby=(0,1))
    if not records:
        session.flash = 'Invalid request'
        redirect(URL('invoice_rules_add',args=[page]))
    else:
        pass
    
    
    return dict(form=form,page=page,records=records,rowID=rowID)
    
    
