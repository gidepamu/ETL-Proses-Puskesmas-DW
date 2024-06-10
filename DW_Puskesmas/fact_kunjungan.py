import config
import petl as etl
import time

def fact_kunjungan():
    start_time = time.time()

    dataKunjungan = etl.fromdb(
        config.db_puskesmas(),"select id as visit_id, patient_id, unit_id,tanggal, orchard_id, village_id, groupage_id, sex_id from visits where tanggal between '2016-01-01' and '2022-12-31'"
    )
    dataBiaya = etl.fromdb(
        config.db_puskesmas(),"select expenses.id as biaya_id, visits.id as visit_id, expenses.jp from expenses LEFT JOIN visits on visits.id = expenses.visit_id"
    )
    dataDiagnosis = etl.fromdb(
        config.db_puskesmas(), "select diagnosis.id as diagnosis_id, visits.id as visit_id, diseases.groupdisease_id from diagnosis left join diseases on diseases.id=diagnosis.disease_id left join visits on visits.id=diagnosis.visit_id"
    )
    dim_dusun = etl.fromdb(
        config.dw_mysql_puskesmas(), f"select * from dim_dusun"
    )
    dim_poli= etl.fromdb(
        config.dw_mysql_puskesmas(), f"select * from dim_poliklinik"
    )
    dim_golongan_umur = etl.fromdb(
        config.dw_mysql_puskesmas(), f"select * from dim_golongan_umur"
    )
    dim_penyakit = etl.fromdb(
        config.dw_mysql_puskesmas(), f"select * from dim_penyakit"
    )
    dim_waktu = etl.fromdb(
        config.dw_mysql_puskesmas(), f"select * from dim_waktu"
    )

    dim_dusun_lookup = etl.dictlookupone(dim_dusun,"id_dusun")
    dim_poli_lookup = etl.dictlookupone(dim_poli,"id_poliklinik")
    dim_penyakit_lookup = etl.dictlookupone(dim_penyakit,"id_penyakit")
    dim_golongan_umur_lookup = etl.dictlookupone(dim_golongan_umur,"id_gol_umur")
    dim_waktu_lookup = etl.dictlookupone(dim_waktu,"tanggal")

    fact_kunjungan = etl.join(
        dataKunjungan, dataBiaya,key="visit_id"
    )
    fact_kunjungan = etl.join(
        fact_kunjungan, dataDiagnosis,key="visit_id"
    )
    fact_kunjungan = etl.convert(fact_kunjungan,{
        "unit_id": lambda id_poliklinik:dim_poli_lookup[id_poliklinik]["poliklinikkey"],
        "orchard_id": lambda orchard_id:dim_dusun_lookup[orchard_id]["dusunkey"],
        "groupage_id": lambda id_gol_umur:dim_golongan_umur_lookup[id_gol_umur]["golumurkey"],
        "tanggal": lambda tanggal:dim_waktu_lookup[tanggal]["waktukey"],
        "groupdisease_id": lambda id_penyakit:dim_penyakit_lookup[id_penyakit]["penyakitkey"]
    })
    fact_kunjungan = etl.convert(fact_kunjungan,"sex_id",{
        "1":'Laki-laki',
        "2":"Perempuan"
    })
    fact_kunjungan = etl.cutout(fact_kunjungan,"visit_id","diagnosis_id","biaya_id","village_id","patient_id")
    fact_kunjungan = etl.rename(fact_kunjungan,{
        "sex_id":"jenis_kelamin",
        "jp":"jumlah_biaya",
        "tanggal":"waktukey",
        "unit_id":"poliklinikkey",
        "orchard_id":"dusunkey",
        "groupage_id":"golumurkey",
        "groupdisease_id":"penyakitkey"
    })
    
    etl.todb(fact_kunjungan,config.dw_mysql_puskesmas(),"fact_kunjungan")
    etl.todb(fact_kunjungan,config.dw_PG_puskesmas(),"fact_kunjungan")
    end_time = time.time()
    proses = end_time - start_time
    print(f"{proses:.2f} detik")
fact_kunjungan()