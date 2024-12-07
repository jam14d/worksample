import numpy as np


"""Stimulus Data:

The stimulus data in STA refers to the recorded representation of the stimuli. For instance, if you are presenting visual patterns, the stimulus data might be a series of images or a matrix of pixel values corresponding to each time point.
Alignment and Averaging:

To perform STA, you extract the segments of this stimulus data that occur just before each recorded spike. These segments are then averaged to find out what specific features of the stimulus are associated with the neuron’s spikes.


Example to Illustrate
Stimulus Presentation: Suppose you show a sequence of images to a subject and record the times when the subject’s brain activity spikes.
Stimulus Data: The actual images or their numerical representation are the stimulus data you record.
Analysis with STA: For each spike, you look at the images presented just before the spike (e.g., the last 100 ms before the spike) and average these images to determine which visual features are most likely to trigger spikes."""



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
