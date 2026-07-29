# Laporan Proyek: 

**Intern Name:** Tirta Aji Nugraha  
**Topic:** ARM AI Wearable - HR (Heart Rate)   
**Supervisor:** Muhammad Faudzan Abdullah  
**Draft Status:** Draft  
**Target Hardware:** Grove Vision AI V2 (Cortex-M55 + Ethos-U55)

---

## 1. Overview
Proyek ini bertujuan untuk mengimplementasikan model machine learning KID-PPG untuk mengestimasi detak jantung berdasarkan sinyal Photoplethysmography (PPG). Sensor yang digunakan adalah sensor PPG Max30102, dan model ini ditargetkan untuk berjalan pada perangkat keras Grove Vision AI V2 yang menggunakan arsitektur Cortex-M55 dan Ethos-U55.

## 2. Background
Estimasi detak jantung yang akurat menggunakan sensor PPG sangat penting untuk pemantauan fisiologis yang berkelanjutan, namun sering kali terhambat oleh artefak gerakan (motion artifacts). Model KID-PPG mengatasi hal ini dengan memanfaatkan arsitektur deep learning berbasis mekanisme atensi (attention mechanism) untuk meningkatkan akurasi estimasi, terutama pada kondisi detak jantung tinggi

## 3. Dataset & Preprocessing
**DATASET**   
Model KID-PPG dibangun di atas dataset publik bernama PPG-Dalia. Dataset ini dipilih karena sangat merepresentasikan kondisi noisy dari perekaman wearable device di dunia nyata.
* **Subjek & Ukuran:** Melibatkan data dari 15 subjek berbeda yang melakukan berbagai aktivitas dinamis sehari-hari (seperti duduk, berjalan, bersepeda). Sinyal yang diambil biasanya berupa data PPG optik dan akselerometer 3-sumbu (3D).
* **Label Target:** Jaringan saraf dilatih untuk memprediksi detak jantung aktual dalam satuan Beats Per Minute (BPM) secara terus-menerus.
* **Strategi Evaluasi (Split):** Alih-alih membagi data secara acak, pelatihan memisahkan data berbasis subjek menggunakan metode Leave-One-Subject-Out (LOSO) atau Leave-One-Group-Out (LOGO). Model dilatih pada 14 subjek, lalu diuji pada 1 subjek sisanya agar benar-benar merepresentasikan kemampuan model terhadap "pengguna baru" yang belum pernah ia lihat.

**PREPROCESSING**   
Preprocessing data untuk model KID-PPG dilakukan dalam dua tahap, yaitu tahap training dan tahap inferensi.
### 3.1 Tahap Training
* **Adaptive Filtering:**  sebuah model filter linier (link ke repo i guess) dilatih berulang-ulang secara spesifik hingga 16.000 epoch sebelum proses training utama dimulai. Filter ini menggunakan manipulasi Fast Fourier Transform (FFT) untuk menganalisis spektrum frekuensi dan mengurangkan pola artefak pergerakan dari sinyal PPG mentah
* **Augmentasi Data:** Untuk mencegah class imbalance di mana sebagian besar dataset merepresentasikan detak jantung saat rileks/duduk, terdapat tahap injeksi data sintetis dan probabilistic augmentation (data_generator_probabilistic_augmantation.py) serta pembuatan sampel detak jantung tinggi (data_generator_high_hr.py).
### 3.2 Tahap Inferensi
* **Downsampling:** Model KID-PPG membutuhkan i
* **Z-Score Normalization:** Setiap segmen aktivitas diseragamkan magnitudonya dengan teknik Z-score. Proses ini mencabut rentang dinamik sinyal optik yang ekstrem dengan mengurangi nilai rata-rata dan membaginya dengan standar deviasi
* **Buffering:**

## 4. Model
![architecture](Images/Architecture.png)
*Berikut adalah ringkasan data hasil simulasi/pengukuran:*

| Parameter | Target Spesifikasi | Hasil Pengukuran | Status |
| :--- | :--- | :--- | :--- |
| Tegangan Output | [Misal: 5V] | [...] | [...] |
| Arus | [Misal: 1A] | [...] | [...] |

## 5. Results
[Analisis data di atas. Apakah komponen bekerja sesuai ekspektasi? Jika ada kendala teknis (seperti *convergence error* pada SPICE atau fluktuasi tegangan), jelaskan di sini dan sebutkan langkah penyelesaiannya.]

## 6. Deployment
[Ringkas hasil akhir dari proyek atau eksperimen ini. Sebutkan langkah apa yang perlu dilakukan selanjutnya untuk iterasi desain atau perbaikan.]

### 6.1 Standart Metric Summary

### 6.2 Deployment Notes

## 7. Conclusion & Challenges