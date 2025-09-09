#!/usr/bin/env python3
"""
Test script for AnimationService to verify all functionality works correctly.
"""

import argparse
import time
import threading
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from service.motors.animation_service import AnimationService


def test_animation_service(port, lamp_id, fps=30, duration=1.0, idle_recording="curious"):
    """Test the AnimationService functionality"""
    print("=== Testing AnimationService ===")
    
    # Create service
    service = AnimationService(
        port=port,
        lamp_id=lamp_id,
        fps=fps,
        duration=duration,
        idle_recording=idle_recording
    )
    
    try:
        print("1. Starting service...")
        service.start()
        time.sleep(2)  # Let idle play
        
        print("2. Testing available recordings...")
        recordings = service.get_available_recordings()
        print(f"   Available recordings: {recordings}")
        
        print("3. Testing single recording dispatch...")
        service.dispatch("play", "excited")
        time.sleep(2)  # Let it play briefly
        
        print("4. Testing interruption with another recording...")
        service.dispatch("play", "happy_wiggle")
        time.sleep(1)  # Let it play briefly
        
        print("5. Testing another interruption...")
        service.dispatch("play", "shock")
        time.sleep(2)  # Let it play briefly
        
        print("6. Testing return to idle after recording finishes...")
        time.sleep(3)  # Should return to idle and loop
        
        print("7. Testing rapid event dispatching...")
        for recording in ["nod", "headshake", "sad"]:
            if recording in recordings:
                print(f"   Dispatching {recording}...")
                service.dispatch("play", recording)
                time.sleep(0.5)  # Very brief play
        
        print("8. Testing idle recording dispatch...")
        service.dispatch("play", "curious")  # Dispatch idle itself
        time.sleep(2)
        
        print("9. Testing unknown event type...")
        service.dispatch("unknown_event", "test")  # Should be ignored
        
        print("10. Final idle test...")
        time.sleep(3)  # Should be playing idle continuously
        
        print("All tests completed successfully!")
        
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Stopping service...")
        service.stop()
        print("Service stopped.")


def test_interruption_timing(port, lamp_id, fps=30, duration=0.5, idle_recording="curious"):
    """Test rapid interruption to verify smooth transitions"""
    print("\n=== Testing Interruption Timing ===")
    
    service = AnimationService(
        port=port,
        lamp_id=lamp_id, 
        fps=fps,
        duration=duration,  # Very fast transitions
        idle_recording=idle_recording
    )
    
    try:
        service.start()
        time.sleep(1)
        
        print("Testing rapid interruptions...")
        recordings = ["excited", "happy_wiggle", "shock", "nod", "headshake"]
        
        for i, recording in enumerate(recordings):
            print(f"   {i+1}. Dispatching {recording}")
            service.dispatch("play", recording)
            time.sleep(0.2)  # Very brief play time
        
        print("Rapid interruption test completed!")
        time.sleep(2)
        
    except Exception as e:
        print(f"Interruption test failed: {e}")
    finally:
        service.stop()


def test_error_handling(port, lamp_id, fps=30, duration=1.0, idle_recording="curious"):
    """Test error handling with invalid recordings"""
    print("\n=== Testing Error Handling ===")
    
    service = AnimationService(
        port=port,
        lamp_id=lamp_id,
        fps=fps,
        duration=duration,
        idle_recording=idle_recording
    )
    
    try:
        service.start()
        time.sleep(1)
        
        print("Testing invalid recording name...")
        service.dispatch("play", "nonexistent_recording")
        time.sleep(1)
        
        print("Testing valid recording after error...")
        service.dispatch("play", "excited")
        time.sleep(2)
        
        print("Error handling test completed!")
        
    except Exception as e:
        print(f"Error handling test failed: {e}")
    finally:
        service.stop()


if __name__ == "__main__":
    print("Starting AnimationService tests...")
    print("Press Ctrl+C to stop tests early\n")
    
    try:
        # Parse arguments for main test
        parser = argparse.ArgumentParser(description="Test Animation Service")
        parser.add_argument('--id', type=str, required=True, help='ID of the lamp')
        parser.add_argument('--port', type=str, required=True, help='Serial port for the lamp')
        parser.add_argument('--fps', type=int, default=30, help='Frames per second (default: 30)')
        parser.add_argument('--duration', type=float, default=1.0, help='Transition duration in seconds (default: 1.0)')
        parser.add_argument('--idle', type=str, default='curious', help='Idle recording name (default: curious)')
        args = parser.parse_args()
        
        # Run all tests with parsed arguments
        test_animation_service(args.port, args.id, args.fps, args.duration, args.idle)
        test_interruption_timing(args.port, args.id, args.fps, 0.5, args.idle)
        test_error_handling(args.port, args.id, args.fps, args.duration, args.idle)
        
        print("\nAll tests completed successfully!")
        
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
    except Exception as e:
        print(f"\nTest suite failed: {e}")
        import traceback
        traceback.print_exc()
