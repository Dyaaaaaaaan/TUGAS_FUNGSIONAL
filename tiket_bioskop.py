"""Aplikasi 1: Pemesanan Tiket Bioskop."""
from Library.fplib import (
    append_item, filter_by, format_rupiah, map_to, remove_where,
    render_table, sort_by, sum_by, validate_all, validate_non_empty, validate_positive,
)


def pesan_tiket(bookings, nama, film, harga, jumlah):
    """Validasi lalu tambahkan pesanan baru (menghasilkan daftar baru)."""
    cek = validate_all(
        validate_non_empty(nama, "Nama"),
        validate_non_empty(film, "Film"),
        validate_positive(harga, "Harga"),
        validate_positive(jumlah, "Jumlah"),
    )
    if not cek[0]:
        return bookings, cek[1]
    pesanan = {"nama": nama, "film": film, "harga": harga, "jumlah": jumlah,
               "total": harga * jumlah}
    return append_item(bookings, pesanan), None


def batalkan(bookings, nama):
    """Hapus semua pesanan atas nama tertentu."""
    return remove_where(bookings, lambda p: p["nama"] == nama)


if __name__ == "__main__":
    bookings = ()
    bookings, _ = pesan_tiket(bookings, "Budi", "Laskar Pelangi", 45000, 2)
    bookings, _ = pesan_tiket(bookings, "Sari", "Dune", 50000, 1)
    bookings, _ = pesan_tiket(bookings, "Andi", "Dune", 50000, 3)
    bookings, err = pesan_tiket(bookings, "", "Dune", 50000, 1)
    print("Error:", err)

    dune = filter_by(bookings, lambda p: p["film"] == "Dune")
    print("Pemesanan Dune:", len(dune))
    print("Total pendapatan:", format_rupiah(sum_by(bookings, "total")))
    print("Nama pemesan:", map_to(bookings, lambda p: p["nama"]))

    bookings = batalkan(bookings, "Sari")
    print(render_table(sort_by(bookings, "total", reverse=True),
                       ("nama", "film", "jumlah", "total")))
