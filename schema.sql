drop table if exists books;
create table books (
  isbn text primary key,
  author text,
  title text,
  last_location text,
  current_location text
);