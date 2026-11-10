"""Aplikasi 4: Rental Kendaraan Kampus."""
from Library.fplib import (
    append_item, filter_by, format_rupiah, group_by, map_to, safe_int,
    sum_by, validate_all, validate_non_empty, validate_positive, with_updated,
)


def sewa(riwayat, peminjam, kendaraan, tarif_text, hari_text):
    """Catat penyewaan baru; tarif dan hari harus angka positif."""
    tarif = safe_int(tarif_text)
    hari = safe_int(hari_text)
    cek = validate_all(
        validate_non_empty(peminjam, "Peminjam"),
        validate_non_empty(kendaraan, "Kendaraan"),
        validate_positive(tarif or 0, "Tarif"),
        validate_positive(hari or 0, "Lama sewa"),
    )
    if not cek[0]:
        return riwayat, cek[1]
    transaksi = {"peminjam": peminjam, "kendaraan": kendaraan,
                 "tarif": tarif, "hari": hari, "selesai": False,
                 "total": tarif * hari}
    return append_item(riwayat, transaksi), None


def kembalikan(riwayat, peminjam):
    """Menandai sewa atas nama peminjam sebagai sudah dikembalikan."""
    return tuple(
        with_updated(t, selesai=True) if t["peminjam"] == peminjam else t
        for t in riwayat
    )


if __name__ == "__main__":
    riwayat = ()
    riwayat, _ = sewa(riwayat, "Fajar", "Honda Beat", "50000", "2")
    riwayat, _ = sewa(riwayat, "Maya", "Yamaha NMAX", "80000", "1")
    riwayat, _ = sewa(riwayat, "Fajar", "Yamaha NMAX", "80000", "3")
    riwayat, err = sewa(riwayat, "Rudi", "Honda Beat", "abc", "1")
    print("Error:", err)

    riwayat = kembalikan(riwayat, "Maya")

    aktif = filter_by(riwayat, lambda t: not t["selesai"])
    print("Sedang disewa:", len(aktif))
    print("Total pendapatan:", format_rupiah(sum_by(riwayat, "total")))
    print("Daftar kendaraan:", map_to(riwayat, lambda t: t["kendaraan"]))

    per_peminjam = group_by(riwayat, "peminjam")
    for nama, daftar in per_peminjam.items():
        print(nama, "->", format_rupiah(sum_by(daftar, "total")))
