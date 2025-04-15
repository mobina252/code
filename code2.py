def read_and_check_numbers():
    
    filename = "random_numbers.txt"
    
    try:
        
        with open(filename, 'r') as file:
            numbers = file.readlines()
        
        
        for line in numbers:
            number = int(line.strip())
            if number % 2 == 0:
                print(f"{number} : زوج")
            else:
                print(f"{number} : فرد")
    
    except FileNotFoundError:
        print(f" {filename} .")


read_and_check_numbers()