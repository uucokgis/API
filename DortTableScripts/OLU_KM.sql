--GYY .NET Reports

/*
 Report 2:
 Güzergah Olu Km Raporu :

 * UYARI


 *
**/

-- DURAK_GARAJ_HEPSI_ROTA
-- GARAJ_DURAK_HEPSI_ROTA

-- DURAK_GAR_ROTA
-- GAR_DURAK_ROTA

-- GARAJ_GARAJ_ROTA


-- O_ILK
-- Garajdan -> Hatbaşına
select concat('O_ILK', rdg.garaj_kodu, '_', rdg.durak_kodu) as GUZERGAH_KODU,
rdg.durak_kodu, rdg.garaj_kodu, rdg.d_isletme_bolgesi, d.isletme_alt_bolgesi, d.durak_x, d.durak_y,
rdg.mesafe, rdg.sure
from garaj_durak_hepsi_rota rdg
join durak_coord_vw d on d.durak_kodu = rdg.durak_kodu
where rdg.durak_kodu in (select hat_basi from hat)


-- O_SON
-- hat sonundan garaja
-- todo: envanter kodunu nereden alacagiz?
select CONCAT('O_SON_', rdg.durak_kodu, '_', garaj_kodu) as GUZERGAH_KODU,
rdg.durak_kodu, rdg.d_isletme_bolgesi, d.isletme_alt_bolgesi, d.durak_x, d.durak_y,
rdg.mesafe, rdg.sure
from DURAK_GARAJ_HEPSI_ROTA rdg
join durak_coord_vw d on d.durak_kodu = rdg.durak_kodu
join durak d2 on d2.durak_kodu = rdg.durak_kodu
where rdg.durak_kodu in (select hat_sonu from hat h )


-- O_ARA
-- Gar noktalarından- hatbaşlarına : ( Durak-  Gar)
-- hatsonlarından- gar noktalarına : ( Gar- Durak)

-- todo: envanter kodunu nereden alacagiz?
select CONCAT('O_ARA', rdg.durak_kodu, rdg.gar_kodu) as GUZERGAH_KODU, d.isletme_alt_bolgesi, d.isletme_bolgesi,
d.durak_x, d.durak_y,
rdg.mesafe, rdg.sure
from DURAK_GAR_ROTA rdg
join durak_coord_vw d on d.durak_kodu = rdg.durak_kodu
where rdg.durak_kodu in (select hat_sonu from hat h)
union
select CONCAT('O_ARA', rdg.durak_kodu, rdg.gar_kodu) as GUZERGAH_KODU, d.isletme_alt_bolgesi, d.isletme_bolgesi,
d.durak_x, d.durak_y,
rdg.mesafe, rdg.sure
from GAR_DURAK_ROTA rdg
join durak_coord_vw d on d.durak_kodu = rdg.durak_kodu
where rdg.durak_kodu in (select hat_basi from hat h)
