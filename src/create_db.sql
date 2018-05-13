CREATE TABLE pass_gen (
   player_name TEXT,
   player_link TEXT,
   game TEXT,
   cmp DOUBLE,
   att DOUBLE,
   yds DOUBLE,
   td DOUBLE,
   _int DOUBLE,
   sk DOUBLE
);

CREATE TABLE rush_dir (
   player_name TEXT,
   player_link TEXT,
   game TEXT,
   l_end__att DOUBLE,
   l_end__yds DOUBLE,
   l_end__td DOUBLE,
   l_tckl__att DOUBLE,
   l_tckl__yds DOUBLE,
   l_tckl__td DOUBLE,
   l_guard__att DOUBLE,
   l_guard__yds DOUBLE,
   l_guard__td DOUBLE,
   mid__att DOUBLE,
   mid__yds DOUBLE,
   mid__td DOUBLE,
   r_guard__att DOUBLE,
   r_guard__yds DOUBLE,
   r_guard__td DOUBLE,
   r_tckl__att DOUBLE,
   r_tckl__yds DOUBLE,
   r_tckl__td DOUBLE,
   r_end__att DOUBLE,
   r_end__yds DOUBLE,
   r_end__td DOUBLE
);

CREATE TABLE rush_tckl (
   player_name TEXT,
   player_link TEXT,
   game TEXT,
   l_end DOUBLE,
   l_tckl DOUBLE,
   l_guard DOUBLE,
   mid DOUBLE,
   r_guard DOUBLE,
   r_tckl DOUBLE,
   r_end DOUBLE
);

CREATE TABLE penalty (
   player_name TEXT,
   game TEXT,
   pen TEXT,
   yds DOUBLE
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
   short_r__tckl DOUBLE,
   short_r__dfnd DOUBLE,
   short_mid__tckl DOUBLE,
   short_mid__dfnd DOUBLE,
   short_l__tckl DOUBLE,
   short_l__dfnd DOUBLE,
   deep_r__tckl DOUBLE,
   deep_r__dfnd DOUBLE,
   deep_mid__tckl DOUBLE,
   deep_mid__dfnd DOUBLE,
   deep_l__tckl DOUBLE,
   deep_l__dfnd DOUBLE
);

CREATE TABLE tgt_dir (
   player_name TEXT,
   player_link TEXT,
   game TEXT,
   short_l__tgt DOUBLE,
   short_l__ctch DOUBLE,
   short_l__yds DOUBLE,
   short_l__td DOUBLE,
   short_mid__tgt DOUBLE,
   short_mid__ctch DOUBLE,
   short_mid__yds DOUBLE,
   short_mid__td DOUBLE,
   short_r__tgt DOUBLE,
   short_r__ctch DOUBLE,
   short_r__yds DOUBLE,
   short_r__td DOUBLE,
   deep_l__tgt DOUBLE,
   deep_l__ctch DOUBLE,
   deep_l__yds DOUBLE,
   deep_l__td DOUBLE,
   deep_mid__tgt DOUBLE,
   deep_mid__ctch DOUBLE,
   deep_mid__yds DOUBLE,
   deep_mid__td DOUBLE,
   deep_r__tgt DOUBLE,
   deep_r__ctch DOUBLE,
   deep_r__yds DOUBLE,
   deep_r__td DOUBLE
);

CREATE TABLE snap_count (
   player_name TEXT,
   player_link TEXT,
   game TEXT,
   team_name TEXT,
   pos TEXT,
   off__num DOUBLE,
   off__pct DOUBLE,
   def__num DOUBLE,
   def__pct DOUBLE,
   st__num DOUBLE,
   st__pct DOUBLE
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
   week DOUBLE,
   injury TEXT,
   wed_ps TEXT,
   thu_ps TEXT,
   fri_ps TEXT,
   final TEXT
);
