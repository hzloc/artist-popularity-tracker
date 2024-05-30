create table if not exists artists(
	id SERIAL primary KEY,
	artist varchar unique,
	created_at timestamp default CURRENT_TIMESTAMP,
	updated_at timestamp
);