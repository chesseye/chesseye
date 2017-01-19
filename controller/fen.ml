(* Import/Export from position to FEN notation *)

open Types

let string_of_white_piece p =
  match p with
  | King -> "K" | Queen -> "Q" | Rook -> "R" | Bishop -> "B" | Knight -> "N" | Pawn -> "P"
	
let string_of_black_piece p =
  match p with
  | King -> "k" | Queen -> "q" | Rook -> "r" | Bishop -> "b" | Knight -> "n" | Pawn -> "p"

let string_of_char c =
  String.init 1 (fun i -> c)
let piece_of_string p =
  match p with
  | 'K' -> (King,White) | 'k' -> (King,Black)
  | 'Q' -> (Queen,White) | 'q' -> (Queen,Black)
  | 'R' -> (Rook,White) | 'r' -> (Rook,Black)
  | 'B' -> (Bishop,White) | 'b' -> (Bishop,Black)
  | 'N' -> (Knight,White) | 'n' -> (Knight,Black)
  | 'P' -> (Pawn,White) | 'p' -> (Pawn,Black)
  | _ -> raise (Failure ("Unknown piece: " ^ (string_of_char p)))
	
let string_of_black_piece p =
  match p with
  | King -> "k" | Queen -> "q" | Rook -> "r" | Bishop -> "b" | Knight -> "n" | Pawn -> "p"

let string_of_turn turn =
  match turn with
  | White -> "w"
  | Black -> "b"

let string_of_castling pos =
  let acc = ref "" in
  begin
    match pos.cas_w with
    | (true,true) -> acc := !acc ^ "KQ"
    | (false,true) -> acc := !acc ^ "K"
    | (true,false) -> acc := !acc ^ "Q"
    | (false,false) -> ()
  end;
  begin
    match pos.cas_b with
    | (true,true) -> acc := !acc ^ "kq"
    | (false,true) -> acc := !acc ^ "k"
    | (true,false) -> acc := !acc ^ "q"
    | (false,false) -> ()
  end;
  if !acc = "" then "-" else !acc

let string_of_enpassant pos =
  match pos.en_passant with
  | None -> "-"
  | Some col ->
      begin
	match pos.turn with
	| White -> Printf.sprintf "%c6" (Ochess.letter_of_int col)
	| Black -> Printf.sprintf "%c3" (Ochess.letter_of_int col)
      end
    
let fen_of_position pos =
  let acc = ref "" in
  let empties = ref 0 in
  for j = 7 downto 0 do
    for i = 0 to 7 do
      match pos.ar.(i).(j) with
      | Empty -> incr empties
      | Piece (pt,White) ->
	  begin
	    if !empties = 0
	    then
	      acc := !acc ^ (string_of_white_piece pt)
	    else
	      begin
		acc := !acc ^ (string_of_int !empties) ^ (string_of_white_piece pt);
		empties := 0;
	      end
	  end
      | Piece (pt,Black) ->
	  begin
	    if !empties = 0
	    then
	      acc := !acc ^ (string_of_black_piece pt)
	    else
	      begin
		acc := !acc ^ (string_of_int !empties) ^ (string_of_black_piece pt);
		empties := 0
	      end
	  end
    done;
    let trans = if j = 0 then " " else "/" in
    if !empties = 0
    then
      acc := !acc ^ trans
    else
      begin
	acc := !acc ^ (string_of_int !empties) ^ trans;
	empties := 0
      end
  done;
  begin
    acc := !acc ^ (string_of_turn pos.turn) ^ " ";
    acc := !acc ^ (string_of_castling pos) ^ " ";
    acc := !acc ^ (string_of_enpassant pos) ^ " ";
    acc := !acc ^ (string_of_int pos.irr_change) ^ " ";
    acc := !acc ^ (string_of_int pos.number)
  end;
  !acc

let print_fen pos =
  Printf.printf "\n[Edwards][%s]\n" (fen_of_position pos)

let long_string_of_smove pos smove =
  let ed = fen_of_position pos in
  "\"" ^ ed ^ "\" \"" ^ (Ochess.string_of_smove pos smove) ^ "\""

let long_string_of_move move pos =
  match pos.prev with
  | Some prev ->
      let ed = fen_of_position prev in
      "\"" ^ ed ^ "\" \"" ^ (Ochess.string_of_move prev move) ^ "\""
  | None ->
      "INIT"

let decompose_fen (fen:string) : (string list * string * string * string * string * string) =
  let white_split = Str.split (Str.regexp "[ \t]+") fen in
  begin match white_split with
  | [a0;a1;a2;a3;a4;a5] ->
      let slash_split = Str.split (Str.regexp "/") a0 in
      (slash_split,a1,a2,a3,a4,a5)
  | _ -> raise (Failure "Cannot parse FEN notation")
  end

let board_and_kings_of_fen (f0:string list) =
  let board = Array.make_matrix 8 8 Empty in
  let kw = ref None in (* To remember white king's position *)
  let kb = ref None in (* To remember black king's position *)
  let k = ref 0 in (* Current file *)
  for i = 0 to 7 do
    let current_rank = List.nth f0 i in
    k := 0; (* Reset current file *)
    for j = 0 to String.length current_rank-1 do
      let c = String.get current_rank j in
      begin try
	let piece = piece_of_string c in
	begin match piece with
	| (King,White) -> kw := Some (!k,7-i)
	| (King,Black) -> kb := Some (!k,7-i)
	| _ -> ()
	end;
	board.(!k).(7-i) <- Piece piece;
	incr k (* Piece has been recognized to increment by one *)
      with
      | Failure _ ->
	  let nb = int_of_string (String.make 1 c) in
	  k := !k+nb; (* Piece has not been recognized to skip as many times as necessary *)
      end
    done
  done;
  begin match !kw,!kb with
  | (Some x, Some y) -> (board, x, y)
  | (_, _) ->
      raise (Failure "Did not found king in position")
  end

let color_of_fen (a1:string) =
  begin match a1 with
  | "w" -> White
  | "b" -> Black
  | _ -> raise (Failure "Not a color in position")
  end

let cb_of_fen (a2:string) =
  if (a2 = "-") then ((false,false),(false,false))
  else
    let ksidew = ref false in
    let qsidew = ref false in
    let ksideb = ref false in
    let qsideb = ref false in
    let n = String.length a2 in
    if n > 4 then
      raise (Failure "Not a valid castling description in position")
    else
      begin
	for i = 0 to (n-1) do
	  let c = String.get a2 i in
	  match c with
	  | 'K' -> ksidew := true
	  | 'Q' -> qsidew := true
	  | 'k' -> ksideb := true
	  | 'q' -> qsideb := true
	  | _ -> raise (Failure "Not a valid castling description in position")
	done;
	((!ksidew,!qsidew),(!ksideb,!qsideb))
      end

let en_passant_of_fen (a3:string) =
  if (a3 = "-") then None
  else
    try Some (Ochess.int_of_letter (String.get a3 0)) with
    | _ -> raise (Failure ("Not a valid en-passant description in position"))

let pawn_moves_of_fen (a4:string) =
  int_of_string a4
    
let full_moves_of_fen (a5:string) =
  int_of_string a5
    
let position_of_fen (fen:string) =
  let (board_fen, a1, a2, a3, a4, a5) = decompose_fen fen in
  let (board,kw,kb) = board_and_kings_of_fen board_fen in
  let color = color_of_fen a1 in
  let (cw,cb) = cb_of_fen a2 in
  let enp = en_passant_of_fen a3 in
  let pmoves = pawn_moves_of_fen a4 in
  let fmoves = full_moves_of_fen a5 in
  { ar = board;
    turn = color;
    cas_w = cw; cas_b = cb;
    en_passant = enp;
    prev = None;
    irr_change = pmoves; (* number of moves since capture or pawn move *)
    king_w = kw; king_b = kb; (* king positions are required often *)
    number = fmoves; (* position number, initial position is 0 *)
    eval = 0 }
