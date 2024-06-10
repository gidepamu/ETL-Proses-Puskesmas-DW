import config
import petl as etl

def dim_penyakit():
    dataPenyakit = etl.fromdb(
        config.db_puskesmas(),"select * from diseases"
    )
    dim_penyakit = etl.cutout(dataPenyakit,"icdx","lb1","menular","bpjs_disease_kode","sisrute_disease_code")
    dim_penyakit = etl.rename(dim_penyakit,{
        "id":"id_penyakit",
        "nama":"nama_penyakit",
        "groupdisease_id":"group_idpenyakit"
    })

    etl.todb(dim_penyakit, config.dw_PG_puskesmas(),"dim_penyakit")
    etl.todb(dim_penyakit, config.dw_mysql_puskesmas(),"dim_penyakit")
dim_penyakit()