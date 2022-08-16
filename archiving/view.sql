select objectid,
       cast(ROW_NUMBER() OVER (ORDER BY objectid) as INTEGER)               AS ROW_ID,
       array_remove(array_agg(adi), null)                                   as guncel_adi,
       lag(array_agg(adi), 1) over (order by gdb_to_date)                   as onceki_adi,
       array_remove(array_agg(aciklama), null)                              as guncel_aciklama,
       lag(array_agg(aciklama), 1) over (order by gdb_to_date)              as onceki_aciklama,
       array_remove(array_agg(durak_kodu), null)                            as guncel_durak_kodu,
       lag(array_agg(durak_kodu), 1) over (order by gdb_to_date)            as onceki_durak_kodu,
       array_remove(array_agg(yon_bilgisi), null)                           as guncel_yon_bilgisi,
       lag(array_agg(yon_bilgisi), 1) over (order by gdb_to_date)           as onceki_yon_bilgisi,
       array_remove(array_agg(modul_adedi), null)                           as guncel_modul_adedi,
       lag(array_agg(modul_adedi), 1) over (order by gdb_to_date)           as onceki_modul_adedi,
       array_remove(array_agg(kaldirim_genisligi), null)                    as guncel_kaldirim_genisligi,
       lag(array_agg(kaldirim_genisligi), 1) over (order by gdb_to_date)    as onceki_kaldirim_genisligi,
       array_remove(array_agg(adres), null)                                 as guncel_adres,
       lag(array_agg(adres), 1) over (order by gdb_to_date)                 as onceki_adres,
       array_remove(array_agg(ilid), null)                                  as guncel_ilid,
       lag(array_agg(ilid), 1) over (order by gdb_to_date)                  as onceki_ilid,
       array_remove(array_agg(ilceid), null)                                as guncel_ilceid,
       lag(array_agg(ilceid), 1) over (order by gdb_to_date)                as onceki_ilceid,
       array_remove(array_agg(mahalleid), null)                             as guncel_mahalleid,
       lag(array_agg(mahalleid), 1) over (order by gdb_to_date)             as onceki_mahalleid,
       array_remove(array_agg(durak_kisa_adi), null)                        as guncel_durak_kisa_adi,
       lag(array_agg(durak_kisa_adi), 1) over (order by gdb_to_date)        as onceki_durak_kisa_adi,
       array_remove(array_agg(levha_var), null)                             as guncel_levha_var,
       lag(array_agg(levha_var), 1) over (order by gdb_to_date)             as onceki_levha_var,
       array_remove(array_agg(peron_kodu), null)                            as guncel_peron_kodu,
       lag(array_agg(peron_kodu), 1) over (order by gdb_to_date)            as onceki_peron_kodu,
       array_remove(array_agg(modul_durak_id), null)                        as guncel_modul_durak_id,
       lag(array_agg(modul_durak_id), 1) over (order by gdb_to_date)        as onceki_modul_durak_id,
       array_remove(array_agg(durak_kume_id), null)                         as guncel_durak_kume_id,
       lag(array_agg(durak_kume_id), 1) over (order by gdb_to_date)         as onceki_durak_kume_id,
       array_remove(array_agg(peron_duragi), null)                          as guncel_peron_duragi,
       lag(array_agg(peron_duragi), 1) over (order by gdb_to_date)          as onceki_peron_duragi,
       array_remove(array_agg(durak_id), null)                              as guncel_durak_id,
       lag(array_agg(durak_id), 1) over (order by gdb_to_date)              as onceki_durak_id,
       array_remove(array_agg(ilcead), null)                                as guncel_ilcead,
       lag(array_agg(ilcead), 1) over (order by gdb_to_date)                as onceki_ilcead,
       array_remove(array_agg(mahad), null)                                 as guncel_mahad,
       lag(array_agg(mahad), 1) over (order by gdb_to_date)                 as onceki_mahad,
       array_remove(array_agg(engellikullanim), null)                       as guncel_engellikullanim,
       lag(array_agg(engellikullanim), 1) over (order by gdb_to_date)       as onceki_engellikullanim,
       array_remove(array_agg(engellirampa), null)                          as guncel_engellirampa,
       lag(array_agg(engellirampa), 1) over (order by gdb_to_date)          as onceki_engellirampa,
       array_remove(array_agg(uygunsuzluknedeni), null)                     as guncel_uygunsuzluknedeni,
       lag(array_agg(uygunsuzluknedeni), 1) over (order by gdb_to_date)     as onceki_uygunsuzluknedeni,
       array_remove(array_agg(o1), null)                                    as guncel_o1,
       lag(array_agg(o1), 1) over (order by gdb_to_date)                    as onceki_o1,
       array_remove(array_agg(o2), null)                                    as guncel_o2,
       lag(array_agg(o2), 1) over (order by gdb_to_date)                    as onceki_o2,
       array_remove(array_agg(o3), null)                                    as guncel_o3,
       lag(array_agg(o3), 1) over (order by gdb_to_date)                    as onceki_o3,
       array_remove(array_agg(o4), null)                                    as guncel_o4,
       lag(array_agg(o4), 1) over (order by gdb_to_date)                    as onceki_o4,
       array_remove(array_agg(durumu), null)                                as guncel_durumu,
       lag(array_agg(durumu), 1) over (order by gdb_to_date)                as onceki_durumu,
       array_remove(array_agg(sebebi), null)                                as guncel_sebebi,
       lag(array_agg(sebebi), 1) over (order by gdb_to_date)                as onceki_sebebi,
       array_remove(array_agg(isletme_bolgesi), null)                       as guncel_isletme_bolgesi,
       lag(array_agg(isletme_bolgesi), 1) over (order by gdb_to_date)       as onceki_isletme_bolgesi,
       array_remove(array_agg(isletmealtbolgesi), null)                     as guncel_isletmealtbolgesi,
       lag(array_agg(isletmealtbolgesi), 1) over (order by gdb_to_date)     as onceki_isletmealtbolgesi,
       array_remove(array_agg(durak_tipi), null)                            as guncel_durak_tipi,
       lag(array_agg(durak_tipi), 1) over (order by gdb_to_date)            as onceki_durak_tipi,
       array_remove(array_agg(akilli_durak_durumu), null)                   as guncel_akilli_durak_durumu,
       lag(array_agg(akilli_durak_durumu), 1) over (order by gdb_to_date)   as onceki_akilli_durak_durumu,
       array_remove(array_agg(abonelik_durumu), null)                       as guncel_abonelik_durumu,
       lag(array_agg(abonelik_durumu), 1) over (order by gdb_to_date)       as onceki_abonelik_durumu,
       array_remove(array_agg(kaldirildi_mi), null)                         as guncel_kaldirildi_mi,
       lag(array_agg(kaldirildi_mi), 1) over (order by gdb_to_date)         as onceki_kaldirildi_mi,
       array_remove(array_agg(ikmal_noktasi_tipi), null)                    as guncel_ikmal_noktasi_tipi,
       lag(array_agg(ikmal_noktasi_tipi), 1) over (order by gdb_to_date)    as onceki_ikmal_noktasi_tipi,
       array_remove(array_agg(sofor_degisim_noktasi), null)                 as guncel_sofor_degisim_noktasi,
       lag(array_agg(sofor_degisim_noktasi), 1) over (order by gdb_to_date) as onceki_sofor_degisim_noktasi,
       array_remove(array_agg(cep_var), null)                               as guncel_cep_var,
       lag(array_agg(cep_var), 1) over (order by gdb_to_date)               as onceki_cep_var,
       array_remove(array_agg(duraklama_durumu), null)                      as guncel_duraklama_durumu,
       lag(array_agg(duraklama_durumu), 1) over (order by gdb_to_date)      as onceki_duraklama_durumu,
       array_remove(array_agg(fiziki_durum), null)                          as guncel_fiziki_durum,
       lag(array_agg(fiziki_durum), 1) over (order by gdb_to_date)          as onceki_fiziki_durum,
       array_remove(array_agg(elektirik_durumu), null)                      as guncel_elektirik_durumu,
       lag(array_agg(elektirik_durumu), 1) over (order by gdb_to_date)      as onceki_elektirik_durumu,
       array_remove(array_agg(enerji_durumu), null)                         as guncel_enerji_durumu,
       lag(array_agg(enerji_durumu), 1) over (order by gdb_to_date)         as onceki_enerji_durumu,
       array_remove(array_agg(modul_durak_durumu), null)                    as guncel_modul_durak_durumu,
       lag(array_agg(modul_durak_durumu), 1) over (order by gdb_to_date)    as onceki_modul_durak_durumu,
       array_remove(array_agg(baslangic_durak_mi), null)                    as guncel_baslangic_durak_mi,
       lag(array_agg(baslangic_durak_mi), 1) over (order by gdb_to_date)    as onceki_baslangic_durak_mi,
       array_remove(array_agg(hatkodu), null)                               as guncel_hatkodu,
       lag(array_agg(hatkodu), 1) over (order by gdb_to_date)               as onceki_hatkodu,
       array_remove(array_agg(hatadi), null)                                as guncel_hatadi,
       lag(array_agg(hatadi), 1) over (order by gdb_to_date)                as onceki_hatadi,
       gdb_to_date
from durakgroup by objectid, gdb_to_date

