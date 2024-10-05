# LLM Chatbot

## How to start?

First step, we need to install those runtimes/tools first:
- `python >= 3.10`
- `pip`
- `node >= 18`
- `yarn`

### Server

To install required packages, we use the command:

```
pip install -r requirements.txt
```

After that, we configure the environment variables:
- `GROQ_API_KEY` is used to invoke Groq API


Final step, use the following command to start the server:

```
fastapi run main.py
```

### User Interface

In the `ui/` directory, we use this command to install the dependencies of the UI

```
yarn install
```

After the installation process finished, we can launch the user interface by type:

```
yarn start
```
