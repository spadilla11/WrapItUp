
import sqlite3
import os
from datetime import datetime
    
def welcome():
        print('''    
                
$$ |$$$\ $$ | $$$$$$\   $$$$$$\   $$$$$$\    $$ |  $$$$$$\   $$ |  $$ | $$$$$$\  
$$ $$ $$\$$ |$$  __$$\  \____$$\ $$  __$$\   $$ |  \_$$  _|  $$ |  $$ |$$  __$$\ 
$$$$  _$$$$ |$$ |  \__| $$$$$$$ |$$ /  $$ |  $$ |    $$ |    $$ |  $$ |$$ /  $$ |
$$$  / \$$$ |$$ |      $$  __$$ |$$ |  $$ |  $$ |    $$ |$$\ $$ |  $$ |$$ |  $$ |
$$  /   \$$ |$$ |      \$$$$$$$ |$$$$$$$  |$$$$$$\   \$$$$  |\$$$$$$  |$$$$$$$  |
\__/     \__|\__|       \_______|$$  ____/ \______|   \____/  \______/ $$  ____/ 
                                 $$ |                                  $$ |      
                                 $$ |                                  $$ |      
                                 \__|                                  \__|                 ''')
        print("Your best best gift idea program!")
    
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def user_input():
    while True:
        gender = input("Are they Male[M] or Female[F]? ").upper()
        if gender in ("M", "F"):
            age = input("Age: Child[C], Teen[T], Young-adult[Y], Adult[A]? ").upper()
            if age in ( "C", "T" , "Y", "A"):
                occasion = input("Ocassion: Birthday[B], Wedding[W], Holidays[H], Graduation[G] ").upper()
                if occasion in ("B", "W", "H", "G"):
                    interest = input("Interest: Pets[P], Sports[S], Music[M], Art[A], Cooking[C], Toys[T], Video-Games[V] ").upper()
                    if interest in ("P", "S", "M", "A", "C", "T", "V"):
                        return gender,age,occasion,interest
                    else:
                        print("Incorrect Input")
                else:
                    print("Incorrect Input")
            else:
                print("Incorrect Input")
        else:
            print("Incorrect Input")

def get_gift(gender,age,occasion,interest):
    conn = sqlite3.connect("mydb.db")  
    cursor = conn.cursor()

    cursor.execute(f"""
    SELECT gift_name FROM gift_idea
    WHERE gender LIKE '{gender}%' AND age LIKE '{age}%' AND occasion LIKE '{occasion}%' AND interest LIKE '{interest}%' """)

    results = cursor.fetchall()
    if len(results) > 0 : 
        gift_idea_list = [row[0] for row in results]
        return gift_idea_list
    else:
        return []

def save_user_info(name,gender,age,occasion,interest,):
    folder_name = "gift-getting_folder"
    if os.path.isdir(folder_name) == False:
        os.mkdir(folder_name)
    file_name = f"{name}-gift"
    with open(f"{folder_name}/{file_name}", 'w') as file:
        file.write(f"Name:{name} \nGender: {gender}\nAge: {age}\nOccasion: {occasion}\nInterest: {interest}\nAt {datetime.now()})")

def get_rating():
    print('''What would you like to rate the program?
1. Amazing
2. Could be better
3. Alright
4. Poor
5. Horrible''')
    user_rate = input("> ")
    with open ("user_rating.txt", "a") as file:
        file.write(f"{user_rate}\n")
        print("Rating saved!")
        
def read_file():
    who_2_view = input("Who do you want to view: ")
    folder_name = "gift-getting_folder"
    try:
        with open(f"{folder_name}/{who_2_view}-gift", 'r') as file:
            lines = file.readlines()
            for line in lines[6:]:
                print(line.strip())
            file.close()
    except FileNotFoundError:
        print("Person not found.")

def save_ideas(name,gift_list):
    which_ideas = input("Which ideas would you like to save? [Input the number idea separated by spaces]: ").split()
    folder_name = "gift-getting_folder"
    file_name = f"{name}-gift"
    with open(f"{folder_name}/{file_name}", 'a') as file:
        file.write(f"\nSaved ideas: \n")
        for idea in which_ideas:
            if idea.isdigit():
                num = int(idea) - 1
                if num >= 0 and num < len(gift_list):
                    file.write(f"-{gift_list[num]}\n")

def view_rating():
    total = 0
    count = 0
    print("Ratings:")
    with open("user_rating.txt", "r") as file:
        for rate in file:
            rating = int(rate.strip())
            print(rating)
            total += rating
            count += 1
    if count > 0:
        average = total / count
        print(f"\nAverage Rating: {average:.2f}\n")
    else:
        print("No ratings found.")
            

    

def main():
    welcome()
    print()
    while True:    
        user_choice = input ("Would you like to Find ideas[i] View Saved Ideas[vi], Rate[r], View Rating[vr], Quit[q]: ")
        
        if user_choice.lower() == "i":
            name = input("What is the recipieent's name? ")
            user = user_input()
            gift = get_gift(user[0],user[1],user[2],user[3])
            save_user_info(name, user[0], user[1], user[2], user[3])
            clear_screen()
            print()
            if len(gift) > 0:
                print(f"Here are some gift ideas for {name}!")
                for i,g in enumerate(gift, 1):
                    print(f"{i}. {g}")    
                    print() 
                save = input("Would you like to save any ideas? Yes[y] No[n] ")
                if save.lower() == "y":
                    save_ideas(name,gift)
                    print("Your ideas were saved!")
                elif save.lower() == "n":
                    print("Alright!\n")
                    
            else:
                print("No gift ideas")

        elif user_choice.lower() == "vi":
            read_file()
        
        elif user_choice.lower() == "r":
            get_rating()
        
        elif user_choice.lower() == "vr":
            view_rating()
            
        elif user_choice.lower() == "q":
            break
        else:
            print("Invalid Input.")



if __name__ == "__main__":
    main()


# when you choose a gift get a link
# aciiart
# clear screen
# Save gift

