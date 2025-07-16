import cv2, argparse
import numpy as np
from os import listdir, path

if not path.isfile('face_detection/detection/sfd/s3fd.pth'):
	raise FileNotFoundError('Save the s3fd model to face_detection/detection/sfd/s3fd.pth \
							before running this script!')
import face_detection  # 导入专用的人脸检测库

parser = argparse.ArgumentParser()
parser.add_argument('--ngpu', help='Number of GPUs across which to run in parallel', default=1, type=int)
args = parser.parse_args()


def detect_face_in_frame(video_path, target_frame=10):
    """
    检测视频中指定帧的人脸区域大小
    :param video_path: 视频文件路径
    :param target_frame: 目标帧序号（默认第10帧）
    """
    # 初始化视频捕获对象
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("错误：无法打开视频文件")
        return
    
    # 设置目标帧位置（帧序号从0开始）
    cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame - 1)  # 第10帧对应索引9
    
    # 读取目标帧
    ret, frame = cap.read()
    if not ret:
        print("错误：无法读取目标帧")
        cap.release()
        return
    
    
    fa = [face_detection.FaceAlignment(face_detection.LandmarksType._2D, flip_input=False, 
			 device='cuda:{}'.format(id)) for id in range(args.ngpu)]
    
    # 执行人脸检测
	
    pred = fa[0].get_detections_for_batch(np.asarray([frame]))

    if pred is None:
        cap.release()
        return 0
    elif len(pred)<1:
        cap.release()
        return 0
    else:
        x1, y1, x2, y2 = pred[0]
        width = x2 - x1  # 计算人脸宽度
        height = y2 - y1  # 计算人脸高度
        print(f"  人脸位置({int(x1)}, {int(y1)}), 尺寸={int(width)}x{int(height)}")       
    
    # 释放资源
    cap.release()
    return min(width, height)

if __name__ == "__main__":
    video_file = "raw_data/00001.mp4"  # 替换为你的视频路径
    num = detect_face_in_frame(video_file)
    print(num)