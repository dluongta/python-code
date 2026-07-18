import cv2

def cut_videos(input_video_path, start_time, end_time, output_video_path):
    """
    Cắt ghép video từ một đoạn video đã cho.

    Args:
        input_video_path (str): Đường dẫn đến video đầu vào.
        start_time (float): Thời gian bắt đầu cắt (giây).
        end_time (float): Thời gian kết thúc cắt (giây).
        output_video_path (str): Đường dẫn đến video đầu ra.
    """

    cap = cv2.VideoCapture(input_video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    cap.set(cv2.CAP_PROP_POS_MSEC, start_time * 1000)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        if current_time >= end_time:
            break

        out.write(frame)

    cap.release()
    out.release()

input_video_path = 'input.mp4'
start_time = 0 
end_time = 3    
output_video_path = 'output.mp4'

cut_videos(input_video_path, start_time, end_time, output_video_path)