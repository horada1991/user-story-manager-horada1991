create table if not exists user_stories (
  id integer primary key,
  title text not null,
  story text not null,
  criteria text not null,
  business_value integer not null,
  estimation float,
  status text not null
);