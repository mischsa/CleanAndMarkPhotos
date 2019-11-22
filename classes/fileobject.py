' The basic object that represents one file '

import os
import hashlib
from PIL import ImageTk, Image, ExifTags

class FileObject(object):
    ' File object that contains all information relating to one file on disk '
    def __init__(self, parent, FullPath=None, *args, **kwargs):

        self.FullPath = FullPath
        self.DirName = os.path.dirname(self.FullPath)
        self.FileName = os.path.basename(self.FullPath)
        dummy, self.FileExtension = os.path.splitext(self.FileName)

        self.ahash = None
        self.dhash = None
        self.phash = None
        self.whash = None

        # These are private variables that allow to call the corresponding method
        # If the variable is None we calculate the value
        # otherwise we return the value of this private variable

        self._IsImage = None
        self._md5 = None
        self._ExifTags = None

        #thumbnail object
        self.ThumbFrame = None

        #Is the thumbnail shown
        self.ThumbFrameHidden = True
        self.ThumbFramePosition = (-1,-1)
        
        #It this file active
        self.Active = True
        self.Selected = False

    def IsImage(self):
        ' Set IsImage to True if the file can be read by PIL '
        if not self._IsImage:
            try:
                Image.open(self.FullPath)
                self._IsImage = True
            except IOError:
                self._IsImage = False
        return self._IsImage


    def md5(self):
        if not self._md5:
            hasher = hashlib.md5()
            with open(self.FullPath, 'rb') as afile:
                buf = afile.read()
                hasher.update(buf)
            self._md5 = hasher.hexdigest()
        return self._md5
            
    def ExifTags(self):
        if self._ExifTags:
            return self._ExifTags

        # default to empty basic values
        self._ExifTags = {
            'Make': '',
            'Model': '',
            'DateTimeOriginal': '',
            'DateTime': '',
            'DateTimeDigitized': ''
        }
        with Image.open(self.FullPath) as image:
            exif = image._getexif()
            if not exif:
                return self._ExifTags

            for key, value in exif.items():
                if key in ExifTags.TAGS:
                    self._ExifTags[ExifTags.TAGS[key]] = value
        return self._ExifTags

    def CameraMake(self):
        return self.ExifTags()['Make']
    
    def CameraModel(self):
        return self.ExifTags()['Model']
    
    def Date(self):
        if self.ExifTags()['DateTimeOriginal']:
            return self.ExifTags()['DateTimeOriginal']
        if self.ExifTags()['DateTime']:
            return self.ExifTags()['DateTime']
        if self.ExifTags()['DateTimeDigitized']:
            return self.ExifTags()['DateTimeDigitized']
        return ''
    
    def MakeThumbnail(self):
        self.ThumbFrame.thumb_load_image()
