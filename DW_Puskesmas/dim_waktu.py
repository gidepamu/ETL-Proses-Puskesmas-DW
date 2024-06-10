import petl as etl
import datetime
import config
import math

def dim_waktu():
    dt =datetime.datetime(2016, 1, 1)
    end = datetime.datetime(2022, 12, 31, 23, 59, 59)
    step = datetime.timedelta(days=1)

    tahun = []
    bulan = []
    namaBulan = []
    hari = []
    namaHari = []
    quarter = []
    tanggal = []
    semester = []

    while dt < end:
        tahun.append(dt.strftime('%Y'))
        tanggal.append(dt.strftime("%Y-%m-%d"))
        bulan.append(dt.strftime('%m'))
        hari.append(dt.strftime('%d'))
        namaHari.append(dt.strftime('%A'))
        quarter.append(math.ceil(int(dt.strftime('%m'))/3))
        if (int(dt.strftime('%m')) <=6):
            semester.append('1')
        else:
            semester.append('2')
        namaBulan.append(dt.strftime('%B'))
        dt += step

    data=[]

    for x in range(len(tanggal)):
        data.append(
            {
                'tanggal' : tanggal[x],
                'namahari': namaHari[x],
                'nohari': hari[x],
                'namabulan': namaBulan[x],
                'nobulan': bulan[x],
                'notahun': tahun[x],
                'quarter': quarter[x],
                'semester': semester[x]
            }
        )
    dim_waktu = etl.fromdicts(data)
    etl.todb(dim_waktu, config.dw_PG_puskesmas(), 'dim_waktu')
    etl.todb(dim_waktu, config.dw_mysql_puskesmas(), 'dim_waktu')

dim_waktu()