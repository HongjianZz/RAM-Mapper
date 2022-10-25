'''
# Hongjian Zhu RAM Mapper
# id 1004291857

# LUTRAM is 64 words x 10 bits wide or 32 words x 20 bits wide

# 8k SRAM-Based (BRAM) can be resize from 8192 words x 1 bits to 256 words x 32 bits |every 10 logic blocks|
# if in TrueDualPort mode, it can only support max width of 512 words x 16 bits

# 128k BRAM can be resize from 128k words x 1 bit to 1024 words x 128 bits |every 300 logic blocks|
# if in TrueDualPort mode, it can only support max width of 2048 x 64 bits

'''
import time
import math

m_LUTRAM = 0.5 # 50% of logic blocks can be implement as LUTRAMs
sKRAMspace = 10 #small BRAM in every 10 LBs
bKRAMspace = 300 #Big BRAM in every 300 LBs
N = 10 #Number of LUTs in a Logic Block

#all possible dimension of memory sizes
space = [(8192,1),(4096,2),(2048,4),(1024,8),(512,16),(256,32)] #8kRAM
space1 = [(131072,1),(65536,2),(32768,4),(16384,8),(8192,16),(4096,32),(2048,64),(1024,128)] #128kRAM
space3 = [(64,10),(32,20)] #LUTRAMs

start_time = time.time() #start program timeer

#All possible combination for LUTRAM
class lutRAM:
    def __init__(self):
        self.words1 = 64
        self.bits1 = 10
        self.words2 = 32
        self.bits2 = 20
        self.num = 2

#All possible combination for 8KRam
class sKBRAM:
    def __init__(self):
        self.words1 = 8192
        self.bits1 = 1
        self.words2 = 4096
        self.bits2 = 2
        self.words3 = 2048
        self.bits3 = 4
        self.words4 = 1024
        self.bits4 = 8
        self.words5 = 512
        self.bits5 = 16
        self.words6 = 256
        self.bits6 = 32
        self.num = 6

#All possible combination for True-Dual-Port 8KRam
class sKBRAM_T:
    def __init__(self):
        self.words1 = 8192
        self.bits1 = 1
        self.words2 = 4096
        self.bits2 = 2
        self.words3 = 2048
        self.bits3 = 4
        self.words4 = 1024
        self.bits4 = 8
        self.words5 = 512
        self.bits5 = 16
        self.num = 5

#All possible combination for 128KRam
class bKBRAM:
    def __init__(self):
        self.words1 = 131072
        self.bits1 = 1
        self.words2 = 65536
        self.bits2 = 2
        self.words3 = 32768
        self.bits3 = 4
        self.words4 = 16384
        self.bits4 = 8
        self.words5 = 8192
        self.bits5 = 16
        self.words6 = 4096
        self.bits6 = 32
        self.words7 = 2048
        self.bits7 = 64
        self.words8 = 1024
        self.bits8 = 128
        self.num = 8

#All possible combination for True-dual-port 128KRam
class bKBRAM_T:
    def __init__(self):
        self.words1 = 131072
        self.bits1 = 1
        self.words2 = 65536
        self.bits2 = 2
        self.words3 = 32768
        self.bits3 = 4
        self.words4 = 16384
        self.bits4 = 8
        self.words5 = 8192
        self.bits5 = 16
        self.words6 = 4096
        self.bits6 = 32
        self.words7 = 2048
        self.bits7 = 64
        self.num = 7

# return the number of LUT needed for decoder
def decoderCount(R):
    return 0 if (R==1) else (1 if(R==2) else R)

# return the number of LUT needed for Mux
def muxCount (R):
    exceed = True if (R>16) else False
    if(R==1):
        result = 0
    elif(R<=4):
        result = 1
    elif(R<= 8):
        result = 3
    else:
        result = 5
    return result, exceed


#Count how many physical rams available in the required logic blocks
#Count how many LUTRAMs can in the required logic blocks
#Output a list [circuit_id,occupied_lb,sKRAM,bKRAM,useable_LUT,how many blocks to the next available sKRAM,how many blocks to the next available next bKRAM]
def countRam(element):
    result = element.split("\t")
    ##print(result)
    circuit_id = int(result[0])
    occupied_lb = int(result[1])
    useable_LUT = int(math.floor(occupied_lb//2))
    sKRAM = occupied_lb//10
    bKRAM = occupied_lb//300
    next_sKRAM = occupied_lb % 10
    next_bKRAM = occupied_lb % 300
    return (list(((circuit_id,occupied_lb,sKRAM,bKRAM,useable_LUT,next_sKRAM,next_bKRAM))))


def saveFile(data):
    with open("output.txt", "w") as txt_file:
        for col in data:
            for line in col:
                txt_file.write(" ".join(line) + "\n")  # works with any number of elements in a line


# find the best combination of LUT Ram that minimize the space
def bestFitlutSeries(a,b,id):
    lutRAM1 = lutRAM()
    type_available = space3
    ramType = lutRAM1.num
    rtotal = math.inf # initial value, will be replaced
    rseries = 1
    rparallel = 1
    depth = lutRAM1.words1
    width = lutRAM1.bits1
    for index in range(ramType):
        series = int(math.ceil(a/type_available[index][0])) # local parameter, calculate how many LUTs in series
        parallel = int(math.ceil(b/type_available[index][1])) # local parameter, calculate how many LUTs in parallel
        total = series * parallel
        if (rtotal > total): # new combination saves space
            rtotal = total
            depth = type_available[index][0]
            width = type_available[index][1]
            rparallel = parallel
            rseries = series
    return depth,width,rseries,rparallel


# find the best combination of rams that minimize the space
# for 8k BRAM
def bestFit8kSeries(a,b,id,portType):
    if(portType):
        sKBRAM1 = sKBRAM_T()
        type_available = space[0:5]
    else:
        sKBRAM1 = sKBRAM()
        type_available = space
    ramType = sKBRAM1.num
    rtotal = math.inf # initial value, will be replaced
    rseries = 1
    rparallel = 1
    depth = sKBRAM1.words1
    width = sKBRAM1.bits1
    for index in range(ramType):
        series = int(math.ceil(a/type_available[index][0])) # local parameter, calculate how many ram in series
        parallel = int(math.ceil(b/type_available[index][1])) # local parameter, calculate how many ram in parallel
        total = series * parallel
        if rtotal > total: # new combination saves space
            rtotal = total
            depth = type_available[index][0]
            width = type_available[index][1]
            rparallel = parallel
            rseries = series
    return depth,width,rseries,rparallel


# find the best combination of rams that minimize the space
# for 128k BRAM
def bestFit128kSeries(a,b,id,portType):
    if(portType):
        bKBRAM1 = bKBRAM_T()
        type_available = space1[0:7]
    else:
        bKBRAM1 = bKBRAM()
        type_available = space1
    ramType = bKBRAM1.num
    rtotal = math.inf # initial value, will be replaced
    rseries = 1
    rparallel = 1
    depth = bKBRAM1.words1
    width = bKBRAM1.bits1
    for index in range(ramType):
        series = int(math.ceil(a/type_available[index][0])) # local parameter, calculate how many ram in series
        parallel = int(math.ceil(b/type_available[index][1])) # local parameter, calculate how many ram in parallel
        total = series * parallel
        if rtotal > total: # new combination saves space
            rtotal = total
            depth = type_available[index][0]
            width = type_available[index][1]
            rparallel = parallel
            rseries = series
    return depth,width,rseries,rparallel

#Compute how many LBs required if using 128K RAM Only
def bBRAM (list):
    combination = []
    bKBRAM1 = bKBRAM()
    sum = 0
    for x in list:
        trueDual = (x[2] == "TrueDualPort  ")  # True if it is true dual port
        exceed = False
        Depth = int(x[3]) # depth
        Width = int(x[4]) # width
        logb = math.log(Width, 2)
        logb = math.ceil(logb)  # get minimum required number of ram in series
        num_parallel = 1
        num_series = 1
        extra_cir = 0
        selectmode = []
        if (2 ** logb == bKBRAM1.bits1): # no need parallel
            ##print('used style 1')
            num_series == math.ceil(Depth / bKBRAM1.words1)  # get minimum required series
            if (num_series == 1): # if perfectly fit in one ram, store the information
                selectmode.append(bKBRAM1.words1)
                selectmode.append(bKBRAM1.bits1)
                num_parallel = int(2 ** logb / bKBRAM1.bits1)
        elif (2 ** logb == bKBRAM1.bits2):
            ##print('used style 2')
            num_series = math.ceil(Depth / bKBRAM1.words2)  # get minimum required series
            if (num_series == 1):
                selectmode.append(bKBRAM1.words2)
                selectmode.append(bKBRAM1.bits2)
                num_parallel = int(2 ** logb / bKBRAM1.bits2)
        elif (2 ** logb == bKBRAM1.bits3):
            ##print('used style 3')
            num_series = math.ceil(Depth / bKBRAM1.words3)  # get minumum required series
            if (num_series == 1):
                selectmode.append(bKBRAM1.words3)
                selectmode.append(bKBRAM1.bits3)
                num_parallel = int(2 ** logb / bKBRAM1.bits3)
        elif (2 ** logb == bKBRAM1.bits4):
            ##print('used style 4')
            num_series = math.ceil(Depth / bKBRAM1.words4)  # get minumum required series
            if (num_series == 1):
                selectmode.append(bKBRAM1.words4)
                selectmode.append(bKBRAM1.bits4)
                num_parallel = int(2 ** logb / bKBRAM1.bits4)
        elif (2 ** logb == bKBRAM1.bits5):
            ##print('used style 5')
            num_series = math.ceil(Depth / bKBRAM1.words5)  # get minumum required series
            if(num_series == 1):
                selectmode.append(bKBRAM1.words5)
                selectmode.append(bKBRAM1.bits5)
                num_parallel = int(2 ** logb / bKBRAM1.bits5)
        elif (2 ** logb == bKBRAM1.bits6 and not trueDual):
            ##print('used style 6')
            num_series = math.ceil(Depth / bKBRAM1.words6)  # get minumum required series
            if (num_series == 1):
                selectmode.append(bKBRAM1.words6)
                selectmode.append(bKBRAM1.bits6)
                num_parallel = int(2 ** logb / bKBRAM1.bits6)
        elif (2 ** logb == bKBRAM1.bits7 and not trueDual):
            ##print('used style 7')
            num_series = math.ceil(Depth / bKBRAM1.words7)  # get minumum required series
            if (num_series == 1):
                selectmode.append(bKBRAM1.words7)
                selectmode.append(bKBRAM1.bits7)
                num_parallel = int(2 ** logb / bKBRAM1.bits7)
        elif (2 ** logb == bKBRAM1.bits8 and not trueDual):
            ##print('used style 8')
            num_series = math.ceil(Depth / bKBRAM1.words8)  # get minumum required series
            if (num_series == 1):
                num_parallel = int(2 ** logb / bKBRAM1.bits8)
                selectmode.append(bKBRAM1.words8)
                selectmode.append(bKBRAM1.bits8)

        # Need extra logic to config the RAM Required
        ## First, check if parallel can fix the problem, if so, do parallel
        else:
            if (trueDual): # if true dual port, only consider 16 bits as the maximum
                num_series = math.ceil(Depth/ bKBRAM1.words5)  # get minumum required series
                if (num_series == 1):
                    selectmode.append(bKBRAM1.words5)
                    selectmode.append(bKBRAM1.bits5)
                    num_parallel = int(2 ** logb / bKBRAM1.bits5)
            else:
                num_series = 2

        # if requires series, haven't append type
        if (num_series > 1): #need series
            ##x[1] is the RAM id
            depth,width,num_series,num_parallel = bestFit128kSeries(Depth,Width,x[1],trueDual) # get the best combination of series, formate
            selectmode.append(depth)
            selectmode.append(width)
            decoder = decoderCount(num_series)
            mux,exceed = muxCount(num_series)
            mux = mux  * Width
            if (trueDual):
                mux = mux * 2
                decoder = decoder *2
            extra_cir = decoder + mux
        totalRAM = num_series * num_parallel
        total_LB = math.ceil(extra_cir/N) + num_parallel * num_series * bKRAMspace
        sum = total_LB + sum
        combination.append([x[0], x[1], total_LB, int(extra_cir), selectmode[0], selectmode[1], num_series, num_parallel,totalRAM, sum, exceed])
    return combination

#Compute how many LBs required if using 8K RAM
def sBRAM (list):
    combination = []
    sKBRAM1 = sKBRAM()
    sum = 0
    for x in list:
        trueDual = (x[2] == "TrueDualPort  ") # True if it is true dual port
        exceed = False
        Depth = int(x[3])
        Width = int(x[4])
        logb = math.log(Width, 2)
        logb = math.ceil(logb)  # get minimum required number of bits width
        num_parallel = 1
        num_series = 1
        extra_cir = 0
        selectmode = []
        if (2 ** logb == sKBRAM1.bits1): # no need parallel
            ##print('used style 1')
            num_series == math.ceil(Depth / sKBRAM1.words1)  # get minimum required series
            if (num_series == 1): # if perfectly fit in one ram, store the information
                selectmode.append(sKBRAM1.words1)
                selectmode.append(sKBRAM1.bits1)
                num_parallel = int(2 ** logb / sKBRAM1.bits1)
        elif (2 ** logb == sKBRAM1.bits2):
            ##print('used style 2')
            num_series = math.ceil(Depth / sKBRAM1.words2)  # get minimum required series
            if (num_series == 1):
                selectmode.append(sKBRAM1.words2)
                selectmode.append(sKBRAM1.bits2)
                num_parallel = int(2 ** logb / sKBRAM1.bits2)
        elif (2 ** logb == sKBRAM1.bits3):
            ##print('used style 3')
            num_series = math.ceil(Depth / sKBRAM1.words3)  # get minumum required series
            if (num_series == 1):
                selectmode.append(sKBRAM1.words3)
                selectmode.append(sKBRAM1.bits3)
                num_parallel = int(2 ** logb / sKBRAM1.bits3)
        elif (2 ** logb == sKBRAM1.bits4):
            ##print('used style 4')
            num_series = math.ceil(Depth / sKBRAM1.words4)  # get minumum required series
            if (num_series == 1):
                selectmode.append(sKBRAM1.words4)
                selectmode.append(sKBRAM1.bits4)
                num_parallel = int(2 ** logb / sKBRAM1.bits4)
        elif (2 ** logb == sKBRAM1.bits5):
            ##print('used style 5')
            num_series = math.ceil(Depth / sKBRAM1.words5)  # get minumum required series
            if(num_series == 1):
                selectmode.append(sKBRAM1.words5)
                selectmode.append(sKBRAM1.bits5)
                num_parallel = int(2 ** logb / sKBRAM1.bits5)

        elif (2 ** logb == sKBRAM1.bits6 and not trueDual):
            num_series = math.ceil(Depth / sKBRAM1.words6)  # get minumum required series
            if (num_series == 1):
                selectmode.append(sKBRAM1.words6)
                selectmode.append(sKBRAM1.bits6)
                num_parallel = int(2 ** logb / sKBRAM1.bits6)
        # Need extra logic to config the RAM Required
        ## First, check if parallel can fix the problem, if so, do parallel
        else:
            if (trueDual): # if true dual port, only consider 16 bits as the maximum
                num_series = math.ceil(Depth / sKBRAM1.words5)  # get minumum required series
                if (num_series == 1):
                    selectmode.append(sKBRAM1.words5)
                    selectmode.append(sKBRAM1.bits5)
                    num_parallel = int(2 ** logb / sKBRAM1.bits5)
            else:
                 # get number of parallel RAM
                num_series = 2  # get minimum required series
        # if requires series, haven't append type
        if (num_series > 1): #need series
            ##x[1] is the RAM id
            depth,width,num_series,num_parallel = bestFit8kSeries(Depth,Width,x[1],trueDual) # get the best combination of series, formate
            selectmode.append(depth)
            selectmode.append(width)
            decoder = decoderCount(num_series)
            mux,exceed = muxCount(num_series)
            mux = mux  * Width
            if (trueDual):
                mux = mux * 2
                decoder = decoder *2
            extra_cir = decoder + mux
        totalRAM = num_series * num_parallel
        total_LB = math.ceil(extra_cir/N) + num_parallel * num_series * sKRAMspace
        sum = total_LB + sum
        combination.append([x[0], x[1], total_LB, int(extra_cir), selectmode[0], selectmode[1], num_series, num_parallel,totalRAM, sum, exceed])
    return combination

# Count how many LB required if using LUTRAM to implement
def lutCount (list):
    lutRAM1 = lutRAM()
    extra_cir = 0
    result = []
    sum = 0
    for x in list:
        TrueDual = (x[2] == "TrueDualPort  ")
        exceed = False
        selectmode = []
        a = int(x[3]) #Depth
        b = int(x[4]) #Width
        parallel = 99 # a random value that cannot be achieve
        series = 99
        #Check if can be implement in parallel mode
        if (b>10 and not TrueDual):
            series = math.ceil(a / lutRAM1.words2)
            if(series == 1):
                parallel = math.ceil(b/lutRAM1.bits2)
                selectmode.append(lutRAM1.words2)
                selectmode.append(lutRAM1.bits2)
        elif (b<=10 and not TrueDual):
            series = math.ceil(a/lutRAM1.words1)
            if (series == 1):
                parallel = 1
                selectmode.append(lutRAM1.words1)
                selectmode.append(lutRAM1.bits1)
        if(series > 1 and not TrueDual):
            depth,width,series,parallel = bestFitlutSeries(a,b,x[1])
            decoder = decoderCount(series)
            mux,exceed = muxCount(series)
            mux = mux  * b
            if (mux == 0):
                extra_cir = 0
            else:
                extra_cir = decoder + mux
            selectmode.append(depth)
            selectmode.append(width)
        else:
            selectmode.append(0)
            selectmode.append(0)
        total_LB = int(math.ceil(extra_cir / N) + (series * parallel) * (1/m_LUTRAM)) #total lb requires
        sum = sum + total_LB
        result.append([x[0], x[1], total_LB, int(extra_cir), selectmode[0], selectmode[1], series, parallel, sum, exceed])
    return result

#return which type is more cost-effective
def modeChose2 (a,b):
    return 2 if(a[2] < b[2]) else 3

#return which type is more cost-effective
def modeChose3 (a,b,c):
    return 2 if(a[2] < b[2] and a[2]<c[2]) else (3 if(b[2] < a[2] and b[2] < c[2]) else 1)

'''
Main Algorithm for mapping

#comb => 8kBRAM, comb2 => 128kBRAM, comb3 => LUTRAM
Try to fill-up with 128kBRAM first, then with 8kBRAM, lastly with LUT RAM
# cir_count (circuit_id,occupied_lb,sKRAM,bKRAM,useable_LUT,next_sKRAM,next_bKRAM)
# comb1, [Circuit Id, Ram ID, total_LB, int(extra_cir), selectmode[0], selectmode[1], num_series, num_parallel,totalRAM, sum]
# comb3 [Circuit Id, Ram ID, total_LB, int(extra_cir), selectmode[0], selectmode[1], series, parallel, sum]
# circuits ['0', '0', 'SimpleDualPort', '45', '12']
'''
def matchRAM(cir_count, comb, comb2, comb3, circuit):
        un_used_sRAM = int(cir_count[2]) # number of 8kRAM embeded in the un-ram lbs
        un_used_bRAM = int(cir_count[3]) # number of 128kRAM embeded in the un-ram lbs
        un_used_LUTRAM = int(cir_count[4]) # number of LUTRAM available
        end = len(circuit) # how many RAM need to do
        output = []
        total_lb = comb3[end-1][8] # total required max of luts
        total_lb -= un_used_LUTRAM
        used_lb = 0
        extra_spadding = 0 # in LB
        extra_bpadding = 0
        extra_circuit = 0
        extra_circuit2 = 0
        for index in range(end):
            Id = index
            Mode = circuit[index][2]
            TrueDual = (circuit[index][2] == "TrueDualPort  ")
            circuit_id = comb[index][0]
            ram_id = comb[index][1]
            LW = circuit[index][4] #width
            LD = circuit[index][3] #depth
            if (un_used_sRAM > 0 or un_used_bRAM > 0) and (comb[index][2]>un_used_sRAM or comb2[index][2]>un_used_bRAM):
                Type = modeChose2(comb[index], comb2[index])

                if (un_used_bRAM > 0 and Type == 3):
                    # if bRAM still available, then all in bRAM
                    un_used_bRAM = un_used_bRAM - comb2[index][8]
                    if (un_used_bRAM < 0):
                        #extra_cir += comb2[index][3]
                        extra_bpadding += (un_used_bRAM) * bKRAMspace  # calculate the number of lb to borrow
                        extra_bpadding += (cir_count[6])
                    # print("128kram")
                    S = comb2[index][6]
                    P = comb2[index][7]
                    W = comb2[index][5]
                    D = comb2[index][4]
                    extra = comb2[index][3]
                    total_lb = total_lb - comb3[index][2]
                    extra_circuit += math.ceil(extra / N)
                    extra_circuit2 += math.ceil(extra / N)
                elif (un_used_sRAM > 0 and Type == 2):
                    un_used_sRAM = un_used_sRAM - comb[index][8]
                    if (un_used_sRAM < 0):
                        #extra_cir += comb[index][3]
                        extra_spadding += (un_used_sRAM) * sKRAMspace  # calculate the number of LB to borrow
                        extra_spadding += cir_count[5]
                    # print("8kram")
                    S = comb[index][6]
                    P = comb[index][7]
                    W = comb[index][5]
                    D = comb[index][4]
                    extra = comb[index][3]
                    total_lb = total_lb - comb3[index][2]
                    extra_circuit += math.ceil(extra / N)
                    extra_circuit2 += math.ceil(extra / N)
                elif(un_used_bRAM > 0 and Type == 2):
                    Type = 3
                    un_used_bRAM = un_used_bRAM - comb2[index][8]
                    if(un_used_bRAM < 0):
                        #extra_cir += comb2[index][3]
                        extra_bpadding += (un_used_bRAM) * bKRAMspace # calculate the number of lb to borrow
                        extra_bpadding += (cir_count[6])
                    #print("128kram")
                    S = comb2[index][6]
                    P = comb2[index][7]
                    W = comb2[index][5]
                    D = comb2[index][4]
                    extra = comb2[index][3]
                    extra_circuit += math.ceil(extra / N)
                    extra_circuit2 += math.ceil(extra / N)
                    total_lb = total_lb - comb3[index][2]
                # un_used_sBRAm > 0, Type ==3
                else:
                    un_used_sRAM = un_used_sRAM - comb[index][8]
                    Type = 2
                    if(un_used_sRAM < 0):
                        #extra_cir += comb[index][3]
                        extra_spadding += (un_used_sRAM) * sKRAMspace # calculate the number of LB to borrow
                        extra_spadding += cir_count[5]
                    #print("8kram")
                    S = comb[index][6]
                    P = comb[index][7]
                    W = comb[index][5]
                    D = comb[index][4]
                    extra = comb[index][3]
                    extra_circuit += math.ceil(extra / N)
                    extra_circuit2 += math.ceil(extra / N)
                    total_lb = total_lb - comb3[index][2]

            # Case II
            # If all RAMs within the Logical Blocks Circuits are been used
            # Still demands for RMAs, need to expand the circuit
            else:
                if(total_lb > used_lb):
                    # if there is a 128k ram available and the next ram can fit this spot
                    if (extra_bpadding >= bKRAMspace and comb2[index][2] <= extra_bpadding):
                        Type = 3
                        total_lb -= comb3[index][2]
                        #print("128Kram")
                        S = comb2[index][6]
                        P = comb2[index][7]
                        W = comb2[index][5]
                        D = comb2[index][4]
                        extra_bpadding -= comb2[index][2]
                        extra = comb2[index][3]
                        extra_circuit += math.ceil(extra / N)
                        extra_circuit2 += math.ceil(extra / N)
                        used_lb += comb2[index][2]
                        extra = comb2[index][3]
                    else:
                        Type = 2
                        total_lb = total_lb - comb3[index][2]
                        extra_bpadding += comb[index][2]
                        #print("8kram")
                        S = comb[index][6]
                        P = comb[index][7]
                        W = comb[index][5]
                        D = comb[index][4]
                        extra = comb[index][3]
                        extra_circuit += math.ceil(extra / N)
                        extra_circuit2 += math.ceil(extra / N)
                        used_lb += comb[index][2]

                elif(TrueDual or comb3[index][9]):
                    Type = modeChose2(comb[index], comb2[index])
                    if(Type == 2):
                        #print('8kram')
                        S = comb[index][6]
                        P = comb[index][7]
                        W = comb[index][5]
                        D = comb[index][4]
                        extra = comb[index][3]
                        extra_circuit += math.ceil(extra / N)
                        extra_circuit2 += math.ceil(extra / N)
                        used_lb += comb[index][2]
                    else:
                        #'128kram'
                        S = comb2[index][6]
                        P = comb2[index][7]
                        W = comb2[index][5]
                        D = comb2[index][4]
                        extra = comb2[index][3]
                        extra_circuit += math.ceil(extra / N)
                        extra_circuit2 += math.ceil(extra / N)
                        used_lb += comb2[index][2]
                    total_lb -= comb3[index][2]

                # use LUTRAM to match the gap
                else:
                    Type = 1
                    #print('LUTRAM')
                    S = comb3[index][6]
                    P = comb3[index][7]
                    W = comb3[index][5]
                    D = comb3[index][4]
                    extra = comb3[index][3]
                    extra_circuit += math.ceil(extra / N)
                    extra_circuit2 += math.ceil(extra / N)
                    total_lb = total_lb - comb3[index][2]
                    used_lb += comb3[index][2]

            if(extra_circuit >= sKRAMspace):
                extra_circuit -= sKRAMspace
                un_used_sRAM += 1
            elif(extra_circuit2 >= bKRAMspace):
                extra_circuit2 -= bKRAMspace
                un_used_bRAM += 1
            #generate desired output format for checker program
            selection = []
            selection.append(str(circuit_id))
            selection.append(str(ram_id))
            selection.append(str(extra))
            selection.append("LW")
            selection.append(str(LW))
            selection.append("LD")
            selection.append(str(LD))
            selection.append("ID")
            selection.append(str(Id))
            selection.append("S")
            selection.append(str(S))
            selection.append("P")
            selection.append(str(P))
            selection.append("Type")
            selection.append(str(Type))
            selection.append("Mode")
            selection.append(Mode.replace(" ", ""))
            selection.append("W")
            selection.append(str(W))
            selection.append("D")
            selection.append(str(D))
            output.append(selection)
        return output

# Sort the list such that circuit with bigger RAM requirement goes first
def SortCircuit(circuits):
    return sorted(circuits, key = lambda x: x[5], reverse = True)

# Read both the document, store in array
f = open("logical_rams.txt", "r")
next(f)
next(f)#skip the two lines header
logicram = (f.read().splitlines())
f.close()

f2 = open("logic_block_count.txt", "r")
next(f2)
blockcount = (f2.read().splitlines())
f2.close()

# Separate circuits from the file
circuits = []
cir_count = []

for index in range(69): #total of 69 benchmark circuits
    row = []
    cir_count.append(countRam(blockcount[index])) #calculate how many 8kRAM, 128kRAM available
    for x in logicram:
        x_n = x.split("\t")
        if int(x_n[0]) == index:
            total_size = int(int(x_n[3])*int(x_n[4]))
            row.append(list((x_n[0],x_n[1], x_n[2], x_n[3],x_n[4], total_size)))
    circuits.append(row)

output = []
for index in range(0,69):
    a = SortCircuit((circuits[index]))
    b = sBRAM(a)
    c = bBRAM(a)
    d = lutCount(a)
    result = matchRAM(cir_count[index],b,c,d,a)
    output.append(result)
saveFile(output)

print("--- CPU Run Time %s  ---" % (time.time() - start_time))