import os
from datetime import datetime

class Outputter:
    def __init__(self, output_folder):
        self.default_file_name = "proxies"
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)
    
    @staticmethod
    def _get_current_time():
        return datetime.now().strftime('%Y_%m_%d-%H_%M_%S')

    @staticmethod
    def _establish_filename(output_folder, current_time, filename):
        return os.path.join(output_folder, f"[{current_time}]_{filename}.txt")
    
    @staticmethod
    def _increment_file_name(file_path):
        name, ext = os.path.splitext(file_path)
        return f"{name}_1{ext}"
    
    def output_result(self, proxies):
        current_time = self._get_current_time()
        file_path = self._establish_filename(
            self.output_folder, 
            current_time, 
            self.default_file_name
        )

        counter = 1
        while os.path.exists(file_path):
            name, ext = os.path.splitext(file_path)
            file_path = f"{name[:-2] if name.endswith('_' + str(counter-1)) else name}_{counter}{ext}"
            counter += 1

        with open(file_path, "w", encoding="utf-8") as f:
            for proxy in proxies:
                f.write(f"{proxy}\n")

        return file_path

# Example usage
if __name__ == "__main__":
    o = Outputter(output_folder="results")
    result_file = o.output_result(["proxy1", "proxy2", "proxy3"])
    print(f"Proxies written to: {result_file}")