#cid<url>httppass<url>synccode<url>repid<url>client_id<url>delivery_date<url>depot_id<url>area_id<url>rd-rditem_id-qty_item_id-qty_

#//http://localhost/mreport_003/syncReturn/return_product/Fast<url>airnetMreport2009<url>-1270296549<url>101<url>FC02104<url>FPT2-50fd-fd3rd-rdFB-35fd-fd5rd-rd<url>003<url>FC-NGJ1
#//http://localhost/mreport_003/syncReturn/return_product/2540343044844939345044744133452343495430438447443434449410447434445444447449383381381390393450447441395378382383388381383390387386385390393450447441395382381382393450447441395403400381383382381385393450447441395403413417383378386381435433378435433384447433378447433403399378384386435433378435433386447433378447433393450447441395381381384393450447441395403400378411404407382


def en_dec():
    mystr1='ACME<url>01<url>123<url>12345'
    mystr1=get_encript(mystr1)
#    3739840041040239345044744139543043844743452343443434449410447434445444447449383381381390393450447441395382385381387383385385381386382393450447441395382381382393450447441395401390390381381382393450447441395383381382382378382382378382387393450447441395400393450447441395383383393450447441395rd-rdG-1_H3-1_
    return mystr1
def orderSubmit():
#    http://127.0.0.1:8000/mreporting/sync_order/orderSubmit/5539840041040239345044744139543043844744343444941044743443452343445444447449383381381390393450447441395382385381387383385385381386382393450447441395382381382393450447441395401390390381381382393450447441395383381382382378382382378382387393450447441395381382393450447441395381381382393450447441395rd-rdI1-1_I2-1_
    
    my_str = request.args(0)
    separator='rd-rd'
    
    if (my_str != ""):
        totalfields=my_str.count(separator)
       
                    
#//without encryption
        my_str=get_decript(my_str)
        
#        return my_str
    
    if my_str != "":
        separator_url='<url>'
        cid=''
        http_pass=''
        sync_code=''
        rep_id=''
        client_id=''
        delivery_date=''
        depot_id=''
        area_id=''
        item_qty_all=''
        order_date = ''
        
        url_list_url=my_str.split(separator_url,my_str.count(separator_url))
        cid=url_list_url[0].upper()
        http_pass=url_list_url[1]
        sync_code=url_list_url[2]
        rep_id=url_list_url[3].upper()
        client_id=url_list_url[4].upper()
        
        item_qty_all=url_list_url[5]
        
        depot_id=url_list_url[6]
        area_id=url_list_url[7].upper()
        
       
        return_date = request.now
        
#        return (cid+'  '+http_pass+'  '+sync_code+'  '+rep_id+'  '+client_id+'  '+delivery_date+'  '+depot_id+'  '+area_id+'  '+item_qty_all)
    
        
        
#        order_date = date_fixed
        com_check=db((db.sm_company.cid==str(cid)) & (db.sm_company.http_pass==str(http_pass))).select()
        if com_check:
            rep_check=db((db.sm_rep.cid==cid) & (db.sm_rep.rep_id==rep_id)).select()
            if rep_check:
                query_sl=db((db.sm_depot.cid==str(cid)) & (db.sm_depot.depot_id==depot_id)).select()
                sl=0
                for row_sl in query_sl:
                    sl=row_sl.return_sl
                sl=int(sl)+1
                
                  
#                return sl
                check_sl=db((db.sm_return.cid==cid) & (db.sm_return.depot_id==depot_id) & (db.sm_return.sl==sl)).select()
                sl_flag=True
                if(check_sl):
                    pass
                else:
                    flag=False
#                return sl_flag
#                ------------Process product list--------------

                if sl_flag==True:
                    product=''
#                    return str_2
                    separator_item='_'
                    
                    prodct_single=item_qty_all.split(separator_item,item_qty_all.count(separator_item))
                    total_product=item_qty_all.count(separator_item)
#                    return total_product
                    i=0
#                    return total_product
#                    for separator_item in range(len(str_2)):
                    n=''
                    while i<total_product:
                        separator_qty='-'
                        prodct_qty=prodct_single[i].split(separator_qty,prodct_single[i].count(separator_qty))
                        prodct_id=prodct_qty[0].upper()
                        product_qty=prodct_qty[1]
                        i=i+1
#                    return prodct_id

                        check_return=db((db.sm_return.cid==cid) & (db.sm_return.depot_id==depot_id)& (db.sm_return.sl==sl)& (db.sm_return.item_id==prodct_id)).select()
                        
                        if check_order:
                            pass
                        else:
                            query_price=db((db.sm_item.cid==cid) & (db.sm_item.item_id==prodct_id)).select(db.sm_item.ALL)
                            price=0
                            for row_price in query_price:
                                price=row_price.price
                                name=row_price.name
                                catagory=row_price.category_id
#                                return price
                                return_insert=db.sm_return.insert(cid=cid,depot_id=depot_id,sl=int(sl),client_id=client_id,rep_id=rep_id,return_date=return_date,area_id=area_id,item_id=prodct_id,quantity=product_qty,price=price,item_name=name,catagory_id=catagory)
#                                return order_insert
                            update_depot=db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id==depot_id)).update(return_sl=int(sl))



                    success="success"+"<fd>"+"SL No: "+str(sl)
                    success=get_encript(success)
                    return "START"+success+"END"
                
                else:
                    fail="Failed"
                    fail = get_encript(fail)
                    return START+fail+END #Invalid sl
            else:
                fail="Failed"
                fail = get_encript(fail)
                return START+fail+END #Invalid rep 
        else:
            fail="Failed"
            fail = get_encript(fail)
            return START+fail+END #Invalid company 
                
            
               
                

