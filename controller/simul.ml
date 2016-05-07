open Ochess

exception WrongMove of string
  
let string_of_file file =
  try
    let inchan = open_in_bin file in
    let len = in_channel_length inchan in
    let buf = Buffer.create len in
    Buffer.add_channel buf inchan len;
    close_in inchan;
    Buffer.contents buf
  with
    Sys_error err ->
      Util.warning
        ("Could not read the file " ^ file ^ ", got error Sys_error " ^ err);
      raise(Sys_error err)

let positions_of_file f =
  let fstring = string_of_file f in
  let str_moves = Str.split (Str.regexp "[ \t\n]+") fstring in
  let curpos = ref init_position in
  let num = ref 0 in
  let allpos = ref [init_position] in
  let proc_one_move move_str =
    let next_move =
      match parse_move !curpos move_str with
      | Some mv -> mv
      | None -> raise (WrongMove ("In pos ["^move_str^"]"))
    in
    let next_pos = make_move !curpos next_move 0 in
    begin
      incr num;
      allpos := next_pos :: !allpos;
      curpos := next_pos
    end
  in
  begin
    List.iter proc_one_move str_moves;
    Util.warning ("Read " ^ (string_of_int !num) ^ " lines");
    List.rev (!allpos)
  end

let bitmaps_of_positions positions =
  List.map Util.string_of_position positions

let print_positions f positions =
  let bitmaps = bitmaps_of_positions positions in
  let oc = open_out f in
  List.iter (fun x -> output_string oc x; output_char oc '\n') bitmaps;
  close_out oc

let print_positions f positions =
  let bitmaps = bitmaps_of_positions positions in
  let oc = open_out f in
  List.iter (fun x -> output_string oc x; output_char oc '\n') bitmaps;
  close_out oc

let _ =
  begin
    let positions = positions_of_file "sample1.eye" in
    print_positions "sample1.bmp" positions
  end

