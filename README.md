# 🐍 Autonomous Snake AI (Deep Q-Learning)

An advanced Artificial Intelligence project that trains an autonomous agent to play the classic Snake game using **Deep Reinforcement Learning (Q-Learning)**. The project is built from scratch utilizing **PyTorch** for the neural network and **Pygame** for the environment visualization.

---

### 🧠 How It Works (The AI Architecture)

The agent learns how to maximize its score through trial and error, guided by a reward system:
* **Neural Network (Linear Q-Net):** A feed-forward network with an input layer of 11 states, a hidden layer of 256 neurons, and an output layer of 3 actions (Go Straight, Turn Right, Turn Left).
* **State Representation (11-Dimensional Vector):**
  * Danger directions (Straight, Right, Left)
  * Current moving direction (Up, Down, Left, Right)
  * Food location relative to the head (Up, Down, Left, Right)
* **Bellman Equation:** Used to update the Q-values and optimize the network using the Mean Squared Error (MSE) loss function and Adam optimizer.

---

### 🚀 Key Custom Optimizations

* **Dynamic Reward Shaping:** Implemented an explicit Euclidean distance calculation ($np.sqrt$) to reward the agent ($+1.0$) for approaching the food and penalize it ($-1.5$) for moving away. This dramatically speeds up the initial training phase (Exploration).
* **Epsilon-Greedy Strategy:** Starts with a high Epsilon ($100$) for maximum exploration, which decays linearly by $1$ after every game to transition smoothly into exploitation as the model matures.
* **Dual Control Mode:** Press `M` anytime during execution to toggle between the **AI Autonomous Mode** and **Manual Keyboard Control (W, A, S, D)**.

---

### 🛠️ Tech Stack & Requirements

* **Language:** Python
* **Deep Learning Framework:** PyTorch
* **Game Environment:** Pygame
* **Math & Logic:** NumPy

---

### 📂 Project Files

* `snake_game.py`: The core environment logic containing the grid, collision detection, and window rendering.
* `agent.py`: The core AI engine managing the QTrainer, state evaluation, memory tuple processing, and the main training loop.

---
_Developed by Andy Builds as part of my Advanced AI & Reinforcement Learning journey._
