# SauceHunter
A Telegram bot for reverse image searching using SauceNAO's API<br>Give it a try! https://t.me/SauceHunter_bot

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/Furglitch/SauceHunter.git
    ```
2. Navigate to the project directory:
    ```sh
    cd SauceHunter
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. Set up your SauceNAO API key and Telegram bot token in a `config.py` file:
    ```python
    from typing import Final
    token = 'your_telegram_bot_token'
    snao_key = 'your_saucenao_api_key'
    ```
2. Run the bot:
    ```sh
    python main.py
    ```
* Alternatively, you can use Docker to run the script. An example docker-compose file is provided and is what the bot is currently running on.

## License
This project is licensed under the GPL-3.0 License.