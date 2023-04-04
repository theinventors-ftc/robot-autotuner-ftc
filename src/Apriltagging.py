import cv2 as cv
from pupil_apriltags import Detector

PLOT_APRIL_TAGS = True

class AprilTagging:
    tagsDetected = []
    detector = Detector(
        families="tag36h11",
        nthreads=1,
        quad_decimate=1.0,
        quad_sigma=0.0,
        refine_edges=1,
        decode_sharpening=0.25,
        debug=0
    )

    def update(self, input):
        copy = input.copy()
        grayscaleImage = cv.cvtColor(copy, cv.COLOR_BGR2GRAY)
        self.tagsDetected = self.detector.detect(grayscaleImage)

        if PLOT_APRIL_TAGS:
            for tag in self.tagsDetected:
                ptA, ptB, ptC, ptD = tag.corners;

                ptB = (int(ptB[0]), int(ptB[1]))
                ptC = (int(ptC[0]), int(ptC[1]))
                ptD = (int(ptD[0]), int(ptD[1]))
                ptA = (int(ptA[0]), int(ptA[1]))

                cv.line(copy, ptA, ptB, (255, 0, 0), 2)
                cv.line(copy, ptB, ptC, (255, 0, 0), 2)
                cv.line(copy, ptC, ptD, (255, 0, 0), 2)
                cv.line(copy, ptD, ptA, (255, 0, 0), 2)

                cv.putText(copy, str(tag.tag_id), (ptB[0] + 10, ptB[1] + 15), cv.FONT_HERSHEY_SIMPLEX, 
                    1, (255, 0, 0), 2, cv.LINE_AA)

        return copy
    
    def getTagCenterById(self, id):
        # print(self.tagsDetected)
        filteredArr = list(filter(lambda x: x.tag_id == id, self.tagsDetected))
        return filteredArr[0].center if filteredArr else None