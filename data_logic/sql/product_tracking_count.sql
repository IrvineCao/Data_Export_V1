WITH product_metrics AS (
  SELECT
    product_a.keyword_id,
    product_a.product_id,
    product_a.device_type,
    product_a.display_type,
    product_a.slot,
    DATE(created_datetime) AS created_date,
    created_datetime
  FROM metric_share_of_search_product product_a
  WHERE product_a.timing = 'daily'
    AND product_a.device_type IN (:device_type)
    AND product_a.display_type IN (:display_type)
    AND created_datetime BETWEEN :start_date AND :end_date
  GROUP BY
    DATE(created_datetime),
    product_a.keyword_id,
    product_a.product_id,
    product_a.device_type,
    product_a.display_type,
    created_datetime,
    product_a.slot
),

main_query AS (
  SELECT
    k.id AS keyword_id,
    k.keyword AS keyword,
    k.keyword_type,
    k.first_interaction_at,

    kw_ws.status AS keyword_status,

    p.id AS product_id,
    p.product_name,
    p.brand_name,
    p.historical_sold,
    p.sold,
    p.selling_price,
    p.discount,
    p.currency,
    p.product_url,
    p.marketplace_name AS product_marketplace,

    s.id AS storefront_id,
    s.storefront_name,
    s.storefront_url,
    s.country_name AS storefront_country,
    s.marketplace_name AS storefront_marketplace,
    s.storefront_type,
    gc.name AS global_company_name,

    ws.id AS workspace_id,

    pm.slot AS product_slot,
    pm.device_type,
    pm.display_type,
    pm.created_date,
    pm.created_datetime

  FROM passport_workspace ws
  JOIN onsite_keyword_workspace kw_ws ON kw_ws.workspace_id = ws.id
  JOIN onsite_keyword_sharded k ON kw_ws.keyword_id = k.id
  JOIN product_metrics pm ON pm.keyword_id = k.id
  JOIN onsite_product p ON p.id = pm.product_id
  JOIN onsite_storefront s ON s.id = p.storefront_id
  LEFT JOIN global_company gc ON s.global_company_id = gc.id

  WHERE ws.id = :workspace_id
--     and k.id = 2251799988004001
    AND kw_ws.status = 'ACTIVATED'
)
select count(1)
from (SELECT
  keyword_id,
  date(created_datetime)
FROM main_query
where true
and (product_name != 'Unspecified' and storefront_name != 'Unspecified')
GROUP BY
  keyword_id,
  date(created_datetime)
ORDER BY product_id, keyword_id, date(created_datetime))