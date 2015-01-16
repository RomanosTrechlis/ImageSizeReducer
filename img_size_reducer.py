from PIL import Image
import sys
import os
import glob
import optparse

__version__ = "1.0"
__author__ = "Romanos Trechlis"

def resize_img(height, image):
    r = float(height) / image.size[1]
    width = int(image.size[0] * r)
    resized = image.resize((width, height), Image.ANTIALIAS)
    return resized

def save_img_JPG(image, image_path, image_name, q):
    image.save(image_path + image_name + "_" + image_name.encode('HEX') + ".JPG",
               option = "optimize",
               quality = q) ###

def single_file(image_name, height, quality):
    print "Opening image..."
    image = Image.open(image_name)
    if image.size[1] > height:
        print "Resizing image..."
        image = resize_img(height, image)
    print "Saving image..."
    img_name = image_name.split(".")[0]
    save_img_JPG(image, ".\\", img_name, quality)
    print "Image successfully saved as: " + img_name + "_" + img_name.encode('HEX') +".JPG"

def directory(image_path, height, quality):
    os.chdir(image_path)
    #print "Path: " + image_path
    #print "!Warning!: The script handles only JPG files."
    image_list = glob.glob("*.JPG")
    
    list_size = len(image_list)
    current = 0
    target_dir = image_path.encode('HEX') + "\\"
    os.system("mkdir " + target_dir)
    
    for image_name in image_list:
        sys.stdout.write("Saving image %d from %d -> [%.2f%% completed]\r"
                         % (current,
                            list_size,
                            float(current) * 100 / list_size))
        sys.stdout.flush()
        
        image = Image.open(image_name)
        if image.size[1] > height:
            image = resize_img(height, image)
            
        img_name = image_name.split(".")[0]
        save_img_JPG(image, target_dir, img_name, quality)

        current += 1
        sys.stdout.write("Saving image %d from %d -> [%.2f%% completed]\r"
                         % (current,
                            list_size,
                            float(current) * 100 / list_size))
        sys.stdout.flush()
 
    print "\nDone!"

def main(argv):
    desc = """This script resize and alter the quality of images in order to reduce the file size.\nFor now it is tested on .JPG image files only."""
    usage = "Usage: python " + argv[0] + " [options]"
    
    parser = optparse.OptionParser(usage,
                                   description = desc,
                                   version = __version__)
    
    parser.add_option("-f", "--file",
                      help="Specify a single image file.",
                      dest = "image_name",
                      action = "store") 
    parser.add_option("-d", "--directory",
                      help="Specify a directory.",
                      dest = "image_path",
                      action = "store")  
    parser.add_option("-i", "--height",
                      help="Specify the new image's height [default = [%default]].",
                      dest = "height",
                      default = 1080,
                      action = "store",
                      type = "int")
    parser.add_option("-q", "--quality",
                      help="Specify the new image's quality [default = [%default]].",
                      default = 95,
                      action = "store",
                      type = "int")

    (opts, args) = parser.parse_args(argv)

    if opts.image_name != None:
        single_file(opts.image_name, opts.height, opts.quality)
    elif opts.image_path != None:
        directory(opts.image_path, opts.height, opts.quality)
    else:
        print usage
        
if __name__ == "__main__":
    main(sys.argv)
    #main(sys.argv[1:])
