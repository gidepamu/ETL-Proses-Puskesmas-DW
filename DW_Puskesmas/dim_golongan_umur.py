import config
import petl as etl

def dim_golongan_umur():
    dataGolUmur = etl.fromdb(
        config.db_puskesmas(), "select * from groupages"
    )
    dim_golongan_umur = etl.rename(dataGolUmur,{
        "id":"id_gol_umur",
        "kelompok_umur":"golongan_umur"
    })

    etl.todb(dim_golongan_umur, config.dw_PG_puskesmas(),"dim_golongan_umur")
    etl.todb(dim_golongan_umur, config.dw_mysql_puskesmas(),"dim_golongan_umur")

dim_golongan_umur()
