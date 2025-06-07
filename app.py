import streamlit as st
from decimal import Decimal

# ------------------ Konfiguracja / Config ------------------
st.set_page_config(
    page_title="Kalkulator Marży / Margin Calculator",
    page_icon="💰",
    layout="centered",
)

# ------------------ Tłumaczenia / Translations -------------
PL = {
    "title": "💰 Kalkulator Marży",
    "tab_discount": "Obniżka marży / ceny",
    "tab_quick": "Szybki kalkulator marży",
    "discount_header": "📉 Obniżka marży / ceny",
    "quick_header": "⚙️ Szybki kalkulator marży",
    "quick_sub": "(podaj dowolne 2 pola)",
    "tkw": "TKW (koszt jednostkowy) [zł]",
    "price": "Cena sprzedaży [zł]",
    "old_margin": "Obecna marża [%]",
    "new_margin": "Nowa marża [%]",
    "new_price": "Nowa cena sprzedaży [zł]",
    "qty": "Ilość sprzedana wcześniej [szt.]",
    "btn_discount": "Oblicz",
    "btn_quick": "Oblicz",
    "or": "lub",
    "err_fill": "Uzupełnij TKW oraz ilość sprzedaną wcześniej.",
    "err_pair_old": "Podaj starą marżę lub starą cenę.",
    "err_pair_new": "Podaj nową marżę lub nową cenę.",
    "err_loss": "Zysk po obniżce wynosi 0 zł lub mniej – obliczenia niemożliwe.",
    "err_two_values": "⚠️ Podaj dowolne dwie wartości.",
    "res_profit_old": "📈 **Zysk przed:** {v:.2f} zł/szt",
    "res_profit_new": "📉 **Zysk po:** {v:.2f} zł/szt",
    "res_loss": "💰 **Strata łączna:** {v:.2f} zł",
    "res_extra": "➕ **Dodatkowa sprzedaż:** {v} szt.",
    "res_total": "📦 **Łącznie:** {v} szt.",
    "res_quick": "**TKW:** {tkw:.2f} zł  |  **Cena:** {price:.2f} zł  |  **Marża:** {margin:.2f} %",
    "author": "Autor programu: Marcin Czerwiński  |  Product Concept"
}
EN = {
    "title": "💰 Margin Calculator",
    "tab_discount": "Margin / price drop",
    "tab_quick": "Quick margin calc",
    "discount_header": "📉 Margin / price drop",
    "quick_header": "⚙️ Quick margin calculator",
    "quick_sub": "(fill any 2 fields)",
    "tkw": "Production cost (unit cost) [PLN]",
    "price": "Sale price [PLN]",
    "old_margin": "Current margin [%]",
    "new_margin": "New margin [%]",
    "new_price": "New sale price [PLN]",
    "qty": "Quantity sold before [pcs]",
    "btn_discount": "Calculate",
    "btn_quick": "Calculate",
    "or": "or",
    "err_fill": "Fill Production cost and previous quantity first.",
    "err_pair_old": "Provide either old margin or old price.",
    "err_pair_new": "Provide either new margin or new price.",
    "err_loss": "Profit after drop is 0 or negative – cannot compute.",
    "err_two_values": "⚠️ Provide any two values.",
    "res_profit_old": "📈 **Profit before:** {v:.2f} PLN/pc",
    "res_profit_new": "📉 **Profit after:** {v:.2f} PLN/pc",
    "res_loss": "💰 **Total loss:** {v:.2f} PLN",
    "res_extra": "➕ **Extra sales needed:** {v} pcs",
    "res_total": "📦 **Total:** {v} pcs",
    "res_quick": "**Production cost:** {tkw:.2f} PLN  |  **Price:** {price:.2f} PLN  |  **Margin:** {margin:.2f} %",
    "author": "Program author: Marcin Czerwiński  |  Product Concept"
}

lang = st.sidebar.selectbox("Language / Język", ("Polski", "English"))
T = PL if lang == "Polski" else EN

# ------------------ Funkcje matematyczne -------------------

def licz_marze_z_ceny(tkw: Decimal, cena: Decimal) -> Decimal:
    """Calculate margin fraction from unit cost and price.

    Parameters
    ----------
    tkw : Decimal
        Unit production cost.
    cena : Decimal
        Sale price per unit.

    Returns
    -------
    Decimal
        Margin expressed as a fraction of the price. Returns ``Decimal('0')`` when
        the price is zero.
    """
    return (cena - tkw) / cena if cena else Decimal("0")

def cena_z_marzy(tkw: Decimal, marza: Decimal) -> Decimal:
    """Calculate sale price required for a given margin.

    Parameters
    ----------
    tkw : Decimal
        Unit production cost.
    marza : Decimal
        Desired margin expressed as a fraction (e.g. ``0.25`` for 25%).

    Returns
    -------
    Decimal
        Sale price that yields the desired margin. Returns ``Decimal('0')`` when the
        provided margin is ``1`` or greater.
    """
    return tkw / (Decimal("1") - marza) if marza < Decimal("1") else Decimal("0")

# ------------------ UI -------------------------------------
st.title(T["title"])

tab_obnizka, tab_szybki = st.tabs([T["tab_discount"], T["tab_quick"]])

# ========= Zakładka 1: obniżka marży / ceny ================
with tab_obnizka:
    st.header(T["discount_header"])

    col_a, col_or1, col_b = st.columns([1, 0.15, 1])
    with col_a:
        tkw = st.number_input(T["tkw"], min_value=0.0, step=0.01)
    with col_or1:
        st.markdown(
            f"<div style='text-align:center; padding-top:2.3rem; font-weight:700;'>{T['or']}</div>",
            unsafe_allow_html=True,
        )
    with col_b:
        cena_stara = st.number_input(T["price"], min_value=0.0, step=0.01)

    col_c, col_or2, col_d = st.columns([1, 0.15, 1])
    with col_c:
        marza_stara = st.number_input(T["old_margin"], min_value=0.0, step=0.01, format="%.2f")
    with col_or2:
        st.markdown(
            f"<div style='text-align:center; padding-top:2.3rem; font-weight:700;'>{T['or']}</div>",
            unsafe_allow_html=True,
        )
    with col_d:
        cena_nowa = st.number_input(T["new_price"], min_value=0.0, step=0.01)

    col_e, col_f = st.columns([1, 1])
    with col_e:
        marza_nowa = st.number_input(T["new_margin"], min_value=0.0, step=0.01, format="%.2f")
    with col_f:
        ilosc_stara = st.number_input(T["qty"], min_value=0, step=1)

    if st.button(T["btn_discount"], key="discount_btn"):
        if tkw == 0 or ilosc_stara == 0:
            st.error(T["err_fill"])
            st.stop()

        if marza_stara:
            cena_stara = float(
                cena_z_marzy(Decimal(tkw), Decimal(marza_stara) / Decimal(100))
            )
        elif not cena_stara:
            st.error(T["err_pair_old"])
            st.stop()
        else:
            marza_stara = float(
                licz_marze_z_ceny(Decimal(tkw), Decimal(cena_stara))
            ) * 100

        if marza_nowa:
            cena_nowa = float(
                cena_z_marzy(Decimal(tkw), Decimal(marza_nowa) / Decimal(100))
            )
        elif not cena_nowa:
            st.error(T["err_pair_new"])
            st.stop()
        else:
            marza_nowa = float(
                licz_marze_z_ceny(Decimal(tkw), Decimal(cena_nowa))
            ) * 100

        zysk_stary = cena_stara - tkw
        zysk_nowy = cena_nowa - tkw
        strata = (zysk_stary - zysk_nowy) * ilosc_stara

        if zysk_nowy <= 0:
            st.error(T["err_loss"])
            st.stop()

        ilosc_dodatkowa = round(strata / zysk_nowy)
        ilosc_nowych = ilosc_stara + ilosc_dodatkowa

        st.success(
            T["res_profit_old"].format(v=zysk_stary)
            + "  \n"
            + T["res_profit_new"].format(v=zysk_nowy)
            + "  \n"
            + T["res_loss"].format(v=strata)
            + "  \n"
            + T["res_extra"].format(v=ilosc_dodatkowa)
            + "  \n"
            + T["res_total"].format(v=ilosc_nowych)
        )

# ========= Zakładka 2: szybki kalkulator ====================
with tab_szybki:
    st.header(T["quick_header"])
    st.markdown(f"<span style='font-size:0.8em;color:gray'>{T['quick_sub']}</span>", unsafe_allow_html=True)

    col_tkw, col_or_a, col_price, col_or_b, col_margin = st.columns([1, 0.13, 1, 0.13, 1])
    with col_tkw:
        tkw_m = st.number_input(T["tkw"], min_value=0.0, step=0.01, key="tkw_m")
    with col_or_a:
        st.markdown(
            f"<div style='text-align:center; padding-top:2.3rem; font-weight:700;'>{T['or']}</div>",
            unsafe_allow_html=True,
        )
    with col_price:
        cena_m = st.number_input(T["price"], min_value=0.0, step=0.01, key="cena_m")
    with col_or_b:
        st.markdown(
            f"<div style='text-align:center; padding-top:2.3rem; font-weight:700;'>{T['or']}</div>",
            unsafe_allow_html=True,
        )
    with col_margin:
        marza_m = st.number_input(T["new_margin"].replace("Nowa ", "").replace("New ", ""), min_value=0.0, step=0.01, key="marza_m")

    if st.button(T["btn_quick"], key="quick_btn"):
        pola = [tkw_m > 0, cena_m > 0, marza_m > 0]
        if sum(pola) < 2:
            st.error(T["err_two_values"])
            st.stop()

        if cena_m and tkw_m:
            marza_m = float(
                licz_marze_z_ceny(Decimal(tkw_m), Decimal(cena_m))
            ) * 100
        elif tkw_m and marza_m:
            cena_m = float(
                cena_z_marzy(Decimal(tkw_m), Decimal(marza_m) / Decimal(100))
            )
        elif cena_m and marza_m:
            tkw_m = cena_m * (1 - marza_m / 100)

        st.success(
            T["res_quick"].format(tkw=tkw_m, price=cena_m, margin=marza_m)
        )

# ====== Informacja o autorze ======
st.markdown(f"<div style='margin-top:2em;text-align:center;color:#999'>{T['author']}</div>", unsafe_allow_html=True)
