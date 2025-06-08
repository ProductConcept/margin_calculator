import streamlit as st
from decimal import Decimal, InvalidOperation

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

# ------------------ Session state defaults -----------------
INITIAL_DISCOUNT = {
    "tkw": "",
    "cena_stara": "",
    "marza_stara": "",
    "cena_nowa": "",
    "marza_nowa": "",
    "ilosc_stara": "",
}

INITIAL_QUICK = {
    "tkw_m": "",
    "cena_m": "",
    "marza_m": "",
}

EXAMPLE_DISCOUNT = {
    "tkw": "80.0",
    "cena_stara": "120.0",
    "marza_stara": "33.33",
    "cena_nowa": "100.0",
    "marza_nowa": "20.0",
    "ilosc_stara": "100",
}

EXAMPLE_QUICK = {
    "tkw_m": "50.0",
    "cena_m": "100.0",
    "marza_m": "50.0",
}

for k, v in {**INITIAL_DISCOUNT, **INITIAL_QUICK}.items():
    st.session_state.setdefault(k, v)


def _clear_field(key: str, init_dict: dict) -> None:
    """Reset a single field in ``st.session_state`` to its initial value."""
    st.session_state[key] = init_dict[key]


def clear_discount_all() -> None:
    for k in INITIAL_DISCOUNT:
        st.session_state[k] = INITIAL_DISCOUNT[k]


def load_discount_example() -> None:
    for k in INITIAL_DISCOUNT:
        st.session_state[k] = EXAMPLE_DISCOUNT[k]


def clear_quick_all() -> None:
    for k in INITIAL_QUICK:
        st.session_state[k] = INITIAL_QUICK[k]


def load_quick_example() -> None:
    for k in INITIAL_QUICK:
        st.session_state[k] = EXAMPLE_QUICK[k]


def _to_decimal(value: str) -> Decimal:
    """Convert user input to ``Decimal``. Returns ``Decimal('0')`` on error."""
    if value is None or value == "":
        return Decimal("0")
    try:
        return Decimal(value.replace(",", "."))
    except (InvalidOperation, AttributeError):
        return Decimal("0")


def _entered(key: str) -> bool:
    """Return ``True`` if the user explicitly provided a value for ``key``."""
    val = st.session_state.get(key, "")
    return str(val).strip() != ""


def _to_int(value: str) -> int:
    """Convert user input to ``int``. Returns ``0`` on error."""
    try:
        return int(_to_decimal(value))
    except (InvalidOperation, ValueError):
        return 0

# ------------------ Funkcje matematyczne -------------------

from calculator import licz_marze_z_ceny, cena_z_marzy

# ------------------ UI -------------------------------------
st.title(T["title"])

tab_obnizka, tab_szybki = st.tabs([T["tab_discount"], T["tab_quick"]])

# ========= Zakładka 1: obniżka marży / ceny ================
with tab_obnizka:
    st.header(T["discount_header"])

    col_a, col_or1, col_b = st.columns([1, 0.15, 1])
    with col_a:
        tkw = _to_decimal(st.text_input(T["tkw"], key="tkw"))
        st.button("Clear", key="clr_tkw", on_click=_clear_field, args=("tkw", INITIAL_DISCOUNT))
    with col_or1:
        st.markdown(
            f"<div style='text-align:center; padding-top:2.3rem; font-weight:700;'>{T['or']}</div>",
            unsafe_allow_html=True,
        )
    with col_b:
        cena_stara = _to_decimal(st.text_input(T["price"], key="cena_stara"))
        st.button("Clear", key="clr_cena_stara", on_click=_clear_field, args=("cena_stara", INITIAL_DISCOUNT))

    col_c, col_or2, col_d = st.columns([1, 0.15, 1])
    with col_c:
        marza_stara = _to_decimal(st.text_input(T["old_margin"], key="marza_stara"))
        st.button("Clear", key="clr_marza_stara", on_click=_clear_field, args=("marza_stara", INITIAL_DISCOUNT))
    with col_or2:
        st.markdown(
            f"<div style='text-align:center; padding-top:2.3rem; font-weight:700;'>{T['or']}</div>",
            unsafe_allow_html=True,
        )
    with col_d:
        cena_nowa = _to_decimal(st.text_input(T["new_price"], key="cena_nowa"))
        st.button("Clear", key="clr_cena_nowa", on_click=_clear_field, args=("cena_nowa", INITIAL_DISCOUNT))

    col_e, col_f = st.columns([1, 1])
    with col_e:
        marza_nowa = _to_decimal(st.text_input(T["new_margin"], key="marza_nowa"))
        st.button("Clear", key="clr_marza_nowa", on_click=_clear_field, args=("marza_nowa", INITIAL_DISCOUNT))
    with col_f:
        ilosc_stara = _to_int(st.text_input(T["qty"], key="ilosc_stara"))
        st.button("Clear", key="clr_ilosc_stara", on_click=_clear_field, args=("ilosc_stara", INITIAL_DISCOUNT))

    col_actions_d1, col_actions_d2 = st.columns([1, 1])
    with col_actions_d1:
        st.button("Clear all", key="clear_all_discount", on_click=clear_discount_all)
    with col_actions_d2:
        st.button("Load example", key="example_discount", on_click=load_discount_example)

    if st.button(T["btn_discount"], key="discount_btn"):
        if not _entered("tkw") or not _entered("ilosc_stara"):
            st.error(T["err_fill"])
            st.stop()

        if _entered("marza_stara"):
            cena_stara = float(
                cena_z_marzy(Decimal(tkw), Decimal(marza_stara) / Decimal(100))
            )
        elif not _entered("cena_stara"):
            st.error(T["err_pair_old"])
            st.stop()
        else:
            marza_stara = float(
                licz_marze_z_ceny(Decimal(tkw), Decimal(cena_stara))
            ) * 100

        if _entered("marza_nowa"):
            cena_nowa = float(
                cena_z_marzy(Decimal(tkw), Decimal(marza_nowa) / Decimal(100))
            )
        elif not _entered("cena_nowa"):
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
        tkw_m = _to_decimal(st.text_input(T["tkw"], key="tkw_m"))
        st.button("Clear", key="clr_tkw_m", on_click=_clear_field, args=("tkw_m", INITIAL_QUICK))
    with col_or_a:
        st.markdown(
            f"<div style='text-align:center; padding-top:2.3rem; font-weight:700;'>{T['or']}</div>",
            unsafe_allow_html=True,
        )
    with col_price:
        cena_m = _to_decimal(st.text_input(T["price"], key="cena_m"))
        st.button("Clear", key="clr_cena_m", on_click=_clear_field, args=("cena_m", INITIAL_QUICK))
    with col_or_b:
        st.markdown(
            f"<div style='text-align:center; padding-top:2.3rem; font-weight:700;'>{T['or']}</div>",
            unsafe_allow_html=True,
        )
    with col_margin:
        marza_m = _to_decimal(
            st.text_input(
                T["new_margin"].replace("Nowa ", "").replace("New ", "").capitalize(),
                key="marza_m",
            )
        )
        st.button("Clear", key="clr_marza_m", on_click=_clear_field, args=("marza_m", INITIAL_QUICK))

    col_actions_q1, col_actions_q2 = st.columns([1, 1])
    with col_actions_q1:
        st.button("Clear all", key="clear_all_quick", on_click=clear_quick_all)
    with col_actions_q2:
        st.button("Load example", key="example_quick", on_click=load_quick_example)

    if st.button(T["btn_quick"], key="quick_btn"):
        pola = [_entered("tkw_m"), _entered("cena_m"), _entered("marza_m")]
        if sum(pola) < 2:
            st.error(T["err_two_values"])
            st.stop()

        if _entered("cena_m") and _entered("tkw_m"):
            marza_m = float(
                licz_marze_z_ceny(Decimal(tkw_m), Decimal(cena_m))
            ) * 100
        elif _entered("tkw_m") and _entered("marza_m"):
            cena_m = float(
                cena_z_marzy(Decimal(tkw_m), Decimal(marza_m) / Decimal(100))
            )
        elif _entered("cena_m") and _entered("marza_m"):
            tkw_m = cena_m * (1 - marza_m / 100)

        st.success(
            T["res_quick"].format(tkw=tkw_m, price=cena_m, margin=marza_m)
        )

# ====== Informacja o autorze ======
st.markdown(f"<div style='margin-top:2em;text-align:center;color:#999'>{T['author']}</div>", unsafe_allow_html=True)
