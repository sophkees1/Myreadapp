import sys
import time
from datetime import date
from typing import Optional
from tabulate import tabulate
from collections import namedtuple
from tqdm import tqdm
from src.schema import StatusEnum, CreateDataType, FetchByIdDataType
from src.database import (
    insert_data,
    fetch_by_id,
    update_data,
    delete_row,
    truncate_table,
    view_table,
    count_completed_books,
    count_pending_books,
    search_books_by_title,
)


class MenuDisplay:
    """
    MENU
    -------
    1. DATA QUERY
        1. how many books were completely read in a specific amount of time
        2. how many books are pending
        3. search books by title
        77. Back to Menu
        99. Exit
    2. DATA MANIPULATION
        1. INSERT DATA
        2. UPDATE DATA
        3. DELETE DATA
        4. TRUNCATE
        77. Go back to menu
        99. Exit
    99. Exit
    """

    @staticmethod
    def display_menu():
        print(
            """\033[1;37m
            WELCOME TO MY READ APP
              
                MAIN MENU
            ------------------
            \033[1;34m1. DATA QUERY\033[0m
            \033[38;5;208m2. DATA MANIPULATION\033[0m
            \033[1;31m99. Quit\033[0m            
            """
        )

    @staticmethod
    def display_dm_menu():
        print(
            """\033[38;5;208m
            MENU > DATA MANIPULATION
            ------------------------
            1. INSERT DATA
            2. UPDATE DATA
            3. DELETE DATA
            4. TRUNCATE
            5. VIEW TABLE
            77. Back to Menu
            99. Quit\033[0m                         
            """
        )

    @staticmethod
    def display_dq_menu():
        print(
            """\033[1;34m
            MENU > DATA QUERY
            -----------------
            1. How many books were completely read during a specific amount of time?
            2. How many books do we have pending?
            3. Search books by title
            77. Back to Menu
            99. Quit\033[0m
            """
        )


class InputOption:
    @staticmethod
    def input_option_dm_insert() -> CreateDataType:
        # FIXME: Add login feature and extract the username from there.
        username = "Sophie"
        print("\033[1;37mPlease provide the following details: ")
        title: str = input("Book title: ")
        description: str = input("(Optional) Book description: ")
        status: StatusEnum = input(
            "(Optional) What is your current read status?(pending, reading, complete): "
        )
        pct_read: str = input("(Optional) What percentage read?: ")
        if pct_read:
            pct_read = int(pct_read)

        start_read_date: str = input("(Optional) Start reading date(YYYY-MM-DD): ")
        if start_read_date:
            start_read_date: date = date.fromisoformat(start_read_date)

        end_read_date: str = input("(Optional) End reading date(YYYY-MM-DD): \033[0m")
        if end_read_date:
            end_read_date: date = date.fromisoformat(end_read_date)

        return {
            "username": username,
            "title": title,
            "description": description if description else None,
            "status": status if status else StatusEnum.pending,
            "pct_read": pct_read if pct_read else 0,
            "start_read_date": start_read_date if start_read_date else None,
            "end_read_date": end_read_date if end_read_date else None,
        }

    @staticmethod
    def input_option_dm_update():
        global field_option
        while True:
            id_to_update = int(input("\033[1;37mInput book id to update: \033[0m"))
            book: Optional[FetchByIdDataType] = fetch_by_id(id_to_update)
            if book is None:
                print("\033[1;31m\nBook does not exist in DB. Please try again\033[0m")
                continue
            else:
                # display book info in a table
                print("\033[1;37m\nBook Information:")
                InputOption.generate_table(book)
                print(
                    """\033[1;37m
                    Fields to update:
                    ------------------
                    1. book title
                    2. book description
                    3. read status
                    4. percentage read
                    5. start date
                    6. end date
                    77. Back to Menu
                    99. Quit 
                    
                    """
                )
                field_option = int(input("Which field do you wish to update? \033[0m"))
                UpdatedInfo = namedtuple("UpdatedInfo", "book_id column value")
                if field_option == 1:
                    book_title = input("\033[1;32mEnter the new title: \033[0m")
                    updated_info = UpdatedInfo(
                        book_id=id_to_update, column="title", value=book_title
                    )
                    return updated_info
                elif field_option == 2:
                    new_desc = input("\033[1;32mEnter the new description: \033[0m")
                    updated_info = UpdatedInfo(
                        book_id=id_to_update, column="description", value=new_desc
                    )
                    return updated_info

                elif field_option == 3:
                    new_status = input("\033[1;32mEnter the new status: \033[0m")
                    updated_info = UpdatedInfo(
                        book_id=id_to_update, column="status", value=new_status
                    )
                    return updated_info

                elif field_option == 4:
                    new_pct = int(input("\033[1;32mEnter the new percentage: \033[0m"))
                    updated_info = UpdatedInfo(
                        book_id=id_to_update, column="pct_read", value=new_pct
                    )
                    return updated_info

                elif field_option == 5:
                    new_start = input(
                        "\033[1;32mEnter the new start date(YYYY-MM-DD): \033[0m"
                    )
                    updated_info = UpdatedInfo(
                        book_id=id_to_update, column="start_read_date", value=new_start
                    )
                    return updated_info

                elif field_option == 6:
                    new_end = input(
                        "\033[1;32mEnter the new end date(YYYY-MM-DD): \033[0m"
                    )
                    updated_info = UpdatedInfo(
                        book_id=id_to_update, column="end_read_date", value=new_end
                    )
                    return updated_info

                elif field_option == 77:
                    # GO BACK TO DM MENU
                    print("")
                    print("\033[1;32mLoading Data Manipulation Menu...\033[0m")
                    for i in tqdm(range(0, 100), total=100, ncols=100):
                        time.sleep(0.01)
                    break

                elif field_option == 99:
                    # EXIT THE PROGRAM
                    print("")
                    for i in tqdm(
                        range(0, 100),
                        total=100,
                        ncols=100,
                        desc="\033[1;31mEXITING THE PROGRAM...\033[0m",
                    ):
                        time.sleep(0.01)
                    sys.exit()

    @staticmethod
    def input_option_dm_delete():
        global d_option
        while True:
            id_to_delete = int(input("\033[1;37mInput book id to delete: \033[0m"))
            book: Optional[FetchByIdDataType] = fetch_by_id(id_to_delete)
            if book is None:
                print("\033[1;31mBook does not exist in DB. Please try again\033[0m")
                continue
            else:
                print("\033[1;37m\nBook Information:")
                InputOption.generate_table(book)
                print(
                    """\033[1;37m
                    Delete Options:
                    ---------------
                    1. Delete Row
                    77. Back to Menu
                    99. Exit 
                    
                    """
                )
                d_option = int(input("Choose an option to continue: \033[0m"))
                if d_option == 1:
                    return id_to_delete

                elif d_option == 77:
                    # GO BACK TO DM MENU
                    print("")
                    print("\033[1;32mLoading Data Manipulation Menu...\033[0m")
                    for i in tqdm(range(0, 100), total=100, ncols=100):
                        time.sleep(0.01)
                    break

                elif d_option == 99:
                    # EXIT THE PROGRAM
                    print("")
                    for i in tqdm(
                        range(0, 100),
                        total=100,
                        ncols=100,
                        desc="\033[1;31mEXITING THE PROGRAM...\033[0m",
                    ):
                        time.sleep(0.01)
                    sys.exit()

    @staticmethod
    def input_option_dm_truncate():
        global t_option
        while True:
            print("\033[1;37m\nTable Information:")
            InputOption.generate_full_table()
            print(
                """\033[1;37m
                  Truncate Options:
                  -----------------
                  1. Truncate Table (clear all rows)
                  77. Go back to Menu
                  99. Quit
                  
                """
            )
            t_option = int(input("Choose an option to continue: \033[0m"))
            if t_option == 1:
                option = input(
                    "\033[1;31mAre you sure? (This will delete all rows)(yes/no): \033[0m"
                )
                if option == "yes":
                    truncate_table()
                    print("\033[1;32mTable successfully truncated.\033[0m")
                    break
                elif option == "no":
                    continue

            elif t_option == 77:
                # GO BACK TO DM MENU
                print("")
                print("\033[1;32mLoading Data Manipulation Menu...\033[0m")
                for i in tqdm(range(0, 100), total=100, ncols=100):
                    time.sleep(0.01)
                break

            elif t_option == 99:
                # EXIT THE PROGRAM
                print("")
                for i in tqdm(
                    range(0, 100),
                    total=100,
                    ncols=100,
                    desc="\033[1;31mEXITING THE PROGRAM...\033[0m",
                ):
                    time.sleep(0.01)
                sys.exit()

            else:
                print("\033[1;31mInvalid input. Try again\033[0m")
                continue

    @staticmethod
    def generate_table(data):
        table = [
            [
                "Title",
                "Description",
                "Status",
                "Percentage read",
                "Start Date",
                "End Date",
            ],
            data,
        ]
        print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))

    @staticmethod
    def generate_full_table():
        view_table()


def main():
    while True:
        MenuDisplay.display_menu()
        option: int = int(input("\033[1;37mChoose an option to continue: \033[0m"))
        if option == 1:
            # OPERATION FOR QUERY
            print("")
            print("\033[1;32mLoading Data Query Menu...\033[0m")
            for i in tqdm(range(0, 100), total=100, ncols=100):
                time.sleep(0.02)
            while True:
                MenuDisplay.display_dq_menu()
                choice = int(input("\033[1;37mChoose an option to continue: \033[0m"))

                if choice == 1:
                    start_date = input(
                        "\033[1;37m\nEnter the start date (YYYY-MM-DD): \033[0m"
                    )
                    end_date = input(
                        "\033[1;37mEnter the end date (YYYY-MM-DD): \033[0m"
                    )
                    count = count_completed_books(start_date, end_date)
                    print(
                        f"\033[1;35m\nNumber of completely read books between {start_date} and {end_date}: {count}\033[0m"
                    )

                elif choice == 2:
                    count = count_pending_books()
                    print(
                        f"\033[1;35m\nWe currently have: {count} pending book(s).\033[0m"
                    )

                elif choice == 3:
                    title = input("\033[1;37m\nEnter the title keyword: \033[0m")
                    print(
                        f"\033[1;35m\nHere is the requested information based on keyword: {title}\033[0m\033[1;37m\n"
                    )
                    search_books_by_title(title)

                elif choice == 77:
                    # GO BACK TO MAIN MENU
                    print("")
                    print("\033[1;32mLoading Main Menu...\033[0m")
                    for i in tqdm(range(0, 100), total=100, ncols=100):
                        time.sleep(0.01)
                    break
                elif choice == 99:
                    # EXIT THE PROGRAM
                    print("")
                    for i in tqdm(
                        range(0, 100),
                        total=100,
                        ncols=100,
                        desc="\033[1;31mEXITING THE PROGRAM...\033[0m",
                    ):
                        time.sleep(0.01)
                    sys.exit()
                else:
                    print("\033[1;31m\nInvalid choice. Please try again.\033[0m")

        elif option == 2:
            # OPERATION FOR MANIPULATION
            print("")
            print("\033[1;32mLoading Data Manipulation Menu...\033[0m")
            for i in tqdm(range(0, 100), total=100, ncols=100):
                time.sleep(0.02)
            while True:
                MenuDisplay.display_dm_menu()
                option: int = int(
                    input("\033[1;37mChoose an option to continue: \033[0m")
                )
                # INSERT
                if option == 1:
                    data: CreateDataType = InputOption.input_option_dm_insert()
                    # insert data to the database
                    id = insert_data(data)

                # UPDATE
                elif option == 2:
                    updated_data = InputOption.input_option_dm_update()
                    # to return back to DM menu
                    if field_option == 77:
                        continue
                    # if option is not 77, keep going with updating data
                    updated_id = update_data(
                        updated_data.book_id, updated_data.column, updated_data.value
                    )
                    if updated_id is not None:
                        print(
                            f"\033[1;32mRecord with id {updated_id} updated successfully.\033[0m"
                        )
                    else:
                        print("\033[1;31mUpdate failed.\033[0m")

                # DELETE
                elif option == 3:
                    deleted_data = InputOption.input_option_dm_delete()
                    # to return back to DM menu
                    if d_option == 77:
                        continue
                    deleted_id = delete_row(deleted_data)
                    if deleted_id is not None:
                        print(
                            f"\033[1;32m\nRecord with id {deleted_id} deleted successfully.\033[0m"
                        )
                    else:
                        print("\033[1;31mDelete failed.\033[0m")

                # TRUNCATE
                elif option == 4:
                    InputOption.input_option_dm_truncate()

                elif option == 5:
                    InputOption.generate_full_table()

                elif option == 77:
                    # GO BACK TO MEIN MENU
                    print("")
                    print("\033[1;32mLoading Main Menu...\033[0m")
                    for i in tqdm(range(0, 100), total=100, ncols=100):
                        time.sleep(0.01)
                    break

                elif option == 99:
                    # EXIT THE PROGRAM
                    print("")
                    for i in tqdm(
                        range(0, 100),
                        total=100,
                        ncols=100,
                        desc="\033[1;31mEXITING THE PROGRAM...\033[0m",
                    ):
                        time.sleep(0.01)
                    sys.exit()

        elif option == 99:
            # EXIT THE PROGRAM
            print("")
            for i in tqdm(
                range(0, 100),
                total=100,
                ncols=100,
                desc="\033[1;31mEXITING THE PROGRAM...\033[0m",
            ):
                time.sleep(0.01)
            sys.exit()

        else:
            print("\033[1;31m\nOPTION NOT RECOGNIZED. PLEASE TRY AGAIN.\033[0m")


if __name__ == "__main__":
    main()
