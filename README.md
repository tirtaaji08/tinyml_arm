# Laporan Proyek 

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
* **Adaptive Filtering:**  sebuah model filter linier dilatih berulang-ulang secara spesifik hingga 16.000 epoch sebelum proses training utama dimulai. Filter ini menggunakan manipulasi Fast Fourier Transform (FFT) untuk menganalisis spektrum frekuensi dan mengurangkan pola artefak pergerakan dari sinyal PPG mentah
* **Augmentasi Data:** Untuk mencegah class imbalance di mana sebagian besar dataset merepresentasikan detak jantung saat rileks/duduk, terdapat tahap injeksi data sintetis dan probabilistic augmentation serta pembuatan sampel detak jantung tinggi.
### 3.2 Tahap Inferensi
* **Downsampling:**
* **Z-Score Normalization:** Setiap segmen aktivitas diseragamkan magnitudonya dengan teknik Z-score. Proses ini mencabut rentang dinamik sinyal optik yang ekstrem dengan mengurangi nilai rata-rata dan membaginya dengan standar deviasi
* **Buffering:**

## 4. Model
![architecture](Images/Architecture.png)  
**Parameters Count:**~112K Parameters  
**Input Shape:**[N, 256, 2]  
**Training Configuration:** 
* Optimizer: Menggunakan Adam Optimizer, yang merupakan standar paling optimal dan stabil untuk mengarahkan konvergensi bobot pada arsitektur yang menggunakan attention mechanism.

* Loss Function: Untuk model utamanya (versi probabilistik), fungsi objektif yang digunakan adalah Negative Log-Likelihood (NLL). Model ini tidak memprediksi nilai mutlak dari detak jantung, melainkan memprediksi parameter distribusi (rata-rata/ mean dan standar deviasi) untuk memberikan estimasi sekaligus tingkat ketidakpastiannya.

* Epochs: Terdapat dua fase iterasi dalam repositori ini:

    * Fase Preprocessing: Filter adaptif dilatih dalam iterasi yang sangat masif, yakni hingga 16.000 epoch.

    * Fase Training Utama: Pelatihan model deep learning-nya ditetapkan maksimal hingga 500 epoch per subjek (menggunakan metode Cross-Validation LOSO).

* Batch Size: Ditetapkan secara eksplisit sebesar 128 atau 256 sampel dalam setiap iterasi pembaruan bobot, memberikan keseimbangan yang baik antara pemanfaatan memori GPU dan kehalusan gradien.

## 5. Results


## 6. Deployment
    
### 6.1 Standart Metric Summary

| Sensor | Model Arch | Input Shape | Params | MAC | Sram Used | Accuracy Metric | Cycles Total | Quantization |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| PPG | 1D-CNN 3 block | [1, 256, 2] | ~112K | 13,450,768 MAC | 26.91 KiB | MAE: 5.3 BPM | 629117 | INT8 |

### 6.2 Deployment Notes

## 7. Conclusion & Challenges