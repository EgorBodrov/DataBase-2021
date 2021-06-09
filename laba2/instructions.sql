create function create_database()
	returns void language sql as $$
		
        create table if not exists "Companies" (
			name text not null primary key,
			email text not null,
			last_release timestamptz default current_timestamp not null
		);

		create table if not exists "Games" (
			id serial not null primary key,,
			title text not null,
			version text not null,
			release date not null,
            genre text not null,
            author text not null references "Companies" (name)
		);

		create index if not exists genre on "Games" (genre);

        create or replace function update_time()
            returns trigger as $u$
            begin 
                if old.version != new.version then
                    update "Companies" set last_release = current_timestamp
                    where name = new.author;
                end if;
                return new;
            end;
        $u$ language plpgsql;

        drop trigger if exists trigger_update on "Games";

        create trigger trigger_update after insert or update on "Games"
            for row execute procedure update_time();
$$;

select "create_database"();

create function drop_database(in db_name text)
    return void language sql as $$
        begin
            drop database db_name;
        end
$$;

create function get_companies()
	returns json language plpgsql as $$
		begin 
			return (select json_agg(json_build_object(
				'name', "Companies".name,
				'email', "Companies".email,
				'last_release', "Companies".last_release
				)) from "Companies");
		end
	$$;

create function get_games() 
	returns json language plpgsql as $$
		begin 
			return (select json_agg(json_build_object(
				'id', "Games".id,
				'title', "Games".title,
				'version', "Games".version,
				'release', "Games".release,
                'genre', "Games".genre,
                'author', "Games".author
				)) from "Games");
		end
	$$;

create function new_company(in name text, in email text)
	returns void language sql as $$
		insert into "Companies"(name, email) 
        values (name, email)
	$$;

create function new_game(in title text, in version text, in release text, in genre text, in author text)
	returns void language sql as $$
		insert into "Games"(title, author, publisher) 
        values (title, version, release, genre, author)
	$$;

create function clear_companies() 
	returns void language sql as $$ 
		truncate "Companies"
	$$;

create function clear_games()
	returns void language sql as $$ 
		truncate "Games"
	$$;

create function find_game(in genre text) 
	returns json language plpgsql as $$
		begin
			return (select json_agg(json_build_object(
				'id', "Games".id,
				'title', "Games".title,
				'version', "Games".version,
				'release', "Games".release,
                'genre', "Games".genre,
                'author', "Games".author
				)) from "Games" where "Games".genre like concat('%', genre, '%'));
		end;
	$$;

create function find_company(in genre text)
	returns json language plpgsql as $$
		begin 
			return (select json_agg(json_build_object(
				'name', "Companies".name,
				'telephone', "Companies".telephone,
				'lastUpdate', "Companies".lastUpdate
				)) from "Companies" where "Companies".name in (
					select author from "Games" where "Games".genre LIKE concat('%', genre, '%')
				)
			);
		end;
	$$;

create function delete_game(in genre1 text)
	returns void language plpgsql as $$
		begin 
			delete from "Games" where genre = genre1;
		end;
	$$;

create function delete_company(in name1 text)
	returns void language plpgsql as $$ 
		begin 
			delete from "Companies" where "Companies".name in (
                select author from "Games" where "Games".genre = name1
            )
		end;
	$$;

create function delete_game_tuple (in num integer)
	returns void language plpgsql as $$
		begin 
			delete from "Games" where id = num;
		end;
	$$;

create function delete_company_tuple (in name1 text)
	returns void language plpgsql as $$
		begin 
			delete from "Companies" where name = name1;
		end;
	$$;

create function update_company_name (in newname text, in oldname text)
	returns void language plpgsql as $$
		begin
			update "Companies" set name = newname where name = oldname;
		end;
	$$;

create function update_company_email(in email1 text, in name1 text)
	returns void language plpgsql as $$
		begin
			update "Companies" set email = email1 where name = name1;
		end;
	$$;

create function update_game_title(in newtitle text, in id1 integer)
	returns void language plpgsql as $$
		begin
			update "Games" set title = newtitle where id = id1;
		end;
	$$;

create function update_game_version(in newversion text, in id1 integer)
	returns void language plpgsql as $$
		begin
			update "Games" set version = newversion where id = id1;
		end;
	$$;

create function update_game_release(in newrelease text, in id1 integer)
	returns void language plpgsql as $$
		begin
			update "Games" set release = newrelease where id = id1;
		end;
	$$;

create function update_game_genre(in newgenre text, in id1 integer)
	returns void language plpgsql as $$
		begin
			update "Games" set genre = newgenre where id = id1;
		end;
	$$;

create function update_game_author(in newauthor text, in id1 integer)
	returns void language plpgsql as $$
		begin
			update "Games" set author = newauthor where id = id1;
		end;
	$$;
