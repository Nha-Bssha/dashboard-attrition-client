"""
Dashboard Attrition Client - Data Analytics pour Telco
Application Streamlit par Naziha Boussemaha
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================================
# CONFIGURATION PAGE
# ============================================================================

st.set_page_config(
    page_title="Dashboard Attrition Client",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: bold; color: #E74C3C; text-align: center; margin-bottom: 0.5rem; }
    .sub-header { font-size: 1.2rem; color: #7F8C8D; text-align: center; margin-bottom: 2rem; }
    .insight-box { background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #ffc107; margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CHARGEMENT ET NETTOYAGE DES DONNÉES
# ============================================================================

@st.cache_data
def load_data():
    df = pd.read_csv('telco_churn_master.csv')
    
    # Conversion forcée en numérique pour éviter les calculs impossibles
    cols_numeriques = ['Churn Score', 'CLTV', 'Satisfaction Score', 'Age', 'Tenure in Months', 'Monthly Charge']
    for col in cols_numeriques:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Nettoyage des textes
    df['Customer Status'] = df['Customer Status'].astype(str).fillna('Inconnu')
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Erreur de chargement : {e}")
    st.stop()

# ============================================================================
# SIDEBAR - FILTRES
# ============================================================================

with st.sidebar:
    st.header("🎯 Filtres")
    
    selected_status = st.multiselect("Statut Client", options=['Tous'] + list(df['Customer Status'].unique()), default=['Tous'])
    selected_cities = st.multiselect("Ville", options=['Toutes'] + sorted(df['City'].dropna().unique().tolist()), default=['Toutes'])
    satisfaction_range = st.slider("Score Satisfaction", 1, 5, (1, 5))
    age_range = st.slider("Âge", int(df['Age'].min()), int(df['Age'].max()), (int(df['Age'].min()), int(df['Age'].max())))
    
    st.markdown("---")
    st.markdown("### 👤 Contact")
    st.markdown("**Naziha Boussemaha** (Data Analyst)")
    st.write("💼 [LinkedIn](https://www.linkedin.com/in/ethicaldataboost-edb-ab4064383)")

# Application des filtres
df_filtered = df.copy()
if 'Tous' not in selected_status and selected_status:
    df_filtered = df_filtered[df_filtered['Customer Status'].isin(selected_status)]
if 'Toutes' not in selected_cities and selected_cities:
    df_filtered = df_filtered[df_filtered['City'].isin(selected_cities)]

df_filtered = df_filtered[
    (df_filtered['Satisfaction Score'] >= satisfaction_range[0]) &
    (df_filtered['Satisfaction Score'] <= satisfaction_range[1]) &
    (df_filtered['Age'] >= age_range[0]) &
    (df_filtered['Age'] <= age_range[1])
]

# ============================================================================
# HEADER ET ONGLETS
# ============================================================================

st.markdown('<div class="main-header">🔴 Dashboard Attrition Client</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Analyse Secteur Télécommunications</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Vue d'ensemble", "👥 Comportement", "⭐ Satisfaction", "💰 Impact Financier", "🗺️ Géo-Analyse"])

# --- TAB 1 : VUE D'ENSEMBLE ---
with tab1:
    col1, col2, col3 = st.columns(3)
    total = len(df_filtered)
    churned = len(df_filtered[df_filtered['Customer Status'] == 'Churned'])
    
    col1.metric("Total Clients", f"{total:,}")
    col2.metric("Clients Partis", f"{churned:,}")
    col3.metric("Taux de Churn", f"{(churned/total*100 if total > 0 else 0):.1f}%")

    # Graphique Pie
    status_counts = df_filtered['Customer Status'].value_counts()
    fig_pie = px.pie(values=status_counts.values, names=status_counts.index, hole=0.4, 
                     color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_pie, use_container_width=True)

# --- TAB 4 : IMPACT FINANCIER (LA SECTION CRITIQUE) ---
with tab4:
    st.header("💰 Impact Financier du Churn")
    
    # Filtrer uniquement les départs
    df_churned = df_filtered[df_filtered['Customer Status'] == 'Churned']
    
    if not df_churned.empty:
        st.subheader("📋 Top Raisons de Churn")
        
        # Préparation des données pour le Waterfall
        reasons = df_churned['Churn Category'].value_counts().head(5)
        
        if not reasons.empty:
            # Création du Waterfall avec protection des types
            fig_waterfall = go.Figure(go.Waterfall(
                orientation = "h",
                measure = ["relative"] * len(reasons),
                y = reasons.index.tolist(),
                x = [float(x) for x in reasons.values], # Conversion explicite en float
                connector = {"line":{"color":"#E74C3C"}},
                text = [str(x) for x in reasons.values],
                textposition = "outside"
            ))
            
            fig_waterfall.update_layout(
                title="Décomposition des départs par catégorie",
                xaxis_title="Nombre de clients",
                height=400,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            
            st.plotly_chart(fig_waterfall, use_container_width=True)
        else:
            st.info("Aucune catégorie de churn renseignée pour ces clients.")
    else:
        st.warning("Aucun client 'Churned' trouvé avec les filtres actuels pour afficher l'impact financier.")

# --- TAB 5 : GÉO-ANALYSE ---
with tab5:
    st.subheader("🗺️ Top Villes par Taux de Churn")
    city_stats = df_filtered.groupby('City').agg({'Customer Status': lambda x: (x == 'Churned').sum(), 'Customer ID': 'count'})
    city_stats.columns = ['Churned', 'Total']
    city_stats['Rate'] = (city_stats['Churned'] / city_stats['Total'] * 100)
    
    top_cities = city_stats.sort_values('Rate', ascending=False).head(10).reset_index()
    fig_geo = px.bar(top_cities, x='Rate', y='City', orientation='h', color='Rate', color_continuous_scale='Reds')
    st.plotly_chart(fig_geo, use_container_width=True)
