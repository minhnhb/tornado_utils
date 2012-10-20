import random
import StringIO
import Image
import ImageFont
import ImageDraw
import ImageFilter


class Captcha:
    _font = ImageFont.truetype("captcha.ttf", 25)

    @staticmethod
    def init(font="captcha.ttf", size=25):
        self._font = ImageFont.truetype(font, size)

    @staticmethod
    def get_value(text):
        """Generate a captcha image"""
        # randomly select the foreground color
        #fgcolor = random.randint(0,0xffff00)
        # make the background color the opposite of fgcolor
        #bgcolor = fgcolor ^ 0xffffff
        bgcolor = "#FFFCE9"
        fgcolor = "#666"
        # determine dimensions of the text
        dim = Captcha._font.getsize(text)
        # create a new image slightly larger that the text
        im = Image.new('RGB', (dim[0]+5,dim[1]+5), bgcolor)
        d = ImageDraw.Draw(im)
        x, y = im.size
        r = random.randint
        # draw 100 random colored boxes on the background
        for num in range(3):
            d.rectangle((r(0,x),r(0,y),r(0,x),r(0,y)),fill=r(0,0xffffff))
        # add the text to the image
        d.text((3,3), text, font=Captcha._font, fill=fgcolor)
        im = im.filter(ImageFilter.EDGE_ENHANCE_MORE)
        buf = StringIO.StringIO()
        im.save(buf, format='JPEG')
        jpeg = buf.getvalue()
        buf.close()

        return jpeg

if __name__ == '__main__':
    print Captcha.get_value("Fuck you")
