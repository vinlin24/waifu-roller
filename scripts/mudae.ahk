#NoEnv ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir% ; Ensures a consistent starting directory.

#SingleInstance, Force
SetTitleMatchMode, 2

DefaultNumRolls := 15 ; Change as needed.
DefaultRollString := "$wa" ; Change as needed.
DefaultRollDelay := 1 ; Change as needed (in seconds).

#IfWinActive, - Discord

    ; Mudae rolling sequence.
    ^+4::
        AbortSequence := false

        InputBox
        , UserInput
        , Roll Configuration ([num rolls] [roll string] [roll delay in seconds] [use $rolls?])
        , (Default "%DefaultNumRolls% %DefaultRollString% %DefaultRollDelay%")
        , , , , ,
        , %DefaultNumRolls%

        if (ErrorLevel = 1) ; Canceled
            return

        UserInputs := StrSplit(UserInput, A_Space)
        NumRolls := UserInputs[1]
        RollString := UserInputs[2]
        RollDelay := UserInputs[3]
        RefreshRolls := UserInputs[4]

        ; Validate and assign defaults.
        if (NumRolls = "" or !(NumRolls is number))
            NumRolls := DefaultNumRolls
        if (RollString = "")
            RollString := DefaultRollString
        if (RollDelay = "" or !(RollDelay is number))
            RollDelay := DefaultRollDelay
        RollDelay := RollDelay * 1000 ; ms -> s
        if (RefreshRolls = "")
            RefreshRolls := False
        else
            RefreshRolls := True

        SendInput $p {Enter}
        Sleep %RollDelay%
        Loop, %NumRolls% {
            if (AbortSequence)
                return
            SendInput %RollString% {Enter}
            Sleep %RollDelay%
        }
        if (RefreshRolls) {
            if (AbortSequence)
                return
            SendInput $rolls {Enter}
            Sleep %RollDelay%
            Loop, %NumRolls% {
                if (AbortSequence)
                    return
                SendInput %RollString% {Enter}
                Sleep %RollDelay%
            }
        }
    return

    ; Abort sequence.
    ^q::
        AbortSequence := true
    return

#IfWinActive
