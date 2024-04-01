import smbus2
import time
import struct
import pathlib
from utils import *
from rich import print
from rich.pretty import pprint
from sqlite_dbcon import db_connect

model_require_data_dict = {"2": 1, "3": 0}

model_name_dict = {"2": "Panasonic SN-GCJA5", "3": "Sensirion SCD4x"}

model_filename_dict = {"2": "pana_log.xlsx", "3": "ss_log.xlsx"}

chart_config_dict = {
    "2": {
            "title": "Panasonic SN-GCJA5 Test Sample",
            "x_axis": "Test number",
            "y_axis": "PM 2.5 (µg/m³)",
         },
    "3": {
            "title": "Sensirion SCD40 Test Sample",
            "x_axis": "Test number",
            "y_axis": "CO2 (ppm)",
         },
}


class I2C_Trinity:
    def __init__(self, bus):
        self.bus = smbus2.SMBus(bus)

    def scan(self):
        devices = []
        for addr in range(0x03, 0x77 + 1):
            try:
                self.bus.read_byte(addr)
                devices.append(str(addr))
            except OSError as expt:
                if expt.errno == 16:
                    pass
        return devices

    def read_sensor(self, address):
        # Interface with sensor
        msg = smbus2.i2c_msg.read(int(address), 27)
        self.bus.i2c_rdwr(msg)

        # data management
        data = bytes(msg)
        data_size = data[0]
        """
        sensirion = Model 1
        Panasonic = Model 2
        """
        model_id = (data[1] << 8) + data[2]
        error_status = (data[5] << 24) + (data[6] << 16) + (data[7] << 8) + data[8]
        float_data_1 = struct.unpack("!f", bytes(data[11:15]))[0]
        float_data_2 = struct.unpack("!f", bytes(data[17:21]))[0]
        float_data_3 = struct.unpack("!f", bytes(data[23:27]))[0]
        return (
            data_size,
            model_id,
            error_status,
            [float_data_1, float_data_2, float_data_3],
        )
    
    def start_test(self, total_round, interval,group_name):
        devices = {}
        timestamp = []
        addresses = self.scan()
        #print(f"we found {addresses}")
        """
        Classifiy Sensor Type
        """
        for address in addresses:
            _, model_id, error_status, _ = self.read_sensor(address)
            model_id = str(model_id)
            if str(model_id) not in model_name_dict.keys():
                print("Unknow model ID")
                continue
            if address not in devices:
                devices[address] = {}
                devices[address]["data"] = []
            devices[address]["model_id"] = model_id
        # Organize addresses by model IDs
        addresses_by_model = {}
        for address, device_info in devices.items():
            model_id = device_info["model_id"]
            if model_id not in addresses_by_model:
                addresses_by_model[model_id] = []
            addresses_by_model[model_id].append(address)

        # Print the organized information
        for model_id, model_addresses in addresses_by_model.items():
            addresses_str = ", ".join(map(str, model_addresses))
            print(
                f"[green]{model_name_dict[model_id]}[/green] has addresses: [purple]{addresses_str}[purple]"
            )
        
        for cnt in range(total_round):
            print()
            print(" [bold white]Group Name : " + group_name + "[/bold white]")
            print(
                    f"[bold white] Round [/bold white] : [white]{cnt}[/white][green]/{total_round}[/green]"
                )

            print(f" [white]{get_human_datetime()}[/white]")
            print()
            timestamp.append(get_datetime())
            start_time = time.time()
            for address in addresses:
                try:
                    _, model_id, _, packet_data = self.read_sensor(address)
                    model_id = str(model_id)

                    targeted_data = packet_data[model_require_data_dict[model_id]]
                    devices[address]["data"].append(targeted_data)

                    # Print Sensor Data to Console  
                    # address is Processor Address [1 - N]  
                    # model_name_dict[model_id] is Sensor ModelType (Sensirion SCD4x or Panasonic SN-GCJA5)  
                    # targeted_data is value form sensor (CO2 for Sensirion SCD4x and PM2.5 for Panasonic SN-GCJA5)
                    print(
                        f"   [bold magenta]Address [/bold magenta] : [orchid]{address}[orchid], [bold light_coral]Type[/bold light_coral] : [salmon1]{model_name_dict[model_id]}[/salmon1], [bold cyan]Data[/bold cyan] : [blue]{targeted_data}[blue]"
                    )
                    #========================================================================================================================================================
                    # ADD Sensor Data to the MY-SQL DataBases
                    # When Start in Round add data to Databases
                    cal_con = db_connect()
                    cal_tab = "db_sde.sensor_income"
                    dt_string = get_datetime()
                    cal_val = "('"+str(group_name)+"','"+str(model_name_dict[model_id])+"','"+str(address)+"','"+str(targeted_data)+"','"+str(dt_string)+"','"+str(cnt)+"')"
                    cal_con.connect_sql_insert(cal_tab,cal_val)
                    #========================================================================================================================================================
                    # devices['datetime'].append(get_datetime())
                    #============================================================================================================================================
                    '''
                        Insert and Update Databases for collect test and re-test routine  
                    '''
                    group_con = db_connect()
                    group_tab = "db_sde.sensor_farformhome"
                    if str(group_name).endswith("A") :
                        companion = "-"
                        sensor_group = "('"+str(group_name)+"','"+str(model_name_dict[model_id])+"','"+str(dt_string)+"','"+str("")+"','"+str(companion)+"')"
                        group_con.connect_sql_insert(group_tab,sensor_group)
                    elif str(group_name).endswith("B") :
                        up_com = str(group_name[0:-2]) + "-A"
                        up_val = "companion_name = '"+str(group_name)+"'"
                        up_con = "group_name = '"+str(up_com)+"'"
                        group_con.connect_update(group_tab,up_val,up_con)
                    else :
                        companion = "Invalid Name"
                        up_val = "companion_name = '"+str(companion)+"'"
                        up_con = "group_name = '"+str(up_com)+"'"
                        group_con.connect_update(group_tab,up_val,up_con)
                    #============================================================================================================================================             
                except Exception as error:
                    devices[address]["data"].append(0)
                    print(
                        f"[red] Can't read data on address [/red] : [bold red]{address}[/bold red]"
                    )
                    print("An exception occurred:", error)

                time.sleep(0.1)

            while time.time() - start_time < interval:
                if cnt == (total_round - 1):
                    ''' 
                        Update Data timestamp when the test is done 
                    '''
                    group_con = db_connect()
                    group_tab = "db_sde.sensor_farformhome"
                    up_val = "stop_test = '"+str(dt_string)+"'"
                    up_con = "group_name = '"+str(group_name)+"'"
                    group_con.connect_update(group_tab,up_val,up_con)
                    break

        sensors_group = format_data_to_excel(devices, timestamp)

        for model_id in sensors_group.keys():
            file_name = os.path.join(
                pathlib.Path(__file__).parent.resolve(),
                "excel",
                model_filename_dict[model_id],
            )
            create_excel(
                file_name,
                sensors_group[model_id],
                total_round,
                chart_config_dict[model_id],
            )


if __name__ == "__main__":
    i2c_handler = I2C_Trinity(1)
    print(i2c_handler.scan())
