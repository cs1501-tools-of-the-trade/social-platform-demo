drop table if exists user;
create table user (
  user_id integer primary key autoincrement,
  username text not null unique,
  first_name text not null,
  last_name text not null,
  email text not null,
  pw_hash text not null
);

drop table if exists tweet;
create table tweet (
  tweet_id integer primary key autoincrement,
  author_id integer not null,
  message text not null,
  pub_date datetime default current_timestamp not null
);