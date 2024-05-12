import cv2
import time
import numpy as np

# cam2 depth  frame
# cam4 origin frame
lists = []

def nonzero_test(img) :
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127,255, cv2.THRESH_BINARY)
    
    if ret : 
        nonzero = thresh.nonzero()
        print(f'first : {nonzero[0].shape}')
        print(f'second : {nonzero[1].shape}')


def nonzero_test2() :
    arr = np.array([
        [0,1,2,3],
        [2,2,2,3],
        [6,0,0,0]
    ])
    
    # print(arr.shape)
    # print(arr.nonzero())
    bool_nonzero_0 = arr.nonzero()[0]
    
    goods = (bool_nonzero_0>1).nonzero()[0]
    print(goods)


def nonzero_test3() :
    arr = np.array([
        [0,1,2,3,6,6,3,2,1],
        [2,2,2,3,3,3,5,2,0],
        [6,0,0,0,2,2,0,0,0],
        [6,0,3,3,0,2,0,9,1]
    ])

    
    nonzero = arr.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])
    
    mini_box_y_low = 2
    mini_box_y_high = 3
    
    mini_box_x_low = 3
    mini_box_x_high = 5
    
    targetx = ((nonzerox >= mini_box_x_low) & (nonzerox <= mini_box_x_high))
    targety = ((nonzeroy >= mini_box_y_low) & (nonzeroy <= mini_box_y_high))
    target = ((nonzeroy >= mini_box_y_low) & (nonzeroy <= mini_box_y_high) & (nonzerox >= mini_box_x_low) & (nonzerox <= mini_box_x_high))
    # target of target is [[0,2,2][3,0,2]]
    ### 전체 배열에 대해서 boolean값이 리턴됨.
    ### nonzero x,y 둘다 nonzero연산 값이 25개라서, 25개의 boolean값이 나오는데,
    ### nonzerox 에 대한 대소비교와 nonzeroy에 대한 대소비교 개수가 정확하게 일치하기 때문에 이런 결과가 나올 수 있는거.
    ### 따라서 line detection에서 nonzerox[lists]한건, 정확하게 ture인 값만 받아올 수 있기 때문임.
    
        
    print(f'x : {targetx}')
    print(f'y : {targety}')
    
    print(f'target : {target}')
    # [False False False False False False False False False False False False
    # False False False False False  True  True False False  True  True False
    # False]
    # print(len(target))
    # print(target.nonzero()[0])
    # [17 18 21 22]

    
        
def list_test() :
    global lists
    
    arr = np.array([
        [0,1,2,3],
        [2,2,2,3],
        [6,0,0,9]
    ])

    arr_test = (arr>2)
    bool_nonzero_0 = arr_test.nonzero()[0]
    # print(arr_test)
    # [[False False False  True]
    #  [False False False  True]
    #  [ True False False  True]]
    
    # print(bool_nonzero_0)
    # (array([0, 1, 2, 2]), array([3, 3, 0, 3]))
    lists.append(bool_nonzero_0)
    
    
    print(arr_test[lists])
    
def list_test2() :
    arr = np.array([
        [0,1,2,3],
        [2,2,2,3],
        [6,0,0,9]
    ])
    
    arr2 = np.array([
        [0,0,1,2]
    ])
    
    print(f'speak {arr[arr2]}')
    


def main() :
    cap = cv2.VideoCapture(0)   
    print("passed cap")

    while True :
        ret, img = cap.read()

        if not ret :
            print("fail to connection")
            time.sleep(1)
        else :
            nonzero_test3()
            # list_test2()
            cv2.imshow("img", img)

            key = cv2.waitKey(1)
            if key == ord('q') :
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__" :
    main()