(LOOP)
    @KBD
    D=M
    @KEY_PRESSED
    D;JNE

(KEY_RELEASED)
    @color
    M=0
    @INIT_BOX
    0;JMP

(KEY_PRESSED)
    @color
    M=-1

(INIT_BOX)
    @SCREEN
    D=A
    @1920        // 32 * 60 = 1920 (Offset for Row 60)
    D=D+A
    @addr
    M=D
    @20          // 20 rows tall
    D=A
    @rows
    M=D

(ROW_LOOP)
    @rows
    D=M
    @LOOP
    D;JEQ

    @color
    D=M
    @addr
    A=M
    M=D          // Writes 1 word (16 pixels wide)

    @32          // Advance to next row
    D=A
    @addr
    M=D+M
    @rows
    M=M-1
    @ROW_LOOP
    0;JMP