#set page(paper: "a4", flipped: false)
#set text(font: "IBM Plex Serif")
#show heading: set align(center)
= SUDOKU


#let default = 0.5pt
#let thick = 1pt
#let border = 1.5pt

#let results = csv("sudoku.csv")
#align(center)[
#table(
  align: center,
  rows: (0.6cm),
  columns: (0.6cm,0.6cm,0.6cm,0.6cm,0.6cm,0.6cm,0.6cm,0.6cm,0.6cm),
  stroke: (x, y) => {
    if (y == 0 ) {(
      top: border,
      bottom: default
    )} else if y == 8 {(
      bottom: border
    )} else if calc.rem(y, 3) == 2 {(
      bottom: thick
    )} else {(
      bottom: default,
    )}
    if (x == 0 ) {(
      left: border,
      right: default
    )} else if x == 8 {(
      right: border
    )} else if calc.rem(x, 3) == 2 {(
      right: thick
    )} else {(
      right: default
    )}
  },
  ..results.flatten()
)]
