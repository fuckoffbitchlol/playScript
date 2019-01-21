import re
import os
from statistics import stdev

# dataList = ["magic", "penbased","ring", "segment", "texture"]
#dataList = ["page-blocks", "satimage","spambase", "twonorm"]
dataList = ["letter", "letter"]

# dataList = ["bupa", "glass","heart", "pima", "yeast"]

for filename in dataList:

    # dir = "C:\\Users\\gao\\Desktop\\1201_noParallel\\major_ensemble_all"
    dir = "C:\\Users\\gao\\Desktop\\balance_big2"
    
    filenum = 1
    parallelParts = 20

    ave_train = 0
    ave_test = 0
    es_test = 0
    train = 0
    test = 0
    rule = 0
    time = 0
    temp_cnt = 1
    temp_train = 0
    temp_test = 0
    file_count = 1
    TencvTime = 0
    count = 0
    testVa = []
    trainVa = []
    tiedTime = 0
    sameCnt = 0

    combiNum = int((parallelParts*(parallelParts-1)/2))

    dm_list = [0]*combiNum
    qs_list = [0]*combiNum
    ks_list = [0]*combiNum

    os.chdir(dir)
    for path, subdirs, files in os.walk("."):
        for f in files:
            f = os.path.join(path, f)
            if f.endswith(".txt") and f.find("result") and f.find(filename) != -1:
                if f.find("result10") is -1:

                    # read single file to fetch data
                    f = open(f, "r", encoding = "utf-8")

                    trainAssigned = False
                    assignCnt = 0
                    # for diversity measure
                    dm_cnt = 0
                    qs_cnt = 0
                    ks_cnt = 0

                    line=f.readline()
                    tmp_es = 0
                    tmp_test = 0
                    while line:
                        if line.find("dm") != -1:
                            Str = line.split(" ")
                            print(Str)
                            tmp = Str[3].split(":")
                            print (tmp)
                            dm_list[dm_cnt] += float(tmp[1])

                            dm_cnt += 1
                        
                        if line.find("kstatic") != -1:
                            Str = line.split(" ")
                            tmp = Str[3].split(":")
                            ks_list[ks_cnt] += float(tmp[1])

                            ks_cnt += 1

                        if line.find("qstatic") != -1:
                            Str = line.split(" ")
                            tmp = Str[3].split(":")
                            qs_list[ks_cnt] += float(tmp[1])
                            qs_cnt += 1
                        
                        # if line.find("classifier:") != -1 and trainAssigned is False:
                        #     Str = line.split(" ")
                        #     tmp = Str[1].split(":")
                        #     ave_train += float(tmp[1])
                        #     assignCnt += 1
                        #     if assignCnt == parallelParts:
                        #         trainAssigned = True
                        if line.find("test acc:") != -1:
                            Str = line.split(":")
                            print(Str)
                            ave_test += float(Str[1])
                            

                        if line.find("final Ensemble") == 0:
                            Str = line.split(":")
                            es_test += float(Str[1])
                            tmp_es = float(Str[1])

                        if line.find("instance Num") == 0:
                            Str = line.split(" ")
                            tmpStr = Str[2].split(":")
                            tiedTime += int(tmpStr[1])
                        if line.find("training accuracy") == 0:
                            count += 1
                            Str=line.split("=")
                            train+=float(Str[1])
                            temp_train += float(Str[1])
                            trainVa.append(float(Str[1]))
                        elif line.find("test accuracy")== 0:
                            Str=line.split("=")
                            # print (float(Str[1]))
                            test+=float(Str[1])
                            temp_test += float(Str[1])
                            testVa.append(float(Str[1]))
                            tmp_test = float(Str[1])
                        elif re.search("Default rule",line):
                            Str=line.split(":")
                            rule+=float(Str[0])+1
                        elif line.find("Total time")==0:
                            Str=line.split(":")

                        line=f.readline()

                    if tmp_es == tmp_test:
                        sameCnt += 1
                        print (f)
                    f.close()
                    file_count += 1

    print (count)
    outfile=open("{}.txt".format(filename),"w")
    outfile.write("%f %f %f %f %f %f\n"%(rule/count, 100 - 100*ave_train/(count*parallelParts)
                                ,100 - 100*ave_test/(count*parallelParts),time/(10*filenum),\
                                    stdev(trainVa), stdev(testVa)))

    outfile.write("Ensemble: %f\n" % (100 - 100*es_test/count))
    outfile.write("tiedTime: %d %d\n" % (tiedTime, sameCnt))
    # for i in range(parallelParts):
    #     outfile.write("{} dm ks qs: {} {} {}\n".format(i, dm_list[i]/count, ks_list[i]/count, qs_list[i]/count))
    outfile.write("sum dm ks: {} {}\n".format(sum(dm_list)/(count*combiNum), sum(ks_list)/(count*combiNum)))
    outfile.close()
