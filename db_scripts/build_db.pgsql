CREATE TABLE IF NOT EXISTS docbot.intentions(
    intention_id serial PRIMARY KEY,
    intention_name varchar(100),
    intention_description varchar(300)
);

CREATE TABLE IF NOT EXISTS docbot.intentions_rel(
    intention_tsvector tsvector,
    intention_id bigint REFERENCES docbot.intentions (intention_id)
);