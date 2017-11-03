import sys, getopt
import PIL
from PIL import Image


def usage():
    print 'resize_image.py -i <input_image_filename> -o <output_image_filename> -s <width:height>'


def main(argv):

    baseheight = 300
    basewidth = 300
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

    #img = Image.open(input)
    #img = img.resize((width, height), PIL.Image.BICUBIC)
    #img.save(output)

    # Keep the same height
    #img = Image.open(input)
    #hpercent = (height / float(img.size[1]))
    #width = int((float(img.size[0]) * float(hpercent)))
    #img = img.resize((width, height), PIL.Image.ANTIALIAS)
    #img.save(output)

    # Keep the same width

    img = Image.open(input)
    wpercent = (width / float(img.size[0]))
    height = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((width, height), PIL.Image.ANTIALIAS)
    img.save(output)

    print 'Resize Image Completed...'

if __name__ == '__main__':
    main(sys.argv[1:])