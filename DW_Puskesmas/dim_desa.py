import config
import petl as etl

def dim_desa():
    dataDesa = etl.fromdb(
        config.db_puskesmas(),"select * from villages"
    )
    dim_desa = etl.cutout(dataDesa,"kode_bps","kode_dukcapil","jml_dusun","luas","penduduk","laki","wanita","acux","acuy","wilayah_asal")
    dim_desa = etl.convert(dim_desa,"wilayah",{
        "T":"Dalam Wilayah",
        "F":"Luar Wilayah"
    })
    dim_desa = etl.rename(dim_desa,{
        "id":"id_desa",
        "desa":"nama_desa"
    })
    etl.todb(dim_desa, config.dw_mysql_puskesmas(),"dim_desa")
    etl.todb(dim_desa, config.dw_PG_puskesmas(),"dim_desa")
    # print(dim_desa)
dim_desa()