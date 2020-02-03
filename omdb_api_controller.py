import omdb_api_view as view
import omdb_api_view_2 as view2

if __name__ == '__main__':
    while True:
        try:
            response = int(input("Click 1 for version 1 gui or 2 for version 2 gui: "))
            if response == 1:
                view_obj = view.View()  # starts the gui
                break
            elif response == 2:
                view_obj = view2.ViewSecond()  # starts the gui
                break
        except:
            print("invalid input")
