import pyrealsense2 as rs
import numpy as np
import cv2

def main():

    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 424, 240, rs.format.bgr8, 15) # 해상도 / 프레임
    pipeline.start(config)

    while True :

        fs = pipeline.wait_for_frames()
        color_f = fs.get_color_frame()
        color_a = np.asanyarray(color_f.get_data())
        color_i = cv2.GaussianBlur(color_a, (5, 5), 0) # 블러 처리. 홀수만 가능.
        
        
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)) ## 추가된 부분
        cen_x = 212
        roi_start_row = int(240 * 0.35)
        roi_end_row = int(240 * 0.5)
        roi_start_col = int(424 * 0.05)
        roi_end_col = int(424 * 0.95)
        yellow_color = [0, 255, 255]
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)) ## 추가된 부분
        
        
        
        color_o = cv2.morphologyEx(color_i, cv2.MORPH_OPEN, kernel) ### 추가된 부분
        color_c = cv2.morphologyEx(color_o, cv2.MORPH_CLOSE, kernel) ### 추가된 부분
        
        hsv_i = cv2.cvtColor(color_c, cv2.COLOR_BGR2HSV)
        roi = hsv_i[roi_start_row:roi_end_row, roi_start_col:roi_end_col]

        mask = np.zeros_like(hsv_i)
        mask[roi_start_row:roi_end_row, roi_start_col:roi_end_col, :] = 255
        hsv_i = cv2.bitwise_and(hsv_i, mask)

        dominant_color = np.mean(roi, axis=(0, 1)) # ROI 내 평균 색상
        lower_bound = dominant_color - np.array([30, 70, 70]) # 하한/ 증가 = 초록색 더 인식 / 감소 = 초록색 덜 인식
        upper_bound = dominant_color + np.array([130, 255, 255]) # 상한/ 증가 = 진한 파란색 더 인식 / 감소 = 진한 파란색 덜 인식
        print(dominant_color, lower_bound, upper_bound)
        
        col_mask = cv2.inRange(roi, lower_bound, upper_bound)
        mask = col_mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        masked_pixel_count = 0
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 10: ## 추가된 부분
                component_mask = np.zeros_like(mask)
                cv2.drawContours(component_mask, [contour], -1, (255, 255, 0), thickness=cv2.FILLED)
                roi[component_mask > 0] = yellow_color
                masked_pixel_count += area
        
        hsv_i[roi_start_row:roi_end_row, roi_start_col:roi_end_col] = roi
        
        cv2.rectangle(hsv_i, (roi_start_col, roi_start_row), (roi_end_col, roi_end_row), (0, 255, 0), 2)
        cv2.line(hsv_i, (cen_x, roi_start_row), (cen_x, roi_end_row), (0, 0, 255), 2)

        left_mask = mask[:, :cen_x - roi_start_col].copy()
        right_mask = mask[:, cen_x - roi_start_col:].copy()

        l_area = np.sum(left_mask == 255)
        r_area = np.sum(right_mask == 255)

        cv2.putText(hsv_i, f"L Area: {l_area}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(hsv_i, f"R Area: {r_area}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        state_msg = 0

        L_AREA = 6876
        R_AREA = 6840
        # 추가한 부분


        hsv_i_cvt = cv2.cvtColor(hsv_i, cv2.COLOR_HSV2BGR)
        cv2.imshow('Track', hsv_i_cvt)
        cv2.imshow('test', color_c)
        print(state_msg)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pass
        
if __name__ == "__main__" :
    main()