import sys
import pathlib
import os
import json
from i2c_handler import I2C_Trinity
from rich.console import Console
from rich import print
from subprocess import check_output
from utils import *

i2c = I2C_Trinity(1)

class MainMenu:
    def __init__(self):
        self.console = Console()
        self.config_path = os.path.join(pathlib.Path(__file__).parent.resolve(),'config.json')
        self.load_config()

    def start(self):
        while(1):
            options_name = ["start_test", "setup_count", "setup_interval", "how_to_export_excel", "exit_program"]
            options_function = [self.start_test, self.setup_count, self.setup_interval, self.how_to, self.exit_program]

            os.system('clear')
            print(f"""  [bold green]Current Config[/bold green]
[bold cyan]Count[/bold cyan]          : [bold magenta]{self.count}[/bold magenta]
[bold cyan]Interval (sec)[/bold cyan] : [bold magenta]{self.interval}[/bold magenta]
            """)

            self.console.print("[bold]Menu options_name:[/bold]")
            for i, option in enumerate(options_name):
                self.console.print(f"  {i}. [cyan]{option}[/cyan]")
            user_option = self.get_user_choice(0, len(options_name) - 1)
            selected_function = options_function[user_option]
            selected_function()

    def get_user_choice(self, lower_bound=0, upper_bound=0, is_having_boundary=True):
        while True:
            try:
                if is_having_boundary:
                    prompt = f"Enter your choice ({lower_bound}-{upper_bound}): "
                else:
                    prompt = "Enter your choice: "

                choice = int(input(prompt))

                if not is_having_boundary or (lower_bound <= choice <= upper_bound):
                    return choice
                else:
                    print("[bold red]Invalid choice.[/bold red]")
            except ValueError:
                print("[red] Invalid input. Please enter a valid number. [/red]")

    def load_config(self):
        f = open(self.config_path)
        data_dict = json.loads(f.read())
        self.count = data_dict["count"]
        self.interval = data_dict["interval"] 

    def save_config(self, var_name, value):
        f = open(self.config_path)
        data_dict = json.loads(f.read())
        data_dict[var_name] = value

        with open(self.config_path, 'w') as f:
            json.dump(data_dict, f)

    def start_test(self):
        os.system('clear')
        print("[bold white] Re-Testing ? [/bold white]")
        print("[bold RED] 0 : No, this is the first test. [/bold RED]")
        print("[bold GREEN] 1 : Yes, I want to RETEST. [/bold GREEN]")
        chs = "Enter Your Choice : "
        ans = int(input(chs))
        if ans == 0 :
            os.system('clear')
            print("")
            print("**************** This is the first time calibration ****************")
            print("")
            group = str(get_datetime_n_sec()+ "-A")
            print("Group Name : " + group )
            print("")
            print("********************************************************************")
            i2c.start_test( self.count, self.interval, group)
        elif ans == 1 :
            os.system('clear')
            print("[green]==================================================[/green]")
            print("")
            print("[red] RRRRR EEEEE         TTTTT  EEEEE  SSSSSS  TTTTT[/red]")
            print("[red] R   R E               T    E      S         T  [/red]")
            print("[red] RRRRR EEEEE  ====     T    EEEEE  SSSSSS    T  [/red]")
            print("[red] R  R  E               T    E           S    T  [/red]")
            print("[red] R   R EEEEE           T    EEEEE  SSSSSS    T  [/red]")
            print("[red]==================================================[/red]")
            print("[red] Press '0' to exit to main Menu[/red]")
            print("[red] Press '1' to choose again [/red]")
            print("[red]==================================================[/red]")
            print("[green]==================================================[/green]")
            print("[yellow]==================================================[/yellow]")
            print("[green yellow]     Enter Group Name that you want to RETEST [/green yellow]")
            print("[yellow]==================================================[/yellow]")
            print("     Template : YYYY-MM-DD HH_MM")
            print("     Example  : 2024-03-08 19_01")
            print("[yellow]==================================================[/yellow]")
            regroup = "Enter Your Group Name --> "
            group = str(input(regroup) + "-B")
            if group == "0-B" :
                self.start()
            elif group == "1-B" :
                self.start_test()
            print("Group Name : " + group)
            i2c.start_test( self.count, self.interval, group)
            pass


    def setup_count(self):
        os.system('clear')
        print("[cyan]Enter the quantity of data points: [/cyan]")
        self.count = self.get_user_choice(is_having_boundary=False)
        self.save_config("count", self.count)
        self.start()

    def setup_interval(self):
        os.system('clear')
        print("[cyan]Enter the interval (in seconds) between each sensor data:[/cyan]")
        self.interval = self.get_user_choice(is_having_boundary=False)
        self.save_config("interval", self.interval)
        self.start()

    def how_to(self):
        try:
            ip_address = check_output(['hostname', '-I']).decode("utf-8").split()[0]
        except:
            ip_address = '192.168.0.244'
            print("[red] couldn't get a proper ip address.[/red]")
        
        os.system('clear')
        print('[green bold]Command[/green bold] : scp <remote_username>@<IPorHost>:<PathToFile> <LocalFileLocation>')

        print('''
              enter [italic green]ifconfig[/italic green] to check rpi ip (wlan0 inet)
              ''')

        print(f'[green cyan]sensirion eg.[/green cyan] scp trinity@{ip_address}:/home/trinity/senlog/excel/ss_log.xlsx C:\\Users')
        print(f'[green yellow]panasonic eg.[/green yellow] scp trinity@{ip_address}:/home/trinity/senlog/excel/pana_log.xlsx C:\\Users')

        print('''
              Press [italic bold green]Enter[/italic bold green] to go to main menu
              ''')
        input('')

    def exit_program(self):
        os.system('clear')
        print("[bold green]Goodbye![/bold green] \U0001F60A")
        sys.exit()

def main():
    main_menu = MainMenu()
    main_menu.start()

if __name__ == '__main__':
    main()
