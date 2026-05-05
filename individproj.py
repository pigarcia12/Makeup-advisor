#Import tkinter for GUI
from tkinter import *
from collections import Counter
import os

#Create main window
root = Tk()
root.title("Makeup Advisor")
root.geometry("800x600")

#Variables to store user input
name_var = StringVar()
skin_var = StringVar()
occasion_var = StringVar()
time_var = StringVar()
exp_var = StringVar()
rating_var = StringVar()

#Sets default
skin_var.set("oily")
occasion_var.set("work")
time_var.set("quick")
exp_var.set("beginner")
rating_var.set("5")

#Stores session data
user_data = []

#Stores last generated profile
last_profile_data = {}

#Generates Makeup Plan
def generate_plan():
    name = name_var.get().strip()
    skin = skin_var.get().lower()
    occasion = occasion_var.get().lower()
    time = time_var.get().lower()
    exp = exp_var.get().lower()

    #Validation
    if "" in [name, skin, occasion, time, exp]:
        result_label.config(text="Please fill all fields")
        return

    #Makeup logic system
    base = {
        "oily": ("Matte foundation", 2),
        "dry": ("Hydrating foundation", 1),
        "normal": ("Balanced foundation", 2)
    }[skin]

    look = {
        "party": ("Full glam look", 3),
        "work": ("Natural look", 1),
        "casual": ("Soft everyday look", 2)
    }.get(occasion, ("Soft look", 2))

    routine = ("Quick routine", 1) if time == "quick" else ("Full routine", 3)

    tip = {
        "beginner": ("Keep it simple", 1),
        "intermediate": ("Try contour", 2),
        "advanced": ("Go bold with full glam", 3)
    }[exp]

    #Score calculation
    score = base[1] + look[1] + routine[1] + tip[1]

    #Profile decision
    if score <= 5:
        profile = "Natural look"
        extra = "Use BB cream, lip balm, mascara"
    elif score <= 8:
        profile = "Balanced"
        extra = "Add blush, eyeliner, soft lipstick"
    else:
        profile = "Full Glam"
        extra = "Contour, highlight, bold lips, eyeshadow"

    #Suggestions on products you can use
    products = {
        "oily": ["Oil-free primer", "Matte setting spray"],
        "dry": ["Hydrating primer", "Dewy setting spray"],
        "normal": ["Standard primer", "Light setting spray"]
    }[skin]

    #Final output
    result = f"""
{name}'s Makeup Profile → {profile}

Base: {base[0]}
Look: {look[0]}
Routine: {routine[0]}
Tip: {tip[0]}

Recommended Products:
- {products[0]}
- {products[1]}

User Rating: (enter rating below and click Submit Rating)
"""

    result_label.config(text=result)

    #Save to session
    global last_profile_data
    last_profile_data = {
        "name": name,
        "profile": profile,
        "skin": skin
    }

#Saves file
def save_to_file():
    if not user_data:
        result_label.config(text="No data to save")
        return

    with open("makeup_profiles.txt", "a") as f:
        for entry in user_data:
            f.write(str(entry) + "\n")

    result_label.config(text="Data saved successfully!")

#Shows history
def show_history():
    try:
        with open("makeup_profiles.txt", "r") as f:
            result_label.config(text=f.read())
    except FileNotFoundError:
        result_label.config(text="No saved data found")

#Shows analytics

def show_analytics():
    if not user_data:
        result_label.config(text="No data to analyze")
        return

    profiles = [d["profile"] for d in user_data]
    skins = [d["skin"] for d in user_data]
    ratings = [d["rating"] for d in user_data]

    profile_count = Counter(profiles)
    skin_count = Counter(skins)
    avg_rating = sum(ratings) / len(ratings)

    analysis = f"""
Analytics Report 

Most Common Profile: {profile_count.most_common(1)[0][0]}
Most Common Skin Type: {skin_count.most_common(1)[0][0]}

Average User Rating: {round(avg_rating, 2)}/5

Profile Distribution:
{profile_count}
"""

    result_label.config(text=analysis)

#Clears users input
def clear_fields():
    name_var.set("")
    rating_var.set("5")
    result_label.config(text="Cleared!")

#NEW: Submits rating AFTER plan is generated
def submit_rating():
    global last_profile_data

    rating = rating_var.get()

    if not last_profile_data:
        result_label.config(text="Generate a plan first before rating")
        return

    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            raise ValueError
    except:
        result_label.config(text="Rating must be a number between 1 and 5")
        return

    #Add rating to stored data
    last_profile_data["rating"] = rating

    #Save into main data list
    user_data.append(last_profile_data.copy())

    result_label.config(text="Rating submitted successfully!")

#GUI Layout
Label(root, text="Name").grid(row=0, column=0)
Entry(root, textvariable=name_var).grid(row=0, column=1)

Label(root, text="Skin Type").grid(row=1, column=0)
OptionMenu(root, skin_var, "oily", "dry", "normal").grid(row=1, column=1)

Label(root, text="Occasion").grid(row=2, column=0)
OptionMenu(root, occasion_var, "work", "party", "casual").grid(row=2, column=1)

Label(root, text="Time Available").grid(row=3, column=0)
OptionMenu(root, time_var, "quick", "full").grid(row=3, column=1)

Label(root, text="Experience").grid(row=4, column=0)
OptionMenu(root, exp_var, "beginner", "intermediate", "advanced").grid(row=4, column=1)

Label(root, text="Rate Advice (1-5)").grid(row=5, column=0)
Entry(root, textvariable=rating_var).grid(row=5, column=1)

#Buttons for app
Button(root, text="Generate Plan", command=generate_plan).grid(row=6, column=1)
Button(root, text="Save Profile", command=save_to_file).grid(row=7, column=1)
Button(root, text="Show History", command=show_history).grid(row=8, column=1)
Button(root, text="Show Analytics", command=show_analytics).grid(row=9, column=1)
Button(root, text="Clear", command=clear_fields).grid(row=10, column=1)

#NEW button
Button(root, text="Submit Rating", command=submit_rating).grid(row=11, column=1)

#Output
result_label = Label(root, text="", fg="white", justify="left")
result_label.grid(row=12, columnspan=2)

#Runs the app
root.mainloop()