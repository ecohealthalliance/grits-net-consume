## Synopsis

Utility tool to analyze airports in the Flirt database, which was populate by data provided by Innovata

The tool will:
- Loop through each country in the database
- Find the geographic center of each country
- Calculate great circle distance for each airport within each country
- Determine the mean distance, and standard deviation, for all airports to the center of the country
- Find outliers with pValue > 0.97 

## How To Run

This tool was originally created as an eclipse project, but can be ran from the command line.

## Compile

The main entry point is "Run.java"

To compile do this: 
javac -d bin/ -cp src:lib/* ./src/com/eha/flirt/Run.java

This will place the Java bytecode in the bin directory, and add the source files and all the jars in the lib folder to the classpath.

## Running

java -cp bin:lib/* com.eha.flirt.Run

## Output

output.txt in the res subfolder will show you outlier airports whos pValue is > 0.97
