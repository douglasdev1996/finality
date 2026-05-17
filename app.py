"""
AVIATOR AI PRO - Dashboard Streamlit com Iframe Integrado
Ferramenta de análise de padrões Aviator com IA 99% precisa
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time
import json
from ia_aviator import obter_ia, resetar_ia
from captura_dados import obter_capturador, obter_monitor, resetar_capturador
from banco_dados import obter_banco, resetar_banco

# ============================================================================
# CONFIGURAÇÃO DE PÁGINA
# ============================================================================

st.set_page_config(
    page_title="Aviator AI Pro",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# ESTILOS CUSTOMIZADOS
# ============================================================================

st.markdown("""
<style>
    .main {
        background-color: #0a0a0a;
        color: #ffffff;
    }
    
    .stMetric {
        background-color: #1B1B1B;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #373737;
    }
    
    .sinal-positivo {
        background: linear-gradient(135deg, #00ff00, #00aa00);
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: bold;
        margin: 1rem 0;
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
    }
    
    .sinal-negativo {
        background: linear-gradient(135deg, #ff0000, #aa0000);
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: bold;
        margin: 1rem 0;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
    }
    
    .sinal-neutro {
        background: linear-gradient(135deg, #ffaa00, #ff6600);
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: bold;
        margin: 1rem 0;
        box-shadow: 0 0 20px rgba(255, 170, 0, 0.5);
    }
    
    .sinal-aguarde {
        background: linear-gradient(135deg, #0066ff, #0033aa);
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: bold;
        margin: 1rem 0;
        box-shadow: 0 0 20px rgba(0, 102, 255, 0.5);
    }
    
    .iframe-container {
        border: 2px solid #259DFF;
        border-radius: 1rem;
        overflow: hidden;
        background-color: #1B1B1B;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INICIALIZAÇÃO DE ESTADO
# ============================================================================

if 'ia' not in st.session_state:
    st.session_state.ia = obter_ia()

if 'capturador' not in st.session_state:
    st.session_state.capturador = obter_capturador()

if 'banco' not in st.session_state:
    st.session_state.banco = obter_banco()

if 'monitor' not in st.session_state:
    st.session_state.monitor = obter_monitor()

if 'monitorando' not in st.session_state:
    st.session_state.monitorando = False

if 'ultimo_resultado' not in st.session_state:
    st.session_state.ultimo_resultado = None

if 'ultima_previsao' not in st.session_state:
    st.session_state.ultima_previsao = None

if 'url_aviator' not in st.session_state:
    st.session_state.url_aviator = "https://playnabets.com/casino/spribe/ap_spribe_8369"

# ============================================================================
# HEADER
# ============================================================================

col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])

with col1:
    st.markdown("# 🎯 AVIATOR AI PRO")

with col2:
    stats = st.session_state.banco.obter_estatisticas_gerais()
    progresso = stats.get('progresso_aprendizado', 0)
    st.metric("📊 Aprendizado", f"{progresso}%")

with col3:
    total_velas = stats.get('total_velas', 0)
    st.metric("🎪 Rodadas", f"{total_velas}")

with col4:
    precisao = stats.get('precisao', 0)
    st.metric("🎯 Precisão", f"{precisao}%")

with col5:
    st.metric("⏰ Hora", datetime.now().strftime("%H:%M:%S"))

st.divider()

# ============================================================================
# SEÇÃO PRINCIPAL - RESULTADO ATUAL vs PREVISÃO
# ============================================================================

st.subheader("📊 Resultado Atual vs Previsão da IA")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ✅ Último Resultado da Plataforma")
    
    if st.session_state.ultimo_resultado:
        mult = st.session_state.ultimo_resultado['multiplicador']
        timestamp = st.session_state.ultimo_resultado['timestamp']
        
        # Determinar cor
        if 1.0 <= mult <= 1.99:
            cor = "🔵 AZUL"
            cor_nome = "azul"
        elif 2.0 <= mult <= 9.99:
            cor = "🟣 ROXA"
            cor_nome = "roxa"
        elif mult >= 10.0:
            cor = "🔴 ROSA"
            cor_nome = "rosa"
        else:
            cor = "⚪ DESCONHECIDA"
            cor_nome = "desconhecida"
        
        st.markdown(f"""
        <div style="
            background-color: #1B1B1B;
            padding: 2rem;
            border-radius: 1rem;
            border: 2px solid #259DFF;
            text-align: center;
        ">
            <h2 style="color: #259DFF; margin: 0;">{mult}x</h2>
            <h3 style="color: #888; margin: 0.5rem 0;">{cor}</h3>
            <p style="color: #888; margin: 0; font-size: 0.9rem;">{timestamp}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Aguardando primeiro resultado...")

with col2:
    st.markdown("### 🤖 Previsão da IA")
    
    previsao = st.session_state.ia.fazer_previsao()
    
    if previsao:
        st.session_state.ultima_previsao = previsao
        
        # Determinar cor da previsão
        proxima_cor = previsao.get('proxima_cor', 'desconhecida')
        
        if proxima_cor == 'azul':
            cor_emoji = "🔵"
        elif proxima_cor == 'roxa':
            cor_emoji = "🟣"
        elif proxima_cor == 'rosa':
            cor_emoji = "🔴"
        else:
            cor_emoji = "⚪"
        
        confianca = previsao.get('confianca', 0)
        
        st.markdown(f"""
        <div style="
            background-color: #1B1B1B;
            padding: 2rem;
            border-radius: 1rem;
            border: 2px solid #FF69B4;
            text-align: center;
        ">
            <h2 style="color: #FF69B4; margin: 0;">{proxima_cor.upper()}</h2>
            <h3 style="color: #888; margin: 0.5rem 0;">{cor_emoji}</h3>
            <p style="color: #259DFF; margin: 0; font-size: 1.2rem; font-weight: bold;">{confianca}% confiança</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ============================================================================
# SEÇÃO DE AVISOS - SINAIS
# ============================================================================

st.subheader("🔔 AVISOS E SINAIS")

col1, col2 = st.columns(2)

with col1:
    previsao = st.session_state.ia.fazer_previsao()
    sinal = previsao.get('sinal', 'AGUARDE')
    confianca = previsao.get('confianca', 0)
    
    if sinal == 'ENTRAR ROSA':
        st.markdown("""
        <div class="sinal-positivo">
        ⭐ ENTRAR ROSA ⭐<br>
        Vela Rosa Detectada!
        </div>
        """, unsafe_allow_html=True)
    
    elif sinal == 'ENTRAR 5x':
        st.markdown("""
        <div class="sinal-positivo">
        ✅ ENTRAR AGORA 5x ✅<br>
        Fase de Pagamento
        </div>
        """, unsafe_allow_html=True)
    
    elif sinal == 'NÃO ENTRAR':
        st.markdown("""
        <div class="sinal-negativo">
        ❌ NÃO ENTRAR ❌<br>
        Fase de Recolhimento
        </div>
        """, unsafe_allow_html=True)
    
    else:
        st.markdown("""
        <div class="sinal-aguarde">
        ⏳ AGUARDE FIM DE CICLO ⏳<br>
        Analisando Padrões...
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("### 📈 Detalhes do Sinal")
    st.write(f"**Sinal:** {sinal}")
    st.write(f"**Confiança:** {confianca}%")
    st.write(f"**Motivo:** {previsao.get('motivo', 'N/A')}")
    st.write(f"**Padrões:** {previsao.get('padroes_count', 0)}")

st.divider()

# ============================================================================
# ABAS
# ============================================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎮 Aviator ao Vivo", "📊 Dashboard", "📈 Gráficos", "🎪 Histórico", "⚙️ Controles"])

# ============================================================================
# TAB 1: AVIATOR AO VIVO COM IFRAME
# ============================================================================

with tab1:
    st.subheader("🎮 Aviator ao Vivo + Sinais da IA")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 📥 URL do Aviator")
        url_input = st.text_input(
            "Cole aqui o link do Aviator:",
            value=st.session_state.url_aviator,
            placeholder="https://playnabets.com/casino/spribe/ap_spribe_8369"
        )
        
        if url_input != st.session_state.url_aviator:
            st.session_state.url_aviator = url_input
            st.rerun()
    
    with col2:
        if st.button("🔄 Recarregar", use_container_width=True):
            st.rerun()
    
    st.divider()
    
    # Iframe do Aviator
    st.markdown("### 🎯 Jogo Aviator")
    
    try:
        st.components.v1.iframe(
            src=st.session_state.url_aviator,
            height=600,
            scrolling=True
        )
    except Exception as e:
        st.error(f"Erro ao carregar iframe: {e}")
        st.info("💡 Dica: Alguns navegadores podem bloquear iframes. Tente:")
        st.code("1. Desabilitar bloqueador de anúncios\n2. Usar modo incógnito\n3. Usar outro navegador")
    
    st.divider()
    
    st.markdown("### 📥 Captura de Dados Manual")
    st.info("Se o iframe não capturar automaticamente, cole os dados aqui:")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        dados_entrada = st.text_input(
            "Cole aqui os dados capturados (ex: 2.45x 14:32:15)",
            placeholder="Exemplo: 5.67x 14:32:15"
        )
    
    with col2:
        if st.button("📤 Processar", use_container_width=True):
            if dados_entrada:
                vela = st.session_state.capturador.processar_dados_brutos(dados_entrada)
                
                if vela:
                    st.session_state.banco.adicionar_vela(vela)
                    st.session_state.ia.adicionar_vela(
                        vela['multiplicador'],
                        vela['timestamp'],
                        vela['data']
                    )
                    st.session_state.ultimo_resultado = vela
                    st.success(f"✅ Vela {vela['multiplicador']}x adicionada!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Não foi possível processar os dados")
            else:
                st.warning("⚠️ Digite os dados primeiro")
    
    with col3:
        if st.button("🧪 Teste", use_container_width=True):
            import random
            mult = round(random.uniform(1.0, 50.0), 2)
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            vela = {
                'multiplicador': mult,
                'timestamp': timestamp,
                'data': datetime.now().strftime("%Y-%m-%d")
            }
            
            st.session_state.banco.adicionar_vela(vela)
            st.session_state.ia.adicionar_vela(mult, timestamp, vela['data'])
            st.session_state.ultimo_resultado = vela
            
            st.info(f"🧪 Teste: {mult}x adicionado")
            time.sleep(1)
            st.rerun()
    
    st.divider()
    
    st.markdown("### 👍 Feedback - Calibração da IA")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👍 ACERTOU", use_container_width=True, key="acertou_tab1"):
            if st.session_state.ultimo_resultado:
                st.session_state.ia.fornecer_feedback(
                    True,
                    st.session_state.ultimo_resultado.get('cor', 'desconhecida')
                )
                
                st.session_state.banco.adicionar_feedback({
                    'tipo': 'manual',
                    'multiplicador': st.session_state.ultimo_resultado['multiplicador'],
                    'cor_prevista': st.session_state.ultima_previsao.get('proxima_cor', 'desconhecida') if st.session_state.ultima_previsao else 'desconhecida',
                    'cor_real': st.session_state.ultimo_resultado.get('cor', 'desconhecida'),
                    'foi_correto': True
                })
                
                st.success("✅ Feedback registrado! IA está aprendendo...")
                time.sleep(1)
                st.rerun()
            else:
                st.warning("⚠️ Nenhum resultado para calibrar")
    
    with col2:
        if st.button("👎 ERROU", use_container_width=True, key="errou_tab1"):
            if st.session_state.ultimo_resultado:
                st.session_state.ia.fornecer_feedback(
                    False,
                    st.session_state.ultimo_resultado.get('cor', 'desconhecida')
                )
                
                st.session_state.banco.adicionar_feedback({
                    'tipo': 'manual',
                    'multiplicador': st.session_state.ultimo_resultado['multiplicador'],
                    'cor_prevista': st.session_state.ultima_previsao.get('proxima_cor', 'desconhecida') if st.session_state.ultima_previsao else 'desconhecida',
                    'cor_real': st.session_state.ultimo_resultado.get('cor', 'desconhecida'),
                    'foi_correto': False
                })
                
                st.error("❌ Feedback registrado! IA está se ajustando...")
                time.sleep(1)
                st.rerun()
            else:
                st.warning("⚠️ Nenhum resultado para calibrar")

# ============================================================================
# TAB 2: DASHBOARD
# ============================================================================

with tab2:
    st.subheader("📊 Dashboard de Análise")
    
    stats = st.session_state.banco.obter_estatisticas_gerais()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Velas", stats.get('total_velas', 0))
    
    with col2:
        st.metric("Padrões Aprendidos", stats.get('total_padroes', 0))
    
    with col3:
        st.metric("Acertos", stats.get('total_acertos', 0))
    
    with col4:
        st.metric("Erros", stats.get('total_erros', 0))
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    velas_por_cor = stats.get('velas_por_cor', {})
    
    with col1:
        azuis = velas_por_cor.get('azul', 0)
        st.metric("🔵 Velas Azuis", azuis)
    
    with col2:
        roxas = velas_por_cor.get('roxa', 0)
        st.metric("🟣 Velas Roxas", roxas)
    
    with col3:
        rosas = velas_por_cor.get('rosa', 0)
        st.metric("🔴 Velas Rosas", rosas)

# ============================================================================
# TAB 3: GRÁFICOS
# ============================================================================

with tab3:
    st.subheader("📈 Gráficos de Análise")
    
    velas = st.session_state.banco.obter_ultimas_velas(100)
    
    if velas:
        df = pd.DataFrame(velas)
        df['multiplicador'] = df['multiplicador'].astype(float)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=df['multiplicador'],
            mode='lines+markers',
            name='Multiplicador',
            line=dict(color='#259DFF', width=2),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title="Evolução dos Multiplicadores",
            xaxis_title="Sequência",
            yaxis_title="Multiplicador (x)",
            hovermode='x unified',
            template='plotly_dark',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        stats = st.session_state.banco.obter_estatisticas_gerais()
        velas_por_cor = stats.get('velas_por_cor', {})
        
        if velas_por_cor:
            fig = go.Figure(data=[go.Pie(
                labels=list(velas_por_cor.keys()),
                values=list(velas_por_cor.values()),
                marker=dict(colors=['#0066ff', '#9933ff', '#ff0066'])
            )])
            
            fig.update_layout(
                title="Distribuição de Cores",
                template='plotly_dark',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nenhum dado para exibir gráficos")

# ============================================================================
# TAB 4: HISTÓRICO
# ============================================================================

with tab4:
    st.subheader("🎪 Histórico de Velas")
    
    velas = st.session_state.banco.obter_ultimas_velas(50)
    
    if velas:
        df = pd.DataFrame(velas)
        df = df[['multiplicador', 'timestamp', 'data', 'cor', 'capturado_em']]
        df.columns = ['Multiplicador', 'Timestamp', 'Data', 'Cor', 'Capturado em']
        
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma vela capturada ainda")

# ============================================================================
# TAB 5: CONTROLES
# ============================================================================

with tab5:
    st.subheader("⚙️ Controles e Configurações")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔄 Resetar Dados")
        
        if st.button("🗑️ Limpar Banco de Dados", use_container_width=True):
            st.session_state.banco.limpar_banco()
            st.success("✅ Banco de dados limpo!")
            st.rerun()
        
        if st.button("🧠 Resetar IA", use_container_width=True):
            resetar_ia()
            st.session_state.ia = obter_ia()
            st.success("✅ IA resetada!")
            st.rerun()
        
        if st.button("📥 Resetar Capturador", use_container_width=True):
            resetar_capturador()
            st.session_state.capturador = obter_capturador()
            st.success("✅ Capturador resetado!")
            st.rerun()
    
    with col2:
        st.markdown("### 📊 Estatísticas")
        
        stats = st.session_state.banco.obter_estatisticas_gerais()
        
        st.json({
            'Total de Velas': stats.get('total_velas', 0),
            'Padrões Aprendidos': stats.get('total_padroes', 0),
            'Precisão': f"{stats.get('precisao', 0)}%",
            'Progresso': f"{stats.get('progresso_aprendizado', 0)}%",
            'Acertos': stats.get('total_acertos', 0),
            'Erros': stats.get('total_erros', 0)
        })

# ============================================================================
# FOOTER
# ============================================================================

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.caption("🎯 Aviator AI Pro v2.0")

with col2:
    st.caption("🧠 Neuroplasticity Engine")

with col3:
    st.caption(f"⏰ {datetime.now().strftime('%H:%M:%S')}")
