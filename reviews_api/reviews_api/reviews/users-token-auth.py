'''
curl -X POST -d "username=admin&password=adminadmin" http://127.0.0.1:8000/api/auth/token/
ex.:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwidXNlcl9pZCI6MywiZW1haWwiOiIiLCJleHAiOjE1MTI0MTk4ODh9.gQEPLnnPwBbZ_xUYzaat4tbzxOVK2GmNWVwbP33okiU
curl -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwidXNlcl9pZCI6MywiZW1haWwiOiIiLCJleHAiOjE1MTI0MTk4ODh9.gQEPLnnPwBbZ_xUYzaat4tbzxOVK2GmNWVwbP33okiU
" http://127.0.0.1:8000/reviews/
curl http://127.0.0.1:8000/reviews/
http POST 127.0.0.1:8000/api-token-auth/ username='admin2' password='fL20363601'


http://127.0.0.1:8000/reviews -H Authorization : Token
'''