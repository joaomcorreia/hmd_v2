from django.test import SimpleTestCase
from django.template.loader import get_template


class TemplateSmokeTests(SimpleTestCase):
    """Compile a handful of important templates to catch syntax errors early.

    This test intentionally only compiles templates (via get_template) without
    rendering them with a full context to avoid DB dependencies. Compilation
    will fail for syntax errors like unbalanced tags or malformed if-expressions.
    """

    def test_templates_compile(self):
        templates = [
            'index.html',
            'base.html',
            'partials/header.html',
            'admin/sidebar.html',
            'admin/sidebar_ai.html',
            'admin/tools/home-preview.html',
            'admin/tools/ai.html',
            'admin/analytics/board.html',
        ]
        for tpl in templates:
            with self.subTest(template=tpl):
                # get_template will compile the template and raise on syntax errors
                get_template(tpl)
