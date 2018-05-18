# 452-Secure-Blockchain-Project
Implementation of a Secure Blockchain in Python

Team Members: Alan Adame aadame4@csu.fullerton.edu Douglas Galm douglasgalm@csu.fullerton.edu Johnson Lien johnsonlien95@csu.fullerton.edu Michael Lindwall michaellindwall@csu.fullerton.edu

Team Collaboration: We all decided that blockchain was a cool new up-and-coming
technology that we heard about and wanted to know how it really works under the
hood.  We all began by reading up on the links given to us in the assignment,
and individually built the basic blockchain functionality and interface.  Once
we had the basics down, our next task was to implement extra security features.
Doug first tried to import our Assignment 3 RSA signer to use for signatures,
but he ran into difficulties with python2/3 compatibility issues.  Then Michael
tried a new RSA library made for python3 and added it to the project.  A
key generator tool was developed to generate RSA keypairs for use by the multiple
nodes.  Once the signatures were added, Johnson realized that identical transactions
create the same fingerprint when only signing the message as (sender, receiver, amount),
so he added a timestamp to the message to create a unique signature for duplicate
transactions.  After thorough testing by Alan, we decided that our project was
complete and ready for presentation.  

Instructions:

  -install python3.6

        https://askubuntu.com/questions/865554/how-do-i-install-python-3-6-using-apt-get?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa

   -install flask for python

        sudo apt-get install python3-flask
        pip install flask

   -install python3-rsa

        sudo apt-get install python3-rsa
        pip install rsa

   -install other requirements:

        pip install requests

   -install an http client - I am using postman

        https://gist.github.com/SanderTheDragon/1331397932abaa1d6fbbf63baed5f043

Usage:

  -Generate keys by running

        python3.6 keygen.py "pubkeyfile.pem" "privkeyfile.pem"

  -run an instance of the blockchain by typing

        python3.6 blockchain.py "privkeyfile.pem"

  -run more virtual instances on different ports with pipenv:

        pip install pipenv

        pipenv --python=python3.6

        pipenv install

        pipenv run blockchain.py "privkeyfile.pem" -p 5000/5001/5002...
