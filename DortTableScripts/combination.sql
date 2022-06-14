create
or replace view HATBASBITDURAK_VIEW_COMBINATION as

select att.*, (row_number() OVER (ORDER BY att.hatbasdurak)) ::integer AS row_id
from (select distinct hv.hatbasdurak,
                      hv2.hatbitdurak,
                      hv.bas_durak_x,
                      hv.bas_durak_y,
                      hv2.bit_durak_x,
                      hv2.bit_durak_y
      from hatbasbitdurak_view hv,
           hatbasbitdurak_view hv2) as att