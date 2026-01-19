#set page(paper: "a4", flipped: false)
#set text(font: "IBM Plex Serif")
#show heading: set text(font: "Metal Mania", size: 24pt)
#show heading: set align(center) 
#show heading: set block(below: 1em)


#let default = 0.5pt
#let thick = 1.2pt
#let border = 2pt

#let results = csv("sudoku.csv")
#let sudokus = results.map(data => [
= KRAZY SUDOKU
#let type = read("sudoku.csv.typefile")
#table(
  align: center,
  rows: (0.6cm),
  columns: (0.6cm,0.6cm,0.6cm,0.6cm,0.6cm,0.6cm,0.6cm,0.6cm,0.6cm),
  fill: (x, y) => {
    if type.contains("Windoku") {
      // topleft
      if (x > 0 and y > 0 and x < 4 and y < 4) or (x > 4 and y > 0 and x < 8 and y < 4) or (x > 0 and y > 4 and x < 4 and y < 8) or (x > 4 and y > 4 and x < 8 and y < 8) { luma(211) }
    } else if type.contains("Center") {
      if calc.rem(x, 3) == 1 and calc.rem(y, 3) == 1 { luma(211) }
    } else { white }
  },
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
  ..data
)

*Type*:
#if type.contains("Classic") {[
  Classic
]}
#if type.contains("Windoku") {[ 
  Windoku (there are four additional coloured 3x3 squares that must also be filled with only unique digits.)
] } else if type.contains("AntiKnight") {[
  Anti-Knight (each number in a square should also consider the move that a knight could make in a game of Chess.)
] } else if type.contains("Nonconsecutive") {[
  Nonconsecutive (no two horizontally or vertically adjacent numbers can be consecutive.)
]} else if type.contains("Center") {[
  Center Dot (each traditional 3x3 square has a coloured middle square that must also all have unique values.)
]}

*Difficulty*:
#if type.contains("EASY") {[ 
  Easy
] } else if type.contains("MEDIUM") {[
  Medium
] } else if type.contains("HARD") {[
  Hard
]} else if type.contains("EXPERT") {[
  Expert
]}
])


#grid(
  columns: (1fr, 1fr),
  rows: (auto, auto),
  gutter: 4cm,
  row-gutter: 4cm,
  align: center,
  ..sudokus
)
