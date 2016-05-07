open Types

let string_of_field color f =
  match f with
  | Empty -> "0"
  | Piece (_, c) when c = color -> "1"
  | Piece (_, c) ->
      assert (c <> color);
      "0"

let string_of_position p =
  let acc = ref "" in
  for i = 0 to 7 do
    for j = 0 to 7 do
      acc := !acc ^ (string_of_field White p.ar.(i).(j))
    done
  done;
  for i = 0 to 7 do
    for j = 0 to 7 do
      acc := !acc ^ (string_of_field Black p.ar.(i).(j))
    done
  done;
  !acc

let mask_of_string s : mask =
  let board = Array.make_matrix 8 8 None in
  let cpt = ref 0 in
  for i = 0 to 7 do
    for j = 0 to 7 do
      let f =
        begin match String.get s !cpt with
        | '0' -> None
        | '1' -> Some White
        | _ -> failwith "mask_of_string: illegal"
        end
      in
      board.(i).(j) <- f;
      incr cpt
    done
  done;
  for i = 0 to 7 do
    for j = 0 to 7 do
      let f =
        begin match String.get s !cpt with
        | '0' -> None
        | '1' -> Some Black
        | _ -> failwith "mask_of_string: illegal"
        end
      in
      board.(i).(j) <- f;
      incr cpt
    done
  done;
  board
