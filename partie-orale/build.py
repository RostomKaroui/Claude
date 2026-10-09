"""Partie orale de Rostom, calée sur l'animation « Le montage, pas à pas ».
Lancer : python3 build.py  puis  NODE_PATH=$(npm root -g) node render.js  ->  partie-orale-rostom.pdf"""
import html, re

INTRO = ("Environ 3 minutes. On ouvre la page « Le montage, pas à pas » et on avance avec le bouton « Suivant → » "
         "(ou la flèche droite du clavier). Les distances s'affichent en haut de l'image : pas besoin de les lire. "
         "Si le temps presse, on dit les étapes 2 et 3 en une seule phrase.")

# (titre, ce qu'on voit / ce qu'on clique, [paragraphes parlés])  ; **gras** autorisé
ETAPES = [
 ("Le tangram", "À l'écran : le tangram posé sur la table.", [
  "Bonjour. Notre abri est construit avec un tangram de 15 cm, collé en double épaisseur pour que chaque pièce soit rigide. Je vais vous montrer comment il se monte. Chaque pièce bouge de trois façons seulement. Par **translation**, elle glisse. Par **rotation**, elle tourne à plat autour d'un coin. Par **pliage**, elle se relève autour d'un côté. Aucune pièce n'est prise pour être posée ailleurs : toutes avancent d'un mouvement continu.",
  "On part du tangram posé en losange, avec une diagonale dans l'axe est–ouest. Cet axe sera celui du cadrage de la vue vers le coucher du soleil."]),
 ("Le pli", "Clic sur Suivant. Les deux grands triangles se relèvent.", [
  "Premier geste, et le plus important : un pliage. Les deux grands triangles se relèvent de 30° autour de leur côté commun. Leurs pointes glissent vers le milieu, et la ligne de pli monte à environ 5 cm. Nous obtenons deux pentes, une vers le nord, une vers le sud. Cette ligne de pli devient l'axe de symétrie de toute la maquette.",
  "Pourquoi 30° ? Chaque pente fait 10,6 cm. À 30°, elle monte de la moitié : 5,3 cm. C'est exactement le côté du carré, et aussi la hauteur du parallélogramme et des petits triangles debout. Toutes les pièces debout vont donc se glisser pile sous le pli : toute la maquette tient sur une seule mesure."]),
 ("L'appui nord", "Clic sur Suivant. Le petit triangle vert.", [
  "Le petit triangle vert part en translation vers l'est, sous la pente : elle devient transparente pour qu'on le suive. Puis une petite translation vers le nord, et un pliage de 90° : il se relève autour de son petit côté. Debout, il devient l'appui nord de l'entrée."]),
 ("L'appui sud", "Clic sur Suivant. Le petit triangle bleu clair.", [
  "Le petit triangle bleu clair fait le même geste de l'autre côté de l'axe : c'est la symétrie. Il doit d'abord contourner le pied de la pente, donc un peu vers le sud. Puis il glisse vers l'est, revient vers le nord et se relève de 90°. C'est l'appui sud."]),
 ("Le toit de l'entrée", "Clic sur Suivant. Le triangle moyen.", [
  "Le triangle moyen monte tout droit, en translation vers le haut, jusqu'à la hauteur du pli. Puis il glisse vers l'est le long du pli, en s'appuyant dessus, jusqu'aux deux appuis. Il continue la ligne de pli à l'horizontale : c'est le toit de l'entrée."]),
 ("La paroi penchée", "Clic sur Suivant. Le parallélogramme.", [
  "Le parallélogramme fait trois mouvements. D'abord une rotation de 90°, à plat, autour de son coin. Ensuite un pliage de 90° : il se relève. Enfin une translation vers l'est, sous le pli. Penché, il tient le pli par en dessous et laisse un passage sous lui."]),
 ("La paroi de la vue", "Clic sur Suivant. Le carré.", [
  "Dernière pièce : le carré. Un pliage de 90° autour de son côté nord, puis une translation vers l'est, sous le pli. Debout dans l'axe, à l'ouest, il partage la vue en deux cadrages sur le coucher du soleil."]),
 ("Le résultat", "Clic sur Suivant, puis sur « Promenade ».", [
  "Voilà l'abri monté. Les sept pièces travaillent, aucune n'est posée à plat sur le sol, et chacune est arrivée par translation, rotation ou pliage. Les pentes s'appuient sur le carré et le parallélogramme, et le toit repose sur les deux appuis. Avec la double épaisseur de carton, l'ensemble est rigide.",
  "Les pièces qui sont sur l'axe, le carré, le parallélogramme et le toit, n'ont pas besoin de double : elles sont déjà au milieu. Les autres vont par deux : deux pentes, deux appuis.",
  "**Je passe la parole à Yassmine, qui va vous parler du cadrage de la vue et de la lumière.**"]),
]

QUESTIONS = [
 ("Pourquoi 30° et pas 45° ?", "À 45°, le pli monterait à 7,5 cm. Les pièces debout, qui mesurent 5,3 cm, ne le toucheraient plus."),
 ("Pourquoi le triangle moyen monte-t-il tout droit ?", "C'est la seule pièce qui finit en hauteur, à 5,3 cm du sol. Il monte d'abord à la hauteur du pli, puis il glisse dessus jusqu'à ses appuis."),
 ("Pourquoi ça tient ?", "Les pentes s'appuient sur le carré et le parallélogramme, le toit repose sur les deux appuis, et la double épaisseur rend chaque pièce rigide."),
]


def typo(s):
    s = s.replace("'", "\u2019")
    s = re.sub(r" ([:;!?»])", lambda m: ("\u00a0" if m.group(1) in ":»" else "\u202f") + m.group(1), s)
    s = re.sub(r"« ", "«\u00a0", s)
    s = re.sub(r"(\d) (cm|°)", "\\1\u00a0\\2", s)
    return s


def gras(s):
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html.escape(typo(s), quote=False))


def page():
    corps = ""
    for i, (titre, cue, paras) in enumerate(ETAPES):
        ps = "".join(f"<p>{gras(p)}</p>" for p in paras)
        corps += f'<section class="etape"><h2><span class="n">{i}</span>{gras(titre)}</h2><div class="cue">{gras(cue)}</div>{ps}</section>'
    qs = "".join(f"<li><b>{gras(q)}</b> {gras(r)}</li>" for q, r in QUESTIONS)
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Partie orale de Rostom</title>
<link rel="stylesheet" href="../planche-a3/fonts/fonts.css">
<style>
@page {{ size: A4; margin: 17mm 18mm 16mm; }}
:root {{ --encre: #1d2220; --gris: #5b625e; --trait: #2346a8; --ligne: #cfd2cc; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: "Source Serif 4", Georgia, serif; color: var(--encre); font-size: 14pt; line-height: 1.55; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.sur {{ font-family: "IBM Plex Mono", monospace; font-size: 8.5pt; letter-spacing: .08em; text-transform: uppercase; color: var(--gris); }}
h1 {{ font-family: "Archivo", sans-serif; font-stretch: 125%; font-weight: 800; font-size: 21pt; line-height: 1.05; margin: 2mm 0 3mm; }}
.intro {{ font-family: "IBM Plex Mono", monospace; font-size: 9.5pt; line-height: 1.5; color: var(--gris); border-left: 1mm solid var(--trait); padding-left: 4mm; margin-bottom: 7mm; }}
.etape {{ break-inside: avoid; margin-bottom: 6.5mm; padding-top: 2.5mm; border-top: .4mm solid var(--encre); }}
h2 {{ font-family: "Archivo", sans-serif; font-stretch: 112%; font-weight: 700; font-size: 15.5pt; line-height: 1.1; display: flex; gap: 4mm; align-items: baseline; }}
h2 .n {{ font-stretch: 62%; font-weight: 800; font-size: 25pt; color: var(--trait); line-height: .8; min-width: 7mm; }}
.cue {{ font-family: "IBM Plex Mono", monospace; font-size: 9.5pt; color: var(--trait); margin: 1.5mm 0 3mm 11mm; font-weight: 500; }}
.etape p {{ margin-bottom: 3mm; }}
.etape p b {{ font-weight: 600; }}
.q {{ break-inside: avoid; border-top: .4mm solid var(--encre); padding-top: 2.5mm; }}
.q h3 {{ font-family: "Archivo", sans-serif; font-stretch: 112%; font-size: 13pt; margin-bottom: 2.5mm; }}
.q ul {{ list-style: none; display: grid; gap: 3mm; font-size: 12.5pt; line-height: 1.5; }}
.q b {{ font-family: "Archivo", sans-serif; font-weight: 700; }}
</style></head><body>
<div class="sur">Jury · Partie 1 sur 4 · Rostom</div>
<h1>La structure, avec l'animation 3D</h1>
<div class="intro">{gras(INTRO)}</div>
{corps}
<div class="q"><h3>Si on nous pose la question</h3><ul>{qs}</ul></div>
</body></html>"""


open("partie-orale.html", "w", encoding="utf-8").write(page())
print("partie-orale.html écrit")
