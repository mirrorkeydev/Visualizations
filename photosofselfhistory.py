from exif import Image
import matplotlib.pyplot as plt
import os

# set the folder we want to analyze pictures from
folder = "C:\\Users\\Melanie\\Downloads\\dspics\\"

# get all pictures inside the folder
allpics = os.listdir(folder)

def main():
    me = 0
    others = 0

    for pic in allpics:
        who_took_pic = process_pic(pic)
        if who_took_pic == "me": me += 1
        else: others += 1

    print("I took %d pictures of myself" % (me))
    print("Others took %d pictures of me" % (others))

def process_pic(path):
    try:
        ext = path[path.find('.'):len(path)].lower()
        if (ext == ".jpg" or ext == ".jpeg" or ext == ".png" or ext == ".raw"):
            with open(folder + path, 'rb') as img:
                exif_data = Image(img)
                if (exif_data.has_exif and len(dir(exif_data)) > 10):
                    try:
                        m = exif_data.model
                        return "me"
                    except:
                        return "others"
                else:
                    return "others"
                img.close()
    except Exception as e:
        print(e)
        
if __name__ == "__main__":
    main()