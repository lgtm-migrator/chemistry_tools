# stdlib
from typing import Optional

# 3rd party
from domdf_python_tools.paths import PathPlus
from sphinx.application import Sphinx  # nodep


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


def setup(app: Sphinx):
	app.connect("build-finished", replace_unicode)
