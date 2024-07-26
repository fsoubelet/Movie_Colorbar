<h1 align="center">
  <b>movie_colorbar</b>
</h1>

A simple script to turn a video into a colorbar.

## Install

### Prerequisites

This code is compatible with all currently supported Python versions, and requires that you have [ffmpgeg][ffmpeg] installed in your path.
You can install it in your virtual enrivonment with:

```bash
python -m pip install movie_colorbar
```

## Usage

With this package is installed in the activated enrivonment, it can be called through `python -m movie_colorbar` or through a newly created `colorbar` command.

Detailed usage goes as follows:

```bash
 Usage: python -m movie_colorbar [OPTIONS] [SOURCE_PATH]                                      
                                                                                              
 Turn a video into a colorbar.                                                                
                                                                                              
╭─ Arguments ────────────────────────────────────────────────────────────────────────────────╮
│   source_path      [SOURCE_PATH]  Location, relative or absolute, of the source video file │
│                                   to get the images from.                                  │
│                                   [default: .]                                             │
╰────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────╮
│ --title                     TEXT     Name that will be given to the output directory.      │
│                                      [default: output]                                     │
│ --method                    TEXT     Method used to calculate the average color. Options   │
│                                      are: 'rgb', 'hsv', 'hue', 'kmeans', 'common', 'lab',  │
│                                      'xyz', 'rgbsquared', 'resize' and 'quantized'.        │
│                                      [default: rgbsquared]                                 │
│ --fps                       INTEGER  Number of frames to extract per second of video       │
│                                      footage.                                              │
│                                      [default: 10]                                         │
│ --log-level                 TEXT     The base console logging level. Can be 'debug',       │
│                                      'info', 'warning' and 'error'.                        │
│                                      [default: info]                                       │
│ --install-completion                 Install completion for the current shell.             │
│ --show-completion                    Show completion for the current shell, to copy it or  │
│                                      customize the installation.                           │
│ --help                               Show this message and exit.                           │
╰────────────────────────────────────────────────────────────────────────────────────────────╯
```

An example command is then:

```bash
python -m movie_colorbar ~/Desktop/STARWARS_9_TRAILER.webm --title sw9_trailer --method rgbsquared --fps 25
```

The script will call `ffmpeg` to extract 25 (in this case) images per second from the video file.
It will then apply the chosen method - here `rgbsquared` - to determine the average color of each frame.
Finally, it creates the colorbar with all averages and saves it in a new folder titled `bars/title`, with `title` being the argument you provided.
The final output's name is a concatenation of the provided file, and of the method used.
Giving a directory as input will process all video files found in this directory.

It is recommended to decrease the fps when processing long videos such as entire movies.

## TODO

- [x] Delete the `images` folder after completion.
- [x] Turn into a package.
- [x] Improving the command line experience.
- [ ] Offer an option to do all at the same time.

## Output example

Here is an example of what the script outputs, when ran on the last [Star Wars 9 trailer](https://www.youtube.com/watch?v=P94M4jlrytQ).
All methods output can be found in the `bars` folder of this repository.

__Kmeans:__
![Example_sw9_trailer_kmeans](bars/sw9_trailer/SW9_trailer_kmeans.png)

__Rgb:__
![Example_sw9_trailer_rgb](bars/sw9_trailer/SW9_trailer_rgb.png)

__Rgbsquared:__
![Example_sw9_trailer_rgbsquared](bars/sw9_trailer/SW9_trailer_rgbsquared.png)

__Lab:__
![Example_sw9_trailer_lab](bars/sw9_trailer/SW9_trailer_lab.png)

---

<div align="center">
  <sub><strong>Made with ♥︎ by fsoubelet</strong></sub>
  <br>
  <sub><strong>MIT &copy 2019 Felix Soubelet</strong></sub>
</div>

[ffmpeg]: https://ffmpeg.org/
