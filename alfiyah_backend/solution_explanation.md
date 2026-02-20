# Solusi untuk Pemetaan Prioritas

Masalah prioritas rendah pada booking yang seharusnya memiliki prioritas tinggi (harga 1.000.000, acara besok) disebabkan oleh metode pemetaan klaster K-means ke label prioritas ("low", "medium", "high") yang sebelumnya kurang robust. Pemetaan tersebut hanya didasarkan pada contoh sampel yang *kebetulan* mendapatkan ID klaster tertentu saat model dilatih, tanpa menganalisis karakteristik sebenarnya dari setiap klaster.

**Solusinya adalah memperbarui logika `train_and_save_model()` di `app/utils/priority.py` agar pemetaan klaster ke label prioritas dilakukan secara dinamis berdasarkan nilai intrinsik (karakteristik) dari setiap klaster (centroid) setelah proses K-means.**

Berikut adalah perubahan yang telah saya implementasikan:

1.  **Analisis Centroid Klaster**: Setelah model K-means dilatih, saya sekarang mengambil pusat (centroid) dari setiap klaster. Centroid ini merepresentasikan nilai rata-rata fitur (seperti `diff_days`, `price_locked`, `jumlah_client`) untuk semua titik data dalam klaster tersebut, tetapi dalam skala yang dinormalisasi.

2.  **Inverse Transform Fitur Numerik**: Untuk dapat menafsirkan centroid ini dalam konteks yang sebenarnya, saya melakukan *inverse transform* pada bagian numerik dari setiap centroid. Ini mengembalikan nilai-nilai fitur numerik (hari tersisa, harga terkunci, jumlah klien) ke skala aslinya.

3.  **Penentuan Skor Klaster**: Untuk setiap centroid yang telah di-inverse transform, saya menghitung "skor komposit". Skor ini mencerminkan prioritas klaster secara objektif:
    *   `price_locked` dan `jumlah_client` memberikan kontribusi positif (semakin tinggi, semakin baik).
    *   `diff_days` memberikan kontribusi negatif (semakin rendah hari tersisa, semakin baik, jadi nilai `diff_days` yang rendah harus menghasilkan skor tinggi).
    Dengan menggunakan bobot heuristik, klaster yang memiliki rata-rata harga tinggi, jumlah klien banyak, dan tanggal acara yang dekat akan mendapatkan skor tertinggi.

4.  **Pengurutan Klaster**: Klaster-klaster kemudian diurutkan berdasarkan skor kompositnya dari yang tertinggi ke terendah.

5.  **Pemetaan Label Prioritas Dinamis**:
    *   Klaster dengan skor tertinggi secara otomatis dipetakan ke label "high" (dengan `priority_score` 90, `urgency_level` "urgent", `monetary_level` "vip").
    *   Klaster berikutnya dipetakan ke "medium" (dengan `priority_score` 60, `urgency_level` "soon", `monetary_level` "premium").
    *   Dan klaster terakhir ke "low" (dengan `priority_score` 20, `urgency_level` "upcoming", `monetary_level` "regular").

Dengan perubahan ini, `cluster_to_priority_map` sekarang dibangun secara logis, memastikan bahwa booking Anda dengan harga 1.000.000 dan tanggal acara yang dekat akan selalu dipetakan ke klaster yang benar-benar mewakili prioritas tinggi, terlepas dari ID klaster yang diberikan oleh algoritma K-means.

**Tindakan Selanjutnya:**

Agar perubahan ini berlaku, Anda perlu menjalankan ulang fungsi `train_and_save_model()`. Ini biasanya dilakukan melalui skrip *seeding data* atau mekanisme pelatihan model Anda (misalnya, `seed_data.py` jika ada). Setelah dijalankan, model yang diperbarui akan disimpan ke `priority_model.pkl`, dan aplikasi Anda akan memuat pemetaan prioritas yang benar.