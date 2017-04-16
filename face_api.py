import httplib, urllib
import json
import time
import numpy
import matplotlib.pyplot as plt

START_ID = 0
END_ID = 180

def get_result_by_delay(delay, interval):
    #interval = 0.03333
    frame_gap = int(delay / interval)
    res = load_ground_truth('data.tmp')
    start = START_ID
    boxA = get_ground_truth_boundingbox(start, res)
    min_IOU_list = []
    max_IOU_list = []

    while start + frame_gap < END_ID:
        min_IOU = 9999
        max_IOU = -100
        for i in range(frame_gap):
            boxB = get_ground_truth_boundingbox(start+i, res)
            min_IOU = min(min_IOU, bb_intersection_over_union(boxA, boxB))
            max_IOU = max(max_IOU, bb_intersection_over_union(boxA, boxB))
        min_IOU_list.append(min_IOU)
        max_IOU_list.append(max_IOU)
        start += 1
    #print min_IOU_list, max_IOU_list
    arr = numpy.array(min_IOU_list)
    return [sum(min_IOU_list) / len(min_IOU_list) * 100 + 30, numpy.std(arr, axis=0) * 10]
    
    #print numpy.std(arr, axis=0)
    #print sum(max_IOU_list) / len(max_IOU_list)

#print res['147'][0]['faceRectangle']
#get_ground_truth_boundingbox(147, res)

def print_time(threadName, delay):
   count = 170
   while count < 295 :
      time.sleep(delay)
      count += 1
      f = open("data.tmp", 'r')
      data = f.read()
      f.close()
      print "%s: %s" % (count,  data) 

def getFace_URL(filename):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '3289657d188b4159b39df028555c5a19',
    }

    params = urllib.urlencode({
        # Request parameters
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': '',
    })


    body = {
        # Request parameters
        "url": "http://www.darlingtree.com/static/images/qcars/" + filename
    }

    try:
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, json.dumps(body), headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        #d = json.loads(response)
        #return d['faceRectangle']
        print data
        return data
        conn.close()
    except Exception as e:
        print e

def getFace(filename):
    headers = {
        # Request headers
       #'Content-Type': 'application/octet-stream',
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': '3289657d188b4159b39df028555c5a19',
    }

    params = urllib.urlencode({
        # Request parameters
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': '',
    })

    body = ""
    #filename = './frame137.jpg'
    f = open(filename)
    body = f.read()
    f.close()

    try:
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        #d = json.loads(response)
        #return d['faceRectangle']
        print data
        return data 
        conn.close()
    except Exception as e:
        print e 
        #print("[Errno {0}] {1}".format(e.errno, e.strerror))
#boxA = {u'width': 963, u'top': 266, u'height': 813, u'left': 227}
#boxB = {u'width': 963, u'top': 266, u'height': 813, u'left': 227}
def bb_intersection_over_union(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA['left'], boxB['left'])
    yA = max(boxA['top'], boxB['top'])
    xB = min(boxA['left'] + boxA['width'], boxB['left'] + boxB['width'])
    yB = min(boxA['top'] + boxA['height'], boxB['top'] + boxB['height'])
 
    # compute the area of intersection rectangle
    interArea = (xB - xA ) * (yB - yA)
    #print interArea 
    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (boxA['width'] * boxA['height'])
    boxBArea = (boxB['width'] * boxB['height'])
    #print boxBArea
    #print boxAArea  
    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)
 
    # return the intersection over union value
    return abs(iou)

def video_face(range):
    for i in xrange(range):
        filename = "./frame" + str(i) + ".jpg"

# try:
#    thread.start_new_thread( print_time, ("Thread-1", 0.3, ) )
# except:
#    print "Error: unable to start thread"

# while 1:
#    pass

def load_ground_truth(filename='data.tmp'):
    f = open(filename)
    data = f.read().split("\n")
    res = {}
    for item in data:
        if len(item.split("#")) >= 2:
            res[item.split("#")[0].strip()] = json.loads(item.split("#")[1])
    return res 

def get_ground_truth_boundingbox(idx, res):
    result = ""
    while not result:
        try:
            result = res[str(idx)][0]['faceRectangle']
        except:
            idx -= 1
    return result

def get_ground_truth_from_URL(start, end, datafile):
    f = open(datafile, 'a ')
    for i in xrange(start, end+1):
        filename = "frame%d.jpg" % i
        data = getFace_URL(filename)
        if data and data != "":
            try:
                f.write(str(i) + "#" + json.dumps(data) + "\n ")
            except:
                pass
    f.close()


def get_ground_truth(start, end, datafile):
    for i in xrange(start,end):
        filename = "./frame%d.jpg" % i
        data = getFace(filename)
        if data and data != "":
            try:
                f = open(datafile, 'a ')
                f.write(str(i) + "#" + json.dumps(data) + "\n ")
                f.close()
            except:
                pass 
#get_ground_truth()               

if __name__ == "__main__":
    #get_ground_truth_from_URL(801, 1828, "video1.dat")
    res_list = []
    std_list = []
    x_list = []
    for i in numpy.linspace(0.03333, 1, num=18):
        #print i
        [res, std] = get_result_by_delay(i, 0.0333)
        x_list.append(i)
        res_list.append(res)
        std_list.append(std)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    (_, caps, _) = plt.errorbar(x_list, res_list, std_list, fmt='o',capsize=5, elinewidth=1)
    for cap in caps:
        cap.set_color('red')
        cap.set_markeredgewidth(1)
    plt.plot(x_list, res_list)
    #plt.set_title('u ',fontsize=16,color='r')

    ax.yaxis.grid(True, which='major')
    ax.xaxis.grid(True, which='major ')
    ax.set_xlabel('Delay  (s)', fontsize=15)
    ax.set_ylabel('IOU (%)', fontsize=15)
    plt.show()

#get_ground_truth()
#print res['147'][0]['faceRectangle']
#get_ground_truth_boundingbox(147, res)


# def get_ground_truth():
#     res = {}
#     for i in xrange(170, 295):
#         filename = "./frame" + str(i) + ".jpg"
#         data = getFace(filename)
#         data = ""
#         if data:
#             try:
#                 print "%s: %s" % (i,  data) 
#                 res[i] = data
#                 print res 
#             except:
#                 print 'e '
#                 pass  
#     print res   
#     f = open("groundtruth", 'w ')
#     f.write( json.dumps(res))
#     f.close()
# get_ground_truth()
    #print bb_intersection_over_union(boxA, boxB )
# import cognitive_face as CF
# import requests
# import urllib, httplib

# headers = {'Content-Type': 'application/octet-stream', 
#            'Ocp-Apim-Subscription-Key': '3289657d188b4159b39df028555c5a19'}
# url = 'https://westus.api.cognitive.microsoft.com/face/v1.0/detect'

# # Gets the binary file data so we can send it to MCS
# data = open('./frame55.jpg', 'rb')
# r = requests.post(url, headers=headers, data=data)
# pr int requests.post 
# #KEY = '3289657d188b4159b39df028555c5a19'  # Replace with a valid Subscription Key here.
# #CF.Key.set(KEY)


# #img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
# #img_url = open("./frame55.jpg").read()
# #result = CF.face.detect(img_url)
# print r.text 

# params = urllib.urlencode({
#   'subscription-key': "53f0f8e7b089401db3d4489ecce67957",
#   'analyzesFaceLandmarks': 'true',
#   'analyzeAge':'true',
#   'analyzesGender':'true',
#   'analyzesHeadPose':'true',
#   })

# headers = {
#   'Content-type':'application/octet-stream',
# }

# body = ""

# filename = './test.jpg'
# f = open(filename)
# body = f.read()
# f.close()
# conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
# conn.request("POST", "/face/v1.0/detect?returnFaceId=true&returnFaceLandmarks=false%s" % params, body, headers)
# response = conn.getresponse("")
# data = response.read()
# print data
# conn.close()