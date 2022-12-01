# macro: IF V = 0 GOTO L

    IF V != 0 GOTO E
    Z <- Z + 1
    IF Z != 0 GOTO L
[E] V <- V
