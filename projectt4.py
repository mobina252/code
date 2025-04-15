def calculate_average_grades(filename):
    try:
        with open(filename, 'r') as file:
          
            lines = file.readlines()
        
     
        for line in lines:
            
            data = line.strip().split(',')
            name = data[0].strip()  #  
            grades = list(map(float, data[1:])) 
            
            if grades:   
                average = sum(grades) / len(grades)  # 
                print(f"{name}:  = {average:.2f}")
            else:
                print(f"{name}:  .")

    except FileNotFoundError:
        print(f" {filename} .")
    except Exception as e:
        print(f": {e}")


calculate_average_grades("grades.txt")