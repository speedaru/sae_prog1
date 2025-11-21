import libs.fltk as fltk
from libs.fltk import FltkEvent, PhotoImage, Anchor


# constants
FLTK_EVENT_EV_TYPE = 0
FLTK_EVENT_TK_EVENT = 1
FLTK_EVENT_COUNT = 2


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

@fltk._fenetre_cree
def image_memoire(
        x: float,
        y: float,
        tk_image: PhotoImage,
        ancrage: Anchor = "center",
        tag: str = "",
) -> int:
    """
    Affiche l'image ``tk_image`` avec ``(x, y)`` comme centre. Les
    valeurs possibles du point d'ancrage sont ``'center'``, ``'nw'``,
    etc. Les arguments optionnels ``largeur`` et ``hauteur`` permettent de
    spécifier des dimensions maximales pour l'image (sans changement de
    proportions).

    :param float x: abscisse du point d'ancrage
    :param float y: ordonnée du point d'ancrage
    :param PhotoImage tk_image: image que l'on souhait dessiner
    :param ancrage: position du point d'ancrage par rapport à l'image
    :param str tag: étiquette d'objet (défaut : pas d'étiquette)
    :return: identificateur d'objet
    """
    assert fltk.__canevas is not None
    img_object = fltk.__canevas.canvas.create_image(
        x, y, anchor=ancrage, image=tk_image, tags=tag
    )
    return img_object

def position_souris(ev: FltkEvent) -> tuple[int, int]:
    x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
    assert isinstance(x, int) and isinstance(y, int)
    return (x, y)
