
import urllib2

# http://127.0.0.1:8000/hamdard/client_coverage/client_coverage_url?cid=Hamdard&rep_id=6478&rep_pass=1234
# http://w05.yeapps.com/hamdard/client_coverage/client_coverage_url?cid=Hamdard&rep_id=ITMSO&rep_pass=1234



def client_coverage_url():

    session.btn_filter=None
    session.btn_all=None

    cid = str(request.vars.cid).strip().upper()
    rep_id = str(request.vars.rep_id).strip().upper()    
    rep_pass = str(request.vars.rep_pass).strip()
    
    
    levelId_name = str(request.vars.levelId_name).strip().upper()

    session.cid = cid 
    session.rep_id = rep_id 
    session.rep_pass = rep_pass     
    session.levelId_name = levelId_name 

    date_from=current_date
    now = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    date_ton=now + datetime.timedelta(days = 1)
    date_to=str(date_ton).split(' ')[0]

    session.from_dt=date_from
    session.to_date=date_from

    btn_filter=request.vars.btn_filter
    btn_all=request.vars.btn_all
    reqPage=len(request.args)
    
    levelId_name=''
    
    if btn_filter:
        levelId_name = str(request.vars.levelId_name).strip().upper()

        # return levelId_name
        if (levelId_name!='' or levelId_name!=None or levelId_name!='None'):
            try:
                levelIdstr = str(levelId_name).split('|')[1]
            except:
                levelIdstr=''

        
        session.btn_filter=btn_filter
        session.levelIdstr=levelIdstr
        
        from_dt = str(request.vars.to_dt_2).strip().upper()
        to_date= str(request.vars.to_dt_3).strip().upper()
        dateFlag=True
        
        try:
            from_dt=datetime.datetime.strptime(str(from_dt),'%Y-%m-%d')
            to_date=datetime.datetime.strptime(str(to_date),'%Y-%m-%d')
            session.from_dt=str(from_dt).split(' ')[0]
            session.to_date=str(to_date).split(' ')[0]

        except:
            session.from_dt=''
            session.to_date=''
            dateFlag=False
        reqPage=0
   
    elif btn_all:
        session.btn_filter=None
        session.btn_all=btn_all
        session.from_dt=date_from
        session.to_date=date_from
        session.levelIdstr=None
        reqPage=0

    redirect(URL(c='client_coverage',f='client_coverage'))




def client_coverage():    
    
    response.title = 'Client Coverage'

    cid  = session.cid 
    rep_id  = session.rep_id 
    rep_pass  = session.rep_pass 

   

    date_from=session.from_dt    
    date_to=session.to_date
    
    levelIdstr=session.levelIdstr
    
    # return date_from
    

    btn_filter=request.vars.btn_filter        
    btn_all=request.vars.btn_all
    
    vChecklist=[]
    vCountList=[]
    
    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.password == rep_pass)  & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:

        condition = ''
        if levelIdstr != '':
            condition += " AND area_id = '" + str(levelIdstr) + "'"  
            condition += " AND area_id = '" + str(levelIdstr) + "'"  

        
        
        records_ov=''        
        if session.btn_filter:

                    
            #=============Total Client===============
            
            clientRecords_str = "SELECT count(client_id) as total_client FROM sm_client WHERE cid = '" + str(cid) + "'  ;"
            clientRecords = db.executesql(clientRecords_str, as_dict=True)
           
            total_client = 0
            for i in range(len(clientRecords)):
                clientRecords_str = clientRecords[i]               
                total_client = clientRecords_str['total_client']
                
             
            
            #=============Unique Client Cover===============             

            client_RecordsStr = "SELECT count(client_id) as unique_client_cover  FROM sm_invoice_head WHERE cid = '" + str(cid) + "' AND rep_id = '" + str(rep_id) + "' AND invoice_date >= '" + str(date_from) + "' AND invoice_date <= '" + str(date_to) + "' " + condition + " GROUP BY client_id,invoice_date;"
            # return client_RecordsStr 
            client_Records = db.executesql(client_RecordsStr, as_dict=True)

            unique_client_cover_show = 0
            for i in range(len(client_Records)):
                unique_client_cover_show=unique_client_cover_show+1
                                           

            #=============Client Cover Percentage=============== 
            
             
            unique_client_cover= (float(unique_client_cover_show) / float(total_client))
            unique_client_cover_per=float(unique_client_cover*100)
                            


                # ============ Client/Invoice ==============

            sql_str="SELECT client_id,name FROM sm_client WHERE cid = '"+ str(cid) +"' " + condition + " GROUP BY client_id order by name asc;"        
            records_ov=db.executesql(sql_str,as_dict = True)    

            inv_count = 0   
            invRecords_str = "SELECT count(client_id) as total_client_count,level3_id,client_id,invoice_date FROM sm_invoice_head WHERE cid = '" + str(cid) + "' AND rep_id = '" + str(rep_id) + "' AND invoice_date >= '" + str(date_from) + "' AND invoice_date <= '" + str(date_to) + "' " + condition + "  AND return_count!='1' GROUP BY client_id;"
            # return invRecords_str
            invRecords = db.executesql(invRecords_str, as_dict=True)
            
            # return len(invRecords)
            invRecords_str_single= ''
            
            for i in range(len(invRecords)):
                invRecords_str_single = invRecords[i]

                vCount=invRecords_str_single['total_client_count']
                vCheck=str(invRecords_str_single['client_id']) 
                vChecklist.append(vCheck)
                vCountList.append(vCount)


        else: 
            total_client=0  
            unique_client_cover_show=0  
            # inv_count=0
            unique_client_cover_per=0    


    return dict(cid=cid,rep_id=rep_id,rep_pass=rep_pass,records_ov=records_ov,total_client=total_client,unique_client_cover_show=unique_client_cover_show,unique_client_cover_per=unique_client_cover_per,vChecklist=vChecklist,vCountList=vCountList)



def get_territory():
    lvlStr = ''
    cid = session.cid

    rep_id = str(request.vars.rep_id).strip().upper()

    repRow = db((db.sm_rep.cid == cid) & (db.sm_rep.rep_id == rep_id)  & (db.sm_rep.status == 'ACTIVE')).select(db.sm_rep.ALL, limitby=(0, 1))
    if not repRow:
       retStatus = 'FAILED<SYNCDATA>Invalid Authorization'
       return retStatus
    else:
        user_type = str(repRow[0].user_type).upper()


   
    qset=db()
    qset=qset(db.sm_level.cid==session.cid)


    if user_type == 'SUP':  

        level_rep = repRow[0].level_id
        depth = repRow[0].field2
        level = 'level' + str(depth)
        # return level


        levelList=[]
        SuplevelRows = db((db.sm_supervisor_level.cid == cid) & (db.sm_supervisor_level.sup_id == rep_id) ).select(db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_depth_no, orderby=~db.sm_supervisor_level.level_id)
        # return SuplevelRows
        
        levelStr=''
        for SuplevelRows in SuplevelRows:
            Suplevel_id = SuplevelRows.level_id
            depth = SuplevelRows.level_depth_no
            level = 'level' + str(depth)#+'_id'
            if Suplevel_id not in levelList:
                levelList.append(Suplevel_id)
                if levelStr=='':
                    levelStr="'"+str(Suplevel_id)+"'"
                else:
                    levelStr=levelStr+",'"+str(Suplevel_id)+"'" 
            # return levelStr
        marketStr=''
        marketStrList=[]
        for i in range(len(levelList)):

            if (level=='level0'):
                levelRows = db((db.sm_level.cid == cid) &(db.sm_level.depth == '3') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code,groupby=db.sm_level.level_id,orderby=db.sm_level.level_name)
                # return levelRows
            if (level=='level1'):
                levelRows = db((db.sm_level.cid == cid) &(db.sm_level.depth == '3')& (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code,groupby=db.sm_level.level_id,orderby=db.sm_level.level_name)
                        
            if (level=='level2'):
                levelRows = db((db.sm_level.cid == cid)  &(db.sm_level.depth == '3') & (db.sm_level[level] == levelList[i]) ).select(db.sm_level.level_id, db.sm_level.level_name, db.sm_level.depot_id,db.sm_level.special_territory_code,groupby=db.sm_level.level_id,orderby=db.sm_level.level_name)
            # return levelRows


            # levelRows = db((db.sm_level.cid == cid) & (db.sm_level.level_id.belongs(session.level_idList))).select(db.sm_level.level0, db.sm_level.level0_name, orderby=db.sm_level.level0_name, groupby=db.sm_level.level0)
            for row in levelRows:
                level_id = str(row.level_id)
                name = str(row.level_name).replace('|', ' ').replace(',', ' ')
                
                if lvlStr == '':
                    lvlStr = name + '|' + level_id 
                else:
                    lvlStr += ',' + name + '|' +  level_id 
            
    else:
        rows = db((db.sm_rep_area.cid == cid)  & (db.sm_rep_area.rep_id == rep_id)).select(db.sm_rep_area.area_id, db.sm_rep_area.area_name, groupby=db.sm_rep_area.area_id ,orderby=db.sm_rep_area.area_name)
        for row in rows:
            level_id = str(row.area_id)
            name = str(row.area_name).replace('|', ' ').replace(',', ' ')
            
            if lvlStr == '':
                lvlStr = name + '|' + level_id 
            else:
                lvlStr += ',' + name + '|' +  level_id 
            
    return lvlStr

        
    

    


