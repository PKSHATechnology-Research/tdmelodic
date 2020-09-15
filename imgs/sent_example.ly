\version "2.18.2"
\pointAndClickOff

% Copyright (c) 2019-, Hideyuki Tachibana.
% All rights reserved.

"|" = {
  \once \override Staff.BarLine.bar-extent = #'(-1 . 1)
  \bar "|"
}

myColorNote = {   \once \override NoteHead.color = #(x11-color "medium turquoise") }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\new Staff \with
{
instrumentName = \markup{}
}{\omit Staff.TimeSignature

    \stopStaff
        \override Staff.StaffSymbol.line-positions = #'(-3 0 3)
        \override Score.BarNumber #'transparent = ##t
    \startStaff

    \time 12/8
    b'8[ e'' \myColorNote e'' b' b'] b' b'[ \myColorNote b' f' f' f' ] f'
    \time 8/8
    f'8[ e'' e''] e'' \myColorNote e''[ b'] b' b'
    \time 9/8
    \myColorNote  b'8[ f'] \myColorNote  e''[ b' b'] b'[ b' b' b']
}
\addlyrics {
    \stopStaff
        \override Lyrics . LyricText #'font-name ="IPAex Mincho"
    \startStaff
    お や ゆ ず り の む て っ ぽ う で
    こ ど も の と き か ら
    そ ん ば か り し て い る
}

\layout {
  indent = 0\cm
}

\header {
  tagline = ""  % removed
}

% ページサイズ
#(set! paper-alist (cons '("my size" . (cons (* 8. in) (* 0.8 in))) paper-alist))

\paper {
    print-page-number = ##f % erase page numbering

    #(set-paper-size "my size")
    ragged-last-bottom = ##f
    ragged-bottom = ##f

    left-margin = 5
    right-margin = 5
}