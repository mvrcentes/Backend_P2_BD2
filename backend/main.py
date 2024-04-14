from crud import *

def main_menu():
    while True:
        print("\n=== Video Game Recommendation System ===")
        print("1. Search games by genre")
        print("2. Get game recommendations")
        print("3. Add a new game")
        print("4. Exit")
        
        choice = input("Select an option: ")
        
        if choice == "1":
            genre = input("Enter the genre to search for: ")
            result = find_games_by_genre(genre)
            for record in result:
                print(f"Name: {record['name']}, Platform: {record['platform']}, Release Year: {record['release_year']}")
                
        elif choice == "2":
            user_id = input("Enter your user ID: ")  # You might need to implement user authentication
            result = recommend_games_for_user(user_id)
            for record in result:
                print(f"Name: {record['name']}, Platform: {record['platform']}, Release Year: {record['release_year']}")
                
        elif choice == "3":
            game_properties = {
                "name": str,
                "platform": str,
                "release_year": int,
                "genres": list
            }
            game_data = request_data(game_properties)
            game_node = create_node(["Game"], **game_data)
            genre_nodes = []
            for genre in game_data["genres"]:
                genre_node = merge_node(["Genre"], name=genre)
                create_relation(game_node, "HAS_GENRE", genre_node)
                genre_nodes.append(genre_node)
                
        elif choice == "4":
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()