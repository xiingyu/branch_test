from ultralytics import YOLO
import numpy as np
import cv2
import time
import pyrealsense2 as rs

cam_num = 4

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth,1280,720, rs.format.z16, 30)
config.enable_stream(rs.stream.color,848,480, rs.format.bgr8, 30)


profile = pipeline.start(config)

depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()
clipping_distance_in_meters = 1 #1 meter
clipping_distance = clipping_distance_in_meters / depth_scale
align_to = rs.stream.color
align = rs.align(align_to)


def main() :
    # cap = cv2.VideoCapture(cam_num)
    
    # model = YOLO('door_knob.yaml')
    model = YOLO('best.pt')

    while True :
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()
        aligned_depth_frame = aligned_frames.get_depth_frame()

        img = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())
        
        depth_intrinsics = aligned_depth_frame.profile.as_video_stream_profile().intrinsics
        
        
        result = model.predict(img, conf= 0.5,verbose=False ) 
        print(result[0].boxes)
        annotated_img = result[0].plot()
        
        
        if len(result[0].boxes.cls) :
            print(result[0].boxes.cls)
            object_xy = np.array(result[0].boxes.xywh.detach().numpy().tolist()[0], dtype='int')
            
            # for r in result :
            #     print(r.boxes.xywh.detach().numpy().tolist()[0]) ###원래 이건데 대체했음.
            print(object_xy[0], object_xy[1]) ### 640 by 480 
            
            distance = depth_image[object_xy[1]][object_xy[0]] * depth_scale    
            # print(f'distance between cam and object is {depth_image[object_xy[1]][object_xy[0]]}')
            print(f'distance between cam and object is {distance:.4f} meters')
            
            annotated_img = cv2.circle(annotated_img,((object_xy[0]),(object_xy[1])),10,(0,0,255), -1, cv2.LINE_AA)
            # annotated_img = cv2.circle(annotated_img,((600),(400)),10,(255,0,0), -1, cv2.LINE_AA)
            depth = aligned_depth_frame.get_distance(object_xy[0], object_xy[1])
            depth_point = rs.rs2_deproject_pixel_to_point(depth_intrinsics, [object_xy[0], object_xy[1]], depth)
            cv2.putText(annotated_img, f"{depth_point[0]:.2f}m,  {depth_point[1]:.2f}m,  {depth_point[2]:.2f}m,", (30,30), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,255),2)
            print(f'{depth_point}')
        
        
        
        key = cv2.waitKey(1)
        # print(1/during_time)
        if key == ord('q') :
            break
        elif key == ord("s") :
            print("switch mode.")
            num = int(input("0~5, 6 is exit"))
            if(num == 0) :
                model = YOLO("/home/skh/ang_backup/src/pump_track/pump_track/army/army_b_5.pt")
            elif (num == 1 ) :
                model = YOLO("/home/skh/ang_backup/src/pump_track/pump_track/army/army_b_6.pt")
            
            elif (num == 2 ) :
                model = YOLO("/home/skh/ang_backup/src/pump_track/pump_track/army/army_b_7.pt")
                
            elif (num == 3 ) :
                model = YOLO("/home/skh/ang_backup/src/pump_track/pump_track/army/army_b_8.pt")
                
            elif (num == 4 ) :
                model = YOLO("/home/skh/ang_backup/src/pump_track/pump_track/chess/chess_b.pt")
                
            elif (num == 5 ) :
                model = YOLO("/home/skh/ang_backup/src/pump_track/pump_track/best_add_box.pt")
            else :
                pass
        
        
        cv2.imshow('real', img)
        cv2.imshow('yolo',annotated_img)
        
            
    cv2.destroyAllWindows()


if __name__ == "__main__" :
    main()