import csv
from random import *
from math import *
from datetime import *

def flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

def dexp(x):
    if x<-100:
        return 0
    elif x>100:
        return exp(100)
    else:
        return exp(x)

def flipLinks(linka, linkb):
    temp = hashOrdem[linkb]
    hashOrdem[linkb] = hashOrdem[linka]
    hashOrdem[linka] = temp

def localEner(linksArray, pair):
    i=pair[0];
    j=pair[1];
    ilocal = hashOrdem[pair[0]]
    jlocal = hashOrdem[pair[1]]
    return abs(i-j)*(-(2*linksArray.get((ilocal, jlocal),0) - 1)*(linksArray.get((hashOrdem[down[i]], jlocal),0) + linksArray.get((ilocal, hashOrdem[down[j]]),0) +linksArray.get((hashOrdem[up[i]], jlocal),0) + linksArray.get((ilocal, hashOrdem[up[j]]),0) - 2) + 2)

def crossEner(linksArray, i):
    ilocal = hashOrdem[i]
    par1=sum([(abs(i-j)*(-(2*linksArray.get((ilocal, hashOrdem[j]),0) - 1)*(linksArray.get((hashOrdem[down[i]], hashOrdem[j]),0) + linksArray.get((ilocal, hashOrdem[down[j]]),0) +linksArray.get((hashOrdem[up[i]],hashOrdem[j]),0) + linksArray.get((ilocal, hashOrdem[up[j]]),0) - 2) + 2)) for j in range(nnodes)])
    par2=sum([(abs(i-j)*(-(2*linksArray.get(( hashOrdem[j],ilocal),0) - 1)*(linksArray.get(( hashOrdem[j],hashOrdem[down[i]]),0) +         linksArray.get(( hashOrdem[down[j]],ilocal),0) +linksArray.get((hashOrdem[j],hashOrdem[up[i]]),0) + linksArray.get(( hashOrdem[up[j]],ilocal),0) - 2) + 2)) for j in range(nnodes)])
    return par1+par2

def geraListDiflin(i,j):
    difList
    for pos in range(nnodes):
        if( linksArray.get(( i,pos),0)!=linksArray.get(( j,pos),0)):
            difList.append(pos)
    return difList

def geraListDifcol(i,j):
    difList=[]
    for pos in range(nnodes):
        if( linksArray.get(( pos,i),0)!=linksArray.get((pos,j),0)):
            difList.append(pos)
    return difList


def crossEner(linksArray, i,lislin,liscol):
    ilocal=hashOrdem[i]
    par1=sum([(abs(i-j)*(-(2*linksArray.get((ilocal, hashOrdem[j]),0) - 1)*(linksArray.get((hashOrdem[down[i]], hashOrdem[j]),0) + linksArray.get((ilocal, hashOrdem[down[j]]),0) +linksArray.get((hashOrdem[up[i]],hashOrdem[j]),0) + linksArray.get((ilocal, hashOrdem[up[j]]),0) - 2) + 2)) for j in lislin])
    par2=sum([(abs(i-j)*(-(2*linksArray.get(( hashOrdem[j],ilocal),0) - 1)*(linksArray.get(( hashOrdem[j],hashOrdem[down[i]]),0) + linksArray.get(( hashOrdem[down[j]],ilocal),0) +linksArray.get((hashOrdem[j],hashOrdem[up[i]]),0) + linksArray.get(( hashOrdem[up[j]],ilocal),0) - 2) + 2)) for j in liscol])
    return par1+par2


def crossEnerComp(linksArray, i):
    ilocal = hashOrdem[i]
    par1=sum([(abs(i-j)*(-(2*linksArray.get((ilocal, hashOrdem[j]),0) - 1)*(linksArray.get((hashOrdem[down[i]], hashOrdem[j]),0) + linksArray.get((ilocal, hashOrdem[down[j]]),0) +linksArray.get((hashOrdem[up[i]],hashOrdem[j]),0) + linksArray.get((ilocal, hashOrdem[up[j]]),0) - 2) + 2)) for j in range(nnodes)])
    par2=sum([(abs(i-j)*(-(2*linksArray.get(( hashOrdem[j],ilocal),0) - 1)*(linksArray.get(( hashOrdem[j],hashOrdem[down[i]]),0) + linksArray.get(( hashOrdem[down[j]],ilocal),0) +linksArray.get((hashOrdem[j],hashOrdem[up[i]]),0) + linksArray.get(( hashOrdem[up[j]],ilocal),0) - 2) + 2)) for j in range(nnodes)])
    return par1+par2



def calcDeltaE(linksArray, pair):
    (sitionovo,sitioatual)=pair
    lislin=[]
    liscol=[]
    for pos in range(nnodes):
        if(linksArray.get((hashOrdem[sitionovo],pos),0)!=linksArray.get((hashOrdem[sitioatual],pos),0)):
            lislin=lislin+[pos,down[pos],up[pos]]
        if(linksArray.get((pos,hashOrdem[sitionovo]),0)!=linksArray.get((pos,hashOrdem[sitioatual]),0)):
            liscol=liscol+[pos,down[pos],up[pos]]
    viz=set([down[sitionovo],sitionovo,up[sitionovo],down[sitioatual],sitioatual,up[sitioatual]])
    lislin=set(lislin)
    liscol=set(liscol)
    lispairs=[]
    for sitio1 in viz:
         for sitio2 in viz:
             if (sitio1!=sitio2):
                 lispairs.append((sitio1,sitio2))       
    listodos=[]
    for sitio1 in lislin:
        for sitio2 in liscol:
            listodos.append((sitio1,sitio2))
            #       print listodos
    listodos=set(listodos)
    setfinal=set(listodos).intersection(set(lispairs))
    #print "viz=", viz
    E1=sumE(linksArray, viz,lislin,liscol,setfinal)
    flipLinks(pair[0], pair[1])    
    E2=sumE(linksArray, viz,lislin,liscol,setfinal)
    flipLinks(pair[0], pair[1])  
    return E2-E1
    
def sumE(linksArray, viz,lislin,liscol,setfinal):
    E=0
    for sitio in viz:
        E+=crossEner(linksArray, sitio,lislin,liscol)
    #    print "bits=",linksArray.get((sitionovo,lislin[0]),0),linksArray.get((sitioatual,lislin[0]),0)
    for pair in setfinal:
        E-=localEner(linksArray, pair)
    return E

def calcEner(linksArray):
    sum=0
    for i in range(nnodes):
        for j in range(nnodes):
            ilocal = hashOrdem[i]
            jlocal = hashOrdem[j]
            sum+=abs(i-j)*(-(2*linksArray.get((ilocal, jlocal),0) - 1)*(linksArray.get((hashOrdem[down[i]], jlocal),0) + 
        linksArray.get((ilocal, hashOrdem[down[j]]),0) +linksArray.get((hashOrdem[up[i]], jlocal),0) + linksArray.get((ilocal, hashOrdem[up[j]]),0) - 2) + 2)
    return sum

def readGraph(file):
    csv.register_dialect('graph', delimiter='\t')
    lisver=[]
    with open(file, 'rb') as f:
        reader=csv.reader(f, 'graph')
        for row in reader:
            if row[0]!=row[1]: 
                lisver.append((row[0],row[1]))
    return lisver

def geraArray(lisver):
    linksArray={}
    for vertex in lisver:
   #     lisLinks.append([hashnodes[vertex[0]],hashnodes[vertex[1]]])
        linksArray[(hashnodes[vertex[0]],hashnodes[vertex[1]])]=1
    return linksArray

def readOrdem(file):
    hashOrdem={}
    with open(file, 'rb') as f:
        reader=csv.reader(f, 'ordem')
        for row in reader:
            hashOrdem[int(row[1])]=int(row[2])
    return hashOrdem

def testaDelta(linksArray,tests):
    for i in range(tests):
        print "Teste ",i
        nodea=randint(0,nnodes-1)
        nodeb=randint(0,nnodes-1)
        print nodea,nodeb
        ce1= calcDeltaE(linksArray,(nodea,nodeb))
        e1=calcEner(linksArray)
        flipLinks(nodea,nodeb)
        e2=calcEner(linksArray)
        ce2=e2-e1
        print ce1,ce2
        print "------------"

def geralisver():
    lisver =[]
    dis=sample(range(40),40)
    for j in range(20):
        for i in range(20):
            lisver.append([dis[i],dis[j]])
    for j in range(20,40,1):
        for i in range(20,40,1):
            lisver.append([dis[i],dis[j]])
    return lisver

def geraOrdemInit(tinit):
    hashOrdem={}
    if (tinit>0):
            hashOrdem={}
            file='ordemStep_'+str(tinit)+'.txt'
            with open(file, 'rb') as f:
                reader=csv.reader(f, 'ordem')
                for row in reader:
                    hashOrdem[int(row[1])]=int(row[2])
    else:   
        tinit=0
        for i in range(nnodes):
            hashOrdem[i]=i
    return hashOrdem
def geraTempInit(linksArray,samples):
    return (1./samples*sum([abs(1.0*calcDeltaE(linksArray,(randint(0,nnodes/2),randint(nnodes/2+1,nnodes-1)))) for i in range(samples)]))+1.

def geraHashNodes(nodes):
    hashnodes={}
    i=0
    for node in nodes:
        hashnodes[node]=i
        i=i+1
    return hashnodes
 
def geraUp(nnodes):
    up={}
    up[nnodes-1]=0
    for i in range(0,nnodes-1):
        up[i]=i+1
    return up

def geraDown(nnodes):
    down={}
    down[0]=nnodes-1
    for i in range(1,nnodes):
        down[i]=i-1
    return down

if __name__ == "__main__":
    csv.register_dialect('ordem', delimiter=',')
    lisver=readGraph('integrated.txt')
    #liver=geralisver
    nodes= set(flatten(lisver))
    nnodes=len(nodes)
    print "Numero de nodes=",nnodes
    hashnodes=geraHashNodes(nodes)
    linksArray=geraArray(lisver)
    up=geraUp(nnodes)
    down=geraDown(nnodes)
    tinit=177
    hashOrdem=geraOrdemInit(tinit)
    #testaDelta(linksArray,100)
    eneratual=calcEner(linksArray)
    enerinit=eneratual
    print "Ener=",eneratual
    samples=100
    tpassos = 200
    lis=[]
    t1=datetime.now()
    tempInicial=geraTempInit(linksArray,samples)
    DeltaT=tempInicial/tpassos
    print "Temp=",tempInicial
    for tsteps in range(tinit+1,tpassos,1):
        print "passo=",tsteps
        with open('matrix.txt', 'w') as f:
            for vertex in lisver:
                line=str(hashOrdem[hashnodes[vertex[0]]])+","+str(hashOrdem[hashnodes[vertex[1]]])+'\n'
                f.write(line)
        with open('ordemStep_'+str(tsteps)+'.txt', 'w') as f:
            for node in nodes:
                line=str(node)+','+str(hashnodes[node])+','+str(hashOrdem[hashnodes[node]])+'\n'
                f.write(line)
        temp=tempInicial-DeltaT*tsteps
        for steps in range(nnodes):
            [linka, linkb] = sample(range(nnodes),2)
            DeltaE = calcDeltaE(linksArray, (linka, linkb))
            if (dexp(-DeltaE/temp) > random()):
                eneratual = eneratual + DeltaE
                flipLinks(linka, linkb)
        for steps in range(10):
            linka=randint(0,nnodes-1)
            lisE=[calcDeltaE(linksArray,(linka,pos)) for pos in range(nnodes)]
            minE=min(lisE)
            posmin=sample([i for i,x in enumerate(lisE) if x == minE],1)[0]
            flipLinks(linka,posmin)
            eneratual=eneratual+lisE[posmin]
        lis.append([temp,eneratual])
        print datetime.now()-t1
        print eneratual
        t1=datetime.now()
        with open('energyStep_'+str(steps)+'.txt', 'w') as f:
            for elem in lis:
                line=str(elem[0])+'\t'+str(elem[1]*1.0/enerinit)+'\n'
                f.write(line)
    with open('energy.txt', 'w') as f:
        for elem in lis:
            line=str(elem[0])+'\t'+str(elem[1]*1.0/enerinit)+'\n'
            f.write(line)
    with open('ordem.txt', 'w') as f:
        for node in nodes:
            line=str(node)+'\t'+str(hashOrdem[hashnodes[node]])+'\n'
            f.write(line)
    with open('matrix.txt', 'w') as f:
        for vertex in lisver:
            line=str(hashOrdem[hashnodes[vertex[0]]])+","+str(hashOrdem[hashnodes[vertex[1]]])+'\n'
            f.write(line)
            
