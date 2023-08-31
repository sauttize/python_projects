from PIL import Image
from os import listdir
from pathlib import Path

# Creates spritesheet for sprites
# Allow image resizing, change location of image and personalized distribution between rows and columns.

types_acc = ('.png', '.jpg', '.jpeg')

image_list = []
final_list = []  # The one to work with in the sheet
blank_bgs = []  # blank images in case the image list is smaller
rows_columns = []  # len = rows // elements = columns

image_size = []

# Errors
ERR_INTEGER = '\nERROR: Only integers allowed.\n'


def main():
    # Title
    print("---- Spritesheet creator script ----\n")

    # Creates the output folder if it doesn't exists
    p = Path('result/')
    p.mkdir(exist_ok=True)

    # Gets only the accepted image files to a list
    file_list = listdir()
    for file in file_list:
        if file.endswith(types_acc):
            try:
                new_image = Image.open(file)
                image_list.append(new_image)
            except Image.DecompressionBombError:
                print(
                    "ERROR: There's a image in the folder that is too big to handle (is there a spritesheet already?)\n")
                return

    if len(image_list) == 0:
        print('ERROR: No compatible images found in this folder, try with other folder!\n')
        return

    resizeImages()
    if createBlank():
        pasteImages()
    getRowsColumns()
    createSpritesheetImage()


def resizeImages():
    global image_list
    if questionMaker("Do you want to resize the images? (y/n) "):
        img_width = getInteger(message="-- New width: ")
        img_height = getInteger(message="-- New height: ")

        print("\n>> Resizing...")
        for i in range(len(image_list)):
            resized = image_list[i].resize(size=(img_width, img_height))
            image_list[i] = resized
        print('>> Done!\n')


def createBlank() -> bool:
    # Creates as many blank bgs as needed
    global final_list, image_size, image_list

    print('Introduce each image desired width and height:')
    # is_smaller = True

    width = getInteger(message='\n-- Image width: ')
    height = getInteger(message='-- Image height: ')

    # while (is_smaller):
    #     width = getInteger(message='\n-- Image width: ')
    #     height = getInteger(message='-- Image height: ')

    #     if width < image_list[0].size[0] or height < image_list[0].size[1]:
    #         print("\nERROR: It can't be smaller than the actual image size.")
    #     else:
    #         is_smaller = False

    image_size = (width, height)
    curr_size = image_list[0].size

    if image_size == curr_size:
        final_list = image_list
        image_size = curr_size

        print('\n>> That matches the image size, no positioning will be happening.')
        return False

    for i in range(len(image_list)):
        new_image = Image.new('RGBA', size=image_size)
        blank_bgs.append(new_image)

    return True


def pasteImages():
    global final_list

    x_pos = 0
    y_pos = 0
    if questionMaker(message='\n---- Is center (x) ok? (y/n) '):
        x_pos = int((blank_bgs[0].size[0] - image_list[0].size[0]) / 2)
    else:
        x_pos = getInteger(message='---- Please enter custom x offset: ')

    y_pos = getInteger(message="---- Please enter custom y offset: ")
    for i in range(len(blank_bgs)):
        blank_bgs[i].paste(
            im=image_list[i], box=(x_pos, y_pos))
        final_img = blank_bgs[i]
        final_list.append(final_img)

    if questionMaker("\n-- Show preview? (y/n) "):
        image_list[0].show()
        final_list[0].show()


def getRowsColumns():
    # Ask for row number and how many images per row
    rows = 0

    print('\n(%s images)' % len(image_list))
    if questionMaker(message='Do you want to evenly distribute the rows? (y/n) '):
        num = len(image_list)
        max_divisor = 1

        if not questionMaker(message="-- Make it automatic? (It may not be the best) (y/n) "):
            max_divisor = getInteger('---- How many rows? ')
            while (num % max_divisor != 0):
                print(
                    '\nERROR: Not possible! Number is not a even divider. Try again...\n')
                max_divisor = getInteger('---- How many rows? ')
        else:
            max_divisor = 1
            for i in range(2, num - 1):
                if num % i == 0:
                    max_divisor = i

        per_row = num / max_divisor
        for r in range(max_divisor):
            rows_columns.append(int(per_row))

        return

    while rows <= 0:
        try:
            rows = int(input('\n---- How many rows (%s images): ' %
                       len(image_list)))
        except ValueError:
            print("\nERROR: Only integers accepted.")
        if rows < 0:
            print("\nERROR: Only number above zero accepted.")

    for i in range(rows):
        row_num = int(input('---- Images in row nro %s: ' % (i+1)))
        rows_columns.append(row_num)


def createSpritesheetImage():
    global image_size

    y_multiplier = len(rows_columns)
    x_multiplier = 1

    for row in rows_columns:
        if row > x_multiplier:
            x_multiplier = row

    sprsheet_width = int(image_size[0] * x_multiplier)
    sprsheet_height = int(image_size[1] * y_multiplier)
    sprsheet = Image.new('RGBA', (sprsheet_width, sprsheet_height))

    pos_x = 0
    pos_y = 0
    img_num = 0
    for i in range(len(rows_columns)):
        for j in range(rows_columns[i]):
            sprsheet.paste(final_list[img_num], (pos_x, pos_y))

            pos_x += image_size[0]
            img_num += 1
        pos_x = 0
        pos_y += image_size[1]

    print('\n>> Creating spritesheet...')
    if questionMaker('\n-- Want to see a preview? (y/n) '):
        sprsheet.show()
    if questionMaker('-- Save file? (y/n) '):
        sprsheet.save('result/r_Spreedsheet.png')
        print('\n>> Succesfully saved! Great ;)\n')

# Utilities


def getInteger(message="Insert number", error=ERR_INTEGER) -> int:
    res = ""
    while True:
        try:
            res = int(input(message))
        except ValueError:
            print(ERR_INTEGER)
        else:
            break
    return res


def questionMaker(message="Do you want to continue? (y/n) ", newline=False) -> bool:
    res = False
    if input(message).upper() == 'Y':
        res = True
    if newline:
        print('\n')
    return res


main()
