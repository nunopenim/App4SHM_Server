# App4SHM Initial Server Python Port
#
# Nuno Penim, Paulo Oliveira, 2021
#
# No tabs allowed for the safety of the entire project
# Use 4 spaces (I KNOW, BUT THAT'S HOW PYTHON ROLLS, I AM SORRY)
from app4shm.entities.data import Data

def main():
    data = Data("test", 11111, 0.0, 0.0, 0.0, "nuno")
    print(data.to_string())
    

if __name__ == '__main__':
    main()
