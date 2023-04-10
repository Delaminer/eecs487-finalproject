
import pickle
import boto3
import boto3.session

ACCESS_KEY = "AKIATB4NJKW5HENP6TE7"
SECRET_KEY = "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"

s3client = boto3.client('s3', 
                        aws_access_key_id = ACCESS_KEY, 
                        aws_secret_access_key = SECRET_KEY
                       )

response = s3client.get_object(Bucket='eecs487-finalproject', Key='question_answer.pkl')

body = response['Body'].read()
data = pickle.loads(body)

print(data)