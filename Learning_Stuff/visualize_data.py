import numpy as np
import matplotlib.pyplot as plt


"""Plot Example Stimuli:

The first plot shows the first 5 stimuli. This helps you visualize what the stimuli look like.
Histogram of Spike Indices:

The second plot is a histogram of the spike indices. This shows the distribution of spikes across the stimuli.
Stimulus with Spike Overlaid:

The third plot displays a specific stimulus (e.g., the first one) and overlays a spike on it for illustration. You can modify the index to visualize other stimuli."""

# Load simulated data
stimuli = np.load('Learning_Stuff/stimuli.npy')
spike_indices = np.load('/Users/jamieannemortel/Projects/Learning_Stuff/spike_indices.npy')

# Parameters
num_stimuli = stimuli.shape[0]
stimulus_length = stimuli.shape[1]

# Plot some example stimuli
plt.figure(figsize=(12, 6))
for i in range(5):  # Plot the first 5 stimuli for illustration
    plt.plot(stimuli[i], label=f'Stimulus {i + 1}')
plt.title('Example Stimuli')
plt.xlabel('Time (units)')
plt.ylabel('Stimulus Intensity')
plt.legend()
plt.show()

# Plot spike indices
plt.figure(figsize=(10, 5))
plt.hist(spike_indices, bins=np.arange(0, num_stimuli + 1) - 0.5, edgecolor='k')
plt.title('Histogram of Spike Indices')
plt.xlabel('Stimulus Index')
plt.ylabel('Number of Spikes')
plt.show()

# Plot a specific stimulus with spikes overlaid (for example, stimulus at index 0)
plt.figure(figsize=(12, 6))
plt.plot(stimuli[0], label='Stimulus 0')
plt.axvline(x=spike_indices[0], color='r', linestyle='--', label='Spike')
plt.title('Stimulus 0 with a Spike Overlaid')
plt.xlabel('Time (units)')
plt.ylabel('Stimulus Intensity')
plt.legend()
plt.show()

