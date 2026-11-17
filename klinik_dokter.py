"""Aplikasi 2: Klinik Jadwal Dokter."""
from Library.fplib import (
    average, count_by, group_by, map_to, render_table, safe_int,
    update_where, validate_all, validate_non_empty, validate_positive, with_updated,
)


def daftar_pasien(antrian, nama, umur_text, dokter):
    """Tambah pasien ke antrian; umur harus berupa angka."""
    umur = safe_int(umur_text)
    if umur is None:
        return antrian, "Umur harus angka."
    ok, err = validate_all(
        validate_non_empty(nama, "Nama"),
        validate_positive(umur, "Umur"),
    )
    if not ok:
        return antrian, err
    pasien = {"nama": nama, "umur": umur, "dokter": dokter, "status": "menunggu"}
    return (*antrian, pasien), None


def tandai_selesai(antrian, nama):
    """Ubah status pasien menjadi selesai (tanpa mengubah data lama)."""
    return update_where(antrian, lambda p: p["nama"] == nama, status="selesai")


def ganti_dokter(antrian, nama, dokter_baru):
    """Pindahkan pasien ke dokter lain."""
    return update_where(antrian, lambda p: p["nama"] == nama, dokter=dokter_baru)


if __name__ == "__main__":
    antrian = ()
    antrian, _ = daftar_pasien(antrian, "Rina", "34", "dr. Yoga")
    antrian, _ = daftar_pasien(antrian, "Dimas", "58", "dr. Ayu")
    antrian, _ = daftar_pasien(antrian, "Lia", "21", "dr. Yoga")
    antrian, err = daftar_pasien(antrian, "Tono", "abc", "dr. Ayu")
    print("Error:", err)
    antrian, err = daftar_pasien(antrian, "Eko", "-5", "dr. Ayu")
    print("Error:", err)

    antrian = tandai_selesai(antrian, "Rina")
    antrian = ganti_dokter(antrian, "Lia", "dr. Ayu")

    print("Jumlah pasien:", count_by(antrian))
    print("Menunggu:", count_by(antrian, lambda p: p["status"] == "menunggu"))
    print("Rata-rata umur:", round(average(map_to(antrian, lambda p: p["umur"])), 1))

    per_dokter = group_by(antrian, "dokter")
    for dokter, daftar in per_dokter.items():
        print(dokter, "->", len(daftar), "pasien")

    # Contoh with_updated: catatan tambahan untuk satu pasien
    pasien_pertama = with_updated(antrian[0], catatan="Kontrol ulang 2 minggu")
    print(render_table((pasien_pertama,), ("nama", "umur", "dokter", "status", "catatan")))
