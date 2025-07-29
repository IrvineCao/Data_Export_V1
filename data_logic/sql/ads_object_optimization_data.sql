select 
    month(pfm.created_at) as month,
    obj.country_code,
    obj.marketplace_code,
    storefront.name as storefront_name,
    obj.tool_code,
    obj.name as object_name,
    camp.name as campaign_name,
    camp.campaign_code as campaign_code,
    obj.note as object_note,
    obj.status as object_status,
    camp.status as campaign_status,
    concat(date(obj.timeline_from)," - ",date(obj.timeline_to)) as object_timeline,
    sum(pfm.click) as object_clicks,
    sum(pfm.impression) as object_impressions,
    sum(pfm.ads_gmv / pfm.cost) as object_roas,
    sum(pfm.cost / pfm.click) as object_cpc,
    sum(pfm.ads_gmv) as object_gmv,
    sum(pfm.cost) as object_cost
from kw_discovery_storefront_workspace workspace
join onsite_storefront ON onsite_storefront.id = workspace.storefront_id
join ads_ops_storefront storefront on onsite_storefront.ads_ops_storefront_id = storefront.id
join ads_ops_ads_campaigns camp on camp.storefront_id = storefront.id
join ads_ops_ads_objects obj on obj.parent_id = camp.id
join ads_ops_ads_objects_performance pfm on pfm.ads_object_id = obj.id
    and date(pfm.created_datetime) between :start_date and :end_date
join global_company on storefront.global_company_id = global_company.id
where workspace.workspace_id = :workspace_id
and storefront.id in (:storefront_ids)
group by obj.id, month(pfm.created_at)