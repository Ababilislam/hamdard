                   #### ADD RX BRAND  ######

def seen_rx_brand():

    response.title='Seen RX Band'
    submit=request.vars.submit
    brand_Name=str(request.vars.brand_name).strip()

    btn_filter=request.vars.btn_filter
    btn_all=request.vars.btn_all


    c_id=session.cid
    userRows=''
    if submit==' ADD ':
        brand_Name=str(request.vars.brand_name).strip()
       
        if brand_Name!='':
            check_userid_sql = "select id, brand_name from seen_rx_brand where brand_name='"+str(brand_Name)+"';"
            checkuserRows = db.executesql(check_userid_sql, as_dict=True)
            
            if len(checkuserRows) > 0:
                response.flash = 'Brand Name already exists'
                userRows_sql = "select id, brand_name from seen_rx_brand order by brand_name;"
                userRows = db.executesql(userRows_sql, as_dict=True)
                
            else:
                insertOperator_sql = "INSERT INTO seen_rx_brand (`cid`, `brand_name`) VALUES ('"+str(c_id)+"','"+str(brand_Name)+"')"          
                insertOperator = db.executesql(insertOperator_sql)
                response.flash= 'Brand Name Insert Successfully'
    

    searchValue_BrandName=str(request.vars.searchValue_BrandName).strip().upper()

    if searchValue_BrandName!='' and btn_filter=='Filter':
        session.searchValue_BrandName=searchValue_BrandName
        userRows_sql = "select id,brand_name from seen_rx_brand where brand_name='"+str(searchValue_BrandName)+"' order by brand_name;"
        userRows = db.executesql(userRows_sql, as_dict=True)

    else:
        # return 'hgjhjjhkh'
        session.searchValue_BrandName=''
        userRows_sql = "select id,brand_name from seen_rx_brand order by brand_name;"
        userRows = db.executesql(userRows_sql, as_dict=True)


    return dict(userRows=userRows)



def seen_rx_brand_delete():

    response.title='Seen RX Band'
    record_id = request.args(0)
    # return record_id
   
    # return record_id
    delete_sql = "delete from seen_rx_brand where id = '"+record_id+"';"
    
    records = db.executesql(delete_sql)
    session.flash = 'Deleted Successfully'
    redirect (URL('seen_rx_brand','seen_rx_brand'))






                  #### SHOW SEEN RX BRAND LIST  ######

         
def rx_band_list():
    retStr = ''

    userRows_sql = "select brand_name from seen_rx_brand order by brand_name;"
    userRows = db.executesql(userRows_sql, as_dict=True)
    for i in range(len(userRows)):
        records_ov_dict=userRows[i]   
        # user_id=str(records_ov_dict["user_id"])      
        brand_Name=str(records_ov_dict["brand_name"])   
        if retStr == '':
            retStr = brand_Name
        else:
            retStr += ',' +brand_Name
    
    return retStr


#                     #### BRAND LIST DOWNLOAD ######

def brand_list_Download():
    btn_filter_e = request.vars.btn_filter_e
    btn_all = request.vars.btn_all
   

    # userid=str(request.vars.user_id).strip().upper()
    brandName=str(request.vars.brand_name).strip()
    # return brand_Name
    if session.brand_name!='':
        record = "select  brand_name from seen_rx_brand where brand_name='"+str(session.brand_name)+"';"
        # return record
        records = db.executesql(record, as_dict=True)
    else:
        record = "select brand_name from seen_rx_brand order by brand_name;"
        records = db.executesql(record, as_dict=True)


    myString = 'Brand Name List\n\n'
    myString += 'brand_name\n'
    total=0
    attTime = ''
    totalCount = 0
    for i in range(len(records)):
        recordsStr = records[i]
        # user_id = str(recordsStr['user_id'])
        brand_Name = str(recordsStr['brand_name'])

        
        myString += str(brand_Name) + ',\n'

    # Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_Brand_List.csv'
    return str(myString)


def delete():

    btn_delete=request.vars.btn_delete
    
    if btn_delete:
        record_id=request.args[1]
        # delete_sql = db((db.sm_leave_type.id == record_id)).delete()
        delete_sql = "delete from seen_rx_brand where brand_name = record_id;"
        records = db.executesql(delete_sql, as_dict=True)
        return records
        response.flash = 'Deleted Successfully'

    return dict(records=records)
