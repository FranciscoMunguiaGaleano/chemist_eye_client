import pyrealsense2 as rs

def get_intrinsics():
    # Configurar el pipeline de la cámara
    pipeline = rs.pipeline()
    config = rs.config()

    # Activar el stream de color
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # Iniciar el pipeline
    pipeline_profile = pipeline.start(config)

    try:
        # Obtener la cámara intrínseca para el stream de color
        color_stream = pipeline_profile.get_stream(rs.stream.color)  # Obtener el perfil del stream
        intrinsics = color_stream.as_video_stream_profile().get_intrinsics()

        # Mostrar los parámetros intrínsecos
        print("Parámetros intrínsecos de la cámara:")
        print(f"  Width: {intrinsics.width}")
        print(f"  Height: {intrinsics.height}")
        print(f"  Focal length (fx, fy): ({intrinsics.fx}, {intrinsics.fy})")
        print(f"  Principal point (cx, cy): ({intrinsics.ppx}, {intrinsics.ppy})")
        print(f"  Distortion model: {intrinsics.model}")
        print(f"  Distortion coefficients: {intrinsics.coeffs}")
    finally:
        # Detener el pipeline
        pipeline.stop()

if __name__ == "__main__":
    get_intrinsics()

