from bs4 import BeautifulSoup
import sys
import os
from typing import List, Optional

def validate_report(file_path: str = "reports/report.html") -> None:
    print("\n🔎 Menjalankan validasi report.html otomatis...")

    if not os.path.exists(file_path):
        print("❌ File report.html tidak ditemukan.")
        sys.exit(1)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, "html.parser")

        # Cari tabel hasil test (pytest-html v2/v3/v4)
        summary_table = (
            soup.find("table", id="results-table") or 
            soup.find("table", id="results-table-1") or
            soup.find("table", class_="results-table")
        )

        if not summary_table:
            print("⚠️ Tidak ditemukan tabel hasil test di report.html.")
            sys.exit(1)

        rows = summary_table.find_all("tr")
        total_tests = len(rows) - 1  # baris header

        # Aman untuk row.get("class")
        def has_class(row, name: str) -> bool:
            classes = row.get("class", [])
            if not isinstance(classes, list):
                return False
            return name in classes

        passed  = len([r for r in rows if has_class(r, "passed")])
        failed  = len([r for r in rows if has_class(r, "failed")])
        error   = len([r for r in rows if has_class(r, "error")])
        skipped = len([r for r in rows if has_class(r, "skipped")])
        xfailed = len([r for r in rows if has_class(r, "xfailed")])
        xpassed = len([r for r in rows if has_class(r, "xpassed")])

        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️ Error: {error}")
        print(f"⏭️ Skipped: {skipped}")
        print(f"🟡 XFailed: {xfailed}")
        print(f"🟢 XPassed: {xpassed}")

        if total_tests <= 0:
            print("⚠️ Tidak ada data test yang terdeteksi — report.html kemungkinan rusak.")
            sys.exit(1)

        if failed > 0 or error > 0:
            print("❌ Validasi gagal: Ada test gagal atau error.")
            sys.exit(1)

        print("🎯 Semua test berhasil! Report valid.")
        sys.exit(0)

    except Exception as e:
        print(f"⚠️ Terjadi error saat validasi report: {e}")
        sys.exit(1)


if __name__ == "__main__":
    validate_report()
