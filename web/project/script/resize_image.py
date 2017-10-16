import sys, getopt
import PIL
from PIL import Image


def usage():
    print 'resize_image.py -i <input_image_filename> -o <output_image_filename> -s <width:height>'


def main(argv):

    baseheight = 350
    basewidth = 624
    height = 0
    width = 0
    input = ''
    output = ''
    size = ''

    try:
        opts, args = getopt.getopt(argv,"hi:o:s:",["input=","output=","size="])

    except getopt.GetoptError:
        usage()
        sys.exit(2)

    if len(opts) == 0:
        usage()
        sys.exit()

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-i", "--input"):
            input = arg
        elif opt in ("-o", "--output"):
            output = arg
        elif opt in ("-s", "--size"):
            size = arg.rsplit(':',1)
            width = int(size[0])
            height = int(size[1])

    if not input:
        usage()
        sys.exit(2)

    if not output:
        mod_input = input.rsplit('.',1)
        output = mod_input[0] + '-modified.' + mod_input[1]

    if not size:
        width = basewidth
        height = baseheight

    img = Image.open(input)
    img = img.resize((width, height), PIL.Image.BICUBIC)
    img.save(output)

    print 'Resize Image Completed...'



    #img = Image.open('../upload/assets/user/screenshots/alejeune@genesys.com/gauge-viz_2.png')
    #hpercent = (baseheight / float(img.size[1]))
    #wsize = int((float(img.size[0]) * float(hpercent)))
    #img = img.resize((wsize, baseheight), PIL.Image.ANTIALIAS)
    #img = img.resize((basewidth, baseheight), PIL.Image.BICUBIC)
    #img.save('../upload/assets/user/screenshots/alejeune@genesys.com/gauge-viz_2-modified.png')



if __name__ == '__main__':
    main(sys.argv[1:])