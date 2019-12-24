import pytest
from day20.solution import sol1, sol2

INPUT_A = """\
         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       
"""

INPUT_B = """\
                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               
"""

INPUT_C = """\
                                 X       G         C   X       Y   U       J                                     
                                 V       W         H   J       A   Z       M                                     
  ###############################.#######.#########.###.#######.###.#######.###################################  
  #.#.....#...#.....#.#...#...#.#.......#...#.#.......#.#.........#.......#.#...#.#.#.....#...#.....#.........#  
  #.#.#######.#####.#.###.###.#.###.#####.###.#######.#.###.#############.#.#.#.#.#.#.#####.#######.###.###.#.#  
  #.#.#.#.#.#.#.#.....#...............#.....#.........#.#...#.......#.....#...#...#.#.......#...#.#.#...#...#.#  
  #.#.#.#.#.#.#.#.###.###.###.#.#.###.###.###.#.#######.###.#.###.#######.#######.#.#.#######.###.#.#######.###  
  #...........#.#.#...#.#.#...#.#...#.#...#.#.#.#.........#.....#.....#...#.....#.....#.........#...#.#.....#.#  
  #.#.#########.#####.#.#####.#######.###.#.###.#####.#.#########.#######.###.#.#.###.#.#######.###.#.###.#.#.#  
  #.#.#...#.....#.#.#.#.#.....#.......#.#.#.#.......#.#...#...........#.#.#...#.....#.......#.#.#.......#.#.#.#  
  ###.#.###.###.#.#.#.#.#####.###.###.#.#.#.#####.#####.#.#.#.###.#####.#.#.#####.###.#######.#####.#.#####.#.#  
  #.....#.#.#.#.................#...#...#.#.#.......#...#.#.#.#...#.......#.....#.#...............#.#.#.#.#...#  
  #####.#.###.#####.###.#.#######.#####.#.#.###.###.#####.#.#.###.#####.###.###.#####.#.###.#.#.#####.#.#.#.###  
  #...#.....#...#.....#.#...#.#.....#...#...#.#...#...#...#.#.#...#.#.....#...#.....#.#.#.#.#.#.#...#...#.....#  
  #.#.###.###.#####.#########.#########.###.#.###.###.###.#.#######.#####.#.#####.#.#.###.#########.###.###.#.#  
  #.#.#.........#.#.#.....#.#.#...#...#.#...#.......#.#.#.#.....#.#...#...#.#...#.#.#.#.........#.......#.#.#.#  
  #.#####.#.#####.#####.###.#.#.###.###.#.#####.###.###.#.#.###.#.#.#####.#.###.#######.###########.###.#.#.###  
  #.....#.#...#.#.#.#.#.....#...#...#...#...#.....#...#...#.#.#.#.......#.#.....#.....#...#.#.#.#.....#.......#  
  #####.#.#####.#.#.#.#.###.###.###.###.###.#####.#####.###.#.#####.#.#.#.###.#.#.#####.###.#.#.###########.###  
  #.#.........#...#.....#...........#.#.#...#.#.......#...#.......#.#.#.....#.#.....#.#.#.....#...#.#.#.#.#...#  
  #.###.###.#####.#######.#######.###.#.#.###.#.#########.###.#.#####.###########.###.#.#.#####.###.#.#.#.#.###  
  #...#.#...#.......#.#.#.#.#.#.......#.#.#...#...#.......#.#.#...#...#...#...#.........#.#.....#.....#.#.#.#.#  
  #.#.#####.###.###.#.#.###.#.###.###.#.#.#.#.#.#########.#.###.#.###.#.###.#####.#.###.#.#####.###.###.#.#.#.#  
  #.#.....#.......#.#.............#.#...#.#.#.#.#.#...#...#.#...#.#.........#.....#.#.....#.#.......#...#.....#  
  #.#.#######.###################.#.#####.#.#.#.#.#.###.#.#.#.###.#######.#.#.#.#######.###.#.#.#.###.#####.###  
  #.#...#.#.#.#.#.#...#.....#...........#...#.#.......#.#.#.#.#.#...#...#.#.#.#.......#.#...#.#.#.#.#...#.....#  
  ###.###.#.#.#.#.#.#####.###########.#.#####.#####.#####.#.###.#.#.###.#.#####.###.#####.#.#.#####.#.###.#.###  
  #.....#.#.#.#.....#...#...#.........#.#.....#.......#.....#.....#.#.....#.......#.#.....#...#.......#.#.#...#  
  ###.###.#.#.###.#####.#.#######.#######.#########.#####.#####.#####.#########.###########.#.#####.###.###.###  
  #...#.#...........#.....#.#    G       P         G     Y     T     X         O    #...#.#.#...#...#.#.....#.#  
  ###.#.#####.#####.#.#####.#    Z       Z         P     A     L     J         F    ###.#.###.#####.#.#####.#.#  
  #.....#.#.#.#.#.......#.#.#                                                       #..........................AA
  ###.###.#.###.###.#.###.#.#                                                       #####.###.#######.###.#.#.#  
  #.#...#.....#...#.#.....#.#                                                       #.#...#.#...#.#...#...#.#..AH
  #.#.#####.###.###.###.###.#                                                       #.###.#.#.###.###########.#  
SD....#.......#.......#.#.#..QE                                                   JM....#...#.....#.#...#.....#  
  #.###.#.#.#####.#####.#.#.#                                                       #.#####.#######.#.#.###.#.#  
  #.....#.#.......#.#.......#                                                       #.........#.#.#...#.#...#.#  
  #.###.###########.#########                                                       ###########.#.###.#########  
  #.#.#.#...............#...#                                                       #.......#.#...........#...#  
  ###.###.#.#####.#.###.#.#.#                                                       #.#####.#.#.#.#.###.###.#.#  
  #...#.#.#...#.#.#.#.....#.#                                                       #...#.......#.#.#.....#.#.#  
  ###.#.#####.#.#.###.###.#.#                                                       #.#####.###.#######.#.#.#.#  
XG....#...#...#.#.#.....#.#.#                                                     GW....#...#...#.#.....#.#.#..KB
  ###.#.###.###.#####.###.#.#                                                       ###########.#.###.###.#.#.#  
  #...........#.#.....#.#.#..DP                                                     #.#.....#.#.#.....#.....#.#  
  #############.#######.###.#                                                       #.###.###.#####.#########.#  
  #.#.#.#.........#.....#...#                                                       #...#...#...#...#.......#.#  
  #.#.#.###.#.###.###.#######                                                       #.###.#.###.#######.###.###  
RC......#...#.#.#.#...#.#...#                                                     AH....#.#.#.#.#...#.....#...#  
  #.###.###.#.#.###.#.#.#.###                                                       #.###.###.#.###.###.###.###  
PO....#.....#.#...#.#.#.#....TI                                                     #.....#.#...#.#...#...#....IU
  #.###.#####.#.#.#.#.#.###.#                                                       #####.#.###.#.###.#.###.###  
  #.#...#.......#...#........KB                                                     #...#.................#.#.#  
  #.###.#.###.###.###########                                                       ###.###################.#.#  
  #.#.#.#.#.#...#...#.......#                                                       #...........#.#.......#.#..CL
  ###.#####.###########.###.#                                                       #.#######.#.#.#.#.###.###.#  
  #...#.#.....#.#.#.....#...#                                                       #...#...#.#.....#...#.#.#.#  
  ###.#.#####.#.#.#.#.#####.#                                                       ###.#.#.###.#.#.#.###.#.#.#  
  #.#.....#.......#.#.#...#..IU                                                     #.#...#.#.#.#.#.#.#.......#  
  #.#.#####.#.#.#.###.###.###                                                       #.###.###.#####.###.#####.#  
PZ..........#.#.#.....#...#.#                                                     NH..........#...#.#.....#...#  
  #####.#.#.#.###.#.#####.#.#                                                       #######.###.#####.#.#######  
  #.#.#.#.#.#.#.#.#.#.#.....#                                                     SD....#.#.#.....#...#.#.#....TL
  #.#.#####.###.#####.#.#.#.#                                                       #.###.#####.###.#####.###.#  
GZ..#.....#...#...#.....#.#..FH                                                     #...#.#...#.#.#.#.#.#.....#  
  #.#.#########.###.#####.###                                                       #.###.###.#.#.###.#.#####.#  
  #.#.#...#...#.#...#.......#                                                       #.#...#.....#.#.......#...#  
  #.#.###.###.#.#.#.#####.###                                                       #.#.#.#.###.#.#.###.#####.#  
  #...............#...#.#.#.#                                                       #...#...#.......#.#.......#  
  #########.#.#.#.#####.###.#                                                       #####.#.###.#.#.#.#.#.#####  
OF........#.#.#.#...#.#.#...#                                                     EJ....#.#.#...#.#.#...#.#...#  
  #####.###.#########.#.###.#                                                       #.#########.###.#.#.#####.#  
  #.......#.#................RC                                                     #.#.....#.#.#.#.#.#.#...#.#  
  #.#######.#####.#.#######.#                                                       #.###.###.###.#########.#.#  
  #.#.....#.#.#.#.#.......#.#                                                       #.#.......#.#.....#...#....NH
  #.#.#.#####.#.#########.###                                                       #.#.###.###.###.#.###.#.#.#  
  #...#.....................#                                                       #...#...........#.......#.#  
  #.#.###.###.#####.#.#.#.#.#        X       U       P       E C         C   X      #.#####.###.#####.###.#.#.#  
  #.#.#.....#.....#.#.#.#.#.#        V       Z       O       Z H         L   G      #...#.#.#.....#...#...#.#.#  
  #######.#####.###.#.###.#.#########.#######.#######.#######.#.#########.###.#######.###.#####.###.#.#.#####.#  
  #.#.#.......#.#.#.#...#.#...#...........#...#.......#.......#...#...#.#...#.#...#.#.......#.....#.#.#.....#.#  
  #.#.#.###.#####.###.#######.###.#########.###.#######.#.###.###.#.###.#.#.#.#.###.#.###.###.###.#####.#######  
  #.....#.....#.........#...#.#.....#.#...#.#.#.....#...#.#...#.#...#.#...#.#.......#.#.#.#.....#...#.........#  
  #.###.###.#######.#.#####.###.#.###.#.###.#.###.###.#.#######.#.#.#.#.#####.#.#.###.#.#.#####.#####.#.###.#.#  
  #...#.#.........#.#.#.........#.........#...#.....#.#.#.........#.#.......#.#.#.#.....#...#...#.....#.#...#.#  
  #.#####.###.#.#####.#######.#########.###.#.#.###.###.###.###.#####.###.#####.#####.###.#######.#.###.###.###  
  #...#.....#.#.#...#.#...#.#.#.........#.#.#.#.#.#...#.#.#.#...#.#.....#...#.#.#.#...#.....#.....#.#...#...#.#  
  #.#########.#####.###.###.#####.#####.#.###.#.#.#.#.#.#.#####.#.#.#########.#.#.#######.###.###.###.#.#.###.#  
  #.....#.......#.#.#...#.........#.......#...#.#.#.#.#...#.#...#.......#.#.#.......#...#...#.#.#.#...#.#.....#  
  #.###.#.#.#.###.#.###.#.#######.#####.#.###.#.#.#####.###.###.#####.###.#.###.###.###.###.###.#.###.###.#.#.#  
  #...#.#.#.#...#.........#.#.......#...#.#...#.#.#.#.#.....#.#...#.....#.........#.#.#.#.#.#.#...#...#...#.#.#  
  #.#####.###.#.###.#######.#####.#.###.#####.#.#.#.#.#.#.#.#.###.#.#########.#######.#.#.###.#.#######.#####.#  
  #...#.....#.#...#.#.....#...#...#.#...#.....#...#...#.#.#.#...#.#.#...#...................#.#.......#.....#.#  
  #.#.###.#.###.#########.#.###.#.#####.#.###.#.###.#.#.#.#####.#.#.#.#####.###.###.#####.#.#.#####.###.#.#####  
  #.#.#...#...#.#...#...#.......#.#...#.#.#...#.#.#.#...#.#.#.#...#.......#...#.#.......#.#.....#...#...#.#.#.#  
  #.###.#.###.#.#.#####.#########.#.#######.#.#.#.#####.###.#.###.#.#.#.#####.#.###.#####.#.###.#.#.#.###.#.#.#  
  #...#.#.#...#.#.......#...............#...#.#.....#.......#.#...#.#.#...#.#.#.#.#.#.#...#.#...#.#.#.#.#.....#  
  #.###################.#####.#.#.#.###.###.#######.#####.###.###.#.###.###.###.#.###.#############.###.#.#.#.#  
  #.......#.....#.............#.#.#...#.#.....#.......#.#...#.#...#.#.#...#.#...#...#...........#.....#...#.#.#  
  #########.###.#######.#.###.#.#.#######.###.#.#######.#.###.#.#.#.#.#.#.#.###.#.###.#.#.###.#.###.###.#.#.#.#  
  #.#.#...#.#.#.......#.#.#.#.#.#.....#...#.#.#.......#.......#.#.#...#.#.#...........#.#...#.#...#.#...#.#.#.#  
  #.#.###.###.#.#####.#####.#####.#########.#.#####.###.#.###.###.#.#######.#######.#######.#.#########.#.###.#  
  #.........#.....#.....#...#...........#...#.#.......#.#.#...#...#...#...........#.......#.#.#...#.....#.#...#  
  #######.#####.#######.###.#####.#########.#.#.#.###.#.#####.###.#.###.###.###.###.###.#####.#.###.#.#.#.#.#.#  
  #.............#.......................#.....#.#...#.#.#.......#.#...#.#...#.....#...#...#.......#.#.#.#.#.#.#  
  #################################.###.#.#####.###########.#####.#.#########.#################################  
                                   Z   E F     D           G     T E         Q                                   
                                   Z   J H     P           P     I Z         E                                   
"""


INPUT_D = """\
             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     
"""

@pytest.mark.parametrize('data, expected',
                         (
                            (INPUT_A, 23),
                            (INPUT_B, 58),
                            (INPUT_C, 100)
                          )
)
def test_1(data, expected):
    assert sol1(data) == expected


@pytest.mark.parametrize('data, expected',
                         (
                                 # (INPUT_D, 396),
                                 (INPUT_C, 100),
                         )
)
def test_2(data, expected):
    assert sol2(data) == expected


if __name__ == '__main__':
    pytest.main()
