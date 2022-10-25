Instruction for RAM Mapper:
~~~~~~~~~~~~~~~~~~~~~~~~
Open in PowerShell:

python RM.py
~~~~~~~~~~~~~~~~~~~~~~~~~
It will run the command on the default setting. Output file-name: output.txt. The checker.exe provided can check the legality of output and calculate the area of the solution by typing the following command into the PowerShell:

./checker -d logical_rams.txt logic_block_count.txt output.txt

#########################
~What is this program?

It is one of my project codes for the FPGA course. The goal is to design a RAM Mapper CAD tool to find the best combination of SRAM and LUTRAM (minimizing the circuit's space). 

There are three types of RAMs (8k SRAM, 128k SRAM, and LUTRAM). For every ten logic blocks, there is an 8k SRAM, and for every 100k, there is 128K RAM. 50% of logic blocks can be implemented as LUTRAM. 

My program needs to read the total number of not RAM-related general logic from logic_block_count.txt corresponding logic RAMs in logic_rams.txt for 69 benchmarks.

Other requirements, such as RAM capability and external circuitries (MUX) are also considered.



~Why do I choose this code?
 
It is a rather long code :) Thanks for your patience! I chose this code because it is my individual work and related to CAD Tools. It shows my understanding of python and my ability to handle relatively complex tasks. The result of 2.2e8 is considered as a Good optimization by my instructor.

