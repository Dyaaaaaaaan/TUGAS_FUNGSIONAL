"""Aplikasi 5: Daftar Tugas Kuliah."""
from Library.fplib import (
    append_item, average, count_by, group_by, remove_where, render_table,
    sort_by, update_where, validate_all, validate_non_empty,
)


def tambah_tugas(daftar, mata_kuliah, judul, prioritas):
    """Tambah tugas baru; mata kuliah dan judul wajib diisi."""
    cek = validate_all(
        validate_non_empty(mata_kuliah, "Mata kuliah"),
        validate_non_empty(judul, "Judul"),
    )
    if not cek[0]:
        return daftar, cek[1]
    tugas = {"mk": mata_kuliah, "judul": judul, "prioritas": prioritas, "selesai": False}
    return append_item(daftar, tugas), None


def tandai_selesai(daftar, judul):
    """Tandai tugas tertentu sebagai selesai."""
    return update_where(daftar, lambda t: t["judul"] == judul, selesai=True)


def hapus_selesai(daftar):
    """Hapus semua tugas yang sudah selesai."""
    return remove_where(daftar, lambda t: t["selesai"])


if __name__ == "__main__":
    daftar = ()
    daftar, _ = tambah_tugas(daftar, "Metopen", "Bab 3 proposal", 1)
    daftar, _ = tambah_tugas(daftar, "Web", "Demo Modul 2", 2)
    daftar, _ = tambah_tugas(daftar, "Mobile", "Layout login", 3)
    daftar, _ = tambah_tugas(daftar, "Web", "Laporan praktikum", 1)
    daftar, err = tambah_tugas(daftar, "", "Tanpa mata kuliah", 2)
    print("Error:", err)

    daftar = tandai_selesai(daftar, "Demo Modul 2")
    print("Total tugas:", count_by(daftar))
    print("Belum selesai:", count_by(daftar, lambda t: not t["selesai"]))
    print("Rata-rata prioritas:", average(t["prioritas"] for t in daftar))

    for mk, tugas in group_by(daftar, "mk").items():
        print(mk, "->", len(tugas), "tugas")

    print(render_table(sort_by(daftar, "prioritas"), ("mk", "judul", "prioritas", "selesai")))

    daftar = hapus_selesai(daftar)
    print("Setelah dibersihkan:", count_by(daftar))
