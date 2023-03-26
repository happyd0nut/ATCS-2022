from models import *
from database import init_db, db_session
from datetime import datetime

class Twitter:
    
    def __init__(self):
        self.current_user = None
        self.logged_in = False
    
    """
    The menu to print once a user has logged in
    """

    def print_menu(self): # Works
        print("\nPlease select a menu option:")
        print("1. View Feed")
        print("2. View My Tweets")
        print("3. Search by Tag")
        print("4. Search by User")
        print("5. Tweet")
        print("6. Follow")
        print("7. Unfollow")
        print("0. Logout")
    
    """
    Prints the provided list of tweets.
    """
    def print_tweets(self, tweets):
        for tweet in tweets:
            print("==============================")
            print(tweet)
        print("==============================")

    """
    Should be run at the end of the program
    """
    def end(self): # Works
        print("Thanks for visiting!")
        db_session.remove()
    
    """
    Registers a new user. The user
    is guaranteed to be logged in after this function.
    """
    def register_user(self): # Works
        
        while True:
            handle = input("What will your handle be? \n")
            password = input("Enter a password: \n")
            re_password = input("Re-enter your password: \n")
            
            notValid = False
            userBook = db_session.query(User)
            for user in userBook:
                if user.username == handle:
                    notValid = True
                    break
            if notValid:
                print("That username is already taken. Try again. \n")
            elif password != re_password:
                print("Those passwords don't match. Try again. \n")
            else:
                db_session.add(User(handle, password))
                db_session.commit()
                self.current_user = handle
                self.logged_in = True
                print("Welcome " + self.current_user + "!")
                break

    """
    Logs the user in. The user
    is guaranteed to be logged in after this function.
    """
    def login(self): # Works
        while True:
            username = input("Username: ")
            password = input("Password: ")

            valid = False
            userBook = db_session.query(User)
            for user in userBook:
                if user.username == username:
                    valid = True
                    break
            if valid:
                login_user = db_session.query(User).where(User.username == username)
                if(login_user[0].password == password):
                    self.current_user = username
                    self.logged_in = True
                    print("Welcome " + self.current_user + "!")
                    break
                else:
                    print("Invalid username or password \n")
            else:
                print("Invalid username or password \n")
    
    def logout(self): # Works
        self.logged_in = False
        print("You successfully logged out")
        self.startup()

    """
    Allows the user to login,  
    register, or exit.
    """
    def startup(self): # Works
        while True:
            print("\nPlease select a Menu Option \n1. Login\n2. Register User\n3. Exit")
            selection = input("")
            if selection == "1":
                self.login()
                break
            elif selection == "2":
                self.register_user()
                break
            elif selection == "3":
                break
            else:
                print("Enter a valid selection:")

    def follow(self): # can follow only valid users? 

        toFollow = input("Who would you like to follow? \n")
        followList = db_session.query(Follower).where(Follower.follower_id == self.current_user)
        follow_yet = False
        for follower in followList:
            if follower.following_id == toFollow:
                print("You already follow " + toFollow)
                follow_yet = True
                break
        if  not follow_yet:
            db_session.add(Follower(self.current_user, toFollow))
            db_session.commit()
            print("You are now following " + toFollow)


    def unfollow(self): # works
        unfollow = input("Who would you like to unfollow? \n")
        followList = db_session.query(Follower).where(Follower.follower_id == self.current_user)
        unfollowed = False
        for follower in followList:
            print("I follow this person")
            if follower.following_id == unfollow:
                db_session.delete(follower)
                db_session.commit()
                unfollowed = True
                print("I unfollowed")
                break
        if not unfollowed:
            print("You don't follow" + unfollow)
        

    def tweet(self):
        content = input("Tweet Content: \n")
        cont_tags = input("Tags (tag separated with spaces):")

        db_session.add(Tweet(content, datetime.now(), self.current_user))
        db_session.commit()
        tweet_id = db_session.query(Tweet).where(Tweet.content == content)

        tagsList = cont_tags.split()
        # works until here
        # able to create tweet and store tweet_id
        # able to create a list of tags from tweet

        tagBook = db_session.query(Tag).all()
        print(tagBook)
        
        for tag in tagsList:
            if tag in tagBook: # if tag already exists
                print("yay!!!")
                tag_id = db_session.query(Tag).where(Tag.content == tag)[0].id
                # db_session.add(TweetTag(tweet_id, tag_id))
                # db_session.commit()
            else:
                print("new!!!")
                db_session.add(Tag(tag)) # create new tag
                db_session.commit() # do i need to commit each time or does flush work too?
                tag_id = db_session.query(Tag).where(Tag.content == tag)[0].id
                print(tag_id)
                db_session.add(TweetTag(tweet_id, tag_id))
                db_session.commit()
                print("committed!")
          
    
    def view_my_tweets(self):
        pass
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        pass

    def search_by_user(self):
        pass

    def search_by_tag(self):
        pass

    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()

        print("Welcome to ATCS Twitter!")
        self.startup()
        tagBook = db_session.query(Tag).all()
        print(tagBook)
        while self.logged_in:
            self.print_menu()
            print()
            option = int(input(""))

            if option == 1:
                self.view_feed()
            elif option == 2:
                self.view_my_tweets()
            elif option == 3:
                self.search_by_tag()
            elif option == 4:
                self.search_by_user()
            elif option == 5:
                self.tweet()
            elif option == 6: # follow
                self.follow()
            elif option == 7:
                self.unfollow()
            else:
                self.logout()
        
        self.end()
