def assignGoals(blocks, goals):
    
    colorGoals = [goal for goal in goals if goal[3] != '?']
    wildGoals = [goal for goal in goals in goal[3] == '?']
    
    goalToBlock = []
    
    for goal in colorGoals:
        for block in blocks:
            if block[3] == goal[3]:
                goalBlock.append((goal, block))
                break
        blocks.remove(block)
        
    for goal in wildGoals:
        for block in blocks:
            goalBlock.append((goal, block))
            break
        blocks.remove(block)
        
    return goalToBlock