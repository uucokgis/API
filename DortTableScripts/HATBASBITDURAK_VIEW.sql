-- hat bas bit durak: isletme bolgesi ayni olanlara gore FILTRELENMEDI
 create or replace view VIEW_HATBASBITDURAK as SELECT h.hat_kodu,
    d.durak_kodu AS hatbasdurak,
    d2.durak_kodu AS hatbitdurak,
    split_part((st_astext((d.shape)::st_geometry))::text, ' '::text, 3)::numeric AS bas_durak_x,
    split_part(split_part((st_astext((d.shape)::st_geometry))::text, ' '::text, 4), ')', 1)::numeric as bas_durak_y,
    split_part((st_astext((d2.shape)::st_geometry))::text, ' '::text, 3)::numeric AS bit_durak_x,
    split_part(split_part((st_astext((d2.shape)::st_geometry))::text, ' '::text, 4), ')', 1)::numeric AS bit_durak_y,
    h.isletme_bolgesi as h_isletme_bolgesi,
    d.isletme_bolgesi as db_isletme_bolgesi,
    d2.isletme_bolgesi as ds_isletme_bolgesi,
    h.globalid,
    (row_number() OVER (ORDER BY h.objectid))::integer AS row_id
   FROM ((hat h
     JOIN durak d ON ((h.hat_basi = (d.durak_kodu)::numeric)))
     JOIN durak d2 ON ((h.hat_sonu = (d2.durak_kodu)::numeric))) where h.hat_basi != h.hat_sonu
and (d.durumu = 1 and d2.durumu = 1);
     
    