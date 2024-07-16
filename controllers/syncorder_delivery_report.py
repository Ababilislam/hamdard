#cid<url>httppass<url>synccode<url>repid<url>client_id<url>item_id<>datefrom<url>dateto
# //client-All
# http://127.0.0.1:8000/mreporting/syncorder_delivery_report/order_report/1239840041040234523434393450447441395430438447443434449410447434445444447449383381381390393450447441395378384388382390384384381390385393450447441395382381382393450447441395398441441393450447441395381382393450447441395381382393450447441395383381382382378382382378381382393450447441395383381382382378382382378384381

#
#  //Item-All
# //http://localhost/mreport_003/syncorder_delivery_report/order_report/fast<url>airnetMreport2009<url>390581693<url>101<url>FC00060<url>All<url>2010-07-29<url>2010-10-29
# //http://localhost/mreport_003/syncorder_delivery_report/order_report/4343543044844939345044744139543043844744343443452343449410447434445444447449383381381390393450447441395384390381386389382387390384393450447441395382381382393450447441395403400381381381387381393450447441395398441441393450447441395383381382381378381388378383390393450447441395383381382381378382381378383390
#
# //client-All,item-All
# //http://localhost/mreport_003/syncorder_delivery_report/order_report/fast<url>airnetMreport2009<url>390581693<url>101<url>All<url>All<url>2010-07-29<url>2010-10-29
# //http://localhost/mreport_003/syncorder_delivery_report/order_report/9143543044844939345044744139543043844744343444941044743444544444744938338138139039345044744133452343495384390381386389382387390384393450447441395382381382393450447441395398441441393450447441395398441441393450447441395383381382381378381388378383390393450447441395383381382381378382381378383390
#
# //client-notAll,item-notAll
# //http://localhost/mreport_003/syncorder_delivery_report/order_report/fast<url>airnetMreport2009<url>390581693<url>101<url>FC00060<url>FPT2-50<url>2010-07-29<url>2010-10-29
# //http://localhost/mreport_003/syncorder_delivery_report/order_report/0443543452343430448449393450447441395430438447443434449410447434445444447449383381381390393450447441395384390381386389382387390384393450447441395382381382393450447441395403400381381381387381393450447441395403413417383378386381393450447441395383381382381378381388378383390393450447441395383381382381378382381378383390

def en_dec():
#    mystr1='ACME<url>airnetMreport2009<url>-371933094<url>101<url>00101<url>All<url>01<url>2011-11-01<url>2011-11-30'
    mystr1='ACME<url>airnetMreport2009<url>-371933094<url>101<url>All<url>01<url>01<url>2011-11-01<url>2011-11-30'
    mystr1=get_encript(mystr1)
#    3739840041040239345044744139543043844743452343443434449410447434445444447449383381381390393450447441395382385381387383385385381386382393450447441395382381382393450447441395401390390381381382393450447441395383381382382378382382378382387393450447441395400393450447441395383383393450447441395rd-rdG-1_H3-1_
    return mystr1


#//order report
def order_report():  
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
        
        
        url_list_url=my_str.split(separator_url,my_str.count(separator_url))
        cid=url_list_url[0].upper()
        http_pass=url_list_url[1]
        sync_code=url_list_url[2]
        rep_id=url_list_url[3].upper()
        client_id=url_list_url[4].upper()
        item_id=url_list_url[5].upper()
        date=url_list_url[6]
        date1=url_list_url[7]
        
        
        sync_result=''
        check_client_from_order=0
        
#        return (cid+'  '+http_pass+'  '+sync_code+'  '+rep_id+'  '+client_id+'  '+delivery_date+'  '+depot_id+'  '+area_id+'  '+item_qty_all)
    
        
        
#        order_date = date_fixed
        com_check=db((db.sm_company.cid==str(cid)) & (db.sm_company.http_pass==str(http_pass))).select()
        if com_check:
            rep_check=db((db.sm_rep.cid==cid) & (db.sm_rep.rep_id==rep_id)).select()
            if rep_check:
                flag_report=1;
                
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
   
   
    report=""      
#    Client All=========================
#    return client_id
    if ((flag_report==1) and (client_id=='ALL') and (item_id!='ALL')) :
#        return 'nn'
        check_item_inorder=db((db.sm_order.cid==cid) & (db.sm_order.rep_id==rep_id) & (db.sm_order.item_id==item_id)  ).select(((db.sm_order.price)*(db.sm_order.quantity)).sum())
        
        
        report="ID: "+str(rep_id)+" From: "+str(date)+" To: "+str(date1)[:10]+"\n"+"Item_id: "+str(item_id)+"  "+"Client: "+str(client_id)+"\n"+  "------------------" + "\n"
        for row in check_item_inorder :
            report=report=report+"TK: "+str(row[((db.sm_order.price * db.sm_order.quantity)).sum()])
        
#        report=get_encript(report)
        return report
        
    
    if((flag_report==1) and (client_id!='ALL') and (item_id=='ALL')) :
        check_item_inorder=db((db.sm_order.cid==cid) & (db.sm_order.rep_id==rep_id) & (db.sm_order.client_id==client_id)  ).select(((db.sm_order.price)*(db.sm_order.quantity)).sum(),db.sm_order.item_id,db.sm_order.item_name,orderby=db.sm_order.item_id,groupby=db.sm_order.item_id)
        
        report="ID: "+str(rep_id)+" From: "+str(date)+" To: "+str(date1)[:10]+"\n"+"Item_id: "+str(item_id)+"  "+"Client: "+str(client_id)+"\n"+  "------------------" + "\n"
        for row in check_item_inorder :
            item_id=row.sm_order.item_id
            report=report=report+str(item_id)+ "TK: "+str(row[((db.sm_order.price * db.sm_order.quantity)).sum()])
        
        report=get_encript(report)
        return report

    
    if((flag_report==1) and (item_id=='ALL') and (client_id=='ALL')) :
        check_item_inorder=db((db.sm_order.cid==cid) & (db.sm_order.rep_id==rep_id)).select(((db.sm_order.price)*(db.sm_order.quantity)).sum(),db.sm_order.item_id,db.sm_order.item_name,orderby=db.sm_order.item_id,groupby=db.sm_order.item_id)
        
        report="ID: "+str(rep_id)+" From: "+str(date)+" To: "+str(date1)[:10]+"\n"+"Item_id: "+str(item_id)+"  "+"Client: "+str(client_id)+"\n"+  "------------------" + "\n"
        for row in check_item_inorder :
            item_id=row.sm_order.item_id
            report=report=report+str(item_id)+ "TK: "+str(row[((db.sm_order.price * db.sm_order.quantity)).sum()])
        
        report=get_encript(report)
        return report

    if((flag_report==1) and (item_id!='ALL') and (client_id!='ALL')) :
        check_item_inorder=db((db.sm_order.cid==cid) & (db.sm_order.rep_id==rep_id) & (db.sm_order.item_id==item_id) & (db.sm_order.client_id==client_id)).select(((db.sm_order.price)*(db.sm_order.quantity)).sum(),db.sm_order.item_id,db.sm_order.item_name,orderby=db.sm_order.item_id,groupby=db.sm_order.item_id)
        
        report="ID: "+str(rep_id)+" From: "+str(date)+" To: "+str(date1)[:10]+"\n"+"Item_id: "+str(item_id)+"  "+"Client: "+str(client_id)+"\n"+  "------------------" + "\n"
        for row in check_item_inorder :
            report=report=report+str(item_id)+ "TK: "+str(row[((db.sm_order.price * db.sm_order.quantity)).sum()])
        
        report=get_encript(report)
        return report
        
 
