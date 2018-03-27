"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import logging

from programy.clients.client import BotClient
from programy.config.sections.client.console import ConsoleConfiguration

import time
from recorder import Recorder
import os, sys

import speech_recognition as sr
from pyraat import PraatAnalysisFunction
from sys import platform
import subprocess


class ConsoleBotClient(BotClient):

    def __init__(self, argument_parser=None):
        self.running = True
        BotClient.__init__(self, "Console", argument_parser)

    def set_environment(self):
        self.bot.brain.properties.add_property("env", "Console")

    def get_client_configuration(self):
        return ConsoleConfiguration()

    def add_client_arguments(self, parser=None):
        return

    def parse_args(self, arguments, parsed_args):
        return

    def get_question(self, input_func=input):
        rec = Recorder(channels=1)
        question = input('>>> ')
        if question != '':
            return question
        with rec.open('test.wav', 'wb') as recfile:
            recfile.start_recording()
            print('Aan het opnemen!')
            input('Druk Enter om opnemen te stoppen')
            time.sleep(0.5)
            recfile.stop_recording()

        r = sr.Recognizer()
        with sr.AudioFile('test.wav') as source:
            audio = r.record(source)

        try:
            ask = r.recognize_google(audio, language='nl-NL')
            print('You asked: ' + ask)

            try:
                output = subprocess.check_output(["praat", "--run", "SingleAudioScript.praat", "test.wav"]).decode('utf')
            except:
                print('NOOOPE')

            # model = pickle.load(open('svm_best_model.p', 'rb'))
            # prediction = model.predict(output)
            # print("HIER KOMT DE OUTPUT")
            # print('output: ', output.decode('utf'))

#            praat_script.process_sound(audio)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        #ask = "%s " % self.bot.prompt
        return ask

    def display_startup_messages(self):
        self.display_response(self.bot.get_version_string)
        self.display_response(self.bot.brain.post_process_response(self.bot, self.clientid,
                                                                   self.bot.get_initial_question(self.clientid)))

    def display_response(self, response, output_func=print):
        output_func(response)

    def process_question_answer(self):
        question = self.get_question()

        if question[-1]=='?':
            question = question[:-1]

        response = self.bot.ask_question(self.clientid, question, responselogger=self)

        if response[-2]==" ":
            response = response[:-2]+"."
        self.display_response(response)
        return question

    def run(self):
        if self.arguments.noloop is False:
            if logging.getLogger().isEnabledFor(logging.INFO):
                logging.info("Entering conversation loop...")
            self.running = True

            self.display_startup_messages()

            while self.running is True:
                try:
                    self.process_question_answer()
                except KeyboardInterrupt as keye:
                    self.running = False
                    self.display_response(self.bot.get_exit_response(self.clientid))
                except Exception as excep:
                    logging.exception(excep)
                    if logging.getLogger().isEnabledFor(logging.ERROR):
                        logging.error("Oops something bad happened !")
        else:
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("noloop set to True, exiting...")


if __name__ == '__main__':

    def run():
        print("Loading, please wait...")
        console_app = ConsoleBotClient()
        console_app.run()

    run()
