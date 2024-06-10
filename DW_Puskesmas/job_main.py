import dim_dusun
import dim_golongan_umur
import dim_penyakit
import dim_poli
import dim_waktu
import fact_kunjungan

# etl pada tabel dimensi
dim_dusun.dim_dusun()
print("1")
dim_golongan_umur.dim_golongan_umur()
print("2")
dim_penyakit.dim_penyakit()
print("3")
dim_poli.dim_poli()
print("4")
dim_waktu.dim_waktu()
print("5")

# etl pada tabel fact
fact_kunjungan.fact_kunjungan()
print("6")
