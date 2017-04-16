import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt


def Simulation(start, end, step):
    centerPoint = [0, 0]
    r = 10
    size = 10
    topology = generateRandomPointR(centerPoint, r, size)

    #plotPoint(centerPoint, r, topology)
    for time in xrange(start, end, step):
        request = prepareRequestInfo(size)
        data = combineAll(topology, request)
        sendData(data)
    return ""


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


def prepareRequestInfo(size = 10):
    request = []
    reqSizeArray = preparePacketSize(size)
    reqTimeArray = prepareTime(size)
    for i in xrange(size):
        request.append([i, reqSizeArray[i], reqTimeArray[i]])
    return request

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


#Simulation(1, 10, 1)
#print topology
#print preparePacketSize(10, 10)
#print prepareTime(10, 10)

#print combineAll(topology, request)
#plotPoint(centerPoint, r, topology)
#print generateRandomPointRec(centerPoint, 0, 0, 10)