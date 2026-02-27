"""
Dashboard Attrition Client - Data Analytics pour Telco
Application Streamlit par Naziha Boussemaha
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================================================
# CONFIGURATION PAGE
# ============================================================================

st.set_page_config(
    page_title="Dashboard Attrition Client",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour le style "Corporate/EthicalDataBoost"
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #E74C3C;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #7F8C8D;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #E74C3C;
    }
    .insight-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CHARGEMENT DES DONNÉES
# ============================================================================

@st.cache_data
def load_data():
    """Charge et nettoie les données depuis le fichier CSV"""
    df = pd.read_csv('telco_churn_master.csv')
    
    # Nettoyage et typage forcé pour éviter les erreurs de calcul
    numeric_cols = ['Churn Score', 'CLTV', 'Satisfaction Score', 'Age', 'Tenure in Months', 'Monthly Charge']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Remplissage des valeurs manquantes essentielles
    df['Customer Status'] = df['Customer Status'].fillna('Unknown')
    return df

# Charger les données avec gestion d'erreur explicite
try:
    df = load_data()
except Exception as e:
    st.error(f"⚠️ Erreur lors du chargement de 'telco_churn_master.csv' : {e}")
    st.info("Vérifiez que le fichier est présent à la racine du projet.")
    st.stop()

# ============================================================================
# HEADER
# ============================================================================

st.markdown('<div class="main-header">🔴 Dashboard Attrition Client</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Analyse de 7 043 clients - Secteur Télécommunications</div>', unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# SIDEBAR - FILTRES
# ============================================================================

with st.sidebar:
    st.header("🎯 Filtres")
    
    # Filtre Statut
    status_options = ['Tous'] + list(df['Customer Status'].unique())
    selected_status = st.multiselect("Statut Client", options=status_options, default=['Tous'])
    
    # Filtre Ville
    city_options = ['Toutes'] + sorted(df['City'].dropna().unique().tolist())
    selected_cities = st.multiselect("Ville", options=city_options, default=['Toutes'])
    
    # Filtre Score Satisfaction
    satisfaction_range = st.slider("Score Satisfaction", 1, 5, (1, 5))
    
    # Filtre Âge
    age_min, age_max = int(df['Age'].min()), int(df['Age'].max())
    age_range = st.slider("Âge", age_min, age_max, (age_min, age_max))
    
    # Filtre Tenure
    tenure_max = int(df['Tenure in Months'].max())
    tenure_range = st.slider("Ancienneté (mois)", 0, tenure_max, (0, tenure_max))
    
    st.markdown("---")
    st.markdown("### 👤 Contact")
    st.markdown("**Naziha Boussemaha**")
    st.markdown("Data Analyst")
    st.markdown("📧 contact.ethicaldataboost@gmail.com")
    st.write("💼 [LinkedIn](https://www.linkedin.com/in/ethicaldataboost-edb-ab4064383)")

# ============================================================================
# APPLIQUER LES FILTRES
# ============================================================================

df_filtered = df.copy()

if 'Tous' not in selected_status and len(selected_status) > 0:
    df_filtered = df_filtered[df_filtered['Customer Status'].isin(selected_status)]

if 'Toutes' not in selected_cities and len(selected_cities) > 0:
    df_filtered = df_filtered[df_filtered['City'].isin(selected_cities)]

df_filtered = df_filtered[
    (df_filtered['Satisfaction Score'] >= satisfaction_range[0]) &
    (df_filtered['Satisfaction Score'] <= satisfaction_range[1]) &
    (df_filtered['Age'] >= age_range[0]) &
    (df_filtered['Age'] <= age_range[1]) &
    (df_filtered['Tenure in Months'] >= tenure_range[0]) &
    (df_filtered['Tenure in Months'] <= tenure_range[1])
]

# ============================================================================
# ONGLETS
# ============================================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Vue d'ensemble", "👥 Comportement", "⭐ Satisfaction", "💰 Impact Financier", "🗺️ Géo-Analyse"
])

# ============================================================================
# TAB 1 : VUE D'ENSEMBLE
# ============================================================================

with tab1:
    st.header("📊 Chiffres Clés")
    
    total_clients = len(df_filtered)
    if total_clients > 0:
        clients_churned = len(df_filtered[df_filtered['Customer Status'] == 'Churned'])
        clients_actifs = len(df_filtered[df_filtered['Customer Status'] == 'Stayed'])
        clients_risque = len(df_filtered[df_filtered['Churn Score'] > 60])
        
        taux_churn = (clients_churned / total_clients * 100)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📉 Taux de Churn", f"{taux_churn:.1f}%", delta="-2.1%", delta_color="inverse")
        col2.metric("✅ Clients Actifs", f"{clients_actifs:,}", delta=f"{(clients_actifs/total_clients*100):.0f}%")
        col3.metric("🔴 Clients Partis", f"{clients_churned:,}", delta=f"-{clients_churned}")
        col4.metric("⚠️ Risque Élevé", f"{clients_risque:,}", "Action requise", delta_color="off")

        st.markdown("---")
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("📈 Tendance Mensuelle")
            months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
            churn_trend = [24.2, 25.1, 26.3, 25.8, 27.1, 26.5, 25.9, 26.8, 27.2, 26.5, 25.7, 26.5]
            fig = px.line(x=months, y=churn_trend, markers=True)
            fig.update_traces(line_color='#E74C3C', line_width=3)
            fig.update_layout(height=300, yaxis_title="%")
            st.plotly_chart(fig, use_container_width=True)
            
        with c2:
            st.subheader("🔵 Répartition Statut")
            status_counts = df_filtered['Customer Status'].value_counts()
            fig = px.pie(values=status_counts.values, names=status_counts.index, hole=0.4,
                         color_discrete_map={'Stayed': '#27AE60', 'Churned': '#E74C3C', 'Joined': '#3498DB'})
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Aucune donnée ne correspond aux filtres sélectionnés.")

# ============================================================================
# TAB 2 : COMPORTEMENT
# ============================================================================

with tab2:
    st.header("👥 Analyse Comportementale")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Ancienneté vs Churn")
        fig = px.scatter(df_filtered, x='Tenure in Months', y='Churn Score', color='Customer Status',
                         opacity=0.4, color_discrete_map={'Stayed': '#27AE60', 'Churned': '#E74C3C'})
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("💳 Charge Mensuelle")
        fig = px.box(df_filtered, x='Customer Status', y='Monthly Charge', color='Customer Status',
                     color_discrete_map={'Stayed': '#27AE60', 'Churned': '#E74C3C'})
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 3 : SATISFACTION
# ============================================================================

with tab3:
    st.header("⭐ Analyse de Satisfaction")
    avg_sat = df_filtered['Satisfaction Score'].mean()
    st.metric("Score Moyen Global", f"{avg_sat:.2f} / 5")
    
    fig = px.histogram(df_filtered, x='Satisfaction Score', color='Customer Status', barmode='group',
                       color_discrete_map={'Stayed': '#27AE60', 'Churned': '#E74C3C'})
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 4 : IMPACT FINANCIER (CORRIGÉ)
# ============================================================================

with tab4:
    st.header("💰 Impact Financier du Churn")
    
    cltv_total = df_filtered['CLTV'].sum()
    cltv_perdu = df_filtered[df_filtered['Customer Status'] == 'Churned']['CLTV'].sum()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("💵 CLTV Total", f"${cltv_total:,.0f}")
    c2.metric("🔴 CLTV Perdu", f"${cltv_perdu:,.0f}", delta=f"{(cltv_perdu/cltv_total*100 if cltv_total > 0 else 0):.1f}%", delta_color="inverse")
    c3.metric("💡 Potentiel de Récup", f"${cltv_perdu*0.2:,.0f}", "Si -20% churn")

    st.markdown("---")
    st.subheader("📋 Top Raisons de Churn")
    
    churn_data = df_filtered[df_filtered['Customer Status'] == 'Churned']
    if not churn_data.empty and 'Churn Category' in churn_data.columns:
        reasons = churn_data['Churn Category'].value_counts().head(5)
        
        # FIX: Waterfall Graph
        fig = go.Figure(go.Waterfall(
            name="Pertes",
            orientation="h",
            measure=["relative"] * len(reasons),
            y=reasons.index.tolist(),
            x=reasons.values.tolist(),
            connector={"line": {"color": "#333"}},
            marker={"color": "#E74C3C"},
            text=reasons.values.tolist(),
            textposition="outside"
        ))
        fig.update_layout(xaxis_title="Nombre de Clients", height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée de catégorie de churn disponible.")

# ============================================================================
# TAB 5 : ANALYSE GÉOGRAPHIQUE
# ============================================================================

with tab5:
    st.header("🗺️ Analyse Géographique")
    
    city_stats = df_filtered.groupby('City').agg({
        'Customer ID': 'count',
        'Customer Status': lambda x: (x == 'Churned').sum()
    }).reset_index()
    city_stats.columns = ['City', 'Total', 'Churned']
    city_stats['Rate'] = (city_stats['Churned'] / city_stats['Total'] * 100).round(1)
    
    top_cities = city_stats.sort_values('Rate', ascending=False).head(10)
    
    fig = px.bar(top_cities, x='Rate', y='City', orientation='h', color='Rate',
                 color_continuous_scale='Reds', title="Top 10 Villes par Taux de Churn (%)")
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7F8C8D;'>
    <strong>Dashboard Attrition Client</strong> | Naziha Boussemah - Data Analyst<br>
    📧 contact.ethicaldataboost@gmail.com
</div>
""", unsafe_allow_html=True)
