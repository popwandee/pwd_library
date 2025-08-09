"""
PWD Vision Works - Camera Usage Examples
ตัวอย่างการใช้งานระบบกล้องใน PWD Library

Author: PWD Vision Works
Version: 1.0.0
"""

import cv2
import time
import logging
from pathlib import Path

# Import PWD Library modules
from pwd_library.camera.picamera2_cm3 import (
    PiCameraManager, 
    CameraHealthMonitor, 
    detect_available_cameras,
    capture_test_image
)
from pwd_library.utils.exceptions import CameraError, handle_exception

# ตั้งค่า logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def example_basic_camera_usage():
    """
    ตัวอย่างการใช้งานกล้องแบบพื้นฐาน
    """
    print("=== Basic Camera Usage Example ===")
    
    try:
        # เริ่มต้นกล้อง
        with PiCameraManager() as camera:
            # เริ่มต้นกล้องด้วยการตั้งค่าต่าง ๆ
            camera.initialize_camera(
                resolution=(1920, 1080),
                framerate=30
            )
            
            # จับภาพเดี่ยว
            print("Capturing single image...")
            image = camera.capture_image()
            print(f"Captured image shape: {image.shape}")
            
            # บันทึกภาพ
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
            
            filename = output_dir / "captured_image.jpg"
            camera.capture_to_file(str(filename))
            print(f"Image saved to: {filename}")
            
            # แสดงภาพที่จับได้
            cv2.imshow("Captured Image", image)
            cv2.waitKey(2000)  # แสดง 2 วินาที
            cv2.destroyAllWindows()
            
    except CameraError as e:
        logger.error(f"Camera error occurred: {e}")
        return False
    
    return True


def example_video_streaming():
    """
    ตัวอย่างการ streaming video จากกล้อง
    """
    print("\n=== Video Streaming Example ===")
    
    try:
        with PiCameraManager() as camera:
            # เริ่ม video streaming
            camera.start_video_stream(resolution=(640, 480), framerate=30)
            
            print("Starting video stream... Press 'q' to quit")
            
            # สร้าง health monitor
            monitor = CameraHealthMonitor()
            
            frame_count = 0
            start_time = time.time()
            
            while True:
                try:
                    # ดึงเฟรม
                    frame = camera.get_frame()
                    frame_count += 1
                    
                    # บันทึกสถิติ
                    monitor.log_frame_capture(success=True)
                    
                    # แสดงข้อมูล FPS บนภาพ
                    current_fps = frame_count / (time.time() - start_time)
                    cv2.putText(frame, f"FPS: {current_fps:.1f}", 
                              (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    # แสดงผล
                    cv2.imshow("Video Stream", frame)
                    
                    # ตรวจสอบการกดปุ่ม
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        break
                    elif key == ord('s'):
                        # บันทึกเฟรมปัจจุบัน
                        save_path = f"output/frame_{frame_count:04d}.jpg"
                        cv2.imwrite(save_path, frame)
                        print(f"Frame saved: {save_path}")
                        
                except Exception as e:
                    monitor.log_frame_capture(success=False)
                    logger.warning(f"Frame capture failed: {e}")
                    continue
            
            cv2.destroyAllWindows()
            
            # แสดงสถิติ
            stats = monitor.get_stats()
            print(f"\nStreaming Statistics:")
            print(f"Total frames: {stats['total_frames']}")
            print(f"Errors: {stats['errors']}")
            print(f"Success rate: {stats['success_rate']:.2%}")
            print(f"Average FPS: {stats['avg_fps']:.2f}")
            
    except CameraError as e:
        logger.error(f"Video streaming failed: {e}")
        return False
    
    return True


def example_camera_controls():
    """
    ตัวอย่างการควบคุมการตั้งค่ากล้อง
    """
    print("\n=== Camera Controls Example ===")
    
    try:
        with PiCameraManager() as camera:
            camera.initialize_camera()
            
            # แสดงข้อมูลกล้อง
            properties = camera.get_camera_properties()
            print(f"Camera properties: {properties}")
            
            # ทดสอบการตั้งค่าต่าง ๆ
            print("Testing different camera settings...")
            
            settings_tests = [
                {
                    "name": "Default Settings",
                    "exposure_time": None,
                    "iso": None,
                    "brightness": 0.0
                },
                {
                    "name": "Bright Settings", 
                    "exposure_time": 20000,
                    "iso": 100,
                    "brightness": 0.2
                },
                {
                    "name": "Low Light Settings",
                    "exposure_time": 50000,
                    "iso": 800,
                    "brightness": -0.1
                }
            ]
            
            for setting in settings_tests:
                print(f"\nTesting: {setting['name']}")
                
                # ตั้งค่า exposure
                camera.set_exposure_settings(
                    exposure_time=setting["exposure_time"],
                    iso=setting["iso"],
                    brightness=setting["brightness"]
                )
                
                # รอให้การตั้งค่าใช้ผล
                time.sleep(1)
                
                # จับภาพทดสอบ
                image = camera.capture_image()
                
                # บันทึกภาพ
                filename = f"output/test_{setting['name'].lower().replace(' ', '_')}.jpg"
                cv2.imwrite(filename, image)
                print(f"Test image saved: {filename}")
            
            # ทดสอบ white balance
            print("\nTesting white balance modes...")
            wb_modes = ["auto", "daylight", "tungsten", "fluorescent"]
            
            for mode in wb_modes:
                camera.set_white_balance(mode)
                time.sleep(1)
                
                image = camera.capture_image()
                filename = f"output/wb_{mode}.jpg"
                cv2.imwrite(filename, image)
                print(f"White balance {mode}: {filename}")
            
    except CameraError as e:
        logger.error(f"Camera controls test failed: {e}")
        return False
    
    return True


def example_performance_optimization():
    """
    ตัวอย่างการปรับแต่งประสิทธิภาพ
    """
    print("\n=== Performance Optimization Example ===")
    
    try:
        with PiCameraManager() as camera:
            camera.initialize_camera(resolution=(1280, 720), framerate=60)
            
            # เปิดใช้งานการปรับแต่งประสิทธิภาพ
            camera.optimize_for_performance()
            
            print("Running performance test...")
            
            # วัดประสิทธิภาพการจับภาพ
            num_frames = 100
            times = []
            
            for i in range(num_frames):
                start_time = time.perf_counter()
                image = camera.capture_image()
                end_time = time.perf_counter()
                
                capture_time = end_time - start_time
                times.append(capture_time)
                
                if (i + 1) % 20 == 0:
                    avg_time = sum(times) / len(times)
                    fps = 1.0 / avg_time
                    print(f"Progress: {i+1}/{num_frames}, Avg FPS: {fps:.2f}")
            
            # แสดงผลสถิติ
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            fps = 1.0 / avg_time
            
            print(f"\nPerformance Results:")
            print(f"Average capture time: {avg_time*1000:.2f}ms")
            print(f"Min capture time: {min_time*1000:.2f}ms") 
            print(f"Max capture time: {max_time*1000:.2f}ms")
            print(f"Average FPS: {fps:.2f}")
            
    except CameraError as e:
        logger.error(f"Performance test failed: {e}")
        return False
    
    return True


def example_error_handling():
    """
    ตัวอย่างการจัดการ error
    """
    print("\n=== Error Handling Example ===")
    
    # ทดสอบการจัดการ error ต่าง ๆ
    test_cases = [
        {
            "name": "Invalid camera number",
            "camera_num": 99,  # กล้องที่ไม่มี
            "expected_error": "Camera initialization"
        },
        {
            "name": "Invalid resolution", 
            "camera_num": 0,
            "resolution": (10000, 10000),  # ความละเอียดที่ใหญ่เกินไป
            "expected_error": "Camera configuration"
        }
    ]
    
    for test in test_cases:
        print(f"\nTesting: {test['name']}")
        
        try:
            camera = PiCameraManager(camera_num=test["camera_num"])
            
            if "resolution" in test:
                camera.initialize_camera(resolution=test["resolution"])
            else:
                camera.initialize_camera()
                
            # ถ้าไม่เกิด error แสดงว่าการทดสอบไม่สำเร็จ
            print(f"❌ Expected error but succeeded")
            camera.cleanup()
            
        except CameraError as e:
            print(f"✅ Caught expected error: {e.error_code} - {e.message}")
            
        except Exception as e:
            # จัดการ error ด้วย utility function
            result = handle_exception(e, default_return=None, raise_on_critical=False)
            print(f"✅ Handled unexpected error: {type(e).__name__}")


def main():
    """
    รันตัวอย่างทั้งหมด
    """
    print("PWD Vision Works - Camera Examples")
    print("=" * 50)
    
    # ตรวจสอบกล้องที่มีอยู่
    print("Detecting available cameras...")
    cameras = detect_available_cameras()
    
    if not cameras:
        print("❌ No cameras found!")
        print("Make sure you have:")
        print("1. Raspberry Pi Camera connected and enabled")
        print("2. picamera2 library installed")
        print("3. Camera interface enabled in raspi-config")
        return
    
    print(f"✅ Found {len(cameras)} camera(s)")
    for i, cam in enumerate(cameras):
        print(f"  Camera {i}: {cam}")
    
    # สร้างโฟลเดอร์ output
    Path("output").mkdir(exist_ok=True)
    
    # รันตัวอย่างต่าง ๆ
    examples = [
        ("Basic Camera Usage", example_basic_camera_usage),
        ("Camera Controls", example_camera_controls),
        ("Performance Optimization", example_performance_optimization),
        ("Video Streaming", example_video_streaming),
        ("Error Handling", example_error_handling),
    ]
    
    results = {}
    
    for name, example_func in examples:
        print(f"\n{'='*20} {name} {'='*20}")
        
        try:
            success = example_func()
            results[name] = "✅ Success" if success else "❌ Failed"
            
        except KeyboardInterrupt:
            print(f"\n⏹️  {name} interrupted by user")
            results[name] = "⏹️ Interrupted"
            break
            
        except Exception as e:
            logger.error(f"Example {name} failed with unexpected error: {e}")
            results[name] = f"❌ Error: {type(e).__name__}"
    
    # แสดงผลสรุป
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    for name, result in results.items():
        print(f"{name:<25}: {result}")
    
    print(f"\nOutput files saved to: output/")


if __name__ == "__main__":
    main()