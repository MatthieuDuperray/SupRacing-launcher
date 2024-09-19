import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os
import ctypes

def generate_sub_leaderboard(track):

    match track:
        case 'zandvoort':
            car = 'ferrari f2004'
            track_name = track
        case 'nurburgring':
            car = 'lotus elise sc'
            track_name = track + '-gp'
        case 'monza':
            car = 'mclaren f1 gtr'
            track_name = track
        case _ :
            print('No leaderboard opened for this track')
            return

    data = pd.read_csv('./leaderboard/leaderboard_{}.csv'.format(track))
    data.sort_values('Time', inplace=True, ignore_index=True)

    n_rows = 24
    padding = 5

    # Define the dimensions of the image
    cell_height = 30

    image_width = 320
    image_height = 880

    time_width = 53 + 3*padding
    rank_width = 46 + 2*padding
    name_width = image_width - time_width - rank_width

    x0 = padding
    y0 = 0


    # Create a blank image with the desired dimensions
    image = Image.new('RGB', (image_width + 4*padding, image_height), color='white')
    draw = ImageDraw.Draw(image)

    # Define the font and font size for the text
    font_result = ImageFont.truetype('./Fonts/Race Sport.ttf', size=12)
    font_header = ImageFont.truetype('./Fonts/Race Sport.ttf', size=24)

    # Header & Background
    draw.polygon(
        [
            (x0 + 8, y0),
            (x0 + image_width + 2*padding, y0),
            (x0 + image_width + 2*padding - 8, y0 + 2*cell_height - 5),
            (x0, y0 + 2*cell_height - 5),
        ],
        fill='#c00000' # slightly dark red
    )
    draw.text((x0 + padding + image_width/2, y0 + cell_height), track_name.upper(), font=font_header, fill='white', anchor='ms')
    draw.text((x0 + padding + image_width/2, y0 + cell_height + padding), car, font=font_result, fill='white', anchor='ma')

    y0 += cell_height + padding


    # Drivers
    for i in range(n_rows + 1):
        x0 = 2*padding
        y0 += cell_height 

        # draw background
        
        match i:
            case 0:
                color='#e0e0e0' # light grey
                color_txt='#606060'
            case 1:
                color='#ffd700' # gold
                color_txt='black'
            case 2:
                color='#a0a0a0' # silver
                color_txt='black'
            case 3:
                color='#cd7f32' # bronze
                color_txt='black'
            case _:
                color='#e0e0e0' # light grey
                color_txt='black'
        
        draw.polygon(
            [
                (x0 + 4, y0),
                (x0 + image_width, y0),
                (x0 + image_width - 4, y0 + cell_height - 5),
                (x0, y0 + cell_height - 5),
            ],
            fill=color
        )

        if i == 0:
            rank = 'Rank'
            driver = 'Driver'
            time = 'Time'
            font = font_result
        else:
            rank = str(i)

            try:
                driver = data['Driver'][i-1].replace('_', ' ').lower()
                time = data['Time'][i-1]
            except:
                driver = ''
                time = ''
            font = font_result

        # draw rank
        draw.text((x0 + rank_width/2, y0 + cell_height/2), rank, font=font, anchor='mm', fill=color_txt)

        # draw name
        x0 += rank_width
        draw.text((x0 + padding, y0 + cell_height/2), driver, font=font, anchor='lm', fill=color_txt)

        # draw time
        x0 += name_width
        draw.text((x0 + time_width/2, y0 + cell_height/2), time, font=font, anchor='mm', fill=color_txt)

        pass

    return image


def generate_leaderboard():
    
    title_pad = 200
    pad_x = 20

    width = 340
    height = 880

    global_leaderbaord = Image.new('RGB', (3*(width + pad_x), height + title_pad), color='white')

    font_title = ImageFont.truetype('./Fonts/dassault italic.otf', size=96)
    font_text = ImageFont.truetype('./Fonts/Race sport.ttf', size=16)
    draw = ImageDraw.Draw(global_leaderbaord)

    draw.text((3*width/2 + pad_x, title_pad/3), 'leaderboard', fill='black', font=font_title, anchor='mm')
    (left, top, right, bottom) = draw.textbbox((3*width/2 + pad_x, title_pad/3), 'leaderboard', font=font_title, anchor='mm')
    draw.text((3*width/2 + pad_x, (title_pad + bottom)/2), 'will only be added times made with the indicated car, pro settings and penalties on', fill='#303030', font=font_text, anchor='mm')

    for i, track in enumerate(['zandvoort', 'nurburgring', 'monza']):
        
        leaderboard = generate_sub_leaderboard(track)
        global_leaderbaord.paste(leaderboard, (i*340 + pad_x, title_pad))

    global_leaderbaord.save('./Image/global_leaderboard.png')


def generate_instruction():

    padding = 80
    title_pad = 200

    image_height = 1080
    image_width = 840

    image = Image.new('RGB', (image_width, image_height), 'white')
    draw = ImageDraw.Draw(image)

    font_title = ImageFont.truetype('./Fonts/dassault italic.otf', size=96)
    font_text = ImageFont.truetype('./Fonts/Race sport.ttf', size=16)

    # title
    x = image_width/2
    y = title_pad/3
    draw.text((x, y), 'instructions', 'black', font_title, 'mm')
    (left, top, right, bottom) = draw.textbbox((x, title_pad/3), 'instructions', font_title, 'mm')
    x += 10
    y = bottom + padding

    # instruction 1
    text = '1 - switch the wheelbase on by pressing the power button'
    draw.text((x,y), text, 'black', font_text, 'mm')
    y += padding/2
    x -= 250/2

    csl_dd_pic = Image.open('./Image/CSL_DD_power_thumb.png')
    image.paste(csl_dd_pic, (int(x), int(y)))
    y += 250 + padding/2
    x += 250/2

    text = 'if the power button is yellow,\npress it once to make it go red'
    draw.multiline_text((x,y), text, '#808080', font_text, 'mm', spacing=6, align='center')
    y += padding

    text = '2 - create or load your profile with the launcher below'
    draw.text((x,y), text, 'black', font_text, 'mm')
    y += padding/4
    

    text = '(This will also launch Assetto Corsa)'
    draw.text((x,y), text, '#808080', font_text, 'mm')
    y += 2*padding

    text = 'note that if it is your first time logging in, you might\nneed to go in setting -> control and load \'CSL_DD\'\nor \'CSL_DD_seq\' to make the game use the wheel input'
    draw.multiline_text((x,y), text, '#808080', font_text, 'mm', spacing=6, align='center')
    y += padding

    text = '3 - before you leave, switch the wheel base off\nby pressing the powerr button for 3 s'
    draw.multiline_text((x,y), text, 'black', font_text, 'mm', spacing=6, align='center')
    y += padding

    text = 'if anything breaks / gets loose / is damaged\nplease contact matthieu duperray'
    font_text = ImageFont.truetype('./Fonts/Race sport.ttf', size=20)
    draw.multiline_text((x,y), text, '#c00000', font_text, 'mm', spacing=6, align='center')

    image.save('./Image/instructions.png')


def generate_background():

    background = Image.new('RGB', (1920, 1080), 'white')

    if not os.path.exists('./Image/instructions.png'):
        generate_instruction()
    instructions = Image.open('./Image/instructions.png')

    generate_leaderboard()
    leaderboard = Image.open('./Image/global_leaderboard.png')

    background.paste(instructions)
    background.paste(leaderboard, (840,0))

    background.save('./Image/background.png')
    
def update():
    generate_background()
    path = os.path.abspath('./Image/background.png')
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path , 0)
    print('Wallpaper updated')

if __name__ == '__main__':
    update()
    