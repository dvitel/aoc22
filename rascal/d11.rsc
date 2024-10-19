module d11 

lexical NUM = [0-9]+;
layout LAYOUT = [\n\t\f\ ]* !>> [\n\t\f\ ];
start syntax MonkeyList = Monkey*;
syntax Expr = 
    "old"
    | NUM
    | Expr + Expr
    | Expr * Expr; 
syntax Monkey = 
    "Monkey" NUM id
    "Starting items:" NUM item1 "," NUM item2
    "Operation:" "new" "=" Expr
    "Test: divisible by" NUM divBy
    "If true: throw to monkey" NUM trueMonkey
    "If false: throw to monkey" NUM falseMonkey
    ;

int x = 42;

int f() = x;