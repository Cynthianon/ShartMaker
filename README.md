# ShartMaker
This tool allows chartkeks to quicky generate sharts after counting the submissions. It's far from perfect, but it was a good exercice for me to practice Python. But **IT WORKS** (tested only on Linux for now)

## Requirements
To use this tool, you need python 3 (check your version with `python --version`) and the PIL library.

## Usage
You need to edit `template.csv` and change all the zeros to the number of usage. You can do it with a text editor or with a spreadsheet editor. This will be your input csv.
If you place your input csv file in the directory and rename it `input.csv`, simply run the script : `python ShartMaker.py`. Otherwise, you can always specify the path to yout input file : `python ShartMaker.py path/to/input.csv`

There is an example file provided in this repository, so to be sure everything is working just run the script without parameters!

For more information, run `python ShartMaker.py --help`

### How to add pairs ?
I'll try to keep this repository up to date, but you can always manually add pairs (and if you do before I, please pull request !). To do that, edit template.csv and add a new entry for that trainer. Then add to `trainer_images` an image of this pair in png format, with the same name as the new entry one. Tadaaa~

## Credits
pmg\_test1 from npantelaios, which was the first and on which my version was inspired [https://github.com/npantelaios/pmg_test1]
