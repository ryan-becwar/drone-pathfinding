import time

cases = ["simple", "pillar"]
def testAlgorithm(algo):
    
    print("Testing algorithm: ", algo)
    for case in cases:
        sim = s.Simulator.from_file("gamestates/" + case)
        
        start_time = time.time()
        result = algo(sim)
        elapsed = time.time()
        
        print("\nStage: ", case)
        print("Elapsed Time: ", elapsed)
        print("Solution Length: ", len(result))