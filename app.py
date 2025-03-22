import streamlit as st
from streamlit_option_menu import option_menu

# Configuração da página
st.set_page_config(page_title="Calculadora de Arbitragem", 
                   layout="wide",
                   initial_sidebar_state='expanded')

# Estilo CSS para personalizar o layout
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1rem;  /* Ajusta o espaço no topo */
        }
    """,
    unsafe_allow_html=True
)
# Título do App
st.title("Calculadora de Arbitragem")

# Tipo de estratégia
with st.sidebar:
    selected = option_menu(menu_title="Menu de Arbitragem", 
                           options=["Aumento", "Super Odd"])

if selected == "Aumento":
    st.subheader("Método: Aumento")

    # Layout dos inputs
    col_odd_casa, col_odd_empate, col_odd_fora, col_aposta = st.columns(4)
    #Layout das odds
    with col_odd_casa:
        odd_casa = st.number_input("Odd Casa", min_value=1.00, format="%.2f")
        tipo_odd_casa = st.selectbox("Aumento Casa", ["Normal", "Com 25%", "Com 30%", "Betbra (2,8%)", "Betbra (4,5%)"], key="odd_casa_tipo")
    with col_odd_empate:
        odd_empate = st.number_input("Odd Empate", min_value=1.00, format="%.2f")
        tipo_odd_empate = st.selectbox("Aumento Empate", ["Normal", "Com 25%", "Com 30%", "Betbra (2,8%)", "Betbra (4,5%)"], key="odd_empate_tipo")
    with col_odd_fora:
        odd_fora = st.number_input("Odd Fora", min_value=1.00, format="%.2f")
        tipo_odd_fora = st.selectbox("Aumento Fora", ["Normal", "Com 25%", "Com 30%", "Betbra (2,8%)", "Betbra (4,5%)"], key="odd_fora_tipo")
    # Layout do valor apostado
    with col_aposta:
        tipo_aposta = st.selectbox("Aposta Principal", ["Casa", "Empate", "Fora"])
        valor_apostado = st.number_input("Valor Apostado", min_value=0.0, format="%.2f")

# Cálculo de retorno
def calcular_valores(odd_casa, odd_empate, odd_fora, tipo_odd_casa, tipo_odd_empate, tipo_odd_fora, valor_apostado, tipo_aposta):
    aumentos = {
    "Normal": 0.00,
    "Com 25%": 0.25,
    "Com 30%": 0.30,
    "Betbra (2,8%)": -0.028,
    "Betbra (4,5%)": -0.045}

    odd_casa = (odd_casa - 1) * (1 + aumentos[tipo_odd_casa]) +1
    odd_empate = (odd_empate - 1) * (1 + aumentos[tipo_odd_empate]) +1
    odd_fora = (odd_fora - 1) * (1 + aumentos[tipo_odd_fora]) +1

    try:
        odd_casa, odd_empate, odd_fora, valor_apostado = map(float, [odd_casa, odd_empate, odd_fora, valor_apostado])

        # Distribuição dos valores apostados (aposta proporcional ao valor da odd)
        if tipo_aposta == "Casa":
            aposta_casa = valor_apostado
            retorno = aposta_casa * odd_casa
            aposta_empate = (retorno / odd_empate) if odd_empate > 0 else 0
            aposta_fora = (retorno / odd_fora) if odd_fora > 0 else 0
        elif tipo_aposta == "Empate":
            aposta_empate = valor_apostado
            retorno = aposta_empate * odd_empate
            aposta_casa = (retorno / odd_casa) if odd_casa > 0 else 0
            aposta_fora = (retorno / odd_fora) if odd_fora > 0 else 0
        else:
            aposta_fora = valor_apostado
            retorno = aposta_fora * odd_fora
            aposta_casa = (retorno / odd_casa) if odd_casa > 0 else 0
            aposta_empate = (retorno / odd_empate) if odd_empate > 0 else 0

        total_investido = aposta_casa + aposta_empate + aposta_fora

        lucro = retorno - total_investido

        roi = 0 if total_investido == 0 else (lucro / total_investido) * 100

        return aposta_casa, aposta_empate, aposta_fora, retorno, total_investido, lucro, roi

    except ValueError:
        return None, None, None, None, None

# Para calcular
aposta_casa, aposta_empate, aposta_fora, retorno, total_investido, lucro, roi = calcular_valores(odd_casa, odd_empate, odd_fora, tipo_odd_casa, tipo_odd_empate, tipo_odd_fora, valor_apostado, tipo_aposta)

col_aposta_casa, col_aposta_empate, col_aposta_fora, col_retorno = st.columns(4)
with col_aposta_casa:
    st.markdown(f"**Aposta casa:** R$ {aposta_casa:.2f}")
with col_aposta_empate:
    st.markdown(f"**Aposta Empate:** R$ {aposta_empate:.2f}")
with col_aposta_fora:
    st.markdown(f"**Aposta Fora:** R$ {aposta_fora:.2f}")
with col_retorno:
    st.markdown(f"**Retorno:** R$ {retorno:.2f}")
st.write("##")

col_total_investido, col_lucro, col_roi, col_branco = st.columns(4)
with col_total_investido:
    st.markdown(f"**Total Investido:** R$ {total_investido:.2f}")
with col_lucro:
    st.markdown(f"**Lucro Da Operação:** <span style='color: {'green' if lucro > 0 else 'red' if lucro < 0 else 'white'}'>R$ {lucro:.2f}</span>", unsafe_allow_html=True)
with col_roi:
    st.markdown(f"**ROI:** <span style='color: {'green' if roi > 0 else 'red' if roi < 0 else 'white'}'> {roi:.2f} % </span>", unsafe_allow_html=True)
with col_branco:
    st.markdown("")