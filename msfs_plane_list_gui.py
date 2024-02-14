from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.message import Message
from textual.widgets import Header, Footer, Log, Button, LoadingIndicator
from textual import events
from datetime import datetime

import msfs_plane_list as pl

class MSFS_Aircraft_Scanner(App):
  """A textual app to search for MSFS airplanes and
  export a list to Excel and/or CSV"""

  BINDINGS = [
    # ('d', 'toggle_dark()', 'Toggle dark mode'),
    # ('a', 'add_text()', 'Add text'),
    ('r', 'add_text', 'Run search'),
    ('q', 'quit()', 'End the program')
  ]
  LOG = Log('abc')
  loading_indicator = None

  def compose(self) -> ComposeResult:
    yield Header()
    yield Footer()
    yield ScrollableContainer(Button("Start", id="start", variant="success"), self.LOG)

  def on_button_pressed(self, event: Button.Pressed) -> None:
     if event.button.id == 'start':
      self.action_add_text()

  def action_toggle_dark(self) -> None:
    self.dark = not self.dark
  
  async def action_add_text(self) -> None:
    with open(pl.LOG_FILE, 'w') as logfile:
      packages = pl.get_packages_folders()
      if len(packages) == 0:
        self.LOG.write_line('No MSFS packages found.')
      else:
        for package in packages:
          self.LOG.write_line(f'{package[0]}: {package[1]}')
          aircrafts = await pl.find_aircrafts(package[1], logfile)
          aircrafts_data = pl.read_aircrafts_data(aircrafts, logfile)
          self.LOG.write_line(f'Found {len(aircrafts_data)} aircrafts')

          try:
              pl.export_to_csv(package[0], aircrafts_data)
              logfile.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: Written to "aircrafts-{package[0]}.csv"\n')
              self.LOG.write_line(f'Exported to "aircrafts-{package[0]}.csv"')
          except:
              logfile.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: Exception on writing to csv file\n')

          try:
              pl.export_to_excel(package[0], aircrafts_data)
              logfile.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: Written to "aircrafts-{package[0]}.xlsx"\n')
              self.LOG.write_line(f'Exported to "aircrafts-{package[0]}.xlsx')
          except:
              logfile.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: Exception on writing to excel file\n')

  class AircraftsFound(Message):
    def __init__(self, aircrafts) -> None:
       self.aircrafts = aircrafts
       
if __name__ == '__main__':
  app = MSFS_Aircraft_Scanner()
  app.run()