import cv2

def insert_video(main_video_path, insert_video_path, output_video_path, x, y, width, height):
    """Inserts a video into another video at specified coordinates.

    Args:
        main_video_path (str): Path to the main video file.
        insert_video_path (str): Path to the video to insert.
        output_video_path (str): Path to save the output video.
        x (int): X-coordinate of the top-left corner of the inserted video.
        y (int): Y-coordinate of the top-left corner of the inserted video.
        width (int): Width of the inserted video.
        height (int): Height of the inserted video.
    """

    main_cap = cv2.VideoCapture(main_video_path)
    main_fps = main_cap.get(cv2.CAP_PROP_FPS)
    main_width = int(main_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    main_height = int(main_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    insert_cap = cv2.VideoCapture(insert_video_path)
    insert_fps = insert_cap.get(cv2.CAP_PROP_FPS)
    insert_width = int(insert_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    insert_height = int(insert_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, main_fps, (main_width, main_height))

    while(main_cap.isOpened() and insert_cap.isOpened()):
        ret_main, main_frame = main_cap.read()
        ret_insert, insert_frame = insert_cap.read()

        if ret_main and ret_insert:
            insert_frame = cv2.resize(insert_frame, (width, height))

            roi = main_frame[y:y+height, x:x+width]

            roi = cv2.addWeighted(roi, 0, insert_frame, 1, 0)

            main_frame[y:y+height, x:x+width] = roi

            out.write(main_frame)
            cv2.imshow('Combined Video', main_frame)

            if cv2.waitKey(int(1000 / main_fps)) & 0xFF == ord('q'):
                break

        else:
            break

    main_cap.release()
    insert_cap.release()
    out.release()
    cv2.destroyAllWindows()

main_video_path = 'video1.mp4'
insert_video_path = 'video2.mp4'
output_video_path = 'output_combined_video.mp4'
x = 100  
y = 200  
width = 300  
height = 200

insert_video(main_video_path, insert_video_path, output_video_path, x, y, width, height)