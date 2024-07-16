import urllib

#sms_order_invoice_submit
#sms_order_submit
#sms_invoice_submit
#sms_order_invoice_submit_with_date
#sms_order_submit_with_date
#sms_invoice_submit_with_date

#=========================================sms with date================================
#Only Delevery is ok

#sms_invoice_submit_with_date_iq
#CID.D.10.CLIENTID.ITEM,QTY.ITEM,QTY.ITEM,QTY
#http://127.0.0.1:8000/sixseasons/sms_order_invoice/sms_order_invoice_submit?password=Compaq510DuoDuo&mob=8801711274122&cid=acme&msg=acme.O.001.10013,10.10026,15.10045,25


#function sms_invoice_submit_with_date_iqf
#CID.D.10.CLIENTID.ITEM,QTY,FreeQty.ITEM,QTY,FreeQty.ITEM,QTY,FreeQty
#http://127.0.0.1:8000/sixseasons/sms_order_invoice/sms_order_invoice_submit_with_date?password=Compaq510DuoDuo&mob=8801777776186&cid=SIXSEASONS&msg=SIXSEASONS.D.24.SHAMPUR01.INMS62G,10,2.INMSFPK,15,0.INMSPPK,25,3

#function sms_invoice_submit_with_date_iqfplus
#CID.D.10.CLIENTID.ITEM,QTY+FreeQty.ITEM,QTY.ITEM,QTY+FreeQty
#http://127.0.0.1:8000/sixseasons/sms_order_invoice/sms_order_invoice_submit_with_date?password=Compaq510DuoDuo&mob=8801777776186&cid=SIXSEASONS&msg=SIXSEASONS.D.24.SHAMPUR01.INMS62G,10+2.INMSFPK,15.INMSPPK,25+3

#CID.D.10.CLIENTID.ITEM,QTY+FreeQty.ITEM,QTY.ITEM,QTY+FreeQty
#IBRA.D.10.10101.A1,10.A2,24.B1,20.B2,10

#http://e.businesssolutionapps.com/mrepconfidence/sms_order_invoice/sms_order_invoice_submit_with_date?password=Compaq510DuoDuo&mob=8801705406601&cid=IBRA&msg=IBRA.D.10.10101.A1,10.A2,24.B1,20.B2,10
def sms_order_invoice_submit_with_date():
        pass_get=request.vars.password
        mobile=request.vars.mob
        cid=request.vars.cid
        
        msgStr=request.vars.msg
        
        #for receive server site to decode
        my_str=urllib.unquote(msgStr.decode('utf8'))
        
        
        #for request site
#        my_str=urllib.quote_plus(urllib.quote_plus(msgStr.encode('utf8')))        
#        return my_str
        
        msg_start='START'
        
#    try:
        if (pass_get!='Compaq510DuoDuo'):
            return str(msg_start)+"Invalid sms"
        sms_type=''
        if my_str != "":
            separator_url='.'
            
            if (my_str.count(separator_url)>1):
                url_list_url=my_str.split(separator_url)
                sms_type=url_list_url[1].upper()
            else:
                return str(msg_start)+'SMS type mismatch'
        
        # Hit related function based on sms type     
#        if sms_type=='O':
#            result=sms_order_submit_with_date(pass_get,mobile,cid,my_str)
#            return result
#        el
        
        if sms_type=='D':            
            result=sms_invoice_submit_with_date_iqfplus(pass_get,mobile,cid,my_str) #change the invoice function according to format
            return result
        
        elif sms_type=='L':            
            result=sms_lifting_submit_with_date_iqfplus(pass_get,mobile,cid,my_str) #change the invoice function according to format
            return result
        
        else:           
            return str(msg_start)+'Error in SMS format. Please contact with your company admin for correct format.'
#    except:
#        return str(msg_start)+'Error in SMS format.'    



#=== (Billal-sixseasons1 ok) Item,Qty
#def sms_invoice_submit_with_date_iq(pass_get,mobile,cid,my_str):
#    START='START'
#    END='END'
#    error_flag=1
#    error_msg=''
#    msg_start='START'
#    try:  
#        pass_get=pass_get
#        my_str=my_str.replace(" ", "")
#        
#        if (pass_get!='Compaq510DuoDuo'):
#            return "STARTInvalid sms"
#        
#        if my_str != "":
#            separator_url='.'
#            totalfields=my_str.count(separator_url)
#            
#            rep_id=''
#            sms_type=''
#            delivery_date=''
#            client_id=''
#            item_qty_all=''
#            order_date = ''
#            data_for_inbox=''
#            order_date=str(date_fixed)[0:10]
#            
#            url_list_url=my_str.split(separator_url,my_str.count(separator_url))
#            
#            sms_type=url_list_url[1].upper().strip()
#            del_date=url_list_url[2].upper().strip()
#            inbox_date=del_date
#            
#            current_date=str(date_fixed)[0:10]
#            current_day=str(current_date)[8:10]
#            set_date=current_day
#            
#            if(del_date.isdigit()):
#                pass
#            else:
#                error_msg= "Error: Invalid date. "
#            
#            #If date greater than current date , date witt treat as date of past month
#            if(int(del_date)==int(current_day)):   
#                set_date=current_date
#                
#            elif (int(del_date)<int(current_day)):            
#                set_date=str(current_date)[0:8]+del_date
#
#            elif(int(del_date)>int(current_day)):                
#                current_month=str(current_date)[5:7]
#                
#                if int(current_month)>1:
#                    current_month=int(current_month)-1
#                    set_date=str(current_date)[0:5]+str(current_month)+"-"+str(del_date)
#                else:
#                    del_year=str(current_date)[0:4]
#                    del_year_past=int(del_year)-1
#                    set_date=str(del_year_past)+'-'+'12'+"-"+str(del_date)
#                    
#            delivery_date=set_date
#            
#            date_flag=False
#            
#            list_date=delivery_date.split("-",delivery_date.count("-"))
#            day_y=list_date[0].strip()
#            day_m=list_date[1].strip()
#            day_d=list_date[2].strip()
#            
#            day_m=int(day_m)
#            day_d=int(day_d)
#                        
#            #Set Valid date for month
#            if ((day_m==1) or (day_m==3) or (day_m==5) or (day_m==7) or (day_m==8) or (day_m==10) or(day_m==12)):
#                if ((day_d > 0) and (day_d<32)):
#                    date_flag=True
#                
#            if ((day_m==4) or (day_m==6) or (day_m==9) or (day_m==11)):
#                if ((day_d > 0) and (day_d<31)):
#                    date_flag=True
#                
#            if ((day_m==2)):
#                if ((day_d > 0) and (day_d<29)):
#                    date_flag=True
#            
#            if (date_flag==False):
#                error_msg= "Error: Invalid date."
#            
#            ym_date=str(delivery_date)[0:7]+'-01'
#            client_id=url_list_url[3].upper().strip()
#            mobile_no=str(mobile).upper().strip()
#            cid=str(cid).upper()
#            
#            data_for_inbox=str(sms_type)+'.'+str(inbox_date)+'.'+str(client_id)
#            
#            #=========================get rep id========================
#            
#            rep_name=''
#            rec_rep=db((db.sm_rep.cid==cid) & (db.sm_rep.mobile_no==mobile_no) & (db.sm_rep.status=='ACTIVE') & (db.sm_rep.sms=='Yes')).select(db.sm_rep.rep_id,db.sm_rep.name,limitby=(0,1))
#            if rec_rep:
#                rep_id=rec_rep[0].rep_id
#                rep_name=rec_rep[0].name
#                
#            if (rep_id==""):
#                error_msg= "Field Force Authorization Error."
#
#            #===========================================================            
#            #Get all item string            
#            item_qty_all=''
#            j=4
#            while j<totalfields+1:
#                if item_qty_all=='':
#                    item_qty_all=str(url_list_url[j]).strip()
#                    j=j+1
#                else:
#                    item_qty_all=str(item_qty_all)+'.'+str(url_list_url[j]).strip()
#                    j=j+1
#            
#            item_qty_all=item_qty_all.upper()
#            #Set data for inbox
#            data_for_inbox=str(data_for_inbox)+'.'+item_qty_all
#            
#            #    =======================check format and duplicate=================
#            separator_item='.'
#            prodct_single=item_qty_all.split(separator_item,item_qty_all.count(separator_item))
#            total_product=item_qty_all.count(separator_item)
#            i=0
#            itemList=[]
#
#            while i<total_product+1:
#                item_id=str(prodct_single[i]).strip()
#                separator_qty=','
#                item_id=''
#                item_qty=0
#                item_qty=prodct_single[i].split(separator_qty,prodct_single[i].count(separator_qty))
#                total_field=prodct_single[i].count(separator_qty)
#                qty=''
#                
#                if total_field==1:
#                    item_id=item_qty[0].strip().upper()
#                    qty=item_qty[1]
#                    if qty.isdigit():
#                        pass
#                    else:
#                        error_msg= "Error: Invalid qty for:"+str(item_id)
#                        break
#                    
#                else:
#                    error_msg= "Error: Qty must for item:"+str(item_id)
#                    break
#
#                if ((qty=="") or (qty=='0')):
#                    error_msg= "Error in Qty:"+str(item_id)
#                    break
#
#                if item_id in itemList:
#                    
#                    error_msg= "Format error or Duplicate Item:"+str(item_id)
#                    break
#
#                else:
#                    itemList.append(item_id)
#                i=i+1
#
#            #Create list of item from sm_company_settings table
#            item_table_list=[]
#            item_list_table=''
#            records_company_item=db(db.sm_company_settings.cid==cid).select(db.sm_company_settings.item_list,limitby=(0,1))
#            if records_company_item:
#                item_list_table=records_company_item[0].item_list
#                
#            item_table_single=item_list_table.split(',',item_list_table.count(','))
#            total_item_table=item_list_table.count(',')
#            
#            x=0
#            while x<total_item_table+1:
#                item=item_table_single[x]
#                item_table_list.append(item)
#                x=x+1
#            
#            #    =========================Check Item validation===============        
#            i=0
#            for i in range(len(itemList)):
#                item_id=itemList[i]
#                if item_id in item_table_list:
#                    pass
#                else:
#                    error_msg="Error: Invalid item:"+str(item_id)                 
#                i=i+1
#            
#            # Get sl for inbox=====================
#            limitby=(0,1)
#            rows_check=db((db.sm_inbox.cid==cid)).select(db.sm_inbox.sl, orderby= ~db.sm_inbox.sl,limitby=limitby)
#            sl_inbox=0
#            
#            if rows_check:
#                sl_inbox=rows_check[0].sl
#                
#            sl_inbox=sl_inbox+1  
#            
##            ===============================================
#            client_check=db((db.sm_client.cid==cid) & (db.sm_client.client_id==client_id) & (db.sm_client.status=='ACTIVE')).select(db.sm_client.area_id,db.sm_client.name,db.sm_client.depot_id,limitby=limitby)
#            
#            depot_id=''
#            depot_name=''
#            area_id=''
#            area_name=''
#            client_name=''
#            if client_check:                
#                area_id=client_check[0].area_id
#                client_name=client_check[0].name
#                depot_id=client_check[0].depot_id
#            else:
#                error_msg= "Error: Invalid Route or Client." 
#            
#            #Check valid rep against client based on sm_rep_area
#            rep_area_check=db((db.sm_rep_area.cid==cid) & (db.sm_rep_area.rep_id==rep_id) & (db.sm_rep_area.client_id==client_id)).select(db.sm_rep_area.rep_id,limitby=limitby)
#            if rep_area_check:
#                pass
#            else:
#                error_msg= "Error: Invalid Route or Client.Please Check Your Valid Route or Client List."  
#            
#            depot_name_check=db((db.sm_depot.cid==cid) & (db.sm_depot.depot_id==depot_id) ).select(db.sm_depot.name,limitby=limitby) 
#            if depot_name_check:
#                depot_name=depot_name_check[0].name 
#                
#            area_name_check=db((db.sm_level.cid==cid) & (db.sm_level.level_id==area_id) ).select(db.sm_level.level_name,limitby=limitby) 
#            if area_name_check:
#                area_name=area_name_check[0].level_name
#                
#            #==============================================================
#            if (error_msg==""):
#                error_flag=0
#                
#            # Insert in inbox 
#            if (error_flag==1):
#                status='ERROR'
#                error_in_sms=error_msg
#                inbox_insert=db.sm_inbox.insert(cid=cid,sl=int(sl_inbox),mobile_no=mobile_no,sms=data_for_inbox,status=status,error_in_sms=error_in_sms)                
#                return str(msg_start)+error_msg
#   
#            elif (error_flag==0):                
#                status='SUCCESS'
#                inbox_insert=db.sm_inbox.insert(cid=cid,sl=int(sl_inbox),mobile_no=mobile_no,sms=data_for_inbox,status='SUCCESS')            
#                
#                #            ===========================insert in to order table=================
#                if sms_type=='D':
#                    sl_flag=False
#                    sl=0
#                    if (depot_id!=''):
#                        query_sl=db((db.sm_depot.cid==str(cid)) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.id,db.sm_depot.del_sl,limitby=(0,1))                        
#                        if query_sl:
#                            sl=query_sl[0].del_sl
#                            sl=int(sl)+1
#                        
#                        query_sl[0].update_record(del_sl=sl)
#                        
#                        # not necessary 
#                        check_sl=db((db.sm_invoice.cid==cid) & (db.sm_invoice.depot_id==depot_id) & (db.sm_invoice.sl==sl)).select(db.sm_invoice.sl,limitby=(0,1))
#                    else:
#                        return  "Error: depot blank"     
#                    
#                    if(sl==0):
#                        pass
#                    else:
#                        sl_flag=True
#                    
#                    if check_sl:
#                        sl_flag=False
#                    else:
#                        pass
#                    
#                    #Process product list--------------
#                    if sl_flag==True:
#                        product=''
#                        separator_item='.'                        
#                        prodct_single=item_qty_all.split(separator_item,item_qty_all.count(separator_item))
#                        total_product=item_qty_all.count(separator_item)
#                        i=0
#                        success=''
#                        
#                        # Insert detail
#                        totalAmount=0
#                        while i<total_product+1:
#                            separator_qty=','
#                            prodct_id=''
#                            product_qty='0'
#                            prodct_qty=prodct_single[i].split(separator_qty,prodct_single[i].count(separator_qty))
#                            total_field=prodct_single[i].count(separator_qty)
#                            if total_field>0:
#                                prodct_id=str(prodct_qty[0]).strip().upper()
#                                product_qty=prodct_qty[1]
#                                
#                                i=i+1
#                                query_price=db((db.sm_item.cid==cid) & (db.sm_item.item_id==prodct_id)).select(db.sm_item.ALL)
#                                price=0
#                                order_insert=0
#                                #Create string for 
#                                data_for_balance_update=''
#
#                                date= str(date_fixed)[0:8]+"01" #Set first date of month
#
#                                for row_price in query_price:
#                                    price=row_price.price
#                                    name=row_price.name
#                                    catagory=row_price.category_id
#                                    
#                                    if product_qty!='0':
#                                        
#                                        temp_amount=float(price)*float(product_qty)                                        
#                                        totalAmount=float(totalAmount)+float(temp_amount)
#                                        
#                                        invoice_insert=db.sm_invoice.insert(cid=cid,depot_id=depot_id,depot_name=depot_name,sl=int(sl),client_id=client_id,client_name=client_name,rep_id=rep_id,rep_name=rep_name,order_datetime=date_fixed,delivery_date=delivery_date,area_id=area_id,area_name=area_name,item_id=prodct_id,quantity=product_qty,price=price,item_name=name,category_id=catagory,invoice_media='SMS',status='Invoiced',ym_date=ym_date)
#                                        
#                                        
#                                if int(invoice_insert)>0:
#                                     success="Success "+"SL No: "+str(sl)
#                                     
#                                else:
#                                    pass
#                        
#                        #Update client depot balance
#                        data_for_balance_update=str(cid)+'<fdfd>DELIVERY<fdfd>'+str(sl)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(depot_id)+'-'+str(sl)+'<fdfd>DPT-'+str(depot_id)+'<fdfd>CLT-'+str(client_id)+'<fdfd>'+str(totalAmount)
#                        result_string=set_balance_transaction(data_for_balance_update)
#                        #Insert head
#                        order_insert_head=db.sm_invoice_head.insert(cid=cid,depot_id=depot_id,depot_name=depot_name,sl=int(sl),client_id=client_id,client_name=client_name,rep_id=rep_id,rep_name=rep_name,order_datetime=date_fixed,delivery_date=delivery_date,area_id=area_id,area_name=area_name,invoice_media='SMS',status='Invoiced',ym_date=ym_date)
#
#                        return str(msg_start)+success
#                    else:
#                        return  str(msg_start)+"sl flag invalid" 
#                else:
#                    return  str(msg_start)+"failed"  
#                    
#            else:
#                return  str(msg_start)+"failed"   
#    except:
#         if error_msg == '':
#             error_msg = 'Invalid SMS. Please check your SMS format'
#         return str(msg_start)+error_msg    

#=== (Billal-sixseasons2 ok) item,qty,freeQty
#def sms_invoice_submit_with_date_iqf(pass_get,mobile,cid,my_str):
#    START='START'
#    END='END'
#    error_flag=1
#    error_msg=''
#    msg_start='START'
#    try:
#        pass_get=pass_get
#        my_str=my_str.replace(" ", "")
#        
#        if (pass_get!='Compaq510DuoDuo'):
#            return "STARTInvalid sms"
#        
#        if my_str != "":
#            separator_url='.'
#            totalfields=my_str.count(separator_url)
#            
#            rep_id=''
#            sms_type=''
#            delivery_date=''
#            client_id=''
#            item_qty_all=''
#            order_date = ''
#            data_for_inbox=''
#            order_date=str(date_fixed)[0:10]
#            
#            url_list_url=my_str.split(separator_url)
#            
#            sms_type=url_list_url[1].upper().strip()
#            del_date=url_list_url[2].upper().strip()
#            inbox_date=del_date
#            
#            client_id=url_list_url[3].upper().strip()
#            mobile_no=str(mobile).upper().strip()
#            cid=str(cid).upper()
#            
#            #========================= Rep check ========           
#            rep_name=''
#            rec_rep=db((db.sm_rep.cid==cid) & (db.sm_rep.mobile_no==mobile_no) & (db.sm_rep.status=='ACTIVE') & (db.sm_rep.sms=='Yes')).select(db.sm_rep.rep_id,db.sm_rep.name,limitby=(0,1))
#            if not rec_rep:
#                return str(msg_start)+"Field Force Authorization Error."
#            else:
#                rep_id=rec_rep[0].rep_id
#                rep_name=rec_rep[0].name
#            
#            
#            #================ Date check            
#            current_date=str(date_fixed)[0:10]
#            current_day=str(current_date)[8:10]
#            set_date=current_day
#            
#            if(del_date.isdigit()):
#                pass
#            else:
#                return str(msg_start)+"Error: Invalid date."
#            
#            #If date greater than current date , date with treat as date of past month
#            if(int(del_date)==int(current_day)):   
#                set_date=current_date
#                
#            elif (int(del_date)<int(current_day)):            
#                set_date=str(current_date)[0:8]+del_date
#
#            elif(int(del_date)>int(current_day)):                
#                current_month=str(current_date)[5:7]
#                
#                if int(current_month)>1:
#                    current_month=int(current_month)-1
#                    set_date=str(current_date)[0:5]+str(current_month)+"-"+str(del_date)
#                else:
#                    del_year=str(current_date)[0:4]
#                    del_year_past=int(del_year)-1
#                    set_date=str(del_year_past)+'-'+'12'+"-"+str(del_date)
#                    
#            #delivery_date=set_date
#            
#            date_flag=True
#            try:
#                delivery_date=datetime.datetime.strptime(set_date,'%Y-%m-%d')
#            except:
#                date_flag=False
#            
#            
#            if (date_flag==False):
#                return str(msg_start)+"Error: Invalid date."
#            
#            ym_date=str(delivery_date)[0:7]+'-01'
#            
#            data_for_inbox=str(sms_type)+'.'+str(inbox_date)+'.'+str(client_id)
#            
#            # =========================== Client check            
#            client_name=''
#            area_id=''
#            area_name=''            
#            depot_id=''
#            depot_name=''            
#            client_check=db((db.sm_client.cid==cid) & (db.sm_client.client_id==client_id) & (db.sm_client.status=='ACTIVE')).select(db.sm_client.area_id,db.sm_client.name,db.sm_client.depot_id,limitby=(0,1))
#            if not client_check:
#                return str(msg_start)+"Error: Invalid Client."
#            else:             
#                area_id=client_check[0].area_id
#                client_name=client_check[0].name
#                depot_id=client_check[0].depot_id
#            
#            #Check valid rep against client based on sm_rep_area
#            rep_area_check=db((db.sm_rep_area.cid==cid) & (db.sm_rep_area.rep_id==rep_id) & (db.sm_rep_area.client_id==client_id)).select(db.sm_rep_area.rep_id,limitby=(0,1))
#            if not rep_area_check:
#                return str(msg_start)+"Error: Invalid Rep-Client. Please Check Your Valid Rep-Client List."  
#            else:
#                pass
#            
#            depot_name_check=db((db.sm_depot.cid==cid) & (db.sm_depot.depot_id==depot_id) ).select(db.sm_depot.name,limitby=(0,1)) 
#            if depot_name_check:
#                depot_name=depot_name_check[0].name 
#                
#            area_name_check=db((db.sm_level.cid==cid) & (db.sm_level.level_id==area_id) ).select(db.sm_level.level_name,limitby=(0,1)) 
#            if area_name_check:
#                area_name=area_name_check[0].level_name
#                
#            #===========================================================            
#            #Get all item string            
#            item_qty_all=''
#            j=4
#            while j<totalfields+1:
#                if item_qty_all=='':
#                    item_qty_all=str(url_list_url[j]).strip()
#                    j=j+1
#                else:
#                    item_qty_all=str(item_qty_all)+'.'+str(url_list_url[j]).strip()
#                    j=j+1
#            
#            item_qty_all=item_qty_all.upper()
#            #Set data for inbox
#            data_for_inbox=str(data_for_inbox)+'.'+item_qty_all
#            
#            #    =======================check format and duplicate=================
#            separator_item='.'
#            prodct_single=item_qty_all.split(separator_item,item_qty_all.count(separator_item))
#            total_product=len(prodct_single)
#            i=0
#            itemList=[]
#            
#            while i<total_product:
#                item_id=str(prodct_single[i]).strip()#item1,Qty,FreeQty
#                
#                separator_qty=','                
#                item_qtyList=prodct_single[i].split(separator_qty)                
#                total_field=len(item_qtyList)
#                
#                item_id=''
#                qty=''
#                freeQty=''
#                
#                if total_field==3:
#                    item_id=item_qtyList[0].strip().upper()
#                    qty=item_qtyList[1]
#                    freeQty=item_qtyList[2]
#                    
#                    if qty.isdigit():
#                        pass
#                    else:
#                        error_msg= "Error: Invalid Sale qty for:"+str(item_id)
#                        break
#                    
#                    if freeQty.isdigit():
#                        pass
#                    else:
#                        error_msg= "Error: Invalid Free qty for:"+str(item_id)
#                        break
#                    
#                else:
#                    error_msg= "Error: Sale Qty and Free Qty must for item:"+str(item_id)
#                    break
#                
#                
#                if ((qty=="") or (qty=='0')):
#                    error_msg= "Error in Sale Qty:"+str(item_id)
#                    break
#                
#                if (freeQty==""):
#                    error_msg= "Error in Free Qty:"+str(item_id)
#                    break
#                
#                
#                if item_id in itemList:                    
#                    error_msg= "Format error or Duplicate Item:"+str(item_id)
#                    break
#
#                else:
#                    itemList.append(item_id)
#                i=i+1
#            
#            
#            #Create list of item from sm_company_settings table
#            item_table_list=[]
#            item_list_table=''
#            records_company_item=db(db.sm_company_settings.cid==cid).select(db.sm_company_settings.item_list,limitby=(0,1))
#            if records_company_item:
#                item_table_list=str(records_company_item[0].item_list).split(',')
#            
#            #    =========================Check Item validation===============        
#            
#            for i in range(len(itemList)):
#                item_id=itemList[i]
#                if item_id in item_table_list:
#                    pass
#                else:
#                    error_msg="Error: Invalid item:"+str(item_id)                 
#            
#            # Get sl for inbox=====================
#            limitby=(0,1)
#            rows_check=db((db.sm_inbox.cid==cid)).select(db.sm_inbox.sl, orderby= ~db.sm_inbox.sl,limitby=limitby)
#            sl_inbox=0            
#            if rows_check:
#                sl_inbox=rows_check[0].sl
#                
#            sl_inbox=sl_inbox+1  
#            
#            #==============================================================
#            if (error_msg==""):
#                error_flag=0
#                
#            # Insert in inbox 
#            if (error_flag==1):
#                status='ERROR'
#                error_in_sms=error_msg
#                inbox_insert=db.sm_inbox.insert(cid=cid,sl=int(sl_inbox),mobile_no=mobile_no,sms=data_for_inbox,status=status,error_in_sms=error_in_sms)                
#                return str(msg_start)+error_msg
#   
#            elif (error_flag==0):                
#                status='SUCCESS'
#                inbox_insert=db.sm_inbox.insert(cid=cid,sl=int(sl_inbox),mobile_no=mobile_no,sms=data_for_inbox,status='SUCCESS')            
#                
#                #            ===========================insert in to order table=================
#                if sms_type=='D':
#                    sl_flag=True
#                    sl=0
#                    if (depot_id!=''):
#                        query_sl=db((db.sm_depot.cid==cid) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.id,db.sm_depot.del_sl,limitby=(0,1))                        
#                        if query_sl:
#                            sl=query_sl[0].del_sl
#                            sl=int(sl)+1
#                        
#                        query_sl[0].update_record(del_sl=sl)
#                        
#                        # not necessary 
#                        check_sl=db((db.sm_invoice.cid==cid) & (db.sm_invoice.depot_id==depot_id) & (db.sm_invoice.sl==sl)).select(db.sm_invoice.sl,limitby=(0,1))
#                        if check_sl:
#                            sl_flag=False
#                        
#                    else:
#                        return  "Error: depot blank"     
#                    
#                    if(sl==0):
#                        sl_flag=False
#                    
#                    #Process product list--------------
#                    if sl_flag==False:
#                        return  str(msg_start)+"sl flag invalid" 
#                    else:
#                        product=''
#                        separator_item='.'                        
#                        prodct_single=item_qty_all.split(separator_item,item_qty_all.count(separator_item))
#                        total_product=len(prodct_single)
#                        i=0
#                        success=''
#                        
#                        # Insert detail
#                        totalAmount=0
#                        while i<total_product:
#                            
#                            separator_qty=','                
#                            
#                            prodct_qtyList=prodct_single[i].split(separator_qty)
#                            total_field=len(prodct_qtyList)
#                            
#                            if total_field==3:
#                                prodct_id=str(prodct_qtyList[0]).strip().upper()
#                                product_qty=prodct_qtyList[1]
#                                product_qty_free=int(prodct_qtyList[2])
#                                
#                                query_item_price=db((db.sm_item.cid==cid) & (db.sm_item.item_id==prodct_id)).select(db.sm_item.name,db.sm_item.category_id,db.sm_item.price,limitby=(0,1))
#                                price=0
#                                if query_item_price:
#                                    name=query_item_price[0].name
#                                    catagory=query_item_price[0].category_id                                    
#                                    price=query_item_price[0].price                                    
#                                    if product_qty!='0':                                        
#                                        temp_amount=float(price)*float(product_qty)                                        
#                                        totalAmount=float(totalAmount)+float(temp_amount)
#                                        
#                                        invoice_insert=db.sm_invoice.insert(cid=cid,depot_id=depot_id,depot_name=depot_name,sl=int(sl),client_id=client_id,client_name=client_name,rep_id=rep_id,rep_name=rep_name,order_datetime=date_fixed,delivery_date=delivery_date,area_id=area_id,area_name=area_name,item_id=prodct_id,quantity=product_qty,price=price,item_name=name,category_id=catagory,invoice_media='SMS',status='Invoiced',ym_date=ym_date)
#                                
#                                #----- Free
#                                if product_qty_free > 0:
#                                    product_id_free=prodct_id+'T'
#                                    query_item_free_price=db((db.sm_item.cid==cid) & (db.sm_item.item_id==product_id_free)).select(db.sm_item.name,db.sm_item.category_id,limitby=(0,1))
#                                    if query_item_free_price:
#                                        name_free=query_item_free_price[0].name
#                                        catagory_free=query_item_free_price[0].category_id
#                                        
#                                        invoice_free_insert=db.sm_invoice.insert(cid=cid,depot_id=depot_id,depot_name=depot_name,sl=int(sl),client_id=client_id,client_name=client_name,rep_id=rep_id,rep_name=rep_name,order_datetime=date_fixed,delivery_date=delivery_date,area_id=area_id,area_name=area_name,item_id=product_id_free,quantity=product_qty_free,price=0,item_name=name_free,category_id=catagory_free,invoice_media='SMS',status='Invoiced',ym_date=ym_date)
#                                
#                                #---------
#                                if int(invoice_insert)>0:
#                                     success="Success "+"SL No: "+str(sl)                                     
#                                else:
#                                   pass
#                               
#                            else:
#                                pass
#                            
#                            i=i+1
#                        
#                        #Update client depot balance
#                        data_for_balance_update=str(cid)+'<fdfd>DELIVERY<fdfd>'+str(sl)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(depot_id)+'-'+str(sl)+'<fdfd>DPT-'+str(depot_id)+'<fdfd>CLT-'+str(client_id)+'<fdfd>'+str(totalAmount)
#                        result_string=set_balance_transaction(data_for_balance_update)
#                        #Insert head
#                        order_insert_head=db.sm_invoice_head.insert(cid=cid,depot_id=depot_id,depot_name=depot_name,sl=int(sl),client_id=client_id,client_name=client_name,rep_id=rep_id,rep_name=rep_name,order_datetime=date_fixed,delivery_date=delivery_date,area_id=area_id,area_name=area_name,invoice_media='SMS',status='Invoiced',ym_date=ym_date)
#
#                        return str(msg_start)+success
#                    
#                else:
#                    return  str(msg_start)+"failed"  
#                    
#            else:
#                return  str(msg_start)+"failed"   
#    except:
#         if error_msg == '':
#             error_msg = 'Invalid SMS. Please check your SMS format'
#         
#         return str(msg_start)+error_msg    

#=== (Billal- ok Rep/Sup, +freeQty(optional), AutoReturn, AutoLedger ) item,qty+freeQty or item,qty
#CID.D.10.CLIENTID.ITEM,QTY.ITEM,QTY.ITEM,QTY+FreeQty
def sms_invoice_submit_with_date_iqfplus(pass_get,mobile,cid,my_str):    
    error_msg=''
    msg_start='START'
    
    try:
        pass_get=pass_get
        my_str=my_str.replace(" ", "")
        
        if (pass_get!='Compaq510DuoDuo'):
            return "STARTInvalid sms"
            
        if my_str != "":
            separator_url='.'
            totalfields=my_str.count(separator_url)
            
            firstDotIndex=my_str.find('.')            
            data_for_inbox=my_str[firstDotIndex+1:]
            
            item_qty_all=''
            order_date=str(date_fixed)[0:10]            
            url_list_url=my_str.split(separator_url)
            
            cid=str(cid).upper()
            mobile_no=str(mobile).upper().strip()
            sms_type=url_list_url[1].upper().strip()
            del_date=url_list_url[2].upper().strip()                        
            client_id=url_list_url[3].upper().strip()
            
            
            # =============== Check valid company and Create list of item from sm_company_settings table
            item_table_list=[]
            records_company_item=db((db.sm_company_settings.cid==cid)&(db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.item_list,limitby=(0,1))
            if not records_company_item:
                return "STARTInvalid Company"
            else:
                item_table_list=str(records_company_item[0].item_list).split(',')
            
            #========================= Rep check ========   
            rep_id=''
            rep_name=''
            user_type=''
            depthNo=0
            level_id=''
            rec_rep=db((db.sm_rep.cid==cid) & (db.sm_rep.mobile_no==mobile_no) & (db.sm_rep.status=='ACTIVE') & (db.sm_rep.sms=='Yes')).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.user_type,db.sm_rep.field2,db.sm_rep.level_id,limitby=(0,1))
            if not rec_rep:
                return str(msg_start)+"Field Force Authorization Error."
            else:
                rep_id=rec_rep[0].rep_id
                rep_name=rec_rep[0].name
                user_type=rec_rep[0].user_type
                depthNo=rec_rep[0].field2
                level_id=rec_rep[0].level_id
                
            #================ Date check            
            current_date=str(date_fixed)[0:10]
            current_day=str(current_date)[8:10]
            set_date=current_day
            
            if(del_date.isdigit()):
                pass
            else:
                error_msg= "Error: Invalid date"
            
            if error_msg=='':
                #If date greater than current date , date with treat as date of past month
                if(int(del_date)==int(current_day)):   
                    set_date=current_date
                    
                elif (int(del_date)<int(current_day)):            
                    set_date=str(current_date)[0:8]+del_date
    
                elif(int(del_date)>int(current_day)):                
                    current_month=str(current_date)[5:7]
                    
                    if int(current_month)>1:
                        current_month=int(current_month)-1
                        set_date=str(current_date)[0:5]+str(current_month)+"-"+str(del_date)
                    else:
                        del_year=str(current_date)[0:4]
                        del_year_past=int(del_year)-1
                        set_date=str(del_year_past)+'-'+'12'+"-"+str(del_date)
                
                #delivery_date            
                date_flag=True
                try:
                    delivery_date=datetime.datetime.strptime(set_date,'%Y-%m-%d')
                except:
                    date_flag=False
                            
                if (date_flag==False):
                    error_msg= "Error: Invalid date"                
                else:                
                    #========= Check back date            
                    today = datetime.datetime.strptime(current_date,'%Y-%m-%d')
                    
                    date_diff=(today-delivery_date).days
                    
                    ALLOW_BACK_DATE=0
                    back_date_settings=db((db.sm_settings.cid==cid) & (db.sm_settings.s_key=="ALLOW_BACK_DATE")).select(db.sm_settings.s_value,limitby=(0,1))
                    if back_date_settings:
                        ALLOW_BACK_DATE=int(back_date_settings[0].s_value)
                    
                    if (date_diff>ALLOW_BACK_DATE):
                        error_msg= "Error: Back Date Not Allowed More Than "+str(ALLOW_BACK_DATE)+" Days"
            
            #-----
            client_name=''
            area_id=''
            area_name=''            
            depot_id=''
            depot_name=''
            
            if error_msg=='': 
                     
                ym_date=str(delivery_date)[0:7]+'-01'
                
                # =========================== Client check
                client_check=db((db.sm_client.cid==cid) & (db.sm_client.client_id==client_id) & (db.sm_client.status=='ACTIVE')).select(db.sm_client.area_id,db.sm_client.name,db.sm_client.depot_id,db.sm_client.depot_name,limitby=(0,1))
                if not client_check:
                    error_msg="Error: Invalid Client."
                else:             
                    area_id=client_check[0].area_id
                    client_name=client_check[0].name
                    depot_id=client_check[0].depot_id
                    depot_name=client_check[0].depot_name
                    
                    #Check valid rep against client based on sm_rep_area
                    if user_type=='rep':
                        rep_area_check=db((db.sm_rep_area.cid==cid) & (db.sm_rep_area.rep_id==rep_id) & (db.sm_rep_area.area_id==area_id)).select(db.sm_rep_area.area_name,limitby=(0,1))
                        if not rep_area_check:
                            error_msg="Error: Invalid Rep-Area/Market for client. Please Check Your Valid Rep-Area/Market of the client List."  
                        else:
                            area_name=rep_area_check[0].area_name
                            
                    elif user_type=='sup':
                        level = 'level' + str(depthNo)
                        levelRows = db((db.sm_level.cid == cid) & (db.sm_level.level_id==area_id) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_id)).select(db.sm_level.level_name,limitby=(0,1))
                        if not levelRows:
                            error_msg="Error: Invalid Client of the Allocated Area"
                        else:
                            area_name=levelRows[0].level_name
                    else:
                        error_msg="Error: Invalid Field-Force Type"
            
            if error_msg=='':
                #Get all item string         
                item_qty_all=''
                j=4
                while j<totalfields+1:
                    if item_qty_all=='':
                        item_qty_all=str(url_list_url[j]).strip()
                        j=j+1
                    else:
                        item_qty_all=str(item_qty_all)+'.'+str(url_list_url[j]).strip()
                        j=j+1
                
                item_qty_all=item_qty_all.upper()
                            
                #    =======================check format and duplicate=================
                separator_item='.'
                prodct_single_list=item_qty_all.split(separator_item,item_qty_all.count(separator_item))
                total_product=len(prodct_single_list)
                i=0
                itemList=[]            
                while i<total_product:
                    item_id_str=str(prodct_single_list[i]).strip()#item1,Qty+FreeQty or item1,Qty
                    
                    separator_qty=','                
                    item_qtyList=item_id_str.split(separator_qty)                
                    total_field=len(item_qtyList)
                    
                    item_id=''
                    qty=''
                    freeQty=''
                    
                    if total_field==2:
                        item_id=item_qtyList[0].strip().upper()
                        qtyStr=str(item_qtyList[1]).strip().upper()
                        
                        item_qtyList=qtyStr.split('+')
                        total_Qtyfield=len(item_qtyList)
                        
                        if total_Qtyfield==1:
                            qty=item_qtyList[0]
                            
                        elif total_Qtyfield==2:
                            qty=item_qtyList[0]
                            freeQty=item_qtyList[1]                        
                        else:
                            error_msg= "Error: Invalid qty format for:"+str(item_id)
                            break
                        
                        
                        if qty.isdigit():
                            if int(qty)<=0:
                                error_msg= "Error: Invalid Sale qty for:"+str(item_id)
                                break
                            else:
                                pass
                        else:
                            error_msg= "Error: Invalid Sale qty for:"+str(item_id)
                            break
                        
                        if freeQty!='':
                            if freeQty.isdigit():
                                if int(freeQty) < 0:
                                    error_msg= "Error: Invalid Free qty for:"+str(item_id)
                                    break
                                else:
                                    pass
                            else:
                                error_msg= "Error: Invalid Free qty for:"+str(item_id)
                                break
                        
                    else:
                        error_msg= "Error: Invalid Qty format for item:"+str(item_id_str)
                        break
                    
                    
                    if ((qty=="") or (qty=='0')):
                        error_msg= "Error in Sale Qty:"+str(item_id)
                        break
                    
                    #take item list
                    if item_id in itemList:                    
                        error_msg= "Format error or Duplicate Item:"+str(item_id)
                        break
                    else:
                        itemList.append(item_id)
                    i=i+1
                
                
                #    =========================Check Item validation===============
                for i in range(len(itemList)):
                    item_id=itemList[i]
                    if item_id in item_table_list:
                        pass
                    else:
                        error_msg="Error: Invalid item:"+str(item_id)
                        break
            
            # Get sl for inbox=====================
            limitby=(0,1)
            rows_check=db((db.sm_inbox.cid==cid)).select(db.sm_inbox.sl, orderby= ~db.sm_inbox.sl,limitby=limitby)
            sl_inbox=1            
            if rows_check:
                sl_inbox=int(rows_check[0].sl)+1
            
            #==============================================================
            if (error_msg==""):
                error_flag=0
            else:
                error_flag=1
            
            # Insert in inbox 
            if error_flag==1:
                status='ERROR'
                error_in_sms=error_msg
                inbox_insert=db.sm_inbox.insert(cid=cid,sl=sl_inbox,mobile_no=mobile_no,sms=data_for_inbox,status=status,error_in_sms=error_in_sms)                
                return str(msg_start)+error_msg
                
            else:                
                status='SUCCESS'
                inbox_insert=db.sm_inbox.insert(cid=cid,sl=sl_inbox,mobile_no=mobile_no,sms=data_for_inbox,status='SUCCESS')            
                
                #            ===========================insert in to order table=================
                if sms_type=='D':
                    sl_flag=True
                    sl=0
                    if (depot_id!=''):
                        query_sl=db((db.sm_depot.cid==cid) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.id,db.sm_depot.del_sl,limitby=(0,1))                        
                        if query_sl:
                            sl=int(query_sl[0].del_sl)+1
                                                    
                        query_sl[0].update_record(del_sl=sl)
                        
                        # not necessary 
                        check_sl=db((db.sm_invoice.cid==cid) & (db.sm_invoice.depot_id==depot_id) & (db.sm_invoice.sl==sl)).select(db.sm_invoice.sl,limitby=(0,1))
                        if check_sl:
                            sl_flag=False
                    else:
                        return  "Error: depot blank"     
                    
                    if(sl==0):
                        sl_flag=False
                    
                    #Process product list--------------
                    if sl_flag==False:
                        return  str(msg_start)+"Submission failed. please try again" 
                    else:
                        #=============== Settings Flag
                        delivery_duplicate_check=False
                        delivery_dup_settings=db((db.sm_settings.cid==cid) & (db.sm_settings.s_key=="D_DUPLICATE_CHECK") & (db.sm_settings.s_value=="YES")).select(db.sm_settings.s_value,limitby=(0,1))
                        if delivery_dup_settings:
                            delivery_duplicate_check=True
                            
                        result=""                        
                        if (delivery_duplicate_check==True):
                            result=duplicate_return(cid,depot_id,rep_id,client_id,delivery_date)
                            if (result=="Success"):
                                pass
                            else:
                                return str(error_msg)+"Error-AutoReturn: Please Contact Your System Admin"
                        
                        product=''
                        separator_item='.'                        
                        prodct_single=item_qty_all.split(separator_item,item_qty_all.count(separator_item))
                        total_product=len(prodct_single)
                        i=0
                        success=''
                        
                        # Insert detail
                        totalAmount=0
                        insertFlag=False
                        
                        while i<total_product:
                            
                            separator_qty=','
                            prodct_qtyList=prodct_single[i].split(separator_qty)
                            total_field=len(prodct_qtyList)
                            
                            i=i+1
                            
                            prodct_id=''
                            product_qty=0
                            product_qty_free=0
                            
                            if total_field==2:
                                prodct_id=str(prodct_qtyList[0]).strip().upper()
                                product_qtyStr=str(prodct_qtyList[1]).upper()
                                
                                
                                product_qtyList=product_qtyStr.split('+')
                                total_Qtyfield=len(product_qtyList)
                                
                                if total_Qtyfield==1:
                                    product_qty=product_qtyList[0]
                                    
                                elif total_Qtyfield==2:
                                    product_qty=product_qtyList[0]
                                    product_qty_free=product_qtyList[1]                        
                                else:
                                    continue
                            else:
                                continue
                            
                            query_item_price=db((db.sm_item.cid==cid) & (db.sm_item.item_id==prodct_id)).select(db.sm_item.name,db.sm_item.category_id,db.sm_item.price,limitby=(0,1))
                            if query_item_price:
                                name=query_item_price[0].name
                                catagory=query_item_price[0].category_id                                    
                                price=query_item_price[0].price                                    
                                if product_qty!=0:                                        
                                    temp_amount=float(price)*float(product_qty)                                        
                                    totalAmount=float(totalAmount)+float(temp_amount)
                                    
                                    db.sm_invoice.insert(cid=cid,depot_id=depot_id,depot_name=depot_name,sl=sl,client_id=client_id,client_name=client_name,rep_id=rep_id,rep_name=rep_name,order_datetime=date_fixed,delivery_date=delivery_date,area_id=area_id,area_name=area_name,item_id=prodct_id,quantity=product_qty,price=price,item_name=name,category_id=catagory,invoice_media='SMS',status='Invoiced',ym_date=ym_date)
                                    insertFlag=True
                                    
                            #----- Free
                            if int(product_qty_free) > 0:
                                product_id_free=prodct_id+'T'
                                query_item_free_price=db((db.sm_item.cid==cid) & (db.sm_item.item_id==product_id_free)).select(db.sm_item.name,db.sm_item.category_id,limitby=(0,1))
                                if query_item_free_price:
                                    name_free=query_item_free_price[0].name
                                    catagory_free=query_item_free_price[0].category_id
                                    
                                    invoice_free_insert=db.sm_invoice.insert(cid=cid,depot_id=depot_id,depot_name=depot_name,sl=sl,client_id=client_id,client_name=client_name,rep_id=rep_id,rep_name=rep_name,order_datetime=date_fixed,delivery_date=delivery_date,area_id=area_id,area_name=area_name,item_id=product_id_free,quantity=product_qty_free,price=0,item_name=name_free,category_id=catagory_free,invoice_media='SMS',status='Invoiced',ym_date=ym_date)
                        
                        #---------           
                        if insertFlag==True:                            
                            if session.ledgerCreate=='YES':
                                #Update client depot balance
                                data_for_balance_update=str(cid)+'<fdfd>DELIVERY<fdfd>'+str(sl)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(depot_id)+'-'+str(sl)+'<fdfd>DPT-'+str(depot_id)+'<fdfd>CLT-'+str(client_id)+'<fdfd>'+str(totalAmount)
                                result_string=set_balance_transaction(data_for_balance_update)
                            
                            #Insert head
                            order_insert_head=db.sm_invoice_head.insert(cid=cid,depot_id=depot_id,depot_name=depot_name,sl=int(sl),client_id=client_id,client_name=client_name,rep_id=rep_id,rep_name=rep_name,order_datetime=date_fixed,delivery_date=delivery_date,area_id=area_id,area_name=area_name,invoice_media='SMS',status='Invoiced',ym_date=ym_date)
                            
                            success="Success "+"SL No: "+str(sl)
                            return str(msg_start)+success                            
                        else:
                            return  str(msg_start)+"failed"
                else:
                    return  str(msg_start)+"failed"  
            
    except:
         if error_msg == '':
             error_msg = 'Invalid SMS. Please check your SMS format'
         return str(msg_start)+error_msg    
def duplicate_return(cid,depot_id,rep_id,client_id,date):     
    maxSl=0
    req_depot_id=depot_id
    reqSl=0
    
    return_date=date
    ym_date=str(return_date)[0:7]+'-01'
    
    #Get records from invoice
    #Insert head in loop
    #Create list for bulk insert
   
    #------------------- requisition items
    invoice_sl=0
    reqhead=db((db.sm_invoice_head.cid==cid) & (db.sm_invoice_head.depot_id==req_depot_id) &(db.sm_invoice_head.rep_id==rep_id) &(db.sm_invoice_head.client_id==client_id) &(db.sm_invoice_head.delivery_date==date) &(db.sm_invoice_head.status=='Invoiced')).select(db.sm_invoice_head.sl,orderby=~db.sm_invoice_head.sl, limitby=(0,1))
    if reqhead:
        invoice_sl=reqhead[0].sl
    
    reqRecords=db((db.sm_invoice.cid==cid) & (db.sm_invoice.depot_id==req_depot_id) &(db.sm_invoice.sl==invoice_sl)&(db.sm_invoice.status=='Invoiced')).select(db.sm_invoice.ALL,orderby=db.sm_invoice.item_name)
    
    if not reqRecords:
        return "Success"
    
    else:
        
        maxSl=1
        records=db((db.sm_depot.cid==cid) & (db.sm_depot.depot_id==req_depot_id)).select(db.sm_depot.id,db.sm_depot.return_sl,limitby=(0,1))
        if records:
            maxSl=int(records[0].return_sl)+1
            
        #---------------
        # sl update in depot
        records[0].update_record(return_sl=maxSl)
        
        reqDict={}
        insList=[]
        invoice_sl=0
        headFlag=False
        totalAmount=0
        for row in reqRecords:
            depot_id=row.depot_id
            depot_name=row.depot_name
            invoice_sl=row.sl
            order_sl=row.order_sl
            client_id=row.client_id
            client_name=row.client_name
            rep_id=row.rep_id
            rep_name=row.rep_name
            req_note=row.note
            area_id=row.area_id
            area_name=row.area_name
            discount=row.discount
            
            item_id=row.item_id
            item_name=row.item_name
            category_id=row.category_id
            item_qty_value=row.quantity
            bonus_qty=row.bonus_qty
            price=row.price
            
            
            totalAmount+=float(price)*item_qty_value 
            
            reqDict={'cid':cid,'depot_id':depot_id,'depot_name':depot_name,'sl':maxSl,'order_sl':order_sl,'invoice_sl':invoice_sl,'client_id':client_id,'client_name':client_name,'rep_id':rep_id,'rep_name':rep_name,'area_id':area_id,'area_name':area_name,'return_date':return_date,'discount':discount,'note':req_note,
                           'item_id':item_id,'item_name':item_name,'category_id':category_id,'quantity':item_qty_value,'bonus_qty':bonus_qty,'price':price,'ym_date':ym_date}
            insList.append(reqDict)
            if headFlag==False:
                db.sm_return_head.insert(cid=cid,depot_id=depot_id,depot_name=depot_name,sl=maxSl,order_sl=order_sl,invoice_sl=invoice_sl,client_id=client_id,client_name=client_name,rep_id=rep_id,rep_name=rep_name,area_id=area_id,area_name=area_name,return_date=return_date,discount=discount,note=req_note,ym_date=ym_date)
                headFlag=True
        totalAmount=totalAmount-discount
                            
        rows=db.sm_return.bulk_insert(insList)
        #update in invoice
        
        db((db.sm_invoice.cid==cid) & (db.sm_invoice.depot_id==req_depot_id) & (db.sm_invoice.client_id==client_id)&(db.sm_invoice.sl==invoice_sl)).update(note='Returned')
        db((db.sm_invoice_head.cid==cid) & (db.sm_invoice_head.depot_id==req_depot_id) & (db.sm_invoice_head.client_id==client_id)&(db.sm_invoice_head.sl==invoice_sl)).update(note='Returned')
        
        #Create string for client_balance_for_del_return to maintain client balance        
        if session.ledgerCreate=='YES':
            strData=str(cid)+'<fdfd>RETURN<fdfd>'+str(maxSl)+'<fdfd>'+str(datetime_fixed)+'<fdfd>'+str(depot_id)+'-'+str(maxSl)+'<fdfd>CLT-'+str(client_id)+'<fdfd>DPT-'+str(depot_id)+'<fdfd>'+str(totalAmount)
            resStr=set_balance_transaction(strData)        
            resStrList=resStr.split('<sep>',resStr.count('<sep>'))
            flag=resStrList[0]
            msg=resStrList[1]
        else:
            flag='True'
            msg='Success'
            
        if flag=='True':
            db((db.sm_return.cid==cid)& (db.sm_return.depot_id==depot_id) & (db.sm_return.sl==maxSl)).update(status='Returned')
            db((db.sm_return_head.cid==cid)& (db.sm_return_head.depot_id==depot_id) & (db.sm_return_head.sl==maxSl)).update(status='Returned')
            return "Success"
        else:
            return "Failed"

#=== (Billal- ok Rep/Sup, +freeQty(optional), AutoLedger ) item,qty+freeQty or item,qty
#CID.L.10.DepotID.ITEM,QTY.ITEM,QTY.ITEM,QTY+FreeQty
#CONFIDENCE.L.12.10101.IS01,10.DW02,24.PO01,20

#http://e.businesssolutionapps.com/mrepconfidence/sms_order_invoice/sms_order_invoice_submit_with_date?password=Compaq510DuoDuo&mob=8801713334107&cid=CONFIDENCE&msg=CONFIDENCE.L.12.10101.IS01,10.DW02,24.PO01,20

def sms_lifting_submit_with_date_iqfplus(pass_get,mobile,cid,my_str):    
    error_msg=''
    msg_start='START'
    
    try:
        pass_get=pass_get
        my_str=my_str.replace(" ", "")
        
        if (pass_get!='Compaq510DuoDuo'):
            return "STARTInvalid sms"
            
        if my_str != "":
            separator_url='.'
            totalfields=my_str.count(separator_url)
            
            firstDotIndex=my_str.find('.')            
            data_for_inbox=my_str[firstDotIndex+1:]
            
            item_qty_all=''            
            order_date=str(date_fixed)[0:10]            
            url_list_url=my_str.split(separator_url)
            
            cid=str(cid).upper()
            mobile_no=str(mobile).upper().strip()
            sms_type=url_list_url[1].upper().strip()
            del_date=url_list_url[2].upper().strip()
            depot_id=url_list_url[3].upper().strip()
            
            
            # =============== Check valid company and Create list of item from sm_company_settings table
            item_table_list=[]
            records_company_item=db((db.sm_company_settings.cid==cid)&(db.sm_company_settings.status == 'ACTIVE')).select(db.sm_company_settings.item_list,limitby=(0,1))
            if not records_company_item:
                return "STARTInvalid Company"
            else:
                item_table_list=str(records_company_item[0].item_list).split(',')
             
            #========================= Rep check ========   
            rep_id=''
            rep_name=''
            user_type=''
            depthNo=0
            level_id=''
            rec_rep=db((db.sm_rep.cid==cid) & (db.sm_rep.mobile_no==mobile_no) & (db.sm_rep.status=='ACTIVE') & (db.sm_rep.sms=='Yes')).select(db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.user_type,db.sm_rep.field2,db.sm_rep.level_id,limitby=(0,1))
            if not rec_rep:
                return str(msg_start)+"Field Force Authorization Error."
            else:
                rep_id=rec_rep[0].rep_id
                rep_name=rec_rep[0].name
                user_type=rec_rep[0].user_type
                depthNo=rec_rep[0].field2
                level_id=rec_rep[0].level_id
            
            #================ Date check            
            current_date=str(date_fixed)[0:10]
            current_day=str(current_date)[8:10]
            set_date=current_day
            
            if(del_date.isdigit()):
                pass
            else:
                error_msg= "Error: Invalid date"
            
            #Date check
            if error_msg=='':
                #If date greater than current date , date with treat as date of past month
                if(int(del_date)==int(current_day)):   
                    set_date=current_date
                    
                elif (int(del_date)<int(current_day)):            
                    set_date=str(current_date)[0:8]+del_date
    
                elif(int(del_date)>int(current_day)):                
                    current_month=str(current_date)[5:7]
                    
                    if int(current_month)>1:
                        current_month=int(current_month)-1
                        set_date=str(current_date)[0:5]+str(current_month)+"-"+str(del_date)
                    else:
                        del_year=str(current_date)[0:4]
                        del_year_past=int(del_year)-1
                        set_date=str(del_year_past)+'-'+'12'+"-"+str(del_date)
                
                #delivery_date            
                date_flag=True
                try:
                    delivery_date=datetime.datetime.strptime(set_date,'%Y-%m-%d')
                except:
                    date_flag=False
                            
                if (date_flag==False):
                    error_msg= "Error: Invalid date"                
                else:
                    #========= Check back date            
                    today = datetime.datetime.strptime(current_date,'%Y-%m-%d')
                    
                    date_diff=(today-delivery_date).days
                    
                    ALLOW_BACK_DATE=0
                    back_date_settings=db((db.sm_settings.cid==cid) & (db.sm_settings.s_key=="ALLOW_BACK_DATE")).select(db.sm_settings.s_value,limitby=(0,1))
                    if back_date_settings:
                        ALLOW_BACK_DATE=int(back_date_settings[0].s_value)
                    
                    if (date_diff>ALLOW_BACK_DATE):
                        error_msg= "Error: Back Date Not Allowed More Than "+str(ALLOW_BACK_DATE)+" Days"
            
            #----- Depot/Client/Area Check
            suprer_depot_id = ''
            suprer_depot_name = ''
            
            depot_name=''
            if error_msg=='':
                ym_date=str(delivery_date)[0:7]+'-01'
                
                depot_Rows = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id == depot_id)).select(db.sm_depot.id, db.sm_depot.name, db.sm_depot.receive_sl, limitby=(0, 1))
                if not depot_Rows:
                    error_msg="Error: Invalid Depot."
                else:
                    depot_name = depot_Rows[0].name
                    
                    superDepotRows = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_category == 'SUPER') & (db.sm_depot.status == 'ACTIVE')).select(db.sm_depot.id, db.sm_depot.depot_id, db.sm_depot.name, limitby=(0, 1))
                    if not superDepotRows:
                        error_msg="Error: Required Super Depot Settings."                        
                    else:
                        suprer_depot_id = superDepotRows[0].depot_id
                        suprer_depot_name = superDepotRows[0].name
                        
                        
                        #Check valid rep against client based on sm_rep_area
                        if user_type=='rep':
                            rep_area_check=db((db.sm_rep_area.cid==cid) & (db.sm_rep_area.rep_id==rep_id) & (db.sm_rep_area.depot_id==depot_id)).select(db.sm_rep_area.area_name,limitby=(0,1))
                            if not rep_area_check:
                                error_msg="Error: Invalid Depot. Please Check Your Valid Depot in Rep-Area/Market."  
                                
                        elif user_type=='sup':
                            level = 'level' + str(depthNo)
                            levelRows = db((db.sm_level.cid == cid) & (db.sm_level.is_leaf == '1') & (db.sm_level[level] == level_id) & (db.sm_level.depot_id == depot_id)).select(db.sm_level.level_name,limitby=(0,1))
                            if not levelRows:
                                error_msg="Error: Depot not available. Please Check Your Valid Depot"
                        else:
                            error_msg="Error: Invalid Field-Force Type"
                        
            #Item Qty Check
            if error_msg=='':
                #Get all item string         
                item_qty_all=''
                j=4
                while j<totalfields+1:
                    if item_qty_all=='':
                        item_qty_all=str(url_list_url[j]).strip()
                        j=j+1
                    else:
                        item_qty_all=str(item_qty_all)+'.'+str(url_list_url[j]).strip()
                        j=j+1
                
                item_qty_all=item_qty_all.upper()
                            
                #    =======================check format and duplicate=================
                separator_item='.'
                prodct_single_list=item_qty_all.split(separator_item,item_qty_all.count(separator_item))
                total_product=len(prodct_single_list)
                i=0
                itemList=[]            
                while i<total_product:
                    item_id_str=str(prodct_single_list[i]).strip()#item1,Qty+FreeQty or item1,Qty
                    
                    separator_qty=','                
                    item_qtyList=item_id_str.split(separator_qty)                
                    total_field=len(item_qtyList)
                    
                    item_id=''
                    qty=''
                    freeQty=''
                    
                    if total_field==2:
                        item_id=item_qtyList[0].strip().upper()
                        qtyStr=str(item_qtyList[1]).strip().upper()
                        
                        item_qtyList=qtyStr.split('+')
                        total_Qtyfield=len(item_qtyList)
                        
                        if total_Qtyfield==1:
                            qty=item_qtyList[0]
                            
                        elif total_Qtyfield==2:
                            qty=item_qtyList[0]
                            freeQty=item_qtyList[1]                        
                        else:
                            error_msg= "Error: Invalid qty format for:"+str(item_id)
                            break
                        
                        
                        if qty.isdigit():
                            if int(qty)<=0:
                                error_msg= "Error: Invalid qty for:"+str(item_id)
                                break
                            else:
                                pass
                        else:
                            error_msg= "Error: Invalid qty for:"+str(item_id)
                            break
                        
                        if freeQty!='':
                            if freeQty.isdigit():
                                if int(freeQty) < 0:
                                    error_msg= "Error: Invalid Free qty for:"+str(item_id)
                                    break
                                else:
                                    pass
                            else:
                                error_msg= "Error: Invalid Free qty for:"+str(item_id)
                                break
                        
                    else:
                        error_msg= "Error: Invalid Qty format for item:"+str(item_id_str)
                        break
                    
                    
                    if ((qty=="") or (qty=='0')):
                        error_msg= "Error in Qty:"+str(item_id)
                        break
                    
                    #take item list
                    if item_id in itemList:                    
                        error_msg= "Format error or Duplicate Item:"+str(item_id)
                        break
                    else:
                        itemList.append(item_id)
                    i=i+1
                
                #    =========================Check Item validation===============
                for i in range(len(itemList)):
                    item_id=itemList[i]
                    if item_id in item_table_list:
                        pass
                    else:
                        error_msg="Error: Invalid item:"+str(item_id)
                        break
            
            
            # Get sl for inbox=====================
            limitby=(0,1)
            rows_check=db((db.sm_inbox.cid==cid)).select(db.sm_inbox.sl, orderby= ~db.sm_inbox.sl,limitby=limitby)
            sl_inbox=1            
            if rows_check:
                sl_inbox=int(rows_check[0].sl)+1
            
            #==============================================================
            if (error_msg==""):
                error_flag=0
            else:
                error_flag=1
            
            # Insert in inbox 
            if error_flag==1:
                status='ERROR'
                error_in_sms=error_msg
                inbox_insert=db.sm_inbox.insert(cid=cid,sl=sl_inbox,mobile_no=mobile_no,sms=data_for_inbox,status=status,error_in_sms=error_in_sms)                
                return str(msg_start)+error_msg
                
            else:                
                status='SUCCESS'
                inbox_insert=db.sm_inbox.insert(cid=cid,sl=sl_inbox,mobile_no=mobile_no,sms=data_for_inbox,status='SUCCESS')            
                
                #==============insert in to order table=================
                if sms_type=='L':
                    sl_flag=True
                    receive_sl=0
                    issue_sl=0
                    if (depot_id=='' or suprer_depot_id==''):
                        return  "Error: depot blank"
                    else:
                        receiveDeportRows=db((db.sm_depot.cid==cid) & (db.sm_depot.depot_id==depot_id)).select(db.sm_depot.id,db.sm_depot.receive_sl,limitby=(0,1))                        
                        if receiveDeportRows:
                            receive_sl = int(receiveDeportRows[0].receive_sl) + 1
                        receiveDeportRows[0].update_record(receive_sl=receive_sl)
                        
                        #---
                        supDepotRows = db((db.sm_depot.cid == cid) & (db.sm_depot.depot_id==suprer_depot_id)).select(db.sm_depot.id, db.sm_depot.issue_sl, limitby=(0, 1))
                        if supDepotRows:
                            issue_sl = int(supDepotRows[0].issue_sl) + 1
                        supDepotRows[0].update_record(issue_sl=issue_sl)
                        
                        # necessary 
                        issue_check_sl=db((db.sm_issue_head.cid==cid) & (db.sm_issue_head.depot_id==suprer_depot_id) & (db.sm_issue_head.sl==issue_sl)).select(db.sm_issue_head.sl,limitby=(0,1))
                        if issue_check_sl:
                            sl_flag=False
                            
                    if(receive_sl==0 or issue_sl==0):
                        sl_flag=False
                    
                    #Process product list--------------
                    if sl_flag==False:
                        return  str(msg_start)+"Submission failed. please try again" 
                    else:
                        #=============== Settings Flag
                        receive_depot_id = depot_id
                        req_date = delivery_date
                        
                        # Insert detail
                        ins_list_Issue = []
                        ins_list_Receive = []
                        
                        totalAmount=0
                        insertFlag=False
                        
                        product=''
                        separator_item='.'                        
                        prodct_single=item_qty_all.split(separator_item,item_qty_all.count(separator_item))
                        total_product=len(prodct_single)
                        i=0
                        
                        while i<total_product:
                            
                            separator_qty=','
                            prodct_qtyList=prodct_single[i].split(separator_qty)
                            total_field=len(prodct_qtyList)
                            
                            i=i+1
                            
                            prodct_id=''
                            product_qty=0
                            product_qty_free=0
                            
                            if total_field==2:
                                prodct_id=str(prodct_qtyList[0]).strip().upper()
                                product_qtyStr=str(prodct_qtyList[1]).upper()
                                
                                
                                product_qtyList=product_qtyStr.split('+')
                                total_Qtyfield=len(product_qtyList)
                                
                                if total_Qtyfield==1:
                                    product_qty=int(product_qtyList[0])
                                    
                                elif total_Qtyfield==2:
                                    product_qty=int(product_qtyList[0])
                                    product_qty_free=int(product_qtyList[1])                        
                                else:
                                    continue
                            else:
                                continue
                            
                            if product_qty>0: 
                                query_item_price=db((db.sm_item.cid==cid) & (db.sm_item.item_id==prodct_id)).select(db.sm_item.ALL,limitby=(0,1))
                                if query_item_price:
                                                                        
                                    itemId = query_item_price[0].item_id
                                    itemName = query_item_price[0].name
                                    categoryId = query_item_price[0].category_id
                                    itemPriceDist = query_item_price[0].dist_price
                                    itemQty = product_qty
    
                                    temp_amount = float(itemPriceDist) * int(itemQty)
                                    totalAmount = totalAmount + temp_amount
    
                                    ins_list_Issue.append({'cid':cid, 'depot_id':suprer_depot_id,'depot_name':suprer_depot_name, 'sl':issue_sl, 'issued_to':receive_depot_id,'depot_to_name':depot_name, 'issue_date':req_date, 'ym_date':ym_date, 'note':'', 'item_id':itemId, 'item_name':itemName, 'quantity':itemQty,'bonus_qty':product_qty_free, 'dist_rate':itemPriceDist, 'status':'Posted', 'issue_process_status':'Received'})
                                    ins_list_Receive.append({'cid':cid, 'depot_id':receive_depot_id,'depot_name':depot_name, 'sl':receive_sl, 'receive_from':suprer_depot_id,'depot_from_name':suprer_depot_name, 'receive_date':req_date, 'ref_sl':issue_sl, 'item_id':itemId, 'item_name':itemName, 'quantity':itemQty,'bonus_qty':product_qty_free, 'dist_rate':itemPriceDist, 'short_note':'', 'ym_date':ym_date, 'note':'', 'status':'Posted'})
                                    
                        if len(ins_list_Issue) > 0:
                            try:
                                db.sm_issue_head.insert(cid=cid, depot_id=suprer_depot_id,depot_name=suprer_depot_name, sl=issue_sl, issued_to=receive_depot_id,depot_to_name=depot_name, issue_date=req_date, ym_date=ym_date, status='Posted', issue_process_status='Received')
                                db.sm_issue.bulk_insert(ins_list_Issue)

                                db.sm_receive_head.insert(cid=cid, depot_id=receive_depot_id,depot_name=depot_name, sl=receive_sl, receive_from=suprer_depot_id,depot_from_name=suprer_depot_name, receive_date=req_date, ref_sl=issue_sl, ym_date=ym_date, note='', status='Posted')
                                db.sm_receive.bulk_insert(ins_list_Receive)
                                insertFlag=True
                                
                            except:
                                db.rollback()
                                return  str(msg_start)+"Failed to process data"
                        
                        #---------           
                        if insertFlag==True:                            
                            if session.ledgerCreate=='YES':
                                #Update client depot balance
                                
                                strData2 = str(cid) + '<fdfd>ISSUERECEIVE<fdfd>' + str(issue_sl) + '<fdfd>' + str(datetime_fixed) + '<fdfd>' + str(suprer_depot_id) + '-' + str(issue_sl) + ':' + str(receive_depot_id) + '-' + str(receive_sl) + '<fdfd>DPT-' + str(suprer_depot_id) + '<fdfd>DPT-' + str(receive_depot_id) + '<fdfd>' + str(totalAmount)
                                resStr2 = set_balance_transaction(strData2)
                                
                                resStrList2 = resStr2.split('<sep>', resStr2.count('<sep>'))
                                flag2 = resStrList2[0]
                                msg2 = resStrList2[1]
                                if flag2 != 'True':
                                    db.rollback()
                                    return  str(msg_start)+"Failed to process data"
                                else:
                                    pass
                            else:
                                pass
                            
                            success="Success "+"SL No: "+str(receive_sl)
                            return str(msg_start)+success
                            
                        else:
                            return  str(msg_start)+"failed"
                else:
                    return  str(msg_start)+"failed"  
            
    except:
         if error_msg == '':
             error_msg = 'Invalid SMS. Please check your SMS format'
         return str(msg_start)+error_msg    
         

def test():
    
    str='CID.D.10.ClientID'
    firstDotIndex=str.find('.')
    
    data=str[firstDotIndex+1:]
    
    return data


                

