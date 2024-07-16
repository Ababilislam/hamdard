def cost_sub_category():
    if (session.cid == '' or session.cid == None):
        redirect (URL('default','index'))

    cat_id = str(request.args[0])
    cat_id = cat_id.replace("_", " ")

    response.title = 'Cost Sub Category'

    cid = session.cid
    user_id = session.user_id

    submit_btn = request.vars.submit
    
    if submit_btn:
        # selected_cat_type = request.vars.search_type
        # return selected_cat_type
        sub_cat_type = str(request.vars.sub_cat_type)
        
        if sub_cat_type != '':
            check_sub_cat_type = f"SELECT category_name, sub_category_name FROM cost_sub_category WHERE cid = '{cid}' AND category_id = '{cat_id}' AND sub_category_id = '{sub_cat_type}';"
            sub_cat_typeRows = db.executesql(check_sub_cat_type, as_dict=True)

            if len(sub_cat_typeRows) > 0:
                response.flash = 'Sub-Category already exists'
               
            else:
                get_category_name_sql = f"SELECT category_name FROM cost_category WHERE cid = '{cid}' AND category_id = '{cat_id}';"
                get_category_name = db.executesql(get_category_name_sql, as_dict=True)
                
                if len(get_category_name) != 0:
                    for i in range(len(get_category_name)):
                        get_data = get_category_name[i]
                        cat_name = get_data['category_name']

                insert_sub_cat_type = f"INSERT INTO cost_sub_category (cid, category_id, category_name, sub_category_id, sub_category_name, created_by) VALUES ('{cid}','{str(cat_id)}','{str(cat_name)}','{str(sub_cat_type)}','{str(sub_cat_type)}','{str(user_id)}');"
                db.executesql(insert_sub_cat_type)

                response.flash= 'Sub-Category Inserted Successfully'

    # get_category_sql = f"SELECT category_name FROM cost_category WHERE cid = '{cid}';"
    # categoryRows = db.executesql(get_category_sql, as_dict=True)

    get_sub_category_sql = f"SELECT * FROM cost_sub_category WHERE cid = '{cid}' AND category_id = '{cat_id}' ORDER BY id;"
    sub_categoryRows = db.executesql(get_sub_category_sql, as_dict=True)

    return dict(cat_type = cat_id, sub_categoryRows = sub_categoryRows)



def sub_category_edit():
    if (session.cid == '' or session.cid == None):
        redirect (URL('default','index'))

    cid = session.cid

    submit = request.vars.submit

    cat_id = request.args[0]
    cat_id = cat_id.replace("_", " ")
    sub_cat_id = request.args[1]
    sub_cat_id = sub_cat_id.replace("_", " ")

    if submit == 'Update':
        update_sub_cat_type = str(request.vars.updated_sub_cat_type).strip().replace('None', '')

        if update_sub_cat_type != '' and update_sub_cat_type != None:
            update_sql = f"UPDATE cost_sub_category SET sub_category_id = '{str(update_sub_cat_type)}', sub_category_name = '{str(update_sub_cat_type)}' WHERE cid = '{cid}' AND category_id = '{str(cat_id)}' AND sub_category_id = '{str(sub_cat_id)}';"
            db.executesql(update_sql)

            session.flash = 'Updated Successfully'

            redirect (URL('branch_cost_sub_category','cost_sub_category',args=[cat_id]))

    return dict(cat_id = cat_id, sub_cat_id = sub_cat_id)



def sub_category_delete():
    if (session.cid == '' or session.cid == None):
        redirect (URL('default','index'))

    cid = session.cid

    if len(request.args) > 0:
        cat_id = request.args[0]
        cat_id = cat_id.replace("_", " ")
        sub_cat_id = request.args[1]
        sub_cat_id = sub_cat_id.replace("_", " ")

        delete_sql = f"DELETE FROM cost_sub_category WHERE cid = '{cid}' AND category_id = '{str(cat_id)}' AND sub_category_id = '{str(sub_cat_id)}';"
        db.executesql(delete_sql)

        session.flash = 'Deleted Successfully'
    
    redirect (URL('branch_cost_sub_category','cost_sub_category',args=[cat_id]))
