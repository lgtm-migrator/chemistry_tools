# stdlib
from typing import List, Optional

# 3rd party
from docutils import nodes  # nodep
from docutils.statemachine import ViewList  # nodep
from domdf_python_tools.paths import PathPlus
from sphinx.application import Sphinx  # nodep
from sphinx.util.docutils import SphinxDirective  # nodep
from tabulate import tabulate

# this package
from chemistry_tools.pubchem import properties


def replace_unicode(app: Sphinx, exception: Optional[Exception] = None):
	if exception:
		return

	if app.builder.name.lower() != "latex":
		return

	output_file = PathPlus(app.builder.outdir) / f"{app.builder.titles[0][1]}.tex"

	output_content = output_file.read_text()

	output_content = output_content.replace('⁺', r'\textsuperscript{+}')
	output_content = output_content.replace('⁻', r'\textsuperscript{-}')
	output_content = output_content.replace('⋅', r'\textbullet{}')
	output_content = output_content.replace('α', r'\textalpha{}')
	output_content = output_content.replace('ₑ', r'\textsubscript{e}')
	output_content = output_content.replace('\u205f', r'\:')

	output_file.write_clean(output_content)


class PropertiesTableDirective(SphinxDirective):
	"""
	Directive to show a table of valid properties and their descriptions for the ``pubchem`` module.
	"""

	has_content: bool = False

	def run(self) -> List[nodes.Node]:
		"""
		Create the rest_example node.
		"""

		valid_property_descriptions: str = tabulate(
				[(prop.name, prop.description) for prop in properties._properties],
				headers=["Property", "Description"],
				tablefmt="rst",
				)

		view = ViewList(valid_property_descriptions.splitlines())

		example_node = nodes.paragraph(rawsource=valid_property_descriptions)  # type: ignore[arg-type]
		self.state.nested_parse(view, self.content_offset, example_node)  # type: ignore[arg-type]

		return [example_node]


def setup(app: Sphinx):
	app.connect("build-finished", replace_unicode)
	app.add_directive("properties-table", PropertiesTableDirective)
