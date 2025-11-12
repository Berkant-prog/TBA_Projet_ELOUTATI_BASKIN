# test.py
# Tests très simples (manuels) pour vérifier que les modules se chargent.

from game import Game

def test_boot():
    g = Game()
    g.start_game()
    assert g.player is not None
    assert g.rooms
    print("Boot OK.")

if __name__ == "__main__":
    test_boot()
    print("Tests de base passés.")

