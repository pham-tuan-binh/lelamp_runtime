import argparse
from ..follower import LeLampFollowerConfig, LeLampFollower
  
def main():
    parser = argparse.ArgumentParser(description="Check motors status and position")
    parser.add_argument('--id', type=str, required=True, help='ID of the lamp')
    parser.add_argument('--port', type=str, required=True, help='Serial port for the lamp')
    args = parser.parse_args()

    robot_config = LeLampFollowerConfig(
        port=args.port,
        id=args.id,
    )

    robot = LeLampFollower(robot_config)
    robot.connect(calibrate=True)

    while True:
        try:
            obs = robot.get_observation()
            print(obs)
        except KeyboardInterrupt:
            print("Shutting down teleop...")
            break

if __name__ == "__main__":
    main()