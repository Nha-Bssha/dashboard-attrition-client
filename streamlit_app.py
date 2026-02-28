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
    "📈 Vue d'ensemble", 
    "🔄 Comportement du Churn", 
    "😊 Satisfaction",
    "💰 Coût du Churn",
    "🔥 Focus Ville Critique"
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
        # BUBBLE CHART - Répartition des churns par tranche d'âge
        st.markdown("#### 📊 Répartition des churns par tranche d'âge")
        
        # FOCUS SUR CHURNED UNIQUEMENT
        age_churned = df_filtered[df_filtered['Customer Status'] == 'Churned'].groupby('Tranche_Age').size().reset_index(name='Count')
        age_churned = age_churned.dropna().sort_values('Tranche_Age')
        
        if len(age_churned) > 0:
            # Emphasis sur seniors (67-74 et 74-81)
            age_churned['Is_Senior'] = age_churned['Tranche_Age'].isin(['67-74', '74-81'])
            
            # Calculer tailles de bulles (minimum 20, maximum basé sur les données)
            max_count = age_churned['Count'].max()
            age_churned['BubbleSize'] = age_churned['Count'].apply(
                lambda x: max(30, (x / max_count) * 100)  # Taille min 30, max 100
            )
            
            fig = go.Figure()
            
            # VRAIES BULLES VISIBLES avec axes
            fig.add_trace(go.Scatter(
                x=age_churned['Tranche_Age'].astype(str),
                y=age_churned['Count'],
                mode='markers+text',
                marker=dict(
                    size=age_churned['BubbleSize'],  # Tailles garanties visibles
                    color=['#ff6b6b' if s else '#4ecdc4' for s in age_churned['Is_Senior']],
                    line=dict(width=3, color='white'),
                    opacity=0.85
                ),
                text=age_churned['Count'].astype(str),
                textposition='middle center',
                textfont=dict(size=18, color='white', family='Arial Black'),
                hovertemplate='<b>%{x}</b><br>Churned: %{y}<extra></extra>'
            ))
            
            fig.update_layout(
                height=350,
                showlegend=False,
                plot_bgcolor='rgba(52, 73, 94, 0.8)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis={'title': 'Tranche d\'âge', 'showgrid': False, 'color': 'white', 'tickangle': -45},
                yaxis={'title': 'Clients churned', 'showgrid': True, 'gridcolor': 'rgba(255,255,255,0.1)', 'color': 'white'},
                font=dict(color='white'),
                margin=dict(l=50, r=20, t=30, b=80)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucun client churned avec les filtres actuels")
    
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
    
    # Calculer le taux de vente incitative (nombre de produits > base)
    product_cols = ['Phone Service', 'Multiple Lines', 'Internet Service', 'Online Security', 
                    'Online Backup', 'Device Protection Plan', 'Premium Tech Support', 
                    'Streaming TV', 'Streaming Movies', 'Streaming Music', 'Unlimited Data']
    
    # Créer colonne Nb_Produits (nombre de services souscrits)
    df_filtered['Nb_Produits'] = 0
    for col in product_cols:
        if col in df_filtered.columns:
            df_filtered['Nb_Produits'] += (df_filtered[col] == 'Yes').astype(int)
    
    # Taux de vente incitative = clients avec 3+ produits
    df_filtered['Upsell'] = (df_filtered['Nb_Produits'] >= 3).astype(int)
    
    # ROW 1 - Taux de vente incitative par Statut + par Offer + par Contract
    row1_cols = st.columns([1, 2, 2])
    
    with row1_cols[0]:
        st.markdown("#### Taux de vente incitative par Statut")
        
        status_upsell = df_filtered.groupby('Customer Status').agg({
            'Upsell': 'mean'
        }).reset_index()
        status_upsell['Upsell_Pct'] = (status_upsell['Upsell'] * 100).round(0)
        
        colors = {'Churned': '#e74c3c', 'Stayed': '#27AE60', 'Joined': '#3498db'}
        status_colors = [colors.get(x, '#95a5a6') for x in status_upsell['Customer Status']]
        
        fig = go.Figure(go.Bar(
            y=status_upsell['Customer Status'],
            x=status_upsell['Upsell_Pct'],
            orientation='h',
            marker=dict(color=status_colors),
            text=status_upsell['Upsell_Pct'].apply(lambda x: f"{x:.0f} %"),
            textposition='inside',
            textfont=dict(color='white', size=14, family='Arial Black')
        ))
        fig.update_layout(
            height=250,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis={'showgrid': False},
            plot_bgcolor='rgba(52, 73, 94, 0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with row1_cols[1]:
        st.markdown("#### Taux de vente incitative, taux de churn et Nombre de Churned par Offer")
        
        offer_stats = df_filtered.groupby('Offer').agg({
            'Upsell': 'mean',
            'Customer ID': 'count',
            'Customer Status': lambda x: (x == 'Churned').sum()
        }).reset_index()
        offer_stats.columns = ['Offer', 'Upsell_Rate', 'Total', 'Churned']
        offer_stats['Churn_Rate'] = (offer_stats['Churned'] / offer_stats['Total'] * 100).round(1)
        offer_stats['Upsell_Pct'] = (offer_stats['Upsell_Rate'] * 100).round(1)
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(go.Bar(
            x=offer_stats['Offer'],
            y=offer_stats['Upsell_Pct'],
            name='Taux vente incitative',
            marker=dict(color='#3498db'),
            text=offer_stats['Upsell_Pct'].apply(lambda x: f"{x:.0f}%"),
            textposition='outside'
        ), secondary_y=False)
        
        fig.add_trace(go.Bar(
            x=offer_stats['Offer'],
            y=offer_stats['Churn_Rate'],
            name='Taux de churn',
            marker=dict(color='#e74c3c'),
            text=offer_stats['Churn_Rate'].apply(lambda x: f"{x:.0f}%"),
            textposition='outside'
        ), secondary_y=False)
        
        fig.add_trace(go.Scatter(
            x=offer_stats['Offer'],
            y=offer_stats['Churned'],
            name='Nombre de Churned',
            mode='markers',
            marker=dict(size=10, color='#f39c12')
        ), secondary_y=True)
        
        fig.update_layout(
            height=300,
            barmode='group',
            plot_bgcolor='rgba(52, 73, 94, 0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=True,
            legend=dict(orientation="h", y=1.1)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with row1_cols[2]:
        st.markdown("#### Taux de vente incitative, taux de churn et Nombre de Churned par Contract")
        
        contract_stats = df_filtered.groupby('Contract').agg({
            'Upsell': 'mean',
            'Customer ID': 'count',
            'Customer Status': lambda x: (x == 'Churned').sum()
        }).reset_index()
        contract_stats.columns = ['Contract', 'Upsell_Rate', 'Total', 'Churned']
        contract_stats['Churn_Rate'] = (contract_stats['Churned'] / contract_stats['Total'] * 100).round(1)
        contract_stats['Upsell_Pct'] = (contract_stats['Upsell_Rate'] * 100).round(1)
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(go.Bar(
            x=contract_stats['Contract'],
            y=contract_stats['Upsell_Pct'],
            name='Taux vente incitative',
            marker=dict(color='#3498db'),
            text=contract_stats['Upsell_Pct'].apply(lambda x: f"{x:.0f}%"),
            textposition='outside'
        ), secondary_y=False)
        
        fig.add_trace(go.Bar(
            x=contract_stats['Contract'],
            y=contract_stats['Churn_Rate'],
            name='Taux de churn',
            marker=dict(color='#e74c3c'),
            text=contract_stats['Churn_Rate'].apply(lambda x: f"{x:.0f}%"),
            textposition='outside'
        ), secondary_y=False)
        
        fig.add_trace(go.Scatter(
            x=contract_stats['Contract'],
            y=contract_stats['Churned'],
            name='Nombre de Churned',
            mode='markers',
            marker=dict(size=10, color='#f39c12')
        ), secondary_y=True)
        
        fig.update_layout(
            height=300,
            barmode='group',
            plot_bgcolor='rgba(52, 73, 94, 0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=True,
            legend=dict(orientation="h", y=1.1)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # ROW 2 - Area charts et scatter
    row2_cols = st.columns([1, 1, 1])
    
    with row2_cols[0]:
        st.markdown("#### Moyenne du CA vs Taux de vente incitative")
        
        ca_upsell = df_filtered.groupby('Customer Status').agg({
            'Total Revenue': 'mean',
            'Upsell': 'mean'
        }).reset_index()
        ca_upsell['CA_Moyen'] = ca_upsell['Total Revenue'] / 1000
        ca_upsell['Upsell_Pct'] = (ca_upsell['Upsell'] * 100).round(1)
        
        fig = go.Figure()
        
        status_order = ['Stayed', 'Churned', 'Joined']
        colors_status = {'Stayed': '#27AE60', 'Churned': '#e74c3c', 'Joined': '#3498db'}
        
        for status in status_order:
            data = ca_upsell[ca_upsell['Customer Status'] == status]
            if len(data) > 0:
                fig.add_trace(go.Scatter(
                    x=[status],
                    y=data['CA_Moyen'].values,
                    fill='tonexty' if status != 'Stayed' else 'tozeroy',
                    fillcolor=colors_status[status],
                    line=dict(color=colors_status[status], width=2),
                    name=status,
                    mode='lines+markers'
                ))
        
        fig.update_layout(
            height=300,
            plot_bgcolor='rgba(52, 73, 94, 0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis_title="CA Moyen (K€)",
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with row2_cols[1]:
        st.markdown("#### Panier moyen vs taux de vente incitative")
        
        scatter_data = df_filtered.groupby(['Customer Status', 'Offer']).agg({
            'Monthly Charge': 'mean',
            'Upsell': 'mean'
        }).reset_index()
        scatter_data['Upsell_Pct'] = (scatter_data['Upsell'] * 100).round(1)
        
        fig = px.scatter(
            scatter_data,
            x='Upsell_Pct',
            y='Monthly Charge',
            color='Customer Status',
            size='Monthly Charge',
            color_discrete_map={'Churned': '#e74c3c', 'Joined': '#3498db', 'Stayed': '#f39c12'},
            hover_data=['Offer']
        )
        fig.update_layout(
            height=300,
            plot_bgcolor='rgba(52, 73, 94, 0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Taux de vente incitative (%)",
            yaxis_title="Moyenne Panier (€)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with row2_cols[2]:
        st.markdown("#### CLV par catégorie vs taux de vente incitative")
        
        # Créer catégories CLV
        df_filtered['CLV_Cat'] = pd.cut(
            df_filtered['CLTV'],
            bins=[0, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 7000],
            labels=['2001-2500', '2501-3000', '3001-3500', '3501-4000', '4001-4500', 
                   '4501-5000', '5001-5500', '5501-6000', '6001-6500']
        )
        
        clv_upsell = df_filtered.groupby(['Customer Status', 'CLV_Cat']).agg({
            'Upsell': 'mean',
            'Customer ID': 'count'
        }).reset_index()
        clv_upsell['Upsell_Pct'] = (clv_upsell['Upsell'] * 100).round(1)
        
        fig = go.Figure()
        
        for status in ['Stayed', 'Churned', 'Joined']:
            data = clv_upsell[clv_upsell['Customer Status'] == status].sort_values('CLV_Cat')
            fig.add_trace(go.Scatter(
                x=data['CLV_Cat'],
                y=data['Upsell_Pct'],
                fill='tonexty',
                name=status,
                line=dict(color=colors_status.get(status, '#95a5a6'))
            ))
        
        fig.update_layout(
            height=300,
            plot_bgcolor='rgba(52, 73, 94, 0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis_title="Taux vente incitative (%)",
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # ROW 3 - Charts finaux
    row3_cols = st.columns([1, 1, 1])
    
    with row3_cols[0]:
        st.markdown("#### Évolution du taux de vente incitative par durée d'engagement")
        
        # Créer bins tenure
        df_filtered['Tenure_Years'] = pd.cut(
            df_filtered['Tenure in Months'],
            bins=[0, 12, 24, 36, 48, 60, 72],
            labels=['1 an', '2 ans', '3 ans', '4 ans', '5 ans', '6 ans']
        )
        
        tenure_upsell = df_filtered.groupby(['Tenure_Years', 'Customer Status']).agg({
            'Upsell': 'mean'
        }).reset_index()
        tenure_upsell['Upsell_Pct'] = (tenure_upsell['Upsell'] * 100).round(1)
        
        fig = px.area(
            tenure_upsell,
            x='Tenure_Years',
            y='Upsell_Pct',
            color='Customer Status',
            color_discrete_map=colors_status,
            groupnorm='percent'
        )
        fig.update_layout(
            height=300,
            plot_bgcolor='rgba(52, 73, 94, 0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis_title="Taux vente incitative (%)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with row3_cols[1]:
        st.markdown("#### Taux de participation par catégorie de CLV")
        
        clv_participation = df_filtered.groupby('CLV_Cat').agg({
            'Customer ID': 'count',
            'Upsell': 'sum'
        }).reset_index()
        clv_participation.columns = ['CLV_Cat', 'Total', 'Upsells']
        clv_participation['Participation'] = (clv_participation['Upsells'] / clv_participation['Total'] * 100).round(0)
        clv_participation = clv_participation.dropna()
        
        fig = go.Figure(go.Bar(
            x=clv_participation['CLV_Cat'],
            y=clv_participation['Participation'],
            marker=dict(color='#3498db'),
            text=clv_participation['Participation'].apply(lambda x: f"{x:.0f}%"),
            textposition='outside'
        ))
        fig.update_layout(
            height=300,
            plot_bgcolor='rgba(52, 73, 94, 0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis_title="Taux participation (%)",
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with row3_cols[2]:
        st.markdown("#### Taux de churn vs taux de vente incitative")
        
        age_behavior = df_filtered.groupby('Tranche_Age').agg({
            'Upsell': 'mean',
            'Customer ID': 'count',
            'Customer Status': lambda x: (x == 'Churned').sum()
        }).reset_index()
        age_behavior.columns = ['Tranche_Age', 'Upsell_Rate', 'Total', 'Churned']
        age_behavior['Upsell_Pct'] = (age_behavior['Upsell_Rate'] * 100).round(1)
        age_behavior['Churn_Rate'] = (age_behavior['Churned'] / age_behavior['Total'] * 100).round(1)
        age_behavior = age_behavior.dropna()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=age_behavior['Tranche_Age'],
            y=age_behavior['Upsell_Pct'],
            fill='tozeroy',
            fillcolor='rgba(52, 152, 219, 0.6)',
            line=dict(color='#3498db', width=3),
            name='Taux de vente incitative'
        ))
        
        fig.add_trace(go.Scatter(
            x=age_behavior['Tranche_Age'],
            y=age_behavior['Churn_Rate'],
            fill='tozeroy',
            fillcolor='rgba(231, 76, 60, 0.6)',
            line=dict(color='#e74c3c', width=3),
            name='Taux de churn'
        ))
        
        fig.update_layout(
            height=300,
            plot_bgcolor='rgba(52, 73, 94, 0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis_title="Taux (%)",
            showlegend=True,
            legend=dict(orientation="h", y=1.1)
        )
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown('<h2 class="sub-title">Taux de satisfaction client</h2>', unsafe_allow_html=True)
    
    # Vérifier qu'il y a des données après filtrage
    if len(df_filtered) == 0:
        st.warning("⚠️ Aucune donnée disponible avec les filtres sélectionnés. Veuillez ajuster vos filtres.")
    else:
        # Calculer NPS avec gestion division par zéro
        promoters = len(df_filtered[df_filtered['Satisfaction Score'] >= 4])
        detractors = len(df_filtered[df_filtered['Satisfaction Score'] <= 2])
        total_respondents = len(df_filtered)
        
        # Protection division par zéro
        if total_respondents > 0:
            nps_score = round((promoters - detractors) / total_respondents * 100, 2)
        else:
            nps_score = 0.0
    
    # ROW 1 - NPS Gauge + Satisfaction bars
    row1_cols = st.columns([1, 1, 1])
    
    with row1_cols[0]:
        st.markdown("#### Net Promoter Score")
        
        # Gauge Chart NPS
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=nps_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "NPS", 'font': {'size': 24, 'color': 'white'}},
            number={'font': {'size': 60, 'color': 'white'}},
            gauge={
                'axis': {'range': [-100, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "#e74c3c" if nps_score < 0 else "#f39c12" if nps_score < 30 else "#27AE60"},
                'bgcolor': "rgba(0,0,0,0.3)",
                'borderwidth': 2,
                'bordercolor': "white",
                'steps': [
                    {'range': [-100, 0], 'color': 'rgba(231, 76, 60, 0.3)'},
                    {'range': [0, 50], 'color': 'rgba(243, 156, 18, 0.3)'},
                    {'range': [50, 100], 'color': 'rgba(39, 174, 96, 0.3)'}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': nps_score
                }
            }
        ))
        fig.update_layout(
            height=350,
            paper_bgcolor='rgba(52, 73, 94, 0.8)',
            font={'color': "white", 'family': "Arial"}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with row1_cols[1]:
        st.markdown("#### Taux de satisfaction par type de client")
        
        # Calculer score moyen par statut
        sat_by_status = df_filtered.groupby('Customer Status').agg({
            'Satisfaction Score': 'mean'
        }).reset_index()
        sat_by_status['Sat_Score'] = ((sat_by_status['Satisfaction Score'] - 3) * 50).round(0)
        
        colors_sat = {'Churned': '#e74c3c', 'Stayed': '#27AE60', 'Joined': '#3498db'}
        bar_colors = [colors_sat.get(x, '#95a5a6') for x in sat_by_status['Customer Status']]
        
        fig = go.Figure(go.Bar(
            y=sat_by_status['Customer Status'],
            x=sat_by_status['Sat_Score'],
            orientation='h',
            marker=dict(color=bar_colors),
            text=sat_by_status['Sat_Score'].apply(lambda x: f"{x:.0f}"),
            textposition='inside',
            textfont=dict(color='white', size=16)
        ))
        fig.update_layout(
            height=350,
            plot_bgcolor='rgba(52, 73, 94, 0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis={'title': 'Score', 'showgrid': False},
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with row1_cols[2]:
        st.markdown("#### Taux de satisfaction par contrat")
        
        sat_by_contract = df_filtered.groupby('Contract').agg({
            'Satisfaction Score': 'mean'
        }).reset_index()
        sat_by_contract['Sat_Score'] = ((sat_by_contract['Satisfaction Score'] - 3) * 50).round(1)
        
        contract_colors = ['#e74c3c' if x < 0 else '#f39c12' if x < 30 else '#27AE60' 
                          for x in sat_by_contract['Sat_Score']]
        
        fig = go.Figure(go.Bar(
            y=sat_by_contract['Contract'],
            x=sat_by_contract['Sat_Score'],
            orientation='h',
            marker=dict(color=contract_colors),
            text=sat_by_contract['Sat_Score'].apply(lambda x: f"{x:.1f}"),
            textposition='inside',
            textfont=dict(color='white', size=16)
        ))
        fig.update_layout(
            height=350,
            plot_bgcolor='rgba(52, 73, 94, 0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis={'title': 'Score', 'showgrid': False},
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # ROW 2 - Classement offres + Donut recommandation
    row2_cols = st.columns([2, 1])
    
    with row2_cols[0]:
        st.markdown("#### Classement des offres par taux de satisfaction")
        
        sat_by_offer = df_filtered.groupby('Offer').agg({
            'Satisfaction Score': 'mean'
        }).reset_index()
        sat_by_offer['Sat_Score'] = ((sat_by_offer['Satisfaction Score'] - 3) * 50).round(2)
        sat_by_offer = sat_by_offer.sort_values('Sat_Score', ascending=False)
        
        offer_colors = ['#e74c3c' if x < 0 else '#f39c12' if x < 30 else '#27AE60' 
                       for x in sat_by_offer['Sat_Score']]
        
        fig = go.Figure(go.Bar(
            y=sat_by_offer['Offer'],
            x=sat_by_offer['Sat_Score'],
            orientation='h',
            marker=dict(color=offer_colors),
            text=sat_by_offer['Sat_Score'].apply(lambda x: f"{x:.2f}"),
            textposition='inside',
            textfont=dict(color='white', size=14)
        ))
        fig.update_layout(
            height=400,
            plot_bgcolor='rgba(52, 73, 94, 0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis={'title': 'Score Satisfaction', 'showgrid': False},
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with row2_cols[1]:
        st.markdown("#### Taux de recommandation global")
        
        # Promoteurs = score >= 4
        recommend_yes = len(df_filtered[df_filtered['Satisfaction Score'] >= 4])
        recommend_no = total_respondents - recommend_yes
        
        fig = go.Figure(data=[go.Pie(
            labels=['Yes', 'No'],
            values=[recommend_yes, recommend_no],
            hole=0.6,
            marker=dict(colors=['#27AE60', '#e74c3c']),
            textposition='inside',
            textinfo='label+percent',
            textfont=dict(size=18, color='white')
        )])
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # ROW 3 - Scatter + NPS vs churn
    row3_cols = st.columns(2)
    
    with row3_cols[0]:
        st.markdown("#### Corrélation entre l'âge et le score de satisfaction")
        
        scatter_sample = df_filtered.sample(min(500, len(df_filtered)))
        
        fig = px.scatter(
            scatter_sample,
            x='Age',
            y='Satisfaction Score',
            opacity=0.4,
            color_discrete_sequence=['#3498db']  # UNE SEULE COULEUR
        )
        fig.update_traces(marker=dict(size=8))
        fig.update_layout(
            height=350,
            plot_bgcolor='rgba(52, 73, 94, 0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis={'title': 'Age', 'showgrid': True, 'gridcolor': 'rgba(255,255,255,0.1)'},
            yaxis={'title': 'Score de satisfaction', 'showgrid': True, 'gridcolor': 'rgba(255,255,255,0.1)'},
            showlegend=False  # PAS DE LÉGENDE
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with row3_cols[1]:
        st.markdown("#### NPS vs taux de churn - Top 5 villes critiques")
        
        # TOP 5 villes PAR TAUX DE CHURN (pas par volume)
        city_stats = df_filtered.groupby('City').agg({
            'Customer ID': 'count',
            'Customer Status': lambda x: (x == 'Churned').sum(),
            'Satisfaction Score': lambda x: ((x >= 4).sum() - (x <= 2).sum()) / len(x) * 100 if len(x) > 0 else 0
        }).reset_index()
        city_stats.columns = ['City', 'Total', 'Churned', 'NPS']
        city_stats['Churn_Rate'] = (city_stats['Churned'] / city_stats['Total'] * 100).round(1)
        
        # Filtrer villes avec minimum 50 clients
        city_stats = city_stats[city_stats['Total'] >= 50]
        
        # ✅ TOP 5 PAR CHURN RATE
        top5_churn = city_stats.nlargest(5, 'Churn_Rate')
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(go.Bar(
            x=top5_churn['City'],
            y=top5_churn['NPS'],
            name='NPS',
            marker=dict(color='#3498db'),
            text=top5_churn['NPS'].round(1),
            textposition='outside',
            textfont=dict(color='white', size=12)
        ), secondary_y=False)
        
        fig.add_trace(go.Scatter(
            x=top5_churn['City'],
            y=top5_churn['Churn_Rate'],
            name='Taux de churn (%)',
            mode='lines+markers',
            line=dict(color='#e74c3c', width=4),
            marker=dict(size=14, symbol='diamond', line=dict(color='white', width=2))
        ), secondary_y=True)
        
        fig.update_yaxes(title_text="NPS", secondary_y=False, showgrid=True, gridcolor='rgba(255,255,255,0.1)')
        fig.update_yaxes(title_text="Taux de churn (%)", secondary_y=True, showgrid=False)
        
        fig.update_layout(
            height=350,
            plot_bgcolor='rgba(52, 73, 94, 0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis={'title': '', 'tickangle': -30},
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=50, r=50, t=60, b=70)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # ROW 4 - Stacked bar + Satisfaction par offre
    row4_cols = st.columns([1, 2])
    
    with row4_cols[0]:
        st.markdown("#### Répartition détracteurs/passives/promoteurs")
        
        # Protection division par zéro
        if total_respondents > 0:
            detractors_pct = round(detractors / total_respondents * 100, 2)
            passives = len(df_filtered[df_filtered['Satisfaction Score'] == 3])
            passives_pct = round(passives / total_respondents * 100, 2)
            promoters_pct = round(promoters / total_respondents * 100, 2)
        else:
            detractors_pct = 0.0
            passives_pct = 0.0
            promoters_pct = 0.0
            passives = 0
        
        fig = go.Figure(go.Bar(
            y=['NPS'],
            x=[detractors_pct],
            orientation='h',
            name='Détracteurs',
            marker=dict(color='#e74c3c'),
            text=f"{detractors_pct:.2f}%",
            textposition='inside'
        ))
        
        fig.add_trace(go.Bar(
            y=['NPS'],
            x=[passives_pct],
            orientation='h',
            name='Passives',
            marker=dict(color='#f39c12'),
            text=f"{passives_pct:.2f}%",
            textposition='inside'
        ))
        
        fig.add_trace(go.Bar(
            y=['NPS'],
            x=[promoters_pct],
            orientation='h',
            name='Promoteurs',
            marker=dict(color='#27AE60'),
            text=f"{promoters_pct:.2f}%",
            textposition='inside'
        ))
        
        fig.update_layout(
            barmode='stack',
            height=300,
            plot_bgcolor='rgba(52, 73, 94, 0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis={'showgrid': False},
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with row4_cols[1]:
        st.markdown("#### Taux de satisfaction par offre")
        
        # Distribution scores 1-5 par offre
        offer_sat_detail = df_filtered.groupby(['Offer', 'Satisfaction Score']).size().reset_index(name='Count')
        offer_totals = df_filtered.groupby('Offer').size().reset_index(name='Total')
        offer_sat_detail = offer_sat_detail.merge(offer_totals, on='Offer')
        offer_sat_detail['Percentage'] = (offer_sat_detail['Count'] / offer_sat_detail['Total'] * 100).round(2)
        
        fig = go.Figure()
        
        score_colors = {1: '#c0392b', 2: '#e74c3c', 3: '#f39c12', 4: '#3498db', 5: '#27AE60'}
        
        for score in [1, 2, 3, 4, 5]:
            data = offer_sat_detail[offer_sat_detail['Satisfaction Score'] == score]
            fig.add_trace(go.Bar(
                y=data['Offer'],
                x=data['Percentage'],
                name=f"★{score}",
                orientation='h',
                marker=dict(color=score_colors[score]),
                text=data['Percentage'].apply(lambda x: f"{x:.1f}%" if x > 5 else ""),
                textposition='inside'
            ))
        
        fig.update_layout(
            barmode='stack',
            height=300,
            plot_bgcolor='rgba(52, 73, 94, 0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis={'showgrid': False, 'title': 'Satisfaction Score'},
            showlegend=True,
            legend=dict(orientation="h", y=1.1)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # ROW 5 - Word Cloud + Treemap + Stream graph
    row5_cols = st.columns(3)
    
    with row5_cols[0]:
        st.markdown("#### Top 5 des raisons du désabonnement")
        
        if 'Churn Reason' in df_filtered.columns:
            churn_reasons = df_filtered[df_filtered['Customer Status'] == 'Churned']['Churn Reason'].value_counts().head(5)
            
            # Treemap simple
            fig = px.treemap(
                names=churn_reasons.index,
                parents=[""]* len(churn_reasons),
                values=churn_reasons.values,
                color=churn_reasons.values,
                color_continuous_scale='Reds'
            )
            fig.update_traces(textinfo="label+value")
            fig.update_layout(
                height=350,
                margin=dict(l=0, r=0, t=0, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with row5_cols[1]:
        st.markdown("#### Raisons avec volumes")
        
        if 'Churn Category' in df_filtered.columns:
            churn_cat = df_filtered[df_filtered['Customer Status'] == 'Churned']['Churn Category'].value_counts().head(5)
            
            fig = go.Figure(go.Bar(
                x=churn_cat.index,
                y=churn_cat.values,
                marker=dict(color=['#e74c3c', '#3498db', '#f39c12', '#9b59b6', '#1abc9c'][:len(churn_cat)]),
                text=churn_cat.values,
                textposition='outside'
            ))
            fig.update_layout(
                height=350,
                plot_bgcolor='rgba(52, 73, 94, 0.8)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis={'title': '', 'tickangle': -45},
                yaxis={'title': 'Nombre'},
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with row5_cols[2]:
        st.markdown("#### Produit et services Internet et téléphonique")
        
        # Stream graph des services par type internet
        internet_services = df_filtered.groupby(['Internet Type', 'Phone Service']).size().reset_index(name='Count')
        
        fig = px.area(
            internet_services,
            x='Internet Type',
            y='Count',
            color='Phone Service',
            color_discrete_map={'Yes': '#3498db', 'No': '#e74c3c'}
        )
        fig.update_layout(
            height=350,
            plot_bgcolor='rgba(52, 73, 94, 0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis={'title': 'Type Internet'},
            yaxis={'title': 'Nombre clients'}
        )
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.markdown('<h2 class="sub-title">Coût du Churn</h2>', unsafe_allow_html=True)
    
    # Vérifier données
    if len(df_filtered) == 0:
        st.warning("⚠️ Aucune donnée disponible")
    else:
        # KPI Total CA
        total_ca = df_filtered['Total Revenue'].sum() / 1_000_000
        
        # ROW 1 - KPI + Diagramme Gini + Répartition CA
        row1_cols = st.columns([1, 1, 2])
        
        with row1_cols[0]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%);
                        padding: 50px 20px; border-radius: 15px; text-align: center;
                        box-shadow: 0 8px 16px rgba(0,0,0,0.4);">
                <div style="font-size: 80px; font-weight: 700; color: #f39c12;">{total_ca:.1f}M€</div>
                <div style="font-size: 20px; color: rgba(255,255,255,0.9); margin-top: 15px; font-weight: 600;">CHIFFRE D'AFFAIRES TOTAL</div>
            </div>
            """, unsafe_allow_html=True)
        
        with row1_cols[1]:
            # Diagramme de Gini - Concentration du CA
            st.markdown("#### 📊 Concentration CA (Gini)")
            
            # Calculer indices de Gini pour différentes dimensions
            def gini_coefficient(values):
                sorted_values = sorted(values)
                n = len(sorted_values)
                cumsum = 0
                for i, val in enumerate(sorted_values):
                    cumsum += (2 * (i + 1) - n - 1) * val
                return cumsum / (n * sum(sorted_values)) if sum(sorted_values) > 0 else 0
            
            gini_data = {
                'Ville': gini_coefficient(df_filtered.groupby('City')['Total Revenue'].sum().values),
                'Âge': gini_coefficient(df_filtered.groupby('Tranche_Age')['Total Revenue'].sum().values),
                'Genre': gini_coefficient(df_filtered.groupby('Gender')['Total Revenue'].sum().values),
                'Offre': gini_coefficient(df_filtered.groupby('Offer')['Total Revenue'].sum().values),
                'Contrat': gini_coefficient(df_filtered.groupby('Contract')['Total Revenue'].sum().values)
            }
            
            gini_df = pd.DataFrame(list(gini_data.items()), columns=['Dimension', 'Gini'])
            gini_df['Concentration'] = (gini_df['Gini'] * 100).round(1)
            
            fig = go.Figure(go.Bar(
                y=gini_df['Dimension'],
                x=gini_df['Concentration'],
                orientation='h',
                marker=dict(
                    color=gini_df['Concentration'],
                    colorscale='Reds',
                    showscale=True
                ),
                text=gini_df['Concentration'].apply(lambda x: f"{x:.1f}%"),
                textposition='inside',
                textfont=dict(color='white', size=14, family='Arial Black')
            ))
            fig.update_layout(
                height=300,
                plot_bgcolor='rgba(52, 73, 94, 0.8)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis={'title': 'Indice de Gini (%)', 'showgrid': False},
                yaxis={'title': ''},
                showlegend=False,
                margin=dict(l=100, r=20, t=20, b=50)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with row1_cols[2]:
            st.markdown("#### Répartition du CA par statut client")
            
            ca_by_status = df_filtered.groupby('Customer Status').agg({
                'Total Revenue': 'sum'
            }).reset_index()
            ca_by_status['CA_M'] = (ca_by_status['Total Revenue'] / 1_000_000).round(2)
            ca_by_status['Percentage'] = (ca_by_status['Total Revenue'] / ca_by_status['Total Revenue'].sum() * 100).round(1)
            ca_by_status = ca_by_status.sort_values('CA_M', ascending=False)
            
            # Funnel chart amélioré
            colors_status = {
                'Stayed': '#27AE60',
                'Churned': '#e74c3c', 
                'Joined': '#3498db'
            }
            
            fig = go.Figure()
            
            for idx, row in ca_by_status.iterrows():
                fig.add_trace(go.Bar(
                    y=['CA Total'],
                    x=[row['Percentage']],
                    name=row['Customer Status'],
                    orientation='h',
                    marker=dict(color=colors_status.get(row['Customer Status'], '#95a5a6')),
                    text=f"{row['CA_M']:.1f}M€ ({row['Percentage']:.0f}%)",
                    textposition='inside',
                    textfont=dict(color='white', size=14, family='Arial')
                ))
            
            fig.update_layout(
                barmode='stack',
                height=300,
                plot_bgcolor='rgba(52, 73, 94, 0.8)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis={'showgrid': False, 'title': ''},
                yaxis={'showgrid': False, 'title': ''},
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # COURBE DE LORENZ + GINI - Concentration CA par clients
        st.markdown("### 📈 Concentration du CA parmi les clients")
        
        row_lorenz = st.columns([2, 1])
        
        with row_lorenz[0]:
            st.markdown("#### Courbe de Lorenz")
            
            # Calculer courbe de Lorenz CORRECTE
            ca_sorted = df_filtered.sort_values('Total Revenue')['Total Revenue'].values
            if len(ca_sorted) > 0:
                # Cumulatif du CA (en %)
                cumsum_ca = np.cumsum(ca_sorted)
                cumsum_ca_pct = (cumsum_ca / cumsum_ca[-1]) * 100
                
                # Ajouter le point de départ (0,0)
                cumsum_ca_pct = np.insert(cumsum_ca_pct, 0, 0)
                
                # Cumulatif des clients (en %)
                cumsum_clients_pct = (np.arange(len(ca_sorted) + 1) / len(ca_sorted)) * 100
                
                # Coefficient de Gini (aire entre courbe et diagonale)
                gini = 1 - 2 * np.trapz(cumsum_ca_pct / 100, cumsum_clients_pct / 100)
                
                fig = go.Figure()
                
                # Ligne d'égalité parfaite (diagonale)
                fig.add_trace(go.Scatter(
                    x=[0, 100],
                    y=[0, 100],
                    mode='lines',
                    name='Égalité parfaite',
                    line=dict(color='#95a5a6', width=2, dash='dash'),
                    hoverinfo='skip'
                ))
                
                # Courbe de Lorenz réelle (démarre à 0,0)
                fig.add_trace(go.Scatter(
                    x=cumsum_clients_pct,
                    y=cumsum_ca_pct,
                    mode='lines',
                    name='Distribution réelle',
                    line=dict(color='#ff6b6b', width=4),
                    fill='tonexty',
                    fillcolor='rgba(255, 107, 107, 0.2)',
                    hovertemplate='<b>%{x:.1f}%</b> clients<br><b>%{y:.1f}%</b> du CA<extra></extra>'
                ))
                
                # Annotation Gini
                fig.add_annotation(
                    x=50, y=25,
                    text=f"<b>Gini = {gini:.3f}</b><br>{'🔴 Forte inégalité' if gini > 0.5 else '🟡 Inégalité modérée' if gini > 0.3 else '🟢 Faible inégalité'}",
                    showarrow=False,
                    font=dict(size=16, color='white', family='Arial Black'),
                    bgcolor='rgba(0, 0, 0, 0.8)',
                    bordercolor='white',
                    borderwidth=2,
                    borderpad=10
                )
                
                fig.update_layout(
                    height=400,
                    plot_bgcolor='rgba(52, 73, 94, 0.8)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis={'title': '% Clients cumulés (classés du plus pauvre au plus riche)', 
                           'showgrid': True, 'gridcolor': 'rgba(255,255,255,0.1)', 'color': 'white',
                           'range': [0, 100]},
                    yaxis={'title': '% CA cumulé', 'showgrid': True, 
                           'gridcolor': 'rgba(255,255,255,0.1)', 'color': 'white',
                           'range': [0, 100]},
                    font=dict(color='white'),
                    showlegend=True,
                    legend=dict(x=0.02, y=0.98, bgcolor='rgba(0,0,0,0.7)', font=dict(color='white')),
                    margin=dict(l=60, r=20, t=30, b=70)
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with row_lorenz[1]:
            st.markdown("#### 💡 Interprétation")
            
            if gini < 0.3:
                interpretation = "🟢 **Faible inégalité**\n\nCA bien réparti entre clients"
            elif gini < 0.5:
                interpretation = "🟡 **Inégalité modérée**\n\nQuelques clients concentrent le CA"
            else:
                interpretation = "🔴 **Forte inégalité**\n\nPeu de clients génèrent l'essentiel du CA"
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(102,126,234,0.2) 0%, rgba(118,75,162,0.2) 100%);
                        padding: 30px; border-radius: 15px; border: 2px solid rgba(255,255,255,0.1);">
                <h3 style="color: white; margin-bottom: 20px;">Coefficient de Gini</h3>
                <div style="font-size: 48px; font-weight: 900; color: #ffd93d; text-align: center; margin: 20px 0;">
                    {gini:.3f}
                </div>
                <p style="color: rgba(255,255,255,0.9); font-size: 16px; line-height: 1.6;">
                    {interpretation}
                </p>
                <hr style="border-color: rgba(255,255,255,0.2); margin: 20px 0;">
                <p style="color: rgba(255,255,255,0.7); font-size: 14px; font-style: italic;">
                    0 = égalité parfaite<br>
                    1 = inégalité maximale
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ROW 2 - CA par Contrat + CA par Offre
        row2_cols = st.columns(2)
        
        with row2_cols[0]:
            st.markdown("#### CA par type de contrat")
            
            ca_contract = df_filtered.groupby('Contract').agg({
                'Total Revenue': 'sum'
            }).reset_index()
            ca_contract['CA_M'] = (ca_contract['Total Revenue'] / 1_000_000).round(2)
            ca_contract['Pct'] = (ca_contract['Total Revenue'] / ca_contract['Total Revenue'].sum() * 100).round(1)
            ca_contract = ca_contract.sort_values('CA_M', ascending=False)
            
            fig = go.Figure()
            contract_colors = {'Month-to-Month': '#f39c12', 'One Year': '#3498db', 'Two Year': '#27AE60'}
            
            for idx, row in ca_contract.iterrows():
                fig.add_trace(go.Bar(
                    y=['CA'],
                    x=[row['Pct']],
                    name=row['Contract'],
                    orientation='h',
                    marker=dict(color=contract_colors.get(row['Contract'], '#95a5a6')),
                    text=f"{row['CA_M']:.1f}M€<br>({row['Pct']:.1f}%)",
                    textposition='inside',
                    textfont=dict(color='white', size=12)
                ))
            
            fig.update_layout(
                barmode='stack',
                height=300,
                plot_bgcolor='rgba(52, 73, 94, 0.8)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis={'showgrid': False, 'title': '% du CA total'},
                yaxis={'showgrid': False, 'visible': False},
                showlegend=True,
                legend=dict(orientation="h", y=1.1),
                margin=dict(l=20, r=20, t=60, b=50)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with row2_cols[1]:
            st.markdown("#### CA par offre")
            
            ca_offer = df_filtered.groupby('Offer').agg({
                'Total Revenue': 'sum'
            }).reset_index()
            ca_offer['CA_M'] = (ca_offer['Total Revenue'] / 1_000_000).round(2)
            ca_offer = ca_offer.sort_values('CA_M', ascending=False)
            
            fig = go.Figure(go.Bar(
                y=ca_offer['Offer'],
                x=ca_offer['CA_M'],
                orientation='h',
                marker=dict(
                    color=ca_offer['CA_M'],
                    colorscale='Blues',
                    showscale=False
                ),
                text=ca_offer['CA_M'].apply(lambda x: f"{x:.2f}M€"),
                textposition='outside',
                textfont=dict(color='white', size=12)
            ))
            fig.update_layout(
                height=300,
                plot_bgcolor='rgba(52, 73, 94, 0.8)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis={'title': 'CA (M€)', 'showgrid': True, 'gridcolor': 'rgba(255,255,255,0.1)'},
                yaxis={'title': ''},
                showlegend=False,
                margin=dict(l=100, r=50, t=20, b=50)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # ROW 3 - CA par tranche d'âge + CA par CLV (Combos avec churn)
        row3_cols = st.columns(2)
        
        with row3_cols[0]:
            st.markdown("#### CA total par tranche d'âge + Taux de churn")
            
            ca_age = df_filtered.groupby('Tranche_Age').agg({
                'Total Revenue': 'sum',
                'Customer ID': 'count',
                'Customer Status': lambda x: (x == 'Churned').sum()
            }).reset_index()
            ca_age.columns = ['Tranche_Age', 'CA', 'Total', 'Churned']
            ca_age['CA_M'] = (ca_age['CA'] / 1_000_000).round(2)
            ca_age['Churn_Rate'] = (ca_age['Churned'] / ca_age['Total'] * 100).round(1)
            ca_age = ca_age.dropna().sort_values('Tranche_Age')
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(go.Scatter(
                x=ca_age['Tranche_Age'].astype(str),
                y=ca_age['CA_M'],
                name='CA Total (M€)',
                mode='lines+markers',
                line=dict(color='#3498db', width=4),
                marker=dict(size=10),
                fill='tozeroy',
                fillcolor='rgba(52, 152, 219, 0.3)'
            ), secondary_y=False)
            
            fig.add_trace(go.Scatter(
                x=ca_age['Tranche_Age'].astype(str),
                y=ca_age['Churn_Rate'],
                name='Taux de churn (%)',
                mode='lines+markers',
                line=dict(color='#e74c3c', width=4, dash='dot'),
                marker=dict(size=10, symbol='diamond')
            ), secondary_y=True)
            
            fig.update_yaxes(title_text="CA (M€)", secondary_y=False, showgrid=True, gridcolor='rgba(255,255,255,0.1)')
            fig.update_yaxes(title_text="Taux de churn (%)", secondary_y=True, showgrid=False)
            
            fig.update_layout(
                height=350,
                plot_bgcolor='rgba(52, 73, 94, 0.8)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis={'title': '', 'tickangle': -45},
                showlegend=True,
                legend=dict(orientation="h", y=1.1),
                margin=dict(l=50, r=50, t=60, b=80)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with row3_cols[1]:
            st.markdown("#### CA total par CLV + Taux de churn")
            
            ca_clv = df_filtered.groupby('CLV_Cat').agg({
                'Total Revenue': 'sum',
                'Customer ID': 'count',
                'Customer Status': lambda x: (x == 'Churned').sum()
            }).reset_index()
            ca_clv.columns = ['CLV_Cat', 'CA', 'Total', 'Churned']
            ca_clv['CA_M'] = (ca_clv['CA'] / 1_000_000).round(2)
            ca_clv['Churn_Rate'] = (ca_clv['Churned'] / ca_clv['Total'] * 100).round(1)
            ca_clv = ca_clv.dropna().sort_values('CLV_Cat')
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(go.Scatter(
                x=ca_clv['CLV_Cat'].astype(str),
                y=ca_clv['CA_M'],
                name='CA Total (M€)',
                mode='lines+markers',
                line=dict(color='#9b59b6', width=4),
                marker=dict(size=10),
                fill='tozeroy',
                fillcolor='rgba(155, 89, 182, 0.3)'
            ), secondary_y=False)
            
            fig.add_trace(go.Scatter(
                x=ca_clv['CLV_Cat'].astype(str),
                y=ca_clv['Churn_Rate'],
                name='Taux de churn (%)',
                mode='lines+markers',
                line=dict(color='#e74c3c', width=4, dash='dot'),
                marker=dict(size=10, symbol='diamond')
            ), secondary_y=True)
            
            fig.update_yaxes(title_text="CA (M€)", secondary_y=False, showgrid=True, gridcolor='rgba(255,255,255,0.1)')
            fig.update_yaxes(title_text="Taux de churn (%)", secondary_y=True, showgrid=False)
            
            fig.update_layout(
                height=350,
                plot_bgcolor='rgba(52, 73, 94, 0.8)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis={'title': '', 'tickangle': -45},
                showlegend=True,
                legend=dict(orientation="h", y=1.1),
                margin=dict(l=50, r=50, t=60, b=80)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # ROW 4 - Carte CA + Top 10 villes
        row4_cols = st.columns([3, 2])
        
        with row4_cols[0]:
            st.markdown("#### 🗺️ Top 10 Villes par CA - Cartographie")
            
            ca_geo = df_filtered.groupby(['City', 'Latitude', 'Longitude']).agg({
                'Total Revenue': 'sum',
                'Customer ID': 'count',
                'Customer Status': lambda x: (x == 'Churned').sum()
            }).reset_index()
            ca_geo.columns = ['City', 'Latitude', 'Longitude', 'CA', 'Total', 'Churned']
            ca_geo['CA_M'] = (ca_geo['CA'] / 1_000_000).round(2)
            ca_geo['Churn_Rate'] = (ca_geo['Churned'] / ca_geo['Total'] * 100).round(1)
            
            # TOP 10 VILLES UNIQUEMENT
            top10_ca_geo = ca_geo.nlargest(10, 'CA_M').dropna(subset=['Latitude', 'Longitude'])
            
            if len(top10_ca_geo) > 0:
                fig = px.scatter_mapbox(
                    top10_ca_geo,
                    lat='Latitude',
                    lon='Longitude',
                    size='CA_M',
                    color='CA_M',
                    hover_name='City',
                    hover_data={'CA_M': ':.2f M€', 'Total': True, 'Churn_Rate': ':.1f%',
                               'Latitude': False, 'Longitude': False},
                    color_continuous_scale='Viridis',  # Palette professionnelle jaune-vert-bleu
                    size_max=60,
                    zoom=5.5,
                    center={'lat': 36.7783, 'lon': -119.4179},
                    mapbox_style='carto-darkmatter',
                    labels={'CA_M': 'CA (M€)'}
                )
                
                # Ajouter labels texte des villes
                fig.add_trace(go.Scattermapbox(
                    lat=top10_ca_geo['Latitude'],
                    lon=top10_ca_geo['Longitude'],
                    mode='text',
                    text=top10_ca_geo['City'],
                    textfont=dict(size=12, color='white', family='Arial Black'),
                    hoverinfo='skip',
                    showlegend=False
                ))
                
                fig.update_layout(
                    height=500,
                    margin=dict(l=0, r=0, t=30, b=0),
                    coloraxis_colorbar=dict(
                        title="CA (M€)",
                        ticksuffix=" M€",
                        bgcolor='rgba(0,0,0,0.5)',
                        tickfont=dict(color='white'),
                        titlefont=dict(color='white')
                    ),
                    font=dict(color='white')
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with row4_cols[1]:
            st.markdown("#### Top 10 villes par CA")
            
            top10_ca = ca_geo.nlargest(10, 'CA_M')
            
            fig = go.Figure(go.Bar(
                y=top10_ca['City'],
                x=top10_ca['CA_M'],
                orientation='h',
                marker=dict(
                    color=top10_ca['CA_M'],
                    colorscale='Greens',
                    showscale=False
                ),
                text=top10_ca['CA_M'].apply(lambda x: f"{x:.2f}M€"),
                textposition='outside',
                textfont=dict(color='white', size=11)
            ))
            fig.update_layout(
                height=400,
                plot_bgcolor='rgba(52, 73, 94, 0.8)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis={'title': 'CA (M€)', 'showgrid': True, 'gridcolor': 'rgba(255,255,255,0.1)'},
                yaxis={'title': '', 'autorange': 'reversed'},
                showlegend=False,
                margin=dict(l=120, r=50, t=20, b=50)
            )
            st.plotly_chart(fig, use_container_width=True)


with tab5:
    st.markdown('<h2 class="sub-title">🔥 Focus Ville Critique - San Diego (Churn le plus élevé)</h2>', unsafe_allow_html=True)
    
    # Filtrer San Diego uniquement
    df_san_diego = df_filtered[df_filtered['City'] == 'San Diego'].copy()
    
    if len(df_san_diego) == 0:
        st.warning("⚠️ Aucune donnée pour San Diego avec les filtres actuels")
    else:
        # HEADER - KPIs San Diego
        sd_total = len(df_san_diego)
        sd_churned = len(df_san_diego[df_san_diego['Customer Status'] == 'Churned'])
        sd_churn_rate = (sd_churned / sd_total * 100).round(1) if sd_total > 0 else 0
        sd_ca = (df_san_diego['Total Revenue'].sum() / 1_000_000).round(2)
        
        kpi_sd = st.columns(4)
        
        with kpi_sd[0]:
            st.markdown(f"""
            <div class="kpi-card red">
                <div class="kpi-value">{sd_churn_rate}%</div>
                <div class="kpi-label">Taux de Churn</div>
            </div>
            """, unsafe_allow_html=True)
        
        with kpi_sd[1]:
            st.markdown(f"""
            <div class="kpi-card dark">
                <div class="kpi-value">{sd_total}</div>
                <div class="kpi-label">Clients Totaux</div>
            </div>
            """, unsafe_allow_html=True)
        
        with kpi_sd[2]:
            st.markdown(f"""
            <div class="kpi-card red">
                <div class="kpi-value">{sd_churned}</div>
                <div class="kpi-label">Clients Perdus</div>
            </div>
            """, unsafe_allow_html=True)
        
        with kpi_sd[3]:
            st.markdown(f"""
            <div class="kpi-card blue">
                <div class="kpi-value">{sd_ca}M€</div>
                <div class="kpi-label">Chiffre d'Affaires</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ROW 1 - Carte quartiers + Répartition offre
        row1_cols = st.columns([2, 1])
        
        with row1_cols[0]:
            st.markdown("#### 🗺️ Répartition géographique par quartier")
            
            # Grouper par coordonnées (quartiers approximatifs)
            district_map = df_san_diego.groupby(['Latitude', 'Longitude']).agg({
                'Customer ID': 'count',
                'Customer Status': lambda x: (x == 'Churned').sum()
            }).reset_index()
            district_map.columns = ['Latitude', 'Longitude', 'Total', 'Churned']
            district_map['Churn_Rate'] = (district_map['Churned'] / district_map['Total'] * 100).round(1)
            district_map = district_map.dropna()
            
            if len(district_map) > 0:
                fig = px.scatter_mapbox(
                    district_map,
                    lat='Latitude',
                    lon='Longitude',
                    size='Total',
                    color='Churn_Rate',
                    hover_data={'Total': True, 'Churned': True, 'Churn_Rate': ':.1f%', 
                               'Latitude': False, 'Longitude': False},
                    color_continuous_scale='Reds',
                    size_max=50,
                    zoom=10,
                    center={'lat': 32.7157, 'lon': -117.1611},
                    mapbox_style='satellite-streets'
                )
                fig.update_layout(
                    height=400,
                    margin=dict(l=0, r=0, t=0, b=0),
                    coloraxis_colorbar=dict(title="Churn %", ticksuffix="%")
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Pas assez de données géographiques pour cartographier les quartiers")
        
        with row1_cols[1]:
            st.markdown("#### Part des souscriptions aux offres")
            
            offer_sd = df_san_diego['Offer'].value_counts()
            
            fig = go.Figure(data=[go.Pie(
                labels=offer_sd.index,
                values=offer_sd.values,
                hole=0.5,
                marker=dict(colors=px.colors.qualitative.Bold),
                textposition='inside',
                textinfo='label+percent',
                textfont=dict(size=14, color='white')
            )])
            fig.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=True,
                legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05),
                margin=dict(l=0, r=100, t=0, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # ROW 2 - Tranches d'âge + Genre + Contrat
        row2_cols = st.columns(3)
        
        with row2_cols[0]:
            st.markdown("#### Répartition par tranche d'âge")
            
            age_sd = df_san_diego.groupby('Tranche_Age').size().reset_index(name='Count')
            age_sd = age_sd.dropna().sort_values('Count', ascending=False)
            
            fig = go.Figure(data=[go.Pie(
                labels=age_sd['Tranche_Age'].astype(str),
                values=age_sd['Count'],
                hole=0.4,
                marker=dict(colors=px.colors.sequential.Reds),
                textposition='inside',
                textinfo='label+percent',
                textfont=dict(size=12, color='white', family='Arial Black')
            )])
            fig.update_layout(
                height=300,
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                margin=dict(l=0, r=0, t=0, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with row2_cols[1]:
            st.markdown("#### Répartition par genre")
            
            gender_sd = df_san_diego['Gender'].value_counts()
            
            fig = go.Figure(data=[go.Pie(
                labels=gender_sd.index,
                values=gender_sd.values,
                hole=0.5,
                marker=dict(colors=['#34495e', '#e91e63']),
                textposition='inside',
                textinfo='label+percent',
                textfont=dict(size=16, color='white', family='Arial Black')
            )])
            fig.update_layout(
                height=300,
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                margin=dict(l=0, r=0, t=0, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with row2_cols[2]:
            st.markdown("#### Répartition par contrat")
            
            contract_sd = df_san_diego['Contract'].value_counts()
            
            contract_colors_pie = {
                'Month-to-Month': '#f39c12',
                'One Year': '#3498db',
                'Two Year': '#27AE60'
            }
            colors_list = [contract_colors_pie.get(c, '#95a5a6') for c in contract_sd.index]
            
            fig = go.Figure(data=[go.Pie(
                labels=contract_sd.index,
                values=contract_sd.values,
                hole=0.5,
                marker=dict(colors=colors_list),
                textposition='inside',
                textinfo='label+percent',
                textfont=dict(size=13, color='white', family='Arial Black')
            )])
            fig.update_layout(
                height=300,
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                margin=dict(l=0, r=0, t=0, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # ROW 3 - Raisons désabonnement + Taux attrition CLV
        row3_cols = st.columns([1, 1])
        
        with row3_cols[0]:
            st.markdown("#### 🚨 Raisons du désabonnement")
            
            if 'Churn Category' in df_san_diego.columns:
                churn_sd = df_san_diego[df_san_diego['Customer Status'] == 'Churned']
                if len(churn_sd) > 0:
                    reasons_sd = churn_sd['Churn Category'].value_counts().head(7)
                    
                    fig = go.Figure(go.Bar(
                        y=reasons_sd.index,
                        x=reasons_sd.values,
                        orientation='h',
                        marker=dict(
                            color=['#e74c3c', '#f39c12', '#3498db', '#9b59b6', '#1abc9c', '#e67e22', '#95a5a6'][:len(reasons_sd)],
                            line=dict(color='white', width=2)
                        ),
                        text=reasons_sd.values,
                        textposition='outside',
                        textfont=dict(color='white', size=14, family='Arial Black')
                    ))
                    fig.update_layout(
                        height=350,
                        plot_bgcolor='rgba(52, 73, 94, 0.8)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        xaxis={'title': 'Nombre de clients', 'showgrid': True, 'gridcolor': 'rgba(255,255,255,0.1)'},
                        yaxis={'title': '', 'autorange': 'reversed'},
                        showlegend=False,
                        margin=dict(l=150, r=50, t=20, b=50)
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Aucun client churned pour analyser les raisons")
            else:
                st.warning("Colonne 'Churn Category' non disponible")
        
        with row3_cols[1]:
            st.markdown("#### Taux d'attrition par CLV")
            
            clv_sd = df_san_diego.groupby('CLV_Cat').agg({
                'Customer ID': 'count',
                'Customer Status': lambda x: (x == 'Churned').sum()
            }).reset_index()
            clv_sd.columns = ['CLV_Cat', 'Total', 'Churned']
            clv_sd['Churn_Rate'] = (clv_sd['Churned'] / clv_sd['Total'] * 100).round(1)
            clv_sd = clv_sd.dropna()
            
            if len(clv_sd) > 0:
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                
                fig.add_trace(go.Bar(
                    x=clv_sd['CLV_Cat'].astype(str),
                    y=clv_sd['Total'],
                    name='Nombre clients',
                    marker=dict(color='#3498db'),
                    text=clv_sd['Total'],
                    textposition='outside'
                ), secondary_y=False)
                
                fig.add_trace(go.Scatter(
                    x=clv_sd['CLV_Cat'].astype(str),
                    y=clv_sd['Churn_Rate'],
                    name='Taux de churn (%)',
                    mode='lines+markers',
                    line=dict(color='#e74c3c', width=4),
                    marker=dict(size=12, symbol='diamond')
                ), secondary_y=True)
                
                fig.update_yaxes(title_text="Nombre clients", secondary_y=False)
                fig.update_yaxes(title_text="Taux de churn (%)", secondary_y=True)
                
                fig.update_layout(
                    height=350,
                    plot_bgcolor='rgba(52, 73, 94, 0.8)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis={'title': 'Catégorie CLV', 'tickangle': -45},
                    showlegend=True,
                    legend=dict(orientation="h", y=1.1),
                    margin=dict(l=50, r=50, t=60, b=80)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Données CLV insuffisantes")
        
        st.markdown("---")
        
        # FOOTER - Recommandations
        st.markdown("""
        ### 💡 Recommandations stratégiques pour San Diego
        
        **Actions prioritaires :**
        - 🎯 **Retention campaigns** ciblées sur les segments à fort churn
        - 📞 **Proactive outreach** pour les clients Month-to-Month
        - 💰 **Incentives** pour upgrade vers contrats annuels
        - 🔍 **Root cause analysis** sur raisons principales de départ
        - 📊 **Monitoring continu** des quartiers à risque élevé
        """)
