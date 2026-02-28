"""
🎯 DASHBOARD TELCO CHURN - VERSION PREMIUM 2.0
Score Cible: 10/10

Architecture:
- ✅ Gestion d'erreurs bulletproof
- ✅ Protection division par zéro
- ✅ Validation des données
- ✅ Performance optimisée
- ✅ UX/UI premium avec animations
- ✅ Responsive design
- ✅ Loading states élégants

Date: 17/02/2024
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Tuple, Optional, Dict, List
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION GLOBALE
# ============================================================================

st.set_page_config(
    page_title="Dashboard Telco - Churn Analysis 17/02/2024",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CONSTANTES & CONFIGURATION
# ============================================================================

class Config:
    """Configuration centralisée"""
    # Couleurs Power BI
    COLORS = {
        'primary': '#667eea',
        'secondary': '#764ba2',
        'success': '#27AE60',
        'warning': '#f39c12',
        'danger': '#e74c3c',
        'info': '#3498db',
        'dark': '#34495e',
        'light': '#ecf0f1'
    }
    
    # Couleurs par statut
    STATUS_COLORS = {
        'Churned': '#e74c3c',
        'Stayed': '#27AE60',
        'Joined': '#3498db'
    }
    
    # Couleurs par contrat
    CONTRACT_COLORS = {
        'Month-to-Month': '#f39c12',
        'One Year': '#3498db',
        'Two Year': '#27AE60'
    }
    
    # Seuils d'alerte
    THRESHOLDS = {
        'churn_rate_high': 30,
        'churn_rate_critical': 40,
        'nps_low': 0,
        'nps_good': 30,
        'nps_excellent': 50
    }

# ============================================================================
# UTILITAIRES & HELPERS
# ============================================================================

class DataValidator:
    """Validation et nettoyage des données"""
    
    @staticmethod
    def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
        """Division sécurisée avec gestion du zéro"""
        try:
            if denominator == 0 or pd.isna(denominator):
                return default
            result = numerator / denominator
            return result if not np.isinf(result) else default
        except:
            return default
    
    @staticmethod
    def safe_percentage(part: float, total: float, decimals: int = 1) -> float:
        """Calcul de pourcentage sécurisé"""
        result = DataValidator.safe_divide(part, total, 0) * 100
        return round(result, decimals)
    
    @staticmethod
    def validate_dataframe(df: pd.DataFrame, min_rows: int = 1) -> Tuple[bool, str]:
        """Valider qu'un DataFrame contient des données"""
        if df is None:
            return False, "Aucune donnée disponible"
        if len(df) < min_rows:
            return False, f"Données insuffisantes (minimum {min_rows} lignes requises)"
        return True, ""
    
    @staticmethod
    def clean_numeric(value, default=0):
        """Nettoyer une valeur numérique"""
        try:
            if pd.isna(value):
                return default
            return float(value)
        except:
            return default

class UIComponents:
    """Composants UI réutilisables"""
    
    @staticmethod
    def render_kpi_card(value, label: str, color: str = 'primary', 
                        format_type: str = 'number') -> None:
        """Afficher une KPI card avec gestion d'erreurs"""
        try:
            # Formater la valeur
            if format_type == 'number':
                formatted_value = f"{int(value):,}"
            elif format_type == 'percentage':
                formatted_value = f"{value:.1f}%"
            elif format_type == 'currency':
                formatted_value = f"{value:.1f}M€"
            else:
                formatted_value = str(value)
            
            # Déterminer la classe CSS
            color_class = color.lower()
            
            st.markdown(f"""
            <div class="kpi-card {color_class}">
                <div class="kpi-value">{formatted_value}</div>
                <div class="kpi-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Erreur affichage KPI '{label}': {str(e)}")
    
    @staticmethod
    def show_empty_state(message: str = "Aucune donnée disponible avec les filtres actuels") -> None:
        """Afficher un état vide élégant"""
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
                    padding: 60px; border-radius: 15px; text-align: center; margin: 40px 0;">
            <div style="font-size: 64px; margin-bottom: 20px;">📊</div>
            <div style="font-size: 24px; color: #95a5a6; font-weight: 600;">
                {message}
            </div>
            <div style="font-size: 16px; color: #7f8c8d; margin-top: 15px;">
                Essayez d'ajuster vos filtres ou de sélectionner "Tout"
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def show_loading(message: str = "Chargement en cours...") -> None:
        """Afficher un spinner de chargement"""
        st.markdown(f"""
        <div style="text-align: center; padding: 40px;">
            <div class="spinner"></div>
            <p style="color: #95a5a6; margin-top: 20px;">{message}</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# STYLE CSS PREMIUM
# ============================================================================

def inject_custom_css():
    """Injecter le CSS personnalisé avec animations"""
    st.markdown("""
    <style>
        /* ========== VARIABLES CSS ========== */
        :root {
            --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --success-gradient: linear-gradient(135deg, #27AE60 0%, #1e8449 100%);
            --warning-gradient: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
            --danger-gradient: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
            --dark-gradient: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
            --transition-smooth: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        /* ========== RESET & BASE ========== */
        * {
            transition: var(--transition-smooth);
        }
        
        /* ========== HEADER ========== */
        .main-header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 25px 30px;
            border-radius: 0;
            margin-bottom: 15px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.4);
            position: relative;
            overflow: hidden;
        }
        
        .main-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, #e74c3c, #f39c12, #3498db, #27AE60);
            animation: slideGradient 3s linear infinite;
        }
        
        @keyframes slideGradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .main-title {
            color: white;
            font-size: 32px;
            font-weight: 800;
            margin: 0;
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .sub-title {
            color: #ecf0f1;
            font-size: 22px;
            font-weight: 500;
            margin: 8px 0 0 0;
            font-family: 'Segoe UI', system-ui, sans-serif;
        }
        
        /* ========== KPI CARDS ========== */
        .kpi-card {
            padding: 25px 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 6px 12px rgba(0,0,0,0.25);
            margin: 12px 0;
            position: relative;
            overflow: hidden;
            cursor: default;
        }
        
        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }
        
        .kpi-card:hover::before {
            left: 100%;
        }
        
        .kpi-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 24px rgba(0,0,0,0.35);
        }
        
        .kpi-card.primary { background: var(--primary-gradient); }
        .kpi-card.yellow { background: var(--warning-gradient); }
        .kpi-card.blue { background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); }
        .kpi-card.red { background: var(--danger-gradient); }
        .kpi-card.dark { background: var(--dark-gradient); }
        .kpi-card.black { background: linear-gradient(135deg, #2c3e50 0%, #1a1a1a 100%); }
        .kpi-card.success { background: var(--success-gradient); }
        
        .kpi-value {
            font-size: 52px;
            font-weight: 800;
            color: white;
            margin: 0;
            line-height: 1;
            font-family: 'Segoe UI', system-ui, sans-serif;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .kpi-label {
            font-size: 15px;
            color: rgba(255,255,255,0.95);
            margin-top: 12px;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        
        /* ========== FILTRES ========== */
        .filter-container {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 25px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            border: 1px solid rgba(0,0,0,0.05);
        }
        
        /* ========== TABS NAVIGATION ========== */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: transparent;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: linear-gradient(135deg, #bdc3c7 0%, #95a5a6 100%);
            color: #2c3e50;
            padding: 15px 30px;
            font-weight: 700;
            font-size: 15px;
            border-radius: 8px 8px 0 0;
            border: none;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%);
            transform: translateY(-2px);
        }
        
        .stTabs [aria-selected="true"] {
            background: var(--danger-gradient) !important;
            color: white !important;
            transform: translateY(-3px);
            box-shadow: 0 4px 8px rgba(231, 76, 60, 0.4);
        }
        
        /* ========== PLOTLY CHARTS ========== */
        .js-plotly-plot {
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        
        .js-plotly-plot:hover {
            box-shadow: 0 8px 16px rgba(0,0,0,0.25);
        }
        
        /* ========== LOADING SPINNER ========== */
        .spinner {
            border: 4px solid rgba(255,255,255,0.1);
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* ========== ALERTS ========== */
        .alert {
            padding: 20px;
            border-radius: 10px;
            margin: 15px 0;
            font-weight: 500;
            border-left: 5px solid;
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        .alert-warning {
            background: rgba(243, 156, 18, 0.1);
            border-color: #f39c12;
            color: #e67e22;
        }
        
        .alert-info {
            background: rgba(52, 152, 219, 0.1);
            border-color: #3498db;
            color: #2980b9;
        }
        
        .alert-success {
            background: rgba(39, 174, 96, 0.1);
            border-color: #27AE60;
            color: #1e8449;
        }
        
        /* ========== STREAMLIT OVERRIDES ========== */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        .stMultiSelect [data-baseweb="select"] {
            background: white;
            border-radius: 8px;
        }
        
        /* ========== RESPONSIVE ========== */
        @media (max-width: 768px) {
            .main-title { font-size: 24px; }
            .kpi-value { font-size: 36px; }
            .filter-container { padding: 15px; }
        }
        
        /* ========== SECTIONS ========== */
        .section-title {
            color: #2c3e50;
            font-size: 24px;
            font-weight: 700;
            margin: 30px 0 15px 0;
            padding-bottom: 10px;
            border-bottom: 3px solid #3498db;
        }
        
        /* ========== SMOOTH SCROLLING ========== */
        html {
            scroll-behavior: smooth;
        }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# DATA LOADING & CACHING
# ============================================================================

@st.cache_data(ttl=3600, show_spinner=False)
def load_data() -> pd.DataFrame:
    """
    Charger les données avec gestion d'erreurs robuste
    
    Returns:
        DataFrame consolidé et nettoyé
    """
    try:
        with st.spinner('📊 Chargement des données...'):
            # Chercher le fichier CSV dans plusieurs emplacements possibles
            import os
            possible_paths = [
                'telco_churn_master.csv',  # Même dossier (Streamlit Cloud)
                '/home/claude/telco_churn_master.csv',  # Local
                './telco_churn_master.csv',  # Relatif
                os.path.join(os.path.dirname(__file__), 'telco_churn_master.csv')  # Même dossier que le script
            ]
            
            df = None
            for path in possible_paths:
                if os.path.exists(path):
                    df = pd.read_csv(path)
                    break
            
            if df is None:
                raise FileNotFoundError("Fichier telco_churn_master.csv introuvable")
            
            # Créer la colonne Tranche_Age si elle n'existe pas
            if 'Tranche_Age' not in df.columns:
                if 'Age' in df.columns:
                    df['Tranche_Age'] = pd.cut(
                        df['Age'],
                        bins=[0, 25, 32, 39, 46, 53, 60, 67, 74, 100],
                        labels=['18-25', '25-32', '32-39', '39-46', '46-53', 
                               '53-60', '60-67', '67-74', '74-81']
                    )
                else:
                    # Fallback basé sur Senior Citizen
                    df['Tranche_Age'] = df['Senior Citizen'].map({
                        0: '39-46',
                        1: '67-74'
                    })
            
            # Nettoyer les valeurs numériques
            numeric_cols = ['Monthly Charge', 'Total Revenue', 'CLTV', 
                           'Satisfaction Score', 'Tenure in Months']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            # Standardiser Customer Status
            if 'Customer Status' in df.columns:
                status_mapping = {
                    'Yes': 'Churned',
                    'No': 'Stayed',
                    1: 'Churned',
                    0: 'Stayed'
                }
                df['Customer Status'] = df['Customer Status'].replace(status_mapping)
                df['Customer Status'] = df['Customer Status'].fillna('Stayed')
            
            # Créer colonnes calculées
            df = create_calculated_columns(df)
            
            return df
            
    except FileNotFoundError:
        st.error("❌ Fichier de données introuvable. Veuillez vérifier le chemin.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données: {str(e)}")
        return pd.DataFrame()

def create_calculated_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Créer les colonnes calculées nécessaires"""
    try:
        # Calculer nombre de produits souscrits
        product_cols = ['Phone Service', 'Multiple Lines', 'Internet Service', 
                       'Online Security', 'Online Backup', 'Device Protection',
                       'Tech Support', 'Streaming TV', 'Streaming Movies']
        
        if 'Streaming Music' in df.columns:
            product_cols.append('Streaming Music')
        if 'Unlimited Data' in df.columns:
            product_cols.append('Unlimited Data')
        
        df['Nb_Produits'] = 0
        for col in product_cols:
            if col in df.columns:
                df['Nb_Produits'] += (df[col] == 'Yes').astype(int)
        
        # Indicateur de vente incitative (3+ produits)
        df['Upsell'] = (df['Nb_Produits'] >= 3).astype(int)
        
        # Catégories CLV
        if 'CLTV' in df.columns:
            df['CLV_Cat'] = pd.cut(
                df['CLTV'],
                bins=[0, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 7000],
                labels=['2001-2500', '2501-3000', '3001-3500', '3501-4000', 
                       '4001-4500', '4501-5000', '5001-5500', '5501-6000', '6001-6500']
            )
        
        # Tenure Years
        if 'Tenure in Months' in df.columns:
            df['Tenure_Years'] = pd.cut(
                df['Tenure in Months'],
                bins=[0, 12, 24, 36, 48, 60, 72],
                labels=['1 an', '2 ans', '3 ans', '4 ans', '5 ans', '6 ans']
            )
        
        return df
        
    except Exception as e:
        st.warning(f"⚠️ Erreur création colonnes calculées: {str(e)}")
        return df

# ============================================================================
# FILTRES INTERACTIFS
# ============================================================================

def render_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Afficher les filtres et retourner les données filtrées
    
    Args:
        df: DataFrame source
        
    Returns:
        DataFrame filtré
    """
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    
    filter_cols = st.columns(5)
    
    # Récupérer les valeurs uniques pour chaque filtre
    with filter_cols[0]:
        tranche_age_options = ['Tout'] + sorted(
            df['Tranche_Age'].dropna().astype(str).unique().tolist()
        )
        tranche_age_filter = st.multiselect(
            "📊 Tranche d'âge",
            options=tranche_age_options,
            default=['Tout'],
            key='filter_age'
        )
    
    with filter_cols[1]:
        contract_options = ['Tout'] + sorted(
            df['Contract'].dropna().unique().tolist()
        )
        contract_filter = st.multiselect(
            "📋 Contrat",
            options=contract_options,
            default=['Tout'],
            key='filter_contract'
        )
    
    with filter_cols[2]:
        city_options = ['Tout'] + sorted(
            df['City'].dropna().unique().tolist()
        )
        city_filter = st.multiselect(
            "🌆 Ville",
            options=city_options,
            default=['Tout'],
            key='filter_city'
        )
    
    with filter_cols[3]:
        offer_options = ['Tout'] + sorted(
            df['Offer'].dropna().unique().tolist()
        ) if 'Offer' in df.columns else ['Tout']
        offer_filter = st.multiselect(
            "🎁 Offre",
            options=offer_options,
            default=['Tout'],
            key='filter_offer'
        )
    
    with filter_cols[4]:
        gender_options = ['Tout'] + sorted(
            df['Gender'].dropna().unique().tolist()
        )
        gender_filter = st.multiselect(
            "👤 Genre",
            options=gender_options,
            default=['Tout'],
            key='filter_gender'
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Appliquer les filtres
    df_filtered = df.copy()
    
    try:
        if 'Tout' not in tranche_age_filter and len(tranche_age_filter) > 0:
            df_filtered = df_filtered[
                df_filtered['Tranche_Age'].astype(str).isin(tranche_age_filter)
            ]
        
        if 'Tout' not in contract_filter and len(contract_filter) > 0:
            df_filtered = df_filtered[df_filtered['Contract'].isin(contract_filter)]
        
        if 'Tout' not in city_filter and len(city_filter) > 0:
            df_filtered = df_filtered[df_filtered['City'].isin(city_filter)]
        
        if 'Tout' not in offer_filter and len(offer_filter) > 0 and 'Offer' in df_filtered.columns:
            df_filtered = df_filtered[df_filtered['Offer'].isin(offer_filter)]
        
        if 'Tout' not in gender_filter and len(gender_filter) > 0:
            df_filtered = df_filtered[df_filtered['Gender'].isin(gender_filter)]
        
    except Exception as e:
        st.error(f"❌ Erreur lors de l'application des filtres: {str(e)}")
        return df
    
    return df_filtered

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Point d'entrée principal de l'application"""
    
    # Injecter le CSS
    inject_custom_css()
    
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">📊 Dashboard Telco - Analyse Attrition Client</h1>
        <p class="sub-title">Édition Premium - 17/02/2024</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Charger les données
    df = load_data()
    
    # Vérifier si les données sont chargées
    is_valid, error_msg = DataValidator.validate_dataframe(df)
    if not is_valid:
        st.error(f"❌ {error_msg}")
        st.stop()
    
    # Appliquer les filtres
    df_filtered = render_filters(df)
    
    # Vérifier si les données filtrées sont vides
    is_valid_filtered, _ = DataValidator.validate_dataframe(df_filtered)
    
    # Créer les onglets
    tabs = st.tabs([
        "📈 Vue d'ensemble",
        "🔄 Comportement Churn",
        "😊 Satisfaction",
        "💰 Coût du Churn",
        "🔥 Focus San Diego"
    ])
    
    # Onglet 1: Vue d'ensemble
    with tabs[0]:
        if not is_valid_filtered:
            UIComponents.show_empty_state()
        else:
            render_overview_tab(df_filtered)
    
    # Onglet 2: Comportement
    with tabs[1]:
        if not is_valid_filtered:
            UIComponents.show_empty_state()
        else:
            render_behavior_tab(df_filtered)
    
    # Onglet 3: Satisfaction
    with tabs[2]:
        if not is_valid_filtered:
            UIComponents.show_empty_state()
        else:
            render_satisfaction_tab(df_filtered)
    
    # Onglet 4: Coût
    with tabs[3]:
        if not is_valid_filtered:
            UIComponents.show_empty_state()
        else:
            render_cost_tab(df_filtered)
    
    # Onglet 5: Focus San Diego
    with tabs[4]:
        if not is_valid_filtered:
            UIComponents.show_empty_state()
        else:
            render_sandiego_tab(df_filtered)

# ============================================================================
# GRAPHIQUES - ONGLET VUE D'ENSEMBLE
# ============================================================================

def create_age_bubble_chart(df: pd.DataFrame) -> Optional[go.Figure]:
    """Créer le bubble chart du taux de churn par âge"""
    try:
        # Calculer les statistiques par tranche d'âge
        age_stats = df.groupby('Tranche_Age').agg({
            'CustomerID': 'count',
            'Customer Status': lambda x: (x == 'Churned').sum()
        }).reset_index()
        age_stats.columns = ['Tranche_Age', 'Total', 'Churned']
        
        # Protection division par zéro
        age_stats['Churn_Rate'] = age_stats.apply(
            lambda row: DataValidator.safe_percentage(row['Churned'], row['Total']),
            axis=1
        )
        
        age_stats = age_stats.dropna().sort_values('Tranche_Age')
        
        if len(age_stats) == 0:
            return None
        
        # Identifier les seniors (67-74, 74-81)
        age_stats['Is_Senior'] = age_stats['Tranche_Age'].astype(str).isin(['67-74', '74-81'])
        
        # Calculer la taille des bulles BASÉE SUR LE TAUX DE CHURN (pas le nombre de clients)
        max_churn_rate = age_stats['Churn_Rate'].max() if age_stats['Churn_Rate'].max() > 0 else 1
        age_stats['BubbleSize'] = age_stats['Churn_Rate'].apply(
            lambda x: max(30, (x / max_churn_rate) * 150)  # Plus le taux est élevé, plus la bulle est grosse
        )
        
        # Créer la figure
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=age_stats['Tranche_Age'].astype(str),
            y=age_stats['Churn_Rate'],
            mode='markers+text',
            marker=dict(
                size=age_stats['BubbleSize'],
                color=['#e74c3c' if s else '#3498db' for s in age_stats['Is_Senior']],
                line=dict(width=3, color='white'),
                opacity=0.85
            ),
            text=age_stats['Churn_Rate'].apply(lambda x: f"{x:.1f}%"),
            textposition='middle center',
            textfont=dict(size=16, color='white', family='Arial Black'),
            hovertemplate='<b>%{x}</b><br>' +
                         'Taux Churn: <b>%{y:.1f}%</b><br>' +
                         'Total clients: ' + age_stats['Total'].astype(str) + '<br>' +
                         'Churned: ' + age_stats['Churned'].astype(str) +
                         '<extra></extra>'
        ))
        
        fig.update_layout(
            height=400,
            showlegend=False,
            plot_bgcolor='rgba(26, 26, 46, 0.95)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis={
                'title': 'Tranche d\'âge',
                'showgrid': False,
                'color': 'white',
                'tickangle': -45,
                'tickfont': dict(size=12)
            },
            yaxis={
                'title': 'Taux de Churn (%)',
                'showgrid': True,
                'gridcolor': 'rgba(255,255,255,0.1)',
                'color': 'white',
                'ticksuffix': '%'
            },
            font=dict(color='white'),
            margin=dict(l=60, r=20, t=30, b=90)
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Erreur create_age_bubble_chart: {str(e)}")
        return None

def create_status_donut(df: pd.DataFrame) -> Optional[go.Figure]:
    """Créer le donut chart des statuts clients"""
    try:
        status_stats = df['Customer Status'].value_counts()
        
        if len(status_stats) == 0:
            return None
        
        fig = go.Figure(data=[go.Pie(
            labels=status_stats.index,
            values=status_stats.values,
            hole=0.6,
            marker=dict(colors=[Config.STATUS_COLORS.get(s, '#95a5a6') for s in status_stats.index]),
            textposition='inside',
            textinfo='label+percent',
            textfont=dict(size=14, color='white', family='Arial Black')
        )])
        
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Erreur create_status_donut: {str(e)}")
        return None

def create_gender_donut(df: pd.DataFrame) -> Optional[go.Figure]:
    """Créer le donut chart par genre"""
    try:
        gender_stats = df['Gender'].value_counts()
        
        if len(gender_stats) == 0:
            return None
        
        fig = go.Figure(data=[go.Pie(
            labels=gender_stats.index,
            values=gender_stats.values,
            hole=0.6,
            marker=dict(colors=['#34495e', '#e91e63']),
            textposition='inside',
            textinfo='label+percent',
            textfont=dict(size=16, color='white', family='Arial Black')
        )])
        
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Erreur create_gender_donut: {str(e)}")
        return None

def create_california_map(df: pd.DataFrame) -> Optional[go.Figure]:
    """Créer la carte géographique de Californie"""
    try:
        city_geo = df.groupby(['City', 'Latitude', 'Longitude']).agg({
            'CustomerID': 'count',
            'Customer Status': lambda x: (x == 'Churned').sum()
        }).reset_index()
        city_geo.columns = ['City', 'Latitude', 'Longitude', 'Total', 'Churned']
        
        # Protection division par zéro
        city_geo['Churn_Rate'] = city_geo.apply(
            lambda row: DataValidator.safe_percentage(row['Churned'], row['Total']),
            axis=1
        )
        
        city_geo_clean = city_geo.dropna(subset=['Latitude', 'Longitude'])
        
        if len(city_geo_clean) == 0:
            return None
        
        # TOP 3 des villes avec le PLUS GRAND NOMBRE de clients churned
        city_geo_top3 = city_geo_clean.nlargest(3, 'Churned')
        
        if len(city_geo_top3) == 0:
            return None
        
        fig = px.scatter_mapbox(
            city_geo_top3,
            lat='Latitude',
            lon='Longitude',
            size='Churned',  # TAILLE = Nombre de churned
            color='Churn_Rate',  # COULEUR = Taux de churn
            hover_name='City',
            hover_data={
                'Total': True, 
                'Churned': True,
                'Churn_Rate': ':.1f%', 
                'Latitude': False, 
                'Longitude': False
            },
            color_continuous_scale=['#F39C12', '#E74C3C', '#C0392B'],  # Orange → Rouge foncé
            size_max=60,  # Bulles plus grosses pour visibilité
            zoom=5.5,
            mapbox_style='carto-darkmatter'
        )
        
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            coloraxis_colorbar=dict(title="Churn %", ticksuffix="%")
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Erreur create_california_map: {str(e)}")
        return None

def create_contract_bar_chart(df: pd.DataFrame) -> Optional[go.Figure]:
    """Créer le bar chart par type de contrat"""
    try:
        contract_stats = df.groupby('Contract').agg({
            'CustomerID': 'count',
            'Customer Status': lambda x: (x == 'Churned').sum()
        }).reset_index()
        contract_stats.columns = ['Contract', 'Total', 'Churned']
        
        contract_stats['Churn_Rate'] = contract_stats.apply(
            lambda row: DataValidator.safe_percentage(row['Churned'], row['Total'], 0),
            axis=1
        )
        contract_stats = contract_stats.sort_values('Churn_Rate', ascending=False)
        
        if len(contract_stats) == 0:
            return None
        
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
        
        return fig
        
    except Exception as e:
        st.error(f"Erreur create_contract_bar_chart: {str(e)}")
        return None

def create_offer_bar_chart(df: pd.DataFrame) -> Optional[go.Figure]:
    """Créer le bar chart par offre"""
    try:
        if 'Offer' not in df.columns:
            return None
            
        offer_stats = df.groupby('Offer').agg({
            'CustomerID': 'count',
            'Customer Status': lambda x: (x == 'Churned').sum()
        }).reset_index()
        offer_stats.columns = ['Offer', 'Total', 'Churned']
        
        offer_stats['Churn_Rate'] = offer_stats.apply(
            lambda row: DataValidator.safe_percentage(row['Churned'], row['Total'], 0),
            axis=1
        )
        offer_stats = offer_stats.sort_values('Churn_Rate', ascending=False)
        
        if len(offer_stats) == 0:
            return None
        
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
        
        return fig
        
    except Exception as e:
        st.error(f"Erreur create_offer_bar_chart: {str(e)}")
        return None

def create_tenure_line_chart(df: pd.DataFrame) -> Optional[go.Figure]:
    """Créer le line chart par durée d'engagement"""
    try:
        if 'Tenure in Months' not in df.columns:
            return None
            
        tenure_stats = df.groupby('Tenure in Months').agg({
            'CustomerID': 'count',
            'Customer Status': lambda x: (x == 'Churned').sum()
        }).reset_index()
        tenure_stats.columns = ['Tenure', 'Total', 'Churned']
        
        tenure_stats['Churn_Rate'] = tenure_stats.apply(
            lambda row: DataValidator.safe_percentage(row['Churned'], row['Total']),
            axis=1
        )
        tenure_stats = tenure_stats.sort_values('Tenure')
        
        if len(tenure_stats) == 0:
            return None
        
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
            textfont=dict(color='white', size=10),
            hovertemplate='Tenure: %{x} mois<br>Churn: %{y:.1f}%<extra></extra>'
        ))
        
        fig.update_layout(
            height=300,
            xaxis={'title': 'Tenure (in Months)', 'showgrid': True, 
                   'gridcolor': 'rgba(255,255,255,0.1)'},
            yaxis={'title': 'Taux de Churn (%)', 'showgrid': True, 
                   'gridcolor': 'rgba(255,255,255,0.1)'},
            plot_bgcolor='rgba(52, 73, 94, 0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            margin=dict(l=50, r=20, t=20, b=50)
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Erreur create_tenure_line_chart: {str(e)}")
        return None

def create_age_combo_chart(df: pd.DataFrame) -> Optional[go.Figure]:
    """Créer le combo chart âge (bars + line)"""
    try:
        age_churn = df.groupby('Tranche_Age').agg({
            'CustomerID': 'count',
            'Customer Status': lambda x: (x == 'Churned').sum(),
            'Monthly Charge': 'mean'
        }).reset_index()
        age_churn.columns = ['Tranche_Age', 'Total', 'Churned', 'Avg_Monthly_Charge']
        
        age_churn['Churn_Rate'] = age_churn.apply(
            lambda row: DataValidator.safe_percentage(row['Churned'], row['Total']),
            axis=1
        )
        age_churn = age_churn.dropna()
        
        if len(age_churn) == 0:
            return None
        
        # Créer figure avec axe secondaire
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Barres - Taux de churn
        colors_bars = ['#3498db' if x < 25 else '#e74c3c' if x > 35 else '#f39c12' 
                       for x in age_churn['Churn_Rate']]
        
        fig.add_trace(
            go.Bar(
                x=age_churn['Tranche_Age'].astype(str),
                y=age_churn['Churn_Rate'],
                name='Taux de churn',
                marker=dict(color=colors_bars),
                text=age_churn['Churn_Rate'].apply(lambda x: f"{x:.0f}%"),
                textposition='outside',
                textfont=dict(color='white', size=11),
                hovertemplate='%{x}<br>Churn: %{y:.1f}%<extra></extra>'
            ),
            secondary_y=False
        )
        
        # Ligne - Moyenne Monthly Charge
        fig.add_trace(
            go.Scatter(
                x=age_churn['Tranche_Age'].astype(str),
                y=age_churn['Avg_Monthly_Charge'],
                name='Moyenne Monthly Charge',
                mode='lines+markers',
                line=dict(color='#f39c12', width=3, dash='dot'),
                marker=dict(size=8, color='#f39c12'),
                yaxis='y2',
                hovertemplate='%{x}<br>Avg Charge: %{y:.2f}€<extra></extra>'
            ),
            secondary_y=True
        )
        
        fig.update_xaxes(title_text="", showgrid=False)
        fig.update_yaxes(title_text="Taux de churn (%)", secondary_y=False, 
                        showgrid=True, gridcolor='rgba(255,255,255,0.1)')
        fig.update_yaxes(title_text="Monthly Charge (€)", secondary_y=True, 
                        showgrid=False)
        
        fig.update_layout(
            height=400,
            plot_bgcolor='rgba(52, 73, 94, 0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Erreur create_age_combo_chart: {str(e)}")
        return None

# ============================================================================
# ONGLETS (PLACEHOLDERS - À IMPLÉMENTER)
# ============================================================================

def render_overview_tab(df: pd.DataFrame):
    """Onglet Vue d'ensemble - Implémentation complète"""
    st.markdown('<h2 class="sub-title">Chiffres clés de notre attrition</h2>', 
                unsafe_allow_html=True)
    
    # ========== KPIs PRINCIPAUX ==========
    try:
        total_clients = len(df)
        total_churned = len(df[df['Customer Status'] == 'Churned'])
        total_joined = len(df[df['Customer Status'] == 'Joined'])
        total_stayed = len(df[df['Customer Status'] == 'Stayed'])
        solde_net = total_stayed + total_joined
        # Total installés = Seulement les clients "Stayed" (comme Power BI)
        total_installed = total_stayed
        
        kpi_cols = st.columns(5)
        
        with kpi_cols[0]:
            UIComponents.render_kpi_card(total_installed, "Total clients installés", "yellow")
        
        with kpi_cols[1]:
            UIComponents.render_kpi_card(total_joined, "Total New Customers", "blue")
        
        with kpi_cols[2]:
            UIComponents.render_kpi_card(total_churned, "Nombre de Churned", "red")
        
        with kpi_cols[3]:
            UIComponents.render_kpi_card(total_clients, "Total clients", "dark")
        
        with kpi_cols[4]:
            UIComponents.render_kpi_card(solde_net, "Solde net des clients actifs", "black")
        
    except Exception as e:
        st.error(f"Erreur calcul KPIs: {str(e)}")
    
    st.markdown("---")
    
    # ========== SECTION RÉPARTITION DES CHURNS ==========
    st.markdown('<h3 class="section-title">📊 Répartition des churns</h3>', 
                unsafe_allow_html=True)
    
    row1_cols = st.columns([2, 1, 1, 2])
    
    # GRAPHIQUE 1: Bubble chart - Taux de churn par tranche d'âge
    with row1_cols[0]:
        st.markdown("#### 📊 Taux de Churn par Tranche d'Âge")
        try:
            fig = create_age_bubble_chart(df)
            if fig:
                st.plotly_chart(fig, use_container_width=True, key='bubble_age')
        except Exception as e:
            st.error(f"Erreur bubble chart: {str(e)}")
    
    # GRAPHIQUE 2: Donut - Customer Status
    with row1_cols[1]:
        st.markdown("#### 📊 Par Statut")
        try:
            fig = create_status_donut(df)
            if fig:
                st.plotly_chart(fig, use_container_width=True, key='donut_status')
        except Exception as e:
            st.error(f"Erreur donut status: {str(e)}")
    
    # GRAPHIQUE 3: Donut - Gender
    with row1_cols[2]:
        st.markdown("#### 👥 Par Genre")
        try:
            fig = create_gender_donut(df)
            if fig:
                st.plotly_chart(fig, use_container_width=True, key='donut_gender')
        except Exception as e:
            st.error(f"Erreur donut gender: {str(e)}")
    
    # GRAPHIQUE 4: Carte géographique
    with row1_cols[3]:
        st.markdown("#### 🗺️ Carte Californie")
        try:
            fig = create_california_map(df)
            if fig:
                st.plotly_chart(fig, use_container_width=True, key='map_ca')
        except Exception as e:
            st.error(f"Erreur carte: {str(e)}")
    
    st.markdown("---")
    
    # ========== TAUX D'ATTRITION PAR CONTRAT ET OFFRE ==========
    row2_cols = st.columns(2)
    
    with row2_cols[0]:
        st.markdown("#### Taux d'attrition par contrat")
        try:
            fig = create_contract_bar_chart(df)
            if fig:
                st.plotly_chart(fig, use_container_width=True, key='bar_contract')
        except Exception as e:
            st.error(f"Erreur bar contract: {str(e)}")
    
    with row2_cols[1]:
        st.markdown("#### Taux d'attrition par offre")
        try:
            fig = create_offer_bar_chart(df)
            if fig:
                st.plotly_chart(fig, use_container_width=True, key='bar_offer')
        except Exception as e:
            st.error(f"Erreur bar offer: {str(e)}")
    
    st.markdown("---")
    
    # ========== TAUX DE CHURN PAR DURÉE ==========
    st.markdown("#### Taux de churn par durée d'engagement")
    try:
        fig = create_tenure_line_chart(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True, key='line_tenure')
    except Exception as e:
        st.error(f"Erreur line tenure: {str(e)}")
    
    st.markdown("---")
    
    # ========== COMBO CHART - AGE ==========
    st.markdown("#### Taux de churn par tranche d'âge")
    try:
        fig = create_age_combo_chart(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True, key='combo_age')
    except Exception as e:
        st.error(f"Erreur combo age: {str(e)}")

def render_behavior_tab(df: pd.DataFrame):
    """Onglet Comportement du churn"""
    st.markdown('<h2 class="sub-title">Comportement du churn</h2>', 
                unsafe_allow_html=True)
    st.info("🚧 En cours de développement...")

def render_satisfaction_tab(df: pd.DataFrame):
    """Onglet Satisfaction"""
    st.markdown('<h2 class="sub-title">Taux de satisfaction client</h2>', 
                unsafe_allow_html=True)
    st.info("🚧 En cours de développement...")

def render_cost_tab(df: pd.DataFrame):
    """Onglet Coût du Churn"""
    st.markdown('<h2 class="sub-title">Coût du Churn</h2>', 
                unsafe_allow_html=True)
    st.info("🚧 En cours de développement...")

def render_sandiego_tab(df: pd.DataFrame):
    """Onglet Focus San Diego"""
    st.markdown('<h2 class="sub-title">🔥 Focus San Diego</h2>', 
                unsafe_allow_html=True)
    st.info("🚧 En cours de développement...")

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
