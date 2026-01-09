# enum representing entity type
EntityE = int

# entity enums
E_ENTITY_UNKNOWN = 0xffff
E_ENTITY_ADVENTURER = 0
E_ENTITY_DRAGON = 1
E_ENTITY_TREASURE = 2
E_ENTITY_STRONG_SWORD = 3
E_ENTITY_COUNT = 4

# entities which are items
ENTITY_ITEMS = { E_ENTITY_STRONG_SWORD }

ENTITY_CHARS = { "A": E_ENTITY_ADVENTURER,
                "D": E_ENTITY_DRAGON,
                "S": E_ENTITY_STRONG_SWORD
                }
