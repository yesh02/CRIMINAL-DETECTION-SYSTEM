# facerec.py
import cv2
import numpy as np
import os

size = 2
haar_cascade = cv2.CascadeClassifier('face_cascade.xml')

def train_model():
    """
    Train a face recognition model using LBPHFaceRecognizer.
    
    Returns:
    - Tuple containing trained model and corresponding names
    """
    model = cv2.face.LBPHFaceRecognizer_create()
    fn_dir = 'face_samples'
    print('Training...')

    images, labels, names = [], [], {}
    id = 0

    for subdir, dirs, files in os.walk(fn_dir):
        for subdir in dirs:
            names[id] = subdir
            subject_path = os.path.join(fn_dir, subdir)
            for filename in os.listdir(subject_path):
                name, extension = os.path.splitext(filename)
                if extension.lower() not in ['.png', '.jpg', '.jpeg', '.gif', '.pgm']:
                    print("Skipping " + filename + ", wrong file type")
                    continue
                path = os.path.join(subject_path, filename)
                label = id
                images.append(cv2.imread(path, 0))
                labels.append(int(label))
            id += 1

    images, labels = np.array(images), np.array(labels)
    model.train(images, labels)
    return model, names

def detect_faces(gray_frame):
    """
    Detect faces in a grayscale frame.
    
    Args:
    - gray_frame: Grayscale frame
    
    Returns:
    - List of face coordinates
    """
    global size, haar_cascade
    mini_frame = cv2.resize(gray_frame, (int(gray_frame.shape[1] / size), int(gray_frame.shape[0] / size)))
    faces = haar_cascade.detectMultiScale(mini_frame)
    return faces

def recognize_face(model, frame, gray_frame, face_coords, names):
    """
    Recognize faces in a frame using a trained model.
    
    Args:
    - model: Trained face recognition model
    - frame: Input frame
    - gray_frame: Grayscale frame
    - face_coords: List of face coordinates
    - names: Dictionary containing subject names
    
    Returns:
    - Tuple containing the annotated frame and recognized faces
    """
    img_width, img_height = 112, 92
    recognized = []
    recog_names = []

    for face_coord in face_coords:
        x, y, w, h = [v * size for v in face_coord]
        face = gray_frame[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (img_width, img_height))
        prediction, confidence = model.predict(face_resize)

        if confidence < 95 and names[prediction] not in recog_names:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            recog_names.append(names[prediction])
            recognized.append((names[prediction].capitalize(), confidence))
        elif confidence >= 95:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return frame, recognized
