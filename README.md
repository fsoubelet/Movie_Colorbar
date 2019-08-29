# Movie Colorbar: Turn a video into a colorbar.

A simple scrip to extract frames from a video and generate a colorbar with the average color from each frame.
Slightly customizable in the number of frames and algorithms used.


## Install

### Prerequisites

This script runs on Python3, and requires the [`Halo`][halo] library.
If you want to get rid of this dependency, simply comment out the three decorators in `color_bar.py`.
It also requires that you have the amazing [ffmpgeg][ffmpeg] tool.

### Install with Git

You can install this by simply cloning the repository with:

```
git clone https://github.com/fsoubelet/Movie_Colorbar.git
```


## Usage

The script parses arguments from the commandline.
The usage goes as:

```
python color_bar.py [-h] -t TITLE -m METHOD -s SOURCE_FILE
                    [-f FRAMES_PER_SECOND]
```

The different options are as bellow:
```
  -h, --help            show this help message and exit
  -t TITLE, --title TITLE
                        String. Filename for output file.
  -m METHOD, --method METHOD
                        String. Method to use to calculate the average color.
                        Options are: rgb, hsv, hue, kmeans, common, lab, xyz,
                        rgbsquared, resize, and quantized.
  -s SOURCE_FILE, --source-file SOURCE_FILE
                        String. Path to source video file to get the images
                        from.
  -f FRAMES_PER_SECOND, --fps FRAMES_PER_SECOND
                        Integer. Number of frames to extract per second of
                        video footage.
```

An example command is then:
```
python color_bar.py -t sw9_trailer -m kmeans -s ~/Desktop/STARWARS_9_TRAILER.webm -fps 15
```

The script will create an `images` folder and call `fmpeg` to extract 15 (here) images per second of video footage into this folder.
It will then apply the chosen method - here `kmeans` - to determine the average color of each frame.
Finally, it creates the colorbar with all averages and saves it in a new folder titled `bars`.
The output's name is a concatenation of the provided title and the method used.

Beware of the `images` folder which can become quite heavy with increased fps, you should remember to delete it.
Similarly, you should decrease the fps for long videos such as entire movies

## TODO

- [ ] Delete the `images` folder after completion?
- [ ] Offer an option to do all at the same time.

## Output example

Here is an example of what the script outputs, when ran on the last [Star Wars 9 trailer](https://www.youtube.com/watch?v=P94M4jlrytQ).
All methods outputs can be found in the `bars` folder of this repository.

Kmeans:
<p align="center">
  <img src="https://github.com/fsoubelet/Movie_Colorbar/blob/master/bars/sw9_trailer_kmeans.png"/>
</p>

Rgbsquared:
<p align="center">
  <img src="https://github.com/fsoubelet/Movie_Colorbar/blob/master/bars/sw9_trailer_rgbsquared.png"/>
</p>

## License

Copyright &copy; 2019 Felix Soubelet. [MIT License][license]

[ffmpeg]: https://ffmpeg.org/
[halo]: https://github.com/ManrajGrover/halo
[license]: https://github.com/fsoubelet/Movie_Colorbar/blob/master/LICENSE