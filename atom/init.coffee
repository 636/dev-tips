# Your init script
#
# Atom will evaluate this file each time a new window is opened. It is run
# after packages are loaded/activated and after the previous editor state
# has been restored.
#
# An example hack to log to the console when each text editor is saved.
#
# atom.workspace.observeTextEditors (editor) ->
#   editor.onDidSave ->
#     console.log "Saved! #{editor.getPath()}"
atom.commands.add 'atom-workspace', 'custom:restart', ->
  atom.restartApplication()

# custom env variable
path = atom.config.get('core.PATH')
if path
  process.env.PATH = "#{path};#{process.env.PATH}"
