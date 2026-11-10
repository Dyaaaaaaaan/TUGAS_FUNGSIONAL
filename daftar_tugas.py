
"""
Aplikasi 5: Daftar Tugas Kuliah.
Menggunakan Shared Library fplib.py
"""

from Library.fplib import (
    append_item,
    average,
    count_by,
    group_by,
    remove_where,
    render_table,
    safe_int,
    sort_by,
    update_where,
    validate_all,
    validate_non_empty,
)


def tambah_tugas(daftar, mata_kuliah, judul, prioritas):
    """Menambahkan tugas dengan validasi input."""

    # Mengubah prioritas menjadi integer
    prioritas = safe_int(prioritas)

    # Validasi prioritas
    if prioritas is None or prioritas <= 0:
        return daftar, "Prioritas harus berupa angka positif."

    # Validasi nama mata kuliah dan judul
    cek = validate_all(
        validate_non_empty(mata_kuliah, "Mata kuliah"),
        validate_non_empty(judul, "Judul"),
    )

    if not cek[0]:
        return daftar, cek[1]

    tugas = {
        "mk": mata_kuliah,
        "judul": judul,
        "prioritas": prioritas,
        "selesai": False
    }

    return append_item(daftar, tugas), None


def tandai_selesai(daftar, judul):
    """Menandai tugas sebagai selesai."""

    return update_where(
        daftar,
        lambda t: t["judul"] == judul,
        selesai=True
    )


def hapus_selesai(daftar):
    """Menghapus semua tugas yang sudah selesai."""

    return remove_where(
        daftar,
        lambda t: t["selesai"]
    )


if __name__ == "__main__":

    daftar = ()

    # Menambahkan beberapa tugas
    daftar, _ = tambah_tugas(
        daftar, "Metopen", "Bab 3 proposal", "1"
    )

    daftar, _ = tambah_tugas(
        daftar, "Web", "Demo Modul 2", "2"
    )

    daftar, _ = tambah_tugas(
        daftar, "Mobile", "Layout login", "3"
    )

    daftar, _ = tambah_tugas(
        daftar, "Web", "Laporan praktikum", "1"
    )

    # Menguji input tidak valid
    daftar, err = tambah_tugas(
        daftar, "", "Tanpa mata kuliah", "2"
    )

    print("Error validasi:", err)

    # Menguji safe_int
    daftar, err = tambah_tugas(
        daftar, "Python", "Latihan fungsi", "abc"
    )

    print("Error prioritas:", err)

    # Menandai tugas selesai
    daftar = tandai_selesai(
        daftar, "Demo Modul 2"
    )

    print("\n=== DAFTAR TUGAS KULIAH ===")

    # Menghitung seluruh tugas
    print("Total tugas:", count_by(daftar))

    # Menghitung tugas belum selesai
    print(
        "Belum selesai:",
        count_by(daftar, lambda t: not t["selesai"])
    )

    # Menghitung rata-rata prioritas
    print(
        "Rata-rata prioritas:",
        average(t["prioritas"] for t in daftar)
    )

    # Mengelompokkan berdasarkan mata kuliah
    print("\n=== KELOMPOK TUGAS ===")

    for mk, tugas in group_by(daftar, "mk").items():
        print(mk, "->", len(tugas), "tugas")

    # Mengurutkan berdasarkan prioritas
    print("\n=== TABEL TUGAS ===")

    print(
        render_table(
            sort_by(daftar, "prioritas"),
            ("mk", "judul", "prioritas", "selesai")
        )
    )

    # Menghapus tugas selesai
    daftar = hapus_selesai(daftar)

    print("\nSetelah tugas selesai dihapus:")
    print("Total tugas tersisa:", count_by(daftar))
