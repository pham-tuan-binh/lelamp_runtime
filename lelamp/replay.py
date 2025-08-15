import argparse
import csv
import time

from .follower import LeLampFollowerConfig, LeLampFollower
from lerobot.utils.robot_utils import busy_wait

def main():
    parser = argparse.ArgumentParser(description="Replay recorded actions from CSV file")
    parser.add_argument('--csv', type=str, required=True, help='Path to CSV file containing recorded data')
    parser.add_argument('--port', type=str, required=True, help='Serial port for the robot')
    parser.add_argument('--id', type=str, required=True, help='ID of the robot')
    parser.add_argument('--fps', type=int, default=30, help='Frames per second for replay (default: 30)')
    args = parser.parse_args()

    robot_config = LeLampFollowerConfig(port=args.port, id=args.id)
    robot = LeLampFollower(robot_config)
    robot.connect(calibrate=True)

    # Read CSV file and replay actions
    with open(args.csv, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        actions = list(csv_reader)
    
    print(f"Replaying {len(actions)} actions from {args.csv}")
    
    for row in actions:
        t0 = time.perf_counter()
        
        # Extract action data (exclude timestamp column)
        action = {key: float(value) for key, value in row.items() if key != 'timestamp'}
        robot.send_action(action)
        
        busy_wait(1.0 / args.fps - (time.perf_counter() - t0))
    
    robot.disconnect()

if __name__ == "__main__":
    main()