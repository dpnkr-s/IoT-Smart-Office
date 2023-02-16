#!/usr/bin/env python
# -*- coding: utf-8 -*-

from array import *
import urllib2
import json

class pre:
	def __init__(self,ts):
		self.ts=ts
        
	def Monday(self):
		
			
			data =  {

					"Inputs": {

							"input1":
							{
								"ColumnNames": ["time"],
								"Values": [ [ self.ts ], [ "0" ], ]
							},        },
						"GlobalParameters": {
			}
				}

			body = str.encode(json.dumps(data))

			url = 'https://ussouthcentral.services.azureml.net/workspaces/5ac2e4bc0ef54ee28baf52a4459f7e89/services/5a9d2e3b32eb4ecfa162287dc37f26dc/execute?api-version=2.0&details=true'
			api_key = 'z7aUHS26TUJ28fcLXMjUE2KfSiqISQQmobkuajIc9gqkWyCaGNQMNrBa3ugLHKDJ33GyRpVa+FEOwslMyuxnBw==' # Replace this with the API key for the web service
			headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
			req = urllib2.Request(url, body, headers) 

			try:
				data = json.loads(urllib2.urlopen(req).read())
				result = data['Results'] #too deep?
				result1=result['output1']
				result2=result1['value']
				result3=result2['Values']
				predict= result3[1][2]
			
			except urllib2.HTTPError, error:
				print("The request failed with status code: " + str(error.code))
				# Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
				print(error.info())
				print(json.loads(error.read()))
			
			return predict

	def Tuesday(self):
		
		data =  {

				"Inputs": {

						"input1":
						{
							"ColumnNames": ["time"],
							"Values": [ [ self.ts ], [ "0" ], ]
						},        },
					"GlobalParameters": {
		}
			}

		body = str.encode(json.dumps(data))
		url = 'https://ussouthcentral.services.azureml.net/workspaces/5ac2e4bc0ef54ee28baf52a4459f7e89/services/cc2d5aafebe9413ebc197d93c50fafb4/execute?api-version=2.0&details=true'
		api_key = '9jjirbgu8SKMKYVmIo6x8iiW+1EojqJ4KQ3fobRSs3M4KULetH1/xFLHTcq1m5Y2jZmOOJ5hfAm1+Fg4G2yJXg==' # Replace this with the API key for the web service
		headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
		req = urllib2.Request(url, body, headers) 

		try:
			response = urllib2.urlopen(req)

			# If you are using Python 3+, replace urllib2 with urllib.request in the above code:
			# req = urllib.request.Request(url, body, headers) 
			# response = urllib.request.urlopen(req)

			data = json.loads(urllib2.urlopen(req).read())
 			result = data['Results'] #too deep?
			result1=result['output1']
			result2=result1['value']
			result3=result2['Values']
			predict= result3[1][2]
	 
		except urllib2.HTTPError, error:
			print("The request failed with status code: " + str(error.code))
			# Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
			print(error.info())
			print(json.loads(error.read()))
			
		return predict
	
	def Wednesday(self):
		
		data =  {

				"Inputs": {

						"input1":
						{
							"ColumnNames": ["time"],
							"Values": [ [ self.ts ], [ "0" ], ]
						},        },
					"GlobalParameters": {
		}
			}

		body = str.encode(json.dumps(data))

		url = 'https://ussouthcentral.services.azureml.net/workspaces/5ac2e4bc0ef54ee28baf52a4459f7e89/services/58053947bdff4d1598b1c77e9edd21c5/execute?api-version=2.0&details=true'
		api_key = '05kVF8MEDP9Rk9SZfBmP1kRPXiyEYFEi1a+J7JM5gh7/A/3QsfjC7JlQo/YgCfprlPiHJVTN+M2ntDBbXdAkZQ==' # Replace this with the API key for the web service
		headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
		req = urllib2.Request(url, body, headers) 

		try:
			response = urllib2.urlopen(req)

			# If you are using Python 3+, replace urllib2 with urllib.request in the above code:
			# req = urllib.request.Request(url, body, headers) 
		# response = urllib.request.urlopen(req)
			data = json.loads(urllib2.urlopen(req).read())
 			result = data['Results'] #too deep?
			result1=result['output1']
			result2=result1['value']
			result3=result2['Values']
			predict= result3[1][2]
			
	 
		except urllib2.HTTPError, error:
			print("The request failed with status code: " + str(error.code))
			# Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
			print(error.info())
			print(json.loads(error.read()))
		
		return predict
		
		
	def Thursday(self):	
		
		data =  {

				"Inputs": {

						"input1":
						{
							"ColumnNames": ["time"],
							"Values": [ [ self.ts ], [ "0" ], ]
						},        },
					"GlobalParameters": {
		}
			}

		body = str.encode(json.dumps(data))

		url = 'https://ussouthcentral.services.azureml.net/workspaces/5ac2e4bc0ef54ee28baf52a4459f7e89/services/43e39e454df1458dba9e8c3501ee7521/execute?api-version=2.0&details=true'
		api_key = 'B+1u6qjWV7viFyZ8s74gKHKSl87A9NLkVRuHZCYoWXTBbU/T8plyR+DyTPt/wNBLW7KkoKVPXp5zxi2zuBghKw==' # Replace this with the API key for the web service
		headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

		req = urllib2.Request(url, body, headers) 

		try:
			response = urllib2.urlopen(req)

    # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
    # req = urllib.request.Request(url, body, headers) 
    # response = urllib.request.urlopen(req)

			data = json.loads(urllib2.urlopen(req).read())
 			result = data['Results'] #too deep?
			result1=result['output1']
			result2=result1['value']
			result3=result2['Values']
			predict= result3[1][2]
			
	 
		except urllib2.HTTPError, error:
			print("The request failed with status code: " + str(error.code))
			# Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
			print(error.info())
			print(json.loads(error.read()))                 

		return predict

	def Friday(self):
		data =  {

				"Inputs": {

						"input1":
						{
							"ColumnNames": ["time"],
							"Values": [ [ self.ts ], [ "0" ], ]
						},        },
					"GlobalParameters": {
		}
			}

		body = str.encode(json.dumps(data))
		url = 'https://ussouthcentral.services.azureml.net/workspaces/5ac2e4bc0ef54ee28baf52a4459f7e89/services/d59adc6654b84b38b5ef00a56549abe0/execute?api-version=2.0&details=true'
		api_key = '2jzcatXsLVaccj1a2e++UTSFKghcx1Mt6CWRYJZJ3n4znwmjaPLn/QaKysDyp9MbT7eBBrCOvGkIITlQ6LCtFQ==' # Replace this with the API key for the web service
		headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
		req = urllib2.Request(url, body, headers) 

		try:
			response = urllib2.urlopen(req)
			data = json.loads(urllib2.urlopen(req).read())
 			result = data['Results'] #too deep?
			result1=result['output1']
			result2=result1['value']
			result3=result2['Values']
			predict= result3[1][2]
			
	 
		except urllib2.HTTPError, error:
			print("The request failed with status code: " + str(error.code))
			# Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
			print(error.info())
			print(json.loads(error.read()))
			
		return predict
