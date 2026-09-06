# Test capture script
import adi
import numpy as np
import matplotlib.pyplot as plt

sdr = adi.Pluto("usb:2.8.5")
sdr.sample_rate = 2e6
sdr.rx_lo = int(1622e6)  # FM band test

# Capture samples
samples = sdr.rx()

# Compute FFT
fft_size = 1024
psd = np.abs(np.fft.fftshift(np.fft.fft(samples[:fft_size])))**2
psd_db = 10*np.log10(psd)

num_samples=int(sdr.sample_rate * 10)
samples=sdr.rx()
np.save("iq_capture.npy",samples)

# Plot
freq = np.linspace(-sdr.sample_rate/2, sdr.sample_rate/2, fft_size)
plt.plot(freq/1e6, psd_db)
plt.xlabel('Frequency (MHz)')
plt.ylabel('Power (dB)')
plt.show()