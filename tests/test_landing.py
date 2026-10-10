"""Dependency-free structural checks for the Café Aurora landing page."""

from html.parser import HTMLParser
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements = []
        self.text = []
        self.text_by_tag = {}
        self.open_tags = []

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))
        if tag not in {"meta", "link", "br"}:
            self.open_tags.append(tag)

    def handle_endtag(self, tag):
        if tag in self.open_tags:
            index = len(self.open_tags) - 1 - self.open_tags[::-1].index(tag)
            del self.open_tags[index:]

    def handle_data(self, data):
        self.text.append(data)
        for tag in self.open_tags:
            self.text_by_tag.setdefault(tag, []).append(data)

    def attrs_for(self, tag):
        return [attrs for name, attrs in self.elements if name == tag]


class LandingTests(unittest.TestCase):
    def setUp(self):
        self.page = PageParser()
        self.page.feed((ROOT / "index.html").read_text(encoding="utf-8"))

    def test_language_and_document_metadata(self):
        self.assertEqual(self.page.attrs_for("html")[0].get("lang"), "es")
        self.assertEqual(len(self.page.attrs_for("title")), 1)
        self.assertEqual("".join(self.page.text_by_tag["title"]),
                         "Café Aurora — Más calma, más calidez")
        self.assertTrue(any(meta.get("charset") == "utf-8"
                            for meta in self.page.attrs_for("meta")))
        self.assertTrue(any(meta.get("name") == "viewport"
                            and "width=device-width" in meta.get("content", "")
                             for meta in self.page.attrs_for("meta")))

    def test_spanish_meta_description(self):
        descriptions = [meta.get("content") for meta in self.page.attrs_for("meta")
                        if meta.get("name") == "description"]
        self.assertEqual(descriptions, [
            "Café Aurora: un concepto de cafetería ficticia que celebra las mañanas "
            "tranquilas y el café preparado con cuidado. Un proyecto académico."
        ])

    def test_spanish_accessible_names_and_heading_references(self):
        labels = [attrs["aria-label"] for _, attrs in self.page.elements
                  if "aria-label" in attrs]
        self.assertEqual(labels, [
            "Café Aurora: inicio", "Navegación principal",
            "Ilustración de una taza de café color crema sobre un platillo bajo un sol cálido naciente",
            "Nuestra filosofía",
        ])
        ids = {attrs["id"] for _, attrs in self.page.elements if "id" in attrs}
        for _, attrs in self.page.elements:
            for reference in attrs.get("aria-labelledby", "").split():
                self.assertIn(reference, ids)

    def test_spanish_representative_content(self):
        text = " ".join(" ".join(self.page.text).split())
        for expected in (
            "Saltar al contenido", "Nuestro café", "Nuestra historia", "El espacio",
            "Más calma.", "Más calidez.", "Encuentra tu café de la mañana",
            "Buenos granos", "Mañanas tranquilas", "Un poco de alegría cada día",
            "El primer café", "Un comienzo suave", "Una mañana sin prisa",
            "CAFÉ ESPRESSO", "CAFÉ CON LECHE DE AVENA", "CAFÉ FILTRADO",
            "Chocolate oscuro", "leche de avena", "notas cítricas",
            "Aurora significa amanecer.", "El ambiente", "La invitación",
            "Sin dirección ni horarios reales.", "Volver a una mañana más luminosa",
            "HECHO CON CUIDADO, PARA APRENDER.",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, text)
        self.assertIn("Nuestras bebidas son propuestas conceptuales, no productos disponibles para pedir.", text)

    def test_spanish_illustration_copy(self):
        text = " ".join(" ".join(self.page.text).split())
        for expected in ("EL RITUAL DE CADA DÍA", "regálate un momento.",
                         "Un nuevo comienzo, en cada taza."):
            with self.subTest(expected=expected):
                self.assertIn(expected, text)

    def test_one_primary_heading(self):
        self.assertEqual(len(self.page.attrs_for("h1")), 1)

    def test_local_stylesheet_without_external_dependencies(self):
        links = self.page.attrs_for("link")
        self.assertEqual([link.get("href") for link in links], ["styles.css"])
        self.assertEqual(links[0].get("rel"), "stylesheet")
        self.assertTrue((ROOT / "styles.css").is_file())
        self.assertFalse(self.page.attrs_for("script"))
        self.assertFalse(self.page.attrs_for("img"))

    def test_unique_ids_and_resolvable_internal_links(self):
        ids = [attrs["id"] for _, attrs in self.page.elements if "id" in attrs]
        self.assertEqual(len(ids), len(set(ids)))
        anchors = self.page.attrs_for("a")
        self.assertTrue(anchors)
        for anchor in anchors:
            href = anchor.get("href", "")
            self.assertTrue(href.startswith("#") and len(href) > 1, href)
            self.assertIn(href[1:], ids)

    def test_landmarks_and_skip_link(self):
        for tag in ("header", "nav", "main", "footer"):
            self.assertEqual(len(self.page.attrs_for(tag)), 1, tag)
        self.assertEqual(self.page.attrs_for("a")[0].get("href"), "#main")
        self.assertEqual(self.page.attrs_for("main")[0].get("id"), "main")
        self.assertTrue(self.page.attrs_for("nav")[0].get("aria-label"))

    def test_menu_story_and_visit_sections(self):
        ids = {attrs.get("id") for attrs in self.page.attrs_for("section")}
        self.assertTrue({"coffee", "story", "visit"}.issubset(ids))
        self.assertEqual(len(self.page.attrs_for("article")), 3)

    def test_honest_academic_disclosure(self):
        text = " ".join(self.page.text).lower()
        self.assertIn("proyecto académico ficticio para tarea 3", text)
        self.assertIn("no es una cafetería real", text)
        self.assertIn("no se ofrecen compras, reservas ni visitas", text)
        self.assertFalse(self.page.attrs_for("button"))
        self.assertFalse(self.page.attrs_for("form"))

    def test_responsive_layout_and_keyboard_focus_rules(self):
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertIn("@media", css)
        self.assertIn(":focus-visible", css)
        self.assertIn("outline:", css)


if __name__ == "__main__":
    unittest.main()
