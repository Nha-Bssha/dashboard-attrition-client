"""
🎮 SIMULATEUR IMPACT NPS - VERSION PREMIUM
Component standalone pour onglet Satisfaction

Features:
- Sliders interactifs (Detractors/Passives conversion)
- Calculs temps réel (NPS, churn, revenue, ROI)
- Graphique sensibilité
- Recommandations auto-générées
- Scénarios prédéfinis

Author: EthicalDataBoost
Date: 2025-03-03
Version: 1.0
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render_nps_simulator(df: pd.DataFrame):
    """
    Simulateur Impact NPS - Version complète
    
    Args:
        df: DataFrame avec colonnes requises:
            - NPS_Category (Detractors/Passives/Promoters)
            - CLTV (Customer Lifetime Value)
            - Is_Churned (0/1)
    
    Returns:
        None (affiche directement dans Streamlit)
    """
    
    st.markdown("""
    <style>
    .simulator-container {
        background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
        padding: 30px;
        border-radius: 15px;
        border: 2px solid rgba(102,126,234,0.3);
        margin: 20px 0;
    }
    
    .metric-simulator {
        background: rgba(255,255,255,0.05);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
    }
    
    .metric-simulator:hover {
        transform: translateY(-5px);
        border-color: rgba(102,126,234,0.5);
        box-shadow: 0 10px 30px rgba(102,126,234,0.2);
    }
    
    .metric-value-big {
        font-size: 48px;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 10px 0;
    }
    
    .metric-label-sim {
        font-size: 14px;
        color: #95a5a6;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    .metric-delta-sim {
        font-size: 16px;
        font-weight: 600;
        margin-top: 8px;
    }
    
    .scenario-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 5px;
    }
    
    .scenario-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102,126,234,0.4);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # ========================================
    # HEADER
    # ========================================
    
    st.markdown("""
    <div class="simulator-container">
        <h2 style="color: #667eea; margin: 0;">🎮 Simulateur Impact NPS</h2>
        <p style="color: #95a5a6; margin: 10px 0 0 0;">
            Ajustez les paramètres pour calculer l'impact business d'une amélioration satisfaction en temps réel
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================
    # CALCULS ÉTAT INITIAL
    # ========================================
    
    try:
        total_clients = len(df)
        
        # Distribution NPS actuelle
        detractors_count = (df['NPS_Category'] == 'Detractors').sum()
        passives_count = (df['NPS_Category'] == 'Passives').sum()
        promoters_count = (df['NPS_Category'] == 'Promoters').sum()
        
        detractors_pct = (detractors_count / total_clients) * 100
        passives_pct = (passives_count / total_clients) * 100
        promoters_pct = (promoters_count / total_clients) * 100
        
        nps_current = promoters_pct - detractors_pct
        
        # CLTV moyen (données réelles)
        if 'CLTV' in df.columns:
            cltv_detractors = df[df['NPS_Category'] == 'Detractors']['CLTV'].mean()
            cltv_passives = df[df['NPS_Category'] == 'Passives']['CLTV'].mean()
            cltv_promoters = df[df['NPS_Category'] == 'Promoters']['CLTV'].mean()
            cltv_avg = df['CLTV'].mean()
        else:
            # Fallback
            cltv_detractors = 4139
            cltv_passives = 4473
            cltv_promoters = 4462
            cltv_avg = 4149
        
        # Taux churn par catégorie NPS (données réelles)
        if 'Is_Churned' in df.columns:
            churn_detractors = df[df['NPS_Category'] == 'Detractors']['Is_Churned'].mean()
            churn_passives = df[df['NPS_Category'] == 'Passives']['Is_Churned'].mean()
            churn_promoters = df[df['NPS_Category'] == 'Promoters']['Is_Churned'].mean()
        else:
            # Valeurs dataset réel
            churn_detractors = 1.00  # 100%
            churn_passives = 0.161   # 16.1%
            churn_promoters = 0.00   # 0%
        
    except Exception as e:
        st.error(f"❌ Erreur chargement données: {str(e)}")
        return
    
    # ========================================
    # SECTION 1: SCÉNARIOS PRÉDÉFINIS
    # ========================================
    
    st.markdown("### 🎯 Scénarios Rapides")
    
    col_sc1, col_sc2, col_sc3, col_sc4 = st.columns(4)
    
    with col_sc1:
        if st.button("🚀 Conservateur", use_container_width=True, key='sc1'):
            st.session_state['det_conv'] = 15
            st.session_state['pas_conv'] = 5
            st.session_state['budget'] = 10
    
    with col_sc2:
        if st.button("💪 Ambitieux", use_container_width=True, key='sc2'):
            st.session_state['det_conv'] = 30
            st.session_state['pas_conv'] = 15
            st.session_state['budget'] = 25
    
    with col_sc3:
        if st.button("🎯 Optimal", use_container_width=True, key='sc3'):
            st.session_state['det_conv'] = 25
            st.session_state['pas_conv'] = 10
            st.session_state['budget'] = 15
    
    with col_sc4:
        if st.button("🔥 Agressif", use_container_width=True, key='sc4'):
            st.session_state['det_conv'] = 40
            st.session_state['pas_conv'] = 20
            st.session_state['budget'] = 40
    
    st.markdown("---")
    
    # ========================================
    # SECTION 2: INPUTS INTERACTIFS
    # ========================================
    
    st.markdown("### ⚙️ Paramètres Simulation")
    
    col_input1, col_input2, col_input3 = st.columns(3)
    
    with col_input1:
        det_conv_pct = st.slider(
            "📉 % Detractors → Passives",
            min_value=5,
            max_value=50,
            value=st.session_state.get('det_conv', 20),
            step=5,
            help="Objectif réaliste: 15-30% avec campagne ciblée",
            key='slider_det'
        )
    
    with col_input2:
        pas_conv_pct = st.slider(
            "📈 % Passives → Promoters",
            min_value=5,
            max_value=30,
            value=st.session_state.get('pas_conv', 10),
            step=5,
            help="Objectif réaliste: 8-15% avec programme fidélité",
            key='slider_pas'
        )
    
    with col_input3:
        budget = st.slider(
            "💵 Budget Campagne ($K)",
            min_value=5,
            max_value=100,
            value=st.session_state.get('budget', 15),
            step=5,
            help="Budget marketing + support + incentives",
            key='slider_budget'
        ) * 1000
    
    # Note explicative CLTV
    with st.expander("💡 Note Méthodologie", expanded=False):
        st.markdown(f"""
        **Source données:**
        - CLTV Detractors: ${cltv_detractors:,.0f} (moyenne réelle dataset)
        - CLTV Passives: ${cltv_passives:,.0f}
        - CLTV Promoters: ${cltv_promoters:,.0f}
        
        **Taux churn observés:**
        - Detractors: {churn_detractors*100:.1f}% (tous churnent)
        - Passives: {churn_passives*100:.1f}%
        - Promoters: {churn_promoters*100:.1f}% (aucun churn)
        
        **Calcul impact:**
        - Detractors convertis qui ne churnent plus: 100% - 16.1% = **83.9% sauvés**
        - Passives convertis qui ne churnent plus: 16.1% - 0% = **16.1% sauvés**
        """)
    
    st.markdown("---")
    
    # ========================================
    # SECTION 3: CALCULS SIMULATION
    # ========================================
    
    # Conversions
    det_converted = int(detractors_count * (det_conv_pct / 100))
    pas_converted = int(passives_count * (pas_conv_pct / 100))
    
    # Nouvelle distribution NPS
    new_detractors = detractors_count - det_converted
    new_passives = passives_count + det_converted - pas_converted
    new_promoters = promoters_count + pas_converted
    
    # Nouveau NPS
    new_detractors_pct = (new_detractors / total_clients) * 100
    new_promoters_pct = (new_promoters / total_clients) * 100
    nps_new = new_promoters_pct - new_detractors_pct
    
    # Churn évité (logique précise)
    # Detractors → Passives: passent de 100% churn à 16.1% churn
    churn_avoided_det = det_converted * (churn_detractors - churn_passives)
    
    # Passives → Promoters: passent de 16.1% churn à 0% churn
    churn_avoided_pas = pas_converted * (churn_passives - churn_promoters)
    
    total_churn_avoided = int(churn_avoided_det + churn_avoided_pas)
    
    # Revenue sauvé
    revenue_saved = total_churn_avoided * cltv_avg
    
    # ROI
    if budget > 0:
        gain_net = revenue_saved - budget
        roi = (gain_net / budget) * 100
        break_even_clients = int(budget / cltv_avg)
    else:
        gain_net = revenue_saved
        roi = 0
        break_even_clients = 0
    
    # ========================================
    # SECTION 4: RÉSULTATS
    # ========================================
    
    st.markdown("### 📊 Résultats Simulation")
    
    res1, res2, res3, res4 = st.columns(4)
    
    with res1:
        nps_delta = nps_new - nps_current
        nps_delta_color = "#27ae60" if nps_delta > 0 else "#e74c3c"
        
        st.markdown(f"""
        <div class="metric-simulator">
            <div class="metric-label-sim">NPS Nouveau</div>
            <div class="metric-value-big">{nps_new:.1f}</div>
            <div class="metric-delta-sim" style="color: {nps_delta_color};">
                {'+' if nps_delta > 0 else ''}{nps_delta:.1f} pts ({'+' if nps_delta > 0 else ''}{(nps_delta/nps_current*100):.0f}%)
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with res2:
        st.markdown(f"""
        <div class="metric-simulator">
            <div class="metric-label-sim">Clients Sauvés</div>
            <div class="metric-value-big">{total_churn_avoided:,}</div>
            <div class="metric-delta-sim" style="color: #3498db;">
                {det_converted + pas_converted:,} conversions
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with res3:
        st.markdown(f"""
        <div class="metric-simulator">
            <div class="metric-label-sim">Revenue Sauvé</div>
            <div class="metric-value-big">${revenue_saved/1000000:.2f}M</div>
            <div class="metric-delta-sim" style="color: #27ae60;">
                ${revenue_saved:,.0f}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with res4:
        roi_color = "#27ae60" if roi > 100 else "#f39c12" if roi > 0 else "#e74c3c"
        roi_status = "Excellent" if roi > 200 else "Bon" if roi > 100 else "Acceptable" if roi > 0 else "Négatif"
        
        st.markdown(f"""
        <div class="metric-simulator">
            <div class="metric-label-sim">ROI</div>
            <div class="metric-value-big" style="background: linear-gradient(135deg, {roi_color}, {roi_color}); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{roi:.0f}%</div>
            <div class="metric-delta-sim" style="color: {roi_color};">
                {roi_status} ({roi/100:.1f}x)
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Métriques secondaires
    st.markdown("<br>", unsafe_allow_html=True)
    
    sec1, sec2, sec3, sec4 = st.columns(4)
    
    sec1.metric(
        "Break-even",
        f"{break_even_clients} clients",
        delta=f"Atteint {break_even_clients/total_churn_avoided*100:.0f}% scénario" if total_churn_avoided > 0 else "N/A"
    )
    
    sec2.metric(
        "Gain Net",
        f"${gain_net:,.0f}",
        delta=f"+{(gain_net/revenue_saved*100):.0f}% du brut" if revenue_saved > 0 else "N/A"
    )
    
    sec3.metric(
        "Coût/Client Sauvé",
        f"${budget/total_churn_avoided:,.0f}" if total_churn_avoided > 0 else "N/A",
        delta=f"CLTV: ${cltv_avg:,.0f}"
    )
    
    sec4.metric(
        "Payback Period",
        f"{int(12 * budget / (revenue_saved/12)) if revenue_saved > 0 else 0} mois",
        delta="Estimation"
    )
    
    st.markdown("---")
    
    # ========================================
    # SECTION 5: GRAPHIQUE SENSIBILITÉ
    # ========================================
    
    st.markdown("### 📈 Analyse de Sensibilité")
    
    # Créer scénarios multiples
    scenarios_det = np.arange(5, 51, 5)  # 5% à 50%
    scenarios_pas = np.arange(5, 31, 5)  # 5% à 30%
    
    # Calcul ROI pour chaque combinaison
    roi_matrix = []
    revenue_matrix = []
    
    for det_pct in scenarios_det:
        roi_row = []
        rev_row = []
        for pas_pct in scenarios_pas:
            # Calculs
            det_conv = int(detractors_count * (det_pct / 100))
            pas_conv = int(passives_count * (pas_pct / 100))
            
            churn_det = det_conv * (churn_detractors - churn_passives)
            churn_pas = pas_conv * (churn_passives - churn_promoters)
            total_saved = int(churn_det + churn_pas)
            
            revenue = total_saved * cltv_avg
            roi_val = ((revenue - budget) / budget * 100) if budget > 0 else 0
            
            roi_row.append(roi_val)
            rev_row.append(revenue)
        
        roi_matrix.append(roi_row)
        revenue_matrix.append(rev_row)
    
    # Créer figure avec 2 graphiques
    fig_sens = make_subplots(
        rows=1, cols=2,
        subplot_titles=(
            f'<b>ROI vs Taux Conversion (Budget ${budget/1000:.0f}K)</b>',
            '<b>Revenue Sauvé vs Scénarios</b>'
        ),
        column_widths=[0.5, 0.5],
        horizontal_spacing=0.12
    )
    
    # Graph 1: Lignes ROI pour différents % Passives
    for i, pas_pct in enumerate([5, 10, 15, 20, 25]):
        if i < len(scenarios_pas):
            idx = list(scenarios_pas).index(pas_pct)
            roi_values = [row[idx] for row in roi_matrix]
            
            fig_sens.add_trace(
                go.Scatter(
                    x=scenarios_det,
                    y=roi_values,
                    mode='lines+markers',
                    name=f'Passives {pas_pct}%',
                    line=dict(width=2),
                    marker=dict(size=6),
                    hovertemplate=f'<b>Passives {pas_pct}%</b><br>Detractors: %{{x}}%<br>ROI: %{{y:.0f}}%<extra></extra>'
                ),
                row=1, col=1
            )
    
    # Ligne scénario actuel
    current_roi_line = [roi_matrix[list(scenarios_det).index(det_conv_pct // 5 * 5)][i] 
                        for i in range(len(scenarios_pas))]
    
    fig_sens.add_trace(
        go.Scatter(
            x=scenarios_det,
            y=[roi] * len(scenarios_det),
            mode='lines',
            name='Scénario actuel',
            line=dict(color='yellow', width=3, dash='dot'),
            showlegend=True,
            hovertemplate='<b>Votre scénario</b><br>ROI: %{y:.0f}%<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Graph 2: Heatmap Revenue
    fig_sens.add_trace(
        go.Heatmap(
            z=revenue_matrix,
            x=scenarios_pas,
            y=scenarios_det,
            colorscale='Viridis',
            colorbar=dict(title="Revenue ($)", x=1.15),
            hovertemplate='Detractors: %{y}%<br>Passives: %{x}%<br>Revenue: $%{z:,.0f}<extra></extra>'
        ),
        row=1, col=2
    )
    
    # Layout
    fig_sens.update_layout(
        height=500,
        template='plotly_dark',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.25)
    )
    
    fig_sens.update_xaxes(title_text="<b>% Detractors Convertis</b>", row=1, col=1)
    fig_sens.update_yaxes(title_text="<b>ROI (%)</b>", row=1, col=1)
    fig_sens.update_xaxes(title_text="<b>% Passives Convertis</b>", row=1, col=2)
    fig_sens.update_yaxes(title_text="<b>% Detractors Convertis</b>", row=1, col=2)
    
    st.plotly_chart(fig_sens, use_container_width=True)
    
    # ========================================
    # SECTION 6: RECOMMANDATIONS AUTO
    # ========================================
    
    st.markdown("### 💡 Recommandations")
    
    # Trouver scénario optimal (max ROI)
    max_roi = max(max(row) for row in roi_matrix)
    max_roi_idx = [(i, j) for i, row in enumerate(roi_matrix) for j, val in enumerate(row) if val == max_roi][0]
    optimal_det = scenarios_det[max_roi_idx[0]]
    optimal_pas = scenarios_pas[max_roi_idx[1]]
    
    # Analyser scénario actuel
    if roi > 200:
        assessment = "🎉 EXCELLENT"
        color = "#27ae60"
        advice = "Votre scénario est très rentable. Recommandation: Exécuter immédiatement."
    elif roi > 100:
        assessment = "👍 BON"
        color = "#3498db"
        advice = "Scénario rentable. Vous pouvez améliorer en ciblant plus de conversions."
    elif roi > 0:
        assessment = "⚠️ ACCEPTABLE"
        color = "#f39c12"
        advice = "ROI positif mais faible. Augmentez les conversions ou réduisez le budget."
    else:
        assessment = "🚨 NÉGATIF"
        color = "#e74c3c"
        advice = "Budget trop élevé pour ce taux de conversion. Ajustez les paramètres."
    
    col_rec1, col_rec2 = st.columns(2)
    
    with col_rec1:
        st.markdown(f"""
        <div style="background: {color}22; padding: 20px; border-radius: 10px; border-left: 4px solid {color};">
            <h4 style="color: {color}; margin-top: 0;">Assessment Scénario Actuel</h4>
            <p style="font-size: 28px; font-weight: 800; color: {color}; margin: 10px 0;">
                {assessment}
            </p>
            <p style="color: #ecf0f1; margin: 0;">
                {advice}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_rec2:
        st.markdown(f"""
        <div style="background: rgba(102,126,234,0.1); padding: 20px; border-radius: 10px; border-left: 4px solid #667eea;">
            <h4 style="color: #667eea; margin-top: 0;">🎯 Scénario Optimal</h4>
            <p style="color: #ecf0f1; margin: 5px 0;">
                <strong>Detractors:</strong> {optimal_det}% conversion<br>
                <strong>Passives:</strong> {optimal_pas}% conversion<br>
                <strong>ROI maximal:</strong> <span style="color: #27ae60; font-size: 20px; font-weight: 700;">{max_roi:.0f}%</span>
            </p>
            <p style="color: #95a5a6; font-size: 13px; margin: 10px 0 0 0;">
                💡 Cliquez "🎯 Optimal" ci-dessus pour appliquer
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Actions concrètes
    st.markdown("#### 🚀 Plan d'Action Recommandé")
    
    if det_conv_pct >= 20:
        action_det = f"""
        **Phase 1 - Detractors (Priorité HAUTE)**
        - Campagne email satisfaction J+30 ({det_converted} clients ciblés)
        - Tech Support gratuit 3 mois (top {det_converted//2} CLTV)
        - Call proactif CSM pour résoudre irritants
        - Budget alloué: ${budget * 0.6:,.0f} (60%)
        """
    else:
        action_det = f"""
        **Phase 1 - Detractors (Effort Modéré)**
        - Email rétention personnalisé ({det_converted} clients)
        - Offre upgrade ciblée
        - Budget alloué: ${budget * 0.4:,.0f} (40%)
        """
    
    if pas_conv_pct >= 15:
        action_pas = f"""
        **Phase 2 - Passives (Priorité HAUTE)**
        - Programme fidélité exclusif ({pas_converted} clients)
        - Incentives référencement (bonus $50/parrainage)
        - Offres bundles premium -15%
        - Budget alloué: ${budget * 0.4:,.0f} (40%)
        """
    else:
        action_pas = f"""
        **Phase 2 - Passives (Effort Standard)**
        - Email upsell services additionnels
        - Offres contrats longs (-10%)
        - Budget alloué: ${budget * 0.3:,.0f} (30%)
        """
    
    col_act1, col_act2 = st.columns(2)
    
    with col_act1:
        st.markdown(f"""
        <div style="background: rgba(231,76,60,0.1); padding: 15px; border-radius: 8px;">
            {action_det}
        </div>
        """, unsafe_allow_html=True)
    
    with col_act2:
        st.markdown(f"""
        <div style="background: rgba(243,156,18,0.1); padding: 15px; border-radius: 8px;">
            {action_pas}
        </div>
        """, unsafe_allow_html=True)
    
    # Timeline
    st.markdown(f"""
    **Timeline Exécution:**
    - **J+0 à J+7:** Setup campagnes + segmentation clients
    - **J+7 à J+30:** Lancement Phase 1 (Detractors)
    - **J+30 à J+60:** Lancement Phase 2 (Passives)
    - **J+60 à J+90:** Mesure résultats + ajustements
    
    **KPIs Suivi:**
    - Taux conversion Detractors → Passives (Cible: {det_conv_pct}%)
    - Taux conversion Passives → Promoters (Cible: {pas_conv_pct}%)
    - NPS hebdomadaire (Objectif: {nps_new:.1f})
    - Churn rate mensuel (Réduction: {total_churn_avoided} clients)
    - ROI campagne (Target: {roi:.0f}%)
    """)
    
    # ========================================
    # EXPORT DONNÉES
    # ========================================
    
    with st.expander("📥 Exporter Résultats Simulation", expanded=False):
        
        # Créer DataFrame résumé
        summary_data = {
            'Métrique': [
                'NPS Actuel',
                'NPS Nouveau',
                'Delta NPS',
                'Detractors Convertis',
                'Passives Convertis',
                'Clients Sauvés',
                'Revenue Sauvé',
                'Budget Campagne',
                'Gain Net',
                'ROI',
                'Break-even Clients'
            ],
            'Valeur': [
                f"{nps_current:.1f}",
                f"{nps_new:.1f}",
                f"+{nps_delta:.1f}",
                f"{det_converted:,}",
                f"{pas_converted:,}",
                f"{total_churn_avoided:,}",
                f"${revenue_saved:,.0f}",
                f"${budget:,.0f}",
                f"${gain_net:,.0f}",
                f"{roi:.0f}%",
                f"{break_even_clients}"
            ]
        }
        
        df_summary = pd.DataFrame(summary_data)
        
        st.dataframe(df_summary, use_container_width=True, hide_index=True)
        
        # Bouton download CSV
        csv = df_summary.to_csv(index=False)
        st.download_button(
            label="⬇️ Télécharger Résumé CSV",
            data=csv,
            file_name=f"simulation_nps_{det_conv_pct}det_{pas_conv_pct}pas.csv",
            mime="text/csv",
            use_container_width=True
        )


# ========================================
# FONCTION HELPER - INTÉGRATION
# ========================================

def integrate_simulator_in_satisfaction_tab(df: pd.DataFrame):
    """
    Fonction wrapper pour intégrer le simulateur dans l'onglet Satisfaction
    
    Usage dans render_satisfaction_tab():
    
    ```python
    # Après la section Sunburst, ajouter:
    st.markdown("---")
    integrate_simulator_in_satisfaction_tab(df_filtered)
    ```
    """
    
    # Vérifier colonnes requises
    required_cols = ['NPS_Category']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        st.warning(f"⚠️ Colonnes manquantes pour simulateur: {', '.join(missing_cols)}")
        st.info("💡 Le simulateur nécessite la colonne 'NPS_Category' (Detractors/Passives/Promoters)")
        return
    
    # Créer NPS_Category si nécessaire
    if 'NPS_Category' not in df.columns and 'Satisfaction Score' in df.columns:
        df['NPS_Category'] = df['Satisfaction Score'].apply(
            lambda x: 'Promoters' if x >= 4 else ('Passives' if x == 3 else 'Detractors')
        )
    
    # Créer Is_Churned si nécessaire
    if 'Is_Churned' not in df.columns:
        if 'Churn Label' in df.columns:
            df['Is_Churned'] = (df['Churn Label'] == 'Yes').astype(int)
        elif 'Churn' in df.columns:
            df['Is_Churned'] = (df['Churn'] == 'Yes').astype(int)
    
    # Lancer simulateur
    render_nps_simulator(df)


# ========================================
# EXEMPLE UTILISATION STANDALONE
# ========================================

if __name__ == "__main__":
    """
    Test du simulateur en mode standalone
    """
    
    # Simuler données test
    np.random.seed(42)
    n = 7043
    
    df_test = pd.DataFrame({
        'customerID': range(n),
        'Satisfaction Score': np.random.choice([1, 2, 3, 4, 5], n, p=[0.13, 0.07, 0.38, 0.25, 0.17]),
        'CLTV': np.random.normal(4149, 500, n),
        'Churn Label': np.random.choice(['Yes', 'No'], n, p=[0.265, 0.735])
    })
    
    # Créer NPS_Category
    df_test['NPS_Category'] = df_test['Satisfaction Score'].apply(
        lambda x: 'Promoters' if x >= 4 else ('Passives' if x == 3 else 'Detractors')
    )
    
    df_test['Is_Churned'] = (df_test['Churn Label'] == 'Yes').astype(int)
    
    # Lancer simulateur
    st.set_page_config(page_title="Test Simulateur NPS", layout="wide")
    st.title("🧪 Test Simulateur NPS")
    
    render_nps_simulator(df_test)
