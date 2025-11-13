import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap

# ==========================================
# Page Configuration & Styling
# ==========================================
st.set_page_config(
    page_title="Cat Cafe MDP Optimizer",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Beautiful Dark Theme CSS with smooth transitions
st.markdown("""
<style>
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    body {
        background-color: #0f1419;
        color: #e0e0e0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        border-bottom: 2px solid #2a3f5f;
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 15px;
        padding: 12px 25px;
        color: #8892aa;
        background-color: transparent;
        border-bottom: 3px solid transparent;
        transition: all 0.4s ease;
    }
    
    .stTabs [data-baseweb="tab-list"] button:hover {
        color: #a8b8d8;
        transition: color 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #7ec8c8;
        border-bottom: 3px solid #7ec8c8;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .param-card {
        background: linear-gradient(135deg, #1a2332 0%, #0f1419 100%);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #2a3f5f;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }
    
    .param-card:hover {
        border-color: #3a5f7f;
        box-shadow: 0 6px 20px rgba(126,200,200,0.1);
        transition: all 0.3s ease;
    }
    
    .info-box {
        background: linear-gradient(135deg, #1a2a2a 0%, #0f1419 100%);
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #7ec8c8;
        color: #d0d8e0;
        transition: all 0.3s ease;
    }
    
    .success-box {
        background: linear-gradient(135deg, #1a2a1a 0%, #0f1419 100%);
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #7ec8c8;
        color: #d0d8e0;
        transition: all 0.3s ease;
    }
    
    .story-box {
        background: linear-gradient(135deg, #1a2a2a 0%, #0f1419 100%);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #2a3f5f;
        color: #d0d8e0;
        font-size: 15px;
        line-height: 1.8;
        transition: all 0.3s ease;
    }
    
    .math-box {
        background: linear-gradient(135deg, #1a2a3a 0%, #0f1419 100%);
        padding: 18px;
        border-radius: 10px;
        border-left: 4px solid #5fa8e8;
        color: #d0d8e0;
        font-size: 13px;
        line-height: 1.7;
        font-family: 'Courier New', monospace;
        margin: 12px 0;
        transition: all 0.3s ease;
    }
    
    .math-box:hover {
        border-left-color: #7ec8c8;
        box-shadow: 0 4px 12px rgba(126,200,200,0.1);
        transition: all 0.3s ease;
    }
    
    .cat-visual {
        font-size: 3em;
        text-align: center;
        animation: float 3s ease-in-out infinite;
        margin: 15px 0;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #7ec8c8 0%, #5fa8e8 100%);
        color: #0f1419;
        border: none;
        padding: 12px 30px;
        border-radius: 10px;
        font-weight: 600;
        font-size: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(126,200,200,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(126,200,200,0.3);
        transition: all 0.3s ease;
    }
    
    h1, h2, h3 {
        color: #d0d8e8;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    h1 { font-size: 32px; }
    h3 { font-size: 20px; }
    
    .metric-box {
        background: linear-gradient(135deg, #1a2332 0%, #0f1419 100%);
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .metric-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(126,200,200,0.1);
    }
    
    .reward-term {
        background: linear-gradient(135deg, #1a2a2a 0%, #0f1419 100%);
        padding: 15px;
        border-radius: 10px;
        border-left: 3px solid #7aae98;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    
    .reward-term:hover {
        border-left-color: #7ec8c8;
        transform: translateX(5px);
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# MDP Core Functions
# ==========================================

PRICE_LEVELS = ["Low ($3)", "Medium ($8)", "High ($15)"]
STAFF_LEVELS = ["1 Person", "2 People", "3 People", "4 People"]
ACTIONS = ["Raise Price", "Lower Price", "Hire Staff", "Fire Staff", "Maintain"]

NUM_PRICES = len(PRICE_LEVELS)
NUM_STAFF = len(STAFF_LEVELS)
NUM_ACTIONS = len(ACTIONS)

def reward(p, s, params, penalty=False):
    """Calculate daily profit for state (price, staff)"""
    price_amounts = [3, 8, 15]
    price = price_amounts[p] * params['multiplier']
    
    # Demand factors
    sensitivity = 1 - params['price_sens'] * (p-1)
    staff_bonus = 1 + params['labor_effect'] * (s)
    
    # Customer arrivals
    total_customers = int(params['cust_rate'] * sensitivity * staff_bonus)
    revenue = total_customers * price
    
    # Costs
    labor = (s + 1) * params['staff_cost'] * 8
    profit = revenue - labor
    
    if penalty:
        profit -= params['penalty']
    
    return profit

def next_state(p, s, action):
    """Transition to next state given action"""
    p_new, s_new = p, s
    
    if action == 0 and p < 2:
        p_new = p + 1
    elif action == 1 and p > 0:
        p_new = p - 1
    elif action == 2 and s < 3:
        s_new = s + 1
    elif action == 3 and s > 0:
        s_new = s - 1
    
    return p_new, s_new

def value_iteration(params, discount, max_iter, convergence_threshold=1e-3):
    """Solve MDP using Value Iteration"""
    v = np.zeros((NUM_PRICES, NUM_STAFF))
    policy = np.zeros((NUM_PRICES, NUM_STAFF), dtype=int)
    deltas = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for iteration in range(max_iter):
        delta = 0
        v_new = v.copy()
        
        for p in range(NUM_PRICES):
            for s in range(NUM_STAFF):
                q_values = []
                
                for action in range(NUM_ACTIONS):
                    p_next, s_next = next_state(p, s, action)
                    r = reward(p_next, s_next, params, penalty=(action != 4))
                    
                    expected_future = 0.9 * v[p_next, s_next] + 0.1 * np.mean(v)
                    q_value = r + discount * expected_future
                    
                    q_values.append(q_value)
                
                best_value = max(q_values)
                best_action = int(np.argmax(q_values))
                
                v_new[p, s] = best_value
                policy[p, s] = best_action
                
                delta = max(delta, abs(best_value - v[p, s]))
        
        v = v_new
        deltas.append(delta)
        
        progress = min((iteration + 1) / max_iter, 1.0)
        progress_bar.progress(progress)
        status_text.text(f"Iteration {iteration + 1}/{max_iter} | Delta: {delta:.8f}")
        
        if delta < convergence_threshold:
            status_text.text(f"Converged in {iteration + 1} iterations | Final delta: {delta:.8f}")
            break
    
    progress_bar.empty()
    status_text.empty()
    
    return v, policy, deltas, iteration + 1

def create_heatmap(values, title="Value Function Heatmap"):
    """Create beautiful soft-color heatmap"""
    fig, ax = plt.subplots(figsize=(11, 6))
    
    colors_soft = [
        '#1a3a4a', '#2a5a7a', '#4a7fa8', '#7a9fc8', '#9ab8d8',
        '#b8c8d8', '#d8b8a8', '#d89878', '#c86858', '#b84848'
    ]
    cmap = LinearSegmentedColormap.from_list('cafe_soft', colors_soft, N=256)
    
    vmin, vmax = values.min(), values.max()
    
    im = ax.imshow(values, cmap=cmap, aspect='auto', vmin=vmin, vmax=vmax)
    
    ax.set_xticks(np.arange(NUM_STAFF))
    ax.set_yticks(np.arange(NUM_PRICES))
    ax.set_xticklabels(STAFF_LEVELS, fontsize=12, color='#a8b8d8', fontweight=500)
    ax.set_yticklabels(PRICE_LEVELS, fontsize=12, color='#a8b8d8', fontweight=500)
    
    ax.set_xticks(np.arange(NUM_STAFF) - 0.5, minor=True)
    ax.set_yticks(np.arange(NUM_PRICES) - 0.5, minor=True)
    ax.grid(which='minor', color='#2a4a6a', linestyle='-', linewidth=2.5, alpha=0.6)
    
    for i in range(NUM_PRICES):
        for j in range(NUM_STAFF):
            value = values[i, j]
            
            normalized = (value - vmin) / (vmax - vmin) if vmax > vmin else 0.5
            text_color = '#0f1419' if normalized > 0.4 else '#d8d8e8'
            
            rect = mpatches.Rectangle((j-0.45, i-0.45), 0.9, 0.9, 
                                     linewidth=0.5, edgecolor='#3a5a7a', 
                                     facecolor='none', alpha=0.3)
            ax.add_patch(rect)
            
            ax.text(j, i, f'${value:.0f}', ha='center', va='center',
                   color=text_color, fontsize=13, fontweight='600', 
                   bbox=dict(boxstyle='round,pad=0.4', facecolor='none', edgecolor='none'))
    
    ax.set_xlabel("Staff Level", fontsize=13, color='#a8b8d8', fontweight=600, labelpad=12)
    ax.set_ylabel("Price Level", fontsize=13, color='#a8b8d8', fontweight=600, labelpad=12)
    ax.set_title(title, fontsize=16, color='#d0d8e8', pad=20, fontweight=600)
    
    cbar = plt.colorbar(im, ax=ax, pad=0.02)
    cbar.set_label('Expected Profit ($)', color='#a8b8d8', fontsize=12, fontweight=500, labelpad=15)
    cbar.ax.tick_params(colors='#a8b8d8', labelsize=11)
    cbar.outline.set_edgecolor('#2a4a6a')
    cbar.outline.set_linewidth(1.5)
    
    fig.patch.set_facecolor('#0f1419')
    ax.set_facecolor('#1a2a3a')
    ax.spines['bottom'].set_color('#2a4a6a')
    ax.spines['left'].set_color('#2a4a6a')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(colors='#a8b8d8', labelsize=11)
    
    plt.tight_layout()
    return fig

def create_policy_table(policy):
    """Create beautiful soft-colored policy table with visible text"""
    fig, ax = plt.subplots(figsize=(12, 5.5))
    ax.axis('off')
    
    action_colors = {
        0: '#7a9fa8',
        1: '#8a9f98',
        2: '#7aae98',
        3: '#c89888',
        4: '#9a7ab8'
    }
    
    action_names = {
        0: "Raise Price",
        1: "Lower Price",
        2: "Hire Staff",
        3: "Fire Staff",
        4: "Maintain"
    }
    
    table_data = []
    
    for i in range(NUM_PRICES):
        row_data = []
        for j in range(NUM_STAFF):
            action_idx = int(policy[i, j])
            action_name = action_names[action_idx]
            row_data.append(action_name)
        table_data.append(row_data)
    
    table = ax.table(cellText=table_data,
                    rowLabels=PRICE_LEVELS,
                    colLabels=STAFF_LEVELS,
                    cellLoc='center',
                    loc='center',
                    colWidths=[0.22]*NUM_STAFF)
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2.8)
    
    for i in range(NUM_PRICES):
        for j in range(NUM_STAFF):
            cell = table[(i+1, j)]
            action_idx = int(policy[i, j])
            cell.set_facecolor(action_colors[action_idx])
            cell.set_text_props(weight='600', color='#f0f0f0', fontsize=11)
            cell.set_linewidth(1.5)
            cell.set_edgecolor('#1a2a3a')
    
    for j in range(NUM_STAFF):
        cell = table[(0, j)]
        cell.set_facecolor('#1a2a3a')
        cell.set_text_props(weight='600', color='#a8b8d8', fontsize=11)
        cell.set_linewidth(1.5)
        cell.set_edgecolor('#2a4a6a')
    
    for i in range(NUM_PRICES):
        cell = table[(i+1, -1)]
        cell.set_facecolor('#1a2a3a')
        cell.set_text_props(weight='600', color='#a8b8d8', fontsize=11)
        cell.set_linewidth(1.5)
        cell.set_edgecolor('#2a4a6a')
    
    fig.patch.set_facecolor('#0f1419')
    plt.suptitle("Optimal Policy: Best Action per State", fontsize=16, color='#d0d8e8', 
             y=0.98, fontweight=600)
    
    return fig

# ==========================================
# Main App
# ==========================================

st.markdown("""
<div style='text-align: center; margin-bottom: 20px; margin-top: -30px;'>
    <h1 style='color: #7ec8c8; font-size: 36px; font-weight: 600; margin-bottom: 8px;'>Whisker's Cafe</h1>
    <p style='color: #8892aa; font-size: 16px; margin: 0; font-style: italic;'>Optimize your adorable cat cafe using Markov Decision Processes</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; margin-bottom: 25px;'>
    <div style='font-size: 2.5em; animation: float 3s ease-in-out infinite;'>🐱</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='story-box'>
    <p style='font-size: 16px; line-height: 1.9; margin: 0;'>
        Welcome to <b>Whisker's Cafe</b> — a cozy corner where caffeine lovers meet curious felines! 
        You've just inherited this charming cat cafe, and business is brewing. But how do you keep both 
        your customers and your cats happy while maximizing profit?
    </p>
    <p style='font-size: 16px; line-height: 1.9; margin-top: 15px; margin-bottom: 0;'>
        Should you charge premium prices and attract quality customers, or offer budget-friendly coffee 
        to maximize volume? Do you hire more staff to handle the rush, or keep costs low with a skeleton crew? 
        <b>The answer lies in Markov Decision Processes</b> — a mathematical framework for finding optimal strategies 
        under uncertainty.
    </p>
</div>
""", unsafe_allow_html=True)

st.write("")

tab1, tab2, tab3 = st.tabs(["Configure & Solve", "Cafe Simulation", "Learn & Explore"])

# ==========================================
# TAB 1: MDP SOLVER
# ==========================================
with tab1:
    col_left, col_right = st.columns([1, 3], gap='large')
    
    with col_left:
        st.markdown("""
        <div class='param-card'>
            <h3 style='margin-top: 0; color: #d0d8e8;'>Cafe Optimization Engine</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        
        st.write("**Discount Factor (γ): {:.2f}**".format(st.session_state.get('gamma', 0.95)))
        st.write("<span style='color: #8892aa; font-size: 13px;'>How much you value future profit</span>", unsafe_allow_html=True)
        gamma = st.slider("Discount Factor", 0.50, 0.99, st.session_state.get('gamma', 0.95), 
                         step=0.01, key='gamma_slider', label_visibility='collapsed')
        
        st.write("")
        st.write("**Max Iterations: {}**".format(st.session_state.get('max_iter', 200)))
        max_iter = st.slider("Max Iterations", 25, 500, st.session_state.get('max_iter', 200),
                            step=10, key='iter_slider', label_visibility='collapsed')
        
        st.write("")
        st.write("**Customer Arrival Rate: {} per day**".format(st.session_state.get('cust_rate', 25)))
        cust_rate = st.slider("Customer Arrival Rate", 5, 50, st.session_state.get('cust_rate', 25),
                             step=1, key='cust_slider', label_visibility='collapsed')
        
        st.write("")
        st.write("**Menu Price Multiplier: {:.1f}x**".format(st.session_state.get('multiplier', 1.0)))
        multiplier = st.slider("Menu Price Multiplier", 0.5, 2.0, st.session_state.get('multiplier', 1.0),
                              step=0.1, key='mult_slider', label_visibility='collapsed')
        
        st.write("")
        st.write("**Staff Cost: ${:.0f} per hour**".format(st.session_state.get('staff_cost', 15)))
        staff_cost = st.slider("Staff Cost ($/hr)", 10, 40, st.session_state.get('staff_cost', 15),
                              step=1, key='cost_slider', label_visibility='collapsed')
        st.write("")
        st.write("**Price Sensitivity (a): {:.2f}**".format(st.session_state.get('price_sens', 0.13)))
        price_sens = st.slider("Price Sensitivity (a)", 0.0, 1.0, st.session_state.get('price_sens', 0.13),
                            step=0.01, key='price_sens_slider', label_visibility='collapsed')

        st.write("")
        st.write("**Alpha (α): {:.2f}**".format(st.session_state.get('alpha', 0.08)))
        alpha = st.slider("Alpha (α)", 0.0, 0.5, st.session_state.get('alpha', 0.08),
                        step=0.01, key='alpha_slider', label_visibility='collapsed')

        st.write("")
        st.write("**Lambda (λ): {:.2f}**".format(st.session_state.get('lambda', 0.9)))
        _lambda = st.slider("Lambda (λ)", 0.0, 1.0, st.session_state.get('lambda', 0.9),
                            step=0.01, key='lambda_slider', label_visibility='collapsed')

        
        st.write("")
        
        if st.button("Solve Optimal Policy", use_container_width=True, key='solve_btn'):
            st.session_state['solve'] = True
            st.session_state['gamma'] = gamma
            st.session_state['max_iter'] = max_iter
            st.session_state['cust_rate'] = cust_rate
            st.session_state['multiplier'] = multiplier
            st.session_state['staff_cost'] = staff_cost
            st.session_state['price_sens'] = price_sens
            st.session_state['alpha'] = alpha
            st.session_state['lambda'] = _lambda
                
        if st.session_state.get('solve', False) and st.session_state.get('iterations'):
            iters = st.session_state.get('iterations', 0)
            deltas = st.session_state.get('deltas', [])
            final_delta = deltas[-1] if deltas else 0
            best_val = st.session_state.get('values', np.zeros((3,4))).max() if st.session_state.get('values') is not None else 0
            
            st.markdown(f"""
            <div class='info-box' style='margin-top: 25px;'>
                <p style='color: #7ec8c8; font-weight: 600; margin: 8px 0;'>Converged in {iters} iterations</p>
                <p style='color: #8892aa; margin: 8px 0; font-size: 13px;'>Final delta: {final_delta:.8f}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class='success-box' style='margin-top: 15px;'>
                <p style='color: #8892aa; margin: 5px 0; font-size: 13px;'>Best Expected Daily Profit</p>
                <p style='color: #7ec8c8; font-size: 32px; font-weight: 600; margin: 12px 0;'>${best_val:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col_right:
        if st.session_state.get('solve', False):
            params = {
                    'cust_rate': cust_rate,
                    'price_sens': price_sens,
                    'labor_effect': alpha,
                    'staff_cost': staff_cost,
                    'multiplier': multiplier,
                    'penalty': 5
                }

            
            with st.spinner('Solving MDP...'):
                values, policy, deltas, iterations = value_iteration(params, gamma, max_iter)
            
            st.session_state['values'] = values
            st.session_state['policy'] = policy
            st.session_state['deltas'] = deltas
            st.session_state['iterations'] = iterations
            
            st.subheader("Value Function Heatmap")
            st.write("<span style='color: #8892aa; font-size: 13px;'>Expected profit for each price/staff combination</span>", 
                    unsafe_allow_html=True)
            fig_heat = create_heatmap(values)
            st.pyplot(fig_heat, use_container_width=True)
            
            st.subheader("Optimal Policy")
            st.write("<span style='color: #8892aa; font-size: 13px;'>Best action for each state</span>", 
                    unsafe_allow_html=True)
            fig_policy = create_policy_table(policy)
            st.pyplot(fig_policy, use_container_width=True)
        else:
            st.markdown("""
            <div class='info-box'>
                <p style='color: #7ec8c8; font-weight: 600;'>Ready to optimize?</p>
                <p style='color: #8892aa;'>Configure the parameters on the left and click <b>'Solve Optimal Policy'</b> to discover the best cafe strategy!</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style='text-align: center; margin-top: 40px;'>
                <div style='font-size: 4em; animation: float 3s ease-in-out infinite;'>😺</div>
                <p style='color: #8892aa; margin-top: 15px;'><i>Your cats are waiting for the perfect strategy...</i></p>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# TAB 2: CAFE SIMULATION
# ==========================================
with tab2:
    st.subheader("Play Cafe Simulator - Make Daily Decisions")
    
    st.markdown("""
    <div class='story-box'>
        <p style='margin: 0;'>
            Your turn to manage Whisker's Cafe! Every day, you make strategic decisions:
            adjust your menu prices, hire or fire staff, and watch how your choices affect profit and customer satisfaction.
            Can you discover the optimal strategy before the algorithm shows you?
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    if 'game_state' not in st.session_state:
        st.session_state['game_state'] = {
            'price_idx': 1,
            'staff_idx': 1,
            'day': 1,
            'total_profit': 0,
            'history': []
        }
    
    if st.session_state.get('values') is not None:
        game = st.session_state['game_state']
        values = st.session_state['values']
        policy = st.session_state['policy']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Day", game['day'])
        with col2:
            st.metric("Price", PRICE_LEVELS[game['price_idx']])
        with col3:
            st.metric("Staff", STAFF_LEVELS[game['staff_idx']])
        with col4:
            st.metric("Total Profit", f"${game['total_profit']:.2f}")
        
        st.divider()
        
        st.markdown("""
        <div style='text-align: center; margin: 15px 0;'>
            <div style='font-size: 2.2em; animation: float 3s ease-in-out infinite;'>🐱‍💼</div>
        </div>
        """, unsafe_allow_html=True)
        
        recommended_action_idx = int(policy[game['price_idx'], game['staff_idx']])
        
        col_recommend, col_spacer = st.columns([3, 1])
        with col_recommend:
            st.write(f"**AI Recommends:** {ACTIONS[recommended_action_idx]}")
        
        col_action, col_btn = st.columns([3, 1])
        
        with col_action:
            action_choice = st.selectbox(
                "Choose your action:", 
                ACTIONS, 
                index=int(recommended_action_idx),
                label_visibility='collapsed'
            )
        
        with col_btn:
            if st.button("Simulate Day", use_container_width=True):
                action_idx = int(ACTIONS.index(action_choice))
                new_p, new_s = next_state(game['price_idx'], game['staff_idx'], action_idx)
                prof = reward(new_p, new_s, {
                    'cust_rate': 25,
                    'price_sens': 0.9,
                    'labor_effect': 0.08,
                    'staff_cost': 15,
                    'multiplier': 1.0,
                    'penalty': 5
                }, penalty=(action_idx != 4))
                
                game['total_profit'] += prof
                game['history'].append({
                    'day': game['day'],
                    'action': action_choice,
                    'profit': prof,
                    'price': new_p,
                    'staff': new_s
                })
                
                game['price_idx'] = new_p
                game['staff_idx'] = new_s
                game['day'] += 1
                
                st.session_state['game_state'] = game
                st.rerun()
        
        if game['history']:
            st.divider()
            st.subheader("Day History")
            
            history_df = pd.DataFrame(game['history'])
            history_df['Price'] = history_df['price'].map(lambda x: PRICE_LEVELS[x])
            history_df['Staff'] = history_df['staff'].map(lambda x: STAFF_LEVELS[x])
            history_df['Profit'] = history_df['profit'].apply(lambda x: f"${x:.2f}")
            
            st.dataframe(history_df[['day', 'action', 'Price', 'Staff', 'Profit']], 
                        use_container_width=True, hide_index=True)
            
            if st.button("Restart Simulation", use_container_width=True):
                st.session_state['game_state'] = {
                    'price_idx': 1,
                    'staff_idx': 1,
                    'day': 1,
                    'total_profit': 0,
                    'history': []
                }
                st.rerun()
    else:
        st.markdown("""
        <div class='info-box'>
            <p style='color: #7ec8c8; font-weight: 600;'>Simulation Not Available</p>
            <p style='color: #8892aa;'>Please solve the MDP first in the <b>'Configure & Solve'</b> tab to unlock the cafe simulation!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='text-align: center; margin-top: 40px;'>
            <div style='font-size: 4em; animation: float 3s ease-in-out infinite;'>🐱</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# TAB 3: STRATEGY GUIDE WITH MATH
# ==========================================
with tab3:
    st.subheader("Understanding Your Cat Cafe Strategy")
    
    st.markdown("""
    ### The Strategic Challenge
    
    Running Whisker's Cafe is like solving a puzzle where every piece affects the others:
    """)
    
    st.markdown("""
    <div style='text-align: center; margin: 20px 0;'>
        <div style='font-size: 3em; animation: float 3s ease-in-out infinite;'>☕ 🐱 ☕</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### Mathematical Foundation
    
    The MDP solver uses dynamic programming to find optimal decisions. Here's the complete math:
    """)
    
    st.markdown("""
    <div class='math-box'>
    <b>State Space Definition:</b>
    s = (price_level, staff_level)
    price_level ∈ {0, 1, 2}  (Low, Medium, High)
    staff_level ∈ {0, 1, 2, 3}  (1, 2, 3, 4 people)
    Total states: |S| = 3 × 4 = 12
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='math-box'>
    <b>Action Space:</b>
    a ∈ {0, 1, 2, 3, 4}
    a₀: Raise Price
    a₁: Lower Price
    a₂: Hire Staff
    a₃: Fire Staff
    a₄: Maintain (no change)
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### Reward Function Breakdown
    
    The immediate reward R(s,a) captures the profit from daily operations:
    """)
    
    st.markdown("""
    <div class='reward-term'>
    <b>Revenue Component:</b><br>
    Revenue = N_customers × Price<br><br>
    Where:<br>
    N_customers = C₀ × f_price(p) × f_staff(w)<br><br>
    <b>Explanation:</b> Customer count depends on base arrival (C₀ = 25/day),
    price level (higher price → fewer customers), and staff level (more staff → better service → more customers stay)
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='reward-term'>
    <b>Price Sensitivity Factor:</b><br>
    f_price(p) = 1 - α × (p - 1)<br>
    where α = 0.13 (price sensitivity coefficient)<br><br>
    p=0 (Low):     f_price = 1 - 0.13×(-1) = 1.13  (13% more customers)<br>
    p=1 (Medium):  f_price = 1 - 0.13×(0) = 1.00   (baseline)<br>
    p=2 (High):    f_price = 1 - 0.13×(1) = 0.87   (13% fewer customers)<br><br>
    <b>Interpretation:</b> Elasticity of demand with respect to price.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='reward-term'>
    <b>Staff Quality Factor:</b><br>
    f_staff(w) = 1 + λ × w<br>
    where λ = 0.08 (staff effectiveness coefficient)<br><br>
    w=0 (1 person):  f_staff = 1 + 0.08×0 = 1.00  (baseline)<br>
    w=1 (2 people):  f_staff = 1 + 0.08×1 = 1.08  (8% more customers)<br>
    w=2 (3 people):  f_staff = 1 + 0.08×2 = 1.16  (16% more customers)<br>
    w=3 (4 people):  f_staff = 1 + 0.08×3 = 1.24  (24% more customers)<br><br>
    <b>Interpretation:</b> Service quality improves with more staff → better customer experience → more sales.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='reward-term'>
    <b>Labor Cost Component:</b><br>
    Cost_labor = (w + 1) × wage × hours<br>
    Cost_labor = (w + 1) × $20/hr × 8 hrs<br><br>
    w=0 (1 person):  Cost = 1 × $20 × 8 = $160<br>
    w=1 (2 people):  Cost = 2 × $20 × 8 = $320<br>
    w=2 (3 people):  Cost = 3 × $20 × 8 = $480<br>
    w=3 (4 people):  Cost = 4 × $20 × 8 = $640<br><br>
    <b>Key Insight:</b> Linear cost but diminishing marginal benefit → need to find optimal staff level.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='reward-term'>
    <b>Total Profit Formula:</b><br>
    R(s,a) = [N_customers × Price] - [Labor_Cost] - [Transition_Penalty × 1(a ≠ "Maintain")]<br><br>
    <b>Transition Penalty:</b> $5 penalty if action changes state (encourages stability)<br>
    1(a ≠ "Maintain") = 1 if action changes state, 0 if maintaining<br><br>
    <b>Example Calculation (Medium Price, 2 Staff):</b><br>
    N = 25 × 1.0 × 1.08 = 27 customers<br>
    Revenue = 27 × $8 = $216<br>
    Labor = 2 × $20 × 8 = $320<br>
    Profit (Maintain) = $216 - $320 - $0 = -$104<br>
    Profit (Change) = $216 - $320 - $5 = -$109
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### Bellman Optimality Equation
    """)
    
    st.markdown("""
    <div class='math-box'>
    <b>Core Recursive Formula:</b><br>
    V*(s) = max_a [ R(s,a) + γ × Σ_s' P(s'|s,a) × V*(s') ]<br><br>
    <b>Components:</b><br>
    V*(s) = optimal expected cumulative discounted reward from state s<br>
    R(s,a) = immediate reward (profit) from action a in state s<br>
    γ = discount factor (0 < γ < 1) — weight of future rewards<br>
    P(s'|s,a) = probability of transitioning to s' when taking action a<br>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='math-box'>
    <b>Q-Function (Action Value):</b><br>
    Q*(s,a) = R(s,a) + γ × Σ_s' P(s'|s,a) × V*(s')<br><br>
    <b>Optimal Policy Extraction:</b><br>
    π*(s) = argmax_a Q*(s,a)<br><br>
    <b>In English:</b> For each state, pick the action with the highest Q-value!
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### Value Iteration Algorithm
    """)
    
    st.markdown("""
    <div class='math-box'>
    <b>Pseudocode:</b><br>
    1. Initialize V(s) ← 0 for all s ∈ S<br>
    2. Repeat until convergence:<br>
       For each state s ∈ S:<br>
         V_old ← V(s)<br>
         V(s) ← max_a [R(s,a) + γ × E[V(s')]]<br>
         Δ ← max(Δ, |V(s) - V_old|)<br>
    3. If Δ < ε, CONVERGED<br>
    4. Extract policy: π(s) = argmax_a Q(s,a)
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### Discount Factor Deep Dive
    """)
    
    col_g1, col_g2, col_g3 = st.columns(3)
    
    with col_g1:
        st.markdown("""
        <div class='math-box' style='border-left-color: #c89888;'>
        <b>γ = 0.50</b><br>
        (Myopic Owner)<br><br>
        Focus: Today only<br>
        Horizon: ~2 days<br>
        V(reward_day1) = $100<br>
        V(reward_day10) = $0.098<br><br>
        Strategy: Squeeze profit today, ignore tomorrow
        </div>
        """, unsafe_allow_html=True)
    
    with col_g2:
        st.markdown("""
        <div class='math-box' style='border-left-color: #7ec8c8;'>
        <b>γ = 0.95</b><br>
        (Balanced Owner)<br><br>
        Focus: Near term<br>
        Horizon: ~20 days<br>
        V(reward_day1) = $100<br>
        V(reward_day20) = $35.85<br><br>
        Strategy: Balance profit & growth
        </div>
        """, unsafe_allow_html=True)
    
    with col_g3:
        st.markdown("""
        <div class='math-box' style='border-left-color: #7aae98;'>
        <b>γ = 0.99</b><br>
        (Strategic Owner)<br><br>
        Focus: Long term<br>
        Horizon: ~100 days<br>
        V(reward_day1) = $100<br>
        V(reward_day100) = $36.60<br><br>
        Strategy: Invest in loyalty
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    ### Why Value Iteration Converges
    """)
    
    st.markdown("""
    <div class='math-box'>
    <b>Contraction Mapping Theorem:</b><br>
    The Bellman operator T is a contraction mapping:<br>
    ||T(V) - T(V')||_∞ ≤ γ × ||V - V'||_∞<br><br>
    <b>Consequence:</b> Since 0 < γ < 1, repeated application of T<br>
    converges geometrically to the unique fixed point V*.<br><br>
    Error after k iterations:<br>
    ||V^k - V*||_∞ ≤ γ^k × ||V^0 - V*||_∞<br><br>
    <b>Convergence is exponential!</b> Doubling iterations roughly squares accuracy.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### Real-World Applications
    
    - **Restaurant Operations**: Price optimization, staffing, menu planning
    - **Retail**: Inventory levels, pricing, promotional timing
    - **Ride-Sharing**: Driver compensation, surge pricing
    - **Healthcare**: Resource allocation, treatment planning
    - **Finance**: Portfolio management, asset allocation
    
    The techniques from Whisker's Cafe form the foundation of operational optimization!
    """)
