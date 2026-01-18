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
  ..data
)

#let type = read("sudoku.csv.typefile")
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
  row-gutter: 2cm,
  align: center,
  ..sudokus
)
