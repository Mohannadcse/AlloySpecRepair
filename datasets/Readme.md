#### This folder contains Benchmark Datasets for Alloy4Fun and Arepair 

#### The folders A4F and Arepair contains buggy specifications 

#### A4F : 1936 spec (single line bugs)
#### Arepair 38 spec (single and multi line bugs)

-------------

#### The correct_spec folder contains the specifications along with the proposed fix suggested by 

#### https://github.com/guolong-zheng/atmprep/tree/master/benchmark 


-------------

## How the dataset was adopted 


### Arepair Benchmark:

This benchmark has single and multi line bugs. 

#### For Buggy version 

-> Lines with `// Fix:` comments has been removed.  
-> considering the bug still existis , running the spceification would generate a counterexample. 

#### For Correct version 
-> Lines with `// Fix:` comments has been removed. 
-> The fix has been implemented in the corresponding / next line. 


There are 20 specifications with single line bug and 18 specifications with multi line bugs. 


### A4F Benchmark:

This benchmark contains single line bugs. 

#### For Buggy version 

-> Removed all commented lines in each invariant ("`--correct`" and "`--incorrect`" marked lines).  

Example : All commented lines in the below example is removed

Original
```
pred inv10 {
--	all c:Class, s:Student | some s.(c.Groups) --correct
 ((Class . Groups) . Group & Student) = Student 
-- ((Class . Groups) . Group) & Student = Student  --incorrect 2
-- ((Class . Groups) . Group) = Student  --incorrect 3
-- (Class . Groups) . Group & Student = Student  --incorrect 4
-- (Class . Groups) . Group = Student  --incorrect 5
-- (Class . Groups) . Group in Student  --incorrect 6

````
modified 

````
((Class . Groups) . Group & Student) = Student
````



-> Uncommented lines left retained/ unchanged from the original benchmark.

From the above example, this specific lines remain in the invariant
`````
((Class . Groups) . Group & Student) = Student
`````

-> Those lines were not removed. 

-> Uncommented lines indicate a buggy line in each invariant. 

-> It would result in a counterexample when checked. 







