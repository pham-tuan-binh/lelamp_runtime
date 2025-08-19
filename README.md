# LeLamp Runtime

![](./assets/images/Banner.png)

This repository holds the code for controlling LeLamp. The runtime provides a comprehensive control system for the robotic lamp, including motor control, recording/replay functionality, voice interaction, and testing capabilities.

[LeLamp](https://github.com/humancomputerlab/LeLamp) is an open source robot lamp based on [Apple's Elegnt](https://machinelearning.apple.com/research/elegnt-expressive-functional-movement), made by [[Human Computer Lab]](https://www.humancomputerlab.com/)

## Overview

LeLamp Runtime is a Python-based control system that interfaces with the hardware components of LeLamp including:

- Servo motors for articulated movement
- Audio system (microphone and speaker)
- RGB LED lighting
- Camera system
- Voice interaction capabilities

## Project Structure

```
lelamp_runtime/
├── main.py                 # Main runtime entry point
├── pyproject.toml         # Project configuration and dependencies
├── lelamp/                # Core package
│   ├── setup_motors.py    # Motor configuration and setup
│   ├── calibrate.py       # Motor calibration utilities
│   ├── record.py          # Movement recording functionality
│   ├── replay.py          # Movement replay functionality
│   ├── app/               # Application modules
│   │   └── voice/         # Voice interaction system
│   ├── follower/          # Follower mode functionality
│   ├── leader/            # Leader mode functionality
│   └── test/              # Hardware testing modules
└── uv.lock               # Dependency lock file
```

## Installation

### Prerequisites

- UV package manager
- Hardware components properly assembled (see main LeLamp documentation)

### Setup

1. Clone the runtime repository:

```bash
git clone https://github.com/humancomputerlab/lelamp_runtime.git
cd lelamp_runtime
```

2. Install UV (if not already installed):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Install dependencies:

```bash
# For basic functionality
uv sync

# For hardware support (Raspberry Pi)
uv sync --extra hardware
```

**Note**: For motor setup and control, LeLamp Runtime can run on your computer and you only need to run `uv sync`. For other functionality that connects to the head Pi (LED control, audio, camera), you need to install LeLamp Runtime on that Pi and run `uv sync --extra hardware`.

If you have LFS problems, run the following command:

```bash
GIT_LFS_SKIP_SMUDGE=1 uv sync
```

If your installation process is slow, use the following environment variable:

```bash
export UV_CONCURRENT_DOWNLOADS=1
```

### Dependencies

The runtime includes several key dependencies:

- **feetech-servo-sdk**: For servo motor control
- **lerobot**: Robotics framework integration
- **livekit-agents**: Real-time voice interaction
- **numpy**: Mathematical operations
- **sounddevice**: Audio input/output
- **adafruit-circuitpython-neopixel**: RGB LED control (hardware)
- **rpi-ws281x**: Raspberry Pi LED control (hardware)

## Core Functionality

### 1. Motor Setup and Calibration

Before using LeLamp, you need to set up and calibrate the servo motors:

1. **Find the servo driver port**:

```bash
uv run lerobot-find-port
```

2. **Setup motors with unique IDs**:

```bash
uv run -m lelamp.setup_motors --id your_lamp_name --port the_port_found_in_previous_step
```

### 2. Unit Testing

The runtime includes comprehensive testing modules to verify all hardware components:

#### RGB LEDs

```bash
# Run with sudo for hardware access
sudo uv run -m lelamp.test.test_rgb
```

#### Audio System (Microphone and Speaker)

```bash
uv run -m lelamp.test.test_audio
```

#### Camera

```bash
# Test camera functionality
libcamera-hello
```

#### Motors

```bash
uv run -m lelamp.test.test_motors --id your_lamp_name --port the_port_found_in_previous_step
```

This can be run on your computer instead of the Raspberry Pi Zero 2W in the lamp head.

### 3. Record and Replay Episodes

One of LeLamp's key features is the ability to record and replay movement sequences:

#### Recording Movement

To record a movement sequence:

```bash
uv run -m lelamp.record --id your_lamp_name --port the_port_found_in_previous_step --name movement_sequence_name
```

This will:

- Put the lamp in recording mode
- Allow you to manually manipulate the lamp
- Save the movement data to a CSV file

#### Replaying Movement

To replay a recorded movement:

```bash
uv run -m lelamp.replay --id your_lamp_name --port the_port_found_in_previous_step --csv movement_sequence_name_lampid.csv
```

The replay system will:

- Load the movement data from the CSV file
- Execute the recorded movements with proper timing
- Reproduce the original motion sequence

#### File Format

Recorded movements are saved as CSV files with the naming convention:
`{sequence_name}_{lamp_id}.csv`

## Sample Apps

Sample apps to test LeLamp's capabilities.

### LiveKit Voice Agent

To run a conversational agent on LeLamp, create a .env file with the following content in the root of this directory in your raspberry pi:

```bash
OPENAI_API_KEY=
LIVEKIT_URL=
LIVEKIT_API_KEY=
LIVEKIT_API_SECRET=
```

On how to gather these information, please refer to [LiveKit's guide](https://docs.livekit.io/agents/start/voice-ai/).

Then you can run the agent app by:

```bash
# Only need to run this once
uv run -m lelamp.app.voice.agent download-files

# For conversational AI
uv run -m lelamp.app.voice.agent console
```

## Troubleshooting

### Common Issues

1. **Servo Connection Issues**:

   - Verify USB connection to servo driver
   - Check port permissions
   - Ensure proper power supply
   - Ensure your servo have the right ID

2. **Audio Problems**:

   - Verify ReSpeaker Hat installation
   - Check ALSA configuration
   - Test with `aplay -l` and `arecord -l`
   - Ensure you have unmuted your speaker by hitting M on the corresponding slider in alsamixer.

3. **Permission Errors**:

   - Run RGB tests with `sudo`
   - Check user permissions for hardware access

## Contributing

This is an open-source project by Human Computer Lab. Contributions are welcome through the GitHub repository.

## License

Check the main [LeLamp repository](https://github.com/humancomputerlab/LeLamp) for licensing information.
