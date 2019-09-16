# Ask you friend to debug for you!

## Usage

- set up config file
```python
# config.py

# add your friends' email addresses over here
GOOD_PEOPLE = {
	'Max': 'max@gmail.com',
	'John': 'john@gmail.com',
	'Anny': 'anny@gmail.com'
}

```

- specify who would be the one to save your buggy code
```python
from helpme import ask_for_help
	
# send Max an email if this function raises error
@ask_for_help('Max')
def buggy_function(x):
	return 10 / x
	
# harrase Max with a DivisionByZero Error
buggy_function(0)
	
```


## Features on the way
1. Include argument values along with the source code  
2. Add regular reminders, if your friend doesn't reponse your email, send again!