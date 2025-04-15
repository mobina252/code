import random

def generate_random_numbers():
  
    filename = "random_numbers.txt"
    
    
    random_numbers = [random.randint(1, 100) for _ in range(100)]
    
    
    with open(filename, 'w') as file:
        for number in random_numbers:
            file.write(str(number) + '\n')
    
    print(f"  {filename} .")


generate_random_numbers()