import cv2
import face_recognition

class ServFaceRecog():
    inframe = None
    outframe = None

    master_image = face_recognition.load_image_file("facedatas/master.jpg")
    master_face_encoding = face_recognition.face_encodings(master_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [master_face_encoding]
    known_face_names = ["master"]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    def __init__(self):
        # load master picture

        pass

    def __str__(self):
        return 'ServFaceRecog:Class to process face recognition'

    def getin(self, frame):
        self.inframe = frame

    def process(self):
        self.outframe = self.inframe
            # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(self.outframe, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if self.process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]

                face_names.append(name)

        #process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(self.outframe, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(self.outframe, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(self.outframe, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


    def out(self):
        return self.outframe

