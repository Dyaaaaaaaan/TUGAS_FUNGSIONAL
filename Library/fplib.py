"""
fplib.py
Library fungsi umum bergaya fungsional. Setiap fungsi dipakai minimal oleh 3 dari 5 aplikasi:
  1. Pemesanan Tiket Bioskop  (tiket_bioskop.py)
  2. Klinik Jadwal Dokter     (klinik_dokter.py)
  3. Stok Toko Sepatu         (stok_sepatu.py)
  4. Rental Kendaraan Kampus  (rental_kendaraan.py)
  5. Daftar Tugas Kuliah      (daftar_tugas.py)

Prinsip: fungsi murni, data immutable (tidak diubah, selalu menghasilkan data baru),
tanpa efek samping (input/output) di dalam library.
"""

from functools import reduce
from typing import Any, Callable, Iterable, Optional, Tuple

Record = dict
Predicate = Callable[[Any], bool]
Result = Tuple[bool, Optional[str]]


# --- Koleksi -----------------------------------------------------------------

def filter_by(items: Iterable, predicate: Predicate) -> tuple:
    """Item yang memenuhi predicate, dalam bentuk tuple baru."""
    return tuple(x for x in items if predicate(x))


def map_to(items: Iterable, transform: Callable) -> tuple:
    """Mengubah setiap item dengan fungsi transform."""
    return tuple(transform(x) for x in items)


def sum_by(items: Iterable, key: str) -> float:
    """Menjumlahkan field tertentu dari daftar record."""
    return sum(r[key] for r in items)


def count_by(items: Iterable, predicate: Predicate = lambda _: True) -> int:
    """Jumlah item yang memenuhi predicate."""
    return sum(1 for x in items if predicate(x))


def group_by(items: Iterable, key: str) -> dict:
    """Mengelompokkan record menjadi {nilai_field: tuple_record}."""
    return reduce(
        lambda acc, r: {**acc, r[key]: (*acc.get(r[key], ()), r)},
        items,
        {},
    )


def sort_by(items: Iterable, key: str, reverse: bool = False) -> tuple:
    """Mengurutkan record berdasarkan field, menghasilkan tuple baru."""
    return tuple(sorted(items, key=lambda r: r[key], reverse=reverse))


# --- Update record (immutable) -----------------------------------------------

def with_updated(record: Record, **changes) -> Record:
    """Record baru dengan perubahan field; record lama tetap."""
    return {**record, **changes}


def update_where(items: Iterable, predicate: Predicate, **changes) -> tuple:
    """Memperbarui record yang cocok, menghasilkan daftar baru."""
    return tuple(with_updated(r, **changes) if predicate(r) else r for r in items)


def remove_where(items: Iterable, predicate: Predicate) -> tuple:
    """Menghapus record yang cocok, menghasilkan daftar baru."""
    return tuple(r for r in items if not predicate(r))


def append_item(items: Iterable, item: Any) -> tuple:
    """Menambahkan item di akhir, menghasilkan tuple baru."""
    return (*items, item)


# --- Validasi (mengembalikan (berhasil, pesan_error)) -------------------------

def validate_non_empty(value: Any, field: str = "Field") -> Result:
    """Memastikan string tidak kosong."""
    if isinstance(value, str) and value.strip():
        return True, None
    return False, f"{field} tidak boleh kosong."


def validate_positive(value: float, field: str = "Nilai") -> Result:
    """Memastikan angka lebih dari nol."""
    if isinstance(value, (int, float)) and value > 0:
        return True, None
    return False, f"{field} harus lebih dari 0."


def validate_all(*results: Result) -> Result:
    """Gabungkan hasil validasi; gagal jika ada yang gagal."""
    errors = tuple(msg for ok, msg in results if not ok)
    return (False, " ".join(errors)) if errors else (True, None)


# --- Parsing & format --------------------------------------------------------

def safe_int(text: Any) -> Optional[int]:
    """String ke int; None jika gagal."""
    try:
        return int(str(text).strip())
    except ValueError:
        return None


def format_rupiah(amount: float) -> str:
    """15000 -> 'Rp 15.000'."""
    integer = int(round(amount))
    sign = "-" if integer < 0 else ""
    return f"{sign}Rp {abs(integer):,}".replace(",", ".")


def render_table(items: Iterable[Record], fields: Tuple[str, ...]) -> str:
    """Tabel teks sederhana dari daftar record."""
    rows = tuple(items)
    widths = tuple(max([len(f)] + [len(str(r.get(f, ""))) for r in rows]) for f in fields)

    def line(values: Iterable[str]) -> str:
        return " | ".join(v.ljust(w) for v, w in zip(values, widths))

    header = line(f.upper() for f in fields)
    divider = "-+-".join("-" * w for w in widths)
    body = tuple(line(str(r.get(f, "")) for f in fields) for r in rows)
    return "\n".join((header, divider, *body))


# --- Statistik ---------------------------------------------------------------

def average(values: Iterable[float]) -> Optional[float]:
    """Rata-rata; None jika kosong."""
    vals = tuple(values)
    return sum(vals) / len(vals) if vals else None
