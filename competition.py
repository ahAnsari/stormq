import numpy as np
import networkx as nx
import tools
import actions
import run


def compete(graph: nx.Graph, q_table, ranges):
    opponent_action = 0

    counter = 0
    max_iteration = 20000000
    un_seen = 0

    while len(graph.graph['free']) > 1 and counter < max_iteration:
        state = tools.get_state(graph, ranges)

        # first player action
        action_choice1 = np.argmax(q_table[state, :])
        if np.sum(q_table[state, :]) == 0:
            un_seen += 1
            action_choice1 = np.random.randint(3)

        if action_choice1 == 0:
            seed1 = actions.action_degree(graph)
        elif action_choice1 == 1:
            seed1 = actions.action_weight(graph)
        elif action_choice1 == 2:
            seed1 = actions.action_blocking(graph, 1)
        # elif action_choice1 == 3:
        #     seed1 = actions.action_last(graph)
        # elif action_choice1 == 4:
        #     seed1 = actions.action_min_degree(graph)

        # illegal action
        if seed1 == -1:
            print("illegal 1")
            print(action_choice1)
            action_choice1 = 0
            seed1 = actions.action_degree(graph)

        tools.activate_node(graph, seed1, 1)

        # second player action
        action_choice2 = opponent_action
        if action_choice2 == 0:
            seed2 = actions.action_degree(graph)
        elif action_choice2 == 1:
            seed2 = actions.action_weight(graph)
        elif action_choice2 == 2:
            seed2 = actions.action_blocking(graph, 2)

        # illegal action
        if seed2 == -1:
            print("illegal 2")
            print(action_choice2)
            action_choice2 = 0
            seed2 = actions.action_degree(graph)
        tools.activate_node(graph, seed2, 2)

        a1, a2 = tools.diffuse(graph)
        for n in a1:
            tools.activate_node(graph, n, 1)
        for n in a2:
            tools.activate_node(graph, n, 2)

        counter += 1

    score = len(graph.graph['1']) - len(graph.graph['2'])
    print("counter: " + str(counter))
    print("unseen: " + str(un_seen))
    print("score: " + str(score))

    result = {"counter": counter, "un_seen": un_seen, "score": score}
    return result
