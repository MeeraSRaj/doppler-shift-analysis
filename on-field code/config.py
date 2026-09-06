# Create configuration script
import adi
import numpy as np

# Initialize Pluto
sdr = adi.Pluto('ip:192.168.2.1')

# Configure parameters
sdr.sample_rate = 2e6  # 2 MHz sampling rate
sdr.rx_rf_bandwidth = int(1e6)  # 200 kHz bandwidth
sdr.rx_lo = int(1622e6)  # Meteor-M2 frequency
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 50  # Adjust based on signal

# Configure buffer
sdr.rx_buffer_size = 2**16  # 65536 samples

print(f"Configured: LO={sdr.rx_lo/1e6} MHz, SR={sdr.sample_rate/1e6} MS/s")