CREATE_TABLES = """--sql
                CREATE EXTENSION IF NOT EXISTS postgis;

                CREATE TABLE IF NOT EXISTS cities(
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(64) NOT NULL UNIQUE,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW()
                );

                CREATE TABLE IF NOT EXISTS addresses(
                    id SERIAL PRIMARY KEY,
                    city_id INT REFERENCES cities(id) NOT NULL,
                    street_title VARCHAR(128) NOT NULL,
                    house_num VARCHAR(16) NOT NULL,
                    house_data JSONB NOT NULL,
                    UNIQUE(street_title, house_num)
                );

                CREATE TABLE IF NOT EXISTS organizations(
                    id SERIAL PRIMARY KEY,
                    address_id INT REFERENCES addresses(id) NOT NULL,
                    title VARCHAR(256) NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW()
                );

                CREATE TABLE IF NOT EXISTS organization_contacts(
                    id SERIAL PRIMARY KEY,
                    organization_id INT REFERENCES organizations(id) NOT NULL,
                    contact_type VARCHAR(32),
                    value VARCHAR(128),
                    created_at TIMESTAMP NOT NULL DEFAULT NOW()
                );

                CREATE TABLE IF NOT EXISTS activities(
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(128) NOT NULL UNIQUE,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW()
                );

                CREATE TABLE IF NOT EXISTS sub_activities(
                    id SERIAL PRIMARY KEY,
                    activity_id INT REFERENCES activities(id) NOT NULL,
                    title VARCHAR(128) NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                    UNIQUE(activity_id, title)
                );

                CREATE TABLE IF NOT EXISTS sub_activities_details(
                    id SERIAL PRIMARY KEY,
                    sub_activity_id INT REFERENCES sub_activities(id) NOT NULL,
                    title VARCHAR(256) NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                    UNIQUE(sub_activity_id, title)
                );

                CREATE TABLE IF NOT EXISTS organization_activities(
                    id SERIAL PRIMARY KEY,
                    organization_id INT REFERENCES organizations(id) NOT NULL,
                    sub_activity_detail_id INT REFERENCES sub_activities_details(id) NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                    UNIQUE(organization_id, sub_activity_detail_id)
                );
"""