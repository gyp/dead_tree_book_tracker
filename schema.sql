drop table if exists book_locations;
create table book_locations {
  isbn text primary key,
  last_location text,
  current_location text
};