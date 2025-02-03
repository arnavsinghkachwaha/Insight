import cv2 as cv
import numpy as np
import mediapipe as mp
mp_face_mesh = mp.solutions.face_mesh
LEFT_IRIS = [474,475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]


if __name__ == "__main__":
    cap = cv.VideoCapture('/Users/arnavkachwaha/Desktop/INSIGHT/Test Videos/vid3.mov')
    with mp_face_mesh. FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
        ) as face_mesh:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv.resize(frame, (440, 800))
            frame = cv.flip(frame, 1)
            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            img_h, img_w = frame.shape[:2]
            results = face_mesh.process(rgb_frame)

            if results.multi_face_landmarks:
                mesh_points=np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in results.multi_face_landmarks[0].landmark])
                (l_cx, l_cy), l_radius = cv.minEnclosingCircle(mesh_points[LEFT_IRIS])
                (r_cx, r_cy), r_radius = cv.minEnclosingCircle(mesh_points[RIGHT_IRIS])
                center_left = np.array([l_cx, l_cy], dtype=np.int32)
                center_right = np.array([r_cx, r_cy], dtype=np.int32)
                
                cv.circle(frame, center_left, int(l_radius), (0,255,0), 1, cv.LINE_AA)
                cv.circle(frame, center_right, int(r_radius), (0,255,0), 1, cv.LINE_AA)

            cv.imshow('img', frame)
            key = cv.waitKey(1)
            if key == ord('q'):
                break
    cap.release()
    cv.destroyAllWindows()


