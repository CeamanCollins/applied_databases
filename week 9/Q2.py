
# Main function
def main():
	# Initialise array
	# array = []

	display_menu()
	
	while True:
		choice = input("Enter choice: ")
		if (choice == "1"):
			array = fill_array()
			display_menu()
		elif (choice == "2"):
			print(array)
			display_menu()
		elif (choice == "3"):
			find_gt_in_array(array)
			display_menu()
		elif (choice == "4"):
			break;
		else:
			display_menu()
			
			
def fill_array():
	array = []
	user_input = 1
	while user_input!=-1:
		user_input = int(input('Enter Number: '))
		if user_input == -1:
			break
		else:
			array.append(user_input)
	return array

def find_gt_in_array(array):
	max = int(input('Enter Choice: '))
	print([i for i in array if i > max])

def display_menu():
    print("")
    print("MENU")
    print("=" * 4)
    print("1 - Fill Array")
    print("2 - Print Array")
    print("3 - Find > in Array")
    print("4 - Exit")

if __name__ == "__main__":
	# execute only if run as a script 
	main()
