# Copyright 2019 Aditya Mehra (aix.m@outlook.com).
#
# Licensed under the General Public License, Version 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.gnu.org/licenses/gpl-3.0.en.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import binascii

from mycroft.messagebus.message import Message
from mycroft.skills.core import MycroftSkill
from mycroft.util import get_ipc_directory
from mycroft.util.log import LOG
from mycroft.util.parse import normalize
from mycroft import intent_file_handler

import os
import subprocess


class RemoteSTT(MycroftSkill):
    """
        The skill handles remote STT related activites for wav based Client 
        implementation in Mycroft Core
    """
    def __init__(self):
        super().__init__('RemoteSTT')

    def initialize(self):
        """
            Registers messagebus handlers
        """
        try:
            self.add_event('recognizer_loop:incoming_aud', self.create_audio)
            
        except Exception:
            LOG.exception('In RemoteSTT Skill')
        
    def create_audio(self, message):
        """ 
            Read raw audio on messagebus and
            convert to usable wav file
        """
        self.bus.emit(Message('recognizer_loop:record_end'))
        LOG.info("Remote STT Recv")
        rawaudio = message.data["audio"]
        binary_string = binascii.unhexlify(rawaudio)
        newFile = open("/tmp/mycroft_stt.raw", "wb")
        newFile.write(binary_string)
        subprocess.call(["sox","-r","8000", "-t", "sw", "-e", "unsigned", "-c", "1", "-b", "8", "/tmp/mycroft_stt.raw", "/tmp/mycroft_in.wav"])
    
    
def create_skill():
    return RemoteSTT()
