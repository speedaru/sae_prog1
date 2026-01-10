GamePhaseE = int

# enum for sequential game phases
E_PHASE_INPUT         = 0     # process mouse/keyboard input events
E_PHASE_PRE_LOGIC     = 1     # pathfinding updates, and other game logic to do before recalculating path
E_PHASE_ADVENTURER    = 2     # moving the adventurer
E_PHASE_POST_ADVENTURER = 3   # check collisions after adventurer moves
E_PHASE_DRAGONS       = 4     # move dragons
E_PHASE_POST_DRAGONS  = 5     # check collisions again bcs dragons moved
E_PHASE_CLEANUP       = 6     # finish round / win-loss checks
E_PHASE_COUNT         = 7
