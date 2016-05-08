open Types
type 'a t
type key = dmove
val empty : 'a t
val find : key -> 'a t -> 'a
val add : key -> 'a -> 'a list t -> 'a list t
