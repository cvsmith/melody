import cv2
import numpy as np
import math
import json

winName = 'threshold'

def assignVarCallback(s,varName):
    def fn(x):
        s[varName] = x
        print (varName + " = " + str(s[varName]))
    return fn

def makeTrackbar(s,winName,var,maxVal=255,default=0):
    if var not in s:
        s[var] = default
    cv2.createTrackbar(var, winName, s[var], maxVal,
                       assignVarCallback(s,var))

def initState(s,img,gui = True):
    if gui:
        if cv2.getTrackbarPos('targetColor',winName) >= 0:
            return img
    colors = ['red','green','blue','orange']
    for c in colors:
        if c not in s:
            s[c] = [0,255]
    if 'targetColor' not in s:
        s['targetColor'] = 0

    if gui:
        def updateTarget(s):
            def fn(x):
                if 'targetColor' in s and s['targetColor'] == x:
                    return
                s['targetColor'] = x
                color = colors[x]
                cv2.setTrackbarPos('lowThresh', winName,s[color][0])
                cv2.setTrackbarPos('highThresh',winName,s[color][1])
            return fn
        startInd = s['targetColor']
        cv2.createTrackbar('targetColor', winName, startInd, len(colors)-1,
                        updateTarget(s))
        def setThresh(s,ind):
            def fn(x):
                color = colors[s['targetColor']]
                s[color][ind] = x
                print ('{}-{} = {}'.format(color,ind,x))
            return fn
        color = colors[startInd]
        cv2.createTrackbar('lowThresh',  winName, s[color][0], 255,
                        setThresh(s,0))
        cv2.createTrackbar('highThresh', winName, s[color][1], 255,
                        setThresh(s,1))

        # makeTrackbar(s,winName,'redLowThresh')
        # makeTrackbar(s,winName,'redHighThresh')
        # makeTrackbar(winName,'openSteps')
        # makeTrackbar(s,winName,'gaussianSize')
        makeTrackbar(s,winName,'closeSteps')
        makeTrackbar(s,winName,'polyApproxK')
        makeTrackbar(s,winName,'pipelineLen',s['pipelineSize'],default=1)
    return img

def isHoriz(p1,p2):
    dx = abs(p2[0] - p1[0])
    dy = abs(p2[1] - p1[1])
    return dy < 0.15*dx

def isVert(p1,p2):
    dx = abs(p2[0] - p1[0])
    dy = abs(p2[1] - p1[1])
    return dx < 0.15*dy

def hsv(s,img):
    return cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

def normalizeRGB(s,img):
    r,g,b = cv2.split(img)
    for c in [r,g,b]:
        cv2.equalizeHist(c,c)
    return cv2.merge([r,g,b])

def normalize(s,img):
    h,s,v = cv2.split(img)
    cv2.equalizeHist(s,s)
    s = s * (1 / 255.0)
    s = s ** 5
    s = (255*s).astype(np.uint8)
    # cv2.equalizeHist(v,v)
    return cv2.merge([h,s,v])

def gaussian(s,img):
    size = 0 if 'gaussianSize' not in s else s['gaussianSize']
    return cv2.GaussianBlur(img, (2*size+1,2*size+1), 50)

def hueThresh(colorName):
    def threshold(s,img):
        lowHue  = s[colorName][0]
        highHue = s[colorName][1]
        channels = cv2.split(img)
        hue,sat,val = channels
        sat = cv2.threshold(sat,0,255,
                            cv2.THRESH_OTSU)[1]

        high,low = highHue,lowHue
        resultFn = cv2.bitwise_and if high > low else cv2.bitwise_or
        hLow  = cv2.threshold(hue,high,255,
                              cv2.THRESH_BINARY_INV)[1]
        hHigh = cv2.threshold(hue,low,255,
                              cv2.THRESH_BINARY)[1]
        return cv2.bitwise_and(sat, resultFn(hLow,hHigh))
    return threshold

def scaleForSize(x,img):
    height,width = img.shape[:2]
    size = math.sqrt(width*height)
    return x*size

def holeClose(s,img):
    steps = scaleForSize(s['closeSteps']/3000.0,img)
    steps = int(steps+0.5)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    return cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernel,
                            iterations=steps)
def holeOpen(s,img):
    steps = scaleForSize(s['closeSteps']/3000.0,img)
    steps = int(steps+0.5)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    return cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel,
                            iterations=steps)

def extractContours(contourKey):
    def contourFn(s,img):
        s[contourKey] = cv2.findContours(img.copy(),cv2.RETR_TREE,
                                         cv2.CHAIN_APPROX_SIMPLE)
        return img
    return contourFn

def polyApprox(contourKey):
    def polyFn(s,img):
        contours,hierarchy = s[contourKey]
        # hulls = (cv2.convexHull(c) for c in contours)
        polys = (cv2.approxPolyDP(c,s['polyApproxK'],True) for c in
                contours)
        s[contourKey] = np.asarray(list(polys))
        return img
    return polyFn

def drawContours(contourKey,color):
    def drawFn(s,img):
        contours = s[contourKey]
        orig = img
        orig = orig.copy()
        cv2.drawContours(orig,contours,-1,color,thickness=10)
        return orig
    return drawFn

def get(key):
    def getFn(s,img):
        return s[key]
    return getFn
def put(key):
    def putFn(s,img):
        s[key] = img.copy()
        return img
    return putFn

def pipeline(fs):
    def fn(s,x):
        s['pipelineSize'] = len(fs)
        count = 0
        for f in fs:
            if 'pipelineLen' in s and count >= s['pipelineLen']:
                break
            print f.__name__
            x = f(s,x)
            count += 1
        return x
    return fn

def getPolys(key):
    return [ holeClose,holeOpen,
             extractContours(key),
             polyApprox(key) ]

def colorPipeline(color,contourKey,outKey):
    return ([ put('preColor'), hueThresh(color) ] +
            getPolys(contourKey) +
            [ put(outKey),get('preColor') ])

def findBlack(contourKey):
    def fn(s,img):
        channels = cv2.split(img)
        # sat = channels[1]
        # sat = cv2.threshold(sat,0,255,
        #                     cv2.THRESH_OTSU)[1]
        val = channels[2]
        valThresh = cv2.threshold(val,0,255,
                                      cv2.THRESH_OTSU)[0]
        val = cv2.threshold(val,valThresh/1.5,255,cv2.THRESH_BINARY)[1]
        # return cv2.bitwise_and(255-sat,255-val)
        return 255-val
    return [fn] + [ holeClose,
                    extractContours(contourKey),
                    polyApprox(contourKey) ]


process = ([ put('orig'),gaussian,hsv ] +
           colorPipeline('red','redContours','redImg') +
           colorPipeline('green','greenContours','greenImg') +
           colorPipeline('blue','blueContours','blueImg') +
           colorPipeline('orange','orgContours','orgImg') +
           # findBlack('blackContours') +
           [ get('orig'),
             drawContours('redContours',(255,0,0)),
             drawContours('greenContours',(0,0,255)),
             drawContours('blueContours',(0,255,0)),
             drawContours('orgContours',(255,255,0)) ])



def swallow(f):
    def fn(s,x):
        try:
            return f(s,x)
        except:
            import traceback
            print (sys.exc_info()[0])
            traceback.print_tb(sys.exc_info()[2])
            return x
    return fn

if __name__ == '__main__':
    import sys
    import imstream
    filename = 'test.jpg'
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    guiProcess = [initState] + process
    pipe = pipeline(guiProcess)
    s = {'red': [147,0],'blue': [100,135],'green':[30,99],
         'orange': [0,27],'closeSteps':3000*15/2827,#'pipelineLen':4}
         'pipelineLen':len(guiProcess)}
    imstream.runStream(lambda x: swallow(pipe)(s,x),
                        winName=winName,
                        filename=filename)

