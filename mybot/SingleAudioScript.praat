  form Variables
    sentence filename test.wav
  endform

   Read from file... 'filename$'
   name$ = "test"

   select Sound 'name$'
       Trim silences... 0.05 1 100 0 -25 0.05 0.05 0 'silence'

trim$ = "_trimmed"
whole_name$  = name$ + trim$

select Sound 'whole_name$'
   
   deleteFile: "singleoutputPraat.csv"
   total_duration = Get total duration
   frame_len = total_duration / 250
   To Pitch... frame_len 75 400 

   select Pitch 'whole_name$'
   
   count_frames = Get number of frames
#   appendInfoLine: count_frames
   
   #hertz_vector# = zero# (78)
   
   for i from 1 to 249
     hertz = Get value in frame... i Hertz
     hertz_vector [i] = hertz
   endfor

   mean = Get mean... 0.0 0.0 Hertz

   #appendInfoLine: hertz_vector

#   write to file
#   appendFile: "singleoutputPraat.csv", "test"
#   output$ = "test"

   for i from 1 to 249
#    output$ = output$ + string$(hertz_vector [i])
       appendFile: "singleoutputPraat.csv", ",", hertz_vector [i]
   endfor
   appendFile: "singleoutputPraat.csv", ",", total_duration, ",", mean, newline$
 
#   select Sound test
#   Remove
#appendInfoLine: output$
#echo 'output$'
