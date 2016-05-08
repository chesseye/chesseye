let () =
  try
    while true do
      let line = input_line stdin in
      Thread.delay 0.01;
      print_endline line
    done
  with
  | _ -> ()

