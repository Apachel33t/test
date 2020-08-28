create procedure transaction_create_dump(ppid integer, ssid integer, title character, address character, descr text)
    language plpgsql
as
$$
BEGIN
    IF EXISTS (SELECT id FROM public.server WHERE ip_address = address) THEN
        INSERT INTO public.project (id, name, description) VALUES (ppid, title, descr);
        INSERT INTO public.many_to_many (pid, sid) VALUES (ppid, (SELECT id FROM public.server WHERE ip_address = address));
    ELSE
        IF NOT EXISTS (SELECT id FROM public.server WHERE ip_address = address) THEN
            INSERT INTO public.server (id, name, ip_address,description) VALUES (ssid, title, address, descr);
            INSERT INTO public.project (id, name, description) VALUES (ppid, title, descr);
            INSERT INTO public.many_to_many (pid, sid) VALUES (ppid, ssid);
        ELSE
            RAISE NOTICE 'Cant execute procedure transaction_create_dump';
        END IF;
    END IF;
END;
$$;

alter procedure transaction_create_dump(integer, integer, char, char, text) owner to postgres;

-- We can call this procedure like this => CALL transaction_create_dump(ARGS[]);