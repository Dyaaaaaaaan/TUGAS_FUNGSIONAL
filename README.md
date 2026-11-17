# Tugas Pemrograman Fungsional: Satu Library, Lima Aplikasi

`Library/fplib.py` berisi fungsi umum bergaya fungsional (pure, data immutable, tanpa I/O).
Setiap fungsi dipakai minimal oleh 3 dari 5 aplikasi.

## Menjalankan (dari folder ini)
```
python tiket_bioskop.py
python klinik_dokter.py
python stok_sepatu.py
python rental_kendaraan.py
python daftar_tugas.py
```

## Pemakaian fungsi library
| Fungsi | Aplikasi |
|---|---|
| `filter_by` | rental_kendaraan, stok_sepatu, tiket_bioskop (3) |
| `map_to` | klinik_dokter, rental_kendaraan, stok_sepatu, tiket_bioskop (4) |
| `sum_by` | rental_kendaraan, stok_sepatu, tiket_bioskop (3) |
| `count_by` | daftar_tugas, klinik_dokter, stok_sepatu (3) |
| `group_by` | daftar_tugas, klinik_dokter, rental_kendaraan (3) |
| `sort_by` | daftar_tugas, stok_sepatu, tiket_bioskop (3) |
| `with_updated` | klinik_dokter, rental_kendaraan, stok_sepatu (3) |
| `update_where` | daftar_tugas, klinik_dokter, stok_sepatu (3) |
| `remove_where` | daftar_tugas, stok_sepatu, tiket_bioskop (3) |
| `append_item` | daftar_tugas, rental_kendaraan, tiket_bioskop (3) |
| `validate_non_empty` | daftar_tugas, klinik_dokter, rental_kendaraan, stok_sepatu, tiket_bioskop (5) |
| `validate_positive` | klinik_dokter, rental_kendaraan, stok_sepatu, tiket_bioskop (4) |
| `validate_all` | daftar_tugas, klinik_dokter, rental_kendaraan, stok_sepatu, tiket_bioskop (5) |
| `safe_int` | klinik_dokter, rental_kendaraan, stok_sepatu (3) |
| `format_rupiah` | rental_kendaraan, stok_sepatu, tiket_bioskop (3) |
| `render_table` | daftar_tugas, klinik_dokter, tiket_bioskop (3) |
| `average` | daftar_tugas, klinik_dokter, stok_sepatu (3) |
