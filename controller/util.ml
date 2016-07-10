open Types

let char_of_color c =
  match c with
  | White -> 'W'
  | Black -> 'B'

let print_mask m =
  let separator = "\n   +----+----+----+----+----+----+----+----+\n" in
  print_string separator;
  for j = 7 downto 0 do
    Printf.printf " %d |" (j + 1);
    for i = 0 to 7 do
      match m.(i).(j) with
      | Some c -> Printf.printf "  %c |" (char_of_color c)
      | None -> print_string "    |"
    done;
    print_string separator;
  done;
  print_string "\n      a    b    c    d    e    f    g    h\n"

let print_diff diff =
  let separator = "\n   +----+----+----+----+----+----+----+----+\n" in
  print_string separator;
  for j = 7 downto 0 do
    Printf.printf " %d |" (j + 1);
    for i = 0 to 7 do
      try
        let (_, before, after) =
          List.find (fun ((i', j'),_, _) -> i = i' && j = j') diff
        in
        match before, after with
        | Some(c1), Some(c2) ->
            Printf.printf " %c%c |" (char_of_color c1) (char_of_color c2)
        | Some(c1), None ->
            Printf.printf " %c. |" (char_of_color c1)
        | None, Some(c2) ->
            Printf.printf " .%c |" (char_of_color c2)
        | None, None -> print_string "    |"
      with Not_found ->
        print_string "    |"
    done;
    print_string separator;
  done;
  print_string "\n      a    b    c    d    e    f    g    h\n"


let warning s =
  Printf.eprintf "%s\n" s

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
      if board.(i).(j) = None then board.(i).(j) <- f;
      incr cpt
    done
  done;
  board

let mask_of_position pos =
  (mask_of_string (string_of_position pos))

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
let dmove_of_masks (p:position) (m1:mask) (m2:mask): dmove =
  let diff = diff_mask m1 m2 in
  let dmove =
    begin match diff with
    | [] -> DNoMove
    | [ _ ] -> DError
    | [ ((i1,j1), Some color1, None);
        ((i2,j2), None, Some color1'); ]
    | [ ((i2,j2), None, Some color1');
        ((i1,j1), Some color1, None); ] ->
          if color1 = color1' && p.turn = color1 then
            DMove (i1, j1, i2, j2)
          else
            DError
    | [ ((i1,j1), Some color1, None);
        ((i2,j2), Some color2, Some color1'); ]
    | [ ((i2,j2), Some color2, Some color1');
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
    | diff ->
        DError
    end
  in
  begin match dmove with
  | DError ->
      begin match p.prev with
      | Some previous_pos ->
          let prev_m = mask_of_position previous_pos in
          if prev_m = m2 then DUndo
          else DError
      | None -> DError
      end
  | _ -> dmove
  end

let is_legal_move pos move =
  begin match move with
  | Undo -> true
  | _ -> List.mem move (Ochess.legal_moves pos)
  end

let is_promotion pos (i1,j1,i2,j2) =
  begin match pos.ar.(i1).(j1) with
  | Piece (Pawn, c) when c = pos.turn ->
      begin match c with
      | White -> j1 = 6 && j2 = 7
      | Black -> j1 = 1 && j2 = 0
      end
  | _ -> false
  end

let move_of_dmove pos dmove =
  let move_opt =
    match dmove with
    | DNoMove -> None
    | DMove (i1,j1,i2,j2) ->
        if is_promotion pos (i1,j1,i2,j2) then
          Some (Promotion (Queen, i1, i2))
        else
          Some (Move (i1,j1,i2,j2))
    | DEnPassant (color,(i1,j1,i2,j2),(o1,o2)) ->
        Some (Move (i1,j1,i2,j2))
    | DQueenside_castle ->
        Some Queenside_castle
    | DKingside_castle ->
        Some Kingside_castle
    | DUndo ->
        Some Undo
    | DError -> None
  in
  begin match move_opt with
  | Some move ->
      if is_legal_move pos move then
        Some move
      else
        None
  | None -> None
  end

let make_move pos move =
  begin match move with
  | Undo ->
      begin match pos.prev with
      | Some previous_pos -> previous_pos
      | None -> assert false
      end

  | _ -> Ochess.make_move pos move 0
  end

let parse_message msg =
  begin match String.sub msg 0 4 with
  | "MASK" ->
      MASK (mask_of_string (String.sub msg 5 128))
  | "OBST" ->
      OBST
  | "NOCB" ->
      NOCB
  | _ ->
      OTHER msg
  end

exception Break

let possible_states_of_position pos =
  let moves = Ochess.legal_moves pos in
  let positions =
    List.map (fun move -> Ochess.make_move pos move 0) moves
  in
  let positions =
    begin match pos.prev with
    | None -> positions
    | Some p -> p :: positions
    end
  in
  let can_white = Array.make_matrix 8 8 false in
  let can_black = Array.make_matrix 8 8 false in
  let can_empty = Array.make_matrix 8 8 false in
  let must_white = Array.make_matrix 8 8 true in
  let must_black = Array.make_matrix 8 8 true in
  let must_empty = Array.make_matrix 8 8 true in
  for i = 0 to 7 do
    for j = 0 to 7 do
      List.iter
        (fun p ->
          begin match p.ar.(i).(j) with
            | Piece (_, White) ->
                can_white.(i).(j) <- true;
                must_black.(i).(j) <- false;
                must_empty.(i).(j) <- false
            | Piece (_, Black) ->
                can_black.(i).(j) <- true;
                must_white.(i).(j) <- false;
                must_empty.(i).(j) <- false
            | Empty ->
                can_empty.(i).(j) <- true;
                must_white.(i).(j) <- false;
                must_black.(i).(j) <- false
          end)
        positions
    done
  done;
  { moves = moves;
    positions = positions;
    can_white = can_white;
    can_black = can_black;
    can_empty = can_empty;
    must_white = must_white;
    must_black = must_black;
    must_empty = must_empty; }

let mask_cleanup possible_states m1 m2 =
  let can_white = possible_states.can_white in
  let can_black = possible_states.can_black in
  let can_empty = possible_states.can_empty in
  let must_white = possible_states.must_white in
  let must_black = possible_states.must_black in
  let must_empty = possible_states.must_empty in
  let new_mask = Array.make_matrix 8 8 None in
  for i = 0 to 7 do
    for j = 0 to 7 do
      begin match m2.(i).(j) with
      | Some White ->
          new_mask.(i).(j) <-
            begin match can_white.(i).(j), must_black.(i).(j), must_empty.(i).(j) with
            | true, false, false -> Some White
            | false, true, false -> Some Black
            | false, false, true -> None
            | _ -> m1.(i).(j)
            end
      | Some Black ->
          new_mask.(i).(j) <-
            begin match can_black.(i).(j), must_white.(i).(j), must_empty.(i).(j) with
            | true, false, false -> Some Black
            | false, true, false -> Some White
            | false, false, true -> None
            | _ -> m1.(i).(j)
            end
      | None ->
          new_mask.(i).(j) <-
            begin match can_empty.(i).(j), must_white.(i).(j), must_white.(i).(j) with
            | true, false, false -> None
            | false, true, false -> Some White
            | false, false, true -> Some Black
            | _ -> m1.(i).(j)
            end
      end
    done
  done;
  new_mask
