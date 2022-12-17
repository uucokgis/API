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
select concat('O_ILK_', gdr.garaj_kodu, '_', gdr.durak_kodu) as GUZERGAH_KODU,
       gdr.durak_kodu,
       gdr.garaj_kodu,
       gdr.d_isletme_bolgesi::TEXT, d.isletmealtbolgesi,
       d.durak_x,
       d.durak_y,
       gdr.mesafe,
       gdr.sure,
       gdr.shape
from garaj_durak_hepsi_rota gdr
         join durak_coord_vw d on d.durak_kodu = gdr.durak_kodu where gdr.durak_kodu in (select hat_basi from hat)


union


select CONCAT('O_SON_', dgr.durak_kodu, '_', garaj_kodu) as GUZERGAH_KODU,
       dgr.durak_kodu,
       dgr.garaj_kodu,
       dgr.d_isletme_bolgesi::TEXT, d.isletmealtbolgesi,
       d.durak_x,
       d.durak_y,
       dgr.mesafe,
       dgr.sure,
       dgr.shape
from DURAK_GARAJ_HEPSI_ROTA dgr
         join durak_coord_vw d on d.durak_kodu = dgr.durak_kodu
         join durak d2 on d2.durak_kodu = dgr.durak_kodu
where dgr.durak_kodu in (select hat_sonu from hat h)


union

select CONCAT('O_ARA_', dgr.durak_kodu, dgr.gar_kodu) as GUZERGAH_KODU,
       dgr.durak_kodu,
       dgr.gar_kodu,
       d.isletmealtbolgesi,
       d.isletmebolgesi,
       d.durak_x,
       d.durak_y,
       dgr.mesafe,
       dgr.sure,
       sde.st_astext(dgr.shape)
from DURAK_GAR_ROTA dgr
         join durak_coord_vw d on d.durak_kodu = dgr.durak_kodu
where dgr.durak_kodu in (select hat_sonu from hat h)



select CONCAT('O_ARA_', gdr.durak_kodu, gdr.gar_kodu) as GUZERGAH_KODU,
       gdr.durak_kodu,
       gdr.gar_kodu,
       d.isletmealtbolgesi,
       d.isletmebolgesi,
       d.durak_x,
       d.durak_y,
       gdr.mesafe,
       gdr.sure,
       sde.st_astext(gdr.shape)
from GAR_DURAK_ROTA gdr
         join durak_coord_vw d on d.durak_kodu = gdr.durak_kodu
where gdr.durak_kodu in (select hat_basi from hat h)

