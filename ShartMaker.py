import sys
import csv
from math import ceil
from PIL import Image, ImageDraw, ImageFont

###############################################################################
################################## VARIABLES ##################################
###############################################################################

pair_size = 128
padding = 4
pairs_per_row = 10

colors = [
    "#837A82",
    "#A811E9",
    "#FF00FF",
    "#7700FF",
    "#0022FF",
    "#00FFE6",
    "#08FD00",
    "#40A56C",
    "#FFF700",
    "#DAD322",
    "#FF4400",
]


###############################################################################
################################## FUNCTIONS ##################################
###############################################################################

#Reads the input csv file and outputs a list with shape [count, [pair1, pair2, ...]] ordered by count
def read_csv(filename: str) -> list:
    try:
        input_csv = open(filename, "r")
    except:
        print("Error opening {}".format(filename))
        print("Try using : python {} -h".format(sys.argv[0]))
        print("for help")
        exit(1)
    
    csv_reader = csv.reader(input_csv, delimiter = ",")
    usage_dict = {}
    for row in csv_reader:
        try:
            if row[1] in usage_dict:
                usage_dict[row[1]].append(row[0])
            else:
                usage_dict[row[1]] = [row[0]]
        except:
            print("Error while processing {} : can't add line {} to dict".format(filename, row))
            exit(1)
    
    usage_list = [ [int(key), usage_dict[key]] for key in usage_dict]
    usage_list.sort(key=lambda x:x[0], reverse=True)
    return usage_list




#This function calculates each row's height and the total shart's width
#Layout is as following, with no more than 10 pairs on each row
# | N_n   | Pair_n1 Pair_n2 ...
# | ...   | ...
# | N_0   | Pair_01 Pair_02 ...
def get_shart_size(usage_list: list) -> tuple:
    row_heights = []
    max_row_width = 0
    
    for row in usage_list:
        row_heights.append(ceil(len(row[1])/pairs_per_row)*(pair_size + 2*padding))
        max_row_width = max(max_row_width, min(len(row[1]), pairs_per_row)*(pair_size + 2*padding))
    
    #We don't forget to add the beginning of the row, containing the number of usage!
    return (max_row_width + pair_size, row_heights)


def print_help():
    print("ShartMaker")
    print("Usage : python {} [path/to/input.csv]".format(sys.argv[0]))
    print("If input.csv is not specified, it tries to load input.csv from working directory")
    print("It will output shart.png in the working directory")
    print("WARNING : IT WILL OVERWRITE shart.png IF EXISTING")

###############################################################################
#################################### MAIN #####################################
###############################################################################

#TODO : I know my main is a mess and I should make more functions
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help"]:
        print_help()
        exit(0)
    
    print("Reading csv")
    csv_filename = "input.csv" if len(sys.argv) <= 1 else sys.argv[1]
    usage_list = read_csv(csv_filename)
    
    (width, row_heights) = get_shart_size(usage_list)
    height = sum(row_heights)
    
    print("Making shart!")
    shart = Image.new("RGB", (width, height))
    
    font = ImageFont.truetype("fonts/arial.ttf", 48) 
    horizontal_line = Image.new("RGB", (width, 1), (150, 150, 150)) #gray horizontal line
    vertical_line = Image.new("RGB", (1, height), (150, 150, 150)) #gray vertical line
    for y,row in enumerate(usage_list):
        count_str = str(row[0]) #string containing the number of usage of this row
        
        #First, we add at the beginning of the row the number of usage
        #It is pair_size in width and row_height[y] in height
        #The color is determined by the number of usage, we change color by group of 10 (1-10 usage is a color, 10-20 usage is another color, ...).
        #Since we don't have an infinite amout of color, we max at len(colors)-1
        number_image = Image.new("RGB", (pair_size, row_heights[y]), colors[min(ceil(row[0]/10), len(colors)-1)])
        draw = ImageDraw.Draw(number_image)
        w, h = draw.textsize(count_str, font=font)
        draw.text(((pair_size - w) / 2, (row_heights[y] - h) / 2), count_str, fill=(0, 0, 0), font=font)
        
        #We paste the number of usage and the horizontal separator line
        shart.paste(number_image, (0, sum(row_heights[:y])))
        shart.paste(horizontal_line, (0,sum(row_heights[:y+1])-1))
        
        #Now we add the trainer icons
        for x, trainer_name in enumerate(row[1]):
            try:
                trainer_image = Image.open("trainer_images/{}.png".format(trainer_name))
            except:
                print("Error opening trainer_images/{}.png".format(trainer_name))
                exit(1)
            
            trainer_image = trainer_image.resize((pair_size, pair_size))
            #This paste looks quite complicated since we have to go to the next line if x (horizontal position) exceeds pairs_per_row
            shart.paste(trainer_image, (pair_size + padding + (x%pairs_per_row)*(pair_size + 2*padding), padding + sum(row_heights[:y]) + (x//pairs_per_row)*(2*padding + pair_size)))
        
        print("Row {}/{} done!".format(y+1, len(usage_list)))
    
    
    #Finally, we add the vertical line separating the number of usage and the pair's icons
    shart.paste(vertical_line, (pair_size, 0))
    
    #We resize to be able to upload to 4chan, image file size should be under 4MB with a max height of 5000 (width is also bounded by about pairs_per_row*pair_size)
    if height > 5000:
        shart = shart.resize((int(width * 5000/height), 5000))
    
    print("Saving... do not turn off power")
    shart.save("shart.png")
