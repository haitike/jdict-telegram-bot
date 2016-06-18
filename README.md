A simple japanese dictionary bot for telegram using the free EDICT dictionary written in Python 3.
It can be executed as a polling script or using a webhook (In my case openshift).

Instructions:
- Raname data/config-default.cfg to data/config.cfg
- Fill the token value (talk to BodFather in telegram).
- If you are going to use a webhook on telegram just fill the webhook_url with your openshift app url.

How to run:
- Webhook: Clone this repository as an openshift app, the app.py file is prepared for that.
- Polling: Execute main.py
