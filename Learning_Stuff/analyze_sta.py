import numpy as np
import matplotlib.pyplot as plt

# Load simulated data
stimuli = np.load('Learning_Stuff/stimuli.npy')
spike_indices = np.load('/Users/jamieannemortel/Projects/Learning_Stuff/spike_indices.npy')

# Parameters
stimulus_length = stimuli.shape[1]  # Length of each stimulus
pre_spike_window = 20  # Time window to consider before each spike

# Initialize the STA array with zeros (length of the pre-spike window)
sta = np.zeros(pre_spike_window)
count = np.zeros(pre_spike_window)  # Array to count valid segments

# Compute STA
for spike_index in spike_indices:
    if spike_index >= pre_spike_window:
        segment = stimuli[spike_index - pre_spike_window:spike_index].mean(axis=0)
        if segment.shape[0] == pre_spike_window:  # Ensure segment has the correct shape
            sta += segment
            count += 1

# Avoid division by zero if count is zero
count[count == 0] = 1
sta /= count

# Debugging output
print("STA values:", sta)
print("Number of valid segments:", np.sum(count))

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(sta, label='STA')
plt.title('Spike-Triggered Averaging')
plt.xlabel('Time (units)')
plt.ylabel('Stimulus Intensity')
plt.legend()
plt.show()
