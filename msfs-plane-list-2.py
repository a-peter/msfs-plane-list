from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual import events

class Scanner(App):
  """A textual app to search for MSFS airplanes and
  export a list to Excel and/or CSV"""

  BINDINGS = [
    ('d', 'toggle_dark()', 'Toggle dark mode'),
    ('q', 'quit()', 'End the program')
  ]

  def compose(self) -> ComposeResult:
    yield Header()
    yield Footer()

  def action_toggle_dark(self) -> None:
    self.dark = not self.dark

if __name__ == '__main__':
  app = Scanner()
  app.run()