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


let diff_mask (mask1:mask) (mask2:mask) =
  let acc = ref [] in
  for i = 0 to 7 do
    for j = 0 to 7 do
      if mask1.(i).(j) <> mask2.(i).(j) then
        acc := ((i,j), mask1.(i).(j), mask2.(i).(j)) :: !acc
    done
  done;
  !acc

(* Auxiliary for Roque *)
let consistent_line_and_color (l1,l2,l3,l4) (color1,color2,color3,color4) =
  if (l1 = 0) && (l1 = l2) && (l2 = l3) && (l3 = l4)
      && (color1 = White) && (color1 = color2) && (color2 = color3) && (color3 = color4)
  then
    true
  else if (l1 = 7) && (l1 = l2) && (l2 = l3) && (l3 = l4)
      && (color1 = Black) && (color1 = color2) && (color2 = color3) && (color3 = color4)
  then
    true
  else
    false

let chose_castle_side (c1,c2,c3,c4) =
  if ((c1 = 4) && (c2 = 7)) || ((c2 = 4) && (c1 = 7))
  then
    if ((c3 = 6) && (c4 = 5)) || ((c4 = 6) && (c3 = 5))
    then
      DKingside_castle
    else
      DError
  else
  if ((c1 = 4) && (c2 = 0)) || ((c2 = 4) && (c1 = 0))
  then
    if ((c3 = 2) && (c4 = 3)) || ((c4 = 2) && (c3 = 3))
    then
      DQueenside_castle
    else
      DError
  else
    DError

(* Main move detection *)
let dmove_of_masks (mask1:mask) (mask2:mask): dmove =
  begin match diff_mask mask1 mask2 with
  | [] -> DNoMove
  | [ _ ] -> DError
  | [ ((i1,j1), Some color1, None);
      ((i2,j2), None, Some color1'); ]
  | [ ((i2,j2), None, Some color1');
      ((i1,j1), Some color1, None); ] ->
      if color1 = color1' then
        DMove (i1, j1, i2, j2)
      else
        DError
  | [ ((i1,j1), Some color1, None);
      ((i2,j2), Some color1', Some color2); ]
  | [ ((i2,j2), Some color1', Some color2);
      ((i1,j1), Some color1, None) ] ->
      if color1 = color1' && color1 <> color2 then
        DMove (i1, j1, i2, j2)
      else
        DError
  | [ ((i1, j1), Some color1, None);
      ((i2, j2), Some color2, None);
      ((i3, j3), None, Some color3); ]
  | [ ((i1, j1), Some color1, None);
      ((i3, j3), None, Some color3);
      ((i2, j2), Some color2, None); ]
  | [ ((i3, j3), None, Some color3);
      ((i1, j1), Some color1, None);
      ((i2, j2), Some color2, None); ]->
        if color1 = color2 then
          DError
        else if color1 = color3 then
          DEnPassant (color1, (i1, j1, i3, j3), (i2, j2))
        else if color2 = color3 then
          DEnPassant (color2, (i2, j2, i3, j3), (i1, j1))
        else
          DError
  (* King side is: K:4->6 && R:7->5 *)
  (* Queen side is: K:4->2 && R:0->3 *)
  | [ ((c1, l1), Some color1, None);
      ((c2, l2), Some color2, None);
      ((c3, l3), None, Some color3);
      ((c4, l4), None, Some color4); ]
  | [ ((c1, l1), Some color1, None);
      ((c3, l3), None, Some color3);
      ((c2, l2), Some color2, None);
      ((c4, l4), None, Some color4); ]
  | [ ((c1, l1), Some color1, None);
      ((c3, l3), None, Some color3);
      ((c4, l4), None, Some color4); 
      ((c2, l2), Some color2, None); ]
  | [ ((c3, l3), None, Some color3);
      ((c1, l1), Some color1, None);
      ((c2, l2), Some color2, None);
      ((c4, l4), None, Some color4); ]
  | [ ((c3, l3), None, Some color3);
      ((c1, l1), Some color1, None);
      ((c4, l4), None, Some color4); 
      ((c2, l2), Some color2, None); ]
  | [ ((c3, l3), None, Some color3);
      ((c4, l4), None, Some color4); 
      ((c1, l1), Some color1, None);
      ((c2, l2), Some color2, None); ] ->
	if (consistent_line_and_color (l1,l2,l3,l4) (color1,color2,color3,color4))
	then
	  chose_castle_side (c1,c2,c3,c4) 
	else
	  DError
(*| [ _ ; _ ] -> DError
  | [ _ ; _ ; _ ] -> DError *)
  end

