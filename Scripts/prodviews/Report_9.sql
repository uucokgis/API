SELECT HAT_KODU,GUZERGAH_KODU,BASLANGIC_ADI, d.SHAPE,
d.DURAK_KODU,d.DURAK_TIPI SIRA 
FROM -V_DURAK_SIRA vds 
JOIN SDE.DURAK d ON D.ID = vds.BA_DURAK_ID WHERE BAS_DURAK_MI =1;

/*koordinatlı hat sıra durak raporu

v durak sıra table amacı hatta bağlı olan
durakların sıralı koordinatlı sıralı listesi yer
almaktadır.

hattan duraklara bir ilişki olacak. base tablolar ile çözülecek.

