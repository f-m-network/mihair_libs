import requests
import json

api_url = 'http://mihair.herokuapp.com/api'
api_name = '/subscribers'
token = '227d860c6af94bac7cd79beea2fa8cea3390a745fdcf1d4f'

print '\n\nShoot it here!\n\n'
data = json.dumps({
      "subscriber": {
      "email":"vlad.janicek@gmail.com",
      "password":"password",
      "first_name":"Juan",
      "last_name":"Hernandez",
      "phone":"4242534177"
      }
    })

headers = {
    'Content-Type': 'application/json;charset=UTF-8'
}

print data
# Make sure the connection goes through, if not, raise excpt

rst = requests.post("{}{}?token={}".format(api_url,
                                       api_name,
                                       token),
                    data=data, headers=headers)
print rst
print rst.text
