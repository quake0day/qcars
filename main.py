import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
import matlab.engine
import face_api as face
from matplotlib.ticker import MaxNLocator


# total frames in the folder
# need to be changed
TOTAL_FRAMES = 1828




def Simulation(start, end, step, num):
    Num = num # number of nodes
    START_ID = [i for i in xrange(int(Num))]
    START_ID = [elem * int(TOTAL_FRAMES / Num) for elem in START_ID]

    eng = matlab.engine.start_matlab()

    #centerPoint = [0, 0]
    #r = 10
    #size = 10
    #topology = generateRandomPointR(centerPoint, r, size)

    # Call matlab function...

    space = 10.0 #simulation space
    distance_BOUND = 2.0 / space #distance_BOUND for a transmitter that serve as interference to another transmitter
    T = end - start
    C = 1.0 #number of channel
    S = 1.0 # scenario

    # Generate random topology
    Z, D = eng.topology(Num, distance_BOUND, space, nargout=2)
    #print Z, D
    SA = eng.zeros(C,T+13);


    #Prepare request
    # R=[t 1 3 2; t 2 3 4; t 3 2 5];%request
    #R = [[1, 1, 3, 2], [1, 2, 3, 4], [1, 3, 2, 5]]
    #R = matlab.double(R)

    # Call FCFS function
    # Decision, row, Trans, p = eng.FCFS(D, R, S, SA, nargout=4)

    # Call SmallestFirst function
    # Decision, SortedR, AvaiChanal, row, Trans = eng.SmallestFirst(D, R, S, SA, nargout=5)

    # Call EarliestFirst function
    # Decision, SortedR, AvaiChanal, row, Trans = eng.EarliestFirst(D, R, S, SA, nargout=5)

    Decision =[]

    # possible delay value
    # need to be changed to make it real
    delays = np.linspace(0.03333, 1, num=6)
    Delay_Data = {}
    for t in xrange(start, end, step):
        # Prepare request for each node
        R = []
        for nid in xrange(int(Num)):
            request_for_nid = prepareNodeRequest(nid, t, 0.95, START_ID )
            if len(request_for_nid) > 0:
                R.append(request_for_nid)

        if len(R) != 0:
            R = matlab.double(R)
            try:
                #Decision, row, Trans, p = eng.FCFS(D, R, S, SA, nargout=4)
                #Decision, SortedR, AvaiChanal, row, Trans = eng.SmallestFirst(D, R, S, SA, nargout=5)
                Decision, SortedR, AvaiChanal, row, Trans = eng.EarliestFirst(D, R, S, SA, nargout=5)
                for item in Decision:
                    time = item[0]
                    nid  = item[1]
                    accept = item[-1]
                    if accept == 0:
                        if time not in Delay_Data:
                            Delay_Data[time] = [nid]
                        else:
                            Delay_Data[time].append(nid)
            except:
                pass
        # def get_IOU_by_delay(delay, start_id, end_id):


    All_Node_IOU_Min_Average = []
    for nid in xrange(int(Num)):
        IOU_Data = []
        for t in xrange(start, end, step):
            i = 1
            for j in xrange(len(delays) - 2):
                try:
                    if(nid in Delay_Data[t-j]):
                        i += 1
                except:
                    pass
            d = delays[i]
            min_IOU, max_IOU = face.get_IOU_by_delay(d, START_ID[nid]+t, START_ID[nid]+t)
            IOU_Data.append(min_IOU)
        All_Node_IOU_Min_Average.append(sum(IOU_Data) / len(IOU_Data) * 100)
    arr = np.array(All_Node_IOU_Min_Average)

    print "Done! Node num = %d" % num
    return [sum(All_Node_IOU_Min_Average) / len(All_Node_IOU_Min_Average), np.std(arr, axis=0) ]    #plotPoint(centerPoint, r, topology)
    # for time in xrange(start, end, step):
    #     request = prepareRequestInfo(size)
    #     data = combineAll(topology, request)
    #     sendData(data)
    # return ""

#R = [[1, 1, 3, 2], [1, 2, 3, 4], [1, 3, 2, 5]]
def prepareNodeRequest(nid, t, threshold, START_ID ,maxT = 20):
    res = face.load_ground_truth('video1.dat')
    boxA = face.get_ground_truth_boundingbox(START_ID[nid]+t, res)
    R = [t+1, nid+1]  # To avoid 0 .. matlab does not support 0
    for i in xrange(maxT):
        boxB = face.get_ground_truth_boundingbox(START_ID[nid]+t + i, res)
        IOU = face.bb_intersection_over_union(boxA, boxB)
        if  IOU < threshold:
            # Assume 1/IOU is the packet size
            # need to change to actual value ...
            # To be DONE.
            R.append(int(1/IOU)*10)
            R.append(i)
            return R
    return []


def generateRandomNumber(size):
    random_points = []
    random_numbers = np.random.uniform(0, 121292, size)
    f = open('tmp2.txt', 'w')
    for i in random_numbers:
        f.write(str(i)+"\n")
    f.close()

generateRandomNumber(99999)

def sendData(data):
    print data



# generate random points based on r
def generateRandomPointR(centerPoint, r, size = 10):
    x = centerPoint[0]
    y = centerPoint[1]

    #Pick two random numbers in the range (0, 1), namely a and b. 
    #If b < a, swap them. Your point is (b*R*cos(2*pi*a/b), b*R*sin(2*pi*a/b)).

    random_points = []
    random_numbers = np.random.uniform(0, 1, 2*size+1)
    for i in xrange(1, size+1):
        a = random_numbers[i * 2]
        b = random_numbers[i]
        if (b < a):
            a,b = b,a
        point = [b * r * math.cos(2 * math.pi * a / b), b * r * math.sin(2 * math.pi * a / b)]
        random_points.append(point)
    return random_points    
    #(b*R*cos(2*pi*a/b), b*R*sin(2*pi*a/b))


# generate random points based on length and width
# still have some issues..
def generateRandomPointRec(centerPoint, length, width, size = 10):
    x = centerPoint[0]
    y = centerPoint[1]

    random_points = []
    random_numbers = np.random.uniform(0, 1, 2*size)
    print random_numbers
    for i in xrange(0, size, 2):
        a = random_numbers[i]
        b = random_numbers[i + 1]
        point = [a, b]
        random_points.append(point)
    return random_points    
    #(b*R*cos(2*pi*a/b), b*R*sin(2*pi*a/b))


# def prepareRequestInfo(size = 10):
#     request = []
#     reqSizeArray = preparePacketSize(size)
#     reqTimeArray = prepareTime(size)
#     for i in xrange(size):
#         request.append([i, reqSizeArray[i], reqTimeArray[i]])
#     return request

def preparePacketSize(size, maxPacketsize = 10):
    return np.random.uniform(0, maxPacketsize, size)

def prepareTime(size, maxTime = 10):
    return np.random.uniform(0, maxTime, size)


def combineAll(topology, request):
    finalRequest = []
    finalRequest.append(topology)
    finalRequest.append(request)
    return finalRequest

def plotPoint(centerPoint, r, topology):
    matplotlib.rcParams['axes.unicode_minus'] = False
    fig, ax = plt.subplots()
    circle = plt.Circle((centerPoint[0], centerPoint[1]), r, color='b', alpha=0.2)
    ax.add_artist(circle)
    ax.plot(centerPoint[0], centerPoint[1], '*')
    for point in topology:
        ax.plot(point[0], point[1], 'o')
    ax.set_title('Display Topology')
    plt.show()

if __name__ == "__main__":
    #get_ground_truth_from_URL(801, 1828, "video1.dat")
    res_list = []
    std_list = []
    x_list = []
    for i in xrange(1, 21):
        [res, std] = Simulation(0, TOTAL_FRAMES / i, 1, i)
        x_list.append(i)
        res_list.append(res)
        std_list.append(std)


    fig = plt.figure()

    ax = fig.add_subplot(111)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    uplims = np.array([100]*20, dtype=bool)

    (_, caps, _) = plt.errorbar(x_list, res_list, std_list, uplims=uplims, fmt='o',capsize=5, elinewidth=1)
    for cap in caps:
        cap.set_color('red')
        cap.set_markeredgewidth(1)
    plt.plot(x_list, res_list)
    #plt.set_title('u ',fontsize=16,color='r')

    ax.yaxis.grid(True, which='major')
    ax.xaxis.grid(True, which='major ')
    ax.set_xlabel('# of Node', fontsize=15)
    ax.set_ylabel('IOU (%)', fontsize=15)
    plt.show()


#@face.get_ground_truth(0, 200, "video1.dat")
#face.getFace("./frame0.jpg")
#print topology
#print preparePacketSize(10, 10)
#print prepareTime(10, 10)

#print combineAll(topology, request)
#plotPoint(centerPoint, r, topology)
#print generateRandomPointRec(centerPoint, 0, 0, 10)