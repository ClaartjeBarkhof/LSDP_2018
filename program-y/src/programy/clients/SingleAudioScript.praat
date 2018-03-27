
     Read from file... ../../../../mybot/test.wav
     select Sound test2
   
   deleteFile: "singleoutputPraat.csv"
   total_duration = Get total duration
#   frame_len = total_duration / 80

   To Pitch... 0.0 75 400 
   select Pitch test2
   
   count_frames = Get number of frames
   appendInfoLine: count_frames
   
   #hertz_vector# = zero# (78)
   
   for i from 1 to 78
      hertz = Get value in frame... i Hertz
     hertz_vector [i] = hertz
   endfor

   mean = Get mean... 0.0 0.0 Hertz

   #appendInfoLine: hertz_vector

   # write to file
#   appendFile: "singleoutputPraat.csv", "test2"
   output$ = "test"
   echo "output$"

#   for i from 1 to 78
#       appendFile: "singleoutputPraat.csv", ",", hertz_vector [i]
#   endfor
#   appendFile: "singleoutputPraat.csv", ",", total_duration, ",", mean, newline$
 
#   select Sound test2
#   Remove