# 452-Blockchain-Project
Implementation of a Blockchain in Python

What we still have to do:

  -Add a digital signature to each transaction to be added to the chain

  -Figure out our own Proof-of-Work problem to solve for originality

  -should support at least 3 users and three miners


Instructions:

  -install python3.6 -> https://askubuntu.com/questions/865554/how-do-i-install-python-3-6-using-apt-get?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa

   -install flask for python -> sudo apt-get install python3-flask

   -install python3-rsa -> sudo apt-get install python3-rsa

   -install an http client - I am using postman -> https://gist.github.com/SanderTheDragon/1331397932abaa1d6fbbf63baed5f043

Usage:

  -Generate keys by running 'python3.6 keygen.py "pubkeyfile.pem" "privkeyfile.pem" '

  -run an instance of the blockchain by typing 'python3.6 blockchain.py "privkeyfile.pem"'

  -run more virtual instances on different ports with pipenv:

        -pip install pipenv

        -pipenv --python=python3.6

        -pipenv install

        -pipenv run blockchain.py "privkeyfile.pem" -p 5000/5001/5002...
