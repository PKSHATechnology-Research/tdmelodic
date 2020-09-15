\version "2.18.2"
\pointAndClickOff

% Copyright (c) 2019-, Hideyuki Tachibana.
% All rights reserved.

"|" = {
  \once \override Staff.BarLine.bar-extent = #'(-1 . 1)
  \bar "|"
}

myColorNote = {   \once \override NoteHead.color = #(x11-color "medium turquoise") }
LS = { \once \override NoteColumn.X-offset = 5 } % little spacing
SP = {\hideNotes r8 \unHideNotes} % little spacing

% アクセント記号用のマクロ
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
\new Staff \with
{
instrumentName = \markup{}
}{\omit Staff.TimeSignature
    \stopStaff
        \override Staff.StaffSymbol.line-positions = #'(-2 2)
        \override Score.BarNumber #'transparent = ##t
    \startStaff

    \time 4/8
    g'8^[ d'' d''  d'' ]  \bar"||"
    \time 5/8
    g'8^[ d'' d''  g' g' ] \bar"||" \break
    \time 7/8
    g'8^[ d'' d'' d'' d'' d'' g' ] \bar"||"\break
    \time 10/8
    g'8^[ d'' d'' d'' d'' d'' d'' d'' g' g'] \bar"||"\break
    \time 3/8
    d''^[ g' g' ] \bar"||"
    \time 3/8
    g'^[ d'' d''] \bar"||"\\
    \time 6/8
    g'^[ d'' d'' d'' g' g' ] \bar"||"\break
    \time 3/8
    d''^[ g' g' ] \bar"||"
    \time 4/8
    g'^[ d'' d'' d''] \bar"||"\\
    \time 7/8
    g'^[ d'' d'' d'' g' g' g' ] \bar"||"
}
\addlyrics {
    \stopStaff
        \override Lyrics . LyricText #'font-name ="IPAex Mincho"
    \startStaff
    \age と う きょ う
    \age と う \sage きょ う と
    \age と う きょ う と \sage ち じ
    \age と う きょ う と ち じ \sage せ ん きょ
    \sage せ か い \age い さ ん
    \age せ か い \sage い さ ん
    \sage き か い \age が く しゅ う
    \age き か い \sage が く しゅ う
}

\layout {
  indent = 0\cm
}

\header {
  tagline = ""  % removed
}

% page size
#(set! paper-alist (cons '("my size" . (cons (* 4. in) (* 0.8 in))) paper-alist))

\paper {
    print-page-number = ##f % erase page numbering

    #(set-paper-size "my size")
    ragged-last-bottom = ##f
    ragged-bottom = ##f

    left-margin = 0
    right-margin = 0
}