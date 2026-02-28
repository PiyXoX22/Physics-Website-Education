import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Fisika Pelajar & Mahasiswa (Fisikawan)",
    page_icon="📘",
    layout="wide"
)

st.title("📘 Fisika Interaktif – SMA sampai level Kuliah")
st.write("Fisika klasik → modern | penjelasan, grafik, simulasi, singularitas")


mode = st.sidebar.selectbox(
    "🎓 Mode Belajar",
    ["SMA", "Kuliah", "Fisikawan"]
)

menu = st.sidebar.radio(
    "Pilih Menu",
    [
        "🏫 Gerak",
        "⚡ Dinamika",
        "🔋 Energi & Usaha",
        "📈 Grafik Gerak",
        "🎓 Topik Kuliah",
        "🌊 Fluida",
        "⚡ Listrik & Magnet",
        "📡 Medan Listrik (Gauss)",
        "🌌 Relativitas",
        "🧮 Kalkulus Fisika",
        "⚙️ Mekanika Lagrange",
        "🧠 Mekanika Hamilton",
        "🧲 Persamaan Maxwell",
        "⚛️ Mekanika Kuantum",
        "🌊 Navier–Stokes"
    ]
)


# =======================
# GERAK
# =======================
if menu == "🏫 Gerak":
    st.header("Gerak Lurus – GLB & GLBB")

    # =========================
    # MODE BELAJAR (KONSEPTUAL)
    # =========================
    if mode == "SMA":
        st.info("""
        🧑‍🎓 **Mode SMA**
        - Pakai rumus jadi
        - Tanpa turunan / integral
        """)

    elif mode == "Kuliah":
        st.info("""
        🎓 **Mode Kuliah**
        - Gerak sebagai fungsi waktu
        - Diturunkan dari definisi v = dx/dt
        """)

    else:  # Fisikawan
        st.warning("""
        🧠 **Fisikawan**
        - Diskretisasi waktu
        - Limit dt → 0
        - Awal kegagalan fisika klasik
        """)

    jenis = st.selectbox(
        "Pilih Jenis Gerak",
        ["GLB (Kecepatan Konstan)", "GLBB (Percepatan Konstan)"]
    )

    t_max = st.slider("Waktu maksimum (s)", 1, 20, 10)
    t = np.linspace(0, t_max, 200)
    dt = t[1] - t[0]

    # =========================
    # GLB
    # =========================
    if jenis == "GLB (Kecepatan Konstan)":
        v = st.number_input("Kecepatan v (m/s)", value=2.0)
        x0 = st.number_input("Posisi awal x₀ (m)", value=0.0)

        # ===== MODE SMA =====
        if mode == "SMA":
            st.latex("x(t) = x_0 + vt")
            x = x0 + v * t

        # ===== MODE KULIAH =====
        elif mode == "Kuliah":
            st.latex("x(t) = \\int v\\,dt")
            v_t = np.full_like(t, v)
            x = np.cumsum(v_t) * dt + x0

        # ===== Fisikawan =====
        else:
            st.latex("x_{n+1} = x_n + v\\Delta t")
            x = np.zeros_like(t)
            x[0] = x0
            for i in range(len(t) - 1):
                x[i+1] = x[i] + v * dt

        fig, ax = plt.subplots()
        ax.plot(t, x)
        ax.set_xlabel("Waktu (s)")
        ax.set_ylabel("Posisi (m)")
        ax.set_title("GLB")
        ax.grid()
        st.pyplot(fig)

        with st.expander("📌 Asumsi & Batas Model"):
            st.markdown("""
            **Asumsi:**
            - v konstan
            - Tidak ada gaya
            - Ruang & waktu kontinu

            **Batas Model:**
            - Gagal jika v berubah
            - Tidak berlaku relativistik
            """)

    # =========================
    # GLBB
    # =========================
    else:
        v0 = st.number_input("Kecepatan awal v₀ (m/s)", value=0.0)
        a = st.number_input("Percepatan a (m/s²)", value=1.0)
        x0 = st.number_input("Posisi awal x₀ (m)", value=0.0)

        # ===== MODE SMA =====
        if mode == "SMA":
            st.latex("x(t) = x_0 + v_0 t + \\frac12 at^2")
            x = x0 + v0 * t + 0.5 * a * t**2
            v = v0 + a * t

        # ===== MODE KULIAH =====
        elif mode == "Kuliah":
            st.latex("""
            v(t) = v_0 + at \\\\
            x(t) = \\int v(t) dt
            """)
            v = v0 + a * t
            x = np.cumsum(v) * dt + x0

        # ===== Fisikawan =====
        else:
            st.latex("""
            v_{n+1} = v_n + a\\Delta t \\\\
            x_{n+1} = x_n + v_n\\Delta t
            """)
            x = np.zeros_like(t)
            v = np.zeros_like(t)
            x[0] = x0
            v[0] = v0

            for i in range(len(t) - 1):
                v[i+1] = v[i] + a * dt
                x[i+1] = x[i] + v[i] * dt

        fig, ax = plt.subplots()
        ax.plot(t, x, label="Posisi x(t)")
        ax.plot(t, v, label="Kecepatan v(t)")
        ax.set_xlabel("Waktu (s)")
        ax.legend()
        ax.set_title("GLBB")
        ax.grid()
        st.pyplot(fig)

        with st.expander("📌 Asumsi & Batas Model"):
            st.markdown("""
            **Asumsi:**
            - a konstan
            - Sistem 1D
            - Waktu kontinu

            **Batas Model:**
            - Gagal untuk gaya berubah waktu
            - Tidak berlaku di skala atom
            - Digantikan Lagrange/Hamilton
            """)


# =======================
# DINAMIKA
# =======================
elif menu == "⚡ Dinamika":
    st.header("Dinamika – Hukum II Newton")

    # =========================
    # MODE BELAJAR
    # =========================
    if mode == "SMA":
        st.info("""
        🧑‍🎓 **Mode SMA**
        - Pakai F = ma langsung
        - Fokus hasil percepatan & grafik
        """)

    elif mode == "Kuliah":
        st.info("""
        🎓 **Mode Kuliah**
        - Percepatan sebagai turunan kecepatan
        - Gerak diturunkan dari definisi
        """)

    else:  # Fisikawan
        st.warning("""
        🧠 **Fisikawan**
        - Diskretisasi waktu
        - Hukum Newton sebagai limit
        - Dasar menuju Lagrange
        """)

    # =========================
    # INPUT
    # =========================
    st.latex("F = ma")

    m = st.number_input("Massa m (kg)", value=1.0)
    F = st.number_input("Gaya F (N)", value=1.0)

    if m == 0:
        st.error("Massa tidak boleh 0")
        st.stop()

    a = F / m
    st.success(f"Percepatan a = {a:.2f} m/s²")

    v0 = st.number_input("Kecepatan awal v₀ (m/s)", value=0.0)
    x0 = st.number_input("Posisi awal x₀ (m)", value=0.0)

    t_max = st.slider("Waktu maksimum (s)", 1, 20, 10)
    t = np.linspace(0, t_max, 200)
    dt = t[1] - t[0]

    # =========================
    # PERHITUNGAN SESUAI MODE
    # =========================

    # ===== MODE SMA =====
    if mode == "SMA":
        st.latex("""
        v(t) = v_0 + at \\\\
        x(t) = x_0 + v_0 t + \\frac{1}{2} a t^2
        """)
        v = v0 + a * t
        x = x0 + v0 * t + 0.5 * a * t**2

    # ===== MODE KULIAH =====
    elif mode == "Kuliah":
        st.latex("""
        a = \\frac{dv}{dt}, \\quad
        v = \\int a\\,dt, \\quad
        x = \\int v\\,dt
        """)
        v = v0 + a * t
        x = np.cumsum(v) * dt + x0

    # ===== Fisikawan =====
    else:
        st.latex("""
        v_{n+1} = v_n + \\frac{F}{m}\\Delta t \\\\
        x_{n+1} = x_n + v_n\\Delta t
        """)
        v = np.zeros_like(t)
        x = np.zeros_like(t)

        v[0] = v0
        x[0] = x0

        for i in range(len(t) - 1):
            v[i+1] = v[i] + a * dt
            x[i+1] = x[i] + v[i] * dt

    # =========================
    # GRAFIK
    # =========================
    fig, ax = plt.subplots()
    ax.plot(t, x, label="Posisi x(t)")
    ax.plot(t, v, label="Kecepatan v(t)")
    ax.set_xlabel("Waktu (s)")
    ax.legend()
    ax.set_title("Gerak Akibat Gaya Konstan")
    ax.grid()
    st.pyplot(fig)

    # =========================
    # INTERPRETASI
    # =========================
    st.info("""
    🔍 **Makna Fisika**
    - Gaya konstan → percepatan konstan
    - v(t) linear
    - x(t) parabola
    """)

    if F == 0:
        st.warning("""
        ⚠️ **Kasus Khusus: F = 0**
        - a = 0
        - Hukum I Newton (inersia)
        """)

    # =========================
    # ASUMSI & BATAS MODEL
    # =========================
    with st.expander("📌 Asumsi & Batas Model"):
        st.markdown("""
        **Asumsi:**
        - Massa konstan
        - Gaya konstan
        - Sistem satu dimensi
        - Waktu kontinu

        **Batas Model:**
        - Gagal untuk gaya berubah waktu
        - Tidak berlaku relativistik
        - Digantikan oleh Lagrange/Hamilton
        """)



# =======================
# ENERGI
# =======================
elif menu == "🔋 Energi & Usaha":
    st.header("Energi & Usaha")

    # =========================
    # MODE BELAJAR
    # =========================
    if mode == "SMA":
        st.info("""
        🧑‍🎓 **Mode SMA**
        - Energi sebagai rumus
        - Fokus perhitungan angka
        """)

    elif mode == "Kuliah":
        st.info("""
        🎓 **Mode Kuliah**
        - Energi diturunkan dari dinamika
        - Usaha sebagai integral gaya
        """)

    else:  # Fisikawan
        st.warning("""
        🧠 **Fisikawan**
        - Energi muncul dari simetri waktu
        - Kekekalan = Teorema Noether
        - Bukan hukum fundamental
        """)

    konsep = st.selectbox(
        "Pilih Konsep",
        [
            "Energi Kinetik",
            "Energi Potensial Gravitasi",
            "Usaha oleh Gaya",
            "Kekekalan Energi (Jatuh Bebas)"
        ]
    )

    g = 9.8

    # =========================
    # ENERGI KINETIK
    # =========================
    if konsep == "Energi Kinetik":
        m = st.number_input("Massa m (kg)", value=1.0)
        v = st.number_input("Kecepatan v (m/s)", value=2.0)

        if mode == "SMA":
            st.latex("E_k = \\frac{1}{2}mv^2")
            Ek = 0.5 * m * v**2

        elif mode == "Kuliah":
            st.latex("E_k = \\int F\\,dx = \\int m a\\,dx")
            Ek = 0.5 * m * v**2
            st.caption("Hasil integral Newton")

        else:  # Fisikawan
            st.latex("E_k = -\\frac{\\partial L}{\\partial t}")
            Ek = 0.5 * m * v**2
            st.caption("Energi sebagai generator waktu")

        st.success(f"Energi Kinetik = {Ek:.2f} J")

        with st.expander("📌 Asumsi & Batas Model"):
            st.markdown("""
            **Asumsi:**
            - Massa konstan
            - Tidak relativistik

            **Batas Model:**
            - Gagal saat v → c
            - Diganti energi relativistik
            """)

    # =========================
    # ENERGI POTENSIAL
    # =========================
    elif konsep == "Energi Potensial Gravitasi":
        m = st.number_input("Massa m (kg)", value=1.0)
        h = st.number_input("Ketinggian h (m)", value=5.0)

        if mode == "SMA":
            st.latex("E_p = mgh")
            Ep = m * g * h

        elif mode == "Kuliah":
            st.latex("E_p = -\\int F\\,dh")
            Ep = m * g * h
            st.caption("Potensial dari gaya konservatif")

        else:  # Fisikawan
            st.latex("V(q) \\subset L = T - V")
            Ep = m * g * h
            st.caption("Energi potensial bagian dari Lagrangian")

        st.success(f"Energi Potensial = {Ep:.2f} J")

        with st.expander("📌 Asumsi & Batas Model"):
            st.markdown("""
            **Asumsi:**
            - Medan gravitasi seragam
            - Gaya konservatif

            **Batas Model:**
            - Tidak berlaku untuk GR
            - Tidak berlaku di kosmologi
            """)

    # =========================
    # USAHA
    # =========================
    elif konsep == "Usaha oleh Gaya":
        F = st.number_input("Gaya F (N)", value=2.0)
        s = st.number_input("Perpindahan s (m)", value=3.0)

        if mode == "SMA":
            st.latex("W = F \\cdot s")
            W = F * s

        elif mode == "Kuliah":
            st.latex("W = \\int \\vec{F}\\cdot d\\vec{r}")
            W = F * s
            st.caption("Kasus gaya konstan")

        else:  # Fisikawan
            st.latex("W = \\Delta E")
            W = F * s
            st.caption("Usaha = perubahan generator waktu")

        st.success(f"Usaha = {W:.2f} J")

        with st.expander("📌 Asumsi & Batas Model"):
            st.markdown("""
            **Asumsi:**
            - Gaya konstan
            - Gerak searah gaya

            **Batas Model:**
            - Tidak berlaku untuk gaya non-konservatif
            - Perlu pendekatan energi disipatif
            """)

    # =========================
    # KEKEKALAN ENERGI
    # =========================
    else:
        m = st.number_input("Massa m (kg)", value=1.0)
        h0 = st.number_input("Ketinggian awal (m)", value=10.0)

        t = np.linspace(0, np.sqrt(2*h0/g), 300)
        dt = t[1] - t[0]

        h = h0 - 0.5 * g * t**2
        h[h < 0] = 0
        v = g * t

        Ep = m * g * h
        Ek = 0.5 * m * v**2
        E_total = Ep + Ek

        fig, ax = plt.subplots()
        ax.plot(t, Ep, label="Energi Potensial")
        ax.plot(t, Ek, label="Energi Kinetik")
        ax.plot(t, E_total, "--", label="Energi Total")
        ax.set_xlabel("Waktu (s)")
        ax.set_ylabel("Energi (J)")
        ax.legend()
        ax.set_title("Kekekalan Energi")
        ax.grid()
        st.pyplot(fig)

        if mode == "Fisikawan":
            st.warning("""
            🧠 **Fisikawan Insight**
            - Kekekalan energi muncul karena simetri waktu
            - Jika hukum berubah terhadap waktu → energi tidak kekal
            """)

        with st.expander("📌 Asumsi & Batas Model"):
            st.markdown("""
            **Asumsi:**
            - Sistem tertutup
            - Tidak ada gesekan
            - Waktu homogen

            **Batas Model:**
            - Energi tidak selalu kekal (GR, kosmologi)
            - Simetri waktu bisa patah
            """)


# =======================
# GRAFIK
# =======================
elif menu == "📈 Grafik Gerak":
    st.header("Grafik Gerak (x–t, v–t, a–t)")

    # =========================
    # MODE BELAJAR
    # =========================
    if mode == "SMA":
        st.info("""
        🧑‍🎓 **Mode SMA**
        - Membaca grafik
        - Hubungan visual antar besaran
        """)

    elif mode == "Kuliah":
        st.info("""
        🎓 **Mode Kuliah**
        - Grafik sebagai turunan & integral
        - Hubungan matematis antar kurva
        """)

    else:  # Fisikawan
        st.warning("""
        🧠 **Fisikawan**
        - Grafik hasil diskretisasi
        - Makna limit Δt → 0
        - Error numerik selalu ada
        """)

    jenis = st.selectbox(
        "Pilih Jenis Gerak",
        ["GLB (a = 0)", "GLBB (a ≠ 0)"]
    )

    t_max = st.slider("Waktu maksimum (s)", 1, 20, 10)
    t = np.linspace(0, t_max, 300)
    dt = t[1] - t[0]

    # =========================
    # GLB
    # =========================
    if jenis == "GLB (a = 0)":
        v = st.number_input("Kecepatan v (m/s)", value=2.0)
        x0 = st.number_input("Posisi awal x₀ (m)", value=0.0)

        if mode == "SMA":
            x = x0 + v * t
            v_t = np.full_like(t, v)
            a = np.zeros_like(t)

        elif mode == "Kuliah":
            v_t = np.full_like(t, v)
            x = np.cumsum(v_t) * dt + x0
            a = np.gradient(v_t, t)

        else:  # Fisikawan
            x = np.zeros_like(t)
            v_t = np.full_like(t, v)
            a = np.zeros_like(t)
            x[0] = x0
            for i in range(len(t) - 1):
                x[i+1] = x[i] + v * dt

    # =========================
    # GLBB
    # =========================
    else:
        v0 = st.number_input("Kecepatan awal v₀ (m/s)", value=0.0)
        a_const = st.number_input("Percepatan a (m/s²)", value=1.0)
        x0 = st.number_input("Posisi awal x₀ (m)", value=0.0)

        if mode == "SMA":
            a = np.full_like(t, a_const)
            v_t = v0 + a_const * t
            x = x0 + v0 * t + 0.5 * a_const * t**2

        elif mode == "Kuliah":
            a = np.full_like(t, a_const)
            v_t = v0 + a_const * t
            x = np.cumsum(v_t) * dt + x0

        else:  # Fisikawan
            a = np.full_like(t, a_const)
            v_t = np.zeros_like(t)
            x = np.zeros_like(t)
            v_t[0] = v0
            x[0] = x0
            for i in range(len(t) - 1):
                v_t[i+1] = v_t[i] + a_const * dt
                x[i+1] = x[i] + v_t[i] * dt

    # =========================
    # PLOT
    # =========================
    fig, axs = plt.subplots(3, 1, figsize=(6, 8), sharex=True)

    axs[0].plot(t, x)
    axs[0].set_ylabel("Posisi x (m)")
    axs[0].grid()

    axs[1].plot(t, v_t)
    axs[1].set_ylabel("Kecepatan v (m/s)")
    axs[1].grid()

    axs[2].plot(t, a)
    axs[2].set_ylabel("Percepatan a (m/s²)")
    axs[2].set_xlabel("Waktu (s)")
    axs[2].grid()

    st.pyplot(fig)

    # =========================
    # INTERPRETASI
    # =========================
    if mode == "SMA":
        st.info("""
        🔍 **Cara Membaca Grafik**
        - Grafik x–t miring → benda bergerak
        - v–t datar → kecepatan tetap
        - a–t nol → tidak ada percepatan
        """)

    elif mode == "Kuliah":
        st.info("""
        🔍 **Makna Matematis**
        - Kemiringan x–t = v
        - Kemiringan v–t = a
        - Luas v–t = perpindahan
        """)

    else:
        st.warning("""
        🧠 **Fisikawan Insight**
        - Grafik bukan kontinu, tapi diskret
        - Turunan ≈ beda hingga
        - Integral ≈ penjumlahan numerik
        """)


# =======================
# TOPIK KULIAH
# =======================
elif menu == "🎓 Topik Kuliah":
    st.header("Topik Kuliah – Momentum, Impuls & Limit")

    # =========================
    # MODE BELAJAR
    # =========================
    if mode == "SMA":
        st.info("""
        🧑‍🎓 **Mode SMA**
        - Momentum sebagai hasil perkalian
        - Fokus perhitungan angka
        """)

    elif mode == "Kuliah":
        st.info("""
        🎓 **Mode Kuliah**
        - Momentum sebagai besaran vektor
        - Terkait hukum kekekalan
        """)

    else:  # Fisikawan
        st.warning("""
        🧠 **Fisikawan**
        - Momentum muncul dari simetri ruang
        - Konsekuensi Teorema Noether
        - Lebih fundamental dari gaya
        """)

    topik = st.selectbox(
        "Pilih Konsep",
        [
            "Momentum Linear",
            "Impuls & Perubahan Momentum",
            "Kekekalan Momentum (Tumbukan)",
            "Limit & Kasus Ekstrem"
        ]
    )

    # =========================
    # MOMENTUM
    # =========================
    if topik == "Momentum Linear":
        m = st.number_input("Massa m (kg)", value=1.0)
        v = st.number_input("Kecepatan v (m/s)", value=2.0)

        if mode == "SMA":
            st.latex("p = mv")
            p = m * v

        elif mode == "Kuliah":
            st.latex("\\vec{p} = m\\vec{v}")
            p = m * v
            st.caption("Momentum adalah besaran vektor")

        else:  # Fisikawan
            st.latex("p = \\frac{\\partial L}{\\partial \\dot{q}}")
            p = m * v
            st.caption("Momentum kanonik dari Lagrangian")

        st.success(f"Momentum = {p:.2f} kg·m/s")

        with st.expander("📌 Asumsi & Batas Model"):
            st.markdown("""
            **Asumsi:**
            - Massa konstan
            - Tidak relativistik

            **Batas Model:**
            - Diganti momentum relativistik saat v → c
            """)

    # =========================
    # IMPULS
    # =========================
    elif topik == "Impuls & Perubahan Momentum":
        F = st.number_input("Gaya F (N)", value=10.0)
        dt = st.number_input("Durasi gaya Δt (s)", value=0.1)

        if mode == "SMA":
            st.latex("J = F\\Delta t")
            J = F * dt

        elif mode == "Kuliah":
            st.latex("J = \\int F\\,dt")
            J = F * dt
            st.caption("Kasus gaya konstan")

        else:  # Fisikawan
            st.latex("\\Delta p = J")
            J = F * dt
            st.caption("Impuls sebagai perubahan momentum")

        st.success(f"Impuls = {J:.2f} N·s")

        with st.expander("📌 Asumsi & Batas Model"):
            st.markdown("""
            **Asumsi:**
            - Gaya konstan
            - Interval waktu singkat

            **Batas Model:**
            - Tidak berlaku untuk gaya kontinu panjang
            """)

    # =========================
    # KEKEKALAN MOMENTUM
    # =========================
    elif topik == "Kekekalan Momentum (Tumbukan)":
        m1 = st.number_input("m₁ (kg)", value=1.0)
        v1 = st.number_input("v₁ (m/s)", value=2.0)
        m2 = st.number_input("m₂ (kg)", value=1.0)
        v2 = st.number_input("v₂ (m/s)", value=0.0)

        p_awal = m1*v1 + m2*v2
        st.success(f"Momentum total awal = {p_awal:.2f} kg·m/s")

        if mode == "Fisikawan":
            st.warning("""
            🧠 **Fisikawan Insight**
            Kekekalan momentum muncul karena:
            - hukum fisika tidak berubah terhadap translasi ruang
            """)

        with st.expander("📌 Asumsi & Batas Model"):
            st.markdown("""
            **Asumsi:**
            - Sistem tertutup
            - Tidak ada gaya eksternal

            **Batas Model:**
            - Tidak berlaku pada sistem terbuka
            """)

    # =========================
    # LIMIT & KASUS EKSTREM
    # =========================
    else:
        st.subheader("Limit & Kasus Ekstrem")

        st.markdown("""
        ### 1️⃣ Massa → 0
        \\[
        p = mv \\rightarrow 0
        \\]

        ### 2️⃣ Kecepatan Tinggi
        Mekanika klasik gagal saat:
        \\[
        v \\to c
        \\]

        Momentum relativistik:
        \\[
        p = \\gamma mv
        \\]
        """)

        if mode == "Fisikawan":
            st.warning("""
            🧠 **Fisikawan Insight**
            - Momentum klasik bukan fundamental
            - Struktur ruang-waktu menentukan bentuknya
            """)

        with st.expander("📌 Asumsi & Batas Model"):
            st.markdown("""
            **Asumsi:**
            - Ruang datar
            - Waktu absolut

            **Batas Model:**
            - Diganti relativitas khusus
            """)



# =======================
# FLUIDA
# =======================
elif menu == "🌊 Fluida":
    st.header("Fluida Dinamis – Persamaan Bernoulli")

    # =========================
    # MODE BELAJAR
    # =========================
    if mode == "SMA":
        st.info("""
        🧑‍🎓 **Mode SMA**
        - Bernoulli sebagai rumus energi
        - Fokus perbandingan dua titik
        """)

    elif mode == "Kuliah":
        st.info("""
        🎓 **Mode Kuliah**
        - Bernoulli dari usaha & kekekalan energi
        - Berlaku sepanjang streamline
        """)

    else:  # Fisikawan
        st.warning("""
        🧠 **Fisikawan**
        - Bernoulli = solusi khusus Navier–Stokes
        - Hanya berlaku untuk fluida ideal
        - Model runtuh saat turbulensi
        """)

    st.markdown("""
    Persamaan Bernoulli:
    \\[
    P + \\frac{1}{2}\\rho v^2 + \\rho g h = \\text{konstan}
    \\]
    """)

    rho = st.number_input("Massa jenis fluida ρ (kg/m³)", value=1000.0)
    g = 9.8

    st.subheader("Titik 1")
    v1 = st.number_input("Kecepatan v₁ (m/s)", value=1.0)
    h1 = st.number_input("Ketinggian h₁ (m)", value=0.0)
    P1 = st.number_input("Tekanan P₁ (Pa)", value=101325.0)

    st.subheader("Titik 2")
    v2 = st.number_input("Kecepatan v₂ (m/s)", value=2.0)
    h2 = st.number_input("Ketinggian h₂ (m)", value=0.0)

    # =========================
    # PERHITUNGAN
    # =========================
    P2 = P1 + 0.5 * rho * (v1**2 - v2**2) + rho * g * (h1 - h2)

    st.success(f"Tekanan di titik 2 (P₂) = {P2:.2f} Pa")

    # =========================
    # INTERPRETASI SESUAI MODE
    # =========================
    if mode == "SMA":
        st.info("""
        🔍 **Interpretasi (SMA)**
        - Aliran makin cepat → tekanan turun
        - Energi fluida berpindah bentuk
        """)

    elif mode == "Kuliah":
        st.info("""
        🔍 **Interpretasi (Kuliah)**
        - Suku tekanan ↔ energi potensial tekanan
        - Suku kecepatan ↔ energi kinetik fluida
        - Suku ketinggian ↔ energi potensial gravitasi
        """)

    else:
        st.warning("""
        🧠 **Fisikawan Insight**
        - Tidak ada istilah kehilangan energi
        - Tidak ada viskositas
        - Tidak ada turbulensi
        - Ini fluida IDEAL (fiksi matematis)
        """)

    if v2 > v1:
        st.warning("""
        ⚠️ Efek Venturi:
        - Penampang mengecil → v naik → P turun
        """)

    # =========================
    # ASUMSI & BATAS MODEL
    # =========================
    with st.expander("📌 Asumsi & Batas Model"):
        st.markdown("""
        **Asumsi:**
        - Fluida tak termampatkan
        - Viskositas diabaikan
        - Aliran stasioner
        - Sepanjang satu streamline

        **Batas Model:**
        - Tidak berlaku untuk turbulensi
        - Gagal pada fluida kental
        - Digantikan oleh Navier–Stokes
        """)


# =======================
# LISTRIK & MAGNET
# =======================
elif menu == "⚡ Listrik & Magnet":
    st.header("Listrik & Magnet – Arus, Energi & Batas Model")

    # =========================
    # MODE BELAJAR
    # =========================
    if mode == "SMA":
        st.info("""
        🧑‍🎓 **Mode SMA**
        - Listrik sebagai rangkaian
        - Fokus V, I, R
        """)

    elif mode == "Kuliah":
        st.info("""
        🎓 **Mode Kuliah**
        - Arus sebagai respons medan listrik
        - Daya sebagai laju energi
        """)

    else:  # Fisikawan
        st.warning("""
        🧠 **Fisikawan**
        - Hukum Ohm bukan hukum alam
        - Hanya aproksimasi material
        - Digantikan teori medan & kuantum
        """)

    konsep = st.selectbox(
        "Pilih Konsep",
        [
            "Hukum Ohm",
            "Daya Listrik",
            "Batas Berlaku Hukum Ohm"
        ]
    )

    # =========================
    # HUKUM OHM
    # =========================
    if konsep == "Hukum Ohm":
        I = st.number_input("Arus I (Ampere)", value=1.0)
        R = st.number_input("Hambatan R (Ohm)", value=5.0)

        if mode == "SMA":
            st.latex("V = IR")
            V = I * R

        elif mode == "Kuliah":
            st.latex("J = \\sigma E")
            st.caption("Versi mikroskopik Hukum Ohm")
            V = I * R

        else:  # Fisikawan
            st.latex("\\vec{J} = nq\\vec{v}_d")
            st.caption("Arus dari gerak pembawa muatan")
            V = I * R

        st.success(f"Tegangan V = {V:.2f} Volt")

        with st.expander("📌 Asumsi & Batas Model"):
            st.markdown("""
            **Asumsi:**
            - Material ohmik
            - Suhu konstan
            - Medan listrik lemah

            **Batas Model:**
            - Gagal pada medan kuat
            - Gagal pada skala atom
            """)

    # =========================
    # DAYA LISTRIK
    # =========================
    elif konsep == "Daya Listrik":
        V = st.number_input("Tegangan V (Volt)", value=10.0)
        I = st.number_input("Arus I (Ampere)", value=2.0)

        if mode == "SMA":
            st.latex("P = VI")
            P = V * I

        elif mode == "Kuliah":
            st.latex("P = I^2 R")
            P = V * I
            st.caption("Energi listrik → panas")

        else:  # Fisikawan
            st.latex("P = \\int \\vec{J}\\cdot\\vec{E}\\, dV")
            P = V * I
            st.caption("Daya sebagai kerja medan")

        st.success(f"Daya Listrik = {P:.2f} Watt")

        with st.expander("📌 Asumsi & Batas Model"):
            st.markdown("""
            **Asumsi:**
            - Arus stasioner
            - R konstan

            **Batas Model:**
            - Tidak berlaku pada AC kompleks
            - Tidak mencakup radiasi EM
            """)

    # =========================
    # BATAS HUKUM OHM
    # =========================
    else:
        st.subheader("Batas Berlaku Hukum Ohm")

        st.markdown("""
        Hukum Ohm **BUKAN hukum fundamental**.

        Berlaku jika:
        - material ohmik
        - suhu stabil
        - medan listrik kecil

        Tidak berlaku untuk:
        - dioda
        - transistor
        - superkonduktor
        - plasma
        """)

        if mode == "Fisikawan":
            st.warning("""
            🧠 **Fisikawan Insight**
            - Tidak ada Hukum Ohm di vakum
            - Arus muncul dari struktur material
            - Elektrodinamika lebih fundamental
            """)

        with st.expander("📌 Asumsi & Batas Model"):
            st.markdown("""
            **Asumsi:**
            - Medium material
            - Elektron klasik

            **Batas Model:**
            - Digantikan mekanika kuantum
            - Terhubung ke Persamaan Maxwell
            """)


# =======================
# GAUSS
# =======================
elif menu == "📡 Medan Listrik (Gauss)":
    st.header("Hukum Gauss – Medan Listrik & Simetri")

    # =========================
    # MODE BELAJAR
    # =========================
    if mode == "SMA":
        st.info("""
        🧑‍🎓 **Mode SMA**
        - Gauss sebagai cara cepat hitung E
        - Fokus simetri & rumus jadi
        """)

    elif mode == "Kuliah":
        st.info("""
        🎓 **Mode Kuliah**
        - Gauss sebagai hukum medan
        - Hubungan divergensi & muatan
        """)

    else:  # Fisikawan
        st.warning("""
        🧠 **Fisikawan**
        - Gauss = salah satu Persamaan Maxwell
        - Pernyataan lokal tentang struktur ruang
        """)

    st.latex("\\oint \\vec{E}\\cdot d\\vec{A} = \\frac{Q_{dalam}}{\\varepsilon_0}")

    kasus = st.selectbox(
        "Pilih Kasus Simetri",
        [
            "Muatan Titik / Bola Simetris",
            "Garis Muatan Tak Hingga",
            "Bidang Bermuatan Tak Hingga"
        ]
    )

    eps0 = 8.854e-12

    # =========================
    # MUATAN TITIK / BOLA
    # =========================
    if kasus == "Muatan Titik / Bola Simetris":
        st.latex("E = \\frac{Q}{4\\pi\\varepsilon_0 r^2}")

        Q = st.number_input("Muatan Q (C)", value=1e-6)
        r = st.number_input("Jari-jari r (m)", min_value=0.0001, value=1.0)

        E = Q / (4 * np.pi * eps0 * r**2)
        st.success(f"Medan listrik E = {E:.2e} N/C")

        if mode == "SMA":
            st.info("""
            🔍 Medan makin jauh → makin lemah  
            Pola seperti gaya gravitasi
            """)

        elif mode == "Kuliah":
            st.info("""
            🔍 Simetri bola:
            - Medan radial
            - Divergensi nol di luar muatan
            """)

        else:
            st.warning("""
            🧠 **Fisikawan Insight**
            - Singularitas di r → 0
            - Medan klasik runtuh
            """)

    # =========================
    # GARIS MUATAN
    # =========================
    elif kasus == "Garis Muatan Tak Hingga":
        st.latex("E = \\frac{\\lambda}{2\\pi\\varepsilon_0 r}")

        lam = st.number_input("Rapat muatan λ (C/m)", value=1e-6)
        r = st.number_input("Jarak r (m)", min_value=0.0001, value=1.0)

        E = lam / (2 * np.pi * eps0 * r)
        st.success(f"Medan listrik E = {E:.2e} N/C")

        if mode == "Kuliah":
            st.caption("Hasil dari simetri silinder")

        if mode == "Fisikawan":
            st.warning("""
            🧠 **Fisikawan Insight**
            - Objek tak hingga tidak fisik
            - Aproksimasi lokal saja
            """)

    # =========================
    # BIDANG MUATAN
    # =========================
    else:
        st.latex("E = \\frac{\\sigma}{2\\varepsilon_0}")

        sigma = st.number_input("Rapat muatan σ (C/m²)", value=1e-6)

        E = sigma / (2 * eps0)
        st.success(f"Medan listrik E = {E:.2e} N/C")

        if mode == "SMA":
            st.info("Medan konstan di semua jarak")

        if mode == "Fisikawan":
            st.warning("""
            🧠 **Fisikawan Insight**
            - Medan tak hingga → energi tak hingga
            - Model ideal matematis
            """)

    # =========================
    # ASUMSI & BATAS MODEL
    # =========================
    with st.expander("📌 Asumsi & Batas Model"):
        st.markdown("""
        **Asumsi:**
        - Medan statik
        - Vakum
        - Simetri tinggi
        - Muatan kontinu

        **Batas Model:**
        - Tidak berlaku untuk sistem acak
        - Gagal di skala atom
        - Digantikan elektrodinamika kuantum
        """)


# =======================
# RELATIVITAS
# =======================
elif menu == "🌌 Relativitas":
    st.header("Relativitas Khusus – Energi & Momentum")

    # =========================
    # MODE BELAJAR
    # =========================
    if mode == "SMA":
        st.info("""
        🧑‍🎓 **Mode SMA**
        - Fokus pada E = mc²
        - Relativitas sebagai koreksi fisika klasik
        """)

    elif mode == "Kuliah":
        st.info("""
        🎓 **Mode Kuliah**
        - Energi & momentum satu kesatuan
        - Ruang dan waktu tidak absolut
        """)

    else:  # Fisikawan
        st.warning("""
        🧠 **Fisikawan**
        - Relativitas = struktur ruang-waktu
        - Energi & momentum berasal dari simetri
        """)

    # =========================
    # RUMUS DASAR
    # =========================
    if mode == "SMA":
        st.latex("E = mc^2")
    else:
        st.latex("E^2 = (pc)^2 + (mc^2)^2")
        st.latex("\\gamma = \\frac{1}{\\sqrt{1 - v^2/c^2}}")

    # =========================
    # INPUT
    # =========================
    m = st.number_input("Massa diam m (kg)", value=1.0)
    c = 3e8
    v = st.slider("Kecepatan v (m/s)", 0.0, 2.99e8, 0.0)

    if v >= c:
        st.error("❌ Kecepatan tidak boleh ≥ kecepatan cahaya")
    else:
        gamma = 1 / np.sqrt(1 - (v**2 / c**2))

        E0 = m * c**2
        E = gamma * E0
        p = gamma * m * v

        # =========================
        # OUTPUT
        # =========================
        st.success(f"Energi diam E₀ = {E0:.2e} J")

        if mode != "SMA":
            st.success(f"Energi total E = {E:.2e} J")
            st.success(f"Momentum relativistik p = {p:.2e} kg·m/s")

        # =========================
        # INTERPRETASI SESUAI MODE
        # =========================
        if mode == "SMA":
            st.info("""
            🔍 **Interpretasi (SMA)**
            - Massa bisa berubah jadi energi
            - Berlaku pada reaksi nuklir
            """)

        elif mode == "Kuliah":
            st.info("""
            🔍 **Interpretasi (Kuliah)**
            - Energi dan momentum membentuk 4-vektor
            - Hukum kekekalan tetap berlaku
            """)

        else:
            st.warning("""
            🧠 **Fisikawan Insight**
            - Tidak ada konsep gaya fundamental
            - Gerak = geodesik ruang-waktu
            - Massa hanyalah parameter invarian
            """)

    # =========================
    # ASUMSI & BATAS MODEL
    # =========================
    with st.expander("📌 Asumsi & Batas Model"):
        st.markdown("""
        **Asumsi:**
        - Kerangka inersial
        - Ruang-waktu datar (tanpa gravitasi)
        - Kecepatan cahaya konstan

        **Batas Model:**
        - Tidak mencakup gravitasi (→ Relativitas Umum)
        - Tidak berlaku di skala kuantum ekstrem
        - Perlu QFT untuk partikel elementer
        """)

# =======================
# KALKULUS
# =======================
elif menu == "🧮 Kalkulus Fisika":
    st.header("Kalkulus dalam Fisika – Bahasa Perubahan")

    # =========================
    # MODE BELAJAR
    # =========================
    if mode == "SMA":
        st.info("""
        🧑‍🎓 **Mode SMA**
        - Turunan = kemiringan grafik
        - Integral = luas daerah
        """)

    elif mode == "Kuliah":
        st.info("""
        🎓 **Mode Kuliah**
        - Turunan = laju perubahan fisis
        - Integral = akumulasi besaran
        """)

    else:  # Fisikawan
        st.warning("""
        🧠 **Fisikawan**
        - Turunan & integral adalah operator
        - Fisika = struktur diferensial
        """)

    konsep = st.selectbox(
        "Pilih Konsep",
        [
            "Turunan: Kecepatan dari Posisi",
            "Turunan: Percepatan dari Kecepatan",
            "Integral: Posisi dari Kecepatan"
        ]
    )

    t_max = st.slider("Waktu maksimum (s)", 1, 20, 10)
    t = np.linspace(0, t_max, 200)

    # =========================
    # TURUNAN POSISI → KECEPATAN
    # =========================
    if konsep == "Turunan: Kecepatan dari Posisi":
        st.latex("v(t) = \\frac{ds}{dt}")

        fungsi = st.selectbox(
            "Pilih fungsi posisi s(t)",
            ["s = t²", "s = t³", "s = sin(t)"]
        )

        if fungsi == "s = t²":
            s = t**2
            teks = "s(t) = t²"
        elif fungsi == "s = t³":
            s = t**3
            teks = "s(t) = t³"
        else:
            s = np.sin(t)
            teks = "s(t) = sin(t)"

        v = np.gradient(s, t)

        fig, ax = plt.subplots()
        ax.plot(t, s, label="Posisi s(t)")
        ax.plot(t, v, label="Kecepatan v(t)")
        ax.legend()
        ax.set_xlabel("Waktu (s)")
        ax.set_title(f"Turunan: {teks}")
        ax.grid()

        st.pyplot(fig)

        if mode == "Fisikawan":
            st.warning("""
            🧠 **Fisikawan Insight**
            - Turunan gagal di titik diskontinu
            - Gerak patah → fisika klasik runtuh
            """)

    # =========================
    # TURUNAN KECEPATAN → PERCEPATAN
    # =========================
    elif konsep == "Turunan: Percepatan dari Kecepatan":
        st.latex("a(t) = \\frac{dv}{dt}")

        v = t**2
        a = np.gradient(v, t)

        fig, ax = plt.subplots()
        ax.plot(t, v, label="Kecepatan v(t)")
        ax.plot(t, a, label="Percepatan a(t)")
        ax.legend()
        ax.set_xlabel("Waktu (s)")
        ax.set_title("Turunan Kecepatan → Percepatan")
        ax.grid()

        st.pyplot(fig)

        if mode == "Kuliah":
            st.caption("Percepatan = turunan kedua posisi")

        if mode == "Fisikawan":
            st.warning("""
            🧠 **Fisikawan Insight**
            - Gaya = operator diferensial
            - Dinamika = persamaan diferensial
            """)

    # =========================
    # INTEGRAL KECEPATAN → POSISI
    # =========================
    else:
        st.latex("s(t) = \\int v(t) \\, dt")

        v = 2 * t
        dt = t[1] - t[0]
        s = np.cumsum(v) * dt

        fig, ax = plt.subplots()
        ax.plot(t, v, label="Kecepatan v(t)")
        ax.plot(t, s, label="Posisi s(t)")
        ax.legend()
        ax.set_xlabel("Waktu (s)")
        ax.set_title("Integral: Luas di bawah grafik v–t")
        ax.grid()

        st.pyplot(fig)

        if mode == "Fisikawan":
            st.warning("""
            🧠 **Fisikawan Insight**
            - Integral = solusi persamaan gerak
            - Aksi minimum = integral Lagrangian
            """)

    # =========================
    # ASUMSI & BATAS MODEL
    # =========================
    with st.expander("📌 Asumsi & Batas Model"):
        st.markdown("""
        **Asumsi:**
        - Fungsi kontinu
        - Waktu kontinu
        - Tidak ada lompatan instan

        **Batas Model:**
        - Gagal pada skala Planck
        - Tidak berlaku untuk proses diskret
        - Digantikan kalkulus kuantum / operator
        """)


# =======================
# LAGRANGE
# =======================
elif menu == "⚙️ Mekanika Lagrange":
    st.header("Mekanika Lagrange – Osilator Harmonik")

    # =========================
    # MODE BELAJAR
    # =========================
    if mode == "SMA":
        st.info("""
        🧑‍🎓 **Mode SMA**
        - Gerak osilasi (pegas)
        - Fokus hasil gerak, bukan turunan rumus
        """)

    elif mode == "Kuliah":
        st.info("""
        🎓 **Mode Kuliah**
        - Dinamika dari prinsip aksi minimum
        - Gaya bukan konsep utama
        """)

    else:  # Fisikawan
        st.warning("""
        🧠 **Fisikawan**
        - Lagrangian = objek fundamental
        - Dinamika muncul dari simetri
        - Dasar mekanika kuantum & medan
        """)

    st.markdown("""
    **Lagrangian sistem:**
    \\[
    L = T - V = \\frac{1}{2}m\\dot{x}^2 - \\frac{1}{2}kx^2
    \\]
    """)

    # =========================
    # INPUT PARAMETER
    # =========================
    m = st.number_input("Massa m (kg)", value=1.0)
    k = st.number_input("Konstanta pegas k (N/m)", value=1.0)

    x0 = st.number_input("Posisi awal x₀ (m)", value=1.0)
    v0 = st.number_input("Kecepatan awal v₀ (m/s)", value=0.0)

    t_max = st.slider("Waktu maksimum (s)", 5, 50, 20)
    dt = 0.01
    t = np.arange(0, t_max, dt)

    # =========================
    # PERSAMAAN LAGRANGE
    # d/dt(∂L/∂ẋ) − ∂L/∂x = 0
    # → m x¨ + kx = 0
    # =========================
    x = np.zeros(len(t))
    v = np.zeros(len(t))

    x[0] = x0
    v[0] = v0

    for i in range(len(t) - 1):
        a = -(k / m) * x[i]
        v[i+1] = v[i] + a * dt
        x[i+1] = x[i] + v[i] * dt

    # =========================
    # GRAFIK
    # =========================
    fig, ax = plt.subplots()
    ax.plot(t, x, label="Posisi x(t)")
    ax.plot(t, v, label="Kecepatan v(t)")
    ax.set_xlabel("Waktu (s)")
    ax.legend()
    ax.set_title("Dinamika dari Persamaan Lagrange")
    ax.grid()

    st.pyplot(fig)

    omega = np.sqrt(k / m)
    st.success(f"Frekuensi sudut ω = {omega:.2f} rad/s")

    # =========================
    # INTERPRETASI SESUAI MODE
    # =========================
    if mode == "SMA":
        st.info("""
        🔍 **Interpretasi (SMA)**
        - Gerak bolak-balik periodik
        - Semakin k besar → osilasi makin cepat
        """)

    elif mode == "Kuliah":
        st.info("""
        🔍 **Interpretasi (Kuliah)**
        - Semua informasi gerak ada di L
        - Tidak perlu gaya eksplisit
        """)

    else:
        st.warning("""
        🧠 **Fisikawan Insight**
        - Koordinat bisa diganti (invarian)
        - Momentum kanonik muncul alami
        - Prinsip aksi minimum lebih fundamental dari Newton
        """)

    # =========================
    # ASUMSI & BATAS MODEL
    # =========================
    with st.expander("📌 Asumsi & Batas Model"):
        st.markdown("""
        **Asumsi:**
        - Sistem konservatif
        - Pegas ideal (linier)
        - Tidak ada redaman

        **Batas Model:**
        - Gagal untuk gesekan
        - Gagal untuk sistem non-linier kuat
        - Digeneralisasi ke Hamiltonian & medan
        """)

    st.caption("Catatan numerik: integrasi Euler sederhana (bukan symplectic)")


# =======================
# HAMILTON
# =======================
elif menu == "🧠 Mekanika Hamilton":
    st.header("Mekanika Hamilton – Osilator Harmonik")

    # =========================
    # MODE BELAJAR
    # =========================
    if mode == "SMA":
        st.info("""
        🧑‍🎓 **Mode SMA**
        - Gerak dilihat sebagai lintasan
        - Energi tetap selama osilasi
        """)

    elif mode == "Kuliah":
        st.info("""
        🎓 **Mode Kuliah**
        - Dinamika di ruang fase (q,p)
        - Hukum gerak dari Hamiltonian
        """)

    else:  # Fisikawan
        st.warning("""
        🧠 **Fisikawan**
        - Hamiltonian = generator waktu
        - Struktur simetri & konservasi
        - Dasar mekanika kuantum
        """)

    st.markdown("""
    **Hamiltonian sistem:**
    \\[
    H(q,p) = \\frac{p^2}{2m} + \\frac{1}{2} k q^2
    \\]
    """)

    st.latex("\\dot{q} = \\frac{\\partial H}{\\partial p}, \\quad \\dot{p} = -\\frac{\\partial H}{\\partial q}")

    # =========================
    # INPUT PARAMETER
    # =========================
    m = st.number_input("Massa m (kg)", value=1.0)
    k = st.number_input("Konstanta pegas k (N/m)", value=1.0)

    q0 = st.number_input("Posisi awal q₀", value=1.0)
    p0 = st.number_input("Momentum awal p₀", value=0.0)

    t_max = st.slider("Waktu maksimum (s)", 5, 50, 20)
    dt = 0.01
    t = np.arange(0, t_max, dt)

    # =========================
    # INTEGRASI HAMILTON
    # =========================
    q = np.zeros(len(t))
    p = np.zeros(len(t))

    q[0] = q0
    p[0] = p0

    for i in range(len(t) - 1):
        dqdt = p[i] / m
        dpdt = -k * q[i]

        q[i+1] = q[i] + dqdt * dt
        p[i+1] = p[i] + dpdt * dt

    # =========================
    # GRAFIK RUANG FASE
    # =========================
    fig, ax = plt.subplots()
    ax.plot(q, p)
    ax.set_xlabel("Koordinat q")
    ax.set_ylabel("Momentum p")
    ax.set_title("Ruang Fase – Dinamika Hamilton")
    ax.grid()

    st.pyplot(fig)

    # =========================
    # ENERGI HAMILTONIAN
    # =========================
    H = p**2/(2*m) + 0.5*k*q**2
    st.line_chart(H)

    st.caption("Energi Hamiltonian (harus hampir konstan)")

    # =========================
    # INTERPRETASI SESUAI MODE
    # =========================
    if mode == "SMA":
        st.info("""
        🔍 **Interpretasi (SMA)**
        - Sistem berosilasi tanpa kehilangan energi
        """)

    elif mode == "Kuliah":
        st.info("""
        🔍 **Interpretasi (Kuliah)**
        - Kurva tertutup → energi konstan
        - Sistem linear → lintasan elips
        """)

    else:
        st.warning("""
        🧠 **Fisikawan Insight**
        - Hamiltonian = generator waktu
        - Struktur ruang fase menentukan chaos
        - Ini fondasi mekanika kuantum (H → operator)
        """)

    # =========================
    # ASUMSI & BATAS MODEL
    # =========================
    with st.expander("📌 Asumsi & Batas Model"):
        st.markdown("""
        **Asumsi:**
        - Sistem konservatif
        - Pegas linier
        - Tidak ada redaman

        **Batas Model:**
        - Euler tidak symplectic → energi drift kecil
        - Gagal untuk sistem non-linear kuat
        - Digantikan formulasi kuantum
        """)



# =======================
# MAXWELL
# =======================
elif menu == "🧲 Persamaan Maxwell":
    st.header("Persamaan Maxwell – Medan & Gelombang Elektromagnetik")

    # =========================
    # MODE BELAJAR
    # =========================
    if mode == "SMA":
        st.info("""
        🧑‍🎓 **Mode SMA**
        - Cahaya sebagai gelombang listrik & magnet
        - Fokus hubungan E dan B
        """)

    elif mode == "Kuliah":
        st.info("""
        🎓 **Mode Kuliah**
        - Maxwell menyatukan listrik & magnet
        - Medan memenuhi persamaan diferensial
        """)

    else:  # Fisikawan
        st.warning("""
        🧠 **Fisikawan**
        - Medan adalah objek fisik fundamental
        - Cahaya = eksitasi ruang-waktu
        - Lagrangian medan menentukan segalanya
        """)

    # =========================
    # PERSAMAAN MAXWELL
    # =========================
    st.markdown("**Empat Persamaan Maxwell (vakum):**")
    st.latex("∇·\\vec{E} = 0")
    st.latex("∇·\\vec{B} = 0")
    st.latex("∇×\\vec{E} = -\\frac{\\partial \\vec{B}}{\\partial t}")
    st.latex("∇×\\vec{B} = \\mu_0\\varepsilon_0 \\frac{\\partial \\vec{E}}{\\partial t}")

    st.markdown("""
    Dalam ruang hampa (ρ = 0, J = 0),
    persamaan di atas mereduksi menjadi **persamaan gelombang**:
    """)

    st.latex("""
    \\frac{\\partial^2 E}{\\partial x^2}
    =
    \\frac{1}{c^2}
    \\frac{\\partial^2 E}{\\partial t^2}
    """)

    # =========================
    # PARAMETER GELOMBANG
    # =========================
    c = 3e8
    k = st.slider("Bilangan gelombang k", 1, 10, 2)
    omega = c * k

    x = np.linspace(0, 10, 400)
    t = st.slider("Waktu t", 0.0, 10.0, 0.0)

    # Solusi gelombang datar
    E = np.sin(k * x - omega * t)
    B = E / c

    # =========================
    # VISUALISASI
    # =========================
    fig, ax = plt.subplots()
    ax.plot(x, E, label="Medan Listrik E")
    ax.plot(x, B, label="Medan Magnet B")
    ax.set_xlabel("Posisi x")
    ax.set_title("Gelombang Elektromagnetik di Vakum")
    ax.legend()
    ax.grid()

    st.pyplot(fig)

    # =========================
    # INTERPRETASI SESUAI MODE
    # =========================
    if mode == "SMA":
        st.info("""
        🔍 **Interpretasi (SMA)**
        - Medan listrik & magnet saling menghasilkan
        - Cahaya tidak butuh medium
        """)

    elif mode == "Kuliah":
        st.info("""
        🔍 **Interpretasi (Kuliah)**
        - Solusi Maxwell adalah gelombang transversal
        - Kecepatan gelombang = c
        """)

    else:
        st.warning("""
        🧠 **Fisikawan Insight**
        - Tidak ada gaya dalam Maxwell
        - Partikel bermuatan berinteraksi lewat medan
        - Ini dasar relativitas & QFT
        """)

    # =========================
    # ASUMSI & BATAS MODEL
    # =========================
    with st.expander("📌 Asumsi & Batas Model"):
        st.markdown("""
        **Asumsi:**
        - Vakum (ρ = 0, J = 0)
        - Medan kontinu & klasik
        - Tidak ada efek kuantum

        **Batas Model:**
        - Tidak mencakup partikel (→ QED)
        - Gagal di medan ultra-kuat
        - Digabung dengan relativitas khusus
        """)



# =======================
# KUANTUM
# =======================
elif menu == "⚛️ Mekanika Kuantum":
    st.header("Mekanika Kuantum – Persamaan Schrödinger")

    # =========================
    # MODE BELAJAR
    # =========================
    if mode == "SMA":
        st.info("""
        🧑‍🎓 **Mode SMA**
        - Partikel bersifat gelombang
        - Energi tidak kontinu
        """)

    elif mode == "Kuliah":
        st.info("""
        🎓 **Mode Kuliah**
        - Sistem dijelaskan oleh fungsi gelombang ψ
        - Observabel dari operator
        """)

    else:  # Fisikawan
        st.warning("""
        🧠 **Fisikawan**
        - ψ bukan objek fisik, tapi amplitudo probabilitas
        - Realitas = struktur Hilbert space
        """)

    # =========================
    # PERSAMAAN DASAR
    # =========================
    if mode == "SMA":
        st.latex("E = hf")
    else:
        st.markdown("""
        **Persamaan Schrödinger (tak bergantung waktu):**
        """)
        st.latex("""
        -\\frac{\\hbar^2}{2m}\\frac{d^2\\psi}{dx^2} = E\\psi
        """)

    # =========================
    # KONSTANTA & INPUT
    # =========================
    hbar = 1.055e-34
    m = 9.11e-31  # massa elektron

    L = st.slider("Panjang kotak L (nm)", 0.5, 5.0, 1.0) * 1e-9
    n = st.slider("Bilangan kuantum n", 1, 5, 1)
    t = st.slider("Waktu t (fs)", 0.0, 10.0, 0.0) * 1e-15

    x = np.linspace(0, L, 500)

    # =========================
    # SOLUSI SCHRÖDINGER
    # =========================
    E = (n**2 * np.pi**2 * hbar**2) / (2 * m * L**2)

    psi = (
        np.sqrt(2 / L)
        * np.sin(n * np.pi * x / L)
        * np.exp(-1j * E * t / hbar)
    )

    prob = np.abs(psi)**2

    # =========================
    # VISUALISASI
    # =========================
    fig, ax = plt.subplots()
    ax.plot(x * 1e9, prob)
    ax.set_xlabel("Posisi x (nm)")
    ax.set_ylabel("|ψ(x,t)|²")
    ax.set_title("Probabilitas Posisi Partikel")

    st.pyplot(fig)

    st.success(f"Energi tingkat ke-{n} = {E:.2e} Joule")

    # =========================
    # INTERPRETASI SESUAI MODE
    # =========================
    if mode == "SMA":
        st.info("""
        🔍 **Interpretasi (SMA)**
        - Partikel tidak bebas berada di mana saja
        - Hanya energi tertentu yang diizinkan
        """)

    elif mode == "Kuliah":
        st.info("""
        🔍 **Interpretasi (Kuliah)**
        - |ψ|² = probabilitas pengukuran
        - Evolusi waktu hanya mengubah fase
        """)

    else:
        st.warning("""
        🧠 **Fisikawan Insight**
        - Tidak ada lintasan klasik
        - Observasi menciptakan hasil
        - Determinisme diganti probabilitas
        """)

    # =========================
    # ASUMSI & BATAS MODEL
    # =========================
    with st.expander("📌 Asumsi & Batas Model"):
        st.markdown("""
        **Asumsi:**
        - Potensial tak hingga (kotak ideal)
        - Sistem satu dimensi
        - Partikel tunggal

        **Batas Model:**
        - Tidak mencakup spin
        - Tidak relativistik
        - Digantikan Dirac & QFT
        """)



# =======================
# NAVIER STOKES
# =======================
elif menu == "🌊 Navier–Stokes":
    st.header("Navier–Stokes – Nonlinearitas & Turbulensi")

    # =========================
    # MODE BELAJAR
    # =========================
    if mode == "SMA":
        st.info("""
        🧑‍🎓 **Mode SMA**
        - Fluida nyata tidak selalu rapi
        - Kecepatan bisa berubah karena gesekan
        """)

    elif mode == "Kuliah":
        st.info("""
        🎓 **Mode Kuliah**
        - Persamaan diferensial non-linear
        - Kompetisi adveksi vs difusi
        """)

    else:  # Fisikawan
        st.warning("""
        🧠 **Fisikawan**
        - Navier–Stokes = masalah terbuka matematika
        - Turbulensi = chaos deterministik
        - Tidak ada solusi umum tertutup
        """)

    st.markdown("""
    **Persamaan Burgers (1D – analog Navier–Stokes):**
    \\[
    \\frac{\\partial u}{\\partial t}
    + u \\frac{\\partial u}{\\partial x}
    =
    \\nu \\frac{\\partial^2 u}{\\partial x^2}
    \\]
    """)

    # =========================
    # PARAMETER SIMULASI
    # =========================
    nu = st.slider("Viskositas kinematik ν", 0.0, 0.5, 0.1)
    nt = st.slider("Jumlah langkah waktu", 10, 300, 100)

    nx = 200
    dx = 2 / nx
    dt = 0.002

    x = np.linspace(0, 2, nx)

    # =========================
    # KONDISI AWAL
    # =========================
    u0 = np.ones(nx)
    u0[int(0.5 / dx):int(1 / dx)] = 2
    u = u0.copy()

    # =========================
    # INTEGRASI NUMERIK
    # =========================
    for _ in range(nt):
        un = u.copy()
        u[1:-1] = (
            un[1:-1]
            - un[1:-1] * dt / dx * (un[1:-1] - un[:-2])
            + nu * dt / dx**2 * (un[2:] - 2 * un[1:-1] + un[:-2])
        )

    # =========================
    # VISUALISASI
    # =========================
    fig, ax = plt.subplots()
    ax.plot(x, u0, "--", label="Awal")
    ax.plot(x, u, label="Akhir")
    ax.set_xlabel("Posisi x")
    ax.set_ylabel("Kecepatan u")
    ax.set_title("Evolusi Aliran Fluida 1D")
    ax.legend()
    ax.grid()

    st.pyplot(fig)

    # =========================
    # INTERPRETASI SESUAI MODE
    # =========================
    if nu < 0.05:
        st.warning("""
        🔥 **ν kecil**
        - Adveksi dominan
        - Gradien tajam (shock)
        - Cikal bakal turbulensi
        """)

        if mode == "Fisikawan":
            st.warning("""
            🧠 **Fisikawan Insight**
            - Turbulensi ≠ acak
            - Sangat sensitif kondisi awal
            """)

    else:
        st.info("""
        💧 **ν besar**
        - Difusi dominan
        - Profil kecepatan halus
        - Aliran stabil
        """)

    # =========================
    # ASUMSI & BATAS MODEL
    # =========================
    with st.expander("📌 Asumsi & Batas Model"):
        st.markdown("""
        **Asumsi:**
        - Fluida tak termampatkan
        - Satu dimensi
        - Tanpa tekanan eksternal

        **Batas Model:**
        - Bukan Navier–Stokes penuh
        - Tidak mencakup vorteks 3D
        - Turbulensi nyata jauh lebih kompleks
        """)

    st.caption("""
    Catatan:
    - Burgers equation = laboratorium matematika
    - Dipakai untuk memahami shock & chaos
    - Batu loncatan ke CFD & iklim
    """)

