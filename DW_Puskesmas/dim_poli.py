import config
import petl as etl

def dim_poli():
    dataPoli = etl.fromdb(
        config.db_puskesmas(), "select * from units"
    )
    dim_poli = etl.cutout(dataPoli,"aktif","bpjs_polyclinic_id")
    dim_poli = etl.rename(dim_poli,{
        "id":"id_poliklinik",
        "unit":"nama_poliklinik"
    })

    etl.todb(dim_poli, config.dw_PG_puskesmas(),"dim_poliklinik")
    etl.todb(dim_poli, config.dw_mysql_puskesmas(),"dim_poliklinik")

dim_poli()