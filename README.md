# CamoFlask
## Kendrick Liang, Derek Song, Zane Wang, Wei Wen Zhou

#### Pay Day
A farming simulator in which the user can plant crops in a grid representing their farm, harvest them, and trade them with other people.

#### Instructions to Run
1. Clone our Repo:
    - To clone with SSH, enter ` git clone git@github.com:KendrickLiang/Softdev_Project02.git ` into terminal
2. Virtual Environment
    - Activate your python virtual environment if you already have one. If not, create one by entering
    - ` python3 -m venv <name-of-venv> `  
    - Enter ` . <path>/<name-of-venv>/bin/activate `  to activate.
3. Install Dependencies
    - ` pip install -r requirements.txt ` will install all necessary packages into your venv.
4. Insert API Keys into their respective files in the **double quotes after key** of each as shown:
    - For aWhere api you can enter at most 5 keys
  ```
        "key": "",
        "secret_key": "" <- only for aWhere.json
  ```
5. Launch with ` python app.py ` in terminal.
6. Open a new browser window and enter ` localhost:5000 ` into address bar to visit our home page.

#### Procuring API Keys
- aWhere API
    - Procure an API key [here](https://developer.awhere.com/). Click on the "Get Started" button. Email registration required.
    - This API can be used to provide information about the various crops that the player will be growing.
- accuWeather API
    - Procure an API key [here](https://developer.accuweather.com/). Email registration required.
    - API is used to access geographical data of a given location (i.e. city name)

[our video demo here](https://youtu.be/axMjSHhPbFs)
