import pyrealsense2 as rs

# 파이프라인 생성
pipeline = rs.pipeline()

# 구성 설정
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# 스트리밍 시작
profile = pipeline.start(config)

# 스트림에서 color stream 프로파일 가져오기
color_profile = profile.get_stream(rs.stream.color)
color_intrinsics = color_profile.as_video_stream_profile().get_intrinsics()

# intrinsics 값 출력
print("Color Sensor Intrinsics:")
print(f"Width: {color_intrinsics.width}")
print(f"Height: {color_intrinsics.height}")
print(f"PPX (principal point X): {color_intrinsics.ppx}")
print(f"PPY (principal point Y): {color_intrinsics.ppy}")
print(f"FX (focal length X): {color_intrinsics.fx}")
print(f"FY (focal length Y): {color_intrinsics.fy}")
print(f"Distortion Model: {color_intrinsics.model}")
print(f"Distortion Coefficients: {color_intrinsics.coeffs}")

# 스트리밍 종료
pipeline.stop()








# import pyrealsense2 as rs

# # Create a context object. This object owns the handles to all connected realsense devices
# context = rs.context()


# # pipeline = rs.pipeline()
# # config = rs.config()

# # Get the list of connected devices
# devices = context.query_devices()

# if not devices:
#     print("No device connected")
# else:
#     for dev in devices:
#         print(f"Device found: {dev.get_info(rs.camera_info.name)}")
#         print(f"Serial number: {dev.get_info(rs.camera_info.serial_number)}")
#         print(f"Firmware version: {dev.get_info(rs.camera_info.firmware_version)}")
#         sensors = dev.query_sensors()
#         for sensor in sensors:
#             print(f"Sensor: {sensor.get_info(rs.camera_info.name)}")
#             ##########################################
#             # Device found: Intel RealSense D435I
#             # Serial number: 030522070636
#             # Firmware version: 5.16.0.1
#             # Sensor: Stereo Module
#             # Sensor: RGB Camera
#             # Sensor: Motion Module
#             #########################################
            
#             # Get the list of available stream profiles
#             stream_profiles = sensor.get_stream_profiles()
#             for s_profile in stream_profiles:
#                 if s_profile.stream_type() in [rs.stream.color, rs.stream.infrared, rs.stream.depth]:
#                     # print(s_profile)
#                     intrinsics = s_profile.as_video_stream_profile().get_intrinsics()
#                     # print(s_profile)
#                     # print(intrinsics)
                    
# print("------------------------------------------")
# print(devices[0].query_sensors())
# # [<pyrealsense2.sensor: "Stereo Module">, <pyrealsense2.sensor: "RGB Camera">, <pyrealsense2.sensor: "Motion Module">]
# # print(type(devices[0].query_sensors()))

# # print(devices[0].query_sensors()[1].get_stream_profiles())
# print("------------------------------------------")

# color_format = rs.format.bgr8
# img_size_x = 640
# img_size_y = 480

# for s_profile in devices[0].query_sensors()[1].get_stream_profiles():
#     vprofile = s_profile.as_video_stream_profile()
#     video_intrinsics = vprofile.get_intrinsics()
#     print(video_intrinsics.width)
#     try :
#         if (vprofile.format() == color_format and video_intrinsics.width == img_size_x and video_intrinsics.height == img_size_y) :
#             print(s_profile.stream_type)
#             intrinsics = vprofile.get_intrinsics()
#             print(f"Stream type: {s_profile.stream_type()}")
#             print(f"  Width: {intrinsics.width}")
#             print(f"  Height: {intrinsics.height}")
#             print(f"  Focal Length (fx): {intrinsics.fx}")
#             print(f"  Focal Length (fy): {intrinsics.fy}")
#             print(f"  Principal Point (ppx): {intrinsics.ppx}")
#             print(f"  Principal Point (ppy): {intrinsics.ppy}")
#             print(f"  Distortion Model: {intrinsics.model}")
#             print(f"  Distortion Coefficients: {intrinsics.coeffs}")
#     except :
#         pass
                    

        # for sensor in sensors:
        #     print(f"Sensor: {sensor.get_info(rs.camera_info.name)}")

        #     # Filter for the color sensor
        #     if sensor.get_info(rs.camera_info.name) == "RGB Camera":
        #         stream_profiles = sensor.get_stream_profiles()
                
        #         # Define the desired format and size
        #         desired_format = rs.format.bgr8
        #         desired_width = 640
        #         desired_height = 480
                
        #         for s_profile in stream_profiles:
        #             if s_profile.stream_type() == rs.stream.color:
        #                 vprofile = s_profile.as_video_stream_profile()
        #                 intrinsics = vprofile.get_intrinsics()
                        
        #                 if (vprofile.format() == desired_format and
        #                         intrinsics.width == desired_width and
        #                         intrinsics.height == desired_height):
        #                     print(f"Stream type: {s_profile.stream_type()}")
        #                     print(f"  Width: {intrinsics.width}")
        #                     print(f"  Height: {intrinsics.height}")
        #                     print(f"  Focal Length (fx): {intrinsics.fx}")
        #                     print(f"  Focal Length (fy): {intrinsics.fy}")
        #                     print(f"  Principal Point (ppx): {intrinsics.ppx}")
        #                     print(f"  Principal Point (ppy): {intrinsics.ppy}")
        #                     print(f"  Distortion Model: {intrinsics.model}")
        #                     print(f"  Distortion Coefficients: {intrinsics.coeffs}")
                    
                    
########################################################################################
#s_profile print data
# <pyrealsense2.[video_]stream_profile: Infrared(1) 1280x720 @ 6fps Y8>
# <pyrealsense2.[video_]stream_profile: Infrared(1) 848x480 @ 10fps Y8>
# <pyrealsense2.[video_]stream_profile: Infrared(1) 848x480 @ 8fps Y8>
# <pyrealsense2.[video_]stream_profile: Infrared(1) 848x480 @ 6fps Y8>
# <pyrealsense2.[video_]stream_profile: Infrared(1) 640x480 @ 30fps Y8>
# <pyrealsense2.[video_]stream_profile: Infrared(1) 640x480 @ 15fps Y8>
# <pyrealsense2.[video_]stream_profile: Infrared(1) 640x480 @ 6fps Y8>
# <pyrealsense2.[video_]stream_profile: Infrared(1) 640x360 @ 30fps Y8>
# <pyrealsense2.[video_]stream_profile: Infrared(1) 480x270 @ 60fps Y8>
# <pyrealsense2.[video_]stream_profile: Infrared(1) 480x270 @ 30fps Y8>
# <pyrealsense2.[video_]stream_profile: Infrared(1) 480x270 @ 15fps Y8>
# <pyrealsense2.[video_]stream_profile: Infrared(1) 480x270 @ 6fps Y8>
# <pyrealsense2.[video_]stream_profile: Infrared(2) 1280x720 @ 6fps Y8>
# <pyrealsense2.[video_]stream_profile: Infrared(2) 848x480 @ 10fps Y8>
# <pyrealsense2.[video_]stream_profile: Infrared(2) 848x480 @ 8fps Y8>
# <pyrealsense2.[video_]stream_profile: Infrared(2) 848x480 @ 6fps Y8>
# <pyrealsense2.[video_]stream_profile: Infrared(2) 640x480 @ 30fps Y8>
# <pyrealsense2.[video_]stream_profile: Infrared(2) 640x480 @ 15fps Y8>
# <pyrealsense2.[video_]stream_profile: Infrared(2) 640x480 @ 6fps Y8>
# <pyrealsense2.[video_]stream_profile: Infrared(2) 640x360 @ 30fps Y8>
# <pyrealsense2.[video_]stream_profile: Infrared(2) 480x270 @ 60fps Y8>
# <pyrealsense2.[video_]stream_profile: Infrared(2) 480x270 @ 30fps Y8>
# <pyrealsense2.[video_]stream_profile: Infrared(2) 480x270 @ 15fps Y8>
# <pyrealsense2.[video_]stream_profile: Infrared(2) 480x270 @ 6fps Y8>
# <pyrealsense2.[video_]stream_profile: Depth(0) 1280x720 @ 6fps Z16>
# <pyrealsense2.[video_]stream_profile: Depth(0) 848x480 @ 10fps Z16>
# <pyrealsense2.[video_]stream_profile: Depth(0) 848x480 @ 8fps Z16>
# <pyrealsense2.[video_]stream_profile: Depth(0) 848x480 @ 6fps Z16>
# <pyrealsense2.[video_]stream_profile: Depth(0) 640x480 @ 30fps Z16>
# <pyrealsense2.[video_]stream_profile: Depth(0) 640x480 @ 15fps Z16>
# <pyrealsense2.[video_]stream_profile: Depth(0) 640x480 @ 6fps Z16>
# <pyrealsense2.[video_]stream_profile: Depth(0) 640x360 @ 30fps Z16>
# <pyrealsense2.[video_]stream_profile: Depth(0) 480x270 @ 60fps Z16>
# <pyrealsense2.[video_]stream_profile: Depth(0) 480x270 @ 30fps Z16>
# <pyrealsense2.[video_]stream_profile: Depth(0) 480x270 @ 15fps Z16>
# <pyrealsense2.[video_]stream_profile: Depth(0) 480x270 @ 6fps Z16>
# <pyrealsense2.[video_]stream_profile: Depth(0) 256x144 @ 90fps Z16>
# Sensor: RGB Camera
# <pyrealsense2.[video_]stream_profile: Color(0) 1920x1080 @ 8fps RGB8>
# <pyrealsense2.[video_]stream_profile: Color(0) 1920x1080 @ 8fps Y16>
# <pyrealsense2.[video_]stream_profile: Color(0) 1920x1080 @ 8fps Y8>
# <pyrealsense2.[video_]stream_profile: Color(0) 1920x1080 @ 8fps BGRA8>
# <pyrealsense2.[video_]stream_profile: Color(0) 1920x1080 @ 8fps RGBA8>
# <pyrealsense2.[video_]stream_profile: Color(0) 1920x1080 @ 8fps BGR8>
# <pyrealsense2.[video_]stream_profile: Color(0) 1920x1080 @ 8fps YUYV>
# <pyrealsense2.[video_]stream_profile: Color(0) 1280x720 @ 15fps RGB8>
# <pyrealsense2.[video_]stream_profile: Color(0) 1280x720 @ 15fps Y16>
# <pyrealsense2.[video_]stream_profile: Color(0) 1280x720 @ 15fps Y8>
# <pyrealsense2.[video_]stream_profile: Color(0) 1280x720 @ 15fps BGRA8>
# <pyrealsense2.[video_]stream_profile: Color(0) 1280x720 @ 15fps RGBA8>
# <pyrealsense2.[video_]stream_profile: Color(0) 1280x720 @ 15fps BGR8>
# <pyrealsense2.[video_]stream_profile: Color(0) 1280x720 @ 15fps YUYV>
# <pyrealsense2.[video_]stream_profile: Color(0) 1280x720 @ 10fps RGB8>
# <pyrealsense2.[video_]stream_profile: Color(0) 1280x720 @ 10fps Y16>
# <pyrealsense2.[video_]stream_profile: Color(0) 1280x720 @ 10fps Y8>
# <pyrealsense2.[video_]stream_profile: Color(0) 1280x720 @ 10fps BGRA8>
# <pyrealsense2.[video_]stream_profile: Color(0) 1280x720 @ 10fps RGBA8>
# <pyrealsense2.[video_]stream_profile: Color(0) 1280x720 @ 10fps BGR8>
# <pyrealsense2.[video_]stream_profile: Color(0) 1280x720 @ 10fps YUYV>
# <pyrealsense2.[video_]stream_profile: Color(0) 1280x720 @ 6fps RGB8>
# <pyrealsense2.[video_]stream_profile: Color(0) 1280x720 @ 6fps Y16>
# <pyrealsense2.[video_]stream_profile: Color(0) 1280x720 @ 6fps Y8>
# <pyrealsense2.[video_]stream_profile: Color(0) 1280x720 @ 6fps BGRA8>
# <pyrealsense2.[video_]stream_profile: Color(0) 1280x720 @ 6fps RGBA8>
# <pyrealsense2.[video_]stream_profile: Color(0) 1280x720 @ 6fps BGR8>
# <pyrealsense2.[video_]stream_profile: Color(0) 1280x720 @ 6fps YUYV>
# <pyrealsense2.[video_]stream_profile: Color(0) 640x480 @ 30fps RGB8>
# <pyrealsense2.[video_]stream_profile: Color(0) 640x480 @ 30fps Y16>
# <pyrealsense2.[video_]stream_profile: Color(0) 640x480 @ 30fps Y8>
# <pyrealsense2.[video_]stream_profile: Color(0) 640x480 @ 30fps BGRA8>
# <pyrealsense2.[video_]stream_profile: Color(0) 640x480 @ 30fps RGBA8>
# <pyrealsense2.[video_]stream_profile: Color(0) 640x480 @ 30fps BGR8>
# <pyrealsense2.[video_]stream_profile: Color(0) 640x480 @ 30fps YUYV>
# <pyrealsense2.[video_]stream_profile: Color(0) 640x480 @ 15fps RGB8>
# <pyrealsense2.[video_]stream_profile: Color(0) 640x480 @ 15fps Y16>
# <pyrealsense2.[video_]stream_profile: Color(0) 640x480 @ 15fps Y8>
# <pyrealsense2.[video_]stream_profile: Color(0) 640x480 @ 15fps BGRA8>
# <pyrealsense2.[video_]stream_profile: Color(0) 640x480 @ 15fps RGBA8>
# <pyrealsense2.[video_]stream_profile: Color(0) 640x480 @ 15fps BGR8>
# <pyrealsense2.[video_]stream_profile: Color(0) 640x480 @ 15fps YUYV>
# <pyrealsense2.[video_]stream_profile: Color(0) 640x480 @ 6fps RGB8>
# <pyrealsense2.[video_]stream_profile: Color(0) 640x480 @ 6fps Y16>
# <pyrealsense2.[video_]stream_profile: Color(0) 640x480 @ 6fps Y8>
# <pyrealsense2.[video_]stream_profile: Color(0) 640x480 @ 6fps BGRA8>
# <pyrealsense2.[video_]stream_profile: Color(0) 640x480 @ 6fps RGBA8>
# <pyrealsense2.[video_]stream_profile: Color(0) 640x480 @ 6fps BGR8>
# <pyrealsense2.[video_]stream_profile: Color(0) 640x480 @ 6fps YUYV>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 60fps RGB8>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 60fps Y16>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 60fps Y8>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 60fps BGRA8>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 60fps RGBA8>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 60fps BGR8>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 60fps YUYV>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 30fps RGB8>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 30fps Y16>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 30fps Y8>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 30fps BGRA8>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 30fps RGBA8>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 30fps BGR8>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 30fps YUYV>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 15fps RGB8>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 15fps Y16>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 15fps Y8>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 15fps BGRA8>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 15fps RGBA8>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 15fps BGR8>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 15fps YUYV>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 6fps RGB8>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 6fps Y16>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 6fps Y8>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 6fps BGRA8>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 6fps RGBA8>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 6fps BGR8>
# <pyrealsense2.[video_]stream_profile: Color(0) 424x240 @ 6fps YUYV>
########################################################################################
# [ 1280x720  p[648.584 357.623]  f[635.299 635.299]  Brown Conrady [0 0 0 0 0] ]
# [ 848x480  p[429.687 238.425]  f[420.886 420.886]  Brown Conrady [0 0 0 0 0] ]
# [ 848x480  p[429.687 238.425]  f[420.886 420.886]  Brown Conrady [0 0 0 0 0] ]
# [ 848x480  p[429.687 238.425]  f[420.886 420.886]  Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[325.151 238.574]  f[381.18 381.18]  Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[325.151 238.574]  f[381.18 381.18]  Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[325.151 238.574]  f[381.18 381.18]  Brown Conrady [0 0 0 0 0] ]
# [ 640x360  p[324.292 178.811]  f[317.65 317.65]  Brown Conrady [0 0 0 0 0] ]
# [ 480x270  p[243.219 134.109]  f[238.237 238.237]  Brown Conrady [0 0 0 0 0] ]
# [ 480x270  p[243.219 134.109]  f[238.237 238.237]  Brown Conrady [0 0 0 0 0] ]
# [ 480x270  p[243.219 134.109]  f[238.237 238.237]  Brown Conrady [0 0 0 0 0] ]
# [ 480x270  p[243.219 134.109]  f[238.237 238.237]  Brown Conrady [0 0 0 0 0] ]
# [ 1280x720  p[648.584 357.623]  f[635.299 635.299]  Brown Conrady [0 0 0 0 0] ]
# [ 848x480  p[429.687 238.425]  f[420.886 420.886]  Brown Conrady [0 0 0 0 0] ]
# [ 848x480  p[429.687 238.425]  f[420.886 420.886]  Brown Conrady [0 0 0 0 0] ]
# [ 848x480  p[429.687 238.425]  f[420.886 420.886]  Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[325.151 238.574]  f[381.18 381.18]  Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[325.151 238.574]  f[381.18 381.18]  Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[325.151 238.574]  f[381.18 381.18]  Brown Conrady [0 0 0 0 0] ]
# [ 640x360  p[324.292 178.811]  f[317.65 317.65]  Brown Conrady [0 0 0 0 0] ]
# [ 480x270  p[243.219 134.109]  f[238.237 238.237]  Brown Conrady [0 0 0 0 0] ]
# [ 480x270  p[243.219 134.109]  f[238.237 238.237]  Brown Conrady [0 0 0 0 0] ]
# [ 480x270  p[243.219 134.109]  f[238.237 238.237]  Brown Conrady [0 0 0 0 0] ]
# [ 480x270  p[243.219 134.109]  f[238.237 238.237]  Brown Conrady [0 0 0 0 0] ]
# [ 1280x720  p[648.584 357.623]  f[635.299 635.299]  Brown Conrady [0 0 0 0 0] ]
# [ 848x480  p[429.687 238.425]  f[420.886 420.886]  Brown Conrady [0 0 0 0 0] ]
# [ 848x480  p[429.687 238.425]  f[420.886 420.886]  Brown Conrady [0 0 0 0 0] ]
# [ 848x480  p[429.687 238.425]  f[420.886 420.886]  Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[325.151 238.574]  f[381.18 381.18]  Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[325.151 238.574]  f[381.18 381.18]  Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[325.151 238.574]  f[381.18 381.18]  Brown Conrady [0 0 0 0 0] ]
# [ 640x360  p[324.292 178.811]  f[317.65 317.65]  Brown Conrady [0 0 0 0 0] ]
# [ 480x270  p[243.219 134.109]  f[238.237 238.237]  Brown Conrady [0 0 0 0 0] ]
# [ 480x270  p[243.219 134.109]  f[238.237 238.237]  Brown Conrady [0 0 0 0 0] ]
# [ 480x270  p[243.219 134.109]  f[238.237 238.237]  Brown Conrady [0 0 0 0 0] ]
# [ 480x270  p[243.219 134.109]  f[238.237 238.237]  Brown Conrady [0 0 0 0 0] ]
# [ 256x144  p[136.584 69.6229]  f[635.299 635.299]  Brown Conrady [0 0 0 0 0] ]
# Sensor: RGB Camera
# [ 1920x1080  p[959.834 553.174]  f[1373.28 1374]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 1920x1080  p[959.834 553.174]  f[1373.28 1374]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 1920x1080  p[959.834 553.174]  f[1373.28 1374]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 1920x1080  p[959.834 553.174]  f[1373.28 1374]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 1920x1080  p[959.834 553.174]  f[1373.28 1374]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 1920x1080  p[959.834 553.174]  f[1373.28 1374]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 1920x1080  p[959.834 553.174]  f[1373.28 1374]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 1280x720  p[639.889 368.783]  f[915.523 915.998]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 1280x720  p[639.889 368.783]  f[915.523 915.998]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 1280x720  p[639.889 368.783]  f[915.523 915.998]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 1280x720  p[639.889 368.783]  f[915.523 915.998]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 1280x720  p[639.889 368.783]  f[915.523 915.998]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 1280x720  p[639.889 368.783]  f[915.523 915.998]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 1280x720  p[639.889 368.783]  f[915.523 915.998]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 1280x720  p[639.889 368.783]  f[915.523 915.998]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 1280x720  p[639.889 368.783]  f[915.523 915.998]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 1280x720  p[639.889 368.783]  f[915.523 915.998]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 1280x720  p[639.889 368.783]  f[915.523 915.998]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 1280x720  p[639.889 368.783]  f[915.523 915.998]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 1280x720  p[639.889 368.783]  f[915.523 915.998]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 1280x720  p[639.889 368.783]  f[915.523 915.998]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 1280x720  p[639.889 368.783]  f[915.523 915.998]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 1280x720  p[639.889 368.783]  f[915.523 915.998]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 1280x720  p[639.889 368.783]  f[915.523 915.998]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 1280x720  p[639.889 368.783]  f[915.523 915.998]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 1280x720  p[639.889 368.783]  f[915.523 915.998]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 1280x720  p[639.889 368.783]  f[915.523 915.998]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 1280x720  p[639.889 368.783]  f[915.523 915.998]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[319.926 245.855]  f[610.349 610.666]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[319.926 245.855]  f[610.349 610.666]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[319.926 245.855]  f[610.349 610.666]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[319.926 245.855]  f[610.349 610.666]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[319.926 245.855]  f[610.349 610.666]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[319.926 245.855]  f[610.349 610.666]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[319.926 245.855]  f[610.349 610.666]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[319.926 245.855]  f[610.349 610.666]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[319.926 245.855]  f[610.349 610.666]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[319.926 245.855]  f[610.349 610.666]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[319.926 245.855]  f[610.349 610.666]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[319.926 245.855]  f[610.349 610.666]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[319.926 245.855]  f[610.349 610.666]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[319.926 245.855]  f[610.349 610.666]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[319.926 245.855]  f[610.349 610.666]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[319.926 245.855]  f[610.349 610.666]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[319.926 245.855]  f[610.349 610.666]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[319.926 245.855]  f[610.349 610.666]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[319.926 245.855]  f[610.349 610.666]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[319.926 245.855]  f[610.349 610.666]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 640x480  p[319.926 245.855]  f[610.349 610.666]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
# [ 424x240  p[211.963 122.928]  f[305.174 305.333]  Inverse Brown Conrady [0 0 0 0 0] ]
########################################################################################