def active_market_list():  
    response.title = 'Active Market List'

    c_id = session.cid
    user_id = session.user_id

    submit = request.vars.btn_submit
    reqPage = len(request.args)

    rep_status = ''
   
    if submit:
        try:
            territory_id = str(request.vars.territory_id).split('|')[0]
            name = str(request.vars.territory_id).split('|')[1]
        except:
            territory_id = ''
            # rep_id = str(request.vars.rep_id)

        if territory_id != '':
            check_ff_sql = f"SELECT market_id, market_name FROM active_market_list WHERE cid = '{c_id}' AND market_id = '{str(territory_id)}';"
            check_ff = db.executesql(check_ff_sql, as_dict=True)

            if len(check_ff) > 0:
                response.flash = 'Already exists'
           
            else:
                # check_rep_status_sql = f"SELECT status FROM sm_rep WHERE cid = '{c_id}' AND rep_id = '{str(rep_id)}';"
                # check_rep_status = db.executesql(check_rep_status_sql, as_dict=True)

                # for i in range(len(check_rep_status)):
                #     data = check_rep_status[i]
                #     rep_status = str(data['status']).strip().upper()

                # if rep_status == 'INACTIVE':
                #     response.flash= 'Inactive Representative'
                
                # else:
                insert_ff_sql = f"INSERT INTO active_market_list (cid, market_id, market_name, created_by) VALUES ('{str(c_id)}','{str(territory_id)}','{str(name)}','{str(user_id)}')"      
                db.executesql(insert_ff_sql)

                response.flash= 'Inserted Successfully'
                
        else:
            response.flash= 'Invalid Market'

    # --------paging
    session.items_per_page = 20

    if reqPage:
        page = int(request.args[0])
    else:
        page = 0

    items_per_page = session.items_per_page
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # --------end paging
    pagination_sql= f"SELECT market_id, market_name FROM active_market_list WHERE cid = '{c_id}' ORDER BY id desc limit %d, %d;" % limitby 
    pagination_sql_data=db.executesql(pagination_sql, as_dict=True)
    
    active_list_sql = f"SELECT market_id, market_name FROM active_market_list WHERE cid = '{c_id}'"
    active_list = db.executesql(active_list_sql, as_dict=True)
    totals=len(active_list)
    
    return dict(pagination_sql_data=pagination_sql_data, page=page, items_per_page=items_per_page,totals=totals)



def record_delete():
    c_id = session.cid
    market_id = request.args(0)
    
    btn_delete = request.vars.btn_delete
    
    # if btn_delete:
    delete_sql = f"DELETE FROM active_market_list WHERE cid = '{c_id}' AND market_id = '{str(market_id)}';"
    db.executesql(delete_sql)

    session.flash = 'Deleted Successfully'

    redirect (URL('active_market_list', 'active_market_list'))



# AUTO-COMPLETE
def territory_list():
    
    # c_id = session.cid
    cid='HAMDARD'

    reiStr = ''

    repRows_sql = "SELECT level3, level3_name FROM sm_level WHERE cid ='HAMDARD' AND is_leaf = '1';"
    
    repRows = db.executesql(repRows_sql, as_dict=True)

    for i in range(len(repRows)):
        records_ov_dict = repRows[i]   
        rep_id = str(records_ov_dict["level3"])      
        name = str(records_ov_dict["level3_name"])   

        if reiStr == '':
            reiStr = rep_id +'|'+ name
        else:
            reiStr += ',' + rep_id +'|'+ name
    
    return reiStr


def batch_upload():
    response.title = 'Active Market List Batch Upload'
    cid = session.cid
    user_id = session.user_id
    btn_upload=request.vars.btn_upload
    count_inserted=0
    count_error=0
    error_str=''
    total_row=0
            
    if btn_upload=='Upload':
        excel_data=str(request.vars.excel_data)
        inserted_count=0
        error_count=0
        
        row_list=excel_data.split( '\n')
        total_row=len(row_list)
        
        ff_list_exist=[]   
        ff_list_excel=[]
                
        ins_list=[]
        ins_dict={}

        # ----------------------
        for i in range(total_row):
            if i>=500:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==1:
                    ffExcel=str(coloum_list[0]).strip().upper()
                    
                    if ffExcel!='':
                        if ffExcel not in ff_list_excel:ff_list_excel
                        ff_list_excel.append(ffExcel)       

        for i in range(total_row):
            if i>=500:
                break
            else:
                row_data=row_list[i]
                coloum_list=row_data.split( '\t')            
            
            if len(coloum_list)!=1:
                error_data=row_data+'(1 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
            else:
                territory_id = str(coloum_list[0]).strip().upper()
                territory_name = ''
                # territory_name = str(coloum_list[1]).strip().upper()
                              
                    
                if territory_id==''or territory_id == 'NONE' or territory_id=='' or territory_id== 'NONE' :
                    error_data=row_data+'(Required all value)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue                    
                
                else:
                    existCheckRows= " select * FROM active_market_list WHERE cid='"+str(cid)+"' and market_id = '"+str(territory_id)+"' LIMIT 0,1"
                    existCheck = db.executesql(existCheckRows)

                    if len(existCheck) > 0:
                        error_data=row_data+'(Duplicate Active Market )\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:
                        check_ff_sql = f"SELECT level3, level3_name FROM sm_level WHERE cid = '{cid}' AND level3 = '{str(territory_id)}' group by level3 limit 1;"
                        check_ff = db.executesql(check_ff_sql, as_dict=True)
                        if len(check_ff) == 0:
                            error_data=row_data+'(Invalid Market)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:
                            for i in range(len(check_ff)):
                                data = check_ff[i]
                                territory_name = str(data['level3_name']).strip().upper()
                            try:
                                insert_sql =  f"INSERT INTO active_market_list (cid, market_id, market_name, created_by) VALUES ('{str(cid)}','{str(territory_id)}','{str(territory_name)}','{str(user_id)}')"      
                                db.executesql(insert_sql)
                                count_inserted+=1
                            except Exception as e:
                                error_str = 'Please do not insert special charachter.'
                                
        if error_str=='':
            error_str='No error'

    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)