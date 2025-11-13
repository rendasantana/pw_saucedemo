from bs4 import BeautifulSoup
import sys
import re

def safe_count(pattern, text):
    match = re.search(pattern, text)
    return int(match.group(1)) if match else 0

def validate_report(file_path="reports/report.html"):
    print("\n🔎 Menjalankan validasi report.html otomatis (final stage)...\n")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator=" ").lower()

        counts = {
            "passed": safe_count(r"(\d+)\s+passed", text),
            "failed": safe_count(r"(\d+)\s+failed", text),
            "error": safe_count(r"(\d+)\s+error", text),
            "skipped": safe_count(r"(\d+)\s+skipped", text),
            "xfailed": safe_count(r"(\d+)\s+xfailed", text),
            "xpassed": safe_count(r"(\d+)\s+xpassed", text),
        }

        print(f"✅ Passed: {counts['passed']}")
        print(f"❌ Failed: {counts['failed']}")
        print(f"⚠️ Error: {counts['error']}")
        print(f"⏭️ Skipped: {counts['skipped']}")
        print(f"🟡 XFailed: {counts['xfailed']}")
        print(f"🟢 XPassed: {counts['xpassed']}")

        total = sum(counts.values())
        if total == 0:
            print("⚠️ Tidak ada data test yang terdeteksi — pastikan report.html valid.")
            sys.exit(1)

        if counts["failed"] > 0 or counts["error"] > 0:
            print("❌ Validasi gagal: Ada test yang failed/error.")
            sys.exit(1)

        print("🎯 Semua test berhasil! Report valid.")
        sys.exit(0)

    except FileNotFoundError:
        print("❌ File report.html tidak ditemukan.")
        sys.exit(1)
    except Exception as e:
        print(f"⚠️ Terjadi error saat memvalidasi report: {e}")
        sys.exit(1)


if __name__ == "__main__":
    validate_report()
