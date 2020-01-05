import sys
import os.path
import configparser
from ..utils import handyfunctions as HF

def str2bool(S):
    '''convert a string to a boolean '''
    if S[0] in [0, 'n', 'N', 'f', 'F']:
        return False
    if S[0] in [1, 'y', 'Y', 't', 'T']:
        return True

class Configuration():
    ' Object that can initialise, change and inform about App configuration'
    def __init__(self, ScriptPath=None):
        # The path of the appdata and ini file
        ConfigPath = os.path.join(
            os.environ.get('APPDATA') or
            os.environ.get('XDG_CONFIG_HOME') or
            os.path.join(os.environ['HOME'], '.config'),
            "simimg"
        )
        self.IniPath = os.path.join(ConfigPath, 'simimg.ini')

        # dict to store all settings
        self.ConfigurationDict = {}
        self.set('cmdlinearguments', sys.argv[1:])
        self.set('iconpath', os.path.join(ScriptPath, 'icons'))
        self.set('databasename', os.path.join(ConfigPath,'simimg.db'))

        self._setDefaultConfiguration()
        self._readConfiguration()

    def _setDefaultConfiguration(self):
        'Default configuration parameters'
        # not yet? configurable
        self.set('maxthumbnails', 300)
        self.set('channeltoshow', 'default')
        # can be overwritten from ini file
        self.set('searchinsubfolders', False)
        self.set('confirmdelete', True)
        self.set('gzipinsteadofdelete', False)
        self.set('savesettings', True)
        self.set('showbuttons', True)
        self.set('filenameonthumbnail', False)
        self.set('thumbnailsize', 150)
        self.set('startupfolder', '')
        self.set('findergeometry', '1200x800+0+0')
        self.set('viewergeometry', '1200x800+50+0')

    def _readConfiguration(self):
        '''Function to get configurable parameters from SimImg.ini.'''
        config = configparser.ConfigParser(converters={'strbool': str2bool})
        if config.read(self.IniPath):
            default = config['simimg']
            doRecursive = default.getstrbool('searchinsubfolders', 'no')
            confirmdelete = default.getstrbool('confirmdelete', 'yes')
            doGzip = default.getstrbool('gzipinsteadofdelete', 'no')
            savesettings = default.getstrbool('savesettings', 'yes')
            showbuttons = default.getstrbool('showbuttons', 'yes')
            filenameonthumbnail = default.getstrbool('filenameonthumbnail', 'no')
            thumbSize = default.getint('thumbnailsize', 150)
            startupDir = default.get('startupfolder', '.')
            finderGeometry = default.get('findergeometry', '1200x800+0+0')
            viewerGeometry = default.get('viewergeometry', '1200x800+50+0')
            # store read values in ConfigurationDict
            self.set('searchinsubfolders', doRecursive)
            self.set('confirmdelete', confirmdelete)
            self.set('gzipinsteadofdelete', doGzip)
            self.set('savesettings', savesettings)
            self.set('showbuttons', showbuttons)
            self.set('filenameonthumbnail', filenameonthumbnail)
            self.set('thumbnailsize', thumbSize)
            self.set('startupfolder', startupDir)
            self.set('findergeometry', finderGeometry)
            self.set('viewergeometry', viewerGeometry)

    def writeConfiguration(self):
        'save configuration info'

        # save settings disabled
        if not self.get('savesettings'):
            return

        config = configparser.ConfigParser()
        config['simimg'] = {
            'searchinsubfolders':self.get('searchinsubfolders'),
            'confirmdelete':self.get('confirmdelete'),
            'gzipinsteadofdelete':self.get('gzipinsteadofdelete'),
            'savesettings':self.get('savesettings'),
            'showbuttons':self.get('showbuttons'),
            'filenameonthumbnail':self.get('filenameonthumbnail'),
            'thumbnailsize':self.get('thumbnailsize'),
            'startupfolder':self.get('startupfolder'),
            'findergeometry':self.get('findergeometry'),
            'viewergeometry':self.get('viewergeometry')
        }
        with open(self.IniPath, 'w') as configfile:
            config.write(configfile)

    def get(self, parameter):
        'Return one value of the configuration'
        if not parameter in self.ConfigurationDict:
            return None
        return self.ConfigurationDict[parameter]

    def set(self, param, value):
        'Add/Change a configuration parameter'
        self.ConfigurationDict[param] = value
