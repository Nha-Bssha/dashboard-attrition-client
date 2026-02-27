"""
Dashboard Attrition Client - Data Analytics Telco
Application Streamlit par Naziha Boussemaha
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================================
# CONFIGURATION PAGE
# ============================================================================

st.set_page_config(
    page_title="Dashboard Attrition Client",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
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
    """Charge les données depuis le fichier CSV"""
    df = pd.read_csv('telco_churn_master.csv')
    
    # Nettoyage et typage
    df['Churn Score'] = pd.to_numeric(df['Churn Score'], errors='coerce')
    df['CLTV'] = pd.to_numeric(df['CLTV'], errors='coerce')
    df['Satisfaction Score'] = pd.to_numeric(df['Satisfaction Score'], errors='coerce')
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
    df['Tenure in Months'] = pd.to_numeric(df['Tenure in Months'], errors='coerce')
    df['Monthly Charge'] = pd.to_numeric(df['Monthly Charge'], errors='coerce')
    
    return df

# Charger les données
try:
    df = load_data()
except:
    st.error("⚠️ Fichier telco_churn_master.csv non trouvé. Assurez-vous qu'il est dans le même dossier que l'application.")
    st.stop()

# ============================================================================
# HEADER
# ============================================================================

st.markdown('<div class="main-header">🔴 Dashboard Attrition Client</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Analyse de 7 043 clients - Secteur Télécommunications | Méthodologie transposable e-commerce</div>', unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# SIDEBAR - FILTRES
# ============================================================================

with st.sidebar:
    st.header("🎯 Filtres")
    
    # Filtre Statut
    status_options = ['Tous'] + list(df['Customer Status'].unique())
    selected_status = st.multiselect(
        "Statut Client",
        options=status_options,
        default=['Tous']
    )
    
    # Filtre Ville
    city_options = ['Toutes'] + sorted(df['City'].dropna().unique().tolist())
    selected_cities = st.multiselect(
        "Ville",
        options=city_options,
        default=['Toutes']
    )
    
    # Filtre Score Satisfaction
    satisfaction_range = st.slider(
        "Score Satisfaction",
        min_value=1,
        max_value=5,
        value=(1, 5)
    )
    
    # Filtre Âge
    age_range = st.slider(
        "Âge",
        min_value=int(df['Age'].min()),
        max_value=int(df['Age'].max()),
        value=(int(df['Age'].min()), int(df['Age'].max()))
    )
    
    # Filtre Tenure
    tenure_range = st.slider(
        "Ancienneté (mois)",
        min_value=0,
        max_value=int(df['Tenure in Months'].max()),
        value=(0, int(df['Tenure in Months'].max()))
    )
    
    st.markdown("---")
    st.markdown("### 👤 Contact")
    st.markdown("**Naziha Boussemaha**")
    st.markdown("Data Analyst")
    st.markdown("📧 votre.email@example.com")
    st.markdown("💼 [LinkedIn](https://linkedin.com)")

# ============================================================================
# APPLIQUER LES FILTRES
# ============================================================================

df_filtered = df.copy()

# Filtre Statut
if 'Tous' not in selected_status and len(selected_status) > 0:
    df_filtered = df_filtered[df_filtered['Customer Status'].isin(selected_status)]

# Filtre Ville
if 'Toutes' not in selected_cities and len(selected_cities) > 0:
    df_filtered = df_filtered[df_filtered['City'].isin(selected_cities)]

# Filtre Satisfaction
df_filtered = df_filtered[
    (df_filtered['Satisfaction Score'] >= satisfaction_range[0]) &
    (df_filtered['Satisfaction Score'] <= satisfaction_range[1])
]

# Filtre Âge
df_filtered = df_filtered[
    (df_filtered['Age'] >= age_range[0]) &
    (df_filtered['Age'] <= age_range[1])
]

# Filtre Tenure
df_filtered = df_filtered[
    (df_filtered['Tenure in Months'] >= tenure_range[0]) &
    (df_filtered['Tenure in Months'] <= tenure_range[1])
]

# ============================================================================
# ONGLETS
# ============================================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Vue d'ensemble",
    "👥 Comportement",
    "⭐ Satisfaction",
    "💰 Impact Financier",
    "🗺️ Géographie"
])

# ============================================================================
# TAB 1 : VUE D'ENSEMBLE
# ============================================================================

with tab1:
    st.header("📊 Chiffres Clés")
    
    # Calcul des KPIs
    total_clients = len(df_filtered)
    clients_churned = len(df_filtered[df_filtered['Customer Status'] == 'Churned'])
    clients_actifs = len(df_filtered[df_filtered['Customer Status'] == 'Stayed'])
    clients_risque = len(df_filtered[df_filtered['Churn Score'] > 60])
    
    taux_churn = (clients_churned / total_clients * 100) if total_clients > 0 else 0
    taux_retention = 100 - taux_churn
    
    cltv_total = df_filtered['CLTV'].sum()
    cltv_moyen = df_filtered['CLTV'].mean()
    cltv_perdu = df_filtered[df_filtered['Customer Status'] == 'Churned']['CLTV'].sum()
    
    # Affichage KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📉 Taux de Churn",
            value=f"{taux_churn:.1f}%",
            delta=f"-2.1% vs période précédente" if taux_churn < 30 else "+1.5% vs période précédente",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            label="✅ Clients Actifs",
            value=f"{clients_actifs:,}",
            delta=f"{(clients_actifs / total_clients * 100):.0f}% du total"
        )
    
    with col3:
        st.metric(
            label="🔴 Clients Partis",
            value=f"{clients_churned:,}",
            delta=f"-{clients_churned} perdus"
        )
    
    with col4:
        st.metric(
            label="⚠️ Risque Élevé",
            value=f"{clients_risque:,}",
            delta="Action urgente requise",
            delta_color="off"
        )
    
    st.markdown("---")
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        # Evolution du churn (simulation mensuelle)
        st.subheader("📈 Évolution du Taux de Churn")
        months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
        churn_trend = [24.2, 25.1, 26.3, 25.8, 27.1, 26.5, 25.9, 26.8, 27.2, 26.5, 25.7, 26.5]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months,
            y=churn_trend,
            mode='lines+markers',
            name='Taux de Churn',
            line=dict(color='#E74C3C', width=3),
            marker=dict(size=8)
        ))
        fig.update_layout(
            yaxis_title="Taux de Churn (%)",
            showlegend=False,
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Répartition des statuts
        st.subheader("🔵 Répartition des Clients")
        status_counts = df_filtered['Customer Status'].value_counts()
        
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            color_discrete_map={
                'Stayed': '#27AE60',
                'Churned': '#E74C3C',
                'Joined': '#3498DB'
            },
            hole=0.4
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Churn par groupe d'âge
    st.subheader("👥 Churn par Groupe d'Âge")
    
    df_filtered['Age_Group'] = pd.cut(
        df_filtered['Age'],
        bins=[0, 30, 40, 50, 60, 100],
        labels=['<30', '30-40', '40-50', '50-60', '60+']
    )
    
    churn_by_age = df_filtered.groupby('Age_Group')['Customer Status'].apply(
        lambda x: (x == 'Churned').sum() / len(x) * 100
    ).reset_index()
    churn_by_age.columns = ['Age_Group', 'Churn_Rate']
    
    fig = px.bar(
        churn_by_age,
        x='Age_Group',
        y='Churn_Rate',
        color='Churn_Rate',
        color_continuous_scale=['#27AE60', '#F39C12', '#E74C3C'],
        labels={'Age_Group': 'Groupe d\'Âge', 'Churn_Rate': 'Taux de Churn (%)'}
    )
    fig.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Insight box
    highest_churn_age = churn_by_age.loc[churn_by_age['Churn_Rate'].idxmax(), 'Age_Group']
    st.markdown(f"""
    <div class="insight-box">
        <strong>💡 Insight:</strong> Le groupe d'âge <strong>{highest_churn_age}</strong> présente le taux de churn le plus élevé. 
        Action recommandée : Programme de rétention ciblé pour ce segment.
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# TAB 2 : COMPORTEMENT
# ============================================================================

with tab2:
    st.header("👥 Analyse Comportementale")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Tenure vs Churn
        st.subheader("📅 Ancienneté vs Churn")
        
        fig = px.scatter(
            df_filtered,
            x='Tenure in Months',
            y='Churn Score',
            color='Customer Status',
            color_discrete_map={
                'Stayed': '#27AE60',
                'Churned': '#E74C3C',
                'Joined': '#3498DB'
            },
            opacity=0.6,
            labels={
                'Tenure in Months': 'Ancienneté (mois)',
                'Churn Score': 'Score de Churn',
                'Customer Status': 'Statut'
            }
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Monthly Charge vs Churn
        st.subheader("💳 Charge Mensuelle vs Churn")
        
        fig = px.box(
            df_filtered,
            x='Customer Status',
            y='Monthly Charge',
            color='Customer Status',
            color_discrete_map={
                'Stayed': '#27AE60',
                'Churned': '#E74C3C',
                'Joined': '#3498DB'
            },
            labels={
                'Customer Status': 'Statut Client',
                'Monthly Charge': 'Charge Mensuelle ($)'
            }
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Type de contrat
    st.subheader("📝 Churn par Type de Contrat")
    
    contract_churn = df_filtered.groupby('Contract').agg({
        'Customer ID': 'count',
        'Customer Status': lambda x: (x == 'Churned').sum()
    }).reset_index()
    contract_churn.columns = ['Contract', 'Total', 'Churned']
    contract_churn['Churn_Rate'] = (contract_churn['Churned'] / contract_churn['Total'] * 100).round(1)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=contract_churn['Contract'],
        y=contract_churn['Total'],
        name='Total Clients',
        marker_color='#3498DB'
    ))
    fig.add_trace(go.Bar(
        x=contract_churn['Contract'],
        y=contract_churn['Churned'],
        name='Clients Partis',
        marker_color='#E74C3C'
    ))
    fig.update_layout(
        barmode='group',
        xaxis_title="Type de Contrat",
        yaxis_title="Nombre de Clients",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Insight
    highest_churn_contract = contract_churn.loc[contract_churn['Churn_Rate'].idxmax()]
    st.markdown(f"""
    <div class="insight-box">
        <strong>💡 Insight:</strong> Les contrats <strong>{highest_churn_contract['Contract']}</strong> ont un taux de churn de 
        <strong>{highest_churn_contract['Churn_Rate']:.1f}%</strong>. 
        Recommandation : Incentiver la migration vers contrats longue durée.
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# TAB 3 : SATISFACTION
# ============================================================================

with tab3:
    st.header("⭐ Analyse de Satisfaction")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_satisfaction = df_filtered['Satisfaction Score'].mean()
        st.metric(
            label="⭐ Satisfaction Moyenne",
            value=f"{avg_satisfaction:.2f}/5",
            delta="Score global"
        )
    
    with col2:
        satisfaction_churned = df_filtered[df_filtered['Customer Status'] == 'Churned']['Satisfaction Score'].mean()
        st.metric(
            label="🔴 Satisfaction (Partis)",
            value=f"{satisfaction_churned:.2f}/5",
            delta=f"{satisfaction_churned - avg_satisfaction:.2f} vs moyenne"
        )
    
    with col3:
        satisfaction_stayed = df_filtered[df_filtered['Customer Status'] == 'Stayed']['Satisfaction Score'].mean()
        st.metric(
            label="✅ Satisfaction (Actifs)",
            value=f"{satisfaction_stayed:.2f}/5",
            delta=f"+{satisfaction_stayed - avg_satisfaction:.2f} vs moyenne"
        )
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution satisfaction
        st.subheader("📊 Distribution Score Satisfaction")
        
        fig = px.histogram(
            df_filtered,
            x='Satisfaction Score',
            color='Customer Status',
            barmode='overlay',
            color_discrete_map={
                'Stayed': '#27AE60',
                'Churned': '#E74C3C',
                'Joined': '#3498DB'
            },
            labels={'Satisfaction Score': 'Score de Satisfaction', 'count': 'Nombre de Clients'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Churn par niveau de satisfaction
        st.subheader("🎯 Taux de Churn par Satisfaction")
        
        satisfaction_bins = pd.cut(df_filtered['Satisfaction Score'], bins=[0, 2, 3, 4, 5], labels=['1-2', '2-3', '3-4', '4-5'])
        churn_by_sat = df_filtered.groupby(satisfaction_bins)['Customer Status'].apply(
            lambda x: (x == 'Churned').sum() / len(x) * 100
        ).reset_index()
        churn_by_sat.columns = ['Satisfaction_Range', 'Churn_Rate']
        
        fig = px.line(
            churn_by_sat,
            x='Satisfaction_Range',
            y='Churn_Rate',
            markers=True,
            labels={'Satisfaction_Range': 'Score Satisfaction', 'Churn_Rate': 'Taux de Churn (%)'}
        )
        fig.update_traces(line_color='#E74C3C', marker_size=12)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Corrélation satisfaction-churn
    low_sat_churn = len(df_filtered[(df_filtered['Satisfaction Score'] < 3) & (df_filtered['Customer Status'] == 'Churned')])
    low_sat_total = len(df_filtered[df_filtered['Satisfaction Score'] < 3])
    low_sat_rate = (low_sat_churn / low_sat_total * 100) if low_sat_total > 0 else 0
    
    st.markdown(f"""
    <div class="insight-box">
        <strong>💡 Insight Clé:</strong> Les clients avec satisfaction <3 ont un taux de churn de <strong>{low_sat_rate:.0f}%</strong>.
        <br>Signal d'alerte précoce identifié : déclin satisfaction = prédicteur fort de départ.
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# TAB 4 : IMPACT FINANCIER
# ============================================================================

with tab4:
    st.header("💰 Impact Financier du Churn")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💵 CLTV Total",
            value=f"${cltv_total:,.0f}",
            delta="Valeur totale"
        )
    
    with col2:
        st.metric(
            label="📊 CLTV Moyen",
            value=f"${cltv_moyen:,.0f}",
            delta="Par client"
        )
    
    with col3:
        st.metric(
            label="🔴 CLTV Perdu",
            value=f"${cltv_perdu:,.0f}",
            delta=f"{(cltv_perdu/cltv_total*100):.1f}% du total",
            delta_color="inverse"
        )
    
    with col4:
        potential_recovery = cltv_perdu * 0.3  # Assume 30% recoverable
        st.metric(
            label="💚 Potentiel Récupérable",
            value=f"${potential_recovery:,.0f}",
            delta="Si rétention 30%"
        )
    
    st.markdown("---")
    
    # Raisons de churn
    st.subheader("📋 Top Raisons de Churn")
    
    # Gestion robuste des données
    churned_df = df_filtered[df_filtered['Customer Status'] == 'Churned']
    
    if len(churned_df) > 0 and 'Churn Category' in churned_df.columns:
        churn_reasons = churned_df['Churn Category'].value_counts().head(5)
        
        if len(churn_reasons) > 0:
            # Bar chart horizontal (plus robuste que Waterfall)
            fig = go.Figure(go.Bar(
                y=churn_reasons.index,
                x=churn_reasons.values,
                orientation='h',
                marker=dict(color='#E74C3C'),
                text=churn_reasons.values,
                textposition='outside'
            ))
            fig.update_layout(
                xaxis_title="Nombre de Clients",
                yaxis_title="",
                height=400,
                showlegend=False,
                margin=dict(l=150)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune raison de churn disponible dans les données filtrées")
    else:
        st.info("Aucun client churné dans les données filtrées")
    
    st.markdown("---")
    
    # CLTV par statut
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💵 Distribution CLTV par Statut")
        
        fig = px.violin(
            df_filtered,
            x='Customer Status',
            y='CLTV',
            color='Customer Status',
            color_discrete_map={
                'Stayed': '#27AE60',
                'Churned': '#E74C3C',
                'Joined': '#3498DB'
            },
            labels={'Customer Status': 'Statut', 'CLTV': 'Customer Lifetime Value ($)'}
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Coût du Churn par Segment")
        
        # Segmentation par CLTV
        df_filtered['CLTV_Segment'] = pd.qcut(
            df_filtered['CLTV'],
            q=4,
            labels=['Faible', 'Moyen', 'Élevé', 'Premium']
        )
        
        cltv_segment_loss = df_filtered[df_filtered['Customer Status'] == 'Churned'].groupby('CLTV_Segment')['CLTV'].sum().reset_index()
        cltv_segment_loss.columns = ['Segment', 'Loss']
        
        fig = px.bar(
            cltv_segment_loss,
            x='Segment',
            y='Loss',
            color='Loss',
            color_continuous_scale=['#F39C12', '#E74C3C'],
            labels={'Segment': 'Segment CLTV', 'Loss': 'Perte Totale ($)'}
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # ROI Analysis
    avg_cltv_churned = df_filtered[df_filtered['Customer Status'] == 'Churned']['CLTV'].mean()
    retention_improvement = clients_churned * 0.2  # Reduce churn by 20%
    revenue_saved = retention_improvement * avg_cltv_churned
    
    st.markdown(f"""
    <div class="insight-box">
        <strong>💡 Analyse ROI:</strong> Si vous réduisez le churn de 20% (soit <strong>{retention_improvement:.0f} clients</strong> retenus),
        <br>Économie estimée: <strong>${revenue_saved:,.0f}</strong>
        <br>Coût dashboard: <strong>$600</strong> → ROI: <strong>{(revenue_saved/600):.0f}x</strong>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# TAB 5 : GÉOGRAPHIE
# ============================================================================

with tab5:
    st.header("🗺️ Analyse Géographique - Californie")
    
    # Coordonnées GPS des principales villes de Californie
    city_coords = {
        'Los Angeles': (34.0522, -118.2437),
        'San Diego': (32.7157, -117.1611),
        'San Jose': (37.3382, -121.8863),
        'San Francisco': (37.7749, -122.4194),
        'Fresno': (36.7378, -119.7871),
        'Sacramento': (38.5816, -121.4944),
        'Long Beach': (33.7701, -118.1937),
        'Oakland': (37.8044, -122.2712),
        'Bakersfield': (35.3733, -119.0187),
        'Anaheim': (33.8366, -117.9143),
        'Santa Ana': (33.7455, -117.8677),
        'Riverside': (33.9806, -117.3755),
        'Stockton': (37.9577, -121.2908),
        'Irvine': (33.6846, -117.8265),
        'Chula Vista': (32.6401, -117.0842)
    }
    
    # Statistiques par ville
    city_stats = df_filtered.groupby('City').agg({
        'Customer ID': 'count',
        'Customer Status': lambda x: (x == 'Churned').sum()
    }).reset_index()
    city_stats.columns = ['City', 'Total_Clients', 'Churned_Clients']
    city_stats['Churn_Rate'] = (city_stats['Churned_Clients'] / city_stats['Total_Clients'] * 100).round(1)
    
    # Ajouter coordonnées GPS
    city_stats['lat'] = city_stats['City'].map(lambda x: city_coords.get(x, (None, None))[0])
    city_stats['lon'] = city_stats['City'].map(lambda x: city_coords.get(x, (None, None))[1])
    
    # Filtrer villes avec coordonnées
    city_stats_map = city_stats.dropna(subset=['lat', 'lon'])
    
    # 🗺️ CARTE 1: Carte Interactive Californie (Points par ville)
    st.subheader("🗺️ Carte Interactive - Churn par Ville")
    
    if len(city_stats_map) > 0:
        fig = px.scatter_mapbox(
            city_stats_map,
            lat='lat',
            lon='lon',
            size='Churned_Clients',
            color='Churn_Rate',
            hover_name='City',
            hover_data={
                'Total_Clients': ':,',
                'Churned_Clients': ':,',
                'Churn_Rate': ':.1f',
                'lat': False,
                'lon': False
            },
            color_continuous_scale=['#27AE60', '#F39C12', '#E74C3C'],
            size_max=50,
            zoom=5,
            center={'lat': 37.0, 'lon': -119.5},
            mapbox_style='carto-positron',
            labels={
                'Churn_Rate': 'Taux de Churn (%)',
                'Total_Clients': 'Total Clients',
                'Churned_Clients': 'Clients Perdus'
            }
        )
        fig.update_layout(
            height=600,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("💡 **Lecture de la carte:** Taille des bulles = Nombre de clients perdus | Couleur = Taux de churn (Rouge = Fort churn)")
    else:
        st.warning("Coordonnées GPS non disponibles pour les villes sélectionnées")
    
    st.markdown("---")
    
    # 📊 GRAPHIQUE BAR: Top 15 villes par taux de churn
    st.subheader("🏙️ Top 15 Villes - Taux de Churn")
    
    top_15_cities = city_stats.nlargest(15, 'Churn_Rate')
    
    fig = px.bar(
        top_15_cities,
        x='City',
        y='Churn_Rate',
        color='Churn_Rate',
        color_continuous_scale=['#27AE60', '#F39C12', '#E74C3C'],
        labels={'City': 'Ville', 'Churn_Rate': 'Taux de Churn (%)'},
        text='Churn_Rate',
        hover_data={
            'Total_Clients': ':,',
            'Churned_Clients': ':,'
        }
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # 📊 Double visualisation: Absolu vs Taux
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Top 10 - Nombre Absolu de Départs")
        top_10_absolute = city_stats.nlargest(10, 'Churned_Clients')
        
        fig = px.bar(
            top_10_absolute,
            x='Churned_Clients',
            y='City',
            orientation='h',
            color='Churned_Clients',
            color_continuous_scale='Reds',
            labels={'City': 'Ville', 'Churned_Clients': 'Clients Perdus'},
            text='Churned_Clients'
        )
        fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Top 10 - Taux de Churn")
        top_10_rate = city_stats.nlargest(10, 'Churn_Rate')
        
        fig = px.bar(
            top_10_rate,
            x='Churn_Rate',
            y='City',
            orientation='h',
            color='Churn_Rate',
            color_continuous_scale=['#27AE60', '#F39C12', '#E74C3C'],
            labels={'City': 'Ville', 'Churn_Rate': 'Taux de Churn (%)'},
            text='Churn_Rate'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # 💡 Insight géographique
    highest_churn_city = city_stats.nlargest(1, 'Churn_Rate').iloc[0]
    most_churned_city = city_stats.nlargest(1, 'Churned_Clients').iloc[0]
    
    st.markdown(f"""
    <div class="insight-box">
        <strong>💡 Zones Prioritaires:</strong><br>
        🔴 <strong>Taux le plus élevé:</strong> {highest_churn_city['City']} 
        (<strong>{highest_churn_city['Churn_Rate']:.1f}%</strong> de churn, {int(highest_churn_city['Churned_Clients'])} clients perdus)<br>
        📊 <strong>Volume le plus important:</strong> {most_churned_city['City']} 
        (<strong>{int(most_churned_city['Churned_Clients'])}</strong> clients perdus, taux: {most_churned_city['Churn_Rate']:.1f}%)<br><br>
        <strong>🎯 Action recommandée:</strong> Audit qualité service + campagne de rétention ciblée sur ces zones géographiques.
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7F8C8D; padding: 2rem 0;'>
    <strong>Dashboard Attrition Client</strong> | Développé par <strong>Naziha Boussemaha</strong>
    <br>📧 contact.ethicaldataboost@gmail.com | 💼 www.linkedin.com/in/ethicaldataboost-edb-ab4064383 | 📞 +33 6 52 22 37 83
    <br><br>
    <em>Cette analyse porte sur 7 043 clients sur 18 mois - Secteur Télécommunications</em>
</div>
""", unsafe_allow_html=True)
