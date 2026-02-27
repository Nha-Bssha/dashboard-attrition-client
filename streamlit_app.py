"""
Dashboard Analyse Attrition Client - Entreprise Telco
Reproduction exacte du dashboard Power BI
Date: 17/02/2024
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# ============================================================================
# CONFIGURATION PAGE
# ============================================================================

st.set_page_config(
    page_title="Dashboard Telco - 17/02/2024",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CUSTOM CSS - STYLE POWER BI
# ============================================================================

st.markdown("""
<style>
    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        padding: 20px;
        border-radius: 0px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    .main-title {
        color: white;
        font-size: 28px;
        font-weight: 700;
        margin: 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .sub-title {
        color: #ecf0f1;
        font-size: 20px;
        font-weight: 400;
        margin: 5px 0 0 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Navigation tabs style Power BI */
    .nav-container {
        display: flex;
        gap: 10px;
        margin: 20px 0;
        justify-content: center;
    }
    
    .nav-tab {
        background: #bdc3c7;
        color: #2c3e50;
        padding: 15px 25px;
        clip-path: polygon(10% 0%, 100% 0%, 90% 100%, 0% 100%);
        font-weight: 600;
        font-size: 14px;
        text-align: center;
        min-width: 150px;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .nav-tab.active {
        background: #e74c3c;
        color: white;
        transform: scale(1.05);
    }
    
    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        margin: 10px 0;
    }
    
    .kpi-card.yellow {
        background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
    }
    
    .kpi-card.blue {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
    }
    
    .kpi-card.red {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
    }
    
    .kpi-card.dark {
        background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
    }
    
    .kpi-card.black {
        background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%);
    }
    
    .kpi-value {
        font-size: 48px;
        font-weight: 700;
        color: white;
        margin: 0;
        line-height: 1;
    }
    
    .kpi-label {
        font-size: 14px;
        color: rgba(255,255,255,0.9);
        margin-top: 8px;
        font-weight: 500;
    }
    
    /* Filtres */
    .filter-container {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Plotly charts */
    .js-plotly-plot {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CHARGEMENT DONNÉES
# ============================================================================

@st.cache_data
def load_data():
    """Charger et préparer les données"""
    df = pd.read_csv('telco_churn_master.csv')
    
    # Créer colonnes calculées si nécessaire
    if 'Tranche_Age' not in df.columns:
        df['Tranche_Age'] = pd.cut(df['Age'], 
                                    bins=[0, 25, 32, 39, 46, 53, 60, 67, 74, 100],
                                    labels=['18-25', '25-32', '32-39', '39-46', '46-53', 
                                           '53-60', '60-67', '67-74', '74-81'])
    
    return df

# Charger les données
df = load_data()

# ============================================================================
# HEADER PRINCIPAL
# ============================================================================

st.markdown("""
<div class="main-header">
    <h1 class="main-title">Dashboard - Entreprise Telco - 17/02/2024</h1>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# FILTRES GLOBAUX (Top Right)
# ============================================================================

st.markdown('<div class="filter-container">', unsafe_allow_html=True)

filter_cols = st.columns(5)

with filter_cols[0]:
    tranche_age_filter = st.multiselect(
        "Tranche_Age",
        options=['Tout'] + sorted(df['Tranche_Age'].dropna().unique().tolist()),
        default=['Tout']
    )

with filter_cols[1]:
    contract_filter = st.multiselect(
        "Contract",
        options=['Tout'] + sorted(df['Contract'].dropna().unique().tolist()),
        default=['Tout']
    )

with filter_cols[2]:
    city_filter = st.multiselect(
        "City",
        options=['Tout'] + sorted(df['City'].dropna().unique().tolist()),
        default=['Tout']
    )

with filter_cols[3]:
    offer_filter = st.multiselect(
        "Offer",
        options=['Tout'] + sorted(df['Offer'].dropna().unique().tolist()),
        default=['Tout']
    )

with filter_cols[4]:
    gender_filter = st.multiselect(
        "Gender",
        options=['Tout'] + sorted(df['Gender'].dropna().unique().tolist()),
        default=['Tout']
    )

st.markdown('</div>', unsafe_allow_html=True)

# Appliquer les filtres
df_filtered = df.copy()

if 'Tout' not in tranche_age_filter and len(tranche_age_filter) > 0:
    df_filtered = df_filtered[df_filtered['Tranche_Age'].isin(tranche_age_filter)]

if 'Tout' not in contract_filter and len(contract_filter) > 0:
    df_filtered = df_filtered[df_filtered['Contract'].isin(contract_filter)]

if 'Tout' not in city_filter and len(city_filter) > 0:
    df_filtered = df_filtered[df_filtered['City'].isin(city_filter)]

if 'Tout' not in offer_filter and len(offer_filter) > 0:
    df_filtered = df_filtered[df_filtered['Offer'].isin(offer_filter)]

if 'Tout' not in gender_filter and len(gender_filter) > 0:
    df_filtered = df_filtered[df_filtered['Gender'].isin(gender_filter)]

# ============================================================================
# NAVIGATION TABS
# ============================================================================

# Créer les tabs Streamlit (invisible, juste pour la logique)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1️⃣ Taux d'attrition",
    "2️⃣ Comportement du churn", 
    "3️⃣ Satisfaction client",
    "4️⃣ Coût du churn",
    "5️⃣ Focus San Diego"
])

# ============================================================================
# ONGLET 1 : TAUX D'ATTRITION
# ============================================================================

with tab1:
    st.markdown('<h2 class="sub-title">Chiffres clés de notre attrition</h2>', unsafe_allow_html=True)
    
    # Calculer les KPIs
    total_clients = len(df_filtered)
    total_churned = len(df_filtered[df_filtered['Customer Status'] == 'Churned'])
    total_joined = len(df_filtered[df_filtered['Customer Status'] == 'Joined'])
    total_stayed = len(df_filtered[df_filtered['Customer Status'] == 'Stayed'])
    total_installed = total_stayed + total_churned
    solde_net = total_stayed + total_joined
    
    # Afficher les 5 KPIs
    kpi_cols = st.columns(5)
    
    with kpi_cols[0]:
        st.markdown(f"""
        <div class="kpi-card yellow">
            <div class="kpi-value">{total_installed:,}</div>
            <div class="kpi-label">Total clients installés</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[1]:
        st.markdown(f"""
        <div class="kpi-card blue">
            <div class="kpi-value">{total_joined:,}</div>
            <div class="kpi-label">Total New Customers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[2]:
        st.markdown(f"""
        <div class="kpi-card red">
            <div class="kpi-value">{total_churned:,}</div>
            <div class="kpi-label">Nombre de Churned</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[3]:
        st.markdown(f"""
        <div class="kpi-card dark">
            <div class="kpi-value">{total_clients:,}</div>
            <div class="kpi-label">Total clients</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[4]:
        st.markdown(f"""
        <div class="kpi-card black">
            <div class="kpi-value">{solde_net:,}</div>
            <div class="kpi-label">Solde net des clients actifs</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # SECTION RÉPARTITION DES CHURNS
    st.markdown("### Répartition des churns")
    
    row1_cols = st.columns([2, 1, 1, 2])
    
    with row1_cols[0]:
        # BUBBLE CHART - Répartition par tranche d'âge
        st.markdown("#### Répartition par tranche d'âge")
        
        age_stats = df_filtered.groupby('Tranche_Age').agg({
            'Customer ID': 'count'
        }).reset_index()
        age_stats.columns = ['Tranche_Age', 'Count']
        
        # Créer bubble chart
        fig = px.scatter(
            age_stats,
            x=[1, 2, 3, 1, 2, 3, 1, 2, 3][:len(age_stats)],
            y=[1, 1, 1, 2, 2, 2, 3, 3, 3][:len(age_stats)],
            size='Count',
            color='Tranche_Age',
            hover_data={'Tranche_Age': True, 'Count': True},
            size_max=100,
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig.update_layout(
            showlegend=False,
            xaxis={'visible': False},
            yaxis={'visible': False},
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with row1_cols[1]:
        # DONUT - Churned/Joined/Stayed
        status_stats = df_filtered['Customer Status'].value_counts()
        
        fig = go.Figure(data=[go.Pie(
            labels=status_stats.index,
            values=status_stats.values,
            hole=0.6,
            marker=dict(colors=['#e74c3c', '#3498db', '#f39c12']),
            textposition='inside',
            textinfo='label+percent'
        )])
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with row1_cols[2]:
        # DONUT - Male/Female
        gender_stats = df_filtered['Gender'].value_counts()
        
        fig = go.Figure(data=[go.Pie(
            labels=gender_stats.index,
            values=gender_stats.values,
            hole=0.6,
            marker=dict(colors=['#34495e', '#e91e63']),
            textposition='inside',
            textinfo='label+percent'
        )])
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with row1_cols[3]:
        # CARTE GÉOGRAPHIQUE CALIFORNIE
        st.markdown("#### Carte Californie")
        
        city_geo = df_filtered.groupby(['City', 'Latitude', 'Longitude']).agg({
            'Customer ID': 'count',
            'Customer Status': lambda x: (x == 'Churned').sum()
        }).reset_index()
        city_geo.columns = ['City', 'Latitude', 'Longitude', 'Total', 'Churned']
        city_geo['Churn_Rate'] = (city_geo['Churned'] / city_geo['Total'] * 100).round(1)
        city_geo_clean = city_geo.dropna(subset=['Latitude', 'Longitude'])
        
        if len(city_geo_clean) > 0:
            fig = px.scatter_mapbox(
                city_geo_clean,
                lat='Latitude',
                lon='Longitude',
                size='Total',
                color='Churn_Rate',
                hover_name='City',
                color_continuous_scale=['#27AE60', '#F39C12', '#E74C3C'],
                size_max=30,
                zoom=5.5,
                mapbox_style='carto-darkmatter'
            )
            fig.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=0, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # SECTION TAUX D'ATTRITION PAR CONTRAT ET OFFRE
    row2_cols = st.columns(2)
    
    with row2_cols[0]:
        st.markdown("#### Taux d'attrition par contrat")
        
        contract_stats = df_filtered.groupby('Contract').agg({
            'Customer ID': 'count',
            'Customer Status': lambda x: (x == 'Churned').sum()
        }).reset_index()
        contract_stats.columns = ['Contract', 'Total', 'Churned']
        contract_stats['Churn_Rate'] = (contract_stats['Churned'] / contract_stats['Total'] * 100).round(0)
        contract_stats = contract_stats.sort_values('Churn_Rate', ascending=False)
        
        # Couleurs selon taux
        colors = ['#e74c3c' if x > 30 else '#3498db' if x < 10 else '#f39c12' 
                  for x in contract_stats['Churn_Rate']]
        
        fig = go.Figure(go.Bar(
            y=contract_stats['Contract'],
            x=contract_stats['Churn_Rate'],
            orientation='h',
            marker=dict(color=colors),
            text=contract_stats['Churn_Rate'].apply(lambda x: f"{x:.0f} %"),
            textposition='inside',
            textfont=dict(color='white', size=14, family='Arial Black')
        ))
        fig.update_layout(
            height=250,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis={'title': '', 'showgrid': False},
            yaxis={'title': ''},
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with row2_cols[1]:
        st.markdown("#### Taux d'attrition par offre")
        
        offer_stats = df_filtered.groupby('Offer').agg({
            'Customer ID': 'count',
            'Customer Status': lambda x: (x == 'Churned').sum()
        }).reset_index()
        offer_stats.columns = ['Offer', 'Total', 'Churned']
        offer_stats['Churn_Rate'] = (offer_stats['Churned'] / offer_stats['Total'] * 100).round(0)
        offer_stats = offer_stats.sort_values('Churn_Rate', ascending=False)
        
        # Couleurs selon taux
        colors = ['#e74c3c' if x > 40 else '#3498db' if x < 15 else '#f39c12' 
                  for x in offer_stats['Churn_Rate']]
        
        fig = go.Figure(go.Bar(
            y=offer_stats['Offer'],
            x=offer_stats['Churn_Rate'],
            orientation='h',
            marker=dict(color=colors),
            text=offer_stats['Churn_Rate'].apply(lambda x: f"{x:.0f} %"),
            textposition='inside',
            textfont=dict(color='white', size=14, family='Arial Black')
        ))
        fig.update_layout(
            height=250,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis={'title': '', 'showgrid': False},
            yaxis={'title': ''},
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # TAUX DE CHURN PAR DURÉE D'ENGAGEMENT
    st.markdown("#### Taux de churn par durée d'engagement")
    
    tenure_stats = df_filtered.groupby('Tenure in Months').agg({
        'Customer ID': 'count',
        'Customer Status': lambda x: (x == 'Churned').sum()
    }).reset_index()
    tenure_stats.columns = ['Tenure', 'Total', 'Churned']
    tenure_stats['Churn_Rate'] = (tenure_stats['Churned'] / tenure_stats['Total'] * 100).round(1)
    tenure_stats = tenure_stats.sort_values('Tenure')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=tenure_stats['Tenure'],
        y=tenure_stats['Churn_Rate'],
        mode='lines+markers',
        line=dict(color='#e74c3c', width=3),
        marker=dict(size=6, color='#c0392b'),
        fill='tozeroy',
        fillcolor='rgba(231, 76, 60, 0.3)',
        text=tenure_stats['Churn_Rate'].apply(lambda x: f"{x:.1f}%"),
        textposition='top center',
        textfont=dict(color='white', size=10)
    ))
    fig.update_layout(
        height=300,
        xaxis={'title': 'Tenure (in Months)', 'showgrid': True, 'gridcolor': 'rgba(255,255,255,0.1)'},
        yaxis={'title': 'Taux de Churn (%)', 'showgrid': True, 'gridcolor': 'rgba(255,255,255,0.1)'},
        plot_bgcolor='rgba(52, 73, 94, 0.8)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=50, r=20, t=20, b=50)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # TAUX DE CHURN PAR TRANCHE D'ÂGE (Combo chart)
    st.markdown("#### Taux de churn par tranche d'âge")
    
    age_churn = df_filtered.groupby('Tranche_Age').agg({
        'Customer ID': 'count',
        'Customer Status': lambda x: (x == 'Churned').sum(),
        'Monthly Charge': 'mean'
    }).reset_index()
    age_churn.columns = ['Tranche_Age', 'Total', 'Churned', 'Avg_Monthly_Charge']
    age_churn['Churn_Rate'] = (age_churn['Churned'] / age_churn['Total'] * 100).round(1)
    age_churn = age_churn.dropna()
    
    # Créer figure avec axe secondaire
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Barres - Taux de churn
    colors_bars = ['#3498db' if x < 25 else '#e74c3c' if x > 35 else '#f39c12' 
                   for x in age_churn['Churn_Rate']]
    
    fig.add_trace(
        go.Bar(
            x=age_churn['Tranche_Age'],
            y=age_churn['Churn_Rate'],
            name='Taux de churn',
            marker=dict(color=colors_bars),
            text=age_churn['Churn_Rate'].apply(lambda x: f"{x:.0f}%"),
            textposition='outside',
            textfont=dict(color='white', size=11)
        ),
        secondary_y=False
    )
    
    # Ligne - Moyenne Monthly Charge
    fig.add_trace(
        go.Scatter(
            x=age_churn['Tranche_Age'],
            y=age_churn['Avg_Monthly_Charge'],
            name='Moyenne de Monthly Charge',
            mode='lines+markers',
            line=dict(color='#f39c12', width=3, dash='dot'),
            marker=dict(size=8, color='#f39c12'),
            yaxis='y2'
        ),
        secondary_y=True
    )
    
    fig.update_xaxes(title_text="", showgrid=False)
    fig.update_yaxes(title_text="Taux de churn (%)", secondary_y=False, showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    fig.update_yaxes(title_text="Monthly Charge (€)", secondary_y=True, showgrid=False)
    
    fig.update_layout(
        height=400,
        plot_bgcolor='rgba(52, 73, 94, 0.8)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# ONGLETS 2-5 : PLACEHOLDER (À COMPLÉTER)
# ============================================================================

with tab2:
    st.markdown('<h2 class="sub-title">Comportement du churn</h2>', unsafe_allow_html=True)
    st.info("🚧 Onglet en cours de construction...")

with tab3:
    st.markdown('<h2 class="sub-title">Taux de satisfaction client</h2>', unsafe_allow_html=True)
    st.info("🚧 Onglet en cours de construction...")

with tab4:
    st.markdown('<h2 class="sub-title">Coût du Churn</h2>', unsafe_allow_html=True)
    st.info("🚧 Onglet en cours de construction...")

with tab5:
    st.markdown('<h2 class="sub-title">Focus sur San Diego</h2>', unsafe_allow_html=True)
    st.info("🚧 Onglet en cours de construction...")
