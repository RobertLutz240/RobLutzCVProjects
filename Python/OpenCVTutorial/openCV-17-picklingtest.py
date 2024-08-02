import os
import pickle

# The array to be pickled
colors = ['red', 'green', 'blue']

# Directory to save the pickle file
directory = 'C:/Users/nedm5/Desktop'

# Create the directory if it doesn't exist
os.makedirs(directory, exist_ok=True)

# Full path to the pickle file
file_path = os.path.join(directory, 'colors.pkl')

# Pickling the array
with open(file_path, 'wb') as file:
    pickle.dump(colors, file)

print(f"Array has been pickled successfully to {file_path}.")