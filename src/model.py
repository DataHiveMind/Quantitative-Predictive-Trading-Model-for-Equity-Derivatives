import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import tf_quant_finance as tff

def build_lstm_model(input_shape, units=64, dropout=0.2):
    """
    Build an LSTM model for market forecasting.
    """
    model = keras.Sequential([
        layers.Input(shape=input_shape),
        layers.LSTM(units, return_sequences=True),
        layers.Dropout(dropout),
        layers.LSTM(units),
        layers.Dropout(dropout),
        layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

def build_transformer_model(input_shape, num_heads=2, ff_dim=32, dropout=0.1):
    """
    Build a simple Transformer model for time series forecasting.
    """
    inputs = keras.Input(shape=input_shape)
    x = layers.LayerNormalization(epsilon=1e-6)(inputs)
    attention_output = layers.MultiHeadAttention(num_heads=num_heads, key_dim=input_shape[-1])(x, x)
    x = layers.Add()([x, attention_output])
    x = layers.LayerNormalization(epsilon=1e-6)(x)
    x = layers.Dense(ff_dim, activation='relu')(x)
    x = layers.Dropout(dropout)(x)
    x = layers.Dense(1)(x)
    model = keras.Model(inputs=inputs, outputs=x)
    model.compile(optimizer='adam', loss='mse')
    return model

def build_dqn_agent(state_shape, action_size):
    """
    Build a Deep Q-Network (DQN) agent for reinforcement learning trading.
    """
    model = keras.Sequential([
        layers.Input(shape=state_shape),
        layers.Dense(128, activation='relu'),
        layers.Dense(128, activation='relu'),
        layers.Dense(action_size, activation='linear')
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

def build_ppo_agent(state_shape, action_size):
    """
    Build a simple PPO agent architecture for reinforcement learning trading.
    """
    # Actor
    actor = keras.Sequential([
        layers.Input(shape=state_shape),
        layers.Dense(128, activation='relu'),
        layers.Dense(128, activation='relu'),
        layers.Dense(action_size, activation='softmax')
    ])
    # Critic
    critic = keras.Sequential([
        layers.Input(shape=state_shape),
        layers.Dense(128, activation='relu'),
        layers.Dense(128, activation='relu'),
        layers.Dense(1)
    ])
    return actor, critic

def tfqf_discounted_cash_flows(cashflows, discount_rate):
    """
    Use tf-quant-finance to compute discounted cash flows.
    """
    return tff.math.discounted_cash_flows(
        discount_rates=discount_rate,
        cashflows=cashflows,
        times=[i for i in range(len(cashflows))]
    )

# Example usage (to be removed or placed under __main__ guard in production)
# lstm_model = build_lstm_model((60, 5))
# transformer_model = build_transformer_model((60, 5))
# dqn_model = build_dqn_agent((10,), 3)
# actor, critic = build_ppo_agent((10,), 3)