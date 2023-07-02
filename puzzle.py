import random
import copy
import heapq
import time

random.seed(314) 

state_x,state_y = 3,3
goal_state = [
    [None,1, 2], 
    [3, 4, 5], 
    [6, 7, 8]
    ]



class Node:
    parent = None
    state = None
    empty_location_x = None
    empty_location_y = None
    g_hat = None
    h_hat = None

    def __init__(self,state,parent=None):

        self.parent = parent
        self.state = state
        self.h_hat = self.get_h_hat()
        if parent:

            self.g_hat = parent.g_hat+1
        else:
            self.g_hat = 0
        self.f_hat = self.h_hat + self.g_hat

        for i_y,i in enumerate(state):
            for j_x,j in enumerate(i):
                if j==None:
                    self.empty_location_x = j_x
                    self.empty_location_y = i_y

    def __lt__(self,other):
        return True

    def __gt__(self,other):
        return True

    def show(self):
        for i in range(state_y):
            for j in range(state_x):
                print(self.state[i][j], end=' ')
            print()
        print()
    def show_score(self):
        print("--------------")
        print("g_hat:" + str(self.g_hat))
        print("h_hat:" + str(self.h_hat))
        print("f_hat:" + str(self.f_hat))
        
    def get_h_hat(self):

        manhattan_distance = 0
        for y,row in enumerate(self.state):
            for x, item in enumerate(row):
                for g_y,g_row in enumerate(goal_state):
                    for g_x, g_item in enumerate(g_row):
                        if not(item is None )and item==g_item :
                            manhattan_distance = abs(x-g_x) + abs(y-g_y) + manhattan_distance
                            
        
        return manhattan_distance


    def generate_children(self):

        children = []

        directions_x_y = [
            [-1,0],
            [ 1,0],
            [ 0,1],
            [ 0,-1],
        ]


        for i in directions_x_y:
            destination_x,destination_y = self.empty_location_x+i[0],self.empty_location_y+i[1]
            if not(0<=destination_x<=2 and 0<=destination_y<=2):
                continue
            
            child_state = copy.deepcopy(self.state)
            child_state[self.empty_location_y][self.empty_location_x] = self.state[destination_y][destination_x]
            child_state[destination_y][destination_x] = None
            child = Node(child_state,self) 
            children.append(child)


        return children

 

    def is_equal(self,target):
        return self.state == target.state

    def where(self,node_list):
        for ind,i in enumerate(node_list):
            if self.is_equal(i):
                return ind
        return -1
    def is_in(self,node_list):
        for i in node_list:
            if self.is_equal(i):
                return True
        return False
    def node_index(self,node_list):
        for ind,i in enumerate(node_list):
            if self.is_equal(i):
                return ind
        
        raise ValueError("指定の要素が配列に存在するような実装になっていることを確認してください。")


    def where_heap(self,node_list):
        for ind,i in enumerate(node_list):
            if self.is_equal(i[1]):
                return ind
        return -1



    def is_in_heap(self,node_list):
        for i in node_list:
            if self.is_equal(i[1]):
                return True
        return False
    def node_index_heap(self,node_list):
        for ind,i in enumerate(node_list):
            if self.is_equal(i[1]):
                return ind
        
        raise ValueError("指定の要素が配列に存在するような実装になっていることを確認してください。")


    


def a_star(puzzle):
    goal_node = Node(goal_state)
    parent = Node(puzzle)


    print("------問題------")
    parent.show()

    open_list = []
    closed_list = []

    heapq.heappush(open_list, (parent.f_hat,parent))


    while open_list:
        
        _,head = heapq.heappop(open_list)

        if head.is_equal(goal_node):
            answer = head
            break

        children = head.generate_children()



        for i in children:

            if not(i.is_in_heap(open_list)) and not(i.is_in(closed_list)):

                heapq.heappush(open_list, (i.f_hat,i))
                
            elif i.is_in_heap(open_list):
                ind = i.node_index_heap(open_list)
                if open_list[ind][1].f_hat > i.f_hat:

                    open_list.pop(ind)
                    heapq.heapify(open_list)
                    heapq.heappush(open_list, (i.f_hat,i))
                
            elif i.is_in(closed_list):
                ind = i.node_index(closed_list)
                if closed_list[ind].f_hat > i.f_hat:
            
                    # closed_list.pop(ind)
                    # heapq.heappush(open_list, (i.f_hat,i))


                    raise ValueError("ヒューリスティック関数に矛盾性があるかもしれません")

        

        closed_list.append(head)
    
    print("------探索完了-------")

    print("経路コスト：" + str(answer.g_hat))
    
    print()


    return answer


def main():

    answer = None

    # 100個の初期状態を生成
    puzzles = [generate_random_puzzle(move_count) for move_count in range(1, 101)]



    for ind,puzzle in enumerate(puzzles):
        
        print("-----何問目：" + str(ind) + "-----")
        a_star(puzzle)






    
def generate_random_puzzle(move_count):
    
    puzzle = copy.deepcopy(goal_state)

    # 空タイルを指定した回数ランダムに移動させる
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # 右、左、下、上に移動するための座標の変化量
    for _ in range(move_count):
        possible_moves = []
        empty_row, empty_col = None, None

        # 空タイルの位置を検索
        for i in range(3):
            for j in range(3):
                if puzzle[i][j] is None:
                    empty_row, empty_col = i, j
                    break

        # 空タイルの周囲に移動可能なタイルの位置を取得
        for dx, dy in moves:
            new_row, new_col = empty_row + dx, empty_col + dy
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                possible_moves.append((new_row, new_col))

        # ランダムに移動先を選択して空タイルを移動させる
        new_row, new_col = random.choice(possible_moves)
        puzzle[empty_row][empty_col] = puzzle[new_row][new_col]
        puzzle[new_row][new_col] = None

    return puzzle


if __name__=="__main__":
    main()