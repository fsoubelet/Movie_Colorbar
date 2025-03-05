<h1 align="center">
  <b>movie_colorbar</b>
</h1>

A command line tool to create colorbars from videos.

## Install

The package requires `Python 3.10+` versions, and to have have [ffmpgeg][ffmpeg] installed in your path.

One can install from `PyPI` in a virtual enrivonment with:

```bash
python -m pip install movie_colorbar
```

<details> <summary><b>As a uv tool</b></summary>

The package also supports being installed as a tool with [uv][uv]:

```bash
uv tool install movie_colorbar
```

</details>

### Speedups

If the `joblib` and/or `numba` packages are available in the environment, they will be used to speed up the processing of video frames and color calculations.
This can lead to drastic speedups when extracting a high number of images (by processing long videos or simply setting a high `fps` option value).
One can install these along with the package via the `fast` extra dependency group:

```bash
python -m pip install movie_colorbar[fast]
```

<details> <summary><b>As a uv tool</b></summary>

```bash
uv tool install movie_colorbar[fast]
```

</details>

## Usage

Once installed, the package generates two executables (`colorbar` and `movie_colorbar`) to be called from the command line.

It can also be called directly through `python` or via the `uv tool` interface.

<details> <summary><b>Full command line interface</b></summary>

Detailed usage goes as follows:

```bash
 Usage: python -m movie_colorbar [OPTIONS] INPUT OUTPUT

 Command line tool to create colorbars from videos.
 From the input video individual frames are extracted with ffmpeg and written to disk in a directory placed next to the final output
 and named after the video. Each frame is reduced to a single color according to the chosen method. Finally a colorbar is created
 from these determined colors, and written to disk as an image file at the provided output location. By default the extracted frames
 are removed after processing, but they can be kept if desired (see the 'cleanup' option).
 Should the input be a directory, then every video file contained within will be processed, provided it is supported by ffmpeg. In
 this case the output should also be a directory, in which one colorbar will be created for each video file.

╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    input       PATH  Path to the input video file or directory. [required]                                                      │
│ *    output      PATH  Path to the output colorbar image or directory. [required]                                                 │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --method                                [common|hsv|hue|kmeans|lab|quantized|resize  Method used to calculate the color for each  │
│                                         |rgb|rgbsquared|xyz]                         frame.                                       │
│                                                                                      [default: rgb]                               │
│ --fps                                   INTEGER RANGE [x>=0]                         Number of frames to extract per second of    │
│                                                                                      video footage.                               │
│                                                                                      [default: 10]                                │
│ --cleanup               --no-cleanup                                                 Whether to remove the extracted frames after │
│                                                                                      processing.                                  │
│                                                                                      [default: cleanup]                           │
│ --log-level                             [trace|debug|info|warning|error|critical]    The base console logging level.              │
│                                                                                      [default: info]                              │
│ --install-completion                                                                 Install completion for the current shell.    │
│ --show-completion                                                                    Show completion for the current shell, to    │
│                                                                                      copy it or customize the installation.       │
│ --help                                                                               Show this message and exit.                  │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

</details>

<details> <summary><b>As a uv tool</b></summary>

One can call the tool via the package name with `uvx`:

```bash
uvx movie_colorbar [OPTIONS] INPUT OUTPUT
```

It is also possible to use the `colorbar` command alias by specifying the tool to source from:

```bash
uvx --from movie_colorbar colorbar [OPTIONS] INPUT OUTPUT
```

</details>

Here is an example command:

```bash
python -m movie_colorbar ~/Desktop/STARWARS_9_TRAILER.mkv ~/Desktop/colorbar.png --method rgbsquared --fps 25
```

One can also provide a directory as input (and must then provide a directory as output), which will process all video files found in this directory.

**Note:** It is recommended to decrease the fps when processing long videos such as entire movies.

## Examples

Here are examples of colorbars produced from the [Star Wars 9 trailer](https://www.youtube.com/watch?v=P94M4jlrytQ).
All these files can be found in the `bars` folder of this repository.

<details> <summary><b>How to reproduce</b></summary>

The following command was used to generate all the colorbars:

```bash
for method in common hsv hue kmeans lab quantized resize rgb rgbsquared xyz; do python -m movie_colorbar ~/Desktop/STARWARS_9_TRAILER.mkv bars/sw9_trailer/SW9_trailer_$method.png --method $method --fps 25; done
```

</details>

**Kmeans:**
![Example_sw9_trailer_kmeans](bars/sw9_trailer/SW9_trailer_kmeans.png)

**Rgb:**
![Example_sw9_trailer_rgb](bars/sw9_trailer/SW9_trailer_rgb.png)

**Rgbsquared:**
![Example_sw9_trailer_rgbsquared](bars/sw9_trailer/SW9_trailer_rgbsquared.png)

**Lab:**
![Example_sw9_trailer_lab](bars/sw9_trailer/SW9_trailer_lab.png)

---

<div align="center">
  <sub><strong>Made with ♥︎ by fsoubelet</strong></sub>
  <br>
  <sub><strong>MIT &copy 2019 Felix Soubelet</strong></sub>
</div>

[ffmpeg]: https://ffmpeg.org/
[uv]: https://docs.astral.sh/uv/guides/tools/