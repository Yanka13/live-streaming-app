from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import queue

#Import for streamlit
import streamlit as st
import av
from streamlit_webrtc import (
    RTCConfiguration,
    VideoProcessorBase,
    WebRtcMode,
    webrtc_streamer,
)

#Import for Deep learning model
import tensorflow as tf
from tensorflow.keras.models import load_model

#Import for handling image
import cv2
from cvzone.HandTrackingModule import HandDetector

#Create a dict for classes
@st.cache(allow_output_mutation=True)
def alphabet():
    """ Generating dictionary to turn prediction into their actual labels"""
    mapping = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'K', 10: 'L', 11: 'M',
                             12: 'N', 13: 'O', 14: 'P', 15: 'Q', 16: 'R', 17: 'S', 18: 'T', 19: 'U', 20: 'V', 21: 'W', 22: 'X', 23: 'Y'}
    return mapping


RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# CWD path
HERE = Path(__file__).parent


#deep learning sign detector model cached
@st.cache(allow_output_mutation=True)
def retrieve_model():
    """ dummy tensorflow CNN model trained on few epochs on multiclassification task (american signs) """
    PATH_MODEL = "saved_models/deep_learning_dummy_model.h5"

    model = load_model(PATH_MODEL)
    return model


#Main intelligence of the file, class to launch a webcam, detect hands, then detect sign and output american letters
def app_object_detection():
    class SignPredictor(VideoProcessorBase):

        result_queue: "queue.Queue[List[Detection]]"
        def __init__(self) -> None:
            # Hand detector
            self.hand_detector = HandDetector(detectionCon=0.5, maxHands=2)
            # Sign detector
            self.model = retrieve_model()

            #Queue to share information that happen within the live video thread outside the thread
            self.result_queue = queue.Queue()

        def find_hands(self, image):

            hands, image_hand = self.hand_detector.findHands(image)
            # loop over all hands and print them on the video + apply predictor
            for hand in hands:
                bbox = hand["bbox"]

                rectangle = cv2.rectangle(image, (bbox[0] - 20, bbox[1] - 20),
                                          (bbox[0] + bbox[2] + 20,
                                           bbox[1] + bbox[3] + 20),
                                          (255, 0, 255), 2)
                #load model
                model = retrieve_model()

                # prediction
                prediction = model.predict(
                    np.expand_dims(tf.image.resize(
                        (rectangle), [64, 64]),
                        axis=0) / 255.0)

                prediction_max = np.argmax(prediction)
                mapping = alphabet()
                pred = mapping[prediction_max]
                #check on terminal the prediction
                print(pred)
                #store prediction on the queue to use them outside of the live thread
                self.result_queue.put(pred)

                #draw letter on images
                cv2.putText(image_hand, pred, (bbox[0] + 130, bbox[1] - 30), cv2.FONT_HERSHEY_PLAIN,
                                2, (255, 0, 255), 2)
            return hands, image_hand

        def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
            image = frame.to_ndarray(format="rgb24")
            hands, annotated_image = self.find_hands(image)
            return av.VideoFrame.from_ndarray(annotated_image, format="rgb24")

    webrtc_ctx = webrtc_streamer(
        key="object-detection",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        video_processor_factory=SignPredictor,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

    if st.checkbox("Show the detected labels", value=True):
      if webrtc_ctx.state.playing:
          labels_placeholder = st.empty()
          # NOTE: The video transformation with object detection and
          # this loop displaying the result labels are running
          # in different threads asynchronously.
          # Then the rendered video frames and the labels displayed here
          # are not strictly synchronized.
          while True:
              if webrtc_ctx.video_processor:
                  try:
                      result = webrtc_ctx.video_processor.result_queue.get(
                          timeout=1.0
                      )
                  except queue.Empty:
                      result = None
                  labels_placeholder.write(result)
              else:
                  break


    st.markdown(
        """All code and tutorial available [here](https://github.com/Yanka13/live-streaming-app),
       thanks to [streamlit webrtc](https://github.com/whitphx/streamlit-webrtcx) for making it possible"""
    )


############################ Sidebar + launching #################################################

object_detection_page = "Real time sign translation"

app_mode = st.sidebar.selectbox(
    "Choose the app mode",
    [
        object_detection_page,
    ],
)
st.subheader(app_mode)
if app_mode == object_detection_page:
    app_object_detection()
