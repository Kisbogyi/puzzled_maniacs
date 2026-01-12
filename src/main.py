from sodoku import Sodoku
from solver import solve


def main():
    sodoku = Sodoku()
    sodoku.set_field(0,1, 9)
    print(sodoku)
    solved_sodoku = solve(sodoku)
    print(solved_sodoku)


if __name__ == "__main__":
    main()
