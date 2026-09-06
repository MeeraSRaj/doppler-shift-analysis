import adi
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.optimize import curve_fit
import datetime
import csv
import time

class DopplerTracker:
    def _init_(self, center_freq=1622e6, sample_rate=2e6, bandwidth=1e6, gain=45):
        # Initialize PlutoSDR
        self.sdr = adi.Pluto()
        self.sdr.sample_rate = int(sample_rate)
        self.sdr.rx_lo = int(center_freq)
        self.sdr.rx_rf_bandwidth = int(bandwidth)
        self.sdr.gain_control_mode_chan0 = 'manual'
        self.sdr.rx_hardwaregain_chan0 = gain

        self.center_freq = center_freq
        self.sample_rate = sample_rate
        self.doppler_measurements = []

    def gaussian(self, x, amp, cen, wid):
        return amp * np.exp(-(x-cen)*2 / (2*wid*2))

    def capture_and_process(self, duration=0.1):
        num_samples = int(self.sample_rate * duration)
        self.sdr.rx_buffer_size = num_samples

        iq_samples = self.sdr.rx()

        window = signal.windows.hann(len(iq_samples))
        iq_windowed = iq_samples * window

        fft_result = np.fft.fftshift(np.fft.fft(iq_windowed))
        psd = np.abs(fft_result)**2

        freqs = np.fft.fftshift(np.fft.fftfreq(len(iq_samples), 1/self.sample_rate))
        freqs_abs = freqs + self.center_freq

        peak_idx = np.argmax(psd)
        peak_freq = freqs_abs[peak_idx]

        try:
            fit_range = 10
            idx_start = max(0, peak_idx - fit_range)
            idx_end = min(len(psd), peak_idx + fit_range)

            x_fit = freqs_abs[idx_start:idx_end]
            y_fit = psd[idx_start:idx_end]

            p0 = [np.max(y_fit), peak_freq, 1000]

            popt, _ = curve_fit(self.gaussian, x_fit, y_fit, p0=p0)
            refined_freq = popt[1]
        except:
            refined_freq = peak_freq

        doppler_shift = refined_freq - self.center_freq

        timestamp = datetime.datetime.now()
        self.doppler_measurements.append({
            'timestamp': timestamp,
            'frequency': refined_freq,
            'doppler_shift': doppler_shift,
            'peak_power': 10*np.log10(np.max(psd))
        })

        return refined_freq, doppler_shift, psd, freqs_abs

    def run_tracking(self, duration_minutes=15, update_interval=0.5):
        end_time = time.time() + (duration_minutes * 60)

        plt.ion()
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

        while time.time() < end_time:
            freq, doppler, psd, freq_axis = self.capture_and_process(update_interval)

            ax1.clear()
            ax1.plot(freq_axis/1e6, 10*np.log10(psd))
            ax1.set_xlabel('Frequency (MHz)')
            ax1.set_ylabel('Power (dB)')
            ax1.set_title(f'Current Spectrum - Doppler: {doppler:.1f} Hz')
            ax1.grid(True)

            if len(self.doppler_measurements) > 1:
                times = [(m['timestamp'] - self.doppler_measurements[0]['timestamp']).total_seconds()
                         for m in self.doppler_measurements]
                dopplers = [m['doppler_shift'] for m in self.doppler_measurements]

                ax2.clear()
                ax2.plot(times, dopplers, 'b.-')
                ax2.set_xlabel('Time (seconds)')
                ax2.set_ylabel('Doppler Shift (Hz)')
                ax2.set_title('Doppler Shift vs Time')
                ax2.grid(True)

            plt.pause(0.01)
            time.sleep(0.1)

        plt.ioff()
        self.save_results()

    def save_results(self):
        filename = f"doppler_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'frequency', 'doppler_shift', 'peak_power']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for measurement in self.doppler_measurements:
                writer.writerow({
                    'timestamp': measurement['timestamp'].isoformat(),
                    'frequency': measurement['frequency'],
                    'doppler_shift': measurement['doppler_shift'],
                    'peak_power': measurement['peak_power']
                })

        print(f"Data saved to {filename}")
        return filename