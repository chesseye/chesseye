open Types
module M = Map.Make (struct
  type t = dmove
  let compare dmov1 dmov2 = Pervasives.compare dmov1 dmov2
end)

type 'a t = 'a M.t
type key = dmove

let empty = M.empty
let find = M.find
let add k v m =
  try
    let l = M.find k m in
    M.add k (v::l) m
  with Not_found -> M.add k (v::[]) m
