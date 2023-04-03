Prerequisite: Training and Testing files are in ipynb make sure to open the files in Jupyter Notebook environment or google colab environment.

Required Libraries: pandas, numpy, pickle, pprint, sklearn, statistics, 

Use "!pip install _______ "(Fill the name of the libraries in blank to just install in Google colab or Jupyter Notebook environment but if you are installing in command line remove the exclamatory mark and use the same command above to install the libraries.

Step 0:

We already extracted the features from praat and saved it in the following file named 'trainingdialectsdataoutput2.csv'. 

But if you want to run the praat script go ahead and run the helpfulscript.praat but while running for training please change the input directory for dialects stored as " path from your computer + /Q5/Dialects"

Step 1:

OPEN --> Open "Training.ipynb" file
RUN --> Go to 'Cell' option and then select 'Run All'
IMPORTANT NOTE--> The files required to run the 'Training.ipynb' are already zipped along with it. So just unzip the Q5 file and run the Training.ipynb file.
OUTPUT --> A pickle file will ve saved in the Q5 folder named "training_model2.pkl" once you ran all the cells in the Training.ipynb. file.
IMPORTANT NOTE --> I had commented out the save_model() command atlast in the "Training.ipynb" file to not overwrite the saved model which is already available in the Q5 folder. But if you want to test it please uncomment the the model and run the cell to OVERWRITE the saved model.

Step 2:

Similar to Step 0 the features for testing data is also extracted from praat and saved it in the folder named Q5 in the name "testdialectsdataoutput2.csv".

But if you want to run the praat script go ahead and run the helpfulscript.praat but while running for testing please change the input directory for dialects stored as " path from your computer + /Q5/DialectsTest/TestData"

IMPORTANT NOTE: I renamed the test files with leading names like northern and southern to generate the csv file for testing. Please ignore this. There is no malpractice done on this but just used the renaming to generate the prat test csv files.

Step 3:

OPEN --> Open "Testing.ipynb" file
RUN --> Go to 'Cell' option and then select 'Run All'
IMPORTANT NOTE--> The files required to run the 'Testing.ipynb' are already zipped along with it. So just unzip the Q5 file and run the Training.ipynb file. The two files required to run Testing.ipynb file is "testdialectsdataoutput2.csv" and "training_model2.pkl".
OUTPUT --> No output file will be generated from this but classification report and confusion matrix will be printed.


