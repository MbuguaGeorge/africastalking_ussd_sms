from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ussd_app.models import UserProfile
from django.conf import settings
import africastalking

# Create your views here

username = 'sandbox'
api_key = settings.AFRICSTALKING_API_KEY

africastalking.initialize(username, api_key)
sms = africastalking.SMS

@csrf_exempt
def ussd_callback(request):
    if request.method == 'POST':
        session_id = request.POST.get("sessionId", None)
        service_code = request.POST.get("serviceCode", None)
        phone_number = request.POST.get("phoneNumber", None)
        text = request.POST.get("text", "default")

        recipients = [phone_number]
        sender = '84672'

        response = ""
        name = None
        age = None
        street = None
        village = None
        group_no = None

        if text == '':
            response = "CON Karibu Daraja Microfinance \n"
            response += "1. Akaunti yangu \n"
            response += "2. Hisa"

        elif text == '1':
            response = "CON Akaunti yangu \n"
            response += "1. Fungua akaunti \n"
            response += "2. Angalia salio \n"
            response += "3. Mikopo yangu"

        elif text == '1*1':
            response = "CON Jina kamili"

        if (len(text) > 3):
            res = text.split('*')
            name = res[2]
        
        if (text == f'1*1*{name}'):
            response = "CON Umri"

        age_res = text.split('*')
        if (len(age_res) > 3):
            age = age_res[3]

        if (text == f'1*1*{name}*{age}'):
            response = "CON Mtaa/kijiji unachoishi"

        street_res = text.split('*')
        if (len(street_res) > 4):
            street = street_res[4]

        if (text == f'1*1*{name}*{age}*{street}'):
            response = "CON Kata unayoishi"

        village_res = text.split('*')
        if (len(village_res) > 5):
            village = village_res[5]

        if (text == f'1*1*{name}*{age}*{street}*{village}'):
            response = "CON Namba ya kikundi"

        group_res = text.split('*')
        if (len(group_res) > 6):
            group_no = group_res[6]

            response = "END Umefanikiwa kufungua akaunti na kujiunga na kikundi cha wamama wa CCM"

        if name is not None and street is not None and age is not None and village is not None and group_no is not None:
            user = UserProfile.objects.create(phone=phone_number)
            user.name = name
            user.age = age
            user.village = village
            user.street = street
            user.group_no = group_no

            user.save()

        if (text == '1*2'):
            response = "END Salio lako ni shilingi 4294527"

        elif (text == '1*3'):
            response = "CON Mikopo yangu \n"
            response += "1. Tujijenge group \n"
            response += "2. Wamama wa CCM"

        elif (text == '1*3*1'):
            response = "END Ndugu mteja unadaiwa tsh 230,000 na kikundi cha tujijenge group"
            message = "Ndugu mteja unadaiwa tsh 230,000 na kikundi cha tujijenge group"
            try:
                msg_response = sms.send(message, recipients, sender)
                print(msg_response)
            except Exception as e:
                print(f'{e}')

        elif (text == '1*3*2'):
            response = "END Ndugu mteja unadaiwa tsh 650,000 na kikundi cha wamama wa CCM"
            message = "Ndugu mteja unadaiwa tsh 650,000 na kikundi cha wamama wa CCM"
            try:
                msg_response = sms.send(message, recipients, sender)
                print(msg_response)
            except Exception as e:
                print(f'{e}')

        elif (text == '2'):
            response = "CON Hisa \n"
            response += "1. Tujijenge group \n"
            response += "2. Wamama wa CCM"

        elif (text == '2*1'):
            response = "CON Tujijenge group \n"
            response += "1. Angalia salio la hisa \n"
            response += "2. Nunua hisa \n"
            response += "3. Uza hisa"

        elif (text == '2*1*1'):
            response = "END  Ndugu mteja una kiasi cha hisa 120 kwenye kikundi cha tujijenge group zenye thamani ya sh 7500000"
            message = "Ndugu mteja una kiasi cha hisa 120 kwenye kikundi cha tujijenge group zenye thamani ya sh 7500000"
            try:
                msg_response = sms.send(message, recipients, sender)
                print(msg_response)
            except Exception as e:
                print(f'{e}')

        elif (text == '2*1*2'):
            response = "CON Kiasi cha hisa unazohitaji kununua \n"
            response += "Thibitisha kununua hisa 12 kwenye kikundi cha tujijenge group sawa na tsh 34000. Bonyeza 1 kuthibitisha au 2 kuahirisha"

        elif(text == '2*1*2*1'):
            message = "Ndugu mteja umenunua hisa"
            try:
                msg_response = sms.send(message, recipients, sender)
                print(msg_response)
            except Exception as e:
                print(f'{e}')

        elif (text == '2*1*3'):
            response = "CON Kiasi cha hisa unazotaka kuuza \n"
            response += "Thibitisha kutaka kuuza hisa 12 kwenye kikundi cha tujijenge group sawa na tsh 34000. Bonyeza 1 kuthibitisha au 2 kuahirisha"

        elif(text == '2*1*3*1'):
            message = "Ndugu mteja umenunua hisa"
            try:
                msg_response = sms.send(message, recipients, sender)
                print(msg_response)
            except Exception as e:
                print(f'{e}')

        elif (text == '2*2'):
            response = "END wamama wa CCM"

        return HttpResponse(response)