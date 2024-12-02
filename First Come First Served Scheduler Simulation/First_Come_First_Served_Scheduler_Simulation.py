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
def display_cpu (queue):
    print("Processes in CPU:")
    print("Process | Current Burst")
    print("-----------------------")
    if not queue.empty():
        i = 0
        limiter = queue.qsize()
        while i < limiter: # Runs as long as i is less than the size of the queue
            slot = queue.get() # Grabs the Process Key
            slotTrace = traces[slot] #Grabs process trace
            slotBurst = slotTrace[0] #Grabs process burst
            print(f"{slot} | {slotBurst}") #Displays the process key and current burst
            queue.put(slot) #Puts the key back into the slot
            i += 1

# I/O Handler, handles all operations involving processes in the IO list if any, also sends processes to the CPU if they are done
def input_output_handler (queue, list, newestProcess):
    #print("I/O is not empty, Handling.") # - Debugging
    i = 0 # Index

    #Tracking the Processes in the 'IO' state and adjusting their burst time to account for the passage of time
    while i < len(io):# Runs through each element in IO once  
        
        #Ensuring that the process selected hasnt JUST arrived
        if io[i] == newestProcess:
            if i + 1 < len(io):#Grabbing the next process in the line if there is one
                i += 1
            else:
                return list 
            
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
                cpu.put(io[i]) # Enqueues the Process Key back to the CPU
                del io[i] # Removes the Process Key from the IO list
                #display_cpu(cpu) # - Debugging
            else:
                i += 1 # Moves to the next process
        
        elif len(currentTrace) == 0: #This should not occur, we do not end on IO
            print(f"{currentProcess}has ended on I/O. This should not happen!") # Error Message
            exit.sys() # Immediately Terminates the program
        
    
    return list

# CPU Handler, handles all operations done by the CPU, subtracts one from the burst if applicable or nullifies the parameters if not
def cpu_handler (currentProcess, currentProcesstrace, io,toggle):
    #print(f"Current Process: {currentProcess}") # - Debugging
    #print(f"Remaining Burst Time: {currentProcesstrace[0]}") # - Debugging
    #If the CPU burst is not over, subtract from the burst
    if currentProcesstrace[0] != 0:
        currentProcesstrace[0] -= 1
    #OUTCOME A: CPU BURST ENDED, SIGNAL TO MOVE ON IF POSSIBLE
    if currentProcesstrace[0] == 0:
        #OUTCOME A.1: CPU BURST ENDED AND TRACE IS OVER
        if len(currentProcesstrace) == 1:
            #print(f"{currentProcess} has concluded.")
            toggle = 'C'
            return toggle # WILL SIGNAL TO MOVE ON TO THE NEXT PROCESS IN QUEUE. PROCESS IS LOST TO TIME 
        #OUTCOME A.2 BURST ENDED AND IO BURST IS NEXT
        else:
            #print(f"{currentProcess} has been sent to I/O with Burst remaining: {currentProcesstrace[0]}") # - Debugging
            del currentProcesstrace[0] # Removes the burst from the list
            io.append(currentProcess) # WILL SEND THE PROCESS TO I/O. IT IS NOT BACK IN CPU
            toggle = 'E'
            return toggle
    # OUTCOME B: BURST IS NOT OVER, RETURN PROCESS KEY
    else:
        return currentProcess,toggle

#Handles tracking process times (TW, TR,TTR), Triggers after a CPU burst finishes
def process_tracker(time, toggle, cpu, currentProcess):
    currentProcessinfo = processInfo[currentProcess]
    
    #Check if Process has been seen before (TR)
    if currentProcessinfo[0] == -1:
        currentProcessinfo[0] = time #Sets the Response time to current Time
       
    #Checks if the Process is Done (TTR)
    if toggle == 'C':
        currentProcessinfo[2] = time + 1 #Sets the turnaround time to current Time
        return
    
    #If the CPU is not empty (TW)
    if not cpu.empty():
        i = 0
        limiter = cpu.qsize()#Ensures we dont repeat elements
        while i < limiter:
            tempSlot = cpu.get()#Grabs the the first element
            tempSlotInfoList = processInfo[tempSlot] #Grabs the info list of the process
            tempSlotInfoList[1] += 1 #Adds 1 to the time
            cpu.put(tempSlot) #Returns the Process back to the CPU
            i += 1
    
    # - Debugging
    #print("Process Tracker Debugger")
    #for key in processInfo:
        #print(f"{key} | {processInfo[key][1]}")
            
    return
#Will generate a report for each context switch
def context_switch_report(time,currentProcess, currentProcesstrace,cpu,io):
    print("\n\n")
    print("======================================================================")
    print("\t\tCONTEXT SWITCH REPORT")
    print("======================================================================")
    print(f"Current Execution Time - {time} in Time Units")
    print(f"Currently Running Process: {currentProcess}")
    print(f"which has {currentProcesstrace[0]} time left on its CPU burst")
    print("----------------------------------------------------------------------")
    display_cpu(cpu)
    display_input_output(io)
    print("======================================================================")
    return

#Will generate a final report with all the requested information. Only executes Once
def grand_finale (time,currentProcess, currentProcesstrace,cpu,io, cpuUtil):
    print("\n\n")
    print("======================================================================")
    print("FINAL REPORT FOR FIRST COME FIRST SERVE SCHEDULER")
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


cpu = queue.Queue(maxsize = 8) #'cpu' Queue acts as the CPU Ready state
io = [] #IO is where input/output occurs

#Pushing all processes to the Ready state, T = 0 so...
for key in traces.keys():
    cpu.put(key)

time = 0 #Used as a clock, All processes arrived at time = 0
runningState = '-' #Holds the Process Key
currentProcesstrace = [] #Holds the trace of the current process
toggle = 'E' # Used to mark whether CPU is Empty, Full, Concluded
cpuUtil = 0 # Used to calculate CPU Utilization Time
#Handles Scheduling
while not (cpu.empty() and len(io) == 0 and toggle == 'E'):
    
    newestProcess = '-'#Used to keep the program from subtracting burst time from a process that just got to I/O

    #print("Program is Running")# - Debugging   
    
    #Updating the current CPU process
    #Checking if the CPU queue is NOT empty and Previous Process has concluded.
    if cpu.empty() != True and toggle == 'E':
        runningState = cpu.get() #Grabs the key of the next process in line and dequeues it
        toggle = 'F' #Toggle to mark CPU as full
        currentProcesstrace = traces[runningState]#Grabs the trace list of the process and stores it
        context_switch_report(time,runningState, currentProcesstrace,cpu,io)
        #process_tracker(time, toggle, cpu, runningState)#Calls in the Process Tracker for TW TTR TR
        #print(f"Currently working on -> {runningState}") # Debugging
    
    #Continues the current CPU burst
    if toggle != 'E':
        process_tracker(time, toggle, cpu, runningState)#Calls in the Process Tracker for TW TTR TR
        toggle = cpu_handler(runningState,currentProcesstrace,io,toggle)#Calls the CPU handler function and asks for a toggle value
        if toggle == 'E':
            #print(f"Process {runningState} finished CPU burst and was sent to I/O. Protecting for this iteration") # - Debugging
            # Marking the finished process as new and preventing it's subsequent burst from being decreased this time
            newestProcess = runningState 
        if toggle == 'C':#C for Concluded
            context_switch_report(time,runningState, currentProcesstrace,cpu,io)
            process_tracker(time, toggle, cpu, runningState)#Calls in the Process Tracker for TW TTR TR
            print(f"At time: {time + 1}. Process {runningState} concluded.")
            toggle = 'E'

    if len(io) != 0:
        input_output_handler(cpu, io, newestProcess)
    #Checks if the CPU is Idle
    if cpu.empty() and toggle == 'E' and len(io) != 0:
        #print("CPU IDLING...") # - Debugging
        cpuUtil += 1
    time += 1 #Time always moves forward
grand_finale (time,runningState, currentProcesstrace,cpu,io, cpuUtil)
#print("Program has concluded") # - Debugging