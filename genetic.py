import random
import math
import collections
import redis
import subprocess

r = redis.Redis(host='127.0.0.1', port = 6379, db=0)
r.flushall()

#print("Enter Number of Queens:")
#nqueen = int(input())

#print("Enter % of Mutation:")
#mi = int(input())

#print("Enter % of CrossOver:")
#co = int(input())
nqueen=8
mi=2
co=7

# Vars
loop = 0
find = 0
npop = 1000
mi =round(mi%10)
co =round((co%10)*2)

#Lists
kia = []
mylist = []
newGeneration = []
p1 = []
p2 = []



def CalculateFitness(chromosome = []):
    Fitness = 0
    for i in range(len(chromosome)):
        for j in range(i+1, len(chromosome)-1):
            #if i + j == nqueen + 1 :
            #    Fitness+=1
            #elif i == j:
            #    Fitness+=1
            if chromosome[i] == chromosome[j]:
                Fitness+=1
            elif math.fabs(chromosome[i] - chromosome[j]) == j - i:
                Fitness+=1
            elif math.fabs(chromosome[j] - chromosome[i]) == i - j:
                Fitness+=1


    return Fitness

def SortbyFitness(chromosome = []):
    tmp = []
    for b in range(1):
        for c in range(npop):
            f = chromosome[c].pop()
            tmp.append(f)
    tmp.sort()
    return tmp

def Mutation(Chromosome = []):
    randOne = random.randint(1,nqueen-1)
    randTwo = random.randint(1,nqueen-1)
    while randOne == randTwo:
        randTwo = random.randint(1,nqueen-1)
    t1 = Chromosome[randOne]
    Chromosome[randOne] = Chromosome[randTwo]
    Chromosome[randTwo] = t1
    Newfitnes = CalculateFitness(Chromosome)
    Chromosome[nqueen] = Newfitnes
    return Chromosome

tmp_slice = []
for b in range(nqueen):
    for c in range(npop):
        tmp_slice.append(0)

def CrossOver(Parent1 = [], Parent2 = []):
    PointSlice = int(nqueen/3)
    for a in range(0, PointSlice):
        tmp_slice[a] = Parent1[a]
        Parent1[a] = Parent2[a]
        Parent2[a] = tmp_slice[a]
    nf1 = CalculateFitness(Parent1)
    nf2 = CalculateFitness(Parent2)
    Parent1[nqueen] = nf1
    Parent2[nqueen] = nf2
    return Parent1,Parent2

def FisrtGeneration():
    ordered = []
    ordered = sorted(kia,key=lambda l:l[nqueen], reverse=False)
    return ordered

def CreateNewGeneration(Generaton = []):
    for order in range (len(Generaton)):
        if order < mi:
            newGeneration.append(Mutation(Generaton[order]))
            continue
        elif order < mi+co :
            p1,p2 = CrossOver(Generaton[order],Generaton[order+1])
            newGeneration.append(p1)
        return newGeneration

def CreateBoard(chromosome = []):
    for N in range(len(chromosome)-1):
        print("", end="|")
        queen = chromosome[N]
        for col in range(1,len(chromosome)):
            if col == queen:
                print("Q", end="|")
            else:
                print("_", end="|")
        print("")


for a in range(npop):
    kia.append([])

for b in range(nqueen):
    for c in range(npop):
        kia[c].append(random.randint(1,nqueen))
        tmp_slice.append(0)

for t in range(npop):
        f = CalculateFitness(kia[t])
        kia[t].append(f)

FisrtGeneration()
mylist = CreateNewGeneration(FisrtGeneration())



while True:
    if find == 1:
        break
    if loop > 200:
        del mylist[:]
        FisrtGeneration()
        mylist = CreateNewGeneration(FisrtGeneration())

    for mylst in range (len(mylist)):
        r.incr(mylist[mylst][nqueen])
        if mylist[mylst][nqueen] == 0:
            find = 1
            print("find in loop: " + str(loop))
            print(mylist[mylst])
            CreateBoard(mylist[mylst])
            break
        else:
            print("in loop: " + str(loop))
            print(mylist[mylst])

            loop+=1
            mylist = CreateNewGeneration(mylist)

subprocess.call("./hist.sh")
