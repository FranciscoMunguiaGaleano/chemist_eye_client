import cv2
import pyrealsense2 as rs
import numpy as np
import base64
import requests

# Initialize RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()

# Configure RealSense to stream color and depth
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# Start pipeline with configuration
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()

# Access sensors
depth_sensor = device.query_sensors()[0]
rgb_sensor = device.query_sensors()[1]

# Disable auto exposure for depth sensor (important for white surfaces)
depth_sensor.set_option(rs.option.enable_auto_exposure, False)

# Enable auto exposure for RGB sensor
rgb_sensor.set_option(rs.option.enable_auto_exposure, True)

# Start streaming from the RealSense camera
pipeline.start(config)

# Function to encode the image as base64
def encode_image_to_base64(image):
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')

# Function to send data to the server
def send_data(image_base64, pixel_distance_array):
    url = 'http://192.168.1.XXX:5000/uploadthree'  # Replace with your server IP and port
    data = {
        'image': image_base64,
        'distance_array': pixel_distance_array.tolist()
    }
    response = requests.post(url, json=data)

try:
    while True:
        # Wait for a new set of frames
        frames = pipeline.wait_for_frames()

        # Get color and depth frames
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        if not color_frame or not depth_frame:
            continue

        # Convert color frame to numpy array (OpenCV format)
        color_image = np.asanyarray(color_frame.get_data())

        # Convert depth frame to numpy array
        depth_image = np.asanyarray(depth_frame.get_data())

        # Prepare an array to store pixel and distance data
        pixel_distance_array = []

        # Iterate over the image and get distance for each pixel
        for y in range(0, depth_image.shape[0], 10):  # Step by 10 for efficiency
            for x in range(0, depth_image.shape[1], 10):
                distance = depth_frame.get_distance(x, y)
                pixel_distance_array.append([x, y, distance])

        # Convert the list to a NumPy array
        pixel_distance_array = np.array(pixel_distance_array)

        # Encode the color image as base64
        image_base64 = encode_image_to_base64(color_image)

        # Send data to the server
        send_data(image_base64, pixel_distance_array)

        # Display the color image
        #cv2.imshow("RealSense Color Image", color_image)

        # Break the loop if 'Esc' key is pressed
        #if cv2.waitKey(1) & 0xFF == 27:
        #    break

finally:
    # Stop the RealSense pipeline
    pipeline.stop()
    cv2.destroyAllWindows()

