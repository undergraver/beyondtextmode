This chapter contains reference to an educational source code called `codetrainer`. IT can be found on bitbucket git provider in this repositories:

* https://bitbucket.org/undergraver/codetrainer/src/master/ (the main application)
* https://bitbucket.org/undergraver/codetrainerplugins/src/master/ (the plugins)

Tutorial on how to fully complile (codetrainer wiki): https://bitbucket.org/undergraver/codetrainer/wiki/Home

Tools used:
* Visual Studio for Windows compilation
* gcc/g++ for Linux compilation (even on Windows)
* cmake - to generate specific project files (makefiles or Visual Studio projects) - that are afterwards used to build the app 
* portaudio - to play sounds
* wxWidgets - as a GUI framework
* Inno Setup - for creating a setup (only in Windows)

The result of the final compilation is a setup that can be installed.

Concepts discussed found inside the application's code:
- frameworks (wxWidgets, portaudio)
- plugins (dll creation, dynamic loading)
- Event handling in GUI framework
- callback handling

Other examples of related software:
* Audacity (sound editing app) - https://en.wikipedia.org/wiki/Audacity_(audio_editor)
* various audio formats read/write library https://en.wikipedia.org/wiki/Libsndfile
* VLC https://en.wikipedia.org/wiki/VLC_media_player
