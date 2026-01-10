# enum representing entity type
EntityE = int

# entity enums
E_ENTITY_UNKNOWN = 0xffff
E_ENTITY_ADVENTURER = 0
E_ENTITY_DRAGON = 1
E_ENTITY_TREASURE = 2
E_ENTITY_STRONG_SWORD = 3
E_ENTITY_CHAOS_SEAL = 4
E_ENTITY_COUNT = 5


# entities which are items that are isntantly consumed
ENTITY_ITEMS_INSTACONSUME = { E_ENTITY_TREASURE, E_ENTITY_CHAOS_SEAL }

# entities which are items
ENTITY_ITEMS = ENTITY_ITEMS_INSTACONSUME.union({ E_ENTITY_STRONG_SWORD })


ENTITY_CHARS = { "A": E_ENTITY_ADVENTURER,
                "D": E_ENTITY_DRAGON,
                "S": E_ENTITY_STRONG_SWORD,
                "CS": E_ENTITY_CHAOS_SEAL
                }
