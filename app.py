import streamlit as st

st.title("Kalkulator marży – demo")
tkw = st.number_input("Koszt jednostkowy (TKW) [zł]", min_value=0.0, step=0.01)
marza = st.number_input("Marża [%]", min_value=0.0, step=0.1)

if st.button("Policz cenę sprzedaży"):
    if marza >= 100:
        st.error("Marża nie może być ≥ 100 %")
    else:
        cena = tkw / (1 - marza/100)
        st.success(f"Cena sprzedaży: **{cena:.2f} zł**")
