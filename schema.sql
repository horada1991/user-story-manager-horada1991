create table if not exists user_stories (
  id integer primary key,
  title text not null,
  story text not null,
  criteria text not null,
  buiness_value integer not null,
  estimation time,
  status text not null
);