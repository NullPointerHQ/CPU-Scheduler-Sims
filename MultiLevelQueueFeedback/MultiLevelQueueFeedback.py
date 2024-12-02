import queue #Imports the Queue library
# = = = = = = = = = = = = = = = = = = = = = #
#                                           #
#                 FUNCTIONS                 #
#                                           #
# = = = = = = = = = = = = = = = = = = = = = #

# Display I/O Function - Exists solely for debugging
def display_input_output (list):
    print("Processes in Input/Output List:")
    print("Process | Current Burst")
    print("-----------------------")
    if (len(io) != 0):#Checks that I/O is not empty before attempting access
        i = 0
        while i < len(io):#Runs as long as i is less than the length of IO
            currentProcess = io[i]#Grabs the process key
            traceGrabber = traces[currentProcess]#Grabs the Process's trace
            burstGrabber = traceGrabber[0]#Grabs the current burst
            print(f"{currentProcess} | {burstGrabber}",end=" ") #Displays the process key at the index
            i += 1 # Moves on
        print("\n")
    return

# Display CPU Function - Exists solely for debugging
def display_cpu (queue, queue2, queue3):
    if not (queue.empty() and queue2.empty() and queue3.empty()):
        print("Process | Current Burst....")
        print("-----------------------")
        if not queue.empty():
            print("Processes in High Priority Ready Queue:")
            print("------------------------------------------")
            i = 0
            limiter = queue.qsize()
            while i < limiter: # Runs as long as i is less than the size of the queue
                slot = queue.get() # Grabs the Process Key
                slotTrace = traces[slot] #Grabs process trace
                slotBurst = slotTrace[0] #Grabs process burst
                print(f"{slot} | {slotBurst}", end= " ") #Displays the process key and current burst
                queue.put(slot) #Puts the key back into the slot
                i += 1
            print("\n")

        if not queue2.empty():
            print("------------------------------------------")
            print("Processes in Medium Priority Ready Queue:")
            print("------------------------------------------")
            i = 0
            limiter = queue2.qsize()
            while i < limiter: # Runs as long as i is less than the size of the queue
                slot = queue2.get() # Grabs the Process Key
                slotTrace = traces[slot] #Grabs process trace
                slotBurst = slotTrace[0] #Grabs process burst
                print(f"{slot} | {slotBurst}", end= " || ") #Displays the process key and current burst
                queue2.put(slot) #Puts the key back into the slot
                i += 1
            print("\n")
        if not queue3.empty():
            print("--------------------------------------")
            print("Processes in Low Priority Ready Queue:")
            print("--------------------------------------")
            i = 0
            limiter = queue3.qsize()
            while i < limiter: # Runs as long as i is less than the size of the queue
                slot = queue3.get() # Grabs the Process Key
                slotTrace = traces[slot] #Grabs process trace
                slotBurst = slotTrace[0] #Grabs process burst
                print(f"{slot} | {slotBurst}", end= " ") #Displays the process key and current burst
                queue3.put(slot) #Puts the key back into the slot
                i += 1
            print("\n")
    else:
        print("CPU is Empty")

#Scheduler, finds the next process
def mlfq_scheduler (queue,queue2, queue3, runningProcess,runningProcesstrace, toggle, priorityTracker):
    
    #Checks if first queue is empty
    if queue.empty() != True:#Runs if High Priority Queue is not empty
        #print("High Priority Queue is not empty")# - Debugging
        runningProcess = queue.get()#Grabs the first process and dequeues it
        runningProcesstrace = traces[runningProcess]#Grabs the Trace of the process
        toggle = 'F' #Marks the CPU as FULL
        priorityTracker = 'H'#Last queue was the High priority
        #print(f"Grabbed:{runningProcess}, has trace: {runningProcesstrace[0]}, Queue Empty? {hiPriority.empty()}") # - Debugging
        
    elif queue2.empty() != True:#Runs if Med Priority Queue is not empty
        #print(f"Medium Priority Queue is not empty ({not medPriority.empty()})")# - Debugging
        runningProcess = queue2.get()#Grabs the first process and dequeues it
        runningProcesstrace = traces[runningProcess]#Grabs the Trace of the process
        toggle = 'F' #Marks the CPU as FULL
        priorityTracker = 'M'#Last queue was the Med priority
        #print(f"Grabbed:{runningProcess}, has trace: {runningProcesstrace[0]}, Queue Empty? {medPriority.empty()}") # - Debugging
        
    elif queue3.empty() != True:#Runs if Low Priority Queue is not empty
        #print("Low Priority Queue is not empty")# - Debugging
        runningProcess = queue3.get()#Grabs the first process and dequeues it
        runningProcesstrace = traces[runningProcess]#Grabs the Trace of the process
        toggle = 'F' #Marks the CPU as FULL
        priorityTracker = 'L'#Last queue was the Low priority
        #print(f"Grabbed:{runningProcess}, has trace: {runningProcesstrace[0]}, Queue Empty? {lowPriority.empty()}")# - Debugging
        
    else:#All Queues are empty
        #print("All Queues are Empty!") # - Debugging Statement# - Debugging
        priorityTracker = '-'#Last queue was NULL
    return runningProcess, runningProcesstrace, toggle, priorityTracker #Returns everything modifying variables in main

# I/O Handler, handles all operations involving processes in the IO list if any, also sends processes to the CPU if they are done
def input_output_handler (queue, iolist, newestProcess):
    #print("I/O is not empty, Handling.") # - Debugging
    i = 0 # Index

    #Tracking the Processes in the 'IO' state and adjusting their burst time to account for the passage of time
    while i < len(iolist):# Runs through each element in IO once
        if iolist[i] == newestProcess:
            if i + 1 < len(iolist):#Grabbing the next process in the line if there is one
                i += 1
            else:
                return iolist 
        currentProcess = iolist[i] # Grabs the current Process
        currentTrace = traces[currentProcess] # Grabs the trace of the process
        
        if len(currentTrace) != 0 and currentTrace[0] != 0:
            #print(f"Currently working on -> {currentProcess} with burst {currentTrace}", end=" ") # Debugging      
        
            currentTrace[0] -= 1 # Subtracts one from the burst
            #print(f"Remaining I/O Burst: {currentTrace[0]}") # Debugging

            #OUTCOME A: I/O Burst Over, Sending back to CPU, Automatically moves to next process
            if currentTrace[0] == 0: 
                #print(f"I/O Burst for: {currentProcess} is {currentTrace[0]}. Sending back to CPU") # Debugging
                del currentTrace[0] # Deletes the burst time from the list (It would be zero at this point)
                queue.put(io[i]) # Enqueues the Process Key back to the CPU
                del iolist[i] # Removes the Process Key from the IO list
                #display_cpu(cpu) # - Debugging
            else:
                i += 1 # Moves to the next process
        
        elif len(currentTrace) == 0: #This should not occur, we do not end on IO
            print(f"{currentProcess}has ended on I/O. This should not happen!") # Error Message
            exit() # Immediately Terminates the program
        
    
    return iolist

# CPU Handler, Handles all operations involving processes in the CPU
def cpu_handler(toggle, runningProcess, runningProcesstrace, queue, io, timeQuantum,i): 
    #Outcome A: CPU Burst is not over
    if (runningProcesstrace[0] != 0):
        #Outcome A.1 There is still time for the burst in the current queue
        if (i < timeQuantum or timeQuantum == -1):
            #print(f"CPU HANDLER: PROCESS {runningProcess} RECEIVED WITH {runningProcesstrace[0]} BURST REMAINING. WILL DECREASE TO {runningProcesstrace[0] - 1}")
            runningProcesstrace[0] -= 1#Subtracts 1 from the burst

        #Outcome A.2 No more time is available to the burst, sent to next queue, flags for next operation
        else:
            #print(f"Sending {runningProcess} with remaining Burst: {runningProcesstrace[0]} to next Queue")# - Debugging
            queue.put(runningProcess)#Pushes process to next queue
            #print("Sent.")# - Debugging
            toggle = 'E'#Marks CPU as empty
    #Outcome B: CPU Burst is Over, Sending to I/O or Termininating
    if (runningProcesstrace[0] == 0):
        del runningProcesstrace[0]#Removes Null burst
        if (len(runningProcesstrace) != 0):#Outcome A.1 Trace is not over, sent to I/O
            #print("Sending to I/O")
            io.append(runningProcess)#Adds the process to the I/O list
            toggle = 'E'#Marks the CPU as ready for more
            #print(f"{runningProcess} sent to I/O")
        else:#Outcome A.2 Trace is over
            toggle = 'C'
            #print(f"{runningProcess} is done")
    return toggle

#I do not know why but every so often there will be an 'off by one' discrepancy with the time.
#I dont know why but this will step and mathematically adjust time as needed
#It will not say anything
def time_lord(time,doioFlag, burstTime,priorityTracker, beforeTime, afterTime, queue, queue2, queue3):
    #Runs every so often, finds the difference between the actual time and the previous time
    #compares the result to the burst time, they should be equal if its not the function will rectify that
    #print(f"Time Received: {time}") # - Debugging
    splitTime = afterTime - beforeTime
    #print(f"After Time:{afterTime} | Before Time: {beforeTime}") # - Debugging
    if splitTime != burstTime:
        #print(f"TIME DIFFERENCE - BEFORE:{beforeTime} time units | AFTER: {afterTime} time units") # - Debugging
        #print(f"SPLIT TIME: {splitTime} time units | BURST TIME {burstTime} time units") # - Debugging
        #print(f"split - burst: {splitTime - burstTime}")
        time = time - (splitTime - burstTime)
        #print(f"ADJUSTED TIME: {time}") # - Debugging
        doioFlag = False #Signals to not do I/O for one iteration
        
        #TO DO: FIX THE WAIT TIMES
        #Checking if any wait times need to be fixed
        if not queue.empty():#High Priority Queue
            #print("High Priority Queue is not empty adjusting their wait times")
            i, limiter = 0, queue.qsize()
            while i < limiter:
                processKey = queue.get()#Grabs the front element and dequeues it
                #print(f"BEFORE ADJUSTING: {processKey} | {processInfo[processKey][1]}") # - Debugging
                processInfo[processKey][1] = processInfo[processKey][1] - (splitTime - burstTime)
                #print(f"AFTER ADJUSTING: {processKey} | {processInfo[processKey][1]}") # - Debugging
                queue.put(processKey)
                i += 1

        if not queue2.empty():#Medium Priority Queue
            #print("Medium Priority Queue is not empty adjusting their wait times")
            i, limiter = 0, queue2.qsize()
            while i < limiter:
                processKey = queue2.get()#Grabs the front element and dequeues it
                #print(f"BEFORE ADJUSTING: {processKey} | {processInfo[processKey][1]}") # - Debugging
                processInfo[processKey][1] = processInfo[processKey][1] - (splitTime - burstTime)
                #print(f"AFTER ADJUSTING: {processKey} | {processInfo[processKey][1]}") # - Debugging
                queue2.put(processKey)
                i += 1
        
        if not queue3.empty():#Low Priority Queue
            #print("Low Priority Queue is not empty adjusting their wait times")
            i, limiter = 0, queue3.qsize()
            while i < limiter:
                processKey = queue3.get()#Grabs the front element and dequeues it
                #print(f"BEFORE ADJUSTING: {processKey} | {processInfo[processKey][1]}") # - Debugging
                processInfo[processKey][1] = processInfo[processKey][1] - (splitTime - burstTime)
                #print(f"AFTER ADJUSTING: {processKey} | {processInfo[processKey][1]}") # - Debugging
                queue3.put(processKey)
                i += 1
    return time, doioFlag

#Handles tracking process times (TW, TR,TTR), Triggers after a CPU burst finishes
def process_tracker(time, toggle, queue, queue2, queue3, currentProcess):
    currentProcessinfo = processInfo[currentProcess]
    
    #Check if Process has been seen before (TR)
    if currentProcessinfo[0] == -1:
        currentProcessinfo[0] = time #Sets the Response time to current Time
        return
       
    #Checks if the Process is Done (TTR)
    if toggle == 'C':
        currentProcessinfo[2] = time + 1 #Sets the turnaround time to current Time
        return
        
    
    #If the Ready Queues are not empty (TW)
    if not queue.empty():
        i = 0
        limiter = queue.qsize()#Ensures we dont repeat elements
        while i < limiter:
            tempSlot = queue.get()#Grabs the the first element
            tempSlotInfoList = processInfo[tempSlot] #Grabs the info list of the process
            tempSlotInfoList[1] += 1 #Adds 1 to the time
            queue.put(tempSlot) #Returns the Process back to the CPU
            i += 1
    
    if not queue2.empty():
        i = 0
        limiter = queue2.qsize()#Ensures we dont repeat elements
        while i < limiter:
            tempSlot = queue2.get()#Grabs the the first element
            tempSlotInfoList = processInfo[tempSlot] #Grabs the info list of the process
            tempSlotInfoList[1] += 1 #Adds 1 to the time
            queue2.put(tempSlot) #Returns the Process back to the CPU
            i += 1
    
    if not queue3.empty():
        i = 0
        limiter = queue3.qsize()#Ensures we dont repeat elements
        while i < limiter:
            tempSlot = queue3.get()#Grabs the the first element
            tempSlotInfoList = processInfo[tempSlot] #Grabs the info list of the process
            tempSlotInfoList[1] += 1 #Adds 1 to the time
            queue3.put(tempSlot) #Returns the Process back to the CPU
            i += 1
            
    return

#Will generate a report for each context switch
def context_switch_report(time,currentProcess, currentProcesstrace,queue,queue2,queue3,io,priorityTracker):
    print("\n\n")
    print("=================================================================================================")
    print("\t\tCONTEXT SWITCH REPORT")
    print("=================================================================================================")
    print(f"Current Execution Time - {time} in Time Units")
    print(f"Currently Running Process: {currentProcess} with {currentProcesstrace[0]} time left on its CPU burst")
    print(f"{currentProcess} came from Queue: {priorityTracker}")
    print("--------------------------------------------------------------------------------------------------")
    display_cpu(queue,queue2,queue3)
    display_input_output(io)
    print("=================================================================================================")
    return

#Will generate a final report with all the requested information. Only executes Once
def grand_finale (time,queue,queue2,queue3,io, cpuIdle):
    print("\n\n")
    print("======================================================================")
    print("FINAL REPORT FOR MULTILEVEL FEEDBACK QUEUE SCHEDULER")
    print("======================================================================")
    print(f"Final Time -  {time} Time Units")
    print(f"CPU Utilization - {(((time - cpuIdle) / time) * 100):.2f}%")#Calculates & Displays CPU Utilization.
    print("----------------------------------------------------------------------")
    print("Process | Time Reponse | Time Waiting | Time Turnaround")
    sumWait = 0
    sumResponse = 0
    sumTurnaround = 0
    for key in processInfo:#iterates over each key once
        keyList = processInfo[key]#Grabs the List with the Values
        #Adding Up the TR,TW,TTR
        sumResponse += keyList[0]
        sumWait += keyList[1]
        sumTurnaround += keyList[2]
        print(f"{key} | {keyList[0]} | {keyList[1]} | {keyList[2]}")#Displaying Values
    print("----------------------------------------------------------------------")
    print(f"Average Response Time: {sumResponse/8:.2f} | Average Wait Time:{sumWait/8:.2f}")
    print(f"Average Turnaround Time: {sumTurnaround/8:.2f}")
    print("Have a Great Day!")

# = = = = = = = = = = = = = = = = = = = = = #
#                                           #
#               MAIN FUNCTION               #
#                                           #
# = = = = = = = = = = = = = = = = = = = = = #
# Dictionaries: Used to store and catalogue information for each process
#traces - Associates the each Process with it's trace
#processInfo - Used to track and store Response, Wait and Turnaround times

#Traces start and end with CPU Burst
traces = {
    "P1" : [5, 27, 3, 31, 5, 43, 4, 18, 6, 22, 4, 26, 3, 24, 4],
    "P2" : [4, 48, 5, 44, 7, 42, 12, 37, 9, 76, 4, 41, 9, 31, 7, 43, 8],
    "P3" : [8, 33, 12, 41, 18, 65, 14, 21, 4, 61, 15, 18, 14, 26, 5, 31, 6],
    "P4" : [3, 35, 4, 41, 5, 45, 3, 51, 4, 61, 5, 54, 6, 82, 5, 77, 3],
    "P5" : [16, 24, 17, 21, 5, 36, 16, 26, 7, 31, 13, 28, 11, 21, 6, 13, 3, 11, 4],
    "P6" : [11, 22, 4, 8, 5, 10, 6, 12, 7, 14, 9, 18, 12, 24, 15, 30, 8],
    "P7" : [14, 46, 17, 41, 11, 42, 15, 21, 4, 32, 7, 19, 16, 33, 10],
    "P8" : [4, 14, 5, 33, 6, 51, 14, 73, 16, 87, 6]}

#Reponse Times all start at -1. Negative time is impossible so this will 
#Indicate when a Process has not been seen yet
processInfo = {
    "P1" : [-1, 0, 0],
    "P2" : [-1, 0, 0],
    "P3" : [-1, 0, 0],
    "P4" : [-1, 0, 0],
    "P5" : [-1, 0, 0],
    "P6" : [-1, 0, 0],
    "P7" : [-1, 0, 0],
    "P8" : [-1, 0, 0]}

#Input/Output List
io = [] 

#Multilevel Feeedback Queues
hiPriority = queue.Queue(maxsize = 8) #'cpu' Queue acts as the CPU Ready state
medPriority = queue.Queue(maxsize = 8) #'cpu' Queue acts as the CPU Ready state
lowPriority = queue.Queue(maxsize = 8) #'cpu' Queue acts as the CPU Ready state

#Variables, mostly trackers
time = 0 #Used as a clock, All processes arrived at time = 0
runningProcess = '-' #Holds the key of the process in the running state
runningProcesstrace = [] #Holds the Trace of the process in the running state
priorityTracker = '-' #H for High, M for Med and L for low, tracks the previous queue
toggle = 'E' #Used to track if the CPU is busy
cpuIdle = 0 #Used to track CPU idle time
i = 0#Tracks time per process

timeBefore = 0#Tracks Time before the new burst
originalBurst = 0#Tracks the original burst length
timeAfter = 0 #Tracks time after the burst
doioFlag = True#Prevents IO function from operating under certain cirucumstances

#Pushing all processes to the Ready state
#All Processes start in the HIGHEST priority
for key in traces.keys():
    hiPriority.put(key)


while not (hiPriority.empty() and medPriority.empty() and lowPriority.empty() and len(io) == 0 and toggle == 'E'):
    #print("Program is running:") # - Debugging
    #print(f"Toggle:{toggle}") # - Debugging 
#CPU SECTION
    #There is no Running Process:
    #OUTCOME A: Check if there is an available Queue and the toggle flag is empty
    if toggle == 'E' and (hiPriority.empty() != True or medPriority.empty() != True or lowPriority.empty() != True):
        #Call the scheduler function
        runningProcess,runningProcesstrace, toggle, priorityTracker = mlfq_scheduler (hiPriority,medPriority, lowPriority, runningProcess,runningProcesstrace, toggle, priorityTracker)
        #Call the tracker to track response times
        process_tracker(time, toggle, hiPriority,medPriority, lowPriority, runningProcess)
        #Call the Context Switch Reporter
        context_switch_report(time,runningProcess, runningProcesstrace,hiPriority,medPriority, lowPriority,io,priorityTracker)
        if i != 0: i = 0#Resets 'i'

        originalBurst = runningProcesstrace[0]#Grabs the unaltered Burst time.
        timeBefore = time#Grabbing the current time
        
        #If the burst is bigger than the tq of the queue the process is in 
        #this will set the original to the max for the queue that the process is in
        if originalBurst > 5 and priorityTracker == 'H': originalBurst = 5
        elif originalBurst > 10 and priorityTracker == 'M':originalBurst = 10

    #OUTCOME B: There is no Running Process and Queues are empty:
    elif toggle == 'E' and (hiPriority.empty() == True and medPriority.empty() == True and lowPriority.empty() == True):
        cpuIdle += 1 #Increase the Idle time by 1
    
    #There is a process currently running: 
    if toggle == 'F':
        #print(f"Calling CPU Handler with i:{i}")# - Debugging
        #Outcome A: Process has Burst time left
        if priorityTracker == 'H':
            toggle = cpu_handler(toggle, runningProcess, runningProcesstrace,medPriority, io, 5,i)
            i += 1
        elif priorityTracker == 'M':
            toggle = cpu_handler(toggle, runningProcess, runningProcesstrace,lowPriority, io, 10,i)
            i += 1
        elif priorityTracker == 'L':
            toggle = cpu_handler(toggle, runningProcess, runningProcesstrace,lowPriority, io, -1,i)
            i += 1
        else:#Error Catcher
            print("What do you mean the toggle is full but there is no priority queue?")#This shouldnt happen
            exit()

        if toggle == 'E' or toggle == 'C':
            #Checking if the current time is off and adjusting if needed.
            #print(f"Calling Time Adjustor")#-Debugging
            #print(f"Time: {time}")#-Debugging
            timeAfter = time + 1#Grabs the current time
            time, doioFlag = time_lord(time,doioFlag, originalBurst, priorityTracker, timeBefore, timeAfter, hiPriority,medPriority, lowPriority)
            #print(f"Time: {time}")#-Debugging
            originalBurst, timeAfter,timeBefore = 0,0,0 #Resetting all the times so that it doesnt affect CPU IDLE times

        if toggle == 'C':
            print(f"At time {time + 1}, Process {runningProcess} concluded") 
            process_tracker(time, toggle, hiPriority,medPriority, lowPriority, runningProcess)#Calling to track turnaround time
            toggle = 'E'
        if toggle == 'E': 
            newestProcess = runningProcess #Grabs the last running process and protects it.

        #print(f"Toggle Status:{toggle} at time {time} with i {i}")
        process_tracker(time, toggle, hiPriority,medPriority, lowPriority, runningProcess)#TW does not stop unless there are no processes in CPU     
        
#EVERYTHING ELSE
    #Handles Input/Output if Needed
    if len(io) != 0 and doioFlag == True:
        #print("I/O is not empty") # - Debugging
        input_output_handler(hiPriority, io,newestProcess)#Calls the I/O Function to handle I/O
        newestProcess = '-'#Resets the protection filter

    elif doioFlag == False:#Resetting the IO Flag if Needed
        doioFlag = True
    
    time += 1#Moves the Clock forward   
    
     
    
    #-Debugging, Time never goes above 1000. Remove if processes necessitate it
    if time > 700:
        print("TIME ERROR")
        display_cpu(hiPriority, medPriority, lowPriority)
        display_input_output(io)
        #print(newestProcess)
        exit() # Immediately Terminates the program

grand_finale (time,hiPriority,medPriority,lowPriority,io, cpuIdle)#Calls for the final report