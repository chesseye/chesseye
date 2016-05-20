open Types

let kibb = ref 3
let sync_input = ref false

let () =
  Arg.parse
    [ "-kibbitz", Arg.Set_int kibb, "<n> where 0: no, 1: white, 2: black, 3: both";
      "-sync-input", Arg.Set sync_input, "read the input in blocking mode"]
    (fun _ -> ())
    (Sys.argv.(0)^" [-kibbitz n]")

let advices =
  match !kibb with
  | 0 -> []
  | 1 -> [White]
  | 2 -> [Black]
  | 3 -> [White; Black]
  | _ -> [White; Black]

let async_input = not !sync_input
