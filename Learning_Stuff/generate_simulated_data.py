import numpy as np

# Parameters
num_stimuli = 1000        # Number of stimuli
stimulus_length = 50      # Length of each stimulus
spike_times = 200         # Number of spikes
pre_spike_window = 20      # Time window to consider before each spike

# Simulate stimuli (e.g., 1000 stimuli, each 50 units long)
stimuli = np.random.randn(num_stimuli, stimulus_length)

# Simulate spike times (e.g., 200 spikes occurring randomly in the stimuli)
spike_indices = np.random.randint(pre_spike_window, num_stimuli, size=spike_times)

# Save data to files
np.save('stimuli.npy', stimuli)
np.save('spike_indices.npy', spike_indices)

print("Simulated data saved.")
