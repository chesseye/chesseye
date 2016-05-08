let () =
  let d =
    if Array.length Sys.argv = 2 then
      try float_of_string Sys.argv.(1)
      with _ -> 0.01
    else
      0.01
  in
  try
    while true do
      let line = input_line stdin in
      Thread.delay d;
      print_endline line
    done
  with
  | _ -> ()

