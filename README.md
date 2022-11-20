# Website + Authentication in Flask

## Set up & Installation

### 1 Clone/Fork the git repo and create an environment 
                    
**Windows**
          
```bash
git clone https://github.com/fedorovea/FlaskSite.git
cd FlaskSite
py -3 -m venv

```
          
**macOS/Linux**
          
```bash
git clone https://github.com/fedorovea/FlaskSite.git
cd FlaskSite
python3 -m venv

```

### 2 Activate the environment
          
**Windows** 

```venv\Scripts\activate```

```python -m pip install --upgrade pip```
          
**macOS/Linux**

```. venv/bin/activate```
or
```source venv/bin/activate```

```python3 -m pip install --upgrade pip```

### 3 Install the requirements

Applies for windows/macOS/Linux

```
cd FlaskSite
pip install -r requirements.txt
```
### 4 Migrate/Create a database

```python manage.py```

### 5 Run Project

**Windows**

```python routes.py runserver```

**macOS/Linux**

```python3 routes.py runserver```


Login           |  Register
:-------------------------:|:-------------------------:
![Sample](https://github.com/fedorovea/FlaskSite/blob/main/frontstatic/1.png)  |  ![Sample](https://github.com/fedorovea/FlaskSite/blob/main/frontstatic/4.png)</br>

Main page           |  Personal offers
:-------------------------:|:-------------------------:
![Sample](https://github.com/fedorovea/FlaskSite/blob/main/frontstatic/2.png)  |  ![Sample](https://github.com/fedorovea/FlaskSite/blob/main/frontstatic/3.png)</br>

