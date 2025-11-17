import logging
import base64
from datetime import datetime
from pathlib import Path
import pytest
import os
from bs4 import BeautifulSoup

# ==========================
# GLOBAL SETUP
# ==========================
def pytest_configure(config):
    """Buat folder laporan dan setup logger global"""
    Path("reports/screenshots").mkdir(parents=True, exist_ok=True)
    Path("reports/videos").mkdir(parents=True, exist_ok=True)
    Path("reports/logs").mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("reports/logs/global_log.txt", mode="a", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

# ==========================
# PER-TEST LOGGER
# ==========================
@pytest.fixture(scope="function", autouse=True)
def per_test_logger(request):
    """Buat logger unik untuk setiap test"""
    log_file = Path(f"reports/logs/{request.node.name}.log")
    handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger = logging.getLogger(request.node.name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    yield logger
    handler.close()
    logger.removeHandler(handler)

# ==========================
# RECORD PAGE FIXTURE
# ==========================
@pytest.fixture(scope="function")
def record_page(browser, request):
    """Buka page baru dengan video recording"""
    videos_dir = Path("reports/videos")
    videos_dir.mkdir(parents=True, exist_ok=True)

    context = browser.new_context(record_video_dir=str(videos_dir))
    page = context.new_page()
    yield page

    try:
        page.close()
        context.close()
    except Exception as e:
        logging.warning(f"Gagal menutup context/video: {e}")

# ==========================
# HOOK UNTUK HTML REPORT
# ==========================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Tambahkan screenshot, video, dan log di report"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when != "call":
        return

    page = item.funcargs.get("page") or item.funcargs.get("record_page")
    pytest_html = item.config.pluginmanager.getplugin("html")
    if not pytest_html:
        return

    status_icon = "✅" if rep.passed else "❌"
    duration = f"{rep.duration:.2f}s"

    # --- SCREENSHOT ---
    screenshot_path = Path("reports/screenshots") / f"{item.name}_{datetime.now():%Y%m%d_%H%M%S}.png"
    encoded_img = ""
    try:
        if page and not page.is_closed():
            page.screenshot(path=screenshot_path, full_page=True)
            with open(screenshot_path, "rb") as f:
                encoded_img = base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        logging.warning(f"Gagal ambil screenshot: {e}")

    # --- VIDEO ---
    encoded_video = ""
    video_message = ""
    try:
        video_path = None
        if page and hasattr(page, "video") and page.video:
            try:
                video_path = page.video.path()
            except Exception:
                pass

        if video_path and Path(video_path).is_file() and Path(video_path).stat().st_size > 1024:
            with open(video_path, "rb") as v:
                encoded_video = base64.b64encode(v.read()).decode("utf-8")
        else:
            video_message = "⚠️ Video tidak tersedia (file kosong atau gagal direkam)"
    except Exception as e:
        video_message = f"⚠️ Gagal memuat video: {e}"

    if encoded_video:
        video_html = f"""
        <video width="100%" controls style="border-radius:8px;">
            <source src="data:video/webm;base64,{encoded_video}" type="video/webm">
            Browser tidak mendukung video.
        </video>
        """
    else:
        video_html = f"""
        <div style="background:#2a2a2a; color:#ffcc00; padding:10px; border-radius:6px; text-align:center;">
            {video_message}
        </div>
        """

    # --- LOG ---
    log_file = Path(f"reports/logs/{item.name}.log")
    log_html = "Tidak ada log."
    if log_file.exists():
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            formatted = []
            for line in lines:
                color = "#ccc"
                if "ERROR" in line:
                    color = "#ff6b6b"
                elif "WARNING" in line:
                    color = "#ffd166"
                elif "INFO" in line:
                    color = "#06d6a0"
                formatted.append(f'<span style="color:{color};">{line.strip()}</span>')
            log_html = "<br>".join(formatted[-60:])

    # --- HTML TEST RESULT ---
    html_block = f"""
<div class="summary-box">
  <b>{status_icon} {item.name}</b> &nbsp;&nbsp; ⏱ {duration}
  <button id="btn-{item.name}" class="toggle-detail" onclick="toggleDetail('{item.name}')">
    Lihat Detail ⬇️
  </button>
</div>

<div id="detail-{item.name}" class="detail-content">
  <div class="flex-container">
    <div class="flex-item" style="text-align:center;">
      <b>📸 Screenshot:</b><br>
      <img src="data:image/png;base64,{encoded_img}" style="max-width:100%; border-radius:8px;">
    </div>

    <div class="flex-item" style="text-align:center;">
      <b>🎥 Video Test:</b><br>
      {video_html}
    </div>

    <div class="flex-item">
      <b>🧾 Log:</b><br>
      <div style="font-family:monospace; max-height:200px; overflow:auto;">{log_html}</div>
    </div>
  </div>
</div>
"""

    extras = getattr(rep, "extras", [])
    extras.append(pytest_html.extras.html(html_block))
    rep.extras = extras

# ==========================
# JS + CSS UNTUK HTML REPORT
# ==========================
def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([ """
    <script>
    function toggleDetail(name) {
      const el = document.getElementById('detail-' + name);
      const btn = document.getElementById('btn-' + name);
      if (!el || !btn) return;
      const visible = el.style.display === 'block';
      el.style.display = visible ? 'none' : 'block';
      btn.innerHTML = visible ? 'Lihat Detail ⬇️' : 'Sembunyikan Detail ⬆️';
    }
    </script>

    <style>
    .summary-box {
      background:#222;
      border-left:6px solid #0078d4;
      color:#fff;
      padding:8px 12px;
      border-radius:8px;
      font-family:Segoe UI, sans-serif;
      margin-top:10px;
    }
    .toggle-detail {
      background:#0078d4;
      color:white;
      border:none;
      border-radius:6px;
      padding:4px 10px;
      cursor:pointer;
      font-size:12px;
      transition: background-color 0.2s ease;
    }
    .toggle-detail:hover {
      background:#005ea6;
    }
    .detail-content {
      display:none;
      margin-top:10px;
      border:1px solid #333;
      border-radius:8px;
      padding:10px;
      background:#111;
    }
    .flex-container {
      display:flex;
      flex-wrap:wrap;
      gap:15px;
      justify-content:space-between;
    }
    .flex-item {
      flex:1;
      min-width:250px;
      background:#1b1b1b;
      padding:8px;
      border-radius:8px;
      color:#dcdcdc;
    }
    </style>
    """ ])

# ==========================
# VALIDASI HTML REPORT SESI AKHIR
# ==========================
def pytest_sessionfinish(session, exitstatus):
    report_path = os.path.join(session.config.rootdir, "reports", "report.html")
    if not os.path.exists(report_path):
        print("⚠️ report.html tidak ditemukan!")
        return

    with open(report_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    passed  = len(soup.select("tr.passed"))
    failed  = len(soup.select("tr.failed"))
    error   = len(soup.select("tr.error"))
    skipped = len(soup.select("tr.skipped"))
    xfailed = len(soup.select("tr.xfailed"))
    xpassed = len(soup.select("tr.xpassed"))

    total = passed + failed + skipped + error + xfailed + xpassed
    if total == 0:
        print("⚠️ Tidak ada test terdeteksi di HTML report.")
        return

    print(f"✅ Passed : {passed}")
    print(f"❌ Failed : {failed}")
    print(f"⚠️ Error  : {error}")
    print(f"⏭️ Skipped: {skipped}")
    print(f"🟡 XFailed: {xfailed}")
    print(f"🟢 XPassed: {xpassed}")
    print("📊 Validasi HTML report selesai!")
