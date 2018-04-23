def assignGoals(sim, goals):
    
    blocks = sim.to_list()
    for block in blocks:
        if block[3] == 'd':
            blocks.remove(block)
    
    colorGoals = [goal for goal in goals if goal[3] != '?']
    wildGoals = [goal for goal in goals if goal[3] == '?']
    
    goalToBlock = {}
    
    for goal in colorGoals:
        for block in blocks:
            if block[3] == goal[3]:
                goalToBlock[block] = goal
                break
        blocks.remove(block)
        
    for goal in wildGoals:
        for block in blocks:
            goalToBlock[block] = goal
            break
        blocks.remove(block)
        
    print(goalToBlock)
        
    return goalToBlock