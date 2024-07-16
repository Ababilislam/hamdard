def cost_category():
    if (session.cid == '' or session.cid == None):
        redirect (URL('default','index'))

    response.title = 'Cost Category'

    cid = session.cid
    user_id = session.user_id

    submit = request.vars.submit
    
    if submit:
        cat_type = request.vars.cat_name

        if cat_type == '' or cat_type == None or cat_type == 'None':
            response.flash = 'Category Required!'

        else:
            check_category_sql = f"SELECT * FROM cost_category WHERE cid = '{cid}' AND category_name = '{str(cat_type)}';"
            check_category = db.executesql(check_category_sql, as_dict=True)

            if len(check_category) > 0:
                response.flash = 'Category already exists!'
                
            else:
                insert_category_sql = f"INSERT INTO cost_category (cid, category_id, category_name, created_by) VALUES ('{cid}','{str(cat_type)}','{str(cat_type)}','{str(user_id)}');"      
                db.executesql(insert_category_sql)
                
                response.flash= 'Successfully saved!'
                redirect(URL('branch_cost_category','cost_category'))
    
    get_category_sql = f"SELECT * FROM cost_category WHERE cid = '{cid}';"
    categoryRows = db.executesql(get_category_sql, as_dict=True)

    return dict(categoryRows = categoryRows)



def category_delete():
    if (session.cid == '' or session.cid == None):
        redirect (URL('default','index'))

    cid = session.cid

    if len(request.args) > 0:
        cat_id = request.args[0]
        cat_id = cat_id.replace("_", " ")

        delete_sql = f"DELETE FROM cost_category WHERE cid = '{cid}' AND category_id = '{str(cat_id)}';"
        db.executesql(delete_sql)

        session.flash = 'Deleted Successfully'
        redirect (URL('branch_cost_category','cost_category'))

