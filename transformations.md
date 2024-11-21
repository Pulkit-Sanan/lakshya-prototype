### Transformations Overview

The targeting system involves several transformations to ensure precise alignment and targeting. These steps include camera calibration, distortion removal, 3D projection, transformations between static and movable cameras, and re-projection to the image plane. Below is the explanation of these steps, added to the README:

---

### Transformations and Their Role

#### 1. **Camera Calibration**
   - **Purpose**: To determine intrinsic and extrinsic parameters of both cameras, enabling correction for lens distortion and mapping 3D world points to 2D image points accurately.
   - **Steps**:
     1. A checkerboard pattern is used to calibrate the cameras by detecting corner points.
     2. Intrinsic parameters (`camera_matrix`), distortion coefficients (`dist`), rotation vectors (`rvecs`), and translation vectors (`tvecs`) are computed using OpenCV's `cv2.calibrateCamera()`.

   - **Outputs**:
     - `camera_matrix`: Internal parameters like focal lengths and optical center.
     - `dist`: Lens distortion coefficients for correcting fisheye or barrel distortions.
     - Parameters are saved for future use in `.pkl` files.

#### 2. **Removing Distortion**
   - **Purpose**: To eliminate lens distortion from images to ensure straight lines in the real world remain straight in the image.
   - **Steps**:
     - Compute an optimal camera matrix using OpenCV's `cv2.getOptimalNewCameraMatrix()`.
     - Apply `cv2.undistort()` to rectify images.

   - **Usage**:
     - Each frame captured by the static and movable cameras is undistorted before further processing.

#### 3. **Projection to 3D Coordinates**
   - **Purpose**: To map 2D bounding box centers in the image to 3D world coordinates for better spatial understanding.
   - **Steps**:
     1. Use the intrinsic matrix to back-project 2D points into 3D space at a fixed depth.
     2. Normalize image coordinates using the camera's focal length and optical center.

   - **Formula**:
     \[
     X = \frac{(x - c_x)}{f_x} \cdot Z, \quad Y = \frac{(y - c_y)}{f_y} \cdot Z, \quad Z = \text{Fixed Depth}
     \]
     Where \( (x, y) \) is the bounding box center, \( (f_x, f_y) \) are the focal lengths, and \( (c_x, c_y) \) is the optical center.

#### 4. **Transforming to Movable Camera**
   - **Purpose**: To map 3D coordinates from the static camera's frame of reference to the movable camera's.
   - **Steps**:
     - Apply a translation vector representing the relative position of the cameras.
   - **Formula**:
     \[
     \text{Point}_{\text{movable}} = \text{Point}_{\text{static}} + \text{Translation Vector}
     \]

#### 5. **Reprojection to 2D Image Plane**
   - **Purpose**: To project the 3D point back onto the image plane of the movable camera for targeting.
   - **Steps**:
     - Use the intrinsic matrix of the movable camera to re-project the transformed 3D point into the image space.

   - **Formula**:
     \[
     \begin{bmatrix} u \\ v \\ w \end{bmatrix} = \text{Camera Matrix} \cdot \begin{bmatrix} X \\ Y \\ Z \end{bmatrix}, \quad (u, v) = \left(\frac{u}{w}, \frac{v}{w}\right)
     \]

#### 6. **Bounding Box Transformation and Display**
   - The bounding box center from the static camera is transformed into the movable camera's view.
   - The target is marked on the movable camera's feed using a circle overlay.

By combining these transformations, the system achieves precise alignment of the movable camera with the detected target, ensuring accurate targeting.