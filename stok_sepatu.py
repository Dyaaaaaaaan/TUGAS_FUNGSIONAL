
"""
Aplikasi 3: Stok Toko Sepatu.
Menggunakan Shared Library fplib.py
"""

from Library.fplib import (
    average,
    count_by,
    filter_by,
    format_rupiah,
    remove_where,
    sort_by,
    sum_by,
    update_where,
    validate_positive,
    with_updated,
)


def tambah_stok(stok, merek, ukuran, harga, jumlah):
    """Menambahkan barang baru ke dalam stok."""

    for ok, msg in (
        validate_positive(harga, "Harga"),
        validate_positive(jumlah, "Jumlah"),
    ):
        if not ok:
            return stok, msg

    barang = {
        "merek": merek,
        "ukuran": ukuran,
        "harga": harga,
        "jumlah": jumlah
    }

    return (*stok, barang), None


def restock(stok, merek, ukuran, tambahan):
    """Menambahkan stok tanpa mengubah data lama."""

    # Memastikan jumlah tambahan valid
    if not isinstance(tambahan, (int, float)) or tambahan <= 0:
        return stok

    # Mencari barang berdasarkan merek dan ukuran
    barang = next(
        (
            b for b in stok
            if b["merek"] == merek and b["ukuran"] == ukuran
        ),
        None
    )

    # Jika barang tidak ditemukan, stok tidak berubah
    if barang is None:
        return stok

    # Memperbarui jumlah stok
    return update_where(
        stok,
        lambda b: (
            b["merek"] == merek
            and b["ukuran"] == ukuran
        ),
        jumlah=barang["jumlah"] + tambahan
    )


def diskon(stok, merek, persen):
    """Memberikan diskon pada semua barang dari merek tertentu."""

    if not 0 <= persen <= 100:
        return stok

    return tuple(
        with_updated(
            b,
            harga=round(b["harga"] * (1 - persen / 100))
        )
        if b["merek"] == merek else b
        for b in stok
    )


def hapus_habis(stok):
    """Menghapus barang yang jumlah stoknya nol."""

    return remove_where(
        stok,
        lambda b: b["jumlah"] == 0
    )


if __name__ == "__main__":

    stok = ()

    # Menambahkan barang
    stok, _ = tambah_stok(
        stok, "Compass", 40, 300000, 5
    )

    stok, _ = tambah_stok(
        stok, "Ventela", 41, 250000, 0
    )

    stok, _ = tambah_stok(
        stok, "Compass", 42, 320000, 2
    )

    stok, _ = tambah_stok(
        stok, "Converse", 40, 900000, 4
    )

    # Menguji validasi harga
    stok, err = tambah_stok(
        stok, "Nike", 43, -1, 3
    )

    print("Error validasi:", err)

    # Menguji restock normal
    stok = restock(stok, "Compass", 40, 10)

    # Menguji barang yang tidak ditemukan
    stok = restock(stok, "Adidas", 42, 5)

    # Memberikan diskon Converse sebesar 10%
    stok = diskon(stok, "Converse", 10)

    print("\n=== MANAJEMEN STOK SEPATU ===")

    # Menghitung jumlah jenis barang
    print("Jumlah jenis barang:", count_by(stok))

    # Menghitung stok berdasarkan merek
    compass = filter_by(
        stok,
        lambda b: b["merek"] == "Compass"
    )

    print(
        "Total stok Compass:",
        sum_by(compass, "jumlah")
    )

    # Menghitung nilai stok
    print(
        "Total nilai stok:",
        format_rupiah(
            sum_by(
                map(
                    lambda b: {
                        "nilai": b["harga"] * b["jumlah"]
                    },
                    stok
                ),
                "nilai"
            )
        )
    )

    # Menghitung rata-rata harga
    print(
        "Rata-rata harga:",
        format_rupiah(
            average(b["harga"] for b in stok)
        )
    )

    # Menghapus barang dengan stok kosong
    stok = hapus_habis(stok)

    # Mengurutkan barang berdasarkan harga
    print("\n=== DAFTAR STOK SEPATU ===")

    for b in sort_by(stok, "harga"):
        print(
            b["merek"],
            "| Ukuran:", b["ukuran"],
            "| Harga:", format_rupiah(b["harga"]),
            "| Stok:", b["jumlah"]
        )
