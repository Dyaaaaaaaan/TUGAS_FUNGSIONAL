"""Aplikasi 3: Stok Toko Sepatu."""
from Library.fplib import (
    average, count_by, filter_by, format_rupiah, map_to, remove_where, safe_int,
    sort_by, sum_by, update_where, validate_all, validate_non_empty,
    validate_positive, with_updated,
)


def tambah_stok(stok, merek, ukuran_text, harga_text, jumlah_text):
    """Menambah barang baru ke stok; harga dan jumlah boleh berupa teks.
    Mengembalikan (stok_baru, error)."""
    ukuran, harga, jumlah = safe_int(ukuran_text), safe_int(harga_text), safe_int(jumlah_text)
    cek = validate_all(
        validate_non_empty(merek, "Merek"),
        validate_positive(ukuran, "Ukuran"),
        validate_positive(harga, "Harga"),
        validate_positive(jumlah, "Jumlah"),
    )
    if not cek[0]:
        return stok, cek[1]
    barang = {"merek": merek, "ukuran": ukuran, "harga": harga, "jumlah": jumlah}
    return (*stok, barang), None


def restock(stok, merek, ukuran, tambahan):
    """Menambah jumlah satu jenis barang tanpa mengubah stok lama.
    Barang yang tidak ditemukan dibiarkan (stok dikembalikan apa adanya)."""
    cocok = lambda b: b["merek"] == merek and b["ukuran"] == ukuran
    ditemukan = filter_by(stok, cocok)
    if not ditemukan:
        return stok
    return update_where(stok, cocok, jumlah=ditemukan[0]["jumlah"] + tambahan)


def diskon(stok, merek, persen):
    """Menurunkan harga semua barang satu merek."""
    return tuple(
        with_updated(b, harga=round(b["harga"] * (1 - persen / 100)))
        if b["merek"] == merek else b
        for b in stok
    )


def hapus_habis(stok):
    """Menghapus barang yang stoknya nol."""
    return remove_where(stok, lambda b: b["jumlah"] == 0)


def nilai_stok(stok):
    """Total nilai persediaan = jumlah harga x jumlah barang."""
    return sum_by(map_to(stok, lambda b: {"nilai": b["harga"] * b["jumlah"]}), "nilai")


if __name__ == "__main__":
    stok = ()
    stok, _ = tambah_stok(stok, "Compass", "40", "300000", "5")
    stok, _ = tambah_stok(stok, "Ventela", "41", "250000", "0x")   # jumlah tidak valid
    stok, _ = tambah_stok(stok, "Compass", "42", "320000", "2")
    stok, _ = tambah_stok(stok, "Converse", "40", "900000", "4")
    stok, err = tambah_stok(stok, "Nike", "43", "-1", "3")
    print("Error:", err)
    stok, err = tambah_stok(stok, "Adidas", "43", "abc", "3")
    print("Error:", err)

    stok = restock(stok, "Compass", 40, 10)
    stok = restock(stok, "Puma", 40, 10)          # tidak ada -> stok tetap
    stok = diskon(stok, "Converse", 10)

    print("Jumlah jenis barang:", count_by(stok))
    print("Stok Compass:", sum_by(filter_by(stok, lambda b: b["merek"] == "Compass"), "jumlah"))
    print("Nilai stok:", format_rupiah(nilai_stok(stok)))
    print("Rata-rata harga:", format_rupiah(average(b["harga"] for b in stok)))

    stok = hapus_habis(stok)
    for b in sort_by(stok, "harga"):
        print(b["merek"], b["ukuran"], format_rupiah(b["harga"]))
