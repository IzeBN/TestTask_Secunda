ADDRESS = """jsonb_build_object(
                                'city', c.title,
                                'street_title', a.street_title,
                                'house_num', a.house_num,
                                'coordinates', a.house_data -> 'coordinates'
                            ) as address"""
                            
CONTACTS_LIST = """json_agg(distinct jsonb_build_object(
                                'type', oc.contact_type,
                                'value', oc.value
                            )) as contacts"""

ACTIVITIES_LIST = """array_agg(distinct concat_ws(', ', act.title, sa.title, sad.title)) as activities"""

FIND_BY_FULL_ADDRESS = f"""--sql
                        SELECT
                            org.id,
                            org.title,
                            {ADDRESS},
                            {CONTACTS_LIST},
                            {ACTIVITIES_LIST}
                        FROM addresses a
                        JOIN cities c ON c.id = a.city_id
                        JOIN organizations org ON org.address_id = a.id
                        LEFT JOIN organization_contacts oc ON oc.organization_id = org.id
                        LEFT JOIN organization_activities oa ON oa.organization_id = org.id
                        LEFT JOIN sub_activities_details sad ON sad.id = oa.sub_activity_detail_id
                        LEFT JOIN sub_activities sa ON sa.id = sad.sub_activity_id
                        LEFT JOIN activities act ON act.id = sa.activity_id
                        WHERE (c.title = $1 AND a.street_title = $2 AND a.house_num = $3)
                        OR ((a.house_data -> 'coordinates' ->> 'lat') = $1 
                            AND (a.house_data -> 'coordinates' ->> 'lng') = $2)
                        GROUP BY 1,2,3
                        """
FIND_BY_ACTIVITIES = f"""--sql
                      SELECT
                        org.id,
                        org.title,
                        {ADDRESS},
                        {CONTACTS_LIST},
                        {ACTIVITIES_LIST}
                      FROM sub_activities_details sad
                      JOIN sub_activities sa ON sa.id = sad.sub_activity_id
                      JOIN activities act ON act.id = sa.activity_id
                      JOIN organization_activities oa ON oa.sub_activity_detail_id = sad.id
                      JOIN organizations org ON org.id = oa.organization_id
                      JOIN organization_contacts oc ON oc.organization_id = org.id
                      JOIN addresses a ON a.id = org.address_id
                      JOIN cities c ON c.id = a.city_id
                      WHERE sad.title ILIKE '%'||$1||'%'
                        OR  sa.title  ILIKE '%'||$1||'%'
                        or  act.title ILIKE '%'||$1||'%'
                      GROUP BY 1,2,3
                      """
                      
FIND_ALL_IN_RADIUS = f"""--sql
                      SELECT 
                        org.id,
                        org.title,
                        {ADDRESS},
                        {CONTACTS_LIST},
                        {ACTIVITIES_LIST}
                      FROM addresses a
                      JOIN cities c ON c.id = a.city_id
                      JOIN organizations org ON org.address_id = a.id
                      LEFT JOIN organization_contacts oc ON oc.organization_id = org.id
                      LEFT JOIN organization_activities oa ON oa.organization_id = org.id
                      LEFT JOIN sub_activities_details sad ON sad.id = oa.sub_activity_detail_id
                      LEFT JOIN sub_activities sa ON sa.id = sad.sub_activity_id
                      LEFT JOIN activities act ON act.id = sa.activity_id
                      WHERE ST_DWithin(ST_SetSRID(ST_MakePoint(
                        (a.house_data->'coordinates'->>'lng')::double precision,
                        (a.house_data->'coordinates'->>'lat')::double precision
                      ), 4326)::geography,
                        ST_SetSRID(ST_MakePoint($2, $1), 4326)::geography,
                        $3)
                      GROUP BY 1,2,3;
                      """
                        
FIND_BY_ID_OR_TITLE = f"""--sql
              SELECT
                org.id,
                org.title,
                {ADDRESS},
                {CONTACTS_LIST},
                {ACTIVITIES_LIST}
              FROM organizations org
              JOIN addresses a ON a.id = org.address_id
              JOIN cities c ON c.id = a.city_id
              LEFT JOIN organization_contacts oc ON oc.organization_id = org.id
              LEFT JOIN organization_activities oa ON oa.organization_id = org.id
              LEFT JOIN sub_activities_details sad ON sad.id = oa.sub_activity_detail_id
              LEFT JOIN sub_activities sa ON sa.id = sad.sub_activity_id
              LEFT JOIN activities act ON act.id = sa.activity_id
              WHERE (org.id = $1) OR (org.title ILIKE '%'||$2||'%')
              GROUP BY 1,2,3
              """