import numpy as np
import matplotlib.pyplot as plt

# 加载数据
def loadDataset(filename):
    data =  np.loadtxt(filename)
    return data

#欧式距离计算
def distEclud(x,y):
    return np.sqrt(np.sum((x-y)**2))

#为给定数据集构建一个包含k个随机质心的集合
def randCent(dataset,k):
    m,n = dataset.shape
    centroids =  np.zeros((k,n))
    for i in range(k):
        index = int(np.random.uniform(0,m))
        centroids[i,:] = dataset[index,:]
    return centroids

# k 均值聚类
def KMeans(dataSet,k):
    m = np.shape(dataSet)[0] # 行的个数
    n = np.shape(dataSet)[1] # 列的个数
    # 第一列存样本属于哪一簇
    # 第二列存样本的到簇的中心点的误差
    clusterAssment = np.mat(np.zeros((m,2)))
    clusterChange = True
 
    # 第1步 初始化centroids
    centroids = randCent(dataSet,k)
    while clusterChange:
        clusterChange = False
 
        # 遍历所有的样本（行数）
        for i in range(m):
            minDist = 100000.0
            minIndex = -1
 
            # 遍历所有的质心
            #第2步 找出最近的质心
            for j in range(k):
                # 计算该样本到质心的欧式距离
                distance = distEclud(centroids[j,:],dataSet[i,:])
                if distance < minDist:
                    minDist = distance
                    minIndex = j
            # 第 3 步：更新每一行样本所属的簇
            if clusterAssment[i,0] != minIndex:
                clusterChange = True
                clusterAssment[i,:] = minIndex,minDist**2
        #第 4 步：更新质心
        for j in range(k):
            pointsInCluster = dataSet[np.nonzero(clusterAssment[:,0].A == j)[0]]  # 获取簇类所有的点
            centroids[j,:] = np.mean(pointsInCluster,axis=0)   # 对矩阵的行求均值
 
    print("Congratulations,cluster complete!")
    return centroids,clusterAssment
def showCluster(dataSet,k,centroids,clusterAssment):
    m,n= dataSet.shape
 
    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
    if k > len(mark):
        print("k值太大了")
        return 1
    # 绘制所有的样本
    for i in range(m):
        markIndex = int(clusterAssment[i,0])
        plt.plot(dataSet[i,0],dataSet[i,1],mark[markIndex])
 
    mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']
    # 绘制质心
    for i in range(k):
        plt.plot(centroids[i,0],centroids[i,1],marker='x')
 
    plt.show()
def testKmeans(dataSet,k,centroids):
    f = open("test.txt",'a')
    m,n=dataSet.shape
    for i in range(m):
        kind = 0
        mindist = 100000.0
        for j in range(k):
            dist = distEclud(centroids[j,:],dataSet[i,:])
            if dist < mindist:
                kind = j+1
                mindist=dist
        # 输出改行数据
        for p in range(n):
            f.write(str(dataSet[i][p]))
            f.write(" ")
        f.write(str(kind))
        f.write('\n')
    print("success test")
dataSet = loadDataset("seeds_dataset.txt")
#去掉最后一列 （为目标）
dataSet = np.delete(dataSet,-1,axis=1)
k = 3
centroids,clusterAssment = KMeans(dataSet,k)
showCluster(dataSet,k,centroids,clusterAssment)
#测试
testKmeans(dataSet,k,centroids)
