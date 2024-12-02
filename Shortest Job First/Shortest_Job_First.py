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
            print(f"{currentProcess} | {burstGrabber}") #Displays the process key at the index
            i += 1 # Moves on
    return

# Display CPU Function - Exists solely for debugging
def display_cpu (cpu):
    print("Processes in CPU:")
    print("Process | Current Burst")
    print("-----------------------")
    if len(cpu) != 0:#Checks that we are not accessing an empty list
        i = 0
        limiter = len(cpu)
        while i < limiter: # Runs as long as i is less than the size of the queue
            slot = cpu[i] # Grabs the Process Key
            slotTrace = traces[slot] #Grabs process trace
            slotBurst = slotTrace[0] #Grabs process burst
            print(f"{slot} | {slotBurst}") #Displays the process key and current burst
            i += 1

# I/O Handler, handles all operations involving processes in the IO list if any, also sends processes to the CPU if they are done
def input_output_handler (cpu, io, sort, newestProcess):
    #print("I/O is not empty, Handling.") # - Debugging
    i = 0 # Index

    #Tracking the Processes in the 'IO' state and adjusting their burst time to account for the passage of time
    while i < len(io):# Runs through each element in IO once  
        #Ensuring that the process selected hasnt JUST arrived
        if io[i] == newestProcess:
            if i + 1 < len(io):#Grabbing the next process in the line if there is one
                i += 1
            else:
                return cpu, io, sort
        currentProcess = io[i] # Grabs the current Process
        currentTrace = traces[currentProcess] # Grabs the trace of the process
                
        if len(currentTrace) != 0 and currentTrace[0] != 0:
            #print(f"Currently working on -> {currentProcess} with burst {currentTrace}", end=" ") # Debugging      
        
            currentTrace[0] -= 1 # Subtracts one from the burst
            #print(f"Remaining I/O Burst: {currentTrace[0]}") # Debugging

            #OUTCOME A: I/O Burst Over, Sending back to CPU, Automatically moves to next process
            if currentTrace[0] == 0: 
                #print(f"I/O Burst for: {currentProcess} is {currentTrace[0]}. Sending back to CPU") # Debugging
                del currentTrace[0] # Deletes the burst time from the list (It would be zero at this point)
                cpu.append(io[i]) # Enqueues the Process Key back to the CPU
                del io[i] # Removes the Process Key from the IO list
                sort = 'Y'#Calls for a sort
                #print(f"Needs Sorting\nCPU:{cpu}\nI/O:{io}")# - Debugging
                #display_cpu(cpu) # - Debugging
            else:
                i += 1 # Moves to the next process
        
        elif len(currentTrace) == 0: #This should not occur, we do not end on IO
            print(f"{currentProcess}has ended on I/O. This should not happen!") # Error Message
            exit() # Immediately Terminates the program
        
    
    return cpu, io, sort

# CPU Handler, handles all operations done by the CPU, subtracts one from the burst if applicable or nullifies the parameters if not
def cpu_handler (runningState, runningProcesstrace, io,toggle):
    #print(f"Current Process: {currentProcess}") # - Debugging
    #print(f"Remaining Burst Time: {currentProcesstrace[0]}") # - Debugging

    #If the CPU burst is not over, subtract from the burst
    if runningProcesstrace[0] != 0:
        runningProcesstrace[0] -= 1
    #OUTCOME A: CPU BURST ENDED, SIGNAL TO MOVE ON IF POSSIBLE
    if runningProcesstrace[0] == 0:
        #OUTCOME A.1: CPU BURST ENDED AND TRACE IS OVER
        if len(runningProcesstrace) == 1:
            #print(f"{currentProcess} has concluded.")
            toggle = 'C'
            return toggle # WILL SIGNAL TO MOVE ON TO THE NEXT PROCESS IN QUEUE. PROCESS IS LOST TO TIME 
        #OUTCOME A.2 BURST ENDED AND IO BURST IS NEXT
        else:
            #print(f"{currentProcess} has been sent to I/O with Burst remaining: {currentProcesstrace[0]}") # - Debugging
            del runningProcesstrace[0] # Removes the burst from the list
            io.append(runningState) # WILL SEND THE PROCESS TO I/O. IT IS NOT BACK IN CPU
            toggle = 'E'
            return toggle
    # OUTCOME B: BURST IS NOT OVER, RETURN TOGGLE
    else:
        return toggle

# Will sort the CPU from shortest to longest
def sjf_scheduler (cpu):
    #print("Made it here!") # - Debugging
    cpuUnsorted = cpu.copy() # Holds a copy of cpu
    cpu = [] #Wipes cpu to prepare for sorting
    i, limit = 0, len(cpuUnsorted)

    #Ensures that there is more than one Process in the Ready state
    if limit > 1:
        while i < limit:#Iterates over each element
            shortestProcess = cpuUnsorted[0] #Grabs the first element in the list (Process Key)
            shortestProcesstrace = traces[shortestProcess]#Grabs the process trace
            originalPosition = 0 #Holds the original position of the process
            #print(f"Checking: {shortestProcess} with Index:{originalPosition} | Unsorted List: {cpuUnsorted}")
            j = 0
            while j < len(cpuUnsorted):#Iterates through the remaining processes
                #Outcome A: If there is a shorter job then that becomes the shortest job.
                if traces[cpuUnsorted[j]][0] < shortestProcesstrace[0]:
                    #Grabbing the new shortest process and its position
                    shortestProcess = cpuUnsorted[j]#Storing New Shortest Process
                    shortestProcesstrace = traces[shortestProcess]#Grabbing the trace list
                    originalPosition = j#Grabbing the index
                    #print(f"Grabbed: {shortestProcess} with Burst: {shortestProcesstrace[0]} CPU List now: {cpuUnsorted}")#- Debugging
                j += 1#Moving to the next index
            
            #Outcome B: There was no shorter job, send the process over to the CPU
            #print(f"Sent to CPU: {shortestProcess}")# - Debugging
            cpu.append(shortestProcess)
            
            #Deleting from the list:
            del cpuUnsorted[originalPosition]
            #print(f"Deleted Index {originalPosition}, List now: {cpuUnsorted}")#- Debugging
            i += 1 #Increased to make sure we don't iterate over the same element more than once
    elif limit == 1:#Applies if there is exactly ONE process in CPU
        cpu = cpuUnsorted.copy()

    del cpuUnsorted
    #print(f"CPU List: {cpu}") # - Debugging
    return cpu

#Handles tracking process times (TW, TR,TTR), Triggers after a CPU burst finishes
def process_tracker(time, toggle, cpu, runningState):
    currentProcessinfo = processInfo[runningState]
    
    #Check if Process has been seen before (TR)
    if currentProcessinfo[0] == -1:
        currentProcessinfo[0] = time #Sets the Response time to current Time
       
    #Checks if the Process is Done (TTR)
    if toggle == 'C':
        currentProcessinfo[2] = time + 1 #Sets the turnaround time to current Time
        return
        
    
    #If the CPU is not empty (TW)
    if len(cpu) != 0:
        i = 0
        limiter = len(cpu)#Ensures we dont repeat elements
        while i < limiter:
            tempSlot = cpu[i]#Grabs the the first element
            tempSlotInfoList = processInfo[tempSlot] #Grabs the info list of the process
            tempSlotInfoList[1] += 1 #Adds 1 to the time
            i += 1
            
    return

#Will generate a report for each context switch
def context_switch_report(time,runningState, runningProcesstrace,cpu,io):
    print("\n\n")
    print("======================================================================")
    print("\t\tCONTEXT SWITCH REPORT")
    print("======================================================================")
    print(f"Current Execution Time - {time} in Time Units")
    print(f"Currently Running Process: {runningState}")
    print(f"which has {runningProcesstrace[0]} time left on its CPU burst")
    #print(f"Remaining Trace:{runningProcesstrace}") # - Debugging
    print("----------------------------------------------------------------------")
    display_cpu(cpu)
    display_input_output(io)
    print("======================================================================")
    return

#Will generate a final report with all the requested information. Only executes Once
def grand_finale (time,currentProcess, currentProcesstrace,cpu,io, cpuUtil):
    print("\n\n")
    print("======================================================================")
    print("FINAL REPORT FOR SHORTEST JOB FIRST SCHEDULER")
    print("======================================================================")
    print(f"Final Time -  {time} Time Units")
    print(f"CPU Utilization - {(((time - cpuUtil) / time) * 100):.2f}%")#Calculates & Displays CPU Utilization.
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

#Lists
cpu = [] #'cpu' acts as the CPU Ready state
io  = [] #IO is where input/output occurs

#Pushing all processes to the Ready state, T = 0 so...
for key in traces.keys():
    cpu.append(key)

#VARIABLE DECLARATIONS
time = 0 #Used as a clock, All processes arrived at time = 0
runningState = '-' #Holds the Process Key
runningProcesstrace = [] #Holds the trace of the current process
toggle = 'E' # Used to mark whether CPU is Empty, Full, Concluded
sort = 'Y' #Used to mark whether the CPU List needs sorting
cpuIdle = 0 # Used to calculate CPU Utilization Time

#Handles Scheduling
while not (len(cpu) == 0 and len(io) == 0 and toggle == 'E'):

    #print("Program is Running")# - Debugging   
    
    newestProcess = '-'#Used to keep the program from subtracting burst time from a process that just got to I/O

    #Task A: Sorting the CPU Processes
    if sort == 'Y' and len(cpu) != 0:
        cpu = sjf_scheduler(cpu)# Calls the sorter
        #print(f"CPU List Received: {cpu}")# - Debugging
        sort = 'N'#Sorting is no longer needed

    #Condition A: Last Process Finished/Didnt Exist AND there is something to sort
    if toggle == 'E' and len(cpu) != 0:
        runningState = cpu[0] #Grabs the key of the next process in line
        runningProcesstrace = traces[runningState]#Grabs the trace of the process
        del cpu[0] #Automatically removes the process from the ready state
        toggle = 'F' #Toggle to mark CPU as full
        context_switch_report(time,runningState, runningProcesstrace,cpu,io)

    if toggle != 'E':#Checking if we have a process in the running state
        process_tracker(time, toggle, cpu, runningState)#Calls in the Process Tracker for TW TTR TR
        toggle = cpu_handler (runningState, runningProcesstrace, io,toggle)
        #If the process's Burst Finished this iteration
        if toggle == 'E':
            newestProcess = runningState 
   
    
    if toggle == 'C':#Process is Done
        process_tracker(time, toggle, cpu, runningState)#Calls in the Process Tracker for TW TTR TR
        print(f"At time: {time + 1}. Process {runningState} concluded.")
        toggle = 'E'
        sort = 'Y'
            
    if len(io) != 0:
        cpu, io, sort = input_output_handler(cpu, io, sort, newestProcess)
    
    #Checks if the CPU is Idle
    if len(cpu) == 0 and toggle == 'E' and len(io) != 0:
        cpuIdle += 1
    time += 1 #Time always moves forward
grand_finale (time,runningState, runningProcesstrace,cpu,io, cpuIdle)
#print("Program has concluded") # - Debugging
