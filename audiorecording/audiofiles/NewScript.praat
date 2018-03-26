form Read all files of the given type from the given directory
   sentence Source_directory ./Archief
   sentence File_extension .wav
endform

Create Strings as file list... list 'source_directory$'/*'file_extension$'
head_words = selected("Strings")
file_count = Get number of strings

file_count
appendInfoLine: file_count

deleteFile: "archiefPraat.csv"
for current_file from 1 to file_count
   select Strings list
   filename$ = Get string... current_file
   Read from file... 'source_directory$'/'filename$'
   
   name$ = filename$ - file_extension$
   select Sound 'name$'
      Trim silences... 0.05 1 100 0 -25 0.05 0.05 0 'silence'

trim$ = "_trimmed"
whole_name$  = name$ + trim$

   total_duration = Get total duration
   frame_len = total_duration / 250

   To Pitch... frame_len 75 400 
   select Pitch 'whole_name$'
   
   count_frames = Get number of frames
   appendInfoLine: count_frames
   
   #hertz_vector# = zero# (78)
   
   for i from 1 to 249
      hertz = Get value in frame... i Hertz
     hertz_vector [i] = hertz
   endfor

   mean = Get mean... 0.0 0.0 Hertz

   #appendInfoLine: hertz_vector

   # write to file

   outputfile$ = "archiefPraat.csv"
   appendFile: outputfile$, filename$
   for i from 1 to 249
       appendFile: outputfile$, ",", hertz_vector [i]
   endfor
   appendFile: outputfile$, ",", total_duration, ",", mean, newline$
 
   select Sound 'name$'
   Remove
endfor