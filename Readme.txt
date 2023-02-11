Summary:
The RAM Mapper is a python CAD tool that helps find the optimal combination of SRAM and LUTRAM in an FPGA archiecture (minimize the circuit space).

~~~~~~~~~~~~~~~~~~~~~~~
Input Files:
logic_block_count.txt: contains the total number of non-RAM-related general logic for 69 benchmarks.
logic_rams.txt: contains information about the corresponding logic RAMs for each benchmark.

~~~~~~~~~~~~~~~~~~~~~~~~
Running the progrtam:
1. Open PowerShell:
2. execute RM.py. This will run the RAM Mapper tool with the default settings.

~~~~~~~~~~~~~~~~~~~~~~~~
Checking the legality of the output:
The checker.exe program provided can be used to verify the legality of the output and calculate the area of the solution. To use it, type the following command into PowerShell:

./checker -d logical_rams.txt logic_block_count.txt output.txt

Note: In this program, there are three types of RAMs: 8k SRAM, 128k SRAM, and LUTRAM. For every ten logic blocks, there is an 8k SRAM, and for every 100k, there is 128K RAM. 50% of logic blocks can be implemented as LUTRAM. Additionally, other requirements, such as RAM capability and external circuitries (MUX), are also considered in the optimization.


~Why do I choose this code?
 
It is a rather long code :) Thanks for your patience! I chose this code because it is my individual work and related to CAD Tools. It shows my understanding of python and my ability to handle relatively complex tasks. The result of 2.2e8 is considered as a Good optimization by my instructor.

