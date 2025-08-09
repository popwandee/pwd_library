"""
PWD Vision Works - Hailo AI Processor Examples
ตัวอย่างการใช้งาน Hailo8 AI processor สำหรับ object detection

Author: PWD Vision Works
Version: 1.0.0
"""

import cv2
import numpy as np
import time
import logging
from pathlib import Path
from typing import List

# Import PWD Library modules
from pwd_library.model.hailo8_processor import (
    Hailo8Processor, 
    HailoModelManager, 
    HailoHealthMonitor,
    benchmark_inference,
    detect_hailo_devices
)
from pwd_library.image_processing.preprocessor import ImagePreprocessor
from pwd_library.utils.exceptions import HailoError, handle_exception
from pwd_library.utils.drawing_utils import draw_detections

# ตั้งค่า logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def setup_sample_data():
    """
    สร้างข้อมูลตัวอย่างสำหรับทดสอบ
    """
    # สร้างโฟลเดอร์
    Path("output").mkdir(exist_ok=True)
    Path("models").mkdir(exist_ok=True)
    Path("sample_images").mkdir(exist_ok=True)
    
    # สร้างภาพตัวอย่าง (ถ้าไม่มี)
    sample_images = []
    for i in range(5):
        img_path = f"sample_images/sample_{i}.jpg"
        
        if not Path(img_path).exists():
            # สร้างภาพตัวอย่าง (สีสุ่ม)
            height, width = 480, 640
            image = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
            
            # เพิ่มข้อความ
            cv2.putText(image, f"Sample Image {i}", 
                       (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            # วาดรูปทรงง่าย ๆ
            cv2.rectangle(image, (100, 100), (200, 200), (0, 255, 0), 3)
            cv2.circle(image, (400, 300), 50, (0, 0, 255), 3)
            
            cv2.imwrite(img_path, image)
        
        sample_images.append(img_path)
    
    return sample_images


def example_model_management():
    """
    ตัวอย่างการจัดการโมเดล Hailo
    """
    print("=== Model Management Example ===")
    
    # เริ่มต้น model manager
    model_manager = HailoModelManager("models/")
    
    # แสดงโมเดลที่มีอยู่
    available_models = model_manager.list_available_models()
    print(f"Available models: {available_models}")
    
    # ถ้าไม่มีโมเดล ให้แสดงคำแนะนำ
    if not available_models:
        print("\n⚠️  No Hailo models found!")
        print("To use this example, please:")
        print("1. Download a Hailo model (.hef file)")
        print("2. Place it in the 'models/' directory")
        print("3. Common models: YOLOv8, YOLOv5, SSD MobileNet")
        print("4. Visit: https://hailo.ai/developer-zone/")
        return None
    
    # เลือกโมเดลแรก
    model_name = available_models[0]
    print(f"Using model: {model_name}")
    
    try:
        # ตรวจสอบโมเดล
        model_path = model_manager.get_model_path(model_name)
        model_info = model_manager.validate_model(model_path)
        
        print(f"Model info:")
        print(f"  Path: {model_info['path']}")
        print(f"  Size: {model_info['size_bytes'] / 1024 / 1024:.2f} MB")
        print(f"  Valid: {model_info['valid']}")
        
        return str(model_path)
        
    except Exception as e:
        logger.error(f"Model management failed: {e}")
        return None


def example_basic_inference(model_path: str, sample_images: List[str]):
    """
    ตัวอย่างการทำ inference แบบพื้นฐาน
    """
    print("\n=== Basic Inference Example ===")
    
    if not model_path:
        print("⚠️ No model available for inference")
        return False
    
    try:
        # เริ่มต้น processor
        with Hailo8Processor(model_path, batch_size=1) as processor:
            print(f"Model loaded successfully: {Path(model_path).name}")
            
            # ทดสอบกับภาพตัวอย่าง
            for img_path in sample_images[:3]:  # ใช้แค่ 3 ภาพแรก
                print(f"\nProcessing: {img_path}")
                
                # อ่านภาพ
                image = cv2.imread(img_path)
                if image is None:
                    print(f"❌ Cannot read image: {img_path}")
                    continue
                
                print(f"Image shape: {image.shape}")
                
                # ทำ inference
                start_time = time.perf_counter()
                results = processor.predict(image)
                end_time = time.perf_counter()
                
                inference_time = end_time - start_time
                print(f"Inference time: {inference_time*1000:.2f}ms")
                print(f"Found {len(results)} detection(s)")
                
                # แสดงผลลัพธ์
                for i, detection in enumerate(results):
                    print(f"  Detection {i+1}: {detection}")
                
                # วาดผลลัพธ์บนภาพ
                output_image = draw_detections(image.copy(), results)
                
                # บันทึกผลลัพธ์
                output_path = f"output/result_{Path(img_path).stem}.jpg"
                cv2.imwrite(output_path, output_image)
                print(f"Result saved: {output_path}")
            
            # แสดงสถิติ
            stats = processor.get_performance_stats()
            print(f"\nPerformance Statistics:")
            print(f"Total inferences: {stats['total_inferences']}")
            print(f"Average time: {stats['avg_inference_time']*1000:.2f}ms")
            print(f"Average FPS: {stats['fps']:.2f}")
            print(f"Error rate: {stats['error_rate']:.2%}")
            
    except HailoError as e:
        logger.error(f"Hailo inference failed: {e}")
        return False
    
    return True


def example_batch_processing(model_path: str, sample_images: List[str]):
    """
    ตัวอย่างการประมวลผลแบบ batch
    """
    print("\n=== Batch Processing Example ===")
    
    if not model_path:
        print("⚠️ No model available for batch processing")
        return False
    
    try:
        # เริ่มต้น processor สำหรับ batch
        with Hailo8Processor(model_path, batch_size=4) as processor:
            
            # โหลดภาพทั้งหมด
            images = []
            valid_paths = []
            
            for img_path in sample_images:
                image = cv2.imread(img_path)
                if image is not None:
                    images.append(image)
                    valid_paths.append(img_path)
            
            if not images:
                print("❌ No valid images for batch processing")
                return False
            
            print(f"Processing batch of {len(images)} images...")
            
            # ทำ batch inference
            start_time = time.perf_counter()
            batch_results = processor.batch_predict(images)
            end_time = time.perf_counter()
            
            total_time = end_time - start_time
            avg_time_per_image = total_time / len(images)
            
            print(f"Batch processing completed:")
            print(f"Total time: {total_time:.3f}s")
            print(f"Average per image: {avg_time_per_image*1000:.2f}ms")
            print(f"Batch FPS: {len(images)/total_time:.2f}")
            
            # ประมวลผลและบันทึกผลลัพธ์
            for i, (results, image, img_path) in enumerate(zip(batch_results, images, valid_paths)):
                print(f"\nImage {i+1} ({Path(img_path).name}):")
                print(f"  Detections: {len(results)}")
                
                # วาดผลลัพธ์
                output_image = draw_detections(image.copy(), results)
                output_path = f"output/batch_result_{i+1}.jpg"
                cv2.imwrite(output_path, output_image)
                
                print(f"  Saved: {output_path}")
    
    except HailoError as e:
        logger.error(f"Batch processing failed: {e}")
        return False
    
    return True


def example_performance_benchmark(model_path: str, sample_images: List[str]):
    """
    ตัวอย่างการ benchmark ประสิทธิภาพ
    """
    print("\n=== Performance Benchmark Example ===")
    
    if not model_path:
        print("⚠️ No model available for benchmarking")
        return False
    
    try:
        # เริ่มต้น processor
        processor = Hailo8Processor(model_path)
        processor.load_model()
        
        # เตรียมภาพทดสอบ
        test_images = []
        for img_path in sample_images:
            image = cv2.imread(img_path)
            if image is not None:
                test_images.append(image)
        
        if not test_images:
            print("❌ No images available for benchmark")
            return False
        
        print(f"Running benchmark with {len(test_images)} test images...")
        
        # รัน benchmark
        benchmark_results = benchmark_inference(
            processor, 
            test_images, 
            iterations=50  # ทำ 50 ครั้ง
        )
        
        print(f"\nBenchmark Results:")
        print(f"Iterations: {benchmark_results['iterations']}")
        print(f"Successful: {benchmark_results['successful']}")
        print(f"Failed: {benchmark_results['failed']}")
        print(f"Average time: {benchmark_results['avg_time_ms']:.2f}ms")
        print(f"Min time: {benchmark_results['min_time_ms']:.2f}ms")
        print(f"Max time: {benchmark_results['max_time_ms']:.2f}ms")
        print(f"FPS: {benchmark_results['fps']:.2f}")
        print(f"Error rate: {benchmark_results['error_rate']:.2%}")
        
        # Cleanup
        processor.cleanup()
        
    except HailoError as e:
        logger.error(f"Benchmark failed: {e}")
        return False
    
    return True


def example_preprocessing_integration(sample_images: List[str]):
    """
    ตัวอย่างการรวม preprocessing กับ Hailo processing
    """
    print("\n=== Preprocessing Integration Example ===")
    
    # สร้าง preprocessor
    preprocessor = ImagePreprocessor(target_size=(640, 640))
    
    for img_path in sample_images[:2]:
        print(f"\nProcessing: {img_path}")
        
        # อ่านภาพ
        original = cv2.imread(img_path)
        if original is None:
            continue
        
        print(f"Original shape: {original.shape}")
        
        # แสดงขั้นตอน preprocessing ต่าง ๆ
        steps = [
            ("Original", original),
            ("Resized with padding", None),
            ("Normalized", None),
            ("Enhanced contrast", None),
            ("Noise reduction", None)
        ]
        
        # ทำ preprocessing ตามขั้นตอน
        processed = original.copy()
        
        # Resize with padding
        processed = preprocessor.resize_with_padding(processed, (640, 640))
        steps[1] = ("Resized with padding", processed.copy())
        
        # Normalize (แปลงกลับเพื่อแสดงผล)
        normalized = preprocessor.normalize(processed, method="zero_one")
        display_normalized = (normalized * 255).astype(np.uint8)
        steps[2] = ("Normalized", display_normalized)
        
        # Enhance contrast
        enhanced = preprocessor.enhance_contrast(processed, method="clahe")
        steps[3] = ("Enhanced contrast", enhanced)
        
        # Noise reduction
        denoised = preprocessor.apply_noise_reduction(enhanced, method="bilateral")
        steps[4] = ("Noise reduction", denoised)
        
        # บันทึกผลลัพธ์แต่ละขั้นตอน
        for i, (step_name, image) in enumerate(steps):
            if image is not None:
                filename = f"output/preprocess_{Path(img_path).stem}_step{i}_{step_name.lower().replace(' ', '_')}.jpg"
                cv2.imwrite(filename, image)
                print(f"  {step_name}: {filename}")


def example_health_monitoring(model_path: str, sample_images: List[str]):
    """
    ตัวอย่างการติดตามสุขภาพระบบ
    """
    print("\n=== Health Monitoring Example ===")
    
    if not model_path:
        print("⚠️ No model available for health monitoring")
        return False
    
    try:
        # สร้าง health monitor
        monitor = HailoHealthMonitor()
        
        with Hailo8Processor(model_path) as processor:
            
            print("Running inference with health monitoring...")
            
            for i, img_path in enumerate(sample_images):
                image = cv2.imread(img_path)
                if image is None:
                    continue
                
                try:
                    start_time = time.perf_counter()
                    results = processor.predict(image)
                    end_time = time.perf_counter()
                    
                    inference_time = end_time - start_time
                    
                    # บันทึกข้อมูลสำเร็จ
                    monitor.log_inference(success=True, inference_time=inference_time)
                    
                    print(f"Image {i+1}: ✅ Success ({inference_time*1000:.1f}ms)")
                    
                except Exception as e:
                    # บันทึกข้อมูลล้มเหลว
                    monitor.log_inference(success=False)
                    print(f"Image {i+1}: ❌ Failed - {e}")
            
            # ตรวจสอบสุขภาพระบบ
            health_info = monitor.check_system_health()
            print(f"\nSystem Health Check:")
            print(f"Status: {health_info['status']}")
            print(f"Device available: {health_info['device_available']}")
            
            # แสดงสถิติ
            stats = monitor.get_stats()
            print(f"\nMonitoring Statistics:")
            print(f"Total inferences: {stats['total_inferences']}")
            print(f"Errors: {stats['errors']}")  
            print(f"Success rate: {stats['success_rate']:.2%}")
            print(f"Average FPS: {stats['avg_fps']:.2f}")
            
    except HailoError as e:
        logger.error(f"Health monitoring failed: {e}")
        return False
    
    return True


def main():
    """
    รันตัวอย่างทั้งหมด
    """
    print("PWD Vision Works - Hailo AI Examples")
    print("=" * 50)
    
    # ตรวจสอบอุปกรณ์ Hailo
    print("Detecting Hailo devices...")
    devices = detect_hailo_devices()
    
    if not devices:
        print("⚠️ No Hailo devices found!")
        print("Make sure you have:")
        print("1. Hailo8 device connected")
        print("2. HailoRT software installed")
        print("3. Proper drivers loaded")
        print("\nContinuing with mock examples...")
        
    else:
        print(f"✅ Found {len(devices)} Hailo device(s)")
        for device in devices:
            print(f"  Device: {device}")
    
    # เตรียมข้อมูลตัวอย่าง
    print("\nPreparing sample data...")
    sample_images = setup_sample_data()
    print(f"✅ Sample images ready: {len(sample_images)} files")
    
    # จัดการโมเดล
    model_path = example_model_management()
    
    # รันตัวอย่างต่าง ๆ
    examples = [
        ("Preprocessing Integration", lambda: example_preprocessing_integration(sample_images)),
    ]
    
    # เพิ่มตัวอย่างที่ต้องใช้โมเดล (ถ้ามี)
    if model_path:
        examples.extend([
            ("Basic Inference", lambda: example_basic_inference(model_path, sample_images)),
            ("Batch Processing", lambda: example_batch_processing(model_path, sample_images)),
            ("Performance Benchmark", lambda: example_performance_benchmark(model_path, sample_images)),
            ("Health Monitoring", lambda: example_health_monitoring(model_path, sample_images)),
        ])
    
    results = {}
    
    for name, example_func in examples:
        print(f"\n{'='*20} {name} {'='*20}")
        
        try:
            success = example_func()
            results[name] = "✅ Success" if success else "❌ Failed"
            
        except KeyboardInterrupt:
            print(f"\n⏹️ {name} interrupted by user")
            results[name] = "⏹️ Interrupted"
            break
            
        except Exception as e:
            error_msg = handle_exception(e, default_return=f"Error: {type(e).__name__}")
            results[name] = f"❌ {error_msg}"
    
    # แสดงผลสรุป
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    for name, result in results.items():
        print(f"{name:<25}: {result}")
    
    print(f"\nOutput files saved to: output/")
    
    if not model_path:
        print(f"\n💡 Tip: To test full AI functionality:")
        print(f"   1. Download Hailo models from https://hailo.ai/")
        print(f"   2. Place .hef files in models/ directory")
        print(f"   3. Re-run this example")


if __name__ == "__main__":
    main()