## Copyright 2020 Cedarville University

import requests


class Pyelethos:

	def __init__(self, token=None):
		self.ethostoken = token
		self.etherealtoken = self.ethosauthentication()

	def ethosauthentication(self, errcount=0):
		# Ethos API Login
		# POST https://integrate.elluciancloud.com/auth
		try:
			response = requests.post(
				url="https://integrate.elluciancloud.com/auth",
				headers={
					"Accept": "application/vnd.ellucian.v1+json",
					"Content-Type": "application/json",
					"Authorization": f"Bearer {self.ethostoken}",
				},
			)
			if response.status_code == 200:
				return response.text
			else:
				print('Response HTTP Status Code: {status_code}'.format(
					status_code=response.status_code))
				print('Response HTTP Response Body: {content}'.format(
					content=response.content))
		except requests.exceptions.RequestException:
			print('HTTP Request failed')

	def getopenterms(self, errcount=0):
		try:
			response = requests.get(
				url="https://integrate.elluciancloud.com/api/academic-periods",
				params={
					"criteria": "{\"registration\":\"open\"}",
				},
				headers={
					"Accept": "application/json",
					"Content-Type": "application/vnd.hedtech.applications.v16.1.0+json",
					"Authorization": f"Bearer {self.etherealtoken}",
					"Accept-Charset": "UTF-8",
				},
			)
			if response.status_code == 200:
				return response.json()
			elif response.status_code == 419 or response.status_code == 401:
				if errcount > 10:
					print(f'{errcount} 419 errors in getopenterms')
					return None
				else:
					errcount += 1
					self.etherealtoken = self.ethosauthentication()
					return self.getopenterms(errcount)
			else:
				print('getopenterms HTTP Status Code: {status_code}'.format(status_code=response.status_code))
				print('getopenterms HTTP Response Body: {content}'.format(content=response.content))
		except requests.exceptions.RequestException:
			print('getopenterms Request failed')
