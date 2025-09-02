
/* init.cql */
CREATE CONSTRAINT source_name IF NOT EXISTS FOR (s:Source) REQUIRE s.name IS UNIQUE;
CREATE CONSTRAINT artifact_eid IF NOT EXISTS FOR (a:Artifact) REQUIRE a.external_id IS UNIQUE;

