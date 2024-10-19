open System.IO 

let process () = 
    File.ReadAllLines("d4.txt")
    |> Seq.map(fun line ->         
        let range (a: string) = let [| s; e |] = a.Split('-') in (int s, int e)
        let [| a; b |] = line.Split(',') in range a, range b)

process() 
|> Seq.filter(fun ((s1, s2), (s3, s4)) -> (s1 <= s3 && s2 >= s4) || (s3 <= s1 && s4 >= s2))
|> Seq.length    

process()
|> Seq.filter(fun ((s1, s2), (s3, s4)) -> 
    (s1 <= s3 && s3 <= s2) || (s1 <= s4 && s4 <= s2) || (s3 <= s1 && s1 <= s4) || (s3 <= s2 && s2 <= s4))
|> Seq.length   