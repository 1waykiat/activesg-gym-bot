from GymDataTracker import GymDataTracker

def main():
    try:
        tracker = GymDataTracker()
        tracker.run()
    except Exception as e:
        print("An error occured: ", e)

# Run Tracker
main()
