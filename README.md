# Dailymotion Technical Test

## Run

1. First we need to build the docker container
`docker build . -t <your_favorite_container_name>`

#### E.q result:

```
[+] Building 3.1s (9/9) FINISHED
 => [internal] load build definition from Dockerfile                                                                                                                                                                               0.0s
 => => transferring dockerfile: 37B                                                                                                                                                                                                0.0s
 => [internal] load .dockerignore                                                                                                                                                                                                  0.0s
 => => transferring context: 2B                                                                                                                                                                                                    0.0s
 => [internal] load metadata for docker.io/library/python:3.9.6                                                                                                                                                                    1.1s
 => [1/4] FROM docker.io/library/python:3.9.6@sha256:2bd64896cf4ff75bf91a513358457ed09d890715d9aa6bb602323aedbee84d14                                                                                                              0.0s
 => [internal] load build context                                                                                                                                                                                                  0.3s
 => => transferring context: 1.21MB                                                                                                                                                                                                0.3s
 => CACHED [2/4] COPY ./requirements.txt .                                                                                                                                                                                         0.0s
 => CACHED [3/4] RUN python -m pip install --upgrade pip &&     pip install -r requirements.txt                                                                                                                                    0.0s
 => [4/4] COPY . .                                                                                                                                                                                                                 0.7s
 => exporting to image                                                                                                                                                                                                             0.8s
 => => exporting layers                                                                                                                                                                                                            0.8s
 => => writing image sha256:9195b7f247b54e3c63e4cc4c1c1962b3eab312b7d2a98f03d6ea89fba5239c45                                                                                                                                       0.0s
 => => naming to docker.io/library/daily-test
```
2. Then you can run the Container
`docker run -p <port:port> --rm <your_favorite_container_name>`

#### E.q result:
```docker run -p 8000:8000 --rm daily-test

Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
September 29, 2022 - 19:27:47
Django version 4.1.1, using settings 'daily.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
```

If everything went good, then you can use the following cURLS in order to do some call APIs.

## Tests by using cURLs

In order tu run the tests you can use the following command:
`python ./daily_project/manage.py test polls`

### Create a User

The response should be **200** and should contain User details like:
- `email` => <your@email>
- `status` => `created`
- `uuid` => "ji6wvntrxaOT2HG6N5ty" # e.q

Also, you must found his current **4 digit** which must be used in the next API call.

#### cURL
```
curl --location --request POST 'http://localhost:8000/polls/create_user' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": <your@email>,
    "password": <your_password>
}'
```

#### E.Q Response
```
{
    "collection": "users",
    "created_at": "2022-09-29T18:55:29.021Z",
    "updated_at": "2022-09-29T18:55:29.021Z",
    "uuid": "ji6wvntrxaOT2HG6N5ty",
    "email": "gabriel3@gmail.com",
    "is_verified": false,
    "status": "created",
    "code": 2417,
    "code_end_on": 1664477789.118678
}
```

### Check the 4 digit / Verify the User

Is should return you the current User with some updated details like:
- `status` => `active`
- `is_verified` => `True`

#### cURL
```
curl --location --request POST 'http://localhost:8000/polls/verify_user' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic <user:password>' \
--data-raw '{
    "digit_code": <digi_code>
}'
```

#### E.Q Response
```
{
    "collection": "users",
    "created_at": "2022-09-29T19:10:22.457",
    "updated_at": "2022-09-29T19:10:22.457",
    "uuid": "ji6wvntrxaOT2HG6N5ty",
    "email": "gabriel3@gmail.com",
    "is_verified": true,
    "status": "active",
    "code": 2861,
    "code_end_on": 1664478669.520461
}
```

### Refresh Digit Code

Just in case you are too slow to activate the user, you can use this endpoint to get a new **4 digit code**.

__PS: To be honest I used it several time because I was checking the data / logs (prints) etc.__
It'll return you a new **4 digit code**.

#### cURL
```
curl --location --request POST 'http://localhost:8000/polls/verify_user' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic <user:password>' \
--data-raw '{
    "digit_code": <digi_code>
}'
```

#### E.Q Response
```
{
    "digit_code": <4 digit code>
}
```


=======================================================================

Thank you.
```
⠀⠀⠀⠀⠀⠀⠀⢀⣤⠖⠛⠉⠉⠛⠶⣄⡤⠞⠻⠫⠙⠳⢤⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⠟⠁⠀⠀⠀⠀⠀⠀⠈⠀⢰⡆⠀⠀⠐⡄⠻⡄⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠦⠤⣤⣇⢀⢷⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡀⢈⡼⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠘⣆⢰⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⣼⠃⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠙⣎⢳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⠃⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⢳⣝⠳⣄⡀⠀⠀⠀⠀⠀⢀⡴⠟⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⢮⣉⣒⣖⣠⠴⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣀⣴⠶⠶⢦⣀⠀⠀⠀⠀⠀⠉⠁⠀⠀⠀⠀⢀⣠⣤⣤⣀⠀⠀⠀
⠀⢀⡾⠋⠀⠀⠀⠀⠉⠧⠶⠒⠛⠛⠛⠛⠓⠲⢤⣴⡟⠅⠀⠀⠈⠙⣦⠀
⠀⣾⠁⠀⠀⠀⠀⠀⠀⠀⣠⡄⠀⠀⠀⣀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠸⣇
⠀⣿⡀⠀⠀⠀⠀⠀⢀⡟⢁⣿⠀⢠⠎⢙⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣽
⠀⠈⢻⡇⠀⠀⠀⠀⣾⣧⣾⡃⠀⣾⣦⣾⠇⠀⠀⠀⠀⠀⠀⠀⠰⠀⣼⠇
⠀⢰⡟⠀⡤⠴⠦⣬⣿⣿⡏⠀⢰⣿⣿⡿⢀⡄⠤⣀⡀⠀⠀⠀⠰⢿⡁⠀
⠀⡞⠀⢸⣇⣄⣤⡏⠙⠛⢁⣴⡈⠻⠿⠃⢚⡀⠀⣨⣿⠀⠀⠀⠀⢸⡇⠀
⢰⡇⠀⠀⠈⠉⠁⠀⠀⠀⠀⠙⠁⠀⠀⠀⠈⠓⠲⠟⠋⠀⠀⠀⠀⢀⡇⠀
⠈⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠇⠀
⠀⢹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡄⠀
⠀⠀⠻⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣽⠋⣷⠀
⠀⠀⢰⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠃⠀⣿⡇
⠀⠀⢸⡯⠈⠛⢶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⠾⠋⠂⠀⠀⣿⠃
⠀⠀⠈⣷⣄⡛⢠⣈⠉⠛⠶⢶⣶⠶⠶⢶⡶⠾⠛⠉⠀⠀⠀⠁⢠⣠⡏⠀
⠀⠀⠀⠈⠳⣅⡺⠟⠀⣀⡶⠟⠁⠀⠀⠘⢷⡄⠀⠛⠻⠦⡄⢀⣒⡿⠀⠀
⠀⠀⠀⠀⠀⠈⠉⠉⠛⠁⠀⠀⠀⠀⠒⠂⠀⠙⠶⢬⣀⣀⣤⡶⠟⠁⠀⠀
```⠀