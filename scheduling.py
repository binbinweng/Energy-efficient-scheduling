

from locale import ERA_D_FMT
import numpy as np
import sys
import random
from datetime import datetime
import ast
import math

def HEFT(EST, EFT, pos, pscheduling, qlist, T, c_t, E, n, p,frequency,processorinfo, c_p,ccr):
    EA=0
    for idx, i in enumerate(qlist):
        if idx<pos:
            continue
        EST[i-1][0]=0
        EST[i-1][1]=0
        EFT[i-1][0]=0
        EFT[i-1][1]=1000000
        for k in range(p):
            if idx==0:
                tmp = 0
                tmp2 = tmp+T[i-1][k]
                if tmp2<EFT[i-1][1]:
                    EFT[i-1][1]=tmp2
                    EFT[i-1][0]=k
                    EST[i-1][1]=tmp
                    EST[i-1][0]=k
                    #pscheduling[k]=tmp2
            else:
                pred = E[i-1]
                tmp = 0
                for idx2, l in enumerate(pred):
                    if l==1:
                        tmp = max(tmp,EFT[idx2][1]+c_t[idx2][i-1]*c_p[k][EFT[idx2][0]]*ccr)
                        #print(c_p[k][EFT[idx2][0]])
                tmp = max(tmp, pscheduling[k])
                tmp2 = tmp+T[i-1][k]
                if tmp2<EFT[i-1][1]:
                    EFT[i-1][1]=tmp2
                    EFT[i-1][0]=k
                    EST[i-1][1]=tmp
                    EST[i-1][0]=k
                    #pscheduling[k]=tmp2
        EA = EA + (processorinfo[EFT[i-1][0]][0]+processorinfo[EFT[i-1][0]][1]*pow(frequency[EFT[i-1][0]][1],processorinfo[EFT[i-1][0]][2]))*T[i-1][EFT[i-1][0]]
        pscheduling[EFT[i-1][0]]=EFT[i-1][1]
        #print(EFT)
    return EA,EFT[qlist[-1]-1][1]


def DUPRS1(EST, EFT, pos, pscheduling, qlist, T, c_t, E, n, p,latency,frequency,processorinfo,proc_freq,sl, c_p,ccr):
    EA = 0
    for idx, i in enumerate(qlist):
        ddl = EFT[i-1][1]*latency/sl
        p_energy = math.inf
        proc = EFT[i-1][0]
        proc_min = frequency[proc][0]
        proc_max = frequency[proc][1]
        stp = (proc_max-proc_min)/100
        rng = np.arange(proc_min, proc_max, stp)
        for f in rng:
            tmp = EST[i-1][1]+T[i-1][proc]*proc_max/f
            tmp2 = (processorinfo[proc][0]+processorinfo[proc][1]*pow(f,processorinfo[proc][2]))*T[i-1][proc]*proc_max/f
            if tmp<=ddl and tmp2<=p_energy:
                proc_freq[i-1]=f
                p_energy=tmp2
                EFT[i-1][1]=tmp
                pscheduling[proc]= tmp
                break
        if(p_energy==math.inf):
            proc_freq[i-1]=proc_max
            p_energy=(processorinfo[proc][0]+processorinfo[proc][1]*pow(proc_max,processorinfo[proc][2]))*T[i-1][proc]
            pscheduling[proc]= EFT[i-1][1]
    
        EA = EA+p_energy
        x,sl = HEFT(EST,EFT,idx+1,pscheduling.copy(),qlist,T,c_t,E,n,p,frequency,processorinfo,c_p,ccr)
    return EA, EFT[qlist[-1]-1][1]

def DUPRS2(EST, EFT, pscheduling, qlist, T, c_t, E, n, p,frequency,processorinfo,proc_freq, c_p,ccr):
    EA=0
    for idx, i  in reversed(list(enumerate(qlist))):
        if idx == len(qlist)-1:
            continue
        ddl2 = math.inf
        for j in range(n):
            if E[j][i-1]==1:
                ddl2=min(ddl2,EST[j][1]-c_t[i-1][j]*c_p[EST[j][0]][EST[i-1][0]]*ccr)
                
        proc = EST[i-1][0]
        start = EST[i-1][1]
        ESTcopy = EST.copy()
        ESTcopy=sorted(ESTcopy,key=lambda x: (x[0],x[1]))
        for k in ESTcopy:
            if k[0]==proc and k[1]>start:
                ddl2=min(ddl2,k[1])
                break
        p_energy = math.inf
        if EFT[i-1][1]<=ddl2:  
            proc_min = frequency[proc][0]
            proc_max = frequency[proc][1]
            stp = (proc_max-proc_min)/100
            rng = np.arange(proc_min, proc_max, stp)
            for f in rng:
                tmp = EST[i-1][1]+T[i-1][proc]*proc_max/f
                tmp2 = (processorinfo[proc][0]+processorinfo[proc][1]*pow(f,processorinfo[proc][2]))*T[i-1][proc]*proc_max/f
                if tmp <=ddl2 and tmp2<p_energy:
                    proc_freq[i-1]=f
                    p_energy=tmp2
                    EFT[i-1][1]=tmp
                    pscheduling[proc]= tmp
                    break
            #EST[i-1][1]=EFT[i-1][1]-T[i-1][proc]*proc_max/proc_freq[i-1]
        if(p_energy==math.inf):
            EA = EA + (processorinfo[proc][0]+processorinfo[proc][1]*pow(proc_freq[i-1],processorinfo[proc][2]))*(T[i-1][proc])*proc_max/proc_freq[i-1]
        else:
            EA = EA+p_energy
    return EA, EFT[qlist[-1]-1][1]


if __name__ == "__main__":
    time1 = datetime.now()
    if len(sys.argv) != 10:
        print("Usage: python scheduling.py <qlist> <T> <c_t> <Edges> <latency> <frequency> <processorinfo> <c_p> <ccr>")
        sys.exit(1) 

    qlist = ast.literal_eval(sys.argv[1])
    T = ast.literal_eval(sys.argv[2])
    c_t = ast.literal_eval(sys.argv[3])
    E = ast.literal_eval(sys.argv[4])
    latency = ast.literal_eval(sys.argv[5])
    frequency = ast.literal_eval(sys.argv[6])
    #Energy = ast.literal_eval(sys.argv[7])
    processorinfo = ast.literal_eval(sys.argv[7])
    c_p = ast.literal_eval(sys.argv[8])
    ccr = ast.literal_eval(sys.argv[9])
    n = len(qlist)
    p = len(T[0])
    EFT = [[None]*2 for _ in range(n)]
    EST = [[None]*2 for _ in range(n)]
    pscheduling = [0]*p
    
    EA,sl = HEFT(EST,EFT,0,pscheduling,qlist,T,c_t,E,n,p,frequency,processorinfo,c_p,ccr)
    print("Phase1: ")
    print("Energy consumption is: ",EA)
    print("scheduling length is: ",sl)
    #print("EST is: ",EST)
    #print("EFT is: ",EFT)
    
    proc_freq = [0]*n
    pscheduling = [0]*p

    EA, sl = DUPRS1(EST,EFT,0,pscheduling,qlist,T,c_t,E,n,p,latency,frequency,processorinfo,proc_freq,sl, c_p,ccr)
    print("Phase2: ")
    print("Energy consumption is: ",EA)
    print("scheduling length is: ",sl)
    #print("EST is: ",EST)
    #print("EFT is: ",EFT)

    EA, sl = DUPRS2(EST,EFT,pscheduling,qlist,T,c_t,E,n,p,frequency,processorinfo,proc_freq,c_p,ccr)
    print("Phase3: ")
    print("Energy consumption is: ",EA)
    print("scheduling length is: ",sl)
    #print("EST is: ",EST)
    #print("EFT is: ",EFT)
    





    


    

            

