"""Streamlit application for interactive margin calculations."""

from decimal import Decimal

import streamlit as st
import inspect

try:  # Prefer relative import when installed as a package
    from .calculator import cena_z_marzy, licz_marze_z_ceny
except ImportError:  # Fallback for running as a standalone script
    from calculator import cena_z_marzy, licz_marze_z_ceny

# ------------------ Konfiguracja / Config ------------------
st.set_page_config(
    page_title="Kalkulator Marży / Margin Calculator",
    page_icon="💰",
)

# Prevent button labels from wrapping
st.markdown(
    "<style>div.stButton>button{white-space:nowrap}</style>",
    unsafe_allow_html=True,
)

# Compatibility helper for older Streamlit versions.
_fsb_params = inspect.signature(st.form_submit_button).parameters


def compat_submit_button(label: str, *, key=None, on_click=None, args=None):
    """Wrapper for ``st.form_submit_button`` handling old Streamlit releases."""
    kwargs = {}
    label_mod = label
    # Encode ``key`` with zero-width characters for uniqueness on old Streamlit
    if "key" not in _fsb_params and key is not None:
        import hashlib

        digest = hashlib.sha256(str(key).encode()).digest()
        bits = "".join(f"{b:08b}" for b in digest)
        zw = "".join("\u200b" if bit == "0" else "\u200c" for bit in bits)
        label_mod += zw
    elif "key" in _fsb_params and key is not None:
        kwargs["key"] = key
    if "on_click" in _fsb_params and on_click is not None:
        kwargs["on_click"] = on_click
    if "args" in _fsb_params and args is not None:
        kwargs["args"] = args
    pressed = st.form_submit_button(label_mod, **kwargs)
    if "on_click" not in _fsb_params and pressed and on_click is not None:
        if args:
            on_click(*args)
        else:
            on_click()
    return pressed

# ------------------ Tłumaczenia / Translations -------------
PL = {
    "title": "💰 Kalkulator Marży",
    "tab_discount": "Obniżka marży / ceny",
    "tab_quick": "Szybki kalkulator marży",
    "discount_header": "📉 Obniżka marży / ceny",
    "quick_header": "⚙️ Szybki kalkulator marży",
    "quick_sub": "podaj dowolne 2 pola",
    "calc_mode": "Tryb kalkulatora",
    "tkw": "TKW (koszt jednostkowy)",
    "price": "Cena sprzedaży",
    "old_margin": "Obecna marża [%]",
    "new_margin": "Nowa marża [%]",
    "new_price": "Nowa cena sprzedaży",
    "qty": "Ilość sprzedana wcześniej [szt.]",
    "btn_discount": "Oblicz",
    "btn_quick": "Oblicz",
    "btn_clear": "Wyczyść",
    "btn_clear_all": "Wyczyść wszystko",
    "btn_example": "Wczytaj przykład",
    "or": "lub",
    "err_fill": "Uzupełnij TKW oraz ilość sprzedaną wcześniej.",
    "err_pair_old": "Podaj starą marżę lub starą cenę.",
    "err_pair_new": "Podaj nową marżę lub nową cenę.",
    "err_loss": "Zysk po obniżce wynosi 0 lub mniej – obliczenia niemożliwe.",
    "err_two_values": "⚠️ Podaj dowolne dwie wartości.",
    "res_profit_old": "📈 **Zysk przed:** {v:.2f}/szt",
    "res_profit_new": "📉 **Zysk po:** {v:.2f}/szt",
    "res_loss": "💰 **Strata łączna:** {v:.2f}",
    "res_extra": "➕ Dodatkowa sprzedaż",
    "res_total": "📦 **Łącznie:** {v} szt.",
    "res_quick": "**TKW:** {tkw:.2f}  |  **Cena:** {price:.2f}  |  **Marża:** {margin:.2f} %",
    "author": "Autor programu: Marcin Czerwiński  |  Product Concept",
}
EN = {
    "title": "💰 Margin Calculator",
    "tab_discount": "Margin / price drop",
    "tab_quick": "Quick margin calc",
    "discount_header": "📉 Margin / price drop",
    "quick_header": "⚙️ Quick margin calculator",
    "quick_sub": "fill any 2 fields",
    "calc_mode": "Calculator mode",
    "tkw": "Production cost (unit cost)",
    "price": "Sale price",
    "old_margin": "Current margin [%]",
    "new_margin": "New margin [%]",
    "new_price": "New sale price",
    "qty": "Quantity sold before [pcs]",
    "btn_discount": "Calculate",
    "btn_quick": "Calculate",
    "btn_clear": "Clear",
    "btn_clear_all": "Clear all",
    "btn_example": "Load example",
    "or": "or",
    "err_fill": "Fill Production cost and previous quantity first.",
    "err_pair_old": "Provide either old margin or old price.",
    "err_pair_new": "Provide either new margin or new price.",
    "err_loss": "Profit after drop is 0 or negative – cannot compute.",
    "err_two_values": "⚠️ Provide any two values.",
    "res_profit_old": "📈 **Profit before:** {v:.2f}/pc",
    "res_profit_new": "📉 **Profit after:** {v:.2f}/pc",
    "res_loss": "💰 **Total loss:** {v:.2f}",
    "res_extra": "➕ Extra sales needed",
    "res_total": "📦 **Total:** {v} pcs",
    "res_quick": "**Production cost:** {tkw:.2f}  |  **Price:** {price:.2f}  |  **Margin:** {margin:.2f} %",
    "author": "Program author: Marcin Czerwiński  |  Product Concept",
}

lang = st.sidebar.selectbox("Language / Język", ("Polski", "English"))
T = PL if lang == "Polski" else EN

# ------------------ Session state defaults -----------------
INITIAL_DISCOUNT = {
    "tkw": 0.0,
    "cena_stara": 0.0,
    "marza_stara": 0.0,
    "cena_nowa": 0.0,
    "marza_nowa": 0.0,
    "ilosc_stara": 0,
}

INITIAL_QUICK = {
    "tkw_m": 0.0,
    "cena_m": 0.0,
    "marza_m": 0.0,
}

EXAMPLE_DISCOUNT_PRICE = {
    "tkw": 80.0,
    "cena_stara": 120.0,
    "marza_stara": 0.0,
    "cena_nowa": 100.0,
    "marza_nowa": 0.0,
    "ilosc_stara": 100,
}

EXAMPLE_DISCOUNT_MARGIN = {
    "tkw": 80.0,
    "cena_stara": 0.0,
    "marza_stara": 40.0,
    "cena_nowa": 0.0,
    "marza_nowa": 20.0,
    "ilosc_stara": 100,
}

EXAMPLE_QUICK = {
    "tkw_m": 50.0,
    "cena_m": 100.0,
    "marza_m": 50.0,
}

for k, v in {**INITIAL_DISCOUNT, **INITIAL_QUICK}.items():
    st.session_state.setdefault(k, v)
st.session_state.setdefault("example_toggle", 0)


def _clear_field(key: str, init_dict: dict) -> None:
    """Reset a single field in ``st.session_state`` to its initial value."""
    st.session_state[key] = init_dict[key]


def _clear_field_cb(key: str, init_dict: dict) -> None:
    """Callback wrapper that clears a field and reruns the app."""
    _clear_field(key, init_dict)
    st.rerun()


def clear_discount_all() -> None:
    """Reset all discount form fields to their default values."""
    for k in INITIAL_DISCOUNT:
        st.session_state[k] = INITIAL_DISCOUNT[k]


def clear_discount_all_cb() -> None:
    """Clear discount fields and rerun the app."""
    clear_discount_all()
    st.rerun()


def load_discount_example() -> None:
    """Load example values for the discount calculator."""
    toggle = st.session_state.get("example_toggle", 0)
    example = EXAMPLE_DISCOUNT_PRICE if toggle == 0 else EXAMPLE_DISCOUNT_MARGIN
    for k in INITIAL_DISCOUNT:
        st.session_state[k] = example[k]
    st.session_state["example_toggle"] = 1 - toggle


def load_discount_example_cb() -> None:
    """Load discount example values and rerun the app."""
    load_discount_example()
    st.rerun()


def clear_quick_all() -> None:
    """Reset all quick calculator fields to their default values."""
    for k in INITIAL_QUICK:
        st.session_state[k] = INITIAL_QUICK[k]


def clear_quick_all_cb() -> None:
    """Clear quick calculator fields and rerun the app."""
    clear_quick_all()
    st.rerun()


def load_quick_example() -> None:
    """Load example values for the quick calculator."""
    for k in INITIAL_QUICK:
        st.session_state[k] = EXAMPLE_QUICK[k]


def load_quick_example_cb() -> None:
    """Load quick example values and rerun the app."""
    load_quick_example()
    st.rerun()


def _entered(key: str) -> bool:
    """Return ``True`` if the user explicitly provided a value for ``key``."""
    val = st.session_state.get(key)
    if val is None:
        return False
    init_discount = globals().get("INITIAL_DISCOUNT", {})
    init_quick = globals().get("INITIAL_QUICK", {})
    if key in init_discount:
        default = init_discount[key]
        return val != default
    if key in init_quick:
        default = init_quick[key]
        return val != default
    return str(val).strip() != ""


# ------------------ UI -------------------------------------
st.title(T["title"])

# determine active tab from query params or session state
query = st.query_params
default_tab = query.get("tab", "discount")
st.session_state.setdefault("selected_tab", default_tab)

tab_labels = [T["tab_discount"], T["tab_quick"]]


def _on_tab_change() -> None:
    label = st.session_state.get("tab_choice", tab_labels[0])
    new_key = "discount" if label == T["tab_discount"] else "quick"
    if new_key != st.session_state.get("selected_tab"):
        clear_discount_all()
        clear_quick_all()
        st.session_state["selected_tab"] = new_key
        st.query_params.update({"tab": new_key})
        # rerun to refresh the UI is no longer needed as the radio widget
        # handles tab switching without a warning
        # st.rerun()


st.radio(
    label=T["calc_mode"],
    options=tab_labels,
    index=0 if st.session_state["selected_tab"] == "discount" else 1,
    key="tab_choice",
    on_change=_on_tab_change,
    label_visibility="collapsed",
)

# ========= Zakładka 1: obniżka marży / ceny ================
if st.session_state["selected_tab"] == "discount":
    st.header(T["discount_header"])
    with st.form("discount_form"):

        col_a, col_or1, col_b = st.columns([1, 0.15, 1])
        with col_a:
            tkw = Decimal(
                str(st.number_input(T["tkw"], key="tkw", value=0.0))
            )
            sub_a1, sub_a2, sub_a3 = st.columns([1, 1, 1])
            with sub_a2:
                compat_submit_button(
                    T["btn_clear"],
                    key="clear_tkw",
                    on_click=_clear_field_cb,
                    args=("tkw", INITIAL_DISCOUNT),
                )
        with col_or1:
            or_html = f"<div style='text-align:center; padding-top:2.3rem; font-weight:700;'>{T['or']}</div>"
            st.markdown(or_html, unsafe_allow_html=True)
        with col_b:
            cena_stara = Decimal(
                str(st.number_input(T["price"], key="cena_stara", value=0.0))
            )
            sub_b1, sub_b2, sub_b3 = st.columns([1, 1, 1])
            with sub_b2:
                compat_submit_button(
                    T["btn_clear"],
                    key="clear_cena_stara",
                    on_click=_clear_field_cb,
                    args=("cena_stara", INITIAL_DISCOUNT),
                )

        col_c, col_or2, col_d = st.columns([1, 0.15, 1])
        with col_c:
            marza_stara = Decimal(
                str(st.number_input(T["old_margin"], key="marza_stara", value=0.0))
            )
            sub_c1, sub_c2, sub_c3 = st.columns([1, 1, 1])
            with sub_c2:
                compat_submit_button(
                    T["btn_clear"],
                    key="clear_marza_stara",
                    on_click=_clear_field_cb,
                    args=("marza_stara", INITIAL_DISCOUNT),
                )
        with col_or2:
            st.markdown(or_html, unsafe_allow_html=True)
        with col_d:
            cena_nowa = Decimal(
                str(st.number_input(T["new_price"], key="cena_nowa", value=0.0))
            )
            sub_d1, sub_d2, sub_d3 = st.columns([1, 1, 1])
            with sub_d2:
                compat_submit_button(
                    T["btn_clear"],
                    key="clear_cena_nowa",
                    on_click=_clear_field_cb,
                    args=("cena_nowa", INITIAL_DISCOUNT),
                )

        col_e, col_f = st.columns([1, 1])
        with col_e:
            marza_nowa = Decimal(
                str(st.number_input(T["new_margin"], key="marza_nowa", value=0.0))
            )
            sub_e1, sub_e2, sub_e3 = st.columns([1, 1, 1])
            with sub_e2:
                compat_submit_button(
                    T["btn_clear"],
                    key="clear_marza_nowa",
                    on_click=_clear_field_cb,
                    args=("marza_nowa", INITIAL_DISCOUNT),
                )
        with col_f:
            ilosc_stara = Decimal(
                str(st.number_input(T["qty"], key="ilosc_stara", value=0, step=1))
            )
            sub_f1, sub_f2, sub_f3 = st.columns([1, 1, 1])
            with sub_f2:
                compat_submit_button(
                    T["btn_clear"],
                    key="clear_ilosc_stara",
                    on_click=_clear_field_cb,
                    args=("ilosc_stara", INITIAL_DISCOUNT),
                )

        col_actions_d1, col_actions_d2 = st.columns([1, 1])
        with col_actions_d1:
            compat_submit_button(
                T["btn_clear_all"],
                key="clear_discount_all",
                on_click=clear_discount_all_cb,
            )
        with col_actions_d2:
            compat_submit_button(
                T["btn_example"],
                key="load_discount_example",
                on_click=load_discount_example_cb,
            )

        submitted_discount = compat_submit_button(
            T["btn_discount"],
            key="submit_discount",
        )
    if submitted_discount:
        with st.spinner("Obliczanie..."):
            if None in (
                tkw,
                cena_stara,
                marza_stara,
                cena_nowa,
                marza_nowa,
                ilosc_stara,
            ):
                st.error("Invalid input")
                st.stop()

            if not _entered("tkw") or not _entered("ilosc_stara"):
                st.error(T["err_fill"])
                st.stop()

            if _entered("marza_stara"):
                cena_stara = cena_z_marzy(
                    tkw,
                    marza_stara / Decimal(100),
                ).quantize(Decimal("0.01"))
            elif not _entered("cena_stara"):
                st.error(T["err_pair_old"])
                st.stop()
            else:
                marza_stara = licz_marze_z_ceny(tkw, cena_stara) * 100

            if _entered("marza_nowa"):
                cena_nowa = cena_z_marzy(
                    tkw,
                    marza_nowa / Decimal(100),
                ).quantize(Decimal("0.01"))
            elif not _entered("cena_nowa"):
                st.error(T["err_pair_new"])
                st.stop()
            else:
                marza_nowa = licz_marze_z_ceny(tkw, cena_nowa) * 100

            zysk_stary = cena_stara - tkw
            zysk_nowy = cena_nowa - tkw
            strata = (zysk_stary - zysk_nowy) * ilosc_stara

            if zysk_nowy <= 0:
                st.error(T["err_loss"])
                st.stop()

            ilosc_dodatkowa = round(strata / zysk_nowy)
            ilosc_nowych = ilosc_stara + ilosc_dodatkowa

            st.metric("➕ Dodatkowa sprzedaż", f"{ilosc_dodatkowa} szt.")

            st.success(
                T["res_profit_old"].format(v=zysk_stary)
                + "  \n"
                + T["res_profit_new"].format(v=zysk_nowy)
                + "  \n"
                + T["res_loss"].format(v=strata)
                + "  \n"
                + T["res_total"].format(v=ilosc_nowych)
            )

# ========= Zakładka 2: szybki kalkulator ====================
elif st.session_state["selected_tab"] == "quick":
    st.header(T["quick_header"])
    with st.form("quick_form"):
        or_html = f"<div style='text-align:center; padding-top:2.3rem; font-weight:700;'>{T['or']}</div>"
        st.markdown(
            f"<div style='text-align:center;font-size:0.75em;color:gray'>{T['quick_sub']}</div>",
            unsafe_allow_html=True,
        )

        col_tkw, col_or_a, col_price, col_or_b, col_margin = st.columns(
            [1, 0.13, 1, 0.13, 1]
        )
        with col_tkw:
            tkw_m = Decimal(
                str(st.number_input(T["tkw"], key="tkw_m", value=0.0))
            )
            sub_q1, sub_q2, sub_q3 = st.columns([1, 1, 1])
            with sub_q2:
                compat_submit_button(
                    T["btn_clear"],
                    key="clear_tkw_m",
                    on_click=_clear_field_cb,
                    args=("tkw_m", INITIAL_QUICK),
                )
        with col_or_a:
            st.markdown(or_html, unsafe_allow_html=True)
        with col_price:
            cena_m = Decimal(
                str(st.number_input(T["price"], key="cena_m", value=0.0))
            )
            sub_q4, sub_q5, sub_q6 = st.columns([1, 1, 1])
            with sub_q5:
                compat_submit_button(
                    T["btn_clear"],
                    key="clear_cena_m",
                    on_click=_clear_field_cb,
                    args=("cena_m", INITIAL_QUICK),
                )
        with col_or_b:
            st.markdown(or_html, unsafe_allow_html=True)
        with col_margin:
            marza_m = Decimal(
                str(
                    st.number_input(
                        T["new_margin"].replace("Nowa ", "").replace("New ", "").capitalize(),
                        key="marza_m",
                        value=0.0,
                    )
                )
            )
            sub_q7, sub_q8, sub_q9 = st.columns([1, 1, 1])
            with sub_q8:
                compat_submit_button(
                    T["btn_clear"],
                    key="clear_marza_m",
                    on_click=_clear_field_cb,
                    args=("marza_m", INITIAL_QUICK),
                )

        col_actions_q1, col_actions_q2 = st.columns([1, 1])
        with col_actions_q1:
            compat_submit_button(
                T["btn_clear_all"],
                key="clear_quick_all",
                on_click=clear_quick_all_cb,
            )
        with col_actions_q2:
            compat_submit_button(
                T["btn_example"],
                key="load_quick_example",
                on_click=load_quick_example_cb,
            )

        submitted_quick = compat_submit_button(
            T["btn_quick"],
            key="submit_quick",
        )
    if submitted_quick:
        with st.spinner("Obliczanie..."):
            if None in (tkw_m, cena_m, marza_m):
                st.error("Invalid input")
                st.stop()

            pola = [_entered("tkw_m"), _entered("cena_m"), _entered("marza_m")]
            if sum(pola) < 2:
                st.error(T["err_two_values"])
                st.stop()

            if _entered("cena_m") and _entered("tkw_m"):
                marza_m = licz_marze_z_ceny(tkw_m, cena_m) * 100
            elif _entered("tkw_m") and _entered("marza_m"):
                cena_m = cena_z_marzy(
                    tkw_m, marza_m / Decimal(100)
                ).quantize(Decimal("0.01"))
            elif _entered("cena_m") and _entered("marza_m"):
                tkw_m = cena_m * (Decimal("1") - marza_m / Decimal(100))

            st.success(T["res_quick"].format(tkw=tkw_m, price=cena_m, margin=marza_m))

# ====== Informacja o autorze ======
author_html = (
    f"<div style='margin-top:2em;text-align:center;color:#999'>{T['author']}</div>"
)
st.markdown(author_html, unsafe_allow_html=True)
