import pyrealsense2 as rs

# Create a context object. This object owns the handles to all connected realsense devices
context = rs.context()

# Get the list of connected devices
devices = context.query_devices()

if not devices:
    print("No device connected")
else:
    for dev in devices:
        print(f"Device found: {dev.get_info(rs.camera_info.name)}")
        print(f"Serial number: {dev.get_info(rs.camera_info.serial_number)}")
        print(f"Firmware version: {dev.get_info(rs.camera_info.firmware_version)}")

        # Get the list of sensors
        sensors = dev.query_sensors()
        for sensor in sensors:
            print(f"Sensor: {sensor.get_info(rs.camera_info.name)}")

            # Get the list of available stream profiles
            stream_profiles = sensor.get_stream_profiles()
            for profile in stream_profiles:
                vprofile = profile.as_video_stream_profile()
                print(f"Stream type: {profile.stream_type()} - Format: {profile.format()} - Width: {vprofile.width()} - Height: {vprofile.height()} - FPS: {vprofile.fps()}")

            # Print sensor options
            sensor_options = sensor.get_supported_options()
            for option in sensor_options:
                try:
                    option_description = sensor.get_option_description(option)
                    option_value = sensor.get_option(option)
                    print(f"Option: {option} - {option_description}")
                    print(f"Current Value: {option_value}")
                except RuntimeError as e:
                    print(f"Option: {option} - Not supported")


# import pyrealsense2 as rs

# # Create a context object. This object owns the handles to all connected realsense devices
# context = rs.context()

# # Get the list of connected devices
# devices = context.query_devices()

# if not devices:
#     print("No device connected")
# else:
#     for dev in devices:
#         print(f"Device found: {dev.get_info(rs.camera_info.name)}")
#         print(f"Serial number: {dev.get_info(rs.camera_info.serial_number)}")
#         print(f"Firmware version: {dev.get_info(rs.camera_info.firmware_version)}")

#         # Get the list of sensors
#         sensors = dev.query_sensors()
#         for sensor in sensors:
#             print(f"Sensor: {sensor.get_info(rs.camera_info.name)}")

#             # Get the list of available stream profiles
#             stream_profiles = sensor.get_stream_profiles()
#             for profile in stream_profiles:
#                 vprofile = profile.as_video_stream_profile()
#                 print(f"Stream type: {profile.stream_type()} - Format: {profile.format()} - Width: {vprofile.width()} - Height: {vprofile.height()} - FPS: {vprofile.fps()}")
                
#                 # Additional sensor details if available
#                 if profile.stream_type() == rs.stream.color:
#                     print("This is the RGB sensor")
#                 elif profile.stream_type() == rs.stream.infrared:
#                     print("This is one of the Infrared sensors")
#                 elif profile.stream_type() == rs.stream.depth:
#                     print("This is the Depth sensor")


