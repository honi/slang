    IF X1 != 0 GOTO A

    Z1 <- Z1 + 1
    IF Z1 != 0 GOTO B

[A] X1 <- X1 - 1
    Y <- Y + 1
    IF X1 != 0 GOTO A

[B] IF X2 != 0 GOTO C

    Z1 <- Z1 + 1
    IF Z1 != 0 GOTO D

[C] X2 <- X2 - 1
    Y <- Y + 1
    IF X2 != 0 GOTO C
