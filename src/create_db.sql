CREATE TABLE pass_gen (
   player_name TEXT,
   player_link TEXT,
   game TEXT,
   cmp INT,
   att INT,
   yds INT,
   td INT,
   _int INT,
   sk INT
);

CREATE TABLE rush_dir (
   player_name TEXT,
   player_link TEXT,
   game TEXT,
   l_end__att INT,
   l_end__yds INT,
   l_end__td INT,
   l_tckl__att INT,
   l_tckl__yds INT,
   l_tckl__td INT,
   l_guard__att INT,
   l_guard__yds INT,
   l_guard__td INT,
   mid__att INT,
   mid__yds INT,
   mid__td INT,
   r_guard__att INT,
   r_guard__yds INT,
   r_guard__td INT,
   r_tckl__att INT,
   r_tckl__yds INT,
   r_tckl__td INT,
   r_end__att INT,
   r_end__yds INT,
   r_end__td INT
);

CREATE TABLE rush_tckl (
   player_name TEXT,
   player_link TEXT,
   game TEXT,
   l_end INT,
   l_tckl INT,
   l_guard INT,
   mid INT,
   r_guard INT,
   r_tckl INT,
   r_end INT
);

CREATE TABLE penalty (
   player_name TEXT,
   game TEXT,
   pen TEXT,
   yds INT
);

CREATE TABLE player (
   player_name TEXT,
   player_link TEXT,
   ht DOUBLE,
   wt DOUBLE,
   _40yd DOUBLE,
   bench DOUBLE,
   broad_jump DOUBLE,
   shuttle DOUBLE,
   _3cone DOUBLE,
   vertical DOUBLE
);

CREATE TABLE pass_tckl (
   player_name TEXT,
   player_link TEXT,
   game TEXT,
   short_r__tckl INT,
   short_r__dfnd INT,
   short_mid__tckl INT,
   short_mid__dfnd INT,
   short_l__tckl INT,
   short_l__dfnd INT,
   deep_r__tckl INT,
   deep_r__dfnd INT,
   deep_mid__tckl INT,
   deep_mid__dfnd INT,
   deep_l__tckl INT,
   deep_l__dfnd INT
);

CREATE TABLE tgt_dir (
   player_name TEXT,
   player_link TEXT,
   game TEXT,
   short_l__tgt INT,
   short_l__ctch INT,
   short_l__yds INT,
   short_l__td INT,
   short_mid__tgt INT,
   short_mid__ctch INT,
   short_mid__yds INT,
   short_mid__td INT,
   short_r__tgt INT,
   short_r__ctch INT,
   short_r__yds INT,
   short_r__td INT,
   deep_l__tgt INT,
   deep_l__ctch INT,
   deep_l__yds INT,
   deep_l__td INT,
   deep_mid__tgt INT,
   deep_mid__ctch INT,
   deep_mid__yds INT,
   deep_mid__td INT,
   deep_r__tgt INT,
   deep_r__ctch INT,
   deep_r__yds INT,
   deep_r__td INT
);

CREATE TABLE snap_count (
   player_name TEXT,
   player_link TEXT,
   game TEXT,
   team_name TEXT,
   pos TEXT,
   off__num INT,
   off__pct INT,
   def__num INT,
   def__pct INT,
   st__num INT,
   st__pct INT
);

CREATE TABLE zebra (
   zebra_name TEXT,
   zebra_link TEXT,
   role TEXT,
   game TEXT
);

CREATE TABLE injury (
   player_name TEXT,
   team TEXT,
   week INT,
   injury TEXT,
   wed_ps TEXT,
   thu_ps TEXT,
   fri_ps TEXT,
   final TEXT
);
