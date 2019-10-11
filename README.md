# pytchie
Random music synthesis in Python. Still a work in progress.

*This was made in about three days as a project for a computer music class. While I hope to do some cleanup and revision in the future, it is currently quite possibly some of the worst code I've ever written. Forker beware.*

### Samples
The following songs were generated using Pytchie. You can view the settings used to generate them in the [examples folder.](https://github.com/jeremycryan/pytchie/tree/master/examples)

- [Download journey.wav](https://github.com/jeremycryan/pytchie/raw/master/examples/journey.wav)

- [Download bounce.wav](https://github.com/jeremycryan/pytchie/raw/master/examples/bounce.wav)

### How to use

To generate your own music, [download the Windows executable](https://github.com/jeremycryan/pytchie/blob/master/win_executable.zip?raw=true), extract it, and run music_gen_gui.exe.

The program will generate a song based on your parameters and save it to a "Pytchie `output`" folder as a `WAV` file. You can then play it, modify it, or move it elsewhere.

>  Note that each new generated song file will be a separate `test_${NUM}.wav` file where `${NUM}` is an increasing number starting from 1.
> 
> For instance, in initially empty `output` folder there will be first file called `test_1.wav`. Then `test_2.wav` will apear, then `test_3.wav` etc.
>

![Screenshot of pytchie](https://github.com/jeremycryan/pytchie/blob/master/examples/bounce.png?raw=true)
