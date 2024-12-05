# CPU Scheduler Algorithm Simulations
### Table of Contents
- [Introduction](https://github.com/NullPointerHQ/CPU-Scheduler-Sims/tree/main?tab=readme-ov-file#introduction)

## Introduction
### Project Objectives
To simulate how a CPU schedules processes using three algorithms and display the results. The algorithms are:
1. **F**irst **C**ome **F**irst **S**erved (FCFS)
2. **S**hortest **J**ob **F**irst (SJF)
3. **M**ulti**l**evel **F**eedback **Q**ueue (MLFQ)

### Prerequisites 
- Language Used: Python Version 3.9
- IDE: [Microsoft's Visual Studio](https://visualstudio.microsoft.com/#vs-section)
  - This program should be able to run in other IDEs though I have not tested this. 
- Python 'Queue' library.
  - Used to simulate a CPU ready queue
  - Required for FCFS and MLFQ Algorithms, SJF imports the library but never uses it
### Repository Guide
Each folder contains three files, two of them are created by Visual Studio and can be safely ignored, I have linked to the source code files below for convenience:
- [Source Code for First Come First Served](First%20Come%20First%20Served%20Scheduler%20Simulation/First_Come_First_Served_Scheduler_Simulation.py) 
- [Source Code for Shortest Job First](Shortest%20Job%20First/Shortest_Job_First.py) 
- [Source Code for Multilevel Feedback Queue](MultiLevelQueueFeedback/MultiLevelQueueFeedback.py)
### Assumptions
1. All processes arrive at _t_ = 0
2. Processes initially arrive in sequential order. (i.e Process 1 will arrive before Process 2 which arrives before Process 3 and so on), the number for each process
 is arbitrarily selected
3. Processes all start and end on a CPU burst
4. A trace list is provided for each process
### Configuration Options
All algorithms come preconfigured with default processes and traces, however if you wish you can reconfigure these to add bursts, remove bursts, add entire new processes 
and so forth. 

To do this, locate the following dictionaries in any of the programs:
```python
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
```
```python
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
```
Warning: _both of these dictionaries must have a matching number of keys and these keys must match across both dictionaries_ 

The primary difference between these two dictionaries is the list held as the value of the pairs detailed below:

traces Dictionary Values: Holds process trace lists
- An integer list that conains _n_ amount of bursts
- Bursts can be any length
- Must end on a CPU burst or the program will shut down preemptively.

processInfo Dictionary Values: Holds the information of processes
- All lists must have exactly 3 values
- The values cannot be configured and are managed by the program
- The first value is the time before initial response, this must start at -1
- The second and third are the total time waiting and total turnaround time respectively, these must start at 0

Steps to add a process:
1. Create a new entry in the traces dictionary
  - The key must be a string ,the specific contents are unimportant
  - The value must be an integer list that obeys the rules above
2. Create an entry in the processInfo dictionary
  - The key must match with the traces dictionary
  - The value must be an integer list with three values [-1, 0, 0]

To remove a process simply delete its entry from both traces and processInfo dictionaries.

To add, remove or modify bursts, change the values in the list associated with the process whose trace list you wish to adjust. For example, before modification:
```python
"P1" : [5, 27, 3, 31, 5, 43, 4, 18, 6, 22, 4, 26, 3, 24, 4],
```
After modification:
```python
"P1" : [5, 27, 3, 31, 5, 43, 4, 18, 6, 22, 4, 26, 3, 24, 4, 1, 2, 3],
```
Note: All algorithims include a grand_finale function that calculates the averages for each metric, this function assumes exactly 8 processes, if you add or remove processes be sure to update the calculation 
formula.
## Algorithm Overviews
From here on is an overview for each algorithm on how they operate, these sections will not explain the exact details of every function as the commentary 
in the source code should be sufficient for this purpose. Instead these sections will focus on explaining in high level terms how the algorithms work and important functions.
## First Come First Served
The algorithm will begin by initializing the dictionaries for the processes and pushing the processes to the cpu queue as shown here:
```python
for key in traces.keys():
    cpu.put(key)
```

 Afterwards it will create the following variables
- time 
	- Counter, tracks current time
- toggle 
	- Tracks the state of the CPU (**E**mpty, **F**ull, **C**oncluded)
- cpuUtil 
	- Tracks time the toggle is set to **E** AND I/O is not empty, The CPU is idle at this point. Used later
- runningState
	- Temporary variable for the process currently in the CPU
- currentProcesstrace
	- Temporary list to hold the trace of the process currently in the CPU
 
After all of the above, the algorithm can begin the simulation. As long as the following three conditions are not met the program will continue to execute:
1. The CPU queue is empty (No processes waiting)
2. The I/O list length is zero (No process in I/O)
3. The value of toggle is "E" (CPU is not occupied)

Simply put, the simulation runs as long as there are processes to execute, the following instructions will occur:
1. Variable newestProcess is initialized to '-', this variable protects a process in the I/O list if that process only joined the list that iteration.
2. If the CPU queue is NOT empty and the CPU is free, the program will grab the next available process, its trace list and set toggle to F.
	- A context switch has occured, the context switch function is called to generate a report and display it.

	![Figure 1: Example Context Switch Report](README%20Images/Context%20Switch%20Report%20Example.png)

	- If both conditions above are not met then this step is skipped altogether.
     - It is expected that this occurs especially towards the end of operations as more processes have concluded
4. If the CPU is busy
	- Call the process tracker function to track Response time (if the process has not appeared before) and time waiting
	- Call the CPU handler function
		- CPU Handler will take the process and
			- Subtract 1 from its burst if the burst isnt already zero 
			- If the burst is zero and the trace list has more than one element, add the process to the back of the I/O list and set toggle to E
			- If the burst is zero and the trace list has only one element, set toggle to C
			- If the value of the burst is not zero nothing is done to toggle.
			- toggle is always returned to the main function
	- If the toggle indicates the process has finished its burst and was sent to I/O then the process becomes the value of the newestProcess,
	to ensure that it is not affected this iteration because time has not yet passed.
	- If the toggle indicates the process has concluded, a context switch report must be generated and the process_tracker function is called to track turnaround time. 
	
 ![Figure 2: Example Context Switch Report](README%20Images/Context%20Switch%20Report%20Example%202.png)

4. If I/O is not empty, the I/O Handler is invoked
	- The I/O handler operates similarly to the CPU_Handler
	- The I/O handler iterates through the list, subtracts 1 from the burst of each process.
		- Exception: The process selected has just arrived, this process is skipped. 
	- If the burst of a process is zero and its trace list has more than one value in it:
		- The burst is deleted from the trace list.
		- The process is sent back to the CPU queue
		- The process is removed from the I/O list.
	- Warning: If the burst of a process is zero and its trace list has only one index, an error is thrown and the program terminates early. 
5. If the CPU is not busy, the CPU queue is empty AND the I/O list has atleast one element, increase the value of cpuUtil by one
6. Increase time by one

Once the conditions outlined at the beginning have been met, the grand_finale function is invoked, this will calculate the averages for response, wait and turnaround times
as well as the CPU utilization percentage and display the final results of everything to the user in a table.

![Figure 3: ExampleFinal Results](README%20Images/Final%20Results%20Example.png)

## Shortest Job First 
The SJF program operates similarly to FCFS, therefore this section will focus on explaining the key implementation differences.
1. Certain variable names have changed however they still server the same function
2. New variable: 'sort' created, used as a flag to indicate when the ready list needs to be sorted
3. CPU Queue replaced with List, much easier to reorder elements in a list than in a queue.
4. New potential task created: CPU ready list is not empty and requires a sort. See below for code snippet:
```python
if sort == 'Y' and len(cpu) != 0:
        cpu = sjf_scheduler(cpu)# Calls the sorter
        #print(f"CPU List Received: {cpu}")# - Debugging
        sort = 'N'#Sorting is no longer needed
```
 - The sjf_scheduler function will do the following:
   - Make a temporary list with the exact same values as the CPU list
   - Delete the contents of the CPU list
     - If there is more than one element in the temp list:
       - Grab the first process key, its trace list and position
       - Iterate through the list checking if any other process in the list has a smaller value at index 0
				- If one is found, grab the process key, trace list and position in the list
			- Once at the end of the temporary list:
				- Add the process to the back of the CPU list
				- Delete the shortest process from the list 
				- Increase i by one
		- If there is only one element in the list then the list can be safely copied back to the CPU list 
		- Delete the temporary list, return the CPU list, it has now been sorted. 
5. The rest of the main functions similarly to FCFS
	- If the CPU is free and there are processes in the CPU list the program will take the next one
	- If the CPU is not free then it will call the cpu_handler to handle the process
		- When a process has concluded, a sort is required
	- Call I/O if needed
		- The I/O handler is able to call for a sort, if a process in its list finishes its I/O burst
	- and so on until grand_finale
## Multilevel Feedback Queue
The MLFQ algorithm is the most complex of the three. The main differences between this algorithm and FCFS are the multiple queues with their priority levels 
and managing the time limitations (known as timeQuantum) for each queue.  

There are now three CPU queues:
```python
hiPriority = queue.Queue(maxsize = 8) #'cpu' Queue acts as the CPU Ready state
medPriority = queue.Queue(maxsize = 8) #'cpu' Queue acts as the CPU Ready state
lowPriority = queue.Queue(maxsize = 8) #'cpu' Queue acts as the CPU Ready state
```
hiPriority
1. Takes precedence over medPriority and lowPriority.
2. Operates using round-robin 
    - Processes are allocated 5 time units each
      - Processes that exceed this allotment are paused and demoted to medPriority
3. Processes that are joining the ready queue start here

medPriority
1.  Takes precedence over lowPriority.
2.  Also uses round-robin
    - Processes are allocated 10 time units each
      - Processes that exceed this allotment are demoted to lowPriority

lowPriority
1. Standard FCFS queue
2. No time allocations
    - Note: In the program timeQuantum is set to -1 here as negative time is impossible to achieve.

New variable:
```python
priorityTracker = '-' #H for High, M for Med and L for low, tracks the previous queue
```
New variables for time_lord function:
```python
timeBefore = 0#Tracks Time before the new burst
originalBurst = 0#Tracks the original burst length
timeAfter = 0 #Tracks time after the burst
doioFlag = True#Prevents IO function from operating under certain cirucumstances
```

The WHILE loop condition has been adjusted to account for the presence of three queues instead of one. 

Previously, the system would check if the CPU was free and if the CPU queue was not empty, now the system will check if the CPU is free and if any of the queues are not 
empty. If these conditions are met, the mlfq_scheduler function will be invoked. 

The mlfq_scheduler function begins by checking each queue to identify which queue is not empty. If it finds one then it will:
- Grab the first process in it and its trace, 
- Set the toggle, 
- Set the priority tracker to the letter that indicates the queue the process was in. 

Back in the main function, After the mlfq scheduler has finished operations the following operations will be conducted:

- Call the process tracker function to track response and wait times.
- Call the context switch report function to inform the user that context switch has occurred
- If it is not zero, I is reset

- And operations relevant to the time lord function:
    - Grab the processes burst time
    - Grab the current time
	    - If the burst time of the process is greater than the allotted time for the process queue, then the value of original burst variable is reset to the max value for that queue (5 or 10).

If the CPU is free and all of the queues are empty then the CPU idle time will increase by one.

If the toggle indicates that a process is currently running on the CPU then the program will need to determine, using the value of the priority tracker variable,
which queue the process came from.
The value of priority tracker will determine:
- The amount of time the process is given in the CPU
- Which queue the process will go to next if it can not finish executing in the allotted time. 

After each call to the CPU Handler, the value of i will increase by one. i tracks the processes execution time, which is then used by the CPU Handler to determine
if a process is eligible to continue executing. If i is greater than timeQuantum, the process is automatically pushed to the next queue. 

If the burst for the process is zero, the CPU Handler function will determine, based on the length of the trace list, whether to send the process to the IO list or if it has finished executing all together. 

Once a process has finished executing and has been either sent to IO or has concluded all together a new routine will begin:
```python
  timeAfter = time + 1#Grabs the current time
  time, doioFlag = time_lord(time,doioFlag, originalBurst, priorityTracker, timeBefore, timeAfter, hiPriority,medPriority, lowPriority)
```
The time_lord function is explained in its own section. 

Returning to the main, if the toggle indicates:
-  The process has concluded
	- The user is informed of the conclusion time
	- The process tracker function is called to record the turnaround time for that process
- The process has been sent to IO
	- newestProcess grabs the value of the running process to protect it in the IO list

Lastly, if the doioFlag permits it, and there are elements in the IO list, then the input_output_handler is called. 
This function operates the same as in the previous two algorithms.

If the input output flag does not permit IO to operate then the flag will be reset to true.

Increment time, repeat this process.

When all processes have executed then the grand_finale function is invoked.

### The time_lord function
The time lord function is responsible for ensuring that the time is correctly tabulated, it achieves this by calculating split time:
```python
splitTime = afterTime - beforeTime
```
which is then compared to the burstTime. If these times do not match, the actual time is recalculated as:
```python 
time = time - (splitTime - burstTime)
```
It will then set the doioFlag to false indicating to the main function to skip the I/O operations for one iteration and adjust the wait times for all processes in the ready queues.

To make this a little more digestible, suppose that you have a process with the following:
1. Process 7
2. Original Queue: hiPriority
3. Burst Time: 7
   - Burst time exceeds maxiumum, new burst time: 5   
5. beforeTime (When the CPU started execution): 266
6. afterTime: 272
splitTime will be 6, which does not match the burst time (5), therefore the new time will be _272 - (6-5)_ which is _271_
 
The time lord function will then conduct all the necessary operations to rectify the time discrepancy, such as adjusting the wait times for processes in the wait queues.

Time discrepancies are guranteed, the time_lord function checks but only adjusts time _when necessary_

## Interpretation of Results
- Time Waiting (TW): Total time spent in CPU Ready List/Queue/Queues, does not include time in I/O.
- Time Response (TR): Total time before first execution
- Time Turnaround (TTR): Total time before concluding.
- CPU Utilization: The percentage of time that the CPU was occupied. 
