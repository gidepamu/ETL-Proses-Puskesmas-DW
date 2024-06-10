import config
import petl as etl

def dim_dusun():
    dataDusun = etl.fromdb(
        config.db_puskesmas(),"select * from orchards"
    )
    data_desa = etl.fromdb(
        config.db_puskesmas(), "select * from villages"
    )
    dim_dusun = etl.cutout(dataDusun,"jml_pdd","acux","acuy","acuepidx","acuepidy")

    dim_desa_lookup = etl.dictlookupone(data_desa,"id")
    dim_dusun = etl.convert(dim_dusun,{
        "village_id": lambda id:dim_desa_lookup[id]["desa"]
    })
    dim_dusun = etl.rename(dim_dusun,{
        "id":"id_dusun",
        "dusun":"nama_dusun",
        "village_id":"nama_desa"
    })

    etl.todb(dim_dusun, config.dw_PG_puskesmas(),"dim_dusun")
    etl.todb(dim_dusun, config.dw_mysql_puskesmas(),"dim_dusun")
dim_dusun()