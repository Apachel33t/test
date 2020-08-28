SELECT *
FROM
    many_to_many m
        inner join project p
                   on m.pid = p.id
        inner join server s
                   on m.sid = s.id
WHERE p.description ~ '28-08-2020';