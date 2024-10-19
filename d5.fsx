let s1 = """N
W
F
R
Z
S
M
D"""

let s2 = """S
G
Q
P
W"""

let s3 = """C
J
N
F
Q
V
R
W"""

let s4 = """L
D
G
C
P
Z
F"""

let s5 = """S
P
T"""

let s6 = """L
R
W
F
D
H"""

let s7 = """C
D
N
Z"""

let s8 = """Q
J
S
V
F
R
N
W"""

let s9 = """V
W
Z
G
S
M
R"""

let t1 = """N
Z"""
let t2 = """D
C
M"""

let t3 = """P"""

let s = [|s1;s2;s3;s4;s5;s6;s7;s8;s9|] |> Array.map(fun x -> x.Split('\n') |> Seq.toList)
let s = [|t1;t2;t3|] |> Array.map(fun x -> x.Split('\n') |> Seq.toList)
open System.Text.RegularExpressions
let r = Regex("move (?<cnt>\d+) from (?<from>\d+) to (?<to>\d+)")
let mvs = 
    System.IO.File.ReadAllLines("d5m.txt") 
    |> Seq.map(fun l -> 
        let m = r.Match(l)
        (int m.Groups.["from"].Value - 1, int m.Groups.["to"].Value - 1, int m.Groups.["cnt"].Value))
        |> Seq.toList

mvs |> Seq.fold(fun acc (froms, tos, cnt) -> 
    let rec pickAndPut (acc: _ list []) cnt = 
        match cnt with 
        | 0 -> acc 
        | _ -> 
            match acc.[froms] with 
            | h::t -> 
                acc.[froms] <- t 
                acc.[tos] <- h::acc.[tos]
                pickAndPut acc (cnt - 1)
            | _ -> acc
    let acc = pickAndPut acc cnt
    acc
    ) s
|> Seq.map(fun a -> a.[0]) |> fun s -> System.String.Join("", s)

mvs |> Seq.fold(fun (acc: _ list []) (froms, tos, cnt) -> 
    let took = acc.[froms].[0..cnt-1]
    acc.[froms] <- acc.[froms].[cnt..]
    acc.[tos] <- took @ acc.[tos]
    acc
    ) s
|> Seq.map(fun a -> a.[0]) |> fun s -> System.String.Join("", s)

