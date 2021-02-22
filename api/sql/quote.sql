CREATE TABLE Quote (
	id serial PRIMARY KEY,
	quote VARCHAR ( 255 ) NOT NULL,
	quote_by VARCHAR ( 100 ) DEFAULT 'Unknown',
	added_by VARCHAR ( 100 )NOT NULL
);