from maintracker import DopplerTracker  # replace with your actual file name

# Initialize tracker for Iridium 120
tracker = DopplerTracker()


# Begin tracking
tracker.run_tracking(duration_minutes=15, update_interval=0.5)