# 🐱 Whisker’s Cafe  
### **AI for Cat Café Optimization Using Markov Decision Processes (MDPs)**  

📄 **Full Report (PDF):**  
[Download Whiskers_Cafe.pdf](./Whisker's Cafe Report)

---

## 🚀 Overview  
Whisker’s Cafe is an interactive, AI-powered educational platform that teaches **Markov Decision Processes (MDPs)** through the cute and relatable setting of managing a cat café.

Built using **Streamlit**, it allows users to:

- Configure MDP parameters  
- Run value iteration to find optimal strategies  
- Play a live simulation of café management  
- Learn the mathematics behind sequential decision-making  

This repository contains the complete PDF report documenting the mathematics, algorithms, and design behind the platform.

---

## 🧠 What is an MDP?

An **MDP (Markov Decision Process)** is a mathematical framework for decision-making where outcomes are uncertain.

Formally, an MDP is:

$$
M = (S, A, P, R, \gamma)
$$

Where:

- **S** — States (e.g., price level, staff level)  
- **A** — Actions (raise price, hire staff, etc.)  
- **P** — Transition probabilities  
- **R** — Rewards (daily profit)  
- **γ** — Discount factor  

---

## 🐾 Cat Café Optimization: State & Actions

### **State Space:**  
Each state is a pair **(p, s)**  
- **p** ∈ {0, 1, 2} → Price Levels (Low / Medium / High)  
- **s** ∈ {0, 1, 2, 3} → Staff Levels (1–4 people)  

Total states: **3 × 4 = 12**

### **Action Space:**  
- Raise Price  
- Lower Price  
- Hire Staff  
- Fire Staff  
- Maintain  

---

## 💰 Reward Function

Daily profit is computed as:

$$
R(p, s, a) = N_{\text{customers}} \cdot Price - LaborCost - Penalty
$$

Where:

- **Customer arrivals:**

$$
N_{\text{customers}} = C_0 \cdot f_{\text{price}}(p) \cdot f_{\text{staff}}(s)
$$

- **Price sensitivity:**

$$
f_{\text{price}}(p) = 1 - 0.13(p - 1)
$$

- **Staff effectiveness:**

$$
f_{\text{staff}}(s) = 1 + 0.08s
$$

- **Labor cost:**  
\((s + 1) \times 160\)

- **Penalty:**  
\$5 if an action changes the state

---

## 🔢 Bellman Equation & Value Iteration

The optimal value of a state follows:

$$
V^*(s) = \max_a \left[ R(s,a) + \gamma V^*(s') \right]
$$

Where \(s'\) is the next state after action \(a\).

### **Value Iteration Algorithm**

1. Initialize:  
   \(V(s) = 0\) for all states  
2. Update repeatedly using the Bellman optimality rule  
3. Stop when:  
   $$\max_s |V_{\text{new}}(s) - V(s)| < \epsilon$$  
4. Extract optimal policy:  
   $$
   \pi^*(s) = \arg\max_a \left[ R(s,a) + \gamma V^*(s') \right]
   $$

---

## 📊 Platform Features

### **1. Configure & Solve**  
- Adjust discount factor γ  
- Set wage, customer arrival rate, price multiplier  
- Run value iteration  
- View:  
  - Value function heatmap  
  - Optimal policy table  
  - Expected daily profit  

### **2. Café Simulation**  
Play as the manager and see:  
- Your chosen action  
- The AI’s recommended action  
- Daily and cumulative profit  

### **3. Learn & Explore**  
A guided walkthrough of MDP mathematics, intuition, and examples.

---

## 🎓 Why This Matters  
This tool brings reinforcement learning concepts to life and applies them to real-world domains such as:

- Restaurant staffing  
- Retail pricing  
- Workforce management  
- Healthcare scheduling  
- Robotics  

And yes — all while managing a cozy cat café 😺☕.

---

## 🧑‍💻 Team Contributions

| Name | Contribution |
|------|-------------|
| Utkarsh Srivastava | Mathematics & Code |
| Rutvi Shah | UI Design |
| Shreyans Jain | Verification |
| Mumuksh Jain | Report |
---

## 📄 Report  
You can view or download the full project report here:

👉 **[Whiskers_Cafe.pdf](.cat_cafe/Whisker's_Cafe_Report.pdf)**

---

