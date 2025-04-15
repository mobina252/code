def save_grades():

    filename = "grades.txt"
    

    num_students = int(input(" : "))
    
    
    grades = []
    
    for i in range(num_students):
        grade = input(f" {i + 1} : ")
        grades.append(grade)
    

    with open(filename, 'w') as file:
        for grade in grades:
            file.write(grade + '\n')
    
    print(f" {filename} .")


