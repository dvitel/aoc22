open System.IO

type cmd = Cd of string | Ls | Out of Map<string, int> 

let lines = File.ReadAllLines("d7.txt") |> Seq.toList 

let rec buildTree acc (lst: string list) =     
    match lst with 
    | l::t when l.StartsWith("$ cd ") -> 
        l.Substring("$ cd ".Length)
    | l::t when l.StartsWith("$ ls") -> 
        buildTree
        