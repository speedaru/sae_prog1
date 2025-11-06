import libs.fltk as fltk


def fenetre_titre(nouveau_titre: str) -> None:
    """
    Change le titre de la fenêtre actuelle.

    :param str nouveau_titre: spécifie le nouveau titre de la fenêtre
    """
    global __canevas
    fltk.__canevas.root.title(nouveau_titre)

def fenetre_icone(fichier_ico: str) -> None:
    """
    Change l'icone de la fenêtre.

    :param str fichier_ico: l'emplacement (relatif ou absolue) du fichier .ico
    """
    global __canevas
    fltk.__canevas.root.iconbitmap(fichier_ico)
