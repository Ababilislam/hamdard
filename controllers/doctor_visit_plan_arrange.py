
def doctor_visit_plan_arrange():     
  
    recordsRep_S="update sm_rep r, sm_doctor_visit_plan d  set  d.rep_name=r.name  WHERE d.cid=r.cid and d.rep_id=r.rep_id and d.rep_name='';"
    recordsRep=db.executesql(recordsRep_S)
    recordsLevel_S="update sm_doctor_visit_plan d, sm_level l  set  d.level2_id=l.level2,d.level2_name=l.level2_name,d.level1_id=l.level1,d.level1_name=l.level1_name,d.level0_id=l.level0,d.level0_name=l.level0_name,d.route_name=l.level_name WHERE d.cid=l.cid and d.route_id=l.level_id and d.route_name='';"
    recordsLevel=db.executesql(recordsLevel_S)

    return "SUCCESS"






