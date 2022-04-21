# 只适合windows系统, 用了windows 系统api
import sys,os,time,psutil
import win32api,win32process,win32con
import threading
import ctypes
import multiprocessing as mp

def CPU_Stress_One_Core( cpu_idx, cpu_load):
    pid = win32api.GetCurrentProcessId()
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
    win32process.SetPriorityClass(handle, win32process.REALTIME_PRIORITY_CLASS)

    cpu_mask = 1 << cpu_idx - 1
    print( "to set cpu index %s mask %s load %s "%(cpu_idx, cpu_mask,cpu_load ))
    win32process.SetProcessAffinityMask(win32api.GetCurrentProcess(), cpu_mask)

    # 期望单核负载多少, 实际偏低，调整一下参数
    E = int(cpu_load*1.3)
    while True:
        # 循环里面不要添加任何代码，有些代码隐含io操作，就会导致负载失效
        curTick = win32api.GetTickCount()
        while win32api.GetTickCount() - curTick < E: continue
        ctypes.windll.kernel32.Sleep( max( (100 - E), 1) )

# cpu_load 为负载百分比
def CPU_Stress_All_Core( cpu_load):
    print("Number of CPUs:", mp.cpu_count() )
    processes = []
    for cpu_idx in range(mp.cpu_count()):
        process = mp.Process(target=CPU_Stress_One_Core, args=(cpu_idx + 1, cpu_load ))
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()

if __name__ == '__main__':
    CPU_Stress_All_Core(40)


