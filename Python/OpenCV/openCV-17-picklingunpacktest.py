import pickle
import os

# Full path to the pickle file
file_path = os.path.join('C:/Users/nedm5/Desktop', 'colors.pkl')

# Unpickling the array
with open(file_path, 'rb') as file:
    colors = pickle.load(file)

print("Unpickled array:", colors)