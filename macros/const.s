    Y <- 0

[A] IF X != 0 GOTO B
    GOTO C

[B] X <- X − 1
    Y <- Y + 1
    Z <- Z + 1
    GOTO A

[C] IF Z != 0 GOTO D
    GOTO E

[D] Z <- Z − 1
    X <- X + 1
    GOTO C
