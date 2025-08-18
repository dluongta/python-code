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

    # Mở video đầu vào
    cap = cv2.VideoCapture(input_video_path)

    # Lấy thông tin về video
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Tạo video writer để lưu video đầu ra
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # Di chuyển đến thời gian bắt đầu
    cap.set(cv2.CAP_PROP_POS_MSEC, start_time * 1000)

    # Cắt và ghi video
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Kiểm tra xem đã đến thời gian kết thúc chưa
        current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        if current_time >= end_time:
            break

        # Ghi frame vào video đầu ra
        out.write(frame)

    # Giải phóng tài nguyên
    cap.release()
    out.release()

# Ví dụ sử dụng hàm
input_video_path = 'input.mp4'
start_time = 0  # Bắt đầu từ giây thứ 10
end_time = 3    # Kết thúc tại giây thứ 20
output_video_path = 'output.mp4'

cut_videos(input_video_path, start_time, end_time, output_video_path)