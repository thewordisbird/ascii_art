# Ascii Art

A python library to convert .jpg, .jpeg or .png files to ascii_art. The ascii art image can be output to the terminal or to a text file.

## Installation

The library can be installed as a docker image downloaded from docker hub or a python package.

### Docker Installation


### PyPi Installation

```bash
pip install ascii_art_theW0rdisbird
```

## Usage

```python
import ascii_art

a = ascii_art.AsciiArt('path/to/image.jpg')
# Print image to terminal
a.print_to_terminal()

# Print image to .txt file
a.print_to_file()
```

## License
[MIT](https://choosealicense.com/licenses/mit/)