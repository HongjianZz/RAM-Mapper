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

Note: There are three types of RAMs available, including 8k SRAM, 128k SRAM, and LUTRAM. By default, an 8k SRAM is allocated for every ten logic blocks, and a 128k RAM is allocated for every 100k logic blocks. Additionally, 50% of logic blocks can be implemented using LUTRAM.


~Why do I choose this code?
 
I selected this project because I developed it independently, and it is related to manual testing. It demonstrates my proficiency in Python and my capability to tackle complex tasks. My instructor considers a result of 2.2e8 to be a good optimization.

