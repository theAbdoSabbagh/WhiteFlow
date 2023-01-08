from time import sleep
from random import choice
from typing import Union, Optional
from time import time
from threading import Thread
from os import system
from rich import print
from toml import loads
from DankCord.objects import Message, Button, Dropdown
from DankCord import Client, Config
from pyloggor import pyloggor

from internal.objects import (
    Settings,
    NormalOptions,
    PowerupOptions,
    ButtonOptions,
    Option,
    Cooldowns
)

class Bot(Client):
    """The WhiteFlow bot. Has some functions, while inheriting from the `Client` class
    from the `DankCord` module."""

    def __init__(self, config: Config, logger: pyloggor):
        super().__init__(config, logger)
        self.queue: list = []
        """All threads that will execute a command append the command name to this list, then wait until their command is the first in the list,
        which indicates that it's their turn to run. Once the command finishes, it is removed from the list,
        allowing other threads to run as well when it's their turn."""
        self.checked_message_id: int = 0
        """The message ID that will be used to match to whatever message is sent to the function `__interaction_end_check()`
        when using the `wait_for` function and setting the first function as the check."""
        self._postmemes_ban_time: float = 0
        """The bot checks if the current time value is higher than this variable, and if it is, it runs the command.
        Whenever the bot is notified that it can't run the command for the next 5 minutes, it assigns the current time
        of that ban + 5 minutes and 30 seconds - the 30 seconds is for safety."""
        self._profile_message: Optional[Message] = None
        """This holds the Message object a message that has the user profile from the /profile command."""
        with open("config.toml", "r+", encoding="utf-8") as configfile:
            self.settings = Settings(loads(configfile.read()))
            """The settings set by the user, but of the type `Settings`."""
        with open("cooldowns.toml", "r+", encoding="utf-8") as configfile:
            self.cooldowns = Cooldowns(loads(configfile.read()))
            """The cooldowns set by the user, but of the type `Cooldowns`."""
        Thread(target=self._live_config, daemon=True).start()
        # Thread(target=self._queue_announcer, daemon=True).start() use for debugging only

    def _live_config(self):
        """Used for live config."""
        while True:
            with open("config.toml", "r+", encoding="utf-8") as configfile:
                self.settings = Settings(loads(configfile.read()))
            with open("cooldowns.toml", "r+", encoding="utf-8") as configfile:
                self.cooldowns = Cooldowns(loads(configfile.read()))
            self.channel_id = self.settings.credentials.channel_id
            sleep(0.25)

    def _queue_announcer(self):
        """This is for debug purposes only."""
        while True:
            print(self.queue)
            system('clear')
    
    def _interaction_end_check(self, message: Message):
        """This function is meant to be used in `wait_for()` as a check for when it is needed to wait for the interaction to end.
        
        Parameters
        ----------
        message: Message
            The message object to check
        
        Returns
        ----------
        bool
            Whether the check was successful or not.
        """
        return all([button.disabled for button in message.buttons]) and message.id is not None and message.id == self.checked_message_id

    def _start_cmd(self, cmd: Option):
        """A function for running a command indefinitely whenever the cooldown is over;
        supports clicking buttons.
        
        Parameters
        -----------
        cmd: Option
            The command to start running.
        """
        father: Union[NormalOptions, ButtonOptions, PowerupOptions]
        name = cmd.name
        command = None
        while True:
            for father in self.settings.options.types:
                for child in father.commands:
                    if child.name == name:
                        command = cmd
                        break

            if not command.state:
                sleep(2.5)
                continue

            cooldown = self.cooldowns.premium.raw[command.name] \
            if self.settings.miscellaneous.premium \
            else self.cooldowns.normal.raw[command.name]

            self.queue.append(command.name)

            while self.queue[0] != command.name:
                continue
            sleep(0.25)

            message: Message = self.run_command(
                command.name,
                retry_attempts = 5,
                timeout = 3
            )
            if command.button_count and message is not None:
                button: Button = choice(message.buttons)
                success_state = self.click(button, retry_attempts = 5, timeout = 3)
                if not success_state:
                    # Wait for interaction to end
                    self.checked_message_id = message.id
                    print(f"[bold red][ Debug - {command.name} ][/] Waiting for interaction to finish.")
                    updatedMessage: Message = self.wait_for('MESSAGE_UPDATE', check = self._interaction_end_check, timeout = 35)
                    if not updatedMessage:
                        print(f"[bold red][ Error - {command.name} ][/] Couldn't wait for the interaction to finish, did the interaction end?")
                    else:
                        print(f"[bold red][ Debug - {command.name} ][/] Interaction finished.")
                    self.checked_message_id = 0
                    self.queue.remove(command.name)
                    sleep(cooldown)
                    continue

            self.queue.remove(command.name)

            sleep(cooldown)
    
    def _post_memes(self):
        """A function for running the command `postmemes` indefinitely whenever the cooldown is over;
        supports choosing from DropDowns."""
        while True:
            if (not self.settings.options.other.postmemes.state
            or time() < self._postmemes_ban_time):
                sleep(2.5)
                continue

            cooldown = self.cooldowns.premium.raw["postmemes"] \
            if self.settings.miscellaneous.premium \
            else self.cooldowns.normal.raw["postmemes"]
            self.queue.append("postmemes")

            while self.queue[0] != "postmemes":
                continue
            sleep(0.25)

            message: Message = self.run_command(
                "postmemes",
                retry_attempts = 5,
                timeout = 3
            )
            if not message:
                self.queue.remove("postmemes")
                continue
            self.checked_message_id = message.id
            
            platform_dropdown: Dropdown = message.dropdowns[0]
            memeType_dropdown: Dropdown = message.dropdowns[1]
            platform_option = [self.settings.miscellaneous.postmemes_platform] if self.settings.miscellaneous.postmemes_platform else [choice([option.value for option in platform_dropdown.options])]
            memeType_option = [self.settings.miscellaneous.postmemes_memeType] if self.settings.miscellaneous.postmemes_memeType else [choice([option.value for option in memeType_dropdown.options])]
            success_state = self.select(
                platform_dropdown, 
                platform_option,
                retry_attempts = 5,
                timeout = 3
            )
            if not success_state:
                # Wait for interaction to end
                print(f"[bold red][ Debug - postmemes ][/] Waiting for interaction to finish.")
                updatedMessage: Message = self.wait_for('MESSAGE_UPDATE', check = self._interaction_end_check, timeout = 35)
                if not updatedMessage:
                    print(f"[bold red][ Error - postmemes ][/] Couldn't wait for the interaction to finish, did the interaction end?")
                else:
                    print(f"[bold red][ Debug - postmemes ][/] Interaction finished.")
                self.checked_message_id = 0
                self.queue.remove("postmemes")
                sleep(cooldown)
                continue

            sleep(0.1)
            success_state = self.select(
                memeType_dropdown, 
                memeType_option,
                retry_attempts = 5,
                timeout = 3
            )
            if not success_state:
                # Wait for interaction to end
                print(f"[bold red][ Debug - postmemes ][/] Waiting for interaction to finish.")
                updatedMessage: Message = self.wait_for('MESSAGE_UPDATE', check = self._interaction_end_check, timeout = 35)
                if not updatedMessage:
                    print(f"[bold red][ Error - postmemes ][/] Couldn't wait for the interaction to finish, did the interaction end?")
                else:
                    print(f"[bold red][ Debug - postmemes ][/] Interaction finished.")
                self.checked_message_id = 0
                self.queue.remove("postmemes")
                sleep(cooldown)
                continue

            sleep(0.1)
            success_state = self.click(
                message.buttons[0],
                retry_attempts = 5,
                timeout = 3
            )
            if not success_state:
                # Wait for interaction to end
                print(f"[bold red][ Debug - postmemes ][/] Waiting for interaction to finish.")
                updatedMessage: Message = self.wait_for('MESSAGE_UPDATE', check = self._interaction_end_check, timeout = 35)
                if not updatedMessage:
                    print(f"[bold red][ Error - postmemes ][/] Couldn't wait for the interaction to finish, did the interaction end?")
                else:
                    print(f"[bold red][ Debug - postmemes ][/] Interaction finished.")
                self.checked_message_id = 0
                self.queue.remove("postmemes")
                sleep(cooldown)
                continue
            
            updatedMessage: Message = self.wait_for('MESSAGE_UPDATE', check = self._interaction_end_check, timeout = 35)
            if updatedMessage is not None and "cannot post another meme" in updatedMessage.embeds[0].description:
                print(f"[bold red][ Debug - postmemes ][/] Sleeping for 5 minutes and 30 seconds - bot is banned from posting memes.")
                self._postmemes_ban_time = time() + 330

            self.queue.remove("postmemes")

            sleep(cooldown)

    def _auto_powerup(self, name: str):
        """A function for buying a certain powerup whenever it runs out.
        
        Parameters
        -----------
        name: str
            The name of the powerup to start buying whenever it runs out."""
        while True:
            powerup = [x for x in self.settings.options.powerup.commands if x.name.lower() == name.lower()][0]
            if not powerup.state:
                sleep(2.5)
                continue

            cooldown = self.cooldowns.premium.raw[powerup.name] \
            if self.settings.miscellaneous.premium \
            else self.cooldowns.normal.raw[powerup.name]

            self.queue.append(powerup.name)

            while self.queue[0] != powerup.name:
                continue
            sleep(0.25)

            message: Message = self.run_command(
                "use",
                retry_attempts = 5,
                timeout = 3,
                item = powerup.name
            )
            if powerup.button_count and message is not None:
                success_state = self.click(message.buttons[1], retry_attempts = 5, timeout = 3)
                if not success_state:
                    # Wait for interaction to end
                    self.checked_message_id = message.id
                    print(f"[bold red][ Debug - {powerup.name} ][/] Waiting for interaction to finish.")
                    updatedMessage: Message = self.wait_for('MESSAGE_UPDATE', check = self._interaction_end_check, timeout = 35)
                    if not updatedMessage:
                        print(f"[bold red][ Error - {powerup.name} ][/] Couldn't wait for the interaction to finish, did the interaction end?")
                    else:
                        print(f"[bold red][ Debug - {powerup.name} ][/] Interaction finished.")
                    self.checked_message_id = 0
                    self.queue.remove(powerup.name)
                    sleep(cooldown)
                    continue

            self.queue.remove(powerup.name)

            sleep(cooldown)


    def start_autofarming(self):
        """Begin the autofarming process."""
        father: Union[NormalOptions, ButtonOptions, PowerupOptions]
        for father in self.settings.options.types:
            for child in father.commands:
                if isinstance(father, PowerupOptions):
                    Thread(target = self._auto_powerup, args = [child], daemon = True).start()
                    sleep(0.15)
                    continue

                if child.name == 'postmemes':
                    Thread(target=self._post_memes, daemon=True).start()
                    sleep(0.15)
                    continue

                Thread(target=self._start_cmd, args=[child], daemon=True).start()
                sleep(0.15)
