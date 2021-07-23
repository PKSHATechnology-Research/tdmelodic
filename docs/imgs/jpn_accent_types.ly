\version "2.18.2"
\pointAndClickOff

% Copyright (c) 2020-, Hideyuki Tachibana.
% All rights reserved.

"|" = {
  \once \override Staff.BarLine.bar-extent = #'(-1 . 1)
  \bar "|"
}

SP = {\hideNotes d''8 \unHideNotes} % little spacing

% note: it converts a command as follows
%     \age xyz
% ->
%     \markup { xyz \with-color " red "[" }
age=#(define-music-function
  (parser location argtext)
  (markup?)
  #{
    \lyricmode{
        \markup{ #argtext \with-color #red "[" }
    }
  #}
)

sage=#(define-music-function
  (parser location argtext)
  (markup?)
  #{
    \lyricmode{
      \markup{ #argtext \with-color #blue "]" }
    }
  #}
)


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\header {
  subtitle = \markup{\fontsize #1 "Six accent patterns of five-mora words"}
}

\new Staff \with
{
instrumentName = \markup{}
}{
    \omit Staff.TimeSignature
    \textLengthOff
    \stopStaff
        \override Staff.StaffSymbol.line-positions = #'(-2 2)
        \override Score.BarNumber #'transparent = ##t
    \startStaff

    \time 6/8
    g'8^[^\markup{type 0 }
        d'' d'' d'' d'' ] d''  \bar"||"
    d''8^[^\markup{type 1 }
        g' g' g' g' ] g' \bar"||"
    g'8^[^\markup{type 2 }
        d'' g' g' g' ] g' \bar"||"
    g'8^[^\markup{type 3 }
        d'' d'' g' g' ] g' \bar"||"
    g'8^[^\markup{type 4 }
        d'' d'' d'' g' ] g' \bar"||"
    g'8^[^\markup{type 5 }
        d'' d'' d'' d'' ] g' \bar"||"

}
\addlyrics {
    \stopStaff
        \override Lyrics . LyricText #'font-name ="Times"
    \startStaff

    \age "*" "*" "*" "*" "*" ga
    \sage "*" "*" "*" "*" "*" ga
    \age "*" \sage "*" "*" "*" "*" ga
    \age "*" "*" \sage"*" "*" "*" ga
    \age "*" "*" "*" \sage "*" "*" ga
    \age "*" "*" "*" "*" \sage "*" ga
    \age "*" "*" "*" "*" "*" \sage ga
}

\layout {
  indent = 0\cm
}

\header {
  tagline = ""  % removed
}

% page size
#(set! paper-alist (cons '("my size" . (cons (* 5. in) (* 2.2 in))) paper-alist))

\paper {
    print-page-number = ##f % erase page numbering

    #(set-paper-size "my size")
    ragged-last-bottom = ##f
    ragged-bottom = ##f

    left-margin = 0
    right-margin = 0
}