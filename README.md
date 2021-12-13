# application_sender

## How to run the code

Install python (version 3.9 and above) in order to run this.

Create a new environment (using [virtualenv](https://virtualenv.pypa.io/en/latest/) or [conda](https://docs.conda.io/en/latest/)) and activate it by doing
- virtualenv:
    ```
    . /<env_folder>/bin/activate
    ```
    where `<env_folder>` is the folder where you put your virtual environments.
- conda:
    ```
    conda activate <env>
    ```
    where `<env>` is the name of your environment

After activating the environment, install the requirements by running:
```
pip install -r requirements.txt
```

Now you can start a new application by running:
```
python send_app.py
```

**Note:** this script will generate and fill fake data into an application form, but it won't solve captchas. That's up to you, you have about 2 minutes to solve a captcha, otherwise it will timeout.