from abjad.tools.markuptools import Markup


def _write_footer(outfile, footer):

   assert isinstance(footer, (Markup, str, type(None)))
   outfile.write('\\paper {\n')
   
   if isinstance(footer, Markup):
      outfile.write('\toddFooterMarkup = %s\n' % footer.format)
      outfile.write('\tevenFooterMarkup = %s\n' % footer.format)
   elif isinstance(footer, str):
      outfile.write('\toddFooterMarkup = "%s"\n' % footer)
      outfile.write('\tevenFooterMarkup = "%s"\n' % footer)
   elif isinstance(footer, type(None)):
      pass
   outfile.write('}\n\n')
