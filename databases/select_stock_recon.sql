select 
  t.depot_id AS depot_id, 
  MAX(t.depot_name) AS depot_name, 
  t.store_id AS store_id, 
  MAX(t.store_name) AS store_name, 
  s.item_id AS item_id, 
  s.name AS name, 
  s.pack_size AS pack_size, 
  s.category_id_sp AS category_id_sp, 
  sum(t.r_factory) AS r_factory, 
  sum(t.r_depot) AS r_depot, 
  sum(t.r_adj_in) AS r_adj_in, 
  sum(t.r_other) AS r_other, 
  sum(t.r_rqty) AS r_rqty, 
  sum(t.r_brqty) AS r_brqty, 
  sum(t.i_depot) AS i_depot, 
  sum(t.i_adj_out) AS i_adj_out, 
  sum(t.i_other) AS i_other, 
  sum(t.i_inv_qty) AS i_inv_qty, 
  sum(t.i_b_qty) AS i_b_qty, 
  (
    (
      (
        (
          (
            sum(t.r_factory) + sum(t.r_depot)
          ) + sum(t.r_adj_in)
        ) + sum(t.r_other)
      ) + sum(t.r_rqty)
    ) + sum(t.r_brqty)
  ) AS r_total, 
  (
    (
      (
        (
          sum(t.i_depot) + sum(t.i_adj_out)
        ) + sum(t.i_other)
      ) + sum(t.i_inv_qty)
    ) + sum(t.i_b_qty)
  ) AS i_total, 
  (
    (
      (
        (
          (
            (
              sum(t.r_factory) + sum(t.r_depot)
            ) + sum(t.r_adj_in)
          ) + sum(t.r_other)
        ) + sum(t.r_rqty)
      ) + sum(t.r_brqty)
    ) - (
      (
        (
          (
            sum(t.i_depot) + sum(t.i_adj_out)
          ) + sum(t.i_other)
        ) + sum(t.i_inv_qty)
      ) + sum(t.i_b_qty)
    )
  ) AS CLOSING 
from 
  (
    select 
      '' AS depot_id, 
      '' AS depot_name, 
      '' AS store_id, 
      '' AS store_name, 
      ibnsina2024_v1.sm_item.item_id AS item_id, 
      sum(0) AS r_factory, 
      sum(0) AS r_depot, 
      sum(0) AS r_adj_in, 
      sum(0) AS r_other, 
      sum(0) AS r_rqty, 
      sum(0) AS r_brqty, 
      sum(0) AS i_depot, 
      sum(0) AS i_adj_out, 
      sum(0) AS i_other, 
      sum(0) AS i_inv_qty, 
      sum(0) AS i_b_qty 
    from 
      ibnsina2024_v1.sm_item 
    where 
      (
        ibnsina2024_v1.sm_item.cid = 'IBNSINA'
      ) 
    group by 
      ibnsina2024_v1.sm_item.item_id 
    union 
    select 
      ibnsina2024_v1.sm_receive.depot_id AS depot_id, 
      MAX(
        ibnsina2024_v1.sm_receive.depot_name
      ) AS depot_name, 
      ibnsina2024_v1.sm_receive.store_id AS store_id, 
      MAX(
        ibnsina2024_v1.sm_receive.store_name
      ) AS store_name, 
      ibnsina2024_v1.sm_receive.item_id AS item_id, 
      sum(
        ibnsina2024_v1.sm_receive.quantity
      ) AS r_factory, 
      sum(0) AS r_depot, 
      sum(0) AS r_adj_in, 
      sum(0) AS r_other, 
      sum(0) AS r_rqty, 
      sum(0) AS r_brqty, 
      sum(0) AS i_depot, 
      sum(0) AS i_adj_out, 
      sum(0) AS i_other, 
      sum(0) AS i_inv_qty, 
      sum(0) AS i_b_qty 
    from 
      ibnsina2024_v1.sm_receive 
    where 
      (
        (
          ibnsina2024_v1.sm_receive.cid = 'IBNSINA'
        ) 
        and (
          ibnsina2024_v1.sm_receive.status = 'Posted'
        ) 
        and (
          ibnsina2024_v1.sm_receive.receive_from = 'FACTORY'
        )
      ) 
    group by 
      ibnsina2024_v1.sm_receive.depot_id, 
      ibnsina2024_v1.sm_receive.store_id, 
      ibnsina2024_v1.sm_receive.item_id 
    union 
    select 
      ibnsina2024_v1.sm_receive.depot_id AS depot_id, 
      MAX(
        ibnsina2024_v1.sm_receive.depot_name
      ) AS depot_name, 
      ibnsina2024_v1.sm_receive.store_id AS store_id, 
      MAX(
        ibnsina2024_v1.sm_receive.store_name
      ) AS store_name, 
      ibnsina2024_v1.sm_receive.item_id AS item_id, 
      sum(0) AS r_factory, 
      sum(
        ibnsina2024_v1.sm_receive.quantity
      ) AS r_depot, 
      sum(0) AS r_adj_in, 
      sum(0) AS r_other, 
      sum(0) AS r_rqty, 
      sum(0) AS r_brqty, 
      sum(0) AS i_depot, 
      sum(0) AS i_adj_out, 
      sum(0) AS i_other, 
      sum(0) AS i_inv_qty, 
      sum(0) AS i_b_qty 
    from 
      ibnsina2024_v1.sm_receive 
    where 
      (
        (
          ibnsina2024_v1.sm_receive.cid = 'IBNSINA'
        ) 
        and (
          ibnsina2024_v1.sm_receive.status = 'Posted'
        ) 
        and (
          ibnsina2024_v1.sm_receive.receive_from <> 'FACTORY'
        )
      ) 
    group by 
      ibnsina2024_v1.sm_receive.depot_id, 
      ibnsina2024_v1.sm_receive.store_id, 
      ibnsina2024_v1.sm_receive.item_id 
    union 
    select 
      ibnsina2024_v1.sm_damage.depot_id AS depot_id, 
      MAX(
        ibnsina2024_v1.sm_damage.depot_name
      ) AS depot_name, 
      ibnsina2024_v1.sm_damage.store_id AS store_id, 
      MAX(
        ibnsina2024_v1.sm_damage.store_name
      ) AS store_name, 
      ibnsina2024_v1.sm_damage.item_id AS item_id, 
      sum(0) AS r_factory, 
      sum(0) AS r_depot, 
      sum(ibnsina2024_v1.sm_damage.quantity) AS r_adj_in, 
      sum(0) AS r_other, 
      sum(0) AS r_rqty, 
      sum(0) AS r_brqty, 
      sum(0) AS i_depot, 
      sum(0) AS i_adj_out, 
      sum(0) AS i_other, 
      sum(0) AS i_inv_qty, 
      sum(0) AS i_b_qty 
    from 
      ibnsina2024_v1.sm_damage 
    where 
      (
        (
          ibnsina2024_v1.sm_damage.cid = 'IBNSINA'
        ) 
        and (
          ibnsina2024_v1.sm_damage.status = 'Posted'
        ) 
        and (
          ibnsina2024_v1.sm_damage.transfer_type = 'ADJUSTMENT'
        ) 
        and (
          ibnsina2024_v1.sm_damage.adjustment_type = 'Increase'
        )
      ) 
    group by 
      ibnsina2024_v1.sm_damage.depot_id, 
      ibnsina2024_v1.sm_damage.store_id, 
      ibnsina2024_v1.sm_damage.item_id 
    union 
    select 
      ibnsina2024_v1.sm_damage.depot_id AS depot_id, 
      MAX(
        ibnsina2024_v1.sm_damage.depot_name
      ) AS depot_name, 
      ibnsina2024_v1.sm_damage.store_id AS store_id, 
      MAX(
        ibnsina2024_v1.sm_damage.store_name
      ) AS store_name, 
      ibnsina2024_v1.sm_damage.item_id AS item_id, 
      sum(0) AS r_factory, 
      sum(0) AS r_depot, 
      sum(0) AS r_adj_in, 
      sum(ibnsina2024_v1.sm_damage.quantity) AS r_other, 
      sum(0) AS r_rqty, 
      sum(0) AS r_brqty, 
      sum(0) AS i_depot, 
      sum(0) AS i_adj_out, 
      sum(0) AS i_other, 
      sum(0) AS i_inv_qty, 
      sum(0) AS i_b_qty 
    from 
      ibnsina2024_v1.sm_damage 
    where 
      (
        (
          ibnsina2024_v1.sm_damage.cid = 'IBNSINA'
        ) 
        and (
          ibnsina2024_v1.sm_damage.status = 'Posted'
        ) 
        and (
          ibnsina2024_v1.sm_damage.transfer_type = 'TRANSFER'
        )
      ) 
    group by 
      ibnsina2024_v1.sm_damage.depot_id, 
      ibnsina2024_v1.sm_damage.store_id, 
      ibnsina2024_v1.sm_damage.item_id 
    union 
    select 
      ibnsina2024_v1.sm_return.depot_id AS depot_id, 
      MAX(
        ibnsina2024_v1.sm_return.depot_name
      ) AS depot_name, 
      ibnsina2024_v1.sm_return.store_id AS store_id, 
      MAX(
        ibnsina2024_v1.sm_return.store_name
      ) AS store_name, 
      ibnsina2024_v1.sm_return.item_id AS item_id, 
      sum(0) AS r_factory, 
      sum(0) AS r_depot, 
      sum(0) AS r_adj_in, 
      sum(0) AS r_other, 
      sum(ibnsina2024_v1.sm_return.quantity) AS r_rqty, 
      sum(
        ibnsina2024_v1.sm_return.bonus_qty
      ) AS r_brqty, 
      sum(0) AS i_depot, 
      sum(0) AS i_adj_out, 
      sum(0) AS i_other, 
      sum(0) AS i_inv_qty, 
      sum(0) AS i_b_qty 
    from 
      ibnsina2024_v1.sm_return 
    where 
      (
        (
          ibnsina2024_v1.sm_return.cid = 'IBNSINA'
        ) 
        and (
          ibnsina2024_v1.sm_return.status = 'Returned'
        )
      ) 
    group by 
      ibnsina2024_v1.sm_return.depot_id, 
      ibnsina2024_v1.sm_return.store_id, 
      ibnsina2024_v1.sm_return.item_id 
    union 
    select 
      ibnsina2024_v1.sm_issue.depot_id AS depot_id, 
      MAX(
        ibnsina2024_v1.sm_issue.depot_name
      ) AS depot_name, 
      ibnsina2024_v1.sm_issue.store_id AS store_id, 
      MAX(
        ibnsina2024_v1.sm_issue.store_name
      ) AS store_name, 
      ibnsina2024_v1.sm_issue.item_id AS item_id, 
      sum(0) AS r_factory, 
      sum(0) AS r_depot, 
      sum(0) AS r_adj_in, 
      sum(0) AS r_other, 
      sum(0) AS r_rqty, 
      sum(0) AS r_brqty, 
      sum(ibnsina2024_v1.sm_issue.quantity) AS i_depot, 
      sum(0) AS i_adj_out, 
      sum(0) AS i_other, 
      sum(0) AS i_inv_qty, 
      sum(0) AS i_b_qty 
    from 
      ibnsina2024_v1.sm_issue 
    where 
      (
        (
          ibnsina2024_v1.sm_issue.cid = 'IBNSINA'
        ) 
        and (
          ibnsina2024_v1.sm_issue.status = 'Posted'
        )
      ) 
    group by 
      ibnsina2024_v1.sm_issue.depot_id, 
      ibnsina2024_v1.sm_issue.store_id, 
      ibnsina2024_v1.sm_issue.item_id 
    union 
    select 
      ibnsina2024_v1.sm_damage.depot_id AS depot_id, 
      MAX(
        ibnsina2024_v1.sm_damage.depot_name
      ) AS depot_name, 
      ibnsina2024_v1.sm_damage.store_id AS store_id, 
      MAX(
        ibnsina2024_v1.sm_damage.store_name
      ) AS store_name, 
      ibnsina2024_v1.sm_damage.item_id AS item_id, 
      sum(0) AS r_factory, 
      sum(0) AS r_depot, 
      sum(0) AS r_adj_in, 
      sum(0) AS r_other, 
      sum(0) AS r_rqty, 
      sum(0) AS r_brqty, 
      sum(0) AS i_depot, 
      sum(ibnsina2024_v1.sm_damage.quantity) AS i_adj_out, 
      sum(0) AS i_other, 
      sum(0) AS i_inv_qty, 
      sum(0) AS i_b_qty 
    from 
      ibnsina2024_v1.sm_damage 
    where 
      (
        (
          ibnsina2024_v1.sm_damage.cid = 'IBNSINA'
        ) 
        and (
          ibnsina2024_v1.sm_damage.status = 'Posted'
        ) 
        and (
          ibnsina2024_v1.sm_damage.transfer_type = 'ADJUSTMENT'
        ) 
        and (
          ibnsina2024_v1.sm_damage.adjustment_type = 'Decrease'
        )
      ) 
    group by 
      ibnsina2024_v1.sm_damage.depot_id, 
      ibnsina2024_v1.sm_damage.store_id, 
      ibnsina2024_v1.sm_damage.item_id 
    union 
    select 
      ibnsina2024_v1.sm_damage.depot_id AS depot_id, 
      MAX(
        ibnsina2024_v1.sm_damage.depot_name
      ) AS depot_name, 
      ibnsina2024_v1.sm_damage.store_id AS store_id, 
      MAX(
        ibnsina2024_v1.sm_damage.store_name
      ) AS store_name, 
      ibnsina2024_v1.sm_damage.item_id AS item_id, 
      sum(0) AS r_factory, 
      sum(0) AS r_depot, 
      sum(0) AS r_adj_in, 
      sum(0) AS r_other, 
      sum(0) AS r_rqty, 
      sum(0) AS r_brqty, 
      sum(0) AS i_depot, 
      sum(0) AS i_adj_out, 
      sum(ibnsina2024_v1.sm_damage.quantity) AS i_other, 
      sum(0) AS i_inv_qty, 
      sum(0) AS i_b_qty 
    from 
      ibnsina2024_v1.sm_damage 
    where 
      (
        (
          ibnsina2024_v1.sm_damage.cid = 'IBNSINA'
        ) 
        and (
          ibnsina2024_v1.sm_damage.status = 'Posted'
        ) 
        and (
          ibnsina2024_v1.sm_damage.transfer_type = 'TRANSFER'
        )
      ) 
    group by 
      ibnsina2024_v1.sm_damage.depot_id, 
      ibnsina2024_v1.sm_damage.store_id, 
      ibnsina2024_v1.sm_damage.item_id 
    union 
    select 
      ibnsina2024_v1.sm_invoice.depot_id AS depot_id, 
      MAX(
        ibnsina2024_v1.sm_invoice.depot_name
      ) AS depot_name, 
      ibnsina2024_v1.sm_invoice.store_id AS store_id, 
      MAX(
        ibnsina2024_v1.sm_invoice.store_name
      ) AS store_name, 
      ibnsina2024_v1.sm_invoice.item_id AS item_id, 
      sum(0) AS r_factory, 
      sum(0) AS r_depot, 
      sum(0) AS r_adj_in, 
      sum(0) AS r_other, 
      sum(0) AS r_rqty, 
      sum(0) AS r_brqty, 
      sum(0) AS i_depot, 
      sum(0) AS i_adj_out, 
      sum(0) AS i_other, 
      sum(
        ibnsina2024_v1.sm_invoice.quantity
      ) AS i_inv_qty, 
      sum(
        ibnsina2024_v1.sm_invoice.bonus_qty
      ) AS i_b_qty 
    from 
      ibnsina2024_v1.sm_invoice 
    where 
      (
        (
          ibnsina2024_v1.sm_invoice.cid = 'IBNSINA'
        ) 
        and (
          ibnsina2024_v1.sm_invoice.status = 'Invoiced'
        )
      ) 
    group by 
      ibnsina2024_v1.sm_invoice.depot_id, 
      ibnsina2024_v1.sm_invoice.store_id, 
      ibnsina2024_v1.sm_invoice.item_id
  ) t 
  join ibnsina2024_v1.sm_item s 
where 
  (s.item_id = t.item_id) 
  AND t.depot_id != '' 
group by 
  t.depot_id, 
  t.store_id, 
  s.item_id, 
  s.name, 
  s.pack_size, 
  s.category_id_sp 
order by 
  t.depot_id, 
  s.category_id_sp, 
  s.name;
