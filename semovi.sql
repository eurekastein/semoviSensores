Querys 
---Filtra por fecha y por sensor y trae la geometría

select s.geom , b.* 
from
(select a.* 
from 
(SELECT v.ts, a.valor, a.sensor
FROM   tmp.velocidades AS v
LEFT   JOIN LATERAL unnest(valores)
                    WITH ORDINALITY AS a(valor, sensor) ON TRUE) as a 
where 
date_part('month', ts) > 5 and date_part('hour', ts)  = 3) as b 
join tmp.sensores s 
on b.sensor = s.id

-- Estos son los que hace el for de arriba 
-- trae los datos de una lista de sensores 
WITH sens AS (SELECT * FROM tmp.sensores WHERE sensores.id = 1),
        vels AS (SELECT ts, valores[1] FROM tmp.velocidades)
        SELECT sens.*, vels.* FROM sens JOIN vels ON sens.id = 1 ORDER BY ts ASC;
WITH sens AS (SELECT * FROM tmp.sensores WHERE sensores.id = 24),
        vels AS (SELECT ts, valores[24] FROM tmp.velocidades)
        SELECT sens.*, vels.* FROM sens JOIN vels ON sens.id = 24 ORDER BY ts ASC;
WITH sens AS (SELECT * FROM tmp.sensores WHERE sensores.id = 320),
        vels AS (SELECT ts, valores[320] FROM tmp.velocidades)
        SELECT sens.*, vels.* FROM sens JOIN vels ON sens.id = 320 ORDER BY ts ASC;
        
