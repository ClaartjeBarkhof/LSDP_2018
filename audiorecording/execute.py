import time
from recorder import Recorder
import os, sys

class Question_Recorder(object):
    def __init__(self):
        self.check_folder('audiofiles')
        while True:
            username = input('Vul hier je naam in: ')
            self.userfolder = 'audiofiles/' + username
            if username != '' and self.check_folder(self.userfolder):
                break
            else:
                print('Geef een unieke naam aub')


        self.questions = {}
        with open('questions.csv', 'r') as questioncsv:
            for index, value in enumerate(questioncsv):
                index += 1
                question, answer, qnum, qtype, _ = value.replace('"','').split(';')
                self.questions[index] = {'question': question,
                                         'answer': answer,
                                         'qnum': qnum,
                                         'qtype': qtype}
        print('Succesvol map aangemaakt!')

    def check_folder(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
            return True
        return False

    def perform_recording(self, filename):
        rec = Recorder(channels=1)
        with rec.open(self.userfolder + '/' + filename + '.wav', 'wb') as recfile:
            input('Druk op enter om te beginnen met opnemen')
            recfile.start_recording()
            print('Aan het opnemen!')
            input('Druk Enter om opnemen te stoppen')
            time.sleep(0.5)
            recfile.stop_recording()
            print('Opname opgeslagen')

    def perform_questions(self):
        for index in sorted(self.questions):
            qdict = self.questions[index]
            print('Vraagnummer: ', index, '/78')
            print('Te beantwoorden vraag: ', qdict['question'])
            if qdict['qtype'] == 'normaal':
                print('Antwoord met: ', qdict['answer'])
                self.perform_recording('norm_' + str(index))
            else:
                print('De chatbot begreep je niet goed!')
                print('Corrigeer deze met: ', qdict['answer'])
                self.perform_recording('corr_' + str(index))
                print('')


questions = Question_Recorder()
questions.perform_questions()
print('Dat was hem! Bedankt!')
