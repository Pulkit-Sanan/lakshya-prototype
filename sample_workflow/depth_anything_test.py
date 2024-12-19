# from transformers import pipeline
# from PIL import Image
# import requests
# import torch
# import matplotlib.pyplot as plt
# import time

# # Check for GPU and set device index
# device = 0 if torch.cuda.is_available() else -1

# # Load pipeline with specified device
# pipe = pipeline(
#     task="depth-estimation",
#     model="depth-anything/Depth-Anything-V2-Metric-Indoor-Small-hf",
#     device=device,
#     depth_estimation_type = 'metric'
# )

# # Load image
# url = 'http://images.cocodataset.org/val2017/000000039769.jpg'
# image = Image.open(requests.get(url, stream=True).raw)
# # image = Image.open('./sample_workflow/test.jpg')

# start = time.time()  # Start timer

# # Perform inference
# result = pipe(image)

# # Retrieve depth result
# depth = result["depth"]
# end = time.time()  # End timer
# print(f"Time taken: {end - start:.4f}s")

# # Display the original and depth images
# plt.figure(figsize=(12, 6))

# # Original image
# plt.subplot(1, 2, 1)
# plt.imshow(image)
# plt.title("Original Image")
# plt.axis("off")

# # Depth map
# plt.subplot(1, 2, 2)
# plt.imshow(depth, cmap='inferno')
# plt.title("Depth Map")
# plt.axis("off")

# plt.show()


from transformers import pipeline
from PIL import Image
import torch
import cv2
import numpy as np
import time

# Check for GPU and set device index
device = 0 if torch.cuda.is_available() else -1

# Load pipeline with specified device
pipe = pipeline(
    task="depth-estimation",
    model="depth-anything/Depth-Anything-V2-Metric-Indoor-Small-hf",
    device=device,
    depth_estimation_type = 'metric'
)

# Start webcam capture
cap = cv2.VideoCapture(0)  # 0 is the default webcam

if not cap.isOpened():
    print("Error: Unable to access the webcam.")
    exit()

print("Press 'q' to quit.")

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to capture frame.")
        break

    # Convert frame to PIL image
    pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Perform inference
    start = time.time()
    result = pipe(pil_image)
    depth = result["depth"]
    end = time.time()
    print(f"Frame processed in {end - start:.4f}s")

    # Convert depth to numpy array for OpenCV
    depth_np = np.array(depth)

    # Normalize depth for visualization
    depth_normalized = cv2.normalize(
        depth_np, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U
    )
    depth_colormap = cv2.applyColorMap(depth_normalized, cv2.COLORMAP_INFERNO)

    # Display the original frame and depth map
    combined = np.hstack((frame, cv2.cvtColor(depth_colormap, cv2.COLOR_BGR2RGB)))
    cv2.imshow("Webcam (Left: Original, Right: Depth Map)", combined)

    # Quit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
