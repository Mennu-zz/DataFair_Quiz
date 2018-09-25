# Copyright 2018 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import json
import random
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler

speechConsCorrect = ['Booya', 'All righty', 'Bam', 'Bazinga', 'Bingo', 'Boom', 'Bravo', 'Cha Ching', 'Cheers', 'Dynomite', 'Hip hip hooray', 'Hurrah', 'Hurray', 'Huzzah', 'Oh dear.  Just kidding.  Hurray', 'Kaboom', 'Kaching', 'Oh snap', 'Phew','Righto', 'Way to go', 'Well done', 'Whee', 'Woo hoo', 'Yay', 'Wowza', 'Yowsa'] 
#27
speechConsWrong = ['Argh', 'Aw man', 'Blarg', 'Blast', 'Boo', 'Bummer', 'Darn', "D'oh", 'Dun dun dun', 'Eek', 'Honk', 'Le sigh', 'Mamma mia', 'Oh boy', 'Oh dear', 'Oof', 'Ouch', 'Ruh roh', 'Shucks', 'Uh oh', 'Wah wah', 'Whoops a daisy', 'Yikes'];
#23

class QuizSkill(MycroftSkill):
    def __init__(self):
        super(QuizSkill, self).__init__(name="QuizSkill")
        self.count = 1
        self.question = 0
        self.correct = 0
        self.questionId = 0
        self.prevquestion = 1
        with open('./data/quiz.json') as f:
            self.data = json.load(f)

    @intent_handler(IntentBuilder("").require("BoolAnswerKeyword"))
    def handle_bool_answer_intent(self, message):
        answer = message.data.get("BoolAnswerKeyword")


    @intent_handler(IntentBuilder("").require("NumberAnswerKeyword"))
    def handle_number_answer_intent(self, message):
        self.enclosure.deactivate_mouth_events()
        answer = message.data.get("NumberAnswerKeyword")
        if answer is self.last_question.answer :
            self.express = speechConsCorrect[random.randint(0,27)]
            self.correct += 1
        else :
            self.express = speechConsWrong[random.randint(0,23)]
        
        if self.count < 4:
            response = self._fetch_question(self)
            response["express"] = self.express
            response["prevanswer"] = response.prevquestion.answer
            response["totalcount"] = self.count - 1
            response["currentscore"] = self.correct
            response["count"] = self.count
            self.speak_dialog("question.quiz", data = response)
        else:
            self.count = 1
            self.question = 0
            self.correct = 0
            self.questionId = 0
            self.prevquestion = 1
        self.enclosure.activate_mouth_events()
        self.enclosure.mouth_reset()


    def _fetch_question(self):
        self.count += 1
        self.rnum = random.randint(0,15)
        question = self._fetch_question(self)
        self.prevquestion = self.question
        options = ", ".join(str(x) for x in question["options"])
        response = {
            "question" : question,
            "options" : options,
            "prevquestion": self.prevquestion
        }
        return self.data[self.rnum]

    @intent_handler(IntentBuilder("") \
            .require("QuizKeyword"))
    def handle_start_quiz_intent(self, message):
        self.enclosure.deactivate_mouth_events()
        self.speak_dialog("start.quiz", data = response)
        self.enclosure.activate_mouth_events()
        self.enclosure.mouth_reset()
        company = message.data.get("Company")
        try:
            response = self.find_and_query(company)
            self.bus.once("recognizer_loop:audio_output_start",
                          self.enclosure.mouth_text(
                              response['symbol'] + ": " + response['price']))
            self.enclosure.deactivate_mouth_events()
            self.speak_dialog("stock.price", data=response)
            time.sleep(12)
            self.enclosure.activate_mouth_events()
            self.enclosure.mouth_reset()

        except Exception as e:
            self.log.exception(e)
            self.speak_dialog("not.found", data={'company': company})

    def stop(self):
        pass


def create_skill():
    return QuizSkill()
