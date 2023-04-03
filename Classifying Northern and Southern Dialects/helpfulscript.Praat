# This script extracts the mean and max intensity of an audio file
# and the mean and max value of each of the first two formants.
# It then writes these values out to a file

# Give Praat the path to the directory where your audio files are stored
# ASSIGN THIS VARIABLE TO THE PATH TO YOUR AUDIO DATA DIRECTORY
directory$ = "/Users/sam/Desktop/Courses/sem4/Speech Processing/Problem Set/Q5/Dialects"

# Give Praat the path to your output file
# ASSIGN THIS VARIABLE TO THE FULL PATH TO YOUR OUTPUTFILE
outputfile$ = "/Users/sam/Desktop/Courses/sem4/Speech Processing/Problem Set/Q5/dialectsdataoutput.csv"
deleteFile: outputfile$ 

# print a line to your output file containing the names of the features
appendFileLine: outputfile$, "maxint,meanint,maxf1,meanf1,maxf2,meanf2, maxpitch, meanpitch, maxharmonicity, meanharmonicity, dx"

# loop through the files one by one
ctr = 0
strings = Create Strings as file list: "list", directory$ + "/*.mp3"
numberOfFiles = Get number of strings
for ifile to numberOfFiles
	ctr = ctr + 1
    selectObject: strings
    fileName$ = Get string: ifile
    appendInfoLine: fileName$

    # this is just so you know the name of the sound you're dealing with
    # that way, you can select it later on if you need to
    fileIntro$ = replace$ (fileName$, ".mp3", "", 1)
    appendInfoLine: fileIntro$

    # read in the sound file
    Read from file: directory$ + "/" + fileName$
    appendInfoLine: fileIntro$ + "read!"

    # make sure you've selected the sound
    selectObject: "Sound " + fileIntro$

    # get max and mean intensity (a.k.a. energy) of that sound
    To Intensity: 100, 0, "yes"
    appendInfoLine: fileIntro$ + "intensity!"

    maxintensity = Get maximum: 0, 0, "Parabolic"
    meanintensity = Get mean: 0, 0, "energy"

    # print the info out to a file
    appendFile: outputfile$, maxintensity, ",", meanintensity, ","

    # make sure you select the sound again
    selectObject: "Sound " + fileIntro$

    # get formant information for that sound
    To Formant (burg): 0, 5, 5500, 0.025, 50
    appendInfoLine: fileIntro$ + " formant!"

    for formnum from 1 to 2
			 appendInfoLine: "formant"
         maxf = Get maximum: formnum, 0, 0, "Hertz", "Parabolic"
         meanf = Get mean: formnum, 0, 0, "Hertz"
	 		 appendFile: outputfile$, maxf, ",", meanf, ","
    endfor

	# make sure you've selected the sound
    selectObject: "Sound " + fileIntro$

    # get max and mean pitch (a.k.a f0) for that sound
    To Pitch: 0, 75, 600
    appendInfoLine: fileIntro$ + "Pitch!"

    maxpitch = Get maximum: 0, 0, "Hertz", "Parabolic"
    meanpitch = Get mean: 0, 0, "Hertz"

    # print the info out to a file
    appendFile: outputfile$, maxpitch, ",", meanpitch, ","

	# make sure you've selected the sound
    selectObject: "Sound " + fileIntro$

    # get harmonicity for that sound
    To Harmonicity (ac): 0.01, 75, 0.1, 4.5
    appendInfoLine: fileIntro$ + "Harmonicity!"

    maxharmonicity = Get maximum: 0, 0, "Parabolic"
    meanharmonicity = Get mean: 0, 0

    # print the info out to a file
    appendFile: outputfile$, maxharmonicity, ",", meanharmonicity, ","

    appendInfoLine: "data complete!"
	appendInfoLine: ctr

    # finally, write out the class (northern or southern)
	  ## IF YOU WANT TO USE WEKA COMMENT THIS OUT
    if startsWith(fileIntro$, "southern")
	     appendFileLine: outputfile$, "1"        
    else
	     appendFileLine: outputfile$, "0"        
    endif

	  ## IF YOU WANT TO USE WEKA UNCOMMENT
    #if startsWith(fileIntro$, "southern")
	  #   appendFileLine: outputfile$, "south"        
    #else
	  #    appendFileLine: outputfile$, "north"        
    #endif


  	 removeObject: "Sound " + fileIntro$
	 removeObject: "Formant " + fileIntro$
	 removeObject: "Intensity " + fileIntro$
	 

endfor


removeObject: "Strings list"