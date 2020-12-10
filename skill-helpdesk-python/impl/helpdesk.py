#
# voice-skill-sdk
#
# (C) 2020, YOUR_NAME (YOUR COMPANY), Deutsche Telekom AG
#
# This file is distributed under the terms of the MIT license.
# For details see the file LICENSE in the top directory.
#
#
from skill_sdk import skill, Response  # , tell, ask
from skill_sdk.responses import tell, Card, Result
from skill_sdk.l10n import _

import re
import itertools
import random
import requests


@skill.intent_handler('TEAM_09_LAUNCH_INTENT')
def handler(sometext: str = None) -> Response:
    """ A handler for a voice based help desk service
    :return:        Response
    """

    # print("Search expression:" + sometext)

    # get result from service
    url = 'https://suudba32pj.execute-api.us-east-1.amazonaws.com/lookup?parameter=' + sometext
    response = requests.get(url, timeout=10)

    # We parse the response json or raise exception if unsuccessful
    response.raise_for_status()

    data = response.json()

    if len(data['filteredResult']) == 0:
        notFoundMsg = unspin(
            "{|Das tut mir leid.} Zu {diesem Begriff|diesem Thema|dieser Anfrage} habe ich {|leider }{keine Informationen|nichts} gefunden. {Deine Anfrage|Das Thema} wurde aber als {offene Frage|offener Punkt} zur Bearbeitung {markiert|vermerkt|gespeichert}. ")
        data = {
            "use_kit": {
                "kit_name": "audio_player",
                "action": "play_stream_before_text",
                "parameters": {
                    "url": "https://skillr2d2.s3-eu-west-1.amazonaws.com/" + randomDroidSound()
                }
            }
        }
        return Response(notFoundMsg, result=Result(data))

    # now we know for sure that we found something
    dataSet = data['filteredResult'][0]

    msg = dataSet['explanation']

    if "contactName" in dataSet:
        contactName = dataSet['contactName']
        msg = msg + " Erste Anlaufstelle: " + contactName + ". "

    if "contactData" in dataSet:
        contactData = dataSet['contactData']
        msg = msg + " Kontaktdaten: " + contactData + ". "

    # text for the card
    cardMsg = msg

    # text to be spoken
    msg = msg + " Diese Informationen findest Du auch in Deiner Hallo Magenta App. "

    informationUrl = ""
    if "informationUrl" in dataSet:
        informationUrl = dataSet['informationUrl']
        msg = msg + " inklusive einer weiterführenden Internetadresse. "
        cardMsg = cardMsg + unspin("Unter {der folgenden|dieser} Adresse findest Du weitere Informationen: ") + informationUrl

    # Unfortunately I learned that card support is currently broken.
    # But if it works again I'd love to use it to present additional information
    resultCard = Card(type_="GENERIC_DEFAULT",
                      title_text='Virtual Help Desk',
                      type_description='Du hast gesucht nach: ' + sometext,
                      text='Das habe ich gefunden',
                      sub_text=cardMsg,
                      #    action='internal://showResponseText', # TODO what is this about?
                      action_text='Full text of the response in an overlay'
                      # icon_url='http://images.linuxquestions.org/lqthumb.png'
                      )

    # We return the response
    return tell(msg, card=resultCard)


# A number of R2D2 droid sounds are waiting for usaaaaaaaaaaaaaawithin an S3 repository
# We select a random URL to be used in case of an error. This way the user might have
# a better experience in case his request cannot be
def randomDroidSound():
    randomNumber = unspin(
        "{01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31|32|33|35|36|37|38|39|40|41|42|43|44|45|46|47|48|49|50}")
    return "r2d2_short_" + randomNumber + ".mp3"


# Utility functions for Spintax evaluation follow
# using the expression 'unspin("{Hallo|Hallihallo|Servus}")'
# within the code we can make the skill behave more flexible
# Note that nested Spintax format is not supported
def optionList(fragment: str):
    if len(fragment) > 0 and fragment[0] == '{':
        return [option for option in fragment[1:-1].split('|')]
    return [fragment]


def makelist(flatSpintaxExpression: str):
    resultList = []
    regExpPattern = re.compile('(\{[^\}]+\}|[^\{\}]*)')
    fragments = regExpPattern.split(flatSpintaxExpression)
    optionLists = [optionList(fragment) for fragment in fragments]
    for item in itertools.product(*optionLists):
        resultList.append(''.join(item))
    return resultList


# return one random spintax representation
def unspin(flatSpintaxExpression: str):
    options = makelist(flatSpintaxExpression)
    random.shuffle(options)
    return options[0]
