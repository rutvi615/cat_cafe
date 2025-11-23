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


# Beautiful Theme CSS with Full Background Image
st.markdown("""
<style>
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Full Background Image */
    .stApp {
        background-image: url('https://i.pinimg.com/1200x/e4/0d/e7/e40de755d51beaf8f179f92c68ee61c3.jpg');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    /* Make default Streamlit backgrounds transparent */
    .main .block-container {
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        border-bottom: 2px solid rgba(238,179,233,0.4);
        background: rgba(45, 20, 44, 0.5);
        padding: 10px;
        border-radius: 15px 15px 0 0;
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 15px;
        padding: 12px 25px;
        color: #84ACC4;
        background-color: transparent;
        border-bottom: 3px solid transparent;
        transition: all 0.4s ease;
    }
    
    .stTabs [data-baseweb="tab-list"] button:hover {
        color: #EEB3E9;
        transition: color 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #EEB3E9;
        border-bottom: 3px solid #EEB3E9;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        background: rgba(45, 20, 44, 0.65);
        border-radius: 0 0 15px 15px;
        padding: 25px;
    }
    
    .param-card {
        background: rgba(45, 20, 44, 0.75);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid rgba(238,179,233,0.3);
        box-shadow: 0 4px 20px rgba(73,49,109,0.4);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .param-card:hover {
        border-color: #EEB3E9;
        box-shadow: 0 6px 25px rgba(238,179,233,0.3);
        background: rgba(73, 49, 109, 0.8);
        transition: all 0.3s ease;
    }
    
    .info-box {
        background: rgba(45, 20, 44, 0.75);
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #84ACC4;
        color: #F7E1E7;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .success-box {
        background: rgba(73, 49, 109, 0.75);
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #EEB3E9;
        color: #F7E1E7;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .story-box {
        background: rgba(45, 20, 44, 0.75);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(238,179,233,0.3);
        color: #F7E1E7;
        font-size: 15px;
        line-height: 1.8;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .story-box:hover {
        background: rgba(73, 49, 109, 0.85);
        border-color: #EEB3E9;
    }
    
    .math-box {
        background: rgba(71, 109, 124, 0.75);
        padding: 18px;
        border-radius: 10px;
        border-left: 4px solid #84ACC4;
        color: #F7E1E7;
        font-size: 13px;
        line-height: 1.7;
        font-family: 'Courier New', monospace;
        margin: 12px 0;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .math-box:hover {
        border-left-color: #EEB3E9;
        box-shadow: 0 4px 12px rgba(238,179,233,0.2);
        background: rgba(132, 172, 196, 0.8);
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
        background: linear-gradient(135deg, #A782A9 0%, #84ACC4 100%);
        color: #2D142C;
        border: none;
        padding: 12px 30px;
        border-radius: 10px;
        font-weight: 600;
        font-size: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(238,179,233,0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(238,179,233,0.5);
        background: linear-gradient(135deg, #EEB3E9 0%, #A782A9 100%);
        transition: all 0.3s ease;
    }
    
    h1, h2, h3 {
        color: #F7E1E7 !important;
        font-weight: 600;
        transition: all 0.3s ease;
        text-shadow: 0 2px 10px rgba(45, 20, 44, 0.8);
    }
    
    h1 { font-size: 32px; }
    h3 { font-size: 20px; }
    
    .metric-box {
        background: rgba(45, 20, 44, 0.75);
        border-radius: 10px;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(238,179,233,0.2);
    }
    
    .metric-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(238,179,233,0.2);
        background: rgba(73, 49, 109, 0.8);
    }
    
    .reward-term {
        background: rgba(71, 109, 124, 0.75);
        padding: 15px;
        border-radius: 10px;
        border-left: 3px solid #84ACC4;
        margin: 10px 0;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        color: #F7E1E7;
    }
    
    .reward-term:hover {
        border-left-color: #EEB3E9;
        transform: translateX(5px);
        background: rgba(132, 172, 196, 0.85);
        transition: all 0.3s ease;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(45, 20, 44, 0.85);
        backdrop-filter: blur(15px);
    }
    
    /* Metric labels */
    [data-testid="stMetricLabel"] {
        color: #F7E1E7 !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #EEB3E9 !important;
    }
    
    /* Slider styling */
    .stSlider [data-baseweb="slider"] {
        background: rgba(73, 49, 109, 0.5);
    }
    
    /* DataFrame styling */
    .stDataFrame {
        background: rgba(45, 20, 44, 0.75);
        backdrop-filter: blur(10px);
    }
    
    /* Text color for better readability */
    p, span, label, .stMarkdown {
        color: #F7E1E7 !important;
    }
    
    /* Divider */
    hr {
        border-color: rgba(238,179,233,0.3) !important;
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
                    
                    expected_future = v[p_next, s_next]
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
        '#2D142C', '#49316D', '#5D4A7A', '#7a6f9a', '#9a8fba',
        '#A782A9', '#c8a8c8', '#d8b8d8', '#EEB3E9', '#f7d8f7'
    ]
    cmap = LinearSegmentedColormap.from_list('cafe_soft', colors_soft, N=256)
    
    vmin, vmax = values.min(), values.max()
    
    im = ax.imshow(values, cmap=cmap, aspect='auto', vmin=vmin, vmax=vmax)
    
    ax.set_xticks(np.arange(NUM_STAFF))
    ax.set_yticks(np.arange(NUM_PRICES))
    ax.set_xticklabels(STAFF_LEVELS, fontsize=12, color='#F7E1E7', fontweight=500)
    ax.set_yticklabels(PRICE_LEVELS, fontsize=12, color='#F7E1E7', fontweight=500)
    
    ax.set_xticks(np.arange(NUM_STAFF) - 0.5, minor=True)
    ax.set_yticks(np.arange(NUM_PRICES) - 0.5, minor=True)
    ax.grid(which='minor', color='#49316D', linestyle='-', linewidth=2.5, alpha=0.6)
    
    for i in range(NUM_PRICES):
        for j in range(NUM_STAFF):
            value = values[i, j]
            
            normalized = (value - vmin) / (vmax - vmin) if vmax > vmin else 0.5
            text_color = '#2D142C' if normalized > 0.5 else '#F7E1E7'
            
            rect = mpatches.Rectangle((j-0.45, i-0.45), 0.9, 0.9, 
                                     linewidth=0.5, edgecolor='#EEB3E9', 
                                     facecolor='none', alpha=0.3)
            ax.add_patch(rect)
            
            ax.text(j, i, f'${value:.0f}', ha='center', va='center',
                   color=text_color, fontsize=13, fontweight='600', 
                   bbox=dict(boxstyle='round,pad=0.4', facecolor='none', edgecolor='none'))
    
    ax.set_xlabel("Staff Level", fontsize=13, color='#F7E1E7', fontweight=600, labelpad=12)
    ax.set_ylabel("Price Level", fontsize=13, color='#F7E1E7', fontweight=600, labelpad=12)
    ax.set_title(title, fontsize=16, color='#F7E1E7', pad=20, fontweight=600)
    
    cbar = plt.colorbar(im, ax=ax, pad=0.02)
    cbar.set_label('Expected Profit ($)', color='#F7E1E7', fontsize=12, fontweight=500, labelpad=15)
    cbar.ax.tick_params(colors='#F7E1E7', labelsize=11)
    cbar.outline.set_edgecolor('#49316D')
    cbar.outline.set_linewidth(1.5)
    
    fig.patch.set_facecolor('#2D142C')
    ax.set_facecolor('#49316D')
    ax.spines['bottom'].set_color('#EEB3E9')
    ax.spines['left'].set_color('#EEB3E9')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(colors='#F7E1E7', labelsize=11)
    
    plt.tight_layout()
    return fig


def create_policy_table(policy):
    """Create beautiful soft-colored policy table with visible text"""
    fig, ax = plt.subplots(figsize=(12, 5.5))
    ax.axis('off')
    
    action_colors = {
        0: '#7a6f9a',
        1: '#9a8fba',
        2: '#84ACC4',
        3: '#A782A9',
        4: '#5D4A7A'
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
            cell.set_text_props(weight='600', color='#F7E1E7', fontsize=11)
            cell.set_linewidth(1.5)
            cell.set_edgecolor('#2D142C')
    
    for j in range(NUM_STAFF):
        cell = table[(0, j)]
        cell.set_facecolor('#2D142C')
        cell.set_text_props(weight='600', color='#F7E1E7', fontsize=11)
        cell.set_linewidth(1.5)
        cell.set_edgecolor('#49316D')
    
    for i in range(NUM_PRICES):
        cell = table[(i+1, -1)]
        cell.set_facecolor('#2D142C')
        cell.set_text_props(weight='600', color='#F7E1E7', fontsize=11)
        cell.set_linewidth(1.5)
        cell.set_edgecolor('#49316D')
    
    fig.patch.set_facecolor('#2D142C')
    plt.suptitle("Optimal Policy: Best Action per State", fontsize=16, color='#F7E1E7', 
             y=0.98, fontweight=600)
    
    return fig


def create_convergence_plot(deltas):
    """Visualize per-iteration delta decay for the value-iteration loop."""
    iterations = np.arange(1, len(deltas) + 1)
    fig, ax = plt.subplots(figsize=(11, 4))
    
    ax.plot(iterations, deltas, color='#EEB3E9', linewidth=2.5, marker='o', markersize=4)
    ax.fill_between(iterations, deltas, color='#EEB3E9', alpha=0.15)
    
    ax.set_yscale('log')
    ax.set_xlabel("Iteration", fontsize=12, color='#F7E1E7', fontweight=600)
    ax.set_ylabel("Delta (log scale)", fontsize=12, color='#F7E1E7', fontweight=600)
    ax.set_title("Value Iteration Convergence", fontsize=15, color='#F7E1E7', pad=14, fontweight=600)
    
    ax.grid(color='#49316D', linestyle='--', linewidth=1, alpha=0.5)
    ax.set_facecolor('#2D142C')
    fig.patch.set_facecolor('#2D142C')
    ax.tick_params(colors='#F7E1E7')
    ax.spines['bottom'].set_color('#EEB3E9')
    ax.spines['left'].set_color('#EEB3E9')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    return fig


def create_reward_history_plot(history):
    """Plot daily and cumulative profit trajectories during the simulator gameplay."""
    if not history:
        return None
    
    df = pd.DataFrame(history)
    df['cumulative_profit'] = df['profit'].cumsum()
    
    fig, ax1 = plt.subplots(figsize=(11, 4))
    ax2 = ax1.twinx()
    
    ax1.plot(df['day'], df['profit'], color='#84ACC4', linewidth=2.2, marker='o', label='Daily Profit')
    ax2.plot(df['day'], df['cumulative_profit'], color='#EEB3E9', linewidth=2.2, linestyle='--', label='Cumulative Profit')
    
    ax1.set_xlabel("Day", fontsize=12, color='#F7E1E7', fontweight=600)
    ax1.set_ylabel("Daily Profit ($)", fontsize=12, color='#84ACC4', fontweight=600)
    ax2.set_ylabel("Cumulative Profit ($)", fontsize=12, color='#EEB3E9', fontweight=600)
    
    ax1.set_title("Cafe Performance Over Time", fontsize=15, color='#F7E1E7', pad=14, fontweight=600)
    
    ax1.grid(color='#49316D', linestyle='--', linewidth=1, alpha=0.4)
    ax1.set_facecolor('#2D142C')
    ax2.set_facecolor('none')
    fig.patch.set_facecolor('#2D142C')
    
    ax1.tick_params(colors='#F7E1E7')
    ax2.tick_params(colors='#F7E1E7')
    for spine in ax1.spines.values():
        spine.set_color('#EEB3E9')
    for spine in ax2.spines.values():
        spine.set_color('#EEB3E9')
    
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper left', facecolor='#2D142C', edgecolor='#EEB3E9')
    
    plt.tight_layout()
    return fig


def q_learning(params, discount, episodes, alpha, epsilon, max_steps):
    """Tabular Q-learning for the cafe MDP."""
    q_table = np.zeros((NUM_PRICES, NUM_STAFF, NUM_ACTIONS))
    rewards_history = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for episode in range(episodes):
        p = np.random.randint(NUM_PRICES)
        s = np.random.randint(NUM_STAFF)
        episode_reward = 0
        
        for step in range(max_steps):
            if np.random.rand() < epsilon:
                action = np.random.randint(NUM_ACTIONS)
            else:
                action = int(np.argmax(q_table[p, s]))
            
            p_next, s_next = next_state(p, s, action)
            r = reward(p_next, s_next, params, penalty=(action != 4))
            
            best_next = np.max(q_table[p_next, s_next])
            q_table[p, s, action] = (1 - alpha) * q_table[p, s, action] + alpha * (r + discount * best_next)
            
            p, s = p_next, s_next
            episode_reward += r
        
        rewards_history.append(episode_reward)
        progress = (episode + 1) / episodes
        progress_bar.progress(progress)
        status_text.text(f"Episode {episode + 1}/{episodes} | Reward: {episode_reward:.2f}")
    
    progress_bar.empty()
    status_text.empty()
    
    state_values = np.max(q_table, axis=2)
    policy = np.argmax(q_table, axis=2)
    
    return state_values, policy, rewards_history


def create_learning_curve(rewards, window=20):
    """Plot episode reward trajectory with rolling average for Q-learning."""
    if not rewards:
        return None
    
    episodes = np.arange(1, len(rewards) + 1)
    rewards_series = pd.Series(rewards)
    rolling = rewards_series.rolling(window=window, min_periods=1).mean()
    
    fig, ax = plt.subplots(figsize=(11, 4))
    
    ax.plot(episodes, rewards, color='#84ACC4', linewidth=1.8, label='Episode Reward', alpha=0.7)
    ax.plot(episodes, rolling, color='#EEB3E9', linewidth=2.5, label=f'Rolling Avg ({window})')
    
    ax.set_xlabel("Episode", fontsize=12, color='#F7E1E7', fontweight=600)
    ax.set_ylabel("Reward", fontsize=12, color='#F7E1E7', fontweight=600)
    ax.set_title("Q-Learning Reward Curve", fontsize=15, color='#F7E1E7', pad=14, fontweight=600)
    
    ax.grid(color='#49316D', linestyle='--', linewidth=1, alpha=0.4)
    ax.set_facecolor('#2D142C')
    fig.patch.set_facecolor('#2D142C')
    ax.tick_params(colors='#F7E1E7')
    
    for spine in ax.spines.values():
        spine.set_color('#EEB3E9')
    
    ax.legend(loc='lower right', facecolor='#2D142C', edgecolor='#EEB3E9')
    plt.tight_layout()
    return fig


# ==========================================
# Main App
# ==========================================


st.markdown("""
<div style='text-align: center; margin-bottom: 20px; margin-top: -30px;'>
    <h1 style='color: #EEB3E9; font-size: 36px; font-weight: 600; margin-bottom: 8px; text-shadow: 0 2px 15px rgba(45, 20, 44, 0.9);'>Whisker's Cafe</h1>
    <p style='color: #F7E1E7; font-size: 16px; margin: 0; font-style: italic; text-shadow: 0 1px 8px rgba(45, 20, 44, 0.8);'>Optimize your adorable cat cafe using Markov Decision Processes</p>
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
            <h3 style='margin-top: 0; color: #F7E1E7;'>Cafe Optimization Engine</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        algo_options = ["Value Iteration", "Q-Learning"]
        default_algo = st.session_state.get('algorithm', algo_options[0])
        algo_index = algo_options.index(default_algo) if default_algo in algo_options else 0
        algorithm = st.radio("Choose Solver", algo_options, index=algo_index)
        
        st.write("")
        
        st.write("**Discount Factor (γ): {:.2f}**".format(st.session_state.get('gamma', 0.95)))
        st.write("<span style='color: #F7E1E7; font-size: 13px;'>How much you value future profit</span>", unsafe_allow_html=True)
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
        st.write("**Labor_effect : {:.2f}**".format(st.session_state.get('labor_effect', 0.08)))
        labor_effect = st.slider("Labor_effect ", 0.0, 0.5, st.session_state.get('labor_effect', 0.08),
                        step=0.01, key='labor_effect_slider', label_visibility='collapsed')


        if algorithm == "Q-Learning":
            st.write("")
            st.write("**Episodes: {}**".format(st.session_state.get('episodes', 400)))
            episodes = st.slider("Episodes", 100, 2000, st.session_state.get('episodes', 400),
                                 step=50, key='episodes_slider', label_visibility='collapsed')
            
            st.write("")
            st.write("**Learning Rate (α): {:.2f}**".format(st.session_state.get('alpha', 0.3)))
            alpha = st.slider("Learning Rate", 0.01, 1.0, st.session_state.get('alpha', 0.3),
                              step=0.01, key='alpha_slider', label_visibility='collapsed')
            
            st.write("")
            st.write("**Exploration (ε): {:.2f}**".format(st.session_state.get('epsilon', 0.2)))
            epsilon = st.slider("Exploration Rate", 0.0, 1.0, st.session_state.get('epsilon', 0.2),
                                step=0.01, key='epsilon_slider', label_visibility='collapsed')
            
            st.write("")
            st.write("**Max Steps / Episode: {}**".format(st.session_state.get('max_steps', 30)))
            max_steps = st.slider("Max Steps", 5, 100, st.session_state.get('max_steps', 30),
                                  step=5, key='steps_slider', label_visibility='collapsed')
        else:
            episodes = st.session_state.get('episodes', 400)
            alpha = st.session_state.get('alpha', 0.3)
            epsilon = st.session_state.get('epsilon', 0.2)
            max_steps = st.session_state.get('max_steps', 30)
        
        st.write("")
        
        if st.button("Solve Optimal Policy", use_container_width=True, key='solve_btn'):
            st.session_state['solve'] = True
            st.session_state['gamma'] = gamma
            st.session_state['max_iter'] = max_iter
            st.session_state['cust_rate'] = cust_rate
            st.session_state['multiplier'] = multiplier
            st.session_state['staff_cost'] = staff_cost
            st.session_state['price_sens'] = price_sens
            st.session_state['labor_effect'] = labor_effect
            st.session_state['algorithm'] = algorithm
            st.session_state['episodes'] = episodes
            st.session_state['alpha'] = alpha
            st.session_state['epsilon'] = epsilon
            st.session_state['max_steps'] = max_steps
            
                
        if st.session_state.get('solve', False):
            best_val = st.session_state.get('values', np.zeros((3,4))).max() if st.session_state.get('values') is not None else 0
            solver_used = st.session_state.get('algorithm', 'Value Iteration')
            
            if solver_used == "Value Iteration" and st.session_state.get('iterations'):
                iters = st.session_state.get('iterations', 0)
                deltas = st.session_state.get('deltas', [])
                final_delta = deltas[-1] if deltas else 0
                
                st.markdown(f"""
                <div class='info-box' style='margin-top: 25px;'>
                    <p style='color: #EEB3E9; font-weight: 600; margin: 8px 0;'>Converged in {iters} iterations</p>
                    <p style='color: #F7E1E7; margin: 8px 0; font-size: 13px;'>Final delta: {final_delta:.8f}</p>
                </div>
                """, unsafe_allow_html=True)
            elif solver_used == "Q-Learning" and st.session_state.get('episodes_run'):
                episodes_run = st.session_state.get('episodes_run', 0)
                rewards = st.session_state.get('learning_rewards', [])
                recent_reward = rewards[-1] if rewards else 0
                best_reward = max(rewards) if rewards else 0
                
                st.markdown(f"""
                <div class='info-box' style='margin-top: 25px;'>
                    <p style='color: #EEB3E9; font-weight: 600; margin: 8px 0;'>Trained for {episodes_run} episodes</p>
                    <p style='color: #F7E1E7; margin: 8px 0; font-size: 13px;'>Latest reward: ${recent_reward:.2f} | Best: ${best_reward:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class='success-box' style='margin-top: 15px;'>
                <p style='color: #F7E1E7; margin: 5px 0; font-size: 13px;'>Best Expected Daily Profit</p>
                <p style='color: #EEB3E9; font-size: 32px; font-weight: 600; margin: 12px 0;'>${best_val:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col_right:
        if st.session_state.get('solve', False):
            params = {
                    'cust_rate': cust_rate,
                    'price_sens': price_sens,
                    'labor_effect': labor_effect,
                    'staff_cost': staff_cost,
                    'multiplier': multiplier,
                    'penalty': 5
                }


            deltas = []
            rewards_history = []
            iterations = None
            
            if algorithm == "Value Iteration":
                with st.spinner('Solving MDP...'):
                    values, policy, deltas, iterations = value_iteration(params, gamma, max_iter)
                st.session_state['deltas'] = deltas
                st.session_state['iterations'] = iterations
                st.session_state['learning_rewards'] = []
                st.session_state['episodes_run'] = None
            else:
                with st.spinner('Training Q-Learning Agent...'):
                    values, policy, rewards_history = q_learning(params, gamma, episodes, alpha, epsilon, max_steps)
                st.session_state['learning_rewards'] = rewards_history
                st.session_state['episodes_run'] = episodes
                st.session_state['deltas'] = []
                st.session_state['iterations'] = None
            
            st.session_state['values'] = values
            st.session_state['policy'] = policy
            
            st.subheader("Value Function Heatmap")
            st.write("<span style='color: #F7E1E7; font-size: 13px;'>Expected profit for each price/staff combination</span>", 
                    unsafe_allow_html=True)
            fig_heat = create_heatmap(values)
            st.pyplot(fig_heat, use_container_width=True)
            
            st.subheader("Optimal Policy")
            st.write("<span style='color: #F7E1E7; font-size: 13px;'>Best action for each state</span>", 
                    unsafe_allow_html=True)
            fig_policy = create_policy_table(policy)
            st.pyplot(fig_policy, use_container_width=True)
            
            if algorithm == "Value Iteration" and deltas:
                st.subheader("Convergence Tracker")
                st.write("<span style='color: #F7E1E7; font-size: 13px;'>Monitor how the Bellman updates shrink over each iteration</span>", 
                        unsafe_allow_html=True)
                fig_conv = create_convergence_plot(deltas)
                st.pyplot(fig_conv, use_container_width=True)
                st.caption("Delta is plotted on a log scale to highlight late-stage convergence.")
            elif algorithm == "Q-Learning" and rewards_history:
                st.subheader("Learning Curve")
                st.write("<span style='color: #F7E1E7; font-size: 13px;'>Episode rewards with a rolling average for stability</span>", 
                        unsafe_allow_html=True)
                fig_learn = create_learning_curve(rewards_history)
                if fig_learn:
                    st.pyplot(fig_learn, use_container_width=True)
        else:
            st.markdown("""
            <div class='info-box'>
                <p style='color: #EEB3E9; font-weight: 600;'>Ready to optimize?</p>
                <p style='color: #F7E1E7;'>Configure the parameters on the left and click <b>'Solve Optimal Policy'</b> to discover the best cafe strategy!</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style='text-align: center; margin-top: 40px;'>
                <div style='font-size: 4em; animation: float 3s ease-in-out infinite;'>😺</div>
                <p style='color: #F7E1E7; margin-top: 15px;'><i>Your cats are waiting for the perfect strategy...</i></p>
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
                # Use solved parameters from tab 1
                params = {
                    'cust_rate': st.session_state.get('cust_rate', 25),
                    'price_sens': st.session_state.get('price_sens', 0.13),
                    'labor_effect': st.session_state.get('labor_effect', 0.08),
                    'staff_cost': st.session_state.get('staff_cost', 15),
                    'multiplier': st.session_state.get('multiplier', 1.0),
                    'penalty': 5
                }
                prof = reward(new_p, new_s, params, penalty=(action_idx != 4))
                
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
            
            fig_rewards = create_reward_history_plot(game['history'])
            if fig_rewards:
                st.write("<span style='color: #F7E1E7; font-size: 13px;'>Track how your decisions compound over time</span>",
                         unsafe_allow_html=True)
                st.pyplot(fig_rewards, use_container_width=True)
            
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
            <p style='color: #EEB3E9; font-weight: 600;'>Simulation Not Available</p>
            <p style='color: #F7E1E7;'>Please solve the MDP first in the <b>'Configure & Solve'</b> tab to unlock the cafe simulation!</p>
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
    current_cust_rate = st.session_state.get('cust_rate', 25)
    current_price_sens = st.session_state.get('price_sens', 0.13)
    current_labor_effect = st.session_state.get('labor_effect', 0.08)
    current_staff_cost = st.session_state.get('staff_cost', 15)
    current_multiplier = st.session_state.get('multiplier', 1.0)
    active_algorithm = st.session_state.get('algorithm', 'Value Iteration')
    current_alpha = st.session_state.get('alpha', 0.3)
    current_epsilon = st.session_state.get('epsilon', 0.2)
    current_episodes = st.session_state.get('episodes', 400)
    current_max_steps = st.session_state.get('max_steps', 30)
    
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
    <b>Explanation:</b> Customer count depends on base arrival (C₀ = """ + f"{current_cust_rate:.0f}" + """/day),
    price level (higher price → fewer customers), and staff level (more staff → better service → more customers stay)
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='reward-term'>
    <b>Price Sensitivity Factor:</b><br>
    f_price(p) = 1 - α × (p - 1)<br>
    where α = """ + f"{current_price_sens:.2f}" + """ (price sensitivity coefficient)<br><br>
    p=0 (Low):     f_price = """ + f"{1 - current_price_sens * (-1):.2f}" + """<br>
    p=1 (Medium):  f_price = """ + f"{1 - current_price_sens * (0):.2f}" + """<br>
    p=2 (High):    f_price = """ + f"{1 - current_price_sens * (1):.2f}" + """<br><br>
    <b>Interpretation:</b> Elasticity of demand with respect to price.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='reward-term'>
    <b>Staff Quality Factor:</b><br>
    f_staff(w) = 1 + λ × w<br>
    where λ = """ + f"{current_labor_effect:.2f}" + """ (staff effectiveness coefficient)<br><br>
    w=0 (1 person):  f_staff = """ + f"{1 + current_labor_effect * 0:.2f}" + """<br>
    w=1 (2 people):  f_staff = """ + f"{1 + current_labor_effect * 1:.2f}" + """<br>
    w=2 (3 people):  f_staff = """ + f"{1 + current_labor_effect * 2:.2f}" + """<br>
    w=3 (4 people):  f_staff = """ + f"{1 + current_labor_effect * 3:.2f}" + """<br><br>
    <b>Interpretation:</b> Service quality improves with more staff → better customer experience → more sales.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='reward-term'>
    <b>Labor Cost Component:</b><br>
    Cost_labor = (w + 1) × wage × hours<br>
    Cost_labor = (w + 1) × $""" + f"{current_staff_cost:.0f}" + """/hr × 8 hrs<br><br>
    w=0 (1 person):  Cost = $""" + f"{(1) * current_staff_cost * 8:.0f}" + """<br>
    w=1 (2 people):  Cost = $""" + f"{(2) * current_staff_cost * 8:.0f}" + """<br>
    w=2 (3 people):  Cost = $""" + f"{(3) * current_staff_cost * 8:.0f}" + """<br>
    w=3 (4 people):  Cost = $""" + f"{(4) * current_staff_cost * 8:.0f}" + """<br><br>
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
    N = """ + f"{current_cust_rate:.0f}" + """ × """ + f"{1 - current_price_sens * 0:.2f}" + """ × """ + f"{1 + current_labor_effect * 1:.2f}" + """ ≈ """ + f"{current_cust_rate * (1 - current_price_sens * 0) * (1 + current_labor_effect * 1):.0f}" + """ customers<br>
    Revenue = N × $""" + f"{8 * current_multiplier:.2f}" + """<br>
    Labor = 2 × $""" + f"{current_staff_cost:.0f}" + """ × 8 = $""" + f"{2 * current_staff_cost * 8:.0f}" + """<br>
    Profit (Maintain) = Revenue - Labor<br>
    Profit (Change) = Revenue - Labor - $5
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
        <div class='math-box' style='border-left-color: #A782A9;'>
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
        <div class='math-box' style='border-left-color: #EEB3E9;'>
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
        <div class='math-box' style='border-left-color: #84ACC4;'>
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
    
    st.markdown("""
    ### Model-Free Reinforcement Learning (Q-Learning)
    """)
    
    st.markdown(f"""
    <div class='math-box'>
    <b>When you select Q-Learning in Tab 1:</b><br>
    • Episodes = {current_episodes}<br>
    • Max Steps per Episode = {current_max_steps}<br>
    • Learning Rate α = {current_alpha:.2f}<br>
    • Exploration ε = {current_epsilon:.2f}<br><br>
    <b>Update Rule:</b><br>
    Q(s,a) ← (1 - α) Q(s,a) + α [ R + γ · max_a' Q(s',a') ]<br><br>
    <b>Exploration:</b> ε-greedy policy randomly explores with probability ε and exploits otherwise.<br>
    <b>Convergence Intuition:</b> With sufficient exploration and a decaying learning rate, the Q-table approaches the optimal action-value function even without knowing transition probabilities.
    </div>
    """, unsafe_allow_html=True)
