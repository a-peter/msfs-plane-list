from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

class Scanner(App):
  """A textual app to search for MSFS airplanes and
  export a list to Excel and/or CSV"""

  BINDINGS = [('d', 'toggle dark', 'Toggle dark mode')]

  def compose(self):
    yield Header()
    yield Footer()

  def action_toggle_dark(self) -> None:
    self.dark = not self.dark

if __name__ == '__main__':
  app = Scanner()
  app.run()