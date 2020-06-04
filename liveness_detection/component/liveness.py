import torch
import models
import base64
import cv2
import argparse
import sys
import numpy as np
import imutils
import time
from flask_socketio import emit


class LivenessDetection:
    def __init__(self, attack=1, genuine=0, thresh=0.7):
        self.ATTACK = attack
        self.GENUINE = genuine
        self.thresh = thresh

    def load(self, protoPath="./face_detector/deploy.prototxt",
             modelPath="./face_detector/res10_300x300_ssd_iter_140000.caffemodel",
             protoPath2="./face_alignment/2_deploy.prototxt",
             modelPath2="./face_alignment/2_solver_iter_800000.caffemodel",
             model_name="MyresNet18", load_model_path="./pretrained_model/a8.pth"):
        try:
            print("Loading models..")
            # protoPath = "./face_detector/deploy.prototxt"
            # modelPath = "./face_detectdsor/res10_300x300_ssd_iter_140000.caffemodel"
            self.net = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

            # protoPath2 = "./face_alignment/2_deploy.prototxt"
            # modelPath2 = "./face_alignment/2_solver_iter_800000.caffemodel"
            self.net2 = cv2.dnn.readNetFromCaffe(protoPath2, modelPath2)

            self.model = getattr(models, model_name)().eval()
            self.model.load(load_model_path)
            self.model.train(False)
            print("Done Loading models..")
        except Exception as e:
            print("Model Failed to load", e)
            raise

    def detector(self, img):
        try:
            frame = imutils.resize(img, width=600)
            (h, w) = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
            self.net.setInput(blob)
            detections = self.net.forward()

            for i in range(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]

                if confidence > 0.5:
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    startX = max(0, startX)
                    startY = max(0, startY)
                    endX = min(w, endX)
                    endY = min(h, endY)

                    face = frame[startY:endY, startX:endX]
                    face = cv2.resize(face, (400, 400))
                    return face
        except Exception as e:
            print("Error in detector method", e)
            raise

    def crop_with_ldmk(self, image, landmark):
        try:
            scale = 3.5
            image_size = 224
            ct_x, std_x = landmark[:, 0].mean(), landmark[:, 0].std()
            ct_y, std_y = landmark[:, 1].mean(), landmark[:, 1].std()

            std_x, std_y = scale * std_x, scale * std_y

            src = np.float32([(ct_x, ct_y), (ct_x + std_x, ct_y + std_y), (ct_x + std_x, ct_y)])
            dst = np.float32([((image_size - 1) / 2.0, (image_size - 1) / 2.0),
                              ((image_size - 1), (image_size - 1)),
                              ((image_size - 1), (image_size - 1) / 2.0)])
            retval = cv2.getAffineTransform(src, dst)
            result = cv2.warpAffine(image, retval, (image_size, image_size), flags=cv2.INTER_LINEAR,
                                    borderMode=cv2.BORDER_CONSTANT)
            return result
        except Exception as e:
            print("Error in crop_with_ldmk", e)
            raise

    def demo(self, img):
        data = np.transpose(np.array(img, dtype=np.float32), (2, 0, 1))
        data = data[np.newaxis, :]
        data = torch.FloatTensor(data)
        with torch.no_grad():
            outputs = self.model(data)
            outputs = torch.softmax(outputs, dim=-1)
            preds = outputs.to('cpu').numpy()
            attack_prob = preds[:, self.ATTACK]
        return attack_prob

    def liveness_detection(self, frame, user_id):
        try:
            liveness_flag = 0
            print("frame Size: ", frame.shape)

            frame = imutils.resize(frame, width=600)

            # frame = imutils.rotate(frame, -90)
            (h, w) = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
            self.net.setInput(blob)
            start = time.time()

            detections = self.net.forward()

            # print("detections: ", detections, len(detections))

            end = time.time()

            print('detect times : %.3f ms' % ((end - start) * 1000))
            for i in range(0, detections.shape[2]):

                confidence = detections[0, 0, i, 2]
                if confidence > 0.5:
                    print('If Loope inside', detections[0, 0, i, 2])
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    sx = startX
                    sy = startY
                    ex = endX
                    ey = endY

                    ww = (endX - startX) // 10
                    hh = (endY - startY) // 5

                    startX = startX - ww
                    startY = startY + hh
                    endX = endX + ww
                    endY = endY + hh

                    startX = max(0, startX)
                    startY = max(0, startY)
                    endX = min(w, endX)
                    endY = min(h, endY)

                    x1 = int(startX)
                    y1 = int(startY)
                    x2 = int(endX)
                    y2 = int(endY)

                    roi = frame[y1:y2, x1:x2]
                    gary_frame = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)
                    resize_mat = np.float32(gary_frame)
                    m = np.zeros((40, 40))
                    sd = np.zeros((40, 40))
                    mean, std_dev = cv2.meanStdDev(resize_mat, m, sd)
                    new_m = mean[0][0]
                    new_sd = std_dev[0][0]
                    new_frame = (resize_mat - new_m) / (0.000001 + new_sd)
                    blob2 = cv2.dnn.blobFromImage(cv2.resize(new_frame, (40, 40)), 1.0, (40, 40), (0, 0, 0))
                    self.net2.setInput(blob2)
                    align = self.net2.forward()

                    aligns = []
                    alignss = []
                    for i in range(0, 68):
                        align1 = []
                        x = align[0][2 * i] * (x2 - x1) + x1
                        y = align[0][2 * i + 1] * (y2 - y1) + y1
                        cv2.circle(frame, (int(x), int(y)), 1, (0, 0, 255), 2)
                        align1.append(int(x))
                        align1.append(int(y))
                        aligns.append(align1)
                    cv2.rectangle(frame, (sx, sy), (ex, ey), (0, 0, 255), 2)
                    alignss.append(aligns)

                    ldmk = np.asarray(alignss, dtype=np.float32)
                    ldmk = ldmk[np.argsort(np.std(ldmk[:, :, 1], axis=1))[-1]]
                    img = self.crop_with_ldmk(frame, ldmk)

                    time1 = time.time()
                    attack_prob = self.demo(img)
                    time2 = time.time()
                    print('prob times : %.3f ms' % ((time2 - time1) * 1000))
                    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

                    true_prob = 1 - attack_prob
                    if attack_prob > self.thresh:
                        label = 'fake'
                        liveness_flag = 0
                        cv2.putText(frame, label + ' :' + str(attack_prob), (sx, sy - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.5,
                                    (0, 0, 255), 2)
                    else:
                        label = 'true'
                        liveness_flag = 1
                        cv2.putText(frame, label + ' :' + str(true_prob), (sx, sy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (0, 0, 255), 2)

                    print("label: ", label)

            return {"liveness_flag": liveness_flag, "user_id": user_id}

        except Exception as e:
            print("Error in crop_with_ldmk", e)
            raise

    def get_liveness_result(self, img, source_id, user_id, agent_id):
        try:
            encoded_data = img.split(',')[1]
            decoded_data = base64.b64decode(encoded_data)

            np_data = np.fromstring(decoded_data, np.uint8)
            # print("original data: ", np_data)
            frame = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)

            result = self.liveness_detection(frame, user_id)
            print("result: ", result)
            return dict(data=dict(face_found=True, liveness_flag=result['liveness_flag'], message="success"))

        except Exception as e:
            print("Error get_liveness_result: ", e)
            raise
