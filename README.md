<h1 align="center">
  <b>movie_colorbar</b>
</h1>

A simple scrip to turn a video into a colorbar.

## Install

### Prerequisites

This code is compatible with `Python 3.6+`, and requires that you have [ffmpgeg][ffmpeg] installed in your path.
You can install it in your virtual enrivonment with:
```bash
pip install movie_colorbar
```

## Usage

With this package is installed in the activated enrivonment, usage is:
```
python -m movie_colorbar [-h] [-t TITLE] [-m METHOD] -s SOURCE_PATH [-f FPS]
                         [-l LOG_LEVEL]
```

Detailed options go as follows:
```bash
usage: __main__.py [-h] [-t TITLE] [-m METHOD] -s SOURCE_PATH [-f FPS]
                   [-l LOG_LEVEL]

Getting your average colorbar.

optional arguments:
  -h, --help            show this help message and exit
  -t TITLE, --title TITLE
                        String. Name that will be given to intermediate
                        directory. Defaults to 'output'.
  -m METHOD, --method METHOD
                        String. Method to use to calculate the average color.
                        Options are: rgb, hsv, hue, kmeans, common, lab, xyz,
                        rgbsquared, resize, and quantized. Defaults to
                        'rgbsquared'.
  -s SOURCE_PATH, --source-path SOURCE_PATH
                        String. Path to source video file to get the images
                        from. Defaults to current directory.
  -f FPS, --fps FPS     Integer. Number of frames to extract per second of
                        video footage. Defaults to 10.
  -l LOG_LEVEL, --logs LOG_LEVEL
                        The base console logging level. Can be 'debug',
                        'info', 'warning' and 'error'. Defaults to 'info'.
```

An example command is then:
```
python -m movie_colorbar -t sw9_trailer -m rgbsquared -s ~/Desktop/STARWARS_9_TRAILER.webm -fps 25
```

The script will call `ffmpeg` to extract 25 (in this case) images per second from the video file.
It will then apply the chosen method - here `rgbsquared` - to determine the average color of each frame.
Finally, it creates the colorbar with all averages and saves it in a new folder titled `bars/title`, with `title` being the argument you provided.
The output's name is a concatenation of the provided file and the method used.
Giving a directory as input will process all video files in this directory.

It is recommended to decrease the fps for when processing long videos such as entire movies.

## TODO

- [x] Delete the `images` folder after completion?
- [x] Turn into a package.
- [ ] Offer an option to do all at the same time.

## Output example

Here is an example of what the script outputs, when ran on the last [Star Wars 9 trailer](https://www.youtube.com/watch?v=P94M4jlrytQ).
All methods outputs can be found in the `bars` folder of this repository.

Kmeans:
![Example_sw9_trailer_kmeans](bars/sw9_trailer/SW9_trailer_kmeans.png)

Rgb:
![Example_sw9_trailer_rgb](bars/sw9_trailer/SW9_trailer_rgb.png)

Rgbsquared:
![Example_sw9_trailer_rgbsquared](bars/sw9_trailer/SW9_trailer_rgbsquared.png)

Lab:
![Example_sw9_trailer_lab](bars/sw9_trailer/SW9_trailer_lab.png)



## License

Copyright &copy; 2019 Felix Soubelet. [MIT License][license]

[ffmpeg]: https://ffmpeg.org/
[license]: https://github.com/fsoubelet/Movie_Colorbar/blob/master/LICENSE