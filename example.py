from dejavu import Dejavu
import warnings
import json
warnings.filterwarnings("ignore")

# load config from a JSON file (or anything outputting a python dictionary)
with open("dejavu/dejavu.cnf") as f:
    config = json.load(f)
    # f.close()
    print `config`

import unittest
from dejavu.recognize import FileRecognizer
from dejavu.recognize import MicrophoneRecognizer

djv = Dejavu(config)

if __name__ == '__main__':


    # Fingerprint all the mp3's in the directory we give it
    djv.fingerprint_directory("mp3", [".mp3"])

    class TestSequenceFunctions(unittest.TestCase):

        def setUp(self):
            self.timeToListenToMicrophone = 5 #in seconds
            self.fileName = "mp3/Sean-Fournier--Falling-For-You.mp3"
            self.song_name = self.fileName.rstrip(".mp3").lstrip("mp3/")
            self.djv = djv

        def test_fromFile(self):
            """Recognize audio from a file"""

            result = self.djv.recognize(FileRecognizer, self.fileName)

            # print "From file we recognized: %s\n" % result
            self.assertEqual(self.song_name, result['song_name'])

        def test_fromMicrophone(self):
            """recognize audio from your microphone for `timeToListenToMicrophone` seconds"""
            song = self.djv.recognize(MicrophoneRecognizer, seconds=self.timeToListenToMicrophone)
            self.assertTrue((not song) or (song['confidence']<10), "Nothing recognized -- did you play the song out loud so your mic could hear it? :)")
            print "From mic with %d seconds we recognized: %s\n" % (
                self.timeToListenToMicrophone, song)

        def testFileRecognizer(self):
            """Recognize audio from a file"""
            recognizer = FileRecognizer(self.djv)
            result = recognizer.recognize_file(self.fileName)

            self.assertEqual(self.song_name, result['song_name'])
            print "(w/o shortcut) we recognized: %s\n" % result['song_name']


    unittest.main()
