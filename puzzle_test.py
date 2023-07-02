import unittest
import puzzle

goal_state = [
    [None,1, 2], 
    [3, 4, 5], 
    [6, 7, 8]
    ]


class MyTest(unittest.TestCase):
    def test_my_function(self):
        state = [
            [7,2,4],
            [5,None,6],
            [8,3,1]
        ]
        result = puzzle.a_star(state)
        print("解のf値："+str(result.f_hat))
        self.assertEqual(result.f_hat, 26)

if __name__=="__main__":

    unittest.main()

"""

1 N 2
3 4 5
6 7 8

g=0
h=2
f=2

N 1 2
3 4 5
6 7 8

g=1
h=0
f=1




"""