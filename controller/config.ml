open Types

let advices = ref [White; Black]
let set_advices kibb =
  advices :=
    begin match kibb with
    | 0 -> []
    | 1 -> [White]
    | 2 -> [Black]
    | 3 -> [White; Black]
    | _ -> [White; Black]
    end

let sync_input = ref false

let options =
  [ "-kibbitz", Arg.Int set_advices, "<n> where 0: no, 1: white, 2: black, 3: both";
    "-sync-input", Arg.Set sync_input, " read the input in blocking mode"]
